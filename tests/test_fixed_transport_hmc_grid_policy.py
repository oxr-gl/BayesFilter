from __future__ import annotations

import json

import bayesfilter
from bayesfilter.inference import (
    FixedTransportHMCGridCandidateSpec,
    FixedTransportHMCJointPreparedGrid,
    FixedTransportHMCPreparedGrid,
    FixedTransportHMCGridPolicyConfig,
    FixedTransportHMCGridPolicySpec,
    build_fixed_transport_hmc_grid_policy_spec,
    prepare_fixed_transport_hmc_adaptive_joint_grid_policy,
    prepare_fixed_transport_hmc_joint_grid_policy,
    prepare_fixed_transport_hmc_grid_policy,
)


def test_fixed_transport_hmc_grid_policy_builds_public_hashable_spec() -> None:
    spec = build_fixed_transport_hmc_grid_policy_spec(step_size_scale=1.3)
    payload = spec.payload()

    assert isinstance(spec, FixedTransportHMCGridPolicySpec)
    assert payload["artifact_type"] == "bayesfilter_fixed_transport_hmc_grid_policy_spec"
    assert payload["candidate_count"] == 63
    assert payload["status"] == "coarse_grid_only"
    assert payload["policy_hash"] == spec.policy_hash
    assert payload["hash_function"] == "bayesfilter.runtime.stable_config_hash"
    assert payload["candidate_specs"][0]["step_size"] == 0.065
    assert payload["candidate_specs"][-1]["step_size"] == 0.65
    assert payload["candidate_specs"][-1]["num_leapfrog_steps"] == 25
    assert "does not run HMC" in payload["nonclaims"]
    assert json.loads(json.dumps(payload, sort_keys=True))


def test_fixed_transport_hmc_grid_policy_enforces_min_l_and_trajectory() -> None:
    config = FixedTransportHMCGridPolicyConfig(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 3, 4, 8),
        min_num_leapfrog_steps=2,
        min_trajectory_time=1.0,
        max_num_leapfrog_steps=8,
    )

    spec = build_fixed_transport_hmc_grid_policy_spec(
        step_size_scale=1.0,
        config=config,
    )
    payload = spec.payload()
    identities = {
        (candidate["step_size"], candidate["num_leapfrog_steps"])
        for candidate in payload["candidate_specs"]
    }

    assert payload["candidate_count"] == 4
    assert identities == {(0.5, 2), (0.5, 3), (0.5, 4), (0.5, 8)}
    assert all(
        candidate["num_leapfrog_steps"] >= 2
        and candidate["trajectory_time"] >= 1.0
        for candidate in payload["candidate_specs"]
    )


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
    assert payload["candidate_count"] > 63
    assert "high_acceptance_shorter_L_and_in_band_longer_L_boundary" in (
        payload["refinement_reasons"]
    )
    assert (0.65, 18) in identities
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
    assert bayesfilter.FixedTransportHMCPreparedGrid is (
        FixedTransportHMCPreparedGrid
    )
    assert bayesfilter.FixedTransportHMCJointPreparedGrid is (
        FixedTransportHMCJointPreparedGrid
    )
    assert bayesfilter.prepare_fixed_transport_hmc_grid_policy is (
        prepare_fixed_transport_hmc_grid_policy
    )
    assert bayesfilter.prepare_fixed_transport_hmc_joint_grid_policy is (
        prepare_fixed_transport_hmc_joint_grid_policy
    )
    assert bayesfilter.prepare_fixed_transport_hmc_adaptive_joint_grid_policy is (
        prepare_fixed_transport_hmc_adaptive_joint_grid_policy
    )
    assert "FixedTransportHMCGridPolicySpec" in bayesfilter.__all__
    assert "FixedTransportHMCPreparedGrid" in bayesfilter.__all__
    assert "FixedTransportHMCJointPreparedGrid" in bayesfilter.__all__
    assert "prepare_fixed_transport_hmc_grid_policy" in bayesfilter.__all__
    assert "prepare_fixed_transport_hmc_joint_grid_policy" in bayesfilter.__all__
    assert "prepare_fixed_transport_hmc_adaptive_joint_grid_policy" in (
        bayesfilter.__all__
    )


def test_prepare_fixed_transport_hmc_grid_policy_requires_real_attempts() -> None:
    try:
        prepare_fixed_transport_hmc_grid_policy(
            base_step_size_candidates=(0.05, 0.5),
            num_leapfrog_step_candidates=(5, 25),
            scale_candidates=(1.0, 5.0, 9.0),
            pilot_acceptance_rates=(),
            pilot_base_step_size=0.5,
            pilot_num_leapfrog_steps=5,
        )
    except ValueError as exc:
        assert "pilot_acceptance_rates" in str(exc)
    else:  # pragma: no cover - defensive assertion
        raise AssertionError("empty pilot attempts must be rejected")


