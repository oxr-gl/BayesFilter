from __future__ import annotations

import json

import numpy as np
import pytest

from bayesfilter.inference import (
    FixedTrajectoryTuningConfig,
    HMCTuningPolicy,
    PrecomputedMassArtifact,
    WindowedMassAdaptationConfig,
    production_leapfrog_count,
    run_fixed_trajectory_tuning_diagnostic,
    run_windowed_mass_adaptation_diagnostic,
)
from bayesfilter.inference.fixed_trajectory_hmc_tuning_v2 import (
    run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2,
)


def _mass_artifact() -> PrecomputedMassArtifact:
    return PrecomputedMassArtifact.from_negative_hessian(
        position=np.zeros(3),
        negative_hessian=np.array(
            [
                [4.0, 0.25, 0.10],
                [0.25, 3.0, 0.05],
                [0.10, 0.05, 2.5],
            ],
            dtype=float,
        ),
        adapter_signature="phase5_trajectory_adapter_v1",
        covariance_source="phase2_regularized_hessian",
        jitter=0.0,
        eigenvalue_floor=1.0e-6,
    )


def _windowed_result():
    config = WindowedMassAdaptationConfig(
        warmup_steps=12,
        initial_buffer=2,
        final_buffer=2,
        first_window_size=3,
        min_window_samples=2,
        mass_shrinkage=0.25,
        covariance_jitter=1.0e-6,
        step_adaptation_rate=0.0,
    )
    draws = np.array(
        [
            [-0.20, 0.10, 0.00],
            [-0.10, 0.00, 0.05],
            [0.10, 0.20, 0.10],
            [0.20, 0.10, 0.15],
            [0.30, 0.30, 0.20],
            [0.40, 0.25, 0.25],
            [0.50, 0.40, 0.30],
            [0.60, 0.35, 0.35],
            [0.70, 0.50, 0.40],
            [0.80, 0.45, 0.45],
            [0.90, 0.55, 0.50],
            [1.00, 0.60, 0.55],
        ],
        dtype=float,
    )
    return run_windowed_mass_adaptation_diagnostic(
        HMCTuningPolicy.windowed_mass_adaptation(
            num_adaptation_steps=12,
            target_accept_prob=0.72,
            source="tests/test_hmc_trajectory_tuning.py",
        ),
        config=config,
        initial_mass_artifact=_mass_artifact(),
        warmup_draws=draws,
        initial_step_size=0.8,
        acceptance_trace=np.full(12, 0.72),
        expected_adapter_signature="phase5_trajectory_adapter_v1",
    )


def _trajectory_policy() -> HMCTuningPolicy:
    return HMCTuningPolicy.fixed_trajectory_tuning(
        target_accept_prob=0.70,
        source="tests/test_hmc_trajectory_tuning.py",
    )


def test_production_leapfrog_count_uses_theory_cap_and_floor():
    count, theory = production_leapfrog_count(
        step_size=0.2,
        max_leapfrog=20,
        min_leapfrog=10,
    )
    assert theory == 16
    assert count == 16

    capped, capped_theory = production_leapfrog_count(
        step_size=0.01,
        max_leapfrog=20,
        min_leapfrog=10,
    )
    assert capped_theory > 20
    assert capped == 20

    floored, floored_theory = production_leapfrog_count(
        step_size=10.0,
        max_leapfrog=20,
        min_leapfrog=10,
    )
    assert floored_theory == 1
    assert floored == 10


