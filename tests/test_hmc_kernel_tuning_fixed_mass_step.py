from __future__ import annotations

import inspect
import os
from collections.abc import Mapping
from dataclasses import dataclass, replace
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
from bayesfilter.inference import (
    FixedMassHMCTuningBudgetCallbackResult,
    HMCBootstrapScreenResult,
    HMCFixedMassStepStageConfig,
    HMCFixedMassStepStageResult,
    HMCGeometryInitializationConfig,
    HMCWindowedMassStageConfig,
    HMCWindowedMassStageResult,
    ValueScoreCapability,
    initialize_hmc_kernel_geometry,
    run_hmc_bootstrap_screen,
    run_hmc_fixed_mass_step_stage,
    run_hmc_frozen_step_trajectory_stage,
    run_hmc_windowed_mass_stage,
)


class _ToyGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "kernel-fixed-mass-step-toy-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=False,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_kernel_tuning_fixed_mass_step.py",
            target_scope="kernel_fixed_mass_step_toy_gaussian",
            nonclaims=("tiny fixed-mass step fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        value = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(value), axis=-1), -value


class _MismatchedAdapter(_ToyGaussianAdapter):
    def adapter_signature(self) -> str:
        return "kernel-fixed-mass-step-mismatched-v1"


@dataclass(frozen=True)
class _FakeRunResult:
    samples: Any
    trace: Mapping[str, Any]
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]


def _geometry(**overrides: Any):
    payload = {
        "adapter": _ToyGaussianAdapter(),
        "initial_position": np.zeros(2),
        "config": HMCGeometryInitializationConfig(
            geometry_scaling_c=0.5,
            stability_guard=0.8,
            covariance_jitter=0.0,
            seed=(123, 456),
        ),
    }
    payload.update(overrides)
    return initialize_hmc_kernel_geometry(**payload)


def _runtime_metadata() -> Mapping[str, Any]:
    return {
        "runtime": "tfp.mcmc.sample_chain",
        "sample_chain_invocation_count": 1,
        "sample_chain_call_s": 0.01,
        "trace_unavailability": {},
        "fixture_or_synthetic": False,
        "nonclaims": (
            "deterministic hmc contract plumbing result",
            "no sampler convergence claim",
            "no posterior validity claim",
        ),
    }


def _warmup_draws(warmup_steps: int = 12) -> np.ndarray:
    base = np.array(
        [
            [-0.20, 0.10],
            [-0.10, 0.00],
            [0.10, 0.20],
            [0.20, 0.10],
            [0.30, 0.30],
            [0.40, 0.25],
            [0.50, 0.40],
            [0.60, 0.35],
            [0.70, 0.50],
            [0.80, 0.45],
            [0.90, 0.55],
            [1.00, 0.60],
        ],
        dtype=float,
    )
    return base[:warmup_steps]


