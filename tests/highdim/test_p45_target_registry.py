from __future__ import annotations

import json
from pathlib import Path


REGISTRY_PATH = Path("docs/plans/bayesfilter-highdim-zhao-cui-p45-target-registry-2026-06-08.json")


REQUIRED_TARGET_IDS = {
    "generalized_sv_native_raw_observation",
    "generalized_sv_transformed_residual_diagnostic",
    "generalized_sv_gaussian_mixture_or_moment_matched_approximation",
    "spatial_sir_additive_gaussian_closure",
    "spatial_sir_native_or_nongaussian_route",
    "predator_prey_additive_gaussian_rk4_closure",
    "predator_prey_native_or_nongaussian_route",
}


def _registry() -> dict[str, object]:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _rows() -> list[dict[str, object]]:
    registry = _registry()
    rows = registry["rows"]
    assert isinstance(rows, list)
    return rows


def _by_target_id() -> dict[str, dict[str, object]]:
    return {str(row["target_id"]): row for row in _rows()}


def test_p45_m0_registry_has_required_rows_and_schema() -> None:
    registry = _registry()

    assert registry["schema_version"] == "p45.target_registry.v1"
    assert registry["phase"] == "P45-M0"
    assert set(_by_target_id()) == REQUIRED_TARGET_IDS

    required_fields = set(registry["required_fields"])
    for row in _rows():
        assert required_fields.issubset(row)
        for field in required_fields:
            assert row[field] not in ("", [], {}, None), field
        assert set(row["route_statuses"]) == {"reference", "cut4", "zhao_cui"}


def test_p45_m0_no_same_target_row_without_three_available_routes() -> None:
    for row in _rows():
        statuses = row["route_statuses"]
        route_triplet_available = all(str(status).startswith("available") for status in statuses.values())
        if row["same_target_comparison_authorized"]:
            assert route_triplet_available, row["target_id"]
        else:
            assert not route_triplet_available, row["target_id"]


def test_p45_m0_generalized_sv_rows_preserve_native_vs_diagnostic_boundaries() -> None:
    rows = _by_target_id()
    native = rows["generalized_sv_native_raw_observation"]
    transformed = rows["generalized_sv_transformed_residual_diagnostic"]
    approximation = rows["generalized_sv_gaussian_mixture_or_moment_matched_approximation"]

    assert native["claim_class"] == "BLOCKED_NATIVE_SAME_TARGET"
    assert native["same_target_comparison_authorized"] is False
    assert "state_dim == 2" in native["zhao_cui_route"]

    assert transformed["claim_class"] == "DIAGNOSTIC_ONLY_NO_EQUALITY_CLAIM"
    assert "conditioning" in transformed["transformation_jacobian_terms"].lower()
    assert "jacobian" in transformed["transformation_jacobian_terms"].lower()
    assert "panel expansions are factorized diagnostics" in transformed["dimension_panel_convention"]
    assert any("not exact native" in item for item in transformed["nonclaims"])

    assert approximation["claim_class"] == "APPROXIMATION_ONLY_NO_NATIVE_EXACT_CLAIM"
    assert "not exact native" in " ".join(approximation["nonclaims"])
    assert "Panel counts 1,2,3 are factorized" in approximation["dimension_panel_convention"]
    assert approximation["route_statuses"]["reference"].startswith("blocked")
    assert "panel counts 1,2,3 must be labeled factorized" in native["dimension_panel_convention"]


def test_p45_m0_sir_and_predator_prey_closures_are_not_native_claims() -> None:
    rows = _by_target_id()
    sir = rows["spatial_sir_additive_gaussian_closure"]
    predator_prey = rows["predator_prey_additive_gaussian_rk4_closure"]

    for row in (sir, predator_prey):
        assert row["claim_class"] == "BLOCKED_CLOSURE_SAME_TARGET_PENDING_M1_AND_REFERENCE"
        assert row["same_target_comparison_authorized"] is False
        assert row["route_statuses"]["cut4"] == "available_diagnostic_only"
        assert row["route_statuses"]["zhao_cui"] == "blocked_current_scalar_nonlinear_route_requires_state_dim_1"
        assert "dense" in row["route_statuses"]["reference"]
        assert any("closure likelihood is not" in item for item in row["nonclaims"])

    assert "J=2,3 are factorized/replicated panels" in sir["dimension_panel_convention"]
    assert "replicated panels are factorized" in predator_prey["dimension_panel_convention"]
    assert "RK4" in predator_prey["target_identity"]


def test_p45_m0_native_nongaussian_rows_are_blocked_pending_target_definition() -> None:
    rows = _by_target_id()
    for target_id in ("spatial_sir_native_or_nongaussian_route", "predator_prey_native_or_nongaussian_route"):
        row = rows[target_id]
        assert row["claim_class"] == "BLOCKED_NATIVE_ROUTE_UNSPECIFIED"
        assert row["same_target_comparison_authorized"] is False
        assert all(str(status).startswith("blocked") for status in row["route_statuses"].values())
        assert "Blocked pending scientific target definition" in row["parameterization"]
