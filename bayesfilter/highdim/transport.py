"""Grid-based KR transport diagnostics for Phase 2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import tensorflow as tf

from bayesfilter.highdim.diagnostics import HighDimStatus, freeze_mapping
from bayesfilter.highdim.squared_tt import SquaredTTDensity, trapezoid_integral


@dataclass(frozen=True)
class KRCDFConfig:
    """Configuration for deterministic grid CDF and bisection inversion."""

    grid_size: int
    bisection_steps: int
    monotonicity_tolerance: float
    bracket_tolerance: float
    denominator_floor: float
    max_floor_count: int
    dtype: tf.DType = tf.float64

    def __post_init__(self) -> None:
        if self.grid_size < 3:
            raise ValueError("grid_size must be at least 3")
        if self.bisection_steps <= 0:
            raise ValueError("bisection_steps must be positive")
        if self.dtype != tf.float64:
            raise ValueError("KRCDFConfig requires tf.float64")


@dataclass(frozen=True)
class KRInversionResult:
    """Result for one coordinate inverse-CDF operation."""

    z_value: tf.Tensor
    cdf_value: tf.Tensor
    iterations: int
    status: HighDimStatus
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "z_value",
            tf.convert_to_tensor(self.z_value, dtype=tf.float64),
        )
        object.__setattr__(
            self,
            "cdf_value",
            tf.convert_to_tensor(self.cdf_value, dtype=tf.float64),
        )
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))


@dataclass(frozen=True)
class KRTransport:
    """Lower-triangular KR map built from Phase-2 grid conditionals."""

    density: SquaredTTDensity
    coordinate_order: tuple[int, ...]
    cdf_config: KRCDFConfig

    def __init__(
        self,
        density: SquaredTTDensity,
        coordinate_order: Sequence[int],
        cdf_config: KRCDFConfig,
    ) -> None:
        if not isinstance(density, SquaredTTDensity):
            raise TypeError("density must be a SquaredTTDensity")
        order = tuple(int(axis) for axis in coordinate_order)
        dimension = len(density.sqrt_tt.cores)
        if sorted(order) != list(range(dimension)):
            raise ValueError(f"coordinate_order: {HighDimStatus.INVALID_SHAPE.value}")
        if order != tuple(range(dimension)):
            raise NotImplementedError("Phase 2 supports natural coordinate order")
        object.__setattr__(self, "density", density)
        object.__setattr__(self, "coordinate_order", order)
        object.__setattr__(self, "cdf_config", cdf_config)

    def forward(self, z_points: tf.Tensor):
        values = tf.convert_to_tensor(z_points, dtype=tf.float64)
        if values.shape.rank != 2 or values.shape[1] != len(self.coordinate_order):
            raise ValueError(f"z_points: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(tf.math.is_finite(values)).numpy()):
            raise ValueError(HighDimStatus.NONFINITE_VALUE.value)
        rows = []
        log_terms = []
        per_axis_results = []
        for row_index in range(int(values.shape[0])):
            row = values[row_index : row_index + 1, :]
            u_columns = []
            row_log_terms = []
            for axis in self.coordinate_order:
                prefix = row[:, :axis]
                z_value = row[:, axis]
                cdf_value, density_value, status, diagnostics = self._cdf_at(axis, prefix, z_value)
                u_columns.append(tf.reshape(cdf_value, []))
                row_log_terms.append(tf.math.log(tf.reshape(density_value, [])))
                per_axis_results.append(
                    KRInversionResult(
                        z_value=tf.reshape(z_value, []),
                        cdf_value=tf.reshape(cdf_value, []),
                        iterations=0,
                        status=status,
                        diagnostics=diagnostics,
                    )
                )
            rows.append(tf.stack(u_columns))
            log_terms.append(tf.reduce_sum(tf.stack(row_log_terms)))
        return tf.stack(rows, axis=0), tf.stack(log_terms), per_axis_results

    def inverse(self, u_points: tf.Tensor):
        values = tf.convert_to_tensor(u_points, dtype=tf.float64)
        if values.shape.rank != 2 or values.shape[1] != len(self.coordinate_order):
            raise ValueError(f"u_points: {HighDimStatus.INVALID_SHAPE.value}")
        if not bool(tf.reduce_all(tf.math.is_finite(values)).numpy()):
            raise ValueError(HighDimStatus.NONFINITE_VALUE.value)
        rows = []
        log_terms = []
        per_axis_results = []
        for row_index in range(int(values.shape[0])):
            current = []
            row_log_terms = []
            for axis in self.coordinate_order:
                if axis != len(current):
                    raise NotImplementedError("Phase 2 supports natural coordinate order")
                prefix = (
                    tf.reshape(tf.stack(current), [1, axis])
                    if current
                    else tf.zeros([1, 0], dtype=tf.float64)
                )
                result, density_value = self._inverse_axis(
                    axis,
                    prefix,
                    tf.reshape(values[row_index, axis], []),
                )
                current.append(tf.reshape(result.z_value, []))
                row_log_terms.append(-tf.math.log(tf.reshape(density_value, [])))
                per_axis_results.append(result)
            rows.append(tf.stack(current))
            log_terms.append(tf.reduce_sum(tf.stack(row_log_terms)))
        return tf.stack(rows, axis=0), tf.stack(log_terms), per_axis_results

    def log_jacobian(self, z_points: tf.Tensor) -> tf.Tensor:
        _, log_det, _ = self.forward(z_points)
        return log_det

    def _axis_grid(self, axis: int) -> tf.Tensor:
        basis = self.density.sqrt_tt.product_basis.bases[axis]
        return tf.linspace(
            basis.domain.left,
            basis.domain.right,
            self.cdf_config.grid_size,
        )

    def _cdf_at(self, axis: int, prefix: tf.Tensor, z_value: tf.Tensor):
        if not bool(tf.reduce_all(tf.math.is_finite(tf.convert_to_tensor(z_value))).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.NONFINITE_VALUE,
                {"z_value": z_value},
            )
        grid = self._axis_grid(axis)
        conditional = self.density.conditional_density(axis, prefix, grid)
        if not bool(tf.reduce_all(tf.math.is_finite(conditional)).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.NONFINITE_VALUE,
                {"reason": "nonfinite conditional"},
            )
        increments = 0.5 * (conditional[1:] + conditional[:-1]) * (grid[1:] - grid[:-1])
        cdf_grid = tf.concat(
            [tf.zeros([1], dtype=tf.float64), tf.cumsum(increments)],
            axis=0,
        )
        total = cdf_grid[-1]
        if not bool(tf.math.is_finite(total).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.NONFINITE_VALUE,
                {"total": total},
            )
        if bool((total <= self.cdf_config.denominator_floor).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.CONDITIONAL_DENOMINATOR_FLOOR_EXCEEDED,
                {"total": total},
            )
        cdf_grid = cdf_grid / total
        min_increment = tf.reduce_min(cdf_grid[1:] - cdf_grid[:-1])
        if not bool(tf.math.is_finite(min_increment).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.NONFINITE_VALUE,
                {"min_increment": min_increment},
            )
        if bool((min_increment < -self.cdf_config.monotonicity_tolerance).numpy()):
            return (
                tf.constant(float("nan"), dtype=tf.float64),
                tf.constant(float("nan"), dtype=tf.float64),
                HighDimStatus.CDF_MONOTONICITY_FAILURE,
                {"min_increment": min_increment},
            )
        z_scalar = tf.reshape(z_value, [])
        cdf_value = _interp_1d(z_scalar, grid, cdf_grid)
        density_value = _interp_1d(z_scalar, grid, conditional)
        return cdf_value, density_value, HighDimStatus.OK, {"min_increment": min_increment}

    def _inverse_axis(self, axis: int, prefix: tf.Tensor, target_u: tf.Tensor):
        target = tf.reshape(tf.convert_to_tensor(target_u, dtype=tf.float64), [])
        if not bool(tf.math.is_finite(target).numpy()):
            result = KRInversionResult(
                z_value=tf.constant(float("nan"), dtype=tf.float64),
                cdf_value=target,
                iterations=0,
                status=HighDimStatus.NONFINITE_VALUE,
                diagnostics={"target": target},
            )
            return result, tf.constant(float("nan"), dtype=tf.float64)
        if bool((target < -self.cdf_config.bracket_tolerance).numpy()) or bool(
            (target > 1.0 + self.cdf_config.bracket_tolerance).numpy()
        ):
            result = KRInversionResult(
                z_value=tf.constant(float("nan"), dtype=tf.float64),
                cdf_value=target,
                iterations=0,
                status=HighDimStatus.INVERSE_BRACKET_FAILURE,
                diagnostics={"target": target},
            )
            return result, tf.constant(float("nan"), dtype=tf.float64)
        grid = self._axis_grid(axis)
        lo = tf.reshape(grid[0], [])
        hi = tf.reshape(grid[-1], [])
        mid = 0.5 * (lo + hi)
        cdf_mid = tf.constant(float("nan"), dtype=tf.float64)
        density_mid = tf.constant(float("nan"), dtype=tf.float64)
        status = HighDimStatus.OK
        diagnostics = {}
        for _ in range(self.cdf_config.bisection_steps):
            mid = 0.5 * (lo + hi)
            cdf_mid, density_mid, status, diagnostics = self._cdf_at(
                axis,
                prefix,
                tf.reshape(mid, [1]),
            )
            if status is not HighDimStatus.OK:
                break
            if bool((cdf_mid < target).numpy()):
                lo = mid
            else:
                hi = mid
        return (
            KRInversionResult(
                z_value=mid,
                cdf_value=cdf_mid,
                iterations=self.cdf_config.bisection_steps,
                status=status,
                diagnostics=diagnostics,
            ),
            density_mid,
        )


def _interp_1d(x: tf.Tensor, grid: tf.Tensor, values: tf.Tensor) -> tf.Tensor:
    clipped = tf.clip_by_value(x, grid[0], grid[-1])
    right = tf.searchsorted(grid, tf.reshape(clipped, [1]), side="right")[0]
    right = tf.clip_by_value(right, 1, tf.shape(grid)[0] - 1)
    left = right - 1
    x0 = tf.gather(grid, left)
    x1 = tf.gather(grid, right)
    y0 = tf.gather(values, left)
    y1 = tf.gather(values, right)
    weight = (clipped - x0) / (x1 - x0)
    return y0 + weight * (y1 - y0)
