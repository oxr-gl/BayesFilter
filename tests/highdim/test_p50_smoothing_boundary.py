from __future__ import annotations

import json
from pathlib import Path

import pytest

import bayesfilter.highdim as highdim


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-result-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p50_m8_manifest_defers_smoothing_without_smoothing_token() -> None:
    manifest = _manifest()
    decision = manifest["decision"]

    assert manifest["schema_version"] == "p50.smoothing_boundary.v1"
    assert decision["smoothing_required_for_p50_parameter_hmc"] is False
    assert decision["smoothing_status"] == "deferred"
    assert decision["gate_status"] == "PASS_P50_M8_SMOOTHING_BOUNDARY"
    assert (
        decision["gate_meaning"]
        == "boundary_and_overclaim_guards_passed_no_smoothing_support_claim"
    )
    assert manifest["dedicated_smoothing_tokens"] == []


def test_p50_m8_filtering_tokens_are_not_smoothing_evidence() -> None:
    manifest = _manifest()
    filtering_tokens = manifest["filtering_tokens_not_smoothing_evidence"]
    rule = manifest["promotion_rule"]

    assert "PASS_P50_M2_ONE_STEP_VALUE_PATH" in filtering_tokens
    assert "PASS_P50_M3_SEQUENTIAL_LIKELIHOOD_PATH" in filtering_tokens
    assert "PASS_P50_M7_HMC_READINESS_TIERS" in filtering_tokens
    assert rule["filtering_likelihood_pass_is_not_smoothing_support"] is True
    assert rule["parameter_hmc_filtering_does_not_require_latent_path_smoothing"] is True


def test_p50_m8_boundary_contract_requires_backward_fields() -> None:
    manifest = _manifest()
    boundary = highdim.SourceRouteSmoothingBoundary(
        smoothing_status="deferred",
        required_backward_fields=tuple(manifest["required_backward_fields_for_any_future_smoother"]),
        filtering_tokens=tuple(manifest["filtering_tokens_not_smoothing_evidence"]),
        dedicated_smoothing_tokens=tuple(manifest["dedicated_smoothing_tokens"]),
        non_claims=tuple(manifest["nonclaims"]),
    )
    payload = boundary.manifest_payload()

    assert payload["smoothing_status"] == "deferred"
    assert payload["filtering_tokens_are_smoothing_evidence"] is False
    assert "backward_conditional_maps" in payload["required_backward_fields"]
    assert "backward_weights" in payload["required_backward_fields"]


def test_p50_m8_deferred_smoothing_cannot_emit_smoother_pass() -> None:
    manifest = _manifest()

    with pytest.raises(ValueError, match="deferred smoothing cannot carry"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=tuple(
                manifest["required_backward_fields_for_any_future_smoother"]
            ),
            filtering_tokens=tuple(manifest["filtering_tokens_not_smoothing_evidence"]),
            dedicated_smoothing_tokens=("PASS_P50_DEDICATED_SMOOTHER",),
            non_claims=tuple(manifest["nonclaims"]),
        )


def test_p50_m8_result_token_is_present_once_and_nonclaims_are_explicit() -> None:
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert result.count("PASS_P50_M8_SMOOTHING_BOUNDARY") == 1
    assert "No smoothing support" in result
    assert "No latent-path posterior inference" in result
    assert "No HMC readiness" in result
    assert "No source-faithful adaptive TT/SIRT filtering" in result
    assert "No S&P 500 reproduction" in result
