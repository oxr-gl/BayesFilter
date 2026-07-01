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

import bayesfilter.inference.hmc_kernel_tuning as hmc_kernel_tuning
from bayesfilter.inference import (
    HMCBootstrapScreenResult,
    HMCGeometryInitializationConfig,
    HMCWindowedMassStageConfig,
    HMCWindowedMassStageResult,
    PrecomputedMassArtifact,
    ValueScoreCapability,
    initialize_hmc_kernel_geometry,
    run_hmc_bootstrap_screen,
    run_hmc_windowed_mass_stage,
)


class _ToyGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "kernel-windowed-mass-toy-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=False,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_kernel_tuning_windowed_mass.py",
            target_scope="kernel_windowed_mass_toy_gaussian",
            nonclaims=("tiny windowed mass fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        value = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(value), axis=-1), -value


class _MismatchedAdapter(_ToyGaussianAdapter):
    def adapter_signature(self) -> str:
        return "kernel-windowed-mass-mismatched-v1"


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


def _bootstrap() -> HMCBootstrapScreenResult:
    def run(_adapter: Any, _initial_state: Any, _config: Any) -> _FakeRunResult:
        return _fake_result(warmup_steps=4, acceptance_trace=[True, True, False, True])

    return run_hmc_bootstrap_screen(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        run_full_chain=run,
    )


def _stage_config(**overrides: Any) -> HMCWindowedMassStageConfig:
    payload = {
        "target_accept_prob": 0.70,
        "seed": (20260621, 40),
        "chain_execution_mode": "eager",
        "target_scope": "kernel_windowed_mass_toy_gaussian",
    }
    payload.update(overrides)
    return HMCWindowedMassStageConfig(**payload)


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
    warmup_steps: int = 12,
    acceptance_trace: list[bool] | None = None,
    finite_samples: bool = True,
    finite_log_accept: bool = True,
    finite_target_log_prob: bool = True,
    runtime_s: float = 0.01,
    metadata_overrides: Mapping[str, Any] | None = None,
) -> _FakeRunResult:
    samples = _warmup_draws(warmup_steps)
    if not finite_samples:
        samples = samples.copy()
        samples[-1, -1] = np.nan
    if acceptance_trace is None:
        acceptance_trace = [
            True,
            True,
            False,
            True,
            True,
            False,
            True,
            True,
            True,
            False,
            True,
            True,
        ][:warmup_steps]
    trace = {
        "is_accepted": tf.constant(acceptance_trace, dtype=tf.bool),
        "log_accept_ratio": tf.constant(
            np.linspace(-0.2, 0.1, warmup_steps)
            if finite_log_accept
            else [0.0] * (warmup_steps - 1) + [np.nan],
            dtype=tf.float64,
        ),
        "target_log_prob": tf.constant(
            -0.5 * np.sum(np.square(samples), axis=-1)
            if finite_target_log_prob
            else [0.0] * (warmup_steps - 1) + [np.nan],
            dtype=tf.float64,
        ),
    }
    diagnostics = {
        "acceptance_rate": tf.constant(
            float(np.mean(np.asarray(acceptance_trace, dtype=float))),
            dtype=tf.float64,
        ),
        "finite_sample_count": tf.constant(
            int(np.sum(np.all(np.isfinite(samples), axis=-1))),
            dtype=tf.int32,
        ),
        "nonfinite_sample_count": tf.constant(
            int(np.sum(~np.all(np.isfinite(samples), axis=-1))),
            dtype=tf.int32,
        ),
        "trace_policy": "standard",
    }
    metadata = {
        "sample_chain_call_s": runtime_s,
        "trace_unavailability": {},
        "fixture_or_synthetic": True,
        "nonclaims": ("fake runner only",),
    }
    if metadata_overrides is not None:
        metadata.update(dict(metadata_overrides))
    return _FakeRunResult(
        samples=tf.constant(samples, dtype=tf.float64),
        trace=trace,
        diagnostics=diagnostics,
        metadata=metadata,
    )


