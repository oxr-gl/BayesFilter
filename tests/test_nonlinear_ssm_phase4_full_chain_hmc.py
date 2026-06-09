from __future__ import annotations

import inspect
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    FullChainHMCConfig,
    HMCTuningPolicy,
    ValueScoreCapability,
    run_gaussian_dual_averaging_diagnostic,
    run_full_chain_tfp_hmc,
)


class ReviewedGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "phase4-reviewed-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_nonlinear_ssm_phase4_full_chain_hmc.py",
            target_scope="phase4_reviewed_gaussian",
            nonclaims=("tiny full-chain HMC engineering fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values)), -values


class UnreviewedGaussianAdapter(ReviewedGaussianAdapter):
    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="gradient_tape_fallback",
            xla_hmc_ready=False,
            runtime_backend="tensorflow",
            nonclaims=("debug fallback only",),
        )


def _config(trace_policy: str = "standard") -> FullChainHMCConfig:
    return FullChainHMCConfig(
        num_results=4,
        num_burnin_steps=2,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260608, 4),
        use_xla=True,
        trace_policy=trace_policy,
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope="phase4_reviewed_gaussian",
    )


def test_phase4_cpu_only_hides_gpu_before_tensorflow_runtime_probe() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []


def test_phase4_tiny_full_chain_hmc_jit_returns_finite_samples_and_metadata() -> None:
    result = run_full_chain_tfp_hmc(
        ReviewedGaussianAdapter(),
        tf.constant([0.1, -0.2], dtype=tf.float64),
        _config(),
    )

    assert result.samples.shape == (4, 2)
    assert int(result.diagnostics["nonfinite_sample_count"].numpy()) == 0
    assert int(result.diagnostics["finite_sample_count"].numpy()) == 4
    assert np.isfinite(float(result.diagnostics["acceptance_rate"].numpy()))
    assert result.diagnostics["divergence_status"] == "unavailable"
    assert result.diagnostics["divergence_count"] is None
    assert set(result.trace) == {"is_accepted", "log_accept_ratio", "target_log_prob"}
    assert result.metadata["runtime"] == "tfp.mcmc.sample_chain"
    assert result.metadata["jit_compile"] is True
    assert result.metadata["trace_policy"] == "standard"
    assert result.metadata["adaptation_policy"] == "fixed_kernel_no_adaptation"
    assert result.metadata["trace_unavailability"] == {}
    assert result.metadata["value_score_authority"] == "graph_native"
    assert result.metadata["target_scope"] == "phase4_reviewed_gaussian"
    assert isinstance(result.metadata["program_signature"], str)
    assert result.metadata["first_call_s"] >= 0.0
    assert result.metadata["warm_call_s"] >= 0.0
    assert "no sampler convergence claim" in result.metadata["nonclaims"]


def test_phase4_xla_full_chain_hmc_fails_closed_without_reviewed_authority() -> None:
    with pytest.raises(ValueError, match="XLA full-chain HMC requires"):
        run_full_chain_tfp_hmc(
            UnreviewedGaussianAdapter(),
            tf.constant([0.1, -0.2], dtype=tf.float64),
            _config(),
        )


def test_phase4_xla_full_chain_hmc_rejects_target_scope_mismatch() -> None:
    config = FullChainHMCConfig(
        num_results=4,
        num_burnin_steps=2,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260608, 4),
        use_xla=True,
        trace_policy="standard",
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope="wrong_scope",
    )

    with pytest.raises(ValueError, match="target_scope mismatch"):
        run_full_chain_tfp_hmc(
            ReviewedGaussianAdapter(),
            tf.constant([0.1, -0.2], dtype=tf.float64),
            config,
        )


def test_phase4_reduced_trace_reports_unavailable_diagnostics_not_zero() -> None:
    result = run_full_chain_tfp_hmc(
        ReviewedGaussianAdapter(),
        tf.constant([0.1, -0.2], dtype=tf.float64),
        _config(trace_policy="reduced"),
    )

    assert set(result.trace) == {"trace_collected"}
    assert result.diagnostics["acceptance_rate"] is None
    assert result.diagnostics["divergence_status"] == "unavailable"
    assert result.diagnostics["divergence_count"] is None
    assert result.metadata["trace_unavailability"] == {
        "is_accepted": "reduced trace policy",
        "log_accept_ratio": "reduced trace policy",
        "target_log_prob": "reduced trace policy",
    }