def _fake_result(
    *,
    num_results: int,
    acceptance: float = 0.70,
    step_size: float | None = None,
    num_adaptation_steps: int | None = None,
    samples: Any | None = None,
    finite_log_accept: bool = True,
    finite_samples: bool = True,
    finite_target_log_prob: bool = True,
    metadata_overrides: Mapping[str, Any] | None = None,
) -> _FakeRunResult:
    if samples is None:
        sample_array = _warmup_draws(max(num_results, 1))[:num_results]
    else:
        sample_array = np.asarray(samples, dtype=float)
    if not finite_samples:
        sample_array = sample_array.copy()
        sample_array.reshape(-1)[-1] = np.nan
    acceptance_count = int(round(float(acceptance) * int(num_results)))
    acceptance_trace = np.zeros(int(num_results), dtype=bool)
    acceptance_trace[:acceptance_count] = True
    log_accept = np.linspace(-0.2, 0.1, int(num_results))
    if not finite_log_accept:
        log_accept[-1] = np.nan
    target_log_prob = -0.5 * np.sum(np.square(sample_array), axis=-1)
    if not finite_target_log_prob:
        target_log_prob[-1] = np.nan
    trace: dict[str, Any] = {
        "is_accepted": tf.constant(acceptance_trace, dtype=tf.bool),
        "log_accept_ratio": tf.constant(log_accept, dtype=tf.float64),
        "target_log_prob": tf.constant(target_log_prob, dtype=tf.float64),
    }
    diagnostics: dict[str, Any] = {
        "acceptance_rate": tf.constant(float(acceptance), dtype=tf.float64),
        "finite_sample_count": tf.constant(
            int(np.sum(np.all(np.isfinite(sample_array), axis=-1))),
            dtype=tf.int32,
        ),
        "nonfinite_sample_count": tf.constant(
            int(np.sum(~np.all(np.isfinite(sample_array), axis=-1))),
            dtype=tf.int32,
        ),
        "trace_policy": "standard",
    }
    if step_size is not None:
        diagnostics["final_step_size"] = tf.constant(float(step_size), dtype=tf.float64)
        diagnostics["final_step_size_finite"] = tf.constant(
            bool(np.isfinite(step_size))
        )
        trace["step_size"] = tf.constant([float(step_size)], dtype=tf.float64)
    if num_adaptation_steps is not None:
        diagnostics["num_adaptation_steps"] = tf.constant(
            int(num_adaptation_steps),
            dtype=tf.int32,
        )
        diagnostics["target_accept_prob"] = tf.constant(0.70, dtype=tf.float64)
        trace["num_adaptation_steps"] = tf.constant(
            [int(num_adaptation_steps)],
            dtype=tf.int32,
        )
    metadata = dict(_runtime_metadata())
    if metadata_overrides is not None:
        metadata.update(dict(metadata_overrides))
    return _FakeRunResult(
        samples=tf.constant(sample_array, dtype=tf.float64),
        trace=trace,
        diagnostics=diagnostics,
        metadata=metadata,
    )


def _bootstrap() -> HMCBootstrapScreenResult:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=np.zeros((int(config.num_results), 2)),
        )

    return run_hmc_bootstrap_screen(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        run_full_chain=run,
    )


def _stage_config(**overrides: Any) -> HMCFixedMassStepStageConfig:
    payload = {
        "target_accept_prob": 0.70,
        "seed": (20260621, 50),
        "chain_execution_mode": "eager",
        "target_scope": "kernel_fixed_mass_step_toy_gaussian",
    }
    payload.update(overrides)
    return HMCFixedMassStepStageConfig(**payload)


def _windowed_config(**overrides: Any) -> HMCWindowedMassStageConfig:
    payload = {
        "target_accept_prob": 0.70,
        "seed": (20260621, 40),
        "chain_execution_mode": "eager",
        "target_scope": "kernel_fixed_mass_step_toy_gaussian",
    }
    payload.update(overrides)
    return HMCWindowedMassStageConfig(**payload)


def _windowed_stage() -> HMCWindowedMassStageResult:
    bootstrap = _bootstrap()

    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            samples=_warmup_draws(int(config.num_results)),
        )

    return run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=bootstrap,
        config=_windowed_config(),
        run_full_chain=run,
    )


def _scripted_step_runner(screen_acceptances: list[float]):
    calls: list[Mapping[str, Any]] = []

    def run(adapter: Any, initial_state: Any, config: Any) -> _FakeRunResult:
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        calls.append(
            {
                "role": "tune" if uses_tuning else "screen",
                "num_results": int(config.num_results),
                "num_burnin_steps": int(config.num_burnin_steps),
                "step_size": float(config.step_size),
                "num_leapfrog_steps": int(config.num_leapfrog_steps),
                "seed": tuple(config.seed),
                "adapter_signature": adapter.adapter_signature(),
                "initial_state": np.asarray(initial_state, dtype=float),
                "use_xla": bool(config.use_xla),
            }
        )
        np.testing.assert_allclose(np.asarray(initial_state, dtype=float), np.zeros(2))
        if uses_tuning:
            return _fake_result(
                num_results=int(config.num_results),
                acceptance=0.70,
                step_size=0.2 + 0.01 * len(calls),
                num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
                samples=np.zeros((int(config.num_results), 2)),
            )
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=screen_acceptances.pop(0),
            samples=np.zeros((int(config.num_results), 2)),
        )

    return run, calls


