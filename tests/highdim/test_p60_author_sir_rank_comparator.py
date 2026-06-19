from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim

FIT_SAMPLE_COUNT = highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT


def test_p59_author_sir_step_assembly_accepts_explicit_rank_one_default() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
        fit_rank=1,
    )

    assert result.status == highdim.P59_9B_PASS_STATUS
    assert result.manifest["fit_rank"] == 1
    assert result.manifest["rank_tuple"] == (1,) * 37


def test_p59_author_sir_prep_can_build_rank_two_fit_artifact() -> None:
    result = highdim.p59_author_sir_36d_target_fit_prep(
        sample_count=2,
        fit_rank=2,
    )

    assert result.status == highdim.P59_9A_PASS_STATUS
    assert result.manifest["fit_rank"] == 2
    assert result.manifest["rank_tuple"] == (1,) + (2,) * 35 + (1,)


def test_p60_rank_comparator_preserves_high_rank_condition_veto() -> None:
    result = highdim.p60_author_sir_same_route_rank_comparator(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )

    assert result.low_result is not None
    assert result.low_result.status == highdim.P59_9B_PASS_STATUS
    assert (
        "candidate_high_exception_P70FixedFitDiagnosticError_fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO"
        in result.blockers
    )
    assert result.high_result is None
    assert result.manifest["candidate_low"]["fit_degree"] == 0
    assert result.manifest["candidate_low"]["fit_rank"] == 1
    assert result.manifest["candidate_high"] is None
    assert "no d18 correctness candidate claim" in result.manifest["nonclaims"]
    assert "no d50 or d100 scaling claim" in result.manifest["nonclaims"]


def test_p65_rank_comparator_blocks_high_rank_sqrt_tt_signature_when_vetoed() -> None:
    result = highdim.p60_author_sir_same_route_rank_comparator(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
        low_fit_degree=0,
        high_fit_degree=1,
        low_fit_rank=1,
        high_fit_rank=2,
    )

    assert result.status == highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    assert any("CONDITION_NUMBER_VETO" in blocker for blocker in result.blockers)
    assert "sqrt_tt_core_diagnostics" not in result.manifest
    assert result.manifest["candidate_high"] is None


def test_p65_high_rank_branch_returns_no_mass_claim_when_vetoed() -> None:
    result = highdim.p60_author_sir_same_route_rank_comparator(
        sample_count=1,
        fit_sample_count=FIT_SAMPLE_COUNT,
        low_fit_degree=0,
        high_fit_degree=1,
        low_fit_rank=1,
        high_fit_rank=2,
    )

    assert result.status == highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    assert any("CONDITION_NUMBER_VETO" in blocker for blocker in result.blockers)
    assert "normalizer_decomposition" not in result.manifest
    assert result.manifest["candidate_high"] is None


def test_p60_rank_comparator_rejects_non_stronger_high_rank() -> None:
    result = highdim.p60_author_sir_same_route_rank_comparator(
        low_fit_rank=1,
        high_fit_rank=1,
    )

    assert result.status == highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    assert "high_fit_rank_must_exceed_low_fit_rank" in result.blockers


def test_p60_rank_comparator_rejects_incoherent_pass_payload() -> None:
    with pytest.raises(ValueError, match="requires low and high"):
        highdim.P60AuthorSIRSameRouteRankComparatorResult(
            status=highdim.P60_D18_RANK_CONVERGENCE_PASS_STATUS,
            blockers=(),
            low_result=None,
            high_result=None,
            manifest={},
        )
