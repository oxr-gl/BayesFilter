from __future__ import annotations

import json
from pathlib import Path

import pytest

from bayesfilter import highdim


FILTERING_PATH = Path("bayesfilter/highdim/filtering.py")
MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-manifest-2026-06-10.json"
)
SUBPLAN_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-subplan-2026-06-10.md"
)


def test_p52_m4_rejects_forbidden_dense_transition_interfaces() -> None:
    for interface in highdim.P52_FORBIDDEN_TRANSITION_INTERFACES:
        with pytest.raises(ValueError, match="dense all-pairs"):
            highdim.FactorizedTransitionRouteContract(
                route_id="bad",
                transition_interface=interface,
                materializes_dense_pairs=True,
                deterministic_replay=True,
                differentiable_backend="tensorflow",
                exposes_reff_bound=False,
                effective_transition_rank_multiplier=None,
                memory_metadata_available=False,
                status="BLOCK_P52_FACTORIZED_ROUTE_IMPLEMENTATION_MISSING",
                blocker="forbidden",
            )


def test_p52_m4_passing_contract_requires_replay_reff_and_memory_metadata() -> None:
    with pytest.raises(ValueError, match="R_eff"):
        highdim.FactorizedTransitionRouteContract(
            route_id="missing-reff",
            transition_interface="tt_mpo_factorized_contraction",
            materializes_dense_pairs=False,
            deterministic_replay=True,
            differentiable_backend="tensorflow",
            exposes_reff_bound=False,
            effective_transition_rank_multiplier=None,
            memory_metadata_available=True,
            status="PASS_P52_FACTORIZED_ROUTE_CONTRACT",
        )

    contract = highdim.FactorizedTransitionRouteContract(
        route_id="ok",
        transition_interface="tt_mpo_factorized_contraction",
        materializes_dense_pairs=False,
        deterministic_replay=True,
        differentiable_backend="tensorflow",
        exposes_reff_bound=True,
        effective_transition_rank_multiplier=16,
        memory_metadata_available=True,
        status="PASS_P52_FACTORIZED_ROUTE_CONTRACT",
    )
    payload = contract.manifest_payload()
    assert payload["status"] == "PASS_P52_FACTORIZED_ROUTE_CONTRACT"
    assert payload["claim_class"] == "route_contract_not_filtering_correctness"
    assert "no filtering correctness" in payload["nonclaims"]


def test_p52_m4_static_audit_finds_current_dense_multistate_pairwise_route() -> None:
    text = FILTERING_PATH.read_text(encoding="utf-8")

    assert "def _multistate_pairwise_transition_between_grids_log_density" in text
    assert "tf.repeat(current, repeats=previous_count, axis=0)" in text
    assert "tf.tile(previous, [current_count, 1])" in text
    assert "Build a fixed multistate transition target from an all-axes retained grid" in text


def test_p52_m4_blocker_manifest_preserves_repair_target_and_nonclaims() -> None:
    manifest = highdim.p52_current_spatial_sir_route_blocker_manifest()
    current = manifest["current_route"]
    required = manifest["required_contract"]
    subplan = SUBPLAN_PATH.read_text(encoding="utf-8")

    assert manifest["schema_version"] == "p52.factorized_transition_route.v1"
    assert manifest["status"] == "BLOCK_P52_FACTORIZED_TRANSITION_ROUTE"
    assert current["materializes_dense_pairs"] is True
    assert current["transition_interface"] == "multistate_grid_pairwise_transition"
    assert "_multistate_pairwise_transition_between_grids_log_density" in current["blocked_functions"]
    assert required["transition_interface"] == "tt_mpo_factorized_contraction"
    assert required["materializes_dense_pairs"] is False
    assert required["status"] == "BLOCK_P52_FACTORIZED_ROUTE_IMPLEMENTATION_MISSING"
    assert "R_eff" in required["blocker"]
    assert "no d=18 spatial SIR filtering" in manifest["nonclaims"]
    assert "Static and dynamic route checks" in subplan
    assert "dense all-pairs" in subplan
    assert "`R_eff`" in subplan
    assert "memory metadata" in subplan


def test_p52_m4_persisted_manifest_matches_blocker_contract() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected = highdim.p52_current_spatial_sir_route_blocker_manifest()

    assert manifest["schema_version"] == expected["schema_version"]
    assert manifest["status"] == "BLOCK_P52_FACTORIZED_TRANSITION_ROUTE"
    assert manifest["current_route"]["materializes_dense_pairs"] is True
    assert manifest["required_contract"]["status"] == (
        "BLOCK_P52_FACTORIZED_ROUTE_IMPLEMENTATION_MISSING"
    )
    assert manifest["tokens_emitted"] == ["BLOCK_P52_FACTORIZED_TRANSITION_ROUTE"]
    assert "no factorized route implementation" in manifest["nonclaims"]
