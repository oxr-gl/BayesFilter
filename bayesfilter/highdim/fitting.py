"""Deterministic fixed-branch TT fitting for Phase-3 highdim contracts."""

from __future__ import annotations

from dataclasses import dataclass
import math
from types import MappingProxyType
from typing import Mapping, Sequence

import tensorflow as tf

from bayesfilter.highdim.bases import ProductBasis
from bayesfilter.highdim.diagnostics import (
    HighDimStatus,
    MeasureConvention,
    assert_density_matches_mass,
    assert_tf_float64,
    freeze_mapping,
)
from bayesfilter.highdim.fixed_branch import BranchHash, BranchIdentity, BranchManifest
from bayesfilter.highdim.tt import FunctionalTT, TTCore
from bayesfilter.highdim.validation import ComplexityBudget


@dataclass(frozen=True)
class FixedTTFitConfig:
    """Declared fixed-rank weighted ridge ALS configuration."""

    ranks: tuple[int, ...]
    ridge: float
    max_sweeps: int
    sweep_order: tuple[int, ...]
    row_budget: int
    column_budget: int
    dense_matrix_byte_budget: int
    normal_matrix_byte_budget: int
    condition_number_warning: float
    condition_number_veto: float
    holdout_tolerance: float
    dtype: tf.DType = tf.float64

    def __post_init__(self) -> None:
        object.__setattr__(self, "ranks", tuple(int(rank) for rank in self.ranks))
        object.__setattr__(
            self,
            "sweep_order",
            tuple(int(axis) for axis in self.sweep_order),
        )
        if self.dtype != tf.float64:
            raise ValueError("FixedTTFitConfig requires tf.float64")
        if len(self.ranks) < 2 or any(rank <= 0 for rank in self.ranks):
            raise ValueError(f"ranks: {HighDimStatus.INVALID_SHAPE.value}")
        if self.ranks[0] != 1 or self.ranks[-1] != 1:
            raise ValueError(f"ranks: {HighDimStatus.INVALID_SHAPE.value}")
        if not self.sweep_order:
            raise ValueError("sweep_order must be nonempty")
        if self.max_sweeps <= 0:
            raise ValueError("max_sweeps must be positive")
        for name in (
            "row_budget",
            "column_budget",
            "dense_matrix_byte_budget",
            "normal_matrix_byte_budget",
        ):
            if int(getattr(self, name)) <= 0:
                raise ValueError(f"{name} must be positive")
        for name in (
            "ridge",
            "condition_number_warning",
            "condition_number_veto",
            "holdout_tolerance",
        ):
            value = float(getattr(self, name))
            if not math.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if value < 0.0:
                raise ValueError(f"{name} must be nonnegative")
        if self.condition_number_warning <= 0.0 or self.condition_number_veto <= 0.0:
            raise ValueError("condition-number thresholds must be positive")


@dataclass(frozen=True)
class FixedTTFitSampleBatch:
    """Weighted sample batch for fixed-design TT fitting."""

    points: tf.Tensor
    target_values: tf.Tensor
    weights: tf.Tensor
    holdout_points: tf.Tensor | None = None
    holdout_values: tf.Tensor | None = None
    holdout_weights: tf.Tensor | None = None

    def __post_init__(self) -> None:
        points = tf.convert_to_tensor(self.points, dtype=tf.float64)
        targets = tf.convert_to_tensor(self.target_values, dtype=tf.float64)
        weights = tf.convert_to_tensor(self.weights, dtype=tf.float64)
        _validate_sample_tensors("samples", points, targets, weights)
        object.__setattr__(self, "points", points)
        object.__setattr__(self, "target_values", targets)
        object.__setattr__(self, "weights", weights)
        if self.holdout_points is None:
            if self.holdout_values is not None or self.holdout_weights is not None:
                raise ValueError(f"holdout: {HighDimStatus.INVALID_SHAPE.value}")
            object.__setattr__(self, "holdout_values", None)
            object.__setattr__(self, "holdout_weights", None)
            return
        if self.holdout_values is None:
            raise ValueError(f"holdout_values: {HighDimStatus.INVALID_SHAPE.value}")
        holdout_points = tf.convert_to_tensor(self.holdout_points, dtype=tf.float64)
        holdout_values = tf.convert_to_tensor(self.holdout_values, dtype=tf.float64)
        holdout_weights = (
            tf.ones_like(holdout_values, dtype=tf.float64)
            if self.holdout_weights is None
            else tf.convert_to_tensor(self.holdout_weights, dtype=tf.float64)
        )
        _validate_sample_tensors(
            "holdout",
            holdout_points,
            holdout_values,
            holdout_weights,
        )
        object.__setattr__(self, "holdout_points", holdout_points)
        object.__setattr__(self, "holdout_values", holdout_values)
        object.__setattr__(self, "holdout_weights", holdout_weights)


