"""TensorFlow SVD/eigh linear Gaussian Kalman score backend.

This module implements the invariant solve/logdet score from
``docs/chapters/ch09_kalman_score.tex`` for dense linear Gaussian models.  It
uses eigensolves to evaluate ``S^{-1}v``, ``S^{-1}``, traces, and log
determinants, but it does not differentiate eigenvectors or spectral factors.
Repeated positive innovation eigenvalues are therefore allowed for this
score-only interface.  Active eigenvalue flooring is blocked rather than
promoted as a derivative of a regularized law.
"""

from __future__ import annotations

import math
from typing import Literal

import tensorflow as tf

from bayesfilter.diagnostics import TFFilterDiagnostics, TFRegularizationDiagnostics
from bayesfilter.linear.svd_factor_tf import (
    eigh_logdet,
    eigh_solve,
    floor_count,
    psd_eigh,
    symmetrize,
)
from bayesfilter.linear.types_tf import (
    TFLinearGaussianStateSpace,
    TFLinearGaussianStateSpaceDerivatives,
)
from bayesfilter.results_tf import TFFilterDerivativeResult
from bayesfilter.structural import FilterRunMetadata


TFSVDLinearDerivativeBackend = Literal["tf_svd_solve_logdet"]


class BlockedSVDSolveLogdetDerivativeError(ValueError):
    """Raised when the SVD/eigh score path reaches an uncertified floor branch."""

    def __init__(self, message: str, result: TFFilterDerivativeResult) -> None:
        super().__init__(message)
        self.result = result
        self.diagnostics = result.diagnostics


def _to_tensor(value: object) -> tf.Tensor:
    return tf.convert_to_tensor(value, dtype=tf.float64)


def _matvec(matrix: tf.Tensor, vector: tf.Tensor) -> tf.Tensor:
    return tf.linalg.matvec(matrix, vector)


def _as_observation_matrix(observations: tf.Tensor) -> tf.Tensor:
    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2:
        raise ValueError("observations must be one- or two-dimensional")
    return y


def _matrix_at_time(matrix: tf.Tensor, time_index: int) -> tf.Tensor:
    if matrix.shape.rank == 3:
        return matrix[time_index]
    return matrix


def _vector_at_time(vector: tf.Tensor, time_index: int) -> tf.Tensor:
    if vector.shape.rank == 2:
        return vector[time_index]
    return vector


def _static_dim(tensor: tf.Tensor, axis: int, name: str) -> int:
    value = tensor.shape[axis]
    if value is None:
        raise ValueError(f"SVD/eigh score backend requires static {name}")
    return int(value)


def _min_eigen_gap(eigenvalues: tf.Tensor) -> tf.Tensor:
    gaps = eigenvalues[1:] - eigenvalues[:-1]
    return tf.cond(
        tf.size(gaps) > 0,
        lambda: tf.reduce_min(tf.abs(gaps)),
        lambda: tf.constant(float("inf"), dtype=tf.float64),
    )


def _validate_model_derivative_shapes(
    model: TFLinearGaussianStateSpace,
    derivatives: TFLinearGaussianStateSpaceDerivatives,
) -> tuple[int, int, int]:
    p = derivatives.parameter_dim
    n = model.state_dim
    m = model.observation_dim
    if p is None or n is None or m is None:
        raise ValueError("SVD/eigh analytic scores require static dimensions")
    if derivatives.state_dim != n:
        raise ValueError("derivative state dimension does not match model")
    if derivatives.observation_dim != m:
        raise ValueError("derivative observation dimension does not match model")
    return int(p), int(n), int(m)


def _metadata(*, filter_name: str, model: TFLinearGaussianStateSpace) -> FilterRunMetadata:
    return FilterRunMetadata(
        filter_name=filter_name,
        partition=model.partition,
        integration_space="full_state",
        deterministic_completion="none",
        approximation_label=None,
        differentiability_status="analytic_score_only",
        compiled_status="tf_function",
    )


