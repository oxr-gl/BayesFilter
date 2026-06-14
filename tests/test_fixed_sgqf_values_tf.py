import numpy as np
import tensorflow as tf

from bayesfilter import affine_structural_to_linear_gaussian_tf
from bayesfilter.linear.kalman_tf import tf_linear_gaussian_log_likelihood
from bayesfilter.nonlinear.fixed_sgqf_tf import (
    TFFixedSGQFAffineModel,
    TFFixedSGQFBranchConfig,
    TFFixedSGQFNonlinearModel,
    tf_fixed_sgqf_cloud,
    tf_fixed_sgqf_filter,
    tf_fixed_sgqf_p47_one_step_oracle,
)
from bayesfilter.structural import StatePartition, StructuralFilterConfig
from bayesfilter.structural_tf import TFStructuralStateSpace, make_affine_structural_tf
from bayesfilter.testing import dense_projection_first_step, make_nonlinear_accumulation_model_tf


OBSERVATION_TOL = 1e-10


def _affine_fixed_sgqf_model() -> tuple[TFFixedSGQFAffineModel, TFStructuralStateSpace, tf.Tensor]:
    partition = StatePartition(
        state_names=("x",),
        stochastic_indices=(0,),
        deterministic_indices=(),
        innovation_dim=1,
    )
    transition_matrix = tf.constant([[0.8]], dtype=tf.float64)
    process_covariance = tf.constant([[0.25]], dtype=tf.float64)
    observation_matrix = tf.constant([[1.3]], dtype=tf.float64)
    observation_covariance = tf.constant([[0.4]], dtype=tf.float64)
    initial_mean = tf.constant([0.2], dtype=tf.float64)
    initial_covariance = tf.constant([[1.1]], dtype=tf.float64)
    observations = tf.constant([[0.1], [-0.2], [0.3]], dtype=tf.float64)

    affine_model = TFFixedSGQFAffineModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_matrix=transition_matrix,
        process_covariance=process_covariance,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
    )
    structural_model = make_affine_structural_tf(
        partition=partition,
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_offset=tf.zeros([1], dtype=tf.float64),
        transition_matrix=transition_matrix,
        innovation_matrix=tf.ones([1, 1], dtype=tf.float64),
        innovation_covariance=process_covariance,
        observation_offset=tf.zeros([1], dtype=tf.float64),
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_affine_oracle",
        ),
    )
    return affine_model, structural_model, observations


def _fixed_sgqf_scalar_quadratic_model() -> tuple[TFFixedSGQFNonlinearModel, TFStructuralStateSpace, tf.Tensor]:
    rho = tf.constant(0.9, dtype=tf.float64)
    process_sigma = tf.constant(0.5, dtype=tf.float64)
    observation_sigma = tf.constant(0.3, dtype=tf.float64)
    initial_mean = tf.constant([0.4], dtype=tf.float64)
    initial_covariance = tf.constant([[0.9]], dtype=tf.float64)
    process_covariance = tf.reshape(tf.square(process_sigma), [1, 1])
    observation_covariance = tf.reshape(tf.square(observation_sigma), [1, 1])
    observations = tf.constant([[0.7]], dtype=tf.float64)

    fixed_model = TFFixedSGQFNonlinearModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        process_covariance=process_covariance,
        observation_covariance=observation_covariance,
        transition_fn=lambda points: rho * tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.square(tf.convert_to_tensor(points, dtype=tf.float64)),
        name="fixed_sgqf_scalar_quadratic_model",
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
        points = tf.convert_to_tensor(state_points, dtype=tf.float64)
        return tf.square(points)

    def residual_fn(previous_state: tf.Tensor, innovation: tf.Tensor, next_state: tf.Tensor) -> tf.Tensor:
        del previous_state, innovation
        point_count = tf.shape(tf.convert_to_tensor(next_state, dtype=tf.float64))[0]
        return tf.zeros([point_count, 0], dtype=tf.float64)

    structural_model = TFStructuralStateSpace(
        partition=partition,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_scalar_quadratic_oracle",
        ),
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        innovation_covariance=tf.ones([1, 1], dtype=tf.float64),
        observation_covariance=observation_covariance,
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        deterministic_residual_fn=residual_fn,
        name="fixed_sgqf_scalar_quadratic_structural_model",
    )
    return fixed_model, structural_model, observations


