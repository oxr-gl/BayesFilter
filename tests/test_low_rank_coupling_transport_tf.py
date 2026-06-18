from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_transport_tf import (
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_transport_resample_tf,
)


DTYPE = tf.float64


def test_low_rank_coupling_transport_returns_factors_and_particles() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)
    result = low_rank_coupling_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        assignment_epsilon=0.5,
        max_iterations=200,
    )

    assert result.particles.shape == particles.shape
    assert result.transport_matrix.shape == (1, 0, 0)
    assert result.q_factor.shape == (1, 4, 2)
    assert result.r_factor.shape == (1, 4, 2)
    assert result.g_weights.shape == (1, 2)
    assert result.diagnostics["transport_object_kind"] == "low_rank_coupling_factors"
    assert result.diagnostics["semantic_class"] == "semantic_replacement"
    assert result.diagnostics["implementation_scope"] == "transport_object_fixture_route"
    assert result.diagnostics["source_route"] == "extension_or_invention"
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_factors"]
    assert result.diagnostics["nonnegative_factors"]
    assert result.diagnostics["positive_g"]
    assert result.diagnostics["max_factor_marginal_residual"] < 1.0e-4
    assert result.diagnostics["max_induced_row_residual"] < 1.0e-4
    assert result.diagnostics["max_induced_column_residual"] < 1.0e-4

    matrix = low_rank_coupling_scaled_matrix_tf(
        result.q_factor,
        result.r_factor,
        result.g_weights,
    )
    np.testing.assert_allclose(
        tf.reduce_sum(matrix, axis=2).numpy(),
        np.ones([1, 4]),
        atol=1.0e-4,
    )
    np.testing.assert_allclose(
        tf.reduce_sum(matrix, axis=1).numpy(),
        (weights * 4.0).numpy(),
        atol=1.0e-4,
    )
    np.testing.assert_allclose(
        tf.reduce_logsumexp(result.log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )


def test_low_rank_coupling_transport_rejects_rank_above_particle_count() -> None:
    particles = tf.zeros([1, 3, 2], dtype=DTYPE)
    log_weights = tf.math.log(tf.ones([1, 3], dtype=DTYPE) / 3.0)

    try:
        low_rank_coupling_transport_resample_tf(particles, log_weights, rank=4)
    except ValueError as exc:
        assert "rank must be <= particle count" in str(exc)
    else:
        raise AssertionError("rank above particle count should fail")
