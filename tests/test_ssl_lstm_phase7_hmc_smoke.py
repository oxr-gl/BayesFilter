from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs/benchmarks/benchmark_ssl_lstm_filter_hmc_phase7.py"


def _read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_phase7_hmc_launch_smoke_writes_hard_veto_classification(tmp_path: Path) -> None:
    output = tmp_path / "phase7.json"
    markdown = tmp_path / "phase7.md"
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
            "--num-results",
            "2",
            "--num-burnin-steps",
            "1",
            "--step-size",
            "1e-5",
            "--num-leapfrog-steps",
            "1",
            "--no-jit-compile",
        ],
        cwd=ROOT,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=240,
    )

    artifact = _read_json(output)
    assert artifact["schema_version"] == "ssl_lstm.filter_hmc.phase7_hmc_smoke.v1"
    assert artifact["phase"] == "PHASE7"
    assert artifact["tier"] == "launch_smoke"
    assert artifact["parameter_matching_primary_criterion"] is False
    assert artifact["ranking_supported"] is False
    assert artifact["rhat_ess_computed"] is False
    assert artifact["run_manifest"]["gpu_trust_basis"] == "cpu_hidden_debug"
    assert artifact["metric_roles"]["acceptance_rate"] == "explanatory_only_in_launch_smoke"
    rows = {row["filter_name"]: row for row in artifact["candidate_rows"]}
    assert rows["fixed_sgqf"]["status"] in {"passed_launch_smoke", "failed_launch_smoke"}
    assert rows["svd_ukf"]["status"] in {"passed_launch_smoke", "failed_launch_smoke"}
    assert rows["zhaocui_fixed"]["status"] in {"passed_launch_smoke", "failed_launch_smoke"}
    assert rows["ledh_streaming_ot"]["status"] == "blocked"
    assert rows["fixed_sgqf"]["value_score_authority"] == "graph_native"
    assert rows["svd_ukf"]["value_score_authority"] == "graph_native"
    assert rows["zhaocui_fixed"]["value_score_authority"] == "graph_native"
    assert rows["zhaocui_fixed"]["gradient_path"] == "analytic_first_order_zhaocui_fixed"
    assert "not a sampler convergence claim" in rows["fixed_sgqf"]["nonclaims"]
    assert "not R-hat or ESS evidence" in artifact["nonclaims"]
    assert markdown.exists()


def test_phase7_hmc_launch_source_forbids_ranking_and_rhat_promotion() -> None:
    source = SCRIPT.read_text(encoding="utf-8")
    assert "ranking_supported" in source
    assert "rhat_ess_computed" in source
    assert "not R-hat or ESS evidence" in source
    assert "not a ranking claim" in source
