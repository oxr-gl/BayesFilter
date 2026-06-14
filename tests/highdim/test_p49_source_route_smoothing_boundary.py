from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def test_p49_smoothing_boundary_defers_without_promoting_filtering_tokens() -> None:
    boundary = highdim.SourceRouteSmoothingBoundary(
        smoothing_status="deferred",
        required_backward_fields=(
            "backward_conditional_maps",
            "backward_weights",
            "smoothing_marginal_checks",
        ),
        filtering_tokens=(
            "PASS_P49_M2_RETAINED_TRANSPORT_OBJECT",
            "PASS_P49_M3_SAMPLE_ESS_PROPOSAL",
            "PASS_P49_M4_RECENTERING_NORMALIZER",
        ),
        dedicated_smoothing_tokens=(),
        non_claims=(
            "filtering likelihood pass is not smoothing support",
            "no backward conditional maps implemented",
        ),
    )

    payload = boundary.manifest_payload()
    assert payload["smoothing_status"] == "deferred"
    assert payload["filtering_tokens_are_smoothing_evidence"] is False
    assert "backward_conditional_maps" in payload["required_backward_fields"]
    assert "backward_weights" in payload["required_backward_fields"]


def test_p49_smoothing_boundary_rejects_deferred_smoothing_with_pass_token() -> None:
    with pytest.raises(ValueError, match="deferred smoothing cannot carry"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=(
                "backward_conditional_maps",
                "backward_weights",
                "smoothing_marginal_checks",
            ),
            filtering_tokens=("PASS_P49_M4_RECENTERING_NORMALIZER",),
            dedicated_smoothing_tokens=("PASS_SOURCE_BACKWARD_CONDITIONAL_SMOOTHER",),
            non_claims=("filtering likelihood pass is not smoothing support",),
        )


def test_p49_smoothing_boundary_requires_dedicated_token_when_implemented() -> None:
    with pytest.raises(ValueError, match="dedicated smoother token"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="implemented",
            required_backward_fields=(
                "backward_conditional_maps",
                "backward_weights",
                "smoothing_marginal_checks",
            ),
            filtering_tokens=("PASS_P49_M5_PRECONDITIONED_PREDATOR_PREY",),
            dedicated_smoothing_tokens=(),
            non_claims=("filtering likelihood pass is not smoothing support",),
        )


def test_p49_smoothing_boundary_requires_backward_conditional_fields() -> None:
    with pytest.raises(ValueError, match="backward_weights"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=(
                "backward_conditional_maps",
                "smoothing_marginal_checks",
            ),
            filtering_tokens=(),
            dedicated_smoothing_tokens=(),
            non_claims=("filtering likelihood pass is not smoothing support",),
        )

    with pytest.raises(ValueError, match="backward_conditional_maps"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=(
                "backward_weights",
                "smoothing_marginal_checks",
            ),
            filtering_tokens=(),
            dedicated_smoothing_tokens=(),
            non_claims=("filtering likelihood pass is not smoothing support",),
        )

    with pytest.raises(ValueError, match="smoothing_marginal_checks"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=(
                "backward_conditional_maps",
                "backward_weights",
            ),
            filtering_tokens=(),
            dedicated_smoothing_tokens=(),
            non_claims=("filtering likelihood pass is not smoothing support",),
        )
