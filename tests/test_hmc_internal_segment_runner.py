from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import inspect

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
from bayesfilter.inference import (
    InternalSegmentHMCRunnerConfig,
    ValueScoreCapability,
    build_internal_segment_hmc_runner,
)


class ReviewedBatchedGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "internal-segment-hmc-reviewed-batched-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_internal_segment_runner.py",
            target_scope="internal_segment_hmc_gaussian",
            nonclaims=("tiny internal-segment HMC engineering fixture only",),
            full_chain_xla_diagnostic_ready=True,
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


class TargetOnlyXLAGaussianAdapter(ReviewedBatchedGaussianAdapter):
    def adapter_signature(self) -> str:
        return "internal-segment-hmc-target-only-xla-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_internal_segment_runner.py",
            target_scope="internal_segment_hmc_target_only",
            nonclaims=("target-only XLA fixture; no full-chain XLA authority",),
        )


def _initial_state() -> tf.Tensor:
    return tf.constant(
        [[0.1, -0.2], [0.2, 0.1], [-0.1, 0.3]],
        dtype=tf.float64,
    )


def _config(*, use_xla: bool = False) -> InternalSegmentHMCRunnerConfig:
    return InternalSegmentHMCRunnerConfig(
        segment_count=3,
        segment_length=2,
        num_burnin_steps=1,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260624, 10),
        use_xla=use_xla,
        target_scope="internal_segment_hmc_gaussian",
        chain_execution_mode="tf_function",
    )


def test_internal_segment_runner_returns_summary_only_without_samples() -> None:
    runner = build_internal_segment_hmc_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False),
    )

    result = runner.run(seed=(20260624, 11))

    assert not hasattr(result, "samples")
    assert result.final_state.shape == (3, 2)
    assert result.final_target_log_prob.shape == (3,)
    assert result.segment_indices.shape == (3,)
    assert result.segment_target_log_prob.shape == (3, 3)
    np.testing.assert_array_equal(result.segment_indices.numpy(), np.asarray([2, 4, 6]))
    assert int(result.final_index.numpy()) == 6
    assert int(result.segment_index.numpy()) == 3
    assert bool(result.diagnostics["final_state_all_finite"].numpy())
    assert bool(result.diagnostics["final_target_log_prob_all_finite"].numpy())
    assert bool(result.diagnostics["segment_target_log_prob_all_finite"].numpy())
    assert bool(result.diagnostics["final_index_matches_total_transitions"].numpy())
    assert bool(result.diagnostics["segment_index_matches_segment_count"].numpy())
    assert bool(result.diagnostics["segment_indices_match_expected"].numpy())
    assert result.diagnostics["returns_samples"] is False
    assert result.metadata["runtime"] == (
        "tfp.mcmc.HamiltonianMonteCarlo.one_step_internal_segment_tf_while_loop"
    )
    assert result.metadata["uses_sample_chain"] is False
    assert result.metadata["returns_samples"] is False
    assert result.metadata["internal_segment_runner"] is True
    assert result.metadata["segment_count"] == 3
    assert result.metadata["segment_length"] == 2
    assert result.metadata["total_transitions"] == 6
    assert result.metadata["compile_trace_count"] == 1
    assert result.metadata["dynamic_inputs"] == ("current_state", "seed", "step_size")
    assert "summary-only mode returns no posterior samples" in result.metadata["nonclaims"]


def test_internal_segment_runner_xla_compiles_tiny_contract() -> None:
    runner = build_internal_segment_hmc_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=True),
    )

    result = runner.run(seed=(20260624, 12))

    assert result.metadata["jit_compile"] is True
    assert result.metadata["compile_trace_count"] == 1
    assert bool(result.diagnostics["final_index_matches_total_transitions"].numpy())
    assert bool(result.diagnostics["segment_indices_match_expected"].numpy())


def test_internal_segment_runner_rejects_invalid_contracts_and_inputs() -> None:
    with pytest.raises(ValueError, match="segment_count"):
        InternalSegmentHMCRunnerConfig(
            segment_count=0,
            segment_length=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
        )
    with pytest.raises(ValueError, match="output_mode"):
        InternalSegmentHMCRunnerConfig(
            segment_count=2,
            segment_length=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
            output_mode="samples",
        )
    with pytest.raises(ValueError, match="chain_execution_mode"):
        InternalSegmentHMCRunnerConfig(
            segment_count=2,
            segment_length=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
            use_xla=True,
            chain_execution_mode="eager",
        )

    runner = build_internal_segment_hmc_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False),
    )
    with pytest.raises(ValueError, match="current_state shape"):
        runner.run(current_state=tf.zeros((2, 2), dtype=tf.float64))
    with pytest.raises(ValueError, match="seed"):
        runner.run(seed=(1, 2, 3))
    with pytest.raises(ValueError, match="step_size"):
        runner.run(step_size=tf.ones((1,), dtype=tf.float64))


def test_internal_segment_runner_preserves_xla_authority_gate() -> None:
    config = InternalSegmentHMCRunnerConfig(
        segment_count=2,
        segment_length=2,
        num_burnin_steps=0,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260624, 13),
        use_xla=True,
        target_scope="internal_segment_hmc_target_only",
    )

    with pytest.raises(ValueError, match="target-only XLA readiness is not sufficient"):
        build_internal_segment_hmc_runner(
            TargetOnlyXLAGaussianAdapter(),
            _initial_state(),
            config,
        )


def test_internal_segment_runner_public_exports_and_no_sample_chain_dependency() -> None:
    import bayesfilter.inference.hmc as hmc_module

    assert bayesfilter.InternalSegmentHMCRunnerConfig is InternalSegmentHMCRunnerConfig
    assert bayesfilter.build_internal_segment_hmc_runner is build_internal_segment_hmc_runner
    assert "InternalSegmentHMCRunnerConfig" in bayesfilter.__all__
    assert "build_internal_segment_hmc_runner" in bayesfilter.__all__

    source = inspect.getsource(hmc_module.InternalSegmentHMCRunner)
    assert "tf.while_loop" in source
    assert "sample_chain(" not in source
