from __future__ import annotations

import ast
import math
import os
import inspect
import textwrap

import pytest

RUN_FULL_N1000 = os.environ.get("BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000") == "1"
if not RUN_FULL_N1000:
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from bayesfilter.linear.experimental_batched_kalman_tf import (
    tf_batched_kalman_value_and_score,
)
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as core_ledh,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf


DTYPE = tf.float32
SEED_COUNT = 10
NUM_PARTICLES = int(os.environ.get("BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES", "1000"))
TIME_STEPS = 10
SINKHORN_ITERATIONS = 8
SINKHORN_EPSILON = 0.5
ANNEALED_SCALING = 0.9
ROW_CHUNK_SIZE = NUM_PARTICLES
COL_CHUNK_SIZE = NUM_PARTICLES
PARTICLE_CHUNK_SIZE = NUM_PARTICLES
THETA = tf.constant([0.72, math.log(0.22), math.log(0.30)], dtype=DTYPE)
FULL_N1000_MARK = pytest.mark.skipif(
    not RUN_FULL_N1000,
    reason=(
        "N=1000+ active-all LEDH-PFPF-OT LGSSM statistical regression is opt-in and "
        "compile-heavy by design; "
        "set BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000=1 and "
        "optionally BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES=<N>, "
        "BAYESFILTER_TEST_DEVICE_SCOPE=visible, then run with trusted GPU visibility "
        "for the full check."
    ),
)
pytestmark = [
    pytest.mark.extended,
    pytest.mark.gpu,
]

core_ledh.DTYPE = DTYPE
annealed_transport_tf.DTYPE = DTYPE
tf.config.experimental.enable_tensor_float_32_execution(True)


def _observations(state_dim: int) -> tf.Tensor:
    time = tf.cast(tf.range(TIME_STEPS), DTYPE)
    if state_dim == 1:
        return tf.reshape(0.18 * tf.sin(0.7 * time) + 0.04 * tf.cos(1.3 * time), [-1, 1])
    return tf.stack(
        [
            0.18 * tf.sin(0.7 * time) + 0.04 * tf.cos(1.3 * time),
            -0.12 * tf.cos(0.5 * time) + 0.05 * tf.sin(1.1 * time),
        ],
        axis=1,
    )


def _theta_to_lgssm(values: tf.Tensor, state_dim: int) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    batch_size = values.shape[0]
    if batch_size is None:
        raise ValueError("test requires static seed batch size")
    eye = tf.eye(state_dim, dtype=DTYPE)[None, :, :]
    transition_matrix = values[:, 0, None, None] * tf.tile(eye, [batch_size, 1, 1])
    transition_covariance = tf.exp(values[:, 1])[:, None, None] * tf.tile(
        eye,
        [batch_size, 1, 1],
    )
    observation_covariance = tf.exp(values[:, 2])[:, None, None] * tf.tile(
        eye,
        [batch_size, 1, 1],
    )
    return transition_matrix, transition_covariance, observation_covariance


