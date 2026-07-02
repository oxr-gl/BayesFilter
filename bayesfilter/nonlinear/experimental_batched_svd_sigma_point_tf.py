"""Experimental batch-native SVD sigma-point value and score kernels.

This module is intentionally not exported from ``bayesfilter.nonlinear`` while
the batch-over-parameters contract is being tested.  The leading batch axis
indexes independent model parameter proposals; time remains sequential.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Literal, Mapping

import tensorflow as tf

from bayesfilter.ops import symmetric_principal_sqrt, symmetric_sylvester_solve
from bayesfilter.nonlinear.cut_tf import tf_cut4g_sigma_point_rule
from bayesfilter.nonlinear.sigma_points_tf import (
    TFSigmaPointRule,
    tf_unit_sigma_point_rule,
)

TFBatchedTransitionFn = Callable[[tf.Tensor, tf.Tensor], tf.Tensor]
TFBatchedObservationFn = Callable[[tf.Tensor], tf.Tensor]
TFBatchedLaggedObservationFn = Callable[
    [tf.Tensor, tf.Tensor, tf.Tensor],
    tf.Tensor,
]
TFBatchedResidualFn = Callable[[tf.Tensor, tf.Tensor, tf.Tensor], tf.Tensor]
TFBatchedTransitionStateJacobianFn = Callable[[tf.Tensor, tf.Tensor], tf.Tensor]
TFBatchedTransitionInnovationJacobianFn = Callable[[tf.Tensor, tf.Tensor], tf.Tensor]
TFBatchedTransitionParameterDerivativeFn = Callable[[tf.Tensor, tf.Tensor], tf.Tensor]
TFBatchedObservationStateJacobianFn = Callable[[tf.Tensor], tf.Tensor]
TFBatchedObservationParameterDerivativeFn = Callable[[tf.Tensor], tf.Tensor]
TFBatchedLaggedObservationStateJacobianFn = Callable[
    [tf.Tensor, tf.Tensor, tf.Tensor],
    tf.Tensor,
]
TFBatchedLaggedObservationInnovationJacobianFn = Callable[
    [tf.Tensor, tf.Tensor, tf.Tensor],
    tf.Tensor,
]
TFBatchedLaggedObservationParameterDerivativeFn = Callable[
    [tf.Tensor, tf.Tensor, tf.Tensor],
    tf.Tensor,
]
TFBatchedSVDBackend = Literal[
    "tf_svd_cubature",
    "tf_svd_ukf",
    "tf_svd_cut4",
    "tf_principal_sqrt_ukf",
]

_PRINCIPAL_SQRT_ROUNDOFF_TOLERANCE = 1.0e-14
_PRINCIPAL_SQRT_MAX_ABS_ENTRY_FOR_REPAIR = 1.0e8
_PRINCIPAL_SQRT_CLASSIFIED_INVALID_LOG_PROB = -1.0e100
_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE = 1.0e100
_PRINCIPAL_SQRT_RECONSTRUCTION_RELATIVE_TOLERANCE = 1.0e-10


@dataclass(frozen=True)
class TFBatchedStructuralStateSpace:
    """Minimal experimental batched structural state-space contract."""

    initial_mean: tf.Tensor
    initial_covariance: tf.Tensor
    innovation_covariance: tf.Tensor
    observation_covariance: tf.Tensor
    transition_fn: TFBatchedTransitionFn
    observation_fn: TFBatchedObservationFn
    deterministic_residual_fn: TFBatchedResidualFn | None = None
    name: str = "tf_batched_structural_state_space"
    lagged_observation_fn: TFBatchedLaggedObservationFn | None = None

    def __post_init__(self) -> None:
        for name, rank in (
            ("initial_mean", 2),
            ("initial_covariance", 3),
            ("innovation_covariance", 3),
            ("observation_covariance", 3),
        ):
            object.__setattr__(self, name, _to_rank(getattr(self, name), rank, name))
        self.validate_static_shapes()

    @property
    def batch_dim(self) -> int | None:
        return self.initial_mean.shape[0]

    @property
    def state_dim(self) -> int | None:
        return self.initial_mean.shape[-1]

    @property
    def innovation_dim(self) -> int | None:
        return self.innovation_covariance.shape[-1]

    @property
    def observation_dim(self) -> int | None:
        return self.observation_covariance.shape[-1]

    def validate_static_shapes(self) -> None:
        batch_dim = self.batch_dim
        state_dim = self.state_dim
        innovation_dim = self.innovation_dim
        observation_dim = self.observation_dim
        if None in (batch_dim, state_dim, innovation_dim, observation_dim):
            raise ValueError("batched structural tensors require static dimensions")
        expected = {
            "initial_covariance": (batch_dim, state_dim, state_dim),
            "innovation_covariance": (batch_dim, innovation_dim, innovation_dim),
            "observation_covariance": (batch_dim, observation_dim, observation_dim),
        }
        for name, shape in expected.items():
            actual = tuple(getattr(self, name).shape.as_list())
            if actual != shape:
                raise ValueError(f"{name} has shape {actual}, expected {shape}")

    def transition(self, previous_points: tf.Tensor, innovation_points: tf.Tensor) -> tf.Tensor:
        return self.transition_fn(previous_points, innovation_points)

    def observe(self, state_points: tf.Tensor) -> tf.Tensor:
        return self.observation_fn(state_points)

    def has_lagged_observation_contract(self) -> bool:
        return self.lagged_observation_fn is not None

    def observe_structural(
        self,
        previous_points: tf.Tensor,
        innovation_points: tf.Tensor,
        next_points: tf.Tensor,
    ) -> tf.Tensor:
        if self.lagged_observation_fn is None:
            return self.observe(next_points)
        return self.lagged_observation_fn(
            previous_points,
            innovation_points,
            next_points,
        )

    def deterministic_residual(
        self,
        previous_points: tf.Tensor,
        innovation_points: tf.Tensor,
        next_points: tf.Tensor,
    ) -> tf.Tensor:
        if self.deterministic_residual_fn is None:
            return tf.zeros(
                [tf.shape(next_points)[0], tf.shape(next_points)[1], 0],
                dtype=tf.float64,
            )
        return self.deterministic_residual_fn(
            previous_points,
            innovation_points,
            next_points,
        )


@dataclass(frozen=True)
class TFBatchedStructuralFirstDerivatives:
    """First-order derivatives for the experimental batched sigma-point score."""

    d_initial_mean: tf.Tensor
    d_initial_covariance: tf.Tensor
    d_innovation_covariance: tf.Tensor
    d_observation_covariance: tf.Tensor
    transition_state_jacobian_fn: TFBatchedTransitionStateJacobianFn
    transition_innovation_jacobian_fn: TFBatchedTransitionInnovationJacobianFn
    d_transition_fn: TFBatchedTransitionParameterDerivativeFn
    observation_state_jacobian_fn: TFBatchedObservationStateJacobianFn
    d_observation_fn: TFBatchedObservationParameterDerivativeFn
    name: str = "tf_batched_structural_first_derivatives"
    lagged_observation_previous_jacobian_fn: (
        TFBatchedLaggedObservationStateJacobianFn | None
    ) = None
    lagged_observation_innovation_jacobian_fn: (
        TFBatchedLaggedObservationInnovationJacobianFn | None
    ) = None
    lagged_observation_next_jacobian_fn: (
        TFBatchedLaggedObservationStateJacobianFn | None
    ) = None
    d_lagged_observation_fn: (
        TFBatchedLaggedObservationParameterDerivativeFn | None
    ) = None

    def __post_init__(self) -> None:
        for name in (
            "d_initial_mean",
            "d_initial_covariance",
            "d_innovation_covariance",
            "d_observation_covariance",
        ):
            object.__setattr__(
                self,
                name,
                tf.convert_to_tensor(getattr(self, name), dtype=tf.float64),
            )
        self.validate_static_shapes()

    @property
    def batch_dim(self) -> int | None:
        return self.d_initial_mean.shape[0]

    @property
    def parameter_dim(self) -> int | None:
        return self.d_initial_mean.shape[1]

    @property
    def state_dim(self) -> int | None:
        return self.d_initial_mean.shape[-1]

    @property
    def innovation_dim(self) -> int | None:
        return self.d_innovation_covariance.shape[-1]

    @property
    def observation_dim(self) -> int | None:
        return self.d_observation_covariance.shape[-1]

    def validate_static_shapes(self) -> None:
        batch_dim = self.batch_dim
        parameter_dim = self.parameter_dim
        state_dim = self.state_dim
        innovation_dim = self.innovation_dim
        observation_dim = self.observation_dim
        if None in (batch_dim, parameter_dim, state_dim, innovation_dim, observation_dim):
            raise ValueError("batched derivative tensors require static dimensions")
        expected = {
            "d_initial_mean": (batch_dim, parameter_dim, state_dim),
            "d_initial_covariance": (batch_dim, parameter_dim, state_dim, state_dim),
            "d_innovation_covariance": (
                batch_dim,
                parameter_dim,
                innovation_dim,
                innovation_dim,
            ),
            "d_observation_covariance": (
                batch_dim,
                parameter_dim,
                observation_dim,
                observation_dim,
            ),
        }
        for name, shape in expected.items():
            actual = tuple(getattr(self, name).shape.as_list())
            if actual != shape:
                raise ValueError(f"{name} has shape {actual}, expected {shape}")


@dataclass(frozen=True)
class TFBatchedSmoothEighFactorFirstDerivatives:
    eigenvalues: tf.Tensor
    floored_eigenvalues: tf.Tensor
    eigenvectors: tf.Tensor
    factor: tf.Tensor
    d_factor: tf.Tensor
    implemented_covariance: tf.Tensor
    floor_count: tf.Tensor
    min_eigen_gap: tf.Tensor
    psd_projection_residual: tf.Tensor
    derivative_reconstruction_residual: tf.Tensor
    structural_null_count: tf.Tensor
    structural_null_covariance_residual: tf.Tensor
    fixed_null_derivative_residual: tf.Tensor
    roundoff_repair_count: tf.Tensor
    classified_invalid_count: tf.Tensor
    derivative_rhs_nonfinite_count: tf.Tensor
    min_eigenvalue: tf.Tensor
    max_abs_covariance_entry: tf.Tensor
    max_abs_derivative_covariance_entry: tf.Tensor


def _to_rank(value: object, rank: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    if tensor.shape.rank != rank:
        raise ValueError(f"{name} must have rank {rank}")
    return tensor


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    matrix = tf.convert_to_tensor(matrix, dtype=tf.float64)
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _as_observation_matrix(observations: tf.Tensor) -> tf.Tensor:
    y = tf.convert_to_tensor(observations, dtype=tf.float64)
    if y.shape.rank == 1:
        y = y[:, tf.newaxis]
    if y.shape.rank != 2:
        raise ValueError("observations must be one- or two-dimensional")
    if y.shape[0] is None:
        raise ValueError("experimental sigma-point filters require static observation length")
    return y


def _principal_sqrt_frechet_derivative_from_eigh(
    eigenvectors: tf.Tensor,
    sqrt_eigenvalues: tf.Tensor,
    d_covariance: tf.Tensor,
) -> tf.Tensor:
    """Compute the SPD principal-square-root Frechet derivative in eigenbasis."""

    transformed_rhs = tf.einsum(
        "bia,bpij,bjc->bpac",
        eigenvectors,
        d_covariance,
        eigenvectors,
    )
    denominator = (
        sqrt_eigenvalues[:, :, tf.newaxis]
        + sqrt_eigenvalues[:, tf.newaxis, :]
    )
    transformed_derivative = (
        transformed_rhs / denominator[:, tf.newaxis, :, :]
    )
    return _symmetrize(
        tf.einsum(
            "bia,bpac,bjc->bpij",
            eigenvectors,
            transformed_derivative,
            eigenvectors,
        )
    )


def _check_model_derivative_shapes(
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
) -> tuple[int, int, int, int, int]:
    values = (
        model.batch_dim,
        derivatives.parameter_dim,
        model.state_dim,
        model.innovation_dim,
        model.observation_dim,
    )
    if any(value is None for value in values):
        raise ValueError("experimental batched sigma-point score requires static dimensions")
    batch_dim, parameter_dim, state_dim, innovation_dim, observation_dim = values
    if derivatives.batch_dim != batch_dim:
        raise ValueError("derivative batch dimension does not match model")
    if derivatives.state_dim != state_dim:
        raise ValueError("derivative state dimension does not match model")
    if derivatives.innovation_dim != innovation_dim:
        raise ValueError("derivative innovation dimension does not match model")
    if derivatives.observation_dim != observation_dim:
        raise ValueError("derivative observation dimension does not match model")
    return (
        int(batch_dim),
        int(parameter_dim),
        int(state_dim),
        int(innovation_dim),
        int(observation_dim),
    )


def _batched_floor_count(eigenvalues: tf.Tensor, singular_floor: tf.Tensor) -> tf.Tensor:
    return tf.reduce_sum(tf.cast(eigenvalues <= singular_floor, tf.int32), axis=-1)


def _batched_psd_eigh(
    covariance: tf.Tensor,
    singular_floor: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    covariance = _symmetrize(covariance)
    eigenvalues, eigenvectors = tf.linalg.eigh(covariance)
    floored = tf.maximum(eigenvalues, singular_floor)
    implemented = (
        eigenvectors
        @ tf.linalg.diag(floored)
        @ tf.linalg.matrix_transpose(eigenvectors)
    )
    residual = tf.linalg.norm(implemented - covariance, axis=[-2, -1])
    return eigenvalues, floored, eigenvectors, implemented, residual


def _principal_sqrt_covariance_classification(
    covariance: tf.Tensor,
    eigenvalues: tf.Tensor,
    singular_floor: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    """Classify strict principal-sqrt covariance rows before the custom op.

    The principal-sqrt backend is strict-SPD by design.  HMC proposals can still
    push a row to tiny negative eigenvalues from accumulated floating-point
    roundoff.  This helper repairs only finite near-SPD rows and fails closed
    for nonfinite or materially indefinite rows before they reach the custom op,
    which keeps XLA diagnostics classified instead of surfacing raw op errors.
    """

    finite_covariance = tf.reduce_all(tf.math.is_finite(covariance), axis=[-2, -1])
    finite_eigenvalues = tf.reduce_all(tf.math.is_finite(eigenvalues), axis=-1)
    finite_row = tf.logical_and(finite_covariance, finite_eigenvalues)
    min_eigenvalue = tf.reduce_min(
        tf.where(
            tf.math.is_finite(eigenvalues),
            eigenvalues,
            tf.fill(
                tf.shape(eigenvalues),
                tf.constant(-_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE, tf.float64),
            ),
        ),
        axis=-1,
    )
    abs_covariance = tf.abs(covariance)
    max_abs_covariance_entry = tf.reduce_max(
        tf.where(
            tf.math.is_finite(abs_covariance),
            abs_covariance,
            tf.fill(
                tf.shape(abs_covariance),
                tf.constant(_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE, tf.float64),
            ),
        ),
        axis=[-2, -1],
    )
    repair_floor = tf.maximum(
        singular_floor,
        tf.constant(_PRINCIPAL_SQRT_ROUNDOFF_TOLERANCE, dtype=tf.float64),
    )
    strict_spd = tf.logical_and(finite_row, min_eigenvalue >= repair_floor)
    near_spd = tf.logical_and(
        finite_row,
        tf.logical_and(
            min_eigenvalue
            >= tf.constant(-_PRINCIPAL_SQRT_ROUNDOFF_TOLERANCE, dtype=tf.float64),
            max_abs_covariance_entry <= _PRINCIPAL_SQRT_MAX_ABS_ENTRY_FOR_REPAIR,
        ),
    )
    roundoff_repaired = tf.logical_and(
        near_spd,
        min_eigenvalue < repair_floor,
    )
    classified_invalid = tf.logical_not(tf.logical_or(strict_spd, roundoff_repaired))
    safe_eigenvalues = tf.where(
        tf.math.is_finite(eigenvalues),
        tf.maximum(eigenvalues, repair_floor),
        tf.fill(tf.shape(eigenvalues), repair_floor),
    )
    repaired_covariance = _symmetrize(
        covariance
        + tf.eye(int(covariance.shape[-1]), dtype=tf.float64)[tf.newaxis, :, :]
        * tf.maximum(repair_floor - min_eigenvalue, 0.0)[:, tf.newaxis, tf.newaxis]
    )
    valid_or_repaired_covariance = tf.where(
        roundoff_repaired[:, tf.newaxis, tf.newaxis],
        repaired_covariance,
        covariance,
    )
    # The strict compiled op uses Eigen's self-adjoint eigensolver, which can
    # disagree with TensorFlow's ``eigh`` by a few ulps near the SPD boundary.
    # Give every finite row accepted by this classifier the same tiny fixed
    # guard margin used for roundoff repair so raw Eigen failures become
    # classified target behavior instead of process-level op crashes.
    raw_op_margin = (
        tf.eye(int(covariance.shape[-1]), dtype=tf.float64)[tf.newaxis, :, :]
        * repair_floor
    )
    valid_or_repaired_covariance = valid_or_repaired_covariance + raw_op_margin
    replacement_scale = tf.maximum(repair_floor, tf.constant(1.0, dtype=tf.float64))
    replacement_covariance = (
        tf.eye(int(covariance.shape[-1]), dtype=tf.float64)[tf.newaxis, :, :]
        * replacement_scale
    )
    safe_covariance = tf.where(
        classified_invalid[:, tf.newaxis, tf.newaxis],
        replacement_covariance,
        valid_or_repaired_covariance,
    )
    return (
        safe_covariance,
        safe_eigenvalues,
        roundoff_repaired,
        classified_invalid,
        max_abs_covariance_entry,
    )


def _batched_eigh_solve(
    eigenvectors: tf.Tensor,
    eigenvalues: tf.Tensor,
    rhs: tf.Tensor,
) -> tf.Tensor:
    rhs = tf.convert_to_tensor(rhs, dtype=tf.float64)
    if rhs.shape.rank == 2:
        projected = tf.linalg.matvec(eigenvectors, rhs, transpose_a=True)
        scaled = projected / eigenvalues
        return tf.linalg.matvec(eigenvectors, scaled)
    if rhs.shape.rank == 3:
        projected = tf.matmul(eigenvectors, rhs, transpose_a=True)
        scaled = projected / eigenvalues[:, :, tf.newaxis]
        return tf.matmul(eigenvectors, scaled)
    if rhs.shape.rank == 4:
        projected = tf.einsum("bia,bpin->bpan", eigenvectors, rhs)
        scaled = projected / eigenvalues[:, tf.newaxis, :, tf.newaxis]
        return tf.einsum("bia,bpan->bpin", eigenvectors, scaled)
    raise ValueError("rhs must have rank 2, 3, or 4")


def _batched_eigh_logdet(eigenvalues: tf.Tensor) -> tf.Tensor:
    return tf.reduce_sum(tf.math.log(eigenvalues), axis=-1)


def _batched_cholesky_solve(cholesky_factor: tf.Tensor, rhs: tf.Tensor) -> tf.Tensor:
    rhs = tf.convert_to_tensor(rhs, dtype=tf.float64)
    if rhs.shape.rank == 2:
        solved = tf.linalg.cholesky_solve(cholesky_factor, rhs[:, :, tf.newaxis])
        return solved[:, :, 0]
    if rhs.shape.rank == 3:
        return tf.linalg.cholesky_solve(cholesky_factor, rhs)
    if rhs.shape.rank == 4:
        batch_size = tf.shape(rhs)[0]
        parameter_dim = tf.shape(rhs)[1]
        matrix_dim = tf.shape(rhs)[2]
        column_dim = tf.shape(rhs)[3]
        tiled_cholesky = tf.repeat(cholesky_factor, parameter_dim, axis=0)
        flat_rhs = tf.reshape(rhs, [batch_size * parameter_dim, matrix_dim, column_dim])
        solved = tf.linalg.cholesky_solve(tiled_cholesky, flat_rhs)
        return tf.reshape(solved, [batch_size, parameter_dim, matrix_dim, column_dim])
    raise ValueError("rhs must have rank 2, 3, or 4")


def _batched_cholesky_logdet(cholesky_factor: tf.Tensor) -> tf.Tensor:
    return 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(cholesky_factor)), axis=-1)


def _batched_min_eigen_gap(eigenvalues: tf.Tensor) -> tf.Tensor:
    dim = eigenvalues.shape[-1]
    if dim is None:
        raise ValueError("eigen dimension must be static")
    if int(dim) <= 1:
        return tf.fill([tf.shape(eigenvalues)[0]], tf.constant(float("inf"), tf.float64))
    gaps = eigenvalues[:, 1:] - eigenvalues[:, :-1]
    return tf.reduce_min(tf.abs(gaps), axis=-1)


def _batched_min_active_factor_gap(
    eigenvalues: tf.Tensor,
    active: tf.Tensor,
) -> tf.Tensor:
    dim = eigenvalues.shape[-1]
    if dim is None:
        raise ValueError("active eigen dimension must be static")
    eye = tf.eye(int(dim), dtype=tf.bool)[tf.newaxis, :, :]
    pair_mask = tf.logical_and(active[:, tf.newaxis, :], tf.logical_not(eye))
    gaps = tf.abs(eigenvalues[:, tf.newaxis, :] - eigenvalues[:, :, tf.newaxis])
    masked = tf.where(
        pair_mask,
        gaps,
        tf.fill(tf.shape(gaps), tf.constant(float("inf"), dtype=tf.float64)),
    )
    return tf.reduce_min(masked, axis=[-2, -1])


def _checked_batched_smooth_eigh_factor_first_derivatives(
    covariance: tf.Tensor,
    d_covariance: tf.Tensor,
    *,
    singular_floor: tf.Tensor,
    rank_tolerance: tf.Tensor,
    spectral_gap_tolerance: tf.Tensor,
    fixed_null_tolerance: tf.Tensor,
    label: str,
    allow_fixed_null_support: bool = False,
) -> TFBatchedSmoothEighFactorFirstDerivatives:
    covariance = _symmetrize(covariance)
    d_covariance = _symmetrize(d_covariance)
    (
        eigenvalues,
        floored,
        eigenvectors,
        implemented_covariance,
        psd_projection_residual,
    ) = _batched_psd_eigh(covariance, singular_floor)
    projected = tf.einsum(
        "bia,bpij,bjc->bpac",
        eigenvectors,
        d_covariance,
        eigenvectors,
    )

    if allow_fixed_null_support:
        active = eigenvalues > rank_tolerance
        null = tf.logical_not(active)
        min_gap = _batched_min_active_factor_gap(eigenvalues, active)
        active_floors = tf.reduce_sum(tf.cast(eigenvalues < singular_floor, tf.int32), axis=-1)
        structural_null_count = tf.reduce_sum(tf.cast(null, tf.int32), axis=-1)
        null_eigenvalues = tf.where(null, tf.abs(eigenvalues), tf.zeros_like(eigenvalues))
        structural_null_covariance_residual = tf.reduce_max(null_eigenvalues, axis=-1)
        null_mask = tf.logical_or(null[:, :, tf.newaxis], null[:, tf.newaxis, :])
        masked_null_derivatives = tf.where(
            null_mask[:, tf.newaxis, :, :],
            projected,
            tf.zeros_like(projected),
        )
        fixed_null_residual = tf.reduce_max(tf.abs(masked_null_derivatives), axis=[-3, -2, -1])
    else:
        active = eigenvalues > singular_floor
        min_gap = _batched_min_eigen_gap(eigenvalues)
        active_floors = _batched_floor_count(eigenvalues, singular_floor)
        structural_null_count = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32)
        structural_null_covariance_residual = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.float64)
        fixed_null_residual = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.float64)

    batch_zeros = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32)
    assertions = [
        tf.debugging.assert_equal(
            active_floors,
            batch_zeros,
            message=f"blocked_active_floor: {label} floor is active",
        ),
        tf.debugging.assert_greater(
            min_gap,
            spectral_gap_tolerance,
            message=f"blocked_weak_spectral_gap: {label} spectrum is not separated",
        ),
        tf.debugging.assert_all_finite(
            eigenvalues,
            f"blocked_nonfinite_factor: {label} eigenvalues are nonfinite",
        ),
        tf.debugging.assert_less_equal(
            structural_null_covariance_residual,
            fixed_null_tolerance,
            message=f"blocked_structural_null_covariance: {label} null support has positive variance",
        ),
        tf.debugging.assert_less_equal(
            fixed_null_residual,
            fixed_null_tolerance,
            message=f"blocked_moving_structural_null: {label} null support is parameter-dependent",
        ),
    ]
    with tf.control_dependencies(assertions):
        eigenvalues = tf.identity(eigenvalues)
        floored = tf.identity(floored)
        eigenvectors = tf.identity(eigenvectors)
        implemented_covariance = tf.identity(implemented_covariance)
        active = tf.identity(active)

    active_float = tf.cast(active, tf.float64)
    sqrt_eigenvalues = tf.sqrt(floored) * active_float
    factor = eigenvectors * sqrt_eigenvalues[:, tf.newaxis, :]
    dim = int(eigenvalues.shape[-1])
    eye = tf.eye(dim, dtype=tf.float64)[tf.newaxis, :, :]
    denominator = eigenvalues[:, tf.newaxis, :] - eigenvalues[:, :, tf.newaxis]
    safe_denominator = tf.where(
        tf.not_equal(denominator, 0.0),
        denominator,
        tf.ones_like(denominator),
    )
    coefficient_mask = (1.0 - eye) * active_float[:, tf.newaxis, :]
    coefficients = (
        projected
        / safe_denominator[:, tf.newaxis, :, :]
        * coefficient_mask[:, tf.newaxis, :, :]
    )
    d_eigenvectors = tf.einsum("bdc,bpca->bpda", eigenvectors, coefficients)
    d_eigenvalues = tf.linalg.diag_part(projected)
    safe_sqrt = tf.where(active, sqrt_eigenvalues, tf.ones_like(sqrt_eigenvalues))
    d_sqrt_eigenvalues = (
        0.5
        * d_eigenvalues
        / safe_sqrt[:, tf.newaxis, :]
        * active_float[:, tf.newaxis, :]
    )
    d_factor = (
        d_eigenvectors * sqrt_eigenvalues[:, tf.newaxis, tf.newaxis, :]
        + eigenvectors[:, tf.newaxis, :, :] * d_sqrt_eigenvalues[:, :, tf.newaxis, :]
    )
    reconstructed = tf.matmul(
        d_factor,
        factor[:, tf.newaxis, :, :],
        transpose_b=True,
    ) + tf.matmul(
        factor[:, tf.newaxis, :, :],
        d_factor,
        transpose_b=True,
    )
    reconstruction_residual = tf.reduce_max(
        tf.linalg.norm(reconstructed - d_covariance, axis=[-2, -1]),
        axis=-1,
    )
    if allow_fixed_null_support:
        implemented_covariance = _symmetrize(factor @ tf.linalg.matrix_transpose(factor))
        psd_projection_residual = tf.linalg.norm(
            implemented_covariance - covariance,
            axis=[-2, -1],
        )
    return TFBatchedSmoothEighFactorFirstDerivatives(
        eigenvalues=eigenvalues,
        floored_eigenvalues=floored,
        eigenvectors=eigenvectors,
        factor=factor,
        d_factor=d_factor,
        implemented_covariance=implemented_covariance,
        floor_count=active_floors,
        min_eigen_gap=min_gap,
        psd_projection_residual=psd_projection_residual,
        derivative_reconstruction_residual=reconstruction_residual,
        structural_null_count=structural_null_count,
        structural_null_covariance_residual=structural_null_covariance_residual,
        fixed_null_derivative_residual=fixed_null_residual,
        roundoff_repair_count=tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32),
        classified_invalid_count=tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32),
        derivative_rhs_nonfinite_count=tf.zeros(
            tf.shape(eigenvalues)[0],
            dtype=tf.int32,
        ),
        min_eigenvalue=tf.reduce_min(eigenvalues, axis=-1),
        max_abs_covariance_entry=tf.reduce_max(tf.abs(covariance), axis=[-2, -1]),
        max_abs_derivative_covariance_entry=tf.reduce_max(
            tf.abs(d_covariance),
            axis=[-3, -2, -1],
        ),
    )


def _checked_batched_principal_sqrt_factor_first_derivatives(
    covariance: tf.Tensor,
    d_covariance: tf.Tensor,
    *,
    singular_floor: tf.Tensor,
    fixed_null_tolerance: tf.Tensor,
    label: str,
    lyapunov_tolerance: tf.Tensor | float = 1.0e-10,
) -> TFBatchedSmoothEighFactorFirstDerivatives:
    covariance = _symmetrize(covariance)
    d_covariance = _symmetrize(d_covariance)
    (
        eigenvalues,
        floored,
        eigenvectors,
        _implemented_covariance,
        psd_projection_residual,
    ) = _batched_psd_eigh(covariance, singular_floor)
    min_eigenvalue = tf.reduce_min(
        tf.where(
            tf.math.is_finite(eigenvalues),
            eigenvalues,
            tf.fill(
                tf.shape(eigenvalues),
                tf.constant(-_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE, tf.float64),
            ),
        ),
        axis=-1,
    )
    (
        safe_covariance,
        safe_eigenvalues,
        roundoff_repaired,
        classified_invalid,
        max_abs_covariance_entry,
    ) = _principal_sqrt_covariance_classification(
        covariance,
        eigenvalues,
        singular_floor,
    )
    identity_eigenvectors = tf.eye(
        int(covariance.shape[-1]),
        dtype=tf.float64,
    )[tf.newaxis, :, :]
    eigenvectors = tf.where(
        classified_invalid[:, tf.newaxis, tf.newaxis],
        identity_eigenvectors,
        eigenvectors,
    )
    active_floors = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32)
    roundoff_repair_count = tf.cast(roundoff_repaired, tf.int32)
    finite_d_covariance = tf.reduce_all(
        tf.math.is_finite(d_covariance),
        axis=[-3, -2, -1],
    )
    derivative_rhs_nonfinite = tf.logical_not(finite_d_covariance)
    combined_classified_invalid = tf.logical_or(
        classified_invalid,
        derivative_rhs_nonfinite,
    )
    classified_invalid_count = tf.cast(combined_classified_invalid, tf.int32)
    derivative_rhs_nonfinite_count = tf.cast(derivative_rhs_nonfinite, tf.int32)
    abs_d_covariance = tf.abs(d_covariance)
    max_abs_derivative_covariance_entry = tf.reduce_max(
        tf.where(
            tf.math.is_finite(abs_d_covariance),
            abs_d_covariance,
            tf.fill(
                tf.shape(abs_d_covariance),
                tf.constant(_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE, tf.float64),
            ),
        ),
        axis=[-3, -2, -1],
    )
    structural_null_count = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.int32)
    structural_null_covariance_residual = tf.zeros(
        tf.shape(eigenvalues)[0],
        dtype=tf.float64,
    )
    fixed_null_residual = tf.zeros(tf.shape(eigenvalues)[0], dtype=tf.float64)
    min_gap = _batched_min_eigen_gap(eigenvalues)
    min_gap = tf.where(
        classified_invalid,
        tf.zeros_like(min_gap),
        min_gap,
    )

    assertions = [
        tf.debugging.assert_all_finite(
            safe_eigenvalues,
            f"blocked_nonfinite_factor: {label} eigenvalues are nonfinite",
        ),
        tf.debugging.assert_less_equal(
            structural_null_covariance_residual,
            fixed_null_tolerance,
            message=f"blocked_structural_null_covariance: {label} null support has positive variance",
        ),
        tf.debugging.assert_less_equal(
            fixed_null_residual,
            fixed_null_tolerance,
            message=f"blocked_moving_structural_null: {label} null support is parameter-dependent",
        ),
    ]
    with tf.control_dependencies(assertions):
        eigenvalues = tf.identity(safe_eigenvalues)
        floored = tf.identity(tf.maximum(safe_eigenvalues, singular_floor))
        eigenvectors = tf.identity(eigenvectors)
        safe_covariance = tf.identity(safe_covariance)

    covariance_valid_or_repaired_mask = tf.logical_not(classified_invalid)
    valid_derivative_mask = tf.logical_not(combined_classified_invalid)
    valid_derivative_parameter_mask = valid_derivative_mask[:, tf.newaxis]
    factor = _symmetrize(symmetric_principal_sqrt(safe_covariance))
    safe_d_covariance = tf.where(
        combined_classified_invalid[:, tf.newaxis, tf.newaxis, tf.newaxis],
        tf.zeros_like(d_covariance),
        tf.where(tf.math.is_finite(d_covariance), d_covariance, tf.zeros_like(d_covariance)),
    )
    d_factor = _symmetrize(symmetric_sylvester_solve(factor, safe_d_covariance))
    implemented_covariance = _symmetrize(factor @ tf.linalg.matrix_transpose(factor))
    psd_projection_residual = tf.linalg.norm(
        implemented_covariance - covariance,
        axis=[-2, -1],
    )
    psd_projection_residual = tf.where(
        covariance_valid_or_repaired_mask,
        psd_projection_residual,
        tf.fill(
            tf.shape(psd_projection_residual),
            tf.constant(_PRINCIPAL_SQRT_DIAGNOSTIC_LARGE, tf.float64),
        ),
    )
    lyapunov_residual = tf.linalg.norm(
        factor[:, tf.newaxis, :, :] @ d_factor
        + d_factor @ factor[:, tf.newaxis, :, :]
        - safe_d_covariance,
        axis=[-2, -1],
    )
    lyapunov_residual = tf.where(
        valid_derivative_parameter_mask,
        lyapunov_residual,
        tf.zeros_like(lyapunov_residual),
    )
    reconstructed = tf.matmul(
        d_factor,
        factor[:, tf.newaxis, :, :],
        transpose_b=True,
    ) + tf.matmul(
        factor[:, tf.newaxis, :, :],
        d_factor,
        transpose_b=True,
    )
    reconstruction_residual = tf.linalg.norm(
        reconstructed - safe_d_covariance,
        axis=[-2, -1],
    )
    reconstruction_residual = tf.where(
        valid_derivative_parameter_mask,
        reconstruction_residual,
        tf.zeros_like(reconstruction_residual),
    )
    max_residual = tf.maximum(lyapunov_residual, reconstruction_residual)
    lyapunov_tolerance = tf.convert_to_tensor(lyapunov_tolerance, dtype=tf.float64)
    derivative_scale = tf.linalg.norm(safe_d_covariance, axis=[-2, -1])
    derivative_scale = tf.where(
        valid_derivative_parameter_mask,
        derivative_scale,
        tf.zeros_like(derivative_scale),
    )
    scaled_tolerance = (
        lyapunov_tolerance
        + tf.constant(
            _PRINCIPAL_SQRT_RECONSTRUCTION_RELATIVE_TOLERANCE,
            dtype=tf.float64,
        )
        * derivative_scale
    )
    with tf.control_dependencies(
        [
            tf.debugging.assert_less_equal(
                tf.reduce_max(max_residual - scaled_tolerance),
                tf.constant(0.0, dtype=tf.float64),
                message=f"blocked_principal_sqrt_reconstruction: {label} derivative reconstruction failed",
            )
        ]
    ):
        d_factor = tf.identity(d_factor)

    return TFBatchedSmoothEighFactorFirstDerivatives(
        eigenvalues=eigenvalues,
        floored_eigenvalues=floored,
        eigenvectors=eigenvectors,
        factor=factor,
        d_factor=d_factor,
        implemented_covariance=implemented_covariance,
        floor_count=active_floors,
        min_eigen_gap=min_gap,
        psd_projection_residual=psd_projection_residual,
        derivative_reconstruction_residual=tf.reduce_max(max_residual, axis=-1),
        structural_null_count=structural_null_count,
        structural_null_covariance_residual=structural_null_covariance_residual,
        fixed_null_derivative_residual=fixed_null_residual,
        roundoff_repair_count=roundoff_repair_count,
        classified_invalid_count=classified_invalid_count,
        derivative_rhs_nonfinite_count=derivative_rhs_nonfinite_count,
        min_eigenvalue=min_eigenvalue,
        max_abs_covariance_entry=max_abs_covariance_entry,
        max_abs_derivative_covariance_entry=max_abs_derivative_covariance_entry,
    )


def _weighted_covariance(centered: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    return _symmetrize(tf.einsum("r,bri,brj->bij", weights, centered, centered))


def _weighted_covariance_first_derivatives(
    centered: tf.Tensor,
    d_centered: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    return _symmetrize(
        tf.einsum("r,bpri,brj->bpij", weights, d_centered, centered)
        + tf.einsum("r,bri,bprj->bpij", weights, centered, d_centered)
    )


def _matvec_points(jacobian: tf.Tensor, vectors: tf.Tensor) -> tf.Tensor:
    return tf.einsum("broi,bpri->bpro", jacobian, vectors)


def _rule_for_backend(
    backend: TFBatchedSVDBackend,
    aug_dim: int,
) -> tuple[TFSigmaPointRule, str]:
    if backend == "tf_svd_cubature":
        return tf_unit_sigma_point_rule(aug_dim, rule="cubature"), "tf_svd_cubature"
    if backend == "tf_svd_ukf":
        return (
            tf_unit_sigma_point_rule(
                aug_dim,
                rule="unscented",
                alpha=1.0,
                beta=2.0,
                kappa=0.0,
            ),
            "tf_svd_ukf",
        )
    if backend == "tf_principal_sqrt_ukf":
        return (
            tf_unit_sigma_point_rule(
                aug_dim,
                rule="unscented",
                alpha=1.0,
                beta=2.0,
                kappa=0.0,
            ),
            "tf_principal_sqrt_ukf",
        )
    if backend == "tf_svd_cut4":
        return tf_cut4g_sigma_point_rule(aug_dim), "tf_svd_cut4"
    raise ValueError(f"unknown batched SVD sigma-point backend: {backend}")


def tf_batched_svd_sigma_point_value_and_score_with_rule(
    observations: tf.Tensor,
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
    *,
    sigma_rule: TFSigmaPointRule,
    backend_name: str = "tf_batched_svd_sigma_point",
    placement_floor: tf.Tensor | float = 0.0,
    innovation_floor: tf.Tensor | float = 1.0e-12,
    rank_tolerance: tf.Tensor | float = 1.0e-12,
    spectral_gap_tolerance: tf.Tensor | float = 1.0e-8,
    fixed_null_tolerance: tf.Tensor | float = 1.0e-10,
    principal_sqrt_reconstruction_tolerance: tf.Tensor | float = 1.0e-10,
    jitter: tf.Tensor | float = 0.0,
    allow_fixed_null_support: bool = False,
) -> tuple[tf.Tensor, tf.Tensor, Mapping[str, tf.Tensor]]:
    """Return batched nonlinear SVD sigma-point likelihood and analytic score."""

    y = _as_observation_matrix(observations)
    n_timesteps = int(y.shape[0])
    batch_dim, parameter_dim, state_dim, innovation_dim, observation_dim = (
        _check_model_derivative_shapes(model, derivatives)
    )
    aug_dim = state_dim + innovation_dim
    if sigma_rule.dim != aug_dim:
        raise ValueError("sigma_rule dimension must equal state_dim + innovation_dim")
    lagged_observation_contract = model.has_lagged_observation_contract()
    observation_contract = (
        "lagged_previous_innovation_predicted"
        if lagged_observation_contract
        else "current_predicted_state"
    )
    if lagged_observation_contract and (
        derivatives.lagged_observation_previous_jacobian_fn is None
        or derivatives.lagged_observation_innovation_jacobian_fn is None
        or derivatives.lagged_observation_next_jacobian_fn is None
        or derivatives.d_lagged_observation_fn is None
    ):
        raise ValueError(
            "lagged observation contract requires previous, innovation, next, "
            "and parameter derivative hooks"
        )

    mean = tf.convert_to_tensor(model.initial_mean, dtype=tf.float64)
    covariance = _symmetrize(model.initial_covariance)
    d_mean = tf.convert_to_tensor(derivatives.d_initial_mean, dtype=tf.float64)
    d_covariance = _symmetrize(derivatives.d_initial_covariance)
    innovation_covariance = _symmetrize(model.innovation_covariance)
    d_innovation_covariance = _symmetrize(derivatives.d_innovation_covariance)
    observation_covariance = _symmetrize(model.observation_covariance)
    d_observation_covariance = _symmetrize(derivatives.d_observation_covariance)

    placement_floor = tf.convert_to_tensor(placement_floor, dtype=tf.float64)
    innovation_floor = tf.convert_to_tensor(innovation_floor, dtype=tf.float64)
    rank_tolerance = tf.convert_to_tensor(rank_tolerance, dtype=tf.float64)
    spectral_gap_tolerance = tf.convert_to_tensor(spectral_gap_tolerance, dtype=tf.float64)
    fixed_null_tolerance = tf.convert_to_tensor(fixed_null_tolerance, dtype=tf.float64)
    principal_sqrt_reconstruction_tolerance = tf.convert_to_tensor(
        principal_sqrt_reconstruction_tolerance,
        dtype=tf.float64,
    )
    jitter = tf.convert_to_tensor(jitter, dtype=tf.float64)

    obs_identity = tf.eye(observation_dim, dtype=tf.float64)[tf.newaxis, :, :]
    two_pi = tf.constant(2.0 * math.pi, dtype=tf.float64)
    log_likelihood = tf.zeros([batch_dim], dtype=tf.float64)
    score = tf.zeros([batch_dim, parameter_dim], dtype=tf.float64)

    max_placement_floor_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_innovation_floor_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_placement_roundoff_repair_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_innovation_roundoff_repair_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_placement_classified_invalid_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_innovation_classified_invalid_count = tf.zeros([batch_dim], dtype=tf.int32)
    max_placement_derivative_rhs_nonfinite_count = tf.zeros(
        [batch_dim],
        dtype=tf.int32,
    )
    max_innovation_derivative_rhs_nonfinite_count = tf.zeros(
        [batch_dim],
        dtype=tf.int32,
    )
    max_placement_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_innovation_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_support_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_deterministic_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_factor_derivative_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_fixed_null_derivative_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_structural_null_covariance_residual = tf.zeros([batch_dim], dtype=tf.float64)
    max_integration_rank = tf.zeros([batch_dim], dtype=tf.int32)
    max_structural_null_count = tf.zeros([batch_dim], dtype=tf.int32)
    min_placement_eigen_gap = tf.fill([batch_dim], tf.constant(float("inf"), dtype=tf.float64))
    min_innovation_eigen_gap = tf.fill([batch_dim], tf.constant(float("inf"), dtype=tf.float64))
    min_placement_eigenvalue = tf.fill([batch_dim], tf.constant(float("inf"), dtype=tf.float64))
    min_innovation_eigenvalue = tf.fill([batch_dim], tf.constant(float("inf"), dtype=tf.float64))
    max_placement_covariance_abs_entry = tf.zeros([batch_dim], dtype=tf.float64)
    max_innovation_covariance_abs_entry = tf.zeros([batch_dim], dtype=tf.float64)
    max_placement_derivative_covariance_abs_entry = tf.zeros(
        [batch_dim],
        dtype=tf.float64,
    )
    max_innovation_derivative_covariance_abs_entry = tf.zeros(
        [batch_dim],
        dtype=tf.float64,
    )
    last_implemented_innovation_covariance = tf.zeros(
        [batch_dim, observation_dim, observation_dim],
        dtype=tf.float64,
    )

    n_timesteps_tensor = tf.constant(n_timesteps, dtype=tf.int32)

    def _loop_body(
        t: tf.Tensor,
        mean: tf.Tensor,
        covariance: tf.Tensor,
        d_mean: tf.Tensor,
        d_covariance: tf.Tensor,
        log_likelihood: tf.Tensor,
        score: tf.Tensor,
        max_placement_floor_count: tf.Tensor,
        max_innovation_floor_count: tf.Tensor,
        max_placement_roundoff_repair_count: tf.Tensor,
        max_innovation_roundoff_repair_count: tf.Tensor,
        max_placement_classified_invalid_count: tf.Tensor,
        max_innovation_classified_invalid_count: tf.Tensor,
        max_placement_derivative_rhs_nonfinite_count: tf.Tensor,
        max_innovation_derivative_rhs_nonfinite_count: tf.Tensor,
        max_placement_residual: tf.Tensor,
        max_innovation_residual: tf.Tensor,
        max_support_residual: tf.Tensor,
        max_deterministic_residual: tf.Tensor,
        max_factor_derivative_residual: tf.Tensor,
        max_fixed_null_derivative_residual: tf.Tensor,
        max_structural_null_covariance_residual: tf.Tensor,
        max_integration_rank: tf.Tensor,
        max_structural_null_count: tf.Tensor,
        min_placement_eigen_gap: tf.Tensor,
        min_innovation_eigen_gap: tf.Tensor,
        min_placement_eigenvalue: tf.Tensor,
        min_innovation_eigenvalue: tf.Tensor,
        max_placement_covariance_abs_entry: tf.Tensor,
        max_innovation_covariance_abs_entry: tf.Tensor,
        max_placement_derivative_covariance_abs_entry: tf.Tensor,
        max_innovation_derivative_covariance_abs_entry: tf.Tensor,
        last_implemented_innovation_covariance: tf.Tensor,
    ) -> tuple[tf.Tensor, ...]:
        aug_mean = tf.concat(
            [mean, tf.zeros([batch_dim, innovation_dim], dtype=tf.float64)],
            axis=1,
        )
        d_aug_mean = tf.concat(
            [
                d_mean,
                tf.zeros([batch_dim, parameter_dim, innovation_dim], dtype=tf.float64),
            ],
            axis=2,
        )
        upper = tf.concat(
            [
                covariance,
                tf.zeros([batch_dim, state_dim, innovation_dim], dtype=tf.float64),
            ],
            axis=2,
        )
        lower = tf.concat(
            [
                tf.zeros([batch_dim, innovation_dim, state_dim], dtype=tf.float64),
                innovation_covariance,
            ],
            axis=2,
        )
        aug_covariance = tf.concat([upper, lower], axis=1)
        d_aug_covariance = tf.concat(
            [
                tf.concat(
                    [
                        d_covariance,
                        tf.zeros(
                            [batch_dim, parameter_dim, state_dim, innovation_dim],
                            dtype=tf.float64,
                        ),
                    ],
                    axis=3,
                ),
                tf.concat(
                    [
                        tf.zeros(
                            [batch_dim, parameter_dim, innovation_dim, state_dim],
                            dtype=tf.float64,
                        ),
                        d_innovation_covariance,
                    ],
                    axis=3,
                ),
            ],
            axis=2,
        )
        if backend_name == "tf_principal_sqrt_ukf":
            if allow_fixed_null_support:
                raise ValueError(
                    "tf_principal_sqrt_ukf is strict-SPD-only in Phase 3 and "
                    "does not support structural null branches"
                )
            placement = _checked_batched_principal_sqrt_factor_first_derivatives(
                aug_covariance,
                d_aug_covariance,
                singular_floor=placement_floor,
                fixed_null_tolerance=fixed_null_tolerance,
                lyapunov_tolerance=principal_sqrt_reconstruction_tolerance,
                label="principal-sqrt sigma-point placement",
            )
        else:
            placement = _checked_batched_smooth_eigh_factor_first_derivatives(
                aug_covariance,
                d_aug_covariance,
                singular_floor=placement_floor,
                rank_tolerance=rank_tolerance,
                spectral_gap_tolerance=spectral_gap_tolerance,
                fixed_null_tolerance=fixed_null_tolerance,
                label="SVD sigma-point placement",
                allow_fixed_null_support=allow_fixed_null_support,
            )
        point_offsets = tf.einsum("ra,bda->brd", sigma_rule.offsets, placement.factor)
        aug_points = aug_mean[:, tf.newaxis, :] + point_offsets
        d_point_offsets = tf.einsum("rd,bpad->bpra", sigma_rule.offsets, placement.d_factor)
        d_aug_points = d_aug_mean[:, :, tf.newaxis, :] + d_point_offsets
        previous_points = aug_points[:, :, :state_dim]
        innovation_points = aug_points[:, :, state_dim:]
        d_previous_points = d_aug_points[:, :, :, :state_dim]
        d_innovation_points = d_aug_points[:, :, :, state_dim:]

        predicted_points = model.transition(previous_points, innovation_points)
        transition_state_jacobian = derivatives.transition_state_jacobian_fn(
            previous_points,
            innovation_points,
        )
        transition_innovation_jacobian = derivatives.transition_innovation_jacobian_fn(
            previous_points,
            innovation_points,
        )
        d_transition_param = derivatives.d_transition_fn(
            previous_points,
            innovation_points,
        )
        _validate_static_shape(
            transition_state_jacobian,
            (batch_dim, sigma_rule.point_count, state_dim, state_dim),
            "transition_state_jacobian",
        )
        _validate_static_shape(
            transition_innovation_jacobian,
            (batch_dim, sigma_rule.point_count, state_dim, innovation_dim),
            "transition_innovation_jacobian",
        )
        _validate_static_shape(
            d_transition_param,
            (batch_dim, parameter_dim, sigma_rule.point_count, state_dim),
            "d_transition",
        )
        d_predicted_points = (
            _matvec_points(transition_state_jacobian, d_previous_points)
            + _matvec_points(transition_innovation_jacobian, d_innovation_points)
            + d_transition_param
        )
        residuals = model.deterministic_residual(
            previous_points,
            innovation_points,
            predicted_points,
        )
        deterministic_residual = (
            tf.zeros([batch_dim], dtype=tf.float64)
            if residuals.shape[-1] == 0
            else tf.reduce_max(tf.abs(residuals), axis=[1, 2])
        )

        predicted_mean = tf.einsum(
            "r,brn->bn",
            sigma_rule.mean_weights,
            predicted_points,
        )
        d_predicted_mean = tf.einsum(
            "r,bprn->bpn",
            sigma_rule.mean_weights,
            d_predicted_points,
        )
        centered_x = predicted_points - predicted_mean[:, tf.newaxis, :]
        d_centered_x = d_predicted_points - d_predicted_mean[:, :, tf.newaxis, :]
        predicted_covariance = _weighted_covariance(
            centered_x,
            sigma_rule.covariance_weights,
        )
        d_predicted_covariance = _weighted_covariance_first_derivatives(
            centered_x,
            d_centered_x,
            sigma_rule.covariance_weights,
        )

        if lagged_observation_contract:
            observation_points = model.observe_structural(
                previous_points,
                innovation_points,
                predicted_points,
            )
            observation_previous_jacobian = (
                derivatives.lagged_observation_previous_jacobian_fn(
                    previous_points,
                    innovation_points,
                    predicted_points,
                )
            )
            observation_innovation_jacobian = (
                derivatives.lagged_observation_innovation_jacobian_fn(
                    previous_points,
                    innovation_points,
                    predicted_points,
                )
            )
            observation_next_jacobian = (
                derivatives.lagged_observation_next_jacobian_fn(
                    previous_points,
                    innovation_points,
                    predicted_points,
                )
            )
            d_observation_param = derivatives.d_lagged_observation_fn(
                previous_points,
                innovation_points,
                predicted_points,
            )
            _validate_static_shape(
                observation_previous_jacobian,
                (batch_dim, sigma_rule.point_count, observation_dim, state_dim),
                "lagged_observation_previous_jacobian",
            )
            _validate_static_shape(
                observation_innovation_jacobian,
                (batch_dim, sigma_rule.point_count, observation_dim, innovation_dim),
                "lagged_observation_innovation_jacobian",
            )
            _validate_static_shape(
                observation_next_jacobian,
                (batch_dim, sigma_rule.point_count, observation_dim, state_dim),
                "lagged_observation_next_jacobian",
            )
            _validate_static_shape(
                d_observation_param,
                (batch_dim, parameter_dim, sigma_rule.point_count, observation_dim),
                "d_lagged_observation",
            )
            d_observation_points = (
                _matvec_points(observation_previous_jacobian, d_previous_points)
                + _matvec_points(
                    observation_innovation_jacobian,
                    d_innovation_points,
                )
                + _matvec_points(observation_next_jacobian, d_predicted_points)
                + d_observation_param
            )
        else:
            observation_points = model.observe(predicted_points)
            observation_state_jacobian = derivatives.observation_state_jacobian_fn(
                predicted_points,
            )
            d_observation_param = derivatives.d_observation_fn(predicted_points)
            _validate_static_shape(
                observation_state_jacobian,
                (batch_dim, sigma_rule.point_count, observation_dim, state_dim),
                "observation_state_jacobian",
            )
            _validate_static_shape(
                d_observation_param,
                (batch_dim, parameter_dim, sigma_rule.point_count, observation_dim),
                "d_observation",
            )
            d_observation_points = (
                _matvec_points(observation_state_jacobian, d_predicted_points)
                + d_observation_param
            )
        observation_mean = tf.einsum(
            "r,brm->bm",
            sigma_rule.mean_weights,
            observation_points,
        )
        d_observation_mean = tf.einsum(
            "r,bprm->bpm",
            sigma_rule.mean_weights,
            d_observation_points,
        )
        centered_y = observation_points - observation_mean[:, tf.newaxis, :]
        d_centered_y = d_observation_points - d_observation_mean[:, :, tf.newaxis, :]
        raw_innovation_covariance = _symmetrize(
            _weighted_covariance(centered_y, sigma_rule.covariance_weights)
            + observation_covariance
            + jitter * obs_identity
        )
        d_raw_innovation_covariance = _symmetrize(
            _weighted_covariance_first_derivatives(
                centered_y,
                d_centered_y,
                sigma_rule.covariance_weights,
            )
            + d_observation_covariance
        )
        if backend_name == "tf_principal_sqrt_ukf":
            innovation_factor = _checked_batched_principal_sqrt_factor_first_derivatives(
                raw_innovation_covariance,
                d_raw_innovation_covariance,
                singular_floor=innovation_floor,
                fixed_null_tolerance=fixed_null_tolerance,
                lyapunov_tolerance=principal_sqrt_reconstruction_tolerance,
                label="principal-sqrt sigma-point innovation",
            )
        else:
            innovation_factor = _checked_batched_smooth_eigh_factor_first_derivatives(
                raw_innovation_covariance,
                d_raw_innovation_covariance,
                singular_floor=innovation_floor,
                rank_tolerance=rank_tolerance,
                spectral_gap_tolerance=spectral_gap_tolerance,
                fixed_null_tolerance=fixed_null_tolerance,
                label="SVD sigma-point innovation",
                allow_fixed_null_support=False,
            )
        cross_covariance = tf.einsum(
            "brn,r,brm->bnm",
            centered_x,
            sigma_rule.covariance_weights,
            centered_y,
        )
        d_cross_covariance = (
            tf.einsum(
                "r,bprn,brm->bpnm",
                sigma_rule.covariance_weights,
                d_centered_x,
                centered_y,
            )
            + tf.einsum(
                "r,brn,bprm->bpnm",
                sigma_rule.covariance_weights,
                centered_x,
                d_centered_y,
            )
        )
        innovation = y[t][tf.newaxis, :] - observation_mean
        d_innovation = -d_observation_mean
        if backend_name == "tf_principal_sqrt_ukf":
            innovation_cholesky = tf.linalg.cholesky(
                innovation_factor.implemented_covariance
            )
            solve_innovation = _batched_cholesky_solve(
                innovation_cholesky,
                innovation,
            )
            innovation_precision = _batched_cholesky_solve(
                innovation_cholesky,
                tf.tile(obs_identity, [batch_dim, 1, 1]),
            )
            log_det = _batched_cholesky_logdet(innovation_cholesky)
        else:
            solve_innovation = _batched_eigh_solve(
                innovation_factor.eigenvectors,
                innovation_factor.floored_eigenvalues,
                innovation,
            )
            innovation_precision = _batched_eigh_solve(
                innovation_factor.eigenvectors,
                innovation_factor.floored_eigenvalues,
                tf.tile(obs_identity, [batch_dim, 1, 1]),
            )
            log_det = _batched_eigh_logdet(innovation_factor.floored_eigenvalues)
        mahalanobis = tf.reduce_sum(innovation * solve_innovation, axis=-1)
        contribution = -0.5 * (
            tf.cast(observation_dim, tf.float64) * tf.math.log(two_pi)
            + log_det
            + mahalanobis
        )
        trace_terms = tf.einsum(
            "bij,bpji->bp",
            innovation_precision,
            d_raw_innovation_covariance,
        )
        innovation_derivative_terms = tf.einsum(
            "bpm,bm->bp",
            d_innovation,
            solve_innovation,
        )
        covariance_quadratic_terms = tf.einsum(
            "bm,bpmn,bn->bp",
            solve_innovation,
            d_raw_innovation_covariance,
            solve_innovation,
        )
        score = score - 0.5 * (
            trace_terms
            + 2.0 * innovation_derivative_terms
            - covariance_quadratic_terms
        )

        kalman_gain = tf.matmul(cross_covariance, innovation_precision)
        rhs = (
            tf.linalg.matrix_transpose(d_cross_covariance)
            - tf.matmul(
                d_raw_innovation_covariance,
                tf.linalg.matrix_transpose(kalman_gain)[:, tf.newaxis, :, :],
            )
        )
        if backend_name == "tf_principal_sqrt_ukf":
            d_kalman_gain = tf.linalg.matrix_transpose(
                _batched_cholesky_solve(innovation_cholesky, rhs)
            )
        else:
            d_kalman_gain = tf.linalg.matrix_transpose(
                _batched_eigh_solve(
                    innovation_factor.eigenvectors,
                    innovation_factor.floored_eigenvalues,
                    rhs,
                )
            )

        mean = predicted_mean + tf.einsum("bnm,bm->bn", kalman_gain, innovation)
        d_mean = (
            d_predicted_mean
            + tf.einsum("bpnm,bm->bpn", d_kalman_gain, innovation)
            + tf.einsum("bnm,bpm->bpn", kalman_gain, d_innovation)
        )
        covariance = _symmetrize(
            predicted_covariance
            - kalman_gain
            @ innovation_factor.implemented_covariance
            @ tf.linalg.matrix_transpose(kalman_gain)
        )
        d_covariance = _symmetrize(
            d_predicted_covariance
            - tf.einsum(
                "bpnm,bml,bkl->bpnk",
                d_kalman_gain,
                innovation_factor.implemented_covariance,
                kalman_gain,
            )
            - tf.einsum(
                "bnm,bpml,bkl->bpnk",
                kalman_gain,
                d_raw_innovation_covariance,
                kalman_gain,
            )
            - tf.einsum(
                "bnm,bml,bpkl->bpnk",
                kalman_gain,
                innovation_factor.implemented_covariance,
                d_kalman_gain,
            )
        )
        log_likelihood = log_likelihood + contribution

        active = placement.eigenvalues > rank_tolerance
        rank = tf.reduce_sum(tf.cast(active, tf.int32), axis=-1)
        null_weights = tf.cast(tf.logical_not(active), tf.float64)
        null_projector = (
            placement.eigenvectors
            @ tf.linalg.diag(null_weights)
            @ tf.linalg.matrix_transpose(placement.eigenvectors)
        )
        support_residual = tf.reduce_max(
            tf.linalg.norm(point_offsets @ null_projector, axis=-1),
            axis=-1,
        )
        max_placement_floor_count = tf.maximum(
            max_placement_floor_count,
            placement.floor_count,
        )
        max_innovation_floor_count = tf.maximum(
            max_innovation_floor_count,
            innovation_factor.floor_count,
        )
        max_placement_roundoff_repair_count = tf.maximum(
            max_placement_roundoff_repair_count,
            placement.roundoff_repair_count,
        )
        max_innovation_roundoff_repair_count = tf.maximum(
            max_innovation_roundoff_repair_count,
            innovation_factor.roundoff_repair_count,
        )
        max_placement_classified_invalid_count = tf.maximum(
            max_placement_classified_invalid_count,
            placement.classified_invalid_count,
        )
        max_innovation_classified_invalid_count = tf.maximum(
            max_innovation_classified_invalid_count,
            innovation_factor.classified_invalid_count,
        )
        max_placement_derivative_rhs_nonfinite_count = tf.maximum(
            max_placement_derivative_rhs_nonfinite_count,
            placement.derivative_rhs_nonfinite_count,
        )
        max_innovation_derivative_rhs_nonfinite_count = tf.maximum(
            max_innovation_derivative_rhs_nonfinite_count,
            innovation_factor.derivative_rhs_nonfinite_count,
        )
        max_placement_residual = tf.maximum(
            max_placement_residual,
            placement.psd_projection_residual,
        )
        max_innovation_residual = tf.maximum(
            max_innovation_residual,
            innovation_factor.psd_projection_residual,
        )
        max_support_residual = tf.maximum(max_support_residual, support_residual)
        max_deterministic_residual = tf.maximum(
            max_deterministic_residual,
            deterministic_residual,
        )
        max_factor_derivative_residual = tf.maximum(
            max_factor_derivative_residual,
            tf.maximum(
                placement.derivative_reconstruction_residual,
                innovation_factor.derivative_reconstruction_residual,
            ),
        )
        max_fixed_null_derivative_residual = tf.maximum(
            max_fixed_null_derivative_residual,
            placement.fixed_null_derivative_residual,
        )
        max_structural_null_covariance_residual = tf.maximum(
            max_structural_null_covariance_residual,
            placement.structural_null_covariance_residual,
        )
        max_integration_rank = tf.maximum(max_integration_rank, rank)
        max_structural_null_count = tf.maximum(
            max_structural_null_count,
            placement.structural_null_count,
        )
        min_placement_eigen_gap = tf.minimum(
            min_placement_eigen_gap,
            placement.min_eigen_gap,
        )
        min_innovation_eigen_gap = tf.minimum(
            min_innovation_eigen_gap,
            innovation_factor.min_eigen_gap,
        )
        min_placement_eigenvalue = tf.minimum(
            min_placement_eigenvalue,
            placement.min_eigenvalue,
        )
        min_innovation_eigenvalue = tf.minimum(
            min_innovation_eigenvalue,
            innovation_factor.min_eigenvalue,
        )
        max_placement_covariance_abs_entry = tf.maximum(
            max_placement_covariance_abs_entry,
            placement.max_abs_covariance_entry,
        )
        max_innovation_covariance_abs_entry = tf.maximum(
            max_innovation_covariance_abs_entry,
            innovation_factor.max_abs_covariance_entry,
        )
        max_placement_derivative_covariance_abs_entry = tf.maximum(
            max_placement_derivative_covariance_abs_entry,
            placement.max_abs_derivative_covariance_entry,
        )
        max_innovation_derivative_covariance_abs_entry = tf.maximum(
            max_innovation_derivative_covariance_abs_entry,
            innovation_factor.max_abs_derivative_covariance_entry,
        )
        last_implemented_innovation_covariance = (
            innovation_factor.implemented_covariance
        )

        return (
            t + tf.constant(1, dtype=tf.int32),
            mean,
            covariance,
            d_mean,
            d_covariance,
            log_likelihood,
            score,
            max_placement_floor_count,
            max_innovation_floor_count,
            max_placement_roundoff_repair_count,
            max_innovation_roundoff_repair_count,
            max_placement_classified_invalid_count,
            max_innovation_classified_invalid_count,
            max_placement_derivative_rhs_nonfinite_count,
            max_innovation_derivative_rhs_nonfinite_count,
            max_placement_residual,
            max_innovation_residual,
            max_support_residual,
            max_deterministic_residual,
            max_factor_derivative_residual,
            max_fixed_null_derivative_residual,
            max_structural_null_covariance_residual,
            max_integration_rank,
            max_structural_null_count,
            min_placement_eigen_gap,
            min_innovation_eigen_gap,
            min_placement_eigenvalue,
            min_innovation_eigenvalue,
            max_placement_covariance_abs_entry,
            max_innovation_covariance_abs_entry,
            max_placement_derivative_covariance_abs_entry,
            max_innovation_derivative_covariance_abs_entry,
            last_implemented_innovation_covariance,
        )

    (
        _t,
        mean,
        covariance,
        d_mean,
        d_covariance,
        log_likelihood,
        score,
        max_placement_floor_count,
        max_innovation_floor_count,
        max_placement_roundoff_repair_count,
        max_innovation_roundoff_repair_count,
        max_placement_classified_invalid_count,
        max_innovation_classified_invalid_count,
        max_placement_derivative_rhs_nonfinite_count,
        max_innovation_derivative_rhs_nonfinite_count,
        max_placement_residual,
        max_innovation_residual,
        max_support_residual,
        max_deterministic_residual,
        max_factor_derivative_residual,
        max_fixed_null_derivative_residual,
        max_structural_null_covariance_residual,
        max_integration_rank,
        max_structural_null_count,
        min_placement_eigen_gap,
        min_innovation_eigen_gap,
        min_placement_eigenvalue,
        min_innovation_eigenvalue,
        max_placement_covariance_abs_entry,
        max_innovation_covariance_abs_entry,
        max_placement_derivative_covariance_abs_entry,
        max_innovation_derivative_covariance_abs_entry,
        last_implemented_innovation_covariance,
    ) = tf.while_loop(
        lambda t, *_unused: t < n_timesteps_tensor,
        _loop_body,
        (
            tf.constant(0, dtype=tf.int32),
            mean,
            covariance,
            d_mean,
            d_covariance,
            log_likelihood,
            score,
            max_placement_floor_count,
            max_innovation_floor_count,
            max_placement_roundoff_repair_count,
            max_innovation_roundoff_repair_count,
            max_placement_classified_invalid_count,
            max_innovation_classified_invalid_count,
            max_placement_derivative_rhs_nonfinite_count,
            max_innovation_derivative_rhs_nonfinite_count,
            max_placement_residual,
            max_innovation_residual,
            max_support_residual,
            max_deterministic_residual,
            max_factor_derivative_residual,
            max_fixed_null_derivative_residual,
            max_structural_null_covariance_residual,
            max_integration_rank,
            max_structural_null_count,
            min_placement_eigen_gap,
            min_innovation_eigen_gap,
            min_placement_eigenvalue,
            min_innovation_eigenvalue,
            max_placement_covariance_abs_entry,
            max_innovation_covariance_abs_entry,
            max_placement_derivative_covariance_abs_entry,
            max_innovation_derivative_covariance_abs_entry,
            last_implemented_innovation_covariance,
        ),
        parallel_iterations=1,
    )

    total_classified_invalid_count = (
        max_placement_classified_invalid_count
        + max_innovation_classified_invalid_count
    )
    total_derivative_rhs_nonfinite_count = (
        max_placement_derivative_rhs_nonfinite_count
        + max_innovation_derivative_rhs_nonfinite_count
    )
    classified_invalid_mask = total_classified_invalid_count > 0
    checked_value = tf.where(
        classified_invalid_mask,
        tf.fill(
            tf.shape(log_likelihood),
            tf.constant(_PRINCIPAL_SQRT_CLASSIFIED_INVALID_LOG_PROB, tf.float64),
        ),
        log_likelihood,
    )
    checked_score = tf.where(
        classified_invalid_mask[:, tf.newaxis],
        tf.zeros_like(score),
        score,
    )
    checked_value = tf.where(
        tf.math.is_finite(checked_value),
        checked_value,
        tf.fill(
            tf.shape(checked_value),
            tf.constant(_PRINCIPAL_SQRT_CLASSIFIED_INVALID_LOG_PROB, tf.float64),
        ),
    )
    checked_score = tf.where(
        tf.math.is_finite(checked_score),
        checked_score,
        tf.zeros_like(checked_score),
    )
    nonfinite_value_gradient_mask = tf.logical_or(
        tf.logical_not(tf.math.is_finite(log_likelihood)),
        tf.reduce_any(tf.logical_not(tf.math.is_finite(score)), axis=-1),
    )
    checked_value = tf.where(
        nonfinite_value_gradient_mask,
        tf.fill(
            tf.shape(checked_value),
            tf.constant(_PRINCIPAL_SQRT_CLASSIFIED_INVALID_LOG_PROB, tf.float64),
        ),
        checked_value,
    )
    checked_score = tf.where(
        nonfinite_value_gradient_mask[:, tf.newaxis],
        tf.zeros_like(checked_score),
        checked_score,
    )
    checked_value = tf.debugging.check_numerics(
        checked_value,
        "blocked_nonfinite_value: batched SVD sigma-point value is nonfinite",
    )
    checked_score = tf.debugging.check_numerics(
        checked_score,
        "blocked_nonfinite_score: batched SVD sigma-point score is nonfinite",
    )
    classified_invalid_count = total_classified_invalid_count + tf.cast(
        tf.logical_and(
            nonfinite_value_gradient_mask,
            tf.logical_not(classified_invalid_mask),
        ),
        tf.int32,
    )
    valid_count = tf.cast(
        tf.logical_not(
            tf.logical_or(classified_invalid_mask, nonfinite_value_gradient_mask)
        ),
        tf.int32,
    )
    roundoff_repair_count = (
        max_placement_roundoff_repair_count + max_innovation_roundoff_repair_count
    )
    target_row_class_code = tf.where(
        classified_invalid_count > 0,
        tf.fill(tf.shape(classified_invalid_count), tf.constant(2, dtype=tf.int32)),
        tf.where(
            roundoff_repair_count > 0,
            tf.fill(tf.shape(roundoff_repair_count), tf.constant(1, dtype=tf.int32)),
            tf.fill(tf.shape(roundoff_repair_count), tf.constant(0, dtype=tf.int32)),
        ),
    )
    diagnostics = {
        "backend": tf.constant(backend_name),
        "rule": tf.constant(sigma_rule.name),
        "observation_contract": tf.constant(observation_contract),
        "observation_contract_runtime_selected": tf.constant(True),
        "augmented_dim": tf.constant(aug_dim, dtype=tf.int32),
        "point_count": tf.constant(sigma_rule.point_count, dtype=tf.int32),
        "polynomial_degree": tf.constant(sigma_rule.polynomial_degree, dtype=tf.int32),
        "max_integration_rank": max_integration_rank,
        "structural_null_count": max_structural_null_count,
        "support_residual": max_support_residual,
        "deterministic_residual": max_deterministic_residual,
        "min_placement_eigen_gap": min_placement_eigen_gap,
        "min_innovation_eigen_gap": min_innovation_eigen_gap,
        "min_placement_eigenvalue": min_placement_eigenvalue,
        "min_innovation_eigenvalue": min_innovation_eigenvalue,
        "max_placement_covariance_abs_entry": max_placement_covariance_abs_entry,
        "max_innovation_covariance_abs_entry": max_innovation_covariance_abs_entry,
        "max_placement_derivative_covariance_abs_entry": (
            max_placement_derivative_covariance_abs_entry
        ),
        "max_innovation_derivative_covariance_abs_entry": (
            max_innovation_derivative_covariance_abs_entry
        ),
        "factor_derivative_reconstruction_residual": max_factor_derivative_residual,
        "fixed_null_derivative_residual": max_fixed_null_derivative_residual,
        "structural_null_covariance_residual": max_structural_null_covariance_residual,
        "placement_psd_projection_residual": max_placement_residual,
        "innovation_psd_projection_residual": max_innovation_residual,
        "placement_floor_count": max_placement_floor_count,
        "innovation_floor_count": max_innovation_floor_count,
        "placement_roundoff_repair_count": max_placement_roundoff_repair_count,
        "innovation_roundoff_repair_count": max_innovation_roundoff_repair_count,
        "placement_classified_invalid_count": max_placement_classified_invalid_count,
        "innovation_classified_invalid_count": max_innovation_classified_invalid_count,
        "placement_derivative_rhs_nonfinite_count": (
            max_placement_derivative_rhs_nonfinite_count
        ),
        "innovation_derivative_rhs_nonfinite_count": (
            max_innovation_derivative_rhs_nonfinite_count
        ),
        "principal_sqrt_target_valid_count": valid_count,
        "principal_sqrt_target_roundoff_repair_count": roundoff_repair_count,
        "principal_sqrt_target_classified_invalid_count": classified_invalid_count,
        "principal_sqrt_target_derivative_rhs_nonfinite_count": (
            total_derivative_rhs_nonfinite_count
        ),
        "principal_sqrt_target_row_class_code": target_row_class_code,
        "principal_sqrt_target_row_class_legend": tf.constant(
            "0=valid,1=roundoff_repaired,2=classified_invalid"
        ),
        "principal_sqrt_classified_invalid_log_prob": tf.constant(
            _PRINCIPAL_SQRT_CLASSIFIED_INVALID_LOG_PROB,
            dtype=tf.float64,
        ),
        "principal_sqrt_covariance_failure_policy": tf.constant(
            "strict_spd_with_roundoff_repair_and_classified_invalid_finite_reject"
        ),
        "principal_sqrt_roundoff_repair_threshold": tf.constant(
            _PRINCIPAL_SQRT_ROUNDOFF_TOLERANCE,
            dtype=tf.float64,
        ),
        "principal_sqrt_roundoff_repair_max_abs_entry": tf.constant(
            _PRINCIPAL_SQRT_MAX_ABS_ENTRY_FOR_REPAIR,
            dtype=tf.float64,
        ),
        "implemented_innovation_covariance": last_implemented_innovation_covariance,
        "derivative_branch": tf.constant(
            "strict_spd_principal_sqrt"
            if backend_name == "tf_principal_sqrt_ukf"
            else (
                "structural_fixed_support_no_active_floor"
                if allow_fixed_null_support
                else "smooth_simple_spectrum_no_active_floor"
            )
        ),
        "derivative_method": tf.constant(
            "analytic_first_order_principal_sqrt_sylvester"
            if backend_name == "tf_principal_sqrt_ukf"
            else (
                "analytic_first_order_structural_fixed_support"
                if allow_fixed_null_support
                else "analytic_first_order_smooth_branch"
            )
        ),
        "derivative_provider": tf.constant(derivatives.name),
    }
    return checked_value, checked_score, diagnostics


def tf_batched_svd_sigma_point_value_and_score(
    observations: tf.Tensor,
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
    *,
    backend: TFBatchedSVDBackend,
    placement_floor: tf.Tensor | float = 0.0,
    innovation_floor: tf.Tensor | float = 1.0e-12,
    rank_tolerance: tf.Tensor | float = 1.0e-12,
    spectral_gap_tolerance: tf.Tensor | float = 1.0e-8,
    fixed_null_tolerance: tf.Tensor | float = 1.0e-10,
    principal_sqrt_reconstruction_tolerance: tf.Tensor | float = 1.0e-10,
    jitter: tf.Tensor | float = 0.0,
    allow_fixed_null_support: bool = False,
) -> tuple[tf.Tensor, tf.Tensor, Mapping[str, tf.Tensor]]:
    """Dispatch to an experimental batch-native SVD sigma-point value+score."""

    _batch_dim, _p, state_dim, innovation_dim, _observation_dim = (
        _check_model_derivative_shapes(model, derivatives)
    )
    rule, backend_name = _rule_for_backend(backend, state_dim + innovation_dim)
    return tf_batched_svd_sigma_point_value_and_score_with_rule(
        observations,
        model,
        derivatives,
        sigma_rule=rule,
        backend_name=backend_name,
        placement_floor=placement_floor,
        innovation_floor=innovation_floor,
        rank_tolerance=rank_tolerance,
        spectral_gap_tolerance=spectral_gap_tolerance,
        fixed_null_tolerance=fixed_null_tolerance,
        principal_sqrt_reconstruction_tolerance=(
            principal_sqrt_reconstruction_tolerance),
        jitter=jitter,
        allow_fixed_null_support=allow_fixed_null_support,
    )


def tf_batched_svd_cubature_value_and_score(
    observations: tf.Tensor,
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
    **kwargs,
) -> tuple[tf.Tensor, tf.Tensor, Mapping[str, tf.Tensor]]:
    return tf_batched_svd_sigma_point_value_and_score(
        observations,
        model,
        derivatives,
        backend="tf_svd_cubature",
        **kwargs,
    )


def tf_batched_svd_ukf_value_and_score(
    observations: tf.Tensor,
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
    **kwargs,
) -> tuple[tf.Tensor, tf.Tensor, Mapping[str, tf.Tensor]]:
    return tf_batched_svd_sigma_point_value_and_score(
        observations,
        model,
        derivatives,
        backend="tf_svd_ukf",
        **kwargs,
    )


def tf_batched_svd_cut4_value_and_score(
    observations: tf.Tensor,
    model: TFBatchedStructuralStateSpace,
    derivatives: TFBatchedStructuralFirstDerivatives,
    **kwargs,
) -> tuple[tf.Tensor, tf.Tensor, Mapping[str, tf.Tensor]]:
    return tf_batched_svd_sigma_point_value_and_score(
        observations,
        model,
        derivatives,
        backend="tf_svd_cut4",
        **kwargs,
    )


def _validate_static_shape(tensor: tf.Tensor, expected: tuple[int | None, ...], name: str) -> None:
    actual = tensor.shape.as_list()
    if any(dim is None for dim in actual):
        return
    if tuple(actual) != expected:
        raise ValueError(f"{name} has shape {tuple(actual)}, expected {expected}")
