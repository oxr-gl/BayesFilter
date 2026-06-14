from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _read_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def test_phase6_cpu_only_canary_writes_complete_reducer_readable_artifacts(tmp_path):
    artifact_root = tmp_path / "phase6_canary"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    repo = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [
            sys.executable,
            str(repo / "scripts/run_nonlinear_ssm_phase6_engineering_canary.py"),
            "--artifact-root",
            str(artifact_root),
            "--num-results",
            "2",
            "--num-burnin-steps",
            "1",
            "--step-size",
            "0.0005",
            "--num-leapfrog-steps",
            "1",
        ],
        check=True,
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        timeout=240,
    )

    assert result.returncode == 0
    manifest = _read_json(artifact_root / "worker_manifest.json")
    summary = _read_json(artifact_root / "summary.json")
    reducer = _read_json(artifact_root / "reducer_status.json")
    partial = _read_json(artifact_root / "partial_snapshot.json")
    worker_result = _read_json(artifact_root / "worker_result.json")
    events = _read_jsonl(artifact_root / "stage_events.jsonl")

    assert manifest["device_policy"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert manifest["device_policy"]["tensorflow_visible_gpus_after_import"] == []
    assert manifest["stale_match_payload"]["program_signature"].endswith("canary-v1")
    assert reducer["status"] == "complete"
    assert worker_result["status"] == "ok"
    assert summary["reducer_status"] == "complete"
    assert summary["cpu_gpu_status"]["CUDA_VISIBLE_DEVICES"] == "-1"
    assert summary["cpu_gpu_status"]["tensorflow_visible_gpus"] == []
    assert summary["value_path"]["backend"] == "tf_svd_cut4"
    assert summary["value_score"]["authority"] == "graph_native"
    assert summary["value_score"]["target_scope"] == "phase6_model_b_nonlinear_canary"
    assert summary["value_score"]["nonfinite_count"] == 0
    assert summary["hmc"]["jit_compile"] is True
    assert summary["hmc"]["runtime"] == "tfp.mcmc.sample_chain"
    assert summary["hmc"]["nonfinite_sample_count"] == 0
    assert summary["hmc"]["finite_sample_count"] == 2
    assert summary["hmc"]["divergence_status"] == "unavailable"
    assert "no sampler convergence claim" in summary["nonclaims"]
    assert all(bucket["role"] == "explanatory_only" for bucket in summary["timing_buckets"])
    assert partial["stage"] == "full_chain_hmc"
    assert partial["nonfinite_count"] == 0
    assert [row["status"] for row in events].count("heartbeat") >= 3
    assert events[-1]["stage"] == "complete"
