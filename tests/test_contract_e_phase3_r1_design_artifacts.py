from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-route-manifest-2026-06-29.json"
)
DESIGN_PATH = (
    ROOT
    / "docs"
    / "plans"
    / "bayesfilter-ledh-pfpf-ot-contract-e-phase3-r1-manual-reverse-scan-design-2026-06-29.md"
)
GRADIENT_SCRIPT = (
    ROOT / "docs" / "benchmarks" / "diagnose_ledh_pfpf_ot_contract_e_lgssm_gradient.py"
)


EXPECTED_BOUNDARY_IDS = {f"B{index:02d}" for index in range(1, 11)}
EXPECTED_RESET_IDS = {f"E{index:02d}" for index in range(1, 15)}
BLOCKER_CODE = "PHASE3_MATERIAL_GATE_BLOCKED_PENDING_MANUAL_REVERSE_SCAN"
FULL_BLOCKER_CODE = "PHASE3_MATERIAL_FULL_GATE_PENDING_T10_MANUAL_ROUTE_VALIDATION"


def _manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_r1_manifest_is_design_only_and_material_blocked() -> None:
    manifest = _manifest()

    assert manifest["route_status"] == "design_only_not_implemented"
    assert manifest["selected_route_name"] == "manual_likelihood_reverse_scan_no_autodiff"
    assert manifest["material_gate_authorized"] is False
    assert manifest["material_blocker_code"] == BLOCKER_CODE
    assert manifest["next_phase"]["may_unblock_material_gate"] is False
    assert "R2 reset-policy decision alone cannot unblock" in manifest["material_unblocking_rule"]


def test_r1_manifest_lists_all_derivative_boundaries() -> None:
    manifest = _manifest()

    boundary_ids = {item["id"] for item in manifest["derivative_boundaries"]}
    reset_ids = {item["id"] for item in manifest["contract_e_reset_sub_boundaries"]}

    assert boundary_ids == EXPECTED_BOUNDARY_IDS
    assert reset_ids == EXPECTED_RESET_IDS
    assert all(
        item["classification"] == "blocked_pending_r2"
        for item in manifest["contract_e_reset_sub_boundaries"]
        if item["id"] != "E14"
    )
    assert next(
        item for item in manifest["contract_e_reset_sub_boundaries"] if item["id"] == "E14"
    )["classification"] == "non_gradient_monitor"


def test_r1_design_names_reset_sub_boundaries_and_nonclaims() -> None:
    design = DESIGN_PATH.read_text(encoding="utf-8")

    for phrase in [
        "Weighted target moments",
        "Barycentric first stage",
        "Residual covariance square root",
        "Tilde covariance pseudo-inverse square root",
        "Final recentering to reset cloud",
        "No Contract E reset VJP is implemented here",
    ]:
        assert phrase in design


def test_phase3_full_material_blocker_and_manual_route_present_after_r8() -> None:
    source = GRADIENT_SCRIPT.read_text(encoding="utf-8")

    assert FULL_BLOCKER_CODE in source
    assert "manual_likelihood_reverse_scan_no_autodiff" in source
    assert "contract_e_cholesky_fixed_ridge_manual_lgssm_tiny" in source
    assert "manual-transport-vjp-only" in source
    assert "manual-custom-vjp" not in source
