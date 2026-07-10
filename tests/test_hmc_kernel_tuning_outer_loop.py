from __future__ import annotations

import inspect
import json
import os
from collections.abc import Mapping
from dataclasses import replace
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest

import bayesfilter
import bayesfilter.inference.hmc_budget_ladder as hmc_budget_ladder
import bayesfilter.inference.hmc_kernel_tuning as hmc_kernel_tuning
from bayesfilter.inference import (
    FixedMassHMCTuningBudgetCallbackResult,
    HMCTuneVerifyRepairAttempt,
    HMCTuneVerifyRepairLoopConfig,
    HMCTuneVerifyRepairLoopResult,
    SequentialRHatCheckpointWriterConfig,
    TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    build_retained_frozen_kernel_hmc_adapter_from_tuning_payload,
    run_hmc_tune_verify_repair_loop,
    stable_adapter_signature,
)
from bayesfilter.inference.hmc_kernel_tuning import (
    _HMCAttemptBudgetPolicy,
    _HMCPhaseAttemptState,
    _default_attempt_budget_policy,
    _fixed_mass_step_initial_step,
    _phase6_trajectory_repair_handoff_payload,
    _phase7_extended_attempt_stall_blocker,
    _phase7_progress_budget_payload,
    _phase7_verification_repair_handoff_payload,
    _public_budget_policy_factory,
)

from tests.test_hmc_kernel_tuning_fixed_mass_step import (
    _ToyGaussianAdapter,
    _bootstrap,
    _fake_result,
    _geometry,
    _scripted_step_runner,
    _windowed_stage,
)


def _loop_config(**overrides: Any) -> HMCTuneVerifyRepairLoopConfig:
    payload = {
        "target_accept_prob": 0.70,
        "acceptance_band": (0.65, 0.75),
        "repair_band": (0.55, 0.85),
        "max_attempts": 5,
        "seed": (20260621, 70),
        "chain_execution_mode": "eager",
        "target_scope": "kernel_fixed_mass_step_toy_gaussian",
    }
    payload.update(overrides)
    return HMCTuneVerifyRepairLoopConfig(**payload)


def _tiny_budget_factory(_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
    budget = 8 * (2 ** int(attempt_index))
    screen = max(4, budget // 2)
    verification = max(4, budget // 2)
    return _HMCAttemptBudgetPolicy(
        target_dimension=2,
        attempt_index=int(attempt_index),
        budget=budget,
        phase4_warmup_steps=12,
        phase5_tune_budgets=(2 * (2 ** int(attempt_index)), 4 * (2 ** int(attempt_index)), budget),
        phase5_screen_num_results=screen,
        phase5_screen_burnin_steps=1,
        phase6_screen_num_results=screen,
        phase6_screen_burnin_steps=1,
        verification_num_results=verification,
        verification_num_burnin_steps=1,
        serious_policy=False,
    )


def _passed_phase7_stage_fixtures():
    windowed = _windowed_stage()
    fixed = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=_scripted_full_chain_runner(verification_acceptances=[0.70])[0],
    )

    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        run_full_chain=trajectory_run,
    )
    assert windowed.passed is True
    assert fixed.passed is True
    assert trajectory.passed is True
    return windowed, fixed, trajectory


def _scripted_full_chain_runner(
    *,
    verification_acceptances: list[float],
    phase5_screen_acceptances: list[float] | None = None,
    trajectory_acceptance: float = 0.70,
):
    calls: list[Mapping[str, Any]] = []
    phase = "windowed"
    phase6_seed_first: int | None = None

    def run(adapter: Any, initial_state: Any, config: Any):
        nonlocal phase, phase6_seed_first
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        call = {
            "adapter_signature": adapter.adapter_signature(),
            "initial_state": np.asarray(initial_state, dtype=float),
            "num_results": int(config.num_results),
            "num_burnin_steps": int(config.num_burnin_steps),
            "step_size": float(config.step_size),
            "num_leapfrog_steps": int(config.num_leapfrog_steps),
            "seed": tuple(config.seed),
            "trace_policy": config.trace_policy,
            "adaptation_policy": config.adaptation_policy,
            "uses_dual_averaging": uses_tuning,
            "target_scope": config.target_scope,
            "use_xla": bool(config.use_xla),
        }
        calls.append(call)
        if uses_tuning:
            phase = "phase5_screen"
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=0.70,
                step_size=0.20 + 0.01 * len(
                    [item for item in calls if item["uses_dual_averaging"]]
                ),
                num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
                samples=np.zeros((int(config.num_results), 2)),
            )
        if int(config.num_results) == 12:
            phase = "phase5_tune"
            phase6_seed_first = None
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=0.70,
                samples=np.zeros((int(config.num_results), 2)),
            )
        if phase == "phase5_tune" and int(config.num_burnin_steps) == 1:
            phase = "phase6"
            acceptance = (
                0.70
                if not phase5_screen_acceptances
                else phase5_screen_acceptances.pop(0)
            )
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=acceptance,
                samples=np.zeros((int(config.num_results), 2)),
            )
        if phase == "phase5_screen":
            phase = "phase6"
            acceptance = (
                0.70
                if not phase5_screen_acceptances
                else phase5_screen_acceptances.pop(0)
            )
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=acceptance,
                samples=np.zeros((int(config.num_results), 2)),
            )
        if phase == "phase6" and (
            phase6_seed_first is None or int(config.seed[0]) == phase6_seed_first
        ):
            phase6_seed_first = int(config.seed[0])
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=trajectory_acceptance,
                samples=np.zeros((int(config.num_results), 2)),
            )
        phase = "windowed"
        phase6_seed_first = None
        acceptance = verification_acceptances.pop(0)
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=acceptance,
            samples=np.zeros((int(config.num_results), 2)),
        )

    return run, calls


def _replay_tuning_payload() -> Mapping[str, Any]:
    geometry = _geometry()
    bootstrap = _bootstrap()
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])
    loop = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        bootstrap=bootstrap,
        config=_loop_config(max_attempts=1),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )
    assert loop.passed is True
    public_final = hmc_kernel_tuning._public_final_kernel_handoff_payload(loop)
    return {
        "schema": "bayesfilter.hmc_kernel_tuning_result.v1",
        "config": _loop_config(max_attempts=1).payload(),
        "adapter_signature": stable_adapter_signature(_ToyGaussianAdapter()),
        "target_dimension": 2,
        "geometry_artifact_hash": geometry.artifact_hash,
        "bootstrap_artifact_hash": bootstrap.artifact_hash,
        "loop_artifact_hash": loop.artifact_hash,
        "geometry": geometry.payload(include_mass_arrays=False),
        "bootstrap": bootstrap.payload(),
        "tune_verify_repair_loop": loop.payload(include_final_mass_arrays=True),
        "final_status": "passed",
        "diagnostic_role": "fresh_fixed_kernel_verified",
        "hard_vetoes": (),
        "repair_triggers": (),
        "final_kernel_payload": public_final,
        "final_kernel_hash": hmc_kernel_tuning.stable_config_hash(public_final),
        "artifact_path": None,
        "diagnostic_roles": {},
        "passed": True,
    }


def test_tune_verify_repair_config_does_not_expose_hmc_mechanics_or_budgets() -> None:
    parameters = set(inspect.signature(HMCTuneVerifyRepairLoopConfig).parameters)
    forbidden = {
        "step_size",
        "num_leapfrog_steps",
        "candidate_l_values",
        "mass_window_schedule",
        "warmup_steps",
        "budget_schedule",
        "tune_num_results",
        "screen_num_results",
        "screen_num_burnin_steps",
        "verification_num_results",
        "verification_num_burnin_steps",
        "trajectory_grid",
    }

    assert parameters.isdisjoint(forbidden)
    payload = HMCTuneVerifyRepairLoopConfig(
        step_repair_factor=2.5,
        step_repair_high_acceptance_directional_factor=3.0,
        verification_chunk_max_results=250,
        verification_min_retained_results_for_pass=1000,
    ).payload()
    assert payload["step_repair_factor"] == pytest.approx(2.5)
    assert payload["step_repair_high_acceptance_directional_factor"] == pytest.approx(3.0)
    assert payload["trajectory_window_lower_multiplier"] == pytest.approx(0.3)
    assert payload["trajectory_window_upper_multiplier"] == pytest.approx(3.0)
    assert payload["verification_chunk_max_results"] == 250
    assert payload["verification_min_retained_results_for_pass"] == 1000
    assert HMCTuneVerifyRepairLoopConfig(max_attempts=10).max_attempts == 10
    with pytest.raises(ValueError, match="hard-capped"):
        HMCTuneVerifyRepairLoopConfig(max_attempts=11)
    with pytest.raises(ValueError, match="verification_chunk_max_results"):
        HMCTuneVerifyRepairLoopConfig(verification_chunk_max_results=0)
    with pytest.raises(ValueError, match="verification_min_retained_results_for_pass"):
        HMCTuneVerifyRepairLoopConfig(verification_min_retained_results_for_pass=0)


def test_default_budget_policy_matches_reviewed_phase7_mapping() -> None:
    policy0 = _default_attempt_budget_policy(17, 0)
    policy1 = _default_attempt_budget_policy(17, 1)

    assert policy0.budget == 1000
    assert policy0.phase4_warmup_steps == 1000
    assert policy0.phase5_tune_budgets == (250, 500, 1000)
    assert policy0.phase5_screen_num_results == 250
    assert policy0.phase5_screen_burnin_steps == 63
    assert policy0.phase6_screen_num_results == 250
    assert policy0.phase6_screen_burnin_steps == 63
    assert policy0.verification_num_results == 500
    assert policy0.verification_num_burnin_steps == 125
    assert policy1.budget == 2000
    assert policy1.verification_num_results == 1000
    assert policy1.phase5_tune_budgets == (500, 1000, 2000)


def test_default_budget_policy_caps_ccma_scale_serious_attempts() -> None:
    policy0 = _default_attempt_budget_policy(314, 0)
    policy1 = _default_attempt_budget_policy(314, 1)
    policy2 = _default_attempt_budget_policy(314, 2)

    assert policy0.budget == 5000
    assert policy0.phase5_tune_budgets == (1250, 2500, 5000)
    assert policy0.phase5_screen_num_results == 1250
    assert policy0.phase5_screen_burnin_steps == 313
    assert policy0.phase6_screen_num_results == 1250
    assert policy0.phase6_screen_burnin_steps == 313
    assert policy0.verification_num_results == 2500
    assert policy0.verification_num_burnin_steps == 625
    assert policy1.budget == 10000
    assert policy1.phase5_tune_budgets == (2500, 5000, 10000)
    assert policy1.phase6_screen_num_results == 2500
    assert policy1.phase6_screen_burnin_steps == 625
    assert policy1.verification_num_results == 5000
    assert policy2.budget == 10000


def test_geometry_scaled_budget_policy_increases_with_condition_number() -> None:
    policy = hmc_kernel_tuning.HMCGeometryScaledBudgetTimingPolicy(
        dimension_factor=2.0,
        min_initial_budget=10,
        max_initial_budget=10_000,
        max_tune_budget=20_000,
    )
    low_mass = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0, 0.0, 0.0, 0.0],
        covariance=np.eye(4),
        adapter_signature="test_geometry_budget_condition_adapter",
        position_role="test",
        covariance_source="test_identity",
        jitter=0.0,
        regularization_report={"method": "none"},
    )
    high_mass = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0, 0.0, 0.0, 0.0],
        covariance=np.diag([1.0, 10.0, 100.0, 1000.0]),
        adapter_signature="test_geometry_budget_condition_adapter",
        position_role="test",
        covariance_source="test_ill_conditioned",
        jitter=0.0,
        regularization_report={"method": "none"},
    )

    low_payload = policy.attempt_budget_payload(
        target_dimension=4,
        attempt_index=0,
        mass_artifact=low_mass,
    )
    high_payload = policy.attempt_budget_payload(
        target_dimension=4,
        attempt_index=0,
        mass_artifact=high_mass,
    )

    assert high_payload["budget"] > low_payload["budget"]
    assert (
        high_payload["geometry_budget_summary"]["condition_number"]
        > low_payload["geometry_budget_summary"]["condition_number"]
    )
    assert high_payload["geometry_budget_summary"]["raw_eigenvalues_exposed"] is False
    assert high_payload["geometry_budget_summary"]["mass_arrays_exposed"] is False


def test_geometry_scaled_budget_policy_increases_with_low_effective_dimension() -> None:
    policy = hmc_kernel_tuning.HMCGeometryScaledBudgetTimingPolicy(
        dimension_factor=2.0,
        min_initial_budget=10,
        max_initial_budget=10_000,
        max_tune_budget=20_000,
        condition_log10_weight=0.0,
    )
    isotropic = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0] * 8,
        covariance=np.eye(8),
        adapter_signature="test_geometry_budget_effective_dimension_adapter",
        position_role="test",
        covariance_source="test_isotropic",
        jitter=0.0,
        regularization_report={"method": "none"},
    )
    anisotropic = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0] * 8,
        covariance=np.diag([1000.0] + [1.0] * 7),
        adapter_signature="test_geometry_budget_effective_dimension_adapter",
        position_role="test",
        covariance_source="test_low_effective_dimension",
        jitter=0.0,
        regularization_report={"method": "none"},
    )

    base = policy.attempt_budget_payload(
        target_dimension=8,
        attempt_index=0,
        mass_artifact=isotropic,
    )
    stressed = policy.attempt_budget_payload(
        target_dimension=8,
        attempt_index=0,
        mass_artifact=anisotropic,
    )

    assert stressed["budget"] > base["budget"]
    assert (
        stressed["geometry_budget_summary"]["effective_dimension"]
        < base["geometry_budget_summary"]["effective_dimension"]
    )


def test_geometry_scaled_budget_policy_increases_with_regularization_pressure() -> None:
    policy = hmc_kernel_tuning.HMCGeometryScaledBudgetTimingPolicy(
        dimension_factor=2.0,
        min_initial_budget=10,
        max_initial_budget=10_000,
        max_tune_budget=20_000,
        condition_log10_weight=0.0,
        anisotropy_sqrt_weight=0.0,
    )
    base_mass = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0] * 4,
        covariance=np.eye(4),
        adapter_signature="test_geometry_budget_regularization_adapter",
        position_role="test",
        covariance_source="test_base",
        jitter=0.0,
        regularization_report={"method": "none"},
    )
    repaired_mass = hmc_kernel_tuning.PrecomputedMassArtifact.from_covariance(
        position=[0.0] * 4,
        covariance=np.eye(4),
        adapter_signature="test_geometry_budget_regularization_adapter",
        position_role="test",
        covariance_source="test_regularized",
        jitter=0.0,
        regularization_report={
            "clipped_eigenvalue_count": 2,
            "raw_nonpositive_eigenvalue_count": 1,
            "diagonal_fallback_used": True,
        },
    )

    base = policy.attempt_budget_payload(
        target_dimension=4,
        attempt_index=0,
        mass_artifact=base_mass,
    )
    repaired = policy.attempt_budget_payload(
        target_dimension=4,
        attempt_index=0,
        mass_artifact=repaired_mass,
    )

    assert repaired["budget"] > base["budget"]
    assert repaired["geometry_budget_summary"]["regularization_pressure"][
        "diagonal_fallback_used"
    ] is True


def test_geometry_scaled_policy_payload_is_public_safe() -> None:
    policy = hmc_kernel_tuning.HMCGeometryScaledBudgetTimingPolicy()
    payload = policy.payload()
    text = json.dumps(payload, sort_keys=True)

    assert payload["emergency_timing_policy"]["role"] == (
        "machine_protection_only_not_scientific_stop_rule"
    )
    assert payload["raw_eigenvalues_exposed"] is False
    assert payload["mass_arrays_exposed"] is False
    for forbidden in (
        '"step_size"',
        '"num_leapfrog_steps"',
        '"covariance"',
        '"factor"',
        '"samples"',
    ):
        assert forbidden not in text


