from __future__ import annotations

import inspect
import json
import os
from pathlib import Path
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import pytest

import bayesfilter
from bayesfilter.inference import (
    FixedMassHMCTuningBudgetCallbackResult,
    HMCFrozenStepTrajectoryStageConfig,
    HMCFrozenStepTrajectoryStageResult,
    HMCKernelTuningConfig,
    HMCKernelTuningResult,
    HMCTuneVerifyRepairAttempt,
    HMCTuneVerifyRepairLoopConfig,
    HMCTuneVerifyRepairLoopResult,
    HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS,
    tune_hmc_kernel,
)
from bayesfilter.runtime import stable_config_hash

import bayesfilter.inference.hmc_kernel_tuning as hmc_kernel_tuning_module
from tests.test_hmc_kernel_tuning_fixed_mass_step import _ToyGaussianAdapter
from tests.test_hmc_kernel_tuning_fixed_mass_step import _bootstrap as _passed_bootstrap
from tests.test_hmc_kernel_tuning_fixed_mass_step import _geometry
from tests.test_hmc_kernel_tuning_outer_loop import _loop_config
from tests.test_hmc_kernel_tuning_bootstrap import _config as _bootstrap_config
from tests.test_hmc_kernel_tuning_bootstrap import _fake_result as _bootstrap_fake_result
from tests.test_hmc_kernel_tuning_bootstrap import run_hmc_bootstrap_screen


def _bootstrap_passed():
    return _passed_bootstrap()


def _loop_result(*, passed: bool = True) -> HMCTuneVerifyRepairLoopResult:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    config = _loop_config(max_attempts=1)
    attempt = HMCTuneVerifyRepairAttempt(
        attempt_index=0,
        budget_policy_payload={"budget": 8, "internal_policy_only": True},
        incoming_state_payload=None,
        windowed_stage=None,
        fixed_mass_step_stage=None,
        frozen_step_trajectory_stage=None,
        verification_config_payload={"trace_policy": "standard"},
        verification_diagnostics={
            "acceptance_rate": 0.70 if passed else 0.82,
            "reports_posterior_convergence": False,
        },
        verification_callback_result=FixedMassHMCTuningBudgetCallbackResult(),
        final_status="passed" if passed else "repair_or_retry",
        diagnostic_role="fresh_fixed_kernel_verification_passed"
        if passed
        else "verification_acceptance_repair_trigger",
        hard_vetoes=(),
        repair_triggers=()
        if passed
        else ("verification_acceptance_outside_pass_band",),
        handoff_state_payload={
            "required_private_handoff_complete": True,
            "mass_artifact_signature": geometry.mass_artifact_signature,
            "selected_step_size": 0.2,
            "selected_step_hash": "step-hash",
            "selected_num_leapfrog_steps": 8,
            "selected_trajectory_hash": "trajectory-hash",
        },
    )
    final_kernel_payload = None
    final_kernel_hash = None
    if passed:
        final_kernel_payload = {
            "runtime": "bayesfilter.inference.run_hmc_tune_verify_repair_loop",
            "schema": "bayesfilter.hmc_frozen_kernel_handoff.v1",
            "target_scope": "kernel_fixed_mass_step_toy_gaussian",
            "target_dimension": geometry.target_dimension,
            "adapted_mass_artifact_payload": geometry.mass_artifact.to_payload(
                include_arrays=True
            ),
            "adapted_mass_artifact_signature": geometry.mass_artifact_signature,
            "step_size": 0.2,
            "num_leapfrog_steps": 8,
            "trajectory_length": 1.6,
            "target_accept_prob": config.target_accept_prob,
            "acceptance_band": config.acceptance_band,
            "geometry_artifact_hash": geometry.artifact_hash,
            "bootstrap_artifact_hash": bootstrap.artifact_hash,
            "windowed_stage_artifact_hash": "windowed-hash",
            "fixed_mass_step_stage_artifact_hash": "fixed-step-hash",
            "frozen_step_trajectory_stage_artifact_hash": "trajectory-hash",
            "selected_step_hash": "step-hash",
            "selected_trajectory_hash": "trajectory-hash",
            "verification_config_payload": {"num_results": 4},
            "verification_acceptance_rate": 0.70,
            "budget_policy": {"budget": 8, "internal_policy_only": True},
            "fresh_fixed_kernel_verification_passed": True,
            "reports_posterior_convergence": False,
            "reports_sampler_superiority": False,
            "reports_default_readiness": False,
            "reports_external_client_scientific_claim": False,
            "reports_gpu_or_xla_readiness": False,
            "nonclaims": ("synthetic phase7 result only",),
        }
        final_kernel_hash = stable_config_hash(final_kernel_payload)
    return HMCTuneVerifyRepairLoopResult(
        config=config,
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash=bootstrap.artifact_hash,
        adapter_signature=geometry.adapter_signature,
        target_dimension=geometry.target_dimension,
        attempts=(attempt,),
        final_status="passed" if passed else "budget_exhausted",
        diagnostic_role="fresh_fixed_kernel_verification_passed"
        if passed
        else "budget_exhausted_non_promoting",
        hard_vetoes=(),
        repair_triggers=()
        if passed
        else ("phase7_budget_exhausted",),
        final_kernel_payload=final_kernel_payload,
        final_kernel_hash=final_kernel_hash,
        seed_report={"seed_owner": "BayesFilter"},
        diagnostic_roles={
            "fresh_fixed_kernel_verification": "promotion_or_repair_or_hard_veto"
        },
    )


