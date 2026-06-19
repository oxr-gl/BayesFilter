from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling.nystrom_transport_tf import (
    nystrom_transport_resample_tf,
)


DTYPE = tf.float64


def _fixture_batch() -> tuple[tf.Tensor, tf.Tensor]:
    particles = tf.constant(
        [
            [
                [-0.50, 0.10, 0.00],
                [-0.20, -0.15, 0.05],
                [0.00, 0.20, -0.10],
                [0.25, -0.05, 0.15],
                [0.55, 0.12, -0.02],
            ],
            [
                [-0.35, -0.20, 0.10],
                [-0.10, 0.05, -0.05],
                [0.12, 0.22, 0.08],
                [0.30, -0.12, -0.12],
                [0.62, 0.02, 0.18],
            ],
        ],
        dtype=DTYPE,
    )
    weights = tf.constant(
        [
            [0.10, 0.18, 0.22, 0.27, 0.23],
            [0.16, 0.14, 0.25, 0.20, 0.25],
        ],
        dtype=DTYPE,
    )
    return particles, weights


def _materialized_factor_plan(result) -> tf.Tensor:
    kernel = tf.einsum(
        "bnr,brs,bms->bnm",
        result.left_factor,
        result.core_matrix,
        result.left_factor,
    )
    return result.scaling_u[:, :, None] * kernel * result.scaling_v[:, None, :]


def test_independent_import_shape_and_reduced_rank_factors() -> None:
    particles, weights = _fixture_batch()

    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=100,
    )

    assert result.particles.shape == particles.shape
    assert result.transport_matrix.shape == (2, 0, 0)
    assert result.left_factor.shape == (2, 5, 2)
    assert result.core_matrix.shape == (2, 2, 2)
    assert result.scaling_u.shape == (2, 5)
    assert result.scaling_v.shape == (2, 5)
    assert result.diagnostics["transport_object_kind"] == "kernel_factors"
    assert result.diagnostics["source_route"] == "fixed_hmc_adaptation"
    assert result.diagnostics["orientation"] == "source_rows_target_columns"
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_factors"]


def test_reduced_rank_is_not_full_rank_replay() -> None:
    particles, weights = _fixture_batch()

    reduced = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=100,
    )
    full = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=5,
        epsilon=0.5,
        max_iterations=100,
    )

    assert reduced.diagnostics["rank"] == 2
    assert reduced.left_factor.shape[-1] == 2
    assert reduced.core_matrix.shape[-1] == 2
    assert reduced.landmark_indices.shape == (2,)
    assert full.diagnostics["rank"] == 5
    assert full.left_factor.shape[-1] == 5
    assert full.landmark_indices.shape == (5,)


def test_batch_shape_and_uniform_log_weights() -> None:
    particles, weights = _fixture_batch()

    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=3,
        epsilon=0.5,
        max_iterations=100,
    )

    assert result.particles.shape == (2, 5, 3)
    assert result.log_weights.shape == (2, 5)
    np.testing.assert_allclose(
        tf.reduce_logsumexp(result.log_weights, axis=1).numpy(),
        np.zeros(2),
        atol=1.0e-12,
    )


def test_materialized_orientation_reconstructs_transport() -> None:
    particles, weights = _fixture_batch()

    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=3,
        epsilon=0.5,
        max_iterations=100,
        convergence_threshold=1.0e-5,
    )
    plan = _materialized_factor_plan(result)
    reconstructed_particles = tf.einsum("bnm,bmd->bnd", plan, particles)
    row_mass = tf.reduce_sum(plan, axis=2)
    column_mass = tf.reduce_sum(plan, axis=1)
    column_target = weights * tf.cast(tf.shape(particles)[1], DTYPE)

    assert result.diagnostics["orientation"] == "source_rows_target_columns"
    np.testing.assert_allclose(
        reconstructed_particles.numpy(),
        result.particles.numpy(),
        atol=1.0e-10,
        rtol=1.0e-10,
    )
    np.testing.assert_allclose(row_mass.numpy(), np.ones((2, 5)), atol=5.0e-4)
    np.testing.assert_allclose(column_mass.numpy(), column_target.numpy(), atol=5.0e-4)


def test_invalid_inputs_do_not_return_valid_looking_results() -> None:
    particles, weights = _fixture_batch()
    log_weights = tf.math.log(weights)

    with pytest.raises(ValueError, match="rank must be positive"):
        nystrom_transport_resample_tf(particles, log_weights, rank=0)
    with pytest.raises(ValueError, match="epsilon must be positive"):
        nystrom_transport_resample_tf(particles, log_weights, rank=2, epsilon=0.0)
    with pytest.raises(ValueError, match="rank must be <= particle count"):
        nystrom_transport_resample_tf(particles, log_weights, rank=6)
    with pytest.raises(ValueError, match="particles and log_weights must agree"):
        nystrom_transport_resample_tf(particles, log_weights[:, :4], rank=2)

    nonfinite_particles = tf.tensor_scatter_nd_update(
        particles,
        indices=tf.constant([[0, 0, 0]], dtype=tf.int32),
        updates=tf.constant([float("nan")], dtype=DTYPE),
    )
    with pytest.raises((FloatingPointError, tf.errors.InvalidArgumentError, ValueError)):
        nystrom_transport_resample_tf(nonfinite_particles, log_weights, rank=2)