def test_public_diagnostic_budget_policy_is_bounded_and_non_serious() -> None:
    config = hmc_kernel_tuning.HMCKernelTuningConfig.diagnostic(use_xla=True)
    factory = _public_budget_policy_factory(config)

    assert factory is not None
    assert config.preset == "diagnostic"
    assert config.max_attempts == 2
    assert config.uses_serious_budget_policy is False

    policy0 = factory(4, 0)
    policy1 = factory(4, 1)
    payload0 = policy0.payload()
    progress_payload = _phase7_progress_budget_payload(policy0)

    assert policy0.budget == 32
    assert policy1.budget == 64
    assert policy0.phase5_tune_budgets == (8, 16, 32)
    assert policy0.phase5_screen_num_results == 8
    assert policy0.phase5_screen_burnin_steps == 2
    assert policy0.phase6_screen_num_results == 8
    assert policy0.phase6_screen_burnin_steps == 2
    assert policy0.verification_num_results == 16
    assert policy0.verification_num_burnin_steps == 4
    assert payload0["serious_policy"] is False
    assert payload0["public_budget_class"] == "bounded_public_diagnostic"
    assert payload0["public_budget_cap"] == 64
    assert payload0["public_max_attempts"] == 2
    assert payload0["public_diagnostic_preset"] == "diagnostic"
    assert payload0["diagnostic_role"] == "public_bounded_timeout_diagnostic"
    assert payload0["nonclaims"] == TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    assert progress_payload["serious_policy"] is False
    assert progress_payload["public_budget_class"] == "bounded_public_diagnostic"
    assert progress_payload["public_budget_cap"] == 64
    assert progress_payload["public_max_attempts"] == 2
    assert progress_payload["public_diagnostic_preset"] == "diagnostic"
    assert progress_payload["diagnostic_role"] == "public_bounded_timeout_diagnostic"
    assert progress_payload["hmc_mechanics_exposed"] is False
    for forbidden in ("step_size", "num_leapfrog_steps", "mass_artifact_payload", "final_state"):
        assert forbidden not in progress_payload


def test_public_diagnostic_plus_budget_policy_is_bounded_and_non_serious() -> None:
    config = hmc_kernel_tuning.HMCKernelTuningConfig.diagnostic_plus(use_xla=True)
    factory = _public_budget_policy_factory(config)

    assert factory is not None
    assert config.preset == "diagnostic_plus"
    assert config.max_attempts == 2
    assert config.uses_serious_budget_policy is False

    policy0 = factory(4, 0)
    policy1 = factory(4, 1)
    policy2 = factory(4, 2)
    payload0 = policy0.payload()
    progress_payload = _phase7_progress_budget_payload(policy1)

    assert policy0.budget == 128
    assert policy1.budget == 256
    assert policy2.budget == 256
    assert policy0.phase5_tune_budgets == (32, 64, 128)
    assert policy1.phase5_tune_budgets == (64, 128, 256)
    assert policy0.phase5_screen_num_results == 32
    assert policy1.phase5_screen_num_results == 64
    assert policy0.phase6_screen_num_results == 32
    assert policy1.phase6_screen_num_results == 64
    assert policy0.verification_num_results == 64
    assert policy1.verification_num_results == 128
    assert payload0["serious_policy"] is False
    assert payload0["public_budget_class"] == "bounded_public_diagnostic_plus"
    assert payload0["public_budget_cap"] == 256
    assert payload0["public_max_attempts"] == 2
    assert payload0["public_diagnostic_preset"] == "diagnostic_plus"
    assert payload0["diagnostic_role"] == "public_bounded_verification_diagnostic_plus"
    assert payload0["nonclaims"] == TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    assert progress_payload["serious_policy"] is False
    assert progress_payload["public_budget_class"] == "bounded_public_diagnostic_plus"
    assert progress_payload["public_budget_cap"] == 256
    assert progress_payload["public_max_attempts"] == 2
    assert progress_payload["public_diagnostic_preset"] == "diagnostic_plus"
    assert progress_payload["diagnostic_role"] == "public_bounded_verification_diagnostic_plus"
    assert progress_payload["hmc_mechanics_exposed"] is False
    for forbidden in ("step_size", "num_leapfrog_steps", "mass_artifact_payload", "final_state"):
        assert forbidden not in progress_payload


def test_public_diagnostic_plus_passed_result_writes_public_artifact_payload() -> None:
    geometry = _geometry()
    bootstrap = _bootstrap()
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])
    loop = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        bootstrap=bootstrap,
        config=_loop_config(max_attempts=1),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )
    final_kernel_payload = hmc_kernel_tuning._public_final_kernel_handoff_payload(loop)
    result = hmc_kernel_tuning.HMCKernelTuningResult(
        config=hmc_kernel_tuning.HMCKernelTuningConfig.diagnostic_plus(),
        adapter_signature=stable_adapter_signature(_ToyGaussianAdapter()),
        target_dimension=2,
        geometry=geometry,
        bootstrap=bootstrap,
        tune_verify_repair_loop=loop,
        final_status="passed",
        diagnostic_role=loop.diagnostic_role,
        hard_vetoes=(),
        repair_triggers=(),
        final_kernel_payload=final_kernel_payload,
        final_kernel_hash=hmc_kernel_tuning.stable_config_hash(final_kernel_payload),
        artifact_path="hmc_kernel_tuning_result.json",
        diagnostic_roles={},
    )

    payload = result.payload()
    artifact = hmc_kernel_tuning._public_tuning_artifact_payload(result)

    assert payload["config"]["preset"] == "diagnostic_plus"
    assert payload["config"]["preset_role"] == "bounded_public_verification_diagnostic_only"
    assert artifact["config"]["preset"] == "diagnostic_plus"
    assert artifact["config"]["preset_role"] == "bounded_public_verification_diagnostic_only"
    assert artifact["status"] == "passed"
    assert artifact["final_kernel_hash"] == result.final_kernel_hash
    public_text = json.dumps(artifact["final_kernel_payload"], sort_keys=True)
    for forbidden in (
        '"step_size"',
        '"num_leapfrog_steps"',
        '"trajectory_length"',
        '"adapted_mass_artifact_payload"',
        '"position"',
        '"covariance"',
        '"factor"',
    ):
        assert forbidden not in public_text
    loop_public = result.payload()["tune_verify_repair_loop"]
    assert loop_public["final_kernel_payload"]["private_replay_payload"] is False
    loop_text = json.dumps(loop_public["final_kernel_payload"], sort_keys=True)
    assert '"step_size"' not in loop_text
    assert '"num_leapfrog_steps"' not in loop_text
    assert '"adapted_mass_artifact_payload"' not in loop_text


def test_phase7_extended_attempt_gate_requires_meaningful_progress() -> None:
    config = _loop_config(max_attempts=10)
    next_policy = _tiny_budget_factory(2, 5)
    last_attempt = HMCTuneVerifyRepairAttempt(
        attempt_index=4,
        budget_policy_payload=_tiny_budget_factory(2, 4).payload(),
        incoming_state_payload=None,
        windowed_stage=None,
        fixed_mass_step_stage=None,
        frozen_step_trajectory_stage=None,
        verification_config_payload=None,
        verification_diagnostics={
            "attempt_index": 4,
            "not_run": True,
            "reports_posterior_convergence": False,
        },
        verification_callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        final_status="repair_or_retry",
        diagnostic_role="repair_trigger",
        hard_vetoes=(),
        repair_triggers=(),
        handoff_state_payload=None,
    )
    stalled_state = _HMCPhaseAttemptState(
        mass_artifact_payload={"schema": "test.mass"},
        mass_artifact_signature="mass-hash",
        selected_step_size=0.2,
        selected_step_hash="step-hash",
        handoff_stage="phase5_selected",
    )

    blocker = _phase7_extended_attempt_stall_blocker(
        config=config,
        attempt_state=stalled_state,
        last_attempt=last_attempt,
        next_attempt_policy=next_policy,
    )

    assert blocker is not None
    assert blocker["classification"] == (
        "phase7_extended_attempt_stalled_no_meaningful_progress"
    )
    assert blocker["base_max_attempts"] == 5
    assert blocker["configured_max_attempts"] == 10
    assert blocker["next_attempt_index"] == 5
    assert blocker["stalled_reason"] == (
        "previous_attempt_left_no_effective_repair_progress"
    )
    assert blocker["hmc_mechanics_exposed"] is False

    repairing_attempt = HMCTuneVerifyRepairAttempt(
        attempt_index=4,
        budget_policy_payload=_tiny_budget_factory(2, 4).payload(),
        incoming_state_payload=None,
        windowed_stage=None,
        fixed_mass_step_stage=None,
        frozen_step_trajectory_stage=None,
        verification_config_payload=None,
        verification_diagnostics={
            "attempt_index": 4,
            "not_run": True,
            "reports_posterior_convergence": False,
        },
        verification_callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        final_status="repair_or_retry",
        diagnostic_role="repair_trigger",
        hard_vetoes=(),
        repair_triggers=("phase6_trajectory_acceptance_outside_pass_band",),
        handoff_state_payload=None,
    )
    repairing_state = _HMCPhaseAttemptState(
        mass_artifact_payload={"schema": "test.mass"},
        mass_artifact_signature="mass-hash",
        selected_step_size=0.2,
        selected_step_hash="step-hash",
        selected_num_leapfrog_steps=8,
        selected_trajectory_hash="trajectory-hash",
        verification_acceptance_rate=0.89,
        verification_acceptance_relation="above_acceptance_band",
        verification_repair_trigger="phase6_trajectory_acceptance_outside_pass_band",
        verification_repair_source="phase6_frozen_step_trajectory_acceptance",
        verification_repair_step_size=0.4,
        verification_repair_step_hash="repair-step-hash",
        verification_repair_applied=True,
        handoff_stage="phase6",
    )

    assert (
        _phase7_extended_attempt_stall_blocker(
            config=config,
            attempt_state=repairing_state,
            last_attempt=repairing_attempt,
            next_attempt_policy=next_policy,
        )
        is None
    )


def test_public_standard_and_serious_budget_policies_remain_unchanged() -> None:
    standard = hmc_kernel_tuning.HMCKernelTuningConfig.standard()
    standard_factory = _public_budget_policy_factory(standard)
    serious = hmc_kernel_tuning.HMCKernelTuningConfig.serious()
    serious_factory = _public_budget_policy_factory(serious)

    assert standard_factory is not None
    standard_policy0 = standard_factory(4, 0)
    standard_policy1 = standard_factory(4, 1)
    standard_policy2 = standard_factory(4, 2)

    assert standard.uses_serious_budget_policy is False
    assert standard_policy0.budget == 128
    assert standard_policy1.budget == 256
    assert standard_policy2.budget == 512
    assert standard_policy0.phase5_tune_budgets == (32, 64, 128)
    assert standard_policy0.phase5_screen_num_results == 32
    assert standard_policy0.phase6_screen_num_results == 32
    assert standard_policy0.verification_num_results == 64
    assert standard_policy0.serious_policy is False
    assert serious.max_attempts == 5
    assert serious.uses_serious_budget_policy is True
    assert serious_factory is not None
    serious_policy0 = serious_factory(4, 0)
    assert serious_policy0.serious_policy is True
    assert serious_policy0.payload()["geometry_budget_summary"]["dimension"] == 4
    assert "geometry_multiplier" in serious_policy0.payload()["geometry_budget_summary"]


def test_public_standard_terminal_phase6_extra_attempt_caps_phase6_screen_only() -> None:
    config = hmc_kernel_tuning.HMCKernelTuningConfig.standard(
        max_attempts=4,
        terminal_phase6_repair_extra_attempts=1,
    )
    factory = _public_budget_policy_factory(config)

    assert factory is not None
    policy3 = factory(4, 3)
    terminal_policy = factory(4, 4)

    assert policy3.budget == 1024
    assert policy3.phase6_screen_num_results == 256
    assert terminal_policy.budget == 2048
    assert terminal_policy.phase5_tune_budgets == (512, 1024, 2048)
    assert terminal_policy.phase5_screen_num_results == 512
    assert terminal_policy.phase6_screen_num_results == 128
    assert terminal_policy.phase6_screen_burnin_steps == 32
    assert terminal_policy.verification_num_results == 1024
    assert terminal_policy.public_budget_class == "standard_public_diagnostic"
    assert terminal_policy.public_diagnostic_preset == "standard"


def test_outer_loop_passes_only_after_fresh_fixed_kernel_verification() -> None:
    run, calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert isinstance(result, HMCTuneVerifyRepairLoopResult)
    assert result.passed is True
    assert result.final_status == "passed"
    assert result.final_kernel_payload is not None
    assert result.final_kernel_hash
    assert result.final_kernel_payload["fresh_fixed_kernel_verification_passed"] is True
    assert result.final_kernel_payload["reports_posterior_convergence"] is False
    assert result.attempts[0].verification_config_payload["trace_policy"] == "standard"
    assert result.attempts[0].verification_config_payload["adaptation_policy"] == "fixed_kernel_no_adaptation"
    assert result.attempts[0].verification_config_payload["use_xla"] is False
    assert result.attempts[0].verification_config_payload["num_results"] == 4
    assert result.attempts[0].verification_config_payload["num_burnin_steps"] == 1
    assert result.attempts[0].verification_diagnostics["acceptance_rate"] == pytest.approx(0.70)
    assert result.nonclaims == TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    verification_calls = [
        call
        for call in calls
        if call["num_results"] == 4
        and call["num_burnin_steps"] == 1
        and call["uses_dual_averaging"] is False
    ]
    assert verification_calls
    assert all(call["trace_policy"] == "standard" for call in verification_calls)
    assert all(call["use_xla"] is False for call in verification_calls)


def test_phase7_public_timeout_before_windowed_mass_skips_windowed_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", lambda: 100.0)
    events: list[tuple[str, Mapping[str, Any]]] = []

    def forbidden_windowed_runner(**_kwargs: Any):
        raise AssertionError("windowed mass runner must not be called after timeout")

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            public_timeout_budget_s=10.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=lambda *_args, **_kwargs: _fake_result(),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=forbidden_windowed_runner,
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
    )

    assert result.final_status == "hard_veto"
    assert result.passed is False
    assert result.hard_vetoes == ("phase7_public_timeout_before_windowed_mass",)
    assert result.repair_triggers == ("phase7_public_timeout_before_windowed_mass",)
    assert result.final_kernel_payload is None
    assert result.attempts[0].windowed_stage is None
    assert result.attempts[0].repair_triggers == (
        "phase7_public_timeout_before_windowed_mass",
    )
    assert result.attempts[0].verification_diagnostics["windowed_stage_runner_called"] is False
    closeout = result.attempts[0].verification_diagnostics["public_timeout_closeout"]
    assert closeout["schema"] == "bayesfilter.phase7_public_timeout_before_windowed_mass.v1"
    assert closeout["stage"] == "phase7_loop_attempt_before_windowed_mass"
    assert closeout["hard_veto"] == "phase7_public_timeout_before_windowed_mass"
    assert closeout["windowed_mass_runner_called"] is False
    assert closeout["closeout_required_before_windowed_mass_runner_build"] is True
    assert closeout["hmc_mechanics_exposed"] is False
    assert [stage for stage, _payload in events] == [
        "loop_attempt_start",
        "phase7_public_timeout_before_windowed_mass",
        "loop_attempt_complete",
        "loop_complete",
    ]
    timeout_event = events[1][1]
    timeout_summary = timeout_event["extra"]["resume_split_public_summary"]
    assert timeout_summary["schema"] == "bayesfilter.phase7_resume_split_public_summary.v1"
    assert timeout_summary["availability_status"] == "unavailable"
    assert timeout_summary["unavailable_reason"] == "no_private_handoff_before_resume_split"
    assert timeout_summary["private_resume_payload_available"] is False
    assert timeout_summary["private_resume_payload_exposed"] is False
    assert timeout_summary["verifier_entry_manifest"] is False
    assert timeout_summary["final_kernel_handoff"] is False
    assert timeout_event["extra"]["repair_trigger"] == (
        "phase7_public_timeout_before_windowed_mass"
    )

    complete_event = events[2][1]
    complete_summary = complete_event["extra"]["resume_split_public_summary"]
    assert complete_summary["schema"] == "bayesfilter.phase7_resume_split_public_summary.v1"
    assert complete_summary["availability_status"] == "unavailable"
    assert complete_summary["private_resume_payload_available"] is False
    assert complete_event["extra"]["repair_trigger_count"] == 1
    progress_text = json.dumps([timeout_event, complete_event], sort_keys=True)
    for forbidden in (
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
        "private/",
        "_manifest.json",
        ".tfs",
        "private_handoff_state",
    ):
        assert forbidden not in progress_text


