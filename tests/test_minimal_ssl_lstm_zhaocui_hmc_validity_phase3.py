from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "minimal_ssl_lstm_zhaocui_hmc_validity_phase3",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_reviewed_phase3_settings_match_subplan_contract() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase3_settings()

    assert settings.chain_count == 4
    assert settings.num_results == 64
    assert settings.num_burnin_steps == 32
    assert settings.step_size == 1.0e-5
    assert settings.num_leapfrog_steps == 1
    assert settings.seed == (20260706, 6301)
    assert settings.use_xla is True
    assert settings.require_gpu is True
    assert settings.rhat_threshold == 1.2
    assert settings.ess_threshold == 16.0
    assert settings.payload()["jit_compile"] is True


def test_deterministic_chain_initial_state_shape_and_dispersion() -> None:
    harness = _load_harness()
    base = harness.initial_minimal_ssl_lstm_hmc_state(1.0e-3)
    state = harness.deterministic_chain_initial_state(
        base,
        chain_count=4,
        spread=0.03,
    )
    array = state.numpy()

    assert array.shape == (4, 24)
    assert np.all(np.isfinite(array))
    assert not np.allclose(array[0], array[-1])
    assert np.allclose(0.5 * (array[0] + array[-1]), base.numpy())


def test_rhat_ess_summary_classifies_synthetic_chains() -> None:
    harness = _load_harness()
    draws = np.arange(32, dtype=np.float64)[:, None, None]
    chains = np.arange(4, dtype=np.float64)[None, :, None] * 0.01
    params = np.arange(3, dtype=np.float64)[None, None, :] * 0.001
    samples = draws * 0.1 + chains + params

    summary = harness.compute_rhat_ess_summaries(
        samples,
        rhat_threshold=2.0,
        ess_threshold=1.0,
    )

    assert summary["rhat"]["finite_count"] == 3
    assert summary["ess"]["finite_count"] == 3
    assert summary["rhat"]["nonfinite_count"] == 0
    assert summary["ess"]["nonfinite_count"] == 0
    assert summary["method"]["sample_shape_convention"] == "[draw, chain, parameter]"


def test_sampled_state_reference_check_accepts_known_states() -> None:
    harness = _load_harness()
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)
    base = harness.initial_minimal_ssl_lstm_hmc_state(1.0e-3).numpy()
    samples = np.repeat(base[None, None, :], 4 * 2, axis=0).reshape(4, 2, 24)

    check = harness.sampled_state_reference_check(
        adapter,
        samples,
        prior_scale=5.0,
    )

    assert check["passed"] is True
    assert check["checked_state_count"] == 6
    assert check["max_abs_error"] <= harness.VALUE_ATOL
    assert check["max_rel_error"] <= harness.VALUE_RTOL


def test_phase3_preflight_records_missing_approval_without_runtime(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    artifact = harness.build_phase3_longer_hmc_artifact(
        trusted_gpu_xla_approval=False,
        settings=harness.reviewed_phase3_settings(),
        command=("pytest", "phase3-preflight"),
    )

    assert artifact["phase"] == "PHASE3"
    assert artifact["status"] == "failed"
    assert artifact["hmc_runtime"]["not_run_reason"] == "preflight_continuation_veto"
    assert "missing_trusted_gpu_xla_approval" in artifact["continuation_vetoes"]
    assert "gpu_hidden_for_trusted_phase3" in artifact["continuation_vetoes"]
    assert artifact["promotion_screen"]["artifact_valid"] is False
    assert "not full posterior correctness evidence" in artifact["nonclaims"]


def test_phase3_cpu_helper_artifact_records_reference_and_boundaries(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    artifact = harness.build_phase3_longer_hmc_artifact(
        trusted_gpu_xla_approval=True,
        settings=harness.test_cpu_phase3_settings(
            num_results=4,
            num_burnin_steps=1,
            chain_count=2,
        ),
        command=("pytest", "phase3-cpu-helper"),
    )

    assert artifact["phase"] == "PHASE3"
    assert artifact["predeclared_settings"]["artifact_mode"] == "focused_cpu_hidden_test_helper"
    assert artifact["predeclared_settings"]["use_xla"] is False
    assert artifact["predeclared_settings"]["require_gpu"] is False
    assert artifact["run_manifest"]["cpu_gpu_status"]["cuda_visible_devices"] == "-1"
    assert artifact["hmc_runtime"]["sample_shape"] == [4, 2, 24]
    assert artifact["sampled_state_reference_check"]["checked_state_count"] == 6
    assert artifact["metric_roles"]["acceptance_rate"] == (
        "explanatory_only_unless_finite_log_diagnostic_missing"
    )
    assert "not broad HMC convergence evidence" in artifact["nonclaims"]
    if artifact["status"] == "passed":
        assert artifact["continuation_vetoes"] == []
        assert artifact["sampled_state_reference_check"]["passed"] is True


def test_phase3_cli_requires_trusted_approval(tmp_path: Path) -> None:
    harness = _load_harness()

    with pytest.raises(RuntimeError, match="trusted-gpu-xla-approval"):
        harness.main(
            [
                "--output",
                str(tmp_path / "phase3.json"),
                "--markdown-output",
                str(tmp_path / "phase3.md"),
            ]
        )


def test_render_markdown_includes_promotion_and_nonclaims(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    artifact = harness.build_phase3_longer_hmc_artifact(
        trusted_gpu_xla_approval=False,
        settings=harness.reviewed_phase3_settings(),
        command=("pytest", "phase3-markdown"),
    )

    summary = harness.render_markdown(artifact)

    assert "Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 3" in summary
    assert "Promotion Screen" in summary
    assert "not full posterior correctness evidence" in summary
    assert "Native Divergence" in summary


def test_phase3_json_roundtrip_for_preflight_artifact(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase3_preflight.json"
    artifact = harness.build_phase3_longer_hmc_artifact(
        trusted_gpu_xla_approval=False,
        settings=harness.reviewed_phase3_settings(),
        command=("pytest", "phase3-json"),
    )

    harness.atomic_write_json(output, artifact)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["schema_version"] == (
        "minimal_ssl_lstm_zhaocui_hmc_validity.phase3_longer_hmc.v1"
    )
    assert payload["status"] == "failed"
    assert payload["hmc_runtime"]["not_run_reason"] == "preflight_continuation_veto"
