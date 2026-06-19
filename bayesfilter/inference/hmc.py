"""Small generic HMC-runtime helpers with fail-closed authority checks."""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

from bayesfilter.inference.mass_matrix import (
    covariance_from_negative_hessian,
    whitening_from_covariance,
)
from bayesfilter.inference.hmc_tuning import (
    HMCTuningPolicy,
    normalize_hmc_tuning_policy,
    require_executable_tuning_policy,
)
from bayesfilter.inference.batched_value_score import reviewed_value_score_target_fn
from bayesfilter.inference.posterior_adapter import value_score_capability


_PROCESS_LOCAL_SIGNATURE_PATTERNS = (
    re.compile(r"\b0x[0-9a-fA-F]+\b"),
    re.compile(r"\bobject at\b"),
    re.compile(r"\bid\s*\("),
)


@dataclass(frozen=True)
class PrecomputedMAP:
    """Shape- and adapter-scoped precomputed MAP/mass artifact metadata."""

    position: Any
    covariance: Any
    adapter_signature: str
    source: str = "precomputed_map"


@dataclass(frozen=True)
class PrecomputedMassArtifact:
    """Validated precomputed position/covariance/factor metadata for HMC.

    The artifact separates the role of the position from the mass matrix.  A
    caller may persist a true MAP, but diagnostic centers such as a known truth
    or prior center must use a non-MAP ``position_role`` so downstream gates do
    not silently promote initialization geometry into a MAP-quality claim.
    """

    position: Any
    covariance: Any
    factor: Any
    adapter_signature: str
    position_role: str = "map"
    covariance_source: str = "unspecified"
    matrix_used_for_square_root: str = "covariance"
    factor_orientation: str = "row_right_transpose"
    source: str = "precomputed_mass_artifact"
    eigen_summary: Mapping[str, Any] | None = None
    precision_eigen_summary: Mapping[str, Any] | None = None
    regularization_report: Mapping[str, Any] | None = None
    log_jacobian_convention: str = "constant_omitted"
    nonclaims: tuple[str, ...] = (
        "precomputed mass artifact only",
        "no posterior convergence claim",
        "no production MAP quality claim",
        "no sampler readiness claim",
    )
    reconstruction_rtol: float = 1.0e-10
    reconstruction_atol: float = 1.0e-10

    def __post_init__(self) -> None:
        position = np.asarray(self.position, dtype=float).copy()
        covariance = np.asarray(self.covariance, dtype=float).copy()
        factor = np.asarray(self.factor, dtype=float).copy()
        if position.ndim != 1:
            raise ValueError("precomputed mass position must be a one-dimensional vector")
        dim = int(position.shape[0])
        if covariance.shape != (dim, dim):
            raise ValueError("precomputed mass covariance shape must match position dimension")
        if factor.shape != (dim, dim):
            raise ValueError("precomputed mass factor shape must match position dimension")
        if not np.all(np.isfinite(position)):
            raise ValueError("precomputed mass position must be finite")
        if not np.all(np.isfinite(covariance)):
            raise ValueError("precomputed mass covariance must be finite")
        if not np.all(np.isfinite(factor)):
            raise ValueError("precomputed mass factor must be finite")
        if not np.allclose(covariance, covariance.T, rtol=self.reconstruction_rtol, atol=self.reconstruction_atol):
            raise ValueError("precomputed mass covariance must be symmetric")
        orientation = str(self.factor_orientation)
        if orientation != "row_right_transpose":
            raise ValueError("factor_orientation must be 'row_right_transpose'")
        reconstruction = factor @ factor.T
        if not np.allclose(
            reconstruction,
            covariance,
            rtol=float(self.reconstruction_rtol),
            atol=float(self.reconstruction_atol),
        ):
            raise ValueError(
                "precomputed mass factor must reconstruct covariance as factor @ factor.T"
            )
        convention = str(self.log_jacobian_convention)
        if convention not in {"constant_omitted", "constant_included"}:
            raise ValueError(
                "log_jacobian_convention must be 'constant_omitted' or 'constant_included'"
            )
        signature = _validate_persisted_signature(str(self.adapter_signature))
        position_role = str(self.position_role)
        if not position_role:
            raise ValueError("position_role must be non-empty")
        covariance_source = str(self.covariance_source)
        if not covariance_source:
            raise ValueError("covariance_source must be non-empty")
        matrix_used = str(self.matrix_used_for_square_root)
        if not matrix_used:
            raise ValueError("matrix_used_for_square_root must be non-empty")
        source = str(self.source)
        if not source:
            raise ValueError("source must be non-empty")
        actual_eigen_summary = _covariance_eigen_summary(covariance)
        if not bool(actual_eigen_summary["finite"]):
            raise ValueError("precomputed mass covariance eigenvalues must be finite")
        if not bool(actual_eigen_summary["positive"]):
            raise ValueError("precomputed mass covariance must be positive definite")
        eigen_summary = (
            actual_eigen_summary
            if self.eigen_summary is None
            else _normalize_eigen_summary(self.eigen_summary)
        )
        if not bool(eigen_summary["finite"]):
            raise ValueError("precomputed mass covariance eigenvalues must be finite")
        if not bool(eigen_summary["positive"]):
            raise ValueError("precomputed mass covariance must be positive definite")
        precision_eigen_summary = (
            None
            if self.precision_eigen_summary is None
            else _normalize_eigen_summary(self.precision_eigen_summary)
        )
        regularization_report = (
            {}
            if self.regularization_report is None
            else dict(self.regularization_report)
        )
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        position.setflags(write=False)
        covariance.setflags(write=False)
        factor.setflags(write=False)
        object.__setattr__(self, "position", position)
        object.__setattr__(self, "covariance", covariance)
        object.__setattr__(self, "factor", factor)
        object.__setattr__(self, "adapter_signature", signature)
        object.__setattr__(self, "position_role", position_role)
        object.__setattr__(self, "covariance_source", covariance_source)
        object.__setattr__(self, "matrix_used_for_square_root", matrix_used)
        object.__setattr__(self, "factor_orientation", orientation)
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "eigen_summary", eigen_summary)
        object.__setattr__(self, "precision_eigen_summary", precision_eigen_summary)
        object.__setattr__(self, "regularization_report", regularization_report)
        object.__setattr__(self, "log_jacobian_convention", convention)
        object.__setattr__(self, "nonclaims", nonclaims)
        object.__setattr__(self, "reconstruction_rtol", float(self.reconstruction_rtol))
        object.__setattr__(self, "reconstruction_atol", float(self.reconstruction_atol))

    @classmethod
    def from_covariance(
        cls,
        *,
        position: Any,
        covariance: Any,
        adapter_signature: str,
        position_role: str = "map",
        covariance_source: str,
        matrix_used_for_square_root: str = "regularized_covariance",
        source: str = "precomputed_covariance",
        jitter: float = 1.0e-9,
        **kwargs: Any,
    ) -> "PrecomputedMassArtifact":
        regularized = np.asarray(covariance, dtype=float) + float(jitter) * np.eye(
            np.asarray(covariance, dtype=float).shape[0]
        )
        factor = whitening_from_covariance(covariance, jitter=jitter)
        return cls(
            position=position,
            covariance=regularized,
            factor=factor,
            adapter_signature=adapter_signature,
            position_role=position_role,
            covariance_source=covariance_source,
            matrix_used_for_square_root=matrix_used_for_square_root,
            source=source,
            **kwargs,
        )

    @classmethod
    def from_negative_hessian(
        cls,
        *,
        position: Any,
        negative_hessian: Any,
        adapter_signature: str,
        position_role: str = "map",
        covariance_source: str = "negative_hessian",
        matrix_used_for_square_root: str = "covariance_from_negative_hessian",
        source: str = "negative_hessian",
        jitter: float = 1.0e-9,
        eigenvalue_floor: float | None = None,
        max_condition_number: float | None = None,
        dense: bool = True,
        **kwargs: Any,
    ) -> "PrecomputedMassArtifact":
        mass = covariance_from_negative_hessian(
            negative_hessian,
            source=covariance_source,
            jitter=jitter,
            eigenvalue_floor=eigenvalue_floor,
            max_condition_number=max_condition_number,
            dense=dense,
        )
        factor = whitening_from_covariance(mass.covariance, jitter=0.0)
        return cls(
            position=position,
            covariance=mass.covariance,
            factor=factor,
            adapter_signature=adapter_signature,
            position_role=position_role,
            covariance_source=mass.source,
            matrix_used_for_square_root=matrix_used_for_square_root,
            source=source,
            eigen_summary=mass.covariance_eigen_summary,
            precision_eigen_summary=mass.precision_eigen_summary,
            regularization_report=mass.regularization_report,
            **kwargs,
        )

    @property
    def dimension(self) -> int:
        return int(self.position.shape[0])

    def validate_for_adapter(
        self,
        adapter: Any,
        *,
        expected_dim: int | None = None,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        if expected_dim is not None and self.dimension != int(expected_dim):
            raise ValueError(
                f"precomputed mass dimension {self.dimension} does not match {expected_dim}"
            )
        expected_signature = stable_adapter_signature(adapter)
        if self.adapter_signature != expected_signature:
            raise ValueError("precomputed mass adapter signature mismatch")
        return self.position, self.covariance, self.factor

    def build_latent_transform(self) -> "LatentAffineHMCTransform":
        return LatentAffineHMCTransform(
            center=self.position,
            factor=self.factor,
            factor_orientation=self.factor_orientation,
            covariance_provenance=self.covariance_source,
            log_jacobian_convention=self.log_jacobian_convention,
            nonclaims=self.nonclaims,
        )

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "dimension": self.dimension,
            "adapter_signature": self.adapter_signature,
            "position_role": self.position_role,
            "covariance_source": self.covariance_source,
            "matrix_used_for_square_root": self.matrix_used_for_square_root,
            "factor_orientation": self.factor_orientation,
            "source": self.source,
            "eigen_summary": self.eigen_summary,
            "precision_eigen_summary": self.precision_eigen_summary,
            "regularization_report": self.regularization_report,
            "log_jacobian_convention": self.log_jacobian_convention,
            "nonclaims": self.nonclaims,
        }

    def to_payload(self, *, include_arrays: bool = False) -> Mapping[str, Any]:
        """Return a JSON-safe reload payload, optionally including arrays.

        ``signature_payload`` remains the stable metadata-only fingerprint
        surface.  This method is the durable handoff schema for callers that
        need to persist and rehydrate the validated mass artifact.
        """

        payload = dict(self.signature_payload())
        payload.update(
            {
                "artifact_type": "bayesfilter_precomputed_mass_artifact",
                "schema_version": 1,
                "include_arrays": bool(include_arrays),
                "reconstruction_rtol": self.reconstruction_rtol,
                "reconstruction_atol": self.reconstruction_atol,
            }
        )
        payload["eigen_summary"] = _json_safe_metadata(self.eigen_summary)
        payload["precision_eigen_summary"] = _json_safe_metadata(
            self.precision_eigen_summary
        )
        payload["regularization_report"] = _json_safe_metadata(
            self.regularization_report
        )
        payload["nonclaims"] = list(self.nonclaims)
        if include_arrays:
            payload.update(
                {
                    "position": np.asarray(self.position, dtype=float).tolist(),
                    "covariance": np.asarray(self.covariance, dtype=float).tolist(),
                    "factor": np.asarray(self.factor, dtype=float).tolist(),
                }
            )
        return payload

    @classmethod
    def from_payload(
        cls,
        payload: Mapping[str, Any],
        *,
        expected_adapter_signature: str | None = None,
        expected_dim: int | None = None,
    ) -> "PrecomputedMassArtifact":
        """Rehydrate a validated artifact from an array-bearing payload."""

        if not isinstance(payload, Mapping):
            raise TypeError("precomputed mass payload must be a mapping")
        if payload.get("artifact_type") != "bayesfilter_precomputed_mass_artifact":
            raise ValueError("precomputed mass payload artifact_type mismatch")
        if int(payload.get("schema_version", -1)) != 1:
            raise ValueError("precomputed mass payload schema_version mismatch")
        if expected_adapter_signature is not None:
            expected = _validate_persisted_signature(str(expected_adapter_signature))
            observed = _validate_persisted_signature(str(payload.get("adapter_signature", "")))
            if observed != expected:
                raise ValueError("precomputed mass payload adapter signature mismatch")
        if expected_dim is not None:
            expected_dimension = int(expected_dim)
            observed_dimension = int(payload.get("dimension", -1))
            if observed_dimension != expected_dimension:
                raise ValueError("precomputed mass payload dimension mismatch")
        missing_arrays = tuple(
            key for key in ("position", "covariance", "factor") if key not in payload
        )
        if missing_arrays:
            raise ValueError(
                "precomputed mass payload missing required array fields: "
                + ", ".join(missing_arrays)
            )
        return cls(
            position=payload["position"],
            covariance=payload["covariance"],
            factor=payload["factor"],
            adapter_signature=str(payload.get("adapter_signature", "")),
            position_role=str(payload.get("position_role", "map")),
            covariance_source=str(payload.get("covariance_source", "")),
            matrix_used_for_square_root=str(
                payload.get("matrix_used_for_square_root", "")
            ),
            factor_orientation=str(
                payload.get("factor_orientation", "row_right_transpose")
            ),
            source=str(payload.get("source", "")),
            eigen_summary=None,
            precision_eigen_summary=payload.get("precision_eigen_summary"),
            regularization_report=payload.get("regularization_report"),
            log_jacobian_convention=str(
                payload.get("log_jacobian_convention", "constant_omitted")
            ),
            nonclaims=tuple(str(item) for item in payload.get("nonclaims", ())),
            reconstruction_rtol=float(payload.get("reconstruction_rtol", 1.0e-10)),
            reconstruction_atol=float(payload.get("reconstruction_atol", 1.0e-10)),
        )


