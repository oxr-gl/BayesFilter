from __future__ import annotations

import math

import pytest

import bayesfilter.highdim as highdim

FIT_SAMPLE_COUNT = highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT


def test_p59_9e_passes_d18_execution_only_after_9d() -> None:
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_execution_only",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9E_D18_EXECUTION_ONLY_PASS_STATUS
    assert result.tier == "d18_execution_only"
    assert result.runner_result is not None
    assert result.runner_result.status == highdim.P59_9D_PASS_STATUS
    assert result.manifest["prerequisite_tokens"]["p59_9d"] == highdim.P59_9D_PASS_STATUS
    assert result.manifest["prerequisite_tokens"]["p58_readiness"] == highdim.P58_M9_READY_STATUS
    assert result.manifest["step_count"] == 2
    assert result.manifest["target_dimension"] == 36
    assert result.manifest["fit_sample_count"] == FIT_SAMPLE_COUNT
    assert all(
        row["row_count"] == FIT_SAMPLE_COUNT
        and row["status"] != "branch_fit_row_adequacy_failed"
        for row in result.manifest["row_adequacy_by_step"]
    )
    assert math.isfinite(result.manifest["log_marginal_likelihood"])
    assert len(result.manifest["effective_sample_size_by_step"]) == 2


def test_p59_9e_execution_only_preserves_nonclaims_and_blocks_higher_tiers() -> None:
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_execution_only",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert "no d18 filtering accuracy claim" in result.manifest["nonclaims"]
    assert "no same-route rank convergence claim" in result.manifest["nonclaims"]
    assert "no d50 or d100 scaling claim" in result.manifest["nonclaims"]
    assert (
        result.manifest["blocked_higher_tiers"]["d18_same_route_rank_convergence"]
        == "missing_higher_rank_same_route_comparator"
    )
    assert (
        result.manifest["blocked_higher_tiers"]["d18_correctness_candidate"]
        == "missing_same_target_reference_or_bridge"
    )


def test_p59_9e_diagnostics_are_manifested_as_diagnostic_only() -> None:
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_execution_only",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    diagnostics = result.manifest["holdout_replay_diagnostics_by_step"]
    assert diagnostics
    assert all(
        row["warning_status"] == highdim.P69_HOLDOUT_REPLAY_DIAGNOSTIC_ONLY_STATUS
        for row in diagnostics
    )
    assert all(
        "holdout/replay residuals are not filtering correctness"
        in row["nonclaims"]
        for row in diagnostics
    )
    assert "no d18 filtering accuracy claim" in result.manifest["nonclaims"]


def test_p59_9e_blocks_same_route_rank_convergence_without_comparator() -> None:
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_same_route_rank_convergence",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9E_BLOCK_STATUS
    assert "missing_higher_rank_same_route_comparator" in result.blockers


def test_p59_9e_blocks_correctness_candidate_without_reference() -> None:
    result = highdim.p59_author_sir_validation_ladder(
        tier="d18_correctness_candidate",
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.status == highdim.P59_9E_BLOCK_STATUS
    assert "missing_same_target_reference_or_bridge" in result.blockers


def test_p59_9e_explicit_under_rowed_fit_count_fails_closed() -> None:
    with pytest.raises(ValueError, match="branch_fit_row_adequacy_failed"):
        highdim.p59_author_sir_validation_ladder(
            tier="d18_execution_only",
            sample_count=1,
            fit_sample_count=2,
        )


def test_p59_9e_rejects_incoherent_pass_payload() -> None:
    with pytest.raises(ValueError, match="requires P59-9d pass"):
        highdim.P59AuthorSIRValidationLadderResult(
            status=highdim.P59_9E_D18_EXECUTION_ONLY_PASS_STATUS,
            blockers=(),
            tier="d18_execution_only",
            runner_result=None,
            manifest={},
        )