def test_staged_timeout_stage_entry_anchor_is_fresh_for_pre_windowed_closeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base_clock = {"value": 0.0}

    def fake_perf_counter() -> float:
        return base_clock["value"]

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)
    stage_entry_times: list[float] = []
    stage_elapsed: list[float] = []

    def record_timeout(
        *,
        config: Any,
        attempt_index: int,
        target_dimension: int,
        budget_policy: Any,
    ) -> Mapping[str, Any] | None:
        del attempt_index, target_dimension, budget_policy
        stage_entry_times.append(float(config.staged_timeout_stage_started_perf_counter_s))
        base_clock["value"] = 12.5
        stage_elapsed.append(
            float(
                hmc_kernel_tuning.time.perf_counter()
                - float(config.staged_timeout_stage_started_perf_counter_s)
            )
        )
        return {
            "schema": "bayesfilter.phase7_public_timeout_before_windowed_mass.v1",
            "stage": "phase7_loop_attempt_before_windowed_mass",
            "attempt_index": 0,
            "enabled": True,
            "timeout_budget_s": 10.0,
            "reserve_s": 5.0,
            "elapsed_s": 12.5,
            "remaining_s": -2.5,
            "within_closeout_window": True,
            "deadline_clock_scope": "public_one_call_global",
            "closeout_required_before_windowed_mass_runner_build": True,
            "diagnostic_role": "phase7_pre_windowed_public_timeout_hard_veto",
            "hard_veto": "phase7_public_timeout_before_windowed_mass",
            "repair_trigger": "phase7_public_timeout_before_windowed_mass",
            "progress_only": True,
            "public_closeout_artifact_expected": True,
            "windowed_mass_runner_called": False,
            "target_dimension": 2,
            "public_budget_class": "bounded_public_diagnostic",
            "public_budget_cap": 64,
            "budget_is_public_policy": True,
            "hmc_mechanics_exposed": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": ("phase7 pre-windowed timeout closeout only",),
        }

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "_phase7_public_timeout_before_windowed_mass",
        record_timeout,
    )
    monkeypatch.setattr(
        hmc_kernel_tuning,
        "run_hmc_bootstrap_screen",
        lambda **_kwargs: _bootstrap(),
    )
    monkeypatch.setattr(
        hmc_kernel_tuning,
        "initialize_hmc_kernel_geometry",
        lambda **_kwargs: _geometry(),
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            public_timeout_budget_s=10.0,
            public_timeout_started_perf_counter_s=0.0,
            staged_timeout_policy=hmc_kernel_tuning.HMCStagedTimeoutPolicy(),
        ),
        run_full_chain=lambda *_args, **_kwargs: _fake_result(),
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "hard_veto"
    assert stage_entry_times == [0.0]
    assert stage_elapsed == [12.5]
    assert result.attempts[0].verification_diagnostics["public_timeout_closeout"]["elapsed_s"] == 12.5
    assert result.attempts[0].verification_diagnostics["public_timeout_closeout"]["stage"] == "phase7_loop_attempt_before_windowed_mass"


def test_terminal_phase6_repair_slot_does_not_bypass_pre_windowed_timeout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windowed = _windowed_stage()
    fixed_pass_run, _ = _scripted_full_chain_runner(
        phase5_screen_acceptances=[0.70],
        verification_acceptances=[0.70],
    )
    fixed_pass = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=fixed_pass_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    def trajectory_fail_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.90,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory_fail = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed_pass,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        run_full_chain=trajectory_fail_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )
    mixed_overreach_candidates = []
    for index, candidate in enumerate(trajectory_fail.candidate_results):
        payload = dict(candidate)
        diagnostics = dict(payload.get("diagnostics", {}))
        diagnostics["acceptance_rate"] = 0.60 if index % 2 == 0 else 0.90
        payload["diagnostics"] = diagnostics
        payload["trajectory_window_relation"] = "above_trajectory_window"
        payload["repair_triggers"] = tuple(
            dict.fromkeys(
                tuple(payload.get("repair_triggers", ()))
                + ("trajectory_length_above_window",)
            )
        )
        mixed_overreach_candidates.append(payload)
    trajectory_fail = replace(
        trajectory_fail,
        candidate_results=tuple(mixed_overreach_candidates),
    )
    clock = {"now": 0.0}
    windowed_calls: list[int] = []

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def windowed_runner(**kwargs: Any):
        attempt_index = int(kwargs["_attempt_index"])
        windowed_calls.append(attempt_index)
        return windowed

    def trajectory_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 0:
            clock["now"] = 100.0
        return trajectory_fail

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            terminal_phase6_repair_extra_attempts=1,
            public_timeout_budget_s=10.0,
            public_timeout_started_perf_counter_s=0.0,
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_runner,
        _fixed_mass_step_stage_runner=lambda **_kwargs: fixed_pass,
        _frozen_step_trajectory_stage_runner=trajectory_runner,
        _phase7_final_verification_runner=lambda **_kwargs: (_ for _ in ()).throw(
            AssertionError("verification must not run when Phase 6 fails")
        ),
    )

    assert result.final_status == "budget_exhausted"
    assert result.hard_vetoes == ()
    assert "verification_acceptance_budget_blocked" in result.repair_triggers
    assert (
        result.diagnostic_roles["phase6_handoff_screen"]
        == "handoff_screen_repair_trigger_non_promoting"
    )
    assert (
        result.diagnostic_roles["trajectory_window"]
        == "engineering_viability_gate_non_scientific"
    )
    assert windowed_calls == [0]
    assert len(result.attempts) == 1
    assert result.attempts[0].frozen_step_trajectory_stage is trajectory_fail

    summary = hmc_kernel_tuning._phase7_public_summary(result)
    latest_resume = summary["latest_resume_split_public_summary"]
    assert latest_resume["schema"] == "bayesfilter.phase7_resume_split_public_summary.v1"
    assert latest_resume["loop_artifact_hash"] == result.artifact_hash
    if "availability_status" in latest_resume:
        assert latest_resume["availability_status"] in {"available", "unavailable"}
    if "private_resume_payload_available" in latest_resume:
        assert latest_resume["private_resume_payload_available"] in {True, False}
    assert latest_resume["verifier_entry_manifest"] is False
    verification = summary["attempt_summaries"][0]["stage_statuses"]["verification"]
    assert verification["final_status"] == "repair_or_retry"
    assert "verification_acceptance_budget_blocked" in summary["repair_triggers"]
    text = json.dumps(summary, sort_keys=True)
    for forbidden in (
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
        "private/",
        "_manifest.json",
        ".tfs",
    ):
        assert forbidden not in text


def test_retained_frozen_kernel_adapter_replay_uses_private_loop_payload() -> None:
    payload = _replay_tuning_payload()

    result = build_retained_frozen_kernel_hmc_adapter_from_tuning_payload(
        adapter=_ToyGaussianAdapter(),
        tuning_payload=payload,
        initial_position=np.zeros(2),
        target_scope="kernel_fixed_mass_step_toy_gaussian",
    )

    assert result.contract["replay_owned_by_bayesfilter"] is True
    assert result.contract["hmc_or_tuning_invoked"] is False
    assert result.contract["final_hmc_adapter_signature"] == stable_adapter_signature(
        result.adapter
    )
    assert (
        result.contract["adapted_mass_parent_adapter_signature"]
        == result.contract["phase4_hmc_adapter_signature"]
    )
    assert result.final_kernel_payload["schema"] == "bayesfilter.hmc_frozen_kernel_handoff.v1"
    assert result.payload()["final_kernel_payload"][
        "public_handoff_schema"
    ] is None


def test_retained_frozen_kernel_adapter_replay_rejects_public_only_handoff() -> None:
    payload = dict(_replay_tuning_payload())
    payload["tune_verify_repair_loop"] = {
        "schema": "bayesfilter.hmc_tune_verify_repair_loop.v1"
    }

    with pytest.raises(ValueError, match="private final kernel payload"):
        build_retained_frozen_kernel_hmc_adapter_from_tuning_payload(
            adapter=_ToyGaussianAdapter(),
            tuning_payload=payload,
            initial_position=np.zeros(2),
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        )


def test_retained_frozen_kernel_adapter_replay_rejects_mass_parent_mismatch() -> None:
    payload = dict(_replay_tuning_payload())
    loop = dict(payload["tune_verify_repair_loop"])
    final_kernel = dict(loop["final_kernel_payload"])
    mass_payload = dict(final_kernel["adapted_mass_artifact_payload"])
    mass_payload["adapter_signature"] = "wrong-phase4-parent-signature"
    final_kernel["adapted_mass_artifact_payload"] = mass_payload
    loop["final_kernel_payload"] = final_kernel
    payload["tune_verify_repair_loop"] = loop

    with pytest.raises(ValueError, match="adapter signature"):
        build_retained_frozen_kernel_hmc_adapter_from_tuning_payload(
            adapter=_ToyGaussianAdapter(),
            tuning_payload=payload,
            initial_position=np.zeros(2),
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        )


def test_retained_frozen_kernel_adapter_replay_rejects_final_signature_mismatch() -> None:
    payload = dict(_replay_tuning_payload())
    loop = dict(payload["tune_verify_repair_loop"])
    attempts = [dict(item) for item in loop["attempts"]]
    trajectory = dict(attempts[0]["frozen_step_trajectory_stage"])
    trajectory["trajectory_hmc_adapter_signature"] = "wrong-final-adapter-signature"
    attempts[0]["frozen_step_trajectory_stage"] = trajectory
    fixed_mass = dict(attempts[0]["fixed_mass_step_stage"])
    fixed_mass["ladder_hmc_adapter_signature"] = "different-layer-signature"
    attempts[0]["fixed_mass_step_stage"] = fixed_mass
    loop["attempts"] = tuple(attempts)
    payload["tune_verify_repair_loop"] = loop

    with pytest.raises(ValueError, match="final HMC adapter signature"):
        build_retained_frozen_kernel_hmc_adapter_from_tuning_payload(
            adapter=_ToyGaussianAdapter(),
            tuning_payload=payload,
            initial_position=np.zeros(2),
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        )


def test_outer_loop_config_use_xla_propagates_to_all_full_chain_calls() -> None:
    run, calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            chain_execution_mode="tf_function",
            use_xla=True,
        ),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.passed is True
    assert result.config.payload()["use_xla"] is True
    assert result.attempts[0].verification_config_payload["use_xla"] is True
    assert calls
    assert all(call["use_xla"] is True for call in calls)


def test_outer_loop_default_tf_function_verification_uses_sequential_rhat_route(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[Mapping[str, Any]] = []

    class _FakeReusableRunner:
        def __init__(
            self,
            config: Any,
            *,
            dynamic_num_leapfrog_steps: bool = False,
        ) -> None:
            self.config = config
            self.dynamic_num_leapfrog_steps = bool(dynamic_num_leapfrog_steps)

        def run(
            self,
            *,
            current_state: Any,
            seed: Any,
            step_size: Any,
            num_leapfrog_steps: Any | None = None,
        ):
            calls.append(
                {
                    "role": "run",
                    "num_results": int(self.config.num_results),
                    "num_burnin_steps": int(self.config.num_burnin_steps),
                    "uses_dual_averaging": bool(
                        self.config.tuning_policy.uses_dual_averaging
                    ),
                    "seed": tuple(int(item) for item in seed),
                    "step_size": float(step_size),
                    "num_leapfrog_steps": int(self.config.num_leapfrog_steps)
                    if num_leapfrog_steps is None
                    else int(num_leapfrog_steps),
                    "dynamic_num_leapfrog_steps": self.dynamic_num_leapfrog_steps,
                    "initial_state": np.asarray(current_state, dtype=float),
                }
            )
            if self.config.tuning_policy.uses_dual_averaging:
                return _fake_result(
                    num_results=int(self.config.num_results),
                    acceptance=0.70,
                    step_size=0.20,
                    num_adaptation_steps=self.config.tuning_policy.num_adaptation_steps,
                )
            return _fake_result(
                num_results=int(self.config.num_results),
                acceptance=0.70,
            )

    def fake_builder(
        adapter: Any,
        initial_state_template: Any,
        config: Any,
        *,
        dynamic_num_leapfrog_steps: bool = False,
    ) -> _FakeReusableRunner:
        calls.append(
            {
                "role": "build",
                "adapter_signature": adapter.adapter_signature(),
                "num_results": int(config.num_results),
                "num_burnin_steps": int(config.num_burnin_steps),
                "uses_dual_averaging": bool(config.tuning_policy.uses_dual_averaging),
                "dynamic_num_leapfrog_steps": bool(dynamic_num_leapfrog_steps),
                "initial_state_template": np.asarray(initial_state_template, dtype=float),
            }
        )
        return _FakeReusableRunner(
            config,
            dynamic_num_leapfrog_steps=dynamic_num_leapfrog_steps,
        )

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_builder,
    )
    monkeypatch.setattr(
        hmc_budget_ladder,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_builder,
    )
    sequential_configs: list[Mapping[str, Any]] = []

    class _FakeSequentialVerifier:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(
            self,
            *,
            checkpoint_writer_config: Any = None,
            checkpoint_reference_callback: Any = None,
        ):
            if checkpoint_writer_config is not None:
                reference = {
                    "artifact_type": "bayesfilter_sequential_rhat_checkpoint_public_reference",
                    "schema_version": 1,
                    "checkpoint_kind": "verification_chunk",
                    "checkpoint_id": "srhat-v1-11111111111111111111111111111111",
                    "checkpoint_sha256": "2" * 64,
                    "contract_sha256": (
                        bayesfilter.sequential_rhat_verification_checkpoint_contract()[
                            "contract_sha256"
                        ]
                    ),
                    "private_paths_publicized": False,
                    "public_summary_contains_paths": False,
                    "public_summary_contains_raw_values": False,
                    "public_summary_contains_tensor_descriptors": False,
                    "public_summary_contains_kernel_payload": False,
                    "nonclaims": bayesfilter.SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_NONCLAIMS,
                }
                if checkpoint_reference_callback is not None:
                    checkpoint_reference_callback(reference)
                checkpoint_count = 1
                checkpoint_references = (reference,)
            else:
                checkpoint_count = 0
                checkpoint_references = ()
            return type(
                "_SequentialResult",
                (),
                {
                    "diagnostics": {
                        "sequential_rhat_verification": True,
                        "passed": True,
                        "cap_hit": False,
                        "retained_sample_count": int(self.config.max_results),
                        "check_interval": int(self.config.check_interval),
                        "max_results": int(self.config.max_results),
                        "chunk_count": 1,
                        "rhat_threshold": float(self.config.rhat_threshold),
                        "max_finite_rhat": 1.0,
                        "finite_rhat_count": 2,
                        "nonfinite_rhat_count": 0,
                        "all_finite_rhat_at_or_below_threshold": True,
                        "samples_all_finite": True,
                        "target_log_prob_finite": True,
                        "log_accept_ratio_finite": True,
                        "runtime_s": 0.01,
                        "runtime_finite": True,
                        "acceptance_rate": 0.70,
                        "divergence_status": "not_exposed_by_kernel",
                        "divergence_count": None,
                        "hard_vetoes": (),
                        "checkpointing_enabled": checkpoint_writer_config is not None,
                        "checkpoint_count": checkpoint_count,
                        "checkpoint_references": checkpoint_references,
                        "privacy_contract": {
                            "public_summary_contains_raw_values": False,
                            "public_summary_contains_chain_states": False,
                            "public_summary_contains_step_size": False,
                            "public_summary_contains_leapfrog_count": False,
                            "public_summary_contains_mass_matrix": False,
                        },
                    },
                },
            )()

    def fake_sequential_builder(
        _adapter: Any,
        _initial_state_template: Any,
        config: Any,
    ) -> _FakeSequentialVerifier:
        sequential_configs.append(
            {
                "check_interval": int(config.check_interval),
                "max_results": int(config.max_results),
                "num_burnin_steps": int(config.num_burnin_steps),
                "use_xla": bool(config.use_xla),
                "chain_execution_mode": config.chain_execution_mode,
                "target_scope": config.target_scope,
            }
        )
        return _FakeSequentialVerifier(config)

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_sequential_rhat_hmc_verifier",
        fake_sequential_builder,
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1, chain_execution_mode="tf_function"),
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.passed is True
    verification = result.attempts[0].verification_diagnostics
    route = verification["runner_route_summary"]
    assert route["active_route"] == "phase7_sequential_rhat_fixed_size_chunk_verifier"
    assert route["single_use_build_count"] == 0
    assert route["fallback_status"] == "none"
    assert "R-hat is a tuning-verification stop rule" in route["route_nonclaims"][1]
    assert verification["sequential_rhat_verification"] is True
    assert verification["all_finite_rhat_at_or_below_threshold"] is True
    assert result.attempts[0].verification_config_payload["verification_policy"] == (
        "sequential_rhat"
    )
    assert result.attempts[0].verification_config_payload["check_interval"] == 4
    assert result.attempts[0].verification_config_payload["max_results"] == 4
    assert (
        result.attempts[0].verification_config_payload["max_results"]
        == result.attempts[0].budget_policy_payload["verification_num_results"]
    )
    assert verification["sequential_rhat_policy"]["max_results"] == 4
    assert verification["sequential_rhat_policy"]["check_interval"] == 4
    assert (
        verification["sequential_rhat_policy"]["cap_rule"]
        == "stop_at_budget_policy_verification_num_results_without_promotion"
    )
    assert sequential_configs == [
        {
            "check_interval": 4,
            "max_results": 4,
            "num_burnin_steps": 1,
            "use_xla": False,
            "chain_execution_mode": "tf_function",
            "target_scope": "kernel_fixed_mass_step_toy_gaussian",
        }
    ]
    forbidden_keys: list[str] = []

    def collect_forbidden_keys(value: Any) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                key_text = str(key)
                if key_text not in {
                    "public_summary_contains_step_size",
                    "public_summary_contains_leapfrog_count",
                    "public_summary_contains_mass_matrix",
                } and any(
                    token in key_text
                    for token in ("step_size", "num_leapfrog", "mass_matrix")
                ):
                    forbidden_keys.append(key_text)
                collect_forbidden_keys(item)
        elif isinstance(value, (tuple, list)):
            for item in value:
                collect_forbidden_keys(item)

    collect_forbidden_keys(verification)
    collect_forbidden_keys(result.attempts[0].verification_config_payload)
    assert forbidden_keys == []
    assert any(
        call["role"] == "build"
        and call["uses_dual_averaging"] is False
        for call in calls
    )


