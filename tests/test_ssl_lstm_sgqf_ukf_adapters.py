import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.fixed_sgqf_tf import tf_fixed_sgqf_filter
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_log_likelihood
from bayesfilter.nonlinear.ssl_lstm_protocol import SSLLSTMStaticConfig
from bayesfilter.nonlinear.ssl_lstm_sgqf_ukf_adapters import (
    build_ssl_lstm_debug_value_score_artifact,
    make_ssl_lstm_fixed_sgqf_components,
    make_ssl_lstm_svd_ukf_components,
    ssl_lstm_observation,
    ssl_lstm_observation_parameter_derivative,
    ssl_lstm_observation_state_jacobian,
    ssl_lstm_parameter_slices,
    ssl_lstm_transition,
    ssl_lstm_transition_parameter_derivative,
    ssl_lstm_transition_state_jacobian,
    tf_ssl_lstm_fixed_sgqf_score,
    tf_ssl_lstm_svd_ukf_score,
    unpack_ssl_lstm_parameters,
)


EVIDENCE_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md"
)


def _config() -> SSLLSTMStaticConfig:
    return SSLLSTMStaticConfig(
        horizon=2,
        latent_dim=1,
        hidden_dim=1,
        observation_dim=1,
    )


def _theta() -> tf.Tensor:
    config = _config()
    values = np.zeros(config.parameter_dim, dtype=np.float64)
    # Gate input, recurrent, and bias blocks.
    values[0:4] = np.array([0.09, -0.07, 0.05, 0.04])
    values[4:8] = np.array([0.03, -0.02, 0.06, -0.05])
    values[8:12] = np.array([0.01, 0.04, -0.03, 0.02])
    values[12] = 0.35  # latent_weight
    values[13] = -0.08  # latent_bias
    values[14] = 0.65  # observation_weight
    values[15] = 0.05  # observation_bias
    values[16:19] = np.array([0.15, -0.10, 0.20])  # initial_mean
    values[19:22] = np.array([-0.35, 0.15, 0.55])  # initial std raw
    values[22] = 0.35  # process std raw
    values[-1] = -0.15
    return tf.constant(values, dtype=tf.float64)


def _observations() -> tf.Tensor:
    return tf.constant([[0.12], [-0.03]], dtype=tf.float64)


def _finite_difference(theta: tf.Tensor, value_fn, *, indices: tuple[int, ...], step: float = 1.0e-5) -> np.ndarray:
    base = np.asarray(theta.numpy(), dtype=np.float64)
    values = np.zeros([len(indices)], dtype=np.float64)
    for offset, index in enumerate(indices):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        values[offset] = (
            float(value_fn(tf.constant(plus, dtype=tf.float64)).numpy())
            - float(value_fn(tf.constant(minus, dtype=tf.float64)).numpy())
        ) / (2.0 * step)
    return values


def test_ssl_lstm_parameter_layout_matches_phase1_config() -> None:
    config = _config()
    theta = _theta()
    params = unpack_ssl_lstm_parameters(theta, config)
    slices = ssl_lstm_parameter_slices(config)

    assert slices.parameter_dim == config.parameter_dim
    assert params.lstm_input.shape == (4, 1, 1)
    assert params.lstm_recurrent.shape == (4, 1, 1)
    assert params.lstm_bias.shape == (4, 1)
    assert params.initial_mean.shape == (3,)
    assert params.d_initial_covariance.shape == (config.parameter_dim, 3, 3)
    assert params.d_sgqf_process_covariance.shape == (config.parameter_dim, 3, 3)
    assert params.d_ukf_innovation_covariance.shape == (config.parameter_dim, 1, 1)
    assert params.d_observation_covariance.shape == (config.parameter_dim, 1, 1)


