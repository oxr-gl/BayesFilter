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
    "prepare_scalar_ssl_lstm_filtering_mass_handoff_2026_07_08.py"
)
GEOMETRY_PATH = (
    ROOT
    / "docs/benchmarks/"
    "scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_mass_handoff",
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
        "script": "docs/benchmarks/fake.json",
        "decision": {"geometry_sanity_passed": True, "vetoes": []},
        "center": {
            "free_parameter_values": [0.35, -0.08, 0.65, 0.05],
            "position_role": "truth_free_initial_center",
            "score_norm": 1.0,
        },
        "settings": {"free_parameter_scale": [0.35, 0.35, 0.35, 0.35]},
        "target": {
            "free_parameter_dim": 4,
            "free_parameter_names": [
                "latent_mean_weight.0.0",
                "latent_mean_bias.0",
                "observation_weight.0.0",
                "observation_bias.0",
            ],
            "free_parameter_indices": [12, 13, 14, 15],
        },
        "low_rank_geometry": {
            "accepted": True,
            "precision": precision.tolist(),
            "covariance": covariance.tolist(),
            "precision_eigen_summary": {"positive": True},
            "covariance_eigen_summary": {"positive": True},
            "diagnostics": {
                "coordinate_system": "whitened_center_plus_scale_times_z",
                "center_refinement": {"accepted": False, "reason": "outside_trust_radius"},
            },
        },
    }


def test_mass_handoff_converts_whitened_precision_to_mass_candidate() -> None:
    harness = _load_harness()
    payload = harness.prepare_mass_handoff(_minimal_geometry_payload())

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["decision"]["mass_handoff_passed"] is True
    assert payload["decision"]["vetoes"] == []
    assert payload["coordinate_contract"]["coordinate_system"] == "whitened_center_plus_scale_times_z"
    assert payload["coordinate_contract"]["refined_center_used"] is False
    assert payload["matrix_convention"]["K_z"].startswith("whitened precision")
    assert payload["matrix_convention"]["M_z"].startswith("whitened covariance")
    assert payload["matrix_convention"]["hmc_handoff_matrix"] == "M_z"
    assert payload["mass_handoff"]["precision_eigen_summary"]["positive"] is True
    assert payload["mass_handoff"]["mass_covariance_eigen_summary"]["positive"] is True
    assert payload["mass_handoff"]["precision_covariance_identity_max_abs_error"] < 1.0e-10
    assert any("not an HMC run" in item for item in payload["nonclaims"])


def test_mass_handoff_vetoes_coordinate_mismatch() -> None:
    harness = _load_harness()
    geometry = _minimal_geometry_payload()
    geometry["low_rank_geometry"]["diagnostics"]["coordinate_system"] = "original_parameters"

    payload = harness.prepare_mass_handoff(geometry)

    assert payload["decision"]["mass_handoff_passed"] is False
    assert "coordinate_system_mismatch" in payload["decision"]["vetoes"]


def test_current_phase1_artifact_contains_private_arrays_if_available() -> None:
    if not GEOMETRY_PATH.exists():
        return
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    low_rank = geometry["low_rank_geometry"]

    assert geometry["decision"]["geometry_sanity_passed"] is True
    assert np.asarray(low_rank["precision"]).shape == (4, 4)
    assert np.asarray(low_rank["covariance"]).shape == (4, 4)
