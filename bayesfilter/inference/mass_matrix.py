"""Mass-matrix and whitening helpers with explicit provenance."""

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

    def __post_init__(self) -> None:
        covariance = np.asarray(self.covariance, dtype=float).copy()
        covariance.setflags(write=False)
        object.__setattr__(self, "covariance", covariance)
        object.__setattr__(self, "source", str(self.source))
        object.__setattr__(self, "matrix_kind", str(self.matrix_kind))
        object.__setattr__(self, "jitter", float(self.jitter))
        if self.eigenvalue_floor is not None:
            object.__setattr__(self, "eigenvalue_floor", float(self.eigenvalue_floor))


def regularize_covariance(covariance: Any, *, jitter: float = 1e-9) -> np.ndarray:
    matrix = _square_matrix(covariance, "covariance")
    return matrix + float(jitter) * np.eye(matrix.shape[0])


def covariance_from_precision(
    precision: Any,
    *,
    source: str,
    jitter: float = 1e-9,
) -> MassMatrixResult:
    matrix = _square_matrix(precision, "precision")
    regularized = matrix + float(jitter) * np.eye(matrix.shape[0])
    covariance = np.linalg.inv(regularized)
    return MassMatrixResult(
        covariance=covariance,
        source=source,
        matrix_kind="dense",
        jitter=float(jitter),
    )


def covariance_from_negative_hessian(
    negative_hessian: Any,
    *,
    source: str = "negative_hessian",
    jitter: float = 1e-9,
) -> MassMatrixResult:
    """Convert an explicit negative log-posterior Hessian/precision to covariance."""

    return covariance_from_precision(negative_hessian, source=source, jitter=jitter)


def whitening_from_covariance(covariance: Any, *, jitter: float = 1e-9) -> np.ndarray:
    """Return W with covariance approximately W @ W.T."""

    regularized = regularize_covariance(covariance, jitter=jitter)
    return np.linalg.cholesky(regularized)


def _square_matrix(value: Any, name: str) -> np.ndarray:
    matrix = np.asarray(value, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"{name} must be a square matrix")
    return matrix
