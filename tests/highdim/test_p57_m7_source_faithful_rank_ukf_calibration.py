from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _evidence(
    rank: int,
    *,
    comparator_kind: str = "dense_lower_rung",
    comparator_rank: int | None = None,
    ll_error: float = 5e-4,
    mean_error: float = 2e-2,
    cov_error: float = 5e-2,
    replay: float = 0.0,
    gradient: bool = False,
    gradient_cosine: float = 0.999,
    gradient_score_error: float = 2e-2,
) -> highdim.P57RankComparatorEvidence:
    kwargs = {
        "rank": rank,
        "comparator_kind": comparator_kind,
        "per_observation_log_likelihood_error": ll_error,
        "filtered_mean_scaled_rmse": mean_error,
        "covariance_relative_frobenius_error": cov_error,
        "replay_residual": replay,
        "comparator_rank": comparator_rank,
        "gradient_reference_available": gradient,
    }
    if gradient:
        kwargs["gradient_directional_cosine"] = gradient_cosine
        kwargs["gradient_relative_score_error"] = gradient_score_error
    return highdim.P57RankComparatorEvidence(**kwargs)


def test_p57_m7_author_rank_ladder_and_memory_terms_are_source_route_specific() -> None:
    assert highdim.P57_AUTHOR_SIR_D18_RANK_LADDER == (10, 20, 40)
    assert highdim.p57_fixed_ttsirt_memory_terms() == (
        "tt_cores",
        "mass_contractions",
        "cdf_kr_state",
        "sample_batches",
        "autodiff_workspace",
        "retained_objects",
    )
    tolerances = highdim.p57_rank_promotion_tolerances()
    assert tolerances["per_observation_log_likelihood_error"] == pytest.approx(1e-3)
    assert tolerances["filtered_mean_scaled_rmse"] == pytest.approx(5e-2)
    assert tolerances["covariance_relative_frobenius_error"] == pytest.approx(1e-1)
    assert tolerances["gradient_directional_cosine_min"] == pytest.approx(0.995)
    assert "never largest-rank self-promotion" in tolerances["promotion_rule"]


def test_p57_m7_selects_smallest_feasible_source_rank_with_comparator() -> None:
    result = highdim.p57_select_source_faithful_rank(
        candidate_ranks=(10, 20, 40),
        feasible_ranks=(10, 20, 40),
        evidence=(
            _evidence(10, ll_error=2e-3),
            _evidence(20),
            _evidence(40),
        ),
    )
    payload = result.manifest_payload()

    assert result.status == "PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION"
    assert result.selected_rank == 20
    assert payload["claim_class"] == highdim.P57_SOURCE_FAITHFUL_RANK_POLICY_CLAIM
    assert payload["ukf_role"] == highdim.P57_UKF_DIAGNOSTIC_ROLE
    assert payload["ukf_claim_class"] == highdim.P57_ALLOWED_UKF_CLAIM_CLASS
    assert "no filtering correctness" in payload["nonclaims"]
    assert "UKF is diagnostic only" in payload["nonclaims"]


def test_p57_m7_blocks_without_dense_or_higher_rank_comparator() -> None:
    result = highdim.p57_select_source_faithful_rank(
        candidate_ranks=(10, 20, 40),
        feasible_ranks=(10, 20, 40),
        evidence=(
            highdim.P57RankComparatorEvidence(
                rank=10,
                comparator_kind="none",
                per_observation_log_likelihood_error=None,
                filtered_mean_scaled_rmse=None,
                covariance_relative_frobenius_error=None,
                replay_residual=None,
            ),
        ),
    )

    assert result.status == "BLOCK_P57_M7_RANK_COMPARATOR_MISSING"
    assert result.selected_rank is None
    assert "comparator" in result.blocker


def test_p57_m7_blocks_when_comparator_fails_value_or_gradient_tolerance() -> None:
    value_fail = highdim.p57_select_source_faithful_rank(
        candidate_ranks=(10, 20, 40),
        feasible_ranks=(10, 20, 40),
        evidence=(_evidence(10, mean_error=0.2),),
    )
    gradient_fail = highdim.p57_select_source_faithful_rank(
        candidate_ranks=(10, 20, 40),
        feasible_ranks=(10, 20, 40),
        evidence=(
            _evidence(
                10,
                gradient=True,
                gradient_cosine=0.99,
                gradient_score_error=1e-2,
            ),
        ),
    )

    assert value_fail.status == "BLOCK_P57_M7_RANK_TOLERANCE_FAILURE"
    assert gradient_fail.status == "BLOCK_P57_M7_RANK_TOLERANCE_FAILURE"


def test_p57_m7_same_route_comparator_must_be_higher_rank() -> None:
    ok = _evidence(
        20,
        comparator_kind="same_route_higher_rank",
        comparator_rank=40,
    )
    assert ok.passes_promotion_rule

    with pytest.raises(ValueError, match="higher rank"):
        _evidence(
            20,
            comparator_kind="same_route_higher_rank",
            comparator_rank=20,
        )


def test_p57_m7_rejects_old_local_operator_or_ukf_promotion() -> None:
    with pytest.raises(ValueError, match="fixed_ttsirt_source_route"):
        highdim.P57RankComparatorEvidence(
            rank=10,
            route_class="scaling_route",
            comparator_kind="dense_lower_rung",
            per_observation_log_likelihood_error=1e-4,
            filtered_mean_scaled_rmse=1e-2,
            covariance_relative_frobenius_error=1e-2,
            replay_residual=0.0,
        )

    with pytest.raises(ValueError, match="UKF"):
        highdim.p57_select_source_faithful_rank(
            candidate_ranks=(10, 20, 40),
            feasible_ranks=(10, 20, 40),
            evidence=(_evidence(10),),
            ukf_claim_class="correctness oracle",
        )
