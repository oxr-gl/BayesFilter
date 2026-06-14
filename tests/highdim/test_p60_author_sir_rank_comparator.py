from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def test_p59_author_sir_step_assembly_accepts_explicit_rank_one_default() -> None:
    result = highdim.p59_author_sir_step_spec_assembly(
        sample_count=1,
        fit_sample_count=2,
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


def test_p60_rank_comparator_fails_closed_on_high_rank_defensive_only_collapse() -> None:
    result = highdim.p60_author_sir_same_route_rank_comparator(
        sample_count=1,
        fit_sample_count=2,
    )

    assert result.status == highdim.P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
    assert result.low_result is not None
    assert result.low_result.status == highdim.P59_9B_PASS_STATUS
    assert result.high_result is not None
    assert result.high_result.status == highdim.P59_9B_PASS_STATUS
    assert "candidate_high_defensive_only_transport" in result.blockers
    assert (
        result.manifest["normalizer_decomposition"][
            "candidate_high_defensive_only_steps"
        ]
        == (1, 2)
    )
    assert result.manifest["candidate_low"]["fit_degree"] == 0
    assert result.manifest["candidate_low"]["fit_rank"] == 1
    assert result.manifest["candidate_high"]["fit_rank"] == 2
    assert (
        result.manifest["candidate_high"]["defensive_tau"]
        == highdim.P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU
    )
    assert not any("NORMALIZER_FLOOR_EXCEEDED" in blocker for blocker in result.blockers)
    assert "no d18 correctness candidate claim" in result.manifest["nonclaims"]
    assert "no d50 or d100 scaling claim" in result.manifest["nonclaims"]


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
