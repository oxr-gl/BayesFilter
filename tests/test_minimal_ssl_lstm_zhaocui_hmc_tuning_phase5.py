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
    "benchmark_minimal_ssl_lstm_zhaocui_hmc_tuning_phase5_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "minimal_ssl_lstm_zhaocui_hmc_tuning_phase5",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_phase5_settings_match_subplan_contract() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase5_settings()

    assert settings.preset == "smoke"
    assert settings.seed == (20260706, 6501)
    assert settings.max_attempts == 1
    assert settings.use_xla is False
    assert settings.public_timeout_budget_s == 90.0
    assert settings.payload()["artifact_mode"] == "cpu_hidden_staged_tuning_smoke_diagnostic"
    assert settings.eigenvalue_floor == 0.04
    assert settings.max_condition_number == 1.0e6


def test_phase5_config_uses_public_tuner_without_xla() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase5_settings()
    config = harness.phase5_tuning_config(
        settings,
        target_scope="scope",
        geometry_position_role="initial_position",
        negative_hessian_source="regularized_negative_hessian_at_initial_position",
    )

    assert config.preset == "smoke"
    assert config.target_scope == "scope"
    assert config.use_xla is False
    assert config.max_attempts == 1
    assert config.public_timeout_budget_s == 90.0
    assert config.bootstrap_max_repairs == 1
    assert config.geometry_position_role == "initial_position"
    assert config.negative_hessian_source == (
        "regularized_negative_hessian_at_initial_position"
    )
    assert config.max_condition_number == 1.0e6
    assert config.eigenvalue_floor == 0.04


def test_initial_covariance_is_positive_diagonal() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase5_settings()
    covariance = harness.initial_covariance(settings, dimension=4)

    assert covariance.shape == (4, 4)
    assert np.allclose(covariance, covariance.T)
    assert np.all(np.linalg.eigvalsh(covariance) > 0.0)


def test_initial_geometry_uses_finite_curvature_with_visible_map_fallback() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase5_settings()
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(
        evidence_path=harness.SUBPLAN_PATH
    )
    initial = harness.initial_minimal_ssl_lstm_hmc_state(
        settings.initial_offset_scale
    )

    geometry_inputs, diagnostics = harness.initial_geometry_inputs(
        adapter,
        initial,
        settings,
    )

    assert settings.initial_geometry_strategy == "map_candidate_hessian"
    assert diagnostics["selected_geometry_hint"] == "negative_hessian"
    assert diagnostics["fallback_used"] is True
    assert diagnostics["fallback_reason"] == (
        "map_candidate_gradient_norm_above_diagnostic_tolerance"
    )
    assert diagnostics["position_role"] == "initial_position"
    assert diagnostics["covariance_source"] == (
        "regularized_negative_hessian_at_initial_position"
    )
    assert diagnostics["negative_hessian_nonpositive_eigenvalue_count"] >= 1
    assert geometry_inputs["initial_covariance"] is None
    assert geometry_inputs["negative_hessian"].shape == (adapter.parameter_dim, adapter.parameter_dim)
    assert np.all(np.isfinite(geometry_inputs["negative_hessian"]))


def test_low_rank_spd_quadratic_strategy_is_optional_and_transforms_precision(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _load_harness()
    settings = harness.replace(
        harness.reviewed_phase5_settings(),
        initial_geometry_strategy="low_rank_spd_quadratic",
    )
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(
        evidence_path=harness.SUBPLAN_PATH
    )
    initial = harness.initial_minimal_ssl_lstm_hmc_state(
        settings.initial_offset_scale
    )

    class FakeGeometryResult:
        accepted = True
        status = "usable"
        precision = np.diag([1.0, 2.0] + [3.0] * (adapter.parameter_dim - 2))
        refined_center = None
        center_refinement_accepted = False

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "include_arrays": include_arrays,
                "reports_hmc_convergence": False,
            }

    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: FakeGeometryResult(),
    )

    geometry_inputs, diagnostics = harness.initial_geometry_inputs(
        adapter,
        initial,
        settings,
    )

    scale_sq = adapter.prior_scale * adapter.prior_scale
    assert diagnostics["selected_geometry_hint"] == "negative_hessian"
    assert diagnostics["fallback_used"] is False
    assert diagnostics["covariance_source"] == "low_rank_spd_quadratic_precision"
    assert diagnostics["classification"] == "extension_or_invention"
    assert diagnostics["reports_hmc_convergence"] is False
    np.testing.assert_allclose(
        np.diag(geometry_inputs["negative_hessian"])[:2],
        np.array([1.0, 2.0]) / scale_sq,
    )
    assert geometry_inputs["initial_covariance"] is None


