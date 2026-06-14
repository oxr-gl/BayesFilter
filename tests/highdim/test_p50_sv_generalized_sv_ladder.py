from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-m5-sv-generalized-sv-ladder-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p50_m5_manifest_uses_m4_calibration_contract() -> None:
    manifest = _manifest()

    assert manifest["schema_version"] == "p50.sv_generalized_sv_ladder.v1"
    assert manifest["phase"] == "P50-M5"
    assert manifest["calibration_contract"].endswith(
        "bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.json"
    )


def test_p50_m5_sv_rows_cover_dimensions_one_two_three_for_value_and_gradient() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}
    pass_rows = [
        rows["ksc_sv_cut4_vs_kalman_dim_1_2_3"],
        rows["exact_transformed_sv_zhaocui_vs_dense_dim_1_2_3"],
    ]

    for row in pass_rows:
        assert row["dimensions"] == [1, 2, 3]
        assert row["m4_class"] == "PASS_SAME_TARGET_VALUE_AND_GRADIENT"
        assert row["candidate"]
        assert row["reference"]
        assert row["target_identity"]
        assert row["evidence_tests"]
        assert "no HMC readiness" in row["nonclaims"]


def test_p50_m5_ksc_zhaocui_row_is_not_promoted_under_loose_existing_tolerances() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}
    row = rows["ksc_sv_zhaocui_vs_dense_dim_1_2_3"]

    assert row["dimensions"] == [1, 2, 3]
    assert row["m4_class"] == "PASS_GRADIENT_LOCAL_DIAGNOSTIC"
    assert "looser than P50-M4 default" in row["m4_promotion_boundary"]
    assert "not adaptive MATLAB TT-cross/SIRT reproduction" in row["nonclaims"]
    assert "no HMC readiness" in row["nonclaims"]


def test_p50_m5_generalized_sv_native_equality_is_blocked_not_overclaimed() -> None:
    rows = {row["row_id"]: row for row in _manifest()["rows"]}
    row = rows["generalized_sv_native_same_target"]

    assert row["m4_class"] == "BLOCKED_REFERENCE_MISSING"
    assert row["reference"] == "none adequate for native same-target value and gradient equality"
    assert "diagnostic approximations only" in row["blocker_reason"]
    assert "no native generalized SV same-target equality" in row["nonclaims"]
    assert "moment-matched Kalman is diagnostic only" in row["nonclaims"]
    assert "transformed-residual CUT4 is diagnostic only" in row["nonclaims"]


def test_p50_m5_phase_decision_and_nonclaims_do_not_revive_non_goals() -> None:
    manifest = _manifest()
    decision = manifest["phase_decision"]
    nonclaims = set(manifest["nonclaims"])
    non_goals = set(manifest["explicit_non_goals"])

    assert decision["status"] == "PASS_WITH_SCOPED_GENERALIZED_SV_NATIVE_BLOCKER"
    assert "blocked rather than overclaimed" in decision["reason"]
    assert "KSC Zhao-Cui-vs-dense is retained as local diagnostic evidence" in decision["reason"]
    assert "adaptive TT/SIRT source-faithful filtering" in non_goals
    assert "S&P 500 reproduction" in non_goals
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims
    assert "no HMC readiness" in nonclaims
