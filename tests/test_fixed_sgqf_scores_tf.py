import numpy as np
import tensorflow as tf

from bayesfilter.nonlinear.fixed_sgqf_derivatives_tf import (
    TFFixedSGQFDerivatives,
    tf_fixed_sgqf_same_branch_signature,
    tf_fixed_sgqf_score,
)
from bayesfilter.nonlinear.fixed_sgqf_tf import (
    TFFixedSGQFBranchConfig,
    TFFixedSGQFBranchIdentity,
    TFFixedSGQFCloud,
    TFFixedSGQFNonlinearModel,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
    tf_fixed_sgqf_p47_one_step_oracle,
)


def _p47_scalar_score_fixture() -> tuple[
    TFFixedSGQFNonlinearModel,
    TFFixedSGQFDerivatives,
    TFFixedSGQFCloud,
    tf.Tensor,
    TFFixedSGQFBranchConfig,
]:
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
        name="p47_scalar_score_fixture",
    )
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    return model, derivatives, cloud, oracle.observation, branch


def _finite_difference_score(
    observations: tf.Tensor,
    cloud: TFFixedSGQFCloud,
    branch: TFFixedSGQFBranchConfig,
    beta: float,
    step: float = 1e-6,
) -> float:
    def value_at(beta_value: float) -> float:
        oracle, _cloud = tf_fixed_sgqf_p47_one_step_oracle()
        shifted_model = TFFixedSGQFNonlinearModel(
            initial_mean=oracle.initial_mean,
            initial_covariance=oracle.initial_covariance,
            process_covariance=oracle.process_covariance,
            observation_covariance=oracle.observation_covariance,
            transition_fn=lambda points: tf.convert_to_tensor(beta_value, dtype=tf.float64)
            * tf.convert_to_tensor(points, dtype=tf.float64),
            observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
            name="p47_scalar_score_fd_model",
        )
        result = tf_fixed_sgqf_filter(observations, shifted_model, cloud=cloud, branch_config=branch, return_filtered=True)
        if result.failure is not None:
            raise AssertionError("finite-difference evaluation left the declared branch")
        return float(result.log_likelihood.numpy())

    return (value_at(beta + step) - value_at(beta - step)) / (2.0 * step)


def test_fixed_sgqf_p47_one_step_analytic_score_matches_oracle_and_fd() -> None:
    model, derivatives, cloud, observations, branch = _p47_scalar_score_fixture()
    value_result = tf_fixed_sgqf_filter(observations, model, cloud=cloud, branch_config=branch, return_filtered=True)
    score_result = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=value_result.branch_identity,
    )
    finite_difference = _finite_difference_score(observations, cloud, branch, beta=1.0)

    assert value_result.failure is None
    assert score_result.failure is None
    np.testing.assert_allclose(score_result.log_likelihood.numpy(), value_result.log_likelihood.numpy(), atol=1e-12)
    np.testing.assert_allclose(score_result.score.numpy(), np.array([-1.0535424554]), atol=1e-8)
    np.testing.assert_allclose(score_result.score.numpy(), np.array([finite_difference]), atol=2e-5, rtol=2e-5)
    assert score_result.diagnostics["derivative_method"] == "analytic_first_order_fixed_branch"


def test_fixed_sgqf_score_rejects_expected_branch_mismatch() -> None:
    model, derivatives, cloud, observations, branch = _p47_scalar_score_fixture()
    other_cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=3)
    expected_identity = branch.branch_identity(other_cloud)

    result = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
        expected_branch_identity=expected_identity,
    )

    assert result.failure is not None
    assert result.failure.reason == "same_scalar_branch_mismatch"
    assert result.score is None


def test_fixed_sgqf_same_branch_signature_tracks_failure_stage() -> None:
    model, derivatives, cloud, observations, branch = _p47_scalar_score_fixture()
    blocked_model = TFFixedSGQFNonlinearModel(
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        process_covariance=tf.constant([[-2.0]], dtype=tf.float64),
        observation_covariance=model.observation_covariance,
        transition_fn=model.transition_fn,
        observation_fn=model.observation_fn,
        name="blocked_score_fixture",
    )

    result = tf_fixed_sgqf_score(
        observations,
        blocked_model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
    )

    assert result.failure is not None
    assert result.failure.stage == "predictive_covariance"
    assert result.diagnostics["same_branch_signature"][1] == "predictive_covariance"



