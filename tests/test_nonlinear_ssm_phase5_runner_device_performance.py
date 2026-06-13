from __future__ import annotations

import json

import pytest

from bayesfilter.runtime import (
    CandidateResult,
    PartialResultSnapshot,
    WorkerRecord,
    append_heartbeat,
    append_stage_event,
    build_trusted_gpu_snapshot,
    build_worker_manifest,
    canonical_candidate_order,
    make_timing_bucket,
    record_timeout,
    record_worker_result,
    reduce_worker_artifacts,
    select_first_tie_candidate,
    select_preferred_gpu,
    stale_match_payload,
    stale_artifacts_match_exact,
    write_partial_result_snapshot,
    write_worker_manifest,
)


def _read_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_jsonl(path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _manifest(tmp_path, *, worker_id="w0", threads=2, program="phase5-toy"):
    config = {"target": "toy", "seed": 11, "candidate_parallel": {"workers": 8}}
    worker_config = {"candidate_index": 3, "step_size": 0.1, "leapfrog_steps": 4}
    return build_worker_manifest(
        worker_id=worker_id,
        command=("python", "-m", "toy_worker"),
        pid=1234,
        git_commit="abc123",
        artifact_root=tmp_path,
        normalized_config=config,
        program_signature=program,
        device_policy={"mode": "cpu_only", "CUDA_VISIBLE_DEVICES": "-1"},
        thread_caps={"OMP_NUM_THREADS": threads, "TF_NUM_INTRAOP_THREADS": threads},
        worker_config=worker_config,
        environment={"CUDA_VISIBLE_DEVICES": "-1"},
    )


def test_worker_manifest_stale_payload_includes_device_threads_and_worker_hash(tmp_path):
    manifest = _manifest(tmp_path)
    path = tmp_path / "worker_manifest.json"

    write_worker_manifest(path, manifest)
    payload = _read_json(path)

    stale_payload = payload["stale_match_payload"]
    assert stale_payload["normalized_config"]["target"] == "toy"
    assert stale_payload["program_signature"] == "phase5-toy"
    assert stale_payload["device_policy"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert stale_payload["thread_caps"]["OMP_NUM_THREADS"] == 2
    assert stale_payload["worker_config_hash"] == payload["worker_config_hash"]
    assert "not scientific evidence" in payload["nonclaims"][0]

    changed_threads = stale_match_payload(
        manifest.normalized_config,
        program_signature=manifest.program_signature,
        device_policy=manifest.device_policy,
        thread_caps={"OMP_NUM_THREADS": 4, "TF_NUM_INTRAOP_THREADS": 4},
        worker_config_hash=manifest.worker_config_hash,
    )
    assert stale_artifacts_match_exact(manifest.stale_match_payload, stale_payload)
    assert not stale_artifacts_match_exact(manifest.stale_match_payload, changed_threads)


def test_heartbeat_stage_events_and_partial_snapshot_survive_without_parent(tmp_path):
    events = tmp_path / "events.jsonl"
    partial = tmp_path / "partial.json"

    append_stage_event(
        events,
        stage="start",
        status="ok",
        timestamp="2026-06-08T00:00:00+08:00",
        payload={"worker_id": "w0"},
    )
    append_heartbeat(
        events,
        worker_id="w0",
        timestamp="2026-06-08T00:00:10+08:00",
        stage="hmc",
        payload={"draws_completed": 4},
    )
    write_partial_result_snapshot(
        partial,
        PartialResultSnapshot(
            worker_id="w0",
            stage="hmc",
            status="running",
            payload={"draws_completed": 4},
            nonfinite_count=0,
        ),
    )

    rows = _read_jsonl(events)
    snapshot = _read_json(partial)
    assert [row["status"] for row in rows] == ["ok", "heartbeat"]
    assert rows[1]["payload"]["draws_completed"] == 4
    assert snapshot["payload"]["draws_completed"] == 4
    assert "diagnostic evidence only" in snapshot["nonclaims"][0]


def test_reducer_classifies_complete_partial_stale_failed_and_timed_out(tmp_path):
    manifest = _manifest(tmp_path)
    expected = manifest.stale_match_payload

    complete_dir = tmp_path / "complete"
    complete_manifest = complete_dir / "manifest.json"
    complete_result = complete_dir / "result.json"
    write_worker_manifest(complete_manifest, manifest)
    record_worker_result(
        complete_result,
        WorkerRecord(
            "w0",
            ("python", "-m", "toy_worker"),
            manifest.config_hash,
            return_code=0,
            runtime_s=1.25,
            status="ok",
            device_policy=manifest.device_policy,
            thread_caps=manifest.thread_caps,
            worker_config_hash=manifest.worker_config_hash,
        ),
    )
    assert (
        reduce_worker_artifacts(
            worker_id="w0",
            expected_stale_payload=expected,
            manifest_path=complete_manifest,
            result_path=complete_result,
        ).status
        == "complete"
    )

    partial_dir = tmp_path / "partial"
    partial_manifest = partial_dir / "manifest.json"
    partial_path = partial_dir / "partial.json"
    write_worker_manifest(partial_manifest, manifest)
    write_partial_result_snapshot(
        partial_path,
        PartialResultSnapshot("w0", "hmc", "running", {"draws_completed": 2}),
    )
    assert (
        reduce_worker_artifacts(
            worker_id="w0",
            expected_stale_payload=expected,
            manifest_path=partial_manifest,
            partial_path=partial_path,
        ).status
        == "partial"
    )

    stale_dir = tmp_path / "stale"
    stale_manifest = stale_dir / "manifest.json"
    write_worker_manifest(stale_manifest, _manifest(tmp_path, program="drifted"))
    stale = reduce_worker_artifacts(
        worker_id="w0",
        expected_stale_payload=expected,
        manifest_path=stale_manifest,
    )
    assert stale.status == "stale"
    assert stale.stale is True

    failed_dir = tmp_path / "failed"
    failed_manifest = failed_dir / "manifest.json"
    failed_result = failed_dir / "result.json"
    write_worker_manifest(failed_manifest, manifest)
    record_worker_result(
        failed_result,
        WorkerRecord(
            "w0",
            ("python", "-m", "toy_worker"),
            manifest.config_hash,
            return_code=2,
            runtime_s=0.5,
            status="failed",
        ),
    )
    failed = reduce_worker_artifacts(
        worker_id="w0",
        expected_stale_payload=expected,
        manifest_path=failed_manifest,
        result_path=failed_result,
    )
    assert failed.status == "failed"
    assert failed.return_code == 2

    timeout_dir = tmp_path / "timeout"
    timeout_manifest = timeout_dir / "manifest.json"
    timeout_record = timeout_dir / "timeout.json"
    write_worker_manifest(timeout_manifest, manifest)
    record_timeout(
        timeout_record,
        worker_id="w0",
        timeout_s=60.0,
        elapsed_s=61.0,
        action="terminate_worker",
    )
    timed_out = reduce_worker_artifacts(
        worker_id="w0",
        expected_stale_payload=expected,
        manifest_path=timeout_manifest,
        timeout_path=timeout_record,
    )
    assert timed_out.status == "timed_out"
    assert timed_out.timed_out is True


def test_timing_buckets_are_explanatory_nonclaims_only():
    bucket = make_timing_bucket("compile", 0.25)

    assert bucket.name == "compile"
    assert bucket.role == "explanatory_only"
    assert "not a validity or promotion criterion" in bucket.nonclaims[0]
    with pytest.raises(ValueError, match="unknown timing bucket"):
        make_timing_bucket("posterior_validity", 1.0)


def test_device_selection_uses_trusted_metadata_without_hardware_probe():
    untrusted = select_preferred_gpu([0, 1], busy_gpu_ids=[1])
    trusted_snapshot = build_trusted_gpu_snapshot(
        [
            {"index": 0, "memory_used_mb": 1024, "memory_total_mb": 32768},
            {"index": 1, "memory_used_mb": 25000, "memory_total_mb": 32768},
        ],
        trusted_or_escalated=True,
        source="synthetic-unit-test",
    )
    trusted = select_preferred_gpu([], gpu_snapshot=trusted_snapshot)

    assert untrusted.selected_gpu == 1
    assert "gpu_busy_evidence_not_trusted" in untrusted.veto_reasons
    assert trusted.selected_gpu == 0
    assert trusted.fallback_used is True


def test_candidate_order_and_first_tie_survive_worker_completion_order():
    completed = (
        CandidateResult(5, 0.2, 4, 2.0),
        CandidateResult(2, 0.1, 8, 1.0),
        CandidateResult(1, 0.1, 4, 1.0),
    )

    ordered = canonical_candidate_order(completed)
    selected = select_first_tie_candidate(completed)

    assert [candidate.candidate_index for candidate in ordered] == [1, 2, 5]
    assert selected.candidate_index == 1