@dataclass(frozen=True)
class LatentAffineHMCTransform:
    """Metadata-bearing row-vector affine transform for latent HMC states.

    The transform is

    ``theta = center + z @ factor.T``

    with latent score ``grad_z = factor.T @ grad_theta`` for a scalar target
    evaluated at ``theta``.  The orientation field is semantic authority, not a
    display label: callers must not reinterpret ``factor`` as a left-multiply or
    column-vector convention.
    """

    center: Any
    factor: Any
    factor_orientation: str = "row_right_transpose"
    covariance_provenance: str = "unspecified"
    log_jacobian_convention: str = "constant_omitted"
    nonclaims: tuple[str, ...] = (
        "affine coordinate transform only",
        "no posterior convergence claim",
        "no sampler readiness claim",
    )

    def __post_init__(self) -> None:
        center = np.asarray(self.center, dtype=float)
        factor = np.asarray(self.factor, dtype=float)
        if center.ndim != 1:
            raise ValueError("latent affine center must be a one-dimensional vector")
        dim = int(center.shape[0])
        if factor.shape != (dim, dim):
            raise ValueError("latent affine factor must be square and match center dimension")
        if not np.all(np.isfinite(center)):
            raise ValueError("latent affine center must be finite")
        if not np.all(np.isfinite(factor)):
            raise ValueError("latent affine factor must be finite")
        orientation = str(self.factor_orientation)
        if orientation != "row_right_transpose":
            raise ValueError("factor_orientation must be 'row_right_transpose'")
        convention = str(self.log_jacobian_convention)
        if convention not in {"constant_omitted", "constant_included"}:
            raise ValueError(
                "log_jacobian_convention must be 'constant_omitted' or 'constant_included'"
            )
        provenance = str(self.covariance_provenance)
        if not provenance:
            raise ValueError("covariance_provenance must be non-empty")
        nonclaims = tuple(str(item) for item in self.nonclaims)
        if not nonclaims:
            raise ValueError("nonclaims must be non-empty")
        object.__setattr__(self, "center", center)
        object.__setattr__(self, "factor", factor)
        object.__setattr__(self, "factor_orientation", orientation)
        object.__setattr__(self, "covariance_provenance", provenance)
        object.__setattr__(self, "log_jacobian_convention", convention)
        object.__setattr__(self, "nonclaims", nonclaims)

    @property
    def dimension(self) -> int:
        return int(self.center.shape[0])

    def latent_to_position(self, z: Any) -> np.ndarray:
        """Map scalar or batched row-vector latent coordinates to positions."""

        z_array = self._validate_latent_shape(z)
        return self.center + z_array @ self.factor.T

    def position_to_latent(self, theta: Any) -> np.ndarray:
        """Invert the affine map for nonsingular factors."""

        theta_array = self._validate_position_shape(theta)
        delta = theta_array - self.center
        try:
            solved = np.linalg.solve(self.factor, np.moveaxis(delta, -1, 0))
            return np.moveaxis(solved, 0, -1)
        except np.linalg.LinAlgError as exc:
            raise ValueError("latent affine factor must be nonsingular to invert") from exc

    def theta_score_to_latent_score(self, grad_theta: Any) -> np.ndarray:
        """Apply the chain rule ``grad_z = factor.T @ grad_theta`` row-wise."""

        grad_array = self._validate_position_shape(grad_theta)
        return grad_array @ self.factor

    def value_and_score(
        self,
        z: Any,
        value_and_grad_fn: Callable[[np.ndarray], tuple[Any, Any]],
    ) -> tuple[Any, np.ndarray]:
        """Evaluate a theta-target and return the corresponding latent score."""

        theta = self.latent_to_position(z)
        value, grad_theta = value_and_grad_fn(theta)
        return value, self.theta_score_to_latent_score(grad_theta)

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "dimension": self.dimension,
            "factor_orientation": self.factor_orientation,
            "covariance_provenance": self.covariance_provenance,
            "log_jacobian_convention": self.log_jacobian_convention,
            "nonclaims": self.nonclaims,
        }

    def _validate_latent_shape(self, value: Any) -> np.ndarray:
        array = np.asarray(value, dtype=float)
        if array.shape[-1:] != (self.dimension,):
            raise ValueError("latent coordinate trailing dimension must match transform dimension")
        if not np.all(np.isfinite(array)):
            raise ValueError("latent coordinates must be finite")
        return array

    def _validate_position_shape(self, value: Any) -> np.ndarray:
        array = np.asarray(value, dtype=float)
        if array.shape[-1:] != (self.dimension,):
            raise ValueError("position/score trailing dimension must match transform dimension")
        if not np.all(np.isfinite(array)):
            raise ValueError("position/score values must be finite")
        return array


@dataclass(frozen=True)
class FullChainHMCConfig:
    """Tiny full-chain TFP HMC runtime configuration."""

    num_results: int
    num_burnin_steps: int
    step_size: float
    num_leapfrog_steps: int
    seed: tuple[int, int]
    use_xla: bool = False
    trace_policy: str = "standard"
    target_status_trace_policy: str = "none"
    adaptation_policy: str = "fixed_kernel_no_adaptation"
    tuning_policy: str | HMCTuningPolicy | None = None
    target_scope: str | None = None
    chain_execution_mode: str = "tf_function"

    def __post_init__(self) -> None:
        for name in ("num_results", "num_burnin_steps", "num_leapfrog_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        step_size = float(self.step_size)
        if not np.isfinite(step_size) or step_size <= 0.0:
            raise ValueError("step_size must be positive and finite")
        object.__setattr__(self, "step_size", step_size)
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        chain_execution_mode = str(self.chain_execution_mode)
        if chain_execution_mode not in {"tf_function", "eager"}:
            raise ValueError("chain_execution_mode must be 'tf_function' or 'eager'")
        if self.use_xla and chain_execution_mode != "tf_function":
            raise ValueError("XLA full-chain HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", chain_execution_mode)
        policy = str(self.trace_policy)
        if policy not in {"standard", "reduced"}:
            raise ValueError("trace_policy must be 'standard' or 'reduced'")
        object.__setattr__(self, "trace_policy", policy)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy not in {"none", "per_chain_step"}:
            raise ValueError(
                "target_status_trace_policy must be 'none' or 'per_chain_step'"
            )
        if target_status_policy != "none" and policy != "standard":
            raise ValueError(
                "target-status telemetry requires trace_policy='standard'"
            )
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        adaptation_policy = str(self.adaptation_policy)
        if self.tuning_policy is None:
            if adaptation_policy != "fixed_kernel_no_adaptation":
                raise ValueError(
                    "BayesFilter HMC adaptation is fail-closed; raw adaptation_policy "
                    "strings support only fixed_kernel_no_adaptation. Pass a reviewed "
                    "HMCTuningPolicy object for diagnostic adaptation."
                )
            tuning_policy = normalize_hmc_tuning_policy(adaptation_policy)
        else:
            if adaptation_policy != "fixed_kernel_no_adaptation":
                raise ValueError(
                    "adaptation_policy strings other than fixed_kernel_no_adaptation "
                    "remain unsupported; use tuning_policy=HMCTuningPolicy(...)"
                )
            tuning_policy = normalize_hmc_tuning_policy(self.tuning_policy)
            require_executable_tuning_policy(tuning_policy)
            if tuning_policy.uses_windowed_mass_adaptation:
                raise ValueError(
                    "windowed mass adaptation is executable only through the "
                    "Phase 4 windowed diagnostic runner, not run_full_chain_tfp_hmc"
                )
            if tuning_policy.uses_dual_averaging and tuning_policy.label != "fixed_mass_dual_averaging":
                raise ValueError(
                    "dual-averaging HMC execution requires fixed_mass_dual_averaging "
                    "in this phase"
                )
        if (
            tuning_policy.num_adaptation_steps > 0
            and tuning_policy.num_adaptation_steps > self.num_burnin_steps
        ):
            raise ValueError("tuning policy adaptation steps must not exceed burnin steps")
        if tuning_policy.uses_dual_averaging and self.use_xla:
            raise ValueError("dual-averaging HMC is not reviewed for XLA in this phase")
        object.__setattr__(self, "tuning_policy", tuning_policy)
        object.__setattr__(self, "adaptation_policy", tuning_policy.adaptation_policy)
        if self.target_scope is not None:
            object.__setattr__(self, "target_scope", str(self.target_scope))

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": self.seed,
            "use_xla": self.use_xla,
            "chain_execution_mode": self.chain_execution_mode,
            "trace_policy": self.trace_policy,
            "target_status_trace_policy": self.target_status_trace_policy,
            "adaptation_policy": self.adaptation_policy,
            "tuning_policy": self.tuning_policy.payload(),
            "target_scope": self.target_scope,
        }


