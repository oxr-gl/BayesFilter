from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-paper-scale-readiness-manifest-2026-06-08.json"
)
REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _manifest_rows() -> dict[str, dict[str, object]]:
    rows = _manifest()["candidate_rows"]
    assert isinstance(rows, list)
    return {str(row["target_id"]): row for row in rows}


def _registry_rows() -> dict[str, dict[str, object]]:
    rows = _registry()["rows"]
    assert isinstance(rows, list)
    return {str(row["target_id"]): row for row in rows}


def test_p47_m2_manifest_is_readiness_only_and_excludes_sp500() -> None:
    manifest = _manifest()
    text = json.dumps(manifest, sort_keys=True).lower()

    assert manifest["schema_version"] == "p47.paper_scale_readiness.v1"
    assert manifest["phase"] == "P47-M2"
    assert manifest["status"] == "READINESS_ONLY"
    assert manifest["pass_token"] == "PASS_P47_M2_PAPER_SCALE_READINESS"
    assert manifest["s_and_p_500_reproduction_in_scope"] is False
    assert "sp500" not in text
    assert "s&p 500" in text
    assert "reproduction is in scope" in text


def test_p47_m2_manifest_preserves_m0_m1_prerequisites_and_route_label() -> None:
    manifest = _manifest()
    registry = _registry()

    assert manifest["prerequisite_tokens_observed"] == [
        "PASS_P47_M0_GOVERNANCE",
        "PASS_P47_M1_ADAPTIVE_ROUTE",
    ]
    assert manifest["m1_route_label_required"] == registry["m1_route_decision"]
    assert manifest["m1_route_label_required"] == "documented-deviation fixed-design substitute"

    for row in _manifest_rows().values():
        assert row["m1_route_label"] == "documented-deviation fixed-design substitute"


def test_p47_m2_candidates_are_registry_backed_without_emitting_production_tokens() -> None:
    manifest = _manifest()
    registry_rows = _registry_rows()
    manifest_rows = _manifest_rows()

    assert set(manifest_rows) == {
        "generalized_sv_same_target_equality",
        "spatial_sir_reference_equality",
        "spatial_sir_production_filtering",
        "predator_prey_reference_filtering",
        "predator_prey_production_filtering",
    }

    forbidden_tokens = set(manifest["claim_boundary"]["forbidden_tokens"])
    assert "PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING" in forbidden_tokens
    assert "PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING" in forbidden_tokens
    assert "PASS_P47_M6_SCORE_HMC_READINESS" in forbidden_tokens
    assert "PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION" in forbidden_tokens

    for target_id, row in manifest_rows.items():
        assert target_id in registry_rows
        assert row["phase_gate"] == registry_rows[target_id]["phase_gate"]
        assert row["model_family"] == registry_rows[target_id]["model_family"]
        assert row["m1_route_label"] == registry_rows[target_id]["m1_route_label"]
        assert row["target_id"] not in forbidden_tokens


def test_p47_m2_production_rows_remain_blocked_by_lower_rung_tokens() -> None:
    rows = _manifest_rows()

    spatial = rows["spatial_sir_production_filtering"]
    assert spatial["readiness_state"] == "resource_caps_defined_but_correctness_blocked"
    assert spatial["production_state"] == "blocked_until_PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY"
    assert "PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY" in spatial["required_before_correctness_claim"]
    assert any("does not emit PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING" in item for item in spatial["nonclaims"])

    predator = rows["predator_prey_production_filtering"]
    assert predator["readiness_state"] == "resource_caps_defined_but_correctness_blocked"
    assert predator["production_state"] == "blocked_until_PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING"
    assert "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING" in predator["required_before_correctness_claim"]
    assert any("does not emit PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING" in item for item in predator["nonclaims"])


def test_p47_m2_ladder_policy_and_resource_caps_prevent_proxy_promotion() -> None:
    manifest = _manifest()

    assert manifest["global_resource_caps"]["max_ladder_axis_changes_per_run"] == 1
    assert manifest["ladder_policy"]["one_axis_at_a_time"] is True
    assert manifest["ladder_policy"]["promotion_requires_model_specific_reference_gate"] is True
    assert manifest["ladder_policy"]["finite_outputs_are_explanatory_only"] is True

    explanatory = set(manifest["explanatory_only_diagnostics"])
    assert {"fit residual", "holdout residual", "finite feasibility output"}.issubset(explanatory)

    for row in _manifest_rows().values():
        assert row["resource_caps"], row["target_id"]
        assert row["stop_conditions"], row["target_id"]
        row_text = json.dumps(row, sort_keys=True).lower()
        assert "finite" in row_text or "lower-rung" in row_text


def test_p47_m2_claim_boundary_forbids_correctness_and_hmc_promotion() -> None:
    boundary = _manifest()["claim_boundary"]
    allowed = " ".join(boundary["allowed_claims"]).lower()
    forbidden = " ".join(boundary["forbidden_claims"]).lower()

    assert boundary["claim_class"] == "FEASIBILITY_ONLY_NO_CORRECTNESS_PROMOTION"
    assert "readiness manifest exists" in allowed
    assert "correctness is established" in forbidden
    assert "hmc readiness is established" in forbidden
    assert "finite output implies correctness" in forbidden
