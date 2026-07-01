from __future__ import annotations

import math
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear import (
    tf_batched_svd_sigma_point_value_and_score_custom_gradient,
)
from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    TFBatchedStructuralFirstDerivatives,
    TFBatchedStructuralStateSpace,
)
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace


def _unit_gauss_legendre(order: int) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return 0.5 * (nodes + 1.0), 0.5 * weights


def _stationary_covariance(transition: np.ndarray, covariance: np.ndarray) -> np.ndarray:
    dim = transition.shape[0]
    system = np.eye(dim * dim, dtype=np.float64) - np.kron(transition, transition)
    return np.linalg.solve(system, covariance.reshape(-1)).reshape(dim, dim)


def _zlb_dns_yield_curve(
    states: tf.Tensor,
    *,
    maturities: tf.Tensor,
    decay: tf.Tensor,
    lower_bound: tf.Tensor,
    alpha: tf.Tensor,
    nodes: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    points = tf.convert_to_tensor(states, dtype=tf.float64)
    if points.shape.rank == 1:
        points = points[tf.newaxis, :]
    u = maturities[:, tf.newaxis] * nodes[tf.newaxis, :]
    exp_term = tf.exp(-decay * u)
    forward = (
        points[:, 0, tf.newaxis, tf.newaxis]
        + points[:, 1, tf.newaxis, tf.newaxis] * exp_term[tf.newaxis, :, :]
        + points[:, 2, tf.newaxis, tf.newaxis]
        * decay
        * u[tf.newaxis, :, :]
        * exp_term[tf.newaxis, :, :]
    )
    constrained = lower_bound + alpha * tf.nn.softplus((forward - lower_bound) / alpha)
    return tf.reduce_sum(constrained * weights[tf.newaxis, tf.newaxis, :], axis=2)


def _batched_zlb_dns_yield_curve(
    states: tf.Tensor,
    *,
    maturities: tf.Tensor,
    decay: tf.Tensor,
    lower_bound: tf.Tensor,
    alpha: tf.Tensor,
    nodes: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    points = tf.convert_to_tensor(states, dtype=tf.float64)
    u = maturities[:, tf.newaxis] * nodes[tf.newaxis, :]
    exp_term = tf.exp(-decay * u)
    forward = (
        points[:, :, 0, tf.newaxis, tf.newaxis]
        + points[:, :, 1, tf.newaxis, tf.newaxis] * exp_term[tf.newaxis, tf.newaxis, :, :]
        + points[:, :, 2, tf.newaxis, tf.newaxis]
        * decay
        * u[tf.newaxis, tf.newaxis, :, :]
        * exp_term[tf.newaxis, tf.newaxis, :, :]
    )
    constrained = lower_bound + alpha * tf.nn.softplus((forward - lower_bound) / alpha)
    return tf.reduce_sum(constrained * weights[tf.newaxis, tf.newaxis, tf.newaxis, :], axis=3)


def _batched_zlb_dns_observation_state_jacobian(
    states: tf.Tensor,
    *,
    maturities: tf.Tensor,
    decay: tf.Tensor,
    lower_bound: tf.Tensor,
    alpha: tf.Tensor,
    nodes: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    points = tf.convert_to_tensor(states, dtype=tf.float64)
    u = maturities[:, tf.newaxis] * nodes[tf.newaxis, :]
    exp_term = tf.exp(-decay * u)
    loading_level = tf.ones_like(exp_term)
    loading_slope = exp_term
    loading_curvature = decay * u * exp_term
    loadings = tf.stack([loading_level, loading_slope, loading_curvature], axis=2)
    forward = (
        points[:, :, 0, tf.newaxis, tf.newaxis]
        + points[:, :, 1, tf.newaxis, tf.newaxis] * exp_term[tf.newaxis, tf.newaxis, :, :]
        + points[:, :, 2, tf.newaxis, tf.newaxis]
        * decay
        * u[tf.newaxis, tf.newaxis, :, :]
        * exp_term[tf.newaxis, tf.newaxis, :, :]
    )
    slope = tf.math.sigmoid((forward - lower_bound) / alpha)
    return tf.einsum("brmq,mqk,q->brmk", slope, loadings, weights)


def _fixture() -> tuple[np.ndarray, np.ndarray]:
    maturities = np.array([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=np.float64)
    truth_vector = np.array([0.0060, -0.0120, 0.0050, np.log(3.0e-4)], dtype=np.float64)
    transition_matrix = np.array(
        [[0.940, 0.020, 0.000], [0.000, 0.875, 0.030], [0.000, -0.020, 0.720]],
        dtype=np.float64,
    )
    process_scales = np.array([0.0018, 0.0025, 0.0022], dtype=np.float64)
    transition_covariance = np.diag(process_scales**2)
    transition_offset = (np.eye(3, dtype=np.float64) - transition_matrix) @ truth_vector[:3]
    states = np.zeros((8, 3), dtype=np.float64)
    states[0] = truth_vector[:3]
    rng = np.random.default_rng(20260626)
    for t in range(1, states.shape[0]):
        shock = rng.multivariate_normal(np.zeros(3, dtype=np.float64), transition_covariance)
        states[t] = transition_offset + transition_matrix @ states[t - 1] + shock
    nodes, weights = _unit_gauss_legendre(20)
    u = maturities[:, None] * nodes[None, :]
    exp_term = np.exp(-0.65 * u)
    forward = (
        states[:, 0, None, None]
        + states[:, 1, None, None] * exp_term[None, :, :]
        + states[:, 2, None, None] * 0.65 * u[None, :, :] * exp_term[None, :, :]
    )
    noiseless = np.sum(
        (0.0 + 1.5e-3 * np.logaddexp(0.0, (forward - 0.0) / 1.5e-3))
        * weights[None, None, :],
        axis=2,
    )
    observations = noiseless + rng.normal(0.0, np.exp(truth_vector[3]), size=noiseless.shape)
    prior_mean = np.array([0.0100, -0.0060, 0.0020, np.log(6.0e-4)], dtype=np.float64)
    return observations, prior_mean


def _model(parameters: tf.Tensor) -> TFStructuralStateSpace:
    theta = tf.convert_to_tensor(parameters, dtype=tf.float64)
    transition_matrix = tf.constant(
        [[0.940, 0.020, 0.000], [0.000, 0.875, 0.030], [0.000, -0.020, 0.720]],
        dtype=tf.float64,
    )
    process_scales = np.array([0.0018, 0.0025, 0.0022], dtype=np.float64)
    transition_covariance_np = np.diag(process_scales**2)
    transition_covariance = tf.constant(transition_covariance_np, dtype=tf.float64)
    initial_covariance = tf.constant(
        _stationary_covariance(
            np.array(
                [[0.940, 0.020, 0.000], [0.000, 0.875, 0.030], [0.000, -0.020, 0.720]],
                dtype=np.float64,
            ),
            transition_covariance_np,
        ),
        dtype=tf.float64,
    )
    transition_offset = tf.linalg.matvec(tf.eye(3, dtype=tf.float64) - transition_matrix, theta[:3])
    maturities = tf.constant([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=tf.float64)
    nodes_np, weights_np = _unit_gauss_legendre(20)
    nodes = tf.constant(nodes_np, dtype=tf.float64)
    weights = tf.constant(weights_np, dtype=tf.float64)
    observation_covariance = tf.exp(2.0 * theta[3]) * tf.eye(6, dtype=tf.float64)

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        was_vector = tf.convert_to_tensor(previous_state).shape.rank == 1
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        if previous.shape.rank == 1:
            previous = previous[tf.newaxis, :]
        shocks = tf.convert_to_tensor(innovation, dtype=tf.float64)
        if shocks.shape.rank == 1:
            shocks = shocks[tf.newaxis, :]
        next_points = (
            transition_offset[tf.newaxis, :]
            + tf.linalg.matmul(previous, transition_matrix, transpose_b=True)
            + shocks
        )
        return next_points[0] if was_vector else next_points

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        was_vector = tf.convert_to_tensor(state_points).shape.rank == 1
        yields = _zlb_dns_yield_curve(
            state_points,
            maturities=maturities,
            decay=tf.constant(0.65, dtype=tf.float64),
            lower_bound=tf.constant(0.0, dtype=tf.float64),
            alpha=tf.constant(1.5e-3, dtype=tf.float64),
            nodes=nodes,
            weights=weights,
        )
        return yields[0] if was_vector else yields

    return TFStructuralStateSpace(
        partition=StatePartition(
            state_names=("level", "slope", "curvature"),
            stochastic_indices=(0, 1, 2),
            deterministic_indices=(),
            innovation_dim=3,
        ),
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="macrofinance_zlb_ns_xla_parity_fixture",
        ),
        initial_mean=theta[:3],
        initial_covariance=initial_covariance,
        innovation_covariance=transition_covariance,
        observation_covariance=observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="macrofinance_zlb_ns_xla_parity_fixture",
    )


def _batched_model_and_derivatives(
    theta_batch: tf.Tensor,
) -> tuple[TFBatchedStructuralStateSpace, TFBatchedStructuralFirstDerivatives]:
    theta = tf.ensure_shape(tf.convert_to_tensor(theta_batch, dtype=tf.float64), [None, 4])
    batch_size = int(theta.shape[0])
    parameter_dim = 4
    state_dim = 3
    observation_dim = 6
    transition_matrix = tf.constant(
        [[0.940, 0.020, 0.000], [0.000, 0.875, 0.030], [0.000, -0.020, 0.720]],
        dtype=tf.float64,
    )
    transition_matrix_np = np.array(
        [[0.940, 0.020, 0.000], [0.000, 0.875, 0.030], [0.000, -0.020, 0.720]],
        dtype=np.float64,
    )
    process_scales = np.array([0.0018, 0.0025, 0.0022], dtype=np.float64)
    transition_covariance_np = np.diag(process_scales**2)
    initial_covariance = tf.constant(
        _stationary_covariance(transition_matrix_np, transition_covariance_np),
        dtype=tf.float64,
    )
    transition_covariance = tf.constant(transition_covariance_np, dtype=tf.float64)
    state_mean = theta[:, :state_dim]
    transition_offset = tf.linalg.matvec(
        tf.eye(state_dim, dtype=tf.float64) - transition_matrix,
        state_mean,
    )
    maturities = tf.constant([0.25, 0.5, 1.0, 2.0, 5.0, 10.0], dtype=tf.float64)
    nodes_np, weights_np = _unit_gauss_legendre(20)
    nodes = tf.constant(nodes_np, dtype=tf.float64)
    weights = tf.constant(weights_np, dtype=tf.float64)
    decay = tf.constant(0.65, dtype=tf.float64)
    lower_bound = tf.constant(0.0, dtype=tf.float64)
    alpha = tf.constant(1.5e-3, dtype=tf.float64)
    observation_variance = tf.exp(2.0 * theta[:, 3])
    eye_state = tf.eye(state_dim, dtype=tf.float64)
    eye_observation = tf.eye(observation_dim, dtype=tf.float64)

    def transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous_points = tf.convert_to_tensor(previous, dtype=tf.float64)
        innovation_points = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return (
            transition_offset[:, tf.newaxis, :]
            + tf.linalg.matmul(previous_points, transition_matrix, transpose_b=True)
            + innovation_points
        )

    def observe(states: tf.Tensor) -> tf.Tensor:
        return _batched_zlb_dns_yield_curve(
            states,
            maturities=maturities,
            decay=decay,
            lower_bound=lower_bound,
            alpha=alpha,
            nodes=nodes,
            weights=weights,
        )

    def transition_state_jacobian(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.broadcast_to(
            transition_matrix[tf.newaxis, tf.newaxis, :, :],
            [tf.shape(previous)[0], tf.shape(previous)[1], state_dim, state_dim],
        )

    def transition_innovation_jacobian(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        return tf.broadcast_to(
            eye_state[tf.newaxis, tf.newaxis, :, :],
            [tf.shape(previous)[0], tf.shape(previous)[1], state_dim, state_dim],
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        offset_jacobian = tf.concat(
            [
                tf.eye(state_dim, dtype=tf.float64) - transition_matrix,
                tf.zeros([state_dim, 1], dtype=tf.float64),
            ],
            axis=1,
        )
        derivative = tf.transpose(offset_jacobian)
        return tf.broadcast_to(
            derivative[tf.newaxis, :, tf.newaxis, :],
            [tf.shape(previous)[0], parameter_dim, tf.shape(previous)[1], state_dim],
        )

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        return _batched_zlb_dns_observation_state_jacobian(
            states,
            maturities=maturities,
            decay=decay,
            lower_bound=lower_bound,
            alpha=alpha,
            nodes=nodes,
            weights=weights,
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return tf.zeros(
            [tf.shape(states)[0], parameter_dim, tf.shape(states)[1], observation_dim],
            dtype=tf.float64,
        )

    d_initial_mean = tf.concat(
        [
            tf.broadcast_to(
                tf.eye(state_dim, dtype=tf.float64)[tf.newaxis, :, :],
                [batch_size, state_dim, state_dim],
            ),
            tf.zeros([batch_size, 1, state_dim], dtype=tf.float64),
        ],
        axis=1,
    )
    d_observation_covariance = tf.zeros(
        [batch_size, parameter_dim, observation_dim, observation_dim],
        dtype=tf.float64,
    )
    d_observation_covariance = tf.tensor_scatter_nd_update(
        d_observation_covariance,
        indices=tf.stack(
            [
                tf.range(batch_size, dtype=tf.int32),
                tf.fill([batch_size], tf.constant(3, dtype=tf.int32)),
            ],
            axis=1,
        ),
        updates=2.0 * observation_variance[:, tf.newaxis, tf.newaxis] * eye_observation,
    )

    model = TFBatchedStructuralStateSpace(
        initial_mean=state_mean,
        initial_covariance=tf.broadcast_to(
            initial_covariance[tf.newaxis, :, :],
            [batch_size, state_dim, state_dim],
        ),
        innovation_covariance=tf.broadcast_to(
            transition_covariance[tf.newaxis, :, :],
            [batch_size, state_dim, state_dim],
        ),
        observation_covariance=observation_variance[:, tf.newaxis, tf.newaxis] * eye_observation,
        transition_fn=transition,
        observation_fn=observe,
        name="macrofinance_zlb_ns_xla_parity_batched_fixture",
    )
    derivatives = TFBatchedStructuralFirstDerivatives(
        d_initial_mean=d_initial_mean,
        d_initial_covariance=tf.zeros(
            [batch_size, parameter_dim, state_dim, state_dim],
            dtype=tf.float64,
        ),
        d_innovation_covariance=tf.zeros(
            [batch_size, parameter_dim, state_dim, state_dim],
            dtype=tf.float64,
        ),
        d_observation_covariance=d_observation_covariance,
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
        name="macrofinance_zlb_ns_xla_parity_batched_first_derivatives",
    )
    return model, derivatives


def _custom_gradient_value_score_and_tape_gradient(
    theta_batch: tf.Tensor,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    model, derivatives = _batched_model_and_derivatives(theta_batch)
    with tf.GradientTape() as tape:
        tape.watch(theta_batch)
        value, score, _diagnostics = tf_batched_svd_sigma_point_value_and_score_custom_gradient(
            theta_batch,
            observations,
            model,
            derivatives,
            backend="tf_principal_sqrt_ukf",
            innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
            spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
            fixed_null_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        )
        objective = tf.reduce_sum(value)
    gradient = tape.gradient(objective, theta_batch)
    if gradient is None:
        raise AssertionError("custom-gradient likelihood gradient is disconnected")
    return value, score, gradient


def _log_likelihood_and_gradient(theta: tf.Tensor, observations: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    with tf.GradientTape() as tape:
        tape.watch(theta)
        value = tf_svd_sigma_point_filter(
            observations,
            _model(theta),
            backend="tf_svd_cubature",
            innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
        ).log_likelihood
    gradient = tape.gradient(value, theta)
    if gradient is None:
        raise AssertionError("likelihood gradient is disconnected")
    return value, gradient


@pytest.mark.xfail(
    strict=True,
    reason=(
        "scalar value-filter GradientTape path is not HMC-grade for this weak "
        "innovation spectral-gap fixture; use the BayesFilter-owned "
        "custom-gradient value/score route"
    ),
)
def test_macrofinance_zlb_ns_public_fixture_cpu_xla_value_gradient_parity() -> None:
    observations_np, prior_mean_np = _fixture()
    observations = tf.constant(observations_np, dtype=tf.float64)
    theta = tf.constant(prior_mean_np, dtype=tf.float64)
    eager_value, eager_gradient = _log_likelihood_and_gradient(theta, observations)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled(x: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return _log_likelihood_and_gradient(x, observations)

    xla_value, xla_gradient = compiled(theta)
    value_residual = abs(float(eager_value.numpy() - xla_value.numpy()))
    gradient_residual = float(
        np.max(np.abs(eager_gradient.numpy() - xla_gradient.numpy()))
    )

    assert bool(tf.math.is_finite(eager_value).numpy())
    assert bool(tf.math.is_finite(xla_value).numpy())
    assert np.all(np.isfinite(eager_gradient.numpy()))
    assert np.all(np.isfinite(xla_gradient.numpy()))
    assert value_residual <= 1.0e-7
    assert gradient_residual <= 1.0e-6


def test_macrofinance_zlb_ns_public_fixture_custom_gradient_cpu_xla_value_score_parity() -> None:
    observations_np, prior_mean_np = _fixture()
    observations = tf.constant(observations_np, dtype=tf.float64)
    theta_batch = tf.constant(prior_mean_np[tf.newaxis, :], dtype=tf.float64)
    eager_value, eager_score, eager_gradient = _custom_gradient_value_score_and_tape_gradient(
        theta_batch,
        observations,
    )

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled(x: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
        return _custom_gradient_value_score_and_tape_gradient(x, observations)

    xla_value, xla_score, xla_gradient = compiled(theta_batch)
    value_residual = float(np.max(np.abs(eager_value.numpy() - xla_value.numpy())))
    score_residual = float(np.max(np.abs(eager_score.numpy() - xla_score.numpy())))
    gradient_residual = float(np.max(np.abs(eager_gradient.numpy() - xla_gradient.numpy())))

    assert bool(tf.reduce_all(tf.math.is_finite(eager_value)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(xla_value)).numpy())
    assert np.all(np.isfinite(eager_score.numpy()))
    assert np.all(np.isfinite(xla_score.numpy()))
    assert np.all(np.isfinite(eager_gradient.numpy()))
    assert np.all(np.isfinite(xla_gradient.numpy()))
    np.testing.assert_allclose(eager_gradient.numpy(), eager_score.numpy(), atol=1.0e-10)
    np.testing.assert_allclose(xla_gradient.numpy(), xla_score.numpy(), atol=1.0e-10)
    assert value_residual <= 1.0e-7
    assert score_residual <= 1.0e-6
    assert gradient_residual <= 1.0e-6


def test_macrofinance_zlb_ns_public_fixture_reports_near_degenerate_innovation_gap() -> None:
    observations_np, prior_mean_np = _fixture()
    result = tf_svd_sigma_point_filter(
        tf.constant(observations_np, dtype=tf.float64),
        _model(tf.constant(prior_mean_np, dtype=tf.float64)),
        backend="tf_svd_cubature",
        innovation_floor=tf.constant(1.0e-12, dtype=tf.float64),
    )

    gap = float(result.diagnostics.extra["min_innovation_eigen_gap"].numpy())
    assert math.isfinite(gap)
    assert gap < 1.0e-10
