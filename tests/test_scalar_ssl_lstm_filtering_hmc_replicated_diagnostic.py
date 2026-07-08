from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py"
)
PHASE4_PATH = (
    ROOT
    / "docs/benchmarks/"
    "scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_hmc_replicated_diagnostic",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _phase4_payload(passed: bool = True):
    return {
        "schema_version": "scalar_ssl_lstm.filtering_hmc_short_smoke.v1",
        "decision": {
            "short_smoke_passed": passed,
            "vetoes": [] if passed else ["fake_veto"],
        },
        "settings": {
            "num_leapfrog_steps": 4,
            "step_size": 0.3925,
        },
        "phase3_gate": {
            "phase3_precondition_passed": True,
            "coordinate_contract": {
                "tfp_hmc_coordinate_u": "z = u @ chol(M_z).T",
                "base_adapter_coordinate": "free parameter values",
                "free_parameters_from_u": "free = center + scale * (u @ chol(M_z).T)",
            },
        },
    }


def test_replicated_settings_match_reviewed_phase5_contract() -> None:
    harness = _load_harness()
    settings = harness.ReplicatedDiagnosticSettings()

    assert settings.num_leapfrog_steps == 4
    assert settings.step_size == 0.3925
    assert settings.trajectory_length == 1.57
    assert settings.num_results == 16
    assert settings.num_burnin_steps == 4
    assert settings.seeds == (
        (20260708, 5501),
        (20260708, 5502),
        (20260708, 5503),
    )


def test_validate_phase4_artifact_rejects_failed_phase4() -> None:
    harness = _load_harness()

    audit = harness.validate_phase4_artifact(_phase4_payload(passed=False))

    assert audit["phase4_precondition_passed"] is False
    assert "phase4_short_smoke_not_passed" in audit["vetoes"]
    assert "phase4_vetoes_present" in audit["vetoes"]


def test_validate_phase4_artifact_rejects_kernel_mismatch() -> None:
    harness = _load_harness()
    payload = _phase4_payload()
    payload["settings"]["step_size"] = 0.1

    audit = harness.validate_phase4_artifact(payload)

    assert audit["phase4_precondition_passed"] is False
    assert "phase4_step_size_mismatch" in audit["vetoes"]


def test_phase5_payload_preserves_nonclaims_when_phase4_fails() -> None:
    harness = _load_harness()

    payload = harness.run_replicated_diagnostic({}, {}, _phase4_payload(passed=False))

    assert payload["schema_version"] == harness.SCHEMA_VERSION
    assert payload["decision"]["replicated_diagnostic_passed"] is False
    assert "phase4_short_smoke_not_passed" in payload["decision"]["vetoes"]
    assert payload["inference_status"]["hmc_readiness"].startswith("not assessed")
    assert any("not HMC convergence" in item for item in payload["nonclaims"])


def test_aggregate_seed_rows_is_descriptive_only() -> None:
    harness = _load_harness()
    rows = [
        {
            "status": "passed_short_smoke",
            "trace_summary": {
                "acceptance_rate": 1.0,
                "target_log_prob": {"min": -2.0, "max": -1.0},
                "log_accept_ratio": {"max_abs_finite": 0.1},
                "native_divergence": {"available": False, "status": "not_exposed_by_kernel"},
            },
            "samples_summary": {
                "finite_sample_count": 16,
                "nonfinite_sample_count": 0,
                "max_abs_u": 1.5,
            },
        }
    ]

    aggregate = harness.aggregate_seed_rows(rows)

    assert aggregate["passed_seed_count"] == 1
    assert aggregate["acceptance_rates"] == [1.0]
    assert aggregate["finite_sample_counts"] == [16]
    assert aggregate["statistical_interpretation"].startswith("descriptive only")


def test_current_phase4_artifact_validates_if_available() -> None:
    if not PHASE4_PATH.exists():
        return
    harness = _load_harness()
    phase4 = json.loads(PHASE4_PATH.read_text(encoding="utf-8"))

    audit = harness.validate_phase4_artifact(phase4)

    assert audit["phase4_precondition_passed"] is True
    assert audit["vetoes"] == ()
