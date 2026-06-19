from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim
import bayesfilter.highdim.source_route as source_route


class _FakeCandidate:
    def __init__(self, **manifest_overrides: object) -> None:
        self.status = highdim.P59_9B_PASS_STATUS
        self.blockers = ()
        self.sequential_result = object()
        self.manifest = {
            "fit_degree": 1,
            "fit_rank": 2,
            "rank_tuple": (1,) + (2,) * 35 + (1,),
            "fit_branch_hashes": ("fit-step1", "fit-step2"),
            "density_branch_hashes": ("density-step1", "density-step2"),
            "fixed_branch_adaptation_class": highdim.P65_FIXED_BRANCH_ADAPTATION_CLASS,
            "fit_initialization_rule": highdim.P65_FIXED_BRANCH_INITIALIZATION_RULE,
            "fit_data_mode": highdim.P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE,
            "defensive_tau": highdim.P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
            "target_dimension": highdim.P59_9A_AUTHOR_SIR_TARGET_DIMENSION,
            "source_target_order": "[theta, x_t, x_{t-1}]",
            "previous_marginal_keep_axes": tuple(range(18)),
            "previous_marginal_input_axes": tuple(range(18, 36)),
            "source_anchors": ("author-source-anchor",),
        }
        self.manifest.update(manifest_overrides)


def _fake_sentinel() -> highdim.P60AuthorSIRSameRouteRankComparatorResult:
    return highdim.P60AuthorSIRSameRouteRankComparatorResult(
        status=highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
        blockers=("log_marginal_delta_threshold_exceeded",),
        low_result=None,
        high_result=None,
        manifest={
            "target_id": highdim.P58_M9_AUTHOR_SIR_TARGET_ID,
            "pipeline_phase": "P60-2",
            "artifact_role": "same_route_rank_comparator",
            "status": highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
            "log_marginal_abs_delta": 12.0,
            "normalizer_increment_abs_deltas": (1.0, 10.0),
            "thresholds": {
                "log_marginal_abs_delta": 5.0,
                "normalizer_increment_abs_delta": 5.0,
            },
            "veto_blockers": ("log_marginal_delta_threshold_exceeded",),
            "nonclaims": ("no d18 correctness candidate claim",),
        },
    )


def _install_fake_route(
    monkeypatch: pytest.MonkeyPatch,
    *,
    fake_candidate: _FakeCandidate | None = None,
) -> None:
    fake_candidate = fake_candidate or _FakeCandidate()
    fake_sentinel = _fake_sentinel()
    monkeypatch.setattr(
        source_route,
        "p59_author_sir_step_spec_assembly",
        lambda **_: fake_candidate,
    )
    monkeypatch.setattr(
        source_route,
        "p60_author_sir_same_route_rank_comparator",
        lambda **_: fake_sentinel,
    )
    monkeypatch.setattr(
        source_route,
        "_p66_candidate_payload",
        lambda result, fit_sample_count: {
            "status": result.status,
            "blockers": result.blockers,
            "degree": result.manifest["fit_degree"],
            "rank": result.manifest["fit_rank"],
            "rank_tuple": result.manifest["rank_tuple"],
            "fit_sample_count": int(fit_sample_count),
            "fit_branch_hashes": result.manifest["fit_branch_hashes"],
            "density_branch_hashes": result.manifest["density_branch_hashes"],
            "square_root_normalizers_by_step": (1.2, 1.6),
            "normalizer_terms_by_step": (),
            "defensive_only_steps": (),
            "core_diagnostics_by_step": (),
            "near_zero_core_counts": (0, 0),
            "effective_sample_size_by_step": (1.0, 1.0),
            "correction_log_weight_ranges": ((0.0, 0.0), (0.0, 0.0)),
            "fixed_branch_adaptation_class": result.manifest[
                "fixed_branch_adaptation_class"
            ],
            "fit_initialization_rule": result.manifest["fit_initialization_rule"],
            "fit_data_mode": result.manifest["fit_data_mode"],
            "defensive_tau": result.manifest["defensive_tau"],
            "sample_adequacy": highdim.p66_fixed_branch_sample_adequacy(
                fit_degree=result.manifest["fit_degree"],
                fit_rank=result.manifest["fit_rank"],
                fit_sample_count=int(fit_sample_count),
            ),
            "admissibility_status": highdim.P66_CANDIDATE_ADMISSIBLE_STATUS,
        },
    )