def test_ssl_lstm_hand_transition_derivatives_match_finite_difference() -> None:
    config = _config()
    theta = _theta()
    params = unpack_ssl_lstm_parameters(theta, config)
    points = tf.constant([[0.2, -0.1, 0.3], [-0.4, 0.25, -0.15]], dtype=tf.float64)
    state_jacobian = ssl_lstm_transition_state_jacobian(params, points).numpy()
    parameter_derivative = ssl_lstm_transition_parameter_derivative(params, points).numpy()

    def transition_at_points(point_values: np.ndarray) -> np.ndarray:
        return ssl_lstm_transition(params, tf.constant(point_values, dtype=tf.float64)).numpy()

    step = 1.0e-6
    fd_state = np.zeros_like(state_jacobian)
    point_values = points.numpy()
    for row in range(point_values.shape[0]):
        for col in range(point_values.shape[1]):
            plus = point_values.copy()
            minus = point_values.copy()
            plus[row, col] += step
            minus[row, col] -= step
            fd_state[row, :, col] = (
                transition_at_points(plus)[row] - transition_at_points(minus)[row]
            ) / (2.0 * step)

    def transition_for_theta(theta_value: tf.Tensor) -> tf.Tensor:
        shifted = unpack_ssl_lstm_parameters(theta_value, config)
        return ssl_lstm_transition(shifted, points)

    checked_indices = (0, 4, 8, 12, 13, 14, 16, 19, 22)
    fd_param = np.zeros([len(checked_indices), points.shape[0], config.augmented_state_dim], dtype=np.float64)
    base = theta.numpy()
    for offset, index in enumerate(checked_indices):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        fd_param[offset] = (
            transition_for_theta(tf.constant(plus, dtype=tf.float64)).numpy()
            - transition_for_theta(tf.constant(minus, dtype=tf.float64)).numpy()
        ) / (2.0 * step)

    np.testing.assert_allclose(state_jacobian, fd_state, rtol=2e-5, atol=2e-6)
    np.testing.assert_allclose(parameter_derivative[list(checked_indices)], fd_param, rtol=2e-5, atol=2e-6)


def test_ssl_lstm_hand_observation_derivatives_match_finite_difference() -> None:
    config = _config()
    theta = _theta()
    params = unpack_ssl_lstm_parameters(theta, config)
    points = tf.constant([[0.2, -0.1, 0.3], [-0.4, 0.25, -0.15]], dtype=tf.float64)
    state_jacobian = ssl_lstm_observation_state_jacobian(params, points).numpy()
    parameter_derivative = ssl_lstm_observation_parameter_derivative(params, points).numpy()

    step = 1.0e-6
    fd_state = np.zeros_like(state_jacobian)
    point_values = points.numpy()
    for row in range(point_values.shape[0]):
        for col in range(point_values.shape[1]):
            plus = point_values.copy()
            minus = point_values.copy()
            plus[row, col] += step
            minus[row, col] -= step
            fd_state[row, :, col] = (
                ssl_lstm_observation(params, tf.constant(plus, dtype=tf.float64)).numpy()[row]
                - ssl_lstm_observation(params, tf.constant(minus, dtype=tf.float64)).numpy()[row]
            ) / (2.0 * step)

    checked_indices = (14, 15)
    fd_param = np.zeros([len(checked_indices), points.shape[0], config.observation_dim], dtype=np.float64)
    base = theta.numpy()
    for offset, index in enumerate(checked_indices):
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        shifted_plus = unpack_ssl_lstm_parameters(tf.constant(plus, dtype=tf.float64), config)
        shifted_minus = unpack_ssl_lstm_parameters(tf.constant(minus, dtype=tf.float64), config)
        fd_param[offset] = (
            ssl_lstm_observation(shifted_plus, points).numpy()
            - ssl_lstm_observation(shifted_minus, points).numpy()
        ) / (2.0 * step)

    np.testing.assert_allclose(state_jacobian, fd_state, rtol=1e-7, atol=1e-8)
    np.testing.assert_allclose(parameter_derivative[list(checked_indices)], fd_param, rtol=1e-7, atol=1e-8)