def test_phase4_rejects_unreviewed_adaptation_policy() -> None:
    with pytest.raises(ValueError, match="fail-closed"):
        FullChainHMCConfig(
            num_results=4,
            num_burnin_steps=2,
            step_size=0.05,
            num_leapfrog_steps=2,
            seed=(20260608, 4),
            use_xla=True,
            trace_policy="standard",
            adaptation_policy="dual_averaging",
            target_scope="phase4_reviewed_gaussian",
        )


def test_phase4_reviewed_dual_averaging_policy_records_diagnostic_telemetry() -> None:
    policy = HMCTuningPolicy.dual_averaging_step_size(
        num_adaptation_steps=2,
        target_accept_prob=0.75,
        source="tests/test_nonlinear_ssm_phase4_full_chain_hmc.py",
    )
    config = FullChainHMCConfig(
        num_results=4,
        num_burnin_steps=2,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260608, 7),
        use_xla=False,
        trace_policy="standard",
        tuning_policy=policy,
        target_scope="phase4_reviewed_gaussian",
    )
    result = run_full_chain_tfp_hmc(
        ReviewedGaussianAdapter(),
        tf.constant([0.1, -0.2], dtype=tf.float64),
        config,
    )

    assert result.metadata["adaptation_policy"] == "dual_averaging_step_size"
    assert result.metadata["tuning_policy"]["label"] == "dual_averaging_step_size"
    assert result.metadata["tuning_policy"]["num_adaptation_steps"] == 2
    assert result.diagnostics["num_adaptation_steps"].numpy() == 2
    assert result.diagnostics["target_accept_prob"].numpy() == pytest.approx(0.75)
    assert np.all(np.isfinite(result.diagnostics["final_step_size"].numpy()))
    assert bool(result.diagnostics["final_step_size_finite"].numpy()) is True
    assert "step_size" in result.trace
    assert "no sampler convergence claim" in result.metadata["nonclaims"]


def test_phase4_gaussian_dual_averaging_diagnostic_records_nonclaims() -> None:
    policy = HMCTuningPolicy.fixed_mass_dual_averaging(
        num_adaptation_steps=2,
        target_accept_prob=0.75,
        source="tests/test_nonlinear_ssm_phase4_full_chain_hmc.py",
    )
    result = run_gaussian_dual_averaging_diagnostic(
        policy,
        initial_state=tf.constant([[0.1, -0.2], [0.2, 0.1]], dtype=tf.float64),
        num_results=4,
        num_burnin_steps=2,
        step_size=0.05,
        num_leapfrog_steps=2,
        seed=(20260609, 3),
    )

    assert result.policy.label == "fixed_mass_dual_averaging"
    assert result.diagnostics["num_adaptation_steps"] == 2
    assert result.diagnostics["target_accept_prob"] == pytest.approx(0.75)
    assert np.isfinite(result.diagnostics["final_step_size"])
    assert result.diagnostics["final_step_size_finite"] is True
    assert result.diagnostics["reports_posterior_convergence"] is False
    assert "step_size" in result.trace
    assert "no posterior convergence claim" in result.metadata["nonclaims"]


def test_phase4_compiled_sampling_source_does_not_materialize_numpy_inside_path() -> None:
    import bayesfilter.inference.hmc as hmc_module

    source = inspect.getsource(hmc_module.run_full_chain_tfp_hmc)
    source += inspect.getsource(hmc_module._make_tfp_target_log_prob_fn)
    source += inspect.getsource(hmc_module._build_sample_chain_runner)
    source += inspect.getsource(hmc_module._standard_trace_fn)
    source += inspect.getsource(hmc_module._reduced_trace_fn)
    source += inspect.getsource(ReviewedGaussianAdapter.log_prob_and_grad)

    assert ".numpy(" not in source
