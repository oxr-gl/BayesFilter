from __future__ import annotations

import ast
import inspect
import os
from dataclasses import fields

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

from bayesfilter.linear.stationary_lgssm_derivatives_tf import (
    continuous_lyapunov_first_derivatives_tf,
    continuous_lyapunov_solution_tf,
    diffusion_from_cholesky_first_derivatives_tf,
    matrix_exponential_frechet_tf,
    stationary_lgssm_first_derivative_coverage,
    stationary_lgssm_from_continuous_first_derivatives_tf,
)
from bayesfilter.linear.types_tf import TFLinearGaussianStateSpaceFirstDerivatives
from bayesfilter.linear import stationary_lgssm_derivatives_tf as stationary_module


def _fixture() -> dict[str, tf.Tensor]:
    p = 4
    drift = tf.constant([[1.4, 0.15], [0.05, 1.2]], dtype=tf.float64)
    mean = tf.constant([0.25, -0.15], dtype=tf.float64)
    sigma = tf.constant([[0.5, 0.0], [0.1, 0.4]], dtype=tf.float64)
    obs_offset = tf.constant([0.03, -0.02], dtype=tf.float64)
    obs_matrix = tf.constant([[1.0, 0.2], [-0.1, 0.7]], dtype=tf.float64)
    obs_cov = tf.constant([[0.2, 0.03], [0.03, 0.25]], dtype=tf.float64)

    d_drift = np.zeros((p, 2, 2), dtype=np.float64)
    d_drift[0, 0, 0] = 0.2
    d_drift[0, 1, 0] = -0.05

    d_mean = np.zeros((p, 2), dtype=np.float64)
    d_mean[1, :] = [0.3, -0.2]

    d_sigma = np.zeros((p, 2, 2), dtype=np.float64)
    d_sigma[2, 0, 0] = 0.15
    d_sigma[2, 1, 0] = -0.03

    d_obs_offset = np.zeros((p, 2), dtype=np.float64)
    d_obs_offset[3, :] = [0.05, -0.04]
    d_obs_matrix = np.zeros((p, 2, 2), dtype=np.float64)
    d_obs_matrix[3, 0, 1] = 0.12
    d_obs_matrix[3, 1, 0] = -0.08
    d_obs_cov = np.zeros((p, 2, 2), dtype=np.float64)
    d_obs_cov[3, 0, 0] = 0.02
    d_obs_cov[3, 1, 1] = -0.01

    return {
        "drift": drift,
        "long_run_mean": mean,
        "diffusion_factor": sigma,
        "observation_offset": obs_offset,
        "observation_matrix": obs_matrix,
        "observation_covariance": obs_cov,
        "d_drift": tf.constant(d_drift, dtype=tf.float64),
        "d_long_run_mean": tf.constant(d_mean, dtype=tf.float64),
        "d_diffusion_factor": tf.constant(d_sigma, dtype=tf.float64),
        "d_observation_offset": tf.constant(d_obs_offset, dtype=tf.float64),
        "d_observation_matrix": tf.constant(d_obs_matrix, dtype=tf.float64),
        "d_observation_covariance": tf.constant(d_obs_cov, dtype=tf.float64),
    }


def _model_from_primitive_shift(data: dict[str, tf.Tensor], index: int, scale: float):
    shifted = {
        "drift": data["drift"] + scale * data["d_drift"][index],
        "long_run_mean": data["long_run_mean"] + scale * data["d_long_run_mean"][index],
        "diffusion_factor": data["diffusion_factor"]
        + scale * data["d_diffusion_factor"][index],
        "observation_offset": data["observation_offset"]
        + scale * data["d_observation_offset"][index],
        "observation_matrix": data["observation_matrix"]
        + scale * data["d_observation_matrix"][index],
        "observation_covariance": data["observation_covariance"]
        + scale * data["d_observation_covariance"][index],
    }
    model, _ = stationary_lgssm_from_continuous_first_derivatives_tf(
        **shifted,
        d_drift=data["d_drift"],
        d_long_run_mean=data["d_long_run_mean"],
        d_diffusion_factor=data["d_diffusion_factor"],
        d_observation_offset=data["d_observation_offset"],
        d_observation_matrix=data["d_observation_matrix"],
        d_observation_covariance=data["d_observation_covariance"],
    )
    return model


def test_matrix_exponential_frechet_matches_central_difference() -> None:
    matrix = tf.constant([[-1.2, 0.15], [0.05, -0.9]], dtype=tf.float64)
    directions = tf.constant(
        [[[0.1, -0.2], [0.0, 0.05]], [[0.0, 0.3], [-0.1, 0.0]]],
        dtype=tf.float64,
    )

    _, derivatives = matrix_exponential_frechet_tf(matrix, directions)

    eps = 1.0e-5
    for index in range(int(directions.shape[0])):
        plus = tf.linalg.expm(matrix + eps * directions[index])
        minus = tf.linalg.expm(matrix - eps * directions[index])
        finite_difference = (plus - minus) / (2.0 * eps)
        np.testing.assert_allclose(
            derivatives[index].numpy(),
            finite_difference.numpy(),
            rtol=2.0e-6,
            atol=2.0e-7,
        )