@dataclass(frozen=True)
class FixedTTFitResult:
    """Result of one deterministic fixed-branch TT fit."""

    fitted_tt: FunctionalTT
    status: HighDimStatus
    termination_reason: str
    stop_condition_triggered: str
    fit_residual: tf.Tensor | None
    holdout_residual: tf.Tensor | None
    branch_identity: BranchIdentity
    core_update_statuses: tuple[Mapping[str, object], ...]
    diagnostics: Mapping[str, object] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.fitted_tt, FunctionalTT):
            raise TypeError("fitted_tt must be a FunctionalTT")
        if not isinstance(self.status, HighDimStatus):
            raise TypeError("status must be a HighDimStatus")
        if not isinstance(self.branch_identity, BranchIdentity):
            raise TypeError("branch_identity must be a BranchIdentity")
        for name in ("termination_reason", "stop_condition_triggered"):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be nonempty")
        for name in ("fit_residual", "holdout_residual"):
            value = getattr(self, name)
            if value is not None:
                tensor = tf.convert_to_tensor(value, dtype=tf.float64)
                if tensor.shape.rank != 0:
                    raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
                object.__setattr__(self, name, tensor)
        object.__setattr__(
            self,
            "core_update_statuses",
            tuple(MappingProxyType(dict(record)) for record in self.core_update_statuses),
        )
        object.__setattr__(self, "diagnostics", freeze_mapping(self.diagnostics))

    @property
    def branch_hash(self) -> BranchHash:
        """Full realized branch hash."""

        return self.branch_identity.hash


@dataclass(frozen=True)
class _CoreUpdateSystem:
    design_matrix: tf.Tensor
    normal_matrix: tf.Tensor
    rhs: tf.Tensor
    condition_number: float
    diagnostics: Mapping[str, object]