def test_fixed_sgqf_scalar_quadratic_first_step_matches_dense_projection_reference() -> None:
    fixed_model, structural_model, observations = _fixed_sgqf_scalar_quadratic_model()
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations[:1], fixed_model, cloud=cloud, return_filtered=True)
    step = result.step_results[0]
    dense = dense_projection_first_step(structural_model, observations[0], nodes_per_dim=21)

    assert result.failure is None
    np.testing.assert_allclose(step.observation_mean.numpy(), dense.observation_mean.numpy(), atol=2e-3, rtol=2e-3)
    np.testing.assert_allclose(step.innovation_covariance.numpy(), dense.observation_covariance.numpy(), atol=5e-3, rtol=5e-3)
    np.testing.assert_allclose(step.filtered_mean.numpy(), dense.filtered_mean.numpy(), atol=5e-3, rtol=5e-3)



def test_fixed_sgqf_scalar_quadratic_multistep_matches_recursive_dense_reference() -> None:
    fixed_model, structural_model, _observations = _fixed_sgqf_scalar_quadratic_model()
    observations = tf.constant([[0.7], [0.1], [-0.2]], dtype=tf.float64)
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations, fixed_model, cloud=cloud, return_filtered=True)

    assert result.failure is None

    mean = structural_model.initial_mean
    covariance = structural_model.initial_covariance
    dense_log_likelihood = 0.0
    dense_means = []
    dense_covariances = []
    for time_index in range(int(observations.shape[0])):
        dense = dense_projection_first_step(
            TFStructuralStateSpace(
                partition=structural_model.partition,
                config=structural_model.config,
                initial_mean=mean,
                initial_covariance=covariance,
                innovation_covariance=structural_model.innovation_covariance,
                observation_covariance=structural_model.observation_covariance,
                transition_fn=structural_model.transition_fn,
                observation_fn=structural_model.observation_fn,
                deterministic_residual_fn=structural_model.deterministic_residual_fn,
                name=f"{structural_model.name}_dense_step_{time_index}",
            ),
            observations[time_index],
            nodes_per_dim=21,
        )
        dense_log_likelihood += float(dense.log_likelihood.numpy())
        dense_means.append(dense.filtered_mean.numpy())
        dense_covariances.append(dense.filtered_covariance.numpy())
        mean = dense.filtered_mean
        covariance = dense.filtered_covariance

    np.testing.assert_allclose(result.log_likelihood.numpy(), dense_log_likelihood, atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), np.stack(dense_means, axis=0), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), np.stack(dense_covariances, axis=0), atol=1e-10)



def test_fixed_sgqf_affine_model_matches_exact_kalman_reference() -> None:
    fixed_model, structural_model, observations = _affine_fixed_sgqf_model()
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations, fixed_model, cloud=cloud, return_filtered=True)
    linear = affine_structural_to_linear_gaussian_tf(structural_model)
    exact = tf_linear_gaussian_log_likelihood(
        observations,
        linear,
        backend="tf_cholesky",
        jitter=tf.constant(0.0, dtype=tf.float64),
        return_filtered=True,
    )

    assert result.failure is None
    np.testing.assert_allclose(result.log_likelihood.numpy(), exact.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), exact.filtered_means.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), exact.filtered_covariances.numpy(), atol=1e-10)


def test_fixed_sgqf_affine_model_matches_exact_kalman_reference() -> None:
    fixed_model, structural_model, observations = _affine_fixed_sgqf_model()
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations, fixed_model, cloud=cloud, return_filtered=True)
    linear = affine_structural_to_linear_gaussian_tf(structural_model)
    exact = tf_linear_gaussian_log_likelihood(
        observations,
        linear,
        backend="tf_cholesky",
        jitter=tf.constant(0.0, dtype=tf.float64),
        return_filtered=True,
    )

    assert result.failure is None
    np.testing.assert_allclose(result.log_likelihood.numpy(), exact.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), exact.filtered_means.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), exact.filtered_covariances.numpy(), atol=1e-10)



