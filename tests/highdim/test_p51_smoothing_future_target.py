from __future__ import annotations

import json
from pathlib import Path

import pytest

import bayesfilter.highdim as highdim


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-result-2026-06-09.md"
)
P50_SMOOTHING_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m8-smoothing-boundary-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p51_m7_manifest_preserves_p50_smoothing_boundary() -> None:
    manifest = _manifest()
    p50 = json.loads(P50_SMOOTHING_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "p51.smoothing_future_target.v1"
    assert manifest["status"] == "PASS_P51_M7_SMOOTHING_FUTURE_TARGET"
    assert manifest["decision"]["smoothing_status"] == "deferred"
    assert manifest["decision"]["smoothing_required_for_p51_parameter_hmc"] is False
    assert manifest["decision"]["future_program_required_for_latent_path_inference"] is True
    assert manifest["required_backward_fields_for_any_future_smoother"] == p50[
        "required_backward_fields_for_any_future_smoother"
    ]
    assert manifest["dedicated_smoothing_tokens"] == []


def test_p51_m7_filtering_and_hmc_tokens_are_not_smoothing_evidence() -> None:
    manifest = _manifest()
    tokens = manifest["p51_tokens_not_smoothing_evidence"]
    rule = manifest["promotion_rule"]

    assert "PASS_P51_M5_HMC_TIER2_LEAPFROG" in tokens
    assert "BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN" in tokens
    assert rule["filtering_likelihood_pass_is_not_smoothing_support"] is True
    assert rule["hmc_tier2_pass_is_not_smoothing_support"] is True
    assert rule["hmc_tier3_blocker_is_not_smoothing_support"] is True
    assert rule["implemented_smoothing_requires_dedicated_smoother_token"] is True


def test_p51_m7_boundary_contract_remains_deferred_and_requires_backward_fields() -> None:
    manifest = _manifest()
    boundary = highdim.SourceRouteSmoothingBoundary(
        smoothing_status=manifest["decision"]["smoothing_status"],
        required_backward_fields=tuple(manifest["required_backward_fields_for_any_future_smoother"]),
        filtering_tokens=tuple(manifest["p51_tokens_not_smoothing_evidence"]),
        dedicated_smoothing_tokens=tuple(manifest["dedicated_smoothing_tokens"]),
        non_claims=tuple(manifest["nonclaims"]),
    )
    payload = boundary.manifest_payload()

    assert payload["smoothing_status"] == "deferred"
    assert payload["filtering_tokens_are_smoothing_evidence"] is False
    assert "backward_conditional_maps" in payload["required_backward_fields"]
    assert "backward_weights" in payload["required_backward_fields"]
    assert "smoothing_marginal_checks" in payload["required_backward_fields"]


def test_p51_m7_deferred_smoothing_rejects_smoother_pass_token() -> None:
    manifest = _manifest()

    with pytest.raises(ValueError, match="deferred smoothing cannot carry"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="deferred",
            required_backward_fields=tuple(manifest["required_backward_fields_for_any_future_smoother"]),
            filtering_tokens=tuple(manifest["p51_tokens_not_smoothing_evidence"]),
            dedicated_smoothing_tokens=("PASS_P51_DEDICATED_SMOOTHER",),
            non_claims=tuple(manifest["nonclaims"]),
        )


def test_p51_m7_future_smoother_contract_requires_marginal_checks() -> None:
    manifest = _manifest()
    missing_marginal_checks = tuple(
        field
        for field in manifest["required_backward_fields_for_any_future_smoother"]
        if field != "smoothing_marginal_checks"
    )

    with pytest.raises(ValueError, match="smoothing_marginal_checks"):
        highdim.SourceRouteSmoothingBoundary(
            smoothing_status="implemented",
            required_backward_fields=missing_marginal_checks,
            filtering_tokens=tuple(manifest["p51_tokens_not_smoothing_evidence"]),
            dedicated_smoothing_tokens=("PASS_P51_DEDICATED_SMOOTHER",),
            non_claims=tuple(manifest["nonclaims"]),
        )


def test_p51_m7_result_emits_token_once_and_keeps_smoothing_nonclaims() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M7_SMOOTHING_FUTURE_TARGET") == 1
    assert "No smoothing support" in text
    assert "No latent-path posterior inference" in text
    assert "No smoother production readiness" in text