def test_prepare_fixed_transport_hmc_grid_policy_builds_ready_spec() -> None:
    prepared = prepare_fixed_transport_hmc_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(5, 25),
        scale_candidates=(1.0, 5.0, 9.0),
        pilot_acceptance_rates=(0.96, 0.91, 0.70),
        pilot_base_step_size=0.5,
        pilot_num_leapfrog_steps=5,
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert prepared.launch_ready
    assert payload["artifact_type"] == "bayesfilter_fixed_transport_hmc_prepared_grid"
    assert payload["status"] == "prepared_grid_ready"
    assert payload["selected_scale"] == 9.0
    assert payload["tuning_attempt_count"] == 3
    assert payload["prepared_candidate_count"] == 4
    assert payload["policy_spec"]["candidate_specs"][0]["step_size"] == 0.45
    assert payload["policy_spec"]["candidate_specs"][-1]["step_size"] == 4.5
    assert payload["prepared_policy_hash"] == payload["policy_spec"]["policy_hash"]
    assert payload["prepared_grid_hash"] == prepared.prepared_grid_hash
    assert "does not run the final HMC candidate grid" in payload["nonclaims"]


def test_prepare_fixed_transport_hmc_grid_policy_fails_warning_band_closed() -> None:
    prepared = prepare_fixed_transport_hmc_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(5, 25),
        scale_candidates=(1.0, 5.0),
        pilot_acceptance_rates=(0.95, 0.80),
        pilot_base_step_size=0.5,
        pilot_num_leapfrog_steps=5,
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["policy_spec"] is None
    assert payload["prepared_policy_hash"] is None
    assert payload["status"] == "scale_selected_warning_band"
    assert payload["hard_vetoes"] == ("scale_not_in_acceptance_band",)


def test_prepare_fixed_transport_hmc_joint_grid_policy_builds_ready_spec() -> None:
    prepared = prepare_fixed_transport_hmc_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 8),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.90,
                "finite": True,
            },
            {
                "candidate_index": 1,
                "step_size": 0.75,
                "num_leapfrog_steps": 2,
                "acceptance_rate": 0.70,
                "finite": True,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert prepared.launch_ready
    assert payload["artifact_type"] == (
        "bayesfilter_fixed_transport_hmc_joint_prepared_grid")
    assert payload["status"] == "joint_prepared_grid_ready"
    assert payload["selected_joint_pilot_tuple"] == {
        "step_size": 0.75,
        "num_leapfrog_steps": 2,
    }
    assert payload["selected_scale"] == 1.5
    assert payload["selected_joint_pilot_candidate_match"] is True
    assert payload["prepared_policy_hash"] == payload["policy_spec"]["policy_hash"]
    identities = {
        (candidate["step_size"], candidate["num_leapfrog_steps"])
        for candidate in payload["policy_spec"]["candidate_specs"]
    }
    assert (0.75, 2) in identities
    assert payload["tuning_attempt_count"] == 2
    assert payload["selected_joint_pilot_row_hash"]
    assert "selected scale is descriptive only when present" in payload["nonclaims"]


def test_prepare_fixed_transport_hmc_joint_grid_policy_enforces_min_trajectory() -> None:
    prepared = prepare_fixed_transport_hmc_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 8),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.8,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.70,
                "finite": True,
            },
            {
                "candidate_index": 1,
                "step_size": 0.2,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.72,
                "finite": True,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        min_num_leapfrog_steps=8,
        min_trajectory_time=1.0,
    )
    payload = prepared.payload()

    assert prepared.launch_ready
    assert payload["selected_joint_pilot_tuple"] == {
        "step_size": 0.2,
        "num_leapfrog_steps": 8,
    }
    assert payload["joint_pilot_rows"][0]["acceptance_class"] == "in_band"
    assert payload["joint_pilot_rows"][0]["launch_eligible"] is False
    assert payload["joint_pilot_rows"][0]["launch_eligibility_reasons"] == (
        "short_leapfrog",
        "short_trajectory_time",
    )
    assert payload["policy_spec"]["config"]["min_num_leapfrog_steps"] == 8
    assert payload["policy_spec"]["config"]["min_trajectory_time"] == 1.0