def _runtime_shaped_result(
    *,
    warmup_steps: int = 12,
    acceptance_trace: list[bool] | None = None,
    **kwargs: Any,
) -> _FakeRunResult:
    return _fake_result(
        warmup_steps=warmup_steps,
        acceptance_trace=acceptance_trace,
        metadata_overrides={
            "runtime": "tfp.mcmc.sample_chain",
            "sample_chain_invocation_count": 1,
            "fixture_or_synthetic": False,
            "nonclaims": (
                "deterministic hmc contract plumbing result",
                "no sampler convergence claim",
                "no posterior validity claim",
            ),
        },
        **kwargs,
    )


def test_windowed_mass_config_does_not_expose_hmc_mechanics() -> None:
    parameters = set(inspect.signature(HMCWindowedMassStageConfig).parameters)
    forbidden = {
        "step_size",
        "initial_step_size",
        "num_leapfrog_steps",
        "min_leapfrog",
        "max_leapfrog",
        "num_results",
        "num_burnin_steps",
        "warmup_steps",
        "initial_buffer",
        "final_buffer",
        "first_window_size",
        "mass_window_schedule",
        "trajectory_grid",
        "candidate_grid",
        "budget_schedule",
    }

    assert parameters.isdisjoint(forbidden)


def test_windowed_mass_stage_runs_retained_draw_route_and_preserves_nonclaims() -> None:
    calls: list[tuple[int, int, float, int, bool]] = []

    def run(adapter: Any, initial_state: Any, config: Any) -> _FakeRunResult:
        calls.append(
            (
                int(config.num_results),
                int(config.num_burnin_steps),
                float(config.step_size),
                int(config.num_leapfrog_steps),
                bool(config.use_xla),
            )
        )
        np.testing.assert_allclose(initial_state.numpy(), np.zeros(2))
        assert adapter.adapter_signature() == _bootstrap().hmc_adapter_signature
        return _runtime_shaped_result(warmup_steps=int(config.num_results))

    bootstrap = _bootstrap()
    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=bootstrap,
        config=_stage_config(),
        run_full_chain=run,
    )

    assert isinstance(result, HMCWindowedMassStageResult)
    assert result.passed is True
    assert result.final_status == "passed"
    assert calls == [(12, 1, bootstrap.selected_round.step_size, bootstrap.selected_round.num_leapfrog_steps, False)]
    assert result.draw_capture_policy["route"] == "retained_fixed_kernel_samples"
    assert result.draw_capture_policy["num_results"] == 12
    assert result.draw_capture_policy["api_discarded_burnin_counted_as_adaptation_input"] is False
    assert result.warmup_draw_provenance["adaptation_input_only"] is True
    assert result.warmup_draw_provenance["fixture_or_synthetic"] is False
    assert result.acceptance_telemetry_provenance["source"].endswith("trace.is_accepted")


