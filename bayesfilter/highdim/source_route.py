"""Clean-room source-route contracts for Zhao--Cui-style filtering."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Mapping

import tensorflow as tf

from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.diagnostics import (
    DensityMeasure,
    HighDimStatus,
    MassMeasure,
    MeasureConvention,
    assert_density_matches_mass,
    assert_tf_float64,
    freeze_mapping,
)
from bayesfilter.highdim.fitting import FixedTTFitConfig, FixedTTFitSampleBatch, FixedTTFitter
from bayesfilter.highdim.fixed_branch import BranchIdentity, BranchManifest
from bayesfilter.highdim.models import zhao_cui_sir_austria_model
from bayesfilter.highdim.squared_tt import (
    SquaredTTDensity,
    SquaredTTMarginal,
    TensorProductReferenceDensity,
)
from bayesfilter.highdim.transport import FixedTTSIRTTransport, KRCDFConfig
from bayesfilter.highdim.tt import TTCore


SOURCE_FAITHFUL_ROUTE_LABEL = "source_faithful_filtering"
GRADIENT_ADAPTATION_ROUTE_LABEL = "gradient_bearing_adaptation"
SOURCE_ROUTE_REQUIRED_OPERATION_IDS = (
    "initialize_samples",
    "push_samples",
    "augment_current_previous_state",
    "ess_enhancement_gate",
    "weighted_recenter_computeL",
    "previous_retained_object_marginalization",
    "shifted_target_construction",
    "transport_fit",
    "normalizer_update",
    "retained_sample_generation",
    "proposal_correction",
)
SOURCE_ROUTE_FORBIDDEN_DRIFT_MARKERS = (
    "pairwise_grid_transition",
    "all_grid_pairwise_transition",
    "multistate_grid_pairwise_transition",
    "retained_grid_only_route",
    "all_grid_retained_storage",
    "multistate_tt_grid_retained_storage",
    "local_neighborhood_rank_multiplier",
    "q_power_dependency_width",
)

P58_M9_READY_STATUS = "PASS_P58_M9_SOURCE_ROUTE_PIPELINE_READY_FOR_PHASE9_LAUNCH"
P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS = (
    "BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_STILL_MISSING_ASSEMBLY"
)
P58_M9_BLOCK_SOURCE_DRIFT_STATUS = "BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_SOURCE_DRIFT"
P58_M9_BLOCK_HUMAN_REQUIRED_STATUS = (
    "BLOCK_P58_M9_SOURCE_ROUTE_PIPELINE_HUMAN_REQUIRED"
)

P58_M9_REQUIRED_ASSEMBLY_FLAGS = (
    "has_author_sir_callback",
    "has_fixed_ttsirt_fit_artifacts",
    "has_fixed_ttsirt_transports",
    "has_frozen_reference_samples",
    "has_source_route_step_specs",
    "has_sequential_retained_carry",
    "has_previous_marginal_evidence",
    "has_m9_runner_manifest_path",
)

P58_M9_ALLOWED_COMPARATOR_TIERS = (
    "d18_execution_only",
    "d18_same_route_rank_convergence",
    "d18_correctness_candidate",
)

P58_M9_SOURCE_ROUTE_PIPELINE_KIND = "author_sir_fixed_ttsirt_source_route"
P58_M9_AUTHOR_SIR_TARGET_ID = "zhao_cui_sir_austria_d18"

P59_9A_PASS_STATUS = "PASS_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP"
P59_9A_BLOCK_STATUS = "BLOCK_P59_9A_AUTHOR_SIR_36D_TARGET_FIT_PREP"
P59_9A_AUTHOR_SIR_TARGET_DIMENSION = 36
P59_9C_PASS_STATUS = "PASS_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION"
P59_9C_BLOCK_STATUS = "BLOCK_P59_9C_PRECONDITIONED_ROUTE_INTEGRATION"
P59_9C_FULL_ROUTE_SELECTED = "full_route_selected"
P59_9C_PRECONDITIONED_ROUTE_REQUIRED = "preconditioned_route_required"
P59_9C_PRECONDITIONED_ROUTE_DEFERRED = "preconditioned_route_deferred_with_source_reason"
P59_9C_ROUTE_DECISION_BLOCKED = "route_decision_blocked"
P59_9C_NOT_REQUIRED_PRECONDITIONED_STATUS = (
    "not_required_author_sir_mainscript_selects_full_sol"
)
P57_M8_PRECONDITIONED_PASS_STATUS = "PASS_P57_M8_PRECONDITIONED_ALGORITHM5"
P59_9B_PASS_STATUS = "PASS_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY"
P59_9B_BLOCK_STATUS = "BLOCK_P59_9B_SOURCE_ROUTE_STEP_SPEC_ASSEMBLY"
P59_9D_PASS_STATUS = "PASS_P59_9D_RUNNER_MANIFEST_PATH"
P59_9D_BLOCK_STATUS = "BLOCK_P59_9D_RUNNER_MANIFEST_PATH"
P59_9D_DEFAULT_MANIFEST_PATH = (
    "docs/plans/bayesfilter-highdim-zhao-cui-p59-9d-runner-readiness-manifest-2026-06-11.json"
)
P59_9E_D18_EXECUTION_ONLY_PASS_STATUS = "PASS_P59_9E_D18_EXECUTION_ONLY"
P59_9E_BLOCK_STATUS = "BLOCK_P59_9E_VALIDATION_LADDER"
P60_D18_RANK_CONVERGENCE_PASS_STATUS = "PASS_P60_D18_SAME_ROUTE_RANK_CONVERGENCE"
P60_D18_RANK_CONVERGENCE_BLOCK_STATUS = "BLOCK_P60_D18_SAME_ROUTE_RANK_CONVERGENCE"
P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU = 1e-8
P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE = "source_pushed_computeL_resampled_local_fit"
P63_AUTHOR_SIR_FIXED_VARIANT_RESAMPLING = "deterministic_systematic_quantile"
P63_AUTHOR_SIR_EXPANSION_FACTOR = 4.0
P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL = 1e-14

_P62_AUTHOR_TTSIRT_DEFENSIVE_TAU_SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:185-188",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:116-120",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:85",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/eval_potential_reference.m:20-33",
)
_P63_AUTHOR_SIR_FIT_DATA_SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:22-30",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-66",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-99",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:1-35",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m:45-55",
)

_P59_9C_AUTHOR_SIR_SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:53-56",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:9-18",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-38",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:1-10",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/precond.m:43-56",
)
_P59_9B_AUTHOR_SIR_SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-56",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-38",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:72-93",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-130",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:132-135",
)
_P59_9D_AUTHOR_SIR_SOURCE_ANCHORS = (
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-25",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:26-30",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:32-39",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:54-87",
    "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:101-130",
)

_FORBIDDEN_SOURCE_STORAGE_KINDS = frozenset(
    {
        "scalar_dense_grid",
        "scalar_tt_grid",
        "multistate_tt_grid",
        "all_axes_tensor_product_grid",
    }
)

_FORBIDDEN_SOURCE_TRANSITION_INTERFACES = frozenset(
    {
        "pairwise_grid_transition",
        "all_grid_pairwise_transition",
        "multistate_grid_pairwise_transition",
    }
)


@dataclass(frozen=True)
class SourceRouteCoordinateFrame:
    """Affine frame carried by the clean-room source route."""

    mu: tf.Tensor
    matrix: tf.Tensor
    expansion_factor: float

    def __post_init__(self) -> None:
        mu = tf.convert_to_tensor(self.mu, dtype=tf.float64)
        matrix = tf.convert_to_tensor(self.matrix, dtype=tf.float64)
        if mu.shape.rank != 1 or matrix.shape.rank != 2:
            raise ValueError(f"SourceRouteCoordinateFrame: {HighDimStatus.INVALID_SHAPE.value}")
        if matrix.shape[0] != matrix.shape[1] or matrix.shape[0] != mu.shape[0]:
            raise ValueError(f"SourceRouteCoordinateFrame: {HighDimStatus.INVALID_SHAPE.value}")
        assert_tf_float64("mu", mu)
        assert_tf_float64("matrix", matrix)
        if not bool(
            tf.reduce_all(tf.math.is_finite(mu)).numpy()
            and tf.reduce_all(tf.math.is_finite(matrix)).numpy()
        ):
            raise ValueError(f"SourceRouteCoordinateFrame: {HighDimStatus.NONFINITE_VALUE.value}")
        det = tf.linalg.det(matrix)
        if not bool(tf.math.is_finite(det).numpy()) or bool((tf.abs(det) <= 0.0).numpy()):
            raise ValueError(f"SourceRouteCoordinateFrame: {HighDimStatus.NONFINITE_VALUE.value}")
        if float(self.expansion_factor) <= 0.0:
            raise ValueError("expansion_factor must be positive")
        object.__setattr__(self, "mu", mu)
        object.__setattr__(self, "matrix", matrix)
        object.__setattr__(self, "expansion_factor", float(self.expansion_factor))

    @property
    def dimension(self) -> int:
        return int(self.mu.shape[0])

    def log_abs_det(self) -> tf.Tensor:
        return tf.math.log(tf.abs(tf.linalg.det(self.matrix)))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteCoordinateFrame",
            "mu": self.mu,
            "matrix": self.matrix,
            "expansion_factor": float(self.expansion_factor),
            "log_abs_det": self.log_abs_det(),
        }


@dataclass(frozen=True)
class SourceRouteSampleDiagnostics:
    """Sample and weight diagnostics carried by a source-route retained object."""

    sample_count: int
    effective_sample_size: tf.Tensor
    enhancement_attempts: int = 0

    def __post_init__(self) -> None:
        if int(self.sample_count) <= 0:
            raise ValueError("sample_count must be positive")
        ess = tf.convert_to_tensor(self.effective_sample_size, dtype=tf.float64)
        if ess.shape.rank != 0:
            raise ValueError(f"effective_sample_size: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.math.is_finite(ess).numpy()) or bool((ess <= 0.0).numpy()):
            raise ValueError(f"effective_sample_size: {HighDimStatus.NONFINITE_VALUE.value}")
        if bool((ess > float(self.sample_count) + 1e-9).numpy()):
            raise ValueError("effective_sample_size cannot exceed sample_count")
        if int(self.enhancement_attempts) < 0:
            raise ValueError("enhancement_attempts must be nonnegative")
        object.__setattr__(self, "sample_count", int(self.sample_count))
        object.__setattr__(self, "effective_sample_size", ess)
        object.__setattr__(self, "enhancement_attempts", int(self.enhancement_attempts))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSampleDiagnostics",
            "sample_count": int(self.sample_count),
            "effective_sample_size": self.effective_sample_size,
            "enhancement_attempts": int(self.enhancement_attempts),
        }


@dataclass(frozen=True)
class SourceRouteNormalizerContribution:
    """Named normalizer terms for the clean-room source route."""

    log_transport_normalizer: tf.Tensor
    shift_constant: tf.Tensor
    log_abs_det_policy: str

    def __post_init__(self) -> None:
        log_z = tf.convert_to_tensor(self.log_transport_normalizer, dtype=tf.float64)
        shift = tf.convert_to_tensor(self.shift_constant, dtype=tf.float64)
        for name, value in (
            ("log_transport_normalizer", log_z),
            ("shift_constant", shift),
        ):
            if value.shape.rank != 0:
                raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
            if not bool(tf.math.is_finite(value).numpy()):
                raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        if str(self.log_abs_det_policy) not in ("included_in_target", "separate_term"):
            raise ValueError("log_abs_det_policy must be included_in_target or separate_term")
        object.__setattr__(self, "log_transport_normalizer", log_z)
        object.__setattr__(self, "shift_constant", shift)
        object.__setattr__(self, "log_abs_det_policy", str(self.log_abs_det_policy))

    def log_increment(self) -> tf.Tensor:
        return self.log_transport_normalizer - self.shift_constant

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteNormalizerContribution",
            "log_transport_normalizer": self.log_transport_normalizer,
            "shift_constant": self.shift_constant,
            "log_abs_det_policy": self.log_abs_det_policy,
            "log_increment": self.log_increment(),
        }


@dataclass(frozen=True)
class SourceRouteSampleBatch:
    """Weighted sample batch used by the clean-room source route."""

    samples: tf.Tensor
    log_weights: tf.Tensor
    time_index: int
    route_label: str
    sample_origin: str

    def __post_init__(self) -> None:
        samples = tf.convert_to_tensor(self.samples, dtype=tf.float64)
        log_weights = tf.convert_to_tensor(self.log_weights, dtype=tf.float64)
        if samples.shape.rank != 2:
            raise ValueError(f"samples: {HighDimStatus.INVALID_SHAPE.value}")
        if log_weights.shape != (int(samples.shape[1]),):
            raise ValueError(f"log_weights: {HighDimStatus.INVALID_SHAPE.value}")
        assert_tf_float64("samples", samples)
        assert_tf_float64("log_weights", log_weights)
        if not bool(
            tf.reduce_all(tf.math.is_finite(samples)).numpy()
            and tf.reduce_all(tf.math.is_finite(log_weights)).numpy()
        ):
            raise ValueError(f"SourceRouteSampleBatch: {HighDimStatus.NONFINITE_VALUE.value}")
        if int(self.time_index) < 0:
            raise ValueError("time_index must be nonnegative")
        if not str(self.route_label).strip():
            raise ValueError("route_label must be nonempty")
        if not str(self.sample_origin).strip():
            raise ValueError("sample_origin must be nonempty")
        object.__setattr__(self, "samples", samples)
        object.__setattr__(self, "log_weights", log_weights)
        object.__setattr__(self, "time_index", int(self.time_index))
        object.__setattr__(self, "route_label", str(self.route_label))
        object.__setattr__(self, "sample_origin", str(self.sample_origin))

    @property
    def dimension(self) -> int:
        return int(self.samples.shape[0])

    @property
    def sample_count(self) -> int:
        return int(self.samples.shape[1])

    def normalized_log_weights(self) -> tf.Tensor:
        return normalize_log_weights(self.log_weights)

    def effective_sample_size(self) -> tf.Tensor:
        return effective_sample_size_from_log_weights(self.log_weights)

    def diagnostics(self, *, enhancement_attempts: int = 0) -> SourceRouteSampleDiagnostics:
        return SourceRouteSampleDiagnostics(
            sample_count=self.sample_count,
            effective_sample_size=self.effective_sample_size(),
            enhancement_attempts=int(enhancement_attempts),
        )

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSampleBatch",
            "samples": self.samples,
            "log_weights": self.log_weights,
            "time_index": int(self.time_index),
            "route_label": self.route_label,
            "sample_origin": self.sample_origin,
            "normalized_log_weights": self.normalized_log_weights(),
            "effective_sample_size": self.effective_sample_size(),
        }


@dataclass(frozen=True)
class SourceRoutePushResult:
    """Clean-room source-route push output for one filtering step."""

    propagated_batch: SourceRouteSampleBatch
    augmented_batch: SourceRouteSampleBatch
    diagnostics: SourceRouteSampleDiagnostics

    def __post_init__(self) -> None:
        if not isinstance(self.propagated_batch, SourceRouteSampleBatch):
            raise TypeError("propagated_batch must be SourceRouteSampleBatch")
        if not isinstance(self.augmented_batch, SourceRouteSampleBatch):
            raise TypeError("augmented_batch must be SourceRouteSampleBatch")
        if not isinstance(self.diagnostics, SourceRouteSampleDiagnostics):
            raise TypeError("diagnostics must be SourceRouteSampleDiagnostics")
        if self.propagated_batch.sample_count != self.augmented_batch.sample_count:
            raise ValueError("propagated and augmented sample counts must match")
        if self.propagated_batch.time_index != self.augmented_batch.time_index:
            raise ValueError("propagated and augmented time indices must match")
        if self.propagated_batch.route_label != SOURCE_FAITHFUL_ROUTE_LABEL:
            raise ValueError("source push result must use source_faithful_filtering")
        if self.augmented_batch.route_label != SOURCE_FAITHFUL_ROUTE_LABEL:
            raise ValueError("source push result must use source_faithful_filtering")

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePushResult",
            "propagated_batch": self.propagated_batch.manifest_payload(),
            "augmented_batch": self.augmented_batch.manifest_payload(),
            "diagnostics": self.diagnostics.manifest_payload(),
        }


@dataclass(frozen=True)
class _P59AuthorSIRSourceFitData:
    """Source-derived fixed-variant fit data for one author-SIR step."""

    time_index: int
    frame: SourceRouteCoordinateFrame
    local_fit_points: tf.Tensor
    target_values: tf.Tensor
    negative_log_values: tf.Tensor
    shift_constant: tf.Tensor
    fit_weights: tf.Tensor
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        if not isinstance(self.frame, SourceRouteCoordinateFrame):
            raise TypeError("frame must be SourceRouteCoordinateFrame")
        local = tf.convert_to_tensor(self.local_fit_points, dtype=tf.float64)
        targets = _finite_vector("target_values", self.target_values)
        negative = _finite_vector("negative_log_values", self.negative_log_values)
        weights = _finite_vector("fit_weights", self.fit_weights)
        shift = tf.convert_to_tensor(self.shift_constant, dtype=tf.float64)
        if local.shape.rank != 2 or int(local.shape[0]) != self.frame.dimension:
            raise ValueError(f"local_fit_points: {HighDimStatus.INVALID_SHAPE.value}")
        if targets.shape != (int(local.shape[1]),):
            raise ValueError(f"target_values: {HighDimStatus.INVALID_SHAPE.value}")
        if negative.shape != targets.shape or weights.shape != targets.shape:
            raise ValueError(f"fit data vectors: {HighDimStatus.INVALID_SHAPE.value}")
        if shift.shape.rank != 0 or not bool(tf.math.is_finite(shift).numpy()):
            raise ValueError(f"shift_constant: {HighDimStatus.INVALID_SHAPE.value}")
        assert_tf_float64("local_fit_points", local)
        if not bool(tf.reduce_all(tf.math.is_finite(local)).numpy()):
            raise ValueError(f"local_fit_points: {HighDimStatus.NONFINITE_VALUE.value}")
        object.__setattr__(self, "time_index", int(self.time_index))
        object.__setattr__(self, "local_fit_points", local)
        object.__setattr__(self, "target_values", targets)
        object.__setattr__(self, "negative_log_values", negative)
        object.__setattr__(self, "shift_constant", shift)
        object.__setattr__(self, "fit_weights", weights)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))


@dataclass(frozen=True)
class SourceRouteTarget:
    """One-step source-route target in local coordinates."""

    negative_log_physical_density_fn: object
    coordinate_frame: SourceRouteCoordinateFrame
    shift_constant: tf.Tensor
    time_index: int
    target_family: str
    source_terms: tuple[str, ...]
    log_abs_det_policy: str = "included_in_target"

    def __post_init__(self) -> None:
        if not callable(self.negative_log_physical_density_fn):
            raise TypeError("negative_log_physical_density_fn must be callable")
        if not isinstance(self.coordinate_frame, SourceRouteCoordinateFrame):
            raise TypeError("coordinate_frame must be SourceRouteCoordinateFrame")
        shift = tf.convert_to_tensor(self.shift_constant, dtype=tf.float64)
        if shift.shape.rank != 0:
            raise ValueError(f"shift_constant: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.math.is_finite(shift).numpy()):
            raise ValueError(f"shift_constant: {HighDimStatus.NONFINITE_VALUE.value}")
        if int(self.time_index) < 1:
            raise ValueError("time_index must be positive for source-route targets")
        if str(self.target_family) not in ("full", "preconditioner", "residual"):
            raise ValueError("target_family must be full, preconditioner, or residual")
        terms = tuple(str(term) for term in self.source_terms)
        if not terms:
            raise ValueError("source_terms must be nonempty")
        for required in ("prior_or_previous", "transition", "likelihood"):
            if required not in terms:
                raise ValueError(f"source_terms missing {required}")
        if str(self.log_abs_det_policy) != "included_in_target":
            raise ValueError("P55 source target requires included_in_target determinant policy")
        object.__setattr__(self, "shift_constant", shift)
        object.__setattr__(self, "time_index", int(self.time_index))
        object.__setattr__(self, "target_family", str(self.target_family))
        object.__setattr__(self, "source_terms", terms)
        object.__setattr__(self, "log_abs_det_policy", str(self.log_abs_det_policy))

    def physical_points_from_reference(self, reference_points: tf.Tensor) -> tf.Tensor:
        reference = tf.convert_to_tensor(reference_points, dtype=tf.float64)
        if reference.shape.rank != 2:
            raise ValueError(f"reference_points: {HighDimStatus.INVALID_SHAPE.value}")
        if int(reference.shape[0]) != self.coordinate_frame.dimension:
            raise ValueError(f"reference_points: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(tf.math.is_finite(reference)).numpy()):
            raise ValueError(f"reference_points: {HighDimStatus.NONFINITE_VALUE.value}")
        return (
            tf.linalg.matmul(self.coordinate_frame.matrix, reference)
            + self.coordinate_frame.mu[:, tf.newaxis]
        )

    def negative_log_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        physical = self.physical_points_from_reference(reference_points)
        negative_log_physical = _finite_vector(
            "negative_log_physical_density",
            self.negative_log_physical_density_fn(physical),
        )
        if negative_log_physical.shape != (int(physical.shape[1]),):
            raise ValueError(
                f"negative_log_physical_density: {HighDimStatus.INVALID_SHAPE.value}"
            )
        local_negative_log = (
            negative_log_physical
            - self.coordinate_frame.log_abs_det()
        )
        return source_route_shifted_negative_log_target(
            negative_log_target=local_negative_log,
            shift_constant=self.shift_constant,
        )

    def log_target_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        return -self.negative_log_density(reference_points)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteTarget",
            "time_index": int(self.time_index),
            "target_family": self.target_family,
            "source_terms": self.source_terms,
            "shift_constant": self.shift_constant,
            "log_abs_det_policy": self.log_abs_det_policy,
            "coordinate_frame": self.coordinate_frame.manifest_payload(),
        }


@dataclass(frozen=True)
class SourceRouteTransportProtocol:
    """Protocol wrapper for source-route transport objects."""

    transport_object: object
    route_label: str = SOURCE_FAITHFUL_ROUTE_LABEL

    def __post_init__(self) -> None:
        if str(self.route_label) != SOURCE_FAITHFUL_ROUTE_LABEL:
            raise ValueError("transport protocol must use source_faithful_filtering")
        required_methods = (
            "manifest_payload",
            "inverse_transport",
            "forward_transport",
            "conditional_inverse_transport",
            "eval_pdf",
            "potential",
            "proposal_log_density",
            "marginalize",
            "log_normalizer",
        )
        missing = tuple(
            method for method in required_methods
            if not callable(getattr(self.transport_object, method, None))
        )
        if missing:
            raise TypeError(
                "transport_object missing required methods: " + ", ".join(missing)
            )
        payload = self.transport_object.manifest_payload()
        if not isinstance(payload, Mapping):
            raise TypeError("transport_object manifest_payload() must return a mapping")
        contract_level = str(payload.get("source_contract_level", ""))
        if contract_level not in ("contract_test_double", "fixed_ttsirt"):
            raise ValueError(
                "transport_object manifest_payload() must declare "
                "source_contract_level as contract_test_double or fixed_ttsirt"
            )
        if contract_level == "fixed_ttsirt":
            for key in ("tt_cores_declared", "defensive_density_declared"):
                if payload.get(key) is not True:
                    raise ValueError(f"fixed_ttsirt transport must declare {key}")
        log_z = tf.convert_to_tensor(self.transport_object.log_normalizer(), dtype=tf.float64)
        if log_z.shape.rank != 0 or not bool(tf.math.is_finite(log_z).numpy()):
            raise ValueError(f"log_normalizer: {HighDimStatus.NONFINITE_VALUE.value}")
        object.__setattr__(self, "route_label", str(self.route_label))

    def inverse_transport(self, reference_points: tf.Tensor) -> tf.Tensor:
        result = tf.convert_to_tensor(
            self.transport_object.inverse_transport(reference_points),
            dtype=tf.float64,
        )
        if result.shape != tf.convert_to_tensor(reference_points, dtype=tf.float64).shape:
            raise ValueError(f"inverse_transport: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(tf.math.is_finite(result)).numpy()):
            raise ValueError(f"inverse_transport: {HighDimStatus.NONFINITE_VALUE.value}")
        return result

    def log_reference_density(self, reference_points: tf.Tensor) -> tf.Tensor:
        if not callable(getattr(self.transport_object, "log_reference_density", None)):
            raise TypeError(
                "log_reference_density is diagnostic-only and unavailable for this source transport"
            )
        values = _finite_vector(
            "log_reference_density",
            self.transport_object.log_reference_density(reference_points),
        )
        reference = tf.convert_to_tensor(reference_points, dtype=tf.float64)
        if reference.shape.rank != 2 or values.shape != (int(reference.shape[1]),):
            raise ValueError(f"log_reference_density: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def forward_transport(self, local_points: tf.Tensor) -> tf.Tensor:
        result = tf.convert_to_tensor(
            self.transport_object.forward_transport(local_points),
            dtype=tf.float64,
        )
        if result.shape != tf.convert_to_tensor(local_points, dtype=tf.float64).shape:
            raise ValueError(f"forward_transport: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(tf.math.is_finite(result)).numpy()):
            raise ValueError(f"forward_transport: {HighDimStatus.NONFINITE_VALUE.value}")
        return result

    def conditional_inverse_transport(
        self,
        conditioning_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        result = tf.convert_to_tensor(
            self.transport_object.conditional_inverse_transport(
                conditioning_points,
                reference_points,
            ),
            dtype=tf.float64,
        )
        reference = tf.convert_to_tensor(reference_points, dtype=tf.float64)
        if result.shape != reference.shape:
            raise ValueError(
                f"conditional_inverse_transport: {HighDimStatus.INVALID_SHAPE.value}"
            )
        if not bool(tf.reduce_all(tf.math.is_finite(result)).numpy()):
            raise ValueError(
                f"conditional_inverse_transport: {HighDimStatus.NONFINITE_VALUE.value}"
            )
        return result

    def eval_pdf(self, local_points: tf.Tensor) -> tf.Tensor:
        values = _finite_vector("eval_pdf", self.transport_object.eval_pdf(local_points))
        local = tf.convert_to_tensor(local_points, dtype=tf.float64)
        if local.shape.rank != 2 or values.shape != (int(local.shape[1]),):
            raise ValueError(f"eval_pdf: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(values > 0.0).numpy()):
            raise ValueError(f"eval_pdf: {HighDimStatus.NONFINITE_VALUE.value}")
        return values

    def potential(self, local_points: tf.Tensor) -> tf.Tensor:
        values = _finite_vector("potential", self.transport_object.potential(local_points))
        local = tf.convert_to_tensor(local_points, dtype=tf.float64)
        if local.shape.rank != 2 or values.shape != (int(local.shape[1]),):
            raise ValueError(f"potential: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def proposal_log_density(
        self,
        *,
        local_points: tf.Tensor,
        reference_points: tf.Tensor,
    ) -> tf.Tensor:
        values = _finite_vector(
            "proposal_log_density",
            self.transport_object.proposal_log_density(
                local_points=local_points,
                reference_points=reference_points,
            ),
        )
        local = tf.convert_to_tensor(local_points, dtype=tf.float64)
        reference = tf.convert_to_tensor(reference_points, dtype=tf.float64)
        if (
            local.shape.rank != 2
            or reference.shape.rank != 2
            or local.shape != reference.shape
            or values.shape != (int(local.shape[1]),)
        ):
            raise ValueError(f"proposal_log_density: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def marginalize(self, keep_axes: tuple[int, ...]) -> object:
        result = self.transport_object.marginalize(tuple(int(axis) for axis in keep_axes))
        if result is None:
            raise ValueError(f"marginalize: {HighDimStatus.INVALID_SHAPE.value}")
        return result

    def log_normalizer(self) -> tf.Tensor:
        value = tf.convert_to_tensor(self.transport_object.log_normalizer(), dtype=tf.float64)
        if value.shape.rank != 0 or not bool(tf.math.is_finite(value).numpy()):
            raise ValueError(f"log_normalizer: {HighDimStatus.NONFINITE_VALUE.value}")
        return value

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteTransportProtocol",
            "route_label": self.route_label,
            "source_contract_level": self.transport_object.manifest_payload().get(
                "source_contract_level"
            ),
            "required_source_methods": (
                "inverse_transport",
                "forward_transport",
                "conditional_inverse_transport",
                "eval_pdf",
                "potential",
                "proposal_log_density",
                "marginalize",
                "log_normalizer",
            ),
            "proposal_density_semantics": "transport_eval_pdf_equivalent_on_local_samples",
            "transport_object": self.transport_object.manifest_payload(),
            "log_normalizer": self.log_normalizer(),
        }


@dataclass(frozen=True)
class SourceRouteRetainedSampleResult:
    """Retained sample generation plus source proposal-correction output."""

    retained_batch: SourceRouteSampleBatch
    proposal_log_density: tf.Tensor
    target_log_density: tf.Tensor
    correction_log_weights: tf.Tensor
    diagnostics: SourceRouteSampleDiagnostics
    normalizer: SourceRouteNormalizerContribution

    def __post_init__(self) -> None:
        if not isinstance(self.retained_batch, SourceRouteSampleBatch):
            raise TypeError("retained_batch must be SourceRouteSampleBatch")
        proposal, target = _finite_same_shape_vectors(
            "proposal_log_density",
            self.proposal_log_density,
            "target_log_density",
            self.target_log_density,
        )
        correction = _finite_vector("correction_log_weights", self.correction_log_weights)
        if correction.shape != proposal.shape:
            raise ValueError(
                f"correction_log_weights: {HighDimStatus.INVALID_SHAPE.value}"
            )
        tf.debugging.assert_near(correction, target - proposal, atol=1e-10)
        if not isinstance(self.diagnostics, SourceRouteSampleDiagnostics):
            raise TypeError("diagnostics must be SourceRouteSampleDiagnostics")
        if not isinstance(self.normalizer, SourceRouteNormalizerContribution):
            raise TypeError("normalizer must be SourceRouteNormalizerContribution")
        if self.retained_batch.sample_count != self.diagnostics.sample_count:
            raise ValueError("diagnostics sample_count must match retained batch")
        object.__setattr__(self, "proposal_log_density", proposal)
        object.__setattr__(self, "target_log_density", target)
        object.__setattr__(self, "correction_log_weights", correction)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteRetainedSampleResult",
            "retained_batch": self.retained_batch.manifest_payload(),
            "proposal_log_density": self.proposal_log_density,
            "target_log_density": self.target_log_density,
            "correction_log_weights": self.correction_log_weights,
            "diagnostics": self.diagnostics.manifest_payload(),
            "normalizer": self.normalizer.manifest_payload(),
        }


@dataclass(frozen=True)
class SourceRouteOneStepResult:
    """P55 one-step source reapproximation boundary result."""

    target: SourceRouteTarget
    transport: SourceRouteTransportProtocol
    retained_samples: SourceRouteRetainedSampleResult
    time_index: int
    sequential_status: str = "one_step_t1_only"

    def __post_init__(self) -> None:
        if not isinstance(self.target, SourceRouteTarget):
            raise TypeError("target must be SourceRouteTarget")
        if not isinstance(self.transport, SourceRouteTransportProtocol):
            raise TypeError("transport must be SourceRouteTransportProtocol")
        if not isinstance(self.retained_samples, SourceRouteRetainedSampleResult):
            raise TypeError("retained_samples must be SourceRouteRetainedSampleResult")
        if int(self.time_index) != 1 or self.target.time_index != 1:
            raise ValueError(
                "P55 one-step source reapproximation only supports t=1; "
                "previous retained-object marginalization is not implemented"
            )
        if str(self.sequential_status) != "one_step_t1_only":
            raise ValueError("sequential_status must be one_step_t1_only")
        object.__setattr__(self, "time_index", int(self.time_index))
        object.__setattr__(self, "sequential_status", str(self.sequential_status))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteOneStepResult",
            "time_index": int(self.time_index),
            "sequential_status": self.sequential_status,
            "target": self.target.manifest_payload(),
            "transport": self.transport.manifest_payload(),
            "retained_samples": self.retained_samples.manifest_payload(),
        }


@dataclass(frozen=True)
class SourceRouteOperationRecord:
    """Audit row for one source-route operation."""

    operation_id: str
    source_anchor: str
    implementation_status: str
    route_label: str = SOURCE_FAITHFUL_ROUTE_LABEL
    notes: str = ""

    def __post_init__(self) -> None:
        operation = str(self.operation_id)
        if operation not in SOURCE_ROUTE_REQUIRED_OPERATION_IDS:
            raise ValueError("unknown source-route operation_id")
        if not str(self.source_anchor).strip():
            raise ValueError("source_anchor must be nonempty")
        status = str(self.implementation_status)
        if status not in {"implemented", "partial", "blocked"}:
            raise ValueError("implementation_status must be implemented, partial, or blocked")
        if not str(self.route_label).strip():
            raise ValueError("route_label must be nonempty")
        object.__setattr__(self, "operation_id", operation)
        object.__setattr__(self, "source_anchor", str(self.source_anchor))
        object.__setattr__(self, "implementation_status", status)
        object.__setattr__(self, "route_label", str(self.route_label))
        object.__setattr__(self, "notes", str(self.notes))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "operation_id": self.operation_id,
            "source_anchor": self.source_anchor,
            "implementation_status": self.implementation_status,
            "route_label": self.route_label,
            "notes": self.notes,
        }


@dataclass(frozen=True)
class SourceRouteImplementationAudit:
    """Drift-aware audit of source-route operation coverage."""

    records: tuple[SourceRouteOperationRecord, ...]
    drift_markers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        records = tuple(self.records)
        if not records:
            raise ValueError("records must be nonempty")
        if not all(isinstance(row, SourceRouteOperationRecord) for row in records):
            raise TypeError("records must contain SourceRouteOperationRecord")
        markers = tuple(str(marker) for marker in self.drift_markers)
        for marker in markers:
            if marker not in SOURCE_ROUTE_FORBIDDEN_DRIFT_MARKERS:
                raise ValueError("unknown source-route drift marker")
        object.__setattr__(self, "records", records)
        object.__setattr__(self, "drift_markers", markers)

    @property
    def missing_required_operations(self) -> tuple[str, ...]:
        present = {row.operation_id for row in self.records}
        return tuple(
            operation
            for operation in SOURCE_ROUTE_REQUIRED_OPERATION_IDS
            if operation not in present
        )

    @property
    def incomplete_required_operations(self) -> tuple[str, ...]:
        return tuple(
            row.operation_id
            for row in self.records
            if row.implementation_status != "implemented"
        )

    @property
    def status(self) -> str:
        if self.drift_markers:
            return "BLOCK_SOURCE_ROUTE_DRIFT"
        if self.missing_required_operations or self.incomplete_required_operations:
            return "BLOCK_SOURCE_ROUTE_INCOMPLETE"
        return "PASS_SOURCE_ROUTE_OPERATION_COVERAGE"

    def assert_no_drift(self) -> None:
        if self.drift_markers:
            raise ValueError("source-route drift markers present")

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteImplementationAudit",
            "required_operation_ids": SOURCE_ROUTE_REQUIRED_OPERATION_IDS,
            "records": [row.manifest_payload() for row in self.records],
            "missing_required_operations": self.missing_required_operations,
            "incomplete_required_operations": self.incomplete_required_operations,
            "drift_markers": self.drift_markers,
            "status": self.status,
        }


@dataclass(frozen=True)
class SourceRouteSequentialDensityComponents:
    """Source density components for one sequential fixed-HMC step."""

    parameter_dim: int
    state_dim: int
    transition_log_density_fn: object
    likelihood_log_density_fn: object
    prior_log_density_fn: object | None = None
    source_anchor: str = "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:76-130"

    def __post_init__(self) -> None:
        d = int(self.parameter_dim)
        m = int(self.state_dim)
        if d < 0 or m <= 0:
            raise ValueError("parameter_dim must be nonnegative and state_dim positive")
        if not callable(self.transition_log_density_fn):
            raise TypeError("transition_log_density_fn must be callable")
        if not callable(self.likelihood_log_density_fn):
            raise TypeError("likelihood_log_density_fn must be callable")
        if self.prior_log_density_fn is not None and not callable(self.prior_log_density_fn):
            raise TypeError("prior_log_density_fn must be callable when provided")
        if not str(self.source_anchor).strip():
            raise ValueError("source_anchor must be nonempty")
        object.__setattr__(self, "parameter_dim", d)
        object.__setattr__(self, "state_dim", m)
        object.__setattr__(self, "source_anchor", str(self.source_anchor))

    def negative_log_physical_density(
        self,
        *,
        physical_points: tf.Tensor,
        time_index: int,
        previous_retained_object: SourceRouteRetainedObject | None,
    ) -> tf.Tensor:
        return source_route_sequential_negative_log_physical_density(
            physical_points=physical_points,
            time_index=int(time_index),
            parameter_dim=self.parameter_dim,
            state_dim=self.state_dim,
            transition_log_density_fn=self.transition_log_density_fn,
            likelihood_log_density_fn=self.likelihood_log_density_fn,
            prior_log_density_fn=self.prior_log_density_fn,
            previous_retained_object=previous_retained_object,
        )

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSequentialDensityComponents",
            "parameter_dim": int(self.parameter_dim),
            "state_dim": int(self.state_dim),
            "has_prior_log_density_fn": self.prior_log_density_fn is not None,
            "source_anchor": self.source_anchor,
            "source_terms": ("prior_or_previous", "transition", "likelihood"),
        }


@dataclass(frozen=True)
class SourceRouteSequentialStepSpec:
    """Frozen inputs for one fixed-HMC replay step of the source route."""

    target: SourceRouteTarget
    transport: SourceRouteTransportProtocol
    reference_samples: tf.Tensor
    measure_convention: MeasureConvention
    density_components: SourceRouteSequentialDensityComponents
    previous_marginal_keep_axes: tuple[int, ...] | None = None
    previous_marginal_input_axes: tuple[int, ...] | None = None
    storage_kind: str = "source_transport_object"
    transition_interface: str = "sample_propagation"

    def __post_init__(self) -> None:
        if not isinstance(self.target, SourceRouteTarget):
            raise TypeError("target must be SourceRouteTarget")
        if not isinstance(self.transport, SourceRouteTransportProtocol):
            raise TypeError("transport must be SourceRouteTransportProtocol")
        assert_density_matches_mass(self.measure_convention)
        if not isinstance(self.density_components, SourceRouteSequentialDensityComponents):
            raise TypeError("density_components must be SourceRouteSequentialDensityComponents")
        reference = tf.convert_to_tensor(self.reference_samples, dtype=tf.float64)
        if reference.shape.rank != 2:
            raise ValueError(f"reference_samples: {HighDimStatus.INVALID_SHAPE.value}")
        if int(reference.shape[0]) != self.target.coordinate_frame.dimension:
            raise ValueError(f"reference_samples: {HighDimStatus.INVALID_SHAPE.value}")
        if int(reference.shape[1]) <= 0:
            raise ValueError("reference_samples must contain at least one column")
        assert_tf_float64("reference_samples", reference)
        if not bool(tf.reduce_all(tf.math.is_finite(reference)).numpy()):
            raise ValueError(f"reference_samples: {HighDimStatus.NONFINITE_VALUE.value}")
        keep_axes = (
            None
            if self.previous_marginal_keep_axes is None
            else tuple(int(axis) for axis in self.previous_marginal_keep_axes)
        )
        input_axes = (
            None
            if self.previous_marginal_input_axes is None
            else tuple(int(axis) for axis in self.previous_marginal_input_axes)
        )
        if self.target.time_index == 1:
            if keep_axes is not None:
                raise ValueError("t=1 must not declare previous_marginal_keep_axes")
            if input_axes is not None:
                raise ValueError("t=1 must not declare previous_marginal_input_axes")
        else:
            if keep_axes is None:
                raise ValueError("t>1 requires previous_marginal_keep_axes")
            if input_axes is None:
                raise ValueError("t>1 requires previous_marginal_input_axes")
            if not keep_axes:
                raise ValueError("previous_marginal_keep_axes must be nonempty")
            if tuple(sorted(keep_axes)) != keep_axes or len(set(keep_axes)) != len(keep_axes):
                raise ValueError("previous_marginal_keep_axes must be unique and increasing")
            if any(axis < 0 for axis in keep_axes):
                raise ValueError("previous_marginal_keep_axes must be nonnegative")
            if keep_axes != tuple(range(len(keep_axes))):
                raise ValueError(
                    "source previous marginalization requires prefix keep axes"
                )
            if len(input_axes) != len(keep_axes):
                raise ValueError(
                    "previous_marginal_input_axes must match keep_axes length"
                )
            if tuple(sorted(input_axes)) != input_axes or len(set(input_axes)) != len(input_axes):
                raise ValueError("previous_marginal_input_axes must be unique and increasing")
            if any(axis < 0 for axis in input_axes):
                raise ValueError("previous_marginal_input_axes must be nonnegative")
            if input_axes[-1] >= self.target.coordinate_frame.dimension:
                raise ValueError(
                    f"previous_marginal_input_axes: {HighDimStatus.INVALID_SHAPE.value}"
                )
        _validate_route_storage_contract(
            route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind=str(self.storage_kind),
            transition_interface=str(self.transition_interface),
        )
        object.__setattr__(self, "reference_samples", reference)
        object.__setattr__(self, "previous_marginal_keep_axes", keep_axes)
        object.__setattr__(self, "previous_marginal_input_axes", input_axes)
        object.__setattr__(self, "storage_kind", str(self.storage_kind))
        object.__setattr__(self, "transition_interface", str(self.transition_interface))

    @property
    def time_index(self) -> int:
        return self.target.time_index

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSequentialStepSpec",
            "time_index": int(self.time_index),
            "target": self.target.manifest_payload(),
            "transport": self.transport.manifest_payload(),
            "reference_samples": self.reference_samples,
            "density_components": self.density_components.manifest_payload(),
            "measure_convention": {
                "density_measure": self.measure_convention.density_measure.value,
                "mass_measure": self.measure_convention.mass_measure.value,
                "reference_weight_name": self.measure_convention.reference_weight_name,
                "physical_coordinate_name": self.measure_convention.physical_coordinate_name,
                "reference_coordinate_name": self.measure_convention.reference_coordinate_name,
                "dtype_name": self.measure_convention.dtype_name,
            },
            "previous_marginal_keep_axes": self.previous_marginal_keep_axes,
            "previous_marginal_input_axes": self.previous_marginal_input_axes,
            "storage_kind": self.storage_kind,
            "transition_interface": self.transition_interface,
        }


@dataclass(frozen=True)
class SourceRouteSequentialStepResult:
    """One step of the fixed-HMC source-route sequential loop."""

    spec: SourceRouteSequentialStepSpec
    target: SourceRouteTarget
    retained_samples: SourceRouteRetainedSampleResult
    retained_object: SourceRouteRetainedObject
    previous_retained_object: SourceRouteRetainedObject | None
    previous_marginal_density: SourceRoutePreviousMarginalDensityResult | None

    def __post_init__(self) -> None:
        if not isinstance(self.spec, SourceRouteSequentialStepSpec):
            raise TypeError("spec must be SourceRouteSequentialStepSpec")
        if not isinstance(self.target, SourceRouteTarget):
            raise TypeError("target must be SourceRouteTarget")
        if self.target.time_index != self.spec.time_index:
            raise ValueError("target time_index must match spec")
        if not isinstance(self.retained_samples, SourceRouteRetainedSampleResult):
            raise TypeError("retained_samples must be SourceRouteRetainedSampleResult")
        if not isinstance(self.retained_object, SourceRouteRetainedObject):
            raise TypeError("retained_object must be SourceRouteRetainedObject")
        if (
            self.retained_object.sample_diagnostics.sample_count
            != self.retained_samples.diagnostics.sample_count
            or self.retained_object.sample_diagnostics.enhancement_attempts
            != self.retained_samples.diagnostics.enhancement_attempts
        ):
            raise ValueError("retained_object diagnostics must match retained_samples")
        tf.debugging.assert_near(
            self.retained_object.sample_diagnostics.effective_sample_size,
            self.retained_samples.diagnostics.effective_sample_size,
            atol=1e-10,
        )
        tf.debugging.assert_near(
            self.retained_object.normalizer.log_transport_normalizer,
            self.retained_samples.normalizer.log_transport_normalizer,
            atol=1e-10,
        )
        tf.debugging.assert_near(
            self.retained_object.normalizer.shift_constant,
            self.retained_samples.normalizer.shift_constant,
            atol=1e-10,
        )
        if (
            self.retained_object.normalizer.log_abs_det_policy
            != self.retained_samples.normalizer.log_abs_det_policy
        ):
            raise ValueError("retained_object normalizer must match retained_samples")
        if self.spec.time_index == 1:
            if self.previous_retained_object is not None:
                raise ValueError("t=1 cannot consume a previous retained object")
            if self.previous_marginal_density is not None:
                raise ValueError("t=1 cannot have a previous marginal density")
        else:
            if not isinstance(self.previous_retained_object, SourceRouteRetainedObject):
                raise TypeError("t>1 requires a previous retained object")
            if not isinstance(
                self.previous_marginal_density,
                SourceRoutePreviousMarginalDensityResult,
            ):
                raise TypeError("t>1 requires a previous marginal density")
            if (
                self.previous_marginal_density.previous_retained_object
                is not self.previous_retained_object
            ):
                raise ValueError("previous marginal density must use previous retained object")
        if self.retained_object.samples.shape != self.retained_samples.retained_batch.samples.shape:
            raise ValueError(f"retained_object samples: {HighDimStatus.INVALID_SHAPE.value}")
        tf.debugging.assert_near(
            self.retained_object.samples,
            self.retained_samples.retained_batch.samples,
            atol=1e-10,
        )
        tf.debugging.assert_near(
            self.retained_object.log_weights,
            self.retained_samples.retained_batch.log_weights,
            atol=1e-10,
        )

    @property
    def time_index(self) -> int:
        return self.spec.time_index

    @property
    def normalizer_increment(self) -> tf.Tensor:
        return self.retained_samples.normalizer.log_increment()

    def manifest_payload(self) -> Mapping[str, object]:
        previous_hash = (
            None
            if self.previous_retained_object is None
            else self.previous_retained_object.branch_identity.hash.value
        )
        previous_marginal_density_payload = (
            None
            if self.previous_marginal_density is None
            else self.previous_marginal_density.manifest_payload()
        )
        return {
            "family": "SourceRouteSequentialStepResult",
            "time_index": int(self.time_index),
            "normalizer_increment": self.normalizer_increment,
            "previous_retained_hash": previous_hash,
            "previous_marginal_keep_axes": self.spec.previous_marginal_keep_axes,
            "previous_marginal_input_axes": self.spec.previous_marginal_input_axes,
            "previous_marginal_density": previous_marginal_density_payload,
            "spec": self.spec.manifest_payload(),
            "target": self.target.manifest_payload(),
            "retained_samples": self.retained_samples.manifest_payload(),
            "retained_object_hash": self.retained_object.branch_identity.hash.value,
        }


@dataclass(frozen=True)
class SourceRouteSequentialResult:
    """Fixed-HMC replayable sequential source-route result."""

    steps: tuple[SourceRouteSequentialStepResult, ...]
    branch_audit: SourceRouteImplementationAudit
    sequential_status: str = "sequential_fixed_hmc_source_loop"

    def __post_init__(self) -> None:
        steps = tuple(self.steps)
        if len(steps) < 2:
            raise ValueError("sequential source loop requires at least two steps")
        if not all(isinstance(step, SourceRouteSequentialStepResult) for step in steps):
            raise TypeError("steps must contain SourceRouteSequentialStepResult")
        expected_times = tuple(range(1, len(steps) + 1))
        actual_times = tuple(step.time_index for step in steps)
        if actual_times != expected_times:
            raise ValueError("sequential steps must be consecutive starting at t=1")
        if not isinstance(self.branch_audit, SourceRouteImplementationAudit):
            raise TypeError("branch_audit must be SourceRouteImplementationAudit")
        if self.branch_audit.status != "PASS_SOURCE_ROUTE_OPERATION_COVERAGE":
            raise ValueError("branch_audit must pass source-route operation coverage")
        if str(self.sequential_status) != "sequential_fixed_hmc_source_loop":
            raise ValueError("sequential_status must be sequential_fixed_hmc_source_loop")
        object.__setattr__(self, "steps", steps)
        object.__setattr__(self, "sequential_status", str(self.sequential_status))

    @property
    def log_marginal_likelihood(self) -> tf.Tensor:
        increments = [step.normalizer_increment for step in self.steps]
        return tf.reduce_sum(tf.stack(increments))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSequentialResult",
            "sequential_status": self.sequential_status,
            "step_count": len(self.steps),
            "log_marginal_likelihood": self.log_marginal_likelihood,
            "branch_audit": self.branch_audit.manifest_payload(),
            "steps": [step.manifest_payload() for step in self.steps],
        }


@dataclass(frozen=True)
class P58M9SourceRoutePipelineReadiness:
    """Phase-9 launch-readiness gate for the author SIR source-route pipeline."""

    status: str
    blockers: tuple[str, ...]
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        allowed = {
            P58_M9_READY_STATUS,
            P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS,
            P58_M9_BLOCK_SOURCE_DRIFT_STATUS,
            P58_M9_BLOCK_HUMAN_REQUIRED_STATUS,
        }
        if status not in allowed:
            raise ValueError("unknown P58 M9 readiness status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P58_M9_READY_STATUS and blockers:
            raise ValueError("ready status cannot carry blockers")
        if status != P58_M9_READY_STATUS and not blockers:
            raise ValueError("blocked status requires at least one blocker")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    @property
    def ready_for_phase9_launch(self) -> bool:
        return self.status == P58_M9_READY_STATUS

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P58M9SourceRoutePipelineReadiness",
            "status": self.status,
            "ready_for_phase9_launch": self.ready_for_phase9_launch,
            "blockers": self.blockers,
            "manifest": self.manifest,
            "required_assembly_flags": P58_M9_REQUIRED_ASSEMBLY_FLAGS,
            "allowed_comparator_tiers": P58_M9_ALLOWED_COMPARATOR_TIERS,
            "nonclaims": (
                "no d18 correctness without comparator-tier result",
                "no d50 or d100 scaling claim",
                "no HMC readiness",
                "no adaptive Zhao-Cui parity",
                "no S&P 500 reproduction",
            ),
        }


def p58_m9_source_route_pipeline_readiness(
    manifest: Mapping[str, object],
) -> P58M9SourceRoutePipelineReadiness:
    """Fail-closed launch gate for P58/P57-M9 source-route execution.

    The gate is intentionally metadata-only.  It prevents Phase 9 launch from
    being claimed when the available evidence is a contract-double loop, UKF or
    memory proxy, old local/operator/all-grid route, or unassembled source
    surface.  It does not build the missing d=18 pipeline.
    """

    if not isinstance(manifest, Mapping):
        raise TypeError("manifest must be a mapping")
    data = dict(manifest)
    blockers: list[str] = []
    drift: list[str] = []

    target_id = str(data.get("target_id", ""))
    pipeline_kind = str(data.get("pipeline_kind", ""))
    if target_id != P58_M9_AUTHOR_SIR_TARGET_ID:
        blockers.append("missing_author_sir_d18_target")
    if pipeline_kind != P58_M9_SOURCE_ROUTE_PIPELINE_KIND:
        blockers.append("missing_author_sir_fixed_ttsirt_source_route_pipeline")

    for flag in P58_M9_REQUIRED_ASSEMBLY_FLAGS:
        if data.get(flag) is not True:
            blockers.append(f"missing_{flag}")

    comparator_tier = str(data.get("m9_comparator_tier", ""))
    if comparator_tier not in P58_M9_ALLOWED_COMPARATOR_TIERS:
        blockers.append("missing_valid_m9_comparator_tier")

    rank_policy_status = str(data.get("rank_policy_status", ""))
    if rank_policy_status != "PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION":
        blockers.append("missing_p57_m7_rank_policy_pass")

    if data.get("preconditioned_route_required") is True:
        preconditioned_status = str(data.get("preconditioned_route_status", ""))
        if preconditioned_status != "PASS_P57_M8_PRECONDITIONED_ALGORITHM5":
            blockers.append("missing_required_preconditioned_route_pass")

    if data.get("uses_contract_test_double") is True:
        drift.append("contract_test_double_cannot_launch_phase9")
    if data.get("uses_ukf_as_comparator") is True:
        drift.append("ukf_proxy_cannot_launch_phase9")
    if data.get("uses_rank_memory_proxy_as_comparator") is True:
        drift.append("rank_memory_proxy_cannot_launch_phase9")

    route_class = str(data.get("route_class", ""))
    storage_kind = str(data.get("storage_kind", ""))
    transition_interface = str(data.get("transition_interface", ""))
    if route_class and route_class != "fixed_ttsirt_source_route":
        drift.append("route_class_is_not_fixed_ttsirt_source_route")
    for marker in SOURCE_ROUTE_FORBIDDEN_DRIFT_MARKERS:
        if marker in (route_class, storage_kind, transition_interface):
            drift.append(f"forbidden_source_route_marker:{marker}")

    if drift:
        return P58M9SourceRoutePipelineReadiness(
            status=P58_M9_BLOCK_SOURCE_DRIFT_STATUS,
            blockers=tuple(drift + blockers),
            manifest=data,
        )
    if blockers:
        return P58M9SourceRoutePipelineReadiness(
            status=P58_M9_BLOCK_MISSING_ASSEMBLY_STATUS,
            blockers=tuple(blockers),
            manifest=data,
        )
    return P58M9SourceRoutePipelineReadiness(
        status=P58_M9_READY_STATUS,
        blockers=(),
        manifest=data,
    )


@dataclass(frozen=True)
class P59AuthorSIRRouteDecisionResult:
    """P59-9c source-cited full/preconditioned route decision gate."""

    status: str
    blockers: tuple[str, ...]
    route_decision: str
    preconditioned_route_required: bool
    preconditioned_route_status: str
    source_anchors: tuple[str, ...]
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (P59_9C_PASS_STATUS, P59_9C_BLOCK_STATUS):
            raise ValueError("unknown P59-9c status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P59_9C_PASS_STATUS and blockers:
            raise ValueError("P59-9c pass cannot carry blockers")
        if status == P59_9C_BLOCK_STATUS and not blockers:
            raise ValueError("P59-9c block requires at least one blocker")
        route_decision = str(self.route_decision)
        allowed_decisions = {
            P59_9C_FULL_ROUTE_SELECTED,
            P59_9C_PRECONDITIONED_ROUTE_REQUIRED,
            P59_9C_PRECONDITIONED_ROUTE_DEFERRED,
            P59_9C_ROUTE_DECISION_BLOCKED,
        }
        if route_decision not in allowed_decisions:
            raise ValueError("unknown P59-9c route decision")
        preconditioned_required = bool(self.preconditioned_route_required)
        if route_decision == P59_9C_FULL_ROUTE_SELECTED and preconditioned_required:
            raise ValueError("full route decision cannot require preconditioned route")
        if (
            route_decision == P59_9C_PRECONDITIONED_ROUTE_REQUIRED
            and not preconditioned_required
        ):
            raise ValueError("preconditioned route decision must require preconditioned route")
        if (
            status == P59_9C_PASS_STATUS
            and preconditioned_required
            and str(self.preconditioned_route_status) != P57_M8_PRECONDITIONED_PASS_STATUS
        ):
            raise ValueError("P59-9c pass with preconditioned route requires P57-M8 pass")
        anchors = tuple(str(anchor) for anchor in self.source_anchors)
        if not anchors:
            raise ValueError("P59-9c source anchors must be nonempty")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "route_decision", route_decision)
        object.__setattr__(
            self, "preconditioned_route_required", preconditioned_required
        )
        object.__setattr__(
            self, "preconditioned_route_status", str(self.preconditioned_route_status)
        )
        object.__setattr__(self, "source_anchors", anchors)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    @property
    def unlocks_step_spec_assembly(self) -> bool:
        return self.status == P59_9C_PASS_STATUS

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P59AuthorSIRRouteDecisionResult",
            "status": self.status,
            "blockers": self.blockers,
            "route_decision": self.route_decision,
            "preconditioned_route_required": self.preconditioned_route_required,
            "preconditioned_route_status": self.preconditioned_route_status,
            "unlocks_step_spec_assembly": self.unlocks_step_spec_assembly,
            "source_anchors": self.source_anchors,
            "manifest": self.manifest,
        }


def p59_author_sir_route_decision(
    *,
    source_root: str | Path = "third_party/audit/zhao_cui_tensor_ssm_p10/source",
    target_id: str = P58_M9_AUTHOR_SIR_TARGET_ID,
) -> P59AuthorSIRRouteDecisionResult:
    """Decide whether author Austria SIR Phase 9 uses ``full_sol`` or ``pre_sol``.

    The decision is intentionally source-backed and fail-closed.  For the
    author SIR row, ``eg3_sir/mainscript.m`` constructs ``full_sol``; therefore
    P59-9b and P59-9d may assemble the full source route without requiring the
    P57-M8 preconditioned surface.  If the source files are absent or
    contradictory, this helper blocks instead of guessing.
    """

    root = Path(source_root)
    files = {
        "mainscript": root / "eg3_sir" / "mainscript.m",
        "full_sol": root / "models" / "full_sol.m",
        "pre_sol": root / "models" / "pre_sol.m",
        "precond": root / "models" / "tensordot" / "precond.m",
    }
    blockers: list[str] = []
    texts: dict[str, str] = {}
    for label, path in files.items():
        try:
            texts[label] = path.read_text(encoding="utf-8")
        except OSError:
            blockers.append(f"missing_source_file:{label}")
            texts[label] = ""

    if str(target_id) != P58_M9_AUTHOR_SIR_TARGET_ID:
        blockers.append("unsupported_target_id_for_p59_9c_author_sir_route")

    mainscript = texts["mainscript"]
    full_source = texts["full_sol"]
    pre_source = texts["pre_sol"]
    precond_source = texts["precond"]
    mainscript_selects_full = (
        "full_sol(myModel" in mainscript and "solve(mySol_unbounded)" in mainscript
    )
    mainscript_selects_pre = "pre_sol(" in mainscript
    full_route_boundary = (
        "classdef full_sol < Y_sol" in full_source
        and "model.d+2*model.m" in full_source
        and "eval_irt(sol.SIRTs{t}" in full_source
        and "eval_pdf(sol.SIRTs{t}, r)" in full_source
    )
    pre_route_boundary = (
        "classdef pre_sol < full_sol" in pre_source
        and "function sol = pre_sol" in pre_source
        and "sol.precond" in pre_source
    )
    precond_boundary = (
        "function [C, Sigmak] = precond" in precond_source
        and "Sigma1\\Sigma2full" in precond_source
        and "Sigmak" in precond_source
    )

    if not mainscript_selects_full:
        blockers.append("author_sir_mainscript_does_not_select_full_sol")
    if mainscript_selects_pre:
        blockers.append("author_sir_mainscript_also_mentions_pre_sol")
    if not full_route_boundary:
        blockers.append("full_sol_source_boundary_not_verified")
    if not pre_route_boundary:
        blockers.append("pre_sol_boundary_not_verified")
    if not precond_boundary:
        blockers.append("precond_boundary_not_verified")

    evidence = {
        "mainscript_selects_full_sol": mainscript_selects_full,
        "mainscript_selects_pre_sol": mainscript_selects_pre,
        "full_sol_source_boundary_verified": full_route_boundary,
        "pre_sol_boundary_verified": pre_route_boundary,
        "precond_boundary_verified": precond_boundary,
    }
    if blockers:
        return _p59_9c_block_result(blockers=tuple(blockers), evidence=evidence)

    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9c",
        "artifact_role": "source_route_decision_gate",
        "route_decision": P59_9C_FULL_ROUTE_SELECTED,
        "source_selected_matlab_constructor": "full_sol",
        "source_selected_python_route": "full_route",
        "route_class": "fixed_ttsirt_source_route",
        "preconditioned_route_required": False,
        "preconditioned_route_status": P59_9C_NOT_REQUIRED_PRECONDITIONED_STATUS,
        "source_evidence": evidence,
        "source_anchors": _P59_9C_AUTHOR_SIR_SOURCE_ANCHORS,
        "unlocks_after_consumed_by": ("P59-9b", "P59-9d"),
        "fail_closed_rule": (
            "P59-9b and P59-9d must block if this route-decision artifact is absent "
            "or if route_decision is not full_route_selected."
        ),
        "nonclaims": (
            "no Phase-9 validation launch",
            "no d18 filtering accuracy claim",
            "no preconditioned route claim for author SIR",
            "no UKF route substitute",
            "no adaptive Zhao-Cui parity claim",
        ),
    }
    return P59AuthorSIRRouteDecisionResult(
        status=P59_9C_PASS_STATUS,
        blockers=(),
        route_decision=P59_9C_FULL_ROUTE_SELECTED,
        preconditioned_route_required=False,
        preconditioned_route_status=P59_9C_NOT_REQUIRED_PRECONDITIONED_STATUS,
        source_anchors=_P59_9C_AUTHOR_SIR_SOURCE_ANCHORS,
        manifest=manifest,
    )


def _p59_9c_block_result(
    *,
    blockers: tuple[str, ...],
    evidence: Mapping[str, object],
) -> P59AuthorSIRRouteDecisionResult:
    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9c",
        "artifact_role": "blocked_source_route_decision_gate",
        "route_decision": P59_9C_ROUTE_DECISION_BLOCKED,
        "preconditioned_route_required": False,
        "preconditioned_route_status": "undecided",
        "blockers": tuple(blockers),
        "source_evidence": dict(evidence),
        "source_anchors": _P59_9C_AUTHOR_SIR_SOURCE_ANCHORS,
        "fail_closed_rule": "P59-9b and P59-9d must not proceed.",
        "nonclaims": (
            "no Phase-9 validation launch",
            "no d18 filtering accuracy claim",
        ),
    }
    return P59AuthorSIRRouteDecisionResult(
        status=P59_9C_BLOCK_STATUS,
        blockers=tuple(blockers),
        route_decision=P59_9C_ROUTE_DECISION_BLOCKED,
        preconditioned_route_required=False,
        preconditioned_route_status="undecided",
        source_anchors=_P59_9C_AUTHOR_SIR_SOURCE_ANCHORS,
        manifest=manifest,
    )


@dataclass(frozen=True)
class P59AuthorSIR36DTargetFitPrepResult:
    """Bounded author-SIR source-route 36D target/fit preparation artifact."""

    status: str
    blockers: tuple[str, ...]
    target_dimension: int
    state_dimension: int
    parameter_dimension: int
    time_index: int
    sample_count: int
    negative_log_values: tf.Tensor
    shift_constant: tf.Tensor
    fit_status: str
    fit_branch_hash: str | None
    density_branch_hash: str | None
    transport_manifest: Mapping[str, object] | None
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (P59_9A_PASS_STATUS, P59_9A_BLOCK_STATUS):
            raise ValueError("unknown P59-9a status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P59_9A_PASS_STATUS and blockers:
            raise ValueError("P59-9a pass cannot carry blockers")
        if status == P59_9A_BLOCK_STATUS and not blockers:
            raise ValueError("P59-9a block requires at least one blocker")
        values = tf.convert_to_tensor(self.negative_log_values, dtype=tf.float64)
        shift = tf.convert_to_tensor(self.shift_constant, dtype=tf.float64)
        if values.shape.rank != 1 or int(values.shape[0]) != int(self.sample_count):
            raise ValueError(f"negative_log_values: {HighDimStatus.INVALID_SHAPE.value}")
        if shift.shape.rank != 0:
            raise ValueError(f"shift_constant: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(
            tf.reduce_all(tf.math.is_finite(values)).numpy()
            and tf.math.is_finite(shift).numpy()
        ):
            raise ValueError(f"P59AuthorSIR36DTargetFitPrepResult: {HighDimStatus.NONFINITE_VALUE.value}")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "target_dimension", int(self.target_dimension))
        object.__setattr__(self, "state_dimension", int(self.state_dimension))
        object.__setattr__(self, "parameter_dimension", int(self.parameter_dimension))
        object.__setattr__(self, "time_index", int(self.time_index))
        object.__setattr__(self, "sample_count", int(self.sample_count))
        object.__setattr__(self, "negative_log_values", values)
        object.__setattr__(self, "shift_constant", shift)
        object.__setattr__(self, "fit_status", str(self.fit_status))
        object.__setattr__(
            self,
            "fit_branch_hash",
            None if self.fit_branch_hash is None else str(self.fit_branch_hash),
        )
        object.__setattr__(
            self,
            "density_branch_hash",
            None if self.density_branch_hash is None else str(self.density_branch_hash),
        )
        object.__setattr__(
            self,
            "transport_manifest",
            None if self.transport_manifest is None else freeze_mapping(self.transport_manifest),
        )
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P59AuthorSIR36DTargetFitPrepResult",
            "status": self.status,
            "blockers": self.blockers,
            "target_dimension": int(self.target_dimension),
            "state_dimension": int(self.state_dimension),
            "parameter_dimension": int(self.parameter_dimension),
            "time_index": int(self.time_index),
            "sample_count": int(self.sample_count),
            "negative_log_values": self.negative_log_values,
            "shift_constant": self.shift_constant,
            "fit_status": self.fit_status,
            "fit_branch_hash": self.fit_branch_hash,
            "density_branch_hash": self.density_branch_hash,
            "transport_manifest": self.transport_manifest,
            "manifest": self.manifest,
        }


@dataclass(frozen=True)
class P59AuthorSIRStepSpecAssemblyResult:
    """P59-9b bounded author-SIR source-route step-spec assembly artifact."""

    status: str
    blockers: tuple[str, ...]
    route_decision: P59AuthorSIRRouteDecisionResult
    prep_result: P59AuthorSIR36DTargetFitPrepResult | None
    step_specs: tuple[SourceRouteSequentialStepSpec, ...]
    sequential_result: SourceRouteSequentialResult | None
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (P59_9B_PASS_STATUS, P59_9B_BLOCK_STATUS):
            raise ValueError("unknown P59-9b status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P59_9B_PASS_STATUS and blockers:
            raise ValueError("P59-9b pass cannot carry blockers")
        if status == P59_9B_BLOCK_STATUS and not blockers:
            raise ValueError("P59-9b block requires at least one blocker")
        if not isinstance(self.route_decision, P59AuthorSIRRouteDecisionResult):
            raise TypeError("route_decision must be P59AuthorSIRRouteDecisionResult")
        if self.prep_result is not None and not isinstance(
            self.prep_result,
            P59AuthorSIR36DTargetFitPrepResult,
        ):
            raise TypeError("prep_result must be P59AuthorSIR36DTargetFitPrepResult")
        specs = tuple(self.step_specs)
        if status == P59_9B_PASS_STATUS:
            if len(specs) < 2:
                raise ValueError("P59-9b pass requires at least two step specs")
            if not all(isinstance(spec, SourceRouteSequentialStepSpec) for spec in specs):
                raise TypeError("step_specs must contain SourceRouteSequentialStepSpec")
            if self.sequential_result is None:
                raise ValueError("P59-9b pass requires sequential_result")
            if not isinstance(self.sequential_result, SourceRouteSequentialResult):
                raise TypeError("sequential_result must be SourceRouteSequentialResult")
        elif self.sequential_result is not None:
            raise ValueError("P59-9b block cannot carry sequential_result")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "step_specs", specs)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    @property
    def ready_for_runner_manifest_path(self) -> bool:
        return self.status == P59_9B_PASS_STATUS

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P59AuthorSIRStepSpecAssemblyResult",
            "status": self.status,
            "blockers": self.blockers,
            "ready_for_runner_manifest_path": self.ready_for_runner_manifest_path,
            "route_decision": self.route_decision.manifest_payload(),
            "prep_result": (
                None if self.prep_result is None else self.prep_result.manifest_payload()
            ),
            "step_specs": [spec.manifest_payload() for spec in self.step_specs],
            "sequential_result": (
                None
                if self.sequential_result is None
                else self.sequential_result.manifest_payload()
            ),
            "manifest": self.manifest,
        }


@dataclass(frozen=True)
class P59AuthorSIRRunnerManifestResult:
    """P59-9d runner path plus P58 readiness manifest artifact."""

    status: str
    blockers: tuple[str, ...]
    assembly_result: P59AuthorSIRStepSpecAssemblyResult | None
    readiness: P58M9SourceRoutePipelineReadiness
    manifest_path: str
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (P59_9D_PASS_STATUS, P59_9D_BLOCK_STATUS):
            raise ValueError("unknown P59-9d status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P59_9D_PASS_STATUS and blockers:
            raise ValueError("P59-9d pass cannot carry blockers")
        if status == P59_9D_BLOCK_STATUS and not blockers:
            raise ValueError("P59-9d block requires at least one blocker")
        if self.assembly_result is not None and not isinstance(
            self.assembly_result,
            P59AuthorSIRStepSpecAssemblyResult,
        ):
            raise TypeError("assembly_result must be P59AuthorSIRStepSpecAssemblyResult")
        if not isinstance(self.readiness, P58M9SourceRoutePipelineReadiness):
            raise TypeError("readiness must be P58M9SourceRoutePipelineReadiness")
        if status == P59_9D_PASS_STATUS:
            if self.readiness.status != P58_M9_READY_STATUS:
                raise ValueError("P59-9d pass requires P58 ready status")
            if self.assembly_result is None:
                raise ValueError("P59-9d pass requires assembly_result")
            if self.assembly_result.status != P59_9B_PASS_STATUS:
                raise ValueError("P59-9d pass requires P59-9b pass")
        if not str(self.manifest_path).strip():
            raise ValueError("manifest_path must be nonempty")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "manifest_path", str(self.manifest_path))
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    @property
    def ready_for_validation_ladder(self) -> bool:
        return self.status == P59_9D_PASS_STATUS and self.readiness.ready_for_phase9_launch

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P59AuthorSIRRunnerManifestResult",
            "status": self.status,
            "blockers": self.blockers,
            "ready_for_validation_ladder": self.ready_for_validation_ladder,
            "manifest_path": self.manifest_path,
            "readiness": self.readiness.manifest_payload(),
            "assembly_result": (
                None
                if self.assembly_result is None
                else self.assembly_result.manifest_payload()
            ),
            "manifest": self.manifest,
        }


@dataclass(frozen=True)
class P59AuthorSIRValidationLadderResult:
    """P59-9e validation-ladder result with explicit tier boundary."""

    status: str
    blockers: tuple[str, ...]
    tier: str
    runner_result: P59AuthorSIRRunnerManifestResult | None
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (P59_9E_D18_EXECUTION_ONLY_PASS_STATUS, P59_9E_BLOCK_STATUS):
            raise ValueError("unknown P59-9e status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P59_9E_D18_EXECUTION_ONLY_PASS_STATUS and blockers:
            raise ValueError("P59-9e pass cannot carry blockers")
        if status == P59_9E_BLOCK_STATUS and not blockers:
            raise ValueError("P59-9e block requires at least one blocker")
        tier = str(self.tier)
        if tier not in P58_M9_ALLOWED_COMPARATOR_TIERS:
            raise ValueError("unknown P59-9e tier")
        if self.runner_result is not None and not isinstance(
            self.runner_result,
            P59AuthorSIRRunnerManifestResult,
        ):
            raise TypeError("runner_result must be P59AuthorSIRRunnerManifestResult")
        if status == P59_9E_D18_EXECUTION_ONLY_PASS_STATUS:
            if tier != "d18_execution_only":
                raise ValueError("only d18_execution_only pass is implemented")
            if self.runner_result is None or self.runner_result.status != P59_9D_PASS_STATUS:
                raise ValueError("P59-9e pass requires P59-9d pass")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "tier", tier)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P59AuthorSIRValidationLadderResult",
            "status": self.status,
            "blockers": self.blockers,
            "tier": self.tier,
            "runner_result": (
                None if self.runner_result is None else self.runner_result.manifest_payload()
            ),
            "manifest": self.manifest,
        }


@dataclass(frozen=True)
class P60AuthorSIRSameRouteRankComparatorResult:
    """P60-2 same-route rank-comparator result with explicit nonclaims."""

    status: str
    blockers: tuple[str, ...]
    low_result: P59AuthorSIRStepSpecAssemblyResult | None
    high_result: P59AuthorSIRStepSpecAssemblyResult | None
    manifest: Mapping[str, object]

    def __post_init__(self) -> None:
        status = str(self.status)
        if status not in (
            P60_D18_RANK_CONVERGENCE_PASS_STATUS,
            P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
        ):
            raise ValueError("unknown P60-2 status")
        blockers = tuple(str(blocker) for blocker in self.blockers)
        if status == P60_D18_RANK_CONVERGENCE_PASS_STATUS and blockers:
            raise ValueError("P60-2 pass cannot carry blockers")
        if status == P60_D18_RANK_CONVERGENCE_BLOCK_STATUS and not blockers:
            raise ValueError("P60-2 block requires at least one blocker")
        for name, value in (
            ("low_result", self.low_result),
            ("high_result", self.high_result),
        ):
            if value is not None and not isinstance(value, P59AuthorSIRStepSpecAssemblyResult):
                raise TypeError(f"{name} must be P59AuthorSIRStepSpecAssemblyResult")
        if status == P60_D18_RANK_CONVERGENCE_PASS_STATUS:
            if self.low_result is None or self.high_result is None:
                raise ValueError("P60-2 pass requires low and high comparator rows")
            if (
                self.low_result.status != P59_9B_PASS_STATUS
                or self.high_result.status != P59_9B_PASS_STATUS
            ):
                raise ValueError("P60-2 pass requires P59-9b pass rows")
        object.__setattr__(self, "status", status)
        object.__setattr__(self, "blockers", blockers)
        object.__setattr__(self, "manifest", freeze_mapping(self.manifest))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "P60AuthorSIRSameRouteRankComparatorResult",
            "status": self.status,
            "blockers": self.blockers,
            "low_result": (
                None if self.low_result is None else self.low_result.manifest_payload()
            ),
            "high_result": (
                None if self.high_result is None else self.high_result.manifest_payload()
            ),
            "manifest": self.manifest,
        }


def p59_author_sir_36d_target_fit_prep(
    *,
    sample_count: int = 6,
    fit_degree: int = 0,
    fit_rank: int = 1,
    ridge: float = 1e-8,
) -> P59AuthorSIR36DTargetFitPrepResult:
    """Build bounded P59-9a author-SIR 36D source-route fit evidence.

    This is deliberately a preparation artifact.  It checks the source-route
    target dimension and finite target/fixed-TT-fit plumbing for the author SIR
    row; it does not claim filtering accuracy or Phase-9 validation success.
    """

    model = zhao_cui_sir_austria_model()
    d = model.parameter_dim()
    m = model.state_dim()
    target_dim = d + 2 * m
    blockers: list[str] = []
    if d != 0:
        blockers.append("author_sir_parameter_dim_not_zero")
    if m != 18:
        blockers.append("author_sir_state_dim_not_18")
    if target_dim != P59_9A_AUTHOR_SIR_TARGET_DIMENSION:
        blockers.append("source_route_target_dimension_not_36")
    if int(sample_count) < 2:
        blockers.append("sample_count_must_be_at_least_2")
    if int(fit_degree) < 0:
        blockers.append("fit_degree_must_be_nonnegative")
    if int(fit_rank) <= 0:
        blockers.append("fit_rank_must_be_positive")
    if blockers:
        return _p59_9a_block_result(
            blockers=tuple(blockers),
            target_dimension=target_dim,
            state_dimension=m,
            parameter_dimension=d,
        )

    observations = model.simulate(final_time=1, seed=5901)[1]
    fit_data = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=int(sample_count),
    )
    coordinate_frame = fit_data.frame
    negative_log_values = fit_data.negative_log_values
    if not bool(tf.reduce_all(tf.math.is_finite(negative_log_values)).numpy()):
        return _p59_9a_block_result(
            blockers=("nonfinite_author_sir_36d_target_values",),
            target_dimension=target_dim,
            state_dimension=m,
            parameter_dimension=d,
            negative_log_values=negative_log_values,
        )

    shift_constant = fit_data.shift_constant
    target_values = fit_data.target_values
    if not bool(tf.reduce_all(tf.math.is_finite(target_values)).numpy()):
        return _p59_9a_block_result(
            blockers=("nonfinite_author_sir_36d_sqrt_target_values",),
            target_dimension=target_dim,
            state_dimension=m,
            parameter_dimension=d,
            negative_log_values=negative_log_values,
            shift_constant=shift_constant,
        )

    convention = _p59_reference_convention()
    product_basis = ProductBasis(
        [
            LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(fit_degree))
            for _ in range(target_dim)
        ],
        convention,
    )
    fit_config = FixedTTFitConfig(
        ranks=_source_route_rank_tuple(target_dim, int(fit_rank)),
        ridge=float(ridge),
        max_sweeps=1,
        sweep_order=tuple(range(target_dim)),
        row_budget=max(int(sample_count), 1),
        column_budget=(int(fit_degree) + 1) * int(fit_rank) * int(fit_rank),
        dense_matrix_byte_budget=2**22,
        normal_matrix_byte_budget=2**24,
        condition_number_warning=1e12,
        condition_number_veto=1e16,
        holdout_tolerance=1e6,
    )
    initial_cores = tuple(
        TTCore(
            _source_route_initial_core_values(
                left_rank=fit_config.ranks[axis],
                basis_dim=int(fit_degree) + 1,
                right_rank=fit_config.ranks[axis + 1],
            )
        )
        for axis in range(target_dim)
    )
    fit_result = FixedTTFitter().fit(
        product_basis=product_basis,
        samples=FixedTTFitSampleBatch(
            points=tf.transpose(fit_data.local_fit_points),
            target_values=target_values,
            weights=fit_data.fit_weights,
        ),
        config=fit_config,
        initial_cores=initial_cores,
        branch_seed="p59-9a-author-sir-36d-bounded-fit",
        measure_convention=convention,
    )
    if fit_result.status is not HighDimStatus.OK:
        return _p59_9a_block_result(
            blockers=(f"fit_status_{fit_result.status.value}",),
            target_dimension=target_dim,
            state_dimension=m,
            parameter_dimension=d,
            negative_log_values=negative_log_values,
            shift_constant=shift_constant,
            fit_status=fit_result.status.value,
            fit_branch_hash=fit_result.branch_hash.value,
        )

    defensive = TensorProductReferenceDensity(product_basis, convention)
    defensive_tau = _p59_author_sir_defensive_tau_tensor()
    density_identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=defensive_tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
    )
    density = SquaredTTDensity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=defensive_tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
        branch_identity=density_identity,
    )
    transport = FixedTTSIRTTransport(
        density=density,
        cdf_config=KRCDFConfig(
            grid_size=5,
            bisection_steps=4,
            monotonicity_tolerance=1e-10,
            bracket_tolerance=1e-10,
            denominator_floor=1e-12,
            max_floor_count=0,
        ),
    )
    transport_manifest = transport.manifest_payload()
    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9a",
        "artifact_role": "bounded_preparation_evidence_only",
        "source_contract_level": "fixed_ttsirt",
        "source_anchors": (
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14-56",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:11-39",
            "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:76-130",
            *_P62_AUTHOR_TTSIRT_DEFENSIVE_TAU_SOURCE_ANCHORS,
            *_P63_AUTHOR_SIR_FIT_DATA_SOURCE_ANCHORS,
        ),
        "fit_data_mode": P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE,
        "fit_data_manifest": fit_data.manifest,
        "defensive_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
        "defensive_tau_source": "author_executable_ttsirt_default",
        "source_declared_tau_unwired": 10.0,
        "source_executable_ttsirt_default_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
        "parameter_dimension": d,
        "state_dimension": m,
        "target_dimension": target_dim,
        "source_target_order": "[theta, x_t, x_{t-1}]",
        "coordinate_frame_dimension": coordinate_frame.dimension,
        "coordinate_frame_log_abs_det": coordinate_frame.log_abs_det(),
        "author_sir_d_plus_2m_dimension_check": target_dim == 36,
        "sample_count": int(sample_count),
        "rank_tuple": fit_config.ranks,
        "fit_degree": int(fit_degree),
        "fit_rank": int(fit_rank),
        "fit_status": fit_result.status.value,
        "fit_branch_hash": fit_result.branch_hash.value,
        "density_branch_hash": density.branch_identity.hash.value,
        "transport_family": transport_manifest["family"],
        "transport_dimension": transport_manifest["dimension"],
        "nonclaims": (
            "no Phase-9 validation launch",
            "no d18 filtering accuracy claim",
            "no same-route rank convergence claim",
            "no d50 or d100 scaling claim",
            "no HMC production readiness claim",
        ),
    }
    return P59AuthorSIR36DTargetFitPrepResult(
        status=P59_9A_PASS_STATUS,
        blockers=(),
        target_dimension=target_dim,
        state_dimension=m,
        parameter_dimension=d,
        time_index=1,
        sample_count=int(sample_count),
        negative_log_values=negative_log_values,
        shift_constant=shift_constant,
        fit_status=fit_result.status.value,
        fit_branch_hash=fit_result.branch_hash.value,
        density_branch_hash=density.branch_identity.hash.value,
        transport_manifest=transport_manifest,
        manifest=manifest,
    )


def _p59_author_sir_source_density_callbacks(model, observation: tf.Tensor):
    theta = tf.zeros([0], dtype=tf.float64)
    y_t = tf.convert_to_tensor(observation, dtype=tf.float64)

    def prior_log_density(prior_points: tf.Tensor) -> tf.Tensor:
        points = tf.convert_to_tensor(prior_points, dtype=tf.float64)
        if points.shape.rank != 2 or int(points.shape[0]) != model.state_dim():
            raise ValueError(f"prior_points: {HighDimStatus.INVALID_SHAPE.value}")
        return model.initial_log_density(theta, tf.transpose(points))

    def transition_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        x_t = tf.transpose(values[: model.state_dim(), :])
        x_previous = tf.transpose(values[model.state_dim() :, :])
        return model.transition_log_density(theta, x_previous, x_t, t=int(time_index))

    def likelihood_log_density(points: tf.Tensor, time_index: int) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        x_t = tf.transpose(values[: model.state_dim(), :])
        return model.observation_log_density(theta, x_t, y_t, t=int(time_index))

    return prior_log_density, transition_log_density, likelihood_log_density


def _p59_author_sir_36d_coordinate_frame(model) -> SourceRouteCoordinateFrame:
    return _p59_author_sir_36d_coordinate_frame_for_time(model, time_index=1)


def _p59_author_sir_uniform_log_weights(sample_count: int) -> tf.Tensor:
    n = int(sample_count)
    if n <= 0:
        raise ValueError("sample_count must be positive")
    return tf.fill(
        [n],
        -tf.math.log(tf.cast(n, tf.float64)),
    )


def _p59_author_sir_prior_sample_batch(
    *,
    model,
    sample_count: int,
    seed: int,
) -> SourceRouteSampleBatch:
    n = int(sample_count)
    if n <= 0:
        raise ValueError("sample_count must be positive")
    generator = tf.random.Generator.from_seed(int(seed))
    initial_chol = tf.linalg.cholesky(model.initial_covariance)
    noise = generator.normal([n, model.state_dim()], dtype=tf.float64)
    x0 = model.initial_mean[tf.newaxis, :] + tf.linalg.matmul(
        noise,
        initial_chol,
        transpose_b=True,
    )
    theta = tf.zeros([model.parameter_dim(), n], dtype=tf.float64)
    samples = tf.concat([theta, tf.transpose(x0)], axis=0)
    return SourceRouteSampleBatch(
        samples=samples,
        log_weights=_p59_author_sir_uniform_log_weights(n),
        time_index=0,
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="author_prior_samples_fixed_seed",
    )


def _p59_author_sir_batch_from_previous_retained_prefix(
    previous_retained_object: SourceRouteRetainedObject,
    *,
    parameter_dim: int,
    state_dim: int,
    time_index: int,
) -> SourceRouteSampleBatch:
    if not isinstance(previous_retained_object, SourceRouteRetainedObject):
        raise TypeError("previous_retained_object must be SourceRouteRetainedObject")
    d = int(parameter_dim)
    m = int(state_dim)
    samples = previous_retained_object.samples[: d + m, :]
    return SourceRouteSampleBatch(
        samples=samples,
        log_weights=_p59_author_sir_uniform_log_weights(int(samples.shape[1])),
        time_index=int(time_index),
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="author_retained_prefix_uniform_weight_fixed_variant",
    )


def _p59_author_sir_source_push_result(
    *,
    model,
    previous_batch: SourceRouteSampleBatch,
    observation: tf.Tensor,
    time_index: int,
    process_noise_seed: int,
) -> SourceRoutePushResult:
    n = previous_batch.sample_count
    m = model.state_dim()
    generator = tf.random.Generator.from_seed(int(process_noise_seed))
    transition_noise = generator.normal([n, m], dtype=tf.float64)
    y_t = tf.convert_to_tensor(observation, dtype=tf.float64)

    def transition_fn(previous_samples: tf.Tensor, step_index: int) -> tf.Tensor:
        values = tf.convert_to_tensor(previous_samples, dtype=tf.float64)
        theta = tf.transpose(values[: model.parameter_dim(), :])
        previous_state = tf.transpose(values[model.parameter_dim() :, :])
        pushed = model.transition_push_from_standard_normal(
            theta,
            previous_state,
            transition_noise,
            t=int(step_index),
        )
        return tf.transpose(pushed)

    def log_likelihood_fn(propagated_samples: tf.Tensor, step_index: int) -> tf.Tensor:
        values = tf.convert_to_tensor(propagated_samples, dtype=tf.float64)
        theta = tf.transpose(values[: model.parameter_dim(), :])
        current_state = tf.transpose(values[model.parameter_dim() :, :])
        return model.observation_log_density(
            theta,
            current_state,
            y_t,
            t=int(step_index),
        )

    return source_route_push_and_augment_samples(
        previous_batch=previous_batch,
        transition_fn=transition_fn,
        log_likelihood_fn=log_likelihood_fn,
        parameter_dim=model.parameter_dim(),
        state_dim=m,
        time_index=int(time_index),
    )


def _p59_author_sir_deterministic_weighted_resample(
    *,
    samples: tf.Tensor,
    log_weights: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    values = tf.convert_to_tensor(samples, dtype=tf.float64)
    weights = tf.exp(normalize_log_weights(log_weights))
    if values.shape.rank != 2 or weights.shape != (int(values.shape[1]),):
        raise ValueError(f"resample inputs: {HighDimStatus.INVALID_SHAPE.value}")
    n = int(values.shape[1])
    positions = (
        tf.cast(tf.range(n), tf.float64) + tf.constant(0.5, dtype=tf.float64)
    ) / tf.cast(n, tf.float64)
    cdf = tf.cumsum(weights)
    cdf = tf.concat(
        [cdf[:-1], tf.ones([1], dtype=tf.float64)],
        axis=0,
    )
    indices = tf.searchsorted(cdf, positions, side="left", out_type=tf.int32)
    indices = tf.minimum(indices, tf.fill([n], n - 1))
    return tf.gather(values, indices, axis=1), indices


def _p59_author_sir_source_fit_data_for_step(
    *,
    model,
    observations: tf.Tensor,
    time_index: int,
    fit_sample_count: int,
    previous_retained_object: SourceRouteRetainedObject | None = None,
) -> _P59AuthorSIRSourceFitData:
    t = int(time_index)
    n = int(fit_sample_count)
    if t < 1:
        raise ValueError("time_index must be positive")
    if n < 2:
        raise ValueError("fit_sample_count must be at least 2")
    d = model.parameter_dim()
    m = model.state_dim()
    if t == 1:
        previous_batch = _p59_author_sir_prior_sample_batch(
            model=model,
            sample_count=n,
            seed=6301,
        )
        previous_for_density = None
    else:
        if previous_retained_object is None:
            raise TypeError("t>1 requires previous_retained_object")
        previous_batch = _p59_author_sir_batch_from_previous_retained_prefix(
            previous_retained_object,
            parameter_dim=d,
            state_dim=m,
            time_index=t - 1,
        )
        previous_for_density = previous_retained_object
    if previous_batch.sample_count != n:
        raise ValueError("source_fit_data_previous_batch_count_mismatch")
    push = _p59_author_sir_source_push_result(
        model=model,
        previous_batch=previous_batch,
        observation=tf.convert_to_tensor(observations[t], dtype=tf.float64),
        time_index=t,
        process_noise_seed=6400 + t,
    )
    frame = source_route_recenter(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
        expansion_factor=P63_AUTHOR_SIR_EXPANSION_FACTOR,
        covariance_jitter=1e-5,
        use_quantile_scale=True,
    )
    resampled, resample_indices = _p59_author_sir_deterministic_weighted_resample(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
    )
    local_unclipped = tf.linalg.solve(
        frame.matrix,
        resampled - frame.mu[:, tf.newaxis],
    )
    clipped_mask = tf.abs(local_unclipped) > tf.constant(1.0, dtype=tf.float64)
    clip_fraction = tf.reduce_mean(tf.cast(clipped_mask, tf.float64))
    if bool((clip_fraction >= 1.0).numpy()):
        raise ValueError("source_fit_data_all_local_entries_clipped")
    local_fit_points = tf.clip_by_value(local_unclipped, -1.0, 1.0)
    physical_fit_points = (
        tf.linalg.matmul(frame.matrix, local_fit_points)
        + frame.mu[:, tf.newaxis]
    )
    prior_log_density, transition_log_density, likelihood_log_density = (
        _p59_author_sir_source_density_callbacks(model, observations[t])
    )
    components = SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_log_density,
        prior_log_density_fn=prior_log_density if t == 1 else None,
    )
    negative_log_physical = components.negative_log_physical_density(
        physical_points=physical_fit_points,
        time_index=t,
        previous_retained_object=previous_for_density,
    )
    local_negative_log = negative_log_physical - frame.log_abs_det()
    shift = tf.reduce_min(local_negative_log)
    shifted = source_route_shifted_negative_log_target(
        negative_log_target=local_negative_log,
        shift_constant=shift,
    )
    target_values = tf.exp(-0.5 * shifted)
    if not bool(tf.reduce_all(tf.math.is_finite(target_values)).numpy()):
        raise ValueError("nonfinite_source_fit_target_values")
    manifest = {
        "fit_data_mode": P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE,
        "fit_data_source": "pushed_weighted_augmented_samples",
        "coordinate_frame_source": "source_computeL_weighted_augmented_samples",
        "fixed_variant_resampling": P63_AUTHOR_SIR_FIXED_VARIANT_RESAMPLING,
        "source_anchors": _P63_AUTHOR_SIR_FIT_DATA_SOURCE_ANCHORS,
        "time_index": t,
        "fit_sample_count": n,
        "source_push_sample_origin": push.augmented_batch.sample_origin,
        "source_push_ess": push.diagnostics.effective_sample_size,
        "source_push_weight_policy": (
            "uniform previous weights then observation likelihood update"
        ),
        "resample_indices": resample_indices,
        "expansion_factor": P63_AUTHOR_SIR_EXPANSION_FACTOR,
        "coordinate_frame_log_abs_det": frame.log_abs_det(),
        "local_clip_fraction": clip_fraction,
        "local_max_abs_before_clip": tf.reduce_max(tf.abs(local_unclipped)),
        "target_value_min": tf.reduce_min(target_values),
        "target_value_max": tf.reduce_max(target_values),
        "nonclaims": (
            "deterministic fixed-variant replacement for MATLAB random datasample",
            "bounded local basis clips fit data when needed",
            "no AlgebraicMapping(1) parity claim",
            "no adaptive Zhao-Cui parity claim",
        ),
    }
    return _P59AuthorSIRSourceFitData(
        time_index=t,
        frame=frame,
        local_fit_points=local_fit_points,
        target_values=target_values,
        negative_log_values=local_negative_log,
        shift_constant=shift,
        fit_weights=tf.ones([n], dtype=tf.float64),
        manifest=manifest,
    )


def _p59_author_sir_36d_coordinate_frame_for_time(
    model,
    *,
    time_index: int,
) -> SourceRouteCoordinateFrame:
    if int(time_index) < 1:
        raise ValueError("time_index must be positive")
    previous = model.initial_mean
    current = model.transition_mean(previous)[0]
    for _ in range(2, int(time_index) + 1):
        previous = current
        current = model.transition_mean(previous)[0]
    center = tf.concat([model.transition_mean(model.initial_mean)[0], model.initial_mean], axis=0)
    if int(time_index) != 1:
        center = tf.concat([current, previous], axis=0)
    scale = tf.concat(
        [
            tf.sqrt(tf.linalg.diag_part(model.process_covariance)),
            tf.sqrt(tf.linalg.diag_part(model.initial_covariance)),
        ],
        axis=0,
    )
    matrix = tf.linalg.diag(scale)
    return SourceRouteCoordinateFrame(
        mu=center,
        matrix=matrix,
        expansion_factor=1.0,
    )


def _p59_author_sir_reference_points(sample_count: int, target_dim: int) -> tf.Tensor:
    columns = []
    base = tf.linspace(
        tf.constant(-0.75, dtype=tf.float64),
        tf.constant(0.75, dtype=tf.float64),
        int(target_dim),
    )
    for index in range(int(sample_count)):
        shift = tf.cast(index, tf.float64) / tf.cast(max(int(sample_count) - 1, 1), tf.float64)
        shifted = tf.math.floormod(base + 0.17 * shift + 1.0, 2.0) - 1.0
        columns.append(shifted)
    return tf.stack(columns, axis=1)


def _p59_reference_convention() -> MeasureConvention:
    return MeasureConvention(
        density_measure=DensityMeasure.REFERENCE_MEASURE,
        mass_measure=MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _p59_9a_block_result(
    *,
    blockers: tuple[str, ...],
    target_dimension: int,
    state_dimension: int,
    parameter_dimension: int,
    negative_log_values: tf.Tensor | None = None,
    shift_constant: tf.Tensor | None = None,
    fit_status: str = "not_attempted",
    fit_branch_hash: str | None = None,
) -> P59AuthorSIR36DTargetFitPrepResult:
    sample_values = (
        tf.zeros([1], dtype=tf.float64)
        if negative_log_values is None
        else tf.convert_to_tensor(negative_log_values, dtype=tf.float64)
    )
    shift = (
        tf.constant(0.0, dtype=tf.float64)
        if shift_constant is None
        else tf.convert_to_tensor(shift_constant, dtype=tf.float64)
    )
    return P59AuthorSIR36DTargetFitPrepResult(
        status=P59_9A_BLOCK_STATUS,
        blockers=tuple(blockers),
        target_dimension=int(target_dimension),
        state_dimension=int(state_dimension),
        parameter_dimension=int(parameter_dimension),
        time_index=1,
        sample_count=int(sample_values.shape[0]),
        negative_log_values=sample_values,
        shift_constant=shift,
        fit_status=str(fit_status),
        fit_branch_hash=fit_branch_hash,
        density_branch_hash=None,
        transport_manifest=None,
        manifest={
            "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
            "pipeline_phase": "P59-9a",
            "artifact_role": "blocked_preparation_evidence",
            "blockers": tuple(blockers),
            "target_dimension": int(target_dimension),
            "state_dimension": int(state_dimension),
            "parameter_dimension": int(parameter_dimension),
            "nonclaims": (
                "no Phase-9 validation launch",
                "no d18 filtering accuracy claim",
            ),
        },
    )


def p59_author_sir_step_spec_assembly(
    *,
    route_decision: P59AuthorSIRRouteDecisionResult | None = None,
    prep_result: P59AuthorSIR36DTargetFitPrepResult | None = None,
    sample_count: int = 3,
    fit_sample_count: int = 6,
    fit_degree: int = 0,
    fit_rank: int = 1,
    ridge: float = 1e-8,
) -> P59AuthorSIRStepSpecAssemblyResult:
    """Assemble bounded two-step P59-9b author-SIR source-route specs."""

    if route_decision is not None and not isinstance(
        route_decision,
        P59AuthorSIRRouteDecisionResult,
    ):
        raise TypeError("route_decision must be P59AuthorSIRRouteDecisionResult")
    if prep_result is not None and not isinstance(
        prep_result,
        P59AuthorSIR36DTargetFitPrepResult,
    ):
        raise TypeError("prep_result must be P59AuthorSIR36DTargetFitPrepResult")

    route = route_decision or p59_author_sir_route_decision()
    prep = prep_result or p59_author_sir_36d_target_fit_prep(
        sample_count=int(fit_sample_count),
        fit_degree=int(fit_degree),
        fit_rank=int(fit_rank),
        ridge=float(ridge),
    )
    blockers: list[str] = []
    if route.status != P59_9C_PASS_STATUS:
        blockers.append("missing_p59_9c_route_decision_pass")
    if route.route_decision != P59_9C_FULL_ROUTE_SELECTED:
        blockers.append("p59_9c_route_not_full_route_selected")
    if route.preconditioned_route_required:
        blockers.append("p59_9b_rewrite_required_for_preconditioned_route")
    if prep.status != P59_9A_PASS_STATUS:
        blockers.append("missing_p59_9a_target_fit_prep_pass")
    if prep.target_dimension != P59_9A_AUTHOR_SIR_TARGET_DIMENSION:
        blockers.append("p59_9a_target_dimension_not_36")
    if prep.transport_manifest is None:
        blockers.append("missing_p59_9a_fixed_ttsirt_transport_manifest")
    elif prep.transport_manifest.get("source_contract_level") != "fixed_ttsirt":
        blockers.append("p59_9a_transport_not_fixed_ttsirt")
    if int(sample_count) <= 0:
        blockers.append("sample_count_must_be_positive")
    if int(fit_sample_count) < 2:
        blockers.append("fit_sample_count_must_be_at_least_2")
    if int(fit_degree) < 0:
        blockers.append("fit_degree_must_be_nonnegative")
    if int(fit_rank) <= 0:
        blockers.append("fit_rank_must_be_positive")
    if blockers:
        return _p59_9b_block_result(
            blockers=tuple(blockers),
            route_decision=route,
            prep_result=prep,
        )

    model = zhao_cui_sir_austria_model()
    d = model.parameter_dim()
    m = model.state_dim()
    target_dim = d + 2 * m
    observations = model.simulate(final_time=2, seed=5901)[1]
    retained_reference = _p59_author_sir_unit_reference_points(
        int(sample_count),
        target_dim,
    )
    convention = _p59_reference_convention()

    prior_log_density, transition_log_density, likelihood_t1 = (
        _p59_author_sir_source_density_callbacks(model, observations[1])
    )
    _, _, likelihood_t2 = _p59_author_sir_source_density_callbacks(model, observations[2])
    fit_data1 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=int(fit_sample_count),
    )
    frame1 = fit_data1.frame
    shift1 = fit_data1.shift_constant
    transport1, fit_hash1, density_hash1 = _p59_fixed_ttsirt_transport_from_values(
        local_fit_points=fit_data1.local_fit_points,
        target_values=fit_data1.target_values,
        fit_weights=fit_data1.fit_weights,
        target_dim=target_dim,
        fit_degree=int(fit_degree),
        fit_rank=int(fit_rank),
        ridge=float(ridge),
        branch_seed="p59-9b-author-sir-step1-fixed-ttsirt",
        convention=convention,
    )
    components1 = SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_t1,
        prior_log_density_fn=prior_log_density,
    )
    components2 = SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_t2,
        prior_log_density_fn=None,
    )
    spec1 = SourceRouteSequentialStepSpec(
        target=_p59_author_sir_source_route_target(
            frame=frame1,
            shift_constant=shift1,
            time_index=1,
            components=components1,
        ),
        transport=SourceRouteTransportProtocol(transport1),
        reference_samples=retained_reference,
        measure_convention=convention,
        density_components=components1,
    )
    retained1 = _p59_retained_object_from_spec(spec1)
    fit_retained_reference = (
        retained_reference
        if int(fit_sample_count) == int(sample_count)
        else _p59_author_sir_unit_reference_points(
            int(fit_sample_count),
            target_dim,
        )
    )
    fit_spec1 = SourceRouteSequentialStepSpec(
        target=spec1.target,
        transport=spec1.transport,
        reference_samples=fit_retained_reference,
        measure_convention=convention,
        density_components=components1,
    )
    fit_retained1 = (
        retained1
        if int(fit_sample_count) == int(sample_count)
        else _p59_retained_object_from_spec(fit_spec1)
    )
    fit_data2 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        fit_sample_count=int(fit_sample_count),
        previous_retained_object=fit_retained1,
    )
    frame2 = fit_data2.frame
    shift2 = fit_data2.shift_constant
    transport2, fit_hash2, density_hash2 = _p59_fixed_ttsirt_transport_from_values(
        local_fit_points=fit_data2.local_fit_points,
        target_values=fit_data2.target_values,
        fit_weights=fit_data2.fit_weights,
        target_dim=target_dim,
        fit_degree=int(fit_degree),
        fit_rank=int(fit_rank),
        ridge=float(ridge),
        branch_seed="p59-9b-author-sir-step2-fixed-ttsirt",
        convention=convention,
    )
    previous_keep_axes = tuple(range(d + m))
    previous_input_axes = tuple(range(d + m, d + 2 * m))
    spec2 = SourceRouteSequentialStepSpec(
        target=_p59_author_sir_placeholder_target(
            frame=frame2,
            shift_constant=shift2,
            time_index=2,
        ),
        transport=SourceRouteTransportProtocol(transport2),
        reference_samples=retained_reference,
        measure_convention=convention,
        density_components=components2,
        previous_marginal_keep_axes=previous_keep_axes,
        previous_marginal_input_axes=previous_input_axes,
    )
    sequential = source_route_run_sequential_fixed_hmc(step_specs=(spec1, spec2))
    previous_marginal_present = sequential.steps[1].previous_marginal_density is not None
    if not previous_marginal_present:
        return _p59_9b_block_result(
            blockers=("missing_time2_previous_marginal_evidence",),
            route_decision=route,
            prep_result=prep,
            step_specs=(spec1, spec2),
        )

    p58_partial_manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_kind": P58_M9_SOURCE_ROUTE_PIPELINE_KIND,
        "route_class": "fixed_ttsirt_source_route",
        "storage_kind": "source_transport_object",
        "transition_interface": "sample_propagation",
        "m9_comparator_tier": "d18_execution_only",
        "rank_policy_status": "PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION",
        "preconditioned_route_required": False,
        "preconditioned_route_status": route.preconditioned_route_status,
        "uses_contract_test_double": False,
        "uses_ukf_as_comparator": False,
        "uses_rank_memory_proxy_as_comparator": False,
        "has_author_sir_callback": True,
        "has_fixed_ttsirt_fit_artifacts": True,
        "has_fixed_ttsirt_transports": True,
        "has_frozen_reference_samples": True,
        "has_source_route_step_specs": True,
        "has_sequential_retained_carry": True,
        "has_previous_marginal_evidence": True,
        "has_m9_runner_manifest_path": False,
    }
    p58_status = p58_m9_source_route_pipeline_readiness(p58_partial_manifest)
    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9b",
        "artifact_role": "bounded_source_route_step_spec_assembly",
        "route_decision_status": route.status,
        "route_decision": route.route_decision,
        "p59_9a_status": prep.status,
        "step_count": 2,
        "target_dimension": target_dim,
        "state_dimension": m,
        "parameter_dimension": d,
        "source_target_order": "[theta, x_t, x_{t-1}]",
        "fit_data_mode": P63_AUTHOR_SIR_SOURCE_FIT_DATA_MODE,
        "fit_data_manifests": (fit_data1.manifest, fit_data2.manifest),
        "previous_marginal_keep_axes": previous_keep_axes,
        "previous_marginal_input_axes": previous_input_axes,
        "previous_marginal_axis_interpretation": (
            "keep previous retained prefix [theta, x_{t-1}] and feed current "
            "target suffix coordinates x_{t-1}"
        ),
        "transport_families": (
            spec1.transport.manifest_payload()["transport_object"]["family"],
            spec2.transport.manifest_payload()["transport_object"]["family"],
        ),
        "transport_source_contract_levels": (
            spec1.transport.manifest_payload()["source_contract_level"],
            spec2.transport.manifest_payload()["source_contract_level"],
        ),
        "fit_branch_hashes": (fit_hash1, fit_hash2),
        "density_branch_hashes": (density_hash1, density_hash2),
        "defensive_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
        "defensive_tau_source": "author_executable_ttsirt_default",
        "source_declared_tau_unwired": 10.0,
        "source_executable_ttsirt_default_tau": P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU,
        "defensive_tau_source_anchors": _P62_AUTHOR_TTSIRT_DEFENSIVE_TAU_SOURCE_ANCHORS,
        "fit_degree": int(fit_degree),
        "fit_rank": int(fit_rank),
        "rank_tuple": _source_route_rank_tuple(target_dim, int(fit_rank)),
        "sequential_status": sequential.sequential_status,
        "time2_previous_marginal_present": previous_marginal_present,
        "source_anchors": _P59_9B_AUTHOR_SIR_SOURCE_ANCHORS,
        "p58_partial_manifest": p58_partial_manifest,
        "p58_readiness_status_after_9b": p58_status.status,
        "p58_expected_remaining_blocker": "missing_has_m9_runner_manifest_path",
        "bounded_transport_note": (
            "Step specs use bounded fixed-TTSIRT transports to prove assembly and "
            "previous-marginal wiring; this is not rank convergence or validation."
        ),
        "nonclaims": (
            "no Phase-9 validation launch",
            "no d18 filtering accuracy claim",
            "no same-route rank convergence claim",
            "no d50 or d100 scaling claim",
            "no HMC production readiness claim",
            "no adaptive Zhao-Cui parity claim",
        ),
    }
    return P59AuthorSIRStepSpecAssemblyResult(
        status=P59_9B_PASS_STATUS,
        blockers=(),
        route_decision=route,
        prep_result=prep,
        step_specs=(spec1, spec2),
        sequential_result=sequential,
        manifest=manifest,
    )


def _p59_9b_block_result(
    *,
    blockers: tuple[str, ...],
    route_decision: P59AuthorSIRRouteDecisionResult,
    prep_result: P59AuthorSIR36DTargetFitPrepResult | None,
    step_specs: tuple[SourceRouteSequentialStepSpec, ...] = (),
) -> P59AuthorSIRStepSpecAssemblyResult:
    return P59AuthorSIRStepSpecAssemblyResult(
        status=P59_9B_BLOCK_STATUS,
        blockers=tuple(blockers),
        route_decision=route_decision,
        prep_result=prep_result,
        step_specs=tuple(step_specs),
        sequential_result=None,
        manifest={
            "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
            "pipeline_phase": "P59-9b",
            "artifact_role": "blocked_source_route_step_spec_assembly",
            "blockers": tuple(blockers),
            "route_decision": route_decision.route_decision,
            "route_decision_status": route_decision.status,
            "p59_9a_status": None if prep_result is None else prep_result.status,
            "fail_closed_rule": "P59-9d and P59-9e must not proceed.",
            "nonclaims": (
                "no Phase-9 validation launch",
                "no d18 filtering accuracy claim",
            ),
        },
    )


def _p59_retained_object_from_spec(spec: SourceRouteSequentialStepSpec) -> SourceRouteRetainedObject:
    retained = source_route_generate_retained_samples(
        target=spec.target,
        transport=spec.transport,
        reference_samples=spec.reference_samples,
        time_index=spec.time_index,
    )
    diagnostics = {
        "phase": "P59-9b-preassembly-step1",
        "time_index": int(spec.time_index),
        "source_anchor": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:33-38",
        "purpose": "materialize previous retained object before fitting bounded time-2 target",
    }
    identity = source_route_retained_object_identity(
        transport_object=spec.transport.transport_object,
        coordinate_frame=spec.target.coordinate_frame,
        samples=retained.retained_batch.samples,
        log_weights=retained.retained_batch.log_weights,
        sample_diagnostics=retained.diagnostics,
        normalizer=retained.normalizer,
        measure_convention=spec.measure_convention,
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        storage_kind=spec.storage_kind,
        transition_interface=spec.transition_interface,
        diagnostics=diagnostics,
    )
    return SourceRouteRetainedObject(
        transport_object=spec.transport.transport_object,
        coordinate_frame=spec.target.coordinate_frame,
        samples=retained.retained_batch.samples,
        log_weights=retained.retained_batch.log_weights,
        sample_diagnostics=retained.diagnostics,
        normalizer=retained.normalizer,
        measure_convention=spec.measure_convention,
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        storage_kind=spec.storage_kind,
        transition_interface=spec.transition_interface,
        branch_identity=identity,
        diagnostics=diagnostics,
    )


def _p59_author_sir_source_route_target(
    *,
    frame: SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    time_index: int,
    components: SourceRouteSequentialDensityComponents,
) -> SourceRouteTarget:
    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        return components.negative_log_physical_density(
            physical_points=points,
            time_index=int(time_index),
            previous_retained_object=None,
        )

    return build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=frame,
        shift_constant=shift_constant,
        time_index=int(time_index),
    )


def _p59_author_sir_placeholder_target(
    *,
    frame: SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    time_index: int,
) -> SourceRouteTarget:
    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank != 2:
            raise ValueError(f"physical_points: {HighDimStatus.INVALID_SHAPE.value}")
        return tf.zeros([int(values.shape[1])], dtype=tf.float64)

    return build_source_route_target(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=frame,
        shift_constant=shift_constant,
        time_index=int(time_index),
    )


def _p59_fixed_ttsirt_transport_from_values(
    *,
    local_fit_points: tf.Tensor,
    target_values: tf.Tensor,
    fit_weights: tf.Tensor | None = None,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
    ridge: float,
    branch_seed: str,
    convention: MeasureConvention,
) -> tuple[FixedTTSIRTTransport, str, str]:
    product_basis = ProductBasis(
        [
            LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(fit_degree))
            for _ in range(int(target_dim))
        ],
        convention,
    )
    fit_config = FixedTTFitConfig(
        ranks=_source_route_rank_tuple(int(target_dim), int(fit_rank)),
        ridge=float(ridge),
        max_sweeps=1,
        sweep_order=tuple(range(int(target_dim))),
        row_budget=max(int(tf.shape(local_fit_points)[1]), 1),
        column_budget=(int(fit_degree) + 1) * int(fit_rank) * int(fit_rank),
        dense_matrix_byte_budget=2**22,
        normal_matrix_byte_budget=2**24,
        condition_number_warning=1e12,
        condition_number_veto=1e16,
        holdout_tolerance=1e6,
    )
    initial_cores = tuple(
        TTCore(
            _source_route_initial_core_values(
                left_rank=fit_config.ranks[axis],
                basis_dim=int(fit_degree) + 1,
                right_rank=fit_config.ranks[axis + 1],
            )
        )
        for axis in range(int(target_dim))
    )
    fit_result = FixedTTFitter().fit(
        product_basis=product_basis,
        samples=FixedTTFitSampleBatch(
            points=tf.transpose(tf.convert_to_tensor(local_fit_points, dtype=tf.float64)),
            target_values=tf.convert_to_tensor(target_values, dtype=tf.float64),
            weights=(
                tf.ones([int(tf.shape(local_fit_points)[1])], dtype=tf.float64)
                if fit_weights is None
                else tf.convert_to_tensor(fit_weights, dtype=tf.float64)
            ),
        ),
        config=fit_config,
        initial_cores=initial_cores,
        branch_seed=str(branch_seed),
        measure_convention=convention,
    )
    if fit_result.status is not HighDimStatus.OK:
        raise ValueError(f"fixed_ttsirt_fit_status_{fit_result.status.value}")
    defensive = TensorProductReferenceDensity(product_basis, convention)
    defensive_tau = _p59_author_sir_defensive_tau_tensor()
    density_identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=defensive_tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
    )
    density = SquaredTTDensity(
        sqrt_tt=fit_result.fitted_tt,
        defensive_density=defensive,
        tau=defensive_tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
        branch_identity=density_identity,
    )
    return (
        FixedTTSIRTTransport(
            density=density,
            cdf_config=KRCDFConfig(
                grid_size=5,
                bisection_steps=4,
                monotonicity_tolerance=1e-10,
                bracket_tolerance=1e-10,
                denominator_floor=1e-12,
                max_floor_count=0,
            ),
        ),
        fit_result.branch_hash.value,
        density.branch_identity.hash.value,
    )


def _source_route_rank_tuple(target_dim: int, fit_rank: int) -> tuple[int, ...]:
    dim = int(target_dim)
    rank = int(fit_rank)
    if dim <= 0:
        raise ValueError("target_dim must be positive")
    if rank <= 0:
        raise ValueError("fit_rank must be positive")
    return tuple([1] + [rank] * (dim - 1) + [1])


def _source_route_initial_core_values(
    *,
    left_rank: int,
    basis_dim: int,
    right_rank: int,
) -> tf.Tensor:
    values = tf.ones(
        [int(left_rank), int(basis_dim), int(right_rank)],
        dtype=tf.float64,
    )
    scale = tf.cast(max(values.shape.num_elements() or 1, 1), tf.float64)
    return values / scale


def _p59_author_sir_unit_reference_points(sample_count: int, target_dim: int) -> tf.Tensor:
    columns = []
    base = tf.linspace(
        tf.constant(0.15, dtype=tf.float64),
        tf.constant(0.85, dtype=tf.float64),
        int(target_dim),
    )
    for index in range(int(sample_count)):
        shift = tf.cast(index, tf.float64) / tf.cast(max(int(sample_count), 1), tf.float64)
        shifted = tf.math.floormod(base + 0.13 * shift, 0.8) + 0.1
        columns.append(shifted)
    return tf.stack(columns, axis=1)


def _p59_author_sir_defensive_tau_tensor() -> tf.Tensor:
    return tf.constant(P62_AUTHOR_TTSIRT_EXECUTABLE_DEFAULT_TAU, dtype=tf.float64)


def p60_author_sir_same_route_rank_comparator(
    *,
    sample_count: int = 1,
    fit_sample_count: int = 2,
    low_fit_degree: int = 0,
    high_fit_degree: int = 1,
    low_fit_rank: int = 1,
    high_fit_rank: int = 2,
) -> P60AuthorSIRSameRouteRankComparatorResult:
    """Run the P60-2 same-route rank comparator with fail-closed gates."""

    if int(high_fit_rank) <= int(low_fit_rank):
        return _p60_rank_comparator_block(
            blockers=("high_fit_rank_must_exceed_low_fit_rank",),
            low_result=None,
            high_result=None,
            extra_manifest={
                "low_fit_rank": int(low_fit_rank),
                "high_fit_rank": int(high_fit_rank),
            },
        )

    low: P59AuthorSIRStepSpecAssemblyResult | None = None
    high: P59AuthorSIRStepSpecAssemblyResult | None = None
    blockers: list[str] = []
    try:
        low = p59_author_sir_step_spec_assembly(
            sample_count=int(sample_count),
            fit_sample_count=int(fit_sample_count),
            fit_degree=int(low_fit_degree),
            fit_rank=int(low_fit_rank),
        )
    except Exception as exc:  # pragma: no cover - preserved in manifest
        blockers.append("candidate_low_exception_" + type(exc).__name__ + "_" + str(exc))
    try:
        high = p59_author_sir_step_spec_assembly(
            sample_count=int(sample_count),
            fit_sample_count=int(fit_sample_count),
            fit_degree=int(high_fit_degree),
            fit_rank=int(high_fit_rank),
        )
    except Exception as exc:
        blockers.append("candidate_high_exception_" + type(exc).__name__ + "_" + str(exc))

    if low is not None and low.status != P59_9B_PASS_STATUS:
        blockers.append("candidate_low_failed_" + "_".join(low.blockers))
    if high is not None and high.status != P59_9B_PASS_STATUS:
        blockers.append("candidate_high_failed_" + "_".join(high.blockers))
    if low is None or high is None or blockers:
        return _p60_rank_comparator_block(
            blockers=tuple(blockers) if blockers else ("missing_candidate_row",),
            low_result=low,
            high_result=high,
            extra_manifest={
                "candidate_low": _p60_candidate_manifest_or_none(low),
                "candidate_high": _p60_candidate_manifest_or_none(high),
                "nonclaims": _p60_rank_nonclaims(),
            },
        )

    manifest = _p60_rank_comparator_manifest(low, high)
    veto_blockers = tuple(str(blocker) for blocker in manifest["veto_blockers"])
    if veto_blockers:
        return P60AuthorSIRSameRouteRankComparatorResult(
            status=P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
            blockers=veto_blockers,
            low_result=low,
            high_result=high,
            manifest=manifest,
        )
    return P60AuthorSIRSameRouteRankComparatorResult(
        status=P60_D18_RANK_CONVERGENCE_PASS_STATUS,
        blockers=(),
        low_result=low,
        high_result=high,
        manifest=manifest,
    )


def _p60_rank_comparator_manifest(
    low: P59AuthorSIRStepSpecAssemblyResult,
    high: P59AuthorSIRStepSpecAssemblyResult,
) -> Mapping[str, object]:
    assert low.sequential_result is not None
    assert high.sequential_result is not None
    blockers: list[str] = []
    low_seq = low.sequential_result
    high_seq = high.sequential_result
    if low.manifest["target_dimension"] != high.manifest["target_dimension"]:
        blockers.append("target_dimension_mismatch")
    if low.manifest["source_target_order"] != high.manifest["source_target_order"]:
        blockers.append("source_target_order_mismatch")
    if low.manifest["previous_marginal_keep_axes"] != high.manifest["previous_marginal_keep_axes"]:
        blockers.append("previous_marginal_keep_axes_mismatch")
    if low.manifest["previous_marginal_input_axes"] != high.manifest["previous_marginal_input_axes"]:
        blockers.append("previous_marginal_input_axes_mismatch")
    low_rank = int(low.manifest.get("fit_rank", 1))
    high_rank = int(high.manifest.get("fit_rank", 1))
    if high_rank <= low_rank:
        blockers.append("high_rank_not_strictly_stronger")
    log_delta = abs(
        float(high_seq.log_marginal_likelihood.numpy())
        - float(low_seq.log_marginal_likelihood.numpy())
    )
    normalizer_deltas = tuple(
        abs(float(high_step.normalizer_increment.numpy()) - float(low_step.normalizer_increment.numpy()))
        for low_step, high_step in zip(low_seq.steps, high_seq.steps)
    )
    low_normalizer_terms = _p64_normalizer_terms_by_step(low_seq)
    high_normalizer_terms = _p64_normalizer_terms_by_step(high_seq)
    low_collapsed = _p64_defensive_only_steps(low_normalizer_terms)
    high_collapsed = _p64_defensive_only_steps(high_normalizer_terms)
    if low_collapsed:
        blockers.append("candidate_low_defensive_only_transport")
    if high_collapsed:
        blockers.append("candidate_high_defensive_only_transport")
    probe_delta = _p60_probe_log_density_delta(low, high)
    retained_delta = _p60_retained_log_density_delta(low, high)
    thresholds = {
        "log_marginal_abs_delta": 5.0,
        "normalizer_increment_abs_delta": 5.0,
        "probe_log_density_median_abs_delta": 10.0,
        "retained_log_density_median_abs_delta": 10.0,
    }
    if log_delta > thresholds["log_marginal_abs_delta"]:
        blockers.append("log_marginal_delta_threshold_exceeded")
    if any(delta > thresholds["normalizer_increment_abs_delta"] for delta in normalizer_deltas):
        blockers.append("normalizer_increment_delta_threshold_exceeded")
    if probe_delta > thresholds["probe_log_density_median_abs_delta"]:
        blockers.append("probe_log_density_delta_threshold_exceeded")
    if retained_delta is None:
        blockers.append("retained_density_delta_unavailable")
    elif retained_delta > thresholds["retained_log_density_median_abs_delta"]:
        blockers.append("retained_log_density_delta_threshold_exceeded")
    return {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P60-2",
        "artifact_role": "same_route_rank_comparator",
        "status": (
            P60_D18_RANK_CONVERGENCE_BLOCK_STATUS
            if blockers
            else P60_D18_RANK_CONVERGENCE_PASS_STATUS
        ),
        "candidate_low": _p60_candidate_manifest_or_none(low),
        "candidate_high": _p60_candidate_manifest_or_none(high),
        "log_marginal_likelihoods": (
            float(low_seq.log_marginal_likelihood.numpy()),
            float(high_seq.log_marginal_likelihood.numpy()),
        ),
        "log_marginal_abs_delta": log_delta,
        "normalizer_increment_abs_deltas": normalizer_deltas,
        "normalizer_decomposition": {
            "candidate_low": low_normalizer_terms,
            "candidate_high": high_normalizer_terms,
            "defensive_only_sqrt_normalizer_tol": P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL,
            "candidate_low_defensive_only_steps": low_collapsed,
            "candidate_high_defensive_only_steps": high_collapsed,
        },
        "effective_sample_size_by_step": {
            "candidate_low": _p60_ess_by_step(low_seq),
            "candidate_high": _p60_ess_by_step(high_seq),
        },
        "correction_log_weight_ranges": {
            "candidate_low": _p60_correction_ranges(low_seq),
            "candidate_high": _p60_correction_ranges(high_seq),
        },
        "probe_log_density_median_abs_delta": probe_delta,
        "retained_log_density_median_abs_delta": retained_delta,
        "thresholds": thresholds,
        "veto_blockers": tuple(blockers),
        "source_invariants": {
            "route": "Zhao-Cui full_sol",
            "realized_target": "[x_t, x_{t-1}]",
            "target_dimension": low.manifest["target_dimension"],
            "previous_marginal_keep_axes": low.manifest["previous_marginal_keep_axes"],
            "previous_marginal_input_axes": low.manifest["previous_marginal_input_axes"],
        },
        "nonclaims": _p60_rank_nonclaims(),
    }


def _p60_probe_log_density_delta(
    low: P59AuthorSIRStepSpecAssemblyResult,
    high: P59AuthorSIRStepSpecAssemblyResult,
) -> float:
    deltas = []
    for low_spec, high_spec in zip(low.step_specs, high.step_specs):
        probes = _p59_author_sir_reference_points(
            3,
            low_spec.target.coordinate_frame.dimension,
        )
        low_values = low_spec.transport.eval_pdf(probes)
        high_values = high_spec.transport.eval_pdf(probes)
        deltas.append(tf.abs(tf.math.log(low_values) - tf.math.log(high_values)))
    joined = tf.concat(deltas, axis=0)
    return _p60_tensor_median_float(joined)


def _p60_retained_log_density_delta(
    low: P59AuthorSIRStepSpecAssemblyResult,
    high: P59AuthorSIRStepSpecAssemblyResult,
) -> float | None:
    assert low.sequential_result is not None
    assert high.sequential_result is not None
    deltas = []
    for low_step, high_step in zip(low.sequential_result.steps, high.sequential_result.steps):
        physical = low_step.retained_object.samples
        low_local = tf.transpose(
            tf.linalg.solve(
                low_step.retained_object.coordinate_frame.matrix,
                physical - low_step.retained_object.coordinate_frame.mu[:, tf.newaxis],
            )
        )
        high_local = tf.transpose(
            tf.linalg.solve(
                high_step.retained_object.coordinate_frame.matrix,
                physical - high_step.retained_object.coordinate_frame.mu[:, tf.newaxis],
            )
        )
        low_density = low_step.retained_object.transport_object.density.normalized_retained_density_values(
            tuple(range(low_step.retained_object.coordinate_frame.dimension)),
            low_local,
        )
        high_density = high_step.retained_object.transport_object.density.normalized_retained_density_values(
            tuple(range(high_step.retained_object.coordinate_frame.dimension)),
            high_local,
        )
        deltas.append(tf.abs(tf.math.log(low_density) - tf.math.log(high_density)))
    if not deltas:
        return None
    return _p60_tensor_median_float(tf.concat(deltas, axis=0))


def _p60_tensor_median_float(values: tf.Tensor) -> float:
    vector = tf.reshape(tf.convert_to_tensor(values, dtype=tf.float64), [-1])
    if int(vector.shape[0]) == 0:
        raise ValueError("median requires nonempty values")
    if not bool(tf.reduce_all(tf.math.is_finite(vector)).numpy()):
        return float("inf")
    ordered = tf.sort(vector)
    return float(ordered[int(vector.shape[0]) // 2].numpy())


def _p64_normalizer_terms_by_step(
    sequential: SourceRouteSequentialResult,
) -> tuple[Mapping[str, object], ...]:
    terms = []
    for step in sequential.steps:
        transport = step.retained_object.transport_object
        density = getattr(transport, "density", None)
        if density is None or not callable(getattr(density, "sqrt_square_normalizer", None)):
            terms.append(
                {
                    "time_index": int(step.time_index),
                    "available": False,
                    "normalizer_increment": float(step.normalizer_increment.numpy()),
                }
            )
            continue
        sqrt_square = tf.convert_to_tensor(
            density.sqrt_square_normalizer(),
            dtype=tf.float64,
        )
        defensive_z = tf.convert_to_tensor(
            density.defensive_density.normalizer(density.measure_convention.mass_measure),
            dtype=tf.float64,
        )
        tau = tf.convert_to_tensor(density.tau, dtype=tf.float64)
        mixture_z = tf.convert_to_tensor(density.normalizer(), dtype=tf.float64)
        terms.append(
            {
                "time_index": int(step.time_index),
                "available": True,
                "sqrt_square_normalizer": float(sqrt_square.numpy()),
                "defensive_normalizer": float(defensive_z.numpy()),
                "tau": float(tau.numpy()),
                "defensive_contribution": float((tau * defensive_z).numpy()),
                "mixture_normalizer": float(mixture_z.numpy()),
                "log_transport_normalizer": float(tf.math.log(mixture_z).numpy()),
                "shift_constant": float(step.target.shift_constant.numpy()),
                "coordinate_frame_log_abs_det": float(
                    step.target.coordinate_frame.log_abs_det().numpy()
                ),
                "normalizer_increment": float(step.normalizer_increment.numpy()),
            }
        )
    return tuple(terms)


def _p64_defensive_only_steps(
    terms_by_step: tuple[Mapping[str, object], ...],
) -> tuple[int, ...]:
    collapsed = []
    for row in terms_by_step:
        if not bool(row.get("available", False)):
            continue
        sqrt_square = float(row["sqrt_square_normalizer"])
        if sqrt_square <= P64_DEFENSIVE_ONLY_SQRT_NORMALIZER_TOL:
            collapsed.append(int(row["time_index"]))
    return tuple(collapsed)


def _p60_ess_by_step(sequential: SourceRouteSequentialResult) -> tuple[float, ...]:
    return tuple(
        float(step.retained_samples.diagnostics.effective_sample_size.numpy())
        for step in sequential.steps
    )


def _p60_correction_ranges(sequential: SourceRouteSequentialResult) -> tuple[tuple[float, float], ...]:
    return tuple(
        (
            float(tf.reduce_min(step.retained_samples.correction_log_weights).numpy()),
            float(tf.reduce_max(step.retained_samples.correction_log_weights).numpy()),
        )
        for step in sequential.steps
    )


def _p60_candidate_manifest_or_none(
    result: P59AuthorSIRStepSpecAssemblyResult | None,
) -> Mapping[str, object] | None:
    if result is None:
        return None
    return {
        "status": result.status,
        "blockers": result.blockers,
        "fit_rank": result.manifest.get("fit_rank"),
        "fit_degree": result.manifest.get("fit_degree"),
        "rank_tuple": result.manifest.get("rank_tuple"),
        "fit_branch_hashes": result.manifest.get("fit_branch_hashes"),
        "density_branch_hashes": result.manifest.get("density_branch_hashes"),
        "defensive_tau": result.manifest.get("defensive_tau"),
        "defensive_tau_source": result.manifest.get("defensive_tau_source"),
        "target_dimension": result.manifest.get("target_dimension"),
        "source_target_order": result.manifest.get("source_target_order"),
    }


def _p60_rank_nonclaims() -> tuple[str, ...]:
    return (
        "same-route rank convergence is not exact correctness",
        "no d18 correctness candidate claim",
        "no d50 or d100 scaling claim",
        "no HMC production readiness claim",
        "no adaptive Zhao-Cui parity claim",
        "no UKF correctness comparator",
    )


def _p60_rank_comparator_block(
    *,
    blockers: tuple[str, ...],
    low_result: P59AuthorSIRStepSpecAssemblyResult | None,
    high_result: P59AuthorSIRStepSpecAssemblyResult | None,
    extra_manifest: Mapping[str, object] | None = None,
) -> P60AuthorSIRSameRouteRankComparatorResult:
    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P60-2",
        "artifact_role": "blocked_same_route_rank_comparator",
        "status": P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
        "veto_blockers": tuple(blockers),
        "nonclaims": _p60_rank_nonclaims(),
    }
    if extra_manifest is not None:
        manifest = {**manifest, **dict(extra_manifest)}
    return P60AuthorSIRSameRouteRankComparatorResult(
        status=P60_D18_RANK_CONVERGENCE_BLOCK_STATUS,
        blockers=tuple(blockers),
        low_result=low_result,
        high_result=high_result,
        manifest=manifest,
    )


def p59_author_sir_runner_manifest_path(
    *,
    assembly_result: P59AuthorSIRStepSpecAssemblyResult | None = None,
    manifest_path: str | Path = P59_9D_DEFAULT_MANIFEST_PATH,
    comparator_tier: str = "d18_execution_only",
    sample_count: int = 1,
    fit_sample_count: int = 2,
    write_manifest: bool = False,
) -> P59AuthorSIRRunnerManifestResult:
    """Build the P59-9d M9 runner/readiness manifest path.

    This is the bounded command surface that consumes the already gated
    P59-9a/9b/9c artifacts.  It does not run the P59-9e validation ladder.
    """

    if assembly_result is not None and not isinstance(
        assembly_result,
        P59AuthorSIRStepSpecAssemblyResult,
    ):
        raise TypeError("assembly_result must be P59AuthorSIRStepSpecAssemblyResult")
    assembly = assembly_result or p59_author_sir_step_spec_assembly(
        sample_count=int(sample_count),
        fit_sample_count=int(fit_sample_count),
    )
    blockers: list[str] = []
    if assembly.status != P59_9B_PASS_STATUS:
        blockers.append("missing_p59_9b_step_spec_assembly_pass")
    if assembly.route_decision.status != P59_9C_PASS_STATUS:
        blockers.append("missing_p59_9c_route_decision_pass")
    if assembly.route_decision.route_decision != P59_9C_FULL_ROUTE_SELECTED:
        blockers.append("p59_9c_route_not_full_route_selected")
    if assembly.prep_result is None or assembly.prep_result.status != P59_9A_PASS_STATUS:
        blockers.append("missing_p59_9a_target_fit_prep_pass")
    if str(comparator_tier) not in P58_M9_ALLOWED_COMPARATOR_TIERS:
        blockers.append("invalid_m9_comparator_tier")
    manifest_target = Path(manifest_path)
    if not str(manifest_target).strip():
        blockers.append("missing_manifest_path")

    p58_manifest = _p59_9d_p58_manifest(
        assembly=assembly,
        comparator_tier=str(comparator_tier),
        manifest_path=str(manifest_target),
        has_runner_manifest_path=not blockers,
    )
    readiness = p58_m9_source_route_pipeline_readiness(p58_manifest)
    if readiness.status != P58_M9_READY_STATUS:
        blockers.extend(
            blocker for blocker in readiness.blockers if blocker not in blockers
        )
    if blockers:
        return P59AuthorSIRRunnerManifestResult(
            status=P59_9D_BLOCK_STATUS,
            blockers=tuple(blockers),
            assembly_result=assembly,
            readiness=readiness,
            manifest_path=str(manifest_target),
            manifest={
                "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
                "pipeline_phase": "P59-9d",
                "artifact_role": "blocked_runner_manifest_path",
                "blockers": tuple(blockers),
                "p58_manifest": p58_manifest,
                "fail_closed_rule": "P59-9e validation ladder must not proceed.",
                "nonclaims": (
                    "no Phase-9 validation launch",
                    "no d18 filtering accuracy claim",
                ),
            },
        )

    manifest = {
        "schema_version": "bayesfilter.p59_9d.runner_manifest.v1",
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9d",
        "artifact_role": "runner_manifest_path",
        "status": P59_9D_PASS_STATUS,
        "runner_command": (
            "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
            "scripts/p59_author_sir_m9_runner_manifest.py --output "
            + str(manifest_target)
        ),
        "consumed_artifacts": {
            "p59_9a_status": assembly.prep_result.status,
            "p59_9b_status": assembly.status,
            "p59_9c_status": assembly.route_decision.status,
            "p59_9c_route_decision": assembly.route_decision.route_decision,
        },
        "source_anchors": _P59_9D_AUTHOR_SIR_SOURCE_ANCHORS,
        "p58_manifest": p58_manifest,
        "p58_readiness": readiness.manifest_payload(),
        "step_spec_count": len(assembly.step_specs),
        "sequential_status": (
            None
            if assembly.sequential_result is None
            else assembly.sequential_result.sequential_status
        ),
        "manifest_path": str(manifest_target),
        "ready_for_validation_ladder": True,
        "nonclaims": (
            "no P59-9e validation has been run",
            "no d18 filtering accuracy claim",
            "no same-route rank convergence claim",
            "no d50 or d100 scaling claim",
            "no HMC production readiness claim",
            "no adaptive Zhao-Cui parity claim",
        ),
    }
    if bool(write_manifest):
        manifest_target.parent.mkdir(parents=True, exist_ok=True)
        manifest_target.write_text(
            json.dumps(_json_ready(manifest), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return P59AuthorSIRRunnerManifestResult(
        status=P59_9D_PASS_STATUS,
        blockers=(),
        assembly_result=assembly,
        readiness=readiness,
        manifest_path=str(manifest_target),
        manifest=manifest,
    )


def _p59_9d_p58_manifest(
    *,
    assembly: P59AuthorSIRStepSpecAssemblyResult,
    comparator_tier: str,
    manifest_path: str,
    has_runner_manifest_path: bool,
) -> Mapping[str, object]:
    return {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_kind": P58_M9_SOURCE_ROUTE_PIPELINE_KIND,
        "route_class": "fixed_ttsirt_source_route",
        "storage_kind": "source_transport_object",
        "transition_interface": "sample_propagation",
        "m9_comparator_tier": str(comparator_tier),
        "rank_policy_status": "PASS_P57_M7_SOURCE_FAITHFUL_RANK_UKF_CALIBRATION",
        "preconditioned_route_required": False,
        "preconditioned_route_status": assembly.route_decision.preconditioned_route_status,
        "uses_contract_test_double": False,
        "uses_ukf_as_comparator": False,
        "uses_rank_memory_proxy_as_comparator": False,
        "has_author_sir_callback": True,
        "has_fixed_ttsirt_fit_artifacts": assembly.status == P59_9B_PASS_STATUS,
        "has_fixed_ttsirt_transports": assembly.status == P59_9B_PASS_STATUS,
        "has_frozen_reference_samples": assembly.status == P59_9B_PASS_STATUS,
        "has_source_route_step_specs": assembly.status == P59_9B_PASS_STATUS,
        "has_sequential_retained_carry": (
            assembly.status == P59_9B_PASS_STATUS and assembly.sequential_result is not None
        ),
        "has_previous_marginal_evidence": bool(
            assembly.sequential_result is not None
            and len(assembly.sequential_result.steps) > 1
            and assembly.sequential_result.steps[1].previous_marginal_density is not None
        ),
        "has_m9_runner_manifest_path": bool(has_runner_manifest_path),
        "runner_manifest_path": str(manifest_path),
        "source_anchors": _P59_9D_AUTHOR_SIR_SOURCE_ANCHORS,
    }


def _json_ready(value):
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tf.Tensor):
        if value.shape.rank == 0:
            raw = value.numpy()
            if hasattr(raw, "item"):
                return raw.item()
            return raw
        return value.numpy().tolist()
    if isinstance(value, Path):
        return str(value)
    return value


def p59_author_sir_validation_ladder(
    *,
    runner_result: P59AuthorSIRRunnerManifestResult | None = None,
    tier: str = "d18_execution_only",
    sample_count: int = 1,
    fit_sample_count: int = 2,
) -> P59AuthorSIRValidationLadderResult:
    """Run the P59-9e validation ladder at the declared honest tier."""

    selected_tier = str(tier)
    if selected_tier not in P58_M9_ALLOWED_COMPARATOR_TIERS:
        return _p59_9e_block_result(
            blockers=("invalid_p59_9e_tier",),
            tier=selected_tier,
            runner_result=runner_result,
        )
    runner = runner_result or p59_author_sir_runner_manifest_path(
        sample_count=int(sample_count),
        fit_sample_count=int(fit_sample_count),
        comparator_tier=selected_tier,
    )
    blockers: list[str] = []
    if runner.status != P59_9D_PASS_STATUS:
        blockers.append("missing_p59_9d_runner_manifest_pass")
    if selected_tier == "d18_same_route_rank_convergence":
        blockers.append("missing_higher_rank_same_route_comparator")
    if selected_tier == "d18_correctness_candidate":
        blockers.append("missing_same_target_reference_or_bridge")
    if selected_tier != "d18_execution_only":
        return _p59_9e_block_result(
            blockers=tuple(blockers),
            tier=selected_tier,
            runner_result=runner,
        )
    if blockers:
        return _p59_9e_block_result(
            blockers=tuple(blockers),
            tier=selected_tier,
            runner_result=runner,
        )
    assembly = runner.assembly_result
    if assembly is None or assembly.sequential_result is None:
        return _p59_9e_block_result(
            blockers=("missing_p59_9b_sequential_result",),
            tier=selected_tier,
            runner_result=runner,
        )
    sequential = assembly.sequential_result
    log_marginal = sequential.log_marginal_likelihood
    if not bool(tf.math.is_finite(log_marginal).numpy()):
        return _p59_9e_block_result(
            blockers=("nonfinite_log_marginal_likelihood",),
            tier=selected_tier,
            runner_result=runner,
        )
    ess_values = tuple(
        float(step.retained_samples.diagnostics.effective_sample_size.numpy())
        for step in sequential.steps
    )
    normalizer_increments = tuple(
        float(step.normalizer_increment.numpy()) for step in sequential.steps
    )
    correction_ranges = tuple(
        (
            float(tf.reduce_min(step.retained_samples.correction_log_weights).numpy()),
            float(tf.reduce_max(step.retained_samples.correction_log_weights).numpy()),
        )
        for step in sequential.steps
    )
    manifest = {
        "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
        "pipeline_phase": "P59-9e",
        "artifact_role": "d18_execution_only_validation_ladder",
        "status": P59_9E_D18_EXECUTION_ONLY_PASS_STATUS,
        "tier": selected_tier,
        "prerequisite_tokens": {
            "p59_9a": assembly.prep_result.status if assembly.prep_result else None,
            "p59_9b": assembly.status,
            "p59_9c": assembly.route_decision.status,
            "p59_9d": runner.status,
            "p58_readiness": runner.readiness.status,
        },
        "step_count": len(sequential.steps),
        "target_dimension": assembly.manifest["target_dimension"],
        "state_dimension": assembly.manifest["state_dimension"],
        "parameter_dimension": assembly.manifest["parameter_dimension"],
        "comparator_tier": selected_tier,
        "log_marginal_likelihood": float(log_marginal.numpy()),
        "normalizer_increments": normalizer_increments,
        "effective_sample_size_by_step": ess_values,
        "correction_log_weight_ranges": correction_ranges,
        "transport_source_contract_levels": assembly.manifest[
            "transport_source_contract_levels"
        ],
        "fit_branch_hashes": assembly.manifest["fit_branch_hashes"],
        "density_branch_hashes": assembly.manifest["density_branch_hashes"],
        "previous_marginal_keep_axes": assembly.manifest["previous_marginal_keep_axes"],
        "previous_marginal_input_axes": assembly.manifest["previous_marginal_input_axes"],
        "source_anchors": _P59_9D_AUTHOR_SIR_SOURCE_ANCHORS,
        "runner_manifest_path": runner.manifest_path,
        "promotion_boundary": (
            "execution-only tier permits finite values, ESS, replay, normalizer, "
            "rank, memory, and wall-time diagnostics; it cannot claim accuracy."
        ),
        "blocked_higher_tiers": {
            "d18_same_route_rank_convergence": "missing_higher_rank_same_route_comparator",
            "d18_correctness_candidate": "missing_same_target_reference_or_bridge",
            "d50": "requires d18_same_route_rank_convergence first",
            "d100": "requires d50 non-veto scaling evidence first",
        },
        "nonclaims": (
            "no d18 filtering accuracy claim",
            "no same-route rank convergence claim",
            "no d18 correctness candidate claim",
            "no d50 or d100 scaling claim",
            "no HMC production readiness claim",
            "no adaptive Zhao-Cui parity claim",
            "no UKF correctness comparator",
        ),
    }
    return P59AuthorSIRValidationLadderResult(
        status=P59_9E_D18_EXECUTION_ONLY_PASS_STATUS,
        blockers=(),
        tier=selected_tier,
        runner_result=runner,
        manifest=manifest,
    )


def _p59_9e_block_result(
    *,
    blockers: tuple[str, ...],
    tier: str,
    runner_result: P59AuthorSIRRunnerManifestResult | None,
) -> P59AuthorSIRValidationLadderResult:
    return P59AuthorSIRValidationLadderResult(
        status=P59_9E_BLOCK_STATUS,
        blockers=tuple(blockers) if blockers else ("p59_9e_validation_ladder_blocked",),
        tier=str(tier) if str(tier) in P58_M9_ALLOWED_COMPARATOR_TIERS else "d18_execution_only",
        runner_result=runner_result,
        manifest={
            "target_id": P58_M9_AUTHOR_SIR_TARGET_ID,
            "pipeline_phase": "P59-9e",
            "artifact_role": "blocked_validation_ladder",
            "requested_tier": str(tier),
            "blockers": tuple(blockers) if blockers else ("p59_9e_validation_ladder_blocked",),
            "fail_closed_rule": "Do not attempt d50/d100 or promote correctness.",
            "nonclaims": (
                "no d18 filtering accuracy claim",
                "no same-route rank convergence claim",
                "no d50 or d100 scaling claim",
            ),
        },
    )


@dataclass(frozen=True)
class SourceRoutePreviousMarginalDensityResult:
    """Previous retained-object marginal density in physical coordinates."""

    previous_retained_object: SourceRouteRetainedObject
    keep_axes: tuple[int, ...]
    marginal_transport: object
    physical_points: tf.Tensor
    local_points: tf.Tensor
    log_density: tf.Tensor

    def __post_init__(self) -> None:
        if not isinstance(self.previous_retained_object, SourceRouteRetainedObject):
            raise TypeError("previous_retained_object must be SourceRouteRetainedObject")
        keep_axes = tuple(int(axis) for axis in self.keep_axes)
        if not keep_axes:
            raise ValueError("keep_axes must be nonempty")
        if keep_axes != tuple(range(len(keep_axes))):
            raise ValueError("source previous marginalization requires prefix keep axes")
        if keep_axes[-1] >= self.previous_retained_object.coordinate_frame.dimension:
            raise ValueError(f"keep_axes: {HighDimStatus.INVALID_SHAPE.value}")
        physical = tf.convert_to_tensor(self.physical_points, dtype=tf.float64)
        local = tf.convert_to_tensor(self.local_points, dtype=tf.float64)
        log_density = _finite_vector("log_density", self.log_density)
        if physical.shape.rank != 2 or local.shape.rank != 2:
            raise ValueError(f"previous marginal points: {HighDimStatus.INVALID_SHAPE.value}")
        if (
            int(physical.shape[0]) != len(keep_axes)
            or local.shape != physical.shape
            or log_density.shape != (int(physical.shape[1]),)
        ):
            raise ValueError(f"previous marginal density: {HighDimStatus.INVALID_SHAPE.value}")
        _transport_manifest_payload(self.marginal_transport)
        object.__setattr__(self, "keep_axes", keep_axes)
        object.__setattr__(self, "physical_points", physical)
        object.__setattr__(self, "local_points", local)
        object.__setattr__(self, "log_density", log_density)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePreviousMarginalDensityResult",
            "previous_retained_hash": (
                self.previous_retained_object.branch_identity.hash.value
            ),
            "keep_axes": self.keep_axes,
            "marginal_transport": _transport_manifest_payload(self.marginal_transport),
            "physical_points": self.physical_points,
            "local_points": self.local_points,
            "log_density": self.log_density,
        }


@dataclass(frozen=True)
class SourceRoutePreconditionerContract:
    """Source-route preconditioner/residual target decomposition metadata."""

    variant: str
    coefficient: tf.Tensor
    reference_density_label: str
    forward_map_label: str
    inverse_map_label: str
    route_label: str = SOURCE_FAITHFUL_ROUTE_LABEL

    def __post_init__(self) -> None:
        if str(self.variant) not in ("full", "preconditioner", "residual"):
            raise ValueError("variant must be full, preconditioner, or residual")
        coefficient = tf.convert_to_tensor(self.coefficient, dtype=tf.float64)
        if coefficient.shape.rank != 0:
            raise ValueError(f"coefficient: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.math.is_finite(coefficient).numpy()):
            raise ValueError(f"coefficient: {HighDimStatus.NONFINITE_VALUE.value}")
        for name, value in (
            ("reference_density_label", self.reference_density_label),
            ("forward_map_label", self.forward_map_label),
            ("inverse_map_label", self.inverse_map_label),
            ("route_label", self.route_label),
        ):
            if not str(value).strip():
                raise ValueError(f"{name} must be nonempty")
        object.__setattr__(self, "variant", str(self.variant))
        object.__setattr__(self, "coefficient", coefficient)
        object.__setattr__(self, "reference_density_label", str(self.reference_density_label))
        object.__setattr__(self, "forward_map_label", str(self.forward_map_label))
        object.__setattr__(self, "inverse_map_label", str(self.inverse_map_label))
        object.__setattr__(self, "route_label", str(self.route_label))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePreconditionerContract",
            "variant": self.variant,
            "coefficient": self.coefficient,
            "reference_density_label": self.reference_density_label,
            "forward_map_label": self.forward_map_label,
            "inverse_map_label": self.inverse_map_label,
            "route_label": self.route_label,
        }


@dataclass(frozen=True)
class SourceRouteLinearPreconditionerResult:
    """Linear preconditioner output mirroring author ``precond.m``."""

    matrix: tf.Tensor
    sigma_k: tf.Tensor
    parameter_dim: int
    state_dim: int
    source_anchor: str = (
        "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/tensordot/"
        "precond.m:43-56"
    )

    def __post_init__(self) -> None:
        matrix = tf.convert_to_tensor(self.matrix, dtype=tf.float64)
        sigma_k = tf.convert_to_tensor(self.sigma_k, dtype=tf.float64)
        if matrix.shape.rank != 2 or sigma_k.shape != matrix.shape:
            raise ValueError(f"linear preconditioner: {HighDimStatus.INVALID_SHAPE.value}")
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError(f"linear preconditioner: {HighDimStatus.INVALID_SHAPE.value}")
        d = int(self.parameter_dim)
        m = int(self.state_dim)
        if d < 0 or m <= 0 or d + m != int(matrix.shape[0]):
            raise ValueError("parameter_dim + state_dim must match matrix shape")
        if not bool(
            tf.reduce_all(tf.math.is_finite(matrix)).numpy()
            and tf.reduce_all(tf.math.is_finite(sigma_k)).numpy()
        ):
            raise ValueError(f"linear preconditioner: {HighDimStatus.NONFINITE_VALUE.value}")
        if not str(self.source_anchor).strip():
            raise ValueError("source_anchor must be nonempty")
        object.__setattr__(self, "matrix", matrix)
        object.__setattr__(self, "sigma_k", sigma_k)
        object.__setattr__(self, "parameter_dim", d)
        object.__setattr__(self, "state_dim", m)
        object.__setattr__(self, "source_anchor", str(self.source_anchor))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteLinearPreconditionerResult",
            "matrix": self.matrix,
            "sigma_k": self.sigma_k,
            "parameter_dim": int(self.parameter_dim),
            "state_dim": int(self.state_dim),
            "source_anchor": self.source_anchor,
        }


def source_route_linear_preconditioner_from_covariances(
    *,
    sigma1: tf.Tensor,
    sigma2: tf.Tensor,
) -> SourceRouteLinearPreconditionerResult:
    """Construct the author linear preconditioner from covariance matrices.

    This is a TensorFlow transcription of ``precond.m:43-56``.  ``sigma1`` has
    dimension ``d + m`` and ``sigma2`` has dimension ``m``; the result contains
    the source matrix ``C`` and diagonal ``Sigmak`` used by the preconditioned
    route.
    """

    s1 = tf.convert_to_tensor(sigma1, dtype=tf.float64)
    s2 = tf.convert_to_tensor(sigma2, dtype=tf.float64)
    if s1.shape.rank != 2 or s2.shape.rank != 2:
        raise ValueError(f"preconditioner covariances: {HighDimStatus.INVALID_SHAPE.value}")
    if s1.shape[0] != s1.shape[1] or s2.shape[0] != s2.shape[1]:
        raise ValueError(f"preconditioner covariances: {HighDimStatus.INVALID_SHAPE.value}")
    if s1.shape[0] is None or s2.shape[0] is None:
        raise ValueError("preconditioner covariance dimensions must be statically known")
    n = int(s1.shape[0])
    m = int(s2.shape[0])
    d = n - m
    if d < 0 or n <= 0 or m <= 0:
        raise ValueError(f"preconditioner covariances: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64("sigma1", s1)
    assert_tf_float64("sigma2", s2)
    if not bool(
        tf.reduce_all(tf.math.is_finite(s1)).numpy()
        and tf.reduce_all(tf.math.is_finite(s2)).numpy()
    ):
        raise ValueError(f"preconditioner covariances: {HighDimStatus.NONFINITE_VALUE.value}")

    sigma2_full = tf.pad(s2, paddings=[[d, 0], [d, 0]])
    sigma3 = tf.linalg.solve(s1, sigma2_full)
    _, eigvecs = tf.linalg.eig(tf.cast(sigma3, tf.complex128))
    c_complex = tf.linalg.adjoint(eigvecs)
    if d > 0:
        chol_param = tf.linalg.cholesky(s1[:d, :d])
        c11 = tf.cast(tf.linalg.inv(chol_param), tf.complex128)
        c_complex = tf.concat(
            [
                tf.concat([c11, c_complex[:d, d:]], axis=1),
                tf.concat([c_complex[d:, :d], c_complex[d:, d:]], axis=1),
            ],
            axis=0,
        )
    s1_complex = tf.cast(s1, tf.complex128)
    row_variance = tf.math.real(
        tf.linalg.diag_part(c_complex @ s1_complex @ tf.linalg.adjoint(c_complex))
    )
    if not bool(tf.reduce_all(row_variance > 0.0).numpy()):
        raise ValueError(f"preconditioner row variance: {HighDimStatus.NONFINITE_VALUE.value}")
    c_matrix = tf.math.real(
        c_complex / tf.cast(tf.sqrt(row_variance)[:, tf.newaxis], tf.complex128)
    )
    c22 = c_matrix[d:, d:]
    sigma_k_block = c22 @ s2 @ tf.transpose(c22)
    sigma_k_diag = tf.concat(
        [
            tf.zeros([d], dtype=tf.float64),
            tf.linalg.diag_part(sigma_k_block),
        ],
        axis=0,
    )
    sigma_k = tf.linalg.diag(sigma_k_diag)
    return SourceRouteLinearPreconditionerResult(
        matrix=c_matrix,
        sigma_k=sigma_k,
        parameter_dim=d,
        state_dim=m,
    )


@dataclass(frozen=True)
class SourceRoutePreconditionedMap:
    """Fixed-HMC version of the author preconditioner maps ``Tu2x``/``Tx2u``."""

    preconditioner_transport: SourceRouteTransportProtocol
    preconditioner_frame: SourceRouteCoordinateFrame
    reference_forward_fn: object
    reference_inverse_fn: object
    reference_log_density_fn: object
    source_anchor: str = (
        "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:212-213"
    )

    def __post_init__(self) -> None:
        if not isinstance(self.preconditioner_transport, SourceRouteTransportProtocol):
            raise TypeError("preconditioner_transport must be SourceRouteTransportProtocol")
        if not isinstance(self.preconditioner_frame, SourceRouteCoordinateFrame):
            raise TypeError("preconditioner_frame must be SourceRouteCoordinateFrame")
        for name in (
            "reference_forward_fn",
            "reference_inverse_fn",
            "reference_log_density_fn",
        ):
            if not callable(getattr(self, name)):
                raise TypeError(f"{name} must be callable")
        if not str(self.source_anchor).strip():
            raise ValueError("source_anchor must be nonempty")
        object.__setattr__(self, "source_anchor", str(self.source_anchor))

    @property
    def dimension(self) -> int:
        return self.preconditioner_frame.dimension

    def Tu2x(self, residual_points: tf.Tensor) -> tf.Tensor:
        residual = self._finite_points("residual_points", residual_points)
        reference = self._reference_forward(residual)
        local = self.preconditioner_transport.inverse_transport(reference)
        return self._frame_forward(local)

    def Tx2u(self, physical_points: tf.Tensor) -> tf.Tensor:
        physical = self._finite_points("physical_points", physical_points)
        local = self._frame_inverse(physical)
        reference = self.preconditioner_transport.forward_transport(local)
        return self._reference_inverse(reference)

    def reference_log_density(self, residual_points: tf.Tensor) -> tf.Tensor:
        residual = self._finite_points("residual_points", residual_points)
        values = _finite_vector("reference_log_density", self.reference_log_density_fn(residual))
        if values.shape != (int(residual.shape[1]),):
            raise ValueError(f"reference_log_density: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def preconditioner_log_density(self, physical_points: tf.Tensor) -> tf.Tensor:
        physical = self._finite_points("physical_points", physical_points)
        local = self._frame_inverse(physical)
        density = self.preconditioner_transport.eval_pdf(local)
        return tf.math.log(density) - self.preconditioner_frame.log_abs_det()

    def map_roundtrip_error(self, residual_points: tf.Tensor) -> tf.Tensor:
        residual = self._finite_points("residual_points", residual_points)
        return tf.reduce_max(tf.abs(self.Tx2u(self.Tu2x(residual)) - residual))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePreconditionedMap",
            "dimension": self.dimension,
            "forward_map_label": "Tu2x",
            "inverse_map_label": "Tx2u",
            "source_anchor": self.source_anchor,
            "preconditioner_transport": self.preconditioner_transport.manifest_payload(),
            "preconditioner_frame": self.preconditioner_frame.manifest_payload(),
        }

    def _finite_points(self, name: str, points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        if values.shape.rank != 2 or int(values.shape[0]) != self.dimension:
            raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
        assert_tf_float64(name, values)
        if not bool(tf.reduce_all(tf.math.is_finite(values)).numpy()):
            raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
        return values

    def _reference_forward(self, residual_points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(
            self.reference_forward_fn(residual_points),
            dtype=tf.float64,
        )
        if values.shape != residual_points.shape:
            raise ValueError(f"reference_forward_fn: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def _reference_inverse(self, reference_points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(
            self.reference_inverse_fn(reference_points),
            dtype=tf.float64,
        )
        if values.shape != reference_points.shape:
            raise ValueError(f"reference_inverse_fn: {HighDimStatus.INVALID_SHAPE.value}")
        return values

    def _frame_inverse(self, physical_points: tf.Tensor) -> tf.Tensor:
        return tf.linalg.solve(
            self.preconditioner_frame.matrix,
            physical_points - self.preconditioner_frame.mu[:, tf.newaxis],
        )

    def _frame_forward(self, local_points: tf.Tensor) -> tf.Tensor:
        return (
            tf.linalg.matmul(self.preconditioner_frame.matrix, local_points)
            + self.preconditioner_frame.mu[:, tf.newaxis]
        )


@dataclass(frozen=True)
class SourceRoutePreconditionedProposalResult:
    """Proposal correction for the fixed preconditioned Algorithm-5 surface."""

    residual_local_samples: tf.Tensor
    physical_samples: tf.Tensor
    residual_log_density: tf.Tensor
    preconditioner_log_density: tf.Tensor
    reference_log_density: tf.Tensor
    full_negative_log_density: tf.Tensor
    proposal_log_density: tf.Tensor
    target_log_density: tf.Tensor
    correction_log_weights: tf.Tensor
    source_anchor: str = (
        "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/pre_sol.m:245-255"
    )

    def __post_init__(self) -> None:
        residual = tf.convert_to_tensor(self.residual_local_samples, dtype=tf.float64)
        physical = tf.convert_to_tensor(self.physical_samples, dtype=tf.float64)
        if residual.shape.rank != 2 or physical.shape != residual.shape:
            raise ValueError(f"preconditioned samples: {HighDimStatus.INVALID_SHAPE.value}")
        residual_log = _finite_vector("residual_log_density", self.residual_log_density)
        pre_log = _finite_vector("preconditioner_log_density", self.preconditioner_log_density)
        ref_log = _finite_vector("reference_log_density", self.reference_log_density)
        full_neg = _finite_vector("full_negative_log_density", self.full_negative_log_density)
        proposal = _finite_vector("proposal_log_density", self.proposal_log_density)
        target = _finite_vector("target_log_density", self.target_log_density)
        correction = _finite_vector("correction_log_weights", self.correction_log_weights)
        expected_shape = (int(residual.shape[1]),)
        for name, values in (
            ("residual_log_density", residual_log),
            ("preconditioner_log_density", pre_log),
            ("reference_log_density", ref_log),
            ("full_negative_log_density", full_neg),
            ("proposal_log_density", proposal),
            ("target_log_density", target),
            ("correction_log_weights", correction),
        ):
            if values.shape != expected_shape:
                raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
        tf.debugging.assert_near(proposal, residual_log + pre_log - ref_log, atol=1e-10)
        tf.debugging.assert_near(target, -full_neg, atol=1e-10)
        tf.debugging.assert_near(correction, target - proposal, atol=1e-10)
        if not str(self.source_anchor).strip():
            raise ValueError("source_anchor must be nonempty")
        object.__setattr__(self, "residual_local_samples", residual)
        object.__setattr__(self, "physical_samples", physical)
        object.__setattr__(self, "residual_log_density", residual_log)
        object.__setattr__(self, "preconditioner_log_density", pre_log)
        object.__setattr__(self, "reference_log_density", ref_log)
        object.__setattr__(self, "full_negative_log_density", full_neg)
        object.__setattr__(self, "proposal_log_density", proposal)
        object.__setattr__(self, "target_log_density", target)
        object.__setattr__(self, "correction_log_weights", correction)
        object.__setattr__(self, "source_anchor", str(self.source_anchor))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePreconditionedProposalResult",
            "residual_local_samples": self.residual_local_samples,
            "physical_samples": self.physical_samples,
            "residual_log_density": self.residual_log_density,
            "preconditioner_log_density": self.preconditioner_log_density,
            "reference_log_density": self.reference_log_density,
            "full_negative_log_density": self.full_negative_log_density,
            "proposal_log_density": self.proposal_log_density,
            "target_log_density": self.target_log_density,
            "correction_log_weights": self.correction_log_weights,
            "source_anchor": self.source_anchor,
        }


def source_route_preconditioned_proposal_correction(
    *,
    preconditioned_map: SourceRoutePreconditionedMap,
    residual_transport: SourceRouteTransportProtocol,
    reference_samples: tf.Tensor,
    full_negative_log_density_fn,
) -> SourceRoutePreconditionedProposalResult:
    """Generate fixed preconditioned-route proposal corrections.

    This mirrors the author-code density identity in ``pre_sol.m:245-255``:
    residual SIRT inverse samples produce ``p``; ``Tu2x`` maps the residual
    sample into physical space; the proposal log density is residual log
    density plus preconditioner log density minus the residual-reference log
    density; the correction is target minus proposal.
    """

    if not isinstance(preconditioned_map, SourceRoutePreconditionedMap):
        raise TypeError("preconditioned_map must be SourceRoutePreconditionedMap")
    if not isinstance(residual_transport, SourceRouteTransportProtocol):
        raise TypeError("residual_transport must be SourceRouteTransportProtocol")
    if not callable(full_negative_log_density_fn):
        raise TypeError("full_negative_log_density_fn must be callable")
    reference = tf.convert_to_tensor(reference_samples, dtype=tf.float64)
    if (
        reference.shape.rank != 2
        or int(reference.shape[0]) != preconditioned_map.dimension
    ):
        raise ValueError(f"reference_samples: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64("reference_samples", reference)
    if not bool(tf.reduce_all(tf.math.is_finite(reference)).numpy()):
        raise ValueError(f"reference_samples: {HighDimStatus.NONFINITE_VALUE.value}")

    residual_local = residual_transport.inverse_transport(reference)
    physical_samples = preconditioned_map.Tu2x(residual_local)
    residual_log_density = residual_transport.proposal_log_density(
        local_points=residual_local,
        reference_points=reference,
    )
    preconditioner_log_density = preconditioned_map.preconditioner_log_density(
        physical_samples
    )
    reference_log_density = preconditioned_map.reference_log_density(residual_local)
    full_negative_log_density = _finite_vector(
        "full_negative_log_density",
        full_negative_log_density_fn(physical_samples),
    )
    if full_negative_log_density.shape != (int(reference.shape[1]),):
        raise ValueError(f"full_negative_log_density: {HighDimStatus.INVALID_SHAPE.value}")
    proposal_log_density = (
        residual_log_density + preconditioner_log_density - reference_log_density
    )
    target_log_density = -full_negative_log_density
    correction = source_route_proposal_log_weights(
        log_target_density=target_log_density,
        log_proposal_density=proposal_log_density,
    )
    return SourceRoutePreconditionedProposalResult(
        residual_local_samples=residual_local,
        physical_samples=physical_samples,
        residual_log_density=residual_log_density,
        preconditioner_log_density=preconditioner_log_density,
        reference_log_density=reference_log_density,
        full_negative_log_density=full_negative_log_density,
        proposal_log_density=proposal_log_density,
        target_log_density=target_log_density,
        correction_log_weights=correction,
    )


@dataclass(frozen=True)
class SourceRoutePredatorPreyLadderRow:
    """Route-separated M5 predator-prey ladder row."""

    row_id: str
    route_label: str
    horizon: int
    baseline: str
    primary_check: str
    decision_status: str
    non_claims: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("row_id", self.row_id),
            ("route_label", self.route_label),
            ("baseline", self.baseline),
            ("primary_check", self.primary_check),
            ("decision_status", self.decision_status),
        ):
            if not str(value).strip():
                raise ValueError(f"{name} must be nonempty")
        if int(self.horizon) <= 0:
            raise ValueError("horizon must be positive")
        claims = tuple(str(item) for item in self.non_claims)
        if not claims:
            raise ValueError("non_claims must be nonempty")
        object.__setattr__(self, "row_id", str(self.row_id))
        object.__setattr__(self, "route_label", str(self.route_label))
        object.__setattr__(self, "horizon", int(self.horizon))
        object.__setattr__(self, "baseline", str(self.baseline))
        object.__setattr__(self, "primary_check", str(self.primary_check))
        object.__setattr__(self, "decision_status", str(self.decision_status))
        object.__setattr__(self, "non_claims", claims)

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "row_id": self.row_id,
            "route_label": self.route_label,
            "horizon": int(self.horizon),
            "baseline": self.baseline,
            "primary_check": self.primary_check,
            "decision_status": self.decision_status,
            "non_claims": self.non_claims,
        }


@dataclass(frozen=True)
class SourceRoutePredatorPreyLadderManifest:
    """M5 ladder manifest separating fixed-branch and source-route evidence."""

    rows: tuple[SourceRoutePredatorPreyLadderRow, ...]
    fixed_design_failure_interpretation: str
    source_route_claim_status: str
    production_token_emitted: bool

    def __post_init__(self) -> None:
        rows = tuple(self.rows)
        if not rows:
            raise ValueError("rows must be nonempty")
        if not all(isinstance(row, SourceRoutePredatorPreyLadderRow) for row in rows):
            raise TypeError("rows must contain SourceRoutePredatorPreyLadderRow")
        if not str(self.fixed_design_failure_interpretation).strip():
            raise ValueError("fixed_design_failure_interpretation must be nonempty")
        if not str(self.source_route_claim_status).strip():
            raise ValueError("source_route_claim_status must be nonempty")
        if bool(self.production_token_emitted):
            has_source_production_pass = any(
                row.route_label == SOURCE_FAITHFUL_ROUTE_LABEL
                and row.decision_status == "PASS_SOURCE_PRECONDITIONED_FILTERING"
                for row in rows
            )
            if not has_source_production_pass:
                raise ValueError(
                    "production token requires PASS_SOURCE_PRECONDITIONED_FILTERING"
                )
        object.__setattr__(self, "rows", rows)
        object.__setattr__(
            self,
            "fixed_design_failure_interpretation",
            str(self.fixed_design_failure_interpretation),
        )
        object.__setattr__(self, "source_route_claim_status", str(self.source_route_claim_status))
        object.__setattr__(self, "production_token_emitted", bool(self.production_token_emitted))

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRoutePredatorPreyLadderManifest",
            "rows": [row.manifest_payload() for row in self.rows],
            "fixed_design_failure_interpretation": self.fixed_design_failure_interpretation,
            "source_route_claim_status": self.source_route_claim_status,
            "production_token_emitted": bool(self.production_token_emitted),
        }


@dataclass(frozen=True)
class SourceRouteSmoothingBoundary:
    """Boundary contract separating filtering evidence from smoothing evidence."""

    smoothing_status: str
    required_backward_fields: tuple[str, ...]
    filtering_tokens: tuple[str, ...]
    dedicated_smoothing_tokens: tuple[str, ...]
    non_claims: tuple[str, ...]

    def __post_init__(self) -> None:
        status = str(self.smoothing_status)
        if status not in ("deferred", "implemented"):
            raise ValueError("smoothing_status must be deferred or implemented")
        required = tuple(str(item) for item in self.required_backward_fields)
        if not required:
            raise ValueError("required_backward_fields must be nonempty")
        for required_name in (
            "backward_conditional_maps",
            "backward_weights",
            "smoothing_marginal_checks",
        ):
            if required_name not in required:
                raise ValueError(f"required_backward_fields missing {required_name}")
        filtering_tokens = tuple(str(item) for item in self.filtering_tokens)
        smoothing_tokens = tuple(str(item) for item in self.dedicated_smoothing_tokens)
        non_claims = tuple(str(item) for item in self.non_claims)
        if not non_claims:
            raise ValueError("non_claims must be nonempty")
        if status == "implemented" and not smoothing_tokens:
            raise ValueError("implemented smoothing requires a dedicated smoother token")
        if status == "deferred" and smoothing_tokens:
            raise ValueError("deferred smoothing cannot carry smoother pass tokens")
        object.__setattr__(self, "smoothing_status", status)
        object.__setattr__(self, "required_backward_fields", required)
        object.__setattr__(self, "filtering_tokens", filtering_tokens)
        object.__setattr__(self, "dedicated_smoothing_tokens", smoothing_tokens)
        object.__setattr__(self, "non_claims", non_claims)

    def filtering_tokens_are_smoothing_evidence(self) -> bool:
        return False

    def manifest_payload(self) -> Mapping[str, object]:
        return {
            "family": "SourceRouteSmoothingBoundary",
            "smoothing_status": self.smoothing_status,
            "required_backward_fields": self.required_backward_fields,
            "filtering_tokens": self.filtering_tokens,
            "dedicated_smoothing_tokens": self.dedicated_smoothing_tokens,
            "filtering_tokens_are_smoothing_evidence": self.filtering_tokens_are_smoothing_evidence(),
            "non_claims": self.non_claims,
        }


@dataclass(frozen=True)
class SourceRouteRetainedObject:
    """Minimal retained object for the clean-room source-faithful filtering lane."""

    transport_object: object
    coordinate_frame: SourceRouteCoordinateFrame
    samples: tf.Tensor
    log_weights: tf.Tensor
    sample_diagnostics: SourceRouteSampleDiagnostics
    normalizer: SourceRouteNormalizerContribution
    measure_convention: MeasureConvention
    route_label: str
    storage_kind: str
    transition_interface: str
    branch_identity: BranchIdentity
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.coordinate_frame, SourceRouteCoordinateFrame):
            raise TypeError("coordinate_frame must be a SourceRouteCoordinateFrame")
        if not isinstance(self.sample_diagnostics, SourceRouteSampleDiagnostics):
            raise TypeError("sample_diagnostics must be a SourceRouteSampleDiagnostics")
        if not isinstance(self.normalizer, SourceRouteNormalizerContribution):
            raise TypeError("normalizer must be a SourceRouteNormalizerContribution")
        assert_density_matches_mass(self.measure_convention)
        samples = tf.convert_to_tensor(self.samples, dtype=tf.float64)
        log_weights = tf.convert_to_tensor(self.log_weights, dtype=tf.float64)
        if samples.shape.rank != 2:
            raise ValueError(f"samples: {HighDimStatus.INVALID_SHAPE.value}")
        if samples.shape[0] != self.coordinate_frame.dimension:
            raise ValueError(f"samples: {HighDimStatus.INVALID_SHAPE.value}")
        if log_weights.shape != (int(samples.shape[1]),):
            raise ValueError(f"log_weights: {HighDimStatus.INVALID_SHAPE.value}")
        assert_tf_float64("samples", samples)
        assert_tf_float64("log_weights", log_weights)
        if not bool(
            tf.reduce_all(tf.math.is_finite(samples)).numpy()
            and tf.reduce_all(tf.math.is_finite(log_weights)).numpy()
        ):
            raise ValueError(f"SourceRouteRetainedObject: {HighDimStatus.NONFINITE_VALUE.value}")
        if int(samples.shape[1]) != self.sample_diagnostics.sample_count:
            raise ValueError("sample_diagnostics sample_count must match samples")
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be a BranchIdentity")
        _validate_route_storage_contract(
            route_label=str(self.route_label),
            storage_kind=str(self.storage_kind),
            transition_interface=str(self.transition_interface),
        )
        expected_manifest = source_route_retained_object_manifest(
            transport_object=self.transport_object,
            coordinate_frame=self.coordinate_frame,
            samples=samples,
            log_weights=log_weights,
            sample_diagnostics=self.sample_diagnostics,
            normalizer=self.normalizer,
            measure_convention=self.measure_convention,
            route_label=str(self.route_label),
            storage_kind=str(self.storage_kind),
            transition_interface=str(self.transition_interface),
            diagnostics=self.diagnostics,
        )
        expected_identity = BranchIdentity(
            manifest=expected_manifest,
            hash=expected_manifest.sha256(),
        )
        if self.branch_identity.hash.value != expected_identity.hash.value:
            raise ValueError(HighDimStatus.INVALID_BRANCH_MISMATCH.value)
        object.__setattr__(self, "samples", samples)
        object.__setattr__(self, "log_weights", log_weights)
        object.__setattr__(self, "route_label", str(self.route_label))
        object.__setattr__(self, "storage_kind", str(self.storage_kind))
        object.__setattr__(self, "transition_interface", str(self.transition_interface))
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


def normalize_log_weights(log_weights: tf.Tensor) -> tf.Tensor:
    """Return log weights normalized to sum to one."""

    values = _finite_vector("log_weights", log_weights)
    return values - tf.reduce_logsumexp(values)


def effective_sample_size_from_log_weights(log_weights: tf.Tensor) -> tf.Tensor:
    """Compute ESS from finite log weights."""

    normalized = tf.exp(normalize_log_weights(log_weights))
    return 1.0 / tf.reduce_sum(tf.square(normalized))


def source_route_needs_enhancement(
    *,
    effective_sample_size: tf.Tensor,
    sample_count: int,
    min_ess_fraction: float,
) -> bool:
    """Return whether source-route sampling should be enhanced by the ESS gate."""

    diagnostics = SourceRouteSampleDiagnostics(
        sample_count=int(sample_count),
        effective_sample_size=tf.convert_to_tensor(effective_sample_size, dtype=tf.float64),
    )
    threshold = float(min_ess_fraction)
    if threshold <= 0.0 or threshold > 1.0:
        raise ValueError("min_ess_fraction must be in (0, 1]")
    required = threshold * float(diagnostics.sample_count)
    return bool((diagnostics.effective_sample_size < required).numpy())


def source_route_proposal_log_weights(
    *,
    log_target_density: tf.Tensor,
    log_proposal_density: tf.Tensor,
) -> tf.Tensor:
    """Compute proposal-correction log weights in log-density convention.

    The source target is often written as a negative-log objective.  This helper
    deliberately does not accept negative-log values: callers must pass
    ``log_target_density``.  Use
    :func:`source_route_proposal_log_weights_from_negative_log_target` when the
    available target value is a negative log density.
    """

    log_target, log_proposal = _finite_same_shape_vectors(
        "log_target_density",
        log_target_density,
        "log_proposal_density",
        log_proposal_density,
    )
    return log_target - log_proposal


def source_route_proposal_log_weights_from_negative_log_target(
    *,
    negative_log_target: tf.Tensor,
    log_proposal_density: tf.Tensor,
) -> tf.Tensor:
    """Compute correction weights from a negative-log target value."""

    neg_log_target, log_proposal = _finite_same_shape_vectors(
        "negative_log_target",
        negative_log_target,
        "log_proposal_density",
        log_proposal_density,
    )
    return -neg_log_target - log_proposal


def source_route_discrete_log_normalizer_from_correction(
    *,
    log_proposal_density: tf.Tensor,
    correction_log_weights: tf.Tensor,
) -> tf.Tensor:
    """Exact discrete-support normalizer implied by proposal correction."""

    log_proposal, correction = _finite_same_shape_vectors(
        "log_proposal_density",
        log_proposal_density,
        "correction_log_weights",
        correction_log_weights,
    )
    return tf.reduce_logsumexp(log_proposal + correction)


def source_route_equal_weight_log_normalizer_estimate(
    correction_log_weights: tf.Tensor,
) -> tf.Tensor:
    """Monte Carlo log-normalizer estimate for equal-weight proposal samples."""

    correction = _finite_vector("correction_log_weights", correction_log_weights)
    sample_count = tf.cast(tf.shape(correction)[0], tf.float64)
    return tf.reduce_logsumexp(correction) - tf.math.log(sample_count)


def source_route_push_sample_batch(
    *,
    previous_batch: SourceRouteSampleBatch,
    propagated_samples: tf.Tensor,
    log_weights: tf.Tensor,
    time_index: int,
    sample_origin: str = "propagated",
) -> SourceRouteSampleBatch:
    """Create a propagated source-route sample batch with explicit metadata."""

    if not isinstance(previous_batch, SourceRouteSampleBatch):
        raise TypeError("previous_batch must be a SourceRouteSampleBatch")
    samples = tf.convert_to_tensor(propagated_samples, dtype=tf.float64)
    if samples.shape.rank != 2:
        raise ValueError(f"propagated_samples: {HighDimStatus.INVALID_SHAPE.value}")
    if int(samples.shape[1]) != previous_batch.sample_count:
        raise ValueError("propagated_samples must preserve sample count")
    if int(time_index) <= previous_batch.time_index:
        raise ValueError("time_index must advance")
    return SourceRouteSampleBatch(
        samples=samples,
        log_weights=log_weights,
        time_index=int(time_index),
        route_label=previous_batch.route_label,
        sample_origin=str(sample_origin),
    )


def source_route_push_and_augment_samples(
    *,
    previous_batch: SourceRouteSampleBatch,
    transition_fn,
    log_likelihood_fn,
    parameter_dim: int,
    state_dim: int,
    time_index: int,
) -> SourceRoutePushResult:
    """Mirror the source ``push_samples`` and full-solver augmentation step.

    ``previous_batch.samples`` must have shape ``[d + m, N]``.  The transition
    callable receives those samples and the integer time index, then returns
    the next state block with shape ``[m, N]``.  The likelihood callable receives
    the propagated ``[theta, x_t]`` samples and the same time index, then returns
    log likelihood values with shape ``[N]``.  The augmented batch has source
    shape ``[d + 2m, N] = [theta, x_t, x_{t-1}]``.
    """

    if not isinstance(previous_batch, SourceRouteSampleBatch):
        raise TypeError("previous_batch must be a SourceRouteSampleBatch")
    if previous_batch.route_label != SOURCE_FAITHFUL_ROUTE_LABEL:
        raise ValueError("source push requires source_faithful_filtering input")
    d = int(parameter_dim)
    m = int(state_dim)
    if d < 0 or m <= 0:
        raise ValueError("parameter_dim must be nonnegative and state_dim positive")
    expected_dim = d + m
    if previous_batch.dimension != expected_dim:
        raise ValueError("previous_batch dimension must equal parameter_dim + state_dim")
    if int(time_index) <= previous_batch.time_index:
        raise ValueError("time_index must advance")
    theta = previous_batch.samples[:d, :]
    previous_state = previous_batch.samples[d : d + m, :]
    next_state = tf.convert_to_tensor(
        transition_fn(previous_batch.samples, int(time_index)),
        dtype=tf.float64,
    )
    if next_state.shape != previous_state.shape:
        raise ValueError(f"transition output: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(next_state)).numpy()):
        raise ValueError(f"transition output: {HighDimStatus.NONFINITE_VALUE.value}")
    propagated_samples = tf.concat([theta, next_state], axis=0)
    log_likelihood = _finite_vector(
        "log_likelihood",
        log_likelihood_fn(propagated_samples, int(time_index)),
    )
    if log_likelihood.shape != previous_batch.log_weights.shape:
        raise ValueError(f"log_likelihood: {HighDimStatus.INVALID_SHAPE.value}")
    propagated_log_weights = normalize_log_weights(
        previous_batch.log_weights + log_likelihood
    )
    propagated = SourceRouteSampleBatch(
        samples=propagated_samples,
        log_weights=propagated_log_weights,
        time_index=int(time_index),
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="propagated",
    )
    augmented = SourceRouteSampleBatch(
        samples=tf.concat([theta, next_state, previous_state], axis=0),
        log_weights=propagated_log_weights,
        time_index=int(time_index),
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="augmented_propagated",
    )
    return SourceRoutePushResult(
        propagated_batch=propagated,
        augmented_batch=augmented,
        diagnostics=augmented.diagnostics(enhancement_attempts=0),
    )


def build_source_route_target(
    *,
    negative_log_physical_density_fn,
    coordinate_frame: SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    time_index: int,
    source_terms: tuple[str, ...] = ("prior_or_previous", "transition", "likelihood"),
    target_family: str = "full",
) -> SourceRouteTarget:
    """Build a clean-room source-route local target object."""

    return SourceRouteTarget(
        negative_log_physical_density_fn=negative_log_physical_density_fn,
        coordinate_frame=coordinate_frame,
        shift_constant=shift_constant,
        time_index=int(time_index),
        target_family=str(target_family),
        source_terms=tuple(source_terms),
    )


def source_route_generate_retained_samples(
    *,
    target: SourceRouteTarget,
    transport: SourceRouteTransportProtocol,
    reference_samples: tf.Tensor,
    time_index: int,
) -> SourceRouteRetainedSampleResult:
    """Generate retained samples and proposal-correction weights."""

    if not isinstance(target, SourceRouteTarget):
        raise TypeError("target must be SourceRouteTarget")
    if not isinstance(transport, SourceRouteTransportProtocol):
        raise TypeError("transport must be SourceRouteTransportProtocol")
    if int(time_index) != target.time_index:
        raise ValueError("time_index must match target")
    reference = tf.convert_to_tensor(reference_samples, dtype=tf.float64)
    if reference.shape.rank != 2:
        raise ValueError(f"reference_samples: {HighDimStatus.INVALID_SHAPE.value}")
    if int(reference.shape[0]) != target.coordinate_frame.dimension:
        raise ValueError(f"reference_samples: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(reference)).numpy()):
        raise ValueError(f"reference_samples: {HighDimStatus.NONFINITE_VALUE.value}")
    local_samples = transport.inverse_transport(reference)
    physical_samples = target.physical_points_from_reference(local_samples)
    proposal_log_density = transport.proposal_log_density(
        local_points=local_samples,
        reference_points=reference,
    )
    target_log_density = target.log_target_density(local_samples)
    correction = source_route_proposal_log_weights(
        log_target_density=target_log_density,
        log_proposal_density=proposal_log_density,
    )
    normalized_correction = normalize_log_weights(correction)
    retained_batch = SourceRouteSampleBatch(
        samples=physical_samples,
        log_weights=normalized_correction,
        time_index=int(time_index),
        route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
        sample_origin="retained_from_transport",
    )
    diagnostics = retained_batch.diagnostics()
    normalizer = SourceRouteNormalizerContribution(
        log_transport_normalizer=transport.log_normalizer(),
        shift_constant=target.shift_constant,
        log_abs_det_policy=target.log_abs_det_policy,
    )
    return SourceRouteRetainedSampleResult(
        retained_batch=retained_batch,
        proposal_log_density=proposal_log_density,
        target_log_density=target_log_density,
        correction_log_weights=correction,
        diagnostics=diagnostics,
        normalizer=normalizer,
    )


def source_route_previous_marginal_log_density(
    *,
    previous_retained_object: SourceRouteRetainedObject,
    physical_points: tf.Tensor,
    keep_axes: tuple[int, ...],
) -> SourceRoutePreviousMarginalDensityResult:
    """Evaluate the previous retained marginal density used at ``t > 1``.

    This mirrors the author-code prior term in ``full_sol.reapprox``:
    marginalize the previous SIRT to the retained ``[theta, x_{t-1}]`` prefix,
    invert the previous affine frame on that prefix, evaluate the marginal
    SIRT density, then divide by the prefix affine determinant.
    """

    if not isinstance(previous_retained_object, SourceRouteRetainedObject):
        raise TypeError("previous_retained_object must be SourceRouteRetainedObject")
    keep = tuple(int(axis) for axis in keep_axes)
    if not keep:
        raise ValueError("keep_axes must be nonempty")
    if keep != tuple(range(len(keep))):
        raise ValueError("source previous marginalization requires prefix keep axes")
    frame = previous_retained_object.coordinate_frame
    if keep[-1] >= frame.dimension:
        raise ValueError(f"keep_axes: {HighDimStatus.INVALID_SHAPE.value}")
    points = tf.convert_to_tensor(physical_points, dtype=tf.float64)
    if points.shape.rank != 2 or int(points.shape[0]) != len(keep):
        raise ValueError(f"physical_points: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64("physical_points", points)
    if not bool(tf.reduce_all(tf.math.is_finite(points)).numpy()):
        raise ValueError(f"physical_points: {HighDimStatus.NONFINITE_VALUE.value}")
    transport = SourceRouteTransportProtocol(
        previous_retained_object.transport_object
    )
    marginal_transport = transport.marginalize(keep)
    mu_prefix = tf.gather(frame.mu, keep)
    matrix_prefix = tf.gather(tf.gather(frame.matrix, keep, axis=0), keep, axis=1)
    local_points = tf.linalg.solve(
        matrix_prefix,
        points - mu_prefix[:, tf.newaxis],
    )
    eval_pdf = _source_route_eval_marginal_pdf(marginal_transport, local_points)
    if not bool(tf.reduce_all(eval_pdf > 0.0).numpy()):
        raise ValueError(f"previous_marginal_eval_pdf: {HighDimStatus.NONFINITE_VALUE.value}")
    log_density = tf.math.log(eval_pdf) - tf.math.log(
        tf.abs(tf.linalg.det(matrix_prefix))
    )
    return SourceRoutePreviousMarginalDensityResult(
        previous_retained_object=previous_retained_object,
        keep_axes=keep,
        marginal_transport=marginal_transport,
        physical_points=points,
        local_points=local_points,
        log_density=log_density,
    )


def _source_route_eval_marginal_pdf(marginal_transport: object, local_points: tf.Tensor) -> tf.Tensor:
    local = tf.convert_to_tensor(local_points, dtype=tf.float64)
    if local.shape.rank != 2:
        raise ValueError(f"local_points: {HighDimStatus.INVALID_SHAPE.value}")
    if callable(getattr(marginal_transport, "eval_pdf", None)):
        values = tf.convert_to_tensor(marginal_transport.eval_pdf(local), dtype=tf.float64)
    elif callable(getattr(marginal_transport, "normalized_retained_density_values", None)):
        values = tf.convert_to_tensor(
            marginal_transport.normalized_retained_density_values(tf.transpose(local)),
            dtype=tf.float64,
        )
    else:
        raise TypeError("marginal transport must provide eval_pdf or normalized_retained_density_values")
    if values.shape != (int(local.shape[1]),):
        raise ValueError(f"previous_marginal_eval_pdf: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(values)).numpy()):
        raise ValueError(f"previous_marginal_eval_pdf: {HighDimStatus.NONFINITE_VALUE.value}")
    return values


def source_route_sequential_negative_log_physical_density(
    *,
    physical_points: tf.Tensor,
    time_index: int,
    parameter_dim: int,
    state_dim: int,
    transition_log_density_fn,
    likelihood_log_density_fn,
    prior_log_density_fn=None,
    previous_retained_object: SourceRouteRetainedObject | None = None,
) -> tf.Tensor:
    """Author-style sequential negative-log density in physical coordinates.

    Physical points use the source ordering ``[theta, x_t, x_{t-1}]``.  At
    ``t=1`` the prior term is supplied by ``prior_log_density_fn`` on
    ``[theta, x_0]``.  At ``t>1`` it is supplied by the previous retained SIRT
    marginal over its ``[theta, x_{t-1}]`` prefix.
    """

    points = tf.convert_to_tensor(physical_points, dtype=tf.float64)
    if points.shape.rank != 2:
        raise ValueError(f"physical_points: {HighDimStatus.INVALID_SHAPE.value}")
    d = int(parameter_dim)
    m = int(state_dim)
    if d < 0 or m <= 0:
        raise ValueError("parameter_dim must be nonnegative and state_dim positive")
    expected_dim = d + 2 * m
    if int(points.shape[0]) != expected_dim:
        raise ValueError(f"physical_points: {HighDimStatus.INVALID_SHAPE.value}")
    if int(time_index) < 1:
        raise ValueError("time_index must be positive")
    if not callable(transition_log_density_fn):
        raise TypeError("transition_log_density_fn must be callable")
    if not callable(likelihood_log_density_fn):
        raise TypeError("likelihood_log_density_fn must be callable")
    input_axes = tuple(range(d)) + tuple(range(d + m, d + 2 * m))
    prior_points = tf.gather(points, input_axes, axis=0)
    if int(time_index) == 1:
        if prior_log_density_fn is None or not callable(prior_log_density_fn):
            raise TypeError("t=1 requires callable prior_log_density_fn")
        prior_log_density = _finite_vector(
            "prior_log_density",
            prior_log_density_fn(prior_points),
        )
    else:
        if prior_log_density_fn is not None:
            raise ValueError("t>1 uses previous retained marginal, not prior_log_density_fn")
        if previous_retained_object is None:
            raise TypeError("t>1 requires previous_retained_object")
        keep_axes = tuple(range(d + m))
        previous_density = source_route_previous_marginal_log_density(
            previous_retained_object=previous_retained_object,
            physical_points=prior_points,
            keep_axes=keep_axes,
        )
        prior_log_density = previous_density.log_density
    transition_log_density = _finite_vector(
        "transition_log_density",
        transition_log_density_fn(points, int(time_index)),
    )
    likelihood_log_density = _finite_vector(
        "likelihood_log_density",
        likelihood_log_density_fn(points, int(time_index)),
    )
    if (
        prior_log_density.shape != transition_log_density.shape
        or prior_log_density.shape != likelihood_log_density.shape
    ):
        raise ValueError(f"source sequential density: {HighDimStatus.INVALID_SHAPE.value}")
    return -prior_log_density - transition_log_density - likelihood_log_density


def source_route_default_operation_audit(
    *,
    source_anchor: str = "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-130",
    notes: str = "P57-M6 fixed-HMC source-loop operation coverage",
) -> SourceRouteImplementationAudit:
    """Build the fixed-HMC source-loop operation audit used by M6."""

    return SourceRouteImplementationAudit(
        records=tuple(
            SourceRouteOperationRecord(
                operation_id=operation_id,
                source_anchor=str(source_anchor),
                implementation_status="implemented",
                route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
                notes=str(notes),
            )
            for operation_id in SOURCE_ROUTE_REQUIRED_OPERATION_IDS
        ),
    )


def _source_route_step_target_from_components(
    *,
    spec: SourceRouteSequentialStepSpec,
    previous_retained_object: SourceRouteRetainedObject | None,
) -> SourceRouteTarget:
    def negative_log_physical(points: tf.Tensor) -> tf.Tensor:
        return spec.density_components.negative_log_physical_density(
            physical_points=points,
            time_index=spec.time_index,
            previous_retained_object=previous_retained_object,
        )

    return SourceRouteTarget(
        negative_log_physical_density_fn=negative_log_physical,
        coordinate_frame=spec.target.coordinate_frame,
        shift_constant=spec.target.shift_constant,
        time_index=spec.time_index,
        target_family=spec.target.target_family,
        source_terms=spec.target.source_terms,
        log_abs_det_policy=spec.target.log_abs_det_policy,
    )


def source_route_run_sequential_fixed_hmc(
    *,
    step_specs: tuple[SourceRouteSequentialStepSpec, ...],
    branch_audit: SourceRouteImplementationAudit | None = None,
) -> SourceRouteSequentialResult:
    """Run the replayable sequential source-route skeleton for fixed HMC.

    The caller supplies frozen targets, transports, reference samples, and
    branch schedules.  This function enforces the retained-object carry and the
    previous retained marginalization gate; it does not fit TT/SIRT objects or
    choose ranks.
    """

    specs = tuple(step_specs)
    if len(specs) < 2:
        raise ValueError("sequential source loop requires at least two steps")
    if not all(isinstance(spec, SourceRouteSequentialStepSpec) for spec in specs):
        raise TypeError("step_specs must contain SourceRouteSequentialStepSpec")
    expected_times = tuple(range(1, len(specs) + 1))
    actual_times = tuple(spec.time_index for spec in specs)
    if actual_times != expected_times:
        raise ValueError("step_specs must be consecutive starting at t=1")
    audit = branch_audit or source_route_default_operation_audit()
    if audit.status != "PASS_SOURCE_ROUTE_OPERATION_COVERAGE":
        raise ValueError("branch_audit must pass source-route operation coverage")

    previous_retained: SourceRouteRetainedObject | None = None
    steps: list[SourceRouteSequentialStepResult] = []
    for spec in specs:
        step_target = _source_route_step_target_from_components(
            spec=spec,
            previous_retained_object=previous_retained,
        )
        current_reference = spec.transport.inverse_transport(spec.reference_samples)
        current_physical = step_target.physical_points_from_reference(
            current_reference
        )
        if spec.time_index == 1:
            previous_marginal_density = None
        else:
            if previous_retained is None:
                raise ValueError("t>1 requires previous retained object")
            if (
                spec.previous_marginal_keep_axes is None
                or spec.previous_marginal_input_axes is None
            ):
                raise ValueError("t>1 requires previous marginal axes")
            previous_physical = tf.gather(
                current_physical,
                spec.previous_marginal_input_axes,
                axis=0,
            )
            previous_marginal_density = source_route_previous_marginal_log_density(
                previous_retained_object=previous_retained,
                physical_points=previous_physical,
                keep_axes=spec.previous_marginal_keep_axes,
            )

        component_negative_log = spec.density_components.negative_log_physical_density(
            physical_points=current_physical,
            time_index=spec.time_index,
            previous_retained_object=previous_retained,
        )
        target_negative_log = _finite_vector(
            "target_negative_log_physical_density",
            step_target.negative_log_physical_density_fn(current_physical),
        )
        tf.debugging.assert_near(
            target_negative_log,
            component_negative_log,
            atol=1e-10,
        )

        retained_samples = source_route_generate_retained_samples(
            target=step_target,
            transport=spec.transport,
            reference_samples=spec.reference_samples,
            time_index=spec.time_index,
        )
        diagnostics = {
            "phase": "P57-M6",
            "time_index": int(spec.time_index),
            "sequential_status": "sequential_fixed_hmc_source_loop",
            "source_anchor": (
                "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21-130"
            ),
            "previous_retained_hash": (
                None
                if previous_retained is None
                else previous_retained.branch_identity.hash.value
            ),
            "previous_marginal_keep_axes": spec.previous_marginal_keep_axes,
            "previous_marginal_input_axes": spec.previous_marginal_input_axes,
        }
        identity = source_route_retained_object_identity(
            transport_object=spec.transport.transport_object,
            coordinate_frame=step_target.coordinate_frame,
            samples=retained_samples.retained_batch.samples,
            log_weights=retained_samples.retained_batch.log_weights,
            sample_diagnostics=retained_samples.diagnostics,
            normalizer=retained_samples.normalizer,
            measure_convention=spec.measure_convention,
            route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind=spec.storage_kind,
            transition_interface=spec.transition_interface,
            diagnostics=diagnostics,
        )
        retained_object = SourceRouteRetainedObject(
            transport_object=spec.transport.transport_object,
            coordinate_frame=step_target.coordinate_frame,
            samples=retained_samples.retained_batch.samples,
            log_weights=retained_samples.retained_batch.log_weights,
            sample_diagnostics=retained_samples.diagnostics,
            normalizer=retained_samples.normalizer,
            measure_convention=spec.measure_convention,
            route_label=SOURCE_FAITHFUL_ROUTE_LABEL,
            storage_kind=spec.storage_kind,
            transition_interface=spec.transition_interface,
            branch_identity=identity,
            diagnostics=diagnostics,
        )
        step = SourceRouteSequentialStepResult(
            spec=spec,
            target=step_target,
            retained_samples=retained_samples,
            retained_object=retained_object,
            previous_retained_object=previous_retained,
            previous_marginal_density=previous_marginal_density,
        )
        steps.append(step)
        previous_retained = retained_object

    return SourceRouteSequentialResult(
        steps=tuple(steps),
        branch_audit=audit,
    )


def source_route_one_step_reapproximation(
    *,
    target: SourceRouteTarget,
    transport: SourceRouteTransportProtocol,
    reference_samples: tf.Tensor,
    time_index: int,
    previous_retained_object: object | None = None,
) -> SourceRouteOneStepResult:
    """Run the P55 one-step source reapproximation boundary.

    This is deliberately limited to ``t=1``.  A later phase must implement
    previous retained-object marginalization before any sequential source-route
    claim is allowed.
    """

    if int(time_index) != 1 or target.time_index != 1:
        raise ValueError(
            "P55 one-step source reapproximation only supports t=1; "
            "previous retained-object marginalization is not implemented"
        )
    if previous_retained_object is not None:
        raise ValueError(
            "previous retained-object marginalization is not implemented"
        )
    retained = source_route_generate_retained_samples(
        target=target,
        transport=transport,
        reference_samples=reference_samples,
        time_index=int(time_index),
    )
    return SourceRouteOneStepResult(
        target=target,
        transport=transport,
        retained_samples=retained,
        time_index=int(time_index),
    )


def source_route_recenter(
    *,
    samples: tf.Tensor,
    log_weights: tf.Tensor,
    expansion_factor: float,
    covariance_jitter: float = 1e-5,
    quantile_fraction: float = 0.01,
    min_ess_for_quantile_scale: float = 1000.0,
    use_quantile_scale: bool = True,
) -> SourceRouteCoordinateFrame:
    """Compute the source-route weighted affine recentering frame.

    This follows the author-code ``computeL`` structure: weighted mean,
    weighted covariance, Cholesky factor with jitter, and, when ESS is large
    enough, a diagonal quantile stretch in whitened coordinates.  The final
    expansion factor corresponds to the source ``epd`` multiplier.
    """

    sample_tensor = tf.convert_to_tensor(samples, dtype=tf.float64)
    if sample_tensor.shape.rank != 2:
        raise ValueError(f"samples: {HighDimStatus.INVALID_SHAPE.value}")
    log_weight_tensor = tf.convert_to_tensor(log_weights, dtype=tf.float64)
    if log_weight_tensor.shape != (int(sample_tensor.shape[1]),):
        raise ValueError(f"log_weights: {HighDimStatus.INVALID_SHAPE.value}")
    finite_columns = tf.reduce_all(tf.math.is_finite(sample_tensor), axis=0)
    finite_weights = tf.math.is_finite(log_weight_tensor)
    keep = tf.logical_and(finite_columns, finite_weights)
    if not bool(tf.reduce_any(keep).numpy()):
        raise ValueError(f"samples/log_weights: {HighDimStatus.NONFINITE_VALUE.value}")
    sample_tensor = tf.boolean_mask(sample_tensor, keep, axis=1)
    log_weight_tensor = tf.boolean_mask(log_weight_tensor, keep)
    weights = tf.exp(normalize_log_weights(log_weight_tensor))
    if float(expansion_factor) <= 0.0:
        raise ValueError("expansion_factor must be positive")
    jitter = float(covariance_jitter)
    if jitter < 0.0:
        raise ValueError("covariance_jitter must be nonnegative")
    q = float(quantile_fraction)
    if q <= 0.0 or q >= 0.5:
        raise ValueError("quantile_fraction must be in (0, 0.5)")
    min_ess = float(min_ess_for_quantile_scale)
    if min_ess < 0.0:
        raise ValueError("min_ess_for_quantile_scale must be nonnegative")
    assert_tf_float64("samples", sample_tensor)
    mu = tf.reduce_sum(sample_tensor * weights[tf.newaxis, :], axis=1)
    centered = sample_tensor - mu[:, tf.newaxis]
    covariance = tf.einsum("n,in,jn->ij", weights, centered, centered)
    covariance = 0.5 * (covariance + tf.transpose(covariance))
    if jitter > 0.0:
        dim = int(sample_tensor.shape[0])
        covariance = covariance + tf.eye(dim, dtype=tf.float64) * tf.constant(
            jitter,
            dtype=tf.float64,
        )
    matrix = tf.linalg.cholesky(covariance)
    ess = effective_sample_size_from_log_weights(log_weight_tensor)
    if bool(use_quantile_scale) and bool((ess > min_ess).numpy()):
        standardized = tf.linalg.triangular_solve(matrix, centered, lower=True)
        scale_diag = _source_route_computeL_quantile_scale(
            standardized,
            weights,
            quantile_fraction=q,
        )
        matrix = tf.matmul(matrix, tf.linalg.diag(scale_diag))
    matrix = matrix * tf.constant(
        float(expansion_factor),
        dtype=tf.float64,
    )
    return SourceRouteCoordinateFrame(
        mu=mu,
        matrix=matrix,
        expansion_factor=float(expansion_factor),
    )


def source_route_reference_log_density_from_physical(
    *,
    log_physical_density: tf.Tensor,
    coordinate_frame: SourceRouteCoordinateFrame,
) -> tf.Tensor:
    """Convert physical log density to local-coordinate log density."""

    log_density = tf.convert_to_tensor(log_physical_density, dtype=tf.float64)
    if log_density.shape.rank not in (0, 1):
        raise ValueError(f"log_physical_density: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64("log_physical_density", log_density)
    if not bool(tf.reduce_all(tf.math.is_finite(log_density)).numpy()):
        raise ValueError(f"log_physical_density: {HighDimStatus.NONFINITE_VALUE.value}")
    return log_density + coordinate_frame.log_abs_det()


def source_route_shifted_negative_log_target(
    *,
    negative_log_target: tf.Tensor,
    shift_constant: tf.Tensor,
) -> tf.Tensor:
    """Apply the source-style stability shift to a negative-log target."""

    target = tf.convert_to_tensor(negative_log_target, dtype=tf.float64)
    shift = tf.convert_to_tensor(shift_constant, dtype=tf.float64)
    if target.shape.rank not in (0, 1):
        raise ValueError(f"negative_log_target: {HighDimStatus.INVALID_SHAPE.value}")
    if shift.shape.rank != 0:
        raise ValueError(f"shift_constant: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64("negative_log_target", target)
    assert_tf_float64("shift_constant", shift)
    if not bool(
        tf.reduce_all(tf.math.is_finite(target)).numpy()
        and tf.math.is_finite(shift).numpy()
    ):
        raise ValueError(f"source_route_shifted_negative_log_target: {HighDimStatus.NONFINITE_VALUE.value}")
    return target - shift


def source_route_log_normalizer_update(
    *,
    log_transport_normalizer: tf.Tensor,
    shift_constant: tf.Tensor,
) -> tf.Tensor:
    """Return the source-style log-likelihood increment `log(z) - const`."""

    normalizer = SourceRouteNormalizerContribution(
        log_transport_normalizer=log_transport_normalizer,
        shift_constant=shift_constant,
        log_abs_det_policy="included_in_target",
    )
    return normalizer.log_increment()


def source_route_residual_negative_log_target(
    *,
    full_negative_log_target: tf.Tensor,
    preconditioner_negative_log_target: tf.Tensor,
) -> tf.Tensor:
    """Return residual negative-log target so preconditioner plus residual is full."""

    full, preconditioner = _finite_same_shape_vectors(
        "full_negative_log_target",
        full_negative_log_target,
        "preconditioner_negative_log_target",
        preconditioner_negative_log_target,
    )
    return full - preconditioner


def source_route_preconditioned_target_identity_error(
    *,
    full_negative_log_target: tf.Tensor,
    preconditioner_negative_log_target: tf.Tensor,
    residual_negative_log_target: tf.Tensor,
) -> tf.Tensor:
    """Return max absolute error in the full = preconditioner + residual identity."""

    full, preconditioner = _finite_same_shape_vectors(
        "full_negative_log_target",
        full_negative_log_target,
        "preconditioner_negative_log_target",
        preconditioner_negative_log_target,
    )
    _, residual = _finite_same_shape_vectors(
        "full_negative_log_target",
        full,
        "residual_negative_log_target",
        residual_negative_log_target,
    )
    return tf.reduce_max(tf.abs(full - (preconditioner + residual)))


def source_route_retained_object_identity(
    *,
    transport_object: object,
    coordinate_frame: SourceRouteCoordinateFrame,
    samples: tf.Tensor,
    log_weights: tf.Tensor,
    sample_diagnostics: SourceRouteSampleDiagnostics,
    normalizer: SourceRouteNormalizerContribution,
    measure_convention: MeasureConvention,
    route_label: str,
    storage_kind: str,
    transition_interface: str,
    diagnostics: Mapping[str, object] | None = None,
) -> BranchIdentity:
    """Build the canonical identity for a source-route retained object."""

    manifest = source_route_retained_object_manifest(
        transport_object=transport_object,
        coordinate_frame=coordinate_frame,
        samples=tf.convert_to_tensor(samples, dtype=tf.float64),
        log_weights=tf.convert_to_tensor(log_weights, dtype=tf.float64),
        sample_diagnostics=sample_diagnostics,
        normalizer=normalizer,
        measure_convention=measure_convention,
        route_label=str(route_label),
        storage_kind=str(storage_kind),
        transition_interface=str(transition_interface),
        diagnostics=diagnostics,
    )
    return BranchIdentity(manifest=manifest, hash=manifest.sha256())


def source_route_retained_object_manifest(
    *,
    transport_object: object,
    coordinate_frame: SourceRouteCoordinateFrame,
    samples: tf.Tensor,
    log_weights: tf.Tensor,
    sample_diagnostics: SourceRouteSampleDiagnostics,
    normalizer: SourceRouteNormalizerContribution,
    measure_convention: MeasureConvention,
    route_label: str,
    storage_kind: str,
    transition_interface: str,
    diagnostics: Mapping[str, object] | None = None,
) -> BranchManifest:
    """Create a canonical retained-object manifest."""

    assert_density_matches_mass(measure_convention)
    _validate_route_storage_contract(
        route_label=str(route_label),
        storage_kind=str(storage_kind),
        transition_interface=str(transition_interface),
    )
    transport_payload = _transport_manifest_payload(transport_object)
    return BranchManifest(
        version="source_route_retained_object.v1",
        payload={
            "transport_object": transport_payload,
            "coordinate_frame": coordinate_frame.manifest_payload(),
            "samples": samples,
            "log_weights": log_weights,
            "sample_diagnostics": sample_diagnostics.manifest_payload(),
            "normalizer": normalizer.manifest_payload(),
            "measure_convention": {
                "density_measure": measure_convention.density_measure.value,
                "mass_measure": measure_convention.mass_measure.value,
                "reference_weight_name": measure_convention.reference_weight_name,
                "physical_coordinate_name": measure_convention.physical_coordinate_name,
                "reference_coordinate_name": measure_convention.reference_coordinate_name,
                "dtype_name": measure_convention.dtype_name,
            },
            "route_label": str(route_label),
            "storage_kind": str(storage_kind),
            "transition_interface": str(transition_interface),
            "diagnostics": freeze_mapping(diagnostics),
        },
    )


def _validate_route_storage_contract(
    *,
    route_label: str,
    storage_kind: str,
    transition_interface: str,
) -> None:
    if not route_label.strip():
        raise ValueError("route_label must be nonempty")
    if not storage_kind.strip():
        raise ValueError("storage_kind must be nonempty")
    if not transition_interface.strip():
        raise ValueError("transition_interface must be nonempty")
    if route_label == SOURCE_FAITHFUL_ROUTE_LABEL:
        if storage_kind in _FORBIDDEN_SOURCE_STORAGE_KINDS:
            raise ValueError(
                "source-faithful retained object cannot use all-grid retained storage"
            )
        if transition_interface in _FORBIDDEN_SOURCE_TRANSITION_INTERFACES:
            raise ValueError(
                "source-faithful retained object cannot use pairwise grid propagation"
            )


def _transport_manifest_payload(transport_object: object) -> Mapping[str, object]:
    manifest_payload = getattr(transport_object, "manifest_payload", None)
    if callable(manifest_payload):
        payload = manifest_payload()
    elif isinstance(transport_object, SquaredTTMarginal):
        payload = {
            "family": "SquaredTTMarginal",
            "source_contract_level": "fixed_ttsirt_marginal",
            "keep_axes": transport_object.keep_axes,
            "normalizer": transport_object.normalizer,
            "diagnostics": transport_object.diagnostics,
        }
    else:
        raise TypeError("transport_object must expose manifest_payload()")
    if not isinstance(payload, Mapping):
        raise TypeError("transport_object manifest_payload() must return a mapping")
    return payload


def _source_route_computeL_quantile_scale(
    standardized_samples: tf.Tensor,
    weights: tf.Tensor,
    *,
    quantile_fraction: float,
) -> tf.Tensor:
    samples = tf.convert_to_tensor(standardized_samples, dtype=tf.float64)
    normalized_weights = tf.convert_to_tensor(weights, dtype=tf.float64)
    if samples.shape.rank != 2 or normalized_weights.shape != (int(samples.shape[1]),):
        raise ValueError(f"quantile scale: {HighDimStatus.INVALID_SHAPE.value}")
    q = tf.constant(float(quantile_fraction), dtype=tf.float64)
    normal_q = tfp_normal_quantile(q)
    scales = []
    for axis in range(int(samples.shape[0])):
        values = samples[axis, :]
        order = tf.argsort(values, stable=True)
        sorted_values = tf.gather(values, order)
        sorted_weights = tf.gather(normalized_weights, order)
        cumulative = tf.cumsum(sorted_weights)
        left_index = tf.argmax(tf.cast(cumulative > q, tf.int32), output_type=tf.int32)
        right_index = tf.argmax(
            tf.cast(cumulative > (1.0 - q), tf.int32),
            output_type=tf.int32,
        )
        width = tf.gather(sorted_values, right_index) - tf.gather(sorted_values, left_index)
        scale = -width / normal_q / 2.0
        scales.append(tf.maximum(scale, tf.constant(1e-12, dtype=tf.float64)))
    return tf.stack(scales)


def tfp_normal_quantile(probability: tf.Tensor) -> tf.Tensor:
    """Return the standard-normal quantile using TensorFlow primitives."""

    p = tf.convert_to_tensor(probability, dtype=tf.float64)
    if p.shape.rank != 0:
        raise ValueError(f"probability: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.math.is_finite(p).numpy()) or not bool((p > 0.0).numpy() and (p < 1.0).numpy()):
        raise ValueError("probability must be in (0, 1)")
    return tf.sqrt(tf.constant(2.0, dtype=tf.float64)) * tf.math.erfinv(
        2.0 * p - 1.0
    )


def _finite_vector(name: str, value: tf.Tensor) -> tf.Tensor:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    if tensor.shape.rank != 1:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    assert_tf_float64(name, tensor)
    if not bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy()):
        raise ValueError(f"{name}: {HighDimStatus.NONFINITE_VALUE.value}")
    return tensor


def _finite_same_shape_vectors(
    left_name: str,
    left: tf.Tensor,
    right_name: str,
    right: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    left_tensor = _finite_vector(left_name, left)
    right_tensor = _finite_vector(right_name, right)
    if left_tensor.shape != right_tensor.shape:
        raise ValueError(f"{left_name}/{right_name}: {HighDimStatus.INVALID_SHAPE.value}")
    return left_tensor, right_tensor
