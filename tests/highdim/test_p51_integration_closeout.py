from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m8-integration-closeout-result-2026-06-09.md"
)
HANDOFF_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-visible-stop-handoff-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p51_m8_closeout_has_all_phase_statuses_and_artifacts() -> None:
    manifest = _manifest()
    phases = manifest["phase_statuses"]

    assert manifest["schema_version"] == "p51.integration_closeout.v1"
    assert manifest["status"] == "PASS_P51_M8_INTEGRATION_CLOSEOUT"
    assert [row["phase"] for row in phases] == [f"P51-M{index}" for index in range(9)]
    expected_statuses = {
        "P51-M0": "PASS_P51_M0_GAP_SCOPE_PREFLIGHT",
        "P51-M1": "PASS_P51_M1_STABLE_SCORE_API",
        "P51-M2": "PASS_P51_M2_NATIVE_GENERALIZED_SV_REFERENCE",
        "P51-M3": "PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT",
        "P51-M4": "PASS_P51_M4_PREDATOR_PREY_PRODUCTION_TUNING",
        "P51-M5": "PASS_P51_M5_HMC_TIER2_LEAPFROG",
        "P51-M6": "BLOCK_P51_M6_HMC_TIER3_SHORT_CHAIN",
        "P51-M7": "PASS_P51_M7_SMOOTHING_FUTURE_TARGET",
        "P51-M8": "PASS_P51_M8_INTEGRATION_CLOSEOUT",
    }
    for row in phases:
        assert row["status"] == expected_statuses[row["phase"]]
        assert Path(row["result_note"]).exists(), row["result_note"]
        if row["manifest"] != "self":
            assert Path(row["manifest"]).exists(), row["manifest"]


def test_p51_m8_original_gap_dispositions_are_complete_and_conservative() -> None:
    manifest = _manifest()
    gaps = {row["id"]: row for row in manifest["original_gap_dispositions"]}

    assert set(gaps) == {
        "native_generalized_sv_same_target_reference",
        "spatial_sir_production_route_architecture",
        "predator_prey_production_accuracy_tuning",
        "hmc_tier2_tier3_sampler_evidence",
        "stable_top_level_score_api",
        "smoother_if_latent_path_inference_becomes_target",
    }
    assert gaps["native_generalized_sv_same_target_reference"]["p51_status"] == "closed_low_dim_dense_reference"
    assert gaps["spatial_sir_production_route_architecture"]["p51_status"] == "blocked_route_architecture"
    assert gaps["predator_prey_production_accuracy_tuning"]["p51_status"] == "closed_declared_horizon25_row"
    assert gaps["hmc_tier2_tier3_sampler_evidence"]["p51_status"] == "tier2_passed_tier3_blocked"
    assert gaps["stable_top_level_score_api"]["p51_status"] == "partially_closed_root_blocked"
    assert gaps["smoother_if_latent_path_inference_becomes_target"]["p51_status"] == "deferred_future_target"


def test_p51_m8_non_goals_are_not_listed_as_remaining_gaps() -> None:
    manifest = _manifest()
    remaining = {row["id"] for row in manifest["remaining_blockers"]}

    assert "spatial_sir_production_route_architecture" in remaining
    assert "hmc_tier3_short_chain_reference_sampler" in remaining
    assert "root_level_public_score_api_decision" in remaining
    assert "smoother_if_latent_path_inference_becomes_target" in remaining
    assert all("adaptive" not in gap for gap in remaining)
    assert all("sp500" not in gap.lower() and "s&p" not in gap.lower() for gap in remaining)
    assert manifest["explicit_non_goals_not_gaps"] == [
        "adaptive TT/SIRT source-faithful filtering",
        "S&P 500 reproduction",
    ]


def test_p51_m8_supported_claims_do_not_overclaim_hmc_production_or_smoothing() -> None:
    manifest = _manifest()
    claims = " ".join(manifest["supported_claims"]).lower()
    nonclaims = {item.lower() for item in manifest["nonclaims"]}

    assert "tier 2" in claims
    assert "tier 3" in claims and "blocked" in claims
    assert "no hmc readiness" in nonclaims
    assert "no production hmc readiness" in nonclaims
    assert "no production spatial sir readiness" in nonclaims
    assert "no smoothing support" in nonclaims
    assert "no stable root-level bayesfilter score api" in nonclaims
    assert "no source-faithful adaptive tt/sirt filtering" in nonclaims
    assert "no s&p 500 reproduction" in nonclaims


def test_p51_m8_result_and_handoff_emit_closeout_without_reviving_non_goals() -> None:
    result = RESULT_PATH.read_text(encoding="utf-8")
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")

    assert result.count("status: PASS_P51_M8_INTEGRATION_CLOSEOUT") == 1
    assert "M6 blocks Tier 3" in result
    assert "Adaptive TT/SIRT source-faithful filtering and S&P 500 reproduction remain" in result
    assert "non-goals, not gaps" in result
    assert "Final phase reached: P51-M8" in handoff
    assert "Human-required stop: no" in handoff
