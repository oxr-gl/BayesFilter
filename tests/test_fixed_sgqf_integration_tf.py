import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf

import bayesfilter
from bayesfilter.nonlinear import (
    TFFixedSGQFBranchConfig,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
    tf_fixed_sgqf_p47_one_step_oracle,
    tf_fixed_sgqf_score,
)
from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import TFFixedSGQFDerivatives


def _score_fixture():
    oracle, cloud = tf_fixed_sgqf_p47_one_step_oracle()
    model = oracle.model()
    derivatives = TFFixedSGQFDerivatives(
        d_initial_mean=tf.zeros([1, 1], dtype=tf.float64),
        d_initial_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        d_process_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        d_observation_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        transition_state_jacobian_fn=lambda points: tf.ones([tf.shape(points)[0], 1, 1], dtype=tf.float64),
        d_transition_fn=lambda points: tf.convert_to_tensor(points, dtype=tf.float64)[tf.newaxis, :, :],
        observation_state_jacobian_fn=lambda points: 2.0 * tf.convert_to_tensor(points, dtype=tf.float64)[:, tf.newaxis, :],
        d_observation_fn=lambda points: tf.zeros([1, tf.shape(points)[0], 1], dtype=tf.float64),
        name="m5_score_fixture",
    )
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    return oracle.observation, model, derivatives, cloud, branch


def test_fixed_sgqf_symbols_are_exposed_through_nonlinear_and_top_level_api() -> None:
    assert hasattr(bayesfilter.nonlinear, "tf_fixed_sgqf_filter")
    assert hasattr(bayesfilter.nonlinear, "tf_fixed_sgqf_score")
    assert hasattr(bayesfilter, "tf_fixed_sgqf_filter")
    assert hasattr(bayesfilter, "tf_fixed_sgqf_score")
    assert "tf_fixed_sgqf_filter" in bayesfilter.__all__
    assert "tf_fixed_sgqf_score" in bayesfilter.__all__


def test_fixed_sgqf_value_api_is_deterministic_across_repeated_calls() -> None:
    oracle, cloud = tf_fixed_sgqf_p47_one_step_oracle()
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    branch_identity = branch.branch_identity(cloud)
    first = tf_fixed_sgqf_filter(
        oracle.observation,
        oracle.model(),
        cloud=cloud,
        branch_config=branch,
        branch_identity=branch_identity,
        return_filtered=True,
    )
    second = tf_fixed_sgqf_filter(
        oracle.observation,
        oracle.model(),
        cloud=cloud,
        branch_config=branch,
        branch_identity=branch_identity,
        return_filtered=True,
    )

    np.testing.assert_allclose(first.log_likelihood.numpy(), second.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(first.filtered_means.numpy(), second.filtered_means.numpy(), atol=1e-12)
    np.testing.assert_allclose(first.filtered_covariances.numpy(), second.filtered_covariances.numpy(), atol=1e-12)


def test_fixed_sgqf_score_api_is_deterministic_across_repeated_calls() -> None:
    observations, model, derivatives, cloud, branch = _score_fixture()
    branch_identity = branch.branch_identity(cloud)
    first = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
        branch_identity=branch_identity,
    )
    second = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
        branch_identity=branch_identity,
    )

    np.testing.assert_allclose(first.log_likelihood.numpy(), second.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(first.score.numpy(), second.score.numpy(), atol=1e-12)


def test_fixed_sgqf_end_to_end_value_and_score_integration_on_p47_oracle() -> None:
    observations, model, derivatives, cloud, branch = _score_fixture()
    value_result = tf_fixed_sgqf_filter(observations, model, cloud=cloud, branch_config=branch, return_filtered=True)
    score_result = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value_result.branch_identity,
    )

    assert value_result.failure is None
    assert score_result.failure is None
    np.testing.assert_allclose(value_result.log_likelihood.numpy(), np.array(-1.7830736342), atol=1e-10)
    np.testing.assert_allclose(score_result.score.numpy(), np.array([-1.0535424554]), atol=1e-8)
    assert score_result.branch_identity == value_result.branch_identity