def test_sequential_verification_uses_configured_compile_chunk_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windowed, fixed, trajectory = _passed_phase7_stage_fixtures()
    sequential_configs: list[Mapping[str, Any]] = []

    class _FakeSequentialVerifier:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(self, **_kwargs: Any):
            return type(
                "_SequentialResult",
                (),
                {
                    "diagnostics": {
                        "sequential_rhat_verification": True,
                        "passed": True,
                        "cap_hit": False,
                        "retained_sample_count": int(self.config.max_results),
                        "check_interval": int(self.config.check_interval),
                        "max_results": int(self.config.max_results),
                        "chunk_count": 4,
                        "rhat_threshold": float(self.config.rhat_threshold),
                        "max_finite_rhat": 1.0,
                        "finite_rhat_count": 2,
                        "nonfinite_rhat_count": 0,
                        "all_finite_rhat_at_or_below_threshold": True,
                        "samples_all_finite": True,
                        "target_log_prob_finite": True,
                        "log_accept_ratio_finite": True,
                        "runtime_s": 0.01,
                        "runtime_finite": True,
                        "acceptance_rate": 0.70,
                        "divergence_status": "not_exposed_by_kernel",
                        "divergence_count": None,
                        "hard_vetoes": (),
                    },
                },
            )()

    def fake_sequential_builder(
        _adapter: Any,
        _initial_state_template: Any,
        config: Any,
    ) -> _FakeSequentialVerifier:
        sequential_configs.append(
            {
                "check_interval": int(config.check_interval),
                "max_results": int(config.max_results),
                "min_retained_results_for_pass": int(
                    config.min_retained_results_for_pass
                ),
            }
        )
        return _FakeSequentialVerifier(config)

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_sequential_rhat_hmc_verifier",
        fake_sequential_builder,
    )

    def budget_factory(_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
        base = _tiny_budget_factory(_dimension, attempt_index)
        return replace(
            base,
            verification_num_results=1000,
            verification_num_burnin_steps=250,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            chain_execution_mode="tf_function",
            verification_chunk_max_results=250,
            verification_min_retained_results_for_pass=1000,
        ),
        _budget_policy_factory=budget_factory,
        _windowed_stage_runner=lambda **_kwargs: windowed,
        _fixed_mass_step_stage_runner=lambda **_kwargs: fixed,
        _frozen_step_trajectory_stage_runner=lambda **_kwargs: trajectory,
    )

    assert result.passed is True
    verification = result.attempts[0].verification_diagnostics
    assert verification["sequential_rhat_policy"]["check_interval"] == 250
    assert verification["sequential_rhat_policy"]["max_results"] == 1000
    assert (
        verification["sequential_rhat_policy"]["minimum_retained_results_for_pass"]
        == 1000
    )
    assert verification["verification_min_retained_pass_gate_satisfied"] is True
    assert sequential_configs == [
        {
            "check_interval": 250,
            "max_results": 1000,
            "min_retained_results_for_pass": 1000,
        }
    ]


def test_sequential_verification_blocks_pass_before_minimum_retained_count(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windowed, fixed, trajectory = _passed_phase7_stage_fixtures()

    class _EarlyPassSequentialVerifier:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(self, **_kwargs: Any):
            return type(
                "_SequentialResult",
                (),
                {
                    "diagnostics": {
                        "sequential_rhat_verification": True,
                        "passed": True,
                        "cap_hit": False,
                        "retained_sample_count": 250,
                        "check_interval": int(self.config.check_interval),
                        "max_results": int(self.config.max_results),
                        "chunk_count": 1,
                        "rhat_threshold": float(self.config.rhat_threshold),
                        "max_finite_rhat": 1.0,
                        "finite_rhat_count": 2,
                        "nonfinite_rhat_count": 0,
                        "all_finite_rhat_at_or_below_threshold": True,
                        "samples_all_finite": True,
                        "target_log_prob_finite": True,
                        "log_accept_ratio_finite": True,
                        "runtime_s": 0.01,
                        "runtime_finite": True,
                        "acceptance_rate": 0.70,
                        "divergence_status": "not_exposed_by_kernel",
                        "divergence_count": None,
                        "hard_vetoes": (),
                    },
                },
            )()

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_sequential_rhat_hmc_verifier",
        lambda _adapter, _initial_state_template, config: _EarlyPassSequentialVerifier(
            config
        ),
    )

    def budget_factory(_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
        base = _tiny_budget_factory(_dimension, attempt_index)
        return replace(
            base,
            verification_num_results=1000,
            verification_num_burnin_steps=250,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            chain_execution_mode="tf_function",
            verification_chunk_max_results=250,
            verification_min_retained_results_for_pass=1000,
        ),
        _budget_policy_factory=budget_factory,
        _windowed_stage_runner=lambda **_kwargs: windowed,
        _fixed_mass_step_stage_runner=lambda **_kwargs: fixed,
        _frozen_step_trajectory_stage_runner=lambda **_kwargs: trajectory,
    )

    assert result.passed is False
    attempt = result.attempts[0]
    assert attempt.final_status == "repair_or_retry"
    assert attempt.diagnostic_role == "verification_rhat_repair_trigger"
    assert "verification_rhat_above_threshold_or_cap_hit" in attempt.repair_triggers
    assert (
        attempt.verification_diagnostics[
            "rhat_passed_before_minimum_retained_count"
        ]
        is True
    )
    assert (
        attempt.verification_diagnostics[
            "verification_min_retained_pass_gate_satisfied"
        ]
        is False
    )


def test_phase7_checkpoint_writer_emits_pre_verification_handoff_before_verification_start(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    writer_config = SequentialRHatCheckpointWriterConfig(
        checkpoint_dir=tmp_path,
        checkpoint_label="phase3",
    )
    events: list[tuple[str, Mapping[str, Any]]] = []
    references: list[Mapping[str, Any]] = []
    contract_sha = bayesfilter.sequential_rhat_verification_checkpoint_contract()[
        "contract_sha256"
    ]

    def make_reference(kind: str, digit: str) -> Mapping[str, Any]:
        reference = {
            "artifact_type": "bayesfilter_sequential_rhat_checkpoint_public_reference",
            "schema_version": 1,
            "checkpoint_kind": kind,
            "checkpoint_id": f"srhat-v1-{digit * 32}",
            "checkpoint_sha256": digit * 64,
            "contract_sha256": contract_sha,
            "private_paths_publicized": False,
            "public_summary_contains_paths": False,
            "public_summary_contains_raw_values": False,
            "public_summary_contains_tensor_descriptors": False,
            "public_summary_contains_kernel_payload": False,
            "nonclaims": bayesfilter.SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_NONCLAIMS,
        }
        bayesfilter.assert_sequential_rhat_checkpoint_public_reference_safe(reference)
        return reference

    def fake_handoff_writer(**kwargs: Any) -> Mapping[str, Any]:
        assert kwargs["writer_config"] is writer_config
        assert kwargs["selected_kernel_private_payload"]["step_size"] > 0.0
        assert kwargs["selected_kernel_private_payload"]["num_leapfrog_steps"] > 0
        assert kwargs["selected_kernel_private_payload"]["private_handoff_only"] is True
        assert kwargs["mass_payload"]["dimension"] == 2
        reference = make_reference("pre_verification_handoff", "1")
        references.append(reference)
        return reference

    class _FakeSequentialVerifier:
        def run(
            self,
            *,
            checkpoint_writer_config: Any = None,
            checkpoint_reference_callback: Any = None,
        ):
            assert checkpoint_writer_config is writer_config
            reference = make_reference("verification_chunk", "2")
            references.append(reference)
            assert checkpoint_reference_callback is not None
            checkpoint_reference_callback(reference)
            return type(
                "_SequentialResult",
                (),
                {
                    "diagnostics": {
                        "sequential_rhat_verification": True,
                        "passed": True,
                        "cap_hit": False,
                        "retained_sample_count": 4,
                        "check_interval": 4,
                        "max_results": 4,
                        "chunk_count": 1,
                        "rhat_threshold": 1.01,
                        "max_finite_rhat": 1.0,
                        "finite_rhat_count": 2,
                        "nonfinite_rhat_count": 0,
                        "all_finite_rhat_at_or_below_threshold": True,
                        "samples_all_finite": True,
                        "target_log_prob_finite": True,
                        "log_accept_ratio_finite": True,
                        "runtime_s": 0.01,
                        "runtime_finite": True,
                        "acceptance_rate": 0.70,
                        "divergence_status": "not_exposed_by_kernel",
                        "divergence_count": None,
                        "hard_vetoes": (),
                        "checkpointing_enabled": True,
                        "checkpoint_count": 1,
                        "checkpoint_references": (reference,),
                    },
                },
            )()

    class _FakeReusableRunner:
        def __init__(
            self,
            config: Any,
            *,
            dynamic_num_leapfrog_steps: bool = False,
        ) -> None:
            self.config = config
            self.dynamic_num_leapfrog_steps = bool(dynamic_num_leapfrog_steps)

        def run(
            self,
            *,
            current_state: Any,
            seed: Any,
            step_size: Any,
            num_leapfrog_steps: Any | None = None,
        ):
            del current_state, seed, step_size
            if (
                num_leapfrog_steps is not None
                and not self.dynamic_num_leapfrog_steps
            ):
                raise AssertionError(
                    "static reusable runner must not receive dynamic L"
                )
            if self.config.tuning_policy.uses_dual_averaging:
                return _fake_result(
                    num_results=int(self.config.num_results),
                    acceptance=0.70,
                    step_size=0.20,
                    num_adaptation_steps=self.config.tuning_policy.num_adaptation_steps,
                )
            return _fake_result(
                num_results=int(self.config.num_results),
                acceptance=0.70,
            )

    def fake_reusable_builder(
        _adapter: Any,
        _initial_state_template: Any,
        config: Any,
        *,
        dynamic_num_leapfrog_steps: bool = False,
    ) -> _FakeReusableRunner:
        return _FakeReusableRunner(
            config,
            dynamic_num_leapfrog_steps=dynamic_num_leapfrog_steps,
        )

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_reusable_builder,
    )
    monkeypatch.setattr(
        hmc_budget_ladder,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_reusable_builder,
    )
    monkeypatch.setattr(
        hmc_kernel_tuning,
        "write_sequential_rhat_pre_verification_handoff_checkpoint",
        fake_handoff_writer,
    )
    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_sequential_rhat_hmc_verifier",
        lambda *_args, **_kwargs: _FakeSequentialVerifier(),
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1, chain_execution_mode="tf_function"),
        verification_checkpoint_writer_config=writer_config,
        _budget_policy_factory=_tiny_budget_factory,
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
    )

    stage_names = [stage for stage, _payload in events]
    assert result.passed is True
    assert references[0]["checkpoint_kind"] == "pre_verification_handoff"
    assert references[1]["checkpoint_kind"] == "verification_chunk"
    assert stage_names.index("trajectory_complete") < stage_names.index(
        "verification_checkpoint_written"
    )
    assert stage_names.index("verification_checkpoint_written") < stage_names.index(
        "verification_start"
    )
    assert stage_names.index("verification_start") < stage_names.index(
        "verification_complete"
    )
    checkpoint_events = [
        payload["extra"]
        for stage, payload in events
        if stage == "verification_checkpoint_written"
    ]
    assert len(checkpoint_events) == 2
    for extra in checkpoint_events:
        reference = extra["checkpoint_reference"]
        bayesfilter.assert_sequential_rhat_checkpoint_public_reference_safe(reference)
        public_text = json.dumps(extra, sort_keys=True)
        for forbidden in (
            str(tmp_path),
            "/",
            "\\",
            "step_size",
            "num_leapfrog_steps",
            "mass_payload",
            "selected_kernel",
            "final_state",
            "samples",
            ".tftensor",
        ):
            assert forbidden not in public_text
        assert extra["private_paths_publicized"] is False
        assert extra["hmc_mechanics_exposed"] is False
    verification = result.attempts[0].verification_diagnostics
    assert verification["phase7_checkpointing_enabled"] is True
    assert verification["phase7_checkpoint_count"] == 2
    assert [item["checkpoint_kind"] for item in verification["phase7_checkpoint_references"]] == [
        "pre_verification_handoff",
        "verification_chunk",
    ]
    summary = hmc_kernel_tuning._phase7_verification_public_summary(
        result.attempts[0]
    )
    assert summary["checkpointing_enabled"] is True
    assert summary["checkpoint_count"] == 2
    assert summary["checkpoint_references_public_safe"] is True
    summary_text = json.dumps(summary, sort_keys=True)
    assert "log_accept" not in summary_text
    assert "target_log_prob" not in summary_text
    assert summary["private_acceptance_log_health_passed"] is True
    assert summary["private_target_value_health_passed"] is True


def test_phase7_checkpoint_writer_emits_boundary_before_windowed_execute_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    writer_config = SequentialRHatCheckpointWriterConfig(
        checkpoint_dir=tmp_path,
        checkpoint_label="boundary",
    )
    events: list[tuple[str, Mapping[str, Any]]] = []
    writer_calls: list[Mapping[str, Any]] = []
    contract_sha = bayesfilter.sequential_rhat_verification_checkpoint_contract()[
        "contract_sha256"
    ]
    boundary_reference = {
        "artifact_type": "bayesfilter_sequential_rhat_checkpoint_public_reference",
        "schema_version": 1,
        "checkpoint_kind": "phase7_boundary_handoff",
        "checkpoint_id": "srhat-v1-" + "3" * 32,
        "checkpoint_sha256": "4" * 64,
        "contract_sha256": contract_sha,
        "private_paths_publicized": False,
        "public_summary_contains_paths": False,
        "public_summary_contains_raw_values": False,
        "public_summary_contains_tensor_descriptors": False,
        "public_summary_contains_kernel_payload": False,
        "nonclaims": bayesfilter.SEQUENTIAL_RHAT_CHECKPOINT_PUBLIC_NONCLAIMS,
    }
    bayesfilter.assert_sequential_rhat_checkpoint_public_reference_safe(
        boundary_reference
    )

    def fake_boundary_writer(**kwargs: Any) -> Mapping[str, Any]:
        assert kwargs["writer_config"] is writer_config
        assert kwargs["boundary_private_payload"]["stage"] == (
            "windowed_mass_runner_execute_start"
        )
        assert kwargs["boundary_private_payload"]["private_raw_state_allowed"] is False
        assert kwargs["state_summary_private_payload"]["raw_state_included"] is False
        writer_calls.append(kwargs)
        return boundary_reference

    class _FailingReusableRunner:
        def run(self, **_kwargs: Any) -> Any:
            raise RuntimeError("windowed execute blocked after boundary checkpoint")

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_reusable_full_chain_tfp_hmc_runner",
        lambda *_args, **_kwargs: _FailingReusableRunner(),
    )
    monkeypatch.setattr(
        hmc_kernel_tuning,
        "write_sequential_rhat_boundary_handoff_checkpoint",
        fake_boundary_writer,
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1, chain_execution_mode="tf_function"),
        verification_checkpoint_writer_config=writer_config,
        _budget_policy_factory=_tiny_budget_factory,
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
    )

    stage_names = [stage for stage, _payload in events]
    assert result.passed is False
    assert writer_calls
    assert "windowed_mass_runner_execute_start" in stage_names
    assert "windowed_mass_runner_execute_complete" not in stage_names
    execute_payload = dict(
        events[stage_names.index("windowed_mass_runner_execute_start")][1]["extra"]
    )
    assert execute_payload["checkpoint_reference"] == boundary_reference
    assert execute_payload["checkpoint_reference_public_safe"] is True
    public_text = json.dumps(execute_payload, sort_keys=True)
    for forbidden in (
        str(tmp_path),
        "/",
        "\\",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "mass_matrix",
        "inverse_mass",
        "selected_kernel",
        "final_state",
    ):
        assert forbidden not in public_text


def test_sequential_rhat_final_verification_requires_acceptance_in_band() -> None:
    diagnostics = {
        "sequential_rhat_verification": True,
        "all_finite_rhat_at_or_below_threshold": True,
        "acceptance_rate": 0.82,
        "runtime_finite": True,
        "log_accept_ratio_finite": True,
        "samples_all_finite": True,
        "target_log_prob_finite": True,
    }
    status, role, hard_vetoes, repair_triggers = (
        hmc_kernel_tuning._classify_phase7_final_verification(
            _loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
            diagnostics=diagnostics,
            screen_error=None,
            callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        )
    )

    assert status == "repair_or_retry"
    assert role == "verification_acceptance_repair_trigger"
    assert hard_vetoes == ()
    assert repair_triggers == ("verification_acceptance_outside_pass_band",)


