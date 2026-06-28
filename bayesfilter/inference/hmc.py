"""Small generic HMC-runtime helpers with fail-closed authority checks."""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
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
        if (
            tuning_policy.uses_dual_averaging
            and self.use_xla
            and tuning_policy.label != "fixed_mass_dual_averaging"
        ):
            raise ValueError(
                "XLA dual-averaging HMC execution requires fixed_mass_dual_averaging "
                "in this phase"
            )
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


@dataclass(frozen=True)
class FixedSizeHMCChunkConfig:
    """Fixed-shape HMC chunk contract with runtime active sample count."""

    max_results: int
    num_burnin_steps: int
    step_size: float
    num_leapfrog_steps: int
    seed: tuple[int, int]
    use_xla: bool = False
    trace_policy: str = "reduced"
    target_status_trace_policy: str = "none"
    target_scope: str | None = None
    chain_execution_mode: str = "tf_function"

    def __post_init__(self) -> None:
        max_results = int(self.max_results)
        if max_results <= 0:
            raise ValueError("max_results must be positive")
        object.__setattr__(self, "max_results", max_results)
        burnin = int(self.num_burnin_steps)
        if burnin < 0:
            raise ValueError("num_burnin_steps must be nonnegative")
        object.__setattr__(self, "num_burnin_steps", burnin)
        leapfrog = int(self.num_leapfrog_steps)
        if leapfrog <= 0:
            raise ValueError("num_leapfrog_steps must be positive")
        object.__setattr__(self, "num_leapfrog_steps", leapfrog)
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
            raise ValueError("XLA fixed-size HMC chunk requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", chain_execution_mode)
        trace_policy = str(self.trace_policy)
        if trace_policy != "reduced":
            raise ValueError("fixed-size HMC chunk runner currently supports only reduced trace")
        object.__setattr__(self, "trace_policy", trace_policy)
        target_status_policy = str(self.target_status_trace_policy)
        if target_status_policy != "none":
            raise ValueError("fixed-size HMC chunk runner does not collect target-status traces")
        object.__setattr__(self, "target_status_trace_policy", target_status_policy)
        if self.target_scope is not None:
            object.__setattr__(self, "target_scope", str(self.target_scope))

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "max_results": self.max_results,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": self.seed,
            "use_xla": self.use_xla,
            "chain_execution_mode": self.chain_execution_mode,
            "trace_policy": self.trace_policy,
            "target_status_trace_policy": self.target_status_trace_policy,
            "target_scope": self.target_scope,
        }


@dataclass(frozen=True)
class FixedSizeHMCChunkRunResult:
    """Fixed-size HMC chunk result with valid-mask and final-state handoff."""

    samples: Any
    valid_mask: Any
    final_state: Any
    trace: Mapping[str, Any]
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class HMCSampleArchiveManifest:
    """Public metadata for a private retained HMC sample archive.

    The manifest records paths, hashes, shapes, dtypes, byte counts, and scalar
    diagnostics only.  The archive files themselves are private because they
    contain raw retained samples and state handoff tensors.
    """

    archive_dir: str
    manifest_path: str
    manifest_hash: str
    payload: Mapping[str, Any]

    def public_payload(self) -> Mapping[str, Any]:
        """Return the metadata-only payload suitable for public run artifacts."""

        return dict(self.payload)


class HMCStreamingSampleArchiveSink:
    """Incremental private sink for retained fixed-size HMC chunks.

    ``write_chunk`` serializes one chunk's sample, mask, and final-state tensors
    immediately and retains only metadata needed for the final public-safe
    manifest.  This is the bounded-retention contract callers should use when
    they need retained samples without accumulating all chunk tensors in Python.
    """

    def __init__(
        self,
        *,
        archive_dir: str | Path,
        config: FixedSizeHMCChunkConfig,
        archive_label: str,
        metadata: Mapping[str, Any] | None = None,
        overwrite: bool = False,
    ) -> None:
        label = str(archive_label).strip()
        if not label:
            raise ValueError("archive_label must be non-empty")
        root = Path(archive_dir)
        if root.exists() and not root.is_dir():
            raise ValueError("archive_dir exists and is not a directory")
        root.mkdir(parents=True, exist_ok=True)
        self.archive_dir = root
        self.config = config
        self.archive_label = label
        self.metadata = {} if metadata is None else _json_safe_metadata(dict(metadata))
        self.overwrite = bool(overwrite)
        self._chunk_payloads: list[dict[str, Any]] = []
        self._total_valid = 0
        self._total_nonfinite = 0
        self._finalized = False

    @property
    def chunk_count(self) -> int:
        return len(self._chunk_payloads)

    def write_chunk(
        self,
        chunk: FixedSizeHMCChunkRunResult,
        *,
        chunk_index: int | None = None,
    ) -> Mapping[str, Any]:
        """Flush one chunk to private tensor shards and return metadata only."""

        if self._finalized:
            raise RuntimeError("cannot write chunks after archive manifest finalization")
        index = self.chunk_count if chunk_index is None else int(chunk_index)
        if index != self.chunk_count:
            raise ValueError("chunk_index must match current sequential chunk_count")
        payload, valid_count, nonfinite_count = _write_hmc_archive_chunk(
            archive_dir=self.archive_dir,
            archive_label=self.archive_label,
            chunk=chunk,
            config=self.config,
            chunk_index=index,
            overwrite=self.overwrite,
        )
        self._chunk_payloads.append(payload)
        self._total_valid += valid_count
        self._total_nonfinite += nonfinite_count
        return dict(payload)

    def finalize(self) -> HMCSampleArchiveManifest:
        """Write and return the final public-safe manifest."""

        if self._finalized:
            raise RuntimeError("archive manifest already finalized")
        if not self._chunk_payloads:
            raise ValueError("cannot finalize an empty HMC sample archive")
        self._finalized = True
        return _finalize_hmc_sample_archive_manifest(
            archive_dir=self.archive_dir,
            archive_label=self.archive_label,
            config=self.config,
            chunk_payloads=tuple(self._chunk_payloads),
            total_valid=self._total_valid,
            total_nonfinite=self._total_nonfinite,
            metadata=self.metadata,
            overwrite=self.overwrite,
        )


@dataclass(frozen=True)
class InternalSegmentHMCRunnerConfig:
    """Single-call HMC runner with fixed internal progress segments.

    The runner executes ``segment_count * segment_length`` HMC transitions in
    one compiled function call.  In the initial ``summary_only`` output mode it
    returns only the final state plus fixed-shape scalar segment summaries.  It
    deliberately does not return sample tensors; retained-sample streaming is a
    separate contract so long-running clients do not accidentally reintroduce
    repeated compiled-call or returned-buffer memory growth.
    """

    segment_count: int
    segment_length: int
    num_burnin_steps: int
    step_size: float
    num_leapfrog_steps: int
    seed: tuple[int, int]
    use_xla: bool = False
    output_mode: str = "summary_only"
    target_scope: str | None = None
    chain_execution_mode: str = "tf_function"

    def __post_init__(self) -> None:
        for name in ("segment_count", "segment_length", "num_leapfrog_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        burnin = int(self.num_burnin_steps)
        if burnin < 0:
            raise ValueError("num_burnin_steps must be nonnegative")
        object.__setattr__(self, "num_burnin_steps", burnin)
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
            raise ValueError("XLA internal-segment HMC requires chain_execution_mode='tf_function'")
        object.__setattr__(self, "chain_execution_mode", chain_execution_mode)
        output_mode = str(self.output_mode)
        if output_mode != "summary_only":
            raise ValueError("internal-segment HMC currently supports only output_mode='summary_only'")
        object.__setattr__(self, "output_mode", output_mode)
        if self.target_scope is not None:
            object.__setattr__(self, "target_scope", str(self.target_scope))

    @property
    def total_transitions(self) -> int:
        return int(self.segment_count * self.segment_length)

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "segment_count": self.segment_count,
            "segment_length": self.segment_length,
            "total_transitions": self.total_transitions,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": self.seed,
            "use_xla": self.use_xla,
            "chain_execution_mode": self.chain_execution_mode,
            "output_mode": self.output_mode,
            "target_scope": self.target_scope,
        }


@dataclass(frozen=True)
class RetainedSampleHMCArchiveConfig:
    """One-call retained HMC contract with private sample archive output.

    The runner executes all burn-in and retained HMC transitions in a single
    TensorFlow call and returns no sample tensor to the caller.  Retained
    samples are persisted privately after the call in exactly one physical
    retained-sample shard; any manifest or final-state files are sidecars, not
    additional sample shards.
    """

    num_results: int
    num_burnin_steps: int
    step_size: float
    num_leapfrog_steps: int
    seed: tuple[int, int]
    use_xla: bool = False
    target_scope: str | None = None
    chain_execution_mode: str = "tf_function"
    sampler_diagnostics_policy: str = "public_safe_summary"

    def __post_init__(self) -> None:
        results = int(self.num_results)
        if results <= 0:
            raise ValueError("num_results must be positive")
        object.__setattr__(self, "num_results", results)
        burnin = int(self.num_burnin_steps)
        if burnin < 0:
            raise ValueError("num_burnin_steps must be nonnegative")
        object.__setattr__(self, "num_burnin_steps", burnin)
        leapfrog = int(self.num_leapfrog_steps)
        if leapfrog <= 0:
            raise ValueError("num_leapfrog_steps must be positive")
        object.__setattr__(self, "num_leapfrog_steps", leapfrog)
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
            raise ValueError(
                "XLA retained-sample HMC archive requires chain_execution_mode='tf_function'"
            )
        object.__setattr__(self, "chain_execution_mode", chain_execution_mode)
        if self.target_scope is not None:
            object.__setattr__(self, "target_scope", str(self.target_scope))
        sampler_diagnostics_policy = str(self.sampler_diagnostics_policy)
        if sampler_diagnostics_policy != "public_safe_summary":
            raise ValueError(
                "retained-sample HMC archive currently supports only "
                "sampler_diagnostics_policy='public_safe_summary'"
            )
        object.__setattr__(
            self,
            "sampler_diagnostics_policy",
            sampler_diagnostics_policy,
        )

    def signature_payload(self) -> Mapping[str, Any]:
        return {
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": self.seed,
            "use_xla": self.use_xla,
            "chain_execution_mode": self.chain_execution_mode,
            "target_scope": self.target_scope,
            "sampler_diagnostics_policy": self.sampler_diagnostics_policy,
        }


@dataclass(frozen=True)
class InternalSegmentHMCRunResult:
    """Summary-only internal-segment HMC result.

    ``segment_indices`` records the transition index at each segment boundary;
    ``segment_target_log_prob`` records the per-chain target log probability at
    those boundaries.  No raw samples are returned in ``summary_only`` mode.
    """

    final_state: Any
    final_target_log_prob: Any
    final_index: Any
    segment_index: Any
    segment_indices: Any
    segment_target_log_prob: Any
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]


