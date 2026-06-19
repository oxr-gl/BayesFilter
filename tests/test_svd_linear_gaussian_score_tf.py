import numpy as np
import pytest
import tensorflow as tf

from bayesfilter import (
    tf_svd_linear_gaussian_score_first_order as top_level_svd_first_order,
)
from bayesfilter import (
    tf_svd_linear_gaussian_score_first_order_graph_status as top_level_svd_first_order_graph_status,
)
from bayesfilter import tf_svd_linear_gaussian_score_hessian as top_level_svd_score
from bayesfilter import (
    tf_svd_linear_gaussian_score_hessian_graph_status as top_level_svd_graph_status,
)
from bayesfilter.linear import (
    SVD_LINEAR_SCORE_STATUS_BLOCKED_ACTIVE_FLOOR,
    SVD_LINEAR_SCORE_STATUS_INVALID_EIGENSOLVER_INPUT,
    SVD_LINEAR_SCORE_STATUS_VALID_PRE_REGULARIZED,
    first_to_full_linear_gaussian_derivatives,
    tf_svd_linear_gaussian_score_first_order,
    tf_svd_linear_gaussian_score_first_order_graph_status,
    tf_svd_linear_gaussian_score_hessian,
    tf_svd_linear_gaussian_score_hessian_graph_status,
)
from bayesfilter.linear.kalman_qr_derivatives_tf import tf_qr_linear_gaussian_score_hessian
from bayesfilter.linear.kalman_svd_derivatives_tf import (
    BlockedSVDSolveLogdetDerivativeError,
)
from bayesfilter.linear.kalman_svd_tf import tf_svd_linear_gaussian_log_likelihood
from bayesfilter.linear.types import (
    LinearGaussianStateSpace,
    LinearGaussianStateSpaceDerivatives,
)
from bayesfilter.linear.types_tf import (
    TFLinearGaussianStateSpace,
    TFLinearGaussianStateSpaceDerivatives,
    TFLinearGaussianStateSpaceFirstDerivatives,
)
from bayesfilter.linear.kalman_derivatives_numpy import solve_kalman_score_hessian
from bayesfilter.results_tf import TFFilterDerivativeResult


JITTER = 0.0


def _observations() -> tf.Tensor:
    return tf.constant([[0.0, 0.3], [0.2, -0.1], [-0.15, 0.25]], dtype=tf.float64)


def _model(observation_covariance: tf.Tensor) -> TFLinearGaussianStateSpace:
    return TFLinearGaussianStateSpace(
        initial_mean=tf.constant([0.2], dtype=tf.float64),
        initial_covariance=tf.constant([[0.4]], dtype=tf.float64),
        transition_offset=tf.constant([0.05], dtype=tf.float64),
        transition_matrix=tf.constant([[0.6]], dtype=tf.float64),
        transition_covariance=tf.constant([[0.1]], dtype=tf.float64),
        observation_offset=tf.constant([0.1, -0.2], dtype=tf.float64),
        observation_matrix=tf.zeros([2, 1], dtype=tf.float64),
        observation_covariance=observation_covariance,
    )


