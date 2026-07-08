from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


HARNESS_PATH = (
    Path(__file__).resolve().parents[1]
    / "docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location("minimal_ssl_lstm_zhaocui_smoke", HARNESS_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_minimal_smoke_artifact_schema_and_primary_gate() -> None:
    harness = _load_harness()
    artifact = harness.build_smoke_artifact(command=("pytest", "minimal-smoke"))

    assert artifact["status"] == "passed"
    assert artifact["primary_filter"] == "zhaocui_fixed"
    assert artifact["primary_filter_role"] == "promotion_criterion_for_minimal_mechanics_smoke"
    assert artifact["comparator_role"] == "fixed_sgqf_and_svd_ukf_are_mechanics_comparators_only"
    assert artifact["fixture"]["latent_dim"] == 1
    assert artifact["fixture"]["hidden_dim"] == 1
    assert artifact["fixture"]["observation_dim"] == 1
    assert artifact["fixture"]["horizon"] == 2
    assert artifact["fixture"]["parameter_dim"] == 24

    primary = artifact["primary_result"]
    assert primary["candidate_role"] == "primary_filter"
    assert primary["filter_name"] == "zhaocui_fixed"
    assert primary["artifact_role"] == "debug_reference"
    assert primary["score_finite"] is True
    assert math.isfinite(float(primary["log_likelihood"]))
    assert np.all(np.isfinite(np.asarray(primary["score"], dtype=np.float64)))
    assert primary["determinism_check"]["passed"] is True
    assert primary["finite_difference_check"]["passed"] is True
    assert primary["finite_difference_check"]["role"] == "promotion_veto_for_adapter_admission"
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert "not source-faithful SSL-LSTM Zhao-Cui parity evidence" in artifact["nonclaims"]


def test_minimal_smoke_comparator_rows_are_descriptive_only() -> None:
    harness = _load_harness()
    artifact = harness.build_smoke_artifact(command=("pytest", "minimal-smoke"))
    rows = {row["filter_name"]: row for row in artifact["comparator_rows"]}

    assert set(rows) == {"fixed_sgqf", "svd_ukf"}
    for row in rows.values():
        assert row["candidate_role"] == "mechanics_comparator_descriptive_only"
        assert row["comparison_role"] == "descriptive_only_not_primary_criterion"
        assert row["finite_difference_check"]["role"] == "explanatory"
        assert row["score_finite"] is True
        assert math.isfinite(float(row["log_likelihood"]))
        assert np.all(np.isfinite(np.asarray(row["score"], dtype=np.float64)))


def test_minimal_smoke_cli_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "minimal_smoke.json"
    markdown_output = tmp_path / "minimal_smoke.md"

    exit_code = harness.main(
        [
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert payload["status"] == "passed"
    assert payload["primary_filter"] == "zhaocui_fixed"
    assert payload["run_manifest"]["cpu_gpu_status"]["cuda_visible_devices"] == "-1"
    assert "CPU-hidden debug artifact only" in payload["nonclaims"]
    assert "Minimal SSL-LSTM Zhao-Cui Smoke" in summary
    assert "not HMC convergence evidence" in summary
