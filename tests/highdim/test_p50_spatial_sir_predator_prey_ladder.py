from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m6-spatial-sir-predator-prey-ladder-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p50_m6_manifest_uses_m4_calibration_contract() -> None:
    manifest = _manifest()

    assert manifest["schema_version"] == "p50.spatial_sir_predator_prey_ladder.v1"
    assert manifest["phase"] == "P50-M6"
    assert manifest["calibration_contract"].endswith(
        "bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.json"
    )


def test_p50_m6_lower_rung_value_rows_are_not_promoted_to_gradient_correctness() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}
    lower_rows = [
        rows["spatial_sir_j1_zhaocui_vs_dense_lower_rung"],
        rows["predator_prey_zhaocui_vs_dense_lower_rung"],
    ]

    for row in lower_rows:
        assert row["m4_class"] == "PASS_VALUE_ONLY_DIAGNOSTIC"
        assert row["dimension"] == 2
        assert "dense tensor-product grid reference" in row["reference"]
        assert "no gradient correctness" in row["nonclaims"]
        assert "no HMC readiness" in row["nonclaims"]


def test_p50_m6_finite_score_rows_keep_uncertified_derivative_boundary() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}
    score_rows = [
        rows["spatial_sir_cut4_finite_score_diagnostic"],
        rows["predator_prey_cut4_finite_score_diagnostic"],
    ]

    for row in score_rows:
        assert row["m4_class"] == "PASS_GRADIENT_LOCAL_DIAGNOSTIC"
        assert row["reference"] == "none for promoted same-target gradient"
        assert "value_only" in row["promotion_boundary"]
        assert "derivatives are not certified" in row["promotion_boundary"]
        assert "no certified derivative" in row["nonclaims"]
        assert "no same-target gradient reference" in row["nonclaims"]


def test_p50_m6_production_rows_preserve_reviewed_blockers() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}

    sir = rows["spatial_sir_production_route"]
    predator = rows["predator_prey_production_route"]

    assert sir["m4_class"] == "FAIL_NUMERICAL_VETO"
    assert sir["blocker"] == "BLOCKED_M4B_ROUTE_ARCHITECTURE"
    assert "no production spatial SIR filtering" in sir["nonclaims"]
    assert predator["m4_class"] == "FAIL_NUMERICAL_VETO"
    assert predator["blocker"] == "BLOCKED_M5B_PRODUCTION_ACCURACY_TUNING"
    assert "no production predator-prey filtering" in predator["nonclaims"]


def test_p50_m6_phase_decision_and_nonclaims_do_not_revive_non_goals_or_hmc() -> None:
    manifest = _manifest()
    decision = manifest["phase_decision"]
    nonclaims = set(manifest["nonclaims"])
    non_goals = set(manifest["explicit_non_goals"])

    assert decision["status"] == "PASS_WITH_PRODUCTION_BLOCKERS_AND_DIAGNOSTIC_GRADIENT_BOUNDARY"
    assert "production spatial SIR and predator-prey rows remain blocked" in decision["reason"]
    assert "adaptive TT/SIRT source-faithful filtering" in non_goals
    assert "S&P 500 reproduction" in non_goals
    assert "no HMC readiness" in nonclaims
    assert "no certified nonlinear-model gradient correctness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims
