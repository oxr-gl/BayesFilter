"""TensorFlow filterflow-style annealed regularized transport."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import tensorflow as tf


DTYPE = tf.float64


@dataclass(frozen=True)
class AnnealedTransportTFResult:
    particles: tf.Tensor
    log_weights: tf.Tensor
    transport_matrix: tf.Tensor
    diagnostics: dict[str, Any]


def annealed_transport_resample_tf(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    *,
    epsilon: float = 0.5,
    scaling: float = 0.9,
    convergence_threshold: float = 1e-3,
    max_iterations: int = 100,
    ess_mask: tf.Tensor | None = None,
    transport_gradient_mode: str = "filterflow_clipped",
    application_mode: str = "active_rows_only",
) -> AnnealedTransportTFResult:
    """Apply filterflow RegularisedTransform-style annealed transport.

    The mathematical target is the executable filterflow RegularisedTransform
    transport, not the local fixed-target Sinkhorn comparator.
    """
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if not 0.0 < scaling <= 1.0:
        raise ValueError("scaling must be in (0, 1]")
    if convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if transport_gradient_mode not in {"filterflow_clipped", "filterflow_custom_op", "raw"}:
        raise ValueError(
            "transport_gradient_mode must be 'filterflow_clipped', "
            "'filterflow_custom_op', or 'raw'"
        )
    if application_mode not in {"active_rows_only", "filterflow_all_rows"}:
        raise ValueError("application_mode must be 'active_rows_only' or 'filterflow_all_rows'")

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
    if ess_mask is None:
        mask = tf.ones([batch_size], dtype=tf.bool)
    else:
        mask = tf.reshape(tf.cast(ess_mask, tf.bool), [-1])
    log_weight_normalization_residual = tf.reduce_max(
        tf.abs(tf.reduce_logsumexp(logw, axis=1))
    )
    uniform_log = tf.fill(
        [batch_size, num_particles],
        -tf.math.log(tf.cast(num_particles, DTYPE)),
    )
    out_particles = tf.identity(x)
    out_log_weights = tf.where(mask[:, None], uniform_log, logw)
    full_transport = tf.zeros([batch_size, num_particles, num_particles], dtype=DTYPE)
    triggered_count = tf.reduce_sum(tf.cast(mask, DTYPE))
    skipped_count = tf.cast(batch_size, DTYPE) - triggered_count

    if application_mode == "filterflow_all_rows":
        transported, transport_matrix, active_diag = _transport_active(
            x,
            logw,
            epsilon=epsilon,
            scaling=scaling,
            convergence_threshold=convergence_threshold,
            max_iterations=max_iterations,
            transport_gradient_mode=transport_gradient_mode,
        )
        out_particles = tf.where(mask[:, None, None], transported, x)
        full_transport = transport_matrix
        max_row_residual = active_diag["max_row_residual"]
        max_column_residual = active_diag["max_column_residual"]
        max_cost_scale = active_diag["max_cost_scale"]
        min_cost_scale = active_diag["min_cost_scale"]
        max_iterations_used = active_diag["max_iterations_used"]
        finite_transport = active_diag["finite_transport"]
        finite_particles = active_diag["finite_particles"]
    elif bool(tf.reduce_any(mask).numpy()):
        active_x = tf.boolean_mask(x, mask)
        active_logw = tf.boolean_mask(logw, mask)
        transported, transport_matrix, active_diag = _transport_active(
            active_x,
            active_logw,
            epsilon=epsilon,
            scaling=scaling,
            convergence_threshold=convergence_threshold,
            max_iterations=max_iterations,
            transport_gradient_mode=transport_gradient_mode,
        )
        active_indices = tf.where(mask)
        out_particles = tf.tensor_scatter_nd_update(out_particles, active_indices, transported)
        full_transport = tf.tensor_scatter_nd_update(full_transport, active_indices, transport_matrix)
        max_row_residual = active_diag["max_row_residual"]
        max_column_residual = active_diag["max_column_residual"]
        max_cost_scale = active_diag["max_cost_scale"]
        min_cost_scale = active_diag["min_cost_scale"]
        max_iterations_used = active_diag["max_iterations_used"]
        finite_transport = active_diag["finite_transport"]
        finite_particles = active_diag["finite_particles"]
    else:
        max_row_residual = tf.constant(0.0, DTYPE)
        max_column_residual = tf.constant(0.0, DTYPE)
        max_cost_scale = tf.constant(0.0, DTYPE)
        min_cost_scale = tf.constant(0.0, DTYPE)
        max_iterations_used = tf.constant(0.0, DTYPE)
        finite_transport = True
        finite_particles = True

    diagnostics = {
        "component_id": "filterflow_style_annealed_transport_tf",
        "reference_algorithm": "canonical_executable_filterflow_regularised_transform",
        "mathematical_object": "annealed_regularized_transport_transform",
        "fixed_target_sinkhorn_status": "not_this_algorithm_local_comparator_only",
        "epsilon": float(epsilon),
        "scaling": float(scaling),
        "convergence_threshold": float(convergence_threshold),
        "max_iterations": int(max_iterations),
        "transport_gradient_mode": transport_gradient_mode,
        "application_mode": application_mode,
        "transport_backward_rule": _transport_backward_rule(transport_gradient_mode),
        "triggered_rows": _float(triggered_count),
        "skipped_rows": _float(skipped_count),
        "max_row_residual": _float(max_row_residual),
        "max_column_residual": _float(max_column_residual),
        "max_cost_scale": _float(max_cost_scale),
        "min_cost_scale": _float(min_cost_scale),
        "max_iterations_used": _float(max_iterations_used),
        "finite_transport": bool(finite_transport),
        "finite_particles": bool(finite_particles),
        "max_log_weight_normalization_residual": _float(log_weight_normalization_residual),
        "backend": "tensorflow",
        "resampling_status": "annealed_transport_triggered_rows_only",
    }
    if not diagnostics["finite_transport"] or not diagnostics["finite_particles"]:
        raise FloatingPointError("annealed transport emitted non-finite values")
    result_particles = out_particles[0] if original_particle_rank == 2 else out_particles
    result_log_weights = out_log_weights[0] if original_weight_rank == 1 else out_log_weights
    result_transport = full_transport[0] if original_particle_rank == 2 else full_transport
    return AnnealedTransportTFResult(
        particles=result_particles,
        log_weights=result_log_weights,
        transport_matrix=result_transport,
        diagnostics=diagnostics,
    )


def _transport_active(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    *,
    epsilon: float,
    scaling: float,
    convergence_threshold: float,
    max_iterations: int,
    transport_gradient_mode: str,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor | bool]]:
    x = tf.cast(particles, DTYPE)
    logw = tf.cast(log_weights, DTYPE)
    batch_size = tf.shape(x)[0]
    num_particles = tf.shape(x)[1]
    centered = x - tf.stop_gradient(tf.reduce_mean(x, axis=1, keepdims=True))
    scale = _filterflow_scale(x)
    scaled_x = centered / tf.stop_gradient(scale[:, None, None])
    cost = 0.5 * _pairwise_squared(scaled_x)
    epsilon_tensor = tf.constant(epsilon, DTYPE)
    scaling_tensor = tf.constant(scaling, DTYPE)
    threshold_tensor = tf.constant(convergence_threshold, DTYPE)
    max_iterations_tensor = tf.constant(max_iterations, tf.int32)
    if transport_gradient_mode == "filterflow_custom_op":
        transport_matrix, iterations = _filterflow_custom_gradient_transport_matrix(
            scaled_x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles,
        )
    else:
        transport_matrix, iterations = _filterflow_exact_transport_matrix(
            scaled_x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles,
        )
    if transport_gradient_mode == "filterflow_clipped":
        transport_matrix = _clip_transport_upstream_gradient(transport_matrix)
    transported = tf.linalg.matmul(transport_matrix, x)
    row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport_matrix, axis=2) - 1.0))
    source_weights = tf.exp(logw)
    column_mass = tf.reduce_sum(transport_matrix, axis=1)
    column_target = source_weights * tf.cast(num_particles, DTYPE)
    column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
    return transported, transport_matrix, {
        "max_row_residual": tf.cast(row_residual, DTYPE),
        "max_column_residual": tf.cast(column_residual, DTYPE),
        "max_cost_scale": tf.reduce_max(scale),
        "min_cost_scale": tf.reduce_min(scale),
        "max_iterations_used": tf.reduce_max(tf.cast(iterations, DTYPE)),
        "finite_transport": bool(tf.reduce_all(tf.math.is_finite(transport_matrix)).numpy()),
        "finite_particles": bool(tf.reduce_all(tf.math.is_finite(transported)).numpy()),
    }


def _transport_backward_rule(mode: str) -> str:
    if mode == "filterflow_clipped":
        return "clip_upstream_d_transport_to_[-1,1]_at_transport_matrix_output"
    if mode == "filterflow_custom_op":
        return "filterflow_style_whole_transport_custom_gradient"
    return "raw_tensorflow_transport_gradient"


@tf.custom_gradient
def _clip_transport_upstream_gradient(
    transport_matrix: tf.Tensor,
) -> tuple[tf.Tensor, Any]:
    """Mirror FilterFlow RegularisedTransform transport backward clipping."""

    def grad(d_transport: tf.Tensor) -> tf.Tensor:
        return tf.clip_by_value(d_transport, -1.0, 1.0)

    return transport_matrix, grad


@tf.custom_gradient
def _filterflow_custom_gradient_transport_matrix(
    x: tf.Tensor,
    logw: tf.Tensor,
    eps: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
    n: tf.Tensor,
) -> tuple[tuple[tf.Tensor, tf.Tensor], Any]:
    transport_matrix, iterations = _filterflow_exact_transport_matrix(
        x,
        logw,
        eps,
        scaling,
        threshold,
        max_iter,
        n,
    )

    def grad(
        d_transport: tf.Tensor,
        d_iterations: tf.Tensor | None = None,
    ) -> tuple[tf.Tensor | None, ...]:
        del d_iterations
        clipped = tf.clip_by_value(d_transport, -1.0, 1.0)
        with tf.GradientTape() as tape:
            tape.watch([x, logw])
            raw_transport_matrix, _raw_iterations = _filterflow_exact_transport_matrix(
                x,
                logw,
                eps,
                scaling,
                threshold,
                max_iter,
                n,
            )
        dx, dlogw = tape.gradient(
            raw_transport_matrix,
            [x, logw],
            output_gradients=clipped,
        )
        return dx, dlogw, None, None, None, None, None

    return (transport_matrix, iterations), grad


@tf.function
def _filterflow_exact_transport_matrix(
    x: tf.Tensor,
    logw: tf.Tensor,
    eps: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
    n: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    float_n = tf.cast(n, x.dtype)
    log_n = tf.math.log(float_n)
    uniform_log_weight = -log_n * tf.ones_like(logw)
    alpha, beta, _, _, iterations = _filterflow_exact_sinkhorn_potentials(
        logw,
        x,
        uniform_log_weight,
        x,
        eps,
        scaling,
        threshold,
        max_iter,
    )
    transport_matrix = _filterflow_exact_transport_from_potentials(
        x,
        alpha,
        beta,
        eps,
        logw,
        float_n,
    )
    return transport_matrix, iterations


@tf.function
def _filterflow_exact_transport_from_potentials(
    x: tf.Tensor,
    f: tf.Tensor,
    g: tf.Tensor,
    eps: tf.Tensor,
    logw: tf.Tensor,
    float_n: tf.Tensor,
) -> tf.Tensor:
    log_n = tf.math.log(float_n)
    cost_matrix = _filterflow_exact_cost(x, x)
    fg = tf.expand_dims(f, 2) + tf.expand_dims(g, 1)
    temp = fg - cost_matrix
    temp = temp / eps
    temp = temp - tf.reduce_logsumexp(temp, 1, keepdims=True) + log_n
    temp = temp + tf.expand_dims(logw, 1)
    return tf.math.exp(temp)


@tf.function
def _filterflow_exact_sinkhorn_potentials(
    log_alpha: tf.Tensor,
    x: tf.Tensor,
    log_beta: tf.Tensor,
    y: tf.Tensor,
    epsilon: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    cost_xy = _filterflow_exact_cost(x, tf.stop_gradient(y))
    cost_yx = _filterflow_exact_cost(y, tf.stop_gradient(x))
    cost_xx = _filterflow_exact_cost(x, tf.stop_gradient(x))
    cost_yy = _filterflow_exact_cost(y, tf.stop_gradient(y))
    scale = tf.stop_gradient(_filterflow_exact_max_min(x, y))
    return _filterflow_exact_sinkhorn_loop(
        log_alpha,
        log_beta,
        cost_xy,
        cost_yx,
        cost_xx,
        cost_yy,
        epsilon,
        scale,
        scaling,
        threshold,
        max_iter,
    )


@tf.function
def _filterflow_exact_sinkhorn_loop(
    log_alpha: tf.Tensor,
    log_beta: tf.Tensor,
    cost_xy: tf.Tensor,
    cost_yx: tf.Tensor,
    cost_xx: tf.Tensor,
    cost_yy: tf.Tensor,
    epsilon: tf.Tensor,
    particles_diameter: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    batch_size = tf.shape(log_alpha)[0]
    continue_flag = tf.ones([batch_size], dtype=tf.bool)
    epsilon_0 = particles_diameter ** 2
    scaling_factor = scaling ** 2

    a_y_init = _filterflow_exact_softmin(epsilon_0, cost_yx, log_alpha)
    b_x_init = _filterflow_exact_softmin(epsilon_0, cost_xy, log_beta)
    a_x_init = _filterflow_exact_softmin(epsilon_0, cost_xx, log_alpha)
    b_y_init = _filterflow_exact_softmin(epsilon_0, cost_yy, log_beta)

    def stop_condition(i, _a_y, _b_x, _a_x, _b_y, continue_, _running_epsilon):
        n_iter_cond = i < max_iter - 1
        return tf.logical_and(n_iter_cond, tf.reduce_all(continue_))

    def apply_one(a_y, b_x, a_x, b_y, continue_, running_epsilon):
        running_epsilon_ = tf.reshape(running_epsilon, [-1, 1])
        continue_reshaped = tf.reshape(continue_, [-1, 1])
        at_y = tf.where(
            continue_reshaped,
            _filterflow_exact_softmin(
                running_epsilon,
                cost_yx,
                log_alpha + b_x / running_epsilon_,
            ),
            a_y,
        )
        bt_x = tf.where(
            continue_reshaped,
            _filterflow_exact_softmin(
                running_epsilon,
                cost_xy,
                log_beta + a_y / running_epsilon_,
            ),
            b_x,
        )
        at_x = tf.where(
            continue_reshaped,
            _filterflow_exact_softmin(
                running_epsilon,
                cost_xx,
                log_alpha + a_x / running_epsilon_,
            ),
            a_x,
        )
        bt_y = tf.where(
            continue_reshaped,
            _filterflow_exact_softmin(
                running_epsilon,
                cost_yy,
                log_beta + b_y / running_epsilon_,
            ),
            b_y,
        )
        a_y_new = (a_y + at_y) / 2
        b_x_new = (b_x + bt_x) / 2
        a_x_new = (a_x + at_x) / 2
        b_y_new = (b_y + bt_y) / 2
        a_y_diff = tf.reduce_max(tf.abs(a_y_new - a_y), 1)
        b_x_diff = tf.reduce_max(tf.abs(b_x_new - b_x), 1)
        local_continue = tf.logical_or(a_y_diff > threshold, b_x_diff > threshold)
        return a_y_new, b_x_new, a_x_new, b_y_new, local_continue

    def body(i, a_y, b_x, a_x, b_y, continue_, running_epsilon):
        new_a_y, new_b_x, new_a_x, new_b_y, local_continue = apply_one(
            a_y,
            b_x,
            a_x,
            b_y,
            continue_,
            running_epsilon,
        )
        new_epsilon = tf.maximum(running_epsilon * scaling_factor, epsilon)
        global_continue = tf.logical_or(new_epsilon < running_epsilon, local_continue)
        return (
            i + 1,
            new_a_y,
            new_b_x,
            new_a_x,
            new_b_y,
            global_continue,
            new_epsilon,
        )

    n_iter = tf.constant(0)
    (
        total_iter,
        converged_a_y,
        converged_b_x,
        converged_a_x,
        converged_b_y,
        _,
        _final_epsilon,
    ) = tf.while_loop(
        stop_condition,
        body,
        loop_vars=[
            n_iter,
            a_y_init,
            b_x_init,
            a_x_init,
            b_y_init,
            continue_flag,
            epsilon_0,
        ],
    )
    (
        converged_a_y,
        converged_b_x,
        converged_a_x,
        converged_b_y,
    ) = tf.nest.map_structure(
        tf.stop_gradient,
        (converged_a_y, converged_b_x, converged_a_x, converged_b_y),
    )
    epsilon_ = tf.reshape(epsilon, [-1, 1])
    final_a_y = _filterflow_exact_softmin(
        epsilon,
        cost_yx,
        log_alpha + converged_b_x / epsilon_,
    )
    final_b_x = _filterflow_exact_softmin(
        epsilon,
        cost_xy,
        log_beta + converged_a_y / epsilon_,
    )
    final_a_x = _filterflow_exact_softmin(
        epsilon,
        cost_xx,
        log_alpha + converged_a_x / epsilon_,
    )
    final_b_y = _filterflow_exact_softmin(
        epsilon,
        cost_yy,
        log_beta + converged_b_y / epsilon_,
    )
    return final_a_y, final_b_x, final_a_x, final_b_y, total_iter + 2


def _filterflow_exact_softmin(
    epsilon: tf.Tensor,
    cost_matrix: tf.Tensor,
    values: tf.Tensor,
) -> tf.Tensor:
    n = cost_matrix.shape[1]
    batch_size = tf.shape(cost_matrix)[0]
    values_reshaped = tf.reshape(values, (batch_size, 1, n))
    temp = values_reshaped - cost_matrix / tf.reshape(epsilon, (-1, 1, 1))
    log_sum_exp = tf.reduce_logsumexp(temp, axis=2)
    return -tf.reshape(epsilon, (-1, 1)) * log_sum_exp


@tf.function
def _filterflow_exact_cost(x: tf.Tensor, y: tf.Tensor) -> tf.Tensor:
    return _filterflow_exact_squared_distances(x, y) / 2.0


@tf.function
def _filterflow_exact_squared_distances(x: tf.Tensor, y: tf.Tensor) -> tf.Tensor:
    xx = tf.reduce_sum(x * x, axis=2, keepdims=True)
    xy = tf.matmul(x, y, transpose_b=True)
    yy = tf.expand_dims(tf.reduce_sum(y * y, axis=-1), 1)
    return tf.clip_by_value(xx - 2 * xy + yy, 0.0, float("inf"))


@tf.function
def _filterflow_exact_max_min(x: tf.Tensor, y: tf.Tensor) -> tf.Tensor:
    max_max = tf.maximum(tf.math.reduce_max(x, [1, 2]), tf.math.reduce_max(y, [1, 2]))
    min_min = tf.minimum(tf.math.reduce_min(x, [1, 2]), tf.math.reduce_min(y, [1, 2]))
    return max_max - min_min


def _filterflow_scale(x: tf.Tensor) -> tf.Tensor:
    std = tf.math.reduce_std(tf.cast(x, DTYPE), axis=1)
    diameter = tf.reduce_max(std, axis=1)
    diameter = tf.where(diameter == 0.0, tf.ones_like(diameter), diameter)
    dimension = tf.cast(tf.shape(x)[2], DTYPE)
    return diameter * tf.sqrt(dimension)


def _filterflow_epsilon_start(scaled_x: tf.Tensor) -> tf.Tensor:
    coordinate_range = tf.reduce_max(scaled_x, axis=[1, 2]) - tf.reduce_min(scaled_x, axis=[1, 2])
    return tf.maximum(coordinate_range * coordinate_range, tf.constant(1e-6, DTYPE))


def _pairwise_squared(x: tf.Tensor) -> tf.Tensor:
    xx = tf.reduce_sum(x * x, axis=2, keepdims=True)
    xy = tf.matmul(x, x, transpose_b=True)
    yy = tf.expand_dims(tf.reduce_sum(x * x, axis=-1), axis=1)
    return tf.clip_by_value(xx - 2.0 * xy + yy, 0.0, float("inf"))


def _float(value: tf.Tensor) -> float:
    return float(tf.cast(value, DTYPE).numpy())
