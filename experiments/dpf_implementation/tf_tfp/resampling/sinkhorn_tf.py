"""TensorFlow finite Sinkhorn relaxed resampling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import tensorflow as tf


DTYPE = tf.float64


@dataclass(frozen=True)
class SinkhornTFResult:
    particles: tf.Tensor
    coupling: tf.Tensor
    source_weights: tf.Tensor
    target_weights: tf.Tensor
    diagnostics: dict[str, Any]


def pairwise_squared_euclidean_tf(x: tf.Tensor, y: tf.Tensor | None = None) -> tf.Tensor:
    x = tf.cast(x, DTYPE)
    y = x if y is None else tf.cast(y, DTYPE)
    diff = x[:, None, :] - y[None, :, :]
    return tf.reduce_sum(diff * diff, axis=2)


def sinkhorn_resample_tf(
    particles: tf.Tensor,
    weights: tf.Tensor,
    *,
    epsilon: float = 0.5,
    max_iterations: int = 80,
    tolerance: float = 1e-7,
    cost: tf.Tensor | None = None,
    stabilization: str = "log_domain",
) -> SinkhornTFResult:
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if stabilization != "log_domain":
        raise ValueError("only log_domain stabilization is implemented")
    x = tf.cast(particles, DTYPE)
    if len(x.shape) == 1:
        x = x[:, None]
    source = tf.reshape(tf.cast(weights, DTYPE), [-1])
    n = tf.shape(x)[0]
    if int(x.shape[0] or 0) and int(source.shape[0] or 0) and x.shape[0] != source.shape[0]:
        raise ValueError("particles and weights must agree on particle count")
    source_total = tf.reduce_sum(source)
    source = source / source_total
    target = tf.ones([n], dtype=DTYPE) / tf.cast(n, DTYPE)
    cost_matrix = pairwise_squared_euclidean_tf(x) if cost is None else tf.cast(cost, DTYPE)
    log_source = tf.math.log(tf.maximum(source, tf.constant(1e-300, dtype=DTYPE)))
    log_target = tf.math.log(target)
    kernel_log = -cost_matrix / tf.constant(epsilon, dtype=DTYPE)
    log_u = tf.zeros([n], dtype=DTYPE)
    log_v = tf.zeros([n], dtype=DTYPE)
    iterations_used = max_iterations

    for iteration in range(1, max_iterations + 1):
        log_u = log_source - tf.reduce_logsumexp(kernel_log + log_v[None, :], axis=1)
        log_v = log_target - tf.reduce_logsumexp(kernel_log + log_u[:, None], axis=0)
        if iteration == max_iterations or iteration % 10 == 0:
            coupling_probe = tf.exp(log_u[:, None] + kernel_log + log_v[None, :])
            row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(coupling_probe, axis=1) - source))
            column_residual = tf.reduce_max(tf.abs(tf.reduce_sum(coupling_probe, axis=0) - target))
            if bool((tf.maximum(row_residual, column_residual) <= tolerance).numpy()):
                iterations_used = iteration
                break

    coupling = tf.exp(log_u[:, None] + kernel_log + log_v[None, :])
    column_mass = tf.reduce_sum(coupling, axis=0)
    safe_column_mass = tf.maximum(column_mass, tf.constant(1e-300, dtype=DTYPE))
    relaxed_particles = tf.linalg.matmul(coupling, x, transpose_a=True) / safe_column_mass[:, None]
    row_residuals = tf.reduce_sum(coupling, axis=1) - source
    column_residuals = column_mass - target
    diagnostics = {
        "component_id": "finite_sinkhorn_relaxed_resampler_tf",
        "mathematical_object": "finite_budget_entropic_ot_coupling",
        "epsilon": float(epsilon),
        "max_iterations": int(max_iterations),
        "iterations_used": int(iterations_used),
        "tolerance": float(tolerance),
        "stabilization": stabilization,
        "cost_function": "pairwise_squared_euclidean",
        "target_marginal": "uniform",
        "max_row_residual": _float(tf.reduce_max(tf.abs(row_residuals))),
        "max_column_residual": _float(tf.reduce_max(tf.abs(column_residuals))),
        "total_mass_residual": _float(tf.abs(tf.reduce_sum(coupling) - 1.0)),
        "min_coupling": _float(tf.reduce_min(coupling)),
        "finite_coupling": bool(tf.reduce_all(tf.math.is_finite(coupling)).numpy()),
        "finite_particles": bool(tf.reduce_all(tf.math.is_finite(relaxed_particles)).numpy()),
        "resampling_status": "relaxed_finite_sinkhorn_not_categorical",
        "backend": "tensorflow",
    }
    if diagnostics["max_row_residual"] > tolerance * 10.0:
        raise FloatingPointError("Sinkhorn row residual exceeded tolerance envelope")
    if diagnostics["max_column_residual"] > tolerance * 10.0:
        raise FloatingPointError("Sinkhorn column residual exceeded tolerance envelope")
    if diagnostics["min_coupling"] < -1e-12:
        raise FloatingPointError("Sinkhorn coupling has negative entries")
    if not diagnostics["finite_coupling"] or not diagnostics["finite_particles"]:
        raise FloatingPointError("Sinkhorn emitted non-finite values")
    return SinkhornTFResult(
        particles=relaxed_particles,
        coupling=coupling,
        source_weights=source,
        target_weights=target,
        diagnostics=diagnostics,
    )


def _float(value: tf.Tensor) -> float:
    return float(tf.cast(value, DTYPE).numpy())