def test_fixed_sgqf_affine_model_matches_exact_kalman_reference_in_2d() -> None:
    partition = StatePartition(
        state_names=("x1", "x2"),
        stochastic_indices=(0, 1),
        deterministic_indices=(),
        innovation_dim=2,
    )
    transition_matrix = tf.constant([[0.8, 0.15], [0.05, 0.7]], dtype=tf.float64)
    process_covariance = tf.constant([[0.2, 0.03], [0.03, 0.15]], dtype=tf.float64)
    observation_matrix = tf.constant([[1.1, -0.2]], dtype=tf.float64)
    observation_covariance = tf.constant([[0.25]], dtype=tf.float64)
    initial_mean = tf.constant([0.1, -0.2], dtype=tf.float64)
    initial_covariance = tf.constant([[1.0, 0.1], [0.1, 0.9]], dtype=tf.float64)
    observations = tf.constant([[0.1], [0.0], [-0.15]], dtype=tf.float64)

    affine_model = TFFixedSGQFAffineModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_matrix=transition_matrix,
        process_covariance=process_covariance,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
    )
    structural_model = make_affine_structural_tf(
        partition=partition,
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_offset=tf.zeros([2], dtype=tf.float64),
        transition_matrix=transition_matrix,
        innovation_matrix=tf.eye(2, dtype=tf.float64),
        innovation_covariance=process_covariance,
        observation_offset=tf.zeros([1], dtype=tf.float64),
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_affine_2d_oracle",
        ),
    )

    cloud = tf_fixed_sgqf_cloud(dim=2, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations, affine_model, cloud=cloud, return_filtered=True)
    linear = affine_structural_to_linear_gaussian_tf(structural_model)
    exact = tf_linear_gaussian_log_likelihood(
        observations,
        linear,
        backend="tf_cholesky",
        jitter=tf.constant(0.0, dtype=tf.float64),
        return_filtered=True,
    )

    assert result.failure is None
    np.testing.assert_allclose(result.log_likelihood.numpy(), exact.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), exact.filtered_means.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), exact.filtered_covariances.numpy(), atol=1e-10)



def test_fixed_sgqf_affine_model_matches_exact_kalman_reference_in_3d_level2() -> None:
    partition = StatePartition(
        state_names=("x1", "x2", "x3"),
        stochastic_indices=(0, 1, 2),
        deterministic_indices=(),
        innovation_dim=3,
    )
    transition_matrix = tf.constant(
        [[0.8, 0.1, 0.0], [0.05, 0.7, 0.1], [0.0, 0.1, 0.65]],
        dtype=tf.float64,
    )
    process_covariance = tf.constant(
        [[0.2, 0.02, 0.0], [0.02, 0.15, 0.01], [0.0, 0.01, 0.12]],
        dtype=tf.float64,
    )
    observation_matrix = tf.constant([[1.0, -0.1, 0.2], [0.0, 0.4, 1.1]], dtype=tf.float64)
    observation_covariance = tf.constant([[0.2, 0.03], [0.03, 0.25]], dtype=tf.float64)
    initial_mean = tf.constant([0.1, -0.2, 0.05], dtype=tf.float64)
    initial_covariance = tf.constant(
        [[1.0, 0.1, 0.0], [0.1, 0.9, 0.05], [0.0, 0.05, 0.8]],
        dtype=tf.float64,
    )
    observations = tf.constant([[0.1, 0.0], [-0.05, 0.1], [0.02, -0.1]], dtype=tf.float64)

    affine_model = TFFixedSGQFAffineModel(
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_matrix=transition_matrix,
        process_covariance=process_covariance,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
    )
    structural_model = make_affine_structural_tf(
        partition=partition,
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_offset=tf.zeros([3], dtype=tf.float64),
        transition_matrix=transition_matrix,
        innovation_matrix=tf.eye(3, dtype=tf.float64),
        innovation_covariance=process_covariance,
        observation_offset=tf.zeros([2], dtype=tf.float64),
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
        config=StructuralFilterConfig(
            integration_space="innovation",
            deterministic_completion="none",
            approximation_label="fixed_sgqf_affine_3d_level2_oracle",
        ),
    )

    cloud = tf_fixed_sgqf_cloud(dim=3, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations, affine_model, cloud=cloud, return_filtered=True)
    linear = affine_structural_to_linear_gaussian_tf(structural_model)
    exact = tf_linear_gaussian_log_likelihood(
        observations,
        linear,
        backend="tf_cholesky",
        jitter=tf.constant(0.0, dtype=tf.float64),
        return_filtered=True,
    )

    assert result.failure is None
    np.testing.assert_allclose(result.log_likelihood.numpy(), exact.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), exact.filtered_means.numpy(), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), exact.filtered_covariances.numpy(), atol=1e-10)