def test_continuous_lyapunov_derivatives_match_residual_and_finite_difference() -> None:
    drift = tf.constant([[1.4, 0.2], [0.1, 1.1]], dtype=tf.float64)
    diffusion = tf.constant([[0.5, 0.1], [0.1, 0.3]], dtype=tf.float64)
    d_drift = tf.constant(
        [[[0.1, 0.0], [0.0, 0.0]], [[0.0, 0.2], [0.0, 0.0]]],
        dtype=tf.float64,
    )
    d_diffusion = tf.constant(
        [[[0.0, 0.1], [0.1, 0.0]], [[0.2, 0.0], [0.0, 0.0]]],
        dtype=tf.float64,
    )

    omega, d_omega = continuous_lyapunov_first_derivatives_tf(
        drift=drift,
        diffusion=diffusion,
        d_drift=d_drift,
        d_diffusion=d_diffusion,
    )

    base_residual = drift @ omega + omega @ tf.transpose(drift) - diffusion
    np.testing.assert_allclose(base_residual.numpy(), np.zeros((2, 2)), atol=2.0e-14)
    derivative_residual = (
        drift[None, :, :] @ d_omega
        + d_omega @ tf.transpose(drift)[None, :, :]
        - d_diffusion
        + d_drift @ omega
        + omega[None, :, :] @ tf.linalg.matrix_transpose(d_drift)
    )
    np.testing.assert_allclose(
        derivative_residual.numpy(),
        np.zeros((2, 2, 2)),
        atol=2.0e-13,
    )

    eps = 1.0e-5
    for index in range(2):
        plus = continuous_lyapunov_solution_tf(
            drift + eps * d_drift[index],
            diffusion + eps * d_diffusion[index],
        )
        minus = continuous_lyapunov_solution_tf(
            drift - eps * d_drift[index],
            diffusion - eps * d_diffusion[index],
        )
        finite_difference = (plus - minus) / (2.0 * eps)
        np.testing.assert_allclose(
            d_omega[index].numpy(),
            finite_difference.numpy(),
            rtol=2.0e-6,
            atol=2.0e-7,
        )


def test_diffusion_from_cholesky_derivatives_match_finite_difference() -> None:
    data = _fixture()
    diffusion, d_diffusion = diffusion_from_cholesky_first_derivatives_tf(
        data["diffusion_factor"],
        data["d_diffusion_factor"],
    )

    np.testing.assert_allclose(
        diffusion.numpy(),
        (data["diffusion_factor"] @ tf.transpose(data["diffusion_factor"])).numpy(),
    )
    eps = 1.0e-5
    for index in range(4):
        plus_factor = data["diffusion_factor"] + eps * data["d_diffusion_factor"][index]
        minus_factor = data["diffusion_factor"] - eps * data["d_diffusion_factor"][index]
        plus = plus_factor @ tf.transpose(plus_factor)
        minus = minus_factor @ tf.transpose(minus_factor)
        finite_difference = (plus - minus) / (2.0 * eps)
        np.testing.assert_allclose(
            d_diffusion[index].numpy(),
            finite_difference.numpy(),
            rtol=2.0e-6,
            atol=2.0e-7,
        )


def test_stationary_lgssm_builder_derivatives_match_central_difference() -> None:
    data = _fixture()
    model, derivatives = stationary_lgssm_from_continuous_first_derivatives_tf(**data)

    expected_initial_mean = data["long_run_mean"]
    np.testing.assert_allclose(model.initial_mean.numpy(), expected_initial_mean.numpy())
    np.testing.assert_allclose(
        derivatives.d_initial_mean.numpy(),
        data["d_long_run_mean"].numpy(),
        rtol=2.0e-6,
        atol=2.0e-7,
    )

    derivative_pairs = {
        "initial_mean": "d_initial_mean",
        "initial_covariance": "d_initial_covariance",
        "transition_offset": "d_transition_offset",
        "transition_matrix": "d_transition_matrix",
        "transition_covariance": "d_transition_covariance",
        "observation_offset": "d_observation_offset",
        "observation_matrix": "d_observation_matrix",
        "observation_covariance": "d_observation_covariance",
    }
    eps = 1.0e-5
    for index in range(4):
        plus = _model_from_primitive_shift(data, index, eps)
        minus = _model_from_primitive_shift(data, index, -eps)
        for model_field, derivative_field in derivative_pairs.items():
            finite_difference = (
                getattr(plus, model_field) - getattr(minus, model_field)
            ) / (2.0 * eps)
            np.testing.assert_allclose(
                getattr(derivatives, derivative_field)[index].numpy(),
                finite_difference.numpy(),
                rtol=4.0e-6,
                atol=3.0e-7,
            )


def test_stationary_lgssm_coverage_reports_missing_zero_parameter() -> None:
    data = _fixture()
    _, derivatives = stationary_lgssm_from_continuous_first_derivatives_tf(**data)

    coverage = stationary_lgssm_first_derivative_coverage(
        ("drift", "mean", "diffusion", "measurement"),
        derivatives,
    )

    assert coverage.coverage_complete is True
    assert coverage.covered_parameter_names == ("drift", "mean", "diffusion", "measurement")
    assert coverage.missing_parameter_names == ()

    values = {
        field.name: getattr(derivatives, field.name).numpy()
        for field in fields(TFLinearGaussianStateSpaceFirstDerivatives)
    }
    for value in values.values():
        value[3, ...] = 0.0
    partial = TFLinearGaussianStateSpaceFirstDerivatives(
        **{name: tf.constant(value, dtype=tf.float64) for name, value in values.items()}
    )
    partial_coverage = stationary_lgssm_first_derivative_coverage(
        ("drift", "mean", "diffusion", "measurement"),
        partial,
    )

    assert partial_coverage.coverage_complete is False
    assert partial_coverage.missing_parameter_names == ("measurement",)


def test_stationary_lgssm_derivative_runtime_uses_no_generic_jacobian_builder() -> None:
    source = inspect.getsource(stationary_module)
    tree = ast.parse(source)

    forbidden_attrs = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute) and node.attr in {"GradientTape", "jacobian"}
    }

    assert forbidden_attrs == set()