@dataclass(frozen=True)
class FullChainHMCRunResult:
    """Tensor-valued full-chain HMC result plus engineering metadata."""

    samples: Any
    trace: Mapping[str, Any]
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]


class ReusableFullChainHMCRunner:
    """Reusable compiled TFP HMC runner for a fixed static HMC contract.

    The ordinary ``run_full_chain_tfp_hmc`` helper builds a TensorFlow/TFP
    ``sample_chain`` callable and immediately calls it once.  That is fine for
    tiny gates, but expensive model clients may need to amortize TensorFlow's
    first-call graph construction.  This runner owns the same BayesFilter HMC
    target, kernel, trace, authority checks, and result schema, but compiles the
    chain callable once for a static state shape.  Per-call ``current_state``,
    ``seed``, and scalar ``step_size`` are tensor arguments, so repeated calls
    can reuse the compiled graph without changing HMC semantics.

    The interface is deliberately narrow: ``num_results``, burn-in length,
    leapfrog count, trace policy, tuning policy, XLA flag, and target scope are
    fixed by ``FullChainHMCConfig``.  A different value for any of those fields
    requires a different runner.
    """

    def __init__(
        self,
        adapter: Any,
        initial_state_template: Any,
        config: FullChainHMCConfig,
    ) -> None:
        self.adapter = adapter
        self.config = config
        self.capability = _validate_full_chain_hmc_authority(adapter, config)

        import tensorflow as tf

        template = tf.cast(tf.convert_to_tensor(initial_state_template), tf.float64)
        if template.shape.rank is None:
            raise ValueError("reusable HMC runner requires static state rank")
        if any(dim is None for dim in template.shape):
            raise ValueError("reusable HMC runner requires fully static state shape")
        self._state_shape = tuple(int(dim) for dim in template.shape)
        self._state_dtype = template.dtype
        self._initial_state_template = template
        self._target_log_prob = _make_tfp_target_log_prob_fn(
            adapter,
            dtype=self._state_dtype,
        )
        self._trace_fn = _trace_fn_for_config(config, adapter=adapter)
        self._runner = self._build_runner()
        self._call_count = 0
        self._first_call_s: float | None = None
        self._warm_call_s: float | None = None

    @property
    def state_shape(self) -> tuple[int, ...]:
        return self._state_shape

    @property
    def state_dtype(self) -> str:
        return self._state_dtype.name

    def run(
        self,
        *,
        current_state: Any | None = None,
        seed: tuple[int, int] | Any | None = None,
        step_size: float | Any | None = None,
    ) -> FullChainHMCRunResult:
        """Run one chain call with tensor-parameterized state, seed, and step."""

        import tensorflow as tf

        state = self._initial_state_template if current_state is None else current_state
        state_tensor = tf.convert_to_tensor(state, dtype=self._state_dtype)
        if tuple(state_tensor.shape.as_list()) != self._state_shape:
            raise ValueError("current_state shape must match reusable runner template")
        seed_value = self.config.seed if seed is None else seed
        seed_tensor = tf.convert_to_tensor(seed_value, dtype=tf.int32)
        if tuple(seed_tensor.shape.as_list()) != (2,):
            raise ValueError("seed must have static shape (2,)")
        step_value = self.config.step_size if step_size is None else step_size
        step_tensor = tf.convert_to_tensor(step_value, dtype=self._state_dtype)
        if step_tensor.shape.rank != 0:
            raise ValueError("step_size must be a scalar")

        sample_chain_start = time.perf_counter()
        samples, trace = self._runner(state_tensor, seed_tensor, step_tensor)
        sample_chain_call_s = time.perf_counter() - sample_chain_start
        self._call_count += 1
        if self._call_count == 1:
            self._first_call_s = sample_chain_call_s
            self._warm_call_s = None
        else:
            self._warm_call_s = sample_chain_call_s

        trace_for_diagnostics = trace if self.config.trace_policy == "standard" else {}
        diagnostics = _full_chain_hmc_diagnostics(
            samples,
            trace_for_diagnostics,
            trace_policy=self.config.trace_policy,
        )
        metadata = self._metadata(
            sample_chain_call_s=sample_chain_call_s,
            trace=trace if isinstance(trace, Mapping) else None,
        )
        return FullChainHMCRunResult(
            samples=samples,
            trace=trace,
            diagnostics=diagnostics,
            metadata=metadata,
        )

    __call__ = run

    def _build_runner(self) -> Callable[[Any, Any, Any], tuple[Any, Mapping[str, Any]]]:
        import tensorflow as tf
        import tensorflow_probability as tfp

        tfm = tfp.mcmc
        config = self.config
        target_log_prob = self._target_log_prob
        trace_fn = self._trace_fn

        def run_chain(current_state: Any, seed: Any, step_size: Any) -> tuple[Any, Mapping[str, Any]]:
            kernel = tfm.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob,
                step_size=step_size,
                num_leapfrog_steps=config.num_leapfrog_steps,
            )
            if config.tuning_policy.uses_dual_averaging:
                kernel = tfm.DualAveragingStepSizeAdaptation(
                    inner_kernel=kernel,
                    num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
                    target_accept_prob=tf.constant(
                        config.tuning_policy.target_accept_prob,
                        dtype=current_state.dtype,
                    ),
                )
            return tfm.sample_chain(
                num_results=config.num_results,
                num_burnin_steps=config.num_burnin_steps,
                current_state=current_state,
                kernel=kernel,
                trace_fn=trace_fn,
                seed=seed,
            )

        if config.chain_execution_mode == "eager":
            return run_chain
        input_signature = [
            tf.TensorSpec(shape=self._state_shape, dtype=self._state_dtype),
            tf.TensorSpec(shape=(2,), dtype=tf.int32),
            tf.TensorSpec(shape=(), dtype=self._state_dtype),
        ]
        if config.use_xla:
            return tf.function(
                run_chain,
                input_signature=input_signature,
                jit_compile=True,
                reduce_retracing=True,
            )
        return tf.function(
            run_chain,
            input_signature=input_signature,
            reduce_retracing=True,
        )

    def _metadata(
        self,
        *,
        sample_chain_call_s: float,
        trace: Mapping[str, Any] | None,
    ) -> Mapping[str, Any]:
        config = self.config
        capability = self.capability
        return {
            "runtime": "tfp.mcmc.sample_chain",
            "reusable_runner": True,
            "jit_compile": config.use_xla,
            "chain_execution_mode": config.chain_execution_mode,
            "trace_policy": config.trace_policy,
            "target_status_trace_policy": config.target_status_trace_policy,
            "adaptation_policy": config.adaptation_policy,
            "tuning_policy": config.tuning_policy.payload(),
            "adaptation_policy_source": config.tuning_policy.source,
            "trace_unavailability": _trace_unavailability(
                config.trace_policy,
                trace,
                target_status_trace_policy=config.target_status_trace_policy,
            ),
            "value_score_authority": capability.value_score_authority,
            "target_scope": capability.target_scope,
            "requested_target_scope": config.target_scope,
            "program_signature": program_signature(
                {
                    "adapter": stable_adapter_signature(self.adapter),
                    "capability": {
                        "value_score_authority": capability.value_score_authority,
                        "xla_hmc_ready": capability.xla_hmc_ready,
                        "full_chain_xla_diagnostic_ready": (
                            capability.full_chain_xla_diagnostic_ready
                        ),
                        "runtime_backend": capability.runtime_backend,
                        "target_scope": capability.target_scope,
                        "evidence_path": capability.evidence_path,
                        "nonclaims": capability.nonclaims,
                    },
                    "config": config.signature_payload(),
                    "initial_state_shape": self._state_shape,
                    "initial_state_dtype": self._state_dtype.name,
                    "dynamic_inputs": ("current_state", "seed", "step_size"),
                }
            ),
            "initial_state_shape": self._state_shape,
            "initial_state_dtype": self._state_dtype.name,
            "dynamic_inputs": ("current_state", "seed", "step_size"),
            "seed_source": "runtime_tensor_argument",
            "current_state_source": "runtime_tensor_argument",
            "step_size_source": "runtime_tensor_argument",
            "sample_chain_call_s": sample_chain_call_s,
            "sample_chain_invocation_count": self._call_count,
            "sample_chain_timing_scope": (
                "reusable_compiled_runner_first_call_compile_plus_execute_then_warm_execute"
            ),
            "first_call_s": self._first_call_s,
            "warm_call_s": self._warm_call_s,
            "warm_sample_shape": None,
            "warm_trace_keys": tuple(sorted(trace.keys())) if trace is not None else tuple(),
            "nonclaims": (
                "reusable full-chain HMC engineering runner only",
                "no sampler convergence claim",
                "no posterior validity claim",
                "no GPU readiness claim",
                "no performance superiority claim",
            ),
        }


