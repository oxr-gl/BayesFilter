from __future__ import annotations

import json

import bayesfilter
from bayesfilter.inference import (
    FixedTransportHMCGridCandidateSpec,
    FixedTransportHMCGridPolicyConfig,
    FixedTransportHMCGridPolicySpec,
    build_fixed_transport_hmc_grid_policy_spec,
)


def test_fixed_transport_hmc_grid_policy_builds_public_hashable_spec() -> None:
    spec = build_fixed_transport_hmc_grid_policy_spec(step_size_scale=1.3)
    payload = spec.payload()

    assert isinstance(spec, FixedTransportHMCGridPolicySpec)
    assert payload["artifact_type"] == "bayesfilter_fixed_transport_hmc_grid_policy_spec"
    assert payload["candidate_count"] == 49
    assert payload["status"] == "coarse_grid_only"
    assert payload["policy_hash"] == spec.policy_hash
    assert payload["hash_function"] == "bayesfilter.runtime.stable_config_hash"
    assert payload["candidate_specs"][0]["step_size"] == 0.065
    assert payload["candidate_specs"][-1]["step_size"] == 0.65
    assert payload["candidate_specs"][-1]["num_leapfrog_steps"] == 25
    assert "does not run HMC" in payload["nonclaims"]
    assert json.loads(json.dumps(payload, sort_keys=True))


def test_fixed_transport_hmc_grid_policy_refines_observed_boundary() -> None:
    rows = (
        {
            "candidate_index": 47,
            "step_size": 0.65,
            "num_leapfrog_steps": 16,
            "acceptance_rate": 0.767578125,
        },
        {
            "candidate_index": 48,
            "step_size": 0.65,
            "num_leapfrog_steps": 25,
            "acceptance_rate": 0.7428385416666666,
        },
    )

    spec = build_fixed_transport_hmc_grid_policy_spec(
        step_size_scale=1.3,
        observed_candidate_rows=rows,
    )
    payload = spec.payload()
    refinement = [
        candidate
        for candidate in payload["candidate_specs"]
        if candidate["grid_stage"] == "local_refinement_grid"
    ]
    identities = {
        (candidate["step_size"], candidate["num_leapfrog_steps"])
        for candidate in refinement
    }

    assert payload["status"] == "refinement_added"
    assert payload["candidate_count"] > 49
    assert "high_acceptance_shorter_L_and_in_band_longer_L_boundary" in (
        payload["refinement_reasons"]
    )
    assert (0.65, 18) in identities
    assert (0.65, 20) in identities
    assert (0.75, 16) in identities
    assert (0.8, 20) in identities
    assert (0.85, 25) in identities
    assert all(candidate["num_leapfrog_steps"] <= 25 for candidate in refinement)


def test_fixed_transport_hmc_grid_policy_hash_changes_with_rules() -> None:
    default_spec = build_fixed_transport_hmc_grid_policy_spec(step_size_scale=1.3)
    changed_spec = build_fixed_transport_hmc_grid_policy_spec(
        step_size_scale=1.3,
        config=FixedTransportHMCGridPolicyConfig(
            refinement_step_size_increment=0.025,
        ),
    )

    assert default_spec.policy_hash != changed_spec.policy_hash


def test_fixed_transport_hmc_grid_policy_public_imports() -> None:
    assert bayesfilter.FixedTransportHMCGridCandidateSpec is (
        FixedTransportHMCGridCandidateSpec
    )
    assert bayesfilter.FixedTransportHMCGridPolicyConfig is (
        FixedTransportHMCGridPolicyConfig
    )
    assert bayesfilter.FixedTransportHMCGridPolicySpec is (
        FixedTransportHMCGridPolicySpec
    )
    assert bayesfilter.build_fixed_transport_hmc_grid_policy_spec is (
        build_fixed_transport_hmc_grid_policy_spec
    )
    assert "FixedTransportHMCGridPolicySpec" in bayesfilter.__all__