@pytest.fixture()
def p66_contract_result(
    monkeypatch: pytest.MonkeyPatch,
) -> highdim.P66AuthorSIRFixedBranchValidationLadderResult:
    _install_fake_route(monkeypatch)
    return highdim.p66_author_sir_fixed_branch_validation_ladder(
        sample_count=1,
        sentinel_fit_sample_count=2,
        candidate_fit_sample_count=2,
        rank_ladder_fit_sample_count=2,
        degree_ladder_fit_sample_count=2,
    )


def test_p66_sample_adequacy_values_match_reviewed_table() -> None:
    candidate = highdim.p66_fixed_branch_sample_adequacy(
        fit_degree=1,
        fit_rank=2,
        fit_sample_count=16,
    )
    rank = highdim.p66_fixed_branch_sample_adequacy(
        fit_degree=1,
        fit_rank=3,
        fit_sample_count=36,
    )
    degree = highdim.p66_fixed_branch_sample_adequacy(
        fit_degree=2,
        fit_rank=2,
        fit_sample_count=24,
    )

    assert candidate["max_core_columns"] == 8
    assert candidate["diagnostic_min_fit_samples"] == 16
    assert candidate["preferred_fit_samples"] == 32
    assert rank["max_core_columns"] == 18
    assert rank["diagnostic_min_fit_samples"] == 36
    assert rank["preferred_fit_samples"] == 72
    assert degree["max_core_columns"] == 12
    assert degree["diagnostic_min_fit_samples"] == 24
    assert degree["preferred_fit_samples"] == 48


def test_p66_fixed_branch_ladder_records_schema_and_sentinel_gap(
    p66_contract_result: highdim.P66AuthorSIRFixedBranchValidationLadderResult,
) -> None:
    result = p66_contract_result
    assert result.status == highdim.P66_FIT_DESIGN_UNDERDETERMINED_BLOCK_STATUS
    assert result.candidate_result is None
    assert result.sentinel_result is not None
    assert result.sentinel_result.status == highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    assert "log_marginal_delta_threshold_exceeded" in result.sentinel_result.blockers
    assert (
        result.manifest["sentinel"]["status"]
        == highdim.P66_SENTINEL_WARN_STATUS
    )
    assert (
        result.manifest["sentinel"]["interpretation"]
        == "explanatory_sentinel_not_primary_gate"
    )
    assert (
        result.manifest["candidate"]["admissibility_status"]
        == highdim.P66_CANDIDATE_ADMISSIBLE_STATUS
    )
    assert result.manifest["candidate"]["defensive_only_steps"] == ()
    assert result.manifest["candidate"]["degree"] == 1
    assert result.manifest["candidate"]["rank"] == 2
    assert result.manifest["sample_adequacy"]["status"] == (
        highdim.P66_FIT_DESIGN_UNDERDETERMINED_BLOCK_STATUS
    )
    assert "no d18 correctness claim" in result.manifest["nonclaims"]
    assert result.manifest["old_p60_sentinel_payload"]["status"] == (
        highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    )


def test_p66_fit_budget_resolution_defaults_are_recorded() -> None:
    resolution = highdim.p66_fixed_branch_fit_budget_resolution()

    assert resolution["recorded_before_interpretation"] is True
    assert resolution["candidate"]["user_supplied_fit_sample_count"] is None
    assert resolution["candidate"]["resolved_fit_sample_count"] == 16
    assert resolution["rank_ladder"]["user_supplied_fit_sample_count"] is None
    assert resolution["rank_ladder"]["resolved_fit_sample_count"] == 36
    assert resolution["degree_ladder"]["user_supplied_fit_sample_count"] is None
    assert resolution["degree_ladder"]["resolved_fit_sample_count"] == 24


def test_p66_user_fit_budget_resolution_and_underdetermined_block() -> None:
    resolution = highdim.p66_fixed_branch_fit_budget_resolution(
        candidate_fit_sample_count=2,
        rank_ladder_fit_sample_count=2,
        degree_ladder_fit_sample_count=2,
    )

    assert resolution["candidate"]["user_supplied_fit_sample_count"] == 2
    assert resolution["candidate"]["resolved_fit_sample_count"] == 2
    assert resolution["rank_ladder"]["user_supplied_fit_sample_count"] == 2
    assert resolution["rank_ladder"]["resolved_fit_sample_count"] == 2
    assert resolution["degree_ladder"]["user_supplied_fit_sample_count"] == 2
    assert resolution["degree_ladder"]["resolved_fit_sample_count"] == 2
    assert highdim.p66_fixed_branch_sample_adequacy(
        fit_degree=1,
        fit_rank=2,
        fit_sample_count=2,
    )["status"] == (
        highdim.P66_FIT_DESIGN_UNDERDETERMINED_BLOCK_STATUS
    )


