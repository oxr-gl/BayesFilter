from __future__ import annotations

import ast
import inspect
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.inference import (
    LatentAffineBatchValueScoreAdapter,
    LatentAffineHMCTransform,
    ValueScoreCapability,
    evaluate_batch_native_value_score,
    reviewed_value_score_target_fn,
)
from bayesfilter.inference import batched_value_score as batched_value_score_module


class BatchedQuadraticAdapter:
    parameter_dim = 3

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow_batched_quadratic_fixture",
            evidence_path="tests/test_batched_value_score.py",
            target_scope="batched_quadratic_fixture",
            nonclaims=("target value/score fixture only",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


class ScalarOnlyQuadraticAdapter(BatchedQuadraticAdapter):
    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values)), -values


class CountingBatchedQuadraticAdapter(BatchedQuadraticAdapter):
    def __init__(self) -> None:
        self.calls = 0

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        self.calls += 1
        return super().log_prob_and_grad(theta)


class Float32OutputBatchedQuadraticAdapter(BatchedQuadraticAdapter):
    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.cast(tf.convert_to_tensor(theta), tf.float32)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


def _theta_batch() -> tf.Tensor:
    return tf.constant(
        [[0.1, -0.2, 0.3], [0.4, 0.0, -0.1], [-0.25, 0.15, 0.05]],
        dtype=tf.float64,
    )


def test_evaluate_batch_native_value_score_returns_shape_metadata_and_nonclaims() -> None:
    adapter = BatchedQuadraticAdapter()
    theta = _theta_batch()

    result = evaluate_batch_native_value_score(adapter, theta)

    expected_value = -0.5 * np.sum(np.square(theta.numpy()), axis=-1)
    np.testing.assert_allclose(result.value.numpy(), expected_value)
    np.testing.assert_allclose(result.score.numpy(), -theta.numpy())
    assert result.metadata.rank == "batch"
    assert result.metadata.batch_size == 3
    assert result.metadata.parameter_dim == 3
    assert result.metadata.value_score_authority == "graph_native"
    assert result.metadata.target_scope == "batched_quadratic_fixture"
    assert "no HMC tuning or sampling claim" in result.metadata.nonclaims
    assert result.diagnostics["path"] == "batch_native_adapter_log_prob_and_grad"
    assert result.diagnostics["accepted_target_xla_authority"] is True
    assert result.diagnostics["full_chain_xla_diagnostic_ready"] is False


def test_reviewed_value_score_target_custom_gradient_matches_adapter_score() -> None:
    theta = _theta_batch()
    target = reviewed_value_score_target_fn(BatchedQuadraticAdapter(), require_batched=True)

    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = target(theta)
    gradient = tape.gradient(value, theta)

    np.testing.assert_allclose(value.numpy(), -0.5 * np.sum(np.square(theta.numpy()), axis=-1))
    np.testing.assert_allclose(gradient.numpy(), -theta.numpy())


def test_reviewed_value_score_target_casts_adapter_outputs_to_hmc_dtype() -> None:
    theta = _theta_batch()
    target = reviewed_value_score_target_fn(
        Float32OutputBatchedQuadraticAdapter(),
        dtype=tf.float64,
        require_batched=True,
    )

    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = target(theta)
    gradient = tape.gradient(value, theta)

    assert value.dtype == tf.float64
    assert gradient.dtype == tf.float64
    expected_value = -0.5 * np.sum(np.square(theta.numpy().astype(np.float32)), axis=-1)
    np.testing.assert_allclose(value.numpy(), expected_value, rtol=1.0e-6, atol=1.0e-6)
    np.testing.assert_allclose(gradient.numpy(), -theta.numpy(), rtol=1.0e-6, atol=1.0e-6)


def test_batch_native_rowwise_parity_against_scalar_fixture() -> None:
    adapter = BatchedQuadraticAdapter()
    theta = _theta_batch()
    batched = evaluate_batch_native_value_score(adapter, theta)

    scalar_values = []
    scalar_scores = []
    for row in tf.unstack(theta, axis=0):
        value, score = adapter.log_prob_and_grad(row)
        scalar_values.append(value)
        scalar_scores.append(score)

    np.testing.assert_allclose(batched.value.numpy(), tf.stack(scalar_values).numpy())
    np.testing.assert_allclose(batched.score.numpy(), tf.stack(scalar_scores).numpy())


