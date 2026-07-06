from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import pytest
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_solver_resample_tf,
)


DTYPE = tf.float64


def _fixture() -> tuple[tf.Tensor, tf.Tensor]:
    particles = tf.constant(
        [
            [
                [-0.40, 0.10, 0.00],
                [-0.15, -0.20, 0.05],
                [0.10, 0.18, -0.10],
                [0.35, -0.02, 0.15],
                [0.60, 0.12, -0.05],
            ],
            [
                [-0.35, -0.15, 0.12],
                [-0.08, 0.02, -0.02],
                [0.16, 0.24, 0.05],
                [0.42, -0.10, -0.12],
                [0.68, 0.04, 0.18],
            ],
        ],
        dtype=DTYPE,
    )
    weights = tf.constant(
        [
            [0.10, 0.16, 0.22, 0.25, 0.27],
            [0.15, 0.18, 0.20, 0.22, 0.25],
        ],
        dtype=DTYPE,
    )
    return particles, weights


def test_solver_route_returns_valid_low_rank_factors() -> None:
    particles, weights = _fixture()
    result = low_rank_coupling_solver_resample_tf(
        particles,
        tf.math.log(weights),
        rank=3,
        assignment_epsilon=0.45,
    )

    assert result.particles.shape == particles.shape
    assert result.transport_matrix.shape == (2, 0, 0)
    assert result.q_factor.shape == (2, 5, 3)
    assert result.r_factor.shape == (2, 5, 3)
    assert result.g_weights.shape == (2, 3)
    assert result.diagnostics["transport_object_kind"] == "low_rank_coupling_factors"
    assert result.diagnostics["semantic_class"] == "semantic_replacement"
    assert result.diagnostics["implementation_scope"] == "solver_route_dykstra_projection_diagnostic"
    assert result.diagnostics["source_route"] == "extension_or_invention"
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_factors"]
    assert result.diagnostics["nonnegative_factors"]
    assert result.diagnostics["positive_g"]
    assert result.diagnostics["max_factor_marginal_residual"] <= 5.0e-3
    assert result.diagnostics["max_induced_row_residual"] <= 5.0e-3
    assert result.diagnostics["max_induced_column_residual"] <= 5.0e-3


def test_materialized_tiny_plan_matches_lazy_apply_and_marginals() -> None:
    particles, weights = _fixture()
    result = low_rank_coupling_solver_resample_tf(
        particles,
        tf.math.log(weights),
        rank=3,
        assignment_epsilon=0.45,
    )
    matrix = low_rank_coupling_scaled_matrix_tf(result.q_factor, result.r_factor, result.g_weights)
    reconstructed = tf.linalg.matmul(matrix, particles)

    tf.debugging.assert_near(reconstructed, result.particles, atol=1.0e-10, rtol=1.0e-10)
    tf.debugging.assert_near(tf.reduce_sum(matrix, axis=2), tf.ones((2, 5), dtype=DTYPE), atol=5.0e-3)
    tf.debugging.assert_near(tf.reduce_sum(matrix, axis=1), weights * 5.0, atol=5.0e-3)
    tf.debugging.assert_near(
        tf.reduce_logsumexp(result.log_weights, axis=1),
        tf.zeros(2, dtype=DTYPE),
        atol=1.0e-12,
    )


def test_solver_route_rejects_invalid_inputs() -> None:
    particles, weights = _fixture()
    log_weights = tf.math.log(weights)

    with pytest.raises(ValueError, match="rank must be positive"):
        low_rank_coupling_solver_resample_tf(particles, log_weights, rank=0)
    with pytest.raises(ValueError, match="rank must be <= particle count"):
        low_rank_coupling_solver_resample_tf(particles, log_weights, rank=6)
    with pytest.raises(ValueError, match="alpha must be smaller than 1/rank"):
        low_rank_coupling_solver_resample_tf(particles, log_weights, rank=3, alpha=0.5)
    with pytest.raises(ValueError, match="particles and log_weights must agree"):
        low_rank_coupling_solver_resample_tf(particles, log_weights[:, :4], rank=3)