class FixedTTFitter:
    """Fixed-rank weighted ridge ALS fitter with replayable branch manifests."""

    def fit(
        self,
        product_basis: ProductBasis,
        samples: FixedTTFitSampleBatch,
        config: FixedTTFitConfig,
        initial_cores: Sequence[TTCore | tf.Tensor],
        branch_seed: int | str,
        measure_convention: MeasureConvention,
    ) -> FixedTTFitResult:
        if not isinstance(product_basis, ProductBasis):
            raise TypeError("product_basis must be a ProductBasis")
        if not isinstance(samples, FixedTTFitSampleBatch):
            raise TypeError("samples must be a FixedTTFitSampleBatch")
        if not isinstance(config, FixedTTFitConfig):
            raise TypeError("config must be a FixedTTFitConfig")
        if measure_convention != product_basis.convention:
            raise ValueError(f"measure_convention: {HighDimStatus.MEASURE_MISMATCH.value}")
        assert_density_matches_mass(measure_convention)
        self._validate_config_for_basis(product_basis, config)
        self._validate_batch_dimension(product_basis, samples)
        cores = list(
            self._validate_initial_cores(
                product_basis,
                measure_convention,
                config,
                initial_cores,
            )
        )
        initial_core_hash = _hash_tensors("initial_cores_hash.v1", [core.values for core in cores])
        update_records: list[Mapping[str, object]] = []
        environment_rebuild_hashes: list[str] = []
        status = HighDimStatus.OK
        termination_reason = "max_sweeps_exhausted"
        stop_condition = "max_sweeps_exhausted"

        for sweep_index in range(config.max_sweeps):
            for axis in config.sweep_order:
                pre_hash = _hash_tensors("pre_update_cores_hash.v1", [core.values for core in cores])
                environment_rebuild_hashes.append(pre_hash)
                updated_core, record = self._fit_core_update(
                    product_basis=product_basis,
                    points=samples.points,
                    target_values=samples.target_values,
                    weights=samples.weights,
                    cores=tuple(cores),
                    core_index=axis,
                    config=config,
                    sweep_index=sweep_index,
                )
                update_records.append(record)
                record_status = HighDimStatus(str(record["status"]))
                if record_status is not HighDimStatus.OK:
                    status = record_status
                    termination_reason = str(record["termination_reason"])
                    stop_condition = str(record["stop_condition_triggered"])
                    return self._finalize_result(
                        product_basis=product_basis,
                        samples=samples,
                        config=config,
                        cores=tuple(cores),
                        branch_seed=branch_seed,
                        measure_convention=measure_convention,
                        initial_core_hash=initial_core_hash,
                        update_records=tuple(update_records),
                        environment_rebuild_hashes=tuple(environment_rebuild_hashes),
                        status=status,
                        termination_reason=termination_reason,
                        stop_condition=stop_condition,
                        fit_residual=None,
                        holdout_residual=None,
                    )
                cores[axis] = updated_core

        fitted_tt_without_identity = FunctionalTT(
            cores,
            product_basis,
            measure_convention,
            complexity_budget=_evaluation_budget_from_fit_config(config),
        )
        fit_residual = _weighted_rms_residual(
            fitted_tt_without_identity.evaluate(samples.points),
            samples.target_values,
            samples.weights,
        )
        if not bool(tf.math.is_finite(fit_residual).numpy()):
            status = HighDimStatus.NONFINITE_VALUE
            termination_reason = "nonfinite_fit_residual"
            stop_condition = HighDimStatus.NONFINITE_VALUE.value
        holdout_residual = None
        if status is HighDimStatus.OK and samples.holdout_points is not None:
            holdout_residual = _weighted_rms_residual(
                fitted_tt_without_identity.evaluate(samples.holdout_points),
                samples.holdout_values,
                samples.holdout_weights,
            )
            if not bool(tf.math.is_finite(holdout_residual).numpy()):
                status = HighDimStatus.NONFINITE_VALUE
                termination_reason = "nonfinite_holdout_residual"
                stop_condition = HighDimStatus.NONFINITE_VALUE.value
            elif bool((holdout_residual > config.holdout_tolerance).numpy()):
                status = HighDimStatus.HOLDOUT_RESIDUAL_VETO
                termination_reason = "holdout_residual_veto"
                stop_condition = HighDimStatus.HOLDOUT_RESIDUAL_VETO.value
        return self._finalize_result(
            product_basis=product_basis,
            samples=samples,
            config=config,
            cores=tuple(cores),
            branch_seed=branch_seed,
            measure_convention=measure_convention,
            initial_core_hash=initial_core_hash,
            update_records=tuple(update_records),
            environment_rebuild_hashes=tuple(environment_rebuild_hashes),
            status=status,
            termination_reason=termination_reason,
            stop_condition=stop_condition,
            fit_residual=fit_residual,
            holdout_residual=holdout_residual,
        )

    def build_core_update_system(
        self,
        product_basis: ProductBasis,
        points: tf.Tensor,
        target_values: tf.Tensor,
        weights: tf.Tensor,
        cores: Sequence[TTCore],
        core_index: int,
        config: FixedTTFitConfig,
    ) -> _CoreUpdateSystem:
        """Build the declared core-design system for direct reference tests."""

        points = tf.convert_to_tensor(points, dtype=tf.float64)
        target_values = tf.convert_to_tensor(target_values, dtype=tf.float64)
        weights = tf.convert_to_tensor(weights, dtype=tf.float64)
        self._validate_batch_dimension(
            product_basis,
            FixedTTFitSampleBatch(points, target_values, weights),
        )
        checked_cores = self._validate_initial_cores(
            product_basis,
            product_basis.convention,
            config,
            cores,
        )
        gate = self._check_design_budget(product_basis, points, checked_cores, core_index, config)
        if gate["status"] != HighDimStatus.OK.value:
            raise ValueError(HighDimStatus.COMPLEXITY_GATE.value)
        design = self._build_design_matrix(product_basis, points, checked_cores, core_index)
        normal, rhs = _normal_equations(design, target_values, weights, config.ridge)
        condition_number = _condition_number(normal)
        return _CoreUpdateSystem(
            design_matrix=design,
            normal_matrix=normal,
            rhs=rhs,
            condition_number=condition_number,
            diagnostics={
                **gate,
                "condition_number": _finite_number_or_text(condition_number),
            },
        )

    def _fit_core_update(
        self,
        product_basis: ProductBasis,
        points: tf.Tensor,
        target_values: tf.Tensor,
        weights: tf.Tensor,
        cores: tuple[TTCore, ...],
        core_index: int,
        config: FixedTTFitConfig,
        sweep_index: int,
    ) -> tuple[TTCore, Mapping[str, object]]:
        gate = self._check_design_budget(product_basis, points, cores, core_index, config)
        if gate["status"] != HighDimStatus.OK.value:
            gate_status = HighDimStatus(str(gate["status"]))
            return cores[core_index], {
                **gate,
                "core_index": core_index,
                "sweep_index": sweep_index,
                "termination_reason": str(gate["gate"]),
                "stop_condition_triggered": gate_status.value,
            }
        design = self._build_design_matrix(product_basis, points, cores, core_index)
        if not bool(tf.reduce_all(tf.math.is_finite(design)).numpy()):
            return cores[core_index], _failed_update_record(
                status=HighDimStatus.NONFINITE_VALUE,
                core_index=core_index,
                sweep_index=sweep_index,
                termination_reason="nonfinite_design_matrix",
            )
        normal, rhs = _normal_equations(design, target_values, weights, config.ridge)
        if not bool(
            tf.reduce_all(tf.math.is_finite(normal)).numpy()
            and tf.reduce_all(tf.math.is_finite(rhs)).numpy()
        ):
            return cores[core_index], _failed_update_record(
                status=HighDimStatus.NONFINITE_VALUE,
                core_index=core_index,
                sweep_index=sweep_index,
                termination_reason="nonfinite_normal_equations",
            )
        condition_number = _condition_number(normal)
        condition_record = {
            "condition_number": _finite_number_or_text(condition_number),
            "condition_warning": bool(condition_number > config.condition_number_warning),
            "condition_number_warning": float(config.condition_number_warning),
            "condition_number_veto": float(config.condition_number_veto),
        }
        if (not math.isfinite(condition_number)) or condition_number > config.condition_number_veto:
            return cores[core_index], {
                **gate,
                **condition_record,
                "status": HighDimStatus.CONDITION_NUMBER_VETO.value,
                "core_index": core_index,
                "sweep_index": sweep_index,
                "termination_reason": "condition_number_veto",
                "stop_condition_triggered": HighDimStatus.CONDITION_NUMBER_VETO.value,
            }
        try:
            solution = tf.linalg.solve(normal, tf.reshape(rhs, [-1, 1]))[:, 0]
        except Exception:
            return cores[core_index], {
                **gate,
                **condition_record,
                "status": HighDimStatus.CONDITION_NUMBER_VETO.value,
                "core_index": core_index,
                "sweep_index": sweep_index,
                "termination_reason": "solve_failure",
                "stop_condition_triggered": HighDimStatus.CONDITION_NUMBER_VETO.value,
            }
        if not bool(tf.reduce_all(tf.math.is_finite(solution)).numpy()):
            return cores[core_index], _failed_update_record(
                status=HighDimStatus.NONFINITE_VALUE,
                core_index=core_index,
                sweep_index=sweep_index,
                termination_reason="nonfinite_solution",
            )
        old_core = cores[core_index]
        new_values = tf.reshape(
            solution,
            [old_core.left_rank, old_core.basis_dim, old_core.right_rank],
        )
        return TTCore(new_values), {
            **gate,
            **condition_record,
            "status": HighDimStatus.OK.value,
            "core_index": core_index,
            "sweep_index": sweep_index,
            "termination_reason": "core_update_accepted",
            "stop_condition_triggered": "none",
            "solver_backend": "tensorflow.linalg.solve",
        }

    def _build_design_matrix(
        self,
        product_basis: ProductBasis,
        points: tf.Tensor,
        cores: Sequence[TTCore],
        core_index: int,
    ) -> tf.Tensor:
        matrices = _core_matrices(product_basis, points, cores)
        left = _left_environments(matrices)[core_index]
        right = _right_environments(matrices)[core_index]
        basis_values = product_basis.evaluate_axis(core_index, points[:, core_index])
        blocks = tf.einsum("na,nl,nb->nalb", left, basis_values, right)
        return tf.reshape(
            blocks,
            [
                int(points.shape[0]),
                cores[core_index].left_rank
                * cores[core_index].basis_dim
                * cores[core_index].right_rank,
            ],
        )

    def _check_design_budget(
        self,
        product_basis: ProductBasis,
        points: tf.Tensor,
        cores: Sequence[TTCore],
        core_index: int,
        config: FixedTTFitConfig,
    ) -> Mapping[str, object]:
        if points.shape.rank != 2 or points.shape[0] is None:
            return {
                "status": HighDimStatus.INVALID_SHAPE.value,
                "gate": "points_shape",
                "message": "static row count is required",
            }
        n_rows = int(points.shape[0])
        core = cores[core_index]
        n_cols = core.left_rank * product_basis.bases[core_index].basis_dim * core.right_rank
        dtype_size = tf.float64.size
        dense_bytes = n_rows * n_cols * dtype_size
        normal_matrix_bytes = n_cols * n_cols * dtype_size
        common = {
            "n_rows": n_rows,
            "n_cols": n_cols,
            "dense_matrix_bytes": dense_bytes,
            "normal_matrix_bytes": normal_matrix_bytes,
            "row_budget": int(config.row_budget),
            "column_budget": int(config.column_budget),
            "dense_matrix_byte_budget": int(config.dense_matrix_byte_budget),
            "normal_matrix_byte_budget": int(config.normal_matrix_byte_budget),
        }
        if n_rows > config.row_budget:
            return {
                **common,
                "status": HighDimStatus.COMPLEXITY_GATE.value,
                "gate": "row_budget",
            }
        if n_cols > config.column_budget:
            return {
                **common,
                "status": HighDimStatus.COMPLEXITY_GATE.value,
                "gate": "column_budget",
            }
        if dense_bytes > config.dense_matrix_byte_budget:
            return {
                **common,
                "status": HighDimStatus.COMPLEXITY_GATE.value,
                "gate": "dense_matrix_byte_budget",
            }
        if normal_matrix_bytes > config.normal_matrix_byte_budget:
            return {
                **common,
                "status": HighDimStatus.COMPLEXITY_GATE.value,
                "gate": "normal_matrix_byte_budget",
            }
        return {**common, "status": HighDimStatus.OK.value, "gate": "ok"}

    def _validate_config_for_basis(
        self,
        product_basis: ProductBasis,
        config: FixedTTFitConfig,
    ) -> None:
        if len(config.ranks) != product_basis.dimension + 1:
            raise ValueError(f"ranks: {HighDimStatus.INVALID_SHAPE.value}")
        if sorted(config.sweep_order) != list(range(product_basis.dimension)):
            raise ValueError(f"sweep_order: {HighDimStatus.INVALID_SHAPE.value}")

    def _validate_batch_dimension(
        self,
        product_basis: ProductBasis,
        samples: FixedTTFitSampleBatch,
    ) -> None:
        if samples.points.shape[1] != product_basis.dimension:
            raise ValueError(f"points: {HighDimStatus.INVALID_SHAPE.value}")
        if samples.holdout_points is not None and samples.holdout_points.shape[1] != product_basis.dimension:
            raise ValueError(f"holdout_points: {HighDimStatus.INVALID_SHAPE.value}")

    def _validate_initial_cores(
        self,
        product_basis: ProductBasis,
        measure_convention: MeasureConvention,
        config: FixedTTFitConfig,
        initial_cores: Sequence[TTCore | tf.Tensor],
    ) -> tuple[TTCore, ...]:
        cores = tuple(core if isinstance(core, TTCore) else TTCore(core) for core in initial_cores)
        ftt = FunctionalTT(cores, product_basis, measure_convention)
        if ftt.rank_tuple() != config.ranks:
            raise ValueError(f"initial_cores: {HighDimStatus.INVALID_SHAPE.value}")
        return cores

    def _finalize_result(
        self,
        product_basis: ProductBasis,
        samples: FixedTTFitSampleBatch,
        config: FixedTTFitConfig,
        cores: tuple[TTCore, ...],
        branch_seed: int | str,
        measure_convention: MeasureConvention,
        initial_core_hash: str,
        update_records: tuple[Mapping[str, object], ...],
        environment_rebuild_hashes: tuple[str, ...],
        status: HighDimStatus,
        termination_reason: str,
        stop_condition: str,
        fit_residual: tf.Tensor | None,
        holdout_residual: tf.Tensor | None,
    ) -> FixedTTFitResult:
        manifest = BranchManifest(
            version="fixed_tt_fit.v1",
            payload={
                "family": "FixedTTFitter",
                "scope": "fixed_branch_weighted_ridge_als_only",
                "product_basis": _product_basis_payload(product_basis),
                "measure_convention": _measure_convention_payload(measure_convention),
                "samples": _sample_payload(samples),
                "sample_hashes": _sample_hashes(samples),
                "ranks": config.ranks,
                "ridge": float(config.ridge),
                "dtype": config.dtype.name,
                "sweep_order": config.sweep_order,
                "coordinate_order": tuple(range(product_basis.dimension)),
                "max_sweeps": int(config.max_sweeps),
                "initial_core_hash": initial_core_hash,
                "initialization_rule": "supplied_initial_cores",
                "fitted_cores": tuple(core.values for core in cores),
                "per_core_update_statuses": tuple(dict(record) for record in update_records),
                "environment_rebuild_hashes": environment_rebuild_hashes,
                "stabilization_choices": {"ridge": float(config.ridge)},
                "complexity_budgets": _config_budget_payload(config),
                "solver_backend": "tensorflow.linalg.solve",
                "deterministic_seed": branch_seed,
                "status": status.value,
                "termination_reason": termination_reason,
                "stop_condition_triggered": stop_condition,
                "fit_residual": fit_residual,
                "holdout_residual": holdout_residual,
                "what_is_not_claimed": (
                    "adaptive_tt_cross",
                    "rank_adaptation",
                    "filtering",
                    "derivative_correctness",
                ),
            },
        )
        branch_identity = BranchIdentity(manifest=manifest, hash=manifest.sha256())
        fitted_tt = FunctionalTT(
            cores,
            product_basis,
            measure_convention,
            complexity_budget=_evaluation_budget_from_fit_config(config),
            branch_identity=branch_identity,
        )
        diagnostics = {
            "status": status.value,
            "termination_reason": termination_reason,
            "stop_condition_triggered": stop_condition,
            "rank_tuple": config.ranks,
            "ridge": float(config.ridge),
            "sweep_count": int(config.max_sweeps),
            "sweep_order": config.sweep_order,
            "coordinate_order": tuple(range(product_basis.dimension)),
            "coordinate_order_sensitivity_reported": True,
            "environment_rebuild_count": len(environment_rebuild_hashes),
            "environment_rebuild_hashes": environment_rebuild_hashes,
            "branch_hash": branch_identity.hash.value,
            "fit_residual": fit_residual,
            "holdout_residual": holdout_residual,
            "fixed_branch_only": True,
        }
        return FixedTTFitResult(
            fitted_tt=fitted_tt,
            status=status,
            termination_reason=termination_reason,
            stop_condition_triggered=stop_condition,
            fit_residual=fit_residual,
            holdout_residual=holdout_residual,
            branch_identity=branch_identity,
            core_update_statuses=update_records,
            diagnostics=diagnostics,
        )


