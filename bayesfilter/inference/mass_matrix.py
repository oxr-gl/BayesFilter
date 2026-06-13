"""Mass-matrix and whitening helpers with explicit provenance.

The HMC tuning path treats a MAP-local negative Hessian as a precision
candidate.  It must therefore fail closed on non-finite inputs and record any
regularization that turns an indefinite/ill-conditioned matrix into a usable
positive-definite mass artifact.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class MassMatrixResult:
    covariance: np.ndarray
    source: str
    matrix_kind: str
    jitter: float
    eigenvalue_floor: float | None = None
    regularized_precision: np.ndarray | None = None
    precision_eigen_summary: dict[str, Any] | None = None
    covariance_eigen_summary: dict[str, Any] | None = None
    regularization_report: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        covariance = np.asarray(self.covariance, dtype=float).copy()
        covariance.setflags(write=False)
        object.__setattr__(self, "covariance", covariance)
        object.__setattr__(self, "source", str(self.source))
        object.__setattr__(self, "matrix_kind", str(self.matrix_kind))
        object.__setattr__(self, "jitter", float(self.jitter))
        if self.eigenvalue_floor is not None:
            object.__setattr__(self, "eigenvalue_floor", float(self.eigenvalue_floor))
        if self.regularized_precision is not None:
            precision = np.asarray(self.regularized_precision, dtype=float).copy()
            precision.setflags(write=False)
            object.__setattr__(self, "regularized_precision", precision)
        if self.regularized_precision is not None:
            object.__setattr__(
                self,
                "precision_eigen_summary",
                _eigen_summary(np.asarray(self.regularized_precision, dtype=float)),
            )
        elif self.precision_eigen_summary is not None:
            object.__setattr__(
                self,
                "precision_eigen_summary",
                _normalize_eigen_summary(self.precision_eigen_summary),
            )
        object.__setattr__(
            self,
            "covariance_eigen_summary",
            _eigen_summary(covariance),
        )
        report = {} if self.regularization_report is None else dict(self.regularization_report)
        object.__setattr__(self, "regularization_report", report)


def regularize_covariance(covariance: Any, *, jitter: float = 1e-9) -> np.ndarray:
    matrix = _square_matrix(covariance, "covariance")
    return matrix + float(jitter) * np.eye(matrix.shape[0])


def covariance_from_precision(
    precision: Any,
    *,
    source: str,
    jitter: float = 1e-9,
    eigenvalue_floor: float | None = None,
    max_condition_number: float | None = None,
    dense: bool = True,
) -> MassMatrixResult:
    matrix = _square_matrix(precision, "precision")
    regularized, report = regularize_precision(
        matrix,
        jitter=jitter,
        eigenvalue_floor=eigenvalue_floor,
        max_condition_number=max_condition_number,
    )
    if dense:
        covariance = np.linalg.inv(regularized)
        matrix_kind = "dense"
    else:
        diagonal = np.diag(regularized)
        if np.any(diagonal <= 0.0) or not np.all(np.isfinite(diagonal)):
            raise ValueError("regularized precision diagonal must be positive finite")
        covariance = np.diag(1.0 / diagonal)
        matrix_kind = "diagonal"
        report = {
            **report,
            "diagonal_fallback_used": True,
            "diagonal_fallback_source": "regularized_precision_diagonal",
        }
    return MassMatrixResult(
        covariance=covariance,
        source=source,
        matrix_kind=matrix_kind,
        jitter=float(jitter),
        eigenvalue_floor=report["effective_eigenvalue_floor"],
        regularized_precision=regularized,
        precision_eigen_summary=_eigen_summary(regularized),
        covariance_eigen_summary=_eigen_summary(covariance),
        regularization_report=report,
    )


def covariance_from_negative_hessian(
    negative_hessian: Any,
    *,
    source: str = "negative_hessian",
    jitter: float = 1e-9,
    eigenvalue_floor: float | None = None,
    max_condition_number: float | None = None,
    dense: bool = True,
) -> MassMatrixResult:
    """Convert an explicit negative log-posterior Hessian/precision to covariance."""

    return covariance_from_precision(
        negative_hessian,
        source=source,
        jitter=jitter,
        eigenvalue_floor=eigenvalue_floor,
        max_condition_number=max_condition_number,
        dense=dense,
    )


def regularize_precision(
    precision: Any,
    *,
    jitter: float = 1e-9,
    eigenvalue_floor: float | None = None,
    max_condition_number: float | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    """Return a positive-definite precision matrix and regularization report."""

    matrix = _square_matrix(precision, "precision")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("precision must be finite")
    jitter_value = float(jitter)
    if not np.isfinite(jitter_value) or jitter_value < 0.0:
        raise ValueError("jitter must be finite and non-negative")
    floor = 0.0 if eigenvalue_floor is None else float(eigenvalue_floor)
    if not np.isfinite(floor) or floor < 0.0:
        raise ValueError("eigenvalue_floor must be finite and non-negative")
    if max_condition_number is not None:
        max_condition = float(max_condition_number)
        if not np.isfinite(max_condition) or max_condition <= 1.0:
            raise ValueError("max_condition_number must be finite and greater than 1")
    else:
        max_condition = None

    asymmetry = matrix - matrix.T
    asymmetry_max_abs = float(np.max(np.abs(asymmetry))) if matrix.size else 0.0
    symmetric = 0.5 * (matrix + matrix.T)
    jittered = symmetric + jitter_value * np.eye(symmetric.shape[0])
    raw_eigvals, eigvecs = np.linalg.eigh(jittered)
    if not np.all(np.isfinite(raw_eigvals)):
        raise ValueError("precision eigenvalues must be finite")

    positive_raw = raw_eigvals[raw_eigvals > 0.0]
    if floor == 0.0:
        if positive_raw.size == 0:
            raise ValueError(
                "precision must have a positive eigenvalue; pass eigenvalue_floor"
            )
        floor = max(floor, np.finfo(float).eps * max(1.0, float(np.max(positive_raw))))
    if max_condition is not None:
        floor = max(floor, float(np.max(raw_eigvals)) / max_condition)
    if floor <= 0.0:
        floor = np.finfo(float).eps

    regularized_eigvals = np.maximum(raw_eigvals, floor)
    regularized = (eigvecs * regularized_eigvals) @ eigvecs.T
    regularized = 0.5 * (regularized + regularized.T)
    clipped = regularized_eigvals > raw_eigvals
    report = {
        "method": "symmetric_eigendecomposition_floor",
        "jitter": jitter_value,
        "requested_eigenvalue_floor": (
            None if eigenvalue_floor is None else float(eigenvalue_floor)
        ),
        "effective_eigenvalue_floor": float(floor),
        "max_condition_number": max_condition,
        "raw_min_eigenvalue": float(np.min(raw_eigvals)),
        "raw_max_eigenvalue": float(np.max(raw_eigvals)),
        "regularized_min_eigenvalue": float(np.min(regularized_eigvals)),
        "regularized_max_eigenvalue": float(np.max(regularized_eigvals)),
        "raw_nonpositive_eigenvalue_count": int(np.sum(raw_eigvals <= 0.0)),
        "clipped_eigenvalue_count": int(np.sum(clipped)),
        "symmetry_projection": "average_with_transpose",
        "input_asymmetry_max_abs": asymmetry_max_abs,
        "input_asymmetric": bool(asymmetry_max_abs > 0.0),
        "diagonal_fallback_used": False,
        "silent_eigenvalue_reflection": False,
    }
    return regularized, report


def whitening_from_covariance(covariance: Any, *, jitter: float = 1e-9) -> np.ndarray:
    """Return W with covariance approximately W @ W.T."""

    regularized = regularize_covariance(covariance, jitter=jitter)
    return np.linalg.cholesky(regularized)


def _square_matrix(value: Any, name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square matrix")
    return matrix


def _eigen_summary(matrix: Any) -> dict[str, Any]:
    square = _square_matrix(matrix, "matrix")
    symmetric = 0.5 * (square + square.T)
    eigenvalues = np.linalg.eigvalsh(symmetric)
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


def _normalize_eigen_summary(summary: dict[str, Any]) -> dict[str, Any]:
    eigenvalues = summary.get("eigenvalues", ())
    return {
        "finite": bool(summary.get("finite")),
        "positive": bool(summary.get("positive")),
        "min": float(summary.get("min")),
        "max": float(summary.get("max")),
        "condition_number": float(summary.get("condition_number")),
        "eigenvalues": tuple(float(value) for value in eigenvalues),
    }
