from __future__ import annotations

import pytest

import bayesfilter.inference as inference
from bayesfilter.inference.fixed_trajectory_hmc_tuning_v2 import (
    FIXED_TRAJECTORY_HMC_V2_ACCEPTANCE_BAND,
    run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2,
)


def test_tiny_gaussian_fixed_trajectory_hmc_selects_explicit_candidate():
    result = run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2(
        step_size_candidates=(0.5, 0.8, 1.0),
        num_leapfrog_step_candidates=(2,),
        num_results=16,
        num_burnin_steps=0,
        seed=(20260612, 7),
    )
    payload = result.payload()

    assert result.passed is True
    assert result.policy_label == "fixed_trajectory_hmc_tuning_v2_first_slice"
    assert result.mass_policy == "identity"
    assert result.acceptance_band == FIXED_TRAJECTORY_HMC_V2_ACCEPTANCE_BAND
    assert result.selected_step_size == pytest.approx(0.8)
    assert result.selected_num_leapfrog_steps == 2
    assert result.selected_trajectory_length == pytest.approx(1.6)
    assert result.selected_candidate is not None
    assert result.selected_candidate.acceptance_rate == pytest.approx(0.75)
    assert result.selected_candidate.outcome == "passed_screen"
    assert "no posterior convergence claim" in result.nonclaims
    assert payload["reports_posterior_convergence"] is False
    assert payload["reports_sampler_superiority"] is False
    assert payload["reports_default_readiness"] is False
    assert payload["diagnostics"]["runtime"] == "tfp.mcmc.HamiltonianMonteCarlo"
    assert payload["diagnostics"]["acceptance_band_role"] == (
        "tuning_promotion_screen_only"
    )
    assert payload["diagnostics"]["legacy_fixed_kernel_screen_band"] == (
        "(0.05, 0.99) separate broad screen"
    )


def test_tiny_gaussian_fixed_trajectory_hmc_rejects_out_of_band_candidates():
    result = run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2(
        step_size_candidates=(0.1,),
        num_leapfrog_step_candidates=(2,),
        num_results=16,
        num_burnin_steps=0,
        seed=(20260612, 7),
    )

    assert result.passed is False
    assert result.vetoes == ("no_candidate_in_closed_acceptance_promotion_band",)
    assert result.selected_candidate is None
    assert result.candidate_results[0].outcome == "rejected_accept_high"
    assert result.candidate_results[0].vetoes == (
        "acceptance_above_closed_promotion_band",
    )


def test_tiny_gaussian_fixed_trajectory_hmc_fails_closed_for_nuts_request():
    with pytest.raises(ValueError, match="NUTS is reference/diagnostic only"):
        run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2(requested_kernel="nuts")


def test_tiny_gaussian_fixed_trajectory_hmc_first_slice_identity_mass_only():
    with pytest.raises(ValueError, match="identity"):
        run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2(
            mass_policy="windowed_mass_adaptation_future"
        )


def test_fixed_trajectory_hmc_tuning_v2_is_not_shared_api_export():
    assert "FIXED_TRAJECTORY_ACCEPTANCE_BAND" not in inference.__all__
    assert "run_tiny_gaussian_fixed_trajectory_hmc_tuning" not in inference.__all__
    assert "FIXED_TRAJECTORY_HMC_V2_ACCEPTANCE_BAND" not in inference.__all__
    assert "run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2" not in inference.__all__
    assert not hasattr(inference, "FIXED_TRAJECTORY_ACCEPTANCE_BAND")
    assert not hasattr(inference, "run_tiny_gaussian_fixed_trajectory_hmc_tuning")
    assert not hasattr(inference, "FIXED_TRAJECTORY_HMC_V2_ACCEPTANCE_BAND")
    assert not hasattr(inference, "run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2")