@dataclass(frozen=True)
class RetainedSampleHMCArchiveRunResult:
    """Public-safe result for one-call retained HMC archive execution.

    Raw retained samples are intentionally absent from this contract.  The
    caller receives only the final state for explicit handoff, finite/count
    diagnostics, public-safe metadata, and an aggregate archive summary.
    """

    final_state: Any
    final_target_log_prob: Any
    final_index: Any
    diagnostics: Mapping[str, Any]
    metadata: Mapping[str, Any]
    archive_summary: Mapping[str, Any]


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
        runner_build_start = time.perf_counter()
        self._runner = self._build_runner()
        self._runner_build_s = time.perf_counter() - runner_build_start
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

        trace_capture_start = time.perf_counter()
        trace_for_diagnostics = trace if self.config.trace_policy == "standard" else {}
        diagnostics = _full_chain_hmc_diagnostics(
            samples,
            trace_for_diagnostics,
            trace_policy=self.config.trace_policy,
        )
        trace_capture_s = time.perf_counter() - trace_capture_start
        metadata = self._metadata(
            sample_chain_call_s=sample_chain_call_s,
            trace_capture_s=trace_capture_s,
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
        trace_capture_s: float,
        trace: Mapping[str, Any] | None,
    ) -> Mapping[str, Any]:
        config = self.config
        capability = self.capability
        if config.chain_execution_mode == "eager":
            timing_scope = "reusable_eager_runner_execute_only"
        elif config.use_xla:
            timing_scope = (
                "reusable_tf_function_xla_first_call_compile_plus_execute_then_warm_execute"
            )
        else:
            timing_scope = (
                "reusable_tf_function_first_call_trace_compile_plus_execute_then_warm_execute"
            )
        return {
            "runtime": "tfp.mcmc.sample_chain",
            "reusable_runner": True,
            "jit_compile": config.use_xla,
            "use_xla": config.use_xla,
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
            "sample_chain_timing_scope": timing_scope,
            "runner_build_s": self._runner_build_s,
            "first_call_s": self._first_call_s,
            "first_sample_chain_compile_execute_s": self._first_call_s,
            "warm_call_s": self._warm_call_s,
            "warm_sample_chain_execute_s": self._warm_call_s,
            "trace_capture_s": trace_capture_s,
            "trace_capture_timing_scope": (
                "post_sample_chain_public_safe_trace_diagnostics_capture"
            ),
            "warm_sample_shape": None,
            "warm_trace_keys": tuple(sorted(trace.keys())) if trace is not None else tuple(),
            "timing_buckets": {
                "runner_build_s": "explanatory_only_runner_callable_construction",
                "first_call_s": (
                    "explanatory_only_first_sample_chain_compile_plus_execute_when_tf_function"
                ),
                "warm_call_s": "explanatory_only_subsequent_sample_chain_execute",
                "trace_capture_s": (
                    "explanatory_only_post_sample_chain_trace_diagnostics_capture"
                ),
            },
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


class FixedSizeHMCChunkRunner:
    """Reusable fixed-shape HMC chunk runner using ``tf.while_loop``.

    The compiled contract fixes ``max_results`` and the static state shape, but
    each call supplies a runtime scalar ``active_results``.  The graph executes
    exactly the active number of sample transitions after fixed burn-in,
    writes valid draws into a fixed-size tensor, and returns a valid mask so
    callers can checkpoint chunks without recompiling for each active count.
    """

    def __init__(
        self,
        adapter: Any,
        initial_state_template: Any,
        config: FixedSizeHMCChunkConfig,
    ) -> None:
        self.adapter = adapter
        self.config = config
        self.capability = _validate_full_chain_hmc_authority(adapter, config)

        import tensorflow as tf

        template = tf.cast(tf.convert_to_tensor(initial_state_template), tf.float64)
        if template.shape.rank is None:
            raise ValueError("fixed-size HMC chunk runner requires static state rank")
        if any(dim is None for dim in template.shape):
            raise ValueError(
                "fixed-size HMC chunk runner requires fully static state shape"
            )
        self._state_shape = tuple(int(dim) for dim in template.shape)
        self._state_dtype = template.dtype
        self._initial_state_template = template
        self._target_log_prob = _make_tfp_target_log_prob_fn(
            adapter,
            dtype=self._state_dtype,
        )
        runner_build_start = time.perf_counter()
        self._runner = self._build_runner()
        self._runner_build_s = time.perf_counter() - runner_build_start
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
        active_results: int | Any,
        current_state: Any | None = None,
        seed: tuple[int, int] | Any | None = None,
        step_size: float | Any | None = None,
    ) -> FixedSizeHMCChunkRunResult:
        """Run one fixed-size chunk with runtime active sample count."""

        import tensorflow as tf

        state = self._initial_state_template if current_state is None else current_state
        state_tensor = tf.convert_to_tensor(state, dtype=self._state_dtype)
        if tuple(state_tensor.shape.as_list()) != self._state_shape:
            raise ValueError("current_state shape must match fixed-size runner template")
        seed_value = self.config.seed if seed is None else seed
        seed_tensor = tf.convert_to_tensor(seed_value, dtype=tf.int32)
        if tuple(seed_tensor.shape.as_list()) != (2,):
            raise ValueError("seed must have static shape (2,)")
        step_value = self.config.step_size if step_size is None else step_size
        step_tensor = tf.convert_to_tensor(step_value, dtype=self._state_dtype)
        if step_tensor.shape.rank != 0:
            raise ValueError("step_size must be a scalar")
        active_tensor = tf.convert_to_tensor(active_results, dtype=tf.int32)
        if active_tensor.shape.rank != 0:
            raise ValueError("active_results must be a scalar")
        if hasattr(active_tensor, "numpy"):
            active_value = int(active_tensor.numpy())
            if active_value < 0 or active_value > self.config.max_results:
                raise ValueError("active_results must satisfy 0 <= active_results <= max_results")

        chunk_start = time.perf_counter()
        samples, valid_mask, final_state, trace = self._runner(
            state_tensor,
            seed_tensor,
            step_tensor,
            active_tensor,
        )
        chunk_call_s = time.perf_counter() - chunk_start
        self._call_count += 1
        if self._call_count == 1:
            self._first_call_s = chunk_call_s
            self._warm_call_s = None
        else:
            self._warm_call_s = chunk_call_s

        trace_capture_start = time.perf_counter()
        diagnostics = _fixed_size_hmc_chunk_diagnostics(
            samples,
            valid_mask,
            trace,
            trace_policy=self.config.trace_policy,
        )
        trace_capture_s = time.perf_counter() - trace_capture_start
        metadata = self._metadata(
            active_results=int(active_tensor.numpy()) if hasattr(active_tensor, "numpy") else None,
            chunk_call_s=chunk_call_s,
            trace_capture_s=trace_capture_s,
            trace=trace,
        )
        return FixedSizeHMCChunkRunResult(
            samples=samples,
            valid_mask=valid_mask,
            final_state=final_state,
            trace=trace,
            diagnostics=diagnostics,
            metadata=metadata,
        )

    __call__ = run

    def _build_runner(self) -> Callable[[Any, Any, Any, Any], tuple[Any, Any, Any, Mapping[str, Any]]]:
        import tensorflow as tf
        import tensorflow_probability as tfp

        tfm = tfp.mcmc
        config = self.config
        target_log_prob = self._target_log_prob
        state_shape = self._state_shape

        def run_chunk(
            current_state: Any,
            seed: Any,
            step_size: Any,
            active_results: Any,
        ) -> tuple[Any, Any, Any, Mapping[str, Any]]:
            active_results = tf.cast(active_results, tf.int32)
            with tf.control_dependencies(
                [
                    tf.debugging.assert_greater_equal(
                        active_results,
                        tf.constant(0, dtype=tf.int32),
                        message="active_results must be nonnegative",
                    ),
                    tf.debugging.assert_less_equal(
                        active_results,
                        tf.constant(config.max_results, dtype=tf.int32),
                        message="active_results must not exceed max_results",
                    ),
                ]
            ):
                active_results = tf.identity(active_results)

            kernel = tfm.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob,
                step_size=step_size,
                num_leapfrog_steps=config.num_leapfrog_steps,
            )
            kernel_results = kernel.bootstrap_results(current_state)

            def burnin_condition(index: Any, _state: Any, _results: Any) -> Any:
                return index < tf.constant(config.num_burnin_steps, dtype=tf.int32)

            def burnin_body(index: Any, state: Any, results: Any) -> tuple[Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(seed, index)
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                return index + 1, next_state, next_results

            _burnin_index, burnin_state, burnin_results = tf.while_loop(
                burnin_condition,
                burnin_body,
                (tf.constant(0, dtype=tf.int32), current_state, kernel_results),
                parallel_iterations=1,
            )

            samples = tf.zeros((config.max_results,) + state_shape, dtype=current_state.dtype)

            def sample_condition(
                index: Any,
                _state: Any,
                _results: Any,
                _samples: Any,
            ) -> Any:
                return index < active_results

            def sample_body(
                index: Any,
                state: Any,
                results: Any,
                sample_buffer: Any,
            ) -> tuple[Any, Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(
                    seed,
                    tf.constant(config.num_burnin_steps, dtype=tf.int32) + index,
                )
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                updated = tf.tensor_scatter_nd_update(
                    sample_buffer,
                    tf.reshape(index, [1, 1]),
                    tf.expand_dims(next_state, axis=0),
                )
                return index + 1, next_state, next_results, updated

            _sample_index, final_state, _final_results, samples = tf.while_loop(
                sample_condition,
                sample_body,
                (tf.constant(0, dtype=tf.int32), burnin_state, burnin_results, samples),
                parallel_iterations=1,
            )
            valid_mask = tf.range(config.max_results, dtype=tf.int32) < active_results
            trace = {"trace_collected": tf.constant(True)}
            return samples, valid_mask, final_state, trace

        if config.chain_execution_mode == "eager":
            return run_chunk
        input_signature = [
            tf.TensorSpec(shape=self._state_shape, dtype=self._state_dtype),
            tf.TensorSpec(shape=(2,), dtype=tf.int32),
            tf.TensorSpec(shape=(), dtype=self._state_dtype),
            tf.TensorSpec(shape=(), dtype=tf.int32),
        ]
        if config.use_xla:
            return tf.function(
                run_chunk,
                input_signature=input_signature,
                jit_compile=True,
                reduce_retracing=True,
            )
        return tf.function(
            run_chunk,
            input_signature=input_signature,
            reduce_retracing=True,
        )

    def _metadata(
        self,
        *,
        active_results: int | None,
        chunk_call_s: float,
        trace_capture_s: float,
        trace: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        config = self.config
        capability = self.capability
        trace_count_fn = getattr(self._runner, "experimental_get_tracing_count", None)
        compile_trace_count = None if trace_count_fn is None else int(trace_count_fn())
        if config.chain_execution_mode == "eager":
            timing_scope = "fixed_size_hmc_chunk_eager_execute_only"
        elif config.use_xla:
            timing_scope = (
                "fixed_size_hmc_chunk_tf_function_xla_first_call_compile_plus_execute_then_warm_execute"
            )
        else:
            timing_scope = (
                "fixed_size_hmc_chunk_tf_function_first_call_trace_compile_plus_execute_then_warm_execute"
            )
        return {
            "runtime": "tfp.mcmc.HamiltonianMonteCarlo.one_step_tf_while_loop",
            "fixed_size_chunk_runner": True,
            "uses_sample_chain": False,
            "jit_compile": config.use_xla,
            "use_xla": config.use_xla,
            "chain_execution_mode": config.chain_execution_mode,
            "trace_policy": config.trace_policy,
            "target_status_trace_policy": config.target_status_trace_policy,
            "max_results": config.max_results,
            "active_results": active_results,
            "num_burnin_steps": config.num_burnin_steps,
            "step_size": config.step_size,
            "num_leapfrog_steps": config.num_leapfrog_steps,
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
                    "dynamic_inputs": (
                        "current_state",
                        "seed",
                        "step_size",
                        "active_results",
                    ),
                }
            ),
            "initial_state_shape": self._state_shape,
            "initial_state_dtype": self._state_dtype.name,
            "dynamic_inputs": (
                "current_state",
                "seed",
                "step_size",
                "active_results",
            ),
            "seed_source": "runtime_tensor_argument",
            "current_state_source": "runtime_tensor_argument",
            "step_size_source": "runtime_tensor_argument",
            "active_results_source": "runtime_tensor_argument",
            "compile_trace_count": compile_trace_count,
            "chunk_call_s": chunk_call_s,
            "chunk_invocation_count": self._call_count,
            "chunk_timing_scope": timing_scope,
            "runner_build_s": self._runner_build_s,
            "first_call_s": self._first_call_s,
            "first_chunk_compile_execute_s": self._first_call_s,
            "warm_call_s": self._warm_call_s,
            "warm_chunk_execute_s": self._warm_call_s,
            "trace_capture_s": trace_capture_s,
            "trace_capture_timing_scope": (
                "post_fixed_size_hmc_chunk_public_safe_trace_diagnostics_capture"
            ),
            "warm_sample_shape": None,
            "warm_trace_keys": tuple(sorted(trace.keys())),
            "timing_buckets": {
                "runner_build_s": "explanatory_only_runner_callable_construction",
                "first_call_s": (
                    "explanatory_only_first_fixed_chunk_compile_plus_execute_when_tf_function"
                ),
                "warm_call_s": "explanatory_only_subsequent_fixed_chunk_execute",
                "trace_capture_s": (
                    "explanatory_only_post_fixed_chunk_trace_diagnostics_capture"
                ),
            },
            "nonclaims": (
                "fixed-size HMC chunk engineering runner only",
                "no sampler convergence claim",
                "no posterior validity claim",
                "no GPU readiness claim",
                "no performance superiority claim",
            ),
        }


def build_fixed_size_hmc_chunk_runner(
    adapter: Any,
    initial_state_template: Any,
    config: FixedSizeHMCChunkConfig,
) -> FixedSizeHMCChunkRunner:
    """Build a fixed-size BayesFilter HMC chunk runner for a static state shape."""

    return FixedSizeHMCChunkRunner(adapter, initial_state_template, config)


def write_hmc_sample_archive(
    *,
    archive_dir: str | Path,
    chunks: Sequence[FixedSizeHMCChunkRunResult],
    config: FixedSizeHMCChunkConfig,
    archive_label: str,
    metadata: Mapping[str, Any] | None = None,
    overwrite: bool = False,
) -> HMCSampleArchiveManifest:
    """Write private fixed-size HMC chunk tensors and a public-safe manifest.

    This convenience wrapper writes a finite sequence of chunks through
    ``HMCStreamingSampleArchiveSink``.  Long-running callers should instantiate
    the sink directly and call ``write_chunk`` inside their HMC loop so raw
    sample tensors can be released before the next chunk.
    """

    if not isinstance(chunks, Sequence) or isinstance(chunks, (str, bytes)):
        raise TypeError("chunks must be a non-empty sequence of chunk results")
    if not chunks:
        raise ValueError("chunks must be non-empty")
    sink = HMCStreamingSampleArchiveSink(
        archive_dir=archive_dir,
        config=config,
        archive_label=archive_label,
        metadata=metadata,
        overwrite=overwrite,
    )
    for index, chunk in enumerate(chunks):
        sink.write_chunk(chunk, chunk_index=index)
    return sink.finalize()


def _write_hmc_archive_chunk(
    *,
    archive_dir: Path,
    archive_label: str,
    chunk: FixedSizeHMCChunkRunResult,
    config: FixedSizeHMCChunkConfig,
    chunk_index: int,
    overwrite: bool,
) -> tuple[dict[str, Any], int, int]:
    import tensorflow as tf

    if not isinstance(chunk, FixedSizeHMCChunkRunResult):
        raise TypeError("chunk must be a FixedSizeHMCChunkRunResult")
    sample_tensor = tf.convert_to_tensor(chunk.samples)
    mask_tensor = tf.convert_to_tensor(chunk.valid_mask, dtype=tf.bool)
    state_tensor = tf.convert_to_tensor(chunk.final_state)
    if sample_tensor.shape.rank is None or mask_tensor.shape.rank != 1:
        raise ValueError("sample and mask tensors must have static rank")
    max_results = int(sample_tensor.shape[0])
    if max_results != int(config.max_results):
        raise ValueError("sample leading dimension must match config.max_results")
    if int(mask_tensor.shape[0]) != int(config.max_results):
        raise ValueError("valid_mask length must match config.max_results")
    if tuple(state_tensor.shape.as_list()) != tuple(sample_tensor.shape.as_list()[1:]):
        raise ValueError("final_state shape must match sample trailing shape")

    valid_count_tensor = tf.reduce_sum(tf.cast(mask_tensor, tf.int32))
    trailing_axes = tf.range(1, tf.rank(sample_tensor), dtype=tf.int32)
    finite_by_row = tf.reduce_all(
        tf.math.is_finite(sample_tensor),
        axis=trailing_axes,
    )
    nonfinite_valid_tensor = tf.reduce_sum(
        tf.cast(
            tf.logical_and(mask_tensor, tf.logical_not(finite_by_row)),
            tf.int32,
        )
    )
    valid_count = int(valid_count_tensor.numpy())
    nonfinite_valid = int(nonfinite_valid_tensor.numpy())

    sample_path = archive_dir / f"{archive_label}_chunk_{chunk_index:04d}_samples.tftensor"
    mask_path = archive_dir / f"{archive_label}_chunk_{chunk_index:04d}_valid_mask.tftensor"
    state_path = archive_dir / f"{archive_label}_chunk_{chunk_index:04d}_final_state.tftensor"
    for path in (sample_path, mask_path, state_path):
        if path.exists() and not overwrite:
            raise FileExistsError(f"archive shard already exists: {path}")
    sample_hash, sample_bytes = _write_serialized_tensor(sample_path, sample_tensor)
    mask_hash, mask_bytes = _write_serialized_tensor(mask_path, mask_tensor)
    state_hash, state_bytes = _write_serialized_tensor(state_path, state_tensor)

    diagnostics = chunk.diagnostics
    metadata_payload = chunk.metadata
    payload = {
        "chunk_index": int(chunk_index),
        "sample_path": str(sample_path),
        "sample_sha256": sample_hash,
        "sample_bytes": sample_bytes,
        "sample_shape": tuple(int(dim) for dim in sample_tensor.shape),
        "sample_dtype": sample_tensor.dtype.name,
        "valid_mask_path": str(mask_path),
        "valid_mask_sha256": mask_hash,
        "valid_mask_bytes": mask_bytes,
        "valid_mask_shape": tuple(int(dim) for dim in mask_tensor.shape),
        "valid_mask_dtype": mask_tensor.dtype.name,
        "final_state_path": str(state_path),
        "final_state_sha256": state_hash,
        "final_state_bytes": state_bytes,
        "final_state_shape": tuple(int(dim) for dim in state_tensor.shape),
        "final_state_dtype": state_tensor.dtype.name,
        "valid_sample_count": valid_count,
        "nonfinite_valid_sample_count": nonfinite_valid,
        "compile_trace_count": metadata_payload.get("compile_trace_count"),
        "chunk_invocation_count": metadata_payload.get("chunk_invocation_count"),
        "chunk_call_s": metadata_payload.get("chunk_call_s"),
        "diagnostic_roles": {
            "valid_sample_count": "archive_accounting",
            "nonfinite_valid_sample_count": "hard_veto",
            "compile_trace_count": "smoke_scale_retrace_diagnostic",
            "chunk_call_s": "explanatory_only_runtime",
        },
        "trace_policy": metadata_payload.get("trace_policy"),
        "native_divergence_status": _tensor_or_plain_to_metadata(
            diagnostics.get("native_divergence_status")
        ),
    }
    return payload, valid_count, nonfinite_valid


def _finalize_hmc_sample_archive_manifest(
    *,
    archive_dir: Path,
    archive_label: str,
    config: FixedSizeHMCChunkConfig,
    chunk_payloads: Sequence[Mapping[str, Any]],
    total_valid: int,
    total_nonfinite: int,
    metadata: Mapping[str, Any],
    overwrite: bool,
) -> HMCSampleArchiveManifest:
    manifest_payload = {
        "artifact_type": "bayesfilter_hmc_sample_archive_manifest",
        "schema_version": 1,
        "archive_label": str(archive_label),
        "archive_dir": str(archive_dir),
        "chunk_count": len(chunk_payloads),
        "total_valid_sample_count": int(total_valid),
        "total_nonfinite_valid_sample_count": int(total_nonfinite),
        "streaming_contract": {
            "incremental_write_before_next_chunk_supported": True,
            "sink_retains_chunk_tensors_after_write": False,
            "finalize_writes_manifest_only": True,
        },
        "config_public_contract": {
            "max_results": int(config.max_results),
            "num_burnin_steps": int(config.num_burnin_steps),
            "use_xla": bool(config.use_xla),
            "chain_execution_mode": str(config.chain_execution_mode),
            "trace_policy": str(config.trace_policy),
            "target_status_trace_policy": str(config.target_status_trace_policy),
            "target_scope": config.target_scope,
        },
        "chunks": tuple(dict(item) for item in chunk_payloads),
        "metadata": _json_safe_metadata(dict(metadata)),
        "privacy_contract": {
            "archive_contains_private_raw_tensors": True,
            "public_manifest_contains_raw_values": False,
            "public_manifest_fields": (
                "paths",
                "hashes",
                "shapes",
                "dtypes",
                "byte_counts",
                "counts",
                "public_diagnostics",
            ),
            "forbidden_public_payloads": (
                "raw_sample_values",
                "raw_state_values",
                "mass_matrices",
                "selected_kernel_payloads",
                "step_sizes",
                "leapfrog_counts",
            ),
        },
        "nonclaims": (
            "retained HMC sample archive mechanics only",
            "no posterior convergence claim",
            "no serious sampler health claim",
            "no long-run retained-memory claim",
            "no scientific validity claim",
        ),
    }
    _assert_hmc_archive_manifest_public_safe(manifest_payload)
    manifest_path = archive_dir / f"{archive_label}_manifest.json"
    if manifest_path.exists() and not overwrite:
        raise FileExistsError(f"archive manifest already exists: {manifest_path}")
    core_text = json.dumps(
        _json_safe_metadata(manifest_payload),
        indent=2,
        sort_keys=True,
    ) + "\n"
    payload_with_hash = dict(manifest_payload)
    payload_with_hash["manifest_path"] = str(manifest_path)
    payload_with_hash["manifest_core_sha256"] = hashlib.sha256(
        core_text.encode("utf-8")
    ).hexdigest()
    manifest_text = json.dumps(
        _json_safe_metadata(payload_with_hash),
        indent=2,
        sort_keys=True,
    ) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest_file_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
    return HMCSampleArchiveManifest(
        archive_dir=str(archive_dir),
        manifest_path=str(manifest_path),
        manifest_hash=manifest_file_hash,
        payload=_json_safe_metadata(payload_with_hash),
    )


class InternalSegmentHMCRunner:
    """Reusable single-call HMC runner with fixed internal summaries.

    This runner is for long HMC calls where repeated Python calls to compiled
    chunk bodies are undesirable.  It runs burn-in and sample transitions inside
    one ``tf.while_loop`` and records compact per-segment target summaries.  The
    initial contract is summary-only: it does not allocate or return sample
    buffers, so clients must not use it as a retained posterior sample runner.
    """

    def __init__(
        self,
        adapter: Any,
        initial_state_template: Any,
        config: InternalSegmentHMCRunnerConfig,
    ) -> None:
        self.adapter = adapter
        self.config = config
        self.capability = _validate_full_chain_hmc_authority(adapter, config)

        import tensorflow as tf

        template = tf.cast(tf.convert_to_tensor(initial_state_template), tf.float64)
        if template.shape.rank is None:
            raise ValueError("internal-segment HMC runner requires static state rank")
        if any(dim is None for dim in template.shape):
            raise ValueError("internal-segment HMC runner requires fully static state shape")
        self._state_shape = tuple(int(dim) for dim in template.shape)
        self._state_dtype = template.dtype
        self._initial_state_template = template
        self._target_log_prob = _make_tfp_target_log_prob_fn(
            adapter,
            dtype=self._state_dtype,
        )
        runner_build_start = time.perf_counter()
        self._runner = self._build_runner()
        self._runner_build_s = time.perf_counter() - runner_build_start
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
    ) -> InternalSegmentHMCRunResult:
        """Run one internally segmented HMC call."""

        import tensorflow as tf

        state = self._initial_state_template if current_state is None else current_state
        state_tensor = tf.convert_to_tensor(state, dtype=self._state_dtype)
        if tuple(state_tensor.shape.as_list()) != self._state_shape:
            raise ValueError("current_state shape must match internal-segment runner template")
        seed_value = self.config.seed if seed is None else seed
        seed_tensor = tf.convert_to_tensor(seed_value, dtype=tf.int32)
        if tuple(seed_tensor.shape.as_list()) != (2,):
            raise ValueError("seed must have static shape (2,)")
        step_value = self.config.step_size if step_size is None else step_size
        step_tensor = tf.convert_to_tensor(step_value, dtype=self._state_dtype)
        if step_tensor.shape.rank != 0:
            raise ValueError("step_size must be a scalar")

        call_start = time.perf_counter()
        (
            final_state,
            final_target_log_prob,
            final_index,
            segment_index,
            segment_indices,
            segment_target_log_prob,
        ) = self._runner(state_tensor, seed_tensor, step_tensor)
        call_s = time.perf_counter() - call_start
        self._call_count += 1
        if self._call_count == 1:
            self._first_call_s = call_s
            self._warm_call_s = None
        else:
            self._warm_call_s = call_s

        diagnostics = _internal_segment_hmc_diagnostics(
            final_state=final_state,
            final_target_log_prob=final_target_log_prob,
            final_index=final_index,
            segment_index=segment_index,
            segment_indices=segment_indices,
            segment_target_log_prob=segment_target_log_prob,
            config=self.config,
        )
        metadata = self._metadata(call_s=call_s)
        return InternalSegmentHMCRunResult(
            final_state=final_state,
            final_target_log_prob=final_target_log_prob,
            final_index=final_index,
            segment_index=segment_index,
            segment_indices=segment_indices,
            segment_target_log_prob=segment_target_log_prob,
            diagnostics=diagnostics,
            metadata=metadata,
        )

    __call__ = run

    def _build_runner(self) -> Callable[[Any, Any, Any], tuple[Any, Any, Any, Any, Any, Any]]:
        import tensorflow as tf
        import tensorflow_probability as tfp

        tfm = tfp.mcmc
        config = self.config
        target_log_prob = self._target_log_prob

        def run_segments(current_state: Any, seed: Any, step_size: Any) -> tuple[Any, Any, Any, Any, Any, Any]:
            kernel = tfm.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob,
                step_size=step_size,
                num_leapfrog_steps=config.num_leapfrog_steps,
            )
            kernel_results = kernel.bootstrap_results(current_state)

            def burnin_condition(index: Any, _state: Any, _results: Any) -> Any:
                return index < tf.constant(config.num_burnin_steps, dtype=tf.int32)

            def burnin_body(index: Any, state: Any, results: Any) -> tuple[Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(seed, index)
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                return index + 1, next_state, next_results

            _burnin_index, burnin_state, burnin_results = tf.while_loop(
                burnin_condition,
                burnin_body,
                (tf.constant(0, dtype=tf.int32), current_state, kernel_results),
                parallel_iterations=1,
            )

            segment_indices = tf.zeros((config.segment_count,), dtype=tf.int32)
            segment_target_log_prob = tf.zeros(
                (config.segment_count,) + self._state_shape[:-1],
                dtype=current_state.dtype,
            )
            total = tf.constant(config.total_transitions, dtype=tf.int32)
            segment_length = tf.constant(config.segment_length, dtype=tf.int32)

            def sample_condition(
                index: Any,
                _segment_index: Any,
                _state: Any,
                _results: Any,
                _segment_indices: Any,
                _segment_target_log_prob: Any,
            ) -> Any:
                return index < total

            def sample_body(
                index: Any,
                segment_index: Any,
                state: Any,
                results: Any,
                indices: Any,
                target_log_probs: Any,
            ) -> tuple[Any, Any, Any, Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(
                    seed,
                    tf.constant(config.num_burnin_steps, dtype=tf.int32) + index,
                )
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                next_index = index + 1
                at_segment_end = tf.equal(tf.math.floormod(next_index, segment_length), 0)
                in_bounds = segment_index < tf.constant(config.segment_count, dtype=tf.int32)
                should_record = tf.logical_and(at_segment_end, in_bounds)
                final_target_log_prob = tf.convert_to_tensor(
                    next_results.accepted_results.target_log_prob
                )
                updated_indices = tf.cond(
                    should_record,
                    lambda: tf.tensor_scatter_nd_update(
                        indices,
                        tf.reshape(segment_index, [1, 1]),
                        tf.reshape(next_index, [1]),
                    ),
                    lambda: indices,
                )
                updated_target_log_probs = tf.cond(
                    should_record,
                    lambda: tf.tensor_scatter_nd_update(
                        target_log_probs,
                        tf.reshape(segment_index, [1, 1]),
                        tf.expand_dims(final_target_log_prob, axis=0),
                    ),
                    lambda: target_log_probs,
                )
                updated_segment_index = tf.where(
                    should_record,
                    segment_index + 1,
                    segment_index,
                )
                return (
                    next_index,
                    updated_segment_index,
                    next_state,
                    next_results,
                    updated_indices,
                    updated_target_log_probs,
                )

            (
                final_index,
                final_segment_index,
                final_state,
                final_results,
                final_segment_indices,
                final_segment_target_log_prob,
            ) = tf.while_loop(
                sample_condition,
                sample_body,
                (
                    tf.constant(0, dtype=tf.int32),
                    tf.constant(0, dtype=tf.int32),
                    burnin_state,
                    burnin_results,
                    segment_indices,
                    segment_target_log_prob,
                ),
                parallel_iterations=1,
            )
            final_target_log_prob = tf.convert_to_tensor(
                final_results.accepted_results.target_log_prob
            )
            return (
                final_state,
                final_target_log_prob,
                final_index,
                final_segment_index,
                final_segment_indices,
                final_segment_target_log_prob,
            )

        if config.chain_execution_mode == "eager":
            return run_segments
        input_signature = [
            tf.TensorSpec(shape=self._state_shape, dtype=self._state_dtype),
            tf.TensorSpec(shape=(2,), dtype=tf.int32),
            tf.TensorSpec(shape=(), dtype=self._state_dtype),
        ]
        if config.use_xla:
            return tf.function(
                run_segments,
                input_signature=input_signature,
                jit_compile=True,
                reduce_retracing=True,
            )
        return tf.function(
            run_segments,
            input_signature=input_signature,
            reduce_retracing=True,
        )

    def _metadata(self, *, call_s: float) -> Mapping[str, Any]:
        config = self.config
        capability = self.capability
        trace_count_fn = getattr(self._runner, "experimental_get_tracing_count", None)
        compile_trace_count = None if trace_count_fn is None else int(trace_count_fn())
        if config.chain_execution_mode == "eager":
            timing_scope = "internal_segment_hmc_eager_execute_only"
        elif config.use_xla:
            timing_scope = (
                "internal_segment_hmc_tf_function_xla_first_call_compile_plus_execute"
            )
        else:
            timing_scope = (
                "internal_segment_hmc_tf_function_first_call_trace_compile_plus_execute"
            )
        return {
            "runtime": "tfp.mcmc.HamiltonianMonteCarlo.one_step_internal_segment_tf_while_loop",
            "internal_segment_runner": True,
            "uses_sample_chain": False,
            "returns_samples": False,
            "jit_compile": config.use_xla,
            "use_xla": config.use_xla,
            "chain_execution_mode": config.chain_execution_mode,
            "output_mode": config.output_mode,
            "target_status_trace_policy": "none",
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
            "segment_count": config.segment_count,
            "segment_length": config.segment_length,
            "total_transitions": config.total_transitions,
            "num_burnin_steps": config.num_burnin_steps,
            "num_leapfrog_steps": config.num_leapfrog_steps,
            "compile_trace_count": compile_trace_count,
            "call_s": call_s,
            "call_invocation_count": self._call_count,
            "call_timing_scope": timing_scope,
            "runner_build_s": self._runner_build_s,
            "first_call_s": self._first_call_s,
            "warm_call_s": self._warm_call_s,
            "timing_buckets": {
                "runner_build_s": "explanatory_only_runner_callable_construction",
                "first_call_s": (
                    "explanatory_only_first_internal_segment_compile_plus_execute_when_tf_function"
                ),
                "warm_call_s": "explanatory_only_subsequent_internal_segment_execute",
            },
            "nonclaims": (
                "internal-segment HMC engineering runner only",
                "summary-only mode returns no posterior samples",
                "no sampler convergence claim",
                "no posterior validity claim",
                "no GPU readiness claim",
                "no performance superiority claim",
            ),
        }


class RetainedSampleHMCArchiveRunner:
    """Reusable one-call HMC runner that archives retained samples privately.

    The runner owns the only HMC execution call: burn-in and all retained
    transitions occur inside one TensorFlow function.  Returned metadata is
    deliberately public-safe; raw retained samples, sample descriptors, kernel
    parameters, and archive paths remain confined to the private archive.
    """

    def __init__(
        self,
        adapter: Any,
        initial_state_template: Any,
        config: RetainedSampleHMCArchiveConfig,
    ) -> None:
        self.adapter = adapter
        self.config = config
        self.capability = _validate_full_chain_hmc_authority(adapter, config)

        import tensorflow as tf

        template = tf.cast(tf.convert_to_tensor(initial_state_template), tf.float64)
        if template.shape.rank is None:
            raise ValueError(
                "retained-sample HMC archive runner requires static state rank"
            )
        if any(dim is None for dim in template.shape):
            raise ValueError(
                "retained-sample HMC archive runner requires fully static state shape"
            )
        self._state_shape = tuple(int(dim) for dim in template.shape)
        self._state_dtype = template.dtype
        self._initial_state_template = template
        self._target_log_prob = _make_tfp_target_log_prob_fn(
            adapter,
            dtype=self._state_dtype,
        )
        runner_build_start = time.perf_counter()
        self._runner = self._build_runner()
        self._runner_build_s = time.perf_counter() - runner_build_start
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
        archive_dir: str | Path,
        archive_label: str,
        metadata: Mapping[str, Any] | None = None,
        current_state: Any | None = None,
        seed: tuple[int, int] | Any | None = None,
        step_size: float | Any | None = None,
        overwrite: bool = False,
    ) -> RetainedSampleHMCArchiveRunResult:
        """Execute one retained HMC call and write one private sample shard."""

        import tensorflow as tf

        label = str(archive_label).strip()
        if not label:
            raise ValueError("archive_label must be non-empty")
        state = self._initial_state_template if current_state is None else current_state
        state_tensor = tf.convert_to_tensor(state, dtype=self._state_dtype)
        if tuple(state_tensor.shape.as_list()) != self._state_shape:
            raise ValueError(
                "current_state shape must match retained-sample archive runner template"
            )
        seed_value = self.config.seed if seed is None else seed
        seed_tensor = tf.convert_to_tensor(seed_value, dtype=tf.int32)
        if tuple(seed_tensor.shape.as_list()) != (2,):
            raise ValueError("seed must have static shape (2,)")
        step_value = self.config.step_size if step_size is None else step_size
        step_tensor = tf.convert_to_tensor(step_value, dtype=self._state_dtype)
        if step_tensor.shape.rank != 0:
            raise ValueError("step_size must be a scalar")

        call_start = time.perf_counter()
        (
            samples,
            final_state,
            final_target_log_prob,
            final_index,
            sampler_telemetry,
        ) = self._runner(
            state_tensor,
            seed_tensor,
            step_tensor,
        )
        call_s = time.perf_counter() - call_start
        self._call_count += 1
        if self._call_count == 1:
            self._first_call_s = call_s
            self._warm_call_s = None
        else:
            self._warm_call_s = call_s

        diagnostics = _retained_sample_hmc_archive_diagnostics(
            samples=samples,
            final_state=final_state,
            final_target_log_prob=final_target_log_prob,
            final_index=final_index,
            config=self.config,
            hmc_execution_call_count=self._call_count,
            sampler_telemetry=sampler_telemetry,
        )
        metadata_payload = self._metadata(call_s=call_s)
        archive_summary = _write_retained_sample_hmc_archive_bundle(
            archive_dir=Path(archive_dir),
            archive_label=label,
            samples=samples,
            final_state=final_state,
            final_target_log_prob=final_target_log_prob,
            config=self.config,
            metadata={
                "caller_metadata": {} if metadata is None else dict(metadata),
                "runner_metadata": dict(metadata_payload),
            },
            diagnostics=diagnostics,
            overwrite=bool(overwrite),
        )
        return RetainedSampleHMCArchiveRunResult(
            final_state=final_state,
            final_target_log_prob=final_target_log_prob,
            final_index=final_index,
            diagnostics=diagnostics,
            metadata=metadata_payload,
            archive_summary=archive_summary,
        )

    __call__ = run

    def _build_runner(self) -> Callable[[Any, Any, Any], tuple[Any, Any, Any, Any, Any]]:
        import tensorflow as tf
        import tensorflow_probability as tfp

        tfm = tfp.mcmc
        config = self.config
        target_log_prob = self._target_log_prob
        state_shape = self._state_shape

        def run_retained_archive(
            current_state: Any,
            seed: Any,
            step_size: Any,
        ) -> tuple[Any, Any, Any, Any, Any]:
            kernel = tfm.HamiltonianMonteCarlo(
                target_log_prob_fn=target_log_prob,
                step_size=step_size,
                num_leapfrog_steps=config.num_leapfrog_steps,
            )
            kernel_results = kernel.bootstrap_results(current_state)
            initial_accepted = tf.convert_to_tensor(kernel_results.is_accepted)
            acceptance_count_by_chain = tf.zeros(
                tf.shape(initial_accepted),
                dtype=tf.int32,
            )
            acceptance_total_by_chain = tf.zeros(
                tf.shape(initial_accepted),
                dtype=tf.int32,
            )
            native_divergence_template = _extract_native_divergence_tensor(
                kernel_results
            )
            native_divergence_available = native_divergence_template is not None
            if native_divergence_available:
                divergence_count_by_chain = tf.zeros(
                    tf.shape(tf.convert_to_tensor(native_divergence_template)),
                    dtype=tf.int32,
                )
            else:
                divergence_count_by_chain = tf.zeros(
                    tf.shape(initial_accepted),
                    dtype=tf.int32,
                )

            def burnin_condition(index: Any, _state: Any, _results: Any) -> Any:
                return index < tf.constant(config.num_burnin_steps, dtype=tf.int32)

            def burnin_body(index: Any, state: Any, results: Any) -> tuple[Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(seed, index)
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                return index + 1, next_state, next_results

            _burnin_index, burnin_state, burnin_results = tf.while_loop(
                burnin_condition,
                burnin_body,
                (tf.constant(0, dtype=tf.int32), current_state, kernel_results),
                parallel_iterations=1,
            )

            samples = tf.zeros(
                (config.num_results,) + state_shape,
                dtype=current_state.dtype,
            )
            total = tf.constant(config.num_results, dtype=tf.int32)

            def sample_condition(
                index: Any,
                _state: Any,
                _results: Any,
                _samples: Any,
                _acceptance_count_by_chain: Any,
                _acceptance_total_by_chain: Any,
                _log_accept_finite_count: Any,
                _log_accept_nonfinite_count: Any,
                _log_accept_max_abs_finite: Any,
                _target_log_prob_finite_count: Any,
                _target_log_prob_nonfinite_count: Any,
                _target_log_prob_min_finite: Any,
                _target_log_prob_max_finite: Any,
                _divergence_count_by_chain: Any,
            ) -> Any:
                return index < total

            def sample_body(
                index: Any,
                state: Any,
                results: Any,
                sample_buffer: Any,
                accepted_count_by_chain: Any,
                total_count_by_chain: Any,
                log_accept_finite_count: Any,
                log_accept_nonfinite_count: Any,
                log_accept_max_abs_finite: Any,
                target_log_prob_finite_count: Any,
                target_log_prob_nonfinite_count: Any,
                target_log_prob_min_finite: Any,
                target_log_prob_max_finite: Any,
                divergence_by_chain: Any,
            ) -> tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
                step_seed = tf.random.experimental.stateless_fold_in(
                    seed,
                    tf.constant(config.num_burnin_steps, dtype=tf.int32) + index,
                )
                next_state, next_results = kernel.one_step(
                    state,
                    results,
                    seed=step_seed,
                )
                updated = tf.tensor_scatter_nd_update(
                    sample_buffer,
                    tf.reshape(index, [1, 1]),
                    tf.expand_dims(next_state, axis=0),
                )
                accepted = tf.cast(next_results.is_accepted, tf.int32)
                accepted_count_by_chain = accepted_count_by_chain + accepted
                total_count_by_chain = total_count_by_chain + tf.ones_like(
                    accepted,
                    dtype=tf.int32,
                )
                log_accept = tf.convert_to_tensor(
                    next_results.log_accept_ratio,
                    dtype=tf.float64,
                )
                log_accept_finite = tf.math.is_finite(log_accept)
                log_accept_finite_count = log_accept_finite_count + tf.reduce_sum(
                    tf.cast(log_accept_finite, tf.int32)
                )
                log_accept_nonfinite_count = (
                    log_accept_nonfinite_count
                    + tf.reduce_sum(
                        tf.cast(tf.logical_not(log_accept_finite), tf.int32)
                    )
                )
                log_accept_max_abs_finite = tf.maximum(
                    log_accept_max_abs_finite,
                    tf.reduce_max(
                        tf.where(
                            log_accept_finite,
                            tf.abs(log_accept),
                            tf.zeros_like(log_accept, dtype=tf.float64),
                        )
                    ),
                )
                target_log_prob = tf.convert_to_tensor(
                    next_results.accepted_results.target_log_prob,
                    dtype=tf.float64,
                )
                target_log_prob_finite = tf.math.is_finite(target_log_prob)
                target_log_prob_finite_count = (
                    target_log_prob_finite_count
                    + tf.reduce_sum(tf.cast(target_log_prob_finite, tf.int32))
                )
                target_log_prob_nonfinite_count = (
                    target_log_prob_nonfinite_count
                    + tf.reduce_sum(
                        tf.cast(tf.logical_not(target_log_prob_finite), tf.int32)
                    )
                )
                target_log_prob_min_finite = tf.minimum(
                    target_log_prob_min_finite,
                    tf.reduce_min(
                        tf.where(
                            target_log_prob_finite,
                            target_log_prob,
                            tf.fill(tf.shape(target_log_prob), tf.constant(float("inf"), dtype=tf.float64)),
                        )
                    ),
                )
                target_log_prob_max_finite = tf.maximum(
                    target_log_prob_max_finite,
                    tf.reduce_max(
                        tf.where(
                            target_log_prob_finite,
                            target_log_prob,
                            tf.fill(tf.shape(target_log_prob), tf.constant(float("-inf"), dtype=tf.float64)),
                        )
                    ),
                )
                if native_divergence_available:
                    divergence = tf.cast(
                        _extract_native_divergence_tensor(next_results),
                        tf.int32,
                    )
                    divergence_by_chain = divergence_by_chain + divergence
                return (
                    index + 1,
                    next_state,
                    next_results,
                    updated,
                    accepted_count_by_chain,
                    total_count_by_chain,
                    log_accept_finite_count,
                    log_accept_nonfinite_count,
                    log_accept_max_abs_finite,
                    target_log_prob_finite_count,
                    target_log_prob_nonfinite_count,
                    target_log_prob_min_finite,
                    target_log_prob_max_finite,
                    divergence_by_chain,
                )

            (
                final_index,
                final_state,
                final_results,
                samples,
                acceptance_count_by_chain,
                acceptance_total_by_chain,
                log_accept_finite_count,
                log_accept_nonfinite_count,
                log_accept_max_abs_finite,
                target_log_prob_finite_count,
                target_log_prob_nonfinite_count,
                target_log_prob_min_finite,
                target_log_prob_max_finite,
                divergence_count_by_chain,
            ) = tf.while_loop(
                sample_condition,
                sample_body,
                (
                    tf.constant(0, dtype=tf.int32),
                    burnin_state,
                    burnin_results,
                    samples,
                    acceptance_count_by_chain,
                    acceptance_total_by_chain,
                    tf.constant(0, dtype=tf.int32),
                    tf.constant(0, dtype=tf.int32),
                    tf.constant(0.0, dtype=tf.float64),
                    tf.constant(0, dtype=tf.int32),
                    tf.constant(0, dtype=tf.int32),
                    tf.constant(float("inf"), dtype=tf.float64),
                    tf.constant(float("-inf"), dtype=tf.float64),
                    divergence_count_by_chain,
                ),
                parallel_iterations=1,
            )
            final_target_log_prob = tf.convert_to_tensor(
                final_results.accepted_results.target_log_prob
            )
            sampler_telemetry = {
                "accepted_count_by_chain": acceptance_count_by_chain,
                "acceptance_total_by_chain": acceptance_total_by_chain,
                "accepted_decision_count": tf.reduce_sum(acceptance_count_by_chain),
                "acceptance_decision_count": tf.reduce_sum(acceptance_total_by_chain),
                "acceptance_rate": tf.reduce_sum(
                    tf.cast(acceptance_count_by_chain, tf.float64)
                )
                / tf.maximum(
                    tf.reduce_sum(tf.cast(acceptance_total_by_chain, tf.float64)),
                    tf.constant(1.0, dtype=tf.float64),
                ),
                "acceptance_rate_by_chain": tf.cast(
                    acceptance_count_by_chain,
                    tf.float64,
                )
                / tf.maximum(
                    tf.cast(acceptance_total_by_chain, tf.float64),
                    tf.ones_like(
                        tf.cast(acceptance_total_by_chain, tf.float64),
                        dtype=tf.float64,
                    ),
                ),
                "log_accept_ratio_finite_count": log_accept_finite_count,
                "log_accept_ratio_nonfinite_count": log_accept_nonfinite_count,
                "log_accept_ratio_max_abs_finite": log_accept_max_abs_finite,
                "target_log_prob_finite_count": target_log_prob_finite_count,
                "target_log_prob_nonfinite_count": target_log_prob_nonfinite_count,
                "target_log_prob_min_finite": tf.cond(
                    target_log_prob_finite_count > 0,
                    lambda: target_log_prob_min_finite,
                    lambda: tf.constant(float("nan"), dtype=tf.float64),
                ),
                "target_log_prob_max_finite": tf.cond(
                    target_log_prob_finite_count > 0,
                    lambda: target_log_prob_max_finite,
                    lambda: tf.constant(float("nan"), dtype=tf.float64),
                ),
                "native_divergence_available": tf.constant(
                    native_divergence_available
                ),
                "divergence_count_by_chain": divergence_count_by_chain,
                "divergence_count": tf.reduce_sum(divergence_count_by_chain),
            }
            return (
                samples,
                final_state,
                final_target_log_prob,
                final_index,
                sampler_telemetry,
            )

        if config.chain_execution_mode == "eager":
            return run_retained_archive
        input_signature = [
            tf.TensorSpec(shape=self._state_shape, dtype=self._state_dtype),
            tf.TensorSpec(shape=(2,), dtype=tf.int32),
            tf.TensorSpec(shape=(), dtype=self._state_dtype),
        ]
        if config.use_xla:
            return tf.function(
                run_retained_archive,
                input_signature=input_signature,
                jit_compile=True,
                reduce_retracing=True,
            )
        return tf.function(
            run_retained_archive,
            input_signature=input_signature,
            reduce_retracing=True,
        )

    def _metadata(self, *, call_s: float) -> Mapping[str, Any]:
        config = self.config
        capability = self.capability
        trace_count_fn = getattr(self._runner, "experimental_get_tracing_count", None)
        compile_trace_count = None if trace_count_fn is None else int(trace_count_fn())
        if config.chain_execution_mode == "eager":
            timing_scope = "retained_sample_hmc_archive_eager_execute_only"
        elif config.use_xla:
            timing_scope = (
                "retained_sample_hmc_archive_tf_function_xla_first_call_compile_plus_execute"
            )
        else:
            timing_scope = (
                "retained_sample_hmc_archive_tf_function_first_call_trace_compile_plus_execute"
            )
        return {
            "runtime": (
                "tfp.mcmc.HamiltonianMonteCarlo.one_step_retained_sample_archive_tf_while_loop"
            ),
            "single_call_retained_archive_runner": True,
            "hmc_execution_call_count": self._call_count,
            "uses_sample_chain": False,
            "returns_samples": False,
            "macrofinance_visible_chunk_count": 0,
            "private_archive_shard_count": 1,
            "private_archive_shard_semantics": (
                "exactly_one_physical_persisted_retained_sample_shard_or_opaque_bundle"
            ),
            "jit_compile": config.use_xla,
            "use_xla": config.use_xla,
            "chain_execution_mode": config.chain_execution_mode,
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
                    "config_private_signature": program_signature(
                        config.signature_payload()
                    ),
                    "initial_state_shape": self._state_shape,
                    "initial_state_dtype": self._state_dtype.name,
                    "dynamic_inputs": (
                        "current_state",
                        "seed",
                        "kernel_step_scalar",
                    ),
                }
            ),
            "initial_state_shape": self._state_shape,
            "initial_state_dtype": self._state_dtype.name,
            "dynamic_inputs": (
                "current_state",
                "seed",
                "kernel_step_scalar",
            ),
            "seed_source": "runtime_tensor_argument",
            "current_state_source": "runtime_tensor_argument",
            "kernel_step_source": "runtime_tensor_argument",
            "num_results": config.num_results,
            "num_burnin_steps": config.num_burnin_steps,
            "sampler_diagnostics_policy": config.sampler_diagnostics_policy,
            "sampler_health_telemetry": "public_safe_aggregate_counts",
            "native_divergence_telemetry": (
                "native_boolean_field_if_exposed_by_tfp_kernel_results"
            ),
            "kernel_parameters_publicized": False,
            "compile_trace_count": compile_trace_count,
            "call_s": call_s,
            "call_invocation_count": self._call_count,
            "call_timing_scope": timing_scope,
            "runner_build_s": self._runner_build_s,
            "first_call_s": self._first_call_s,
            "warm_call_s": self._warm_call_s,
            "timing_buckets": {
                "runner_build_s": "explanatory_only_runner_callable_construction",
                "first_call_s": (
                    "explanatory_only_first_retained_archive_compile_plus_execute_when_tf_function"
                ),
                "warm_call_s": "explanatory_only_subsequent_retained_archive_execute",
            },
            "nonclaims": (
                "retained-sample HMC archive engineering runner only",
                "raw retained samples are private and not returned",
                "no sampler convergence claim",
                "no posterior validity claim",
                "no GPU readiness claim",
                "no performance superiority claim",
            ),
        }


