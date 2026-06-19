from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling.nystrom_transport_tf import (
    nystrom_transport_resample_tf,
)


DTYPE = tf.float64


def test_nystrom_transport_returns_kernel_factors_and_uniform_weights() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)
    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=4,
        epsilon=0.5,
        max_iterations=80,
    )

    assert result.particles.shape == particles.shape
    assert result.transport_matrix.shape == (1, 0, 0)
    assert result.left_factor.shape == (1, 4, 4)
    assert result.core_matrix.shape == (1, 4, 4)
    assert result.scaling_u.shape == (1, 4)
    assert result.scaling_v.shape == (1, 4)
    assert result.diagnostics["transport_object_kind"] == "kernel_factors"
    assert result.diagnostics["source_route"] == "fixed_hmc_adaptation"
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_factors"]
    np.testing.assert_allclose(
        tf.reduce_logsumexp(result.log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )


def test_nystrom_transport_supports_reduced_rank_kernel_factors() -> None:
    particles = tf.constant(
        [
            [
                [-0.40, 0.05, 0.10],
                [-0.20, -0.10, 0.00],
                [0.00, 0.15, -0.05],
                [0.15, -0.05, 0.20],
                [0.30, 0.10, -0.10],
                [0.45, -0.15, 0.05],
            ]
        ],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.08, 0.12, 0.18, 0.22, 0.17, 0.23]], dtype=DTYPE)

    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=100,
    )

    assert result.particles.shape == particles.shape
    assert result.left_factor.shape == (1, 6, 2)
    assert result.core_matrix.shape == (1, 2, 2)
    assert result.scaling_u.shape == (1, 6)
    assert result.scaling_v.shape == (1, 6)
    assert result.diagnostics["rank"] == 2
    assert result.diagnostics["landmark_indices"] == [0, 5]
    assert result.diagnostics["finite_particles"]
    assert result.diagnostics["finite_factors"]
    assert np.isfinite(result.diagnostics["max_row_residual"])
    assert np.isfinite(result.diagnostics["max_column_residual"])


def test_nystrom_transport_rejects_rank_above_particle_count() -> None:
    particles = tf.zeros([1, 3, 2], dtype=DTYPE)
    log_weights = tf.math.log(tf.ones([1, 3], dtype=DTYPE) / 3.0)

    try:
        nystrom_transport_resample_tf(particles, log_weights, rank=4)
    except ValueError as exc:
        assert "rank must be <= particle count" in str(exc)
    else:
        raise AssertionError("rank above particle count should fail")
