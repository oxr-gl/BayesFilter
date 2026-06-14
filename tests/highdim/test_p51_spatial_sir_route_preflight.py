from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-manifest-2026-06-09.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p51-m3-spatial-sir-production-route-result-2026-06-09.md"
)
P47_M4B_MANIFEST = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p47-m4b-production-row-manifest-2026-06-09.json"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p51_m3_manifest_is_same_p47_p50_spatial_sir_production_row() -> None:
    manifest = _manifest()
    source = json.loads(P47_M4B_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["schema_version"] == "p51.spatial_sir_route_preflight.v1"
    assert manifest["status"] == "PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT"
    assert manifest["target_id"] == source["target_id"] == "spatial_sir_production_filtering"
    assert manifest["source_blocker"] == "BLOCKED_M4B_ROUTE_ARCHITECTURE"
    assert manifest["production_filtering_status"] == "blocked_route_architecture"
    assert manifest["production_readiness_claimed"] is False
    assert manifest["hmc_readiness_claimed"] is False


def test_p51_m3_preflight_preserves_all_axes_grid_complexity_blocker() -> None:
    manifest = _manifest()
    preflight = manifest["preflight_gate"]
    candidates = {row["candidate_id"]: row for row in manifest["candidate_ladder"]}
    cap = int(preflight["max_pairwise_transition_evaluations_cpu"])

    assert preflight["current_route"] == "P46/P47 all-axes multistate retained-grid fixed-design TT route"
    assert preflight["pairwise_transition_evaluations_formula"] == "order^(4*sites)"
    assert candidates["M4b-0"]["route_preflight"] == "below_cap_feasibility_only"
    assert candidates["M4b-1"]["route_preflight"] == "blocked_above_cap"
    assert candidates["M4b-2"]["route_preflight"] == "blocked_above_cap_near_paper"

    for row in manifest["candidate_ladder"]:
        grid_points = int(row["order"]) ** (2 * int(row["sites"]))
        pairwise = grid_points * grid_points
        assert row["grid_points"] == grid_points
        assert row["pairwise_transition_evaluations"] == pairwise
        assert (pairwise <= cap) == row["below_cap"]


def test_p51_m3_required_architecture_change_is_explicit_and_not_production_pass() -> None:
    manifest = _manifest()
    repair = manifest["required_architecture_change"]

    assert repair["decision"] == "required_before_production_spatial_sir_filtering"
    assert repair["missing_component"] == "streamed_or_factorized_transition_application"
    assert repair["must_avoid"] == "materializing all grid_points^2 transition pairs"
    assert repair["must_preserve"] == [
        "same P50/P47 spatial SIR production target family",
        "deterministic replay and branch identity",
        "TensorFlow/TFP differentiable route",
        "production-row metrics and nonclaims"
    ]
    assert "PASS_P47_M4_SPATIAL_SIR_PRODUCTION_FILTERING" not in manifest["tokens_emitted"]
    assert "PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT" in manifest["tokens_emitted"]


def test_p51_m3_nonclaims_exclude_lower_rung_and_hmc_promotion() -> None:
    nonclaims = set(_manifest()["nonclaims"])

    assert "no production spatial SIR filtering readiness" in nonclaims
    assert "no HMC readiness" in nonclaims
    assert "no lower-rung J=1 to J=9 promotion" in nonclaims
    assert "no certified nonlinear-model gradient correctness" in nonclaims
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims


def test_p51_m3_result_emits_token_once_and_blocker_is_visible() -> None:
    text = RESULT_PATH.read_text(encoding="utf-8")

    assert text.count("status: PASS_P51_M3_SPATIAL_SIR_ROUTE_PREFLIGHT") == 1
    assert "Production spatial SIR filtering remains blocked" in text
    assert "BLOCKED_M4B_ROUTE_ARCHITECTURE" in text
    assert "No HMC readiness" in text