def test_windowed_mass_stage_private_progress_callback_is_allowlisted() -> None:
    events: list[tuple[str, Mapping[str, Any]]] = []
    forbidden_keys = {
        "step_size",
        "initial_step_size",
        "num_leapfrog_steps",
        "min_leapfrog",
        "max_leapfrog",
        "bracket",
        "bracket_low",
        "bracket_high",
        "acceptance_rate",
        "runtime_metadata",
        "raw_diagnostics",
        "trace",
        "samples",
        "mass",
        "mass_artifact",
        "mass_artifact_payload",
        "budget_policy",
        "phase4_warmup_steps",
        "phase5_tune_budgets",
        "config",
        "diagnostic_config",
    }

    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _runtime_shaped_result(warmup_steps=int(config.num_results))

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(),
        run_full_chain=run,
        _progress_callback=lambda stage, payload: events.append((stage, payload)),
        _attempt_index=3,
    )

    assert result.passed is True
    assert [stage for stage, _payload in events] == [
        "windowed_mass_runner_build_start",
        "windowed_mass_runner_build_complete",
        "windowed_mass_runner_execute_start",
        "windowed_mass_runner_execute_complete",
        "windowed_mass_capture_start",
        "windowed_mass_capture_complete",
        "windowed_mass_semantic_diagnostic_start",
        "windowed_mass_semantic_diagnostic_complete",
    ]
    for stage, payload in events:
        assert payload["stage"] == stage
        assert payload["attempt_index"] == 3
        assert payload["progress_only"] is True
        assert payload["hmc_mechanics_exposed"] is False
        assert payload["route_category"] == "injected_runner"
        assert payload["reports_posterior_convergence"] is False
        assert payload["reports_sampler_superiority"] is False
        assert payload["reports_default_readiness"] is False
        assert payload["reports_external_client_scientific_claim"] is False
        assert payload["reports_gpu_or_xla_readiness"] is False
        assert "no posterior convergence claim" in payload["nonclaims"]
        assert set(payload).isdisjoint(forbidden_keys)
    for _stage, payload in events[1::2]:
        assert payload["completed"] is True
        assert payload["elapsed_s"] >= 0.0
    for _stage, payload in events[0::2]:
        assert payload["started"] is True
        assert payload["elapsed_s"] == pytest.approx(0.0)
        assert payload["started_perf_counter_s"] >= 0.0
        assert payload["timing_anchor_role"] == "process_local_monotonic_debug_only"


def test_windowed_mass_config_use_xla_propagates_to_full_chain_config() -> None:
    calls: list[bool] = []

    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        calls.append(bool(config.use_xla))
        return _runtime_shaped_result(warmup_steps=int(config.num_results))

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(chain_execution_mode="tf_function", use_xla=True),
        run_full_chain=run,
    )

    assert result.passed is True
    assert result.config.payload()["use_xla"] is True
    assert calls == [True]
    assert result.acceptance_telemetry_provenance["fixture_or_synthetic"] is False
    assert result.acceptance_telemetry_provenance["policy_filled_or_default"] is False
    assert result.windowed_mass_result is not None
    assert result.windowed_mass_result.final_mass_artifact_signature == result.adapted_mass_artifact_signature
    assert result.candidate_step_size == result.windowed_mass_result.final_step_size
    assert result.payload()["reports_posterior_convergence"] is False
    assert "no posterior convergence claim" in result.nonclaims


def test_windowed_mass_injected_tf_function_run_does_not_build_reusable_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, Any]] = []

    def fail_if_built(*_args: Any, **_kwargs: Any) -> Any:
        raise AssertionError("injected run_full_chain must bypass reusable runner")

    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        calls.append(
            {
                "chain_execution_mode": config.chain_execution_mode,
                "use_xla": bool(config.use_xla),
            }
        )
        return _runtime_shaped_result(warmup_steps=int(config.num_results))

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_reusable_full_chain_tfp_hmc_runner",
        fail_if_built,
    )

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(chain_execution_mode="tf_function", use_xla=True),
        run_full_chain=run,
    )

    assert result.passed is True
    assert calls == [{"chain_execution_mode": "tf_function", "use_xla": True}]
    assert result.diagnostics["runtime_metadata"]["sample_chain_invocation_count"] == 1


