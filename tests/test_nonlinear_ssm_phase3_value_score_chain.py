from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    ValueScoreCapability,
    static_unroll_chain_value_and_score,
)
from bayesfilter.testing import ModelBNonlinearSVDTarget


class ModelBReviewedValueScoreAdapter:
    parameter_dim = 3

    def __init__(self) -> None:
        self.target = ModelBNonlinearSVDTarget.default()

    def parameter_names(self) -> tuple[str, str, str]:
        return ("rho", "sigma", "beta")

    def adapter_signature(self) -> str:
        return "phase3-model-b-cut4-static-score-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_nonlinear_ssm_phase3_value_score_chain.py",
            target_scope="phase3_model_b_cut4_target_only",
            nonclaims=(
                "target-only value+score fixture",
                "not full-chain HMC evidence",
            ),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return self.target.target_log_prob_and_grad(theta)


def _chain_fixture() -> tf.Tensor:
    return tf.constant(
        [
            [0.70, 0.25, 0.80],
            [0.66, 0.23, 0.76],
            [0.74, 0.27, 0.84],
        ],
        dtype=tf.float64,
    )


def test_phase3_cpu_only_hides_gpu_before_tensorflow_runtime_probe() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []


def test_phase3_scalar_value_score_matches_eager_graph_and_xla() -> None:
    adapter = ModelBReviewedValueScoreAdapter()
    theta = adapter.target.initial_parameters
    eager_value, eager_score = adapter.log_prob_and_grad(theta)

    @tf.function(reduce_retracing=True)
    def graph(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return adapter.log_prob_and_grad(values)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return adapter.log_prob_and_grad(values)

    graph_value, graph_score = graph(theta)
    xla_value, xla_score = xla(theta)

    np.testing.assert_allclose(graph_value.numpy(), eager_value.numpy(), atol=1e-10)
    np.testing.assert_allclose(graph_score.numpy(), eager_score.numpy(), atol=1e-8)
    np.testing.assert_allclose(xla_value.numpy(), eager_value.numpy(), atol=1e-10)
    np.testing.assert_allclose(xla_score.numpy(), eager_score.numpy(), atol=1e-8)


def test_phase3_static_unroll_chain_value_score_matches_scalar_and_preserves_order() -> None:
    adapter = ModelBReviewedValueScoreAdapter()
    chain = _chain_fixture()
    expected_values = []
    expected_scores = []
    for index in range(int(chain.shape[0])):
        value, score = adapter.log_prob_and_grad(chain[index])
        expected_values.append(value)
        expected_scores.append(score)
    expected_value_tensor = tf.stack(expected_values, axis=0)
    expected_score_tensor = tf.stack(expected_scores, axis=0)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def xla_chain(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return static_unroll_chain_value_and_score(
            adapter,
            values,
            use_xla=True,
            target_scope="phase3_model_b_cut4_target_only",
        )

    chain_values, chain_scores = xla_chain(chain)

    np.testing.assert_allclose(
        chain_values.numpy(),
        expected_value_tensor.numpy(),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        chain_scores.numpy(),
        expected_score_tensor.numpy(),
        atol=1e-8,
    )
    permuted = tf.gather(chain, [2, 0, 1])
    permuted_values, permuted_scores = xla_chain(permuted)
    np.testing.assert_allclose(
        permuted_values.numpy(),
        tf.gather(expected_value_tensor, [2, 0, 1]).numpy(),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        permuted_scores.numpy(),
        tf.gather(expected_score_tensor, [2, 0, 1]).numpy(),
        atol=1e-8,
    )
    assert len(xla_chain._list_all_concrete_functions_for_serialization()) == 1


def test_phase3_static_unroll_chain_value_score_rejects_scope_mismatch() -> None:
    adapter = ModelBReviewedValueScoreAdapter()

    with pytest.raises(ValueError, match="target_scope mismatch"):
        static_unroll_chain_value_and_score(
            adapter,
            _chain_fixture(),
            use_xla=True,
            target_scope="wrong_scope",
        )


def test_phase3_static_unroll_chain_value_score_rejects_unknown_chain_dimension() -> None:
    adapter = ModelBReviewedValueScoreAdapter()
    chain = tf.TensorSpec([None, 3], dtype=tf.float64)

    @tf.function(input_signature=[chain], reduce_retracing=True)
    def graph(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return static_unroll_chain_value_and_score(
            adapter,
            values,
            use_xla=True,
            target_scope="phase3_model_b_cut4_target_only",
        )

    with pytest.raises(ValueError, match="static chain and parameter dimensions"):
        graph.get_concrete_function()


def test_phase3_static_unroll_chain_value_score_rejects_unknown_parameter_dimension() -> None:
    adapter = ModelBReviewedValueScoreAdapter()
    chain = tf.TensorSpec([3, None], dtype=tf.float64)

    @tf.function(input_signature=[chain], reduce_retracing=True)
    def graph(values: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return static_unroll_chain_value_and_score(
            adapter,
            values,
            use_xla=True,
            target_scope="phase3_model_b_cut4_target_only",
        )

    with pytest.raises(ValueError, match="static chain and parameter dimensions"):
        graph.get_concrete_function()