@pytest.mark.parametrize("acceptance", [0.82, 0.60])
def test_sequential_rhat_failure_preserves_out_of_band_acceptance_repair_trigger(
    acceptance: float,
) -> None:
    diagnostics = {
        "sequential_rhat_verification": True,
        "all_finite_rhat_at_or_below_threshold": False,
        "cap_hit": True,
        "acceptance_rate": acceptance,
        "runtime_finite": True,
        "acceptance_log_health_passed": True,
        "samples_all_finite": True,
        "target_value_health_passed": True,
    }
    status, role, hard_vetoes, repair_triggers = (
        hmc_kernel_tuning._classify_phase7_final_verification(
            _loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
            diagnostics=diagnostics,
            screen_error=None,
            callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        )
    )

    assert status == "repair_or_retry"
    assert role == "verification_rhat_repair_trigger"
    assert hard_vetoes == ()
    assert "verification_rhat_above_threshold_or_cap_hit" in repair_triggers
    assert "verification_rhat_cap_hit" in repair_triggers
    assert "verification_acceptance_outside_pass_band" in repair_triggers


def test_sequential_rhat_final_verification_passes_when_acceptance_in_band() -> None:
    diagnostics = {
        "sequential_rhat_verification": True,
        "all_finite_rhat_at_or_below_threshold": True,
        "acceptance_rate": 0.70,
        "runtime_finite": True,
        "acceptance_log_health_passed": True,
        "samples_all_finite": True,
        "target_value_health_passed": True,
    }
    status, role, hard_vetoes, repair_triggers = (
        hmc_kernel_tuning._classify_phase7_final_verification(
            _loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
            diagnostics=diagnostics,
            screen_error=None,
            callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        )
    )

    assert status == "passed"
    assert role == "sequential_rhat_fixed_kernel_verification_passed"
    assert hard_vetoes == ()
    assert repair_triggers == ()


def test_verification_high_acceptance_handoff_supplies_private_repair_step() -> None:
    repair = _phase7_verification_repair_handoff_payload(
        config=_loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
        selected_step_size=0.125,
        selected_step_hash="selected-step-hash",
        verification_config_payload={"verification_policy": "sequential_rhat"},
        verification_diagnostics={
            "acceptance_rate": 0.82,
            "sequential_rhat_verification": True,
        },
        verification_final_status="repair_or_retry",
        verification_diagnostic_role="verification_acceptance_repair_trigger",
        verification_repair_triggers=("verification_acceptance_outside_pass_band",),
    )
    state = _HMCPhaseAttemptState(
        mass_artifact_payload={"dimension": 2},
        mass_artifact_signature="mass-signature",
        selected_step_size=0.125,
        selected_step_hash="selected-step-hash",
        selected_num_leapfrog_steps=9,
        selected_trajectory_hash="trajectory-hash",
        handoff_stage="phase6",
        **repair,
    )

    assert state.verification_acceptance_rate == pytest.approx(0.82)
    assert state.verification_acceptance_relation == "above_acceptance_band"
    assert state.verification_repair_trigger == "verification_acceptance_outside_pass_band"
    assert state.verification_repair_source == "phase7_final_verification_acceptance"
    assert state.verification_repair_step_size == pytest.approx(0.25)
    assert state.verification_repair_step_hash is not None
    assert state.verification_repair_applied is True
    assert state.payload()["verification_repair_applied"] is True
    assert _fixed_mass_step_initial_step(_windowed_stage(), attempt_state=state) == pytest.approx(0.25)


def test_verification_mixed_rhat_acceptance_handoff_supplies_private_repair_step() -> None:
    repair = _phase7_verification_repair_handoff_payload(
        config=_loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
        selected_step_size=0.125,
        selected_step_hash="selected-step-hash",
        verification_config_payload={"verification_policy": "sequential_rhat"},
        verification_diagnostics={
            "acceptance_rate": 0.82,
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": False,
            "cap_hit": True,
        },
        verification_final_status="repair_or_retry",
        verification_diagnostic_role="verification_rhat_repair_trigger",
        verification_repair_triggers=(
            "verification_rhat_above_threshold_or_cap_hit",
            "verification_rhat_cap_hit",
            "verification_acceptance_outside_pass_band",
        ),
    )

    assert repair["verification_acceptance_relation"] == "above_acceptance_band"
    assert repair["verification_repair_trigger"] == "verification_acceptance_outside_pass_band"
    assert repair["verification_repair_source"] == "phase7_final_verification_acceptance"
    assert repair["verification_repair_step_size"] == pytest.approx(0.25)
    assert repair["verification_repair_step_hash"] is not None
    assert repair["verification_repair_applied"] is True


def test_verification_in_band_handoff_does_not_create_repair_step() -> None:
    repair = _phase7_verification_repair_handoff_payload(
        config=_loop_config(acceptance_band=(0.65, 0.75), repair_band=(0.55, 0.85)),
        selected_step_size=0.125,
        selected_step_hash="selected-step-hash",
        verification_config_payload={"verification_policy": "sequential_rhat"},
        verification_diagnostics={"acceptance_rate": 0.70},
        verification_final_status="passed",
        verification_diagnostic_role="sequential_rhat_fixed_kernel_verification_passed",
        verification_repair_triggers=(),
    )

    assert repair["verification_acceptance_relation"] == "inside_acceptance_band"
    assert repair["verification_repair_step_size"] is None
    assert repair["verification_repair_step_hash"] is None
    assert repair["verification_repair_applied"] is False


def test_outer_loop_progress_callback_marks_internal_substages() -> None:
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])
    events: list[tuple[str, Mapping[str, Any]]] = []

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
    )

    stage_names = [stage for stage, _payload in events]
    assert result.passed is True
    expected_prefix = [
        "loop_attempt_start",
        "windowed_mass_start",
        "windowed_mass_runner_build_start",
        "windowed_mass_runner_build_complete",
        "windowed_mass_runner_execute_start",
        "windowed_mass_runner_execute_complete",
        "windowed_mass_capture_start",
        "windowed_mass_capture_complete",
        "windowed_mass_semantic_diagnostic_start",
        "windowed_mass_semantic_diagnostic_complete",
        "windowed_mass_complete",
        "fixed_mass_step_start",
    ]
    assert stage_names[: len(expected_prefix)] == expected_prefix
    assert stage_names.count("fixed_mass_ladder_tune_call_start") > 1
    assert stage_names.count("fixed_mass_ladder_screen_call_start") > 1
    assert "fixed_mass_step_complete" in stage_names
    assert stage_names.count("trajectory_candidate_call_start") == 1
    assert stage_names.count("trajectory_candidate_call_complete") == 1
    assert stage_names[-4:] == [
        "verification_start",
        "verification_complete",
        "loop_attempt_complete",
        "loop_complete",
    ]
    first_budget = events[0][1]["bounded_public_budget_payload"]
    assert first_budget["target_dimension"] == 2
    assert first_budget["budget"] == 8
    assert first_budget["substage_budget_details_exposed"] is False
    assert first_budget["hmc_mechanics_exposed"] is False
    forbidden_progress_keys = {
        "step_size",
        "num_leapfrog_steps",
        "acceptance_rate",
        "runtime_metadata",
        "raw_diagnostics",
        "trace",
        "samples",
        "mass_artifact_payload",
        "diagnostic_config",
    }
    inner_events = [
        payload
        for stage, payload in events
        if stage.startswith("windowed_mass_") and stage not in {"windowed_mass_start", "windowed_mass_complete"}
    ]
    assert inner_events
    for payload in inner_events:
        assert payload["hmc_mechanics_exposed"] is False
        assert payload["reports_posterior_convergence"] is False
        extra = payload["extra"]
        assert set(extra).isdisjoint(forbidden_progress_keys)
        assert extra["route_category"] == "injected_runner"
        assert extra["hmc_mechanics_exposed"] is False
        assert extra["progress_only"] is True
        if payload["started"] is True:
            assert extra["elapsed_s"] == pytest.approx(0.0)
            assert extra["started_perf_counter_s"] >= 0.0
            assert extra["timing_anchor_role"] == "process_local_monotonic_debug_only"
    boundary_events = [
        (stage, payload)
        for stage, payload in events
        if stage.startswith("fixed_mass_ladder_")
        or stage.startswith("trajectory_candidate_")
    ]
    assert boundary_events
    for stage, payload in boundary_events:
        assert payload["hmc_mechanics_exposed"] is False
        assert payload["reports_posterior_convergence"] is False
        assert payload["bounded_public_budget_payload"][
            "substage_budget_details_exposed"
        ] is True
        extra = payload["extra"]
        assert set(extra).isdisjoint(forbidden_progress_keys)
        assert extra["hmc_mechanics_exposed"] is False
        assert extra["progress_only"] is True
        assert extra["substage_budget_details_exposed"] is True
        assert "call_config_hash" in extra
        assert "num_results" in extra
        assert "num_burnin_steps" in extra
        if stage.startswith("fixed_mass_ladder_"):
            assert extra["round_index"] == 0
            assert extra["budget"] in {2}
            assert extra["role"] in {"tune", "screen"}
        if stage.startswith("trajectory_candidate_"):
            assert 0 <= extra["candidate_index"] < extra["candidate_count"]
            assert extra["candidate_count"] == 1
        if payload["started"] is True:
            assert extra["elapsed_s"] == pytest.approx(0.0)
            assert extra["started_perf_counter_s"] >= 0.0
            assert extra["timing_anchor_role"] == "process_local_monotonic_debug_only"
        else:
            assert "started_perf_counter_s" not in extra
            assert "timing_anchor_role" not in extra
    assert events[-1][1]["extra"]["final_status"] == "passed"
    assert all(payload["reports_posterior_convergence"] is False for _stage, payload in events)


def test_outer_loop_progress_helper_allowlists_timing_anchors_without_private_mechanics() -> None:
    budget_extra = hmc_kernel_tuning._budget_ladder_progress_extra(
        {
            "stage": "fixed_mass_ladder_tune_call_start",
            "round_index": 0,
            "budget": 8,
            "role": "tune",
            "started": True,
            "completed": False,
            "route_category": "reusable_runner",
            "call_config_hash": "public-call-hash",
            "num_results": 4,
            "num_burnin_steps": 2,
            "substage_budget_details_exposed": True,
            "uses_dual_averaging": True,
            "runner_reused": False,
            "static_contract_hash": "public-static-contract-hash",
            "elapsed_s": 0.0,
            "started_perf_counter_s": 123.0,
            "timing_anchor_role": "process_local_monotonic_debug_only",
            "progress_only": True,
            "hmc_mechanics_exposed": False,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": ("progress only",),
            "step_size": 0.1,
            "num_leapfrog_steps": 5,
            "mass_artifact_payload": {"private": True},
            "samples": [[0.0]],
            "trace": {"target_log_prob": [0.0]},
            "final_state": [0.0],
        }
    )
    assert budget_extra["started_perf_counter_s"] == pytest.approx(123.0)
    assert budget_extra["timing_anchor_role"] == "process_local_monotonic_debug_only"
    assert budget_extra["elapsed_s"] == pytest.approx(0.0)

    trajectory_config = hmc_budget_ladder.FullChainHMCConfig(
        num_results=4,
        num_burnin_steps=2,
        step_size=0.1,
        num_leapfrog_steps=5,
        seed=(20260630, 1),
        chain_execution_mode="tf_function",
        use_xla=True,
        target_scope="kernel_fixed_mass_step_toy_gaussian",
    )
    trajectory_extra = hmc_kernel_tuning._trajectory_candidate_progress_extra(
        stage="trajectory_candidate_call_start",
        candidate_index=0,
        candidate_count=3,
        config=trajectory_config,
        runner_event=None,
        elapsed_s=0.0,
        started_perf_counter_s=456.0,
    )
    assert trajectory_extra["started_perf_counter_s"] == pytest.approx(456.0)
    assert trajectory_extra["timing_anchor_role"] == "process_local_monotonic_debug_only"
    assert trajectory_extra["elapsed_s"] == pytest.approx(0.0)

    forbidden = {
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    }
    assert set(budget_extra).isdisjoint(forbidden)
    assert set(trajectory_extra).isdisjoint(forbidden)


def test_outer_loop_repairs_with_private_handoff_and_doubled_budget() -> None:
    run, calls = _scripted_full_chain_runner(verification_acceptances=[0.82, 0.70])
    private_events: list[tuple[str, Mapping[str, Any]]] = []

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=3),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _private_diagnostic_callback=lambda event_type, payload: private_events.append(
            (event_type, dict(payload))
        ),
    )

    assert result.final_status == "passed"
    assert len(result.attempts) == 2
    assert result.attempts[0].final_status == "repair_or_retry"
    assert "verification_acceptance_outside_pass_band" in result.attempts[0].repair_triggers
    assert result.attempts[0].handoff_state_payload["handoff_stage"] == "phase6"
    assert result.attempts[0].handoff_state_payload["required_private_handoff_complete"] is True
    assert result.attempts[0].handoff_state_payload["final_kernel_handoff_complete"] is True
    assert (
        result.attempts[0].handoff_state_payload["verification_acceptance_relation"]
        == "above_acceptance_band"
    )
    assert result.attempts[0].handoff_state_payload["verification_repair_applied"] is True
    repair_step = result.attempts[0].handoff_state_payload["verification_repair_step_size"]
    assert repair_step is not None
    assert result.attempts[1].incoming_state_payload["required_private_handoff_complete"] is True
    assert result.attempts[1].fixed_mass_step_stage.initial_step_size == pytest.approx(
        repair_step
    )
    dual_averaging_calls = [call for call in calls if call["uses_dual_averaging"]]
    assert any(call["step_size"] == pytest.approx(repair_step) for call in dual_averaging_calls)
    assert result.attempts[0].budget_policy_payload["budget"] == 8
    assert result.attempts[1].budget_policy_payload["budget"] == 16
    assert result.attempts[1].verification_config_payload["num_results"] == 8
    assert result.final_kernel_payload["attempt_index"] == 1
    handoff_events = [
        payload
        for event_type, payload in private_events
        if event_type == "phase7_handoff_kernel_change"
    ]
    assert handoff_events
    assert handoff_events[0]["verification_repair_applied"] is True
    assert handoff_events[0]["verification_repair_step_size"] == pytest.approx(
        repair_step
    )
    assert handoff_events[0]["num_leapfrog_steps"] > 0
    assert handoff_events[0]["private_hmc_mechanics"] is True


def test_phase7_resume_split_contract_public_summary_is_sanitized() -> None:
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.82, 0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    contract = hmc_kernel_tuning._phase7_private_resume_split_contract(
        loop=result,
        attempt_index=0,
    )
    summary = hmc_kernel_tuning._phase7_resume_split_public_summary(contract)

    assert contract["schema"] == "bayesfilter.phase7_private_resume_split_contract.v1"
    assert contract["private_resume_payload_only"] is True
    assert contract["private_handoff_state"]["handoff_stage"] == "phase6"
    assert contract["private_handoff_state_hash"]
    assert contract["contract_hash"]
    assert contract["verifier_entry_manifest"] is False
    assert contract["final_kernel_handoff"] is False
    assert summary["schema"] == "bayesfilter.phase7_resume_split_public_summary.v1"
    assert summary["contract_hash"] == contract["contract_hash"]
    assert summary["private_resume_payload_hash"] == contract["private_handoff_state_hash"]
    assert summary["handoff_stage"] == "phase6"
    assert (
        summary["resume_entry_stage"]
        == "phase7_final_verification_or_verification_only_retry"
    )
    assert summary["private_resume_payload_exposed"] is False
    assert summary["verifier_entry_manifest"] is False
    assert summary["final_kernel_handoff"] is False
    assert summary["actual_target_runtime_executed"] is False
    assert summary["reports_posterior_convergence"] is False
    assert summary["reports_sampler_superiority"] is False
    assert summary["reports_default_readiness"] is False
    assert summary["reports_gpu_or_xla_readiness"] is False
    text = json.dumps(summary, sort_keys=True)
    for forbidden in (
        "private/",
        "private_checkpoints",
        "_manifest.json",
        ".tfs",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
        "private_handoff_state",
        "private_handoff_payload",
    ):
        assert forbidden not in text


