from __future__ import annotations

import importlib.util
import os
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_geometry",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_settings_encode_phase1_fixed_numeric_contract() -> None:
    harness = _load_harness()
    settings = harness.default_settings()

    assert settings.horizon == 30
    assert settings.filter_name == "svd_ukf"
    assert settings.dimension == 4
    assert settings.effective_low_rank_rank == 3
    assert settings.regression_parameter_count == 9
    assert settings.required_finite_samples == 45
    assert settings.low_rank_sample_count == 72
    assert settings.low_rank_sample_count >= settings.required_finite_samples
    assert settings.prior_scale == 4.0
    assert settings.use_compiled_value_score is True
    assert settings.jit_compile_value_score is False


def test_filtering_target_has_four_free_parameters_and_finite_score() -> None:
    harness = _load_harness()
    settings = replace(
        harness.default_settings(),
        horizon=4,
        compute_finite_difference_curvature=False,
    )
    target = harness.build_filtering_geometry_target(settings)

    assert target.config.parameter_dim == 24
    assert target.observations.shape == (4, 1)
    assert len(target.free_indices) == 4
    assert target.free_parameter_names == harness.FREE_PARAMETER_NAMES

    value, score, status = harness.safe_value_and_score(target, target.truth_free)
    assert status == "finite"
    assert value is not None and np.isfinite(value)
    assert score is not None and np.asarray(score).shape == (4,)
    assert np.all(np.isfinite(score))


def test_compiled_value_score_matches_eager_on_micro_target() -> None:
    harness = _load_harness()
    settings = replace(
        harness.default_settings(),
        horizon=4,
        compute_finite_difference_curvature=False,
    )
    target = harness.build_filtering_geometry_target(settings)

    parity = target.compiled_eager_parity(target.truth_free)

    assert parity["checked"] is True
    assert parity["passed"] is True
    assert parity["jit_compile"] is False
    assert parity["value_abs_error"] <= 1.0e-10
    assert parity["score_max_abs_error"] <= 1.0e-10


def test_phase1_payload_records_nonclaims_and_contract(monkeypatch) -> None:
    harness = _load_harness()

    class FakeGeometryResult:
        accepted = True
        status = "usable"

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "diagnostics": {
                    "finite_sample_count": 60,
                    "required_finite_samples": 45,
                    "holdout_passed": True,
                },
                "precision_eigen_summary": {
                    "positive": True,
                    "condition_number": 10.0,
                    "min": 1.0,
                    "max": 10.0,
                },
                "include_arrays": include_arrays,
            }

    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: FakeGeometryResult(),
    )
    settings = replace(
        harness.default_settings(),
        horizon=4,
        compute_finite_difference_curvature=False,
    )

    payload = harness.run_filtering_geometry_diagnostic(settings)

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["classification"] == "extension_or_invention"
    assert payload["target"]["filter_name"] == "svd_ukf"
    assert payload["target"]["free_parameter_dim"] == 4
    assert payload["center"]["position_role"] == "truth_free_initial_center"
    assert payload["center"]["reports_map_quality"] is False
    assert payload["compiled_value_score"]["passed"] is True
    assert payload["decision"]["compiled_eager_parity_passed"] is True
    assert payload["decision"]["geometry_sanity_passed"] is True
    assert payload["decision"]["viable_for_phase2_mass_handoff"] is True
    assert payload["metric_roles"]["center_score_norm"] == "explanatory_only"
    assert payload["inference_status"]["hmc_readiness"].startswith("not assessed")
    assert any("not an HMC run" in item for item in payload["nonclaims"])
    assert any("not Zhao-Cui source-faithfulness" in item for item in payload["nonclaims"])


def test_phase1_veto_when_low_rank_geometry_rejected(monkeypatch) -> None:
    harness = _load_harness()

    class RejectedGeometryResult:
        accepted = False
        status = "holdout_fit_rejected"

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "diagnostics": {
                    "finite_sample_count": 60,
                    "required_finite_samples": 45,
                    "holdout_passed": False,
                },
                "include_arrays": include_arrays,
            }

    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: RejectedGeometryResult(),
    )
    settings = replace(
        harness.default_settings(),
        horizon=4,
        compute_finite_difference_curvature=False,
    )

    payload = harness.run_filtering_geometry_diagnostic(settings)

    assert payload["decision"]["geometry_sanity_passed"] is False
    assert "low_rank_geometry_holdout_fit_rejected" in payload["decision"]["vetoes"]
    assert payload["decision"]["viable_for_phase2_mass_handoff"] is False
