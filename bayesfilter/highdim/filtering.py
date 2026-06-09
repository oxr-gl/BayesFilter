"""Deterministic highdim filtering value-path contracts for Phase 4."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, Sequence

import tensorflow as tf
import tensorflow_probability as tfp

from bayesfilter.highdim.diagnostics import (
    HighDimStatus,
    MeasureConvention,
    assert_density_matches_mass,
    assert_tf_float64,
    freeze_mapping,
)
from bayesfilter.highdim.fixed_branch import BranchIdentity, BranchManifest
from bayesfilter.highdim.bases import ProductBasis
from bayesfilter.highdim.fitting import FixedTTFitConfig, FixedTTFitSampleBatch, FixedTTFitter
from bayesfilter.highdim.models import LinearGaussianSSM, TFHighDimStateSpaceModel
from bayesfilter.highdim.squared_tt import SquaredTTDensity, TensorProductReferenceDensity
from bayesfilter.highdim.tt import TTCore


class HighDimCoordinateMap(Protocol):
    """Coordinate map from reference points to physical points."""

    def forward(self, reference_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        """Return physical points and log absolute determinant."""

    def inverse(self, physical_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        """Return reference points and log absolute determinant."""

    def manifest_payload(self) -> Mapping[str, object]:
        """Return deterministic coordinate-map fields."""


@dataclass(frozen=True)
class IdentityCoordinateMap:
    """Identity reference-to-physical coordinate map."""

    dimension: int
    dtype: tf.DType = tf.float64

    def __post_init__(self) -> None:
        if int(self.dimension) <= 0:
            raise ValueError("dimension must be positive")
        if self.dtype != tf.float64:
            raise ValueError("IdentityCoordinateMap requires tf.float64")

    def forward(self, reference_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        points = _as_matrix(reference_points, int(self.dimension), "reference_points")
        return points, tf.zeros([tf.shape(points)[0]], dtype=tf.float64)

    def inverse(self, physical_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        points = _as_matrix(physical_points, int(self.dimension), "physical_points")
        return points, tf.zeros([tf.shape(points)[0]], dtype=tf.float64)

    def manifest_payload(self) -> Mapping[str, object]:
        return {"family": "IdentityCoordinateMap", "dimension": int(self.dimension)}


@dataclass(frozen=True)
class AffineCoordinateMap:
    """Affine map ``r = offset + reference_points @ matrix.T``."""

    offset: tf.Tensor
    matrix: tf.Tensor

    def __post_init__(self) -> None:
        offset = tf.convert_to_tensor(self.offset, dtype=tf.float64)
        matrix = tf.convert_to_tensor(self.matrix, dtype=tf.float64)
        if offset.shape.rank != 1 or matrix.shape.rank != 2:
            raise ValueError(f"AffineCoordinateMap: {HighDimStatus.INVALID_SHAPE.value}")
        if matrix.shape[0] != matrix.shape[1] or matrix.shape[0] != offset.shape[0]:
            raise ValueError(f"AffineCoordinateMap: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.reduce_all(tf.math.is_finite(offset)).numpy()
            and tf.reduce_all(tf.math.is_finite(matrix)).numpy()
        ):
            raise ValueError(f"AffineCoordinateMap: {HighDimStatus.NONFINITE_VALUE.value}")
        det = tf.linalg.det(matrix)
        if not bool(tf.math.is_finite(det).numpy()) or bool((tf.abs(det) <= 0.0).numpy()):
            raise ValueError(f"AffineCoordinateMap: {HighDimStatus.NONFINITE_VALUE.value}")
        object.__setattr__(self, "offset", offset)
        object.__setattr__(self, "matrix", matrix)

    @property
    def dimension(self) -> int:
        return int(self.offset.shape[0])

    def forward(self, reference_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        points = _as_matrix(reference_points, self.dimension, "reference_points")
        physical = self.offset[tf.newaxis, :] + tf.linalg.matmul(
            points,
            self.matrix,
            transpose_b=True,
        )
        return physical, tf.fill([tf.shape(points)[0]], self.log_abs_det())

    def inverse(self, physical_points: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        points = _as_matrix(physical_points, self.dimension, "physical_points")
        shifted = points - self.offset[tf.newaxis, :]
        reference = tf.linalg.matrix_transpose(
            tf.linalg.solve(self.matrix, tf.linalg.matrix_transpose(shifted))
        )
        return reference, tf.fill([tf.shape(points)[0]], -self.log_abs_det())

    def log_abs_det(self) -> tf.Tensor:
        return tf.math.log(tf.abs(tf.linalg.det(self.matrix)))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "AffineCoordinateMap",
            "offset": self.offset,
            "matrix": self.matrix,
        }


@dataclass(frozen=True)
class FixedBranchFilterConfig:
    """Declared deterministic value-path configuration for Phase 4."""

    fit_config: object | None
    density_tau: float
    normalizer_floor: float
    denominator_floor: float
    retained_storage_byte_budget: int
    coordinate_maps: tuple[HighDimCoordinateMap, ...]
    measure_convention: MeasureConvention
    deterministic_seed: int | str
    dtype: tf.DType = tf.float64
    product_basis: ProductBasis | None = None
    initial_cores: tuple[TTCore, ...] | None = None
    fit_quadrature_order: int = 48

    def __post_init__(self) -> None:
        if self.dtype != tf.float64:
            raise ValueError("FixedBranchFilterConfig requires tf.float64")
        assert_density_matches_mass(self.measure_convention)
        if int(self.retained_storage_byte_budget) <= 0:
            raise ValueError("retained_storage_byte_budget must be positive")
        for name in ("density_tau", "normalizer_floor", "denominator_floor"):
            value = tf.convert_to_tensor(getattr(self, name), dtype=tf.float64)
            if not bool(tf.math.is_finite(value).numpy()) or bool((value < 0.0).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
            object.__setattr__(self, name, float(value.numpy()))
        object.__setattr__(self, "coordinate_maps", tuple(self.coordinate_maps))
        if self.fit_config is not None and not isinstance(self.fit_config, FixedTTFitConfig):
            raise TypeError("fit_config must be a FixedTTFitConfig or None")
        if self.product_basis is not None:
            if not isinstance(self.product_basis, ProductBasis):
                raise TypeError("product_basis must be a ProductBasis or None")
            if self.product_basis.convention != self.measure_convention:
                raise ValueError(f"product_basis: {HighDimStatus.MEASURE_MISMATCH.value}")
        if self.initial_cores is not None:
            object.__setattr__(
                self,
                "initial_cores",
                tuple(core if isinstance(core, TTCore) else TTCore(core) for core in self.initial_cores),
            )
        if int(self.fit_quadrature_order) < 2:
            raise ValueError("fit_quadrature_order must be at least 2")
        object.__setattr__(self, "fit_quadrature_order", int(self.fit_quadrature_order))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "fit_config": str(type(self.fit_config).__name__) if self.fit_config is not None else "none",
            "density_tau": float(self.density_tau),
            "normalizer_floor": float(self.normalizer_floor),
            "denominator_floor": float(self.denominator_floor),
            "retained_storage_byte_budget": int(self.retained_storage_byte_budget),
            "coordinate_maps": tuple(coord.manifest_payload() for coord in self.coordinate_maps),
            "measure_convention": _measure_convention_payload(self.measure_convention),
            "deterministic_seed": self.deterministic_seed,
            "dtype": self.dtype.name,
            "product_basis": _product_basis_payload(self.product_basis),
            "initial_cores_hash": _core_values_hash(self.initial_cores),
            "fit_quadrature_order": int(self.fit_quadrature_order),
        }


@dataclass(frozen=True)
class RetainedFilter:
    """Retained filtering marginal and metadata for the next target."""

    density: SquaredTTDensity | object | None
    retained_axes: tuple[int, ...]
    retained_coordinate_names: tuple[str, ...]
    measure_convention: MeasureConvention
    normalizer: tf.Tensor
    branch_identity: BranchIdentity
    storage_kind: str
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        assert_density_matches_mass(self.measure_convention)
        normalizer = tf.convert_to_tensor(self.normalizer, dtype=tf.float64)
        if normalizer.shape.rank != 0:
            raise ValueError(f"normalizer: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.math.is_finite(normalizer).numpy()) or bool((normalizer <= 0.0).numpy()):
            raise ValueError(HighDimStatus.NORMALIZER_FLOOR_EXCEEDED.value)
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be a BranchIdentity")
        if len(self.retained_axes) != len(self.retained_coordinate_names):
            raise ValueError(f"retained axes: {HighDimStatus.INVALID_SHAPE.value}")
        if not str(self.storage_kind).strip():
            raise ValueError("storage_kind must be nonempty")
        object.__setattr__(self, "normalizer", normalizer)
        object.__setattr__(self, "retained_axes", tuple(int(axis) for axis in self.retained_axes))
        object.__setattr__(
            self,
            "retained_coordinate_names",
            tuple(str(name) for name in self.retained_coordinate_names),
        )
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class AdjacentTargetBatch:
    """Fixed sample target values for one adjacent filtering block."""

    time_index: int
    physical_points: tf.Tensor
    reference_points: tf.Tensor
    log_target: tf.Tensor
    sqrt_target: tf.Tensor
    weights: tf.Tensor
    measure_convention: MeasureConvention
    retained_filter_hash: str | None

    def __post_init__(self) -> None:
        physical = tf.convert_to_tensor(self.physical_points, dtype=tf.float64)
        reference = tf.convert_to_tensor(self.reference_points, dtype=tf.float64)
        log_target = tf.convert_to_tensor(self.log_target, dtype=tf.float64)
        sqrt_target = tf.convert_to_tensor(self.sqrt_target, dtype=tf.float64)
        weights = tf.convert_to_tensor(self.weights, dtype=tf.float64)
        if physical.shape.rank != 2 or reference.shape.rank != 2:
            raise ValueError(f"AdjacentTargetBatch: {HighDimStatus.INVALID_SHAPE.value}")
        n_rows = int(physical.shape[0])
        if reference.shape[0] != n_rows or log_target.shape != (n_rows,) or sqrt_target.shape != (n_rows,) or weights.shape != (n_rows,):
            raise ValueError(f"AdjacentTargetBatch: {HighDimStatus.INVALID_SHAPE.value}")
        for name, value in (
            ("physical_points", physical),
            ("reference_points", reference),
            ("log_target", log_target),
            ("sqrt_target", sqrt_target),
            ("weights", weights),
        ):
            assert_tf_float64(name, value)
            if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        if bool(tf.reduce_any(weights < 0.0).numpy()):
            raise ValueError(f"weights: {HighDimStatus.NONFINITE_VALUE.value}")
        object.__setattr__(self, "physical_points", physical)
        object.__setattr__(self, "reference_points", reference)
        object.__setattr__(self, "log_target", log_target)
        object.__setattr__(self, "sqrt_target", sqrt_target)
        object.__setattr__(self, "weights", weights)


@dataclass(frozen=True)
class ScalarAdjacentTargetBuildResult:
    """Built scalar adjacent-target batch with replayable construction metadata."""

    target_batch: AdjacentTargetBatch
    branch_identity: BranchIdentity
    status: HighDimStatus
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target_batch, AdjacentTargetBatch):
            raise TypeError("target_batch must be an AdjacentTargetBatch")
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be a BranchIdentity")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class MultistateAdjacentTargetBuildResult:
    """Built multistate adjacent-target batch with replayable metadata."""

    target_batch: AdjacentTargetBatch
    branch_identity: BranchIdentity
    status: HighDimStatus
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target_batch, AdjacentTargetBatch):
            raise TypeError("target_batch must be an AdjacentTargetBatch")
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be a BranchIdentity")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class FixedBranchFilterStepResult:
    """One deterministic filtering value-path step."""

    time_index: int
    fit_result: object | None
    density: object | None
    log_normalizer: tf.Tensor
    retained_filter: RetainedFilter
    branch_identity: BranchIdentity
    status: HighDimStatus
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        log_normalizer = tf.convert_to_tensor(self.log_normalizer, dtype=tf.float64)
        if log_normalizer.shape.rank != 0:
            raise ValueError(f"log_normalizer: {HighDimStatus.INVALID_SHAPE.value}")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        object.__setattr__(self, "log_normalizer", log_normalizer)
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class FixedBranchFilterResult:
    """Full deterministic filtering value-path result."""

    log_likelihood: tf.Tensor
    retained_filter: RetainedFilter
    steps: tuple[FixedBranchFilterStepResult, ...]
    branch_identity: BranchIdentity
    status: HighDimStatus
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        log_likelihood = tf.convert_to_tensor(self.log_likelihood, dtype=tf.float64)
        if log_likelihood.shape.rank != 0:
            raise ValueError(f"log_likelihood: {HighDimStatus.INVALID_SHAPE.value}")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        object.__setattr__(self, "log_likelihood", log_likelihood)
        object.__setattr__(self, "steps", tuple(self.steps))
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


class FixedBranchSquaredTTFilter:
    """Phase-4 deterministic value path with retained-filter branch identity."""

    def __init__(self, config: FixedBranchFilterConfig) -> None:
        if not isinstance(config, FixedBranchFilterConfig):
            raise TypeError("config must be a FixedBranchFilterConfig")
        self.config = config

    def log_likelihood(
        self,
        model: TFHighDimStateSpaceModel,
        theta: tf.Tensor,
        observations: tf.Tensor,
        initial_branch: BranchIdentity | None = None,
    ) -> FixedBranchFilterResult:
        if initial_branch is not None and not isinstance(initial_branch, BranchIdentity):
            raise TypeError("initial_branch must be a BranchIdentity")
        if isinstance(model, LinearGaussianSSM):
            return self._linear_gaussian_value_path(model, theta, observations, initial_branch)
        return self._scalar_nonlinear_dense_value_path(model, theta, observations, initial_branch)

    def _scalar_nonlinear_dense_value_path(
        self,
        model: TFHighDimStateSpaceModel,
        theta: tf.Tensor,
        observations: tf.Tensor,
        initial_branch: BranchIdentity | None,
    ) -> FixedBranchFilterResult:
        if int(model.state_dim()) != 1:
            raise TypeError("scalar nonlinear dense value path requires state_dim == 1")
        if self.config.fit_config is not None or self.config.product_basis is not None:
            raise TypeError("scalar nonlinear dense value path is value-only and does not fit TT artifacts")
        theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
        observation_matrix = _as_observation_matrix(observations, int(model.observation_dim()))
        reference_points, weights, physical_points, log_abs_det = self._scalar_dense_reference_grid()
        x_grid = physical_points[:, 0]
        steps: list[FixedBranchFilterStepResult] = []
        log_terms = []
        log_posterior_physical: tf.Tensor | None = None
        retained: RetainedFilter | None = None
        previous_step_hash: str | None = None
        for time_index in range(int(observation_matrix.shape[0])):
            if time_index == 0:
                log_unnormalized_physical = model.initial_log_density(
                    theta_vector,
                    physical_points,
                ) + model.observation_log_density(
                    theta_vector,
                    physical_points,
                    observation_matrix[time_index],
                    t=time_index,
                )
            else:
                if log_posterior_physical is None:
                    raise RuntimeError("missing retained scalar dense posterior")
                transition_log = _scalar_pairwise_transition_log_density(
                    model=model,
                    theta=theta_vector,
                    physical_points=physical_points,
                    t=time_index,
                )
                predictive_log_terms = (
                    tf.math.log(weights)[tf.newaxis, :]
                    + log_abs_det[tf.newaxis, :]
                    + log_posterior_physical[tf.newaxis, :]
                    + transition_log
                )
                log_predictive = tf.reduce_logsumexp(predictive_log_terms, axis=1)
                log_unnormalized_physical = log_predictive + model.observation_log_density(
                    theta_vector,
                    physical_points,
                    observation_matrix[time_index],
                    t=time_index,
                )
            log_unnormalized_reference = log_unnormalized_physical + log_abs_det
            log_increment = _logsumexp_weighted(log_unnormalized_reference, weights)
            log_posterior_physical = log_unnormalized_physical - log_increment
            mean, variance = _scalar_grid_moments(
                x_grid=x_grid,
                weights=weights,
                log_abs_det=log_abs_det,
                log_density_physical=log_posterior_physical,
            )
            retained = scalar_dense_retained_filter(
                physical_points=physical_points,
                reference_points=reference_points,
                weights=weights,
                log_density_physical=log_posterior_physical,
                mean=mean,
                variance=variance,
                retained_axes=tuple(range(int(model.parameter_dim()), int(model.parameter_dim()) + 1)),
                retained_coordinate_names=("x0",),
                measure_convention=self.config.measure_convention,
                normalizer=tf.exp(log_increment),
                storage_byte_budget=self.config.retained_storage_byte_budget,
                stage=f"time_{time_index}",
            )
            step_manifest = BranchManifest(
                version="fixed_branch_scalar_nonlinear_filter_step.v1",
                payload={
                    "time_index": time_index,
                    "model": model.manifest_payload(),
                    "theta": theta_vector,
                    "observation": observation_matrix[time_index],
                    "log_normalizer": log_increment,
                    "retained_filter_hash": retained.branch_identity.hash.value,
                    "previous_step_hash": previous_step_hash,
                    "grid": _scalar_grid_payload(reference_points, weights, physical_points, log_abs_det),
                    "config": self.config.manifest_payload(),
                    "initial_branch": initial_branch.hash.value if initial_branch is not None else None,
                },
            )
            step_identity = BranchIdentity(manifest=step_manifest, hash=step_manifest.sha256())
            previous_step_hash = step_identity.hash.value
            steps.append(
                FixedBranchFilterStepResult(
                    time_index=time_index,
                    fit_result=None,
                    density=None,
                    log_normalizer=log_increment,
                    retained_filter=retained,
                    branch_identity=step_identity,
                    status=HighDimStatus.OK,
                    diagnostics={
                        "value_path": "scalar_nonlinear_dense_quadrature_value_path",
                        "fixed_branch_only": True,
                        "tt_artifact_status": "not_requested",
                        "retained_mean": tf.reshape(mean, [1]),
                        "retained_covariance": tf.reshape(variance, [1, 1]),
                        "integration_grid_size": int(reference_points.shape[0]),
                        "integration_window": _scalar_window_from_grid(physical_points),
                    },
                )
            )
            log_terms.append(log_increment)
        if retained is None:
            raise ValueError("observations must contain at least one row")
        log_likelihood = tf.reduce_sum(tf.stack(log_terms))
        manifest = BranchManifest(
            version="fixed_branch_scalar_nonlinear_filter_result.v1",
            payload={
                "model": model.manifest_payload(),
                "theta": theta_vector,
                "observations": observation_matrix,
                "config": self.config.manifest_payload(),
                "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
                "retained_filter_hash": retained.branch_identity.hash.value,
                "log_likelihood": log_likelihood,
                "status": HighDimStatus.OK.value,
                "scope": "scalar_nonlinear_dense_value_path",
                "what_is_not_claimed": (
                    "tt_posterior_accuracy",
                    "adaptive_tt_cross",
                    "kr_transport_accuracy",
                    "derivative_correctness",
                    "large_scale_performance",
                    "zhao_cui_t1000_reproduction",
                ),
            },
        )
        branch_identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
        return FixedBranchFilterResult(
            log_likelihood=log_likelihood,
            retained_filter=retained,
            steps=tuple(steps),
            branch_identity=branch_identity,
            status=HighDimStatus.OK,
            diagnostics={
                "value_path": "scalar_nonlinear_dense_quadrature_value_path",
                "fixed_branch_only": True,
                "tt_artifacts_present": False,
                "integration_grid_size": int(reference_points.shape[0]),
                "integration_window": _scalar_window_from_grid(physical_points),
            },
        )

    def _linear_gaussian_value_path(
        self,
        model: LinearGaussianSSM,
        theta: tf.Tensor,
        observations: tf.Tensor,
        initial_branch: BranchIdentity | None,
    ) -> FixedBranchFilterResult:
        theta_tensor = tf.convert_to_tensor(theta, dtype=tf.float64)
        if theta_tensor.shape.rank == 1:
            theta_tensor = theta_tensor[tf.newaxis, :]
        if theta_tensor.shape.rank != 2 or theta_tensor.shape[1] != model.parameter_dim():
            raise ValueError(f"theta: {HighDimStatus.INVALID_SHAPE.value}")
        observation_matrix = _as_observation_matrix(observations, model.observation_dim())
        mean = model.initial_mean
        covariance = model.initial_covariance
        steps: list[FixedBranchFilterStepResult] = []
        log_terms = []
        for time_index in range(int(observation_matrix.shape[0])):
            if time_index > 0:
                mean = model.transition_offset + tf.linalg.matvec(model.transition_matrix, mean)
                covariance = _symmetrize(
                    model.transition_matrix @ covariance @ tf.transpose(model.transition_matrix)
                    + model.transition_covariance
                )
            innovation = observation_matrix[time_index] - (
                model.observation_offset + tf.linalg.matvec(model.observation_matrix, mean)
            )
            innovation_covariance = _symmetrize(
                model.observation_matrix @ covariance @ tf.transpose(model.observation_matrix)
                + model.observation_covariance
            )
            log_increment = _mvn_log_prob(
                innovation[tf.newaxis, :],
                tf.zeros([1, model.observation_dim()], dtype=tf.float64),
                innovation_covariance,
            )[0]
            gain_rhs = covariance @ tf.transpose(model.observation_matrix)
            chol = tf.linalg.cholesky(innovation_covariance)
            kalman_gain = tf.transpose(tf.linalg.cholesky_solve(chol, tf.transpose(gain_rhs)))
            mean = mean + tf.linalg.matvec(kalman_gain, innovation)
            left = tf.eye(model.state_dim(), dtype=tf.float64) - kalman_gain @ model.observation_matrix
            covariance = _symmetrize(
                left @ covariance @ tf.transpose(left)
                + kalman_gain @ model.observation_covariance @ tf.transpose(kalman_gain)
            )
            tt_artifacts = self._fit_current_filtering_density_artifacts(
                time_index=time_index,
                mean=mean,
                covariance=covariance,
            )
            retained = gaussian_retained_filter(
                mean=mean,
                covariance=covariance,
                retained_axes=tuple(range(model.parameter_dim(), model.parameter_dim() + model.state_dim())),
                retained_coordinate_names=tuple(f"x{axis}" for axis in range(model.state_dim())),
                measure_convention=self.config.measure_convention,
                normalizer=tf.exp(log_increment),
                storage_byte_budget=self.config.retained_storage_byte_budget,
                stage=f"time_{time_index}",
                density=tt_artifacts["density"],
                storage_kind=(
                    "gaussian_moment_plus_squared_tt_density"
                    if tt_artifacts["density"] is not None
                    else "gaussian_moment"
                ),
            )
            step_manifest = BranchManifest(
                version="fixed_branch_filter_step.v1",
                payload={
                    "time_index": time_index,
                    "model": model.manifest_payload(),
                    "observation": observation_matrix[time_index],
                    "log_normalizer": log_increment,
                    "retained_filter_hash": retained.branch_identity.hash.value,
                    "fit_result_hash": (
                        tt_artifacts["fit_result"].branch_identity.hash.value
                        if tt_artifacts["fit_result"] is not None
                        else None
                    ),
                    "density_hash": (
                        tt_artifacts["density"].branch_identity.hash.value
                        if tt_artifacts["density"] is not None
                        else None
                    ),
                    "config": self.config.manifest_payload(),
                    "initial_branch": initial_branch.hash.value if initial_branch is not None else None,
                },
            )
            step_identity = BranchIdentity(manifest=step_manifest, hash=step_manifest.sha256())
            steps.append(
                FixedBranchFilterStepResult(
                    time_index=time_index,
                    fit_result=tt_artifacts["fit_result"],
                    density=tt_artifacts["density"],
                    log_normalizer=log_increment,
                    retained_filter=retained,
                    branch_identity=step_identity,
                    status=HighDimStatus.OK,
                    diagnostics={
                        "value_path": "exact_linear_gaussian_phase4_gate",
                        "fixed_branch_only": True,
                        "tt_artifact_status": tt_artifacts["status"],
                        "tt_artifact_target": tt_artifacts["target"],
                        "tt_density_normalizer": tt_artifacts["density_normalizer"],
                        "adjacent_target_batch": tt_artifacts["target_batch"],
                        "retained_mean": mean,
                        "retained_covariance": covariance,
                    },
                )
            )
            log_terms.append(log_increment)
        log_likelihood = tf.reduce_sum(tf.stack(log_terms))
        manifest = BranchManifest(
            version="fixed_branch_filter_result.v1",
            payload={
                "model": model.manifest_payload(),
                "theta": theta_tensor,
                "observations": observation_matrix,
                "config": self.config.manifest_payload(),
                "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
                "retained_filter_hash": steps[-1].retained_filter.branch_identity.hash.value,
                "log_likelihood": log_likelihood,
                "status": HighDimStatus.OK.value,
                "scope": "phase4_exact_small_model_value_path",
                "what_is_not_claimed": (
                    "derivative_correctness",
                    "adaptive_tt_cross",
                    "dsge_readiness",
                    "large_scale_performance",
                ),
            },
        )
        branch_identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
        return FixedBranchFilterResult(
            log_likelihood=log_likelihood,
            retained_filter=steps[-1].retained_filter,
            steps=tuple(steps),
            branch_identity=branch_identity,
            status=HighDimStatus.OK,
            diagnostics={
                "value_path": "exact_linear_gaussian_phase4_gate",
                "p10_stage_sanity": HighDimStatus.STAGE_SANITY_ONLY.value,
                "fixed_branch_only": True,
                "tt_artifacts_present": all(step.density is not None for step in steps),
            },
        )

    def _fit_current_filtering_density_artifacts(
        self,
        time_index: int,
        mean: tf.Tensor,
        covariance: tf.Tensor,
    ) -> Mapping[str, object]:
        if self.config.fit_config is None and self.config.product_basis is None:
            return {
                "status": "not_requested",
                "target": "none",
                "target_batch": None,
                "fit_result": None,
                "density": None,
                "density_normalizer": None,
            }
        if self.config.fit_config is None or self.config.product_basis is None:
            raise ValueError(f"tt_artifacts: {HighDimStatus.INVALID_SHAPE.value}")
        product_basis = self.config.product_basis
        fit_config = self.config.fit_config
        if product_basis.dimension != int(mean.shape[0]):
            raise ValueError(f"product_basis: {HighDimStatus.INVALID_SHAPE.value}")
        reference_points, weights = _tensor_product_reference_quadrature(
            product_basis,
            self.config.fit_quadrature_order,
        )
        coordinate_map = self._coordinate_map_for_dimension(product_basis.dimension)
        physical_points, log_abs_det = coordinate_map.forward(reference_points)
        log_reference_weight = _log_uniform_reference_weight_density(product_basis)
        log_target = _gaussian_log_density(physical_points, mean, covariance)
        log_target = log_target + log_abs_det - log_reference_weight
        target_batch = build_adjacent_target_batch(
            time_index=time_index,
            physical_points=physical_points,
            reference_points=reference_points,
            log_target=log_target,
            weights=weights,
            measure_convention=self.config.measure_convention,
            retained_filter=None,
            expected_retained_axes=None,
        )
        initial_cores = self.config.initial_cores or _default_initial_cores(
            product_basis,
            fit_config,
        )
        fit_result = FixedTTFitter().fit(
            product_basis=product_basis,
            samples=FixedTTFitSampleBatch(
                points=target_batch.reference_points,
                target_values=target_batch.sqrt_target,
                weights=target_batch.weights,
            ),
            config=fit_config,
            initial_cores=initial_cores,
            branch_seed=f"{self.config.deterministic_seed}:time_{time_index}:current_filter",
            measure_convention=self.config.measure_convention,
        )
        if fit_result.status is not HighDimStatus.OK:
            raise ValueError(fit_result.status.value)
        defensive = TensorProductReferenceDensity(
            product_basis=product_basis,
            measure_convention=self.config.measure_convention,
        )
        tau = tf.constant(self.config.density_tau, dtype=tf.float64)
        normalizer_floor = tf.constant(self.config.normalizer_floor, dtype=tf.float64)
        denominator_floor = tf.constant(self.config.denominator_floor, dtype=tf.float64)
        density_identity = SquaredTTDensity.expected_branch_identity(
            sqrt_tt=fit_result.fitted_tt,
            defensive_density=defensive,
            tau=tau,
            normalizer_floor=normalizer_floor,
            denominator_floor=denominator_floor,
            measure_convention=self.config.measure_convention,
        )
        density = SquaredTTDensity(
            sqrt_tt=fit_result.fitted_tt,
            defensive_density=defensive,
            tau=tau,
            normalizer_floor=normalizer_floor,
            denominator_floor=denominator_floor,
            measure_convention=self.config.measure_convention,
            branch_identity=density_identity,
        )
        return {
            "status": HighDimStatus.OK.value,
            "target": "current_filtering_density_under_reference_measure",
            "target_batch": target_batch,
            "fit_result": fit_result,
            "density": density,
            "density_normalizer": density.normalizer(),
        }

    def _coordinate_map_for_dimension(self, dimension: int) -> HighDimCoordinateMap:
        return _coordinate_map_for_config(self.config, dimension)

    def _scalar_dense_reference_grid(
        self,
    ) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        nodes, weights = legendre_gauss_nodes_weights(self.config.fit_quadrature_order)
        reference_points = nodes[:, tf.newaxis]
        coordinate_map = self._coordinate_map_for_dimension(1)
        physical_points, log_abs_det = coordinate_map.forward(reference_points)
        if physical_points.shape[1] != 1:
            raise ValueError(f"coordinate_map: {HighDimStatus.INVALID_SHAPE.value}")
        return reference_points, weights, physical_points, log_abs_det


def scalar_nonlinear_fixed_design_tt_value_path(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observations: tf.Tensor,
    config: FixedBranchFilterConfig,
    *,
    fixture_id: str = "p37.m2p6c.sv.short-sequential-tt-value-path.v1",
    initial_target_id: str = "p37.m2p6c.sv.initial.t0.v1",
    transition_target_id: str = "p37.m2p6c.sv.transition.t1.tt-retained.v1",
    branch_seed_prefix: str = "p37-m2p6c-sv-short-tt",
    retained_moment_order: int = 257,
    retained_propagation_order: int = 321,
) -> FixedBranchFilterResult:
    """Run the M2.6c scalar fixed-design TT value path for two observations."""

    if not isinstance(config, FixedBranchFilterConfig):
        raise TypeError("config must be a FixedBranchFilterConfig")
    if int(model.state_dim()) != 1:
        raise TypeError("scalar nonlinear fixed-design TT value path requires state_dim == 1")
    if config.fit_config is None or config.product_basis is None:
        raise TypeError("scalar nonlinear fixed-design TT value path requires fit_config and product_basis")
    observation_matrix = _as_observation_matrix(observations, int(model.observation_dim()))
    if int(observation_matrix.shape[0]) != 2:
        raise ValueError("M2.6c scalar TT value path is pinned to exactly two observations")
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    product_basis = config.product_basis
    fit_config = config.fit_config
    coordinate_map = _coordinate_map_for_config(config, 1)
    initial_cores = config.initial_cores or _default_initial_cores(product_basis, fit_config)
    steps: list[FixedBranchFilterStepResult] = []
    retained: RetainedFilter | None = None
    previous_step_hash: str | None = None
    log_terms = []

    for time_index in range(2):
        if time_index == 0:
            target_result = scalar_nonlinear_initial_adjacent_target_batch(
                model=model,
                theta=theta_vector,
                observation=observation_matrix[time_index],
                product_basis=product_basis,
                coordinate_map=coordinate_map,
                quadrature_order=config.fit_quadrature_order,
                measure_convention=config.measure_convention,
                fixture_id=fixture_id,
                target_id=initial_target_id,
                branch_seed=f"{branch_seed_prefix}:t0:target",
                time_index=0,
            )
        else:
            if retained is None or retained.storage_kind != "scalar_tt_grid":
                raise ValueError("M2.6c transition requires scalar_tt_grid retained filter")
            target_result = scalar_nonlinear_transition_adjacent_target_batch(
                model=model,
                theta=theta_vector,
                observation=observation_matrix[time_index],
                retained_filter=retained,
                product_basis=product_basis,
                coordinate_map=coordinate_map,
                quadrature_order=config.fit_quadrature_order,
                measure_convention=config.measure_convention,
                fixture_id=fixture_id,
                target_id=transition_target_id,
                branch_seed=f"{branch_seed_prefix}:t1:target",
                time_index=1,
            )

        fit_result = FixedTTFitter().fit(
            product_basis=product_basis,
            samples=FixedTTFitSampleBatch(
                points=target_result.target_batch.reference_points,
                target_values=target_result.target_batch.sqrt_target,
                weights=target_result.target_batch.weights,
            ),
            config=fit_config,
            initial_cores=initial_cores,
            branch_seed=f"{branch_seed_prefix}:t{time_index}:fit",
            measure_convention=config.measure_convention,
        )
        if fit_result.status is not HighDimStatus.OK:
            raise ValueError(fit_result.status.value)

        density = _squared_density_from_fit_result(fit_result, product_basis, config)
        scaled_normalizer = density.normalizer()
        log_scale_shift = tf.convert_to_tensor(
            target_result.diagnostics["log_scale_shift"],
            dtype=tf.float64,
        )
        log_normalizer = tf.math.log(scaled_normalizer) + log_scale_shift
        moment_payload = _scalar_tt_retained_moments(
            density=density,
            coordinate_map=coordinate_map,
            order=retained_moment_order,
        )
        retained = _scalar_tt_grid_retained_from_density(
            density=density,
            coordinate_map=coordinate_map,
            order=retained_propagation_order,
            measure_convention=config.measure_convention,
            normalizer=tf.exp(log_normalizer),
            storage_byte_budget=config.retained_storage_byte_budget,
            stage=f"time_{time_index}",
            mean=moment_payload["mean"],
            variance=moment_payload["variance"],
        )
        step_manifest = BranchManifest(
            version="fixed_branch_scalar_tt_filter_step.v1",
            payload={
                "fixture_id": fixture_id,
                "time_index": int(time_index),
                "model": model.manifest_payload(),
                "theta": theta_vector,
                "observation": observation_matrix[time_index],
                "target_hash": target_result.branch_identity.hash.value,
                "fit_result_hash": fit_result.branch_identity.hash.value,
                "density_hash": density.branch_identity.hash.value,
                "retained_filter_hash": retained.branch_identity.hash.value,
                "previous_step_hash": previous_step_hash,
                "log_normalizer": log_normalizer,
                "scaled_normalizer": scaled_normalizer,
                "log_scale_shift": log_scale_shift,
                "config": config.manifest_payload(),
                "branch_seed_prefix": branch_seed_prefix,
                "value_path": "scalar_nonlinear_fixed_design_tt_value_path",
                "what_is_not_claimed": (
                    "adaptive_tt_cross",
                    "zhao_cui_t1000_reproduction",
                    "integrated_axis_marginalization",
                    "derivative_correctness",
                    "hmc_or_dsge_readiness",
                    "gpu_readiness",
                    "high_dimensional_scalability",
                ),
            },
        )
        step_identity = BranchIdentity(manifest=step_manifest, hash=step_manifest.sha256())
        previous_step_hash = step_identity.hash.value
        steps.append(
            FixedBranchFilterStepResult(
                time_index=time_index,
                fit_result=fit_result,
                density=density,
                log_normalizer=log_normalizer,
                retained_filter=retained,
                branch_identity=step_identity,
                status=HighDimStatus.OK,
                diagnostics={
                    "value_path": "scalar_nonlinear_fixed_design_tt_value_path",
                    "tt_artifacts_present": True,
                    "target_hash": target_result.branch_identity.hash.value,
                    "target_id": target_result.diagnostics["target_id"],
                    "fit_result_hash": fit_result.branch_identity.hash.value,
                    "density_hash": density.branch_identity.hash.value,
                    "retained_filter_hash": retained.branch_identity.hash.value,
                    "scaled_normalizer": scaled_normalizer,
                    "log_scale_shift": log_scale_shift,
                    "retained_mean": tf.reshape(moment_payload["mean"], [1]),
                    "retained_covariance": tf.reshape(moment_payload["variance"], [1, 1]),
                    "retained_variance": moment_payload["variance"],
                    "retained_moment_mass": moment_payload["mass"],
                    "retained_moment_order": int(retained_moment_order),
                    "retained_propagation_order": int(retained_propagation_order),
                    "target_batch": target_result.target_batch,
                },
            )
        )
        log_terms.append(log_normalizer)

    if retained is None:
        raise RuntimeError("missing final retained filter")
    log_likelihood = tf.reduce_sum(tf.stack(log_terms))
    manifest = BranchManifest(
        version="fixed_branch_scalar_tt_filter_result.v1",
        payload={
            "fixture_id": fixture_id,
            "model": model.manifest_payload(),
            "theta": theta_vector,
            "observations": observation_matrix,
            "config": config.manifest_payload(),
            "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
            "retained_filter_hash": retained.branch_identity.hash.value,
            "log_likelihood": log_likelihood,
            "status": HighDimStatus.OK.value,
            "scope": "p37_m2p6c_scalar_nonlinear_fixed_design_tt_value_path",
            "value_path": "scalar_nonlinear_fixed_design_tt_value_path",
            "what_is_not_claimed": (
                "adaptive_tt_cross",
                "zhao_cui_t1000_reproduction",
                "smc_or_real_data_validation",
                "derivative_correctness",
                "hmc_or_dsge_readiness",
                "gpu_readiness",
                "high_dimensional_scalability",
            ),
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return FixedBranchFilterResult(
        log_likelihood=log_likelihood,
        retained_filter=retained,
        steps=tuple(steps),
        branch_identity=identity,
        status=HighDimStatus.OK,
        diagnostics={
            "value_path": "scalar_nonlinear_fixed_design_tt_value_path",
            "tt_artifacts_present": True,
            "fixture_id": fixture_id,
            "promoted_horizon": 2,
            "retained_storage_kind": retained.storage_kind,
            "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
        },
    )


def multistate_nonlinear_fixed_design_tt_value_path(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observations: tf.Tensor,
    config: FixedBranchFilterConfig,
    *,
    fixture_id: str = "p46.multistate-nonlinear-fixed-design-tt-value-path.v1",
    initial_target_id: str = "p46.multistate.initial.t0.v1",
    transition_target_id: str = "p46.multistate.transition.tt-retained.v1",
    branch_seed_prefix: str = "p46-multistate-nonlinear-tt",
    retained_moment_order: int | None = None,
    retained_propagation_order: int | None = None,
) -> FixedBranchFilterResult:
    """Run a tiny multistate fixed-design TT nonlinear filtering value path.

    This P46 adapter retains all state axes on a deterministic tensor-product
    grid after each TT fit.  It is intentionally bounded to small reviewed
    targets; it is not adaptive TT-cross, SIRT, or a paper-scale Zhao--Cui
    reproduction.
    """

    if not isinstance(config, FixedBranchFilterConfig):
        raise TypeError("config must be a FixedBranchFilterConfig")
    if config.fit_config is None or config.product_basis is None:
        raise TypeError("multistate nonlinear fixed-design TT value path requires fit_config and product_basis")
    state_dim = int(model.state_dim())
    if state_dim <= 1:
        raise TypeError("multistate nonlinear fixed-design TT value path requires state_dim > 1")
    product_basis = config.product_basis
    if int(product_basis.dimension) != state_dim:
        raise ValueError(f"product_basis: {HighDimStatus.INVALID_SHAPE.value}")
    if product_basis.convention != config.measure_convention:
        raise ValueError(f"product_basis: {HighDimStatus.MEASURE_MISMATCH.value}")
    observation_matrix = _as_observation_matrix(observations, int(model.observation_dim()))
    if int(observation_matrix.shape[0]) < 1:
        raise ValueError("observations must contain at least one row")
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    fit_config = config.fit_config
    coordinate_map = _coordinate_map_for_config(config, state_dim)
    initial_cores = config.initial_cores or _default_initial_cores(product_basis, fit_config)
    moment_order = int(retained_moment_order or config.fit_quadrature_order)
    propagation_order = int(retained_propagation_order or config.fit_quadrature_order)
    if moment_order < 2 or propagation_order < 2:
        raise ValueError("retained quadrature orders must be at least 2")

    steps: list[FixedBranchFilterStepResult] = []
    retained: RetainedFilter | None = None
    previous_step_hash: str | None = None
    log_terms = []

    for time_index in range(int(observation_matrix.shape[0])):
        if time_index == 0:
            target_result = multistate_nonlinear_initial_adjacent_target_batch(
                model=model,
                theta=theta_vector,
                observation=observation_matrix[time_index],
                product_basis=product_basis,
                coordinate_map=coordinate_map,
                quadrature_order=config.fit_quadrature_order,
                measure_convention=config.measure_convention,
                fixture_id=fixture_id,
                target_id=initial_target_id,
                branch_seed=f"{branch_seed_prefix}:t0:target",
                time_index=0,
            )
        else:
            if retained is None or retained.storage_kind != "multistate_tt_grid":
                raise ValueError("multistate transition requires multistate_tt_grid retained filter")
            target_result = multistate_nonlinear_transition_adjacent_target_batch(
                model=model,
                theta=theta_vector,
                observation=observation_matrix[time_index],
                retained_filter=retained,
                product_basis=product_basis,
                coordinate_map=coordinate_map,
                quadrature_order=config.fit_quadrature_order,
                measure_convention=config.measure_convention,
                fixture_id=fixture_id,
                target_id=transition_target_id,
                branch_seed=f"{branch_seed_prefix}:t{time_index}:target",
                time_index=time_index,
            )

        fit_result = FixedTTFitter().fit(
            product_basis=product_basis,
            samples=FixedTTFitSampleBatch(
                points=target_result.target_batch.reference_points,
                target_values=target_result.target_batch.sqrt_target,
                weights=target_result.target_batch.weights,
            ),
            config=fit_config,
            initial_cores=initial_cores,
            branch_seed=f"{branch_seed_prefix}:t{time_index}:fit",
            measure_convention=config.measure_convention,
        )
        if fit_result.status is not HighDimStatus.OK:
            raise ValueError(fit_result.status.value)

        density = _squared_density_from_fit_result(fit_result, product_basis, config)
        scaled_normalizer = density.normalizer()
        log_scale_shift = tf.convert_to_tensor(
            target_result.diagnostics["log_scale_shift"],
            dtype=tf.float64,
        )
        log_normalizer = tf.math.log(scaled_normalizer) + log_scale_shift
        moment_payload = _multistate_tt_retained_moments(
            density=density,
            coordinate_map=coordinate_map,
            order=moment_order,
        )
        retained = _multistate_tt_grid_retained_from_density(
            density=density,
            coordinate_map=coordinate_map,
            order=propagation_order,
            measure_convention=config.measure_convention,
            normalizer=tf.exp(log_normalizer),
            storage_byte_budget=config.retained_storage_byte_budget,
            stage=f"time_{time_index}",
            mean=moment_payload["mean"],
            covariance=moment_payload["covariance"],
        )
        step_manifest = BranchManifest(
            version="fixed_branch_multistate_tt_filter_step.v1",
            payload={
                "fixture_id": fixture_id,
                "time_index": int(time_index),
                "state_dim": state_dim,
                "model": model.manifest_payload(),
                "theta": theta_vector,
                "observation": observation_matrix[time_index],
                "target_hash": target_result.branch_identity.hash.value,
                "fit_result_hash": fit_result.branch_identity.hash.value,
                "density_hash": density.branch_identity.hash.value,
                "retained_filter_hash": retained.branch_identity.hash.value,
                "previous_step_hash": previous_step_hash,
                "log_normalizer": log_normalizer,
                "scaled_normalizer": scaled_normalizer,
                "log_scale_shift": log_scale_shift,
                "config": config.manifest_payload(),
                "branch_seed_prefix": branch_seed_prefix,
                "value_path": "multistate_nonlinear_fixed_design_tt_value_path",
                "what_is_not_claimed": (
                    "adaptive_tt_cross",
                    "zhao_cui_t1000_reproduction",
                    "integrated_axis_marginalization",
                    "derivative_correctness",
                    "hmc_or_dsge_readiness",
                    "gpu_readiness",
                    "high_dimensional_scalability",
                ),
            },
        )
        step_identity = BranchIdentity(manifest=step_manifest, hash=step_manifest.sha256())
        previous_step_hash = step_identity.hash.value
        steps.append(
            FixedBranchFilterStepResult(
                time_index=time_index,
                fit_result=fit_result,
                density=density,
                log_normalizer=log_normalizer,
                retained_filter=retained,
                branch_identity=step_identity,
                status=HighDimStatus.OK,
                diagnostics={
                    "value_path": "multistate_nonlinear_fixed_design_tt_value_path",
                    "tt_artifacts_present": True,
                    "target_hash": target_result.branch_identity.hash.value,
                    "target_id": target_result.diagnostics["target_id"],
                    "fit_result_hash": fit_result.branch_identity.hash.value,
                    "density_hash": density.branch_identity.hash.value,
                    "retained_filter_hash": retained.branch_identity.hash.value,
                    "scaled_normalizer": scaled_normalizer,
                    "log_scale_shift": log_scale_shift,
                    "retained_mean": moment_payload["mean"],
                    "retained_covariance": moment_payload["covariance"],
                    "retained_moment_mass": moment_payload["mass"],
                    "retained_moment_order": moment_order,
                    "retained_propagation_order": propagation_order,
                    "target_batch": target_result.target_batch,
                },
            )
        )
        log_terms.append(log_normalizer)

    if retained is None:
        raise RuntimeError("missing final retained filter")
    log_likelihood = tf.reduce_sum(tf.stack(log_terms))
    manifest = BranchManifest(
        version="fixed_branch_multistate_tt_filter_result.v1",
        payload={
            "fixture_id": fixture_id,
            "model": model.manifest_payload(),
            "theta": theta_vector,
            "observations": observation_matrix,
            "config": config.manifest_payload(),
            "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
            "retained_filter_hash": retained.branch_identity.hash.value,
            "log_likelihood": log_likelihood,
            "status": HighDimStatus.OK.value,
            "scope": "p46_multistate_nonlinear_fixed_design_tt_value_path",
            "value_path": "multistate_nonlinear_fixed_design_tt_value_path",
            "what_is_not_claimed": (
                "adaptive_tt_cross",
                "zhao_cui_t1000_reproduction",
                "smc_or_real_data_validation",
                "derivative_correctness",
                "hmc_or_dsge_readiness",
                "gpu_readiness",
                "high_dimensional_scalability",
            ),
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return FixedBranchFilterResult(
        log_likelihood=log_likelihood,
        retained_filter=retained,
        steps=tuple(steps),
        branch_identity=identity,
        status=HighDimStatus.OK,
        diagnostics={
            "value_path": "multistate_nonlinear_fixed_design_tt_value_path",
            "tt_artifacts_present": True,
            "fixture_id": fixture_id,
            "promoted_horizon": int(observation_matrix.shape[0]),
            "state_dim": state_dim,
            "retained_storage_kind": retained.storage_kind,
            "step_hashes": tuple(step.branch_identity.hash.value for step in steps),
            "what_is_not_claimed": (
                "adaptive_tt_cross",
                "zhao_cui_t1000_reproduction",
                "integrated_axis_marginalization",
                "derivative_correctness",
                "hmc_or_dsge_readiness",
                "high_dimensional_scalability",
            ),
        },
    )


def gaussian_retained_filter(
    mean: tf.Tensor,
    covariance: tf.Tensor,
    retained_axes: Sequence[int],
    retained_coordinate_names: Sequence[str],
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
    density: SquaredTTDensity | None = None,
    storage_kind: str = "gaussian_moment",
) -> RetainedFilter:
    mean = tf.convert_to_tensor(mean, dtype=tf.float64)
    covariance = _symmetrize(tf.convert_to_tensor(covariance, dtype=tf.float64))
    estimated_bytes = (int(mean.shape[0]) + int(covariance.shape[0]) * int(covariance.shape[1])) * tf.float64.size
    if estimated_bytes > int(storage_byte_budget):
        raise ValueError(HighDimStatus.RETAINED_STORAGE_BUDGET_EXCEEDED.value)
    manifest = BranchManifest(
        version="retained_filter_gaussian.v1",
        payload={
            "stage": stage,
            "storage_kind": "gaussian_moment",
            "mean": mean,
            "covariance": covariance,
            "retained_axes": tuple(int(axis) for axis in retained_axes),
            "retained_coordinate_names": tuple(str(name) for name in retained_coordinate_names),
            "measure_convention": _measure_convention_payload(measure_convention),
            "normalizer": normalizer,
            "density_hash": density.branch_identity.hash.value if density is not None else None,
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return RetainedFilter(
        density=density,
        retained_axes=tuple(int(axis) for axis in retained_axes),
        retained_coordinate_names=tuple(str(name) for name in retained_coordinate_names),
        measure_convention=measure_convention,
        normalizer=normalizer,
        branch_identity=identity,
        storage_kind=storage_kind,
        diagnostics={
            "mean": mean,
            "covariance": covariance,
            "estimated_storage_bytes": estimated_bytes,
            "density_hash": density.branch_identity.hash.value if density is not None else None,
        },
    )


def scalar_dense_retained_filter(
    physical_points: tf.Tensor,
    reference_points: tf.Tensor,
    weights: tf.Tensor,
    log_density_physical: tf.Tensor,
    mean: tf.Tensor,
    variance: tf.Tensor,
    retained_axes: Sequence[int],
    retained_coordinate_names: Sequence[str],
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
) -> RetainedFilter:
    physical = _as_matrix(physical_points, 1, "physical_points")
    reference = _as_matrix(reference_points, 1, "reference_points")
    weights_tensor = tf.convert_to_tensor(weights, dtype=tf.float64)
    log_density = tf.convert_to_tensor(log_density_physical, dtype=tf.float64)
    if weights_tensor.shape != (int(physical.shape[0]),) or log_density.shape != (int(physical.shape[0]),):
        raise ValueError(f"scalar_dense_retained_filter: {HighDimStatus.INVALID_SHAPE.value}")
    for name, value in (
        ("weights", weights_tensor),
        ("log_density_physical", log_density),
        ("mean", mean),
        ("variance", variance),
    ):
        assert_tf_float64(name, tf.convert_to_tensor(value, dtype=tf.float64))
        if not bool(tf.reduce_all(tf.math.is_finite(tf.convert_to_tensor(value, dtype=tf.float64))).numpy()):
            raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    if bool(tf.reduce_any(weights_tensor <= 0.0).numpy()) or bool((variance < 0.0).numpy()):
        raise ValueError(f"scalar_dense_retained_filter: {HighDimStatus.NONFINITE_VALUE.value}")
    estimated_bytes = (
        int(physical.shape[0]) * 4
        + 2
    ) * tf.float64.size
    if estimated_bytes > int(storage_byte_budget):
        raise ValueError(HighDimStatus.RETAINED_STORAGE_BUDGET_EXCEEDED.value)
    manifest = BranchManifest(
        version="retained_filter_scalar_dense_grid.v1",
        payload={
            "stage": stage,
            "storage_kind": "scalar_dense_grid",
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": mean,
            "variance": variance,
            "retained_axes": tuple(int(axis) for axis in retained_axes),
            "retained_coordinate_names": tuple(str(name) for name in retained_coordinate_names),
            "measure_convention": _measure_convention_payload(measure_convention),
            "normalizer": normalizer,
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return RetainedFilter(
        density=None,
        retained_axes=tuple(int(axis) for axis in retained_axes),
        retained_coordinate_names=tuple(str(name) for name in retained_coordinate_names),
        measure_convention=measure_convention,
        normalizer=normalizer,
        branch_identity=identity,
        storage_kind="scalar_dense_grid",
        diagnostics={
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": tf.reshape(mean, [1]),
            "covariance": tf.reshape(variance, [1, 1]),
            "variance": variance,
            "estimated_storage_bytes": estimated_bytes,
        },
    )


def multistate_tt_grid_retained_filter(
    physical_points: tf.Tensor,
    reference_points: tf.Tensor,
    weights: tf.Tensor,
    log_density_physical: tf.Tensor,
    mean: tf.Tensor,
    covariance: tf.Tensor,
    retained_axes: Sequence[int],
    retained_coordinate_names: Sequence[str],
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
    density: SquaredTTDensity,
) -> RetainedFilter:
    """Build an all-axes multistate retained grid generated by a squared TT density."""

    if not isinstance(density, SquaredTTDensity):
        raise TypeError("density must be a SquaredTTDensity")
    state_dim = int(density.sqrt_tt.product_basis.dimension)
    physical = _as_matrix(physical_points, state_dim, "physical_points")
    reference = _as_matrix(reference_points, state_dim, "reference_points")
    weights_tensor = tf.convert_to_tensor(weights, dtype=tf.float64)
    log_density = tf.convert_to_tensor(log_density_physical, dtype=tf.float64)
    mean_tensor = tf.convert_to_tensor(mean, dtype=tf.float64)
    covariance_tensor = _symmetrize(tf.convert_to_tensor(covariance, dtype=tf.float64))
    if weights_tensor.shape != (int(physical.shape[0]),) or log_density.shape != (int(physical.shape[0]),):
        raise ValueError(f"multistate_tt_grid_retained_filter: {HighDimStatus.INVALID_SHAPE.value}")
    if mean_tensor.shape != (state_dim,) or covariance_tensor.shape != (state_dim, state_dim):
        raise ValueError(f"multistate_tt_grid_retained_filter: {HighDimStatus.INVALID_SHAPE.value}")
    for name, value in (
        ("weights", weights_tensor),
        ("log_density_physical", log_density),
        ("mean", mean_tensor),
        ("covariance", covariance_tensor),
    ):
        assert_tf_float64(name, value)
        if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
            raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    if bool(tf.reduce_any(weights_tensor <= 0.0).numpy()):
        raise ValueError(f"multistate_tt_grid_retained_filter: {HighDimStatus.NONFINITE_VALUE.value}")
    estimated_bytes = (
        int(physical.shape[0]) * (state_dim * 2 + 2)
        + state_dim
        + state_dim * state_dim
    ) * tf.float64.size
    if estimated_bytes > int(storage_byte_budget):
        raise ValueError(HighDimStatus.RETAINED_STORAGE_BUDGET_EXCEEDED.value)
    density_hash = density.branch_identity.hash.value
    manifest = BranchManifest(
        version="retained_filter_multistate_tt_grid.v1",
        payload={
            "stage": stage,
            "storage_kind": "multistate_tt_grid",
            "state_dim": state_dim,
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": mean_tensor,
            "covariance": covariance_tensor,
            "retained_axes": tuple(int(axis) for axis in retained_axes),
            "retained_coordinate_names": tuple(str(name) for name in retained_coordinate_names),
            "measure_convention": _measure_convention_payload(measure_convention),
            "normalizer": normalizer,
            "density_hash": density_hash,
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return RetainedFilter(
        density=density,
        retained_axes=tuple(int(axis) for axis in retained_axes),
        retained_coordinate_names=tuple(str(name) for name in retained_coordinate_names),
        measure_convention=measure_convention,
        normalizer=normalizer,
        branch_identity=identity,
        storage_kind="multistate_tt_grid",
        diagnostics={
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": mean_tensor,
            "covariance": covariance_tensor,
            "density_hash": density_hash,
            "estimated_storage_bytes": estimated_bytes,
            "all_axes_retained": True,
        },
    )


def build_adjacent_target_batch(
    time_index: int,
    physical_points: tf.Tensor,
    reference_points: tf.Tensor,
    log_target: tf.Tensor,
    weights: tf.Tensor,
    measure_convention: MeasureConvention,
    retained_filter: RetainedFilter | None = None,
    expected_retained_axes: Sequence[int] | None = None,
    log_scale_shift: tf.Tensor | None = None,
) -> AdjacentTargetBatch:
    if retained_filter is not None:
        if retained_filter.measure_convention != measure_convention:
            raise ValueError(HighDimStatus.RETAINED_MEASURE_MISMATCH.value)
        if expected_retained_axes is not None and tuple(expected_retained_axes) != retained_filter.retained_axes:
            raise ValueError(HighDimStatus.RETAINED_AXES_MISMATCH.value)
    log_values = tf.convert_to_tensor(log_target, dtype=tf.float64)
    scale_shift = (
        tf.reduce_max(log_values)
        if log_scale_shift is None
        else tf.convert_to_tensor(log_scale_shift, dtype=tf.float64)
    )
    if scale_shift.shape.rank != 0:
        raise ValueError(f"log_scale_shift: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.math.is_finite(scale_shift).numpy()):
        raise ValueError(f"log_scale_shift: {HighDimStatus.NONFINITE_VALUE.value}")
    sqrt_target = tf.exp(0.5 * (log_values - scale_shift))
    return AdjacentTargetBatch(
        time_index=time_index,
        physical_points=physical_points,
        reference_points=reference_points,
        log_target=log_values,
        sqrt_target=sqrt_target,
        weights=weights,
        measure_convention=measure_convention,
        retained_filter_hash=retained_filter.branch_identity.hash.value if retained_filter is not None else None,
    )


def scalar_nonlinear_initial_adjacent_target_batch(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    quadrature_order: int,
    measure_convention: MeasureConvention,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None = None,
    time_index: int = 0,
) -> ScalarAdjacentTargetBuildResult:
    """Build a fixed scalar initial target batch in reference-measure coordinates."""

    _validate_scalar_adjacent_target_common(
        model=model,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        measure_convention=measure_convention,
        quadrature_order=quadrature_order,
        fixture_id=fixture_id,
        target_id=target_id,
    )
    if int(time_index) != 0:
        raise ValueError("initial adjacent target requires time_index == 0")
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    observation_vector = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64),
        [int(model.observation_dim())],
    )
    reference_points, weights = _tensor_product_reference_quadrature(
        product_basis,
        int(quadrature_order),
    )
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    log_reference_weight = _log_uniform_reference_weight_density(product_basis)
    log_physical_target = model.initial_log_density(
        theta_vector,
        physical_points,
    ) + model.observation_log_density(
        theta_vector,
        physical_points,
        observation_vector,
        t=int(time_index),
    )
    log_reference_target = log_physical_target + log_abs_det - log_reference_weight
    return _finalize_scalar_adjacent_target_result(
        target_kind="initial",
        model=model,
        theta=theta_vector,
        observation=observation_vector,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        reference_points=reference_points,
        physical_points=physical_points,
        log_abs_det=log_abs_det,
        weights=weights,
        log_reference_target=log_reference_target,
        measure_convention=measure_convention,
        retained_filter=None,
        fixture_id=fixture_id,
        target_id=target_id,
        branch_seed=branch_seed,
        log_scale_shift=log_scale_shift,
        time_index=int(time_index),
    )


def scalar_nonlinear_transition_adjacent_target_batch(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    retained_filter: RetainedFilter,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    quadrature_order: int,
    measure_convention: MeasureConvention,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None = None,
    time_index: int = 1,
) -> ScalarAdjacentTargetBuildResult:
    """Build a fixed scalar transition target using a scalar dense retained filter."""

    _validate_scalar_adjacent_target_common(
        model=model,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        measure_convention=measure_convention,
        quadrature_order=quadrature_order,
        fixture_id=fixture_id,
        target_id=target_id,
    )
    if int(time_index) <= 0:
        raise ValueError("transition adjacent target requires time_index > 0")
    if not isinstance(retained_filter, RetainedFilter):
        raise TypeError("retained_filter must be a RetainedFilter")
    if retained_filter.storage_kind not in ("scalar_dense_grid", "scalar_tt_grid"):
        raise ValueError("transition adjacent target requires scalar_dense_grid or scalar_tt_grid retained filter")
    if retained_filter.storage_kind == "scalar_tt_grid" and not retained_filter.diagnostics.get("density_hash"):
        raise ValueError("scalar_tt_grid transition target requires density_hash")
    if retained_filter.measure_convention != measure_convention:
        raise ValueError(HighDimStatus.RETAINED_MEASURE_MISMATCH.value)
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    observation_vector = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64),
        [int(model.observation_dim())],
    )
    reference_points, weights = _tensor_product_reference_quadrature(
        product_basis,
        int(quadrature_order),
    )
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    if retained_filter.storage_kind == "scalar_tt_grid":
        log_predictive = _scalar_tt_predictive_log_density_from_retained(
            model=model,
            theta=theta_vector,
            current_physical_points=physical_points,
            retained_filter=retained_filter,
            coordinate_map=coordinate_map,
            time_index=int(time_index),
        )
    else:
        log_predictive = _scalar_dense_predictive_log_density_from_retained(
            model=model,
            theta=theta_vector,
            current_physical_points=physical_points,
            retained_filter=retained_filter,
            coordinate_map=coordinate_map,
            time_index=int(time_index),
        )
    log_physical_target = log_predictive + model.observation_log_density(
        theta_vector,
        physical_points,
        observation_vector,
        t=int(time_index),
    )
    log_reference_weight = _log_uniform_reference_weight_density(product_basis)
    log_reference_target = log_physical_target + log_abs_det - log_reference_weight
    return _finalize_scalar_adjacent_target_result(
        target_kind="transition",
        model=model,
        theta=theta_vector,
        observation=observation_vector,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        reference_points=reference_points,
        physical_points=physical_points,
        log_abs_det=log_abs_det,
        weights=weights,
        log_reference_target=log_reference_target,
        measure_convention=measure_convention,
        retained_filter=retained_filter,
        fixture_id=fixture_id,
        target_id=target_id,
        branch_seed=branch_seed,
        log_scale_shift=log_scale_shift,
        time_index=int(time_index),
    )


def multistate_nonlinear_initial_adjacent_target_batch(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    quadrature_order: int,
    measure_convention: MeasureConvention,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None = None,
    time_index: int = 0,
) -> MultistateAdjacentTargetBuildResult:
    """Build a fixed multistate initial target batch in reference coordinates."""

    _validate_multistate_adjacent_target_common(
        model=model,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        measure_convention=measure_convention,
        quadrature_order=quadrature_order,
        fixture_id=fixture_id,
        target_id=target_id,
    )
    if int(time_index) != 0:
        raise ValueError("initial adjacent target requires time_index == 0")
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    observation_vector = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64),
        [int(model.observation_dim())],
    )
    reference_points, weights = _tensor_product_reference_quadrature(
        product_basis,
        int(quadrature_order),
    )
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    log_reference_weight = _log_uniform_reference_weight_density(product_basis)
    log_physical_target = model.initial_log_density(
        theta_vector,
        physical_points,
    ) + model.observation_log_density(
        theta_vector,
        physical_points,
        observation_vector,
        t=int(time_index),
    )
    log_reference_target = log_physical_target + log_abs_det - log_reference_weight
    return _finalize_multistate_adjacent_target_result(
        target_kind="initial",
        model=model,
        theta=theta_vector,
        observation=observation_vector,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        reference_points=reference_points,
        physical_points=physical_points,
        log_abs_det=log_abs_det,
        weights=weights,
        log_reference_target=log_reference_target,
        measure_convention=measure_convention,
        retained_filter=None,
        fixture_id=fixture_id,
        target_id=target_id,
        branch_seed=branch_seed,
        log_scale_shift=log_scale_shift,
        time_index=int(time_index),
    )


def multistate_nonlinear_transition_adjacent_target_batch(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    retained_filter: RetainedFilter,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    quadrature_order: int,
    measure_convention: MeasureConvention,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None = None,
    time_index: int = 1,
) -> MultistateAdjacentTargetBuildResult:
    """Build a fixed multistate transition target from an all-axes retained grid."""

    _validate_multistate_adjacent_target_common(
        model=model,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        measure_convention=measure_convention,
        quadrature_order=quadrature_order,
        fixture_id=fixture_id,
        target_id=target_id,
    )
    if int(time_index) <= 0:
        raise ValueError("transition adjacent target requires time_index > 0")
    if not isinstance(retained_filter, RetainedFilter):
        raise TypeError("retained_filter must be a RetainedFilter")
    if retained_filter.storage_kind != "multistate_tt_grid":
        raise ValueError("transition adjacent target requires multistate_tt_grid retained filter")
    if retained_filter.measure_convention != measure_convention:
        raise ValueError(HighDimStatus.RETAINED_MEASURE_MISMATCH.value)
    if retained_filter.retained_axes != tuple(range(int(model.state_dim()))):
        raise ValueError(HighDimStatus.RETAINED_AXES_MISMATCH.value)
    theta_vector = _as_theta_vector(theta, int(model.parameter_dim()))
    observation_vector = tf.reshape(
        tf.convert_to_tensor(observation, dtype=tf.float64),
        [int(model.observation_dim())],
    )
    reference_points, weights = _tensor_product_reference_quadrature(
        product_basis,
        int(quadrature_order),
    )
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    log_predictive = _multistate_tt_predictive_log_density_from_retained(
        model=model,
        theta=theta_vector,
        current_physical_points=physical_points,
        retained_filter=retained_filter,
        coordinate_map=coordinate_map,
        time_index=int(time_index),
    )
    log_physical_target = log_predictive + model.observation_log_density(
        theta_vector,
        physical_points,
        observation_vector,
        t=int(time_index),
    )
    log_reference_weight = _log_uniform_reference_weight_density(product_basis)
    log_reference_target = log_physical_target + log_abs_det - log_reference_weight
    return _finalize_multistate_adjacent_target_result(
        target_kind="transition",
        model=model,
        theta=theta_vector,
        observation=observation_vector,
        product_basis=product_basis,
        coordinate_map=coordinate_map,
        reference_points=reference_points,
        physical_points=physical_points,
        log_abs_det=log_abs_det,
        weights=weights,
        log_reference_target=log_reference_target,
        measure_convention=measure_convention,
        retained_filter=retained_filter,
        fixture_id=fixture_id,
        target_id=target_id,
        branch_seed=branch_seed,
        log_scale_shift=log_scale_shift,
        time_index=int(time_index),
    )


def affine_nonuniform_reference_scalar_fixture(
    observation: float = 0.2,
    quadrature_order: int = 128,
) -> Mapping[str, tf.Tensor]:
    """Evaluate the pinned affine/non-uniform reference conversion fixture."""

    nodes, weights = legendre_gauss_nodes_weights(quadrature_order)
    z = nodes
    r = 0.5 + 2.0 * z
    omega = (1.0 + 0.25 * z) / 2.0
    prior = tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )
    likelihood = tfp.distributions.Normal(
        loc=r,
        scale=tf.constant(0.3, dtype=tf.float64),
    )
    gamma_r = tf.exp(prior.log_prob(r) + likelihood.log_prob(tf.constant(observation, dtype=tf.float64)))
    gamma_nu = gamma_r * 2.0 / omega
    density_mass = gamma_nu * omega
    evidence = tf.reduce_sum(weights * density_mass)
    mean = tf.reduce_sum(weights * r * density_mass) / evidence
    second = tf.reduce_sum(weights * tf.square(r) * density_mass) / evidence
    wrong_without_omega = tf.reduce_sum(weights * gamma_r * 2.0 * omega)
    return {
        "log_evidence": tf.math.log(evidence),
        "filter_mean": mean,
        "filter_variance": second - tf.square(mean),
        "wrong_log_evidence_without_omega_division": tf.math.log(wrong_without_omega),
    }


def dense_scalar_nonlinear_observation_oracle(
    observation: float,
    quadrature_order: int = 160,
    domain_radius: float = 6.0,
) -> tf.Tensor:
    """Dense quadrature oracle for ``x~N(0,1), y|x~N(x^2,0.25)``."""

    nodes, weights = legendre_gauss_nodes_weights(quadrature_order)
    x = domain_radius * nodes
    scaled_weights = domain_radius * weights
    prior = tfp.distributions.Normal(
        loc=tf.constant(0.0, dtype=tf.float64),
        scale=tf.constant(1.0, dtype=tf.float64),
    )
    likelihood = tfp.distributions.Normal(
        loc=tf.square(x),
        scale=tf.constant(0.5, dtype=tf.float64),
    )
    gamma = tf.exp(prior.log_prob(x) + likelihood.log_prob(tf.constant(observation, dtype=tf.float64)))
    return tf.math.log(tf.reduce_sum(scaled_weights * gamma))


def legendre_gauss_nodes_weights(order: int) -> tuple[tf.Tensor, tf.Tensor]:
    """Compute Gauss-Legendre nodes and weights on ``[-1,1]`` using TensorFlow."""

    if int(order) < 2:
        raise ValueError("order must be at least 2")
    k = tf.cast(tf.range(1, int(order), dtype=tf.int32), tf.float64)
    beta = k / tf.sqrt(4.0 * tf.square(k) - 1.0)
    jacobi = tf.linalg.diag(beta, k=1) + tf.linalg.diag(beta, k=-1)
    eigenvalues, eigenvectors = tf.linalg.eigh(jacobi)
    weights = 2.0 * tf.square(eigenvectors[0, :])
    return eigenvalues, weights


def _tensor_product_reference_quadrature(
    product_basis: ProductBasis,
    order: int,
) -> tuple[tf.Tensor, tf.Tensor]:
    nodes_1d, weights_1d = legendre_gauss_nodes_weights(order)
    axis_nodes = []
    axis_weights = []
    for basis in product_basis.bases:
        half_length = 0.5 * basis.domain.length
        midpoint = 0.5 * (basis.domain.left + basis.domain.right)
        physical_nodes = midpoint + half_length * nodes_1d
        uniform_weights = 0.5 * weights_1d
        axis_nodes.append(physical_nodes)
        axis_weights.append(uniform_weights)
    mesh_nodes = tf.meshgrid(*axis_nodes, indexing="ij")
    mesh_weights = tf.meshgrid(*axis_weights, indexing="ij")
    points = tf.stack([tf.reshape(axis, [-1]) for axis in mesh_nodes], axis=1)
    weights = tf.ones([tf.shape(points)[0]], dtype=tf.float64)
    for axis_weight in mesh_weights:
        weights = weights * tf.reshape(axis_weight, [-1])
    return points, weights


def _log_uniform_reference_weight_density(product_basis: ProductBasis) -> tf.Tensor:
    log_density = tf.constant(0.0, dtype=tf.float64)
    for basis in product_basis.bases:
        log_density = log_density - tf.math.log(basis.domain.length)
    return log_density


def _gaussian_log_density(points: tf.Tensor, mean: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    mean = tf.convert_to_tensor(mean, dtype=tf.float64)
    covariance = _symmetrize(tf.convert_to_tensor(covariance, dtype=tf.float64))
    return _mvn_log_prob(points, mean[tf.newaxis, :], covariance)


def _scalar_pairwise_transition_log_density(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    physical_points: tf.Tensor,
    t: int,
) -> tf.Tensor:
    points = _as_matrix(physical_points, 1, "physical_points")
    next_points = tf.repeat(points, repeats=int(points.shape[0]), axis=0)
    previous_points = tf.tile(points, [int(points.shape[0]), 1])
    values = model.transition_log_density(theta, previous_points, next_points, t=t)
    return tf.reshape(values, [int(points.shape[0]), int(points.shape[0])])


def _scalar_grid_moments(
    x_grid: tf.Tensor,
    weights: tf.Tensor,
    log_abs_det: tf.Tensor,
    log_density_physical: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    x = tf.convert_to_tensor(x_grid, dtype=tf.float64)
    weights_tensor = tf.convert_to_tensor(weights, dtype=tf.float64)
    log_jacobian = tf.convert_to_tensor(log_abs_det, dtype=tf.float64)
    log_density = tf.convert_to_tensor(log_density_physical, dtype=tf.float64)
    mass = weights_tensor * tf.exp(log_density + log_jacobian)
    normalizer = tf.reduce_sum(mass)
    if not bool(tf.math.is_finite(normalizer).numpy()) or bool((normalizer <= 0.0).numpy()):
        raise ValueError(HighDimStatus.NORMALIZER_FLOOR_EXCEEDED.value)
    mean = tf.reduce_sum(mass * x) / normalizer
    second = tf.reduce_sum(mass * tf.square(x)) / normalizer
    variance = tf.maximum(second - tf.square(mean), tf.constant(0.0, dtype=tf.float64))
    return mean, variance


def _validate_scalar_adjacent_target_common(
    model: TFHighDimStateSpaceModel,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    measure_convention: MeasureConvention,
    quadrature_order: int,
    fixture_id: str,
    target_id: str,
) -> None:
    if int(model.state_dim()) != 1:
        raise TypeError("scalar adjacent target requires state_dim == 1")
    if not isinstance(product_basis, ProductBasis):
        raise TypeError("product_basis must be a ProductBasis")
    if product_basis.dimension != 1:
        raise ValueError(f"product_basis: {HighDimStatus.INVALID_SHAPE.value}")
    if product_basis.convention != measure_convention:
        raise ValueError(f"product_basis: {HighDimStatus.MEASURE_MISMATCH.value}")
    if not hasattr(coordinate_map, "forward") or not hasattr(coordinate_map, "manifest_payload"):
        raise TypeError("coordinate_map must implement HighDimCoordinateMap")
    if int(quadrature_order) < 2:
        raise ValueError("quadrature_order must be at least 2")
    if not str(fixture_id).strip():
        raise ValueError("fixture_id must be nonempty")
    if not str(target_id).strip():
        raise ValueError("target_id must be nonempty")
    assert_density_matches_mass(measure_convention)


def _finalize_scalar_adjacent_target_result(
    target_kind: str,
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    reference_points: tf.Tensor,
    physical_points: tf.Tensor,
    log_abs_det: tf.Tensor,
    weights: tf.Tensor,
    log_reference_target: tf.Tensor,
    measure_convention: MeasureConvention,
    retained_filter: RetainedFilter | None,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None,
    time_index: int,
) -> ScalarAdjacentTargetBuildResult:
    scale_shift = (
        tf.reduce_max(log_reference_target)
        if log_scale_shift is None
        else tf.convert_to_tensor(log_scale_shift, dtype=tf.float64)
    )
    target_batch = build_adjacent_target_batch(
        time_index=int(time_index),
        physical_points=physical_points,
        reference_points=reference_points,
        log_target=log_reference_target,
        weights=weights,
        measure_convention=measure_convention,
        retained_filter=retained_filter,
        expected_retained_axes=retained_filter.retained_axes if retained_filter is not None else None,
        log_scale_shift=scale_shift,
    )
    if not bool(
        tf.reduce_all(tf.math.is_finite(target_batch.sqrt_target)).numpy()
        and tf.reduce_all(tf.math.is_finite(target_batch.log_target)).numpy()
    ):
        raise ValueError(f"scalar adjacent target: {HighDimStatus.NONFINITE_VALUE.value}")
    diagnostics = {
        "target_kind": str(target_kind),
        "fixture_id": str(fixture_id),
        "target_id": str(target_id),
        "time_index": int(time_index),
        "reference_space_target": "sqrt(g_t(T(z)) * abs_det_jacobian / omega(z))",
        "max_log_scaling": "BAYESFILTER_EXTENSION",
        "log_scale_shift": scale_shift,
        "reference_density_convention": _measure_convention_payload(measure_convention),
        "coordinate_map": coordinate_map.manifest_payload(),
        "product_basis": _product_basis_payload(product_basis),
        "retained_filter_hash": (
            retained_filter.branch_identity.hash.value if retained_filter is not None else None
        ),
        "grid_size": int(reference_points.shape[0]),
        "reference_window": _scalar_window_from_grid(reference_points),
        "physical_window": _scalar_window_from_grid(physical_points),
        "what_is_not_claimed": (
            "sequential_tt_sirt_filtering",
            "squared_density_normalizer",
            "adaptive_tt_cross",
            "zhao_cui_t1000_reproduction",
        ),
    }
    manifest = BranchManifest(
        version="scalar_adjacent_target_batch.v1",
        payload={
            "target_kind": str(target_kind),
            "fixture_id": str(fixture_id),
            "target_id": str(target_id),
            "time_index": int(time_index),
            "model": model.manifest_payload(),
            "theta": theta,
            "observation": observation,
            "product_basis": _product_basis_payload(product_basis),
            "coordinate_map": coordinate_map.manifest_payload(),
            "reference_points": reference_points,
            "physical_points": physical_points,
            "log_abs_det": log_abs_det,
            "weights": weights,
            "log_reference_target": log_reference_target,
            "sqrt_target": target_batch.sqrt_target,
            "log_scale_shift": scale_shift,
            "measure_convention": _measure_convention_payload(measure_convention),
            "retained_filter_hash": (
                retained_filter.branch_identity.hash.value if retained_filter is not None else None
            ),
            "branch_seed": branch_seed,
            "status": HighDimStatus.OK.value,
            "scope": "p37_m2p6a_fixed_design_scalar_adjacent_target",
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return ScalarAdjacentTargetBuildResult(
        target_batch=target_batch,
        branch_identity=identity,
        status=HighDimStatus.OK,
        diagnostics=diagnostics,
    )


def _validate_multistate_adjacent_target_common(
    model: TFHighDimStateSpaceModel,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    measure_convention: MeasureConvention,
    quadrature_order: int,
    fixture_id: str,
    target_id: str,
) -> None:
    state_dim = int(model.state_dim())
    if state_dim <= 1:
        raise TypeError("multistate adjacent target requires state_dim > 1")
    if not isinstance(product_basis, ProductBasis):
        raise TypeError("product_basis must be a ProductBasis")
    if int(product_basis.dimension) != state_dim:
        raise ValueError(f"product_basis: {HighDimStatus.INVALID_SHAPE.value}")
    if product_basis.convention != measure_convention:
        raise ValueError(f"product_basis: {HighDimStatus.MEASURE_MISMATCH.value}")
    if not hasattr(coordinate_map, "forward") or not hasattr(coordinate_map, "manifest_payload"):
        raise TypeError("coordinate_map must implement HighDimCoordinateMap")
    if int(quadrature_order) < 2:
        raise ValueError("quadrature_order must be at least 2")
    if not str(fixture_id).strip():
        raise ValueError("fixture_id must be nonempty")
    if not str(target_id).strip():
        raise ValueError("target_id must be nonempty")
    assert_density_matches_mass(measure_convention)


def _finalize_multistate_adjacent_target_result(
    target_kind: str,
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    observation: tf.Tensor,
    product_basis: ProductBasis,
    coordinate_map: HighDimCoordinateMap,
    reference_points: tf.Tensor,
    physical_points: tf.Tensor,
    log_abs_det: tf.Tensor,
    weights: tf.Tensor,
    log_reference_target: tf.Tensor,
    measure_convention: MeasureConvention,
    retained_filter: RetainedFilter | None,
    fixture_id: str,
    target_id: str,
    branch_seed: int | str,
    log_scale_shift: tf.Tensor | None,
    time_index: int,
) -> MultistateAdjacentTargetBuildResult:
    scale_shift = (
        tf.reduce_max(log_reference_target)
        if log_scale_shift is None
        else tf.convert_to_tensor(log_scale_shift, dtype=tf.float64)
    )
    target_batch = build_adjacent_target_batch(
        time_index=int(time_index),
        physical_points=physical_points,
        reference_points=reference_points,
        log_target=log_reference_target,
        weights=weights,
        measure_convention=measure_convention,
        retained_filter=retained_filter,
        expected_retained_axes=retained_filter.retained_axes if retained_filter is not None else None,
        log_scale_shift=scale_shift,
    )
    if not bool(
        tf.reduce_all(tf.math.is_finite(target_batch.sqrt_target)).numpy()
        and tf.reduce_all(tf.math.is_finite(target_batch.log_target)).numpy()
    ):
        raise ValueError(f"multistate adjacent target: {HighDimStatus.NONFINITE_VALUE.value}")
    diagnostics = {
        "target_kind": str(target_kind),
        "fixture_id": str(fixture_id),
        "target_id": str(target_id),
        "time_index": int(time_index),
        "state_dim": int(model.state_dim()),
        "reference_space_target": "sqrt(g_t(T(z)) * abs_det_jacobian / omega(z))",
        "max_log_scaling": "BAYESFILTER_EXTENSION",
        "log_scale_shift": scale_shift,
        "reference_density_convention": _measure_convention_payload(measure_convention),
        "coordinate_map": coordinate_map.manifest_payload(),
        "product_basis": _product_basis_payload(product_basis),
        "retained_filter_hash": (
            retained_filter.branch_identity.hash.value if retained_filter is not None else None
        ),
        "grid_size": int(reference_points.shape[0]),
        "all_axes_retained": True,
        "what_is_not_claimed": (
            "sequential_tt_sirt_filtering",
            "adaptive_tt_cross",
            "zhao_cui_t1000_reproduction",
            "integrated_axis_marginalization",
            "large_scale_performance",
        ),
    }
    manifest = BranchManifest(
        version="multistate_adjacent_target_batch.v1",
        payload={
            "target_kind": str(target_kind),
            "fixture_id": str(fixture_id),
            "target_id": str(target_id),
            "time_index": int(time_index),
            "state_dim": int(model.state_dim()),
            "model": model.manifest_payload(),
            "theta": theta,
            "observation": observation,
            "product_basis": _product_basis_payload(product_basis),
            "coordinate_map": coordinate_map.manifest_payload(),
            "reference_points": reference_points,
            "physical_points": physical_points,
            "log_abs_det": log_abs_det,
            "weights": weights,
            "log_reference_target": log_reference_target,
            "sqrt_target": target_batch.sqrt_target,
            "log_scale_shift": scale_shift,
            "measure_convention": _measure_convention_payload(measure_convention),
            "retained_filter_hash": (
                retained_filter.branch_identity.hash.value if retained_filter is not None else None
            ),
            "branch_seed": branch_seed,
            "status": HighDimStatus.OK.value,
            "scope": "p46_fixed_design_multistate_adjacent_target",
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return MultistateAdjacentTargetBuildResult(
        target_batch=target_batch,
        branch_identity=identity,
        status=HighDimStatus.OK,
        diagnostics=diagnostics,
    )


def _scalar_dense_predictive_log_density_from_retained(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    retained_filter: RetainedFilter,
    coordinate_map: HighDimCoordinateMap,
    time_index: int,
) -> tf.Tensor:
    return _scalar_grid_predictive_log_density_from_retained(
        model=model,
        theta=theta,
        current_physical_points=current_physical_points,
        retained_filter=retained_filter,
        coordinate_map=coordinate_map,
        time_index=int(time_index),
        expected_storage_kind="scalar_dense_grid",
    )


def _scalar_tt_predictive_log_density_from_retained(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    retained_filter: RetainedFilter,
    coordinate_map: HighDimCoordinateMap,
    time_index: int,
) -> tf.Tensor:
    if retained_filter.storage_kind != "scalar_tt_grid":
        raise ValueError("TT predictive propagation requires scalar_tt_grid retained filter")
    if not isinstance(retained_filter.density, SquaredTTDensity):
        raise ValueError("scalar_tt_grid retained filter requires SquaredTTDensity")
    density_hash = retained_filter.diagnostics.get("density_hash")
    if density_hash != retained_filter.density.branch_identity.hash.value:
        raise ValueError(HighDimStatus.INVALID_BRANCH_MISMATCH.value)
    return _scalar_grid_predictive_log_density_from_retained(
        model=model,
        theta=theta,
        current_physical_points=current_physical_points,
        retained_filter=retained_filter,
        coordinate_map=coordinate_map,
        time_index=int(time_index),
        expected_storage_kind="scalar_tt_grid",
    )


def _multistate_tt_predictive_log_density_from_retained(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    retained_filter: RetainedFilter,
    coordinate_map: HighDimCoordinateMap,
    time_index: int,
) -> tf.Tensor:
    if retained_filter.storage_kind != "multistate_tt_grid":
        raise ValueError("TT predictive propagation requires multistate_tt_grid retained filter")
    if not isinstance(retained_filter.density, SquaredTTDensity):
        raise ValueError("multistate_tt_grid retained filter requires SquaredTTDensity")
    density_hash = retained_filter.diagnostics.get("density_hash")
    if density_hash != retained_filter.density.branch_identity.hash.value:
        raise ValueError(HighDimStatus.INVALID_BRANCH_MISMATCH.value)
    return _multistate_grid_predictive_log_density_from_retained(
        model=model,
        theta=theta,
        current_physical_points=current_physical_points,
        retained_filter=retained_filter,
        coordinate_map=coordinate_map,
        time_index=int(time_index),
    )


def _scalar_grid_predictive_log_density_from_retained(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    retained_filter: RetainedFilter,
    coordinate_map: HighDimCoordinateMap,
    time_index: int,
    expected_storage_kind: str,
) -> tf.Tensor:
    if retained_filter.storage_kind != expected_storage_kind:
        raise ValueError(f"retained filter requires {expected_storage_kind}")
    diagnostics = retained_filter.diagnostics
    previous_physical = _as_matrix(diagnostics["physical_points"], 1, "retained.physical_points")
    previous_reference = _as_matrix(diagnostics["reference_points"], 1, "retained.reference_points")
    previous_weights = tf.convert_to_tensor(diagnostics["weights"], dtype=tf.float64)
    previous_log_density = tf.convert_to_tensor(
        diagnostics["log_density_physical"],
        dtype=tf.float64,
    )
    if previous_weights.shape != (int(previous_physical.shape[0]),):
        raise ValueError(f"retained weights: {HighDimStatus.INVALID_SHAPE.value}")
    previous_physical_from_map, previous_log_abs_det = coordinate_map.forward(previous_reference)
    if not bool(
        tf.reduce_all(tf.abs(previous_physical_from_map - previous_physical) <= 1e-10).numpy()
    ):
        raise ValueError(f"retained coordinate map: {HighDimStatus.INVALID_BRANCH_MISMATCH.value}")
    transition_log = _scalar_pairwise_transition_between_grids_log_density(
        model=model,
        theta=theta,
        current_physical_points=current_physical_points,
        previous_physical_points=previous_physical,
        time_index=int(time_index),
    )
    terms = (
        tf.math.log(previous_weights)[tf.newaxis, :]
        + previous_log_abs_det[tf.newaxis, :]
        + previous_log_density[tf.newaxis, :]
        + transition_log
    )
    return tf.reduce_logsumexp(terms, axis=1)


def _multistate_grid_predictive_log_density_from_retained(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    retained_filter: RetainedFilter,
    coordinate_map: HighDimCoordinateMap,
    time_index: int,
) -> tf.Tensor:
    state_dim = int(model.state_dim())
    if retained_filter.storage_kind != "multistate_tt_grid":
        raise ValueError("retained filter requires multistate_tt_grid")
    diagnostics = retained_filter.diagnostics
    previous_physical = _as_matrix(diagnostics["physical_points"], state_dim, "retained.physical_points")
    previous_reference = _as_matrix(diagnostics["reference_points"], state_dim, "retained.reference_points")
    previous_weights = tf.convert_to_tensor(diagnostics["weights"], dtype=tf.float64)
    previous_log_density = tf.convert_to_tensor(
        diagnostics["log_density_physical"],
        dtype=tf.float64,
    )
    if previous_weights.shape != (int(previous_physical.shape[0]),):
        raise ValueError(f"retained weights: {HighDimStatus.INVALID_SHAPE.value}")
    previous_physical_from_map, previous_log_abs_det = coordinate_map.forward(previous_reference)
    if not bool(
        tf.reduce_all(tf.abs(previous_physical_from_map - previous_physical) <= 1e-10).numpy()
    ):
        raise ValueError(f"retained coordinate map: {HighDimStatus.INVALID_BRANCH_MISMATCH.value}")
    transition_log = _multistate_pairwise_transition_between_grids_log_density(
        model=model,
        theta=theta,
        current_physical_points=current_physical_points,
        previous_physical_points=previous_physical,
        time_index=int(time_index),
    )
    if not isinstance(retained_filter.density, SquaredTTDensity):
        raise ValueError("multistate_tt_grid retained filter requires SquaredTTDensity")
    log_reference_weight = _log_uniform_reference_weight_density(retained_filter.density.sqrt_tt.product_basis)
    terms = (
        tf.math.log(previous_weights)[tf.newaxis, :]
        + previous_log_abs_det[tf.newaxis, :]
        - log_reference_weight
        + previous_log_density[tf.newaxis, :]
        + transition_log
    )
    return tf.reduce_logsumexp(terms, axis=1)


def scalar_tt_grid_retained_filter(
    physical_points: tf.Tensor,
    reference_points: tf.Tensor,
    weights: tf.Tensor,
    log_density_physical: tf.Tensor,
    mean: tf.Tensor,
    variance: tf.Tensor,
    retained_axes: Sequence[int],
    retained_coordinate_names: Sequence[str],
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
    density: SquaredTTDensity,
) -> RetainedFilter:
    """Build a scalar retained grid generated by a squared TT density."""

    if not isinstance(density, SquaredTTDensity):
        raise TypeError("density must be a SquaredTTDensity")
    physical = _as_matrix(physical_points, 1, "physical_points")
    reference = _as_matrix(reference_points, 1, "reference_points")
    weights_tensor = tf.convert_to_tensor(weights, dtype=tf.float64)
    log_density = tf.convert_to_tensor(log_density_physical, dtype=tf.float64)
    mean_tensor = tf.convert_to_tensor(mean, dtype=tf.float64)
    variance_tensor = tf.convert_to_tensor(variance, dtype=tf.float64)
    if weights_tensor.shape != (int(physical.shape[0]),) or log_density.shape != (int(physical.shape[0]),):
        raise ValueError(f"scalar_tt_grid_retained_filter: {HighDimStatus.INVALID_SHAPE.value}")
    if mean_tensor.shape.rank != 0 or variance_tensor.shape.rank != 0:
        raise ValueError(f"scalar_tt_grid_retained_filter: {HighDimStatus.INVALID_SHAPE.value}")
    for name, value in (
        ("weights", weights_tensor),
        ("log_density_physical", log_density),
        ("mean", mean_tensor),
        ("variance", variance_tensor),
    ):
        assert_tf_float64(name, value)
        if not bool(tf.reduce_all(tf.math.is_finite(value)).numpy()):
            raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    if bool(tf.reduce_any(weights_tensor <= 0.0).numpy()) or bool((variance_tensor < 0.0).numpy()):
        raise ValueError(f"scalar_tt_grid_retained_filter: {HighDimStatus.NONFINITE_VALUE.value}")
    estimated_bytes = (int(physical.shape[0]) * 4 + 3) * tf.float64.size
    if estimated_bytes > int(storage_byte_budget):
        raise ValueError(HighDimStatus.RETAINED_STORAGE_BUDGET_EXCEEDED.value)
    density_hash = density.branch_identity.hash.value
    manifest = BranchManifest(
        version="retained_filter_scalar_tt_grid.v1",
        payload={
            "stage": stage,
            "storage_kind": "scalar_tt_grid",
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": mean_tensor,
            "variance": variance_tensor,
            "retained_axes": tuple(int(axis) for axis in retained_axes),
            "retained_coordinate_names": tuple(str(name) for name in retained_coordinate_names),
            "measure_convention": _measure_convention_payload(measure_convention),
            "normalizer": normalizer,
            "density_hash": density_hash,
        },
    )
    identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
    return RetainedFilter(
        density=density,
        retained_axes=tuple(int(axis) for axis in retained_axes),
        retained_coordinate_names=tuple(str(name) for name in retained_coordinate_names),
        measure_convention=measure_convention,
        normalizer=normalizer,
        branch_identity=identity,
        storage_kind="scalar_tt_grid",
        diagnostics={
            "physical_points": physical,
            "reference_points": reference,
            "weights": weights_tensor,
            "log_density_physical": log_density,
            "mean": tf.reshape(mean_tensor, [1]),
            "covariance": tf.reshape(variance_tensor, [1, 1]),
            "variance": variance_tensor,
            "density_hash": density_hash,
            "estimated_storage_bytes": estimated_bytes,
        },
    )


def _squared_density_from_fit_result(
    fit_result: object,
    product_basis: ProductBasis,
    config: FixedBranchFilterConfig,
) -> SquaredTTDensity:
    defensive = TensorProductReferenceDensity(
        product_basis=product_basis,
        measure_convention=config.measure_convention,
    )
    tau = tf.constant(config.density_tau, dtype=tf.float64)
    normalizer_floor = tf.constant(config.normalizer_floor, dtype=tf.float64)
    denominator_floor = tf.constant(config.denominator_floor, dtype=tf.float64)
    density_identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=config.measure_convention,
    )
    return SquaredTTDensity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=config.measure_convention,
        branch_identity=density_identity,
    )


def _scalar_tt_retained_moments(
    density: SquaredTTDensity,
    coordinate_map: HighDimCoordinateMap,
    order: int,
) -> Mapping[str, tf.Tensor]:
    nodes, weights = legendre_gauss_nodes_weights(int(order))
    reference_points = nodes[:, tf.newaxis]
    moment_weights = 0.5 * weights
    values = _normalized_retained_density_values_chunked(density, reference_points)
    physical_points, _ = coordinate_map.forward(reference_points)
    mass = tf.reduce_sum(moment_weights * values)
    if not bool(tf.math.is_finite(mass).numpy()) or bool((mass <= 0.0).numpy()):
        raise ValueError(HighDimStatus.NORMALIZER_FLOOR_EXCEEDED.value)
    mean = tf.reduce_sum(moment_weights * physical_points[:, 0] * values)
    second = tf.reduce_sum(moment_weights * tf.square(physical_points[:, 0]) * values)
    variance = tf.maximum(second - tf.square(mean), tf.constant(0.0, dtype=tf.float64))
    return {
        "mass": mass,
        "mean": mean,
        "variance": variance,
    }


def _scalar_tt_grid_retained_from_density(
    density: SquaredTTDensity,
    coordinate_map: HighDimCoordinateMap,
    order: int,
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
    mean: tf.Tensor,
    variance: tf.Tensor,
) -> RetainedFilter:
    nodes, weights = legendre_gauss_nodes_weights(int(order))
    reference_points = nodes[:, tf.newaxis]
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    reference_density = _normalized_retained_density_values_chunked(density, reference_points)
    log_reference_density = tf.math.log(reference_density)
    log_physical_density = (
        log_reference_density
        - log_abs_det
        + _log_uniform_reference_weight_density(density.sqrt_tt.product_basis)
    )
    return scalar_tt_grid_retained_filter(
        physical_points=physical_points,
        reference_points=reference_points,
        weights=weights,
        log_density_physical=log_physical_density,
        mean=mean,
        variance=variance,
        retained_axes=(0,),
        retained_coordinate_names=("x0",),
        measure_convention=measure_convention,
        normalizer=normalizer,
        storage_byte_budget=storage_byte_budget,
        stage=stage,
        density=density,
    )


def _multistate_tt_retained_moments(
    density: SquaredTTDensity,
    coordinate_map: HighDimCoordinateMap,
    order: int,
) -> Mapping[str, tf.Tensor]:
    reference_points, moment_weights = _tensor_product_reference_quadrature(
        density.sqrt_tt.product_basis,
        int(order),
    )
    values = _normalized_retained_density_values_chunked(density, reference_points)
    physical_points, _ = coordinate_map.forward(reference_points)
    mass = tf.reduce_sum(moment_weights * values)
    if not bool(tf.math.is_finite(mass).numpy()) or bool((mass <= 0.0).numpy()):
        raise ValueError(HighDimStatus.NORMALIZER_FLOOR_EXCEEDED.value)
    normalized_mass = moment_weights * values / mass
    mean = tf.reduce_sum(physical_points * normalized_mass[:, tf.newaxis], axis=0)
    centered = physical_points - mean[tf.newaxis, :]
    covariance = tf.einsum("n,ni,nj->ij", normalized_mass, centered, centered)
    return {
        "mass": mass,
        "mean": mean,
        "covariance": _symmetrize(covariance),
    }


def _multistate_tt_grid_retained_from_density(
    density: SquaredTTDensity,
    coordinate_map: HighDimCoordinateMap,
    order: int,
    measure_convention: MeasureConvention,
    normalizer: tf.Tensor,
    storage_byte_budget: int,
    stage: str,
    mean: tf.Tensor,
    covariance: tf.Tensor,
) -> RetainedFilter:
    reference_points, weights = _tensor_product_reference_quadrature(
        density.sqrt_tt.product_basis,
        int(order),
    )
    physical_points, log_abs_det = coordinate_map.forward(reference_points)
    reference_density = _normalized_retained_density_values_chunked(density, reference_points)
    log_reference_density = tf.math.log(reference_density)
    log_physical_density = (
        log_reference_density
        - log_abs_det
        + _log_uniform_reference_weight_density(density.sqrt_tt.product_basis)
    )
    state_dim = int(density.sqrt_tt.product_basis.dimension)
    return multistate_tt_grid_retained_filter(
        physical_points=physical_points,
        reference_points=reference_points,
        weights=weights,
        log_density_physical=log_physical_density,
        mean=mean,
        covariance=covariance,
        retained_axes=tuple(range(state_dim)),
        retained_coordinate_names=tuple(f"x{axis}" for axis in range(state_dim)),
        measure_convention=measure_convention,
        normalizer=normalizer,
        storage_byte_budget=storage_byte_budget,
        stage=stage,
        density=density,
    )


def _normalized_retained_density_values_chunked(
    density: SquaredTTDensity,
    reference_points: tf.Tensor,
) -> tf.Tensor:
    points_tensor = tf.convert_to_tensor(reference_points, dtype=tf.float64)
    if points_tensor.shape.rank != 2:
        raise ValueError(f"reference_points: {HighDimStatus.INVALID_SHAPE.value}")
    points = _as_matrix(
        points_tensor,
        int(density.sqrt_tt.product_basis.dimension),
        "reference_points",
    )
    row_count = int(points.shape[0])
    chunk_size = max(1, int(density.sqrt_tt.complexity_budget.max_elements) // 80)
    chunks = []
    for start in range(0, row_count, chunk_size):
        stop = min(row_count, start + chunk_size)
        chunks.append(
            density.normalized_retained_density_values(
                tuple(range(int(density.sqrt_tt.product_basis.dimension))),
                points[start:stop],
            )
        )
    return tf.concat(chunks, axis=0)


def _scalar_pairwise_transition_between_grids_log_density(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    previous_physical_points: tf.Tensor,
    time_index: int,
) -> tf.Tensor:
    current = _as_matrix(current_physical_points, 1, "current_physical_points")
    previous = _as_matrix(previous_physical_points, 1, "previous_physical_points")
    current_count = int(current.shape[0])
    previous_count = int(previous.shape[0])
    next_points = tf.repeat(current, repeats=previous_count, axis=0)
    previous_points = tf.tile(previous, [current_count, 1])
    values = model.transition_log_density(
        theta,
        previous_points,
        next_points,
        t=int(time_index),
    )
    return tf.reshape(values, [current_count, previous_count])


def _multistate_pairwise_transition_between_grids_log_density(
    model: TFHighDimStateSpaceModel,
    theta: tf.Tensor,
    current_physical_points: tf.Tensor,
    previous_physical_points: tf.Tensor,
    time_index: int,
) -> tf.Tensor:
    state_dim = int(model.state_dim())
    current = _as_matrix(current_physical_points, state_dim, "current_physical_points")
    previous = _as_matrix(previous_physical_points, state_dim, "previous_physical_points")
    current_count = int(current.shape[0])
    previous_count = int(previous.shape[0])
    next_points = tf.repeat(current, repeats=previous_count, axis=0)
    previous_points = tf.tile(previous, [current_count, 1])
    values = model.transition_log_density(
        theta,
        previous_points,
        next_points,
        t=int(time_index),
    )
    return tf.reshape(values, [current_count, previous_count])


def _logsumexp_weighted(log_values: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    values = tf.convert_to_tensor(log_values, dtype=tf.float64)
    weights_tensor = tf.convert_to_tensor(weights, dtype=tf.float64)
    if values.shape != weights_tensor.shape:
        raise ValueError(f"weighted logsumexp: {HighDimStatus.INVALID_SHAPE.value}")
    if bool(tf.reduce_any(weights_tensor <= 0.0).numpy()):
        raise ValueError(f"weights: {HighDimStatus.NONFINITE_VALUE.value}")
    max_value = tf.reduce_max(values)
    return tf.math.log(tf.reduce_sum(weights_tensor * tf.exp(values - max_value))) + max_value


def _as_theta_vector(theta: tf.Tensor, parameter_dim: int) -> tf.Tensor:
    tensor = tf.convert_to_tensor(theta, dtype=tf.float64)
    if tensor.shape.rank == 2 and tensor.shape[0] == 1:
        tensor = tensor[0]
    if tensor.shape.rank != 1 or tensor.shape[0] != int(parameter_dim):
        raise ValueError(f"theta: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"theta: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _scalar_grid_payload(
    reference_points: tf.Tensor,
    weights: tf.Tensor,
    physical_points: tf.Tensor,
    log_abs_det: tf.Tensor,
) -> Mapping[str, object]:
    return {
        "reference_points": reference_points,
        "weights": weights,
        "physical_points": physical_points,
        "log_abs_det": log_abs_det,
        "window": _scalar_window_from_grid(physical_points),
    }


def _coordinate_map_for_config(
    config: FixedBranchFilterConfig,
    dimension: int,
) -> HighDimCoordinateMap:
    for coordinate_map in config.coordinate_maps:
        payload = coordinate_map.manifest_payload()
        payload_dimension = payload.get("dimension")
        if payload_dimension is not None and int(payload_dimension) == int(dimension):
            return coordinate_map
        if payload.get("family") == "AffineCoordinateMap":
            matrix = payload.get("matrix")
            if matrix is not None and int(tf.convert_to_tensor(matrix).shape[0]) == int(dimension):
                return coordinate_map
    return IdentityCoordinateMap(int(dimension))


def _scalar_window_from_grid(physical_points: tf.Tensor) -> tuple[float, float]:
    points = _as_matrix(physical_points, 1, "physical_points")
    return (
        float(tf.reduce_min(points[:, 0]).numpy()),
        float(tf.reduce_max(points[:, 0]).numpy()),
    )


def _default_initial_cores(
    product_basis: ProductBasis,
    fit_config: FixedTTFitConfig,
) -> tuple[TTCore, ...]:
    if len(fit_config.ranks) != product_basis.dimension + 1:
        raise ValueError(f"ranks: {HighDimStatus.INVALID_SHAPE.value}")
    cores = []
    for axis, basis in enumerate(product_basis.bases):
        values = tf.zeros(
            [fit_config.ranks[axis], basis.basis_dim, fit_config.ranks[axis + 1]],
            dtype=tf.float64,
        )
        updates = []
        if axis == 0:
            updates.append(([0, 0, 0], tf.constant(1.0, dtype=tf.float64)))
        else:
            for rank in range(min(fit_config.ranks[axis], fit_config.ranks[axis + 1])):
                updates.append(([rank, 0, rank], tf.constant(1.0, dtype=tf.float64)))
        if not updates:
            updates.append(([0, 0, 0], tf.constant(1.0, dtype=tf.float64)))
        indices = tf.constant([update[0] for update in updates], dtype=tf.int32)
        values_to_update = tf.stack([update[1] for update in updates])
        cores.append(TTCore(tf.tensor_scatter_nd_update(values, indices, values_to_update)))
    return tuple(cores)


def _core_values_hash(cores: Sequence[TTCore] | None) -> str | None:
    if cores is None:
        return None
    manifest = BranchManifest(
        version="phase4_initial_cores_hash.v1",
        payload={"cores": tuple(core.values for core in cores)},
    )
    return manifest.sha256().value


def _product_basis_payload(product_basis: ProductBasis | None) -> Mapping[str, object] | None:
    if product_basis is None:
        return None
    return {
        "family": "ProductBasis",
        "dimension": int(product_basis.dimension),
        "basis_dim_tuple": product_basis.basis_dim_tuple(),
        "convention": _measure_convention_payload(product_basis.convention),
        "bases": tuple(
            {
                "family": "LegendreBasis1D",
                "left": basis.domain.left,
                "right": basis.domain.right,
                "max_degree": int(basis.max_degree),
                "normalized": bool(basis.normalized),
            }
            for basis in product_basis.bases
        ),
    }


def _as_matrix(values: tf.Tensor, width: int, name: str) -> tf.Tensor:
    tensor = tf.convert_to_tensor(values, dtype=tf.float64)
    if tensor.shape.rank == 1:
        tensor = tensor[:, tf.newaxis] if int(width) == 1 else tensor[tf.newaxis, :]
    if tensor.shape.rank != 2 or tensor.shape[1] != width:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _as_observation_matrix(observations: tf.Tensor, observation_dim: int) -> tf.Tensor:
    values = tf.convert_to_tensor(observations, dtype=tf.float64)
    if values.shape.rank == 1:
        values = values[:, tf.newaxis]
    if values.shape.rank != 2 or values.shape[1] != observation_dim:
        raise ValueError(f"observations: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(values)).numpy()):
        raise ValueError(f"observations: {HighDimStatus.NONFINITE_VALUE.value}")
    return values


def _mvn_log_prob(values: tf.Tensor, loc: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    covariance = _symmetrize(covariance)
    chol = tf.linalg.cholesky(covariance)
    return tfp.distributions.MultivariateNormalTriL(loc=loc, scale_tril=chol).log_prob(values)


def _symmetrize(matrix: tf.Tensor) -> tf.Tensor:
    return 0.5 * (matrix + tf.linalg.matrix_transpose(matrix))


def _measure_convention_payload(convention: MeasureConvention) -> Mapping[str, object]:
    return {
        "density_measure": convention.density_measure.value,
        "mass_measure": convention.mass_measure.value,
        "reference_weight_name": convention.reference_weight_name,
        "physical_coordinate_name": convention.physical_coordinate_name,
        "reference_coordinate_name": convention.reference_coordinate_name,
        "dtype_name": convention.dtype_name,
    }
