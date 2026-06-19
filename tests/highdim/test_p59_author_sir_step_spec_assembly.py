from __future__ import annotations

import math

import pytest

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route
from scripts import p67_author_sir_adjacent_ladder_diagnostics as p67_runner
from scripts import p71_phase4d_validate_ladder_artifact as phase4d_validator

FIT_SAMPLE_COUNT = highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT


def _as_float(value: object) -> float:
    if hasattr(value, "numpy"):
        value = value.numpy()
        if getattr(value, "shape", ()) == ():
            value = value.item()
    return float(value)


def test_p59_9b_assembles_two_author_sir_36d_step_specs() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=2,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9B_PASS_STATUS
    assert result.ready_for_runner_manifest_path is True
    assert result.route_decision.route_decision == highdim.P59_9C_FULL_ROUTE_SELECTED
    assert result.prep_result is not None
    assert result.prep_result.status == highdim.P59_9A_PASS_STATUS
    assert len(result.step_specs) == 2
    assert result.manifest["target_dimension"] == highdim.P59_9A_AUTHOR_SIR_TARGET_DIMENSION
    assert result.manifest["source_target_order"] == "[theta, x_t, x_{t-1}]"
    assert result.manifest["fit_data_mode"] == highdim.P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE
    assert tuple(row["time_index"] for row in result.manifest["fit_data_manifests"]) == (1, 2)
    assert all(
        row["coordinate_frame_source"] == "source_computeL_weighted_augmented_samples"
        for row in result.manifest["fit_data_manifests"]
    )
    assert all(
        row["fixed_variant_resampling"] == highdim.P63_AUTHOR_SIR_FIXED_VARIANT_RESAMPLING
        for row in result.manifest["fit_data_manifests"]
    )
    assert result.manifest["transport_source_contract_levels"] == (
        "fixed_ttsirt",
        "fixed_ttsirt",
    )
    fit_quality = result.manifest["fit_quality_diagnostics_by_step"]
    assert len(fit_quality) == 2
    for row in fit_quality:
        assert row["status"] == highdim.HighDimStatus.OK.value
        assert row["fit_residual_available"] is True
        assert row["fit_residual"] is not None
        assert row["holdout_available"] is False
        assert row["holdout_status"] == "not_supplied"
        assert row["condition_number_summary"]["available"] is True
        assert row["condition_number_summary"]["condition_number_warning"] == pytest.approx(
            source_route.P70_CONDITION_NUMBER_WARNING
        )
        assert row["condition_number_summary"]["condition_number_veto"] == pytest.approx(
            source_route.P70_CONDITION_NUMBER_VETO
        )
        assert row["condition_number_summary"]["condition_veto_core_indices"] == ()
        assert row["per_core_update_statuses"]
    holdout_replay = result.manifest["holdout_replay_diagnostics_by_step"]
    assert len(holdout_replay) == 2
    for row in holdout_replay:
        assert row["diagnostic_role"] == "post_fit_diagnostic_only"
        assert row["diagnostic_classification"] == highdim.P65_FIXED_BRANCH_ADAPTATION_CLASS
        assert row["status"] == highdim.P69_HOLDOUT_REPLAY_AVAILABLE_STATUS
        assert row["warning_status"] == highdim.P69_HOLDOUT_REPLAY_DIAGNOSTIC_ONLY_STATUS
        assert row["holdout_available"] is True
        assert row["holdout_residual_available"] is True
        assert math.isfinite(_as_float(row["holdout_residual"]))
        assert row["replay_available"] is True
        assert row["replay_residual_available"] is True
        assert math.isfinite(_as_float(row["replay_residual"]))
        assert row["branch_identity_unchanged_by_diagnostics"] is True
        assert (
            row["fit_branch_hash_before_diagnostic"]
            == row["fit_branch_hash_after_diagnostic"]
        )
        assert (
            row["density_branch_hash_before_diagnostic"]
            == row["density_branch_hash_after_diagnostic"]
        )
        assert row["source_route_invariants"]["route_mismatch"] is False
    assert result.manifest["time2_previous_marginal_present"] is True