def test_fixed_sgqf_p47_one_step_numeric_oracle_matches_note() -> None:
    oracle, cloud = tf_fixed_sgqf_p47_one_step_oracle()
    branch = TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10)
    result = tf_fixed_sgqf_filter(oracle.observation, oracle.model(), cloud=cloud, branch_config=branch, return_filtered=True)
    step = result.step_results[0]

    assert result.failure is None
    assert step.accepted
    np.testing.assert_allclose(step.predicted_mean.numpy(), np.array([0.5]), atol=1e-12)
    np.testing.assert_allclose(step.predicted_covariance.numpy(), np.array([[1.25]]), atol=1e-12)
    np.testing.assert_allclose(step.predicted_factor.numpy(), np.array([[np.sqrt(1.25)]]), atol=1e-12)
    np.testing.assert_allclose(step.observation_mean.numpy(), np.array([1.5]), atol=1e-12)
    np.testing.assert_allclose(step.innovation_covariance.numpy(), np.array([[43.0 / 8.0]]), atol=1e-12)
    np.testing.assert_allclose(step.cross_covariance.numpy(), np.array([[1.25]]), atol=1e-12)
    np.testing.assert_allclose(step.innovation.numpy(), np.array([0.5]), atol=1e-12)
    np.testing.assert_allclose(step.gain.numpy(), np.array([[10.0 / 43.0]]), atol=1e-12)
    np.testing.assert_allclose(step.filtered_mean.numpy(), np.array([53.0 / 86.0]), atol=1e-12)
    np.testing.assert_allclose(step.filtered_covariance.numpy(), np.array([[165.0 / 172.0]]), atol=1e-12)
    np.testing.assert_allclose(result.log_likelihood.numpy(), np.array(-1.7830736342), atol=1e-10)


def test_fixed_sgqf_scalar_quadratic_first_step_matches_dense_projection_reference() -> None:
    fixed_model, structural_model, observations = _fixed_sgqf_scalar_quadratic_model()
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    result = tf_fixed_sgqf_filter(observations[:1], fixed_model, cloud=cloud, return_filtered=True)
    step = result.step_results[0]
    dense = dense_projection_first_step(structural_model, observations[0], nodes_per_dim=21)

    assert result.failure is None
    np.testing.assert_allclose(step.observation_mean.numpy(), dense.observation_mean.numpy(), atol=2e-3, rtol=2e-3)
    np.testing.assert_allclose(step.innovation_covariance.numpy(), dense.observation_covariance.numpy(), atol=5e-3, rtol=5e-3)
    np.testing.assert_allclose(step.filtered_mean.numpy(), dense.filtered_mean.numpy(), atol=5e-3, rtol=5e-3)


def test_fixed_sgqf_filter_reports_predictive_branch_failure_without_repair() -> None:
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    model = TFFixedSGQFNonlinearModel(
        initial_mean=tf.constant([0.0], dtype=tf.float64),
        initial_covariance=tf.constant([[1.0]], dtype=tf.float64),
        process_covariance=tf.constant([[-2.0]], dtype=tf.float64),
        observation_covariance=tf.constant([[1.0]], dtype=tf.float64),
        transition_fn=lambda points: tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.convert_to_tensor(points, dtype=tf.float64),
        name="predictive_failure_fixture",
    )
    result = tf_fixed_sgqf_filter(
        tf.constant([[0.0]], dtype=tf.float64),
        model,
        cloud=cloud,
        branch_config=TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10),
        return_filtered=True,
    )

    assert result.failure is not None
    assert result.failure.stage == "predictive_covariance"
    assert result.step_results[0].accepted is False