def test_windowed_mass_default_tf_function_route_uses_reusable_runner(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []

    class _FakeReusableRunner:
        def __init__(self, diagnostic_config: Any) -> None:
            self.diagnostic_config = diagnostic_config

        def run(self, *, current_state: Any, seed: Any, step_size: Any) -> _FakeRunResult:
            calls.append(
                {
                    "run_called": True,
                    "seed": tuple(int(item) for item in seed),
                    "step_size": float(step_size),
                    "initial_state": np.asarray(current_state, dtype=float),
                }
            )
            return _fake_result(
                warmup_steps=int(self.diagnostic_config.num_results),
                metadata_overrides={
                    "runtime": "tfp.mcmc.sample_chain",
                    "sample_chain_invocation_count": 1,
                    "fixture_or_synthetic": False,
                    "reusable_runner": True,
                    "sample_chain_timing_scope": (
                        "reusable_tf_function_first_call_trace_compile_plus_execute_then_warm_execute"
                    ),
                    "nonclaims": (
                        "deterministic reusable hmc contract plumbing result",
                        "no sampler convergence claim",
                        "no posterior validity claim",
                    ),
                },
            )

    def fake_builder(adapter: Any, initial_state_template: Any, config: Any) -> _FakeReusableRunner:
        calls.append(
            {
                "builder_called": True,
                "adapter_signature": adapter.adapter_signature(),
                "initial_state_template": np.asarray(initial_state_template, dtype=float),
                "chain_execution_mode": config.chain_execution_mode,
                "use_xla": bool(config.use_xla),
            }
        )
        return _FakeReusableRunner(config)

    monkeypatch.setattr(
        hmc_kernel_tuning,
        "build_reusable_full_chain_tfp_hmc_runner",
        fake_builder,
    )
    bootstrap = _bootstrap()

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=bootstrap,
        config=_stage_config(chain_execution_mode="tf_function", use_xla=False),
    )

    assert result.passed is True
    assert [sorted(call) for call in calls] == [
        sorted(
            {
                "builder_called": True,
                "adapter_signature": "",
                "initial_state_template": np.array([]),
                "chain_execution_mode": "",
                "use_xla": False,
            }
        ),
        sorted(
            {
                "run_called": True,
                "seed": (),
                "step_size": 0.0,
                "initial_state": np.array([]),
            }
        ),
    ]
    assert calls[0]["adapter_signature"] == bootstrap.hmc_adapter_signature
    np.testing.assert_allclose(calls[0]["initial_state_template"], np.zeros(2))
    assert calls[0]["chain_execution_mode"] == "tf_function"
    assert calls[0]["use_xla"] is False
    np.testing.assert_allclose(calls[1]["initial_state"], np.zeros(2))
    assert calls[1]["step_size"] == pytest.approx(bootstrap.selected_round.step_size)
    assert result.diagnostics["runtime_metadata"]["reusable_runner"] is True
    assert result.diagnostics["runtime_metadata"]["sample_chain_timing_scope"].startswith(
        "reusable_tf_function"
    )
    assert result.diagnostics["runtime_metadata"]["windowed_stage_route_category"] == (
        "reusable_runner"
    )
    assert result.diagnostics["runtime_metadata"]["windowed_stage_runner_build_s"] >= 0.0
    assert result.diagnostics["runtime_metadata"]["windowed_stage_runner_execute_s"] >= 0.0
    assert result.diagnostics["runtime_metadata"]["windowed_stage_capture_s"] >= 0.0
    assert (
        result.diagnostics["runtime_metadata"]["timing_buckets"][
            "windowed_stage_capture_s"
        ]
        == "explanatory_only_windowed_stage_public_safe_capture"
    )


def test_windowed_mass_stage_hard_vetoes_fixture_runtime_evidence() -> None:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _fake_result(warmup_steps=int(config.num_results))

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert "windowed_stage_fixture_or_nonruntime_telemetry" in result.hard_vetoes
    assert result.warmup_draw_provenance["fixture_or_synthetic"] is True
    assert result.acceptance_telemetry_provenance["fixture_or_synthetic"] is True
    assert result.windowed_mass_result is None


def test_windowed_mass_stage_hard_vetoes_default_like_acceptance_trace() -> None:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _runtime_shaped_result(
            warmup_steps=int(config.num_results),
            acceptance_trace=[True] * int(config.num_results),
        )

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert "windowed_stage_acceptance_telemetry_invalid_or_default" in result.hard_vetoes
    assert result.acceptance_telemetry_provenance["policy_filled_or_default"] is True
    assert result.windowed_mass_result is None