def test_fixed_mass_step_config_does_not_expose_hmc_mechanics() -> None:
    parameters = set(inspect.signature(HMCFixedMassStepStageConfig).parameters)
    forbidden = {
        "budget_schedule",
        "tune_num_results",
        "screen_num_results",
        "screen_num_burnin_steps",
        "step_size",
        "initial_step_size",
        "num_leapfrog_steps",
        "min_leapfrog",
        "max_leapfrog",
        "trajectory_grid",
        "candidate_grid",
        "mass_window_schedule",
        "warmup_steps",
    }

    assert parameters.isdisjoint(forbidden)


def test_fixed_mass_step_stage_passes_with_frozen_mass_and_internal_budget() -> None:
    geometry = _geometry()
    bootstrap = _bootstrap()
    windowed = _windowed_stage()
    assert windowed.passed is True
    run, calls = _scripted_step_runner([0.70])

    result = run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed,
        config=_stage_config(),
        run_full_chain=run,
    )

    assert isinstance(result, HMCFixedMassStepStageResult)
    assert result.passed is True
    assert result.final_status == "passed"
    assert [call["role"] for call in calls] == ["tune", "screen"]
    assert calls[0]["step_size"] == pytest.approx(windowed.candidate_step_size)
    assert calls[0]["num_leapfrog_steps"] == bootstrap.selected_round.num_leapfrog_steps
    assert calls[1]["num_leapfrog_steps"] == bootstrap.selected_round.num_leapfrog_steps
    assert calls[0]["use_xla"] is False
    assert calls[1]["use_xla"] is False
    assert result.initial_step_size == pytest.approx(windowed.candidate_step_size)
    assert result.fixed_num_leapfrog_steps == bootstrap.selected_round.num_leapfrog_steps
    assert result.budget_ladder_config_payload["budget_schedule"] == (3, 6, 12)
    assert result.budget_ladder_config_payload["tune_num_results"] == 4
    assert result.budget_ladder_config_payload["screen_num_results"] == 4
    assert result.frozen_mass_invariant["passed"] is True
    assert result.frozen_mass_invariant["mass_update_allowed"] is False


def test_fixed_mass_step_config_use_xla_propagates_to_tune_and_screen_configs() -> None:
    geometry = _geometry()
    bootstrap = _bootstrap()
    windowed = _windowed_stage()
    run, calls = _scripted_step_runner([0.70])

    result = run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed,
        config=_stage_config(chain_execution_mode="tf_function", use_xla=True),
        run_full_chain=run,
    )

    assert result.passed is True
    assert result.config.payload()["use_xla"] is True
    assert [call["use_xla"] for call in calls] == [True, True]
    assert result.selected_step_payload is not None
    assert result.selected_step_hash
    assert result.selected_step_size == pytest.approx(
        result.budget_ladder_result.selected_round.tuned_step_size
    )
    assert result.payload()["reports_trajectory_tuning"] is False
    assert result.payload()["reports_posterior_convergence"] is False
    assert "no trajectory tuning claim" in result.nonclaims


def test_fixed_mass_step_stage_repairs_without_selected_step_when_budget_exhausts() -> None:
    run, _calls = _scripted_step_runner([0.82, 0.83, 0.84])
    geometry = _geometry()
    bootstrap = _bootstrap()
    windowed = _windowed_stage()

    result = run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=geometry,
        bootstrap=bootstrap,
        windowed_stage=windowed,
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "repair_or_retry"
    assert result.selected_step_payload is None
    assert result.selected_step_hash is None
    assert result.selected_step_size is None
    assert result.repair_step_payload is not None
    assert result.repair_step_hash
    assert result.repair_step_size == pytest.approx(
        result.budget_ladder_result.last_finite_tuned_round.tuned_step_size
    )
    assert result.budget_ladder_result.final_status == "budget_exhausted"
    assert result.repair_triggers == ("acceptance_outside_pass_band_inside_repair_band",)
    payload = result.payload()
    assert payload["repair_step_available"] is True
    assert payload["repair_step_payload_exposed"] is False
    assert "repair_step_payload" not in payload
    with pytest.raises(ValueError, match="requires passed Phase 5"):
        run_hmc_frozen_step_trajectory_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=geometry,
            bootstrap=bootstrap,
            windowed_stage=windowed,
            fixed_mass_step_stage=result,
            run_full_chain=_scripted_step_runner([0.70])[0],
        )


