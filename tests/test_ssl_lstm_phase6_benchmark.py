from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase6.py"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase6_runner_builds_shared_fixture_and_status_rows(tmp_path: Path) -> None:
    output = tmp_path / "phase6.json"
    markdown = tmp_path / "phase6.md"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--seed",
            "20260704",
            "--horizon",
            "4",
            "--latent-dim",
            "2",
            "--hidden-dim",
            "2",
            "--observation-dim",
            "1",
            "--heldout-start",
            "3",
            "--fd-step",
            "1e-6",
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=240,
    )

    artifact = _read_json(output)
    assert artifact["schema_version"] == "ssl_lstm.filter_hmc.phase6_benchmark.v1"
    assert artifact["phase"] == "PHASE6"
    assert artifact["status"] == "PHASE6_SHARED_BENCHMARK_READY"
    assert artifact["parameter_matching_primary_criterion"] is False
    assert artifact["dataset_manifest"]["schema_version"] == "ssl_lstm.filter_hmc.dataset_manifest.v1"
    assert artifact["dataset_manifest"]["train_count"] == 3
    assert artifact["dataset_manifest"]["heldout_count"] == 1
    assert artifact["run_manifest"]["gpu_trust_basis"] == "cpu_hidden_debug"
    assert artifact["run_manifest"]["cpu_gpu_status"]["device_scope"] == "cpu"
    assert artifact["metric_roles"]["heldout_predictive_log_score"] == "explanatory_proxy"
    assert artifact["score_finite_all_admitted"] is True
    assert set(artifact["admitted_filters"]) == {"fixed_sgqf", "svd_ukf", "zhaocui_fixed"}
    assert set(artifact["blocked_filters"]) == {"ledh_streaming_ot"}
    rows = {row["filter_name"]: row for row in artifact["candidate_rows"]}
    assert rows["fixed_sgqf"]["status"] == "admitted"
    assert rows["svd_ukf"]["status"] == "admitted"
    assert rows["zhaocui_fixed"]["status"] == "admitted"
    assert rows["ledh_streaming_ot"]["status"] == "blocked"
    assert rows["fixed_sgqf"]["target_scope_provenance"]["target_scope_relation"] == "inherited_from_adapter_protocol"
    assert rows["svd_ukf"]["target_scope_provenance"]["target_scope_relation"] == "inherited_from_adapter_protocol"
    assert rows["zhaocui_fixed"]["target_scope_provenance"]["target_scope_relation"] == "inherited_from_adapter_protocol"
    assert rows["zhaocui_fixed"]["target_scope_provenance"]["protocol_phase"] == "PHASE2_PLUS_PHASE3_GATE"
    assert rows["fixed_sgqf"]["finite_difference_check"]["role"] == "promotion_veto_for_adapter_admission"
    assert rows["svd_ukf"]["finite_difference_check"]["role"] == "promotion_veto_for_adapter_admission"
    assert rows["zhaocui_fixed"]["finite_difference_check"]["role"] == "promotion_veto_for_adapter_admission"
    assert rows["fixed_sgqf"]["heldout_predictive_log_score"] is not None
    assert rows["svd_ukf"]["heldout_predictive_log_score"] is not None
    assert rows["zhaocui_fixed"]["heldout_predictive_log_score"] is not None
    assert rows["zhaocui_fixed"]["artifact"]["zhaocui_fixed_manifest"]["score_path"] == "manual_first_order_tensorflow_chain_rule"
    assert "parameter-by-parameter matching is not a primary criterion" in artifact["nonclaims"]
    assert "heldout predictive log score is a filter-likelihood proxy" in artifact["nonclaims"]
    assert markdown.exists()


def test_phase6_runner_mentions_parameter_matching_as_non_primary() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert "parameter_matching_primary_criterion" in source
    assert "not a ranking claim" in source
    assert "heldout predictive log score" in source
    assert "target_scope_provenance" in source
