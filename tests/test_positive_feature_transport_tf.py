from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling.positive_feature_transport_tf import (
    positive_feature_transport_resample_tf,
)


DTYPE = tf.float64


def test_positive_feature_transport_returns_factors_and_semantic_replacement() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)
    result = positive_feature_transport_resample_tf(
        particles,
        tf.math.log(weights),
        num_features=8,
        epsilon=0.5,
        max_iterations=120,
    )

    assert result.particles.shape == particles.shape
    assert result.transport_matrix.shape == (1, 0, 0)
    assert result.left_features.shape == (1, 4, 8)
    assert result.right_features.shape == (1, 4, 8)
    assert result.scaling_u.shape == (1, 4)
    assert result.scaling_v.shape == (1, 4)
    assert result.diagnostics["transport_object_kind"] == "kernel_factors"
    assert result.diagnostics["semantic_class"] == "semantic_replacement"
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_features"]
    assert result.diagnostics["positive_features"]
    np.testing.assert_allclose(
        tf.reduce_logsumexp(result.log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )


def test_positive_feature_transport_rejects_invalid_feature_count() -> None:
    particles = tf.zeros([1, 3, 2], dtype=DTYPE)
    log_weights = tf.math.log(tf.ones([1, 3], dtype=DTYPE) / 3.0)

    try:
        positive_feature_transport_resample_tf(particles, log_weights, num_features=0)
    except ValueError as exc:
        assert "num_features must be positive" in str(exc)
    else:
        raise AssertionError("nonpositive feature count should fail")