def build_reusable_full_chain_tfp_hmc_runner(
    adapter: Any,
    initial_state_template: Any,
    config: FullChainHMCConfig,
) -> ReusableFullChainHMCRunner:
    """Build a reusable BayesFilter TFP HMC runner for a static contract."""

    return ReusableFullChainHMCRunner(adapter, initial_state_template, config)


def _make_hmc_target_log_prob_fn(
    adapter: Any,
    *,
    use_xla: bool = False,
    target_scope: str | None = None,
) -> Callable[[Any], Any]:
    """Build a target value function, refusing XLA without reviewed authority."""

    capability = value_score_capability(adapter)
    if use_xla and not capability.is_accepted_xla_hmc_authority:
        raise ValueError(
            "XLA HMC requires graph-native or reviewed value/score authority; "
            f"got {capability.value_score_authority!r}"
        )
    if use_xla and capability.target_scope is not None and str(target_scope) != capability.target_scope:
        raise ValueError("value/score target_scope mismatch")

    def target_log_prob(theta: Any) -> Any:
        if hasattr(adapter, "log_prob"):
            return adapter.log_prob(theta)
        if hasattr(adapter, "log_prob_and_grad"):
            value, _grad = adapter.log_prob_and_grad(theta)
            return value
        raise TypeError("adapter must expose log_prob or log_prob_and_grad")

    return target_log_prob


def _validate_full_chain_hmc_authority(
    adapter: Any,
    config: FullChainHMCConfig,
) -> Any:
    """Return adapter value/score authority after full-chain HMC checks."""

    capability = value_score_capability(adapter)
    if config.use_xla and not capability.is_accepted_full_chain_xla_diagnostic_authority:
        raise ValueError(
            "XLA full-chain HMC requires explicit full-chain-XLA diagnostic "
            "authority; target-only XLA readiness is not sufficient; got "
            f"{capability.value_score_authority!r}"
        )
    if config.use_xla and capability.target_scope is not None:
        if config.target_scope != capability.target_scope:
            raise ValueError("value/score target_scope mismatch")
    return capability


def run_full_chain_tfp_hmc(
    adapter: Any,
    initial_state: Any,
    config: FullChainHMCConfig,
) -> FullChainHMCRunResult:
    """Run exact ``tfp.mcmc.sample_chain`` for a tiny engineering HMC gate.

    This wrapper deliberately materializes no tensors to NumPy inside the
    compiled sampling path.  It returns TensorFlow tensors and metadata only;
    callers may convert tensors after this function returns.
    """

    capability = _validate_full_chain_hmc_authority(adapter, config)

    import tensorflow as tf
    import tensorflow_probability as tfp

    tfm = tfp.mcmc
    state = tf.cast(tf.convert_to_tensor(initial_state), tf.float64)
    _ = _make_hmc_target_log_prob_fn(
        adapter,
        use_xla=config.use_xla,
        target_scope=config.target_scope,
    )
    target_log_prob = _make_tfp_target_log_prob_fn(
        adapter,
        dtype=state.dtype,
    )
    kernel = tfm.HamiltonianMonteCarlo(
        target_log_prob_fn=target_log_prob,
        step_size=tf.constant(config.step_size, dtype=state.dtype),
        num_leapfrog_steps=config.num_leapfrog_steps,
    )
    if config.tuning_policy.uses_dual_averaging:
        kernel = tfm.DualAveragingStepSizeAdaptation(
            inner_kernel=kernel,
            num_adaptation_steps=config.tuning_policy.num_adaptation_steps,
            target_accept_prob=tf.constant(
                config.tuning_policy.target_accept_prob,
                dtype=state.dtype,
            ),
    )
    trace_fn = _trace_fn_for_config(config, adapter=adapter)
    runner = _build_sample_chain_runner(config, kernel, trace_fn, state)
    sample_chain_start = time.perf_counter()
    samples, trace = runner()
    sample_chain_call_s = time.perf_counter() - sample_chain_start
    trace_for_diagnostics = trace if config.trace_policy == "standard" else {}
    diagnostics = _full_chain_hmc_diagnostics(
        samples,
        trace_for_diagnostics,
        trace_policy=config.trace_policy,
    )
    metadata = {
        "runtime": "tfp.mcmc.sample_chain",
        "jit_compile": config.use_xla,
        "chain_execution_mode": config.chain_execution_mode,
        "trace_policy": config.trace_policy,
        "target_status_trace_policy": config.target_status_trace_policy,
        "adaptation_policy": config.adaptation_policy,
        "tuning_policy": config.tuning_policy.payload(),
        "adaptation_policy_source": config.tuning_policy.source,
        "trace_unavailability": _trace_unavailability(
            config.trace_policy,
            trace if isinstance(trace, Mapping) else None,
            target_status_trace_policy=config.target_status_trace_policy,
        ),
        "value_score_authority": capability.value_score_authority,
        "target_scope": capability.target_scope,
        "requested_target_scope": config.target_scope,
        "program_signature": program_signature(
            {
                "adapter": stable_adapter_signature(adapter),
                "capability": {
                    "value_score_authority": capability.value_score_authority,
                    "xla_hmc_ready": capability.xla_hmc_ready,
                    "full_chain_xla_diagnostic_ready": (
                        capability.full_chain_xla_diagnostic_ready
                    ),
                    "runtime_backend": capability.runtime_backend,
                    "target_scope": capability.target_scope,
                    "evidence_path": capability.evidence_path,
                    "nonclaims": capability.nonclaims,
                },
                "config": config.signature_payload(),
                "initial_state_shape": tuple(int(dim) for dim in state.shape),
                "initial_state_dtype": state.dtype.name,
            }
        ),
        "sample_chain_call_s": sample_chain_call_s,
        "sample_chain_invocation_count": 1,
        "sample_chain_timing_scope": "compile_plus_execute_when_xla_first_call",
        "initial_state_shape": tuple(int(dim) for dim in state.shape),
        "initial_state_dtype": state.dtype.name,
        "first_call_s": sample_chain_call_s,
        "warm_call_s": None,
        "warm_sample_shape": None,
        "warm_trace_keys": tuple(),
        "nonclaims": (
            "tiny full-chain HMC engineering gate only",
            "no sampler convergence claim",
            "no posterior validity claim",
            "no GPU readiness claim",
            "no performance superiority claim",
        ),
    }
    return FullChainHMCRunResult(
        samples=samples,
        trace=trace,
        diagnostics=diagnostics,
        metadata=metadata,
    )