def _validate_sample_tensors(
    name: str,
    points: tf.Tensor,
    targets: tf.Tensor,
    weights: tf.Tensor,
) -> None:
    assert_tf_float64(f"{name}.points", points)
    assert_tf_float64(f"{name}.target_values", targets)
    assert_tf_float64(f"{name}.weights", weights)
    if points.shape.rank != 2 or targets.shape.rank != 1 or weights.shape.rank != 1:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if points.shape[0] is None or targets.shape[0] is None or weights.shape[0] is None:
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if int(points.shape[0]) != int(targets.shape[0]) or int(points.shape[0]) != int(weights.shape[0]):
        raise ValueError(f"{name}: {HighDimStatus.INVALID_SHAPE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(points)).numpy()):
        raise ValueError(f"{name}.points: {HighDimStatus.NONFINITE_VALUE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(targets)).numpy()):
        raise ValueError(f"{name}.target_values: {HighDimStatus.NONFINITE_VALUE.value}")
    if not bool(tf.reduce_all(tf.math.is_finite(weights)).numpy()):
        raise ValueError(f"{name}.weights: {HighDimStatus.NONFINITE_VALUE.value}")
    if bool(tf.reduce_any(weights < 0.0).numpy()):
        raise ValueError(f"{name}.weights: {HighDimStatus.NONFINITE_VALUE.value}")
    if bool((tf.reduce_sum(weights) <= 0.0).numpy()):
        raise ValueError(f"{name}.weights: {HighDimStatus.NONFINITE_VALUE.value}")


def _core_matrices(
    product_basis: ProductBasis,
    points: tf.Tensor,
    cores: Sequence[TTCore],
) -> tuple[tf.Tensor, ...]:
    matrices = []
    for axis, core in enumerate(cores):
        basis_values = product_basis.evaluate_axis(axis, points[:, axis])
        matrices.append(tf.einsum("nl,alb->nab", basis_values, core.values))
    return tuple(matrices)


def _left_environments(matrices: Sequence[tf.Tensor]) -> tuple[tf.Tensor, ...]:
    n_rows = tf.shape(matrices[0])[0]
    environments = [tf.ones([n_rows, 1], dtype=tf.float64)]
    for matrix in matrices[:-1]:
        environments.append(tf.einsum("na,nab->nb", environments[-1], matrix))
    return tuple(environments)


def _right_environments(matrices: Sequence[tf.Tensor]) -> tuple[tf.Tensor, ...]:
    n_rows = tf.shape(matrices[0])[0]
    environments = [None] * len(matrices)
    accumulator = tf.ones([n_rows, 1], dtype=tf.float64)
    for axis in range(len(matrices) - 1, -1, -1):
        environments[axis] = accumulator
        if axis > 0:
            accumulator = tf.einsum("nab,nb->na", matrices[axis], accumulator)
    return tuple(environments)


def _normal_equations(
    design: tf.Tensor,
    target_values: tf.Tensor,
    weights: tf.Tensor,
    ridge: float,
) -> tuple[tf.Tensor, tf.Tensor]:
    weighted_design = design * tf.reshape(weights, [-1, 1])
    normal = tf.matmul(design, weighted_design, transpose_a=True)
    normal = normal + tf.cast(ridge, tf.float64) * tf.eye(
        int(design.shape[1]),
        dtype=tf.float64,
    )
    rhs = tf.linalg.matvec(design, weights * target_values, transpose_a=True)
    return normal, rhs


def _condition_number(matrix: tf.Tensor) -> float:
    singular_values = tf.linalg.svd(matrix, compute_uv=False)
    min_value = float(tf.reduce_min(singular_values).numpy())
    max_value = float(tf.reduce_max(singular_values).numpy())
    if min_value <= 0.0 or not math.isfinite(min_value) or not math.isfinite(max_value):
        return float("inf")
    return max_value / min_value


def _weighted_rms_residual(
    predicted: tf.Tensor,
    target: tf.Tensor,
    weights: tf.Tensor,
) -> tf.Tensor:
    denominator = tf.reduce_sum(weights)
    residual = predicted - target
    return tf.sqrt(tf.reduce_sum(weights * tf.square(residual)) / denominator)


def _failed_update_record(
    status: HighDimStatus,
    core_index: int,
    sweep_index: int,
    termination_reason: str,
) -> Mapping[str, object]:
    return {
        "status": status.value,
        "core_index": core_index,
        "sweep_index": sweep_index,
        "termination_reason": termination_reason,
        "stop_condition_triggered": status.value,
    }


def _evaluation_budget_from_fit_config(config: FixedTTFitConfig) -> ComplexityBudget:
    max_bytes = max(
        int(config.dense_matrix_byte_budget),
        int(config.normal_matrix_byte_budget),
        tf.float64.size,
    )
    return ComplexityBudget(max_elements=max_bytes // tf.float64.size, max_bytes=max_bytes)


def _measure_convention_payload(convention: MeasureConvention) -> Mapping[str, object]:
    return {
        "density_measure": convention.density_measure.value,
        "mass_measure": convention.mass_measure.value,
        "reference_weight_name": convention.reference_weight_name,
        "physical_coordinate_name": convention.physical_coordinate_name,
        "reference_coordinate_name": convention.reference_coordinate_name,
        "dtype_name": convention.dtype_name,
    }


def _basis_payload(basis) -> Mapping[str, object]:
    return {
        "family": "LegendreBasis1D",
        "left": basis.domain.left,
        "right": basis.domain.right,
        "dtype": basis.dtype.name,
        "reference_measure": "UniformReferenceMeasure",
        "max_degree": int(basis.max_degree),
        "normalized": bool(basis.normalized),
    }


def _product_basis_payload(product_basis: ProductBasis) -> Mapping[str, object]:
    return {
        "family": "ProductBasis",
        "dimension": int(product_basis.dimension),
        "basis_dim_tuple": product_basis.basis_dim_tuple(),
        "convention": _measure_convention_payload(product_basis.convention),
        "bases": tuple(_basis_payload(basis) for basis in product_basis.bases),
    }


def _sample_payload(samples: FixedTTFitSampleBatch) -> Mapping[str, object]:
    return {
        "points": samples.points,
        "target_values": samples.target_values,
        "weights": samples.weights,
        "holdout_points": samples.holdout_points,
        "holdout_values": samples.holdout_values,
        "holdout_weights": samples.holdout_weights,
    }


def _sample_hashes(samples: FixedTTFitSampleBatch) -> Mapping[str, object]:
    return {
        "sample_points_hash": _hash_tensor_or_none("sample_points_hash.v1", samples.points),
        "target_values_hash": _hash_tensor_or_none("target_values_hash.v1", samples.target_values),
        "weights_hash": _hash_tensor_or_none("weights_hash.v1", samples.weights),
        "holdout_hash": BranchManifest(
            version="holdout_hash.v1",
            payload={
                "points": samples.holdout_points,
                "values": samples.holdout_values,
                "weights": samples.holdout_weights,
            },
        ).sha256().value,
    }


def _config_budget_payload(config: FixedTTFitConfig) -> Mapping[str, object]:
    return {
        "row_budget": int(config.row_budget),
        "column_budget": int(config.column_budget),
        "dense_matrix_byte_budget": int(config.dense_matrix_byte_budget),
        "normal_matrix_byte_budget": int(config.normal_matrix_byte_budget),
    }


def _hash_tensor_or_none(version: str, value: tf.Tensor | None) -> str | None:
    if value is None:
        return None
    return BranchManifest(version=version, payload={"value": value}).sha256().value


def _hash_tensors(version: str, tensors: Sequence[tf.Tensor]) -> str:
    return BranchManifest(version=version, payload={"tensors": tuple(tensors)}).sha256().value


def _finite_number_or_text(value: float) -> float | str:
    return float(value) if math.isfinite(value) else "inf"