def test_fixed_sgqf_filter_reports_innovation_branch_failure_without_repair() -> None:
    cloud = tf_fixed_sgqf_cloud(dim=1, sparse_level=2)
    model = TFFixedSGQFNonlinearModel(
        initial_mean=tf.constant([0.0], dtype=tf.float64),
        initial_covariance=tf.constant([[1.0]], dtype=tf.float64),
        process_covariance=tf.constant([[0.0]], dtype=tf.float64),
        observation_covariance=tf.constant([[-1.0]], dtype=tf.float64),
        transition_fn=lambda points: tf.convert_to_tensor(points, dtype=tf.float64),
        observation_fn=lambda points: tf.zeros([tf.shape(tf.convert_to_tensor(points, dtype=tf.float64))[0], 1], dtype=tf.float64),
        name="innovation_failure_fixture",
    )
    result = tf_fixed_sgqf_filter(
        tf.constant([[0.0]], dtype=tf.float64),
        model,
        cloud=cloud,
        branch_config=TFFixedSGQFBranchConfig(predictive_epsilon=1e-10, innovation_epsilon=1e-10),
        return_filtered=True,
    )

    assert result.failure is not None
    assert result.failure.stage == "innovation_covariance"
    assert result.step_results[0].accepted is False



def test_fixed_sgqf_scalar_quadratic_level1_is_less_accurate_than_level2_dense_reference() -> None:
    fixed_model, structural_model, observations = _fixed_sgqf_scalar_quadratic_model()
    dense = dense_projection_first_step(structural_model, observations[0], nodes_per_dim=21)

    level1 = tf_fixed_sgqf_filter(observations[:1], fixed_model, cloud=tf_fixed_sgqf_cloud(dim=1, sparse_level=1), return_filtered=True)
    level2 = tf_fixed_sgqf_filter(observations[:1], fixed_model, cloud=tf_fixed_sgqf_cloud(dim=1, sparse_level=2), return_filtered=True)

    assert level1.failure is None
    assert level2.failure is None

    level1_error = abs(float(level1.step_results[0].observation_mean.numpy()[0] - dense.observation_mean.numpy()[0]))
    level2_error = abs(float(level2.step_results[0].observation_mean.numpy()[0] - dense.observation_mean.numpy()[0]))

    assert level2_error < 1e-12
    assert level1_error > 0.9



def test_fixed_sgqf_scalar_quadratic_level3_reports_carried_covariance_block() -> None:
    fixed_model, _structural_model, observations = _fixed_sgqf_scalar_quadratic_model()
    result = tf_fixed_sgqf_filter(observations[:1], fixed_model, cloud=tf_fixed_sgqf_cloud(dim=1, sparse_level=3), return_filtered=True)

    assert result.failure is not None
    assert result.failure.stage == "carried_covariance"
    assert result.failure.time_index == 0



def test_fixed_sgqf_scalar_quadratic_matches_recursive_dense_reference_through_three_steps() -> None:
    fixed_model, structural_model, _observations = _fixed_sgqf_scalar_quadratic_model()
    observations = tf.constant([[0.7], [0.1], [-0.2]], dtype=tf.float64)
    result = tf_fixed_sgqf_filter(observations, fixed_model, cloud=tf_fixed_sgqf_cloud(dim=1, sparse_level=2), return_filtered=True)

    assert result.failure is None

    mean = structural_model.initial_mean
    covariance = structural_model.initial_covariance
    dense_log_likelihood = 0.0
    dense_means = []
    dense_covariances = []
    for time_index in range(int(observations.shape[0])):
        dense = dense_projection_first_step(
            TFStructuralStateSpace(
                partition=structural_model.partition,
                config=structural_model.config,
                initial_mean=mean,
                initial_covariance=covariance,
                innovation_covariance=structural_model.innovation_covariance,
                observation_covariance=structural_model.observation_covariance,
                transition_fn=structural_model.transition_fn,
                observation_fn=structural_model.observation_fn,
                deterministic_residual_fn=structural_model.deterministic_residual_fn,
                name=f"{structural_model.name}_dense_recursive_step_{time_index}",
            ),
            observations[time_index],
            nodes_per_dim=21,
        )
        dense_log_likelihood += float(dense.log_likelihood.numpy())
        dense_means.append(dense.filtered_mean.numpy())
        dense_covariances.append(dense.filtered_covariance.numpy())
        mean = dense.filtered_mean
        covariance = dense.filtered_covariance

    np.testing.assert_allclose(result.log_likelihood.numpy(), dense_log_likelihood, atol=1e-10)
    np.testing.assert_allclose(result.filtered_means.numpy(), np.stack(dense_means, axis=0), atol=1e-10)
    np.testing.assert_allclose(result.filtered_covariances.numpy(), np.stack(dense_covariances, axis=0), atol=1e-10)
