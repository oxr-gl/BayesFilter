from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import inspect

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
from bayesfilter.inference import (
    FixedSizeHMCChunkConfig,
    ValueScoreCapability,
    build_fixed_size_hmc_chunk_runner,
)


class ReviewedBatchedGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "fixed-size-hmc-chunk-reviewed-batched-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_fixed_size_chunk_runner.py",
            target_scope="fixed_size_hmc_chunk_gaussian",
            nonclaims=("tiny fixed-size HMC chunk engineering fixture only",),
            full_chain_xla_diagnostic_ready=True,
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


class TargetOnlyXLAGaussianAdapter(ReviewedBatchedGaussianAdapter):
    def adapter_signature(self) -> str:
        return "fixed-size-hmc-chunk-target-only-xla-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_fixed_size_chunk_runner.py",
            target_scope="fixed_size_hmc_chunk_target_only",
            nonclaims=("target-only XLA fixture; no full-chain XLA authority",),
        )


def _initial_state() -> tf.Tensor:
    return tf.constant(
        [[0.1, -0.2], [0.2, 0.1], [-0.1, 0.3]],
        dtype=tf.float64,
    )


def _config(*, use_xla: bool = False, max_results: int = 5) -> FixedSizeHMCChunkConfig:
    return FixedSizeHMCChunkConfig(
        max_results=max_results,
        num_burnin_steps=1,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260622, 10),
        use_xla=use_xla,
        target_scope="fixed_size_hmc_chunk_gaussian",
        chain_execution_mode="tf_function",
    )


def test_fixed_size_chunk_runner_changes_active_count_without_retrace() -> None:
    runner = build_fixed_size_hmc_chunk_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False, max_results=5),
    )

    first = runner.run(active_results=2, seed=(20260622, 11))
    second = runner.run(
        active_results=4,
        current_state=first.final_state,
        seed=(20260622, 12),
    )

    assert first.samples.shape == (5, 3, 2)
    assert second.samples.shape == (5, 3, 2)
    assert first.valid_mask.shape == (5,)
    assert second.valid_mask.shape == (5,)
    np.testing.assert_array_equal(
        first.valid_mask.numpy(),
        np.asarray([True, True, False, False, False]),
    )
    np.testing.assert_array_equal(
        second.valid_mask.numpy(),
        np.asarray([True, True, True, True, False]),
    )
    assert first.final_state.shape == (3, 2)
    assert second.final_state.shape == (3, 2)
    assert not np.allclose(first.final_state.numpy(), second.final_state.numpy())
    assert int(first.diagnostics["valid_sample_count"].numpy()) == 2
    assert int(first.diagnostics["invalid_sample_count"].numpy()) == 3
    assert int(second.diagnostics["valid_sample_count"].numpy()) == 4
    assert int(second.diagnostics["invalid_sample_count"].numpy()) == 1
    assert int(first.diagnostics["nonfinite_valid_sample_count"].numpy()) == 0
    assert int(second.diagnostics["nonfinite_valid_sample_count"].numpy()) == 0
    assert first.metadata["runtime"] == "tfp.mcmc.HamiltonianMonteCarlo.one_step_tf_while_loop"
    assert first.metadata["uses_sample_chain"] is False
    assert second.metadata["fixed_size_chunk_runner"] is True
    assert second.metadata["max_results"] == 5
    assert second.metadata["active_results"] == 4
    assert second.metadata["chunk_invocation_count"] == 2
    assert first.metadata["compile_trace_count"] == 1
    assert second.metadata["compile_trace_count"] == 1
    assert second.metadata["first_call_s"] == first.metadata["first_call_s"]
    assert second.metadata["warm_call_s"] >= 0.0
    assert second.metadata["dynamic_inputs"] == (
        "current_state",
        "seed",
        "step_size",
        "active_results",
    )
    assert "no sampler convergence claim" in second.metadata["nonclaims"]


def test_fixed_size_chunk_runner_xla_compiles_tiny_contract() -> None:
    runner = build_fixed_size_hmc_chunk_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=True, max_results=2),
    )

    result = runner.run(active_results=1, seed=(20260622, 13))

    assert result.samples.shape == (2, 3, 2)
    assert int(result.diagnostics["valid_sample_count"].numpy()) == 1
    assert int(result.diagnostics["nonfinite_valid_sample_count"].numpy()) == 0
    assert result.metadata["jit_compile"] is True
    assert result.metadata["compile_trace_count"] == 1


def test_fixed_size_chunk_runner_rejects_invalid_contracts_and_inputs() -> None:
    with pytest.raises(ValueError, match="max_results"):
        FixedSizeHMCChunkConfig(
            max_results=0,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
        )
    with pytest.raises(ValueError, match="reduced trace"):
        FixedSizeHMCChunkConfig(
            max_results=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
            trace_policy="standard",
        )
    with pytest.raises(ValueError, match="chain_execution_mode"):
        FixedSizeHMCChunkConfig(
            max_results=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
            use_xla=True,
            chain_execution_mode="eager",
        )

    runner = build_fixed_size_hmc_chunk_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False, max_results=2),
    )
    with pytest.raises(ValueError, match="current_state shape"):
        runner.run(active_results=1, current_state=tf.zeros((2, 2), dtype=tf.float64))
    with pytest.raises(ValueError, match="seed"):
        runner.run(active_results=1, seed=(1, 2, 3))
    with pytest.raises(ValueError, match="step_size"):
        runner.run(active_results=1, step_size=tf.ones((1,), dtype=tf.float64))
    with pytest.raises(ValueError, match="active_results"):
        runner.run(active_results=3)


def test_fixed_size_chunk_runner_preserves_xla_authority_gate() -> None:
    config = FixedSizeHMCChunkConfig(
        max_results=2,
        num_burnin_steps=0,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260622, 14),
        use_xla=True,
        target_scope="fixed_size_hmc_chunk_target_only",
    )

    with pytest.raises(ValueError, match="target-only XLA readiness is not sufficient"):
        build_fixed_size_hmc_chunk_runner(
            TargetOnlyXLAGaussianAdapter(),
            _initial_state(),
            config,
        )


def test_fixed_size_chunk_runner_public_exports_and_no_sample_chain_dependency() -> None:
    import bayesfilter.inference.hmc as hmc_module

    assert bayesfilter.FixedSizeHMCChunkConfig is FixedSizeHMCChunkConfig
    assert bayesfilter.build_fixed_size_hmc_chunk_runner is build_fixed_size_hmc_chunk_runner
    assert "FixedSizeHMCChunkConfig" in bayesfilter.__all__
    assert "build_fixed_size_hmc_chunk_runner" in bayesfilter.__all__

    source = inspect.getsource(hmc_module.FixedSizeHMCChunkRunner)
    assert "tf.while_loop" in source
    assert "sample_chain(" not in source
