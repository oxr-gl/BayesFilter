from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling import nystrom_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling.nystrom_transport_tf import (
    nystrom_transport_resample_tensors_tf,
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
    assert result.diagnostics["kernel_mode"] == "raw"
    assert result.diagnostics["scaling_normalization"] == "none"
    assert result.diagnostics["max_abs_log_scaling_gauge_shift"] == 0.0
    assert result.diagnostics["scaling_normalization_applications"] == 0.0
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


def test_nystrom_tensor_core_is_xla_compilable() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_resample() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        result = nystrom_transport_resample_tensors_tf(
            particles,
            tf.math.log(weights),
            rank=2,
            epsilon=0.5,
            max_iterations=20,
        )
        return (
            result.particles,
            result.log_weights,
            result.max_row_residual,
            result.max_column_residual,
        )

    resampled_particles, log_weights, row_residual, column_residual = compiled_resample()

    assert resampled_particles.shape == particles.shape
    np.testing.assert_allclose(
        tf.reduce_logsumexp(log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )
    assert np.isfinite(row_residual.numpy())
    assert np.isfinite(column_residual.numpy())


def test_nystrom_tensor_core_supports_truncated_svd_solver() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_resample() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        result = nystrom_transport_resample_tensors_tf(
            particles,
            tf.math.log(weights),
            rank=2,
            epsilon=0.5,
            max_iterations=20,
            core_solver="svd_truncated",
            core_rcond=1.0e-6,
        )
        return (
            result.particles,
            result.log_weights,
            result.finite_factors,
            result.finite_particles,
        )

    resampled_particles, log_weights, finite_factors, finite_particles = compiled_resample()

    assert resampled_particles.shape == particles.shape
    np.testing.assert_allclose(
        tf.reduce_logsumexp(log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )
    assert bool(finite_factors.numpy())
    assert bool(finite_particles.numpy())


def test_nystrom_tensor_core_svd_float32_uses_finite_core_metadata() -> None:
    old_dtype = nystrom_transport_tf.DTYPE
    old_default_dtype = nystrom_transport_tf.DEFAULT_DTYPE
    nystrom_transport_tf.DTYPE = tf.float32
    nystrom_transport_tf.DEFAULT_DTYPE = tf.float32
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=tf.float32,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=tf.float32)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_resample() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        result = nystrom_transport_resample_tensors_tf(
            particles,
            tf.math.log(weights),
            rank=2,
            epsilon=0.5,
            max_iterations=20,
            core_solver="svd_truncated",
            core_rcond=1.0e-6,
            diagnostics_enabled=True,
        )
        return (
            result.core_matrix,
            result.landmark_core_effective_rank,
            result.landmark_core_condition_proxy,
            result.finite_factors,
            result.finite_particles,
        )

    try:
        core_matrix, effective_rank, condition_proxy, finite_factors, finite_particles = compiled_resample()
    finally:
        nystrom_transport_tf.DTYPE = old_dtype
        nystrom_transport_tf.DEFAULT_DTYPE = old_default_dtype

    assert core_matrix.dtype == tf.float32
    assert np.all(np.isfinite(core_matrix.numpy()))
    assert np.isfinite(effective_rank.numpy())
    assert np.isfinite(condition_proxy.numpy())
    assert bool(finite_factors.numpy())
    assert bool(finite_particles.numpy())


def test_nystrom_tensor_core_supports_positive_projected_kernel_mode() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_resample() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        result = nystrom_transport_resample_tensors_tf(
            particles,
            tf.math.log(weights),
            rank=2,
            epsilon=0.5,
            max_iterations=20,
            kernel_mode="positive_projected",
            diagnostics_enabled=True,
        )
        return (
            result.particles,
            result.log_weights,
            result.finite_particles,
            result.projected_kernel_min,
            result.projection_floor_hits,
        )

    resampled_particles, log_weights, finite_particles, projected_min, floor_hits = compiled_resample()

    assert resampled_particles.shape == particles.shape
    np.testing.assert_allclose(
        tf.reduce_logsumexp(log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )
    assert bool(finite_particles.numpy())
    assert np.isfinite(projected_min.numpy())
    assert np.isfinite(floor_hits.numpy())


def test_nystrom_tensor_core_supports_balanced_scaling_normalization() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_resample() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        result = nystrom_transport_resample_tensors_tf(
            particles,
            tf.math.log(weights),
            rank=2,
            epsilon=0.5,
            max_iterations=20,
            scaling_normalization="balanced",
        )
        return (
            result.particles,
            result.log_weights,
            result.max_abs_log_scaling_gauge_shift,
            result.scaling_normalization_applications,
        )

    resampled_particles, log_weights, gauge_shift, applications = compiled_resample()

    assert resampled_particles.shape == particles.shape
    np.testing.assert_allclose(
        tf.reduce_logsumexp(log_weights, axis=1).numpy(),
        np.zeros([1]),
        atol=1.0e-12,
    )
    assert np.isfinite(gauge_shift.numpy())
    assert gauge_shift.numpy() > 0.0
    assert applications.numpy() > 0.0


def test_balanced_scaling_normalization_records_discriminating_shift() -> None:
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

    default_result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
    )
    balanced_result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
        scaling_normalization="balanced",
    )

    assert default_result.diagnostics["scaling_normalization"] == "none"
    assert default_result.diagnostics["max_abs_log_scaling_gauge_shift"] == 0.0
    assert default_result.diagnostics["scaling_normalization_applications"] == 0.0
    assert balanced_result.diagnostics["scaling_normalization"] == "balanced"
    assert balanced_result.diagnostics["max_abs_log_scaling_gauge_shift"] > 0.0
    assert balanced_result.diagnostics["scaling_normalization_applications"] > 0.0
    assert balanced_result.diagnostics["finite_particles"]
    assert balanced_result.diagnostics["finite_factors"]


def test_positive_projected_kernel_mode_records_discriminating_floor_hits() -> None:
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

    raw = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
        denominator_floor=0.25,
        diagnostics_enabled=True,
    )
    projected = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
        denominator_floor=0.25,
        kernel_mode="positive_projected",
        diagnostics_enabled=True,
    )

    assert raw.diagnostics["kernel_mode"] == "raw"
    assert projected.diagnostics["kernel_mode"] == "positive_projected"
    assert np.isnan(raw.diagnostics["raw_kernel_min"])
    assert projected.diagnostics["raw_kernel_min"] < 0.25
    assert projected.diagnostics["projected_kernel_min"] >= 0.25
    assert projected.diagnostics["projection_floor_hits"] > 0.0
    assert projected.diagnostics["finite_particles"]
    assert projected.diagnostics["finite_factors"]


