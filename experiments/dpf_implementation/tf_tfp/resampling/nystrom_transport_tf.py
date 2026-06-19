"""Experimental TensorFlow fixed-rank Nystrom annealed transport.

This module is experimental infrastructure for the scalable OT program.  It is
an experimental candidate path only; it does not change BayesFilter defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import tensorflow as tf


DEFAULT_DTYPE = tf.float64
DTYPE = DEFAULT_DTYPE


@dataclass(frozen=True)
class NystromTransportTFResult:
    particles: tf.Tensor
    log_weights: tf.Tensor
    transport_matrix: tf.Tensor
    left_factor: tf.Tensor
    core_matrix: tf.Tensor
    scaling_u: tf.Tensor
    scaling_v: tf.Tensor
    landmark_indices: tf.Tensor
    diagnostics: dict[str, Any]


def nystrom_transport_resample_tf(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    *,
    rank: int,
    epsilon: float = 0.5,
    max_iterations: int = 80,
    convergence_threshold: float = 1.0e-4,
    cholesky_jitter: float = 1.0e-8,
    denominator_floor: float = 1.0e-30,
) -> NystromTransportTFResult:
    """Apply a fixed-rank Nystrom kernel transport candidate.

    The source-faithful core is the Nystrom factorization
    ``K ~= V A^{-1} V^T`` and low-rank Sinkhorn scaling through these factors.
    The local FilterFlow scaling and deterministic landmark rule are Phase 4
    adapters, not paper-faithful adaptive-rank claims.
    """

    if rank <= 0:
        raise ValueError("rank must be positive")
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    if cholesky_jitter < 0.0:
        raise ValueError("cholesky_jitter must be non-negative")
    if denominator_floor <= 0.0:
        raise ValueError("denominator_floor must be positive")

    original_particle_rank = len(particles.shape)
    original_weight_rank = len(log_weights.shape)
    x = tf.cast(particles, DTYPE)
    logw = tf.cast(log_weights, DTYPE)
    if original_particle_rank == 2:
        x = x[None, :, :]
    if original_weight_rank == 1:
        logw = logw[None, :]
    if len(x.shape) != 3 or len(logw.shape) != 2:
        raise ValueError("particles must be [N,D] or [B,N,D]; log_weights must be [N] or [B,N]")
    if int(x.shape[1] or 0) and int(logw.shape[1] or 0) and x.shape[1] != logw.shape[1]:
        raise ValueError("particles and log_weights must agree on particle count")

    batch_size = tf.shape(x)[0]
    num_particles = tf.shape(x)[1]
    if int(x.shape[1] or 0) and rank > int(x.shape[1]):
        raise ValueError("rank must be <= particle count")
    if not int(x.shape[1] or 0):
        rank_tensor = tf.cast(rank, tf.int32)
        with tf.control_dependencies([
            tf.debugging.assert_less_equal(rank_tensor, num_particles, message="rank must be <= particle count")
        ]):
            x = tf.identity(x)

    centered = x - tf.stop_gradient(tf.reduce_mean(x, axis=1, keepdims=True))
    scale = _filterflow_scale(x)
    scaled_x = centered / tf.stop_gradient(scale[:, None, None])
    landmark_indices = _deterministic_landmark_indices(num_particles, rank)
    landmarks = tf.gather(scaled_x, landmark_indices, axis=1)
    left_factor, core_matrix, factor_diag = _nystrom_factors(
        scaled_x,
        landmarks,
        epsilon=tf.constant(epsilon, DTYPE),
        cholesky_jitter=tf.constant(cholesky_jitter, DTYPE),
    )
    source_weights = tf.exp(logw)
    float_n = tf.cast(num_particles, DTYPE)
    row_target = tf.ones([batch_size, num_particles], dtype=DTYPE)
    column_target = source_weights * float_n
    scaling_u, scaling_v, iterations_used, scale_diag = _sinkhorn_scale_factors(
        left_factor,
        core_matrix,
        row_target,
        column_target,
        max_iterations=max_iterations,
        convergence_threshold=tf.constant(convergence_threshold, DTYPE),
        denominator_floor=tf.constant(denominator_floor, DTYPE),
    )
    transported = scaling_u[:, :, None] * _factor_matmul(
        left_factor,
        core_matrix,
        scaling_v[:, :, None] * x,
    )
    row_mass = scaling_u * _factor_matvec(left_factor, core_matrix, scaling_v)
    column_mass = scaling_v * _factor_matvec(left_factor, core_matrix, scaling_u)
    row_residual = tf.reduce_max(tf.abs(row_mass - row_target))
    column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
    uniform_log = tf.fill(
        [batch_size, num_particles],
        -tf.math.log(float_n),
    )
    transport_matrix = tf.zeros([batch_size, 0, 0], dtype=DTYPE)
    finite_factors = (
        tf.reduce_all(tf.math.is_finite(left_factor))
        & tf.reduce_all(tf.math.is_finite(core_matrix))
        & tf.reduce_all(tf.math.is_finite(scaling_u))
        & tf.reduce_all(tf.math.is_finite(scaling_v))
    )
    finite_particles = tf.reduce_all(tf.math.is_finite(transported))
    diagnostics = {
        "component_id": "fixed_rank_nystrom_transport_tf",
        "mathematical_object": "approximate_kernel_nystrom_transport",
        "source_status": "source_locked",
        "semantic_class": "approximate_kernel",
        "source_route": "fixed_hmc_adaptation",
        "source_route_components": {
            "nystrom_factors": "source_faithful",
            "low_rank_scaling": "source_faithful",
            "filterflow_cost_scaling_adapter": "fixed_hmc_adaptation",
            "deterministic_landmarks": "fixed_hmc_adaptation",
            "cholesky_jitter": "fixed_hmc_adaptation",
        },
        "backend": "tensorflow",
        "transport_object_kind": "kernel_factors",
        "transport_matrix_materialized": False,
        "not_materialized_reason": "kernel_factors_nonmaterialized",
        "orientation": "source_rows_target_columns",
        "rank": int(rank),
        "landmark_rule": "deterministic_evenly_spaced_indices",
        "landmark_indices": [int(v) for v in landmark_indices.numpy().tolist()],
        "epsilon": float(epsilon),
        "eta_map": "eta=1/(2*epsilon) for exp(-0.5*||x-y||^2/epsilon)",
        "reg_sigma_map": "sigma=sqrt(epsilon) for POT exp(-dist/(2*sigma^2)) convention",
        "max_iterations": int(max_iterations),
        "iterations_used": int(iterations_used.numpy()),
        "convergence_threshold": float(convergence_threshold),
        "cholesky_jitter": float(cholesky_jitter),
        "denominator_floor": float(denominator_floor),
        "factor_shapes": {
            "V": left_factor.shape.as_list(),
            "A_inv": core_matrix.shape.as_list(),
            "scaling_u": scaling_u.shape.as_list(),
            "scaling_v": scaling_v.shape.as_list(),
        },
        "max_row_residual": _float(row_residual),
        "max_column_residual": _float(column_residual),
        "min_kernel_denominator": _float(scale_diag["min_denominator"]),
        "denominator_floor_hits": _float(scale_diag["floor_hits"]),
        "max_factor_diag_error": _float(factor_diag["max_diag_error"]),
        "min_factor_diagonal": _float(factor_diag["min_factor_diagonal"]),
        "finite_factors": bool(finite_factors.numpy()),
        "finite_particles": bool(finite_particles.numpy()),
        "nonclaims": [
            "experimental scalable OT candidate only",
            "no speedup claim",
            "no ranking claim",
            "no production default change",
            "no posterior correctness claim",
        ],
    }
    if not diagnostics["finite_factors"] or not diagnostics["finite_particles"]:
        raise FloatingPointError("Nystrom transport emitted non-finite values")
    result_particles = transported[0] if original_particle_rank == 2 else transported
    result_log_weights = uniform_log[0] if original_weight_rank == 1 else uniform_log
    result_transport = transport_matrix[0] if original_particle_rank == 2 else transport_matrix
    result_left = left_factor[0] if original_particle_rank == 2 else left_factor
    result_core = core_matrix[0] if original_particle_rank == 2 else core_matrix
    result_u = scaling_u[0] if original_particle_rank == 2 else scaling_u
    result_v = scaling_v[0] if original_particle_rank == 2 else scaling_v
    return NystromTransportTFResult(
        particles=result_particles,
        log_weights=result_log_weights,
        transport_matrix=result_transport,
        left_factor=result_left,
        core_matrix=result_core,
        scaling_u=result_u,
        scaling_v=result_v,
        landmark_indices=landmark_indices,
        diagnostics=diagnostics,
    )


def _deterministic_landmark_indices(num_particles: tf.Tensor, rank: int) -> tf.Tensor:
    if rank == 1:
        return tf.zeros([1], dtype=tf.int32)
    end = tf.cast(num_particles - 1, DTYPE)
    indices = tf.cast(tf.round(tf.linspace(tf.constant(0.0, DTYPE), end, rank)), tf.int32)
    return indices


def _nystrom_factors(
    x: tf.Tensor,
    landmarks: tf.Tensor,
    *,
    epsilon: tf.Tensor,
    cholesky_jitter: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    v = _gaussian_kernel(x, landmarks, epsilon)
    a = _gaussian_kernel(landmarks, landmarks, epsilon)
    rank = tf.shape(a)[1]
    eye = tf.eye(rank, dtype=DTYPE)[None, :, :]
    jittered = a + cholesky_jitter * eye
    chol = tf.linalg.cholesky(jittered)
    core = tf.linalg.cholesky_solve(chol, eye)
    diagonal = tf.einsum("bnr,brs,bns->bn", v, core, v)
    return v, core, {
        "max_diag_error": tf.reduce_max(tf.abs(1.0 - diagonal)),
        "min_factor_diagonal": tf.reduce_min(diagonal),
    }


def _sinkhorn_scale_factors(
    left_factor: tf.Tensor,
    core_matrix: tf.Tensor,
    row_target: tf.Tensor,
    column_target: tf.Tensor,
    *,
    max_iterations: int,
    convergence_threshold: tf.Tensor,
    denominator_floor: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    u = tf.ones_like(row_target)
    v = tf.ones_like(column_target)
    min_denominator = tf.constant(float("inf"), dtype=DTYPE)
    floor_hits = tf.constant(0.0, dtype=DTYPE)
    iterations_used = tf.constant(max_iterations, dtype=tf.int32)
    for iteration in range(1, max_iterations + 1):
        raw_kv = _factor_matvec(left_factor, core_matrix, v)
        min_denominator = tf.minimum(min_denominator, tf.reduce_min(raw_kv))
        safe_kv = tf.maximum(raw_kv, denominator_floor)
        floor_hits += tf.reduce_sum(tf.cast(raw_kv <= denominator_floor, DTYPE))
        u = row_target / safe_kv
        raw_ktu = _factor_matvec(left_factor, core_matrix, u)
        min_denominator = tf.minimum(min_denominator, tf.reduce_min(raw_ktu))
        safe_ktu = tf.maximum(raw_ktu, denominator_floor)
        floor_hits += tf.reduce_sum(tf.cast(raw_ktu <= denominator_floor, DTYPE))
        v = column_target / safe_ktu
        row_residual = tf.reduce_max(tf.abs(u * _factor_matvec(left_factor, core_matrix, v) - row_target))
        column_residual = tf.reduce_max(
            tf.abs(v * _factor_matvec(left_factor, core_matrix, u) - column_target)
        )
        if bool((tf.maximum(row_residual, column_residual) <= convergence_threshold).numpy()):
            iterations_used = tf.constant(iteration, dtype=tf.int32)
            break
    return u, v, iterations_used, {
        "min_denominator": min_denominator,
        "floor_hits": floor_hits,
    }


def _factor_matvec(left_factor: tf.Tensor, core_matrix: tf.Tensor, vector: tf.Tensor) -> tf.Tensor:
    projected = tf.einsum("bnr,bn->br", left_factor, vector)
    solved = tf.einsum("brs,bs->br", core_matrix, projected)
    return tf.einsum("bnr,br->bn", left_factor, solved)


def _factor_matmul(left_factor: tf.Tensor, core_matrix: tf.Tensor, matrix: tf.Tensor) -> tf.Tensor:
    projected = tf.einsum("bnr,bnd->brd", left_factor, matrix)
    solved = tf.einsum("brs,bsd->brd", core_matrix, projected)
    return tf.einsum("bnr,brd->bnd", left_factor, solved)


def _gaussian_kernel(x: tf.Tensor, y: tf.Tensor, epsilon: tf.Tensor) -> tf.Tensor:
    cost = 0.5 * _pairwise_squared_cross(x, y)
    return tf.exp(-cost / epsilon)


def _pairwise_squared_cross(query: tf.Tensor, key: tf.Tensor) -> tf.Tensor:
    xx = tf.reduce_sum(query * query, axis=2, keepdims=True)
    xy = tf.matmul(query, key, transpose_b=True)
    yy = tf.expand_dims(tf.reduce_sum(key * key, axis=-1), axis=1)
    return tf.clip_by_value(xx - 2.0 * xy + yy, 0.0, float("inf"))


def _filterflow_scale(x: tf.Tensor) -> tf.Tensor:
    std = tf.math.reduce_std(tf.cast(x, DTYPE), axis=1)
    diameter = tf.reduce_max(std, axis=1)
    diameter = tf.where(diameter == 0.0, tf.ones_like(diameter), diameter)
    dimension = tf.cast(tf.shape(x)[2], DTYPE)
    return diameter * tf.sqrt(dimension)


def _float(value: tf.Tensor) -> float:
    return float(tf.cast(value, DTYPE).numpy())