def _loop_result_with_rhat_cap_public_summary() -> HMCTuneVerifyRepairLoopResult:
    base = _loop_result(passed=False)
    attempt = base.attempts[0]
    attempt = HMCTuneVerifyRepairAttempt(
        attempt_index=attempt.attempt_index,
        budget_policy_payload={
            "target_dimension": 2,
            "attempt_index": 0,
            "budget": 8,
            "verification_num_results": 64,
            "verification_num_burnin_steps": 16,
            "phase5_tune_budgets": (2, 4, 8),
            "internal_policy_only": True,
            "public_budget_class": "bounded_public_diagnostic_plus",
            "public_budget_cap": 256,
            "public_max_attempts": 3,
            "public_diagnostic_preset": "diagnostic_plus",
        },
        incoming_state_payload=None,
        windowed_stage=None,
        fixed_mass_step_stage=None,
        frozen_step_trajectory_stage=None,
        verification_config_payload={
            "verification_policy": "sequential_rhat",
            "acceptance_band": (0.65, 0.75),
            "max_results": 64,
            "num_burnin_steps": 16,
            "chain_count": 4,
            "step_size": 0.2,
            "num_leapfrog_steps": 8,
        },
        verification_diagnostics={
            "sequential_rhat_verification": True,
            "rhat_threshold": 1.01,
            "check_interval": 64,
            "max_results": 64,
            "all_finite_rhat_at_or_below_threshold": False,
            "cap_hit": True,
            "acceptance_rate": 0.82,
            "runtime_finite": True,
            "log_accept_ratio_finite": True,
            "samples_all_finite": True,
            "target_log_prob_finite": True,
            "runner_route_summary": {
                "active_route": "phase7_sequential_rhat_fixed_size_chunk_verifier",
                "single_use_build_count": 0,
                "fallback_status": "none",
                "semantic_source": "_run_phase7_sequential_rhat_final_verification",
                "step_size": 0.2,
            },
            "samples": [[0.0, 0.1]],
            "trace": {"target_log_prob": [-1.0]},
            "target_status_telemetry": {"target_status_trace": [True]},
            "reports_posterior_convergence": False,
        },
        verification_callback_result=attempt.verification_callback_result,
        final_status="repair_or_retry",
        diagnostic_role="verification_rhat_repair_trigger",
        hard_vetoes=(),
        repair_triggers=(
            "verification_rhat_above_threshold_or_cap_hit",
            "verification_rhat_cap_hit",
        ),
        handoff_state_payload=attempt.handoff_state_payload,
    )
    return HMCTuneVerifyRepairLoopResult(
        config=base.config,
        geometry_artifact_hash=base.geometry_artifact_hash,
        bootstrap_artifact_hash=base.bootstrap_artifact_hash,
        adapter_signature=base.adapter_signature,
        target_dimension=base.target_dimension,
        attempts=(attempt,),
        final_status="budget_exhausted",
        diagnostic_role="budget_exhausted_non_promoting",
        hard_vetoes=(),
        repair_triggers=(
            "verification_rhat_above_threshold_or_cap_hit",
            "verification_rhat_cap_hit",
        ),
        final_kernel_payload=None,
        final_kernel_hash=None,
        seed_report=base.seed_report,
        diagnostic_roles=base.diagnostic_roles,
    )