def test_nystrom_python_result_records_core_solver() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
        core_solver="eigh_truncated",
        core_rcond=1.0e-5,
    )

    assert result.diagnostics["core_solver"] == "eigh_truncated"
    assert result.diagnostics["core_rcond"] == 1.0e-5
    assert result.diagnostics["kernel_mode"] == "raw"
    assert result.diagnostics["finite_factors"]
    assert result.diagnostics["finite_particles"]


def test_nystrom_diagnostics_are_opt_in_and_record_spectrum() -> None:
    particles = tf.constant(
        [[[-0.30, 0.10], [-0.10, -0.20], [0.20, 0.05], [0.45, 0.15]]],
        dtype=DTYPE,
    )
    weights = tf.constant([[0.10, 0.20, 0.30, 0.40]], dtype=DTYPE)

    default_result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
    )
    diagnostic_result = nystrom_transport_resample_tf(
        particles,
        tf.math.log(weights),
        rank=2,
        epsilon=0.5,
        max_iterations=20,
        diagnostics_enabled=True,
    )

    assert not default_result.diagnostics["diagnostics_enabled"]
    assert np.isnan(default_result.diagnostics["landmark_core_condition_proxy"])
    assert diagnostic_result.diagnostics["diagnostics_enabled"]
    assert np.isfinite(diagnostic_result.diagnostics["landmark_core_condition_proxy"])
    assert diagnostic_result.diagnostics["landmark_core_effective_rank"] > 0.0
    assert np.isfinite(diagnostic_result.diagnostics["min_factor_diagonal"])
    assert np.isfinite(diagnostic_result.diagnostics["max_factor_diagonal"])
