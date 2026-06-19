from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route


def _load_phase6_script():
    script_path = (
        Path(__file__).resolve().parents[2]
        / "scripts"
        / "p70_phase6_rank_channel_normalizer_diagnostic.py"
    )
    spec = importlib.util.spec_from_file_location("p70_phase6_diagnostic", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _convention():
    return highdim.MeasureConvention(
        density_measure=highdim.DensityMeasure.REFERENCE_MEASURE,
        mass_measure=highdim.MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="uniform",
    )


def _passing_step(time_index: int = 1):
    return {
        "time_index": time_index,
        "rank_channel_summary": {"active_channel_count": 2},
        "degree_activity_summary": {"basis_dim": 2},
        "fit_target_stats": {"rms": 2.0, "std": 0.5, "mean": 1.0, "max_abs": 3.0},
        "fit_quality": {
            "status": source_route.HighDimStatus.OK.value,
            "fit_residual": 0.1,
            "p70_fixed_fitting_policy": {
                "row_adequacy": {"status": "ok"},
                "channel_activity": {"status": "ok"},
            },
        },
        "condition_summary": {
            "condition_veto_core_indices": (),
            "condition_warning_core_indices": (),
        },
        "holdout_replay_diagnostics": {
            "holdout_available": True,
            "holdout_nonfinite": False,
            "holdout_disjoint_from_fit": True,
            "holdout_residual": 3.0,
            "replay_available": True,
            "replay_nonfinite": False,
            "replay_disjoint_from_fit": True,
            "replay_residual": 4.0,
            "branch_identity_unchanged_by_diagnostics": True,
        },
        "normalizer_terms": {
            "mixture_normalizer": 2.0,
            "sqrt_tt_normalizer": 1.5,
            "log_transport_normalizer": 0.25,
            "defensive_tau": 1e-8,
        },
    }


def _passing_row(label: str = "rank_candidate_1_2_fit36"):
    return {
        "label": label,
        "status": source_route.P59_9B_PASS_STATUS,
        "fit_initialization_rule": source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
        "fixed_branch_adaptation_class": source_route.P65_FIXED_BRANCH_ADAPTATION_CLASS,
        "step_diagnostics": [_passing_step(1), _passing_step(2)],
    }


def _captured_error_payload():
    return {
        "message": "fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO",
        "fit_status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
        "termination_reason": "condition_number_veto",
        "stop_condition_triggered": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
        "fit_quality_diagnostics": {
            "status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
            "per_core_update_statuses": (
                {
                    "status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
                    "core_index": 0,
                    "sweep_index": 0,
                    "n_rows": 36,
                    "n_cols": 4,
                    "condition_number": 1e16,
                    "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
                },
            ),
            "p70_fixed_fitting_policy": {
                "row_adequacy": {"status": "ok"},
                "channel_activity": {"status": "ok"},
            },
        },
        "core_update_statuses": (
            {
                "status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
                "core_index": 0,
                "sweep_index": 0,
                "n_rows": 36,
                "n_cols": 4,
                "condition_number": 1e16,
                "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
            },
        ),
        "p70_fixed_fitting_policy": {
            "row_adequacy": {"status": "ok"},
            "channel_activity": {"status": "ok"},
        },
        "fit_branch_hash": "failed-hash",
        "rank_tuple": (1, 2, 1),
        "fit_degree": 1,
        "fit_rank": 2,
        "target_dim": 2,
        "initialization_rule": source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
        "ridge": source_route.P70_FIT_RIDGE,
        "max_sweeps": source_route.P70_FIXED_BRANCH_MAX_SWEEPS,
        "sweep_order": (0, 1, 1, 0),
        "condition_number_warning": source_route.P70_CONDITION_NUMBER_WARNING,
        "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
        "failed_fit_remains_inadmissible": True,
        "transport_returned": False,
        "nonclaims": ("failed fit is not admissible",),
    }


def _captured_error():
    return source_route.P70FixedFitDiagnosticError(
        "fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO",
        status=source_route.HighDimStatus.CONDITION_NUMBER_VETO,
        payload=_captured_error_payload(),
    )


def test_p70_phase6_gate_summary_passes_complete_synthetic_row():
    module = _load_phase6_script()

    summary = module.p70_phase6_gate_summary({"row": _passing_row()})

    assert summary["overall_status"] == "pass"
    assert summary["veto_status"]["any_veto_failed"] is False
    row_gate = summary["primary_criterion_status_by_row"][0]
    assert row_gate["status"] == "pass"
    assert row_gate["step_gates"][0]["holdout_replay"]["holdout"]["normalized_residual"] == 1.5
    assert row_gate["step_gates"][0]["holdout_replay"]["replay"]["normalized_residual"] == 2.0


def test_p70_phase6_gate_summary_fails_missing_p70_policy():
    module = _load_phase6_script()
    row = _passing_row()
    row["step_diagnostics"][0]["fit_quality"].pop("p70_fixed_fitting_policy")

    summary = module.p70_phase6_gate_summary({"row": row})

    assert summary["overall_status"] == "fail"
    first_step = summary["primary_criterion_status_by_row"][0]["step_gates"][0]
    assert first_step["status"] == "fail"
    assert "row_adequacy_missing" in first_step["reasons"]
    assert "rank_channel_activity_failed" in first_step["reasons"]


def test_p70_phase6_gate_summary_fails_holdout_normalized_residual_veto():
    module = _load_phase6_script()
    row = _passing_row()
    row["step_diagnostics"][1]["holdout_replay_diagnostics"]["holdout_residual"] = 25.0

    summary = module.p70_phase6_gate_summary({"row": row})

    assert summary["overall_status"] == "fail"
    second_step = summary["primary_criterion_status_by_row"][0]["step_gates"][1]
    assert second_step["status"] == "fail"
    assert "holdout_normalized_residual_veto" in second_step["reasons"]
    assert second_step["holdout_replay"]["holdout"]["normalized_residual"] == 12.5


def test_p70_phase6_gate_accepts_source_route_sqrt_square_normalizer_schema():
    module = _load_phase6_script()
    row = _passing_row()
    for step in row["step_diagnostics"]:
        normalizer = step["normalizer_terms"]
        normalizer["sqrt_square_normalizer"] = normalizer.pop("sqrt_tt_normalizer")

    summary = module.p70_phase6_gate_summary({"row": row})

    assert summary["overall_status"] == "pass"
    first_step = summary["primary_criterion_status_by_row"][0]["step_gates"][0]
    assert first_step["normalizer_ok"] is True
    assert "missing_sqrt_tt_normalizer" not in first_step["reasons"]


def test_p70_phase6_gate_accepts_finite_numpy_scalar_residuals():
    module = _load_phase6_script()
    row = _passing_row()
    diagnostics = row["step_diagnostics"][0]["holdout_replay_diagnostics"]
    diagnostics["holdout_residual"] = np.float64(3.0)
    diagnostics["replay_residual"] = np.array(4.0)

    summary = module.p70_phase6_gate_summary({"row": row})

    assert summary["overall_status"] == "pass"
    first_step = summary["primary_criterion_status_by_row"][0]["step_gates"][0]
    holdout_replay = first_step["holdout_replay"]
    assert "holdout_residual_nonfinite" not in first_step["reasons"]
    assert "replay_residual_nonfinite" not in first_step["reasons"]
    assert holdout_replay["holdout"]["raw_residual"] == 3.0
    assert holdout_replay["holdout"]["normalized_residual"] == 1.5
    assert holdout_replay["replay"]["raw_residual"] == 4.0
    assert holdout_replay["replay"]["normalized_residual"] == 2.0


def test_p70_phase6_gate_summary_fails_condition_veto():
    module = _load_phase6_script()
    row = _passing_row()
    row["step_diagnostics"][0]["condition_summary"]["condition_veto_core_indices"] = (3,)

    summary = module.p70_phase6_gate_summary({"row": row})

    assert summary["overall_status"] == "fail"
    first_step = summary["primary_criterion_status_by_row"][0]["step_gates"][0]
    assert "condition_number_veto" in first_step["reasons"]


def test_p70_phase6_gate_summary_fails_captured_failed_fit():
    module = _load_phase6_script()
    failed = module._failed_row_payload(
        label="rank_candidate_1_2_fit36",
        degree=1,
        rank=2,
        fit_sample_count=36,
        error=_captured_error(),
    )

    summary = module.p70_phase6_gate_summary({"rank_candidate_1_2_fit36": failed})

    assert summary["overall_status"] == "fail"
    row_gate = summary["primary_criterion_status_by_row"][0]
    assert "captured_failed_fit" in row_gate["reasons"]
    assert row_gate["failed_fit_diagnostics"]["fit_status"] == (
        source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
    )
    assert failed["transport_returned"] is False
    assert failed["success_payload_emitted"] is False


def test_p70_phase6_run_rows_stops_after_first_captured_failure(tmp_path):
    module = _load_phase6_script()
    calls = []

    def row_builder(label, degree, rank, fit_sample_count):
        calls.append(label)
        raise _captured_error()

    output = tmp_path / "phase6.json"
    exit_status, rows, payload = module._run_rows(
        row_specs=(
            ("first", 1, 2, 36),
            ("second", 1, 3, 36),
        ),
        row_builder=row_builder,
        output=output,
        command="test command",
    )

    assert exit_status == 1
    assert calls == ["first"]
    assert tuple(rows) == ("first",)
    assert payload["status"] == "P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT"
    assert payload["gate_summary"]["continued_after_failed_row"] is False
    assert payload["rows"]["first"]["transport_returned"] is False
    assert payload["rows"]["first"]["success_payload_emitted"] is False
    assert output.exists()


def test_source_route_failed_fit_raises_diagnostic_error(monkeypatch):
    class StubHash:
        value = "failed-branch"

    class StubResult:
        status = source_route.HighDimStatus.CONDITION_NUMBER_VETO
        termination_reason = "condition_number_veto"
        stop_condition_triggered = source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
        branch_hash = StubHash()
        core_update_statuses = (
            {
                "status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
                "core_index": 0,
                "sweep_index": 0,
                "n_rows": 3,
                "n_cols": 2,
                "condition_number": 1e20,
                "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
            },
        )
        fit_residual = None
        holdout_residual = None
        diagnostics = {
            "status": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
            "termination_reason": "condition_number_veto",
            "stop_condition_triggered": source_route.HighDimStatus.CONDITION_NUMBER_VETO.value,
        }
        fitted_tt = highdim.FunctionalTT(
            [
                highdim.TTCore(tf.ones([1, 2, 1], dtype=tf.float64)),
                highdim.TTCore(tf.ones([1, 2, 1], dtype=tf.float64)),
            ],
            highdim.ProductBasis(
                [
                    highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
                    highdim.LegendreBasis1D(highdim.BoundedInterval(-1.0, 1.0), 1),
                ],
                _convention(),
            ),
            _convention(),
        )

    class StubFitter:
        def fit(self, **_kwargs):
            return StubResult()

    monkeypatch.setattr(source_route, "FixedTTFitter", lambda: StubFitter())

    with pytest.raises(source_route.P70FixedFitDiagnosticError) as exc_info:
        source_route._p59_fixed_ttsirt_transport_from_values(
            local_fit_points=tf.ones([2, 4], dtype=tf.float64),
            target_values=tf.ones([4], dtype=tf.float64),
            fit_weights=tf.ones([4], dtype=tf.float64),
            target_dim=2,
            fit_degree=1,
            fit_rank=1,
            ridge=source_route.P70_FIT_RIDGE,
            branch_seed="stub",
            convention=_convention(),
        )

    err = exc_info.value
    assert str(err) == "fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO"
    assert err.status is source_route.HighDimStatus.CONDITION_NUMBER_VETO
    assert err.payload["fit_status"] == source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
    assert err.payload["transport_returned"] is False
    assert err.payload["failed_fit_remains_inadmissible"] is True
    assert err.payload["core_update_statuses"][0]["n_rows"] == 3
    assert err.payload["p70_fixed_fitting_policy"]["row_adequacy"]["status"] == "ok"


def test_p70_phase6_default_command_and_output_are_p70_scoped():
    module = _load_phase6_script()

    assert "p70_phase6_rank_channel_normalizer_diagnostic.py" in module.EXPECTED_COMMAND
    assert "p70-phase6-rank-channel-normalizer-diagnostics" in str(module.DEFAULT_OUTPUT)
    assert "p69_phase5c" not in module.EXPECTED_COMMAND