def _derivatives() -> TFLinearGaussianStateSpaceDerivatives:
    p, n, m = 3, 1, 2
    zeros_pn = tf.zeros([p, n], dtype=tf.float64)
    zeros_pnn = tf.zeros([p, n, n], dtype=tf.float64)
    zeros_pm = tf.zeros([p, m], dtype=tf.float64)
    zeros_pmn = tf.zeros([p, m, n], dtype=tf.float64)
    zeros_pmm = tf.zeros([p, m, m], dtype=tf.float64)
    zeros_ppn = tf.zeros([p, p, n], dtype=tf.float64)
    zeros_ppnn = tf.zeros([p, p, n, n], dtype=tf.float64)
    zeros_ppm = tf.zeros([p, p, m], dtype=tf.float64)
    zeros_ppmn = tf.zeros([p, p, m, n], dtype=tf.float64)
    zeros_ppmm = tf.zeros([p, p, m, m], dtype=tf.float64)

    d_observation_offset = tf.constant(
        [[1.0, 0.0], [0.0, 1.0], [0.0, 0.0]],
        dtype=tf.float64,
    )
    d_observation_covariance = zeros_pmm.numpy()
    d_observation_covariance[2] = np.eye(2)

    return TFLinearGaussianStateSpaceDerivatives(
        d_initial_mean=zeros_pn,
        d_initial_covariance=zeros_pnn,
        d_transition_offset=zeros_pn,
        d_transition_matrix=zeros_pnn,
        d_transition_covariance=zeros_pnn,
        d_observation_offset=d_observation_offset,
        d_observation_matrix=zeros_pmn,
        d_observation_covariance=tf.constant(d_observation_covariance, dtype=tf.float64),
        d2_initial_mean=zeros_ppn,
        d2_initial_covariance=zeros_ppnn,
        d2_transition_offset=zeros_ppn,
        d2_transition_matrix=zeros_ppnn,
        d2_transition_covariance=zeros_ppnn,
        d2_observation_offset=zeros_ppm,
        d2_observation_matrix=zeros_ppmn,
        d2_observation_covariance=zeros_ppmm,
    )


def _first_derivatives() -> TFLinearGaussianStateSpaceFirstDerivatives:
    derivatives = _derivatives()
    return TFLinearGaussianStateSpaceFirstDerivatives(
        d_initial_mean=derivatives.d_initial_mean,
        d_initial_covariance=derivatives.d_initial_covariance,
        d_transition_offset=derivatives.d_transition_offset,
        d_transition_matrix=derivatives.d_transition_matrix,
        d_transition_covariance=derivatives.d_transition_covariance,
        d_observation_offset=derivatives.d_observation_offset,
        d_observation_matrix=derivatives.d_observation_matrix,
        d_observation_covariance=derivatives.d_observation_covariance,
    )


def _numpy_model(model: TFLinearGaussianStateSpace) -> LinearGaussianStateSpace:
    return LinearGaussianStateSpace(
        initial_mean=model.initial_mean.numpy(),
        initial_covariance=model.initial_covariance.numpy(),
        transition_offset=model.transition_offset.numpy(),
        transition_matrix=model.transition_matrix.numpy(),
        transition_covariance=model.transition_covariance.numpy(),
        observation_offset=model.observation_offset.numpy(),
        observation_matrix=model.observation_matrix.numpy(),
        observation_covariance=model.observation_covariance.numpy(),
    )


def _numpy_derivatives(
    derivatives: TFLinearGaussianStateSpaceDerivatives,
) -> LinearGaussianStateSpaceDerivatives:
    return LinearGaussianStateSpaceDerivatives(
        d_initial_mean=derivatives.d_initial_mean.numpy(),
        d_initial_covariance=derivatives.d_initial_covariance.numpy(),
        d_transition_offset=derivatives.d_transition_offset.numpy(),
        d_transition_matrix=derivatives.d_transition_matrix.numpy(),
        d_transition_covariance=derivatives.d_transition_covariance.numpy(),
        d_observation_offset=derivatives.d_observation_offset.numpy(),
        d_observation_matrix=derivatives.d_observation_matrix.numpy(),
        d_observation_covariance=derivatives.d_observation_covariance.numpy(),
        d2_initial_mean=derivatives.d2_initial_mean.numpy(),
        d2_initial_covariance=derivatives.d2_initial_covariance.numpy(),
        d2_transition_offset=derivatives.d2_transition_offset.numpy(),
        d2_transition_matrix=derivatives.d2_transition_matrix.numpy(),
        d2_transition_covariance=derivatives.d2_transition_covariance.numpy(),
        d2_observation_offset=derivatives.d2_observation_offset.numpy(),
        d2_observation_matrix=derivatives.d2_observation_matrix.numpy(),
        d2_observation_covariance=derivatives.d2_observation_covariance.numpy(),
    )


