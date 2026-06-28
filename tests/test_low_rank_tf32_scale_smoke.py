from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import scalable_ot_low_rank_tf32_scale_smoke as smoke


def test_small_scale_smoke_writes_manifest_and_passes(tmp_path: Path) -> None:
    output = tmp_path / "small.json"
    markdown = tmp_path / "small.md"
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "small",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ]
    )
    result = smoke.build_result(args)
    output.write_text(json.dumps(smoke._json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    smoke.write_markdown(result, markdown)

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["status"] == "PASS"
    assert loaded["phase"] == "LR-TF32-1"
    assert loaded["hard_vetoes"] == []
    assert loaded["run_manifest"]["fixture_id"] == "bounded_smooth_v1"
    assert loaded["run_manifest"]["batch_size"] == 2
    assert loaded["run_manifest"]["state_dim"] == 4
    assert loaded["run_manifest"]["particle_counts"] == [32]
    assert loaded["run_manifest"]["rank"] == 8
    assert loaded["run_manifest"]["dtype"] == "float64"
    assert loaded["run_manifest"]["cuda_visible_devices"] == "-1"
    assert loaded["rows"][0]["dense_transport_materialized"] is True
    assert loaded["rows"][0]["dense_materialization_role"] == "tiny_invariant_only"
    assert loaded["summary"]["max_tiny_materialized_apply_parity"] <= smoke.TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD
    assert markdown.exists()


def test_fixture_contract_is_bounded() -> None:
    particles, log_weights = smoke._fixture_bounded_smooth(2, 32, 4, smoke.tf.float64)
    assert float(smoke.tf.reduce_max(smoke.tf.abs(particles)).numpy()) <= 1.0
    logits = log_weights - smoke.tf.reduce_mean(log_weights, axis=1, keepdims=True)
    assert float(smoke.tf.reduce_max(smoke.tf.abs(logits)).numpy()) <= 1.25 + 1.0e-12


def test_medium_defaults_preserve_no_dense_contract(tmp_path: Path) -> None:
    output = tmp_path / "medium.json"
    markdown = tmp_path / "medium.md"
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "medium-cpu",
            "--particle-counts",
            "64",
            "--batch-size",
            "2",
            "--state-dim",
            "4",
            "--rank",
            "8",
            "--dtype",
            "float32",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ]
    )
    result = smoke.build_result(args)
    assert result["rows"][0]["status"] in {"PASS", "FAIL"}
    assert result["rows"][0]["dense_transport_materialized"] is False
    assert result["rows"][0]["transport_matrix_shape"] == [2, 0, 0]
    assert result["run_manifest"]["device_scope"] == "cpu"
    assert result["run_manifest"]["dtype"] == "float32"
    assert result["rows"][0]["moment_threshold_role"] == "hard_veto"


def test_tuning_mode_records_grid_rows_without_dense_transport(tmp_path: Path) -> None:
    output = tmp_path / "tuning.json"
    markdown = tmp_path / "tuning.md"
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "tuning-cpu",
            "--particle-counts",
            "64",
            "--batch-size",
            "2",
            "--state-dim",
            "4",
            "--tuning-ranks",
            "4",
            "8",
            "--tuning-assignment-epsilons",
            "0.5",
            "0.25",
            "--dtype",
            "float32",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ]
    )
    result = smoke.build_result(args)
    assert result["phase"] == "LR-TF32-2A"
    assert len(result["rows"]) == 4
    assert all(row["dense_transport_materialized"] is False for row in result["rows"])
    assert all(row["grid_role"] == "tuning_candidate" for row in result["rows"])
    assert result["run_manifest"]["tuning_ranks"] == [4, 8]
    assert result["run_manifest"]["tuning_assignment_epsilons"] == [0.5, 0.25]