def test_phase7_resume_split_contract_rejects_missing_private_handoff() -> None:
    geometry = _geometry()
    bootstrap = _bootstrap()
    attempt = hmc_kernel_tuning.HMCTuneVerifyRepairAttempt(
        attempt_index=0,
        budget_policy_payload=_tiny_budget_factory(2, 0).payload(),
        incoming_state_payload=None,
        windowed_stage=None,
        fixed_mass_step_stage=None,
        frozen_step_trajectory_stage=None,
        verification_config_payload=None,
        verification_diagnostics={"not_run": True},
        verification_callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        final_status="architecture_blocked",
        diagnostic_role="architecture_blocked",
        hard_vetoes=(),
        repair_triggers=("phase7_required_private_handoff_missing",),
        handoff_state_payload=None,
    )
    result = HMCTuneVerifyRepairLoopResult(
        config=_loop_config(max_attempts=1),
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash=bootstrap.artifact_hash,
        adapter_signature=geometry.adapter_signature,
        target_dimension=geometry.target_dimension,
        attempts=(attempt,),
        final_status="architecture_blocked",
        diagnostic_role="architecture_blocked",
        hard_vetoes=(),
        repair_triggers=("phase7_required_private_handoff_missing",),
        final_kernel_payload=None,
        final_kernel_hash=None,
        seed_report={"phase7_root_seed": (20260621, 70)},
        diagnostic_roles={"architecture_blocked": "test"},
    )

    assert result.final_status == "architecture_blocked"
    with pytest.raises(ValueError, match="private handoff state"):
        hmc_kernel_tuning._phase7_private_resume_split_contract(loop=result)


def test_outer_loop_classifies_verification_acceptance_retry_when_public_budget_insufficient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0, "verification_count": 0}
    base_run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.82, 0.83, 0.70]
    )

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def run(adapter: Any, initial_state: Any, config: Any):
        result = base_run(adapter, initial_state, config)
        acceptance = float(np.asarray(result.diagnostics["acceptance_rate"]))
        if acceptance in {0.82, 0.83}:
            clock["verification_count"] += 1
            clock["now"] = 100.0 if clock["verification_count"] == 1 else 760.0
        return result

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=3,
            public_timeout_budget_s=810.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_acceptance_budget_blocked"
    assert "verification_acceptance_budget_blocked" in result.repair_triggers
    assert len(result.attempts) == 2
    assert result.attempts[-1].attempt_index == 1
    assert result.attempts[-1].handoff_state_payload[
        "verification_acceptance_relation"
    ] == "above_acceptance_band"
    assert result.attempts[-1].handoff_state_payload[
        "verification_repair_applied"
    ] is True
    assert all(
        "phase6_public_timeout_soft_deadline" not in attempt.hard_vetoes
        for attempt in result.attempts
    )
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    assert public_summary["diagnostic_role"] == "verification_acceptance_budget_blocked"
    assert public_summary["attempt_count"] == 2
    guard = public_summary["terminal_budget_guard"]
    assert guard["classification"] == "verification_acceptance_budget_blocked"
    assert guard["previous_verification_acceptance_relation"] == "above_acceptance_band"
    assert guard["closeout_required_before_next_attempt"] is True
    assert guard["hmc_mechanics_exposed"] is False
    assert guard["next_attempt_budget_is_public_policy"] is False
    assert guard["remaining_s"] == pytest.approx(50.0)
    text = json.dumps(public_summary, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in text


def test_terminal_phase6_repair_slot_does_not_bypass_verification_acceptance_budget_block(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0}
    retry_stage_calls = {"windowed": 0, "fixed": 0, "trajectory": 0}
    run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.70],
        trajectory_acceptance=0.90,
    )

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def trajectory_stage_runner(**kwargs: Any):
        result = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(**kwargs)
        if int(kwargs["_attempt_index"]) == 0:
            clock["now"] = 680.0
        elif int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["trajectory"] += 1
        return result

    def windowed_stage_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["windowed"] += 1
        return hmc_kernel_tuning.run_hmc_windowed_mass_stage(**kwargs)

    def fixed_step_stage_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["fixed"] += 1
        return hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(**kwargs)

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            terminal_phase6_repair_extra_attempts=1,
            public_timeout_budget_s=810.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_stage_runner,
        _fixed_mass_step_stage_runner=fixed_step_stage_runner,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_acceptance_budget_blocked"
    assert len(result.attempts) == 1
    assert retry_stage_calls == {"windowed": 0, "fixed": 0, "trajectory": 0}
    guard = hmc_kernel_tuning._phase7_public_summary(result)["terminal_budget_guard"]
    assert guard["classification"] == "verification_acceptance_budget_blocked"
    assert (
        guard["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert guard["hmc_mechanics_exposed"] is False


def test_phase7_fixed_mass_stage_config_threads_public_timeout_fields() -> None:
    config = _loop_config(
        chain_execution_mode="tf_function",
        use_xla=True,
        public_timeout_budget_s=810.0,
        public_timeout_started_perf_counter_s=12.5,
    )

    fixed_config = hmc_kernel_tuning._phase7_fixed_step_stage_config(
        config,
        attempt_index=2,
    )
    ladder_config = hmc_kernel_tuning._fixed_mass_step_stage_ladder_config(
        fixed_config,
        initial_step=0.1,
        num_leapfrog_steps=5,
        target_scope="kernel_fixed_mass_step_toy_gaussian",
        attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    assert fixed_config.public_timeout_budget_s == pytest.approx(810.0)
    assert fixed_config.public_timeout_started_perf_counter_s == pytest.approx(12.5)
    assert ladder_config.public_timeout_budget_s == pytest.approx(810.0)
    assert ladder_config.public_timeout_started_perf_counter_s == pytest.approx(12.5)
    assert ladder_config.chain_execution_mode == "tf_function"
    assert ladder_config.use_xla is True



def test_windowed_mass_public_timeout_closeout_before_runner_skips_hmc_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", lambda: 9.0)
    calls: list[str] = []
    events: list[tuple[str, Mapping[str, Any]]] = []

    def run(_adapter: Any, _initial_state: Any, _config: Any):
        calls.append("unexpected")
        raise AssertionError("windowed mass HMC runner must not run after closeout")

    result = hmc_kernel_tuning.run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=hmc_kernel_tuning.HMCWindowedMassStageConfig(
            target_accept_prob=0.70,
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            public_timeout_budget_s=10.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=run,
        _attempt_budget_policy=_tiny_budget_factory(2, 0),
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
        _attempt_index=0,
    )

    assert calls == []
    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert result.diagnostic_role == "hard_veto"
    assert result.hard_vetoes == ("windowed_mass_public_timeout_soft_deadline",)
    closeout = result.diagnostics["public_timeout_closeout"]
    assert closeout["remaining_s"] == pytest.approx(1.0)
    assert closeout["closeout_required_before_hmc_call"] is True
    assert closeout["deadline_clock_scope"] == "public_one_call_global"
    assert closeout["hmc_mechanics_exposed"] is False
    assert [stage for stage, _payload in events] == [
        "windowed_mass_public_timeout_closeout"
    ]
    event_payload = events[0][1]
    assert event_payload["public_timeout_closeout"]["hard_veto"] == (
        "windowed_mass_public_timeout_soft_deadline"
    )
    assert event_payload["hmc_mechanics_exposed"] is False
    forbidden_fields = {
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    }
    assert forbidden_fields.isdisjoint(event_payload)
    assert forbidden_fields.isdisjoint(event_payload["public_timeout_closeout"])
    public_text = json.dumps(event_payload, sort_keys=True)
    for forbidden in (
        "mass_artifact_payload",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in public_text

def test_outer_loop_blocks_verification_acceptance_retry_before_stage_overhead(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0, "verification_count": 0}
    retry_stage_calls = {"windowed": 0, "fixed": 0, "trajectory": 0}
    base_run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.82, 0.83, 0.70]
    )

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def run(adapter: Any, initial_state: Any, config: Any):
        result = base_run(adapter, initial_state, config)
        acceptance = float(np.asarray(result.diagnostics["acceptance_rate"]))
        if acceptance in {0.82, 0.83}:
            clock["verification_count"] += 1
            # At t=680 the Phase 4v guard's old reserve+first-candidate check
            # still looked affordable for an 810s public budget. Attempt 2
            # then paid retry-stage overhead and reached Phase 6 with too
            # little remaining budget for candidate 0.
            clock["now"] = 100.0 if clock["verification_count"] == 1 else 680.0
        return result

    def windowed_stage_runner(**kwargs: Any):
        result = hmc_kernel_tuning.run_hmc_windowed_mass_stage(**kwargs)
        if int(kwargs["_attempt_index"]) == 2:
            retry_stage_calls["windowed"] += 1
            clock["now"] += 35.0
        return result

    def fixed_step_stage_runner(**kwargs: Any):
        result = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(**kwargs)
        if int(kwargs["_attempt_index"]) == 2:
            retry_stage_calls["fixed"] += 1
            clock["now"] += 45.0
        return result

    def trajectory_stage_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 2:
            retry_stage_calls["trajectory"] += 1
        return hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(**kwargs)

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=3,
            public_timeout_budget_s=810.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_stage_runner,
        _fixed_mass_step_stage_runner=fixed_step_stage_runner,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_acceptance_budget_blocked"
    assert len(result.attempts) == 2
    assert retry_stage_calls == {"windowed": 0, "fixed": 0, "trajectory": 0}
    assert all(
        "phase6_public_timeout_soft_deadline" not in attempt.hard_vetoes
        for attempt in result.attempts
    )
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    guard = public_summary["terminal_budget_guard"]
    assert guard["classification"] == "verification_acceptance_budget_blocked"
    assert guard["remaining_s"] == pytest.approx(130.0)
    assert guard["reserve_s"] == pytest.approx(60.0)
    assert guard["estimated_next_candidate_s"] == pytest.approx(60.0)
    assert guard["estimated_pre_phase6_retry_overhead_s"] == pytest.approx(60.0)
    assert guard["estimated_minimum_next_attempt_s"] == pytest.approx(120.0)
    assert guard["hmc_mechanics_exposed"] is False
    text = json.dumps(guard, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in text


def test_outer_loop_blocks_phase6_repair_retry_before_stage_overhead(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = {"now": 0.0}
    retry_stage_calls = {"windowed": 0, "fixed": 0, "trajectory": 0}
    run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.70],
        trajectory_acceptance=0.90,
    )

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def trajectory_stage_runner(**kwargs: Any):
        result = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(**kwargs)
        if int(kwargs["_attempt_index"]) == 0:
            clock["now"] = 680.0
        elif int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["trajectory"] += 1
        return result

    def windowed_stage_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["windowed"] += 1
        return hmc_kernel_tuning.run_hmc_windowed_mass_stage(**kwargs)

    def fixed_step_stage_runner(**kwargs: Any):
        if int(kwargs["_attempt_index"]) == 1:
            retry_stage_calls["fixed"] += 1
        return hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(**kwargs)

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=3,
            public_timeout_budget_s=810.0,
            public_timeout_started_perf_counter_s=0.0,
        ),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_stage_runner,
        _fixed_mass_step_stage_runner=fixed_step_stage_runner,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_acceptance_budget_blocked"
    assert "verification_acceptance_budget_blocked" in result.repair_triggers
    assert len(result.attempts) == 1
    assert result.attempts[0].handoff_state_payload[
        "verification_repair_trigger"
    ] == "phase6_trajectory_acceptance_outside_pass_band"
    assert result.attempts[0].handoff_state_payload[
        "verification_acceptance_relation"
    ] == "above_acceptance_band"
    assert result.attempts[0].handoff_state_payload[
        "verification_repair_applied"
    ] is True
    assert retry_stage_calls == {"windowed": 0, "fixed": 0, "trajectory": 0}
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    guard = public_summary["terminal_budget_guard"]
    assert guard["classification"] == "verification_acceptance_budget_blocked"
    assert (
        guard["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert guard["previous_verification_acceptance_relation"] == (
        "above_acceptance_band"
    )
    assert guard["closeout_required_before_next_attempt"] is True
    assert guard["hmc_mechanics_exposed"] is False
    assert guard["remaining_s"] == pytest.approx(130.0)
    text = json.dumps(public_summary, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in text


def test_outer_loop_phase5_acceptance_repair_uses_private_step_handoff() -> None:
    run, calls = _scripted_full_chain_runner(
        phase5_screen_acceptances=[0.90, 0.91, 0.92, 0.70],
        verification_acceptances=[0.70],
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "passed"
    assert len(result.attempts) == 1
    first = result.attempts[0]
    assert first.final_status == "passed"
    assert first.fixed_mass_step_stage.selected_step_payload is not None
    assert first.fixed_mass_step_stage.passed is True
    assert first.fixed_mass_step_stage.diagnostics["algorithm"] == (
        "joint_l_epsilon_grid_fixed_mass_hmc"
    )
    assert first.fixed_mass_step_stage.repair_step_payload is None
    assert first.frozen_step_trajectory_stage is not None
    assert first.frozen_step_trajectory_stage.passed is True
    assert first.verification_config_payload is not None
    dual_averaging_calls = [call for call in calls if call["uses_dual_averaging"]]
    assert len(dual_averaging_calls) > 1


def test_phase6_high_acceptance_handoff_supplies_private_repair_step() -> None:
    run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.70],
        trajectory_acceptance=0.90,
    )
    config = _loop_config(
        acceptance_band=(0.65, 0.75),
        repair_band=(0.55, 0.85),
        trajectory_window_lower_multiplier=0.01,
        trajectory_window_upper_multiplier=100.0,
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=replace(config, max_attempts=1),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    attempt = result.attempts[0]
    repair = _phase6_trajectory_repair_handoff_payload(
        config=config,
        selected_step_size=attempt.fixed_mass_step_stage.selected_step_size,
        selected_step_hash=attempt.fixed_mass_step_stage.selected_step_hash,
        frozen_step_trajectory_stage=attempt.frozen_step_trajectory_stage,
    )
    state = _HMCPhaseAttemptState(
        mass_artifact_payload={"dimension": 2},
        mass_artifact_signature="mass-signature",
        selected_step_size=attempt.fixed_mass_step_stage.selected_step_size,
        selected_step_hash=attempt.fixed_mass_step_stage.selected_step_hash,
        handoff_stage="phase5_selected",
        **repair,
    )

    assert attempt.final_status == "repair_or_retry"
    assert {
        candidate["trajectory_window_relation"]
        for candidate in attempt.frozen_step_trajectory_stage.candidate_results
    } == {"inside_trajectory_window"}
    assert repair["verification_acceptance_relation"] == "above_acceptance_band"
    assert (
        repair["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert (
        repair["verification_repair_source"]
        == "phase6_frozen_step_trajectory_acceptance"
    )
    assert repair["verification_repair_step_size"] == pytest.approx(
        2.0 * attempt.fixed_mass_step_stage.selected_step_size
    )
    assert repair["verification_repair_step_hash"] is not None
    assert repair["verification_repair_applied"] is True
    assert _fixed_mass_step_initial_step(_windowed_stage(), attempt_state=state) == (
        pytest.approx(repair["verification_repair_step_size"])
    )


def test_phase6_low_acceptance_handoff_supplies_private_repair_step() -> None:
    run, _calls = _scripted_full_chain_runner(
        verification_acceptances=[0.70],
        trajectory_acceptance=0.50,
    )
    config = _loop_config(
        acceptance_band=(0.65, 0.75),
        repair_band=(0.55, 0.85),
        trajectory_window_lower_multiplier=0.01,
        trajectory_window_upper_multiplier=100.0,
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=replace(config, max_attempts=1),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    attempt = result.attempts[0]
    repair = _phase6_trajectory_repair_handoff_payload(
        config=config,
        selected_step_size=attempt.fixed_mass_step_stage.selected_step_size,
        selected_step_hash=attempt.fixed_mass_step_stage.selected_step_hash,
        frozen_step_trajectory_stage=attempt.frozen_step_trajectory_stage,
    )

    assert attempt.final_status == "repair_or_retry"
    assert {
        candidate["trajectory_window_relation"]
        for candidate in attempt.frozen_step_trajectory_stage.candidate_results
    } == {"inside_trajectory_window"}
    assert repair["verification_acceptance_relation"] == "below_acceptance_band"
    assert (
        repair["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert repair["verification_repair_step_size"] == pytest.approx(
        0.5 * attempt.fixed_mass_step_stage.selected_step_size
    )
    assert repair["verification_repair_applied"] is True


def test_outer_loop_phase6_repair_uses_directional_private_step_handoff() -> None:
    run, calls = _scripted_full_chain_runner(
        verification_acceptances=[0.70],
        trajectory_acceptance=0.90,
    )
    config = _loop_config(
        max_attempts=2,
        trajectory_window_lower_multiplier=0.01,
        trajectory_window_upper_multiplier=100.0,
    )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=config,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "budget_exhausted"
    assert result.final_kernel_payload is None
    assert len(result.attempts) == 2
    first = result.attempts[0]
    assert first.final_status == "repair_or_retry"
    assert first.fixed_mass_step_stage.passed is True
    assert first.frozen_step_trajectory_stage.passed is False
    assert first.frozen_step_trajectory_stage.selected_trajectory_hash is None
    assert {
        candidate["trajectory_window_relation"]
        for candidate in first.frozen_step_trajectory_stage.candidate_results
    } == {"inside_trajectory_window"}
    assert "phase6_trajectory_status:repair_or_retry" in first.repair_triggers
    assert first.handoff_state_payload["handoff_stage"] == "phase5_selected"
    assert first.handoff_state_payload["step_handoff_complete"] is True
    assert first.handoff_state_payload["stage_repair_handoff_complete"] is True
    assert first.handoff_state_payload["final_kernel_handoff_complete"] is False
    assert (
        first.handoff_state_payload["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert (
        first.handoff_state_payload["verification_repair_source"]
        == "phase6_frozen_step_trajectory_acceptance"
    )
    assert first.handoff_state_payload["verification_acceptance_relation"] == (
        "above_acceptance_band"
    )
    assert first.handoff_state_payload["verification_repair_applied"] is True
    assert first.handoff_state_payload["verification_repair_step_size"] == pytest.approx(
        2.0 * first.fixed_mass_step_stage.selected_step_size
    )
    bracket_state = first.handoff_state_payload["fixed_mass_bracket_state"]
    assert bracket_state["next_step_size"] == pytest.approx(
        first.handoff_state_payload["verification_repair_step_size"]
    )
    assert bracket_state["high_acceptance_step_lower_bound"] == pytest.approx(
        first.handoff_state_payload["verification_repair_step_size"]
    )
    assert bracket_state["private_handoff_only"] is True
    assert bracket_state["public_progress_exposes_step"] is False
    assert first.handoff_state_payload["selected_num_leapfrog_steps"] is None
    assert first.handoff_state_payload["phase6_retry_num_leapfrog_steps"] is not None
    assert first.handoff_state_payload["phase6_retry_anchor_source"] == (
        "phase6_failed_candidate_nearest_tau"
    )
    assert result.attempts[1].incoming_state_payload["handoff_stage"] == "phase5_selected"
    assert result.attempts[1].incoming_state_payload["selected_step_hash"] is not None
    assert result.attempts[1].incoming_state_payload["phase6_retry_num_leapfrog_steps"] == (
        first.handoff_state_payload["phase6_retry_num_leapfrog_steps"]
    )
    assert result.attempts[1].incoming_state_payload["phase6_retry_anchor_source"] == (
        "phase6_failed_candidate_nearest_tau"
    )
    assert result.attempts[1].incoming_state_payload[
        "verification_repair_applied"
    ] is True
    assert result.attempts[1].incoming_state_payload[
        "fixed_mass_bracket_state_available"
    ] is True
    assert result.attempts[1].fixed_mass_step_stage.initial_step_size == pytest.approx(
        first.handoff_state_payload["verification_repair_step_size"]
    )
    assert result.attempts[1].budget_policy_payload["budget"] == 16
    retry_step = first.handoff_state_payload["verification_repair_step_size"]
    retry_fixed_mass_calls = [
        call
        for call in calls
        if abs(call["step_size"] - retry_step) < 1.0e-12
        and call["num_burnin_steps"] == 1
    ]
    assert retry_fixed_mass_calls
    assert retry_fixed_mass_calls[0]["uses_dual_averaging"] is False


def test_outer_loop_budget_exhausted_emits_no_final_kernel() -> None:
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.82, 0.83])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "budget_exhausted"
    assert result.passed is False
    assert result.final_kernel_payload is None
    assert result.final_kernel_hash is None
    assert result.payload()["budget_exhausted_is_non_promoting"] is True
    assert "phase7_budget_exhausted" in result.repair_triggers


def test_outer_loop_propagates_fixed_mass_budget_incomplete_without_final_kernel(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    windowed = _windowed_stage()
    clock = {"now": 0.0}
    timed_screen_l: set[int] = set()
    fixed_run, _calls = _scripted_step_runner(
        {3: 0.82, 4: 0.82, 5: 0.82, 6: 0.82, 8: 0.70}
    )

    def fake_perf_counter() -> float:
        return float(clock["now"])

    def timed_fixed_run(adapter: Any, initial_state: Any, config: Any):
        result = fixed_run(adapter, initial_state, config)
        leapfrog = int(config.num_leapfrog_steps)
        if (
            not bool(config.tuning_policy.uses_dual_averaging)
            and leapfrog not in timed_screen_l
        ):
            timed_screen_l.add(leapfrog)
            clock["now"] += 12.0
        return result

    def windowed_runner(**_kwargs: Any):
        return windowed

    def fixed_runner(**kwargs: Any):
        return hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
            **{
                **kwargs,
                "run_full_chain": timed_fixed_run,
            }
        )

    def forbidden_trajectory_runner(**_kwargs: Any):
        raise AssertionError("trajectory stage must not run after fixed-mass budget closeout")

    def forbidden_verification_runner(**_kwargs: Any):
        raise AssertionError("verification must not run after fixed-mass budget closeout")

    monkeypatch.setattr(hmc_kernel_tuning.time, "perf_counter", fake_perf_counter)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=3,
            public_timeout_budget_s=130.0,
            public_timeout_started_perf_counter_s=0.0,
            max_leapfrog_steps=12,
        ),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_runner,
        _fixed_mass_step_stage_runner=fixed_runner,
        _frozen_step_trajectory_stage_runner=forbidden_trajectory_runner,
        _phase7_final_verification_runner=forbidden_verification_runner,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == (
        hmc_kernel_tuning._FIXED_MASS_STEP_PUBLIC_TIMEOUT_BUDGET_INCOMPLETE_ROLE
    )
    assert result.hard_vetoes == ()
    assert result.final_kernel_payload is None
    assert result.final_kernel_hash is None
    assert len(result.attempts) == 1
    attempt = result.attempts[0]
    assert attempt.final_status == "budget_exhausted"
    assert attempt.frozen_step_trajectory_stage is None
    assert attempt.verification_diagnostics["not_run"] is True
    assert attempt.hard_vetoes == ()
    assert (
        hmc_kernel_tuning._FIXED_MASS_STEP_PUBLIC_TIMEOUT_BUDGET_INCOMPLETE_REPAIR_TRIGGER
        in attempt.repair_triggers
    )
    fixed_stage = attempt.fixed_mass_step_stage
    assert fixed_stage.final_status == "budget_exhausted"
    assert fixed_stage.selected_step_payload is None
    assert fixed_stage.repair_step_payload is None
    assert fixed_stage.diagnostics["public_timeout_budget_incomplete"] is True
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    fixed_summary = public_summary["attempt_summaries"][0]["stage_statuses"][
        "fixed_mass_step"
    ]
    assert fixed_summary["final_status"] == "budget_exhausted"
    assert fixed_summary["public_timeout_closeout"]["budget_incomplete"] is True
    assert "hard_veto" not in fixed_summary["public_timeout_closeout"]


def test_outer_loop_rhat_cap_retries_verification_without_retuning_stages() -> None:
    windowed = _windowed_stage()
    fixed = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=_scripted_full_chain_runner(verification_acceptances=[0.70])[0],
    )
    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=trajectory_run,
    )
    verification_calls: list[int] = []
    stage_calls: list[str] = []

    def windowed_runner(**_kwargs: Any):
        stage_calls.append("windowed")
        return windowed

    def fixed_runner(**_kwargs: Any):
        stage_calls.append("fixed")
        return fixed

    def trajectory_runner(**_kwargs: Any):
        stage_calls.append("trajectory")
        return trajectory

    def verification_runner(
        *,
        budget_policy: Any,
        attempt_index: int,
        verification_start_callback: Any,
        **_kwargs: Any,
    ):
        verification_calls.append(int(attempt_index))
        if verification_start_callback is not None:
            verification_start_callback()
        passed = len(verification_calls) == 2
        diagnostics = {
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": passed,
            "cap_hit": not passed,
            "rhat_threshold": 1.01,
            "check_interval": int(budget_policy.verification_num_results),
            "max_results": int(budget_policy.verification_num_results),
            "runtime_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "log_accept_ratio_finite": True,
            "acceptance_rate": 0.70,
        }
        return hmc_kernel_tuning._classify_phase7_final_verification(
            _loop_config(max_attempts=2),
            diagnostics=diagnostics,
            screen_error=None,
            callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        )

    def verification_wrapper(**kwargs: Any):
        (
            status,
            role,
            hard_vetoes,
            repair_triggers,
        ) = verification_runner(**kwargs)
        budget_policy = kwargs["budget_policy"]
        diagnostics = {
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": status == "passed",
            "cap_hit": status != "passed",
            "rhat_threshold": 1.01,
            "check_interval": int(budget_policy.verification_num_results),
            "max_results": int(budget_policy.verification_num_results),
            "runtime_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "log_accept_ratio_finite": True,
            "acceptance_rate": 0.70,
        }
        return (
            {
                "verification_policy": "sequential_rhat",
                "max_results": int(budget_policy.verification_num_results),
                "acceptance_band": (0.65, 0.75),
            },
            diagnostics,
            FixedMassHMCTuningBudgetCallbackResult(),
            status,
            role,
            hard_vetoes,
            repair_triggers,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_runner,
        _fixed_mass_step_stage_runner=fixed_runner,
        _frozen_step_trajectory_stage_runner=trajectory_runner,
        _phase7_final_verification_runner=verification_wrapper,
    )

    assert result.final_status == "passed"
    assert verification_calls == [0, 1]
    assert stage_calls == ["windowed", "fixed", "trajectory"]
    assert result.attempts[1].windowed_stage is windowed
    assert result.attempts[1].fixed_mass_step_stage is fixed
    assert result.attempts[1].frozen_step_trajectory_stage is trajectory
    assert result.attempts[0].handoff_state_payload["verification_budget_results"] == 4
    assert (
        result.attempts[1].verification_diagnostics["phase7_retry_class"]
        == "verification_only_after_rhat_cap"
    )
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    second_verification = public_summary["attempt_summaries"][1]["stage_statuses"][
        "verification"
    ]
    assert second_verification["verification_only_retry"] is True
    assert second_verification["reused_frozen_kernel_handoff"] is True
    assert second_verification["hmc_mechanics_exposed"] is False


def test_outer_loop_saturated_verify_only_retry_closes_out_before_final_slot() -> None:
    windowed = _windowed_stage()
    fixed = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=_scripted_full_chain_runner(verification_acceptances=[0.70])[0],
    )

    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=trajectory_run,
    )
    verification_calls: list[int] = []
    stage_calls: list[str] = []

    def capped_budget_factory(_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
        base = _tiny_budget_factory(_dimension, attempt_index)
        return replace(
            base,
            budget=16,
            verification_num_results=8,
            verification_num_burnin_steps=2,
            public_budget_cap=16,
            public_max_attempts=3,
            public_diagnostic_preset="diagnostic_plus",
        )

    def windowed_runner(**_kwargs: Any):
        stage_calls.append("windowed")
        return windowed

    def fixed_runner(**_kwargs: Any):
        stage_calls.append("fixed")
        return fixed

    def trajectory_runner(**_kwargs: Any):
        stage_calls.append("trajectory")
        return trajectory

    def verification_wrapper(
        *,
        budget_policy: Any,
        attempt_index: int,
        verification_start_callback: Any,
        **_kwargs: Any,
    ):
        verification_calls.append(int(attempt_index))
        if verification_start_callback is not None:
            verification_start_callback()
        diagnostics = {
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": False,
            "cap_hit": True,
            "rhat_threshold": 1.01,
            "check_interval": int(budget_policy.verification_num_results),
            "max_results": int(budget_policy.verification_num_results),
            "runtime_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "log_accept_ratio_finite": True,
            "acceptance_rate": 0.70,
        }
        status, role, hard_vetoes, repair_triggers = (
            hmc_kernel_tuning._classify_phase7_final_verification(
                _loop_config(max_attempts=3),
                diagnostics=diagnostics,
                screen_error=None,
                callback_result=FixedMassHMCTuningBudgetCallbackResult(),
            )
        )
        return (
            {
                "verification_policy": "sequential_rhat",
                "max_results": int(budget_policy.verification_num_results),
                "acceptance_band": (0.65, 0.75),
            },
            diagnostics,
            FixedMassHMCTuningBudgetCallbackResult(),
            status,
            role,
            hard_vetoes,
            repair_triggers,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=3),
        _budget_policy_factory=capped_budget_factory,
        _windowed_stage_runner=windowed_runner,
        _fixed_mass_step_stage_runner=fixed_runner,
        _frozen_step_trajectory_stage_runner=trajectory_runner,
        _phase7_final_verification_runner=verification_wrapper,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_only_rhat_cap_budget_saturated_no_repair_slot"
    assert result.repair_triggers == (
        "verification_rhat_above_threshold_or_cap_hit",
        "verification_rhat_cap_hit",
        "verification_only_rhat_cap_budget_saturated_no_repair_slot",
    )
    assert verification_calls == [0, 1]
    assert stage_calls == ["windowed", "fixed", "trajectory"]
    guard = result.terminal_budget_guard_payload
    assert guard["previous_verification_budget_results"] == 8
    assert guard["next_attempt_verification_budget_results"] == 8
    assert guard["remaining_attempts_after_next"] == 0
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    assert public_summary["terminal_budget_guard"]["classification"] == (
        "verification_only_rhat_cap_budget_saturated_no_repair_slot"
    )


def test_terminal_phase6_repair_slot_does_not_bypass_verify_only_saturation() -> None:
    windowed = _windowed_stage()
    fixed = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=_scripted_full_chain_runner(verification_acceptances=[0.70])[0],
    )

    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=trajectory_run,
    )
    verification_calls: list[int] = []
    stage_calls: list[str] = []

    def capped_budget_factory(_dimension: int, attempt_index: int) -> _HMCAttemptBudgetPolicy:
        base = _tiny_budget_factory(_dimension, attempt_index)
        return replace(
            base,
            budget=16,
            verification_num_results=8,
            verification_num_burnin_steps=2,
            public_budget_cap=16,
            public_max_attempts=3,
            public_diagnostic_preset="diagnostic_plus",
        )

    def verification_wrapper(
        *,
        budget_policy: Any,
        attempt_index: int,
        verification_start_callback: Any,
        **_kwargs: Any,
    ):
        verification_calls.append(int(attempt_index))
        if verification_start_callback is not None:
            verification_start_callback()
        diagnostics = {
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": False,
            "cap_hit": True,
            "rhat_threshold": 1.01,
            "check_interval": int(budget_policy.verification_num_results),
            "max_results": int(budget_policy.verification_num_results),
            "runtime_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "log_accept_ratio_finite": True,
            "acceptance_rate": 0.70,
        }
        status, role, hard_vetoes, repair_triggers = (
            hmc_kernel_tuning._classify_phase7_final_verification(
                _loop_config(max_attempts=3),
                diagnostics=diagnostics,
                screen_error=None,
                callback_result=FixedMassHMCTuningBudgetCallbackResult(),
            )
        )
        return (
            {
                "verification_policy": "sequential_rhat",
                "max_results": int(budget_policy.verification_num_results),
                "acceptance_band": (0.65, 0.75),
            },
            diagnostics,
            FixedMassHMCTuningBudgetCallbackResult(),
            status,
            role,
            hard_vetoes,
            repair_triggers,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=3, terminal_phase6_repair_extra_attempts=1),
        _budget_policy_factory=capped_budget_factory,
        _windowed_stage_runner=lambda **_kwargs: stage_calls.append("windowed") or windowed,
        _fixed_mass_step_stage_runner=lambda **_kwargs: stage_calls.append("fixed") or fixed,
        _frozen_step_trajectory_stage_runner=lambda **_kwargs: stage_calls.append("trajectory") or trajectory,
        _phase7_final_verification_runner=verification_wrapper,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "verification_only_rhat_cap_budget_saturated_no_repair_slot"
    assert verification_calls == [0, 1]
    assert stage_calls == ["windowed", "fixed", "trajectory"]
    guard = result.terminal_budget_guard_payload
    assert guard["classification"] == (
        "verification_only_rhat_cap_budget_saturated_no_repair_slot"
    )
    assert guard["remaining_attempts_after_next"] == 0


