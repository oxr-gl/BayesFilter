from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-integration-closeout-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m9-integration-closeout-result-2026-06-09.md"
)
HANDOFF_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-visible-stop-handoff-2026-06-09.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p50_m9_closeout_has_all_phase_statuses_and_artifacts() -> None:
    manifest = _manifest()
    phases = manifest["phase_statuses"]

    assert manifest["schema_version"] == "p50.integration_closeout.v1"
    assert manifest["status"] == "PASS_P50_M9_INTEGRATION_CLOSEOUT"
    assert [row["phase"] for row in phases] == [f"P50-M{index}" for index in range(10)]
    for row in phases:
        assert row["status"].startswith(f"PASS_{row['phase'].replace('-', '_')}")
        assert Path(row["result_note"]).exists(), row["result_note"]


def test_p50_m9_remaining_gaps_exclude_adaptive_filtering_and_sp500() -> None:
    manifest = _manifest()
    gaps = {row["id"] for row in manifest["remaining_gaps"]}

    assert "native_generalized_sv_same_target_reference" in gaps
    assert "spatial_sir_production_route_architecture" in gaps
    assert "predator_prey_production_accuracy_tuning" in gaps
    assert "hmc_tier2_tier3_sampler_evidence" in gaps
    assert "stable_top_level_score_api" in gaps
    assert "smoother_if_latent_path_inference_becomes_target" in gaps
    assert all("adaptive" not in gap for gap in gaps)
    assert all("sp500" not in gap.lower() and "s&p" not in gap.lower() for gap in gaps)
    assert manifest["explicit_non_goals_not_gaps"] == [
        "adaptive TT/SIRT source-faithful filtering",
        "S&P 500 reproduction",
    ]


def test_p50_m9_closeout_has_h1_h8_crosswalk_and_route_inventory() -> None:
    manifest = _manifest()
    closure = {row["target"]: row for row in manifest["h1_h8_closure"]}
    route_labels = {row["route_label"]: row for row in manifest["route_label_inventory"]}

    assert list(closure) == [f"H{index}" for index in range(1, 9)]
    assert closure["H4"]["closeout_status"] == (
        "SCOPED_PASS_WITH_NATIVE_GENERALIZED_SV_REFERENCE_BLOCKER"
    )
    assert closure["H6"]["closeout_status"] == "PASS_TIER_DEFINITIONS_NO_HMC_READY_PROMOTION"
    assert "Tier 2" in closure["H6"]["boundary"]
    assert closure["H8"]["closeout_status"] == "PASS_NON_GOAL_GOVERNANCE"
    assert "non-goals, not gaps" in closure["H8"]["boundary"]

    assert set(route_labels) == {
        "hmc_compatible_deterministic_filtering",
        "gradient_calibration_diagnostic",
        "model_ladder_diagnostic",
        "hmc_readiness_tier",
        "smoothing_boundary",
        "historical_source_context",
    }
    assert "P50-M7" in route_labels["hmc_readiness_tier"]["used_by"]
    assert "HMC readiness without Tier 2 and Tier 3 evidence" in route_labels[
        "hmc_readiness_tier"
    ]["forbidden_claim"]
    assert "P50-M8" in route_labels["smoothing_boundary"]["used_by"]
    assert "smoothing support from filtering pass tokens" in route_labels[
        "smoothing_boundary"
    ]["forbidden_claim"]


def test_p50_m9_nonclaims_prevent_hmc_smoothing_and_production_overclaims() -> None:
    manifest = _manifest()
    nonclaims = set(manifest["nonclaims"])

    assert "no HMC readiness" in nonclaims
    assert "no production HMC readiness" in nonclaims
    assert "no production spatial SIR readiness" in nonclaims
    assert "no production predator-prey readiness" in nonclaims
    assert "no certified nonlinear-model gradient correctness" in nonclaims
    assert "no stable top-level score API" in nonclaims
    assert "no smoothing support" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims


def test_p50_m9_result_and_handoff_emit_closeout_without_revival_non_goals() -> None:
    result = RESULT_PATH.read_text(encoding="utf-8")
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")

    assert result.count("status: PASS_P50_M9_INTEGRATION_CLOSEOUT") == 1
    assert "adaptive TT/SIRT source-faithful filtering and S&P 500 reproduction are non-goals, not gaps" in result
    assert "Final phase reached: P50-M9" in handoff
    assert "Completion reason: all P50 gates M0--M9 passed in scoped form" in handoff
    assert "Human-required stop: no" in handoff
