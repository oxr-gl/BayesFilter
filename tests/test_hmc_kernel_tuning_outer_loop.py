from __future__ import annotations

import inspect
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
    HMCTuneVerifyRepairLoopConfig,
    HMCTuneVerifyRepairLoopResult,
    TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS,
    run_hmc_tune_verify_repair_loop,
)
from bayesfilter.inference.hmc_kernel_tuning import (
    _HMCAttemptBudgetPolicy,
    _default_attempt_budget_policy,
)

from tests.test_hmc_kernel_tuning_fixed_mass_step import (
    _ToyGaussianAdapter,
    _bootstrap,
    _fake_result,
    _geometry,
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
    with pytest.raises(ValueError, match="hard-capped"):
        HMCTuneVerifyRepairLoopConfig(max_attempts=6)


def test_default_budget_policy_matches_reviewed_phase7_mapping() -> None:
    policy0 = _default_attempt_budget_policy(17, 0)
    policy1 = _default_attempt_budget_policy(17, 1)

    assert policy0.budget == 1700
    assert policy0.phase4_warmup_steps == 1700
    assert policy0.phase5_tune_budgets == (425, 850, 1700)
    assert policy0.phase5_screen_num_results == 425
    assert policy0.phase5_screen_burnin_steps == 107
    assert policy0.phase6_screen_num_results == 425
    assert policy0.phase6_screen_burnin_steps == 107
    assert policy0.verification_num_results == 850
    assert policy0.verification_num_burnin_steps == 213
    assert policy1.budget == 3400
    assert policy1.verification_num_results == 1700
    assert policy1.phase5_tune_budgets == (850, 1700, 3400)


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


def test_outer_loop_default_tf_function_verification_uses_reusable_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[Mapping[str, Any]] = []

    class _FakeReusableRunner:
        def __init__(self, config: Any) -> None:
            self.config = config

        def run(self, *, current_state: Any, seed: Any, step_size: Any):
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

    def fake_builder(adapter: Any, initial_state_template: Any, config: Any) -> _FakeReusableRunner:
        calls.append(
            {
                "role": "build",
                "adapter_signature": adapter.adapter_signature(),
                "num_results": int(config.num_results),
                "num_burnin_steps": int(config.num_burnin_steps),
                "uses_dual_averaging": bool(config.tuning_policy.uses_dual_averaging),
                "initial_state_template": np.asarray(initial_state_template, dtype=float),
            }
        )
        return _FakeReusableRunner(config)

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
    assert route["active_route"] == "phase7_final_verification_scoped_reusable_runner"
    assert route["single_use_build_count"] == 0
    assert route["fallback_status"] == "none"
    assert "primarily consistency and regression protection" in route[
        "route_nonclaims"
    ][1]
    assert verification["runtime_metadata"]["kernel_stage_route"] == (
        "phase7_final_verification_scoped_reusable_runner"
    )
    assert any(
        call["role"] == "build"
        and call["num_results"] == result.attempts[0].verification_config_payload[
            "num_results"
        ]
        and call["num_burnin_steps"]
        == result.attempts[0].verification_config_payload["num_burnin_steps"]
        and call["uses_dual_averaging"] is False
        for call in calls
    )


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
    assert stage_names == [
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
        "fixed_mass_step_complete",
        "trajectory_start",
        "trajectory_complete",
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
    assert events[-1][1]["extra"]["final_status"] == "passed"
    assert all(payload["reports_posterior_convergence"] is False for _stage, payload in events)


def test_outer_loop_repairs_with_private_handoff_and_doubled_budget() -> None:
    run, _calls = _scripted_full_chain_runner(verification_acceptances=[0.82, 0.70])

    result = run_hmc_tune_verify_repair_loop(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_loop_config(max_attempts=3),
        run_full_chain=run,
        _budget_policy_factory=_tiny_budget_factory,
    )

    assert result.final_status == "passed"
    assert len(result.attempts) == 2
    assert result.attempts[0].final_status == "repair_or_retry"
    assert "verification_acceptance_outside_pass_band" in result.attempts[0].repair_triggers
    assert result.attempts[0].handoff_state_payload["handoff_stage"] == "phase6"
    assert result.attempts[0].handoff_state_payload["required_private_handoff_complete"] is True
    assert result.attempts[0].handoff_state_payload["final_kernel_handoff_complete"] is True
    assert result.attempts[1].incoming_state_payload["required_private_handoff_complete"] is True
    assert result.attempts[0].budget_policy_payload["budget"] == 8
    assert result.attempts[1].budget_policy_payload["budget"] == 16
    assert result.attempts[1].verification_config_payload["num_results"] == 8
    assert result.final_kernel_payload["attempt_index"] == 1


def test_outer_loop_phase5_acceptance_repair_uses_private_step_handoff() -> None:
    run, _calls = _scripted_full_chain_runner(
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
    assert len(result.attempts) == 2
    first = result.attempts[0]
    assert first.final_status == "repair_or_retry"
    assert "screen_acceptance_above_repair_band" in first.repair_triggers
    assert first.fixed_mass_step_stage.selected_step_payload is None
    assert first.fixed_mass_step_stage.repair_step_payload is not None
    assert first.frozen_step_trajectory_stage is None
    assert first.verification_config_payload is None
    assert first.handoff_state_payload["handoff_stage"] == "phase5_repair"
    assert first.handoff_state_payload["stage_repair_handoff_complete"] is True
    assert first.handoff_state_payload["final_kernel_handoff_complete"] is False
    assert result.attempts[1].incoming_state_payload["handoff_stage"] == "phase5_repair"
    assert result.attempts[1].budget_policy_payload["budget"] == 16


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


def test_outer_loop_public_exports_are_scoped_without_final_tuner() -> None:
    assert bayesfilter.HMCTuneVerifyRepairLoopConfig is HMCTuneVerifyRepairLoopConfig
    assert bayesfilter.HMCTuneVerifyRepairLoopResult is HMCTuneVerifyRepairLoopResult
    assert bayesfilter.run_hmc_tune_verify_repair_loop is run_hmc_tune_verify_repair_loop
    assert bayesfilter.TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS is TUNE_VERIFY_REPAIR_LOOP_NONCLAIMS
    assert hasattr(bayesfilter, "tune_hmc_kernel")
    assert "tune_hmc_kernel" in bayesfilter.__all__