def test_outer_loop_out_of_band_verification_acceptance_still_reenters_stage_repair() -> None:
    run, calls = _scripted_full_chain_runner(verification_acceptances=[0.82, 0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "passed"
    dual_averaging_calls = [call for call in calls if call["uses_dual_averaging"]]
    assert len(dual_averaging_calls) > 2
    assert len(result.attempts) == 2
    assert (
        result.attempts[0].handoff_state_payload["verification_repair_trigger"]
        == "verification_acceptance_outside_pass_band"
    )


def test_outer_loop_verify_only_retry_disarms_when_acceptance_leaves_band() -> None:
    windowed = _windowed_stage()
    fixed = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=_scripted_full_chain_runner(verification_acceptances=[0.70])[0],
    )

    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=trajectory_run,
    )
    verification_acceptances = [0.70, 0.82, 0.70]
    verification_calls: list[int] = []
    stage_calls: list[str] = []

    def windowed_runner(**_kwargs: Any):
        stage_calls.append("windowed")
        return windowed

    def fixed_runner(**_kwargs: Any):
        stage_calls.append("fixed")
        return fixed

    def trajectory_runner(**_kwargs: Any):
        stage_calls.append("trajectory")
        return trajectory

    def verification_wrapper(
        *,
        budget_policy: Any,
        attempt_index: int,
        verification_start_callback: Any,
        **_kwargs: Any,
    ):
        verification_calls.append(int(attempt_index))
        if verification_start_callback is not None:
            verification_start_callback()
        acceptance = verification_acceptances[len(verification_calls) - 1]
        passed = len(verification_calls) == 3
        diagnostics = {
            "sequential_rhat_verification": True,
            "all_finite_rhat_at_or_below_threshold": passed,
            "cap_hit": not passed,
            "rhat_threshold": 1.01,
            "check_interval": int(budget_policy.verification_num_results),
            "max_results": int(budget_policy.verification_num_results),
            "runtime_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "log_accept_ratio_finite": True,
            "acceptance_rate": acceptance,
        }
        status, role, hard_vetoes, repair_triggers = (
            hmc_kernel_tuning._classify_phase7_final_verification(
                _loop_config(max_attempts=3),
                diagnostics=diagnostics,
                screen_error=None,
                callback_result=FixedMassHMCTuningBudgetCallbackResult(),
            )
        )
        return (
            {
                "verification_policy": "sequential_rhat",
                "max_results": int(budget_policy.verification_num_results),
                "acceptance_band": (0.65, 0.75),
            },
            diagnostics,
            FixedMassHMCTuningBudgetCallbackResult(),
            status,
            role,
            hard_vetoes,
            repair_triggers,
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=3),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_runner,
        _fixed_mass_step_stage_runner=fixed_runner,
        _frozen_step_trajectory_stage_runner=trajectory_runner,
        _phase7_final_verification_runner=verification_wrapper,
    )

    assert result.final_status == "passed"
    assert verification_calls == [0, 1, 2]
    assert stage_calls == [
        "windowed",
        "fixed",
        "trajectory",
        "windowed",
        "fixed",
        "trajectory",
    ]
    second_attempt = result.attempts[1]
    assert (
        second_attempt.verification_diagnostics["phase7_retry_class"]
        == "verification_only_disarmed_acceptance_repair"
    )
    assert second_attempt.verification_diagnostics["phase7_verification_only_retry"] is False
    assert (
        second_attempt.handoff_state_payload["verification_repair_trigger"]
        == "verification_acceptance_outside_pass_band"
    )
    assert second_attempt.handoff_state_payload["verification_repair_applied"] is True
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    second_verification = public_summary["attempt_summaries"][1]["stage_statuses"][
        "verification"
    ]
    assert second_verification["acceptance_relation"] == "above_acceptance_band"
    assert second_verification["verification_only_retry"] is False
    assert second_verification["reused_frozen_kernel_handoff"] is True