def test_low_rank_spd_quadratic_rejection_preserves_attempt_and_falls_back(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _load_harness()
    settings = harness.replace(
        harness.reviewed_phase5_settings(),
        initial_geometry_strategy="low_rank_spd_quadratic",
    )
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(
        evidence_path=harness.SUBPLAN_PATH
    )
    initial = harness.initial_minimal_ssl_lstm_hmc_state(
        settings.initial_offset_scale
    )

    class RejectedGeometryResult:
        accepted = False
        status = "holdout_fit_rejected"
        precision = None
        refined_center = None
        center_refinement_accepted = False

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "include_arrays": include_arrays,
            }

    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: RejectedGeometryResult(),
    )

    geometry_inputs, diagnostics = harness.initial_geometry_inputs(
        adapter,
        initial,
        settings,
    )

    assert diagnostics["fallback_used"] is True
    assert diagnostics["fallback_reason"] == (
        "low_rank_spd_quadratic_holdout_fit_rejected"
    )
    assert diagnostics["low_rank_spd_quadratic_attempt"]["fallback_reason"] == (
        "holdout_fit_rejected"
    )
    assert diagnostics["selected_geometry_hint"] in {
        "negative_hessian",
        "initial_covariance",
    }
    assert geometry_inputs["negative_hessian"] is not None or geometry_inputs[
        "initial_covariance"
    ] is not None


def test_phase5_preconditions_require_phase3_and_phase4() -> None:
    harness = _load_harness()

    assert harness.load_phase3_baseline()["phase3_preconditions_met"] is True
    phase4 = harness.load_phase4_baseline()
    assert phase4["phase4_preconditions_met"] is True
    assert phase4["native_divergence_telemetry_status"] == (
        "native_divergence_not_exposed_by_kernel"
    )


