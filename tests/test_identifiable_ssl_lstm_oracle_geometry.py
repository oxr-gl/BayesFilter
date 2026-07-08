from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

import numpy as np


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_identifiable_ssl_lstm_oracle_geometry_2026_07_08.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "identifiable_ssl_lstm_oracle_geometry",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_settings_encode_sample_ratio_contract() -> None:
    harness = _load_harness()
    settings = harness.default_settings()

    assert settings.horizon == 200
    assert settings.dimension == 4
    assert settings.effective_low_rank_rank == 3
    assert settings.regression_parameter_count == 9
    assert settings.required_finite_samples == 45
    assert settings.low_rank_sample_count >= settings.required_finite_samples
    assert settings.free_parameter_names == harness.FREE_PARAMETER_NAMES


def test_oracle_target_has_four_free_parameters_and_longer_data() -> None:
    harness = _load_harness()
    target = harness.build_identifiable_oracle_target()

    assert target.config.horizon == 200
    assert target.config.parameter_dim == 24
    assert len(target.free_indices) == 4
    assert target.states.shape == (200, 3)
    assert target.observations.shape == (200, 1)
    assert all(name in target.config.parameter_names for name in target.free_parameter_names)

    value, score = target.value_and_score(target.truth_free)
    assert np.isfinite(float(value.numpy()))
    assert np.all(np.isfinite(score.numpy()))


def test_dense_negative_hessian_is_finite_spd_on_oracle_target() -> None:
    harness = _load_harness()
    settings = harness.default_settings()
    target = harness.build_identifiable_oracle_target(settings)

    center, diagnostics = harness.estimate_map_center(target, settings)
    dense = harness.dense_negative_hessian(target, center)
    scale = np.asarray(target.scale.numpy(), dtype=float)
    whitened = scale[:, np.newaxis] * dense * scale[np.newaxis, :]
    summary = harness.eigen_summary(whitened)

    assert diagnostics["center_position_role"] == "map_candidate"
    assert diagnostics["score_norm"] < 1.0e-5
    assert dense.shape == (4, 4)
    assert np.all(np.isfinite(dense))
    assert summary["positive"] is True


def test_diagnostic_payload_records_nonclaims_and_contract(monkeypatch) -> None:
    harness = _load_harness()

    class FakeGeometryResult:
        accepted = True
        status = "usable"
        precision = np.eye(4)

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "diagnostics": {
                    "finite_sample_count": 260,
                    "required_finite_samples": 50,
                    "holdout_passed": True,
                },
                "include_arrays": include_arrays,
            }

    monkeypatch.setattr(
        harness,
        "estimate_map_center",
        lambda target, settings=None: (
            target.truth_free,
            {
                "center_position_role": "map_candidate",
                "gradient_norm_passed": True,
                "failed": False,
                "score_norm": 0.0,
            },
        ),
    )
    monkeypatch.setattr(
        harness,
        "dense_negative_hessian",
        lambda target, center: np.diag(1.0 / np.square(np.asarray(target.scale.numpy(), dtype=float))),
    )
    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: FakeGeometryResult(),
    )

    payload = harness.run_identifiable_geometry_diagnostic()

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["classification"] == "extension_or_invention"
    assert payload["target"]["free_parameter_dim"] == 4
    assert payload["decision"]["geometry_sanity_passed"] is True
    assert payload["decision"]["map_candidate_passed"] is True
    assert payload["center"]["position_role"] == "map_candidate"
    assert payload["comparison"]["coordinate_system"] == (
        "whitened_center_plus_scale_times_z"
    )
    assert payload["inference_status"]["default_readiness"] == "not assessed"
    assert any("not HMC convergence" in item for item in payload["nonclaims"])
    assert any("not Zhao-Cui source-faithfulness" in item for item in payload["nonclaims"])


def test_veto_when_low_rank_geometry_rejected(monkeypatch) -> None:
    harness = _load_harness()

    class RejectedGeometryResult:
        accepted = False
        status = "holdout_fit_rejected"
        precision = None

        def payload(self, *, include_arrays: bool = False):
            return {
                "schema": "bayesfilter.low_rank_spd_quadratic_geometry.v1",
                "accepted": self.accepted,
                "status": self.status,
                "diagnostics": {
                    "finite_sample_count": 260,
                    "required_finite_samples": 50,
                    "holdout_passed": False,
                },
                "include_arrays": include_arrays,
            }

    monkeypatch.setattr(
        harness,
        "estimate_map_center",
        lambda target, settings=None: (
            target.truth_free,
            {
                "center_position_role": "map_candidate",
                "gradient_norm_passed": True,
                "failed": False,
                "score_norm": 0.0,
            },
        ),
    )
    monkeypatch.setattr(
        harness,
        "dense_negative_hessian",
        lambda target, center: np.diag(1.0 / np.square(np.asarray(target.scale.numpy(), dtype=float))),
    )
    monkeypatch.setattr(
        harness,
        "fit_low_rank_spd_quadratic_geometry",
        lambda *_args, **_kwargs: RejectedGeometryResult(),
    )

    payload = harness.run_identifiable_geometry_diagnostic()

    assert payload["decision"]["geometry_sanity_passed"] is False
    assert "low_rank_geometry_holdout_fit_rejected" in payload["decision"]["vetoes"]
    assert payload["decision"]["viable_for_next_step"] is False