def test_windowed_mass_stage_requires_passed_bootstrap_selected_kernel() -> None:
    bootstrap = replace(_bootstrap(), selected_round_index=None, final_status="hard_veto")

    with pytest.raises(ValueError, match="passed bootstrap"):
        run_hmc_windowed_mass_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=_geometry(),
            bootstrap=bootstrap,
            config=_stage_config(),
            run_full_chain=lambda *_args: _fake_result(),
        )


def test_windowed_mass_stage_validates_adapter_and_mass_signatures() -> None:
    with pytest.raises(ValueError, match="adapter signature"):
        run_hmc_windowed_mass_stage(
            adapter=_MismatchedAdapter(),
            geometry=_geometry(),
            bootstrap=_bootstrap(),
            config=_stage_config(),
            run_full_chain=lambda *_args: _fake_result(),
        )

    geometry = _geometry()
    bad_mass = PrecomputedMassArtifact.from_covariance(
        position=np.zeros(2),
        covariance=2.0 * np.eye(2),
        adapter_signature=geometry.adapter_signature,
        position_role="initial_position",
        covariance_source="unit_test_bad_mass",
        source="unit_test_bad_mass",
        jitter=0.0,
    )
    bad_geometry = replace(geometry, mass_artifact=bad_mass)
    with pytest.raises(ValueError, match="mass artifact signature"):
        run_hmc_windowed_mass_stage(
            adapter=_ToyGaussianAdapter(),
            geometry=bad_geometry,
            bootstrap=_bootstrap(),
            config=_stage_config(),
            run_full_chain=lambda *_args: _fake_result(),
        )


@pytest.mark.parametrize(
    "fake_kwargs, expected_veto",
    [
        ({"runtime_s": np.nan}, "windowed_stage_runtime_missing_or_nonfinite"),
        ({"finite_samples": False}, "windowed_stage_warmup_draws_invalid"),
        ({"finite_log_accept": False}, "windowed_stage_log_accept_invalid"),
        ({"finite_target_log_prob": False}, "windowed_stage_target_log_prob_invalid"),
    ],
)
def test_windowed_mass_stage_hard_vetoes_invalid_retained_diagnostics(
    fake_kwargs: Mapping[str, Any],
    expected_veto: str,
) -> None:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        return _runtime_shaped_result(warmup_steps=int(config.num_results), **fake_kwargs)

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.passed is False
    assert result.final_status == "hard_veto"
    assert expected_veto in result.hard_vetoes
    assert result.windowed_mass_result is None


def test_windowed_mass_stage_hard_vetoes_missing_acceptance_trace() -> None:
    def run(_adapter: Any, _initial_state: Any, config: Any) -> _FakeRunResult:
        result = _fake_result(warmup_steps=int(config.num_results))
        trace = dict(result.trace)
        trace.pop("is_accepted")
        return replace(result, trace=trace)

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=_bootstrap(),
        config=_stage_config(),
        run_full_chain=run,
    )

    assert result.passed is False
    assert "windowed_stage_acceptance_telemetry_invalid_or_default" in result.hard_vetoes
    assert result.acceptance_telemetry_provenance["trace_key_present"] is False
    assert result.acceptance_telemetry_provenance["policy_filled_or_default"] is True


def test_real_tiny_gaussian_windowed_mass_stage_returns_structured_result() -> None:
    bootstrap = run_hmc_bootstrap_screen(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        config=None,
    )
    if not bootstrap.passed:
        pytest.skip(f"tiny bootstrap did not pass: {bootstrap.final_status}")

    result = run_hmc_windowed_mass_stage(
        adapter=_ToyGaussianAdapter(),
        geometry=_geometry(),
        bootstrap=bootstrap,
        config=_stage_config(chain_execution_mode="eager"),
    )

    assert result.final_status in {"passed", "hard_veto"}
    assert result.draw_capture_policy["num_results"] == 12
    assert result.payload()["reports_fixed_mass_step_tuning"] is False
    assert result.payload()["reports_trajectory_tuning"] is False
