from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-manifest-2026-06-29.json"
)
DECISION_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r2-reset-vjp-decision-2026-06-29.md"
)
R3_SUBPLAN_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-reset-blocker-resolution-subplan-2026-06-29.md"
)
R3_CHOL_POLICY_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r3-cholesky-ridge-reset-policy-2026-06-29.md"
)
GRADIENT_SCRIPT = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
)
BLOCKER_CODE = "PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN"
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"
EXPECTED_RESET_IDS = {f"E{index:02d}" for index in range(1, 15)}
SPECTRAL_IDS = {"E05", "E07", "E10", "E11"}


def _manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_r2_manifest_preserves_material_blocker() -> None:
    manifest = _manifest()

    assert manifest["route_status"] == "blocked_reset_vjp_not_implemented"
    assert manifest["selected_route_name"] == "manual_likelihood_reverse_scan_no_autodiff"
    assert manifest["material_gate_authorized"] is False
    assert manifest["material_blocker_code"] == BLOCKER_CODE
    assert manifest["next_phase"]["may_unblock_material_gate"] is False
    assert "cannot unblock material mode" in manifest["material_unblocking_rule"]


def test_r2_manifest_classifies_every_reset_boundary_terminally() -> None:
    manifest = _manifest()
    rows = manifest["contract_e_reset_sub_boundaries"]

    assert {row["id"] for row in rows} == EXPECTED_RESET_IDS
    for row in rows:
        assert "blocked_pending_r2" not in row.values()
        assert row["evidence_artifact"] == str(DECISION_PATH.relative_to(ROOT))
        if row["id"] == "E14":
            assert row["terminal_classification"] == "non_gradient_monitor"
            assert row["fd_parity_required_for_manual_vjp"] is False
        else:
            assert row["terminal_classification"] == "blocked"
            assert row["fd_parity_required_for_manual_vjp"] is True
            assert row["fd_parity_status"] == "not_run_no_manual_vjp_claim"
            assert row["blocker"]


def test_r2_manifest_has_spectral_boundary_rule() -> None:
    manifest = _manifest()
    rule = manifest["spectral_boundary_safety_rule"]

    assert set(rule["applies_to"]) == SPECTRAL_IDS
    assert rule["hidden_autodiff_fallback_allowed"] is False
    assert "unchanged retained rank" in rule["rule"]
    assert "no eigenvalue floor crossing" in rule["rule"]

    rows = {row["id"]: row for row in manifest["contract_e_reset_sub_boundaries"]}
    for boundary_id in SPECTRAL_IDS:
        assert rows[boundary_id]["fixed_rank_scope"] == "required_but_not_derived"
        assert "spectral" in rows[boundary_id]["blocker"] or "floor" in rows[boundary_id]["blocker"]


def test_r2_decision_and_r3_subplan_state_nonclaims_and_stop_conditions() -> None:
    decision = DECISION_PATH.read_text(encoding="utf-8")
    r3_subplan = R3_SUBPLAN_PATH.read_text(encoding="utf-8")

    for phrase in [
        "No Contract E reset VJP is implemented",
        "No stop-gradient reset policy is approved",
        "No full Phase 3 LGSSM gradient correctness claim is made",
        BLOCKER_CODE,
    ]:
        assert phrase in decision

    for phrase in [
        "fixed_rank_manual_vjp",
        "reviewed_stop_gradient_policy",
        "does not authorize GPU runs",
        "full-filter finite differences",
        "local tiny reset-fixture checks",
        "reset path, eigensystem boundary, or material score route",
        "Do not remove or weaken the material Phase 3 blocker",
        "R4 may then plan the full manual likelihood reverse scan integration",
    ]:
        assert phrase in r3_subplan

    chol_policy = R3_CHOL_POLICY_PATH.read_text(encoding="utf-8")
    assert "Cholesky-Ridge Contract E Reset" in chol_policy
    assert "default until broader evidence" in chol_policy


def test_phase3_script_replaced_tiny_material_taped_route_after_r8() -> None:
    source = GRADIENT_SCRIPT.read_text(encoding="utf-8")

    assert FULL_BLOCKER_CODE in source
    assert "manual_likelihood_reverse_scan_no_autodiff" in source
    assert "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny" in source
    assert "tf.GradientTape" in source
    assert "manual-transport-vjp-only" in source
    assert "manual-custom-vjp" not in source
