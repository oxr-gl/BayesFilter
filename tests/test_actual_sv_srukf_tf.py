from __future__ import annotations

from pathlib import Path

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

import bayesfilter.highdim as highdim
from bayesfilter.nonlinear.srukf_route_guard import assert_no_forbidden_srukf_routes


ROOT = Path(__file__).resolve().parents[1]
ADMITTED_ACTUAL_SV_SRUKF = ROOT / "bayesfilter" / "highdim" / "actual_sv_srukf_tf.py"
STD_NORMAL = tfp.distributions.Normal(
    loc=tf.constant(0.0, dtype=tf.float64),
    scale=tf.constant(1.0, dtype=tf.float64),
)


def _observations(dim: int) -> tf.Tensor:
    values = tf.constant(
        [
            [0.35, -0.20, 0.55],
            [0.72, 0.18, -0.45],
            [-0.11, 0.44, 0.30],
        ],
        dtype=tf.float64,
    )
    return values[:, :dim]


def _theta_from_physical(gamma: tf.Tensor, beta: tf.Tensor) -> tf.Tensor:
    return tf.reshape(tf.stack([STD_NORMAL.quantile(gamma), tf.math.log(beta)], axis=1), [-1])


def _physical_from_theta(theta: tf.Tensor, dim: int) -> tuple[tf.Tensor, tf.Tensor]:
    theta_matrix = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [dim, 2])
    return STD_NORMAL.cdf(theta_matrix[:, 0]), tf.exp(theta_matrix[:, 1])


def _centered_finite_difference_score(value_fn, theta: tf.Tensor, eps: float = 1e-5) -> tf.Tensor:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=tf.float64), [-1])
    rows = []
    for parameter_index in range(int(theta.shape[0])):
        direction = tf.one_hot(parameter_index, int(theta.shape[0]), dtype=tf.float64)
        plus = value_fn(theta + eps * direction)
        minus = value_fn(theta - eps * direction)
        rows.append((plus - minus) / (2.0 * eps))
    return tf.stack(rows)


def test_actual_sv_srukf_admitted_module_passes_route_guard() -> None:
    assert assert_no_forbidden_srukf_routes([ADMITTED_ACTUAL_SV_SRUKF]) == ()


def test_actual_sv_srukf_short_prefix_finite_and_dimensioned() -> None:
    observations = _observations(2)
    gamma = tf.constant([0.55, 0.68], dtype=tf.float64)
    beta = tf.constant([0.90, 1.15], dtype=tf.float64)
    sigma = tf.constant([0.22, 0.35], dtype=tf.float64)

    result = highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )

    assert result.log_normalizers.shape == (3,)
    assert result.score.shape == (4,)
    assert result.mean_path.shape == (3, 2)
    assert result.covariance_path.shape == (3, 2, 2)
    assert result.factor_path.shape == (3, 2, 2)
    assert result.d_mean_path.shape == (3, 4, 2)
    assert result.d_covariance_path.shape == (3, 4, 2, 2)
    assert result.d_factor_path.shape == (3, 4, 2, 2)
    assert bool(tf.math.is_finite(result.log_likelihood).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(result.score)).numpy())
    assert result.diagnostics["score_provenance"] == "manual_factor_branch_analytical_score"
    assert result.diagnostics["wrapper_score_contract"] == "factor_propagating_srukf_manual_score"
    assert result.diagnostics["augmented_variable"] == "A_t=(H_{t-1}, U_t, E_t)"


def test_actual_sv_srukf_t1_score_matches_centered_finite_difference() -> None:
    observations = tf.constant([[0.35]], dtype=tf.float64)
    gamma = tf.constant([0.55], dtype=tf.float64)
    beta = tf.constant([0.90], dtype=tf.float64)
    sigma = tf.constant([0.22], dtype=tf.float64)
    theta = _theta_from_physical(gamma, beta)

    analytic = highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )

    def same_scalar_objective(current_theta: tf.Tensor) -> tf.Tensor:
        current_gamma, current_beta = _physical_from_theta(current_theta, 1)
        return highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
            observations,
            gamma=current_gamma,
            beta=current_beta,
            sigma=sigma,
        ).log_likelihood

    finite_difference = _centered_finite_difference_score(same_scalar_objective, theta)
    np.testing.assert_allclose(analytic.score.numpy(), finite_difference.numpy(), atol=2e-5, rtol=2e-5)


def test_actual_sv_srukf_same_scalar_score_matches_centered_finite_difference() -> None:
    dim = 2
    observations = _observations(dim)
    gamma = tf.constant([0.55, 0.68], dtype=tf.float64)
    beta = tf.constant([0.90, 1.15], dtype=tf.float64)
    sigma = tf.constant([0.22, 0.35], dtype=tf.float64)
    theta = _theta_from_physical(gamma, beta)

    analytic = highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
        observations,
        gamma=gamma,
        beta=beta,
        sigma=sigma,
    )

    def same_scalar_objective(current_theta: tf.Tensor) -> tf.Tensor:
        current_gamma, current_beta = _physical_from_theta(current_theta, dim)
        return highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
            observations,
            gamma=current_gamma,
            beta=current_beta,
            sigma=sigma,
        ).log_likelihood

    finite_difference = _centered_finite_difference_score(same_scalar_objective, theta)
    np.testing.assert_allclose(analytic.score.numpy(), finite_difference.numpy(), atol=2e-5, rtol=2e-5)


def test_actual_sv_srukf_parameterization_rejects_free_sigma_score() -> None:
    observations = _observations(1)
    result = highdim.actual_transformed_sv_independent_panel_augmented_noise_srukf_score(
        observations,
        gamma=0.55,
        beta=0.90,
        sigma=0.22,
    )

    assert result.score.shape == (2,)
    assert "fixed sigma" in result.diagnostics["parameterization"]
    assert "no leaderboard admission before the downstream ladder" in result.diagnostics["non_claims"]