def _phase6_public_summary_stage() -> HMCFrozenStepTrajectoryStageResult:
    geometry = _geometry()
    return HMCFrozenStepTrajectoryStageResult(
        config=HMCFrozenStepTrajectoryStageConfig(
            target_accept_prob=0.70,
            acceptance_band=(0.65, 0.75),
            seed=(20260630, 41),
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        geometry_artifact_hash=geometry.artifact_hash,
        bootstrap_artifact_hash="bootstrap-hash",
        windowed_stage_artifact_hash="windowed-hash",
        fixed_mass_step_stage_artifact_hash="fixed-step-hash",
        selected_bootstrap_kernel_hash="bootstrap-kernel-hash",
        selected_step_hash="step-hash",
        adapter_signature=geometry.adapter_signature,
        phase4_hmc_adapter_signature="phase4-hmc-signature",
        phase5_ladder_hmc_adapter_signature="phase5-hmc-signature",
        trajectory_hmc_adapter_signature="phase6-hmc-signature",
        adapted_mass_artifact_payload=geometry.mass_artifact.to_payload(
            include_arrays=True
        ),
        adapted_mass_artifact_signature=geometry.mass_artifact_signature,
        frozen_step_size=0.2,
        fixed_bootstrap_num_leapfrog_steps=8,
        target_dimension=geometry.target_dimension,
        candidate_generation={
            "candidate_l_values": (3, 4, 5),
            "verification_repair_neighborhood_applied": True,
        },
        candidate_results=(
            {
                "candidate_index": 0,
                "classification": "repair_or_retry",
                "diagnostics": {"acceptance_rate": 0.80},
            },
            {
                "candidate_index": 1,
                "classification": "repair_or_retry",
                "diagnostics": {},
            },
        ),
        selected_candidate_index=None,
        selected_trajectory_payload=None,
        selected_trajectory_hash=None,
        final_status="repair_or_retry",
        diagnostic_role="repair_trigger",
        hard_vetoes=(),
        repair_triggers=("acceptance_outside_pass_band",),
        diagnostics={
            "expected_candidate_count": 3,
            "completed_candidate_count": 2,
            "skipped_candidate_count": 1,
            "passed_candidate_count": 0,
            "public_timeout_closeout": {
                "enabled": True,
                "timeout_budget_s": 10.0,
                "reserve_s": 5.0,
                "elapsed_s": 9.2,
                "remaining_s": 0.8,
                "within_closeout_window": True,
                "deadline_clock_scope": "public_one_call_global",
                "stage_elapsed_s": 1.2,
                "stage_remaining_s": 8.8,
                "estimated_next_candidate_s": 1.25,
                "completed_candidate_elapsed_count": 2,
                "closeout_required_before_next_candidate": True,
                "diagnostic_role": "public_timeout_closeout_hard_veto",
                "candidate_index": 2,
                "candidate_count": 3,
                "completed_candidate_count": 2,
                "progress_only": True,
                "public_closeout_artifact_expected": True,
                "reason": "phase6_public_timeout_soft_deadline_before_next_candidate",
                "hmc_mechanics_exposed": False,
                "reports_posterior_convergence": False,
                "reports_sampler_superiority": False,
                "reports_default_readiness": False,
                "reports_gpu_or_xla_readiness": False,
                "step_size": 0.2,
                "num_leapfrog_steps": 5,
            },
            "runner_route_summary": {
                "active_route": "single_use_or_injected_runner",
                "reusable_runner_build_count": 0,
                "distinct_static_runner_contract_count": 0,
                "single_use_build_count": 1,
                "injected_runner_call_count": 0,
                "fallback_status": "inactive_reusable_route",
                "round_route_events": ({"num_leapfrog_steps": 3},),
            },
        },
        frozen_mass_invariant={"passed": True},
        frozen_step_invariant={"passed": True},
        seed_report={"seed_owner": "BayesFilter"},
        diagnostic_roles={"trajectory": "handoff_screen_only"},
    )


def _loop_result_with_phase6_public_summary() -> HMCTuneVerifyRepairLoopResult:
    base = _loop_result(passed=False)
    attempt = base.attempts[0]
    attempt = HMCTuneVerifyRepairAttempt(
        attempt_index=attempt.attempt_index,
        budget_policy_payload=attempt.budget_policy_payload,
        incoming_state_payload=attempt.incoming_state_payload,
        windowed_stage=attempt.windowed_stage,
        fixed_mass_step_stage=attempt.fixed_mass_step_stage,
        frozen_step_trajectory_stage=_phase6_public_summary_stage(),
        verification_config_payload=None,
        verification_diagnostics={
            "not_run": "phase6_repair_or_retry",
            "reports_posterior_convergence": False,
        },
        verification_callback_result=attempt.verification_callback_result,
        final_status="repair_or_retry",
        diagnostic_role="repair_trigger",
        hard_vetoes=(),
        repair_triggers=("phase6_trajectory_status:repair_or_retry",),
        handoff_state_payload=attempt.handoff_state_payload,
    )
    return HMCTuneVerifyRepairLoopResult(
        config=base.config,
        geometry_artifact_hash=base.geometry_artifact_hash,
        bootstrap_artifact_hash=base.bootstrap_artifact_hash,
        adapter_signature=base.adapter_signature,
        target_dimension=base.target_dimension,
        attempts=(attempt,),
        final_status="budget_exhausted",
        diagnostic_role="budget_exhausted_non_promoting",
        hard_vetoes=(),
        repair_triggers=("phase6_trajectory_status:repair_or_retry",),
        final_kernel_payload=None,
        final_kernel_hash=None,
        seed_report=base.seed_report,
        diagnostic_roles=base.diagnostic_roles,
    )


def test_public_config_hides_raw_hmc_mechanics() -> None:
    parameters = set(inspect.signature(HMCKernelTuningConfig).parameters)
    forbidden = {
        "step_size",
        "initial_step_size",
        "num_leapfrog_steps",
        "leapfrog_count",
        "min_leapfrog",
        "max_leapfrog",
        "candidate_l_grid",
        "trajectory_grid",
        "mass_window_schedule",
        "warmup_budget_schedule",
        "tuning_budget_schedule",
        "tune_num_results",
        "screen_num_results",
        "verification_num_results",
        "verification_num_burnin_steps",
    }

    assert parameters.isdisjoint(forbidden)
    assert set(HMCKernelTuningConfig.smoke().payload()["forbidden_public_fields"]) >= forbidden


@pytest.mark.parametrize("factory,preset", [
    (HMCKernelTuningConfig.smoke, "smoke"),
    (HMCKernelTuningConfig.standard, "standard"),
    (HMCKernelTuningConfig.serious, "serious"),
])
def test_public_presets_construct_nonclaim_configs(factory: Any, preset: str) -> None:
    config = factory(target_scope="kernel_fixed_mass_step_toy_gaussian")

    assert config.preset == preset
    assert config.use_xla is False
    assert config.payload()["reports_posterior_convergence"] is False
    assert config.payload()["reports_gpu_or_xla_readiness"] is False
    assert config.payload()["hmc_mechanics_owned_by_bayesfilter"] is True


def test_public_xla_runtime_parameter_propagates_to_internal_stage_configs() -> None:
    config = HMCKernelTuningConfig.standard(
        target_scope="kernel_fixed_mass_step_toy_gaussian",
        use_xla=True,
        public_timeout_budget_s=810.0,
    )
    bootstrap = hmc_kernel_tuning_module._public_bootstrap_config(config)
    loop = hmc_kernel_tuning_module._public_loop_config(config)

    assert config.payload()["use_xla"] is True
    assert config.payload()["public_timeout_budget_s"] == pytest.approx(810.0)
    assert bootstrap.use_xla is True
    assert bootstrap.payload()["use_xla"] is True
    assert loop.use_xla is True
    assert loop.payload()["use_xla"] is True
    assert loop.public_timeout_budget_s == pytest.approx(810.0)
    assert loop.public_timeout_started_perf_counter_s is None

    loop_with_anchor = hmc_kernel_tuning_module._public_loop_config(
        config,
        public_timeout_started_perf_counter_s=12.5,
    )
    assert loop_with_anchor.public_timeout_started_perf_counter_s == pytest.approx(12.5)

    windowed = hmc_kernel_tuning_module._phase7_windowed_stage_config(
        loop_with_anchor,
        attempt_index=0,
    )
    fixed_step = hmc_kernel_tuning_module._phase7_fixed_step_stage_config(
        loop_with_anchor,
        attempt_index=0,
    )
    trajectory = hmc_kernel_tuning_module._phase7_trajectory_stage_config(
        loop_with_anchor,
        attempt_index=0,
    )

    assert windowed.use_xla is True
    assert fixed_step.use_xla is True
    assert trajectory.use_xla is True
    assert trajectory.public_timeout_budget_s == pytest.approx(810.0)
    assert trajectory.public_timeout_started_perf_counter_s == pytest.approx(12.5)


def test_public_xla_runtime_parameter_rejects_eager_mode() -> None:
    with pytest.raises(ValueError, match="XLA HMC requires"):
        HMCKernelTuningConfig(
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            chain_execution_mode="eager",
            use_xla=True,
        )

    with pytest.raises(ValueError, match="XLA HMC requires"):
        HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            use_xla=True,
        )


