from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/run_model_suite_hmc_qualification.py"


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _load_runner_module():
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    spec = importlib.util.spec_from_file_location("model_suite_runner", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_model_suite_stop_after_b_writes_robust_cpu_artifacts(tmp_path):
    artifact_root = tmp_path / "model_suite"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--artifact-root",
            str(artifact_root),
            "--num-results",
            "1",
            "--num-burnin-steps",
            "1",
            "--num-leapfrog-steps",
            "1",
            "--stop-after",
            "B",
        ],
        check=True,
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        timeout=360,
    )

    assert result.returncode == 0
    manifest = _read_json(artifact_root / "worker_manifest.json")
    summary = _read_json(artifact_root / "summary.json")
    reducer = _read_json(artifact_root / "reducer_status.json")
    worker_result = _read_json(artifact_root / "worker_result.json")
    partial = _read_json(artifact_root / "partial_snapshot.json")
    events = _read_jsonl(artifact_root / "stage_events.jsonl")

    assert manifest["device_policy"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert manifest["device_policy"]["tensorflow_visible_gpus_after_import"] == []
    assert manifest["environment"]["git_dirty_state"]["available"] is True
    assert isinstance(manifest["environment"]["git_dirty_state"]["is_dirty"], bool)
    assert reducer["status"] == "complete"
    assert worker_result["status"] == "ok"
    assert summary["status"] == "passed_bounded_stop_after"
    assert summary["reducer_status"] == "complete"
    assert summary["cpu_gpu_status"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert summary["cpu_gpu_status"]["tensorflow_visible_gpus"] == []
    assert summary["executed_model_order"] == ["A", "QR", "B"]
    assert summary["skipped_models"] == [{"model_id": "C", "reason": "stop_after_B"}]
    assert summary["execution_design"]["final_hmc_evidence_path"].endswith(
        "run_full_chain_tfp_hmc"
    )
    assert summary["execution_design"]["old_smoke_helpers_final_evidence"] is False
    assert partial["stage"] == "model_suite_complete"
    assert all(model["status"] == "passed" for model in summary["models"])
    assert all(
        model["hmc"]["runtime"] == "tfp.mcmc.sample_chain"
        and model["hmc"]["jit_compile"] is True
        and model["hmc"]["nonfinite_sample_count"] == 0
        for model in summary["models"]
    )
    assert all(
        model["value_score"]["nonfinite_count"] == 0
        for model in summary["models"]
    )
    assert "no sampler convergence claim" in summary["nonclaims"]
    assert "no DSGE readiness claim" in summary["nonclaims"]
    assert "no real-NK readiness claim" in summary["nonclaims"]
    assert "no GPU readiness claim" in summary["nonclaims"]
    assert "no score-matching readiness claim" in summary["nonclaims"]
    assert all(bucket["role"] == "explanatory_only" for bucket in summary["timing_buckets"])
    assert [row["stage"] for row in events].index("model_A_start") < [
        row["stage"] for row in events
    ].index("model_QR_start")
    assert [row["stage"] for row in events].index("model_QR_start") < [
        row["stage"] for row in events
    ].index("model_B_start")


def test_model_c_gate_requires_model_b_pass():
    runner = _load_runner_module()
    assert runner._should_run_model_c(
        [{"model_id": "A", "status": "passed"}, {"model_id": "B", "status": "passed"}],
        "C",
    )
    assert not runner._should_run_model_c(
        [{"model_id": "A", "status": "passed"}, {"model_id": "B", "status": "failed"}],
        "C",
    )
    assert not runner._should_run_model_c(
        [{"model_id": "A", "status": "passed"}, {"model_id": "B", "status": "passed"}],
        "B",
    )


def test_branch_summary_accepts_mapping_and_dataclass_like_objects():
    runner = _load_runner_module()

    class MappingAdapter:
        def branch_summary(self):
            return {
                "total_count": 1,
                "ok_count": 1,
                "active_floor_count": 0,
                "weak_spectral_gap_count": 0,
                "nonfinite_count": 0,
                "failure_labels": (),
                "max_deterministic_residual": 0.0,
                "max_support_residual": 0.0,
            }

    class DataclassLikeAdapter:
        def branch_summary(self):
            return SimpleNamespace(
                total_count=1,
                ok_count=1,
                active_floor_count=0,
                weak_spectral_gap_count=0,
                nonfinite_count=0,
                failure_labels=(),
                max_deterministic_residual=0.0,
                max_support_residual=0.0,
                other_blocked_count=0,
            )

    assert runner._branch_summary(MappingAdapter())["ok_count"] == 1
    dataclass_payload = runner._branch_summary(DataclassLikeAdapter())
    assert dataclass_payload["ok_count"] == 1
    assert dataclass_payload["other_blocked_count"] == 0.0


def test_artifact_force_refuses_unknown_and_removes_only_expected(tmp_path):
    runner = _load_runner_module()
    root = tmp_path / "artifacts"
    root.mkdir()
    (root / "worker_manifest.json").write_text("old\n", encoding="utf-8")
    (root / "unknown.txt").write_text("do not remove\n", encoding="utf-8")

    try:
        runner._prepare_artifact_root(root, force=True)
    except SystemExit as exc:
        assert "unknown entries" in str(exc)
    else:
        raise AssertionError("unknown artifact entry should be refused")

    assert (root / "unknown.txt").read_text(encoding="utf-8") == "do not remove\n"
    (root / "unknown.txt").unlink()
    paths = runner._prepare_artifact_root(root, force=True)
    assert not (root / "worker_manifest.json").exists()
    assert set(paths) == {"manifest", "events", "partial", "result", "reducer", "summary"}


def test_old_hmc_smoke_helpers_are_not_called_by_runner_source():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "run_qr_static_lgssm_hmc_smoke(" not in source
    assert "run_model_b_nonlinear_svd_cut4_hmc_smoke(" not in source
    assert "run_full_chain_tfp_hmc(" in source