def test_p59_9b_previous_marginal_axes_match_full_sol_ordering() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=2,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )
    spec1, spec2 = result.step_specs

    assert spec1.previous_marginal_keep_axes is None
    assert spec1.previous_marginal_input_axes is None
    assert spec1.target.coordinate_frame.dimension == 36
    assert spec2.target.coordinate_frame.dimension == 36
    assert spec2.previous_marginal_keep_axes == tuple(range(18))
    assert spec2.previous_marginal_input_axes == tuple(range(18, 36))
    assert result.sequential_result is not None
    assert result.sequential_result.steps[1].previous_marginal_density is not None
    assert result.sequential_result.steps[1].previous_marginal_density.keep_axes == tuple(
        range(18)
    )


def test_p59_9b_partial_p58_manifest_only_leaves_runner_path_blocker() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=2,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )
    partial = result.manifest["p58_partial_manifest"]
    readiness = highdim.p58_m9_source_route_pipeline_readiness(partial)

    assert readiness.status == highdim.P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS
    assert readiness.blockers == ("missing_has_m9_runner_manifest_path",)
    assert result.manifest["p58_expected_remaining_blocker"] == "missing_has_m9_runner_manifest_path"


def test_p59_9b_blocks_without_p59_9c_route_pass() -> None:
    blocked_route = highdim.P59AuthorSIRRouteDecisionResult(
        status=highdim.P59_9C_BLOCK_STATUS,
        blockers=("source_missing",),
        route_decision=highdim.P59_9C_ROUTE_DECISION_BLOCKED,
        preconditioned_route_required=False,
        preconditioned_route_status="undecided",
        source_anchors=("source.m:1",),
        manifest={"pipeline_phase": "P59-9c"},
    )

    result = highdim.p59_author_sir_step_spec_assembly(
        route_decision=blocked_route,
        sample_count=2,
        fit_sample_count=3,
    )

    assert result.status == highdim.P59_9B_BLOCK_STATUS
    assert "missing_p59_9c_route_decision_pass" in result.blockers
    assert "p59_9c_route_not_full_route_selected" in result.blockers
    assert result.ready_for_runner_manifest_path is False
    assert result.step_specs == ()
    assert result.sequential_result is None


def test_p59_9b_rejects_incoherent_result_payloads() -> None:
    route = highdim.p59_author_sir_route_decision()

    with pytest.raises(ValueError, match="pass cannot carry blockers"):
        highdim.P59AuthorSIRStepSpecAssemblyResult(
            status=highdim.P59_9B_PASS_STATUS,
            blockers=("hidden",),
            route_decision=route,
            prep_result=None,
            step_specs=(),
            sequential_result=None,
            manifest={},
        )

    with pytest.raises(ValueError, match="block requires"):
        highdim.P59AuthorSIRStepSpecAssemblyResult(
            status=highdim.P59_9B_BLOCK_STATUS,
            blockers=(),
            route_decision=route,
            prep_result=None,
            step_specs=(),
            sequential_result=None,
            manifest={},
        )


def _fit_quality_record() -> dict[str, object]:
    return {
        "status": highdim.HighDimStatus.OK.value,
        "stop_condition_triggered": "none",
        "fit_residual": 0.25,
        "fit_residual_available": True,
        "holdout_available": False,
        "holdout_status": "not_supplied",
        "condition_number_summary": {
            "max_condition_number": 10.0,
            "condition_number_warning": source_route.P70_CONDITION_NUMBER_WARNING,
            "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
            "condition_warning_core_indices": (),
            "condition_veto_core_indices": (),
        },
        "per_core_update_statuses": (
            {
                "status": highdim.HighDimStatus.OK.value,
                "condition_number": 10.0,
                "condition_number_warning": source_route.P70_CONDITION_NUMBER_WARNING,
                "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
                "condition_warning": False,
            },
        ),
    }


def _holdout_replay_record(**overrides: object) -> dict[str, object]:
    record = {
        "diagnostic_role": "post_fit_diagnostic_only",
        "diagnostic_classification": highdim.P65_FIXED_BRANCH_ADAPTATION_CLASS,
        "holdout_available": True,
        "holdout_residual_available": True,
        "holdout_residual": 0.1,
        "holdout_nonfinite": False,
        "replay_available": True,
        "replay_residual_available": True,
        "replay_residual": 0.2,
        "replay_nonfinite": False,
        "branch_identity_unchanged_by_diagnostics": True,
        "source_route_invariants": {"route_mismatch": False},
    }
    record.update(overrides)
    return record


