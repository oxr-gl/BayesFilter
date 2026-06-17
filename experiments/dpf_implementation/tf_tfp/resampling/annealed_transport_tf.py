"""TensorFlow filterflow-style annealed regularized transport."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import tensorflow as tf


DEFAULT_DTYPE = tf.float64
DTYPE = DEFAULT_DTYPE
DEFAULT_STREAMING_CHUNK_SIZE = 1024
_STREAMING_LOG_ZERO = -1.0e30


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
    transport_plan_mode: str = "dense",
    row_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
    col_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
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
    if transport_plan_mode not in {"dense", "streaming"}:
        raise ValueError("transport_plan_mode must be 'dense' or 'streaming'")
    if transport_plan_mode == "streaming" and transport_gradient_mode != "raw":
        raise ValueError("streaming transport currently supports transport_gradient_mode='raw' only")
    if row_chunk_size <= 0 or col_chunk_size <= 0:
        raise ValueError("row_chunk_size and col_chunk_size must be positive")

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
    if transport_plan_mode == "dense":
        full_transport = tf.zeros([batch_size, num_particles, num_particles], dtype=DTYPE)
    else:
        full_transport = tf.zeros([batch_size, 0, 0], dtype=DTYPE)
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
            transport_plan_mode=transport_plan_mode,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        out_particles = tf.where(mask[:, None, None], transported, x)
        if transport_plan_mode == "dense":
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
            transport_plan_mode=transport_plan_mode,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        active_indices = tf.where(mask)
        out_particles = tf.tensor_scatter_nd_update(out_particles, active_indices, transported)
        if transport_plan_mode == "dense":
            full_transport = tf.tensor_scatter_nd_update(
                full_transport,
                active_indices,
                transport_matrix,
            )
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
        "transport_plan_mode": transport_plan_mode,
        "transport_matrix_materialized": transport_plan_mode == "dense",
        "row_chunk_size": int(row_chunk_size),
        "col_chunk_size": int(col_chunk_size),
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
    transport_plan_mode: str = "dense",
    row_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
    col_chunk_size: int = DEFAULT_STREAMING_CHUNK_SIZE,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor | bool]]:
    x = tf.cast(particles, DTYPE)
    logw = tf.cast(log_weights, DTYPE)
    batch_size = tf.shape(x)[0]
    num_particles = tf.shape(x)[1]
    centered = x - tf.stop_gradient(tf.reduce_mean(x, axis=1, keepdims=True))
    scale = _filterflow_scale(x)
    scaled_x = centered / tf.stop_gradient(scale[:, None, None])
    epsilon_tensor = tf.constant(epsilon, DTYPE)
    scaling_tensor = tf.constant(scaling, DTYPE)
    threshold_tensor = tf.constant(convergence_threshold, DTYPE)
    max_iterations_tensor = tf.constant(max_iterations, tf.int32)
    if transport_plan_mode == "streaming":
        if transport_gradient_mode != "raw":
            raise ValueError("streaming transport currently supports raw gradients only")
        transport_matrix = tf.zeros([batch_size, 0, 0], dtype=DTYPE)
        transported, iterations, row_residual, column_residual = _filterflow_streaming_transport(
            scaled_x,
            x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
    elif transport_gradient_mode == "filterflow_custom_op":
        transport_matrix, iterations = _filterflow_custom_gradient_transport_matrix(
            scaled_x,
            logw,
            epsilon_tensor,
            scaling_tensor,
            threshold_tensor,
            max_iterations_tensor,
            num_particles,
        )
        transported = tf.linalg.matmul(transport_matrix, x)
        row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport_matrix, axis=2) - 1.0))
        source_weights = tf.exp(logw)
        column_mass = tf.reduce_sum(transport_matrix, axis=1)
        column_target = source_weights * tf.cast(num_particles, DTYPE)
        column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
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


def _validate_chunk_size(value: int, name: str) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def _slice_axis1_padded_3d(
    tensor: tf.Tensor,
    start: tf.Tensor,
    chunk_size: int,
) -> tf.Tensor:
    chunk_size = _validate_chunk_size(chunk_size, "chunk_size")
    total = tf.shape(tensor)[1]
    raw_indices = start + tf.range(tf.cast(chunk_size, tf.int32), dtype=tf.int32)
    safe_indices = tf.minimum(raw_indices, total - 1)
    gathered = tf.gather(tensor, safe_indices, axis=1)
    gathered.set_shape([tensor.shape[0], chunk_size, tensor.shape[2]])
    return gathered


def _slice_axis1_padded_2d(
    tensor: tf.Tensor,
    start: tf.Tensor,
    chunk_size: int,
    *,
    pad_value: float,
) -> tf.Tensor:
    chunk_size = _validate_chunk_size(chunk_size, "chunk_size")
    total = tf.shape(tensor)[1]
    raw_indices = start + tf.range(tf.cast(chunk_size, tf.int32), dtype=tf.int32)
    safe_indices = tf.minimum(raw_indices, total - 1)
    gathered = tf.gather(tensor, safe_indices, axis=1)
    valid = raw_indices < total
    padded = tf.where(
        valid[None, :],
        gathered,
        tf.fill(tf.shape(gathered), tf.cast(pad_value, tensor.dtype)),
    )
    padded.set_shape([tensor.shape[0], chunk_size])
    return padded


def _streaming_log_zero(dtype: tf.DType) -> tf.Tensor:
    return tf.cast(_STREAMING_LOG_ZERO, dtype)


def _logaddexp(lhs: tf.Tensor, rhs: tf.Tensor) -> tf.Tensor:
    return tf.reduce_logsumexp(tf.stack([lhs, rhs], axis=0), axis=0)


def _pairwise_squared_cross(query: tf.Tensor, key: tf.Tensor) -> tf.Tensor:
    xx = tf.reduce_sum(query * query, axis=2, keepdims=True)
    xy = tf.matmul(query, key, transpose_b=True)
    yy = tf.expand_dims(tf.reduce_sum(key * key, axis=-1), axis=1)
    return tf.clip_by_value(xx - 2.0 * xy + yy, 0.0, float("inf"))


def _filterflow_streaming_softmin(
    epsilon: tf.Tensor,
    query: tf.Tensor,
    key: tf.Tensor,
    values: tf.Tensor,
    *,
    row_chunk_size: int,
    col_chunk_size: int,
) -> tf.Tensor:
    """Compute FilterFlow softmin without materializing the cost matrix."""

    row_chunk_size = _validate_chunk_size(row_chunk_size, "row_chunk_size")
    col_chunk_size = _validate_chunk_size(col_chunk_size, "col_chunk_size")
    query = tf.cast(query, DTYPE)
    key = tf.cast(key, DTYPE)
    values = tf.cast(values, DTYPE)
    epsilon = tf.reshape(tf.cast(epsilon, DTYPE), [-1])
    batch_size = tf.shape(query)[0]
    num_rows = tf.shape(query)[1]
    num_cols = tf.shape(key)[1]
    row_chunk_tensor = tf.cast(row_chunk_size, tf.int32)
    col_chunk_tensor = tf.cast(col_chunk_size, tf.int32)
    num_row_blocks = (num_rows + row_chunk_tensor - 1) // row_chunk_tensor
    blocks = tf.TensorArray(
        dtype=DTYPE,
        size=num_row_blocks,
        element_shape=tf.TensorShape([None, row_chunk_size]),
    )

    def row_cond(row_start: tf.Tensor, _blocks: tf.TensorArray) -> tf.Tensor:
        return row_start < num_rows

    def row_body(row_start: tf.Tensor, blocks_ta: tf.TensorArray):
        query_block = _slice_axis1_padded_3d(query, row_start, row_chunk_size)
        running = tf.fill([batch_size, row_chunk_size], tf.constant(-float("inf"), DTYPE))

        def col_cond(col_start: tf.Tensor, _running: tf.Tensor) -> tf.Tensor:
            return col_start < num_cols

        def col_body(col_start: tf.Tensor, running_logsum: tf.Tensor):
            key_block = _slice_axis1_padded_3d(key, col_start, col_chunk_size)
            values_block = _slice_axis1_padded_2d(
                values,
                col_start,
                col_chunk_size,
                pad_value=float(_STREAMING_LOG_ZERO),
            )
            cost = 0.5 * _pairwise_squared_cross(query_block, key_block)
            logits = values_block[:, None, :] - cost / epsilon[:, None, None]
            block_logsum = tf.reduce_logsumexp(logits, axis=2)
            return col_start + col_chunk_tensor, _logaddexp(running_logsum, block_logsum)

        _, row_logsum = tf.while_loop(
            col_cond,
            col_body,
            loop_vars=(tf.constant(0, tf.int32), running),
            maximum_iterations=(num_cols + col_chunk_tensor - 1) // col_chunk_tensor,
        )
        result_block = -epsilon[:, None] * row_logsum
        block_index = row_start // row_chunk_tensor
        blocks_ta = blocks_ta.write(block_index, result_block)
        return row_start + row_chunk_tensor, blocks_ta

    _, blocks = tf.while_loop(
        row_cond,
        row_body,
        loop_vars=(tf.constant(0, tf.int32), blocks),
        maximum_iterations=num_row_blocks,
    )
    stacked = blocks.stack()
    transposed = tf.transpose(stacked, [1, 0, 2])
    flat = tf.reshape(transposed, [batch_size, num_row_blocks * row_chunk_tensor])
    return flat[:, :num_rows]


def _filterflow_streaming_sinkhorn_potentials(
    log_alpha: tf.Tensor,
    x: tf.Tensor,
    log_beta: tf.Tensor,
    y: tf.Tensor,
    epsilon: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
    *,
    row_chunk_size: int,
    col_chunk_size: int,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    batch_size = tf.shape(log_alpha)[0]
    continue_flag = tf.ones([batch_size], dtype=tf.bool)
    epsilon_0 = tf.stop_gradient(_filterflow_exact_max_min(x, y)) ** 2
    scaling_factor = scaling ** 2
    x_key = tf.stop_gradient(x)
    y_key = tf.stop_gradient(y)

    a_y_init = _filterflow_streaming_softmin(
        epsilon_0,
        y,
        x_key,
        log_alpha,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    b_x_init = _filterflow_streaming_softmin(
        epsilon_0,
        x,
        y_key,
        log_beta,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    a_x_init = _filterflow_streaming_softmin(
        epsilon_0,
        x,
        x_key,
        log_alpha,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    b_y_init = _filterflow_streaming_softmin(
        epsilon_0,
        y,
        y_key,
        log_beta,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )

    def stop_condition(i, _a_y, _b_x, _a_x, _b_y, continue_, _running_epsilon):
        n_iter_cond = i < max_iter - 1
        return tf.logical_and(n_iter_cond, tf.reduce_all(continue_))

    def apply_one(a_y, b_x, a_x, b_y, continue_, running_epsilon):
        running_epsilon_ = tf.reshape(running_epsilon, [-1, 1])
        continue_reshaped = tf.reshape(continue_, [-1, 1])
        at_y_raw = _filterflow_streaming_softmin(
            running_epsilon,
            y,
            x_key,
            log_alpha + b_x / running_epsilon_,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        bt_x_raw = _filterflow_streaming_softmin(
            running_epsilon,
            x,
            y_key,
            log_beta + a_y / running_epsilon_,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        at_x_raw = _filterflow_streaming_softmin(
            running_epsilon,
            x,
            x_key,
            log_alpha + a_x / running_epsilon_,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        bt_y_raw = _filterflow_streaming_softmin(
            running_epsilon,
            y,
            y_key,
            log_beta + b_y / running_epsilon_,
            row_chunk_size=row_chunk_size,
            col_chunk_size=col_chunk_size,
        )
        at_y = tf.where(continue_reshaped, at_y_raw, a_y)
        bt_x = tf.where(continue_reshaped, bt_x_raw, b_x)
        at_x = tf.where(continue_reshaped, at_x_raw, a_x)
        bt_y = tf.where(continue_reshaped, bt_y_raw, b_y)
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
        return i + 1, new_a_y, new_b_x, new_a_x, new_b_y, global_continue, new_epsilon

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
        loop_vars=(
            tf.constant(0, tf.int32),
            a_y_init,
            b_x_init,
            a_x_init,
            b_y_init,
            continue_flag,
            epsilon_0,
        ),
        maximum_iterations=max_iter,
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
    final_a_y = _filterflow_streaming_softmin(
        epsilon,
        y,
        x_key,
        log_alpha + converged_b_x / epsilon_,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    final_b_x = _filterflow_streaming_softmin(
        epsilon,
        x,
        y_key,
        log_beta + converged_a_y / epsilon_,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    final_a_x = _filterflow_streaming_softmin(
        epsilon,
        x,
        x_key,
        log_alpha + converged_a_x / epsilon_,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    final_b_y = _filterflow_streaming_softmin(
        epsilon,
        y,
        y_key,
        log_beta + converged_b_y / epsilon_,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    return final_a_y, final_b_x, final_a_x, final_b_y, total_iter + 2


def _filterflow_streaming_column_log_normalizer(
    x: tf.Tensor,
    f: tf.Tensor,
    g: tf.Tensor,
    eps: tf.Tensor,
    *,
    row_chunk_size: int,
    col_chunk_size: int,
) -> tf.Tensor:
    row_chunk_size = _validate_chunk_size(row_chunk_size, "row_chunk_size")
    col_chunk_size = _validate_chunk_size(col_chunk_size, "col_chunk_size")
    batch_size = tf.shape(x)[0]
    num_particles = tf.shape(x)[1]
    eps = tf.reshape(tf.cast(eps, DTYPE), [-1])
    row_chunk_tensor = tf.cast(row_chunk_size, tf.int32)
    col_chunk_tensor = tf.cast(col_chunk_size, tf.int32)
    num_col_blocks = (num_particles + col_chunk_tensor - 1) // col_chunk_tensor
    blocks = tf.TensorArray(
        dtype=DTYPE,
        size=num_col_blocks,
        element_shape=tf.TensorShape([None, col_chunk_size]),
    )

    def col_cond(col_start: tf.Tensor, _blocks: tf.TensorArray) -> tf.Tensor:
        return col_start < num_particles

    def col_body(col_start: tf.Tensor, blocks_ta: tf.TensorArray):
        key_block = _slice_axis1_padded_3d(x, col_start, col_chunk_size)
        g_block = _slice_axis1_padded_2d(
            g,
            col_start,
            col_chunk_size,
            pad_value=float(_STREAMING_LOG_ZERO),
        )
        running = tf.fill(
            [batch_size, col_chunk_size],
            _streaming_log_zero(DTYPE),
        )

        def row_cond(row_start: tf.Tensor, _running: tf.Tensor) -> tf.Tensor:
            return row_start < num_particles

        def row_body(row_start: tf.Tensor, running_logsum: tf.Tensor):
            query_block = _slice_axis1_padded_3d(x, row_start, row_chunk_size)
            f_block = _slice_axis1_padded_2d(
                f,
                row_start,
                row_chunk_size,
                pad_value=float(_STREAMING_LOG_ZERO),
            )
            cost = 0.5 * _pairwise_squared_cross(query_block, key_block)
            logits = (
                f_block[:, :, None]
                + g_block[:, None, :]
                - cost
            ) / eps[:, None, None]
            block_logsum = tf.reduce_logsumexp(logits, axis=1)
            return row_start + row_chunk_tensor, _logaddexp(running_logsum, block_logsum)

        _, col_logsum = tf.while_loop(
            row_cond,
            row_body,
            loop_vars=(tf.constant(0, tf.int32), running),
            maximum_iterations=(num_particles + row_chunk_tensor - 1) // row_chunk_tensor,
        )
        block_index = col_start // col_chunk_tensor
        blocks_ta = blocks_ta.write(block_index, col_logsum)
        return col_start + col_chunk_tensor, blocks_ta

    _, blocks = tf.while_loop(
        col_cond,
        col_body,
        loop_vars=(tf.constant(0, tf.int32), blocks),
        maximum_iterations=num_col_blocks,
    )
    stacked = blocks.stack()
    transposed = tf.transpose(stacked, [1, 0, 2])
    flat = tf.reshape(transposed, [batch_size, num_col_blocks * col_chunk_tensor])
    return flat[:, :num_particles]


def _filterflow_streaming_transport_from_potentials(
    scaled_x: tf.Tensor,
    particles: tf.Tensor,
    f: tf.Tensor,
    g: tf.Tensor,
    eps: tf.Tensor,
    logw: tf.Tensor,
    float_n: tf.Tensor,
    *,
    row_chunk_size: int,
    col_chunk_size: int,
) -> tuple[tf.Tensor, tf.Tensor]:
    row_chunk_size = _validate_chunk_size(row_chunk_size, "row_chunk_size")
    col_chunk_size = _validate_chunk_size(col_chunk_size, "col_chunk_size")
    batch_size = tf.shape(scaled_x)[0]
    num_particles = tf.shape(scaled_x)[1]
    state_dim = tf.shape(particles)[2]
    eps = tf.reshape(tf.cast(eps, DTYPE), [-1])
    log_n = tf.math.log(float_n)
    column_log_norm = _filterflow_streaming_column_log_normalizer(
        scaled_x,
        f,
        g,
        eps,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    row_chunk_tensor = tf.cast(row_chunk_size, tf.int32)
    col_chunk_tensor = tf.cast(col_chunk_size, tf.int32)
    num_row_blocks = (num_particles + row_chunk_tensor - 1) // row_chunk_tensor
    num_col_blocks = (num_particles + col_chunk_tensor - 1) // col_chunk_tensor
    particle_blocks = tf.TensorArray(
        dtype=DTYPE,
        size=num_row_blocks,
        element_shape=tf.TensorShape([None, row_chunk_size, None]),
    )
    mass_blocks = tf.TensorArray(
        dtype=DTYPE,
        size=num_row_blocks,
        element_shape=tf.TensorShape([None, row_chunk_size]),
    )

    def row_cond(row_start: tf.Tensor, _particle_blocks, _mass_blocks) -> tf.Tensor:
        return row_start < num_particles

    def row_body(row_start: tf.Tensor, particle_ta: tf.TensorArray, mass_ta: tf.TensorArray):
        query_block = _slice_axis1_padded_3d(scaled_x, row_start, row_chunk_size)
        f_block = _slice_axis1_padded_2d(
            f,
            row_start,
            row_chunk_size,
            pad_value=float(_STREAMING_LOG_ZERO),
        )
        carried = tf.zeros([batch_size, row_chunk_size, state_dim], dtype=DTYPE)
        mass = tf.zeros([batch_size, row_chunk_size], dtype=DTYPE)

        def col_cond(col_start: tf.Tensor, _carried: tf.Tensor, _mass: tf.Tensor) -> tf.Tensor:
            return col_start < num_particles

        def col_body(col_start: tf.Tensor, carried_accum: tf.Tensor, mass_accum: tf.Tensor):
            key_block = _slice_axis1_padded_3d(scaled_x, col_start, col_chunk_size)
            particle_block = _slice_axis1_padded_3d(particles, col_start, col_chunk_size)
            g_block = _slice_axis1_padded_2d(
                g,
                col_start,
                col_chunk_size,
                pad_value=float(_STREAMING_LOG_ZERO),
            )
            logw_block = _slice_axis1_padded_2d(
                logw,
                col_start,
                col_chunk_size,
                pad_value=float(_STREAMING_LOG_ZERO),
            )
            norm_block = _slice_axis1_padded_2d(
                column_log_norm,
                col_start,
                col_chunk_size,
                pad_value=0.0,
            )
            cost = 0.5 * _pairwise_squared_cross(query_block, key_block)
            log_transport = (
                f_block[:, :, None]
                + g_block[:, None, :]
                - cost
            ) / eps[:, None, None]
            log_transport = (
                log_transport
                - norm_block[:, None, :]
                + log_n
                + logw_block[:, None, :]
            )
            transport_block = tf.exp(log_transport)
            carried_next = carried_accum + tf.matmul(transport_block, particle_block)
            mass_next = mass_accum + tf.reduce_sum(transport_block, axis=2)
            return col_start + col_chunk_tensor, carried_next, mass_next

        _, carried, mass = tf.while_loop(
            col_cond,
            col_body,
            loop_vars=(tf.constant(0, tf.int32), carried, mass),
            maximum_iterations=num_col_blocks,
        )
        block_index = row_start // row_chunk_tensor
        particle_ta = particle_ta.write(block_index, carried)
        mass_ta = mass_ta.write(block_index, mass)
        return row_start + row_chunk_tensor, particle_ta, mass_ta

    _, particle_blocks, mass_blocks = tf.while_loop(
        row_cond,
        row_body,
        loop_vars=(tf.constant(0, tf.int32), particle_blocks, mass_blocks),
        maximum_iterations=num_row_blocks,
    )
    stacked_particles = particle_blocks.stack()
    transposed_particles = tf.transpose(stacked_particles, [1, 0, 2, 3])
    transported = tf.reshape(
        transposed_particles,
        [batch_size, num_row_blocks * row_chunk_tensor, state_dim],
    )[:, :num_particles, :]
    stacked_mass = mass_blocks.stack()
    transposed_mass = tf.transpose(stacked_mass, [1, 0, 2])
    row_mass = tf.reshape(
        transposed_mass,
        [batch_size, num_row_blocks * row_chunk_tensor],
    )[:, :num_particles]
    row_residual = tf.reduce_max(tf.abs(row_mass - 1.0))
    return transported, tf.cast(row_residual, DTYPE)


def _filterflow_streaming_transport(
    scaled_x: tf.Tensor,
    particles: tf.Tensor,
    logw: tf.Tensor,
    eps: tf.Tensor,
    scaling: tf.Tensor,
    threshold: tf.Tensor,
    max_iter: tf.Tensor,
    n: tf.Tensor,
    *,
    row_chunk_size: int,
    col_chunk_size: int,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    float_n = tf.cast(n, DTYPE)
    log_n = tf.math.log(float_n)
    uniform_log_weight = -log_n * tf.ones_like(logw)
    alpha, beta, _, _, iterations = _filterflow_streaming_sinkhorn_potentials(
        logw,
        scaled_x,
        uniform_log_weight,
        scaled_x,
        eps,
        scaling,
        threshold,
        max_iter,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    transported, row_residual = _filterflow_streaming_transport_from_potentials(
        scaled_x,
        particles,
        alpha,
        beta,
        eps,
        logw,
        float_n,
        row_chunk_size=row_chunk_size,
        col_chunk_size=col_chunk_size,
    )
    column_residual = tf.constant(0.0, DTYPE)
    return transported, iterations, row_residual, column_residual


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
        loop_vars=(
            n_iter,
            a_y_init,
            b_x_init,
            a_x_init,
            b_y_init,
            continue_flag,
            epsilon_0,
        ),
        maximum_iterations=max_iter,
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
