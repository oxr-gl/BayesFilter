from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest
import tensorflow as tf

from bayesfilter.nonlinear.srukf_factor_tf import (
    TFSRUKFStepDerivatives,
    tf_srukf_factor_score_step,
    tf_srukf_unit_sigma_point_rule,
)
from bayesfilter.nonlinear.srukf_route_guard import (
    assert_no_forbidden_srukf_routes,
    find_forbidden_srukf_routes,
)


ROOT = Path(__file__).resolve().parents[1]
SRUKF_BACKEND = ROOT / "bayesfilter" / "nonlinear" / "srukf_factor_tf.py"


def _linear_result(theta: float):
    mean = tf.constant([theta, 0.0], dtype=tf.float64)
    factor = tf.eye(2, dtype=tf.float64)
    observation = tf.constant([0.25], dtype=tf.float64)
    derivatives = TFSRUKFStepDerivatives(
        d_augmented_mean=tf.constant([[1.0, 0.0]], dtype=tf.float64),
        d_augmented_factor=tf.zeros([1, 2, 2], dtype=tf.float64),
        transition_jacobian_fn=lambda points: tf.broadcast_to(
            tf.constant([[[1.0, 0.0]]], dtype=tf.float64),
            [tf.shape(points)[0], 1, 2],
        ),
        d_transition_fn=lambda points: tf.zeros([1, tf.shape(points)[0], 1], dtype=tf.float64),
        observation_jacobian_fn=lambda points: tf.broadcast_to(
            tf.constant([[[2.0, 1.0]]], dtype=tf.float64),
            [tf.shape(points)[0], 1, 2],
        ),
        d_observation_fn=lambda points: tf.zeros([1, tf.shape(points)[0], 1], dtype=tf.float64),
    )
    return tf_srukf_factor_score_step(
        observation,
        mean,
        factor,
        transition_fn=lambda points: points[:, 0:1],
        observation_fn=lambda points: 2.0 * points[:, 0:1] + points[:, 1:2],
        derivatives=derivatives,
        rule=tf_srukf_unit_sigma_point_rule(2, rule="cubature"),
    )


def test_srukf_factor_score_matches_linear_gaussian_closed_form_and_fd() -> None:
    theta = 0.1
    result = _linear_result(theta)
    innovation = 0.25 - 2.0 * theta
    expected_loglik = -0.5 * (np.log(2.0 * np.pi * 5.0) + innovation**2 / 5.0)
    expected_score = 2.0 * innovation / 5.0

    np.testing.assert_allclose(result.log_likelihood.numpy(), expected_loglik, atol=1e-12)
    np.testing.assert_allclose(result.score.numpy(), [expected_score], atol=1e-12)
    np.testing.assert_allclose(result.filtered_mean.numpy(), [theta + 2.0 * innovation / 5.0], atol=1e-12)

    eps = 1e-5
    plus = _linear_result(theta + eps).log_likelihood.numpy()
    minus = _linear_result(theta - eps).log_likelihood.numpy()
    finite_difference = (plus - minus) / (2.0 * eps)
    np.testing.assert_allclose(result.score.numpy()[0], finite_difference, atol=1e-9)


def test_srukf_factor_diagnostics_report_small_reconstruction_residuals() -> None:
    result = _linear_result(0.1)

    for key in (
        "state_factor_reconstruction_residual",
        "innovation_factor_reconstruction_residual",
        "filtered_factor_reconstruction_residual",
        "filtered_factor_derivative_residual",
        "innovation_solve_residual",
    ):
        assert float(result.diagnostics[key].numpy()) < 1e-10
    assert result.diagnostics["score_provenance"] == "manual_factor_branch_analytical_score"
    assert result.diagnostics["derivative_target"] == "implemented_factor_branch"


def test_srukf_backend_source_passes_static_route_guard() -> None:
    assert assert_no_forbidden_srukf_routes([SRUKF_BACKEND]) == ()


@pytest.mark.parametrize(
    "snippet",
    [
        "with tf.GradientTape() as tape: pass",
        "tf_svd_sigma_point_filter(observations, model)",
        "historical eigenderivative helper",
        "strict_spd_principal_sqrt_first_derivatives(cov, dcov)",
        "principal_sqrt_frechet_derivative(cov, dcov)",
    ],
)
def test_srukf_route_guard_rejects_forbidden_route_families(snippet: str) -> None:
    violations = find_forbidden_srukf_routes(snippet)
    assert violations, snippet


def test_srukf_route_guard_assertion_rejects_forbidden_file(tmp_path: Path) -> None:
    bad_path = tmp_path / "bad_backend.py"
    bad_path.write_text("tf_svd_sigma_point_filter(observations, model)\n", encoding="utf-8")

    with pytest.raises(ValueError, match="forbidden_srukf_route_detected"):
        assert_no_forbidden_srukf_routes([bad_path])