def _diagnostics(
    *,
    backend: str,
    jitter: tf.Tensor | float,
    singular_floor: tf.Tensor | float,
    floor_count_value: tf.Tensor,
    psd_projection_residual: tf.Tensor,
    implemented_covariance: tf.Tensor,
    min_innovation_eigenvalue: tf.Tensor,
    innovation_condition_estimate: tf.Tensor,
    min_eigen_gap: tf.Tensor,
    derivative_target: str,
) -> TFFilterDiagnostics:
    return TFFilterDiagnostics(
        backend=backend,
        mask_convention="none",
        regularization=TFRegularizationDiagnostics(
            jitter=tf.convert_to_tensor(jitter, dtype=tf.float64),
            singular_floor=tf.convert_to_tensor(singular_floor, dtype=tf.float64),
            floor_count=tf.convert_to_tensor(floor_count_value, dtype=tf.int32),
            psd_projection_residual=tf.convert_to_tensor(
                psd_projection_residual,
                dtype=tf.float64,
            ),
            implemented_covariance=tf.convert_to_tensor(
                implemented_covariance,
                dtype=tf.float64,
            ),
            branch_label="eigensolve_logdet_score_repeated_eigenvalues_allowed",
            derivative_target=derivative_target,
        ),
        extra={
            "factorization": "tf.linalg.eigh",
            "min_innovation_eigenvalue": tf.convert_to_tensor(
                min_innovation_eigenvalue,
                dtype=tf.float64,
            ),
            "innovation_condition_estimate": tf.convert_to_tensor(
                innovation_condition_estimate,
                dtype=tf.float64,
            ),
            "min_eigen_gap": tf.convert_to_tensor(min_eigen_gap, dtype=tf.float64),
            "min_eigen_gap_role": "telemetry_only",
        },
    )