class _XLAReadyToyGaussianAdapter(_ToyGaussianAdapter):
    def value_score_capability(self) -> Any:
        return hmc_kernel_tuning_module.ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            full_chain_xla_diagnostic_ready=True,
            runtime_backend="tests.xla_ready_toy",
            evidence_path="tests/test_hmc_kernel_tuning_public_api.py",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            nonclaims=("tiny xla authority fixture only",),
        )


class _MismatchedScopeXLAReadyToyGaussianAdapter(_ToyGaussianAdapter):
    def value_score_capability(self) -> Any:
        return hmc_kernel_tuning_module.ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            full_chain_xla_diagnostic_ready=True,
            runtime_backend="tests.xla_ready_mismatched_scope_toy",
            evidence_path="tests/test_hmc_kernel_tuning_public_api.py",
            target_scope="different_scope",
            nonclaims=("tiny xla authority fixture only",),
        )


def test_latent_fixed_mass_wrapper_preserves_only_accepted_xla_authority() -> None:
    geometry = _geometry(adapter=_XLAReadyToyGaussianAdapter())
    wrapper = hmc_kernel_tuning_module._build_bootstrap_fixed_mass_adapter(
        adapter=_XLAReadyToyGaussianAdapter(),
        mass_artifact=geometry.mass_artifact,
        mass_signature=geometry.mass_artifact_signature,
        target_scope="kernel_fixed_mass_step_toy_gaussian",
    )
    capability = wrapper.value_score_capability()

    assert capability.xla_hmc_ready is True
    assert capability.full_chain_xla_diagnostic_ready is True
    assert capability.is_accepted_full_chain_xla_diagnostic_authority is True
    assert capability.target_scope == "kernel_fixed_mass_step_toy_gaussian"
    assert capability.evidence_path == "tests/test_hmc_kernel_tuning_public_api.py"

    non_xla_geometry = _geometry()
    non_xla_wrapper = hmc_kernel_tuning_module._build_bootstrap_fixed_mass_adapter(
        adapter=_ToyGaussianAdapter(),
        mass_artifact=non_xla_geometry.mass_artifact,
        mass_signature=non_xla_geometry.mass_artifact_signature,
        target_scope="kernel_fixed_mass_step_toy_gaussian",
    )
    non_xla_capability = non_xla_wrapper.value_score_capability()
    assert non_xla_capability.xla_hmc_ready is False
    assert non_xla_capability.full_chain_xla_diagnostic_ready is False

    mismatched_geometry = _geometry(adapter=_MismatchedScopeXLAReadyToyGaussianAdapter())
    mismatched_wrapper = hmc_kernel_tuning_module._build_bootstrap_fixed_mass_adapter(
        adapter=_MismatchedScopeXLAReadyToyGaussianAdapter(),
        mass_artifact=mismatched_geometry.mass_artifact,
        mass_signature=mismatched_geometry.mass_artifact_signature,
        target_scope="kernel_fixed_mass_step_toy_gaussian",
    )
    mismatched_capability = mismatched_wrapper.value_score_capability()
    assert mismatched_capability.xla_hmc_ready is False
    assert mismatched_capability.full_chain_xla_diagnostic_ready is False