def test_fixed_sgqf_score_tracks_carried_covariance_failure_signature() -> None:
    observations = tf.constant([[0.7]], dtype=tf.float64)
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=3)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    model = TFFixedSGQFNonlinearModel(
        initial_mean=tf.constant([0.4], dtype=tf.float64),
        initial_covariance=tf.constant([[0.9]], dtype=tf.float64),
        process_covariance=tf.constant([[0.25]], dtype=tf.float64),
        observation_covariance=tf.constant([[0.09]], dtype=tf.float64),
        transition_fn=lambda points: 0.9 * tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
        name="carried_failure_score_fixture",
    )
    derivatives = TFFixedSGQFDerivatives(
        d_initial_mean=tf.zeros([1, 1], dtype=tf.float64),
        d_initial_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        d_process_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        d_observation_covariance=tf.zeros([1, 1, 1], dtype=tf.float64),
        transition_state_jacobian_fn=lambda points: tf.ones([tf.shape(points)[0], 1, 1], dtype=tf.float64) * 0.9,
        d_transition_fn=lambda points: tf.zeros([1, tf.shape(points)[0], 1], dtype=tf.float64),
        observation_state_jacobian_fn=lambda points: 2.0 * tf.convert_to_tensor(points, dtype=tf.float64)[:, tf.newaxis, :],
        d_observation_fn=lambda points: tf.zeros([1, tf.shape(points)[0], 1], dtype=tf.float64),
        name="carried_failure_score_derivatives",
    )

    result = tf_fixed_sgqf_score(
        observations,
        model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
    )

    assert result.failure is not None
    assert result.failure.stage == "carried_covariance"
    assert result.diagnostics["same_branch_signature"][1] == "carried_covariance"



def test_fixed_sgqf_scalar_quadratic_multistep_score_matches_finite_difference_for_multiple_parameters() -> None:
    observations = tf.constant([[0.7], [0.1]], dtype=tf.float64)
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    params = {"mu0": 0.4, "beta": 0.9, "q": 0.25, "r": 0.09}

    model = TFFixedSGQFNonlinearModel(
        initial_mean=tf.constant([params["mu0"]], dtype=tf.float64),
        initial_covariance=tf.constant([[0.9]], dtype=tf.float64),
        process_covariance=tf.constant([[params["q"]]], dtype=tf.float64),
        observation_covariance=tf.constant([[params["r"]]], dtype=tf.float64),
        transition_fn=lambda points: params["beta"] * tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
        name="multistep_multi_parameter_score_fixture",
    )
    derivatives = TFFixedSGQFDerivatives(
        d_initial_mean=tf.constant([[1.0], [0.0], [0.0], [0.0]], dtype=tf.float64),
        d_initial_covariance=tf.zeros([4, 1, 1], dtype=tf.float64),
        d_process_covariance=tf.constant([[[0.0]], [[0.0]], [[1.0]], [[0.0]]], dtype=tf.float64),
        d_observation_covariance=tf.constant([[[0.0]], [[0.0]], [[0.0]], [[1.0]]], dtype=tf.float64),
        transition_state_jacobian_fn=lambda points: tf.ones([tf.shape(points)[0], 1, 1], dtype=tf.float64) * params["beta"],
        d_transition_fn=lambda points: tf.stack(
            [
                tf.zeros([tf.shape(points)[0], 1], dtype=tf.float64),
                tf.convert_to_tensor(points, dtype=tf.float64),
                tf.zeros([tf.shape(points)[0], 1], dtype=tf.float64),
                tf.zeros([tf.shape(points)[0], 1], dtype=tf.float64),
            ],
            axis=0,
        ),
        observation_state_jacobian_fn=lambda points: 2.0 * tf.convert_to_tensor(points, dtype=tf.float64)[:, tf.newaxis, :],
        d_observation_fn=lambda points: tf.zeros([4, tf.shape(points)[0], 1], dtype=tf.float64),
        name="multistep_multi_parameter_derivatives",
    )

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

    def value_at(mu0: float, beta: float, q: float, r: float) -> float:
        shifted = TFFixedSGQFNonlinearModel(
            initial_mean=tf.constant([mu0], dtype=tf.float64),
            initial_covariance=tf.constant([[0.9]], dtype=tf.float64),
            process_covariance=tf.constant([[q]], dtype=tf.float64),
            observation_covariance=tf.constant([[r]], dtype=tf.float64),
            transition_fn=lambda points: tf.convert_to_tensor(beta, dtype=tf.float64)
            * tf.convert_to_tensor(points, dtype=tf.float64),
            observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
            name="multistep_multi_parameter_fd_fixture",
        )
        result = tf_fixed_sgqf_filter(observations, shifted, cloud=cloud, branch_config=branch, return_filtered=True)
        if result.failure is not None:
            raise AssertionError(f"finite-difference evaluation left the declared branch at {result.failure.stage}")
        return float(result.log_likelihood.numpy())

    step = 1e-6
    finite_difference = []
    for name in ("mu0", "beta", "q", "r"):
        plus = dict(params)
        minus = dict(params)
        plus[name] += step
        minus[name] -= step
        finite_difference.append((value_at(**plus) - value_at(**minus)) / (2.0 * step))

    np.testing.assert_allclose(score_result.score.numpy(), np.array(finite_difference), atol=8e-5, rtol=2e-2)