@tf.function
def _tf_svd_solve_logdet_kalman_score(
    observations: tf.Tensor,
    transition_offset: tf.Tensor,
    transition_matrix: tf.Tensor,
    transition_covariance: tf.Tensor,
    observation_offset: tf.Tensor,
    observation_matrix: tf.Tensor,
    observation_covariance: tf.Tensor,
    initial_state_mean: tf.Tensor,
    initial_state_covariance: tf.Tensor,
    d_initial_state_mean: tf.Tensor,
    d_initial_state_covariance: tf.Tensor,
    d_transition_offset: tf.Tensor,
    d_transition_matrix: tf.Tensor,
    d_transition_covariance: tf.Tensor,
    d_observation_offset: tf.Tensor,
    d_observation_matrix: tf.Tensor,
    d_observation_covariance: tf.Tensor,
    jitter: tf.Tensor | float = 0.0,
    singular_floor: tf.Tensor | float = 1e-12,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Return dense eigensolve/logdet log likelihood and first score.

    The score contribution is
    ``-0.5 * [tr(S^{-1} dS) + 2 dv' w - w' dS w]`` with ``S w = v``.
    No derivative of eigenvectors or eigenvalues is taken; eigensystems are used
    only to solve and evaluate log determinants of the innovation covariance.
    """

    y = _as_observation_matrix(observations)
    n_timesteps = _static_dim(y, 0, "observation length")
    transition_offset = _to_tensor(transition_offset)
    transition_matrix = _to_tensor(transition_matrix)
    transition_covariance = _to_tensor(transition_covariance)
    observation_offset = _to_tensor(observation_offset)
    observation_matrix = _to_tensor(observation_matrix)
    observation_covariance = _to_tensor(observation_covariance)
    mean = _to_tensor(initial_state_mean)
    covariance = symmetrize(_to_tensor(initial_state_covariance))
    dmean = _to_tensor(d_initial_state_mean)
    dcovariance = symmetrize(_to_tensor(d_initial_state_covariance))
    d_transition_offset = _to_tensor(d_transition_offset)
    d_transition_matrix = _to_tensor(d_transition_matrix)
    d_transition_covariance = symmetrize(_to_tensor(d_transition_covariance))
    d_observation_offset = _to_tensor(d_observation_offset)
    d_observation_matrix = _to_tensor(d_observation_matrix)
    d_observation_covariance = symmetrize(_to_tensor(d_observation_covariance))
    jitter_tensor = tf.cast(jitter, tf.float64)
    singular_floor_tensor = tf.cast(singular_floor, tf.float64)

    parameter_dim = _static_dim(dmean, 0, "parameter dimension")
    state_dim = _static_dim(mean, 0, "state dimension")
    obs_dim = _static_dim(
        _matrix_at_time(observation_matrix, 0),
        0,
        "observation dimension",
    )
    identity_state = tf.eye(state_dim, dtype=tf.float64)
    identity_obs = tf.eye(obs_dim, dtype=tf.float64)
    two_pi = tf.constant(2.0 * math.pi, dtype=tf.float64)

    log_likelihood = tf.constant(0.0, dtype=tf.float64)
    score = tf.zeros((parameter_dim,), dtype=tf.float64)
    max_floor_count = tf.constant(0, dtype=tf.int32)
    max_projection_residual = tf.constant(0.0, dtype=tf.float64)
    min_innovation_eigenvalue = tf.constant(float("inf"), dtype=tf.float64)
    max_innovation_condition = tf.constant(0.0, dtype=tf.float64)
    min_gap = tf.constant(float("inf"), dtype=tf.float64)
    last_implemented_covariance = tf.zeros((obs_dim, obs_dim), dtype=tf.float64)

    for t in range(n_timesteps):
        c = _vector_at_time(transition_offset, t)
        T = _matrix_at_time(transition_matrix, t)
        Q = _matrix_at_time(transition_covariance, t)
        a = _vector_at_time(observation_offset, t)
        H = _matrix_at_time(observation_matrix, t)
        R = _matrix_at_time(observation_covariance, t)
        observation_noise = R + jitter_tensor * identity_obs

        predicted_mean = c + _matvec(T, mean)
        predicted_covariance = symmetrize(T @ covariance @ tf.transpose(T) + Q)

        dpredicted_mean_values = []
        dpredicted_covariance_values = []
        for i in range(parameter_dim):
            dpredicted_mean_values.append(
                d_transition_offset[i]
                + _matvec(d_transition_matrix[i], mean)
                + _matvec(T, dmean[i])
            )
            dpredicted_covariance_values.append(
                symmetrize(
                    d_transition_matrix[i] @ covariance @ tf.transpose(T)
                    + T @ dcovariance[i] @ tf.transpose(T)
                    + T @ covariance @ tf.transpose(d_transition_matrix[i])
                    + d_transition_covariance[i]
                )
            )
        dpredicted_mean = tf.stack(dpredicted_mean_values, axis=0)
        dpredicted_covariance = tf.stack(dpredicted_covariance_values, axis=0)

        innovation = y[t] - (a + _matvec(H, predicted_mean))
        innovation_covariance = symmetrize(
            H @ predicted_covariance @ tf.transpose(H) + observation_noise
        )
        eigenvalues, floored, eigenvectors, implemented_covariance, residual = psd_eigh(
            innovation_covariance,
            singular_floor_tensor,
        )
        innovation_solve = eigh_solve(eigenvectors, floored, innovation)
        innovation_precision = eigh_solve(eigenvectors, floored, identity_obs)
        log_det = eigh_logdet(floored)
        mahalanobis = tf.reduce_sum(innovation * innovation_solve)
        contribution = -0.5 * (
            tf.cast(obs_dim, tf.float64) * tf.math.log(two_pi)
            + log_det
            + mahalanobis
        )
        log_likelihood = log_likelihood + contribution

        dinnovation_values = []
        dS_values = []
        grad_values = []
        dK_values = []
        for i in range(parameter_dim):
            dinnovation_i = (
                -d_observation_offset[i]
                - _matvec(d_observation_matrix[i], predicted_mean)
                - _matvec(H, dpredicted_mean[i])
            )
            dS_i = symmetrize(
                d_observation_matrix[i]
                @ predicted_covariance
                @ tf.transpose(H)
                + H @ dpredicted_covariance[i] @ tf.transpose(H)
                + H
                @ predicted_covariance
                @ tf.transpose(d_observation_matrix[i])
                + d_observation_covariance[i]
            )
            dSinv_i = -(innovation_precision @ dS_i @ innovation_precision)
            dK_i = (
                dpredicted_covariance[i] @ tf.transpose(H) @ innovation_precision
                + predicted_covariance
                @ tf.transpose(d_observation_matrix[i])
                @ innovation_precision
                + predicted_covariance @ tf.transpose(H) @ dSinv_i
            )
            grad_i = -0.5 * (
                tf.linalg.trace(innovation_precision @ dS_i)
                + 2.0 * tf.tensordot(dinnovation_i, innovation_solve, axes=1)
                - tf.tensordot(
                    innovation_solve,
                    _matvec(dS_i, innovation_solve),
                    axes=1,
                )
            )
            dinnovation_values.append(dinnovation_i)
            dS_values.append(dS_i)
            dK_values.append(dK_i)
            grad_values.append(grad_i)
        dinnovation = tf.stack(dinnovation_values, axis=0)
        dK = tf.stack(dK_values, axis=0)
        score = score + tf.stack(grad_values, axis=0)

        kalman_gain = predicted_covariance @ tf.transpose(H) @ innovation_precision
        mean = predicted_mean + _matvec(kalman_gain, innovation)
        joseph_left = identity_state - kalman_gain @ H
        covariance = symmetrize(
            joseph_left @ predicted_covariance @ tf.transpose(joseph_left)
            + kalman_gain @ observation_noise @ tf.transpose(kalman_gain)
        )

        next_dmean_values = []
        next_dcovariance_values = []
        for i in range(parameter_dim):
            d_joseph_left_i = -dK[i] @ H - kalman_gain @ d_observation_matrix[i]
            next_dmean_values.append(
                dpredicted_mean[i]
                + _matvec(dK[i], innovation)
                + _matvec(kalman_gain, dinnovation[i])
            )
            next_dcovariance_values.append(
                symmetrize(
                    d_joseph_left_i
                    @ predicted_covariance
                    @ tf.transpose(joseph_left)
                    + joseph_left
                    @ dpredicted_covariance[i]
                    @ tf.transpose(joseph_left)
                    + joseph_left
                    @ predicted_covariance
                    @ tf.transpose(d_joseph_left_i)
                    + dK[i] @ observation_noise @ tf.transpose(kalman_gain)
                    + kalman_gain
                    @ d_observation_covariance[i]
                    @ tf.transpose(kalman_gain)
                    + kalman_gain @ observation_noise @ tf.transpose(dK[i])
                )
            )
        dmean = tf.stack(next_dmean_values, axis=0)
        dcovariance = tf.stack(next_dcovariance_values, axis=0)

        step_floor_count = floor_count(eigenvalues, singular_floor_tensor)
        max_floor_count = tf.maximum(max_floor_count, step_floor_count)
        max_projection_residual = tf.maximum(max_projection_residual, residual)
        min_innovation_eigenvalue = tf.minimum(
            min_innovation_eigenvalue,
            tf.reduce_min(eigenvalues),
        )
        condition = tf.reduce_max(eigenvalues) / tf.maximum(
            tf.reduce_min(eigenvalues),
            tf.constant(1e-300, dtype=tf.float64),
        )
        max_innovation_condition = tf.maximum(max_innovation_condition, condition)
        min_gap = tf.minimum(min_gap, _min_eigen_gap(eigenvalues))
        last_implemented_covariance = implemented_covariance

    return (
        log_likelihood,
        score,
        max_floor_count,
        max_projection_residual,
        last_implemented_covariance,
        min_innovation_eigenvalue,
        max_innovation_condition,
        min_gap,
    )


@tf.autograph.experimental.do_not_convert
def tf_svd_linear_gaussian_score_hessian(
    observations: tf.Tensor,
    model: TFLinearGaussianStateSpace,
    derivatives: TFLinearGaussianStateSpaceDerivatives,
    *,
    backend: TFSVDLinearDerivativeBackend = "tf_svd_solve_logdet",
    observation_mask: tf.Tensor | None = None,
    jitter: tf.Tensor | float = 0.0,
    singular_floor: tf.Tensor | float = 1e-12,
) -> TFFilterDerivativeResult:
    """Return the dense SVD/eigh solve-form LGSSM likelihood and score.

    The public name follows the existing ``*_score_hessian`` convention, but
    Hessian support is intentionally absent in this phase and ``hessian`` is
    always ``None``.  Active eigenvalue flooring raises ``ValueError`` because
    no floored-law derivative contract is certified here.
    """

    if backend != "tf_svd_solve_logdet":
        raise ValueError(f"unknown TensorFlow SVD derivative backend: {backend}")
    mask = observation_mask if observation_mask is not None else model.observation_mask
    if mask is not None:
        raise ValueError("tf_svd_linear_gaussian_score_hessian supports dense observations only")
    parameter_dim, _, observation_dim = _validate_model_derivative_shapes(model, derivatives)
    if not tf.executing_eagerly():
        blocked_result = TFFilterDerivativeResult(
            log_likelihood=tf.constant(float("nan"), dtype=tf.float64),
            score=tf.fill(
                (parameter_dim,),
                tf.constant(float("nan"), dtype=tf.float64),
            ),
            hessian=None,
            metadata=_metadata(
                filter_name="tf_svd_solve_logdet_score_kalman_blocked",
                model=model,
            ),
            diagnostics=_diagnostics(
                backend=backend,
                jitter=jitter,
                singular_floor=singular_floor,
                floor_count_value=tf.constant(-1, dtype=tf.int32),
                psd_projection_residual=tf.constant(float("nan"), dtype=tf.float64),
                implemented_covariance=tf.fill(
                    (observation_dim, observation_dim),
                    tf.constant(float("nan"), dtype=tf.float64),
                ),
                min_innovation_eigenvalue=tf.constant(float("nan"), dtype=tf.float64),
                innovation_condition_estimate=tf.constant(float("nan"), dtype=tf.float64),
                min_eigen_gap=tf.constant(float("nan"), dtype=tf.float64),
                derivative_target="blocked",
            ),
        )
        raise BlockedSVDSolveLogdetDerivativeError(
            "blocked_non_eager: tf_svd_linear_gaussian_score_hessian must be "
            "called from eager Python orchestration so active-floor blocked "
            "diagnostics can carry a TFFilterDerivativeResult",
            blocked_result,
        )
    y = _as_observation_matrix(observations)
    (
        log_likelihood,
        score,
        floor_count_value,
        residual,
        implemented_covariance,
        min_innovation_eigenvalue,
        condition_estimate,
        min_gap,
    ) = _tf_svd_solve_logdet_kalman_score(
        observations=y,
        transition_offset=model.transition_offset,
        transition_matrix=model.transition_matrix,
        transition_covariance=model.transition_covariance,
        observation_offset=model.observation_offset,
        observation_matrix=model.observation_matrix,
        observation_covariance=model.observation_covariance,
        initial_state_mean=model.initial_mean,
        initial_state_covariance=model.initial_covariance,
        d_initial_state_mean=derivatives.d_initial_mean,
        d_initial_state_covariance=derivatives.d_initial_covariance,
        d_transition_offset=derivatives.d_transition_offset,
        d_transition_matrix=derivatives.d_transition_matrix,
        d_transition_covariance=derivatives.d_transition_covariance,
        d_observation_offset=derivatives.d_observation_offset,
        d_observation_matrix=derivatives.d_observation_matrix,
        d_observation_covariance=derivatives.d_observation_covariance,
        jitter=jitter,
        singular_floor=singular_floor,
    )
    if tf.executing_eagerly() and int(floor_count_value.numpy()) > 0:
        blocked_result = TFFilterDerivativeResult(
            log_likelihood=log_likelihood,
            score=tf.fill(tf.shape(score), tf.constant(float("nan"), dtype=tf.float64)),
            hessian=None,
            metadata=_metadata(
                filter_name="tf_svd_solve_logdet_score_kalman_blocked",
                model=model,
            ),
            diagnostics=_diagnostics(
                backend=backend,
                jitter=jitter,
                singular_floor=singular_floor,
                floor_count_value=floor_count_value,
                psd_projection_residual=residual,
                implemented_covariance=implemented_covariance,
                min_innovation_eigenvalue=min_innovation_eigenvalue,
                innovation_condition_estimate=condition_estimate,
                min_eigen_gap=min_gap,
                derivative_target="blocked",
            ),
        )
        raise BlockedSVDSolveLogdetDerivativeError(
            "blocked_active_floor: SVD/eigh score derivative is blocked when "
            "the innovation eigenvalue floor is active",
            blocked_result,
        )
    return TFFilterDerivativeResult(
        log_likelihood=log_likelihood,
        score=score,
        hessian=None,
        metadata=_metadata(filter_name="tf_svd_solve_logdet_score_kalman", model=model),
        diagnostics=_diagnostics(
            backend=backend,
            jitter=jitter,
            singular_floor=singular_floor,
            floor_count_value=floor_count_value,
            psd_projection_residual=residual,
            implemented_covariance=implemented_covariance,
            min_innovation_eigenvalue=min_innovation_eigenvalue,
            innovation_condition_estimate=condition_estimate,
            min_eigen_gap=min_gap,
            derivative_target="pre_regularized_law",
        ),
    )
