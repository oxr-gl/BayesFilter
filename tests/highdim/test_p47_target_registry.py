from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p47-target-registry-2026-06-08.json")


REQUIRED_TARGET_IDS = {
    "adaptive_tt_sirt_route_label",
    "paper_scale_readiness_synthetic_model_suite",
    "generalized_sv_same_target_equality",
    "spatial_sir_reference_equality",
    "spatial_sir_production_filtering",
    "predator_prey_reference_filtering",
    "predator_prey_production_filtering",
    "score_api_hmc_readiness_by_evidence_class",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _rows() -> list[dict[str, object]]:
    rows = _registry()["rows"]
    assert isinstance(rows, list)
    return rows


def _by_target_id() -> dict[str, dict[str, object]]:
    return {str(row["target_id"]): row for row in _rows()}


def test_p47_registry_has_required_rows_schema_and_no_sp500_scope() -> None:
    registry = _registry()

    assert registry["schema_version"] == "p47.target_registry.v1"
    assert registry["phase"] == "P47-M0"
    assert registry["s_and_p_500_reproduction_in_scope"] is False
    assert set(_by_target_id()) == REQUIRED_TARGET_IDS

    required_fields = set(registry["required_fields"])
    allowed_labels = set(registry["allowed_m1_route_labels"])
    for row in _rows():
        assert required_fields.issubset(row), row["target_id"]
        for field in required_fields:
            assert row[field] not in ("", [], {}, None), (row["target_id"], field)
        assert row["m1_route_label"] in allowed_labels
        row_text = json.dumps(row, sort_keys=True).lower()
        assert "sp500" not in row_text
        assert "available s&p 500" not in row_text
        assert "s&p 500 reproduction in scope" not in row_text
        assert (
            "s&p 500 reproduction" in " ".join(row["nonclaims"]).lower()
            or row["target_id"] != "paper_scale_readiness_synthetic_model_suite"
        )


def test_p47_registry_preserves_route_label_nonclaim_boundary() -> None:
    route_row = _by_target_id()["adaptive_tt_sirt_route_label"]

    assert route_row["claim_class"] == "ROUTE_LABEL_ONLY"
    assert route_row["same_target_comparison_authorized"] is False
    assert "PASS_P47_M1_ADAPTIVE_ROUTE" in route_row["pass_tokens"]
    assert "PASS_ADAPTIVE_MATLAB_TT_CROSS_SIRT_REPRODUCTION" in route_row["forbidden_tokens"]
    assert any("not adaptive MATLAB TT-cross/SIRT reproduction" in item for item in route_row["nonclaims"])


def test_p47_registry_splits_spatial_sir_reference_and_production_tokens() -> None:
    rows = _by_target_id()
    lower = rows["spatial_sir_reference_equality"]
    production = rows["spatial_sir_production_filtering"]

    assert lower["evidence_class"] == "lower_rung_reference_equality"
    assert lower["pass_tokens"] == ["PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY"]
    assert "PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING" in lower["forbidden_tokens"]
    assert any("not production filtering" in item for item in lower["nonclaims"])

    assert production["evidence_class"] == "production_filtering"
    assert production["pass_tokens"] == ["PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING"]
    assert "PASS_P47_M2_PAPER_SCALE_READINESS" in production["prerequisite_tokens"]
    assert "PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY" in production["prerequisite_tokens"]
    assert any("production or near-paper-scale row" in item for item in production["nonclaims"])


def test_p47_registry_splits_predator_prey_reference_and_production_tokens() -> None:
    rows = _by_target_id()
    lower = rows["predator_prey_reference_filtering"]
    production = rows["predator_prey_production_filtering"]

    assert lower["evidence_class"] == "lower_rung_reference_filtering"
    assert lower["pass_tokens"] == ["PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING"]
    assert "PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING" in lower["forbidden_tokens"]
    assert any("not production filtering" in item for item in lower["nonclaims"])

    assert production["evidence_class"] == "production_filtering"
    assert production["pass_tokens"] == ["PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING"]
    assert "PASS_P47_M2_PAPER_SCALE_READINESS" in production["prerequisite_tokens"]
    assert "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING" in production["prerequisite_tokens"]
    assert any("production or near-paper-scale row" in item for item in production["nonclaims"])


def test_p47_registry_m6_cannot_promote_production_from_lower_rung_only() -> None:
    registry = _registry()
    m6 = _by_target_id()["score_api_hmc_readiness_by_evidence_class"]
    dependency_classes = registry["api_hmc_dependency_classes"]

    assert m6["claim_class"] == "API_HMC_BY_EVIDENCE_CLASS"
    assert "PASS_P47_M6_SCORE_HMC_READINESS" in m6["pass_tokens"]
    assert "PER_TARGET_UPSTREAM_TOKEN_REQUIRED" in m6["prerequisite_tokens"]
    assert "P42_TIER_EVIDENCE_REQUIRED" in m6["prerequisite_tokens"]
    assert "PASS_PRODUCTION_HMC_FROM_LOWER_RUNG_ONLY" in m6["forbidden_tokens"]
    assert any("lower-rung tokens support only lower-rung" in item for item in m6["nonclaims"])
    assert any("production API/HMC readiness requires" in item for item in m6["nonclaims"])

    assert set(dependency_classes) == {
        "generalized_sv_lower_rung",
        "spatial_sir_lower_rung",
        "spatial_sir_production",
        "predator_prey_lower_rung",
        "predator_prey_production",
    }

    for dependency in dependency_classes.values():
        upstream_tokens = dependency["upstream_tokens"]
        assert isinstance(upstream_tokens, list)
        assert len(upstream_tokens) == 1
        assert upstream_tokens[0].startswith("PASS_P47_")
        p42_required_tiers = dependency["p42_required_tiers"]
        assert isinstance(p42_required_tiers, list)
        assert "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE" in p42_required_tiers

    assert dependency_classes["generalized_sv_lower_rung"]["upstream_tokens"] == [
        "PASS_P47_M3_GENERALIZED_SV_EQUALITY"
    ]
    assert dependency_classes["spatial_sir_lower_rung"]["upstream_tokens"] == [
        "PASS_P47_M4_SPATIAL_SIR_REFERENCE_EQUALITY"
    ]
    assert dependency_classes["spatial_sir_production"]["upstream_tokens"] == [
        "PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING"
    ]
    assert dependency_classes["predator_prey_lower_rung"]["upstream_tokens"] == [
        "PASS_P47_M5_PREDATOR_PREY_REFERENCE_FILTERING"
    ]
    assert dependency_classes["predator_prey_production"]["upstream_tokens"] == [
        "PASS_P47_M5_PREDATOR_PREY_PRODUCTION_FILTERING"
    ]

    for key, dependency in dependency_classes.items():
        if key.endswith("_production"):
            assert dependency["evidence_class"] == "production_filtering"
            assert "production" in dependency["allowed_claim"]
            assert dependency["p42_required_tiers"] == [
                "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE",
                "TIER_2_STATISTICAL_SCALE",
                "TIER_3_HAMILTONIAN_LEAPFROG_FOR_HMC",
            ]
        else:
            assert dependency["evidence_class"].startswith("lower_rung")
            assert "lower-rung" in dependency["allowed_claim"]
            assert dependency["p42_required_tiers"] == [
                "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE"
            ]


def test_p47_same_target_authorization_requires_reference_cut4_and_zhaocui_routes() -> None:
    for row in _rows():
        if row["same_target_comparison_authorized"]:
            assert "Blocked" not in row["reference_route"], row["target_id"]
            assert "Only" in row["cut4_route"] or "Authorized" in row["cut4_route"], row["target_id"]
            assert "route" in row["zhao_cui_route"], row["target_id"]
        else:
            assert row["claim_class"] != "SAME_TARGET_VALUE_GRADIENT_GATE" or row["target_id"] == "generalized_sv_same_target_equality"