def test_p66_schema_only_adjacent_ladder_rows_have_reasons(
    p66_contract_result: highdim.P66AuthorSIRFixedBranchValidationLadderResult,
) -> None:
    result = p66_contract_result

    rank_ladder = result.manifest["rank_ladder"]
    degree_ladder = result.manifest["degree_ladder"]
    assert rank_ladder["executed"] is False
    assert rank_ladder["status"] == highdim.P66_RANK_LADDER_SCHEMA_ONLY_STATUS
    assert rank_ladder["schema_only_reason"]
    assert degree_ladder["executed"] is False
    assert degree_ladder["status"] == highdim.P66_DEGREE_LADDER_SCHEMA_ONLY_STATUS
    assert degree_ladder["schema_only_reason"]


def test_p66_comparison_invariants_authorize_only_ladder_field_changes(
    p66_contract_result: highdim.P66AuthorSIRFixedBranchValidationLadderResult,
) -> None:
    result = p66_contract_result

    rank_invariants = result.manifest["comparison_invariants"]["candidate_to_rank_ladder"]
    degree_invariants = result.manifest["comparison_invariants"]["candidate_to_degree_ladder"]
    assert rank_invariants["authorized_comparison_difference"] is True
    assert rank_invariants["authorized_comparison_difference_field"] == "fit_rank"
    assert rank_invariants["unauthorized_differences"] == ()
    assert degree_invariants["authorized_comparison_difference"] is True
    assert degree_invariants["authorized_comparison_difference_field"] == "fit_degree"
    assert degree_invariants["unauthorized_differences"] == ()


def test_p66_source_route_invariant_drift_block_result_contract() -> None:
    with pytest.raises(ValueError, match="P66 block requires"):
        highdim.P66AuthorSIRFixedBranchValidationLadderResult(
            status=highdim.P66_SOURCE_ROUTE_INVARIANT_DRIFT_BLOCK_STATUS,
            blockers=(),
            candidate_result=None,
            sentinel_result=None,
            manifest={},
        )

    result = highdim.P66AuthorSIRFixedBranchValidationLadderResult(
        status=highdim.P66_SOURCE_ROUTE_INVARIANT_DRIFT_BLOCK_STATUS,
        blockers=("target_dimension_mismatch",),
        candidate_result=None,
        sentinel_result=None,
        manifest={"status": highdim.P66_SOURCE_ROUTE_INVARIANT_DRIFT_BLOCK_STATUS},
    )

    assert result.status == highdim.P66_SOURCE_ROUTE_INVARIANT_DRIFT_BLOCK_STATUS
    assert result.blockers == ("target_dimension_mismatch",)


def test_p66_source_route_invariant_drift_blocks_function(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_route(
        monkeypatch,
        fake_candidate=_FakeCandidate(target_dimension=35),
    )

    result = highdim.p66_author_sir_fixed_branch_validation_ladder(
        sample_count=1,
        candidate_fit_sample_count=2,
        rank_ladder_fit_sample_count=2,
        degree_ladder_fit_sample_count=2,
    )

    assert result.status == highdim.P66_SOURCE_ROUTE_INVARIANT_DRIFT_BLOCK_STATUS
    assert "target_dimension_mismatch" in result.blockers
    assert result.manifest["source_invariants"]["passed"] is False


def test_p66_default_budget_ready_schema_with_synthetic_artifacts(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_fake_route(monkeypatch)

    result = highdim.p66_author_sir_fixed_branch_validation_ladder(sample_count=1)

    assert result.status == highdim.P66_FIXED_BRANCH_VALIDATION_LADDER_READY_STATUS
    assert result.manifest["fit_budget_resolution"]["candidate"][
        "resolved_fit_sample_count"
    ] == 16
    assert result.manifest["fit_budget_resolution"]["rank_ladder"][
        "resolved_fit_sample_count"
    ] == 36
    assert result.manifest["fit_budget_resolution"]["degree_ladder"][
        "resolved_fit_sample_count"
    ] == 24
    assert result.manifest["sample_adequacy"]["status"] == highdim.P66_SAMPLE_ADEQUATE_STATUS


def test_p66_execute_adjacent_ladders_requires_reviewed_experiment_plan() -> None:
    result = highdim.p66_author_sir_fixed_branch_validation_ladder(
        sample_count=1,
        candidate_fit_sample_count=2,
        rank_ladder_fit_sample_count=2,
        degree_ladder_fit_sample_count=2,
        execute_adjacent_ladders=True,
    )

    assert result.status == highdim.P66_VALIDATION_LADDER_SCOPE_BLOCK_STATUS
    assert "execute_adjacent_ladders_requires_reviewed_experiment_plan" in result.blockers