def _budget_manifest(*records: dict[str, object]) -> dict[str, object]:
    return {
        "fit_data_manifests": tuple({"time_index": index} for index, _ in enumerate(records, start=1)),
        "fit_quality_diagnostics_by_step": tuple(_fit_quality_record() for _ in records),
        "holdout_replay_diagnostics_by_step": tuple(records),
    }


def test_p67_budget_diagnostics_accept_finite_holdout_and_replay() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(_holdout_replay_record())
    )

    assert diagnostics["missing_fit_resolution_fields"] == ()
    assert diagnostics["fit_quality_diagnostics_present"] is True
    assert diagnostics["fit_residual_unavailable_steps"] == ()
    assert diagnostics["condition_veto_steps"] == ()
    assert diagnostics["fitter_internal_holdout_unavailable_steps"] == (1,)
    assert diagnostics["holdout_unavailable_steps"] == ()
    assert diagnostics["replay_unavailable_steps"] == ()
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_AVAILABLE_STATUS
    )


def test_p67_budget_diagnostics_distinguish_missing_holdout() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(
                holdout_available=False,
                holdout_residual_available=False,
                holdout_residual=None,
            )
        )
    )

    assert diagnostics["holdout_unavailable_steps"] == (1,)
    assert diagnostics["replay_unavailable_steps"] == ()
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_MISSING_STATUS
    )


def test_p67_budget_diagnostics_distinguish_missing_replay() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(
                replay_available=False,
                replay_residual_available=False,
                replay_residual=None,
            )
        )
    )

    assert diagnostics["holdout_unavailable_steps"] == ()
    assert diagnostics["replay_unavailable_steps"] == (1,)
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_MISSING_STATUS
    )


def test_p67_budget_diagnostics_distinguish_nonfinite_holdout() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(
                holdout_available=False,
                holdout_residual_available=False,
                holdout_residual=float("nan"),
                holdout_nonfinite=True,
            )
        )
    )

    assert diagnostics["holdout_nonfinite_steps"] == (1,)
    assert diagnostics["replay_nonfinite_steps"] == ()
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_NONFINITE_STATUS
    )


def test_p67_budget_diagnostics_distinguish_nonfinite_replay() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(
                replay_available=False,
                replay_residual_available=False,
                replay_residual=float("nan"),
                replay_nonfinite=True,
            )
        )
    )

    assert diagnostics["holdout_nonfinite_steps"] == ()
    assert diagnostics["replay_nonfinite_steps"] == (1,)
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_NONFINITE_STATUS
    )


def test_p67_budget_diagnostics_treat_branch_identity_drift_as_veto() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(branch_identity_unchanged_by_diagnostics=False)
        )
    )

    assert diagnostics["branch_identity_drift_steps"] == (1,)
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_BRANCH_IDENTITY_DRIFT_STATUS
    )


def test_p67_budget_diagnostics_treat_route_mismatch_as_veto() -> None:
    diagnostics = p67_runner._budget_diagnostics(
        _budget_manifest(
            _holdout_replay_record(
                holdout_available=False,
                replay_available=False,
                source_route_invariants={"route_mismatch": True},
            )
        )
    )

    assert diagnostics["route_mismatch_steps"] == (1,)
    assert diagnostics["holdout_replay_resolution_status"] == (
        highdim.P69_HOLDOUT_REPLAY_ROUTE_MISMATCH_STATUS
    )


def test_p67_failed_fit_row_payload_preserves_p70_diagnostics() -> None:
    error = source_route.P70FixedFitDiagnosticError(
        "fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO",
        status=highdim.HighDimStatus.CONDITION_NUMBER_VETO,
        payload={
            "fit_status": highdim.HighDimStatus.CONDITION_NUMBER_VETO.value,
            "stop_condition_triggered": highdim.HighDimStatus.CONDITION_NUMBER_VETO.value,
            "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
            "transport_returned": False,
            "failed_fit_remains_inadmissible": True,
            "core_update_statuses": (
                {
                    "status": highdim.HighDimStatus.CONDITION_NUMBER_VETO.value,
                    "condition_number": source_route.P70_CONDITION_NUMBER_VETO * 10.0,
                    "condition_number_veto": source_route.P70_CONDITION_NUMBER_VETO,
                },
            ),
        },
    )

    row = p67_runner._failed_fit_row_payload(
        label="rank_candidate_1_2_fit36",
        degree=1,
        rank=2,
        fit_sample_count=36,
        error=error,
    )

    assert row["status"] == "P67_ROW_BLOCKED_ON_FAILED_FIT"
    assert row["failed_fit_diagnostics"]["fit_status"] == (
        highdim.HighDimStatus.CONDITION_NUMBER_VETO.value
    )
    assert row["failed_fit_diagnostics"]["core_update_statuses"]
    assert row["transport_returned"] is False
    assert row["success_payload_emitted"] is False
    assert row["budget_limitation_diagnostics"]["condition_number_veto"] == (
        source_route.P70_CONDITION_NUMBER_VETO
    )
    assert row["source_invariants"]["passed"] is False


