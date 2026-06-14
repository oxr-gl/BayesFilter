from __future__ import annotations

import pytest

import bayesfilter.highdim as highdim


def _contract(**overrides: object) -> highdim.GradientLaneEvidenceContract:
    values = {
        "route_label": highdim.GRADIENT_ADAPTATION_ROUTE_LABEL,
        "branch_replay_status": "passed_full_manifest_replay",
        "value_gradient_status": "passed_scale_aware_directional_checks",
        "likelihood_variance_calibration_status": "policy_defined_not_promotion",
        "hmc_readiness_status": "blocked_tier2_tier3_not_run",
        "source_fidelity_claim": False,
        "differentiates_adaptive_random_branch": False,
        "required_hmc_tiers": (),
        "nonclaims": (
            "no source-faithful filtering claim",
            "no HMC readiness by default",
        ),
    }
    values.update(overrides)
    return highdim.GradientLaneEvidenceContract(**values)


def test_p49_gradient_lane_contract_accepts_honest_adaptation_boundary() -> None:
    contract = _contract()
    payload = contract.manifest_payload()

    assert payload["route_label"] == highdim.GRADIENT_ADAPTATION_ROUTE_LABEL
    assert payload["source_fidelity_claim"] is False
    assert payload["hmc_readiness_status"] == "blocked_tier2_tier3_not_run"
    assert "no source-faithful filtering claim" in payload["nonclaims"]


def test_p49_gradient_lane_contract_rejects_source_fidelity_claim() -> None:
    with pytest.raises(ValueError, match="source-faithful"):
        _contract(source_fidelity_claim=True)


def test_p49_gradient_lane_contract_rejects_adaptive_random_differentiation() -> None:
    with pytest.raises(ValueError, match="adaptive random"):
        _contract(differentiates_adaptive_random_branch=True)


def test_p49_gradient_lane_contract_rejects_hmc_promotion_without_tiers() -> None:
    with pytest.raises(ValueError, match="HMC readiness promotion"):
        _contract(hmc_readiness_status="promoted")


def test_p49_gradient_lane_contract_rejects_unknown_hmc_status_and_tiers() -> None:
    with pytest.raises(ValueError, match="unknown P49"):
        _contract(hmc_readiness_status="looks_good")

    with pytest.raises(ValueError, match="nonempty tiers"):
        _contract(hmc_readiness_status="promoted", required_hmc_tiers=("",))

    with pytest.raises(ValueError, match="unknown HMC tier"):
        _contract(
            hmc_readiness_status="promoted",
            required_hmc_tiers=("TIER_MAGIC_FAST_CHAINS",),
        )


def test_p49_gradient_lane_contract_allows_hmc_promotion_only_with_tiers() -> None:
    contract = _contract(
        hmc_readiness_status="promoted",
        required_hmc_tiers=(
            "TIER_1_LOCAL_VALUE_AND_DIRECTIONAL_SCORE",
            "TIER_2_SHORT_CHAIN_DIAGNOSTICS",
            "TIER_3_HAMILTONIAN_LEAPFROG_FOR_HMC",
        ),
        nonclaims=(
            "no source-faithful filtering claim",
            "no HMC readiness by default",
            "HMC readiness is limited to the declared target and tiers",
        ),
    )

    assert contract.hmc_readiness_status == "promoted"
    assert "TIER_3_HAMILTONIAN_LEAPFROG_FOR_HMC" in contract.required_hmc_tiers


def test_p49_gradient_lane_contract_rejects_wrong_route_label_and_missing_nonclaims() -> None:
    with pytest.raises(ValueError, match="gradient_bearing_adaptation"):
        _contract(route_label=highdim.SOURCE_FAITHFUL_ROUTE_LABEL)

    with pytest.raises(ValueError, match="missing nonclaim"):
        _contract(nonclaims=("no source-faithful filtering claim",))