def test_fixed_trajectory_tuning_consumes_phase4_frozen_mass_and_step():
    windowed = _windowed_result()
    result = run_fixed_trajectory_tuning_diagnostic(
        _trajectory_policy(),
        config=FixedTrajectoryTuningConfig(
            num_leapfrog_step_candidates=(1, 2, 3),
            num_results=16,
            num_burnin_steps=0,
            seed=(20260612, 7),
        ),
        windowed_mass_result=windowed,
    )
    payload = result.payload()

    assert result.passed is True
    assert result.frozen_mass_artifact_signature == windowed.final_mass_artifact_signature
    assert result.frozen_step_size == pytest.approx(windowed.final_step_size)
    assert result.selected_candidate is not None
    assert result.selected_candidate.acceptance_rate == pytest.approx(0.75)
    passing = [
        candidate for candidate in result.candidate_results
        if candidate.outcome == "passed_screen"
    ]
    assert result.selected_trajectory_length == min(
        candidate.trajectory_length for candidate in passing
        if abs(candidate.acceptance_rate - 0.75) < 1.0e-12
    )
    assert result.selected_trajectory_length == pytest.approx(
        result.frozen_step_size * result.selected_num_leapfrog_steps
    )
    assert payload["diagnostics"]["acceptance_band_role"] == (
        "closed tuning promotion screen only"
    )
    assert payload["diagnostics"]["reports_posterior_convergence"] is False
    assert payload["diagnostics"]["reports_gpu_xla_readiness"] is False
    assert payload["diagnostics"]["reports_macrofinance_model_success"] is False
    assert payload["production_leapfrog_rule"]["target_dimension"] == 3
    assert "no posterior convergence claim" in payload["diagnostics"]["nonclaims"]
    assert "no GPU/XLA readiness claim" in payload["diagnostics"]["nonclaims"]
    assert "no MacroFinance model success claim" in payload["diagnostics"][
        "nonclaims"
    ]
    json.dumps(payload)


def test_fixed_trajectory_tuning_rejects_no_closed_band_candidate():
    windowed = _windowed_result()
    result = run_fixed_trajectory_tuning_diagnostic(
        _trajectory_policy(),
        config=FixedTrajectoryTuningConfig(
            num_leapfrog_step_candidates=(1, 2),
            acceptance_band=(0.2, 0.3),
            num_results=16,
            num_burnin_steps=0,
            seed=(20260613, 5),
        ),
        windowed_mass_result=windowed,
    )

    assert result.passed is False
    assert result.selected_candidate is None
    assert result.blocker_reason == "no_candidate_in_closed_acceptance_promotion_band"
    assert all(candidate.outcome == "rejected_accept_high" for candidate in result.candidate_results)


def test_fixed_trajectory_tuning_requires_reviewed_policy_and_phase4_fields():
    with pytest.raises(ValueError, match="reviewed HMCTuningPolicy"):
        run_fixed_trajectory_tuning_diagnostic(
            "fixed_trajectory_tuning",
            config=FixedTrajectoryTuningConfig(num_leapfrog_step_candidates=(1, 2)),
            windowed_mass_result=_windowed_result(),
        )
    with pytest.raises(ValueError, match="not implemented"):
        run_fixed_trajectory_tuning_diagnostic(
            HMCTuningPolicy.windowed_mass_adaptation_future(),
            config=FixedTrajectoryTuningConfig(num_leapfrog_step_candidates=(1, 2)),
            windowed_mass_result=_windowed_result(),
        )
    with pytest.raises(ValueError, match="WindowedMassAdaptationResult"):
        run_fixed_trajectory_tuning_diagnostic(
            _trajectory_policy(),
            config=FixedTrajectoryTuningConfig(num_leapfrog_step_candidates=(1, 2)),
        )
    with pytest.raises(ValueError, match="WindowedMassAdaptationResult"):
        run_fixed_trajectory_tuning_diagnostic(
            _trajectory_policy(),
            config=FixedTrajectoryTuningConfig(num_leapfrog_step_candidates=(1, 2)),
            windowed_mass_result=object(),
        )


def test_identity_mass_v2_fixture_remains_comparator_not_phase5_selector():
    toy = run_tiny_gaussian_fixed_trajectory_hmc_tuning_v2(
        step_size_candidates=(0.8,),
        num_leapfrog_step_candidates=(1, 2),
        num_results=16,
        num_burnin_steps=0,
        seed=(20260612, 7),
    )
    generic = run_fixed_trajectory_tuning_diagnostic(
        _trajectory_policy(),
        config=FixedTrajectoryTuningConfig(
            num_leapfrog_step_candidates=(1, 2),
            num_results=16,
            num_burnin_steps=0,
            seed=(20260612, 7),
        ),
        windowed_mass_result=_windowed_result(),
    )

    assert toy.mass_policy == "identity"
    assert generic.frozen_mass_artifact_signature
    assert "frozen_mass_artifact_signature" in generic.payload()