def _diag_gaussian_logpdf(residual: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    variance = tf.linalg.diag_part(covariance)
    state_dim = residual.shape[-1]
    if state_dim is None:
        raise ValueError("test requires static state dimension")
    quad = tf.reduce_sum(tf.square(residual) / variance[:, None, :], axis=-1)
    log_det = tf.reduce_sum(tf.math.log(variance), axis=-1)
    return -0.5 * (
        tf.cast(state_dim, DTYPE) * tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
        + log_det[:, None]
        + quad
    )


def _stateless_seeded_normals(state_dim: int, seed_index: int) -> tuple[tf.Tensor, tf.Tensor]:
    seed = 9100 + seed_index
    initial_draws = tf.random.stateless_normal(
        [1, NUM_PARTICLES, state_dim],
        seed=tf.constant([seed, 17], dtype=tf.int32),
        dtype=DTYPE,
    )
    transition_draws = tf.random.stateless_normal(
        [1, TIME_STEPS, NUM_PARTICLES, state_dim],
        seed=tf.constant([seed, 29], dtype=tf.int32),
        dtype=DTYPE,
    )
    return initial_draws, transition_draws


def _stateless_seeded_normals_batch(state_dim: int) -> tuple[tf.Tensor, tf.Tensor]:
    seed_indices = tf.range(SEED_COUNT, dtype=tf.int32) + tf.constant(9100, dtype=tf.int32)
    initial_seeds = tf.stack(
        [seed_indices, tf.fill([SEED_COUNT], tf.constant(17, dtype=tf.int32))],
        axis=1,
    )
    transition_seeds = tf.stack(
        [seed_indices, tf.fill([SEED_COUNT], tf.constant(29, dtype=tf.int32))],
        axis=1,
    )
    initial_draws = tf.map_fn(
        lambda seed: tf.random.stateless_normal(
            [NUM_PARTICLES, state_dim],
            seed=seed,
            dtype=DTYPE,
        ),
        initial_seeds,
        fn_output_signature=tf.TensorSpec([NUM_PARTICLES, state_dim], DTYPE),
    )
    transition_draws = tf.map_fn(
        lambda seed: tf.random.stateless_normal(
            [TIME_STEPS, NUM_PARTICLES, state_dim],
            seed=seed,
            dtype=DTYPE,
        ),
        transition_seeds,
        fn_output_signature=tf.TensorSpec([TIME_STEPS, NUM_PARTICLES, state_dim], DTYPE),
    )
    return initial_draws, transition_draws


def _observation_fn(points: tf.Tensor) -> tf.Tensor:
    return points


def _observation_jacobian_fn(points: tf.Tensor) -> tf.Tensor:
    batch_size, num_particles, state_dim = points.shape
    if batch_size is None or num_particles is None or state_dim is None:
        raise ValueError("test requires static particle dimensions")
    eye = tf.eye(state_dim, dtype=DTYPE)
    return tf.tile(eye[None, None, :, :], [batch_size, num_particles, 1, 1])


def _observation_residual_fn(h_ref: tf.Tensor, observation: tf.Tensor) -> tf.Tensor:
    return observation[None, None, :] - h_ref


def _transport_forward(
    post_flow: tf.Tensor,
    normalized_log_weights: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    batch_size, num_particles, _state_dim = core_ledh._static_shape(post_flow, "post_flow")
    center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
    scale = tf.stop_gradient(annealed_transport_tf._filterflow_scale(post_flow))
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon = tf.constant(SINKHORN_EPSILON, dtype=DTYPE)
    epsilon0 = tf.stop_gradient(annealed_transport_tf._filterflow_epsilon_start(scaled_x))
    transported, _row_residual = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_stopped_scale_keys(
            scaled_x,
            post_flow,
            normalized_log_weights,
            epsilon,
            epsilon0,
            tf.constant(ANNEALED_SCALING, dtype=DTYPE),
            steps=core_ledh._manual_dense_finite_steps(SINKHORN_ITERATIONS),
            row_chunk_size=ROW_CHUNK_SIZE,
            col_chunk_size=COL_CHUNK_SIZE,
        )
    )
    return transported, core_ledh.uniform_log_weights(batch_size, num_particles)


def _transport_vjp(
    post_flow: tf.Tensor,
    normalized_log_weights: tf.Tensor,
    upstream_particles: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
    scale = tf.stop_gradient(annealed_transport_tf._filterflow_scale(post_flow))
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon = tf.constant(SINKHORN_EPSILON, dtype=DTYPE)
    epsilon0 = tf.stop_gradient(annealed_transport_tf._filterflow_epsilon_start(scaled_x))
    scaling = tf.constant(ANNEALED_SCALING, dtype=DTYPE)
    steps = core_ledh._manual_dense_finite_steps(SINKHORN_ITERATIONS)
    float_n = tf.cast(tf.shape(post_flow)[1], DTYPE)
    uniform_log_weight = -tf.math.log(float_n) * tf.ones_like(normalized_log_weights)
    alpha, beta = (
        annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_stopped_scale_keys(
            normalized_log_weights,
            uniform_log_weight,
            scaled_x,
            epsilon,
            epsilon0,
            scaling,
            steps=steps,
            row_chunk_size=ROW_CHUNK_SIZE,
            col_chunk_size=COL_CHUNK_SIZE,
        )
    )
    (
        d_scaled_x_transport,
        d_particles,
        d_alpha,
        d_beta,
        d_logw_transport,
    ) = annealed_transport_tf._filterflow_streaming_transport_from_potentials_vjp(
        scaled_x,
        post_flow,
        alpha,
        beta,
        epsilon,
        normalized_log_weights,
        float_n,
        upstream_particles,
        row_chunk_size=ROW_CHUNK_SIZE,
        col_chunk_size=COL_CHUNK_SIZE,
    )
    (
        d_log_alpha,
        _d_log_beta,
        d_scaled_x_sinkhorn,
    ) = annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys(
        normalized_log_weights,
        uniform_log_weight,
        scaled_x,
        d_alpha,
        d_beta,
        epsilon,
        epsilon0,
        scaling,
        steps=steps,
        row_chunk_size=ROW_CHUNK_SIZE,
        col_chunk_size=COL_CHUNK_SIZE,
    )
    d_post_flow = d_particles + (d_scaled_x_transport + d_scaled_x_sinkhorn) / scale[:, None, None]
    return d_post_flow, d_logw_transport + d_log_alpha


def _lgssm_manual_value_and_score(
    values: tf.Tensor,
    state_dim: int,
    initial_particles: tf.Tensor,
    transition_noise: tf.Tensor,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    batch_size = values.shape[0]
    if batch_size is None:
        raise ValueError("test requires static seed batch size")
    transition_matrix, transition_covariance, observation_covariance = _theta_to_lgssm(
        values,
        state_dim,
    )
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    observation_matrix = tf.eye(state_dim, dtype=DTYPE)
    h_jac = tf.tile(
        observation_matrix[None, None, :, :],
        [batch_size, NUM_PARTICLES, 1, 1],
    )
    particles = initial_particles
    log_weights = core_ledh.uniform_log_weights(batch_size, NUM_PARTICLES)
    log_likelihood = tf.zeros([batch_size], dtype=DTYPE)

    def new_ta(element_shape: list[int]) -> tf.TensorArray:
        return tf.TensorArray(
            dtype=DTYPE,
            size=TIME_STEPS,
            element_shape=tf.TensorShape(element_shape),
            clear_after_read=False,
        )

    batch_particles_shape = [batch_size, NUM_PARTICLES, state_dim]
    batch_weights_shape = [batch_size, NUM_PARTICLES]
    batch_matrix_shape = [batch_size, state_dim, state_dim]
    batch_particle_matrix_shape = [batch_size, NUM_PARTICLES, state_dim, state_dim]

    ancestors_ta = new_ta(batch_particles_shape)
    noise_ta = new_ta(batch_particles_shape)
    post_flow_ta = new_ta(batch_particles_shape)
    corrected_log_weights_ta = new_ta(batch_weights_shape)
    normalized_log_weights_ta = new_ta(batch_weights_shape)
    aux_x0_ta = new_ta(batch_particles_shape)
    aux_prior_means_ta = new_ta(batch_particles_shape)
    aux_observation_jacobian_ta = new_ta(batch_particle_matrix_shape)
    aux_observation_residual_ta = new_ta(batch_particles_shape)
    aux_transition_covariance_ta = new_ta(batch_matrix_shape)
    aux_observation_covariance_ta = new_ta(batch_matrix_shape)
    aux_transition_covariance_stable_ta = new_ta(batch_matrix_shape)
    aux_observation_covariance_stable_ta = new_ta(batch_matrix_shape)
    aux_prior_chol_ta = new_ta(batch_matrix_shape)
    aux_prior_precision_ta = new_ta(batch_matrix_shape)
    aux_obs_precision_ta = new_ta(batch_matrix_shape)
    aux_pseudo_observation_ta = new_ta(batch_particles_shape)
    aux_post_precision_ta = new_ta(batch_particle_matrix_shape)
    aux_post_precision_stable_ta = new_ta(batch_particle_matrix_shape)
    aux_post_covariance_unstabilized_ta = new_ta(batch_particle_matrix_shape)
    aux_post_covariance_ta = new_ta(batch_particle_matrix_shape)
    aux_post_chol_ta = new_ta(batch_particle_matrix_shape)
    aux_prior_inv_ta = new_ta(batch_matrix_shape)
    aux_affine_transform_ta = new_ta(batch_particle_matrix_shape)
    aux_delta_ta = new_ta(batch_particles_shape)
    aux_info_ta = new_ta(batch_particles_shape)

    def forward_cond(
        time_index: tf.Tensor,
        *_loop_vars: object,
    ) -> tf.Tensor:
        return time_index < tf.constant(TIME_STEPS, dtype=tf.int32)

    def forward_body(
        time_index: tf.Tensor,
        current_particles: tf.Tensor,
        current_log_weights: tf.Tensor,
        current_log_likelihood: tf.Tensor,
        ancestors_acc: tf.TensorArray,
        noise_acc: tf.TensorArray,
        post_flow_acc: tf.TensorArray,
        corrected_log_weights_acc: tf.TensorArray,
        normalized_log_weights_acc: tf.TensorArray,
        aux_x0_acc: tf.TensorArray,
        aux_prior_means_acc: tf.TensorArray,
        aux_observation_jacobian_acc: tf.TensorArray,
        aux_observation_residual_acc: tf.TensorArray,
        aux_transition_covariance_acc: tf.TensorArray,
        aux_observation_covariance_acc: tf.TensorArray,
        aux_transition_covariance_stable_acc: tf.TensorArray,
        aux_observation_covariance_stable_acc: tf.TensorArray,
        aux_prior_chol_acc: tf.TensorArray,
        aux_prior_precision_acc: tf.TensorArray,
        aux_obs_precision_acc: tf.TensorArray,
        aux_pseudo_observation_acc: tf.TensorArray,
        aux_post_precision_acc: tf.TensorArray,
        aux_post_precision_stable_acc: tf.TensorArray,
        aux_post_covariance_unstabilized_acc: tf.TensorArray,
        aux_post_covariance_acc: tf.TensorArray,
        aux_post_chol_acc: tf.TensorArray,
        aux_prior_inv_acc: tf.TensorArray,
        aux_affine_transform_acc: tf.TensorArray,
        aux_delta_acc: tf.TensorArray,
        aux_info_acc: tf.TensorArray,
    ):
        observation = observations[time_index]
        ancestors = current_particles
        prior_mean = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
        noise = transition_noise[:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        residual = observation[None, None, :] - pre_flow
        flow, flow_aux = core_ledh._batched_ledh_linearized_flow_with_aux_tf(
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = _diag_gaussian_logpdf(
            post_flow - prior_mean,
            transition_covariance,
        )
        observation_log_density = _diag_gaussian_logpdf(
            post_flow - observation[None, None, :],
            observation_covariance,
        )
        corrected_log_weights = (
            current_log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, incremental = core_ledh._normalize_log_weights(corrected_log_weights)
        next_log_likelihood = current_log_likelihood + incremental
        normalized_log_weights = tf.math.log(
            tf.maximum(weights, core_ledh._log_weight_floor())
        )
        next_particles, next_log_weights = _transport_forward(post_flow, normalized_log_weights)
        return (
            time_index + 1,
            next_particles,
            next_log_weights,
            next_log_likelihood,
            ancestors_acc.write(time_index, ancestors),
            noise_acc.write(time_index, noise),
            post_flow_acc.write(time_index, post_flow),
            corrected_log_weights_acc.write(time_index, corrected_log_weights),
            normalized_log_weights_acc.write(time_index, normalized_log_weights),
            aux_x0_acc.write(time_index, flow_aux.x0),
            aux_prior_means_acc.write(time_index, flow_aux.prior_means),
            aux_observation_jacobian_acc.write(time_index, flow_aux.observation_jacobian),
            aux_observation_residual_acc.write(time_index, flow_aux.observation_residual),
            aux_transition_covariance_acc.write(time_index, flow_aux.transition_covariance),
            aux_observation_covariance_acc.write(time_index, flow_aux.observation_covariance),
            aux_transition_covariance_stable_acc.write(
                time_index,
                flow_aux.transition_covariance_stable,
            ),
            aux_observation_covariance_stable_acc.write(
                time_index,
                flow_aux.observation_covariance_stable,
            ),
            aux_prior_chol_acc.write(time_index, flow_aux.prior_chol),
            aux_prior_precision_acc.write(time_index, flow_aux.prior_precision),
            aux_obs_precision_acc.write(time_index, flow_aux.obs_precision),
            aux_pseudo_observation_acc.write(time_index, flow_aux.pseudo_observation),
            aux_post_precision_acc.write(time_index, flow_aux.post_precision),
            aux_post_precision_stable_acc.write(time_index, flow_aux.post_precision_stable),
            aux_post_covariance_unstabilized_acc.write(
                time_index,
                flow_aux.post_covariance_unstabilized,
            ),
            aux_post_covariance_acc.write(time_index, flow_aux.post_covariance),
            aux_post_chol_acc.write(time_index, flow_aux.post_chol),
            aux_prior_inv_acc.write(time_index, flow_aux.prior_inv),
            aux_affine_transform_acc.write(time_index, flow_aux.affine_transform),
            aux_delta_acc.write(time_index, flow_aux.delta),
            aux_info_acc.write(time_index, flow_aux.info),
        )

    (
        _,
        final_particles,
        _final_log_weights,
        log_likelihood,
        ancestors_ta,
        noise_ta,
        post_flow_ta,
        corrected_log_weights_ta,
        normalized_log_weights_ta,
        aux_x0_ta,
        aux_prior_means_ta,
        aux_observation_jacobian_ta,
        aux_observation_residual_ta,
        aux_transition_covariance_ta,
        aux_observation_covariance_ta,
        aux_transition_covariance_stable_ta,
        aux_observation_covariance_stable_ta,
        aux_prior_chol_ta,
        aux_prior_precision_ta,
        aux_obs_precision_ta,
        aux_pseudo_observation_ta,
        aux_post_precision_ta,
        aux_post_precision_stable_ta,
        aux_post_covariance_unstabilized_ta,
        aux_post_covariance_ta,
        aux_post_chol_ta,
        aux_prior_inv_ta,
        aux_affine_transform_ta,
        aux_delta_ta,
        aux_info_ta,
    ) = tf.while_loop(
        forward_cond,
        forward_body,
        loop_vars=(
            tf.constant(0, dtype=tf.int32),
            particles,
            log_weights,
            log_likelihood,
            ancestors_ta,
            noise_ta,
            post_flow_ta,
            corrected_log_weights_ta,
            normalized_log_weights_ta,
            aux_x0_ta,
            aux_prior_means_ta,
            aux_observation_jacobian_ta,
            aux_observation_residual_ta,
            aux_transition_covariance_ta,
            aux_observation_covariance_ta,
            aux_transition_covariance_stable_ta,
            aux_observation_covariance_stable_ta,
            aux_prior_chol_ta,
            aux_prior_precision_ta,
            aux_obs_precision_ta,
            aux_pseudo_observation_ta,
            aux_post_precision_ta,
            aux_post_precision_stable_ta,
            aux_post_covariance_unstabilized_ta,
            aux_post_covariance_ta,
            aux_post_chol_ta,
            aux_prior_inv_ta,
            aux_affine_transform_ta,
            aux_delta_ta,
            aux_info_ta,
        ),
        parallel_iterations=1,
        maximum_iterations=TIME_STEPS,
    )

    def reverse_cond(
        reverse_index: tf.Tensor,
        _bar_particles: tf.Tensor,
        _score: tf.Tensor,
    ) -> tf.Tensor:
        return reverse_index < tf.constant(TIME_STEPS, dtype=tf.int32)

    def reverse_body(
        reverse_index: tf.Tensor,
        upstream_particles: tf.Tensor,
        current_score: tf.Tensor,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        time_index = tf.constant(TIME_STEPS - 1, dtype=tf.int32) - reverse_index
        post_flow = post_flow_ta.read(time_index)
        normalized_log_weights = normalized_log_weights_ta.read(time_index)
        bar_post_transport, bar_normalized_log_weights = _transport_vjp(
            post_flow,
            normalized_log_weights,
            upstream_particles,
        )
        bar_corrected, _weights, _incremental, _floor_active = (
            core_ledh._normalize_log_weights_with_floor_vjp(
                corrected_log_weights_ta.read(time_index),
                bar_normalized_log_weights,
                tf.ones([batch_size], dtype=DTYPE),
            )
        )
        correction_bars = core_ledh._log_weight_correction_vjp(bar_corrected)
        flow_aux = core_ledh._BatchedLEDHLinearizedFlowAux(
            x0=aux_x0_ta.read(time_index),
            prior_means=aux_prior_means_ta.read(time_index),
            observation_jacobian=aux_observation_jacobian_ta.read(time_index),
            observation_residual=aux_observation_residual_ta.read(time_index),
            transition_covariance=aux_transition_covariance_ta.read(time_index),
            observation_covariance=aux_observation_covariance_ta.read(time_index),
            transition_covariance_stable=aux_transition_covariance_stable_ta.read(time_index),
            observation_covariance_stable=aux_observation_covariance_stable_ta.read(time_index),
            prior_chol=aux_prior_chol_ta.read(time_index),
            prior_precision=aux_prior_precision_ta.read(time_index),
            obs_precision=aux_obs_precision_ta.read(time_index),
            pseudo_observation=aux_pseudo_observation_ta.read(time_index),
            post_precision=aux_post_precision_ta.read(time_index),
            post_precision_stable=aux_post_precision_stable_ta.read(time_index),
            post_covariance_unstabilized=aux_post_covariance_unstabilized_ta.read(time_index),
            post_covariance=aux_post_covariance_ta.read(time_index),
            post_chol=aux_post_chol_ta.read(time_index),
            prior_inv=aux_prior_inv_ta.read(time_index),
            affine_transform=aux_affine_transform_ta.read(time_index),
            delta=aux_delta_ta.read(time_index),
            info=aux_info_ta.read(time_index),
        )
        transition_vjp = core_ledh._transition_gaussian_log_density_vjp(
            post_flow,
            flow_aux.prior_means,
            transition_covariance,
            correction_bars["transition_log_density"],
        )
        observation_vjp = core_ledh._observation_gaussian_log_density_vjp(
            post_flow,
            observations[time_index],
            observation_covariance,
            correction_bars["observation_log_density"],
            residual_convention="model_minus_observation",
        )
        bar_post = (
            bar_post_transport
            + transition_vjp["x_next"]
            + observation_vjp["predicted_observation"]
        )
        flow_vjp = core_ledh._batched_ledh_linearized_flow_vjp(
            flow_aux,
            bar_post,
            correction_bars["pre_flow_log_density"],
            correction_bars["forward_log_det"],
        )
        bar_pre_flow = flow_vjp.pre_flow_particles - flow_vjp.observation_residual
        bar_prior_mean = transition_vjp["transition_mean"] + flow_vjp.prior_means + bar_pre_flow
        transition_covariance_score = tf.reduce_sum(
            (transition_vjp["transition_covariance"] + flow_vjp.transition_covariance)
            * transition_covariance,
            axis=[1, 2],
        )
        pre_flow_noise_score = tf.reduce_sum(
            bar_pre_flow * noise_ta.read(time_index) * (0.5 * transition_std[:, None, :]),
            axis=[1, 2],
        )
        observation_covariance_score = tf.reduce_sum(
            (observation_vjp["observation_covariance"] + flow_vjp.observation_covariance)
            * observation_covariance,
            axis=[1, 2],
        )
        transition_matrix_score = tf.reduce_sum(
            bar_prior_mean * ancestors_ta.read(time_index),
            axis=[1, 2],
        )
        next_score = current_score + tf.stack(
            [
                transition_matrix_score,
                transition_covariance_score + pre_flow_noise_score,
                observation_covariance_score,
            ],
            axis=1,
        )
        next_bar_particles = tf.einsum("bnd,bdj->bnj", bar_prior_mean, transition_matrix)
        return reverse_index + 1, next_bar_particles, next_score

    _, _bar_particles, score = tf.while_loop(
        reverse_cond,
        reverse_body,
        loop_vars=(
            tf.constant(0, dtype=tf.int32),
            tf.zeros_like(final_particles),
            tf.zeros([batch_size, 3], dtype=DTYPE),
        ),
        parallel_iterations=1,
        maximum_iterations=TIME_STEPS,
    )
    return log_likelihood, score


def _ledh_value_and_score_xla_compiled(state_dim: int) -> tuple[tf.Tensor, tf.Tensor]:
    observations = _observations(state_dim)
    initial_noise, transition_noise = _stateless_seeded_normals_batch(state_dim)
    initial_particles = tf.sqrt(tf.constant(0.7, dtype=DTYPE)) * initial_noise
    theta_batch = tf.tile(THETA[None, :], [SEED_COUNT, 1])

    @tf.function(
        input_signature=[
            tf.TensorSpec([SEED_COUNT, 3], DTYPE),
            tf.TensorSpec([SEED_COUNT, NUM_PARTICLES, state_dim], DTYPE),
            tf.TensorSpec([SEED_COUNT, TIME_STEPS, NUM_PARTICLES, state_dim], DTYPE),
        ],
        jit_compile=True,
        reduce_retracing=True,
    )
    def compiled(
        values: tf.Tensor,
        particles: tf.Tensor,
        noise: tf.Tensor,
    ) -> tuple[tf.Tensor, tf.Tensor]:
        return _lgssm_manual_value_and_score(
            values,
            state_dim,
            particles,
            noise,
            observations,
        )

    return compiled(theta_batch, initial_particles, transition_noise)


def _ledh_value_and_score(state_dim: int) -> tuple[tf.Tensor, tf.Tensor]:
    tf.config.experimental.enable_tensor_float_32_execution(True)
    return _ledh_value_and_score_xla_compiled(state_dim)


def _kalman_value_and_score(state_dim: int) -> tuple[tf.Tensor, tf.Tensor]:
    reference_dtype = tf.float64
    observations = tf.cast(_observations(state_dim), reference_dtype)
    theta_batch = tf.cast(THETA[None, :], reference_dtype)
    eye = tf.eye(state_dim, dtype=reference_dtype)[None, :, :]
    transition_matrix = theta_batch[:, 0, None, None] * eye
    transition_covariance = tf.exp(theta_batch[:, 1])[:, None, None] * eye
    observation_covariance = tf.exp(theta_batch[:, 2])[:, None, None] * eye
    zeros_state = tf.zeros([1, state_dim], dtype=reference_dtype)
    zeros_obs = tf.zeros([1, state_dim], dtype=reference_dtype)
    zeros_d_state = tf.zeros([1, 3, state_dim], dtype=reference_dtype)
    zeros_d_matrix = tf.zeros([1, 3, state_dim, state_dim], dtype=reference_dtype)
    d_transition_matrix = tf.tensor_scatter_nd_update(
        zeros_d_matrix,
        indices=tf.constant([[0, 0]], dtype=tf.int32),
        updates=tf.eye(state_dim, dtype=reference_dtype)[None, :, :],
    )
    d_transition_covariance = tf.tensor_scatter_nd_update(
        zeros_d_matrix,
        indices=tf.constant([[0, 1]], dtype=tf.int32),
        updates=transition_covariance,
    )
    d_observation_covariance = tf.tensor_scatter_nd_update(
        zeros_d_matrix,
        indices=tf.constant([[0, 2]], dtype=tf.int32),
        updates=observation_covariance,
    )
    return tf_batched_kalman_value_and_score(
        observations=observations,
        transition_offset=zeros_state,
        transition_matrix=transition_matrix,
        transition_covariance=transition_covariance,
        observation_offset=zeros_obs,
        observation_matrix=eye,
        observation_covariance=observation_covariance,
        initial_state_mean=zeros_state,
        initial_state_covariance=tf.constant(0.7, dtype=reference_dtype) * eye,
        d_initial_state_mean=zeros_d_state,
        d_initial_state_covariance=zeros_d_matrix,
        d_transition_offset=zeros_d_state,
        d_transition_matrix=d_transition_matrix,
        d_transition_covariance=d_transition_covariance,
        d_observation_offset=zeros_d_state,
        d_observation_matrix=zeros_d_matrix,
        d_observation_covariance=d_observation_covariance,
    )


def _mean_sd_mcse(samples: tf.Tensor) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = tf.reduce_mean(samples, axis=0)
    centered = samples - mean
    sd = tf.sqrt(
        tf.reduce_sum(tf.square(centered), axis=0)
        / tf.cast(tf.shape(samples)[0] - 1, DTYPE)
    )
    mcse = sd / tf.sqrt(tf.cast(tf.shape(samples)[0], DTYPE))
    return mean.numpy(), sd.numpy(), mcse.numpy()


def _assert_kalman_within_two_seed_sd(state_dim: int) -> None:
    ledh_value, ledh_score = _ledh_value_and_score(state_dim)
    kalman_value, kalman_score = _kalman_value_and_score(state_dim)

    value_mean, value_sd, value_mcse = _mean_sd_mcse(ledh_value)
    score_mean, score_sd, score_mcse = _mean_sd_mcse(ledh_score)
    value_delta = np.asarray(kalman_value.numpy()[0] - value_mean)
    score_delta = np.asarray(kalman_score.numpy()[0] - score_mean)

    np.testing.assert_allclose(
        value_mean,
        kalman_value.numpy()[0],
        atol=float(2.0 * value_sd + 1.0e-8),
        rtol=0.0,
        err_msg=(
            f"1d/2d LGSSM value failed state_dim={state_dim}; "
            f"delta={value_delta}, seed_sd={value_sd}, mcse={value_mcse}"
        ),
    )
    np.testing.assert_allclose(
        score_mean,
        kalman_score.numpy()[0],
        atol=2.0 * score_sd + 1.0e-8,
        rtol=0.0,
        err_msg=(
            f"1d/2d LGSSM score failed state_dim={state_dim}; "
            f"delta={score_delta}, seed_sd={score_sd}, mcse={score_mcse}"
        ),
    )


@FULL_N1000_MARK
def test_ledh_pfpf_ot_1d_lgssm_t10_n1000_value_and_gradient_match_kalman_two_seed_sd() -> None:
    _assert_kalman_within_two_seed_sd(state_dim=1)


@FULL_N1000_MARK
def test_ledh_pfpf_ot_2d_lgssm_t10_n1000_value_and_gradient_match_kalman_two_seed_sd() -> None:
    _assert_kalman_within_two_seed_sd(state_dim=2)


def test_lgssm_statistical_harness_uses_xla_tf32_batched_manual_route() -> None:
    source = inspect.getsource(_ledh_value_and_score_xla_compiled)
    entry_source = inspect.getsource(_ledh_value_and_score)
    assert "jit_compile=True" in source
    assert "tf.function" in source
    assert "TensorSpec([SEED_COUNT, 3], DTYPE)" in source
    assert "for seed_index in range(SEED_COUNT)" not in source
    assert "range(0, SEED_COUNT" not in source
    assert "_ledh_value_and_score_one_seed" not in globals()
    assert "for seed_index in range(SEED_COUNT)" not in entry_source
    assert "enable_tensor_float_32_execution(True)" in entry_source
    assert tf.config.experimental.tensor_float_32_execution_enabled()


def _leaf_call_name(node: ast.expr) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def test_lgssm_statistical_harness_xla_driver_has_no_python_loops() -> None:
    source = textwrap.dedent(inspect.getsource(_ledh_value_and_score_xla_compiled))
    tree = ast.parse(source)
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)

    for_nodes = [node for node in ast.walk(function) if isinstance(node, ast.For)]
    while_nodes = [node for node in ast.walk(function) if isinstance(node, ast.While)]
    assert not for_nodes
    assert not while_nodes

    allowed_calls = {
        "_observations",
        "_stateless_seeded_normals_batch",
        "_lgssm_manual_value_and_score",
        "compiled",
        "constant",
        "function",
        "sqrt",
        "TensorSpec",
        "tile",
    }
    for call in [node for node in ast.walk(function) if isinstance(node, ast.Call)]:
        name = _leaf_call_name(call.func)
        assert name in allowed_calls


def test_lgssm_statistical_manual_score_has_no_seed_loop() -> None:
    source = textwrap.dedent(inspect.getsource(_lgssm_manual_value_and_score))
    tree = ast.parse(source)
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)

    for_nodes = [node for node in ast.walk(function) if isinstance(node, ast.For)]
    while_nodes = [node for node in ast.walk(function) if isinstance(node, ast.While)]
    assert not for_nodes
    assert not while_nodes
    assert "tf.while_loop" in source
    assert "tf.TensorArray" in source
    assert "TensorArray" in source
    assert "seed_index" not in source
    assert "SEED_COUNT" not in source
    assert "records" not in source
    assert "reversed(" not in source


def test_lgssm_statistical_harness_does_not_use_generic_autodiff_score_wrapper() -> None:
    route_source = "\n".join(
        [
            inspect.getsource(_transport_forward),
            inspect.getsource(_transport_vjp),
            inspect.getsource(_lgssm_manual_value_and_score),
            inspect.getsource(_ledh_value_and_score_xla_compiled),
            inspect.getsource(_ledh_value_and_score),
        ]
    )
    forbidden_terms = (
        "streaming_batched_ledh_pfpf_ot_value" + "_and_score_tf",
        "batched_ledh_pfpf_ot_value" + "_and_score_tf",
        "tf." + "GradientTape",
    )
    for term in forbidden_terms:
        assert term not in route_source
    assert "transport_ad_mode" not in route_source
    assert "full" not in route_source
    assert "_filterflow_manual_streaming_finite_transport_stopped_scale_keys" in route_source
    assert "_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys" in route_source


def test_lgssm_statistical_harness_called_transport_primitives_have_no_ad_wrapper() -> None:
    primitive_sources = "\n".join(
        [
            inspect.getsource(
                annealed_transport_tf._filterflow_manual_streaming_finite_transport_stopped_scale_keys
            ),
            inspect.getsource(
                annealed_transport_tf._filterflow_streaming_transport_from_potentials_vjp
            ),
            inspect.getsource(
                annealed_transport_tf._filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys
            ),
            inspect.getsource(core_ledh._batched_ledh_linearized_flow_with_aux_tf),
            inspect.getsource(core_ledh._batched_ledh_linearized_flow_vjp),
        ]
    )
    assert "GradientTape" not in primitive_sources
    assert "transport_ad_mode" not in primitive_sources or "full" not in primitive_sources