def test_fixed_mass_step_stage_requires_passed_phase4() -> None:
    windowed = replace(_windowed_stage(), final_status="hard_veto")

    with pytest.raises(ValueError, match="requires passed Phase 4"):
        run_hmc_fixed_mass_step_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            windowed_stage=windowed,
            config=_stage_config(),
            run_full_chain=_scripted_step_runner([0.70])[0],
        )


def test_fixed_mass_step_stage_rejects_signature_and_lineage_mismatch() -> None:
    with pytest.raises(ValueError, match="adapter signature"):
        run_hmc_fixed_mass_step_stage(
            adapter=_MismatchedAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            windowed_stage=_windowed_stage(),
            config=_stage_config(),
            run_full_chain=_scripted_step_runner([0.70])[0],
        )

    bad_windowed = replace(
        _windowed_stage(),
        selected_bootstrap_kernel_hash="stale-selected-kernel",
    )
    with pytest.raises(ValueError, match="selected bootstrap kernel mismatch"):
        run_hmc_fixed_mass_step_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            windowed_stage=bad_windowed,
            config=_stage_config(),
            run_full_chain=_scripted_step_runner([0.70])[0],
        )


def test_fixed_mass_step_stage_rejects_adapted_mass_signature_mismatch() -> None:
    windowed = _windowed_stage()
    bad_windowed_result = replace(windowed.windowed_mass_result)
    object.__setattr__(
        bad_windowed_result,
        "final_mass_artifact_signature",
        "stale-adapted-mass-signature",
    )
    bad_windowed = replace(windowed, windowed_mass_result=bad_windowed_result)

    with pytest.raises(ValueError, match="Phase 4 adapted mass signature mismatch"):
        run_hmc_fixed_mass_step_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            windowed_stage=bad_windowed,
            config=_stage_config(),
            run_full_chain=_scripted_step_runner([0.70])[0],
        )


def test_fixed_mass_step_stage_callback_roles_are_preserved() -> None:
    run, _calls = _scripted_step_runner([0.70])

    def callback(
        _round_payload: Mapping[str, Any],
        _samples: Any,
        _diagnostics: Mapping[str, Any],
    ) -> FixedMassHMCTuningBudgetCallbackResult:
        return FixedMassHMCTuningBudgetCallbackResult(
            continuation_vetoes=("artifact_cannot_answer_question",),
        )

    result = run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=_windowed_stage(),
        config=_stage_config(),
        screen_callback=callback,
        run_full_chain=run,
    )

    assert result.final_status == "hard_veto"
    assert "fixed_mass_step_continuation_veto" in result.hard_vetoes
    assert result.diagnostics["continuation_vetoes"] == (
        "artifact_cannot_answer_question",
    )
    assert result.selected_step_payload is None


def test_fixed_mass_step_stage_hard_veto_on_nonfinite_tune_diagnostic() -> None:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        uses_tuning = bool(config.tuning_policy.uses_dual_averaging)
        return _fake_result(
            num_results=int(config.num_results),
            acceptance=0.70,
            step_size=np.nan if uses_tuning else None,
            num_adaptation_steps=(
                config.tuning_policy.num_adaptation_steps if uses_tuning else None
            ),
            samples=np.zeros((int(config.num_results), 2)),
        )

    result = run_hmc_fixed_mass_step_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        windowed_stage=_windowed_stage(),
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.final_status == "hard_veto"
    assert "tune_final_step_missing_or_nonfinite" in result.hard_vetoes
    assert result.selected_step_payload is None


def test_fixed_mass_step_stage_public_exports_are_scoped_without_final_tuner() -> None:
    assert bayesfilter.HMCFixedMassStepStageConfig is HMCFixedMassStepStageConfig
    assert bayesfilter.run_hmc_fixed_mass_step_stage is run_hmc_fixed_mass_step_stage
    assert hasattr(bayesfilter, "tune_hmc_kernel")
    assert "tune_hmc_kernel" in bayesfilter.__all__
