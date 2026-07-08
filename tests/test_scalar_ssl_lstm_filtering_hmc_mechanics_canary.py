from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py"
)
GEOMETRY_PATH = (
    ROOT
    / "docs/benchmarks/"
    "scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
MASS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_hmc_mechanics_canary",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _minimal_geometry_payload():
    precision = np.diag([2.0, 3.0, 4.0, 5.0])
    covariance = np.linalg.inv(precision)
    return {
        "schema_version": "scalar_ssl_lstm.filtering_geometry.v1",
        "decision": {"geometry_sanity_passed": True, "vetoes": []},
        "center": {
            "free_parameter_values": [0.35, -0.08, 0.65, 0.05],
            "position_role": "truth_free_initial_center",
        },
        "low_rank_geometry": {
            "accepted": True,
            "precision": precision.tolist(),
            "covariance": covariance.tolist(),
        },
    }


def _minimal_mass_payload():
    covariance = np.diag([0.5, 1.0 / 3.0, 0.25, 0.2])
    precision = np.linalg.inv(covariance)
    return {
        "schema_version": "scalar_ssl_lstm.filtering_mass_handoff.v1",
        "decision": {"mass_handoff_passed": True, "vetoes": []},
        "coordinate_contract": {
            "coordinate_system": "whitened_center_plus_scale_times_z",
            "theta_from_z": "theta = center + scale * z",
            "center_role": "truth_free_initial_center",
            "scale": [0.35, 0.35, 0.35, 0.35],
            "free_parameter_names": [
                "latent_mean_weight.0.0",
                "latent_mean_bias.0",
                "observation_weight.0.0",
                "observation_bias.0",
            ],
            "free_parameter_indices": [12, 13, 14, 15],
            "refined_center_used": False,
        },
        "matrix_convention": {
            "K_z": "whitened precision from Phase 1 low-rank geometry",
            "M_z": "whitened covariance/mass candidate equal to inv(regularized K_z)",
            "hmc_handoff_matrix": "M_z",
            "inverse_mass_for_formula": "K_z",
            "original_coordinate_mass": "not used for handoff",
        },
        "mass_handoff": {
            "factor": np.linalg.cholesky(covariance).tolist(),
            "mass_covariance_M_z": covariance.tolist(),
            "regularized_precision_K_z": precision.tolist(),
        },
    }


def test_settings_encode_exact_phase3_grid() -> None:
    harness = _load_harness()
    settings = harness.MechanicsCanarySettings()

    assert settings.candidate_grid == ((1, 0.10), (2, 0.25), (4, 0.3925))
    assert settings.payload()["candidate_grid"][-1]["trajectory_length"] == 1.57
    assert settings.num_results == 2
    assert settings.num_burnin_steps == 1


def test_precondition_vetoes_coordinate_mismatch() -> None:
    harness = _load_harness()
    mass = _minimal_mass_payload()
    mass["coordinate_contract"]["coordinate_system"] = "original_parameters"

    adapter, audit = harness.build_phase3_adapter(_minimal_geometry_payload(), mass)

    assert adapter is None
    assert audit["precondition_passed"] is False
    assert "coordinate_system_mismatch" in audit["vetoes"]


def test_precondition_vetoes_bad_mass_factor() -> None:
    harness = _load_harness()
    mass = _minimal_mass_payload()
    mass["mass_handoff"]["factor"][0][0] = 2.0

    adapter, audit = harness.build_phase3_adapter(_minimal_geometry_payload(), mass)

    assert adapter is None
    assert "mass_factor_reconstruction_failed" in audit["vetoes"]


def test_current_phase2_artifacts_build_mass_preconditioned_adapter_if_available() -> None:
    if not GEOMETRY_PATH.exists() or not MASS_PATH.exists():
        return
    harness = _load_harness()
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    mass = json.loads(MASS_PATH.read_text(encoding="utf-8"))

    adapter, audit = harness.build_phase3_adapter(geometry, mass)

    assert adapter is not None
    assert audit["precondition_passed"] is True
    assert audit["vetoes"] == []
    assert audit["coordinate_contract"]["tfp_hmc_coordinate_u"] == "z = u @ chol(M_z).T"
    assert audit["coordinate_contract"]["base_adapter_coordinate"] == "free parameter values"
    assert audit["mass_audit"]["factor_reconstructs_M_z_max_abs_error"] < 1.0e-8
    assert adapter.parameter_dim == 4
    value, score = adapter.log_prob_and_grad(adapter.initial_position())
    assert np.isfinite(float(value.numpy()))
    assert np.all(np.isfinite(score.numpy()))


def test_phase3_payload_preserves_nonclaims_when_precondition_fails() -> None:
    harness = _load_harness()
    mass = _minimal_mass_payload()
    mass["decision"]["mass_handoff_passed"] = False

    payload = harness.run_mechanics_canary(_minimal_geometry_payload(), mass)

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["decision"]["mechanics_canary_passed"] is False
    assert "phase2_mass_handoff_not_passed" in payload["decision"]["vetoes"]
    assert payload["inference_status"]["hmc_readiness"].startswith("not assessed")
    assert any("not HMC convergence" in item for item in payload["nonclaims"])
