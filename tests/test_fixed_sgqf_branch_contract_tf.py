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
        name="branch_contract_score_fixture",
    )
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    return oracle.observation, model, derivatives, cloud, branch


def test_fixed_sgqf_value_and_score_share_branch_identity_on_success() -> None:
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
    assert score_result.branch_identity == value_result.branch_identity
    assert score_result.diagnostics["same_branch_signature"] == (
        value_result.branch_identity.hash.value,
        "accepted",
        -1,
    )


def test_fixed_sgqf_value_and_score_record_same_failure_stage_when_branch_breaks() -> None:
    observations, model, derivatives, cloud, branch = _score_fixture()
    blocked_model = TFFixedSGQFNonlinearModel(
        initial_mean=model.initial_mean,
        initial_covariance=model.initial_covariance,
        process_covariance=tf.constant([[-2.0]], dtype=tf.float64),
        observation_covariance=model.observation_covariance,
        transition_fn=model.transition_fn,
        observation_fn=model.observation_fn,
        name="shared_failure_fixture",
    )
    value_result = tf_fixed_sgqf_filter(observations, blocked_model, cloud=cloud, branch_config=branch, return_filtered=True)
    score_result = tf_fixed_sgqf_score(
        observations,
        blocked_model,
        derivatives,
        cloud=cloud,
        branch_config=branch,
    )

    assert value_result.failure is not None
    assert score_result.failure is not None
    assert value_result.failure.stage == "predictive_covariance"
    assert score_result.failure.stage == "predictive_covariance"
    assert score_result.diagnostics["same_branch_signature"][1] == "predictive_covariance"