def test_prepare_fixed_transport_hmc_joint_grid_policy_fails_without_in_band() -> None:
    prepared = prepare_fixed_transport_hmc_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 8),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.80,
                "finite": True,
            },
            {
                "candidate_index": 1,
                "step_size": 0.5,
                "num_leapfrog_steps": 2,
                "acceptance_rate": 0.60,
                "finite": True,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["policy_spec"] is None
    assert payload["selected_joint_pilot_tuple"] is None
    assert payload["status"] == "joint_grid_selected_warning_band"
    assert payload["hard_vetoes"] == (
        "joint_pilot_warning_band_not_launch_ready",)


def test_prepare_fixed_transport_hmc_joint_grid_policy_fails_invalid_closed() -> None:
    prepared = prepare_fixed_transport_hmc_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 8),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.70,
                "finite": False,
                "hard_veto_reasons": ["bayesfilter_principal_sqrt_nonpositive_covariance"],
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["status"] == "joint_grid_search_failed_all_invalid"
    assert payload["hard_vetoes"] == ("joint_pilot_rows_all_invalid",)
    assert payload["joint_pilot_rows"][0]["acceptance_class"] == "invalid"


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_requests_high_scale() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.05,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 1.0,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.5,
                "num_leapfrog_steps": 2,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["adaptive"] is True
    assert payload["status"] == "adaptive_joint_grid_next_round_requested"
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_scale_request"] == 9.0
    assert payload["policy_spec"] is None
    assert payload["hard_vetoes"] == ()
    assert payload["next_joint_pilot_candidate_count"] == 4
    assert {
        (row["step_size"], row["num_leapfrog_steps"])
        for row in payload["next_joint_pilot_tuples"]
    } == {(0.45, 1), (0.45, 2), (4.5, 1), (4.5, 2)}
    assert payload["reports_posterior_convergence"] is False


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_respects_finite_domain_ceiling() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(8, 16),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.45,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.94,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.9,
                "num_leapfrog_steps": 16,
                "acceptance_rate": None,
                "finite": False,
                "hard_veto_reasons": [
                    "candidate_finite_domain_error",
                    "bayesfilter_principal_sqrt_nonpositive_covariance",
                ],
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_scale_request"] == 1.62
    assert payload["adaptive_request_reason"] == (
        "latest_valid_acceptance_high_with_finite_domain_ceiling_factor_0.9")


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_nudges_warning_with_finite_domain_ceiling() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(8, 16),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.6075,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.7734375,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.81,
                "num_leapfrog_steps": 16,
                "acceptance_rate": None,
                "finite": False,
                "hard_veto_reasons": [
                    "candidate_finite_domain_error",
                    "bayesfilter_principal_sqrt_nonpositive_covariance",
                ],
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_scale_request"] == 1.701
    assert payload["adaptive_request_reason"] == (
        "latest_high_warning_candidate_local_scale_refinement")
    assert payload["next_joint_pilot_candidate_count"] == 16


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_refines_too_high_same_l() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(2, 3),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 2,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.6,
                "num_leapfrog_steps": 3,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 2,
                "step_size": 0.8,
                "num_leapfrog_steps": 3,
                "acceptance_rate": None,
                "finite": False,
                "hard_veto_reasons": [
                    "candidate_finite_domain_error",
                    "bayesfilter_principal_sqrt_nonpositive_covariance",
                ],
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        min_num_leapfrog_steps=2,
        min_trajectory_time=1.0,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()
    requested = {
        (row["step_size"], row["num_leapfrog_steps"])
        for row in payload["next_joint_pilot_tuples"]
    }

    assert not prepared.launch_ready
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_request_reason"] == (
        "latest_too_high_candidate_same_leapfrog_local_step_refinement")
    assert (0.8, 2) in requested
    assert (0.72, 3) in requested


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_local_refines_near_band_ceiling() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.075, 0.1, 0.15, 0.2, 0.3, 0.5),
        num_leapfrog_step_candidates=(8, 16, 25),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.3255076125,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.984375,
                "finite": True,
                "base_step_size": 0.05,
                "adaptive_round_index": 7,
            },
            {
                "candidate_index": 1,
                "step_size": 0.48826141875,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.7578125,
                "finite": True,
                "base_step_size": 0.075,
                "adaptive_round_index": 7,
            },
            {
                "candidate_index": 2,
                "step_size": 0.651015225,
                "num_leapfrog_steps": 8,
                "acceptance_rate": None,
                "finite": False,
                "base_step_size": 0.1,
                "hard_veto_reasons": [
                    "candidate_finite_domain_error",
                    "bayesfilter_principal_sqrt_nonpositive_covariance",
                ],
                "adaptive_round_index": 7,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        min_num_leapfrog_steps=8,
        min_trajectory_time=1.0,
        max_adaptive_rounds=10,
    )
    payload = prepared.payload()
    requested = {
        (row["step_size"], row["num_leapfrog_steps"])
        for row in payload["next_joint_pilot_tuples"]
    }

    assert not prepared.launch_ready
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_request_reason"] == (
        "latest_high_warning_candidate_local_scale_refinement")
    assert (0.463848347812, 8) in requested
    assert (0.476054883281, 8) in requested
    assert (0.500467954219, 8) in requested
    assert payload["next_joint_pilot_candidate_count"] <= 36


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_treats_sylvester_factor_as_ceiling() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(8, 16),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.6075,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.7734375,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.81,
                "num_leapfrog_steps": 16,
                "acceptance_rate": None,
                "finite": False,
                "hard_veto_reasons": [
                    "candidate_finite_domain_error",
                    "bayesfilter_symmetric_sylvester_nonpositive_factor",
                ],
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["adaptive_request_reason"] == (
        "latest_high_warning_candidate_local_scale_refinement")


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_ignores_short_in_band() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2, 8),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.8,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.70,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 0.2,
                "num_leapfrog_steps": 8,
                "acceptance_rate": 0.95,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
        min_num_leapfrog_steps=8,
        min_trajectory_time=1.0,
        max_adaptive_rounds=5,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["status"] == "adaptive_joint_grid_next_round_requested"
    assert payload["adaptive_request_status"] == "next_round_requested"
    assert payload["selected_joint_pilot_tuple"] is None
    assert payload["joint_pilot_rows"][0]["acceptance_class"] == "in_band"
    assert payload["joint_pilot_rows"][0]["launch_eligible"] is False
    assert payload["joint_pilot_rows"][0]["launch_eligibility_reasons"] == (
        "short_leapfrog",
        "short_trajectory_time",
    )
    assert payload["next_joint_pilot_candidate_count"] > 0


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_requests_warning_scale_five() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1,),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.80,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        fallback_acceptance_max=0.85,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["adaptive_scale_request"] == 5.0
    assert payload["next_joint_pilot_tuples"][0]["step_size"] == 0.25
    assert payload["next_joint_pilot_tuples"][-1]["step_size"] == 2.5


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_requests_low_scale() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1,),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.45,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
    )
    payload = prepared.payload()
    assert payload["adaptive_scale_request"] == 0.2

    prepared_lower = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1,),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.35,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
    )
    assert prepared_lower.payload()["adaptive_scale_request"] == 0.1


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_excludes_seen_invalid_rows() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1,),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.90,
                "finite": False,
                "hard_vetoes": ["finite_domain"],
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 4.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 1,
            },
        ),
        acceptance_band=(0.65, 0.75),
    )
    payload = prepared.payload()

    assert payload["adaptive_round_count"] == 2
    assert payload["adaptive_scale_request"] == 81.0
    assert {
        (row["step_size"], row["num_leapfrog_steps"])
        for row in payload["next_joint_pilot_tuples"]
    } == {(4.05, 1), (40.5, 1)}
    assert payload["joint_pilot_rows"][0]["acceptance_class"] == "invalid"


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_ready_later_round() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1, 2),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 0,
            },
            {
                "candidate_index": 1,
                "step_size": 4.5,
                "num_leapfrog_steps": 2,
                "acceptance_rate": 0.70,
                "finite": True,
                "adaptive_round_index": 1,
            },
        ),
        acceptance_band=(0.65, 0.75),
    )
    payload = prepared.payload()

    assert prepared.launch_ready
    assert payload["status"] == "joint_prepared_grid_ready"
    assert payload["adaptive_request_status"] == "ready"
    assert payload["adaptive_round_count"] == 2
    assert payload["next_joint_pilot_tuples"] == ()
    assert payload["selected_joint_pilot_tuple"] == {
        "step_size": 4.5,
        "num_leapfrog_steps": 2,
    }
    assert payload["selected_joint_pilot_candidate_match"] is True
    assert payload["prepared_policy_hash"] == payload["policy_spec"]["policy_hash"]


def test_prepare_fixed_transport_hmc_adaptive_joint_grid_max_rounds_closed() -> None:
    prepared = prepare_fixed_transport_hmc_adaptive_joint_grid_policy(
        base_step_size_candidates=(0.05, 0.5),
        num_leapfrog_step_candidates=(1,),
        joint_pilot_rows=(
            {
                "candidate_index": 0,
                "step_size": 0.5,
                "num_leapfrog_steps": 1,
                "acceptance_rate": 0.90,
                "finite": True,
                "adaptive_round_index": 0,
            },
        ),
        acceptance_band=(0.65, 0.75),
        max_adaptive_rounds=1,
    )
    payload = prepared.payload()

    assert not prepared.launch_ready
    assert payload["status"] == "adaptive_joint_grid_max_rounds_exhausted"
    assert payload["adaptive_request_status"] == "max_rounds_exhausted"
    assert payload["policy_spec"] is None
    assert payload["hard_vetoes"] == (
        "adaptive_joint_pilot_max_rounds_exhausted",)
