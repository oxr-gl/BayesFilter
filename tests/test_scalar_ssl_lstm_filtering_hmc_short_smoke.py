from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py"
)
PHASE3_PATH = (
    ROOT
    / "docs/benchmarks/"
    "scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json"
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
        "scalar_ssl_lstm_filtering_hmc_short_smoke",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _phase3_payload(passed: bool = True):
    return {
        "schema_version": "scalar_ssl_lstm.filtering_hmc_mechanics_canary.v1",
        "decision": {
            "mechanics_canary_passed": passed,
            "vetoes": [] if passed else ["fake_veto"],
        },
        "settings": {
            "candidate_grid": [
                {
                    "num_leapfrog_steps": 4,
                    "step_size": 0.3925,
                    "trajectory_length": 1.57,
                }
            ]
        },
        "precondition": {
            "coordinate_contract": {
                "tfp_hmc_coordinate_u": "z = u @ chol(M_z).T",
                "base_adapter_coordinate": "free parameter values",
                "free_parameters_from_u": "free = center + scale * (u @ chol(M_z).T)",
            }
        },
    }


def test_short_smoke_settings_match_reviewed_phase4_contract() -> None:
    harness = _load_harness()
    settings = harness.ShortSmokeSettings()

    assert settings.num_leapfrog_steps == 4
    assert settings.step_size == 0.3925
    assert settings.trajectory_length == 1.57
    assert settings.num_results == 8
    assert settings.num_burnin_steps == 2
    assert settings.payload()["adaptation_policy"] == "fixed_kernel_no_adaptation"


def test_validate_phase3_artifact_rejects_failed_phase3() -> None:
    harness = _load_harness()

    audit = harness.validate_phase3_artifact(_phase3_payload(passed=False))

    assert audit["phase3_precondition_passed"] is False
    assert "phase3_mechanics_canary_not_passed" in audit["vetoes"]
    assert "phase3_vetoes_present" in audit["vetoes"]


def test_validate_phase3_artifact_rejects_missing_coordinate_contract() -> None:
    harness = _load_harness()
    payload = _phase3_payload()
    payload["precondition"]["coordinate_contract"]["tfp_hmc_coordinate_u"] = "original_parameters"

    audit = harness.validate_phase3_artifact(payload)

    assert audit["phase3_precondition_passed"] is False
    assert "phase3_u_to_z_contract_missing" in audit["vetoes"]


def test_phase4_payload_preserves_nonclaims_when_phase3_fails() -> None:
    harness = _load_harness()

    payload = harness.run_short_smoke({}, {}, _phase3_payload(passed=False))

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["decision"]["short_smoke_passed"] is False
    assert "phase3_mechanics_canary_not_passed" in payload["decision"]["vetoes"]
    assert payload["inference_status"]["hmc_readiness"].startswith("not assessed")
    assert any("not HMC convergence" in item for item in payload["nonclaims"])


def test_current_phase3_artifact_validates_if_available() -> None:
    if not PHASE3_PATH.exists():
        return
    harness = _load_harness()
    phase3 = json.loads(PHASE3_PATH.read_text(encoding="utf-8"))

    audit = harness.validate_phase3_artifact(phase3)

    assert audit["phase3_precondition_passed"] is True
    assert audit["vetoes"] == ()
    assert audit["coordinate_contract"]["tfp_hmc_coordinate_u"] == "z = u @ chol(M_z).T"


def test_current_artifacts_build_phase4_payload_precondition_if_available() -> None:
    if not (GEOMETRY_PATH.exists() and MASS_PATH.exists() and PHASE3_PATH.exists()):
        return
    harness = _load_harness()
    geometry = json.loads(GEOMETRY_PATH.read_text(encoding="utf-8"))
    mass = json.loads(MASS_PATH.read_text(encoding="utf-8"))
    phase3 = json.loads(PHASE3_PATH.read_text(encoding="utf-8"))

    phase3_audit = harness.validate_phase3_artifact(phase3)
    phase3_module = harness.load_phase3_module()
    adapter, precondition = phase3_module.build_phase3_adapter(geometry, mass)

    assert phase3_audit["phase3_precondition_passed"] is True
    assert adapter is not None
    assert precondition["precondition_passed"] is True