def test_tune_hmc_kernel_runs_phase2_phase3_phase7_in_order(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[str] = []
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    loop = _loop_result(passed=True)

    def geometry_runner(**_kwargs: Any):
        calls.append("geometry")
        return geometry

    def bootstrap_runner(**_kwargs: Any):
        calls.append("bootstrap")
        return bootstrap

    def loop_runner(**_kwargs: Any):
        calls.append("loop")
        return loop

    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", geometry_runner)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", bootstrap_runner)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", loop_runner)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
    )

    assert calls == ["geometry", "bootstrap", "loop"]
    assert isinstance(result, HMCKernelTuningResult)
    assert result.passed is True
    assert result.final_kernel_payload is not None
    assert result.final_kernel_payload["runtime"] == "bayesfilter.inference.tune_hmc_kernel"
    assert result.final_kernel_payload["internal_tuning_controls_exposed"] is False
    assert result.final_kernel_hash == stable_config_hash(result.final_kernel_payload)


def test_phase3_non_pass_does_not_call_phase7(monkeypatch: pytest.MonkeyPatch) -> None:
    geometry = _geometry()
    bootstrap = run_hmc_bootstrap_screen(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        config=_bootstrap_config(
            max_repairs=0,
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=lambda _adapter, _initial_state, _config: _bootstrap_fake_result(
            acceptance=0.95
        ),
    )
    calls: list[str] = []

    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)

    def forbidden_loop(**_kwargs: Any):
        calls.append("loop")
        raise AssertionError("Phase 7 must not run after non-passed bootstrap")

    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", forbidden_loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
    )

    assert calls == []
    assert result.passed is False
    assert result.tune_verify_repair_loop is None
    assert result.final_kernel_payload is None
    assert result.final_kernel_hash is None


def test_final_kernel_emitted_only_after_phase7_pass(monkeypatch: pytest.MonkeyPatch) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    loop = _loop_result(passed=False)
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", lambda **_kwargs: loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
    )

    assert result.passed is False
    assert result.final_kernel_payload is None
    assert result.final_kernel_hash is None
    assert "phase7_budget_exhausted" in result.repair_triggers


