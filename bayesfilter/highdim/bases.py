"""Basis functions for internal high-dimensional TT contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import tensorflow as tf

from bayesfilter.highdim.diagnostics import (
    MassMeasure,
    MeasureConvention,
    assert_density_matches_mass,
    assert_tf_float64,
)


@dataclass(frozen=True)
class BoundedInterval:
    """Closed one-dimensional interval for bounded polynomial bases."""

    left: tf.Tensor
    right: tf.Tensor
    dtype: tf.DType = tf.float64

    def __init__(self, left, right, dtype: tf.DType = tf.float64) -> None:
        object.__setattr__(self, "dtype", dtype)
        object.__setattr__(self, "left", tf.convert_to_tensor(left, dtype=dtype))
        object.__setattr__(self, "right", tf.convert_to_tensor(right, dtype=dtype))
        if self.dtype != tf.float64:
            raise ValueError("Phase-1 highdim bases require tf.float64")
        if not bool((self.right > self.left).numpy()):
            raise ValueError("right must be greater than left")

    @property
    def length(self) -> tf.Tensor:
        return self.right - self.left

    def to_reference(self, points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=self.dtype)
        return 2.0 * (values - self.left) / self.length - 1.0


@dataclass(frozen=True)
class UniformReferenceMeasure:
    """Uniform probability reference measure on a bounded interval."""

    domain: BoundedInterval

    def __post_init__(self) -> None:
        if not isinstance(self.domain, BoundedInterval):
            raise TypeError("domain must be a BoundedInterval")


@dataclass(frozen=True)
class LegendreBasis1D:
    """Normalized Legendre basis under the uniform probability measure."""

    domain: BoundedInterval
    max_degree: int
    normalized: bool = True

    def __post_init__(self) -> None:
        if not isinstance(self.domain, BoundedInterval):
            raise TypeError("domain must be a BoundedInterval")
        if int(self.max_degree) < 0:
            raise ValueError("max_degree must be nonnegative")
        if not self.normalized:
            raise ValueError("Phase-1 pins normalized Legendre bases only")

    @property
    def basis_dim(self) -> int:
        return int(self.max_degree) + 1

    @property
    def dtype(self) -> tf.DType:
        return self.domain.dtype

    @property
    def reference_measure(self) -> UniformReferenceMeasure:
        return UniformReferenceMeasure(self.domain)

    def evaluate(self, points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        xi = self.domain.to_reference(values)
        polys = _legendre_values(xi, self.max_degree)
        scales = tf.sqrt(
            tf.cast(2 * tf.range(self.basis_dim, dtype=tf.int32) + 1, tf.float64)
        )
        return polys * scales

    def derivative(self, points: tf.Tensor) -> tf.Tensor:
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        xi = self.domain.to_reference(values)
        derivs = _legendre_reference_derivatives(xi, self.max_degree)
        scales = tf.sqrt(
            tf.cast(2 * tf.range(self.basis_dim, dtype=tf.int32) + 1, tf.float64)
        )
        return derivs * scales * (2.0 / self.domain.length)

    def mass_matrix(self, measure: MassMeasure) -> tf.Tensor:
        if not isinstance(measure, MassMeasure):
            raise TypeError("measure must be a MassMeasure")
        identity = tf.eye(self.basis_dim, dtype=tf.float64)
        if measure is MassMeasure.REFERENCE_MEASURE:
            return identity
        return identity * self.domain.length

    def integral_vector(self, measure: MassMeasure) -> tf.Tensor:
        if not isinstance(measure, MassMeasure):
            raise TypeError("measure must be a MassMeasure")
        first = tf.concat(
            [
                tf.ones([1], dtype=tf.float64),
                tf.zeros([self.basis_dim - 1], dtype=tf.float64),
            ],
            axis=0,
        )
        if measure is MassMeasure.REFERENCE_MEASURE:
            return first
        return first * self.domain.length


@dataclass(frozen=True)
class ProductBasis:
    """Tensor-product collection of one-dimensional bases."""

    bases: tuple[LegendreBasis1D, ...]
    convention: MeasureConvention

    def __init__(
        self,
        bases: Sequence[LegendreBasis1D],
        convention: MeasureConvention,
    ) -> None:
        object.__setattr__(self, "bases", tuple(bases))
        object.__setattr__(self, "convention", convention)
        if not self.bases:
            raise ValueError("ProductBasis requires at least one basis")
        for basis in self.bases:
            if not isinstance(basis, LegendreBasis1D):
                raise TypeError("ProductBasis currently supports LegendreBasis1D")
        assert_density_matches_mass(convention)

    @property
    def dimension(self) -> int:
        return len(self.bases)

    def basis_dim_tuple(self) -> tuple[int, ...]:
        return tuple(basis.basis_dim for basis in self.bases)

    def evaluate_axis(self, axis: int, points: tf.Tensor) -> tf.Tensor:
        if axis < 0 or axis >= self.dimension:
            raise IndexError("axis out of range")
        values = tf.convert_to_tensor(points, dtype=tf.float64)
        assert_tf_float64("points", values)
        return self.bases[axis].evaluate(values)


def _legendre_values(xi: tf.Tensor, max_degree: int) -> tf.Tensor:
    xi = tf.convert_to_tensor(xi, dtype=tf.float64)
    flat = tf.reshape(xi, [-1])
    values = [tf.ones_like(flat)]
    if max_degree >= 1:
        values.append(flat)
    for n in range(1, max_degree):
        n_float = tf.cast(n, tf.float64)
        next_value = ((2.0 * n_float + 1.0) * flat * values[n] - n_float * values[n - 1]) / (
            n_float + 1.0
        )
        values.append(next_value)
    stacked = tf.stack(values, axis=-1)
    return tf.reshape(stacked, tf.concat([tf.shape(xi), [max_degree + 1]], axis=0))


def _legendre_reference_derivatives(xi: tf.Tensor, max_degree: int) -> tf.Tensor:
    xi = tf.convert_to_tensor(xi, dtype=tf.float64)
    flat = tf.reshape(xi, [-1])
    polys = tf.reshape(_legendre_values(flat, max_degree), [tf.shape(flat)[0], max_degree + 1])
    derivs = [tf.zeros_like(flat)]
    if max_degree >= 1:
        derivs.append(tf.ones_like(flat))
    for n in range(2, max_degree + 1):
        n_float = tf.cast(n, tf.float64)
        deriv = n_float * (polys[:, n - 1] + flat * derivs[n - 1]) - n_float * derivs[n - 2] / (
            n_float - 1.0
        )
        # Simpler and stable for low-degree tests: differentiate recurrence.
        prev_n = tf.cast(n - 1, tf.float64)
        deriv = (
            (2.0 * prev_n + 1.0) * (polys[:, n - 1] + flat * derivs[n - 1])
            - prev_n * derivs[n - 2]
        ) / (prev_n + 1.0)
        derivs.append(deriv)
    stacked = tf.stack(derivs, axis=-1)
    return tf.reshape(stacked, tf.concat([tf.shape(xi), [max_degree + 1]], axis=0))