def test_latent_affine_batch_value_score_adapter_calls_base_once_and_applies_chain_rule() -> None:
    base = CountingBatchedQuadraticAdapter()
    center = np.array([0.25, -0.5, 0.75])
    factor = np.array(
        [
            [2.0, 0.1, 0.0],
            [0.0, 1.5, -0.2],
            [0.3, 0.0, 1.25],
        ]
    )
    transform = LatentAffineHMCTransform(
        center=center,
        factor=factor,
        covariance_provenance="unit_test_covariance",
    )
    adapter = LatentAffineBatchValueScoreAdapter(
        base_adapter=base,
        transform=transform,
        target_scope="latent_affine_batch_fixture",
    )
    z = _theta_batch()

    value, score = adapter.log_prob_and_grad(z)
    theta = center + z.numpy() @ factor.T

    assert base.calls == 1
    np.testing.assert_allclose(value.numpy(), -0.5 * np.sum(theta * theta, axis=-1))
    np.testing.assert_allclose(score.numpy(), (-theta) @ factor)
    assert value.shape == (3,)
    assert score.shape == (3, 3)


def test_batch_native_target_tf_function_reuses_concrete_function() -> None:
    theta = _theta_batch()
    target = reviewed_value_score_target_fn(BatchedQuadraticAdapter(), require_batched=True)

    @tf.function(
        input_signature=[tf.TensorSpec(shape=(3, 3), dtype=tf.float64)],
        reduce_retracing=True,
    )
    def compiled_target(x: tf.Tensor) -> tf.Tensor:
        return target(x)

    first = compiled_target(theta)
    second = compiled_target(tf.identity(theta))

    np.testing.assert_allclose(first.numpy(), second.numpy())
    assert len(compiled_target._list_all_concrete_functions_for_serialization()) == 1


def test_batch_native_target_cpu_xla_value_and_gradient_parity_is_scoped_fixture_only() -> None:
    theta = _theta_batch()
    target = reviewed_value_score_target_fn(BatchedQuadraticAdapter(), require_batched=True)

    @tf.function(
        input_signature=[tf.TensorSpec(shape=(3, 3), dtype=tf.float64)],
        jit_compile=True,
        reduce_retracing=True,
    )
    def compiled_value_and_gradient(x: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        with tf.GradientTape() as tape:
            tape.watch(x)
            value = target(x)
        gradient = tape.gradient(value, x)
        if gradient is None:
            raise ValueError("compiled target gradient is unavailable")
        return value, gradient

    eager_value = target(theta)
    eager_gradient = tf.convert_to_tensor(-theta, dtype=tf.float64)
    compiled_value, compiled_gradient = compiled_value_and_gradient(theta)

    np.testing.assert_allclose(compiled_value.numpy(), eager_value.numpy())
    np.testing.assert_allclose(compiled_gradient.numpy(), eager_gradient.numpy())
    assert len(compiled_value_and_gradient._list_all_concrete_functions_for_serialization()) == 1


def test_batch_native_helpers_fail_closed_for_scalar_only_adapter() -> None:
    theta = _theta_batch()
    adapter = ScalarOnlyQuadraticAdapter()

    with pytest.raises(ValueError, match="batched target value must have rank 1"):
        evaluate_batch_native_value_score(adapter, theta)

    target = reviewed_value_score_target_fn(adapter, require_batched=True)
    with pytest.raises(ValueError, match="batched target value must have rank 1"):
        target(theta)


def test_batch_native_helpers_reject_scalar_input_when_batch_required() -> None:
    adapter = BatchedQuadraticAdapter()
    theta = tf.constant([0.1, -0.2, 0.3], dtype=tf.float64)

    with pytest.raises(ValueError, match="rank 2 theta"):
        evaluate_batch_native_value_score(adapter, theta)

    target = reviewed_value_score_target_fn(adapter, require_batched=True)
    with pytest.raises(ValueError, match="rank 2 theta"):
        target(theta)


def test_batch_native_helper_source_has_no_python_row_loop_or_stack() -> None:
    for fn in (
        batched_value_score_module.evaluate_batch_native_value_score,
        batched_value_score_module.reviewed_value_score_target_fn,
    ):
        source = inspect.getsource(fn)
        tree = ast.parse(source)
        assert not any(isinstance(node, (ast.For, ast.AsyncFor)) for node in ast.walk(tree))
        assert not any(isinstance(node, ast.ListComp) for node in ast.walk(tree))
        assert not any(
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"append", "stack", "unstack", "map_fn", "vectorized_map"}
            for node in ast.walk(tree)
        )
        adapter_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "log_prob_and_grad"
        ]
        assert len(adapter_calls) == 1