def test_phase5_artifact_with_fake_public_tuner_records_nonpromoting_result(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    class FakeResult:
        final_status = "budget_exhausted"
        passed = False
        diagnostic_role = "phase7_budget_exhausted"
        hard_vetoes = ()
        repair_triggers = ("phase7_budget_exhausted",)
        final_kernel_hash = None
        final_kernel_payload = None
        target_dimension = 24
        geometry = object()
        bootstrap = object()
        tune_verify_repair_loop = None
        artifact_path = str(tmp_path / "hmc_kernel_tuning_result.json")
        nonclaims = ("no posterior convergence claim",)

        def payload(self, *, include_internal_diagnostics: bool = True):
            return {
                "schema": "bayesfilter.hmc_kernel_tuning_result.v1",
                "final_status": self.final_status,
                "passed": self.passed,
                "hard_vetoes": self.hard_vetoes,
                "repair_triggers": self.repair_triggers,
                "include_internal_diagnostics": include_internal_diagnostics,
            }

    def fake_tune_hmc_kernel(**_kwargs):
        (tmp_path / "hmc_kernel_tuning_result.json").write_text(
            json.dumps(
                {
                    "schema": "bayesfilter.hmc_kernel_tuning_public_artifact.v1",
                    "status": "budget_exhausted",
                    "hard_vetoes": [],
                }
            ),
            encoding="utf-8",
        )
        (tmp_path / "hmc_kernel_tuning_progress.json").write_text(
            json.dumps({"schema": "bayesfilter.hmc_kernel_tuning_progress.v1"}),
            encoding="utf-8",
        )
        return FakeResult()

    monkeypatch.setattr(harness, "tune_hmc_kernel", fake_tune_hmc_kernel)
    artifact = harness.build_phase5_tuning_artifact(
        output_dir=tmp_path,
        command=("pytest", "phase5-fake"),
    )

    assert artifact["status"] == "passed"
    assert artifact["phase_decision"] == "structured_non_promoting_tuning_result_recorded"
    assert artifact["hard_vetoes"] == []
    assert artifact["tuning_result_summary"]["final_status"] == "budget_exhausted"
    assert artifact["native_divergence_status_carried_forward"] == (
        "native_divergence_not_exposed_by_kernel"
    )
    assert "not zero divergences" in artifact["native_divergence_interpretation"]


def test_phase5_artifact_marks_tuning_hard_veto_as_failed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    class FakeResult:
        final_status = "hard_veto"
        passed = False
        diagnostic_role = "bootstrap_screen_hard_veto"
        hard_vetoes = ("bootstrap_screen_error",)
        repair_triggers = ("RuntimeError",)
        final_kernel_hash = None
        final_kernel_payload = None
        target_dimension = 24
        geometry = object()
        bootstrap = None
        tune_verify_repair_loop = None
        artifact_path = None
        nonclaims = ("no posterior convergence claim",)

        def payload(self, *, include_internal_diagnostics: bool = True):
            return {
                "schema": "bayesfilter.hmc_kernel_tuning_result.v1",
                "final_status": self.final_status,
                "hard_vetoes": self.hard_vetoes,
            }

    monkeypatch.setattr(harness, "tune_hmc_kernel", lambda **_kwargs: FakeResult())
    artifact = harness.build_phase5_tuning_artifact(
        output_dir=tmp_path,
        command=("pytest", "phase5-hard-veto"),
    )

    assert artifact["status"] == "passed"
    assert artifact["phase_decision"] == "structured_tuning_hard_veto_blocks_phase6"
    assert artifact["hard_vetoes"] == []
    assert artifact["tuning_result_summary"]["hard_vetoes"] == ["bootstrap_screen_error"]


def test_phase5_markdown_and_json_roundtrip_with_fake_tuner(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    class FakeResult:
        final_status = "budget_exhausted"
        passed = False
        diagnostic_role = "phase7_budget_exhausted"
        hard_vetoes = ()
        repair_triggers = ("phase7_budget_exhausted",)
        final_kernel_hash = None
        final_kernel_payload = None
        target_dimension = 24
        geometry = object()
        bootstrap = object()
        tune_verify_repair_loop = None
        artifact_path = str(tmp_path / "tuning" / "hmc_kernel_tuning_result.json")
        nonclaims = ("no posterior convergence claim",)

        def payload(self, *, include_internal_diagnostics: bool = True):
            return {"schema": "bayesfilter.hmc_kernel_tuning_result.v1"}

    def fake_tune_hmc_kernel(**kwargs):
        assert kwargs["config"].public_timeout_budget_s == 180.0
        assert kwargs["config"].terminal_phase6_repair_extra_attempts == 1
        out = kwargs["output_dir"]
        out.mkdir(parents=True, exist_ok=True)
        (out / "hmc_kernel_tuning_result.json").write_text(
            json.dumps({"schema": "bayesfilter.hmc_kernel_tuning_public_artifact.v1"}),
            encoding="utf-8",
        )
        return FakeResult()

    monkeypatch.setattr(harness, "tune_hmc_kernel", fake_tune_hmc_kernel)
    output = tmp_path / "phase5.json"
    markdown = tmp_path / "phase5.md"
    tuning_dir = tmp_path / "tuning"

    rc = harness.main(
        [
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
            "--tuning-output-dir",
            str(tuning_dir),
            "--public-timeout-budget-s",
            "180.0",
            "--terminal-phase6-repair-extra-attempts",
            "1",
        ]
    )
    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown.read_text(encoding="utf-8")
    manifest = payload["run_manifest"]

    assert rc == 0
    assert payload["schema_version"] == (
        "minimal_ssl_lstm_zhaocui_hmc_validity.phase5_tuning_mass.v1"
    )
    assert payload["status"] == "passed"
    assert payload["predeclared_settings"]["public_timeout_budget_s"] == 180.0
    assert payload["predeclared_settings"]["terminal_phase6_repair_extra_attempts"] == 1
    assert manifest["output_artifact"] == str(output)
    assert manifest["markdown_artifact"] == str(markdown)
    assert "Tuning final status" in summary
    assert "missing native divergence telemetry is not zero divergences" in summary