def test_output_artifact_is_sanitized_public_evidence(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    loop = _loop_result(passed=True)
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", lambda **_kwargs: loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    artifact_path = tmp_path / "hmc_kernel_tuning_result.json"
    assert result.artifact_path == str(artifact_path)
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert payload["final_kernel_hash"] == result.final_kernel_hash
    assert payload["repair_triggers"] == []
    assert payload["active_repair_triggers"] == []
    assert payload["historical_repair_triggers"] == []
    assert payload["artifact_policy"]["posterior_samples_written"] is False
    assert payload["artifact_policy"]["internal_tuning_controls_exposed"] is False
    assert payload["artifact_policy"]["public_reconstruction_api"] is False
    assert payload["reports_posterior_convergence"] is False
    assert payload["final_kernel_payload"]["verification_acceptance_rate"] == 0.70
    assert payload["final_kernel_payload"]["fresh_fixed_kernel_verification_passed"] is True
    text = json.dumps(payload, sort_keys=True)
    assert "_HMCAttemptBudgetPolicy" not in text
    assert "_HMCPhaseAttemptState" not in text
    assert "candidate_results" not in text
    assert "verification_config_payload" not in text
    assert "budget_policy" not in payload["final_kernel_payload"]


def test_passed_public_artifact_separates_active_and_historical_repair_triggers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    base_loop = _loop_result(passed=True)
    loop = HMCTuneVerifyRepairLoopResult(
        config=base_loop.config,
        geometry_artifact_hash=base_loop.geometry_artifact_hash,
        bootstrap_artifact_hash=base_loop.bootstrap_artifact_hash,
        adapter_signature=base_loop.adapter_signature,
        target_dimension=base_loop.target_dimension,
        attempts=base_loop.attempts,
        final_status=base_loop.final_status,
        diagnostic_role=base_loop.diagnostic_role,
        hard_vetoes=base_loop.hard_vetoes,
        repair_triggers=("verification_acceptance_outside_pass_band",),
        final_kernel_payload=base_loop.final_kernel_payload,
        final_kernel_hash=base_loop.final_kernel_hash,
        seed_report=base_loop.seed_report,
        diagnostic_roles=base_loop.diagnostic_roles,
    )
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", lambda **_kwargs: loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    payload = json.loads(
        (tmp_path / "hmc_kernel_tuning_result.json").read_text(encoding="utf-8")
    )
    assert result.passed is True
    assert result.repair_triggers == ("verification_acceptance_outside_pass_band",)
    assert payload["status"] == "passed"
    assert payload["repair_triggers"] == []
    assert payload["active_repair_triggers"] == []
    assert payload["historical_repair_triggers"] == [
        "verification_acceptance_outside_pass_band"
    ]
    assert payload["final_kernel_payload"]["verification_acceptance_rate"] == 0.70
    assert payload["final_kernel_payload"]["fresh_fixed_kernel_verification_passed"] is True


def test_public_artifact_exposes_phase6_summary_without_candidate_grid_or_mechanics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    loop = _loop_result_with_phase6_public_summary()
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", lambda **_kwargs: loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    payload = json.loads(
        (tmp_path / "hmc_kernel_tuning_result.json").read_text(encoding="utf-8")
    )
    phase7 = payload["phase7_public_summary"]
    phase6 = phase7["latest_phase6_public_summary"]
    assert result.final_kernel_hash is None
    assert payload["artifact_policy"]["candidate_grid_exposed"] is False
    assert payload["artifact_policy"]["phase7_public_summary_exposed"] is True
    assert phase7["final_status"] == "budget_exhausted"
    assert phase6["schema"] == "bayesfilter.hmc_frozen_step_trajectory_public_summary.v1"
    assert phase6["candidate_count"] == 3
    assert phase6["completed_candidate_count"] == 2
    assert phase6["skipped_candidate_count"] == 1
    assert phase6["passed_candidate_count"] == 0
    assert phase6["candidate_acceptance_relation_counts"] == {
        "above_acceptance_band": 1,
        "below_acceptance_band": 0,
        "inside_acceptance_band": 0,
        "unavailable": 1,
    }
    assert phase6["public_timeout_closeout"]["enabled"] is True
    assert phase6["public_timeout_closeout"]["completed_candidate_count"] == 2
    assert phase6["public_timeout_closeout"]["public_closeout_artifact_expected"] is True
    assert (
        phase6["public_timeout_closeout"]["deadline_clock_scope"]
        == "public_one_call_global"
    )
    assert phase6["public_timeout_closeout"]["stage_elapsed_s"] == pytest.approx(1.2)
    assert phase6["public_timeout_closeout"]["hmc_mechanics_exposed"] is False
    assert phase6["candidate_grid_exposed"] is False
    assert phase6["hmc_mechanics_exposed"] is False
    text = json.dumps(phase7, sort_keys=True)
    for forbidden in (
        "candidate_l_values",
        "candidate_results",
        "num_leapfrog_steps",
        "step_size",
        "mass_artifact_payload",
        "samples",
        "trace",
        "target_log_prob",
        "final_state",
        "round_route_events",
    ):
        assert forbidden not in text


