from __future__ import annotations

import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import tensorflow as tf

from experiments.dpf_implementation.tf_tfp.filters import experimental_batched_ledh_pfpf_ot_tf as ledh


DTYPE = tf.float64
ledh.DTYPE = DTYPE
ATOL = 2.0e-8


def _assert_near(lhs: tf.Tensor, rhs: tf.Tensor, *, atol: float = ATOL) -> None:
    tf.debugging.assert_near(
        tf.convert_to_tensor(lhs, DTYPE),
        tf.convert_to_tensor(rhs, DTYPE),
        atol=atol,
        rtol=atol,
    )


def _spd_batch(batch_size: int, dim: int, *, start: float) -> tf.Tensor:
    count = batch_size * dim * dim
    raw = tf.reshape(
        tf.linspace(tf.constant(start, DTYPE), tf.constant(start + 0.4, DTYPE), count),
        [batch_size, dim, dim],
    )
    matrix = tf.matmul(raw, raw, transpose_b=True)
    return matrix + tf.eye(dim, dtype=DTYPE)[None, :, :] * tf.constant(0.75, DTYPE)


def _cotangent(shape: tuple[int, ...], *, scale: float = 0.07) -> tf.Tensor:
    count = 1
    for dim in shape:
        count *= dim
    return tf.reshape(
        tf.linspace(tf.constant(-scale, DTYPE), tf.constant(scale, DTYPE), count),
        shape,
    )


def test_p5_gaussian_logpdf_vjp_matches_tiny_autodiff() -> None:
    residuals = tf.reshape(
        tf.linspace(tf.constant(-0.35, DTYPE), tf.constant(0.45, DTYPE), 12),
        [2, 3, 2],
    )
    covariance = _spd_batch(2, 2, start=0.1)
    upstream = _cotangent((2, 3), scale=0.11)

    manual_residuals, manual_covariance = ledh._batched_gaussian_logpdf_vjp(  # noqa: SLF001
        residuals,
        covariance,
        upstream,
    )

    with tf.GradientTape() as tape:
        tape.watch([residuals, covariance])
        value = ledh._batched_gaussian_logpdf(residuals, covariance)  # noqa: SLF001
        objective = tf.reduce_sum(value * upstream)
    auto_residuals, auto_covariance = tape.gradient(objective, [residuals, covariance])

    _assert_near(manual_residuals, auto_residuals)
    _assert_near(manual_covariance, auto_covariance)


def test_p5_log_normalization_and_floor_vjp_matches_tiny_autodiff() -> None:
    corrected = tf.constant(
        [[-1.5, -0.1, 0.2, 1.1], [-2.0, -1.6, -0.4, 0.7]],
        dtype=DTYPE,
    )
    upstream_logw = _cotangent((2, 4), scale=0.09)
    upstream_incremental = tf.constant([0.4, -0.2], dtype=DTYPE)
    floor = tf.constant(0.18, dtype=DTYPE)

    manual, weights, incremental, active = ledh._normalize_log_weights_with_floor_vjp(  # noqa: SLF001
        corrected,
        upstream_logw,
        upstream_incremental,
        floor=floor,
    )

    with tf.GradientTape() as tape:
        tape.watch(corrected)
        tape_weights, tape_incremental = ledh._normalize_log_weights(corrected)  # noqa: SLF001
        floored = tf.math.log(tf.maximum(tape_weights, floor))
        objective = (
            tf.reduce_sum(floored * upstream_logw)
            + tf.reduce_sum(tape_incremental * upstream_incremental)
        )
    auto = tape.gradient(objective, corrected)

    _assert_near(weights, tape_weights)
    _assert_near(incremental, tape_incremental)
    _assert_near(manual, auto)
    tf.debugging.assert_equal(active, weights > floor)


def test_p5_named_transition_observation_log_density_vjps_match_tiny_autodiff() -> None:
    x_next = tf.reshape(
        tf.linspace(tf.constant(-0.2, DTYPE), tf.constant(0.4, DTYPE), 12),
        [2, 3, 2],
    )
    transition_mean = x_next * tf.constant(0.4, DTYPE) - tf.constant(0.05, DTYPE)
    predicted_observation = tf.reshape(
        tf.linspace(tf.constant(0.1, DTYPE), tf.constant(-0.3, DTYPE), 12),
        [2, 3, 2],
    )
    observation = tf.constant([[0.04, -0.10], [0.12, -0.05]], dtype=DTYPE)
    transition_covariance = _spd_batch(2, 2, start=0.3)
    observation_covariance = _spd_batch(2, 2, start=0.5)
    transition_upstream = _cotangent((2, 3), scale=0.06)
    observation_upstream = _cotangent((2, 3), scale=0.08)

    transition_manual = ledh._transition_gaussian_log_density_vjp(  # noqa: SLF001
        x_next,
        transition_mean,
        transition_covariance,
        transition_upstream,
    )
    observation_manual = ledh._observation_gaussian_log_density_vjp(  # noqa: SLF001
        predicted_observation,
        observation,
        observation_covariance,
        observation_upstream,
        residual_convention="model_minus_observation",
    )

    with tf.GradientTape() as tape:
        tape.watch([x_next, transition_mean, transition_covariance])
        transition_value = ledh._batched_gaussian_logpdf(  # noqa: SLF001
            x_next - transition_mean,
            transition_covariance,
        )
        transition_objective = tf.reduce_sum(transition_value * transition_upstream)
    transition_auto = tape.gradient(
        transition_objective,
        [x_next, transition_mean, transition_covariance],
    )

    with tf.GradientTape() as tape:
        tape.watch([predicted_observation, observation, observation_covariance])
        observation_value = ledh._batched_gaussian_logpdf(  # noqa: SLF001
            predicted_observation - observation[:, None, :],
            observation_covariance,
        )
        observation_objective = tf.reduce_sum(observation_value * observation_upstream)
    observation_auto = tape.gradient(
        observation_objective,
        [predicted_observation, observation, observation_covariance],
    )

    _assert_near(transition_manual["x_next"], transition_auto[0])
    _assert_near(transition_manual["transition_mean"], transition_auto[1])
    _assert_near(transition_manual["transition_covariance"], transition_auto[2])
    _assert_near(observation_manual["predicted_observation"], observation_auto[0])
    _assert_near(observation_manual["observation"], observation_auto[1])
    _assert_near(observation_manual["observation_covariance"], observation_auto[2])