def _numpy_reference(model, derivatives):
    return solve_kalman_score_hessian(
        _observations().numpy(),
        _numpy_model(model),
        _numpy_derivatives(derivatives),
        jitter=JITTER,
    )


def test_svd_score_allows_repeated_positive_innovation_eigenvalues() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    result = tf_svd_linear_gaussian_score_hessian(
        _observations(),
        model,
        derivatives,
        jitter=JITTER,
        singular_floor=1e-12,
    )
    reference = _numpy_reference(model, derivatives)

    assert isinstance(result, TFFilterDerivativeResult)
    assert result.hessian is None
    np.testing.assert_allclose(result.log_likelihood.numpy(), reference.log_likelihood, atol=1e-10)
    np.testing.assert_allclose(result.score.numpy(), reference.score, rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(result.diagnostics.extra["min_eigen_gap"].numpy(), 0.0, atol=1e-14)
    assert result.diagnostics.extra["min_eigen_gap_role"] == "telemetry_only"


def test_svd_score_matches_numpy_with_nearly_repeated_positive_eigenvalues() -> None:
    model = _model(tf.constant([[0.7, 0.0], [0.0, 0.70000001]], dtype=tf.float64))
    derivatives = _derivatives()

    result = tf_svd_linear_gaussian_score_hessian(_observations(), model, derivatives)
    reference = _numpy_reference(model, derivatives)

    np.testing.assert_allclose(result.log_likelihood.numpy(), reference.log_likelihood, atol=1e-10)
    np.testing.assert_allclose(result.score.numpy(), reference.score, rtol=1e-8, atol=1e-8)
    assert result.diagnostics.extra["min_eigen_gap"].numpy() > 0.0


def test_svd_score_blocks_active_floor_without_regularized_law_claim() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    with pytest.raises(BlockedSVDSolveLogdetDerivativeError, match="blocked_active_floor") as exc_info:
        tf_svd_linear_gaussian_score_hessian(
            _observations(),
            model,
            derivatives,
            singular_floor=1.0,
        )
    blocked_result = exc_info.value.result
    assert blocked_result.diagnostics.regularization.derivative_target == "blocked"
    assert int(blocked_result.diagnostics.regularization.floor_count.numpy()) > 0
    assert blocked_result.hessian is None
    assert np.all(np.isnan(blocked_result.score.numpy()))


def test_svd_score_rejects_graph_wrapped_public_wrapper_without_derivative_claim() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    @tf.function
    def graph_wrapped_call():
        return tf_svd_linear_gaussian_score_hessian(_observations(), model, derivatives)

    with pytest.raises(Exception, match="blocked_non_eager") as exc_info:
        graph_wrapped_call()
    assert "BlockedSVDSolveLogdetDerivativeError" in str(exc_info.value)


def test_svd_graph_status_eager_valid_state_matches_public_wrapper() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    reference = tf_svd_linear_gaussian_score_hessian(_observations(), model, derivatives)
    result = tf_svd_linear_gaussian_score_hessian_graph_status(
        _observations(),
        model,
        derivatives,
    )

    assert isinstance(result, TFFilterDerivativeResult)
    assert result.metadata.filter_name == "tf_svd_solve_logdet_score_kalman_graph_status"
    assert result.diagnostics.regularization.derivative_target == "blocked"
    assert result.diagnostics.extra["status_label"].startswith("tensor_status_code")
    assert int(result.diagnostics.regularization.floor_count.numpy()) == 0
    assert int(result.diagnostics.extra["status_code"].numpy()) == (
        SVD_LINEAR_SCORE_STATUS_VALID_PRE_REGULARIZED
    )
    assert bool(result.diagnostics.extra["valid_pre_regularized_score"].numpy())
    assert not bool(result.diagnostics.extra["active_floor_blocked"].numpy())
    np.testing.assert_allclose(
        result.log_likelihood.numpy(),
        reference.log_likelihood.numpy(),
        atol=1e-10,
    )
    np.testing.assert_allclose(
        result.score.numpy(),
        reference.score.numpy(),
        rtol=1e-8,
        atol=1e-8,
    )


def test_svd_graph_status_tf_function_valid_state_matches_public_wrapper() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()
    reference = tf_svd_linear_gaussian_score_hessian(_observations(), model, derivatives)

    @tf.function(reduce_retracing=True)
    def graph_call(shift: tf.Tensor):
        result = tf_svd_linear_gaussian_score_hessian_graph_status(
            _observations() + shift,
            model,
            derivatives,
        )
        return (
            result.log_likelihood,
            result.score,
            result.diagnostics.extra["status_code"],
            result.diagnostics.extra["valid_pre_regularized_score"],
            result.diagnostics.extra["active_floor_blocked"],
            result.diagnostics.regularization.floor_count,
        )

    log_likelihood, score, status_code, valid, blocked, floor_count_value = graph_call(
        tf.zeros_like(_observations())
    )

    assert int(status_code.numpy()) == SVD_LINEAR_SCORE_STATUS_VALID_PRE_REGULARIZED
    assert bool(valid.numpy())
    assert not bool(blocked.numpy())
    assert int(floor_count_value.numpy()) == 0
    np.testing.assert_allclose(log_likelihood.numpy(), reference.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(score.numpy(), reference.score.numpy(), rtol=1e-8, atol=1e-8)


def test_svd_graph_status_active_floor_returns_blocked_tensor_diagnostics() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    @tf.function(reduce_retracing=True)
    def graph_call():
        result = tf_svd_linear_gaussian_score_hessian_graph_status(
            _observations(),
            model,
            derivatives,
            singular_floor=1.0,
        )
        return (
            result.log_likelihood,
            result.score,
            result.diagnostics.extra["status_code"],
            result.diagnostics.extra["valid_pre_regularized_score"],
            result.diagnostics.extra["active_floor_blocked"],
            result.diagnostics.regularization.floor_count,
            result.diagnostics.extra["status_blocked_active_floor_code"],
        )

    (
        log_likelihood,
        score,
        status_code,
        valid,
        blocked,
        floor_count_value,
        blocked_status_code,
    ) = graph_call()

    assert int(status_code.numpy()) == SVD_LINEAR_SCORE_STATUS_BLOCKED_ACTIVE_FLOOR
    assert int(blocked_status_code.numpy()) == SVD_LINEAR_SCORE_STATUS_BLOCKED_ACTIVE_FLOOR
    assert not bool(valid.numpy())
    assert bool(blocked.numpy())
    assert int(floor_count_value.numpy()) > 0
    assert log_likelihood.shape == ()
    assert score.shape == (3,)


def test_svd_graph_status_invalid_covariance_returns_tensor_status_without_eigh_raise() -> None:
    model = _model(tf.constant([[0.7, np.nan], [np.nan, 0.7]], dtype=tf.float64))
    derivatives = _derivatives()

    @tf.function(reduce_retracing=True)
    def graph_call():
        result = tf_svd_linear_gaussian_score_hessian_graph_status(
            _observations(),
            model,
            derivatives,
        )
        return (
            result.log_likelihood,
            result.score,
            result.diagnostics.extra["status_code"],
            result.diagnostics.extra["valid_pre_regularized_score"],
            result.diagnostics.extra["invalid_eigensolver_input"],
            result.diagnostics.extra["nonfinite_covariance"],
            result.diagnostics.extra["active_floor_blocked"],
            result.diagnostics.extra["status_invalid_eigensolver_input_code"],
            result.diagnostics.regularization.floor_count,
        )

    (
        log_likelihood,
        score,
        status_code,
        valid,
        invalid_eigensolver_input,
        nonfinite_covariance,
        active_floor_blocked,
        invalid_status_code,
        floor_count_value,
    ) = graph_call()

    assert int(status_code.numpy()) == SVD_LINEAR_SCORE_STATUS_INVALID_EIGENSOLVER_INPUT
    assert int(invalid_status_code.numpy()) == SVD_LINEAR_SCORE_STATUS_INVALID_EIGENSOLVER_INPUT
    assert not bool(valid.numpy())
    assert bool(invalid_eigensolver_input.numpy())
    assert bool(nonfinite_covariance.numpy())
    assert not bool(active_floor_blocked.numpy())
    assert int(floor_count_value.numpy()) == 0
    assert log_likelihood.shape == ()
    assert score.shape == (3,)


def test_first_order_derivative_conversion_zero_fills_second_derivatives() -> None:
    first_derivatives = _first_derivatives()

    full = first_to_full_linear_gaussian_derivatives(first_derivatives)

    np.testing.assert_allclose(
        full.d_observation_offset.numpy(),
        first_derivatives.d_observation_offset.numpy(),
    )
    np.testing.assert_allclose(
        full.d_observation_covariance.numpy(),
        first_derivatives.d_observation_covariance.numpy(),
    )
    for tensor in (
        full.d2_initial_mean,
        full.d2_initial_covariance,
        full.d2_transition_offset,
        full.d2_transition_matrix,
        full.d2_transition_covariance,
        full.d2_observation_offset,
        full.d2_observation_matrix,
        full.d2_observation_covariance,
    ):
        assert not np.any(tensor.numpy())


def test_svd_first_order_score_matches_full_derivative_score() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    full_derivatives = _derivatives()
    first_derivatives = _first_derivatives()

    reference = tf_svd_linear_gaussian_score_hessian(
        _observations(),
        model,
        full_derivatives,
    )
    result = tf_svd_linear_gaussian_score_first_order(
        _observations(),
        model,
        first_derivatives,
    )
    top_level_result = top_level_svd_first_order(
        _observations(),
        model,
        first_derivatives,
    )

    assert result.hessian is None
    assert result.metadata.filter_name == "tf_svd_solve_logdet_score_first_order_kalman"
    np.testing.assert_allclose(result.log_likelihood.numpy(), reference.log_likelihood.numpy())
    np.testing.assert_allclose(result.score.numpy(), reference.score.numpy())
    np.testing.assert_allclose(top_level_result.score.numpy(), reference.score.numpy())


def test_svd_first_order_graph_status_matches_full_graph_status() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    full_derivatives = _derivatives()
    first_derivatives = _first_derivatives()

    reference = tf_svd_linear_gaussian_score_hessian_graph_status(
        _observations(),
        model,
        full_derivatives,
    )
    result = tf_svd_linear_gaussian_score_first_order_graph_status(
        _observations(),
        model,
        first_derivatives,
    )
    top_level_result = top_level_svd_first_order_graph_status(
        _observations(),
        model,
        first_derivatives,
    )

    assert result.hessian is None
    assert (
        result.metadata.filter_name
        == "tf_svd_solve_logdet_score_first_order_kalman_graph_status"
    )
    assert int(result.diagnostics.extra["status_code"].numpy()) == (
        SVD_LINEAR_SCORE_STATUS_VALID_PRE_REGULARIZED
    )
    assert bool(result.diagnostics.extra["valid_pre_regularized_score"].numpy())
    np.testing.assert_allclose(result.log_likelihood.numpy(), reference.log_likelihood.numpy())
    np.testing.assert_allclose(result.score.numpy(), reference.score.numpy())
    np.testing.assert_allclose(top_level_result.score.numpy(), reference.score.numpy())


def test_svd_first_order_graph_status_preserves_blocked_and_invalid_status_codes() -> None:
    first_derivatives = _first_derivatives()

    @tf.function(reduce_retracing=True)
    def active_floor_call():
        result = tf_svd_linear_gaussian_score_first_order_graph_status(
            _observations(),
            _model(tf.eye(2, dtype=tf.float64) * 0.7),
            first_derivatives,
            singular_floor=1.0,
        )
        return (
            result.diagnostics.extra["status_code"],
            result.diagnostics.extra["active_floor_blocked"],
            result.diagnostics.extra["valid_pre_regularized_score"],
        )

    @tf.function(reduce_retracing=True)
    def invalid_covariance_call():
        result = tf_svd_linear_gaussian_score_first_order_graph_status(
            _observations(),
            _model(tf.constant([[0.7, np.nan], [np.nan, 0.7]], dtype=tf.float64)),
            first_derivatives,
        )
        return (
            result.diagnostics.extra["status_code"],
            result.diagnostics.extra["invalid_eigensolver_input"],
            result.diagnostics.extra["valid_pre_regularized_score"],
        )

    active_status, active_blocked, active_valid = active_floor_call()
    invalid_status, invalid_input, invalid_valid = invalid_covariance_call()

    assert int(active_status.numpy()) == SVD_LINEAR_SCORE_STATUS_BLOCKED_ACTIVE_FLOOR
    assert bool(active_blocked.numpy())
    assert not bool(active_valid.numpy())
    assert int(invalid_status.numpy()) == SVD_LINEAR_SCORE_STATUS_INVALID_EIGENSOLVER_INPUT
    assert bool(invalid_input.numpy())
    assert not bool(invalid_valid.numpy())


def test_svd_score_matches_qr_derivative_and_svd_value_likelihood() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    svd_score = tf_svd_linear_gaussian_score_hessian(_observations(), model, derivatives)
    qr_score = tf_qr_linear_gaussian_score_hessian(
        _observations(),
        model,
        derivatives,
        jitter=JITTER,
    )
    svd_value = tf_svd_linear_gaussian_log_likelihood(
        _observations(),
        model,
        jitter=JITTER,
        singular_floor=1e-12,
    )

    np.testing.assert_allclose(svd_score.log_likelihood.numpy(), qr_score.log_likelihood.numpy(), atol=1e-10)
    np.testing.assert_allclose(svd_score.score.numpy(), qr_score.score.numpy(), rtol=1e-8, atol=1e-8)
    np.testing.assert_allclose(svd_score.log_likelihood.numpy(), svd_value.log_likelihood.numpy(), atol=1e-10)


def test_svd_score_metadata_diagnostics_and_exports() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    result = top_level_svd_score(_observations(), model, derivatives)
    graph_status = top_level_svd_graph_status(_observations(), model, derivatives)

    assert result.metadata.filter_name == "tf_svd_solve_logdet_score_kalman"
    assert result.metadata.differentiability_status == "analytic_score_only"
    assert result.metadata.compiled_status == "tf_function"
    assert result.hessian is None
    assert result.diagnostics.backend == "tf_svd_solve_logdet"
    assert result.diagnostics.mask_convention == "none"
    assert (
        result.diagnostics.regularization.branch_label
        == "eigensolve_logdet_score_repeated_eigenvalues_allowed"
    )
    assert result.diagnostics.regularization.derivative_target == "pre_regularized_law"
    assert int(result.diagnostics.regularization.floor_count.numpy()) == 0
    assert result.diagnostics.extra["min_innovation_eigenvalue"].numpy() > 0.0
    assert result.diagnostics.extra["innovation_condition_estimate"].numpy() >= 1.0
    assert graph_status.metadata.filter_name == "tf_svd_solve_logdet_score_kalman_graph_status"


def test_svd_score_rejects_masks_and_unknown_backend() -> None:
    model = _model(tf.eye(2, dtype=tf.float64) * 0.7)
    derivatives = _derivatives()

    with pytest.raises(ValueError, match="dense observations only"):
        tf_svd_linear_gaussian_score_hessian(
            _observations(),
            model,
            derivatives,
            observation_mask=tf.ones_like(_observations(), dtype=tf.bool),
        )
    with pytest.raises(ValueError, match="unknown TensorFlow SVD derivative backend"):
        tf_svd_linear_gaussian_score_hessian(
            _observations(),
            model,
            derivatives,
            backend="not_svd_solve_logdet",
        )
