from __future__ import annotations

from pathlib import Path


EXECUTION_RESULT = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-overnight-gated-self-recovery-execution-result-2026-06-08.md"
)
CLOSEOUT_RESULT = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-result-2026-06-08.md"
)
CLOSEOUT_SUBPLAN = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-subplan-2026-06-08.md"
)
CLOSEOUT_REVIEW_LEDGER = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-phase7-integration-closeout-claude-review-ledger-2026-06-08.md"
)


def test_p47_m7_closeout_blocks_full_pass_when_production_tokens_are_missing() -> None:
    text = CLOSEOUT_RESULT.read_text(encoding="utf-8")

    assert "status: `BLOCKED_UPSTREAM_PRODUCTION_TOKENS`" in text
    assert "`PASS_P47_M7_CLOSEOUT` is not emitted" in text
    assert "`PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING` and `PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING` did not pass" in text
    assert "No production filtering" in text
    assert "No full P47 closeout pass" in text


def test_p47_m7_claim_ledger_preserves_passed_lower_rung_and_blocked_production_rows() -> None:
    text = CLOSEOUT_RESULT.read_text(encoding="utf-8")
    required = (
        "`PASS_P47_M0_GOVERNANCE`",
        "`PASS_P47_M1_ADAPTIVE_ROUTE`",
        "`PASS_P47_M2_PAPER_SCALE_READINESS`",
        "`PASS_P47_M3_GENERALIZED_SV_EQUALITY`",
        "`PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY`",
        "`PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING`",
        "`PASS_P47_M6_SCORE_HMC_READINESS`",
        "`BLOCKED_NO_PRODUCTION_TOKEN`",
        "`BLOCKED_UPSTREAM_PRODUCTION_TOKENS`",
    )

    assert all(token in text for token in required)
    assert "Lower-rung KSC transformed-SV same-target value/gradient equality" in text
    assert "SIR/predator-prey score/HMC rows blocked" in text


def test_p47_execution_result_records_m4_m5_m6_boundaries() -> None:
    text = EXECUTION_RESULT.read_text(encoding="utf-8")

    assert "### P47-M4b" in text
    assert "Token not emitted: `PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING`" in text
    assert "### P47-M5b" in text
    assert "production or near-paper-scale" in text
    assert "predator-prey filtering" in text
    assert "### P47-M6" in text
    assert "evidence-class readiness table correctness, not" in text
    assert "production HMC readiness" in text
    assert "### P47-M7" in text
    assert "Full token not emitted: `PASS_P47_M7_CLOSEOUT`" in text
    assert "STOPPED_WITH_REVIEWED_M7_BLOCKER_CLOSEOUT" in text
    assert "PENDING_FINAL_REVIEW" not in text
    assert "must stop at M7 blocker closeout rather than fabricate production rows" in text


def test_p47_closeout_nonclaims_keep_sp500_and_adaptive_reproduction_out() -> None:
    text = CLOSEOUT_RESULT.read_text(encoding="utf-8")

    assert "no adaptive MATLAB reproduction" in text
    assert "no S&P 500 reproduction" in text
    assert "The weakest part of the evidence is the gap between lower-rung" in text
    assert "adaptive TT-cross/SIRT production-scale" in text


def test_p47_m7_subplan_and_review_ledger_use_blocker_closeout_token_when_upstream_blocks() -> None:
    subplan = CLOSEOUT_SUBPLAN.read_text(encoding="utf-8")
    ledger = CLOSEOUT_REVIEW_LEDGER.read_text(encoding="utf-8")

    assert "If any upstream phase is blocked" in subplan
    assert "PASS_P47_M7_BLOCKER_CLOSEOUT" in subplan
    assert "PASS_P47_M7_BLOCKER_CLOSEOUT" in ledger
    assert "PASS_P47_M7_CLOSEOUT` is not requested" in ledger
