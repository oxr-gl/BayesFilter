from __future__ import annotations

import json
import os
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf


DTYPE = tf.float64
TAPE_ATOL = 1.0e-8
FD_ATOL = 5.0e-5
NEGATIVE_MIN_GAP = 1.0e-6
FD_STEP = tf.constant(1.0e-5, DTYPE)


def _fixture() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    particles = tf.reshape(
        tf.linspace(tf.constant(-0.45, DTYPE), tf.constant(0.55, DTYPE), 6),
        [1, 3, 2],
    )
    scaled_x = particles + tf.constant([[[0.02, -0.01], [0.00, 0.015], [-0.015, 0.005]]], DTYPE)
    raw_logw = tf.constant([[-0.35, 0.05, 0.25]], dtype=DTYPE)
    logw = raw_logw - tf.reduce_logsumexp(raw_logw, axis=1, keepdims=True)
    epsilon = tf.constant(0.45, DTYPE)
    epsilon0 = tf.constant([0.9], DTYPE)
    scaling = tf.constant(0.8, DTYPE)
    return scaled_x, particles, logw, epsilon, epsilon0, scaling


def _upstream() -> tf.Tensor:
    return tf.reshape(
        tf.linspace(tf.constant(-0.03, DTYPE), tf.constant(0.025, DTYPE), 6),
        [1, 3, 2],
    )


def _tangent_like(value: tf.Tensor, scale: float) -> tf.Tensor:
    count = int(tf.size(value).numpy())
    return tf.reshape(
        tf.linspace(tf.constant(-scale, DTYPE), tf.constant(scale, DTYPE), count),
        tf.shape(value),
    )


def _value_scalar(
    scaled_x: tf.Tensor,
    particles: tf.Tensor,
    logw: tf.Tensor,
    epsilon: tf.Tensor,
    epsilon0: tf.Tensor,
    scaling: tf.Tensor,
) -> tf.Tensor:
    transported, _ = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_value_total_vjp(  # noqa: SLF001
            scaled_x,
            particles,
            logw,
            epsilon,
            epsilon0,
            scaling,
            steps=2,
            row_chunk_size=2,
            col_chunk_size=2,
        )
    )
    return tf.reduce_sum(transported * _upstream())


def _custom_scalar(
    scaled_x: tf.Tensor,
    particles: tf.Tensor,
    logw: tf.Tensor,
    epsilon: tf.Tensor,
    epsilon0: tf.Tensor,
    scaling: tf.Tensor,
) -> tf.Tensor:
    transported, _ = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_total_vjp(  # noqa: SLF001
            scaled_x,
            particles,
            logw,
            epsilon,
            epsilon0,
            scaling,
            steps=2,
            row_chunk_size=2,
            col_chunk_size=2,
        )
    )
    return tf.reduce_sum(transported * _upstream())


def _stopped_scalar(
    scaled_x: tf.Tensor,
    particles: tf.Tensor,
    logw: tf.Tensor,
    epsilon: tf.Tensor,
    epsilon0: tf.Tensor,
    scaling: tf.Tensor,
) -> tf.Tensor:
    transported, _ = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_stopped_scale_keys(  # noqa: SLF001
            scaled_x,
            particles,
            logw,
            epsilon,
            epsilon0,
            scaling,
            steps=2,
            row_chunk_size=2,
            col_chunk_size=2,
        )
    )
    return tf.reduce_sum(transported * _upstream())


def _gradients(scalar_fn) -> tuple[tf.Tensor, ...]:
    scaled_x, particles, logw, epsilon, epsilon0, scaling = _fixture()
    inputs = [scaled_x, particles, logw, epsilon0]
    with tf.GradientTape() as tape:
        tape.watch(inputs)
        scalar = scalar_fn(scaled_x, particles, logw, epsilon, epsilon0, scaling)
    return tuple(
        tape.gradient(
            scalar,
            inputs,
            unconnected_gradients=tf.UnconnectedGradients.ZERO,
        )
    )


def _max_abs(lhs: tf.Tensor, rhs: tf.Tensor) -> float:
    return float(tf.reduce_max(tf.abs(tf.cast(lhs, DTYPE) - tf.cast(rhs, DTYPE))).numpy())