def stable_adapter_signature(adapter: Any) -> str:
    """Return stable adapter metadata without process-local object identity."""

    explicit = getattr(adapter, "adapter_signature", None)
    if explicit is not None:
        signature = explicit() if callable(explicit) else explicit
        return _validate_persisted_signature(str(signature))
    payload: dict[str, Any] = {
        "class": adapter.__class__.__qualname__,
        "module": adapter.__class__.__module__,
    }
    if hasattr(adapter, "parameter_dim"):
        payload["parameter_dim"] = int(getattr(adapter, "parameter_dim"))
    names = getattr(adapter, "parameter_names", None)
    if names is not None:
        values = names() if callable(names) else names
        payload["parameter_names"] = tuple(str(name) for name in values)
    return program_signature(payload)


def _validate_persisted_signature(signature: str) -> str:
    if not signature:
        raise ValueError("adapter_signature must be non-empty")
    if any(pattern.search(signature) for pattern in _PROCESS_LOCAL_SIGNATURE_PATTERNS):
        raise ValueError(
            "adapter_signature must not contain process-local object identity"
        )
    return signature


def _json_safe_metadata(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe_metadata(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe_metadata(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json_safe_metadata(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value


def _covariance_eigen_summary(covariance: np.ndarray) -> Mapping[str, Any]:
    eigenvalues = np.linalg.eigvalsh(0.5 * (covariance + covariance.T))
    finite = bool(np.all(np.isfinite(eigenvalues)))
    positive = bool(finite and float(np.min(eigenvalues)) > 0.0)
    return {
        "finite": finite,
        "positive": positive,
        "min": float(np.min(eigenvalues)) if finite else float("nan"),
        "max": float(np.max(eigenvalues)) if finite else float("nan"),
        "condition_number": (
            float(np.max(eigenvalues) / np.min(eigenvalues)) if positive else float("inf")
        ),
        "eigenvalues": tuple(float(value) for value in eigenvalues),
    }


def _normalize_eigen_summary(summary: Mapping[str, Any]) -> Mapping[str, Any]:
    eigenvalues = summary.get("eigenvalues", ())
    return {
        "finite": bool(summary.get("finite")),
        "positive": bool(summary.get("positive")),
        "min": float(summary.get("min")),
        "max": float(summary.get("max")),
        "condition_number": float(summary.get("condition_number")),
        "eigenvalues": tuple(float(value) for value in eigenvalues),
    }


def validate_precomputed_map(
    artifact: PrecomputedMAP,
    adapter: Any,
    *,
    expected_dim: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Validate reusable MAP/mass metadata before it can be consumed."""

    position = np.asarray(artifact.position, dtype=float)
    covariance = np.asarray(artifact.covariance, dtype=float)
    if position.ndim != 1:
        raise ValueError("precomputed MAP position must be a one-dimensional vector")
    dim = int(position.shape[0])
    if expected_dim is not None and dim != int(expected_dim):
        raise ValueError(f"precomputed MAP dimension {dim} does not match {expected_dim}")
    if covariance.shape != (dim, dim):
        raise ValueError(
            "precomputed covariance shape must match the MAP position dimension"
        )
    expected_signature = stable_adapter_signature(adapter)
    if str(artifact.adapter_signature) != expected_signature:
        raise ValueError("precomputed MAP adapter signature mismatch")
    return position, covariance


def latent_to_position(z: Any, center: Any, whitening_factor: Any) -> np.ndarray:
    """Map row-vector latent coordinates with theta = center + z @ W.T."""

    transform = LatentAffineHMCTransform(
        center=center,
        factor=whitening_factor,
        covariance_provenance="legacy_whitening_factor",
    )
    return transform.latent_to_position(z)


def latent_value_and_score(
    z: Any,
    center: Any,
    whitening_factor: Any,
    value_and_grad_fn: Callable[[np.ndarray], tuple[Any, Any]],
) -> tuple[Any, np.ndarray]:
    """Evaluate a transformed target and map theta-score to latent-score."""

    transform = LatentAffineHMCTransform(
        center=center,
        factor=whitening_factor,
        covariance_provenance="legacy_whitening_factor",
    )
    return transform.value_and_score(z, value_and_grad_fn)


def static_unroll_chain_value_and_score(
    adapter: Any,
    chain_state: Any,
    *,
    use_xla: bool = False,
    target_scope: str | None = None,
) -> tuple[Any, Any]:
    """Evaluate value/score for a statically sized chain batch.

    This helper intentionally uses a static Python unroll over the leading
    chain axis.  It avoids ``tf.map_fn``/``tf.vectorized_map`` TensorArray
    semantics in early XLA gates and fails closed when the chain axis is not
    statically known.
    """

    capability = value_score_capability(adapter)
    if use_xla and not capability.is_accepted_xla_hmc_authority:
        raise ValueError(
            "XLA chain-batched value/score requires graph-native or reviewed authority; "
            f"got {capability.value_score_authority!r}"
        )
    if use_xla and capability.target_scope is not None and str(target_scope) != capability.target_scope:
        raise ValueError("value/score target_scope mismatch")
    if not hasattr(adapter, "log_prob_and_grad"):
        raise TypeError("adapter must expose log_prob_and_grad for chain value/score")

    shape = getattr(chain_state, "shape", None)
    rank = getattr(shape, "rank", None)
    if rank is None and shape is not None:
        rank = len(shape)
    if rank != 2:
        raise ValueError("chain_state must have static rank 2 [chain, parameter]")
    chain_count = shape[0]
    parameter_dim = shape[1]
    if chain_count is None or parameter_dim is None:
        raise ValueError("chain_state must have static chain and parameter dimensions")

    values = []
    scores = []
    for index in range(int(chain_count)):
        value, score = adapter.log_prob_and_grad(chain_state[index])
        values.append(value)
        scores.append(score)
    return _stack_like_chain(chain_state, values), _stack_like_chain(chain_state, scores)


def _make_tfp_target_log_prob_fn(
    adapter: Any,
    *,
    dtype: Any,
) -> Callable[[Any], Any]:
    if hasattr(adapter, "log_prob_and_grad"):
        return reviewed_value_score_target_fn(adapter, dtype=dtype)
    return _make_hmc_target_log_prob_fn(adapter)


def _broadcast_upstream_gradient_to_score(dy: Any, score: Any) -> Any:
    """Broadcast target upstream gradients over trailing parameter axes only."""

    import tensorflow as tf

    score_tensor = tf.convert_to_tensor(score)
    upstream = tf.cast(dy, score_tensor.dtype)
    upstream_shape = upstream.shape
    score_shape = score_tensor.shape
    if upstream_shape.rank is not None and score_shape.rank is not None:
        if upstream_shape.rank > score_shape.rank:
            raise ValueError("target upstream gradient rank exceeds score rank")
        for idx, dim in enumerate(upstream_shape.as_list()):
            score_dim = score_shape[idx]
            if dim is not None and score_dim is not None and int(dim) != int(score_dim):
                raise ValueError(
                    "target upstream gradient leading dimensions must match score"
                )
        if upstream_shape.rank == score_shape.rank:
            return upstream
        return tf.reshape(
            upstream,
            tf.concat(
                [
                    tf.shape(upstream),
                    tf.ones([score_shape.rank - upstream_shape.rank], dtype=tf.int32),
                ],
                axis=0,
            ),
        )
    rank_delta = tf.rank(score_tensor) - tf.rank(upstream)
    with tf.control_dependencies(
        [
            tf.debugging.assert_greater_equal(
                rank_delta,
                0,
                message="target upstream gradient rank exceeds score rank",
            ),
            tf.debugging.assert_equal(
                tf.shape(upstream),
                tf.shape(score_tensor)[: tf.rank(upstream)],
                message="target upstream gradient leading dimensions must match score",
            ),
        ]
    ):
        return tf.reshape(
            upstream,
            tf.concat([tf.shape(upstream), tf.ones([rank_delta], dtype=tf.int32)], axis=0),
        )


def _build_sample_chain_runner(
    config: FullChainHMCConfig,
    kernel: Any,
    trace_fn: Callable[[Any, Any], Mapping[str, Any]],
    initial_state: Any,
) -> Callable[[], tuple[Any, Mapping[str, Any]]]:
    import tensorflow as tf
    import tensorflow_probability as tfp

    tfm = tfp.mcmc

    def run_chain() -> tuple[Any, Mapping[str, Any]]:
        return tfm.sample_chain(
            num_results=config.num_results,
            num_burnin_steps=config.num_burnin_steps,
            current_state=initial_state,
            kernel=kernel,
            trace_fn=trace_fn,
            seed=tf.constant(config.seed, dtype=tf.int32),
        )

    if config.use_xla:
        return tf.function(run_chain, jit_compile=True, reduce_retracing=True)
    if config.chain_execution_mode == "eager":
        return run_chain
    return tf.function(run_chain, reduce_retracing=True)


def _trace_fn_for_config(
    config: FullChainHMCConfig,
    *,
    adapter: Any | None = None,
) -> Callable[[Any, Any], Mapping[str, Any]]:
    if config.target_status_trace_policy != "none":
        if adapter is None or not callable(getattr(adapter, "target_status_telemetry", None)):
            raise TypeError(
                "target_status_trace_policy='per_chain_step' requires adapter "
                "target_status_telemetry"
            )
    if config.trace_policy != "standard":
        return _reduced_trace_fn
    if config.target_status_trace_policy == "per_chain_step":
        if config.tuning_policy.uses_dual_averaging:
            return _adaptive_standard_trace_fn_with_target_status(adapter)
        return _standard_trace_fn_with_target_status(adapter)
    if config.tuning_policy.uses_dual_averaging:
        return _adaptive_standard_trace_fn
    return _standard_trace_fn


def _standard_trace_fn_with_target_status(adapter: Any) -> Callable[[Any, Any], Mapping[str, Any]]:
    def trace_fn(state: Any, kernel_results: Any) -> Mapping[str, Any]:
        trace = dict(_standard_trace_fn(state, kernel_results))
        trace["target_status_telemetry"] = adapter.target_status_telemetry(state)
        return trace

    return trace_fn


def _standard_trace_fn(_state: Any, kernel_results: Any) -> Mapping[str, Any]:
    trace = {
        "is_accepted": kernel_results.is_accepted,
        "log_accept_ratio": kernel_results.log_accept_ratio,
        "target_log_prob": kernel_results.accepted_results.target_log_prob,
    }
    trace.update(_native_divergence_trace(kernel_results))
    return trace


def _adaptive_standard_trace_fn_with_target_status(adapter: Any) -> Callable[[Any, Any], Mapping[str, Any]]:
    def trace_fn(state: Any, kernel_results: Any) -> Mapping[str, Any]:
        trace = dict(_adaptive_standard_trace_fn(state, kernel_results))
        trace["target_status_telemetry"] = adapter.target_status_telemetry(state)
        return trace

    return trace_fn


def _adaptive_standard_trace_fn(_state: Any, kernel_results: Any) -> Mapping[str, Any]:
    inner_results = kernel_results.inner_results
    trace = {
        "is_accepted": inner_results.is_accepted,
        "log_accept_ratio": inner_results.log_accept_ratio,
        "target_log_prob": inner_results.accepted_results.target_log_prob,
        "step_size": kernel_results.new_step_size,
        "target_accept_prob": kernel_results.target_accept_prob,
        "num_adaptation_steps": kernel_results.num_adaptation_steps,
    }
    trace.update(_native_divergence_trace(inner_results))
    return trace


def _native_divergence_trace(kernel_results: Any) -> Mapping[str, Any]:
    """Expose only native boolean divergence fields from kernel results."""

    divergence = _extract_native_divergence_tensor(kernel_results)
    if divergence is None:
        return {}
    return {"divergence": divergence}


def _extract_native_divergence_tensor(kernel_results: Any) -> Any | None:
    """Return a native divergence tensor, never an energy/log-accept proxy."""

    import tensorflow as tf

    result_objects = (
        kernel_results,
        getattr(kernel_results, "proposed_results", None),
        getattr(kernel_results, "accepted_results", None),
    )
    field_names = (
        "is_divergent",
        "has_divergence",
        "divergence",
        "divergences",
    )
    for result_object in result_objects:
        if result_object is None:
            continue
        for field_name in field_names:
            if not hasattr(result_object, field_name):
                continue
            value = getattr(result_object, field_name)
            if value is None:
                continue
            try:
                tensor = tf.convert_to_tensor(value)
            except (TypeError, ValueError):
                continue
            if tensor.dtype == tf.bool:
                return tensor
    return None


def _reduced_trace_fn(_state: Any, _kernel_results: Any) -> Mapping[str, Any]:
    import tensorflow as tf

    return {"trace_collected": tf.constant(True)}


def _trace_unavailability(
    trace_policy: str,
    trace: Mapping[str, Any] | None = None,
    *,
    target_status_trace_policy: str = "none",
) -> Mapping[str, str]:
    target_status_trace_policy = str(target_status_trace_policy)
    if trace_policy == "standard":
        unavailable = {}
        if trace is not None and "divergence" not in trace:
            unavailable.update(
                {
                    "divergence": (
                        "native boolean divergence field not exposed by "
                        "TensorFlow Probability HMC kernel results"
                    ),
                }
            )
        if (
            target_status_trace_policy == "per_chain_step"
            and trace is not None
            and "target_status_telemetry" not in trace
        ):
            unavailable["target_status_telemetry"] = "target-status trace missing"
        return unavailable
    unavailable = {
        "is_accepted": "reduced trace policy",
        "log_accept_ratio": "reduced trace policy",
        "target_log_prob": "reduced trace policy",
        "divergence": "reduced trace policy",
    }
    if target_status_trace_policy != "none":
        unavailable["target_status_telemetry"] = "reduced trace policy"
    return unavailable


def _full_chain_hmc_diagnostics(
    samples: Any,
    trace: Mapping[str, Any],
    *,
    trace_policy: str,
) -> Mapping[str, Any]:
    import tensorflow as tf

    finite_by_sample = tf.reduce_all(tf.math.is_finite(samples), axis=-1)
    diagnostics: dict[str, Any] = {
        "finite_sample_count": tf.reduce_sum(tf.cast(finite_by_sample, tf.int32)),
        "nonfinite_sample_count": tf.reduce_sum(
            tf.cast(tf.logical_not(finite_by_sample), tf.int32)
        ),
        "sample_shape": tuple(int(dim) for dim in samples.shape),
        "trace_policy": trace_policy,
        "divergence_status": "unavailable",
        "divergence_count": None,
        "divergence_source": None,
        "nonclaims": (
            "finite tiny-chain diagnostics only",
            "no sampler convergence claim",
        ),
    }
    if "is_accepted" in trace:
        diagnostics["acceptance_rate"] = tf.reduce_mean(
            tf.cast(trace["is_accepted"], tf.float64)
        )
    else:
        diagnostics["acceptance_rate"] = None
    if "divergence" in trace:
        divergence = tf.convert_to_tensor(trace["divergence"], dtype=tf.bool)
        diagnostics["divergence_status"] = "available"
        diagnostics["divergence_count"] = tf.reduce_sum(
            tf.cast(divergence, tf.int32)
        )
        diagnostics["divergence_source"] = "native_boolean_tfp_kernel_result"
    if "target_log_prob" in trace:
        diagnostics["min_target_log_prob"] = tf.reduce_min(trace["target_log_prob"])
        diagnostics["max_target_log_prob"] = tf.reduce_max(trace["target_log_prob"])
    if "target_status_telemetry" in trace:
        diagnostics["target_status_telemetry"] = _target_status_telemetry_diagnostics(
            trace["target_status_telemetry"]
        )
    if "step_size" in trace:
        step_size = tf.convert_to_tensor(trace["step_size"], dtype=tf.float64)
        diagnostics["final_step_size"] = step_size[-1]
        diagnostics["final_step_size_finite"] = tf.reduce_all(tf.math.is_finite(step_size))
    if "target_accept_prob" in trace:
        target_accept = tf.convert_to_tensor(
            trace["target_accept_prob"],
            dtype=tf.float64,
        )
        diagnostics["target_accept_prob"] = tf.reshape(target_accept, [-1])[-1]
    if "num_adaptation_steps" in trace:
        adaptation_steps = tf.convert_to_tensor(
            trace["num_adaptation_steps"],
            dtype=tf.int32,
        )
        diagnostics["num_adaptation_steps"] = tf.reshape(adaptation_steps, [-1])[-1]
    return diagnostics


def _target_status_telemetry_diagnostics(telemetry: Mapping[str, Any]) -> Mapping[str, Any]:
    import tensorflow as tf

    if not isinstance(telemetry, Mapping):
        raise TypeError("target_status_telemetry trace must be a mapping")
    required = (
        "status_code",
        "valid_pre_regularized_score",
        "floor_count_value",
        "min_innovation_eigenvalue",
        "innovation_condition_estimate",
    )
    missing = tuple(key for key in required if key not in telemetry)
    if missing:
        raise ValueError(
            "target_status_telemetry missing required fields: " + ", ".join(missing)
        )
    status = tf.convert_to_tensor(telemetry["status_code"], dtype=tf.int32)
    valid = tf.convert_to_tensor(telemetry["valid_pre_regularized_score"], dtype=tf.bool)
    floors = tf.convert_to_tensor(telemetry["floor_count_value"], dtype=tf.int32)
    min_eigen = tf.convert_to_tensor(telemetry["min_innovation_eigenvalue"], dtype=tf.float64)
    condition = tf.convert_to_tensor(
        telemetry["innovation_condition_estimate"],
        dtype=tf.float64,
    )
    status_nonvalid = tf.logical_or(
        tf.not_equal(status, tf.zeros_like(status)),
        tf.logical_not(valid),
    )
    return {
        "trace_entry_count": tf.size(status),
        "status_nonvalid_count": tf.reduce_sum(tf.cast(status_nonvalid, tf.int32)),
        "all_status_valid": tf.reduce_all(tf.logical_not(status_nonvalid)),
        "floor_count_total": tf.reduce_sum(floors),
        "max_floor_count_value": tf.reduce_max(floors),
        "min_min_innovation_eigenvalue": tf.reduce_min(min_eigen),
        "max_innovation_condition_estimate": tf.reduce_max(condition),
        "telemetry_failure_veto": tf.logical_not(
            tf.reduce_all(tf.logical_not(status_nonvalid))
        ),
    }


def program_signature(payload: Mapping[str, Any] | Any) -> str:
    """Build a stable SHA-256 signature for JSON-like metadata."""

    normalized = _normalize_for_json(payload)
    blob = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _stack_like_chain(chain_state: Any, rows: list[Any]) -> Any:
    if hasattr(chain_state, "dtype") and chain_state.__class__.__module__.startswith("tensorflow"):
        import tensorflow as tf

        return tf.stack(rows, axis=0)
    return np.stack(rows, axis=0)


def _normalize_for_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _normalize_for_json(val) for key, val in value.items()}
    if isinstance(value, (tuple, list)):
        return [_normalize_for_json(item) for item in value]
    if isinstance(value, np.ndarray):
        return _normalize_for_json(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value