def test_outer_loop_callback_roles_are_classified_for_verification() -> None:
    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            promotion_vetoes=("domain_screen_not_yet_passed",),
        )

    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1),
        verification_callback=callback,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "budget_exhausted"
    assert result.attempts[0].final_status == "repair_or_retry"
    assert "domain_screen_not_yet_passed" in result.attempts[0].repair_triggers
    assert result.final_kernel_payload is None


def test_outer_loop_callback_repair_trigger_is_retry_without_final_kernel() -> None:
    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            repair_triggers=("domain_repair_requested",),
        )

    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=1),
        verification_callback=callback,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "budget_exhausted"
    assert result.attempts[0].final_status == "repair_or_retry"
    assert "domain_repair_requested" in result.attempts[0].repair_triggers
    assert result.final_kernel_payload is None


def test_outer_loop_hard_veto_for_continuation_veto_callback() -> None:
    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            continuation_vetoes=("artifact_cannot_answer_question",),
        )

    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        verification_callback=callback,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "hard_veto"
    assert "verification_callback_continuation_veto" in result.hard_vetoes
    assert result.final_kernel_payload is None


def test_outer_loop_hard_veto_for_hard_veto_callback() -> None:
    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            hard_vetoes=("domain_hard_veto",),
        )

    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        verification_callback=callback,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "hard_veto"
    assert "domain_hard_veto" in result.hard_vetoes
    assert result.final_kernel_payload is None


def test_outer_loop_missing_required_private_handoff_is_architecture_blocked() -> None:
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.82])

    def fixed_stage_callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            promotion_vetoes=("private_step_handoff_not_available",),
        )

    def fixed_stage_without_repair_handoff(**kwargs: Any):
        stage = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(**kwargs)
        return replace(stage, repair_step_payload=None, repair_step_hash=None)

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=2),
        fixed_mass_screen_callback=fixed_stage_callback,
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
        _fixed_mass_step_stage_runner=fixed_stage_without_repair_handoff,
    )

    assert result.final_status == "architecture_blocked"
    assert result.attempts[0].final_status == "architecture_blocked"
    assert "phase7_required_private_handoff_missing" in result.repair_triggers
    assert result.final_kernel_payload is None
    assert result.final_kernel_hash is None


def test_outer_loop_labels_phase6_repair_handoff_when_final_attempt_has_no_slot() -> None:
    windowed = _windowed_stage()
    fixed_pass_run, _ = _scripted_full_chain_runner(
        phase5_screen_acceptances=[0.70],
        verification_acceptances=[0.70],
    )
    fixed_pass = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=fixed_pass_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    def trajectory_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.90,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory_fail = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed_pass,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        run_full_chain=trajectory_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    assert fixed_pass.passed is True
    assert trajectory_fail.passed is False
    assert {
        candidate["trajectory_window_relation"]
        for candidate in trajectory_fail.candidate_results
    } == {"inside_trajectory_window"}

    def windowed_stage_runner(**_kwargs: Any):
        return windowed

    fixed_stage_calls: list[int] = []

    def fixed_step_stage_runner(**kwargs: Any):
        attempt_index = int(kwargs["_attempt_index"])
        fixed_stage_calls.append(attempt_index)
        if attempt_index < 2:
            repair_payload = {
                "runtime": "bayesfilter.test.phase5_repair_fixture",
                "step_size": 0.1,
                "private_handoff_only": True,
            }
            return replace(
                fixed_pass,
                final_status="repair_or_retry",
                diagnostic_role="repair_trigger",
                repair_triggers=("fixed_mass_fixture_repair",),
                selected_step_payload=None,
                selected_step_hash=None,
                repair_step_payload=repair_payload,
                repair_step_hash=hmc_kernel_tuning.stable_config_hash(repair_payload),
            )
        return fixed_pass

    def trajectory_stage_runner(**_kwargs: Any):
        return trajectory_fail

    def verification_runner(**_kwargs: Any):
        raise AssertionError("verification must not run without a Phase 6 pass")

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=3,
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_stage_runner,
        _fixed_mass_step_stage_runner=fixed_step_stage_runner,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
        _phase7_final_verification_runner=verification_runner,
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == (
        "phase7_repair_handoff_budget_exhausted_no_attempt_slot"
    )
    assert len(result.attempts) == 3
    assert fixed_stage_calls == [0, 1, 2]
    assert result.attempts[0].fixed_mass_step_stage.passed is False
    assert result.attempts[0].frozen_step_trajectory_stage is None
    assert result.attempts[1].fixed_mass_step_stage.passed is False
    assert result.attempts[1].frozen_step_trajectory_stage is None
    final_attempt = result.attempts[2]
    assert final_attempt.fixed_mass_step_stage.passed is True
    assert final_attempt.frozen_step_trajectory_stage.passed is False
    assert final_attempt.handoff_state_payload["verification_repair_applied"] is True
    assert (
        final_attempt.handoff_state_payload["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    assert (
        final_attempt.handoff_state_payload["verification_repair_source"]
        == "phase6_frozen_step_trajectory_acceptance"
    )
    assert (
        "phase7_repair_handoff_budget_exhausted_no_attempt_slot"
        in result.repair_triggers
    )
    assert "phase7_budget_exhausted" not in result.repair_triggers
    guard = result.terminal_budget_guard_payload
    assert guard["classification"] == (
        "phase7_repair_handoff_budget_exhausted_no_attempt_slot"
    )
    assert guard["last_attempt_index"] == 2
    assert guard["configured_max_attempts"] == 3
    assert guard["remaining_attempt_slots"] == 0
    assert guard["last_handoff_stage"] == "phase5_selected"
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    public_guard = public_summary["terminal_budget_guard"]
    assert public_guard["classification"] == guard["classification"]
    assert public_guard["hmc_mechanics_exposed"] is False
    text = json.dumps(public_summary, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in text


def test_outer_loop_terminal_phase6_repair_slot_can_pass_once() -> None:
    windowed = _windowed_stage()
    fixed_pass_run, _ = _scripted_full_chain_runner(
        phase5_screen_acceptances=[0.70],
        verification_acceptances=[0.70],
    )
    fixed_pass = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=fixed_pass_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    def trajectory_fail_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.90,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory_fail = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed_pass,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        run_full_chain=trajectory_fail_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )
    fixed_stage_calls: list[int] = []
    trajectory_stage_calls: list[int] = []
    verification_calls: list[int] = []

    def windowed_stage_runner(**_kwargs: Any):
        return windowed

    def fixed_step_stage_runner(**kwargs: Any):
        attempt_index = int(kwargs["_attempt_index"])
        fixed_stage_calls.append(attempt_index)
        return fixed_pass

    def trajectory_stage_runner(**kwargs: Any):
        attempt_index = int(kwargs["_attempt_index"])
        trajectory_stage_calls.append(attempt_index)
        if attempt_index == 0:
            return trajectory_fail

        def trajectory_pass_run(_adapter: Any, _initial_state: Any, config: Any):
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=0.70,
                samples=np.zeros((int(config.num_results), 2)),
            )

        return hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            windowed_stage=windowed,
            fixed_mass_step_stage=fixed_pass,
            config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
                target_accept_prob=0.70,
                seed=(20260621, 61),
                chain_execution_mode="eager",
                target_scope="kernel_fixed_mass_step_toy_gaussian",
                trajectory_window_lower_multiplier=0.01,
                trajectory_window_upper_multiplier=100.0,
            ),
            run_full_chain=trajectory_pass_run,
            _attempt_budget_policy=kwargs["_attempt_budget_policy"],
            _attempt_state=kwargs.get("_attempt_state"),
        )

    def verification_runner(
        *,
        attempt_index: int,
        budget_policy: Any,
        verification_start_callback: Any,
        **_kwargs: Any,
    ):
        verification_calls.append(int(attempt_index))
        if verification_start_callback is not None:
            verification_start_callback()
        return (
            {
                "verification_policy": "fixed_kernel",
                "num_results": int(budget_policy.verification_num_results),
                "acceptance_band": (0.65, 0.75),
            },
            {
                "acceptance_rate": 0.70,
                "runtime_finite": True,
                "samples_all_finite": True,
                "target_log_prob_finite": True,
                "log_accept_ratio_finite": True,
            },
            FixedMassHMCTuningBudgetCallbackResult(),
            "passed",
            "fresh_fixed_kernel_verification_passed",
            (),
            (),
        )

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            terminal_phase6_repair_extra_attempts=1,
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=windowed_stage_runner,
        _fixed_mass_step_stage_runner=fixed_step_stage_runner,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
        _phase7_final_verification_runner=verification_runner,
    )

    assert result.final_status == "passed"
    assert len(result.attempts) == 2
    assert [attempt.attempt_index for attempt in result.attempts] == [0, 1]
    assert fixed_stage_calls == [0, 1]
    assert trajectory_stage_calls == [0, 1]
    assert verification_calls == [1]
    first, extra = result.attempts
    assert first.final_status == "repair_or_retry"
    assert first.handoff_state_payload["verification_repair_applied"] is True
    assert (
        first.handoff_state_payload["verification_repair_trigger"]
        == "phase6_trajectory_acceptance_outside_pass_band"
    )
    budget_summary = hmc_kernel_tuning._phase7_attempt_budget_public_summary(
        extra.budget_policy_payload
    )
    assert budget_summary["terminal_phase6_repair_extra_attempt"] is True
    assert budget_summary["terminal_phase6_repair_extra_attempt_index"] == 1
    assert budget_summary["terminal_phase6_repair_extra_attempts"] == 1
    public_summary = hmc_kernel_tuning._phase7_public_summary(result)
    assert public_summary["attempt_count"] == 2
    public_text = json.dumps(public_summary, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "step_size",
        "num_leapfrog_steps",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
    ):
        assert forbidden not in public_text


def test_outer_loop_terminal_phase6_repair_slot_closes_after_one_extra_attempt() -> None:
    windowed = _windowed_stage()
    fixed_pass_run, _ = _scripted_full_chain_runner(
        phase5_screen_acceptances=[0.70],
        verification_acceptances=[0.70],
    )
    fixed_pass = hmc_kernel_tuning.run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        config=hmc_kernel_tuning.HMCFixedMassStepStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 50),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=fixed_pass_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )

    def trajectory_fail_run(_adapter: Any, _initial_state: Any, config: Any):
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.90,
            samples=np.zeros((int(config.num_results), 2)),
        )

    trajectory_fail = hmc_kernel_tuning.run_hmc_frozen_step_trajectory_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=windowed,
        fixed_mass_step_stage=fixed_pass,
        config=hmc_kernel_tuning.HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            seed=(20260621, 60),
            chain_execution_mode="eager",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        run_full_chain=trajectory_fail_run,
        _attempt_budget_policy=_tiny_budget_factory(2, 2),
    )
    trajectory_stage_calls: list[int] = []

    def trajectory_stage_runner(**kwargs: Any):
        attempt_index = int(kwargs["_attempt_index"])
        trajectory_stage_calls.append(attempt_index)
        return trajectory_fail

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(
            max_attempts=1,
            terminal_phase6_repair_extra_attempts=1,
            trajectory_window_lower_multiplier=0.01,
            trajectory_window_upper_multiplier=100.0,
        ),
        _budget_policy_factory=_tiny_budget_factory,
        _windowed_stage_runner=lambda **_kwargs: windowed,
        _fixed_mass_step_stage_runner=lambda **_kwargs: fixed_pass,
        _frozen_step_trajectory_stage_runner=trajectory_stage_runner,
        _phase7_final_verification_runner=lambda **_kwargs: (_ for _ in ()).throw(
            AssertionError("verification must not run when Phase 6 fails")
        ),
    )

    assert result.final_status == "budget_exhausted"
    assert result.diagnostic_role == "phase7_terminal_phase6_repair_slot_exhausted"
    assert len(result.attempts) == 2
    assert trajectory_stage_calls == [0, 1]
    guard = result.terminal_budget_guard_payload
    assert guard["classification"] == "phase7_terminal_phase6_repair_slot_exhausted"
    assert guard["terminal_phase6_repair_extra_attempts"] == 1
    assert guard["terminal_phase6_repair_extra_attempts_consumed"] == 1
    public_guard = hmc_kernel_tuning._phase7_public_summary(result)[
        "terminal_budget_guard"
    ]
    assert public_guard["classification"] == guard["classification"]
    assert public_guard["hmc_mechanics_exposed"] is False


def test_outer_loop_terminal_phase6_repair_slot_config_default_and_public_threading() -> None:
    kernel_config = hmc_kernel_tuning.HMCKernelTuningConfig.standard()
    assert kernel_config.terminal_phase6_repair_extra_attempts == 0
    assert (
        kernel_config.payload()["terminal_phase6_repair_extra_attempts"]
        == 0
    )
    loop_config = hmc_kernel_tuning._public_loop_config(kernel_config)
    assert loop_config.terminal_phase6_repair_extra_attempts == 0
    assert (
        loop_config.payload()["terminal_phase6_repair_extra_attempts"]
        == 0
    )
    opted_in = hmc_kernel_tuning.HMCKernelTuningConfig.standard(
        terminal_phase6_repair_extra_attempts=1
    )
    assert (
        hmc_kernel_tuning._public_loop_config(opted_in)
        .terminal_phase6_repair_extra_attempts
        == 1
    )
    with pytest.raises(ValueError, match="terminal_phase6_repair_extra_attempts"):
        hmc_kernel_tuning.HMCKernelTuningConfig.standard(
            terminal_phase6_repair_extra_attempts=2
        )
    with pytest.raises(ValueError, match="terminal_phase6_repair_extra_attempts"):
        _loop_config(terminal_phase6_repair_extra_attempts=-1)


def test_outer_loop_public_exports_are_scoped_without_final_tuner() -> None:
    assert bayesfilter.HMCTuneVerifyRepairLoopConfig is HMCTuneVerifyRepairLoopConfig
    assert bayesfilter.HMCTuneVerifyRepairLoopResult is HMCTuneVerifyRepairLoopResult
    assert bayesfilter.run_hmc_tune_verify_repair_loop is run_hmc_tune_verify_repair_loop
    assert bayesfilter.TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS is TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    assert hasattr(bayesfilter, "tune_hmc_kernel")
    assert "tune_hmc_kernel" in bayesfilter.__all__