def test_ssl_lstm_fixed_sgqf_score_is_finite_deterministic_and_matches_fd_subset() -> None:
    config = _config()
    theta = _theta()
    result, components = tf_ssl_lstm_fixed_sgqf_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        sparse_level=2,
    )
    repeated, _ = tf_ssl_lstm_fixed_sgqf_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        sparse_level=2,
    )

    assert result.failure is None
    assert result.score is not None
    assert result.log_likelihood is not None
    np.testing.assert_allclose(result.log_likelihood.numpy(), repeated.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(result.score.numpy(), repeated.score.numpy(), atol=1e-12)
    assert result.diagnostics["derivative_method"] == "analytic_first_order_fixed_branch"
    assert components.protocol.gradient_path == "analytic_first_order_fixed_sgqf"

    def value_fn(theta_value: tf.Tensor) -> tf.Tensor:
        local = make_ssl_lstm_fixed_sgqf_components(
            theta_value,
            config,
            evidence_path=EVIDENCE_PATH,
            sparse_level=2,
        )
        value = tf_fixed_sgqf_filter(
            _observations(),
            local.model,
            cloud=local.cloud,
            branch_config=local.branch_config,
            return_filtered=True,
        )
        if value.failure is not None:
            raise AssertionError(value.failure.reason)
        return value.log_likelihood

    indices = (0, 4, 8, 12, 13, 14, 15, 16, 19, 22)
    finite_difference = _finite_difference(theta, value_fn, indices=indices)
    residual = np.max(np.abs(result.score.numpy()[list(indices)] - finite_difference))
    np.testing.assert_allclose(result.score.numpy()[list(indices)], finite_difference, rtol=3e-3, atol=5e-4)
    artifact = build_ssl_lstm_debug_value_score_artifact(
        protocol=components.protocol,
        log_likelihood=result.log_likelihood,
        score=result.score,
        finite_difference_max_abs_error=float(residual),
    )
    assert artifact["filter_name"] == "fixed_sgqf"
    assert artifact["artifact_role"] == "debug_reference"


def test_ssl_lstm_svd_ukf_score_is_finite_deterministic_and_matches_fd_subset() -> None:
    config = _config()
    theta = _theta()
    result, components = tf_ssl_lstm_svd_ukf_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        spectral_gap_tolerance=tf.constant(1e-10, dtype=tf.float64),
    )
    repeated, _ = tf_ssl_lstm_svd_ukf_score(
        _observations(),
        theta,
        config,
        evidence_path=EVIDENCE_PATH,
        spectral_gap_tolerance=tf.constant(1e-10, dtype=tf.float64),
    )

    np.testing.assert_allclose(result.log_likelihood.numpy(), repeated.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(result.score.numpy(), repeated.score.numpy(), atol=1e-12)
    assert result.diagnostics.extra["derivative_provider"] == "ssl_lstm_svd_ukf_hand_derivatives"
    assert result.diagnostics.extra["derivative_method"] == "analytic_first_order_smooth_branch"
    assert components.protocol.gradient_path == "analytic_first_order_svd_ukf"

    def value_fn(theta_value: tf.Tensor) -> tf.Tensor:
        local = make_ssl_lstm_svd_ukf_components(
            theta_value,
            config,
            evidence_path=EVIDENCE_PATH,
        )
        value, _means, _covariances, _diagnostics = tf_svd_sigma_point_log_likelihood(
            _observations(),
            local.model,
            rule="unscented",
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
        )
        return value

    indices = (0, 4, 8, 12, 13, 14, 15, 16, 19, 22)
    finite_difference = _finite_difference(theta, value_fn, indices=indices)
    residual = np.max(np.abs(result.score.numpy()[list(indices)] - finite_difference))
    np.testing.assert_allclose(result.score.numpy()[list(indices)], finite_difference, rtol=5e-3, atol=8e-4)
    artifact = build_ssl_lstm_debug_value_score_artifact(
        protocol=components.protocol,
        log_likelihood=result.log_likelihood,
        score=result.score,
        finite_difference_max_abs_error=float(residual),
    )
    assert artifact["filter_name"] == "svd_ukf"
    assert artifact["artifact_role"] == "debug_reference"


def test_ssl_lstm_transition_and_jacobian_xla_smoke() -> None:
    config = _config()
    theta = _theta()
    points = tf.constant([[0.2, -0.1, 0.3], [-0.4, 0.25, -0.15]], dtype=tf.float64)

    @tf.function(jit_compile=True)
    def compiled(theta_value: tf.Tensor, point_values: tf.Tensor):
        params = unpack_ssl_lstm_parameters(theta_value, config)
        return (
            ssl_lstm_transition(params, point_values),
            ssl_lstm_transition_state_jacobian(params, point_values),
            ssl_lstm_transition_parameter_derivative(params, point_values),
        )

    try:
        transition, state_jacobian, parameter_derivative = compiled(theta, points)
    except tf.errors.InvalidArgumentError as exc:
        pytest.skip(f"local CPU XLA unavailable for SSL-LSTM transition smoke: {exc}")
    assert transition.shape == (2, 3)
    assert state_jacobian.shape == (2, 3, 3)
    assert parameter_derivative.shape == (config.parameter_dim, 2, 3)