def _directional_fd(input_name: str, tangent: tf.Tensor) -> float:
    scaled_x, particles, logw, epsilon, epsilon0, scaling = _fixture()
    h = FD_STEP
    if input_name == "scaled_x":
        plus = _value_scalar(scaled_x + h * tangent, particles, logw, epsilon, epsilon0, scaling)
        minus = _value_scalar(scaled_x - h * tangent, particles, logw, epsilon, epsilon0, scaling)
    elif input_name == "particles":
        plus = _value_scalar(scaled_x, particles + h * tangent, logw, epsilon, epsilon0, scaling)
        minus = _value_scalar(scaled_x, particles - h * tangent, logw, epsilon, epsilon0, scaling)
    elif input_name == "logw":
        plus = _value_scalar(scaled_x, particles, logw + h * tangent, epsilon, epsilon0, scaling)
        minus = _value_scalar(scaled_x, particles, logw - h * tangent, epsilon, epsilon0, scaling)
    elif input_name == "epsilon0":
        plus = _value_scalar(scaled_x, particles, logw, epsilon, epsilon0 + h * tangent, scaling)
        minus = _value_scalar(scaled_x, particles, logw, epsilon, epsilon0 - h * tangent, scaling)
    else:
        raise ValueError(input_name)
    return float(((plus - minus) / (2.0 * h)).numpy())


def collect_phase2_diagnostics() -> dict[str, Any]:
    old_dtype = annealed_transport_tf.DTYPE
    annealed_transport_tf.DTYPE = DTYPE
    try:
        scaled_x, particles, logw, epsilon, epsilon0, scaling = _fixture()
        tape_grads = _gradients(_value_scalar)
        custom_grads = _gradients(_custom_scalar)
        stopped_grads = _gradients(_stopped_scalar)
        names = ("scaled_x", "particles", "logw", "epsilon0")
        values = (scaled_x, particles, logw, epsilon0)
        tangents = (
            _tangent_like(scaled_x, 0.013),
            _tangent_like(particles, 0.011),
            _tangent_like(logw, 0.017),
            tf.constant([0.019], DTYPE),
        )
        tape_errors = {
            name: _max_abs(custom, taped)
            for name, custom, taped in zip(names, custom_grads, tape_grads, strict=True)
        }
        fd_errors = {}
        fd_values = {}
        vjp_dots = {}
        for name, value, tangent, grad in zip(names, values, tangents, custom_grads, strict=True):
            del value
            fd = _directional_fd(name, tangent)
            dot = float(tf.reduce_sum(grad * tangent).numpy())
            fd_values[name] = fd
            vjp_dots[name] = dot
            fd_errors[name] = abs(fd - dot)
        stopped_gaps = {
            name: _max_abs(stopped, taped)
            for name, stopped, taped in zip(names, stopped_grads, tape_grads, strict=True)
        }
        same_scalar_value_gap = abs(
            float(
                (
                    _custom_scalar(scaled_x, particles, logw, epsilon, epsilon0, scaling)
                    - _value_scalar(scaled_x, particles, logw, epsilon, epsilon0, scaling)
                ).numpy()
            )
        )
        return {
            "route": "manual_streaming_total_finite_sinkhorn_no_tape_candidate",
            "dtype": "float64",
            "execution_class": "cpu_tiny_primitive_validation",
            "steps": 2,
            "row_chunk_size": 2,
            "col_chunk_size": 2,
            "tolerances": {
                "tape_atol": TAPE_ATOL,
                "fd_atol": FD_ATOL,
                "negative_min_gap": NEGATIVE_MIN_GAP,
                "fd_step": float(FD_STEP.numpy()),
            },
            "same_scalar_value_gap": same_scalar_value_gap,
            "tape_max_abs_errors": tape_errors,
            "fd_directional_values": fd_values,
            "vjp_directional_values": vjp_dots,
            "fd_directional_abs_errors": fd_errors,
            "stopped_route_vs_total_tape_max_abs_gaps": stopped_gaps,
            "max_tape_error": max(tape_errors.values()),
            "max_fd_error": max(fd_errors.values()),
            "max_stopped_gap": max(stopped_gaps.values()),
            "epsilon0_total_tape_gradient": float(tape_grads[3][0].numpy()),
            "epsilon0_custom_gradient": float(custom_grads[3][0].numpy()),
            "epsilon0_stopped_gradient": float(stopped_grads[3][0].numpy()),
            "nonclaims": [
                "no_p8p_regression_admission",
                "no_lgssm_score_admission",
                "no_gpu_xla_evidence",
                "no_hmc_readiness",
            ],
        }
    finally:
        annealed_transport_tf.DTYPE = old_dtype


def test_no_tape_total_transport_vjp_matches_same_scalar_tape_and_fd() -> None:
    diagnostics = collect_phase2_diagnostics()

    assert diagnostics["same_scalar_value_gap"] <= TAPE_ATOL
    assert diagnostics["max_tape_error"] <= TAPE_ATOL
    assert diagnostics["max_fd_error"] <= FD_ATOL


def test_stopped_route_fails_unstopped_total_derivative_target() -> None:
    diagnostics = collect_phase2_diagnostics()

    assert diagnostics["stopped_route_vs_total_tape_max_abs_gaps"]["epsilon0"] > NEGATIVE_MIN_GAP
    assert diagnostics["max_stopped_gap"] > NEGATIVE_MIN_GAP


if __name__ == "__main__":
    print(json.dumps(collect_phase2_diagnostics(), indent=2, sort_keys=True))
