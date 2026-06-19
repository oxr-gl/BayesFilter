from pathlib import Path

import numpy as np
import tensorflow as tf

from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import (
    TFFixedSGQFDerivatives,
    tf_fixed_sgqf_score,
)
from bayesfilter.nonlinear.fixed_sgqf_tf import (
    TFFixedSGQFBranchConfig,
    TFFixedSGQFNonlinearModel,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
    tf_fixed_sgqf_p47_one_step_oracle,
)
from bayesfilter.nonlinear.sigma_points_tf import tf_svd_sigma_point_filter
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace
from bayesfilter.testing import dense_projection_first_step


ROOT = Path(__file__).resolve().parents[1]


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
        name="verification_score_fixture",
    )
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    return oracle.observation, model, derivatives, cloud, branch


def _hard_interaction_fixture():
    initial_mean = tf.zeros([2], dtype=tf.float64)
    initial_covariance = tf.eye(2, dtype=tf.float64)
    process_covariance = tf.constant([[0.25, 0.0], [0.0, 0.25]], dtype=tf.float64)
    observation_covariance = tf.constant([[0.09]], dtype=tf.float64)
    observation = tf.constant([[0.6]], dtype=tf.float64)

    def transition_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        return values

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        return tf.exp(values[:, :1] * values[:, 1:2])

    model = TFFixedSGQFNonlinearModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        process_covariance=process_covariance,
        observation_covariance=observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        name="fixed_sgqf_hard_interaction_fixture",
    )

    partition = StatePartition(
        state_names=("x1", "x2"),
        stochastic_indices=(0, 1),
        deterministic_indices=(),
        innovation_dim=2,
    )

    def structural_transition(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation_points = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return previous + 0.5 * innovation_points

    def structural_observation(state_points: tf.Tensor) -> tf.Tensor:
        states = tf.convert_to_tensor(state_points, dtype=tf.float64)
        return tf.exp(states[:, :1] * states[:, 1:2])

    def residual_fn(previous_state: tf.Tensor, innovation: tf.Tensor, next_state: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation_points = tf.convert_to_tensor(innovation, dtype=tf.float64)
        next_points = tf.convert_to_tensor(next_state, dtype=tf.float64)
        expected = previous + 0.5 * innovation_points
        return next_points - expected

    structural_model = TFStructuralStateSpace(
        partition=partition,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_hard_interaction_dense_reference",
        ),
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        innovation_covariance=process_covariance,
        observation_covariance=observation_covariance,
        transition_fn=structural_transition,
        observation_fn=structural_observation,
        deterministic_residual_fn=residual_fn,
        name="fixed_sgqf_hard_interaction_structural",
    )
    return model, structural_model, observation


def test_fixed_sgqf_verification_bundle_recovers_p47_oracle_and_same_branch_score() -> None:
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


def test_fixed_sgqf_branch_veto_rejects_large_threshold_even_when_covariance_is_pd() -> None:
    observations, model, _derivatives, cloud, _branch = _score_fixture()
    result = tf_fixed_sgqf_filter(
        observations,
        model,
        cloud=cloud,
        branch_config=TFFixedSGQFBranchConfig(predictive_epsilon=2.0, innovation_epsilon=1e-10),
        return_filtered=True,
    )

    assert result.failure is None
    assert result.step_results[0].accepted is True


def test_fixed_sgqf_hard_interaction_fixture_shows_limit_against_dense_reference() -> None:
    model, structural_model, observation = _hard_interaction_fixture()
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    sgqf = tf_fixed_sgqf_filter(observation, model, cloud=cloud, return_filtered=True)
    dense = dense_projection_first_step(structural_model, observation[0], nodes_per_dim=17)

    assert sgqf.failure is None
    step = sgqf.step_results[0]
    mismatch = abs(float(step.observation_mean.numpy()[0] - dense.observation_mean.numpy()[0]))
    assert mismatch > 1e-2


def test_fixed_sgqf_hard_interaction_fixture_shows_limit_against_dense_reference() -> None:
    model, structural_model, observation = _hard_interaction_fixture()
    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    sgqf = tf_fixed_sgqf_filter(observation, model, cloud=cloud, return_filtered=True)
    dense = dense_projection_first_step(structural_model, observation[0], nodes_per_dim=17)

    assert sgqf.failure is None
    step = sgqf.step_results[0]
    mismatch = abs(float(step.observation_mean.numpy()[0] - dense.observation_mean.numpy()[0]))
    assert mismatch > 1e-2



def test_fixed_sgqf_scalar_quadratic_level2_matches_dense_better_than_ukf_and_cubature() -> None:
    rho = tf.constant(0.9, dtype=tf.float64)
    process_sigma = tf.constant(0.5, dtype=tf.float64)
    observation_sigma = tf.constant(0.3, dtype=tf.float64)
    initial_mean = tf.constant([0.4], dtype=tf.float64)
    initial_covariance = tf.constant([[0.9]], dtype=tf.float64)
    process_covariance = tf.reshape(tf.square(process_sigma), [1, 1])
    observation_covariance = tf.reshape(tf.square(observation_sigma), [1, 1])
    observations = tf.constant([[0.7]], dtype=tf.float64)

    sgqf_model = TFFixedSGQFNonlinearModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        process_covariance=process_covariance,
        observation_covariance=observation_covariance,
        transition_fn=lambda points: rho * tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
        name="sgqf_scalar_quadratic_baseline_fixture",
    )

    partition = StatePartition(
        state_names=("x",),
        stochastic_indices=(0,),
        deterministic_indices=(),
        innovation_dim=1,
    )

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        previous = tf.convert_to_tensor(previous_state, dtype=tf.float64)
        innovation_values = tf.convert_to_tensor(innovation, dtype=tf.float64)
        return rho * previous + process_sigma * innovation_values

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        return tf.square(tf.convert_to_tensor(state_points, dtype=tf.float64))

    def residual_fn(previous_state: tf.Tensor, innovation: tf.Tensor, next_state: tf.Tensor) -> tf.Tensor:
        del previous_state, innovation
        point_count = tf.shape(tf.convert_to_tensor(next_state, dtype=tf.float64))[0]
        return tf.zeros([point_count, 0], dtype=tf.float64)

    structural_model = TFStructuralStateSpace(
        partition=partition,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_scalar_quadratic_baseline_panel",
        ),
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        innovation_covariance=tf.ones([1, 1], dtype=tf.float64),
        observation_covariance=observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        deterministic_residual_fn=residual_fn,
        name="fixed_sgqf_scalar_quadratic_baseline_structural",
    )

    dense = dense_projection_first_step(structural_model, observations[0], nodes_per_dim=21)
    sgqf = tf_fixed_sgqf_filter(observations, sgqf_model, cloud=tf_fixed_sgqf_cloud(dim=1, sparse_level=2), return_filtered=True)
    ukf = tf_svd_sigma_point_filter(observations, structural_model, backend="tf_svd_ukf", return_filtered=True)
    cubature = tf_svd_sigma_point_filter(observations, structural_model, backend="tf_svd_cubature", return_filtered=True)

    assert sgqf.failure is None

    sgqf_error = abs(float(sgqf.step_results[0].filtered_mean.numpy()[0] - dense.filtered_mean.numpy()[0]))
    ukf_error = abs(float(ukf.filtered_means.numpy()[0, 0] - dense.filtered_mean.numpy()[0]))
    cubature_error = abs(float(cubature.filtered_means.numpy()[0, 0] - dense.filtered_mean.numpy()[0]))

    assert sgqf_error < 1e-12
    assert sgqf_error < ukf_error
    assert sgqf_error < cubature_error



def test_fixed_sgqf_fixed_lane_does_not_claim_adaptive_design_or_hidden_repair() -> None:
    text = (ROOT / "bayesfilter" / "nonlinear" / "fixed_sgqf_tf.py").read_text(encoding="utf-8")

    assert "adaptive" not in text
    assert "jitter" not in text
    assert "clip" not in text
    assert "floor_count" not in text