def test_public_artifact_exposes_attempt_and_verification_summary_without_mechanics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    loop = _loop_result_with_rhat_cap_public_summary()
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)
    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", lambda **_kwargs: loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    payload = json.loads(
        (tmp_path / "hmc_kernel_tuning_result.json").read_text(encoding="utf-8")
    )
    phase7 = payload["phase7_public_summary"]
    attempt = phase7["attempt_summaries"][0]
    verification = attempt["stage_statuses"]["verification"]
    assert result.final_kernel_hash is None
    assert phase7["attempt_count"] == 1
    assert attempt["attempt_index"] == 0
    assert attempt["budget_public_summary"]["public_budget_class"] == (
        "bounded_public_diagnostic_plus"
    )
    assert attempt["budget_public_summary"]["substage_budget_details_exposed"] is False
    assert verification["verification_policy"] == "sequential_rhat"
    assert verification["sequential_rhat_verification"] is True
    assert verification["cap_hit"] is True
    assert verification["all_finite_rhat_at_or_below_threshold"] is False
    assert verification["acceptance_relation"] == "above_acceptance_band"
    assert verification["acceptance_band_from_payload"] is True
    assert verification["acceptance_band_fallback_used"] is False
    assert verification["max_results"] == 64
    assert verification["runner_route_public_summary"]["active_route"] == (
        "phase7_sequential_rhat_fixed_size_chunk_verifier"
    )
    assert verification["hmc_mechanics_exposed"] is False
    assert attempt["private_handoff_payload_exposed"] is False

    text = json.dumps(phase7, sort_keys=True)
    for forbidden in (
        "step_size",
        "num_leapfrog_steps",
        "phase5_tune_budgets",
        "samples",
        "trace",
        "target_log_prob",
        "target_status_trace",
        "target_status_telemetry",
        "mass_artifact_payload",
        "final_state",
        "selected_kernel_payload",
    ):
        assert forbidden not in text


def test_public_smoke_budget_is_capped_contract_policy() -> None:
    factory = hmc_kernel_tuning_module._public_budget_policy_factory(
        HMCKernelTuningConfig.smoke(target_scope="kernel_fixed_mass_step_toy_gaussian")
    )
    assert factory is not None

    policy = factory(314, 0)

    assert policy.serious_policy is False
    assert policy.budget == 64
    assert policy.phase4_warmup_steps == 64
    assert policy.phase5_tune_budgets == (16, 32, 64)
    assert policy.phase5_screen_num_results == 16
    assert policy.phase5_screen_burnin_steps == 4
    assert policy.phase6_screen_num_results == 16
    assert policy.phase6_screen_burnin_steps == 4
    assert policy.verification_num_results == 32
    assert policy.verification_num_burnin_steps == 8


def test_public_progress_artifact_survives_loop_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)

    def failing_loop(**_kwargs: Any) -> None:
        raise RuntimeError("synthetic loop stop")

    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", failing_loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    progress_path = tmp_path / "hmc_kernel_tuning_progress.json"
    progress = json.loads(progress_path.read_text(encoding="utf-8"))
    assert result.final_status == "hard_veto"
    assert progress["schema"] == "bayesfilter.hmc_kernel_tuning_progress.v1"
    assert progress["current_stage"] == "result_written"
    assert progress["last_started_stage"] == "loop_start"
    assert progress["last_completed_stage"] == "bootstrap_complete"
    assert progress["last_started_artifact_stage"] == "artifact_finalization_start"
    assert progress["last_completed_artifact_stage"] == "artifact_finalization_complete"
    assert progress["adapter_signature"] == geometry.adapter_signature
    assert progress["target_dimension"] == 2
    assert progress["reports_posterior_convergence"] is False
    assert "no posterior convergence claim" in progress["nonclaims"]


def test_public_progress_artifact_survives_internal_loop_substage_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    bootstrap = _bootstrap_passed()
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)

    def failing_loop(**kwargs: Any) -> None:
        callback = kwargs["_progress_callback"]
        budget_policy = kwargs["_budget_policy_factory"](geometry.target_dimension, 0)
        hmc_kernel_tuning_module._emit_phase7_progress(
            callback,
            "loop_attempt_start",
            attempt_index=0,
            budget_policy=budget_policy,
            started=True,
        )
        hmc_kernel_tuning_module._emit_phase7_progress(
            callback,
            "windowed_mass_start",
            attempt_index=0,
            budget_policy=budget_policy,
            started=True,
        )
        hmc_kernel_tuning_module._emit_phase7_progress(
            callback,
            "windowed_mass_complete",
            attempt_index=0,
            budget_policy=budget_policy,
            completed=True,
        )
        hmc_kernel_tuning_module._emit_phase7_progress(
            callback,
            "fixed_mass_step_start",
            attempt_index=0,
            budget_policy=budget_policy,
            started=True,
        )
        raise RuntimeError("synthetic fixed stage stop")

    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", failing_loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.smoke(
            target_scope="kernel_fixed_mass_step_toy_gaussian"
        ),
        output_dir=tmp_path,
    )

    progress = json.loads(
        (tmp_path / "hmc_kernel_tuning_progress.json").read_text(encoding="utf-8")
    )
    assert result.final_status == "hard_veto"
    assert progress["current_stage"] == "result_written"
    assert progress["last_started_stage"] == "fixed_mass_step_start"
    assert progress["last_completed_stage"] == "windowed_mass_complete"
    assert progress["last_started_artifact_stage"] == "artifact_finalization_start"
    assert progress["last_completed_artifact_stage"] == "artifact_finalization_complete"
    assert progress["last_started_substage"] == "fixed_mass_step_start"
    assert progress["last_completed_substage"] == "windowed_mass_complete"
    assert progress["phase7_last_attempt_index"] == 0
    assert progress["phase7_last_budget_payload"]["target_dimension"] == 2
    assert progress["phase7_last_budget_payload"]["budget"] == 8
    assert progress["phase7_last_budget_payload"]["substage_budget_details_exposed"] is False
    assert progress["phase7_last_budget_payload"]["hmc_mechanics_exposed"] is False
    assert progress["reports_posterior_convergence"] is False


