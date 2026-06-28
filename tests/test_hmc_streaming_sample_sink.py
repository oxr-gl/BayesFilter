from __future__ import annotations

import json
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import pytest
import tensorflow as tf

import bayesfilter
from bayesfilter.inference import (
    FixedSizeHMCChunkConfig,
    FixedSizeHMCChunkRunResult,
    HMCSampleArchiveManifest,
    HMCStreamingSampleArchiveSink,
    write_hmc_sample_archive,
)


def _config() -> FixedSizeHMCChunkConfig:
    return FixedSizeHMCChunkConfig(
        max_results=3,
        num_burnin_steps=1,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260624, 5),
        use_xla=False,
        target_scope="unit_hmc_streaming_sink",
    )


def _chunk(offset: float = 0.0) -> FixedSizeHMCChunkRunResult:
    samples = tf.constant(
        [
            [[0.1 + offset, 0.2], [0.3, 0.4]],
            [[0.5, 0.6], [0.7, 0.8]],
            [[0.0, 0.0], [0.0, 0.0]],
        ],
        dtype=tf.float64,
    )
    valid_mask = tf.constant([True, True, False])
    final_state = tf.constant([[0.5 + offset, 0.6], [0.7, 0.8]], dtype=tf.float64)
    diagnostics = {
        "valid_sample_count": tf.constant(2, dtype=tf.int32),
        "nonfinite_valid_sample_count": tf.constant(0, dtype=tf.int32),
        "native_divergence_status": "unavailable",
    }
    metadata = {
        "compile_trace_count": 1,
        "chunk_invocation_count": 1,
        "chunk_call_s": 0.25,
        "trace_policy": "reduced",
    }
    return FixedSizeHMCChunkRunResult(
        samples=samples,
        valid_mask=valid_mask,
        final_state=final_state,
        trace={"trace_collected": tf.constant(True)},
        diagnostics=diagnostics,
        metadata=metadata,
    )


def test_write_hmc_sample_archive_writes_private_shards_and_public_manifest(tmp_path):
    manifest = write_hmc_sample_archive(
        archive_dir=tmp_path / "samples",
        chunks=[_chunk(), _chunk(1.0)],
        config=_config(),
        archive_label="unit",
        metadata={"run_id": "unit-test"},
    )

    assert isinstance(manifest, HMCSampleArchiveManifest)
    payload = manifest.public_payload()
    assert payload["artifact_type"] == "bayesfilter_hmc_sample_archive_manifest"
    assert payload["chunk_count"] == 2
    assert payload["total_valid_sample_count"] == 4
    assert payload["total_nonfinite_valid_sample_count"] == 0
    assert payload["privacy_contract"]["archive_contains_private_raw_tensors"] is True
    assert payload["privacy_contract"]["public_manifest_contains_raw_values"] is False
    assert payload["metadata"] == {"run_id": "unit-test"}
    assert "manifest_core_sha256" in payload
    assert manifest.manifest_hash

    manifest_path = tmp_path / "samples" / "unit_manifest.json"
    assert manifest.manifest_path == str(manifest_path)
    on_disk = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert on_disk == payload

    chunk = payload["chunks"][0]
    for key in ("sample_path", "valid_mask_path", "final_state_path"):
        assert os.path.exists(chunk[key])
    assert chunk["sample_shape"] == [3, 2, 2]
    assert chunk["final_state_shape"] == [2, 2]
    assert chunk["sample_dtype"] == "float64"
    assert chunk["sample_sha256"]
    assert chunk["sample_bytes"] > 0

    text = json.dumps(payload)
    assert payload["privacy_contract"]["forbidden_public_payloads"] == [
        "raw_sample_values",
        "raw_state_values",
        "mass_matrices",
        "selected_kernel_payloads",
        "step_sizes",
        "leapfrog_counts",
    ]
    forbidden_keys = {
        "samples",
        "valid_mask",
        "final_state",
        "raw_sample_values",
        "raw_state_values",
        "mass_matrices",
        "selected_kernel_payloads",
        "step_sizes",
        "leapfrog_counts",
    }
    assert not any(key in chunk for chunk in payload["chunks"] for key in forbidden_keys)
    assert "\"samples\"" not in text
    assert "\"final_state\"" not in text


def test_hmc_streaming_sample_archive_sink_flushes_each_chunk_incrementally(tmp_path):
    sink = HMCStreamingSampleArchiveSink(
        archive_dir=tmp_path / "streamed",
        config=_config(),
        archive_label="unit_stream",
        metadata={"run_id": "stream-test"},
    )

    first_chunk = _chunk()
    first_payload = sink.write_chunk(first_chunk, chunk_index=0)

    assert sink.chunk_count == 1
    assert sink._chunk_payloads == [first_payload]
    assert not any(
        isinstance(item, FixedSizeHMCChunkRunResult)
        for item in sink._chunk_payloads
    )
    assert (tmp_path / "streamed" / "unit_stream_chunk_0000_samples.tftensor").exists()
    assert (tmp_path / "streamed" / "unit_stream_chunk_0000_valid_mask.tftensor").exists()
    assert (tmp_path / "streamed" / "unit_stream_chunk_0000_final_state.tftensor").exists()
    assert not (tmp_path / "streamed" / "unit_stream_manifest.json").exists()

    sink.write_chunk(_chunk(1.0), chunk_index=1)
    manifest = sink.finalize()
    payload = manifest.public_payload()

    assert payload["chunk_count"] == 2
    assert payload["total_valid_sample_count"] == 4
    assert payload["streaming_contract"] == {
        "incremental_write_before_next_chunk_supported": True,
        "sink_retains_chunk_tensors_after_write": False,
        "finalize_writes_manifest_only": True,
    }
    assert (tmp_path / "streamed" / "unit_stream_manifest.json").exists()

    with pytest.raises(RuntimeError, match="cannot write chunks after"):
        sink.write_chunk(_chunk(2.0), chunk_index=2)

    with pytest.raises(RuntimeError, match="already finalized"):
        sink.finalize()


def test_write_hmc_sample_archive_rejects_overwrite_and_bad_shapes(tmp_path):
    archive_dir = tmp_path / "samples"
    write_hmc_sample_archive(
        archive_dir=archive_dir,
        chunks=[_chunk()],
        config=_config(),
        archive_label="unit",
    )

    with pytest.raises(FileExistsError):
        write_hmc_sample_archive(
            archive_dir=archive_dir,
            chunks=[_chunk()],
            config=_config(),
            archive_label="unit",
        )

    bad_chunk = FixedSizeHMCChunkRunResult(
        samples=tf.zeros((2, 2, 2), dtype=tf.float64),
        valid_mask=tf.constant([True, False]),
        final_state=tf.zeros((2, 2), dtype=tf.float64),
        trace={},
        diagnostics={},
        metadata={},
    )
    with pytest.raises(ValueError, match="leading dimension"):
        write_hmc_sample_archive(
            archive_dir=tmp_path / "bad",
            chunks=[bad_chunk],
            config=_config(),
            archive_label="bad",
        )


def test_hmc_sample_archive_public_exports() -> None:
    assert bayesfilter.HMCSampleArchiveManifest is HMCSampleArchiveManifest
    assert bayesfilter.HMCStreamingSampleArchiveSink is HMCStreamingSampleArchiveSink
    assert bayesfilter.write_hmc_sample_archive is write_hmc_sample_archive
    assert "HMCSampleArchiveManifest" in bayesfilter.__all__
    assert "HMCStreamingSampleArchiveSink" in bayesfilter.__all__
    assert "write_hmc_sample_archive" in bayesfilter.__all__
