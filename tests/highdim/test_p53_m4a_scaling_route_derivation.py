from __future__ import annotations

import json
from pathlib import Path


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-manifest-2026-06-10.json"
)
RESULT_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-result-2026-06-10.md"
)
SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-subplan-2026-06-10.md"
)


def _manifest() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_p53_m4a_selects_exactly_one_scaling_route_not_c_low_relabel() -> None:
    manifest = _manifest()
    selected = manifest["selected_route"]

    assert manifest["schema_version"] == "p53.scaling_route_derivation.v1"
    assert manifest["status"] == "PASS_P53_M4A_SCALING_ROUTE_DERIVATION"
    assert selected["route_class"] == "scaling_route"
    assert selected["selected_design"] == "local-neighborhood sparse transition contraction"
    assert len(selected["rejected_designs"]) == 1
    assert selected["not_a_relabel_of"] == "p53_lower_rung_streaming_dense_equivalent"
    assert selected["implementation_phase"] == "P53-M4B"
    assert selected["tieout_phase"] == "P53-M4C"
    assert selected["admission_phase"] == "P53-M4D"


def test_p53_m4a_derivation_declares_exactness_scope_and_block_conditions() -> None:
    manifest = _manifest()
    applicability = manifest["applicability"]
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert applicability["exact_when"][0] == "process covariance is diagonal"
    assert "neighborhood mask contains every previous-state coordinate" in applicability["exact_when"][1]
    assert "process covariance is non-diagonal" in applicability["blocks_when"][0]
    assert "approximation_status" in applicability
    assert "Exactness Scope" in result
    assert "must block rather than pass" in result
    assert "block-local" not in applicability["approximation_status"]


def test_p53_m4a_metadata_contract_exposes_reff_memory_and_replay() -> None:
    manifest = _manifest()
    metadata = manifest["metadata_contract"]
    derivation = manifest["derivation"]
    result = RESULT_PATH.read_text(encoding="utf-8")

    assert metadata["route_width_bound_name"] == "R_eff"
    assert "q^(|N_a|)" in metadata["route_width_bound_formula"]
    assert "O(d * q^w" in metadata["memory_forecast_formula"]
    for field in (
        "route_id",
        "route_class",
        "selected_design",
        "dependency_neighborhoods",
        "R_eff",
        "memory_forecast_bytes",
        "replay_identity",
        "covariance_scope",
    ):
        assert field in metadata["required_fields"]
    for field in (
        "route_id",
        "route_class",
        "selected_design",
        "rk4_substeps",
        "dependency_neighborhoods",
        "basis_order",
        "tt_rank_metadata",
        "R_eff",
        "memory_forecast_bytes",
        "covariance_scope",
        "dtype",
        "branch_id",
    ):
        assert field in metadata["required_replay_identity_fields"]
    assert "log K_theta" in derivation["transition_factorization"]
    assert "Replay And Metadata" in result


def test_p53_m4a_tieout_contract_is_predeclared_for_j1_j2_j3() -> None:
    manifest = _manifest()
    tieout = manifest["tieout_contract"]

    assert [row["compartments"] for row in tieout["dimensions"]] == [1, 2, 3]
    assert [row["state_dim"] for row in tieout["dimensions"]] == [2, 4, 6]
    assert tieout["predictive_log_density_atol"] == 1e-8
    assert tieout["one_step_log_increment_atol"] == 1e-8
    assert tieout["gradient_atol"] == 1e-6
    assert "dense retained-grid route" in tieout["baseline"]
    assert "C_low predictive update is admissible only as a computational proxy" in tieout["baseline"]
    assert "no dense all-pairs global pair enumeration" in tieout["metadata_checks"]


def test_p53_m4a_emits_only_derivation_token_and_subplan_forbids_deferral() -> None:
    manifest = _manifest()
    subplan = SUBPLAN_PATH.read_text(encoding="utf-8")

    assert manifest["tokens_emitted"] == ["PASS_P53_M4A_SCALING_ROUTE_DERIVATION"]
    assert "PASS_P53_M4D_SCALING_ROUTE_ADMISSION" in manifest["forbidden_tokens"]
    assert "PASS_P53_M5_RANK_SELECTION_INTEGRATION" in manifest["forbidden_tokens"]
    assert "Route choice deferred to M4B" in subplan
    assert "Passing M4A does not implement the route" in subplan
