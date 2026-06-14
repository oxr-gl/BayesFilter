from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def test_p59_9b_assembles_two_author_sir_36d_step_specs() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(sample_count=2, fit_sample_count=3)

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
    assert result.manifest["time2_previous_marginal_present"] is True


def test_p59_9b_previous_marginal_axes_match_full_sol_ordering() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(sample_count=2, fit_sample_count=3)
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
    result = highdim.p59_author_sir_step_spec_assembly(sample_count=2, fit_sample_count=3)
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