def build_internal_segment_hmc_runner(
    adapter: Any,
    initial_state_template: Any,
    config: InternalSegmentHMCRunnerConfig,
) -> InternalSegmentHMCRunner:
    """Build a summary-only BayesFilter HMC runner with internal segments."""

    return InternalSegmentHMCRunner(adapter, initial_state_template, config)


def build_retained_sample_hmc_archive_runner(
    adapter: Any,
    initial_state_template: Any,
    config: RetainedSampleHMCArchiveConfig,
) -> RetainedSampleHMCArchiveRunner:
    """Build a one-call HMC runner that writes retained samples privately."""

    return RetainedSampleHMCArchiveRunner(adapter, initial_state_template, config)


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
    runner_build_start = time.perf_counter()
    runner = _build_sample_chain_runner(config, kernel, trace_fn, state)
    runner_build_s = time.perf_counter() - runner_build_start
    sample_chain_start = time.perf_counter()
    samples, trace = runner()
    sample_chain_call_s = time.perf_counter() - sample_chain_start
    trace_capture_start = time.perf_counter()
    trace_for_diagnostics = trace if config.trace_policy == "standard" else {}
    diagnostics = _full_chain_hmc_diagnostics(
        samples,
        trace_for_diagnostics,
        trace_policy=config.trace_policy,
    )
    trace_capture_s = time.perf_counter() - trace_capture_start
    metadata = {
        "runtime": "tfp.mcmc.sample_chain",
        "jit_compile": config.use_xla,
        "use_xla": config.use_xla,
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
        "runner_build_s": runner_build_s,
        "first_call_s": sample_chain_call_s,
        "first_sample_chain_compile_execute_s": sample_chain_call_s,
        "warm_call_s": None,
        "warm_sample_chain_execute_s": None,
        "trace_capture_s": trace_capture_s,
        "trace_capture_timing_scope": (
            "post_sample_chain_public_safe_trace_diagnostics_capture"
        ),
        "warm_sample_shape": None,
        "warm_trace_keys": tuple(),
        "timing_buckets": {
            "runner_build_s": "explanatory_only_runner_callable_construction",
            "first_call_s": "explanatory_only_first_sample_chain_call",
            "warm_call_s": "not_available_single_use_runner",
            "trace_capture_s": (
                "explanatory_only_post_sample_chain_trace_diagnostics_capture"
            ),
        },
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
    if hasattr(value, "numpy"):
        return _json_safe_metadata(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _json_safe_metadata(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_safe_metadata(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json_safe_metadata(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    return value


def _write_serialized_tensor(path: Path, tensor: Any) -> tuple[str, int]:
    """Write one TensorFlow tensor shard and return SHA256 plus byte count."""

    import tensorflow as tf

    serialized = tf.io.serialize_tensor(tf.convert_to_tensor(tensor))
    data = bytes(serialized.numpy())
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest(), len(data)


def _tensor_or_plain_to_metadata(value: Any) -> Any:
    """Convert scalar TensorFlow/NumPy values to JSON-safe public metadata."""

    if value is None:
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    return _json_safe_metadata(value)


def _assert_hmc_archive_manifest_public_safe(payload: Mapping[str, Any]) -> None:
    """Fail closed if archive metadata exposes forbidden raw HMC payload keys."""

    forbidden_tokens = (
        "raw_sample",
        "raw_state",
        "mass_matrix",
        "selected_kernel_payload",
        "step_size",
        "leapfrog",
    )

    def walk(value: Any, path: tuple[str, ...]) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                key_text = str(key)
                lowered = key_text.lower()
                if any(token in lowered for token in forbidden_tokens):
                    if key_text == "forbidden_public_payloads":
                        walk(item, path + (key_text,))
                        continue
                    raise ValueError(
                        "HMC archive manifest contains forbidden public key: "
                        + ".".join(path + (key_text,))
                    )
                walk(item, path + (key_text,))
        elif isinstance(value, (tuple, list)):
            for index, item in enumerate(value):
                walk(item, path + (str(index),))

    walk(payload, tuple())


def _write_retained_sample_hmc_archive_bundle(
    *,
    archive_dir: Path,
    archive_label: str,
    samples: Any,
    final_state: Any,
    final_target_log_prob: Any,
    config: RetainedSampleHMCArchiveConfig,
    metadata: Mapping[str, Any],
    diagnostics: Mapping[str, Any],
    overwrite: bool,
) -> Mapping[str, Any]:
    """Persist one private retained-sample shard and public-safe summary.

    The returned summary intentionally omits file paths, tensor shapes, dtypes,
    and per-shard hashes.  Those details remain in the private manifest so a
    public client can prove the archive exists without seeing raw sample
    descriptors.
    """

    import tensorflow as tf

    root = Path(archive_dir)
    if root.exists() and not root.is_dir():
        raise ValueError("archive_dir exists and is not a directory")
    root.mkdir(parents=True, exist_ok=True)
    sample_tensor = tf.convert_to_tensor(samples)
    state_tensor = tf.convert_to_tensor(final_state)
    target_tensor = tf.convert_to_tensor(final_target_log_prob)
    expected_sample_shape = (int(config.num_results),) + tuple(
        int(dim) for dim in state_tensor.shape
    )
    if tuple(sample_tensor.shape.as_list()) != expected_sample_shape:
        raise ValueError("retained sample tensor shape must be (num_results,) + state shape")

    sample_path = root / f"{archive_label}_retained_samples.tftensor"
    state_path = root / f"{archive_label}_final_state.tftensor"
    target_path = root / f"{archive_label}_final_target_log_prob.tftensor"
    manifest_path = root / f"{archive_label}_private_manifest.json"
    for path in (sample_path, state_path, target_path, manifest_path):
        if path.exists() and not overwrite:
            raise FileExistsError(f"retained archive file already exists: {path}")

    sample_hash, sample_bytes = _write_serialized_tensor(sample_path, sample_tensor)
    state_hash, state_bytes = _write_serialized_tensor(state_path, state_tensor)
    target_hash, target_bytes = _write_serialized_tensor(target_path, target_tensor)
    finite_by_sample = tf.reduce_all(
        tf.math.is_finite(sample_tensor),
        axis=tf.range(1, tf.rank(sample_tensor), dtype=tf.int32),
    )
    nonfinite_count = int(
        tf.reduce_sum(
            tf.cast(tf.logical_not(finite_by_sample), tf.int32)
        ).numpy()
    )
    private_manifest = {
        "artifact_type": "bayesfilter_private_retained_sample_hmc_archive",
        "schema_version": 1,
        "archive_label": str(archive_label),
        "archive_dir": str(root),
        "sample_shards": (
            {
                "kind": "retained_samples",
                "path": str(sample_path),
                "sha256": sample_hash,
                "bytes": sample_bytes,
                "shape": tuple(int(dim) for dim in sample_tensor.shape),
                "dtype": sample_tensor.dtype.name,
            },
        ),
        "sidecars": {
            "final_state": {
                "path": str(state_path),
                "sha256": state_hash,
                "bytes": state_bytes,
                "shape": tuple(int(dim) for dim in state_tensor.shape),
                "dtype": state_tensor.dtype.name,
            },
            "final_target_log_prob": {
                "path": str(target_path),
                "sha256": target_hash,
                "bytes": target_bytes,
                "shape": tuple(int(dim) for dim in target_tensor.shape),
                "dtype": target_tensor.dtype.name,
            },
        },
        "sample_shard_count": 1,
        "sidecar_count": 2,
        "retained_sample_count": int(config.num_results),
        "nonfinite_retained_sample_count": int(nonfinite_count),
        "config_private_signature": program_signature(config.signature_payload()),
        "metadata": _json_safe_metadata(dict(metadata)),
        "diagnostics_private_metadata": _json_safe_metadata(
            {key: _tensor_or_plain_to_metadata(value) for key, value in diagnostics.items()}
        ),
        "privacy_contract": {
            "contains_private_raw_tensors": True,
            "public_summary_contains_paths": False,
            "public_summary_contains_raw_values": False,
            "public_summary_contains_tensor_descriptors": False,
        },
    }
    manifest_text = json.dumps(
        _json_safe_metadata(private_manifest),
        indent=2,
        sort_keys=True,
    ) + "\n"
    manifest_path.write_text(manifest_text, encoding="utf-8")
    manifest_hash = hashlib.sha256(manifest_text.encode("utf-8")).hexdigest()
    public_summary = {
        "artifact_type": "bayesfilter_retained_sample_hmc_archive_summary",
        "schema_version": 1,
        "archive_label": str(archive_label),
        "private_archive_shard_count": 1,
        "sample_shard_count": 1,
        "non_sample_sidecar_count": 3,
        "retained_sample_count": int(config.num_results),
        "total_valid_sample_count": int(config.num_results),
        "total_nonfinite_valid_sample_count": int(nonfinite_count),
        "aggregate_private_tensor_bytes": int(sample_bytes + state_bytes + target_bytes),
        "sample_shard_bytes": int(sample_bytes),
        "private_manifest_sha256": manifest_hash,
        "private_manifest_bytes": len(manifest_text.encode("utf-8")),
        "private_paths_publicized": False,
        "private_sample_or_state_descriptors_publicized": False,
        "public_summary_contains_raw_values": False,
        "public_summary_contains_kernel_payload": False,
        "private_manifest_is_sidecar_not_sample_shard": True,
        "final_state_sidecar_is_not_sample_shard": True,
        "privacy_contract": {
            "archive_contains_private_raw_tensors": True,
            "public_summary_contains_paths": False,
            "public_summary_contains_raw_values": False,
            "public_summary_contains_tensor_descriptors": False,
            "public_summary_contains_step_size": False,
            "public_summary_contains_leapfrog_count": False,
            "public_summary_contains_mass_matrix": False,
        },
        "nonclaims": (
            "retained HMC sample archive mechanics only",
            "no posterior convergence claim",
            "no serious sampler health claim",
            "no long-run retained-memory claim",
            "no scientific validity claim",
        ),
    }
    _assert_retained_archive_public_summary_safe(public_summary)
    return _json_safe_metadata(public_summary)


def _assert_retained_archive_public_summary_safe(payload: Mapping[str, Any]) -> None:
    """Fail closed on public retained-archive summary leakage."""

    forbidden_tokens = (
        "_path",
        "path",
        "shape",
        "dtype",
        "sample_sha",
        "state_sha",
        "raw_sample",
        "raw_state",
        "step_size",
        "leapfrog",
        "mass_matrix",
        "selected_kernel",
    )

    def walk(value: Any, path: tuple[str, ...]) -> None:
        if isinstance(value, Mapping):
            for key, item in value.items():
                key_text = str(key)
                lowered = key_text.lower()
                if any(token in lowered for token in forbidden_tokens):
                    allowed = key_text in {
                        "private_paths_publicized",
                        "sample_shard_count",
                        "sample_shard_bytes",
                        "private_manifest_is_sidecar_not_sample_shard",
                        "final_state_sidecar_is_not_sample_shard",
                        "public_summary_contains_paths",
                        "public_summary_contains_raw_values",
                        "public_summary_contains_step_size",
                        "public_summary_contains_leapfrog_count",
                        "public_summary_contains_mass_matrix",
                    }
                    if not allowed:
                        raise ValueError(
                            "retained archive public summary contains forbidden key: "
                            + ".".join(path + (key_text,))
                        )
                walk(item, path + (key_text,))
        elif isinstance(value, (tuple, list)):
            for index, item in enumerate(value):
                walk(item, path + (str(index),))

    walk(payload, tuple())


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


def _native_divergence_status_for_trace(
    trace: Mapping[str, Any],
    *,
    trace_policy: str,
) -> str:
    """Classify native divergence telemetry availability without proxies."""

    if "divergence" in trace:
        return "available"
    if trace_policy == "standard":
        return "not_exposed_by_kernel"
    return "unavailable"


def _hmc_health_diagnostics(trace: Mapping[str, Any]) -> Mapping[str, Any]:
    """Summarize non-divergence sampler health traces separately."""

    import tensorflow as tf

    health: dict[str, Any] = {
        "diagnostic_role": "hmc_health_diagnostics_not_native_divergence",
        "nonclaims": (
            "acceptance/log-accept/target-log-prob diagnostics are not native divergence telemetry",
            "no sampler convergence claim",
        ),
    }
    if "is_accepted" in trace:
        accepted = tf.cast(trace["is_accepted"], tf.float64)
        health["acceptance_rate"] = tf.reduce_mean(accepted)
        health["acceptance_finite"] = tf.reduce_all(tf.math.is_finite(accepted))
    else:
        health["acceptance_rate"] = None
        health["acceptance_finite"] = None
    if "log_accept_ratio" in trace:
        log_accept = tf.convert_to_tensor(trace["log_accept_ratio"], dtype=tf.float64)
        finite = tf.math.is_finite(log_accept)
        finite_values = tf.boolean_mask(log_accept, finite)
        health["log_accept_ratio"] = {
            "available": True,
            "finite": tf.reduce_all(finite),
            "finite_count": tf.reduce_sum(tf.cast(finite, tf.int32)),
            "nonfinite_count": tf.reduce_sum(tf.cast(tf.logical_not(finite), tf.int32)),
            "max_abs_finite": tf.cond(
                tf.size(finite_values) > 0,
                lambda: tf.reduce_max(tf.abs(finite_values)),
                lambda: tf.constant(float("nan"), dtype=tf.float64),
            ),
        }
    else:
        health["log_accept_ratio"] = {"available": False}
    if "target_log_prob" in trace:
        target_log_prob = tf.convert_to_tensor(trace["target_log_prob"], dtype=tf.float64)
        health["target_log_prob"] = {
            "available": True,
            "finite": tf.reduce_all(tf.math.is_finite(target_log_prob)),
            "min": tf.reduce_min(target_log_prob),
            "max": tf.reduce_max(target_log_prob),
        }
    else:
        health["target_log_prob"] = {"available": False}
    return health


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
        "native_divergence_status": _native_divergence_status_for_trace(
            trace,
            trace_policy=trace_policy,
        ),
        "divergence_status": _native_divergence_status_for_trace(
            trace,
            trace_policy=trace_policy,
        ),
        "divergence_count": None,
        "divergence_source": None,
        "hmc_health_diagnostics": _hmc_health_diagnostics(trace),
        "nonclaims": (
            "finite tiny-chain diagnostics only",
            "no sampler convergence claim",
            "native divergence unavailability is not zero divergences",
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
        diagnostics["native_divergence_status"] = "available"
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


def _fixed_size_hmc_chunk_diagnostics(
    samples: Any,
    valid_mask: Any,
    trace: Mapping[str, Any],
    *,
    trace_policy: str,
) -> Mapping[str, Any]:
    """Summarize only valid rows from a fixed-size HMC chunk buffer."""

    import tensorflow as tf

    mask = tf.convert_to_tensor(valid_mask, dtype=tf.bool)
    finite_by_row = tf.reduce_all(tf.math.is_finite(samples), axis=-1)
    valid_finite = tf.boolean_mask(finite_by_row, mask)
    valid_count = tf.reduce_sum(tf.cast(mask, tf.int32))
    invalid_count = tf.shape(mask, out_type=tf.int32)[0] - valid_count
    diagnostics: dict[str, Any] = {
        "valid_sample_count": valid_count,
        "invalid_sample_count": invalid_count,
        "finite_valid_sample_count": tf.reduce_sum(tf.cast(valid_finite, tf.int32)),
        "nonfinite_valid_sample_count": tf.reduce_sum(
            tf.cast(tf.logical_not(valid_finite), tf.int32)
        ),
        "sample_shape": tuple(int(dim) for dim in samples.shape),
        "valid_mask_shape": tuple(int(dim) for dim in mask.shape),
        "trace_policy": trace_policy,
        "native_divergence_status": _native_divergence_status_for_trace(
            trace,
            trace_policy=trace_policy,
        ),
        "divergence_status": _native_divergence_status_for_trace(
            trace,
            trace_policy=trace_policy,
        ),
        "divergence_count": None,
        "divergence_source": None,
        "hmc_health_diagnostics": _hmc_health_diagnostics(trace),
        "nonclaims": (
            "fixed-size chunk finite-sample diagnostics only",
            "invalid buffer rows are not counted as samples",
            "no sampler convergence claim",
            "native divergence unavailability is not zero divergences",
        ),
    }
    if "divergence" in trace:
        divergence = tf.boolean_mask(
            tf.convert_to_tensor(trace["divergence"], dtype=tf.bool),
            mask,
        )
        diagnostics["native_divergence_status"] = "available"
        diagnostics["divergence_status"] = "available"
        diagnostics["divergence_count"] = tf.reduce_sum(
            tf.cast(divergence, tf.int32)
        )
        diagnostics["divergence_source"] = "native_boolean_tfp_kernel_result"
    return diagnostics


def _internal_segment_hmc_diagnostics(
    *,
    final_state: Any,
    final_target_log_prob: Any,
    final_index: Any,
    segment_index: Any,
    segment_indices: Any,
    segment_target_log_prob: Any,
    config: InternalSegmentHMCRunnerConfig,
) -> Mapping[str, Any]:
    """Summarize a summary-only internal-segment HMC call."""

    import tensorflow as tf

    final_state_tensor = tf.convert_to_tensor(final_state)
    final_target_log_prob_tensor = tf.convert_to_tensor(final_target_log_prob)
    final_index_tensor = tf.convert_to_tensor(final_index, dtype=tf.int32)
    segment_index_tensor = tf.convert_to_tensor(segment_index, dtype=tf.int32)
    segment_indices_tensor = tf.convert_to_tensor(segment_indices, dtype=tf.int32)
    segment_target_log_prob_tensor = tf.convert_to_tensor(segment_target_log_prob)
    expected_indices = tf.range(
        tf.constant(1, dtype=tf.int32),
        tf.constant(config.segment_count + 1, dtype=tf.int32),
        dtype=tf.int32,
    ) * tf.constant(config.segment_length, dtype=tf.int32)
    return {
        "final_state_all_finite": tf.reduce_all(tf.math.is_finite(final_state_tensor)),
        "final_target_log_prob_all_finite": tf.reduce_all(
            tf.math.is_finite(final_target_log_prob_tensor)
        ),
        "segment_target_log_prob_all_finite": tf.reduce_all(
            tf.math.is_finite(segment_target_log_prob_tensor)
        ),
        "final_index": final_index_tensor,
        "expected_final_index": tf.constant(config.total_transitions, dtype=tf.int32),
        "final_index_matches_total_transitions": tf.equal(
            final_index_tensor,
            tf.constant(config.total_transitions, dtype=tf.int32),
        ),
        "segment_index": segment_index_tensor,
        "expected_segment_count": tf.constant(config.segment_count, dtype=tf.int32),
        "segment_index_matches_segment_count": tf.equal(
            segment_index_tensor,
            tf.constant(config.segment_count, dtype=tf.int32),
        ),
        "segment_indices_match_expected": tf.reduce_all(
            tf.equal(segment_indices_tensor, expected_indices)
        ),
        "segment_indices_shape": tuple(int(dim) for dim in segment_indices_tensor.shape),
        "segment_target_log_prob_shape": tuple(
            int(dim) for dim in segment_target_log_prob_tensor.shape
        ),
        "returns_samples": False,
        "output_mode": config.output_mode,
        "nonclaims": (
            "summary-only internal-segment diagnostics only",
            "no retained posterior samples",
            "no sampler convergence claim",
            "native divergence telemetry is unavailable in this reduced summary mode",
        ),
    }


def _retained_sample_hmc_archive_diagnostics(
    *,
    samples: Any,
    final_state: Any,
    final_target_log_prob: Any,
    final_index: Any,
    config: RetainedSampleHMCArchiveConfig,
    hmc_execution_call_count: int,
    sampler_telemetry: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    """Summarize one-call retained HMC output without returning samples."""

    import tensorflow as tf

    sample_tensor = tf.convert_to_tensor(samples)
    final_state_tensor = tf.convert_to_tensor(final_state)
    final_target_log_prob_tensor = tf.convert_to_tensor(final_target_log_prob)
    final_index_tensor = tf.convert_to_tensor(final_index, dtype=tf.int32)
    finite_by_sample = tf.reduce_all(
        tf.math.is_finite(sample_tensor),
        axis=tf.range(1, tf.rank(sample_tensor), dtype=tf.int32),
    )
    diagnostics = {
        "retained_sample_count": tf.constant(config.num_results, dtype=tf.int32),
        "valid_sample_count": tf.constant(config.num_results, dtype=tf.int32),
        "finite_retained_sample_count": tf.reduce_sum(
            tf.cast(finite_by_sample, tf.int32)
        ),
        "nonfinite_retained_sample_count": tf.reduce_sum(
            tf.cast(tf.logical_not(finite_by_sample), tf.int32)
        ),
        "retained_samples_all_finite": tf.reduce_all(finite_by_sample),
        "final_state_all_finite": tf.reduce_all(tf.math.is_finite(final_state_tensor)),
        "final_target_log_prob_all_finite": tf.reduce_all(
            tf.math.is_finite(final_target_log_prob_tensor)
        ),
        "final_index": final_index_tensor,
        "expected_final_index": tf.constant(config.num_results, dtype=tf.int32),
        "final_index_matches_num_results": tf.equal(
            final_index_tensor,
            tf.constant(config.num_results, dtype=tf.int32),
        ),
        "returns_samples": False,
        "uses_sample_chain": False,
        "hmc_execution_call_count": int(hmc_execution_call_count),
        "macrofinance_visible_chunk_count": 0,
        "private_archive_shard_count": 1,
        "native_divergence_status": "not_collected",
        "divergence_status": "not_collected",
        "divergence_count": None,
        "divergence_source": None,
        "sampler_diagnostics_policy": config.sampler_diagnostics_policy,
        "sampler_health_diagnostics": {
            "available": False,
            "diagnostic_role": "hmc_health_diagnostics_not_native_divergence",
            "nonclaims": (
                "acceptance/log-accept/target-log-prob diagnostics are not native divergence telemetry",
                "no sampler convergence claim",
            ),
        },
        "nonclaims": (
            "one-call retained archive finite-sample diagnostics only",
            "raw retained samples are private and not returned",
            "no sampler convergence claim",
            "native divergence unavailability is not zero divergences",
        ),
    }
    if sampler_telemetry is None:
        return diagnostics
    telemetry = dict(sampler_telemetry)
    native_divergence_available = bool(
        tf.convert_to_tensor(telemetry["native_divergence_available"]).numpy()
    )
    if native_divergence_available:
        diagnostics["native_divergence_status"] = "available"
        diagnostics["divergence_status"] = "available"
        diagnostics["divergence_count"] = tf.convert_to_tensor(
            telemetry["divergence_count"],
            dtype=tf.int32,
        )
        diagnostics["divergence_count_by_chain"] = tf.convert_to_tensor(
            telemetry["divergence_count_by_chain"],
            dtype=tf.int32,
        )
        diagnostics["divergence_source"] = "native_boolean_tfp_kernel_result"
    else:
        diagnostics["native_divergence_status"] = "not_exposed_by_kernel"
        diagnostics["divergence_status"] = "not_exposed_by_kernel"
        diagnostics["divergence_count"] = None
        diagnostics["divergence_count_by_chain"] = None
        diagnostics["divergence_source"] = None
    diagnostics["acceptance_rate"] = tf.convert_to_tensor(
        telemetry["acceptance_rate"],
        dtype=tf.float64,
    )
    diagnostics["acceptance_rate_by_chain"] = tf.convert_to_tensor(
        telemetry["acceptance_rate_by_chain"],
        dtype=tf.float64,
    )
    diagnostics["accepted_decision_count"] = tf.convert_to_tensor(
        telemetry["accepted_decision_count"],
        dtype=tf.int32,
    )
    diagnostics["acceptance_decision_count"] = tf.convert_to_tensor(
        telemetry["acceptance_decision_count"],
        dtype=tf.int32,
    )
    diagnostics["sampler_health_diagnostics"] = {
        "available": True,
        "diagnostic_role": "hmc_health_diagnostics_not_native_divergence",
        "acceptance_rate": diagnostics["acceptance_rate"],
        "acceptance_rate_by_chain": diagnostics["acceptance_rate_by_chain"],
        "accepted_decision_count": diagnostics["accepted_decision_count"],
        "acceptance_decision_count": diagnostics["acceptance_decision_count"],
        "log_accept_ratio": {
            "available": True,
            "finite_count": tf.convert_to_tensor(
                telemetry["log_accept_ratio_finite_count"],
                dtype=tf.int32,
            ),
            "nonfinite_count": tf.convert_to_tensor(
                telemetry["log_accept_ratio_nonfinite_count"],
                dtype=tf.int32,
            ),
            "max_abs_finite": tf.convert_to_tensor(
                telemetry["log_accept_ratio_max_abs_finite"],
                dtype=tf.float64,
            ),
        },
        "target_log_prob": {
            "available": True,
            "finite_count": tf.convert_to_tensor(
                telemetry["target_log_prob_finite_count"],
                dtype=tf.int32,
            ),
            "nonfinite_count": tf.convert_to_tensor(
                telemetry["target_log_prob_nonfinite_count"],
                dtype=tf.int32,
            ),
            "min_finite": tf.convert_to_tensor(
                telemetry["target_log_prob_min_finite"],
                dtype=tf.float64,
            ),
            "max_finite": tf.convert_to_tensor(
                telemetry["target_log_prob_max_finite"],
                dtype=tf.float64,
            ),
        },
        "native_divergence": {
            "status": diagnostics["native_divergence_status"],
            "count": diagnostics["divergence_count"],
            "count_by_chain": diagnostics["divergence_count_by_chain"],
            "source": diagnostics["divergence_source"],
        },
        "nonclaims": (
            "acceptance/log-accept/target-log-prob diagnostics are not native divergence telemetry",
            "native divergence unavailability is not zero divergences",
            "no sampler convergence claim",
        ),
    }
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
