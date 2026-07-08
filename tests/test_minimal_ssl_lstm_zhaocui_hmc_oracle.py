from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from pathlib import Path

import numpy as np


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT / "docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "minimal_ssl_lstm_zhaocui_hmc_oracle",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_numpy_reference_matches_base_target_value() -> None:
    harness = _load_harness()
    theta_center = np.asarray(harness.minimal_ssl_lstm_theta().numpy(), dtype=np.float64)
    theta = np.asarray(harness.initial_minimal_ssl_lstm_hmc_state(1.0e-3).numpy())
    observations = np.asarray(harness.minimal_ssl_lstm_observations().numpy())
    noise = harness.materialize_replay_noise()
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)

    target_value, target_score = harness.target_log_prob_and_score(adapter, theta)
    reference_value = harness.reference_log_prob_np(
        theta,
        observations,
        noise,
        prior_center=theta_center,
        prior_scale=5.0,
    )

    assert math.isfinite(target_value)
    assert np.all(np.isfinite(target_score))
    assert abs(target_value - reference_value) <= harness.VALUE_ATOL


def test_oracle_artifact_records_boundaries_with_reduced_grid() -> None:
    harness = _load_harness()
    artifact = harness.build_oracle_artifact(
        widths=(0.5, 2.0, 20.0),
        points_per_width=21,
        coordinates=harness.SELECTED_COORDINATES[:3],
        command=("pytest", "phase2-oracle-reduced"),
    )

    assert artifact["phase"] == "PHASE2"
    assert artifact["artifact_role"] == "conditional_slice_reference_debug"
    assert artifact["target_quantity"]["prior_scale"] == 5.0
    assert artifact["grid_settings"]["widths"] == [0.5, 2.0, 20.0]
    assert artifact["grid_settings"]["points_per_width"] == 21
    assert artifact["target_reference_value_check"]["passed"] is True
    assert artifact["finite_difference_score_check"]["passed"] is True
    assert artifact["determinism_check"]["passed"] is True
    assert len(artifact["conditional_slice_rows"]) == 3
    assert "not full posterior correctness evidence" in artifact["nonclaims"]
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert "not source-faithful SSL-LSTM Zhao-Cui parity evidence" in artifact["nonclaims"]
    assert artifact["run_manifest"]["jit_compile"] is False
    assert artifact["run_manifest"]["cpu_gpu_status"]["cuda_visible_devices"] == "-1"


def test_oracle_cli_writes_json_and_markdown_with_reduced_grid(tmp_path: Path) -> None:
    harness = _load_harness()
    output = tmp_path / "oracle.json"
    markdown_output = tmp_path / "oracle.md"

    exit_code = harness.main(
        [
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
            "--widths",
            "0.5",
            "2.0",
            "20.0",
            "--points-per-width",
            "41",
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert exit_code == (0 if payload["status"] == "passed" else 1)
    assert payload["schema_version"] == "minimal_ssl_lstm_zhaocui_hmc_validity.phase2_oracle.v1"
    assert payload["target_reference_value_check"]["passed"] is True
    assert "Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 2 Oracle" in summary
    assert "not full posterior correctness evidence" in summary
