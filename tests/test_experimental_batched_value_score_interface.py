from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
import bayesfilter.linear
import bayesfilter.nonlinear
from bayesfilter.experimental_batched_value_score import (
    experimental_batched_kalman_value_score,
    experimental_batched_svd_sigma_point_value_score,
    experimental_scalar_callback_fallback_value_score,
)
from bayesfilter.linear.experimental_batched_kalman_tf import (
    tf_batched_kalman_value_and_score,
)
from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    tf_batched_svd_sigma_point_value_and_score,
)
from tests.test_experimental_batched_linear_kalman_tf import (
    _batch_model_and_derivatives,
    _observations,
    _theta_batch,
)
from tests.test_experimental_batched_svd_sigma_point_nonlinear_tf import (
    _batched_model_and_derivatives,
    _batched_value_and_score,
    _scalar_rows,
    _theta_batch as _nonlinear_theta_batch,
)


def test_experimental_interface_kalman_wrapper_matches_kernel() -> None:
    model_batch, derivative_batch = _batch_model_and_derivatives(_theta_batch())
    wrapped = experimental_batched_kalman_value_score(
        _observations(),
        jitter=tf.constant(1.0e-9, dtype=tf.float64),
        **model_batch,
        **derivative_batch,
    )
    raw_value, raw_score = tf_batched_kalman_value_and_score(
        _observations(),
        jitter=tf.constant(1.0e-9, dtype=tf.float64),
        **model_batch,
        **derivative_batch,
    )

    np.testing.assert_allclose(wrapped.value.numpy(), raw_value.numpy(), atol=1.0e-10)
    np.testing.assert_allclose(wrapped.score.numpy(), raw_score.numpy(), atol=1.0e-10)
    assert wrapped.value.shape == raw_value.shape == (3,)
    assert wrapped.score.shape == raw_score.shape == (3, 2)
    assert wrapped.metadata.backend == "tf_batched_kalman"
    assert wrapped.metadata.experimental is True
    assert wrapped.metadata.scalar_fallback_used is False
    assert "no production default readiness claim" in wrapped.metadata.nonclaims


def test_experimental_interface_svd_wrapper_matches_nonlinear_kernel() -> None:
    theta_batch = _nonlinear_theta_batch()
    model, derivatives = _batched_model_and_derivatives(theta_batch)
    wrapped = experimental_batched_svd_sigma_point_value_score(
        tf.constant([[0.10], [0.04], [0.16]], dtype=tf.float64),
        model,
        derivatives,
        backend="tf_svd_ukf",
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(1.0e-8, dtype=tf.float64),
    )
    raw_value, raw_score, _diagnostics = tf_batched_svd_sigma_point_value_and_score(
        tf.constant([[0.10], [0.04], [0.16]], dtype=tf.float64),
        model,
        derivatives,
        backend="tf_svd_ukf",
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(1.0e-8, dtype=tf.float64),
    )

    np.testing.assert_allclose(wrapped.value.numpy(), raw_value.numpy(), atol=1.0e-8)
    np.testing.assert_allclose(wrapped.score.numpy(), raw_score.numpy(), atol=1.0e-7)
    assert wrapped.value.shape == raw_value.shape == (2,)
    assert wrapped.score.shape == raw_score.shape == (2, 3)
    assert wrapped.metadata.backend == "tf_svd_ukf"
    assert wrapped.metadata.experimental is True
    assert wrapped.metadata.scalar_fallback_used is False
    assert "no production default readiness claim" in wrapped.metadata.nonclaims


def test_experimental_interface_svd_wrapper_rejects_cut4_default_scope() -> None:
    theta_batch = _nonlinear_theta_batch()
    model, derivatives = _batched_model_and_derivatives(theta_batch)

    with pytest.raises(ValueError, match="unsupported experimental batched SVD backend"):
        experimental_batched_svd_sigma_point_value_score(
            tf.constant([[0.10], [0.04], [0.16]], dtype=tf.float64),
            model,
            derivatives,
            backend="tf_svd_cut4",
        )


def test_experimental_scalar_callback_fallback_preserves_values_scores_and_order() -> None:
    theta_batch = _nonlinear_theta_batch()
    calls = []

    def scalar_callback(theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        calls.append(theta.numpy().tolist())
        value, score = _scalar_rows(theta[tf.newaxis, :], backend="tf_svd_ukf")
        return value[0], score[0]

    result = experimental_scalar_callback_fallback_value_score(
        theta_batch,
        scalar_callback,
        backend="tf_svd_ukf_scalar_callback",
    )
    expected_value, expected_score = _scalar_rows(theta_batch, backend="tf_svd_ukf")

    assert calls == theta_batch.numpy().tolist()
    np.testing.assert_allclose(result.value.numpy(), expected_value.numpy(), atol=1.0e-8)
    np.testing.assert_allclose(result.score.numpy(), expected_score.numpy(), atol=1.0e-7)
    assert result.value.shape == (2,)
    assert result.score.shape == (2, 3)
    assert result.metadata.scalar_fallback_used is True
    assert result.metadata.backend == "tf_svd_ukf_scalar_callback"


def test_experimental_scalar_callback_fallback_requires_batched_theta() -> None:
    with pytest.raises(ValueError, match="theta_batch must have rank 2"):
        experimental_scalar_callback_fallback_value_score(
            tf.constant([0.70, 0.25, 0.80], dtype=tf.float64),
            lambda theta: (tf.reduce_sum(theta), theta),
        )


def test_experimental_interface_is_not_reexported_from_public_packages() -> None:
    assert "experimental_batched_value_score" not in bayesfilter.__all__
    assert "experimental_batched_value_score" not in bayesfilter.linear.__all__
    assert "experimental_batched_value_score" not in bayesfilter.nonlinear.__all__
    assert "experimental_batched_value_score" not in bayesfilter._EXPORT_MODULES
    assert "experimental_batched_value_score" not in bayesfilter.linear._EXPORT_MODULES
    assert "experimental_batched_value_score" not in bayesfilter.nonlinear._EXPORT_MODULES


def test_experimental_interface_cpu_only_hides_gpu() -> None:
    assert os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
    assert tf.config.list_physical_devices("GPU") == []