def test_public_exports_are_available() -> None:
    assert bayesfilter.HMCKernelTuningConfig is HMCKernelTuningConfig
    assert bayesfilter.HMCKernelTuningResult is HMCKernelTuningResult
    assert bayesfilter.tune_hmc_kernel is tune_hmc_kernel
    assert bayesfilter.HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS is HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS
    assert "tune_hmc_kernel" in bayesfilter.__all__
    assert "no posterior convergence claim" in HMC_KERNEL_TUNING_PUBLIC_NONCLAIMS


def test_public_artifacts_include_sanitized_bootstrap_summary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    geometry = _geometry()
    acceptances = [0.95, 0.20]
    runtimes = [0.2, 0.4]
    bootstrap = run_hmc_bootstrap_screen(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        config=_bootstrap_config(
            max_repairs=1,
            chain_execution_mode="tf_function",
            use_xla=True,
            target_scope="kernel_fixed_mass_step_toy_gaussian",
        ),
        run_full_chain=lambda _adapter, _initial_state, config: _bootstrap_fake_result(
            acceptance=acceptances.pop(0),
            runtime_s=runtimes.pop(0),
            use_xla=bool(config.use_xla),
            timing_scope="synthetic_bootstrap_timing_scope",
        ),
    )
    module = __import__("bayesfilter.inference.hmc_kernel_tuning", fromlist=[""])
    monkeypatch.setattr(module, "initialize_hmc_kernel_geometry", lambda **_kwargs: geometry)
    monkeypatch.setattr(module, "run_hmc_bootstrap_screen", lambda **_kwargs: bootstrap)

    def forbidden_loop(**_kwargs: Any) -> None:
        raise AssertionError("Phase 7 must not run after non-passed bootstrap")

    monkeypatch.setattr(module, "run_hmc_tune_verify_repair_loop", forbidden_loop)

    result = tune_hmc_kernel(
        adapter=_ToyGaussianAdapter(),
        initial_position=[0.0, 0.0],
        config=HMCKernelTuningConfig.standard(
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            bootstrap_max_repairs=1,
            use_xla=True,
        ),
        output_dir=tmp_path,
    )

    assert result.final_status == "repair_budget_exhausted"
    result_payload = json.loads(
        (tmp_path / "hmc_kernel_tuning_result.json").read_text(encoding="utf-8")
    )
    progress_payload = json.loads(
        (tmp_path / "hmc_kernel_tuning_progress.json").read_text(encoding="utf-8")
    )
    allowed = {
        "round_count",
        "final_status",
        "last_round_index",
        "last_classification",
        "last_diagnostic_role",
        "last_acceptance_relation_to_band",
        "observed_acceptance_relations",
        "oscillatory_acceptance_repair_observed",
        "hard_veto_present",
        "hard_veto_categories",
        "leapfrog_cap_saturation_observed",
        "leapfrog_cap_saturation_direction",
        "xla_requested",
        "jit_compile_metadata",
        "round_timing_available",
        "max_round_runtime_s",
        "timing_scope",
        "metadata_limitations",
    }
    forbidden = {
        "step_size",
        "num_leapfrog_steps",
        "unclamped_num_leapfrog_steps",
        "target_trajectory_length",
        "mass_artifact_payload",
        "screen_config_payload",
        "acceptance_rate",
        "repair_band",
        "budget_schedule",
    }
    for payload in (result_payload, progress_payload):
        summary = payload["bootstrap_public_summary"]
        assert set(summary) == allowed
        assert set(summary).isdisjoint(forbidden)
        assert summary["round_count"] == 2
        assert summary["final_status"] == "repair_budget_exhausted"
        assert summary["last_round_index"] == 1
        assert summary["last_classification"] == "repair"
        assert summary["last_diagnostic_role"] == "bootstrap_acceptance_repair_trigger"
        assert summary["last_acceptance_relation_to_band"] == "below"
        assert summary["observed_acceptance_relations"] == ["above", "below"]
        assert summary["oscillatory_acceptance_repair_observed"] is True
        assert summary["hard_veto_present"] is False
        assert summary["hard_veto_categories"] == []
        assert summary["xla_requested"] is True
        assert summary["jit_compile_metadata"] == "true"
        assert summary["round_timing_available"] is True
        assert summary["max_round_runtime_s"] == pytest.approx(0.4)
        assert summary["timing_scope"] == "synthetic_bootstrap_timing_scope"
        summary_text = json.dumps(summary, sort_keys=True)
        assert all(name not in summary_text for name in forbidden)