def test_p67_source_invariant_accepts_p70_seeded_channel_initializer() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=2,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    payload = p67_runner._source_invariant_payload(result)

    assert payload["expected"]["fit_initialization_rule"] == (
        source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE
    )
    assert payload["observed"]["fit_initialization_rule"] == (
        source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE
    )
    assert payload["passed"] is True
    assert payload["mismatches"] == ()


def test_phase4d_validator_enforces_frozen_rows_thresholds_and_single_admission() -> None:
    rows = {}
    for label, degree, rank, fit_count in p67_runner.ROW_SPECS:
        rows[label] = {
            **p67_runner._planned_row_payload(
                label=label,
                degree=degree,
                rank=rank,
                fit_sample_count=fit_count,
            ),
            "status": phase4d_validator.ROW_EXECUTION_PASS_STATUS,
            "budget_limited": False,
            "source_invariants": {"passed": True},
        }
    for label in rows:
        if label == "base_candidate_1_2_fit16":
            continue
        rows[label]["status"] = "P67_ROW_BLOCKED_ON_FAILED_FIT"
        rows[label]["budget_limited"] = True
    payload = {
        "rows": rows,
        "thresholds": p67_runner.THRESHOLDS,
        "rank_ladder": {"thresholds": p67_runner.THRESHOLDS},
        "degree_ladder": {"thresholds": p67_runner.THRESHOLDS},
        "run_manifest": {
            "cpu_only_intent": "CUDA_VISIBLE_DEVICES=-1",
            "fit_budgets": {
                "base_candidate": 16,
                "rank_pair": 36,
                "degree_pair": 24,
            },
            "sample_count": 1,
            "bounded_screen_only": True,
        },
    }

    assert phase4d_validator.validate_payload(payload) == ()
    rows["rank_candidate_1_2_fit36"]["status"] = (
        phase4d_validator.ROW_EXECUTION_PASS_STATUS
    )
    rows["rank_candidate_1_2_fit36"]["budget_limited"] = False

    blockers = phase4d_validator.validate_payload(payload)

    assert "admitted_configuration_count_mismatch:2" in blockers


def test_p69_aggregate_status_treats_unsupplied_channel_as_missing() -> None:
    diagnostics = source_route._p69_post_fit_holdout_replay_diagnostics(
        fit_result=type(
            "FitResult",
            (),
            {
                "branch_hash": type("Hash", (), {"value": "fit-hash"})(),
                "fitted_tt": None,
            },
        )(),
        density=type(
            "Density",
            (),
            {
                "branch_identity": type(
                    "Identity",
                    (),
                    {"hash": type("Hash", (), {"value": "density-hash"})()},
                )()
            },
        )(),
        local_fit_points=source_route.tf.zeros([1, 1], dtype=source_route.tf.float64),
        target_values=source_route.tf.zeros([1], dtype=source_route.tf.float64),
        fit_weights=source_route.tf.ones([1], dtype=source_route.tf.float64),
        fit_data_manifest={"coordinate_frame_hash": "frame-hash"},
        holdout_local_points=None,
        holdout_target_values=None,
        holdout_weights=None,
        holdout_manifest=None,
        replay_local_points=None,
        replay_target_values=None,
        replay_weights=None,
        replay_manifest=None,
    )

    assert diagnostics["status"] == highdim.P69_HOLDOUT_REPLAY_MISSING_STATUS
    assert diagnostics["source_route_invariants"]["route_mismatch"] is False