def test_p5_log_weight_correction_vjp_signs() -> None:
    upstream = tf.constant([[0.1, -0.2, 0.3]], dtype=DTYPE)

    cotangents = ledh._log_weight_correction_vjp(upstream)  # noqa: SLF001

    _assert_near(cotangents["current_log_weights"], upstream)
    _assert_near(cotangents["transition_log_density"], upstream)
    _assert_near(cotangents["observation_log_density"], upstream)
    _assert_near(cotangents["pre_flow_log_density"], -upstream)
    _assert_near(cotangents["forward_log_det"], upstream)


def test_p5_observation_difference_residual_vjp_conventions() -> None:
    upstream = tf.reshape(
        tf.linspace(tf.constant(-0.2, DTYPE), tf.constant(0.3, DTYPE), 12),
        [2, 3, 2],
    )

    bar_h, bar_obs = ledh._observation_difference_residual_vjp(  # noqa: SLF001
        upstream,
        convention="model_minus_observation",
    )
    _assert_near(bar_h, upstream)
    _assert_near(bar_obs, -tf.reduce_sum(upstream, axis=1))

    bar_h, bar_obs = ledh._observation_difference_residual_vjp(  # noqa: SLF001
        upstream,
        convention="observation_minus_model",
    )
    _assert_near(bar_h, -upstream)
    _assert_near(bar_obs, tf.reduce_sum(upstream, axis=1))


def test_p5_linearized_ledh_flow_vjp_matches_tiny_autodiff() -> None:
    x0 = tf.reshape(
        tf.linspace(tf.constant(-0.25, DTYPE), tf.constant(0.50, DTYPE), 12),
        [2, 3, 2],
    )
    prior_means = x0 * tf.constant(0.35, DTYPE) + tf.constant(0.08, DTYPE)
    observation_jacobian = tf.reshape(
        tf.linspace(tf.constant(-0.2, DTYPE), tf.constant(0.3, DTYPE), 24),
        [2, 3, 2, 2],
    )
    observation_residual = tf.reshape(
        tf.linspace(tf.constant(0.15, DTYPE), tf.constant(-0.10, DTYPE), 12),
        [2, 3, 2],
    )
    transition_covariance = _spd_batch(2, 2, start=0.2)
    observation_covariance = _spd_batch(2, 2, start=0.4)
    bar_post = _cotangent((2, 3, 2), scale=0.05)
    bar_pre_log = _cotangent((2, 3), scale=0.07)
    bar_logdet = _cotangent((2, 3), scale=0.03)

    flow, aux = ledh._batched_ledh_linearized_flow_with_aux_tf(  # noqa: SLF001
        pre_flow_particles=x0,
        prior_means=prior_means,
        observation_jacobian=observation_jacobian,
        observation_residual=observation_residual,
        transition_covariance=transition_covariance,
        observation_covariance=observation_covariance,
    )
    manual = ledh._batched_ledh_linearized_flow_vjp(  # noqa: SLF001
        aux,
        bar_post,
        bar_pre_log,
        bar_logdet,
    )

    with tf.GradientTape() as tape:
        tape.watch(
            [
                x0,
                prior_means,
                observation_jacobian,
                observation_residual,
                transition_covariance,
                observation_covariance,
            ]
        )
        tape_flow, _ = ledh._batched_ledh_linearized_flow_with_aux_tf(  # noqa: SLF001
            pre_flow_particles=x0,
            prior_means=prior_means,
            observation_jacobian=observation_jacobian,
            observation_residual=observation_residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        objective = (
            tf.reduce_sum(tape_flow.post_flow_particles * bar_post)
            + tf.reduce_sum(tape_flow.pre_flow_log_density * bar_pre_log)
            + tf.reduce_sum(tape_flow.forward_log_det * bar_logdet)
        )
    auto = tape.gradient(
        objective,
        [
            x0,
            prior_means,
            observation_jacobian,
            observation_residual,
            transition_covariance,
            observation_covariance,
        ],
    )

    _assert_near(flow.post_flow_particles, tape_flow.post_flow_particles)
    _assert_near(flow.pre_flow_log_density, tape_flow.pre_flow_log_density)
    _assert_near(flow.forward_log_det, tape_flow.forward_log_det)
    _assert_near(manual.pre_flow_particles, auto[0], atol=5.0e-8)
    _assert_near(manual.prior_means, auto[1], atol=5.0e-8)
    _assert_near(manual.observation_jacobian, auto[2], atol=5.0e-8)
    _assert_near(manual.observation_residual, auto[3], atol=5.0e-8)
    _assert_near(manual.transition_covariance, auto[4], atol=5.0e-8)
    _assert_near(manual.observation_covariance, auto[5], atol=5.0e-8)
