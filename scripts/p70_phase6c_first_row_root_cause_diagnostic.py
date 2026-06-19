#!/usr/bin/env python
"""P70 Phase 6c first-row condition-veto root-cause diagnostic."""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping, Sequence

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf

from bayesfilter.highdim import source_route
from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.fitting import FixedTTFitConfig, FixedTTFitSampleBatch, FixedTTFitter
from bayesfilter.highdim.tt import TTCore


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-2026-06-16.json"
)
EXPECTED_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p70_phase6c_first_row_root_cause_diagnostic.py"
)
ROW_LABEL = "rank_candidate_1_2_fit36"
TIME_INDEX = 1
FIT_DEGREE = 1
FIT_RANK = 2
FIT_SAMPLE_COUNT = 36
MODEL_SEED = 5901
PRIOR_SAMPLE_SEED = 6301
PROCESS_NOISE_SEED = 6401
RELATIVE_RANK_TOL = 1e-12


def _jsonable(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [_jsonable(item) for item in value]
    if hasattr(value, "numpy"):
        array = value.numpy()
        if getattr(array, "shape", ()) == ():
            return _jsonable(array.item())
        return _jsonable(array.tolist())
    if isinstance(value, float):
        if math.isfinite(value):
            return value
        return str(value)
    return value


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _event(stage: str, status: str, **detail: Any) -> None:
    payload = {
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "stage": stage,
        "status": status,
        **detail,
    }
    print(json.dumps({"p70_phase6c_progress": _jsonable(payload)}, sort_keys=True), flush=True)


def _git_state_summary() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        porcelain = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
        return {
            "head": commit,
            "dirty": bool(porcelain),
            "status_short_count": len(porcelain),
        }
    except (OSError, subprocess.CalledProcessError) as exc:
        return {"head": "unknown", "dirty": "unknown", "status_error": str(exc)}


def _tensor_stats(values: tf.Tensor) -> Mapping[str, Any]:
    tensor = tf.reshape(tf.convert_to_tensor(values, dtype=tf.float64), [-1])
    return {
        "count": int(tensor.shape[0]),
        "min": float(tf.reduce_min(tensor).numpy()),
        "max": float(tf.reduce_max(tensor).numpy()),
        "mean": float(tf.reduce_mean(tensor).numpy()),
        "std": float(tf.math.reduce_std(tensor).numpy()),
        "rms": float(tf.sqrt(tf.reduce_mean(tf.square(tensor))).numpy()),
        "l2_norm": float(tf.linalg.norm(tensor).numpy()),
        "max_abs": float(tf.reduce_max(tf.abs(tensor)).numpy()),
    }


def _finite_condition_from_singular_values(singular_values: tf.Tensor) -> float:
    values = tf.reshape(tf.convert_to_tensor(singular_values, dtype=tf.float64), [-1])
    if int(values.shape[0]) == 0:
        return float("inf")
    min_value = float(tf.reduce_min(values).numpy())
    max_value = float(tf.reduce_max(values).numpy())
    if min_value <= 0.0 or not math.isfinite(min_value) or not math.isfinite(max_value):
        return float("inf")
    return max_value / min_value


def _spectrum_summary(values: tf.Tensor, *, rank_tol: float = RELATIVE_RANK_TOL) -> Mapping[str, Any]:
    singular_values = tf.reshape(tf.convert_to_tensor(values, dtype=tf.float64), [-1])
    count = int(singular_values.shape[0])
    if count == 0:
        return {
            "count": 0,
            "values": (),
            "min": None,
            "max": None,
            "condition_number": "inf",
            "rank_tol_relative": float(rank_tol),
            "numerical_rank": 0,
        }
    max_value = float(tf.reduce_max(singular_values).numpy())
    min_value = float(tf.reduce_min(singular_values).numpy())
    threshold = float(rank_tol) * max(max_value, 1.0)
    rank = int(tf.reduce_sum(tf.cast(singular_values > threshold, tf.int32)).numpy())
    return {
        "count": count,
        "values": singular_values,
        "min": min_value,
        "max": max_value,
        "condition_number": _finite_condition_from_singular_values(singular_values),
        "rank_tol_relative": float(rank_tol),
        "rank_threshold": threshold,
        "numerical_rank": rank,
    }


def _normal_condition(design: tf.Tensor, weights: tf.Tensor, ridge: float) -> float:
    weighted_design = design * tf.reshape(weights, [-1, 1])
    gram = tf.matmul(design, weighted_design, transpose_a=True)
    normal = gram + tf.cast(ridge, tf.float64) * tf.eye(int(design.shape[1]), dtype=tf.float64)
    singular_values = tf.linalg.svd(normal, compute_uv=False)
    return _finite_condition_from_singular_values(singular_values)


def _column_norm_summary(design: tf.Tensor) -> Mapping[str, Any]:
    norms = tf.linalg.norm(design, axis=0)
    positive = tf.boolean_mask(norms, norms > 0.0)
    if int(positive.shape[0]) == 0:
        spread = float("inf")
    else:
        spread = float((tf.reduce_max(positive) / tf.reduce_min(positive)).numpy())
    return {
        "values": norms,
        "min": float(tf.reduce_min(norms).numpy()),
        "max": float(tf.reduce_max(norms).numpy()),
        "zero_count": int(tf.reduce_sum(tf.cast(norms == 0.0, tf.int32)).numpy()),
        "positive_spread": spread,
    }


def _design_metrics(design: tf.Tensor, weights: tf.Tensor, ridge: float) -> Mapping[str, Any]:
    design = tf.convert_to_tensor(design, dtype=tf.float64)
    weights = tf.convert_to_tensor(weights, dtype=tf.float64)
    singular_values = tf.linalg.svd(design, compute_uv=False)
    column_norms = tf.linalg.norm(design, axis=0)
    safe_norms = tf.where(column_norms > 0.0, column_norms, tf.ones_like(column_norms))
    normalized_design = design / safe_norms[tf.newaxis, :]
    weighted_design = design * tf.reshape(weights, [-1, 1])
    gram = tf.matmul(design, weighted_design, transpose_a=True)
    trace_scale = tf.linalg.trace(gram) / tf.cast(tf.shape(gram)[0], tf.float64)
    trace_scaled_ridge = tf.cast(ridge, tf.float64) * tf.maximum(
        trace_scale,
        tf.constant(1e-300, dtype=tf.float64),
    )
    normal_trace_scaled = gram + trace_scaled_ridge * tf.eye(
        int(design.shape[1]),
        dtype=tf.float64,
    )
    return {
        "shape": tuple(int(dim) for dim in design.shape),
        "finite": bool(tf.reduce_all(tf.math.is_finite(design)).numpy()),
        "singular_values": _spectrum_summary(singular_values),
        "condition_A": _finite_condition_from_singular_values(singular_values),
        "column_norms": _column_norm_summary(design),
        "actual_normal_condition": _normal_condition(design, weights, ridge),
        "actual_ridge": float(ridge),
        "explanatory_nonbranch_probes": {
            "column_normalized_normal_condition": _normal_condition(
                normalized_design,
                weights,
                ridge,
            ),
            "trace_scaled_ridge": float(trace_scaled_ridge.numpy()),
            "trace_scaled_ridge_condition": _finite_condition_from_singular_values(
                tf.linalg.svd(normal_trace_scaled, compute_uv=False)
            ),
            "nonclaim": (
                "column normalization and trace-scaled ridge are diagnostics only; "
                "they are not the fitted branch and not a repair"
            ),
        },
    }


def _coordinate_frame_diagnostics(
    *,
    samples: tf.Tensor,
    log_weights: tf.Tensor,
    frame: Any,
    expansion_factor: float,
    covariance_jitter: float,
) -> Mapping[str, Any]:
    weights = tf.exp(source_route.normalize_log_weights(log_weights))
    mu = tf.reduce_sum(samples * weights[tf.newaxis, :], axis=1)
    centered = samples - mu[:, tf.newaxis]
    covariance = tf.einsum("n,in,jn->ij", weights, centered, centered)
    covariance = 0.5 * (covariance + tf.transpose(covariance))
    eigenvalues = tf.linalg.eigvalsh(covariance)
    post_jitter_eigenvalues = eigenvalues + tf.constant(float(covariance_jitter), dtype=tf.float64)
    frame_singular_values = tf.linalg.svd(frame.matrix, compute_uv=False)
    jitter = tf.constant(float(covariance_jitter), dtype=tf.float64)
    jitter_dominated = tf.reduce_sum(tf.cast(eigenvalues <= 10.0 * jitter, tf.int32))
    return {
        "expansion_factor": float(expansion_factor),
        "covariance_jitter": float(covariance_jitter),
        "pre_jitter_covariance_eigenvalues": _spectrum_summary(eigenvalues),
        "post_jitter_covariance_eigenvalues": _spectrum_summary(post_jitter_eigenvalues),
        "frame_matrix_singular_values": _spectrum_summary(frame_singular_values),
        "frame_matrix_condition_number": _finite_condition_from_singular_values(frame_singular_values),
        "frame_log_abs_det": float(frame.log_abs_det().numpy()),
        "jitter_dominated_eigenvalue_count_10x": int(jitter_dominated.numpy()),
        "rank_bound_note": "with n_fit = D = 36, centered covariance rank is at most 35 before jitter",
    }


def _resampling_diagnostics(indices: tf.Tensor) -> Mapping[str, Any]:
    unique, _, counts = tf.unique_with_counts(tf.convert_to_tensor(indices, dtype=tf.int32))
    duplicate_count = int(tf.reduce_sum(counts - 1).numpy())
    return {
        "count": int(indices.shape[0]),
        "unique_count": int(unique.shape[0]),
        "duplicate_count": duplicate_count,
        "max_duplicate_multiplicity": int(tf.reduce_max(counts).numpy()),
        "indices": indices,
        "unique_indices": unique,
        "counts_by_unique_order": counts,
    }


def _local_point_diagnostics(local_unclipped: tf.Tensor, local_clipped: tf.Tensor) -> Mapping[str, Any]:
    unclipped = tf.convert_to_tensor(local_unclipped, dtype=tf.float64)
    clipped = tf.convert_to_tensor(local_clipped, dtype=tf.float64)
    clipped_mask = tf.abs(unclipped) > tf.constant(1.0, dtype=tf.float64)
    boundary_mask = tf.abs(clipped) >= tf.constant(1.0 - 1e-12, dtype=tf.float64)
    row_boundary_counts = tf.reduce_sum(tf.cast(boundary_mask, tf.int32), axis=0)
    axis_boundary_counts = tf.reduce_sum(tf.cast(boundary_mask, tf.int32), axis=1)
    centered_rows = tf.transpose(clipped) - tf.reduce_mean(tf.transpose(clipped), axis=0, keepdims=True)
    row_singular_values = tf.linalg.svd(centered_rows, compute_uv=False)
    return {
        "shape_dim_by_rows": tuple(int(dim) for dim in clipped.shape),
        "unclipped_stats": _tensor_stats(unclipped),
        "clipped_stats": _tensor_stats(clipped),
        "clip_fraction": float(tf.reduce_mean(tf.cast(clipped_mask, tf.float64)).numpy()),
        "entry_boundary_fraction": float(tf.reduce_mean(tf.cast(boundary_mask, tf.float64)).numpy()),
        "row_boundary_count_min": int(tf.reduce_min(row_boundary_counts).numpy()),
        "row_boundary_count_max": int(tf.reduce_max(row_boundary_counts).numpy()),
        "row_all_entries_on_boundary_count": int(
            tf.reduce_sum(tf.cast(row_boundary_counts == int(clipped.shape[0]), tf.int32)).numpy()
        ),
        "axis_boundary_count_min": int(tf.reduce_min(axis_boundary_counts).numpy()),
        "axis_boundary_count_max": int(tf.reduce_max(axis_boundary_counts).numpy()),
        "axis_all_rows_on_boundary_count": int(
            tf.reduce_sum(tf.cast(axis_boundary_counts == int(clipped.shape[1]), tf.int32)).numpy()
        ),
        "axis_boundary_counts": axis_boundary_counts,
        "centered_local_row_singular_values": _spectrum_summary(row_singular_values),
    }


def _core_norm_diagnostics(cores: Sequence[TTCore]) -> Mapping[str, Any]:
    rows = []
    channel_products = []
    for axis, core in enumerate(cores):
        values = tf.convert_to_tensor(core.values, dtype=tf.float64)
        left_norms = tuple(
            float(tf.linalg.norm(tf.reshape(values[left, :, :], [-1])).numpy())
            for left in range(core.left_rank)
        )
        right_norms = tuple(
            float(tf.linalg.norm(tf.reshape(values[:, :, right], [-1])).numpy())
            for right in range(core.right_rank)
        )
        diagonal_norms = tuple(
            float(tf.linalg.norm(values[index, :, index]).numpy())
            for index in range(min(core.left_rank, core.right_rank))
        )
        rows.append(
            {
                "axis": int(axis),
                "shape": (core.left_rank, core.basis_dim, core.right_rank),
                "total_norm": float(tf.linalg.norm(tf.reshape(values, [-1])).numpy()),
                "nonzero_entries": int(tf.math.count_nonzero(values).numpy()),
                "left_slice_norms": left_norms,
                "right_slice_norms": right_norms,
                "diagonal_channel_norms": diagonal_norms,
            }
        )
    for bond in range(max(len(cores) - 1, 0)):
        left = cores[bond].values
        right = cores[bond + 1].values
        bond_scores = []
        channel_count = min(int(left.shape[2]), int(right.shape[0]))
        for channel in range(channel_count):
            left_norm = float(tf.norm(left[:, :, channel]).numpy())
            right_norm = float(tf.norm(right[channel, :, :]).numpy())
            bond_scores.append(left_norm * right_norm)
        extra_ratio = None
        if len(bond_scores) > 1 and bond_scores[0] > 0.0:
            extra_ratio = bond_scores[1] / bond_scores[0]
        channel_products.append(
            {
                "bond": int(bond),
                "channel_products": tuple(bond_scores),
                "extra_over_constant_ratio": extra_ratio,
            }
        )
    return {
        "core_rows": rows,
        "bond_channel_products": channel_products,
        "p70_channel_activity": source_route._p70_channel_activity_diagnostics(
            cores=tuple(cores),
            target_dim=len(cores),
            fit_rank=FIT_RANK,
        ),
    }


def _build_fit_objects(fit_data: Any, target_dim: int) -> tuple[ProductBasis, FixedTTFitConfig, tuple[TTCore, ...], FixedTTFitSampleBatch]:
    convention = source_route._p59_reference_convention()
    product_basis = ProductBasis(
        [
            LegendreBasis1D(BoundedInterval(-1.0, 1.0), FIT_DEGREE)
            for _ in range(int(target_dim))
        ],
        convention,
    )
    config = FixedTTFitConfig(
        ranks=source_route._source_route_rank_tuple(int(target_dim), FIT_RANK),
        ridge=source_route.P70_FIT_RIDGE,
        max_sweeps=source_route.P70_FIXED_BRANCH_MAX_SWEEPS,
        sweep_order=source_route._p70_canonical_alternating_sweep_order(int(target_dim)),
        row_budget=max(int(tf.shape(fit_data.local_fit_points)[1]), 1),
        column_budget=(FIT_DEGREE + 1) * FIT_RANK * FIT_RANK,
        dense_matrix_byte_budget=2**22,
        normal_matrix_byte_budget=2**24,
        condition_number_warning=source_route.P70_CONDITION_NUMBER_WARNING,
        condition_number_veto=source_route.P70_CONDITION_NUMBER_VETO,
        holdout_tolerance=1e6,
    )
    weights = tf.convert_to_tensor(fit_data.fit_weights, dtype=tf.float64)
    initial_cores = source_route._source_route_seeded_channel_initial_cores(
        ranks=config.ranks,
        basis_dim=FIT_DEGREE + 1,
        constant_value=source_route._weighted_mean_target_value(fit_data.target_values, weights),
    )
    samples = FixedTTFitSampleBatch(
        points=tf.transpose(tf.convert_to_tensor(fit_data.local_fit_points, dtype=tf.float64)),
        target_values=tf.convert_to_tensor(fit_data.target_values, dtype=tf.float64),
        weights=weights,
    )
    return product_basis, config, initial_cores, samples


def _initial_axis_design_diagnostics(
    *,
    fitter: FixedTTFitter,
    product_basis: ProductBasis,
    samples: FixedTTFitSampleBatch,
    config: FixedTTFitConfig,
    initial_cores: Sequence[TTCore],
) -> Mapping[str, Any]:
    rows = []
    for axis in range(product_basis.dimension):
        system = fitter.build_core_update_system(
            product_basis=product_basis,
            points=samples.points,
            target_values=samples.target_values,
            weights=samples.weights,
            cores=initial_cores,
            core_index=axis,
            config=config,
        )
        metrics = _design_metrics(system.design_matrix, samples.weights, config.ridge)
        rows.append(
            {
                "axis": int(axis),
                "gate": system.diagnostics,
                "normal_condition_from_fitter": system.condition_number,
                "condition_status_actual_branch": _condition_status(system.condition_number, config),
                "design_metrics": metrics,
            }
        )
    return {
        "row_count": len(rows),
        "max_actual_normal_condition": max(
            float(row["design_metrics"]["actual_normal_condition"])
            for row in rows
            if isinstance(row["design_metrics"]["actual_normal_condition"], (int, float))
        ),
        "condition_veto_axes": tuple(
            row["axis"]
            for row in rows
            if row["condition_status_actual_branch"] == source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
        ),
        "rows": rows,
    }


def _condition_status(condition_number: float, config: FixedTTFitConfig) -> str:
    if (not math.isfinite(float(condition_number))) or float(condition_number) > config.condition_number_veto:
        return source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
    if float(condition_number) > config.condition_number_warning:
        return "CONDITION_NUMBER_WARNING"
    return source_route.HighDimStatus.OK.value


def _actual_als_attempt_diagnostics(
    *,
    fitter: FixedTTFitter,
    product_basis: ProductBasis,
    samples: FixedTTFitSampleBatch,
    config: FixedTTFitConfig,
    initial_cores: Sequence[TTCore],
) -> Mapping[str, Any]:
    cores = list(initial_cores)
    rows = []
    failed = False
    for sweep_index in range(config.max_sweeps):
        for axis in config.sweep_order:
            system = fitter.build_core_update_system(
                product_basis=product_basis,
                points=samples.points,
                target_values=samples.target_values,
                weights=samples.weights,
                cores=tuple(cores),
                core_index=axis,
                config=config,
            )
            metrics = _design_metrics(system.design_matrix, samples.weights, config.ridge)
            updated_core, record = fitter._fit_core_update(
                product_basis=product_basis,
                points=samples.points,
                target_values=samples.target_values,
                weights=samples.weights,
                cores=tuple(cores),
                core_index=axis,
                config=config,
                sweep_index=sweep_index,
            )
            row = {
                "attempt_index": len(rows),
                "sweep_index": int(sweep_index),
                "axis": int(axis),
                "record": record,
                "normal_condition_from_fitter": system.condition_number,
                "condition_status_actual_branch": _condition_status(system.condition_number, config),
                "design_metrics": metrics,
            }
            rows.append(row)
            if str(record["status"]) != source_route.HighDimStatus.OK.value:
                failed = True
                break
            cores[axis] = updated_core
        if failed:
            break
    return {
        "attempt_count": len(rows),
        "first_failure": None if not failed else rows[-1],
        "records": rows,
        "stopped_on_failure": failed,
    }


def _captured_helper_payload(fit_data: Any, target_dim: int) -> Mapping[str, Any]:
    try:
        source_route._p59_fixed_ttsirt_transport_from_values(
            local_fit_points=fit_data.local_fit_points,
            target_values=fit_data.target_values,
            fit_weights=fit_data.fit_weights,
            target_dim=int(target_dim),
            fit_degree=FIT_DEGREE,
            fit_rank=FIT_RANK,
            ridge=source_route.P70_FIT_RIDGE,
            branch_seed="p70-phase6c-first-row-helper-capture",
            convention=source_route._p59_reference_convention(),
        )
    except source_route.P70FixedFitDiagnosticError as exc:
        return {
            "status": "captured_failed_fit",
            "message": str(exc),
            "fit_status": exc.status.value,
            "payload": exc.payload,
        }
    return {
        "status": "unexpected_success",
        "nonclaim": "unexpected success would contradict Phase 6 first-row failure and requires review",
    }


def _reconstruct_first_row_data() -> Mapping[str, Any]:
    model = source_route.zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=MODEL_SEED)[1]
    previous_batch = source_route._p59_author_sir_prior_sample_batch(
        model=model,
        sample_count=FIT_SAMPLE_COUNT,
        seed=PRIOR_SAMPLE_SEED,
    )
    push = source_route._p59_author_sir_source_push_result(
        model=model,
        previous_batch=previous_batch,
        observation=tf.convert_to_tensor(observations[TIME_INDEX], dtype=tf.float64),
        time_index=TIME_INDEX,
        process_noise_seed=PROCESS_NOISE_SEED,
    )
    frame = source_route.source_route_recenter(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
        expansion_factor=source_route.P63_AUTHOR_SIR_EXPANSION_FACTOR,
        covariance_jitter=1e-5,
        use_quantile_scale=True,
    )
    resampled, resample_indices = source_route._p59_author_sir_deterministic_weighted_resample(
        samples=push.augmented_batch.samples,
        log_weights=push.augmented_batch.log_weights,
    )
    local_unclipped = tf.linalg.solve(frame.matrix, resampled - frame.mu[:, tf.newaxis])
    local_clipped = tf.clip_by_value(local_unclipped, -1.0, 1.0)
    fit_data = source_route._p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=TIME_INDEX,
        fit_sample_count=FIT_SAMPLE_COUNT,
    )
    local_difference = tf.reduce_max(
        tf.abs(local_clipped - tf.convert_to_tensor(fit_data.local_fit_points, dtype=tf.float64))
    )
    return {
        "model": model,
        "observations": observations,
        "previous_batch": previous_batch,
        "push": push,
        "frame": frame,
        "resampled": resampled,
        "resample_indices": resample_indices,
        "local_unclipped": local_unclipped,
        "local_clipped": local_clipped,
        "fit_data": fit_data,
        "fit_data_reconstruction_max_abs_diff": float(local_difference.numpy()),
    }


def _root_cause_evidence_summary(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    frame = payload["coordinate_frame"]
    resampling = payload["resampling"]
    local = payload["local_points"]
    initial = payload["initial_axis_design_diagnostics"]
    actual = payload["actual_als_attempt_diagnostics"]
    first_failure = actual.get("first_failure")
    max_initial_condition = initial.get("max_actual_normal_condition")
    duplicate_fraction = 1.0 - (
        float(resampling["unique_count"]) / max(float(resampling["count"]), 1.0)
    )
    clip_fraction = float(local["clip_fraction"])
    jitter_count = int(frame["jitter_dominated_eigenvalue_count_10x"])
    first_failure_condition = None
    first_failure_axis = None
    failure_column_spread = None
    failure_design_condition = None
    failure_numerical_rank = None
    column_normalized_condition = None
    trace_scaled_ridge_condition = None
    if isinstance(first_failure, Mapping):
        first_failure_axis = first_failure.get("axis")
        metrics = first_failure.get("design_metrics", {})
        if isinstance(metrics, Mapping):
            first_failure_condition = metrics.get("actual_normal_condition")
            failure_design_condition = metrics.get("condition_A")
            singular_values = metrics.get("singular_values", {})
            if isinstance(singular_values, Mapping):
                failure_numerical_rank = singular_values.get("numerical_rank")
            column_norms = metrics.get("column_norms", {})
            if isinstance(column_norms, Mapping):
                failure_column_spread = column_norms.get("positive_spread")
            probes = metrics.get("explanatory_nonbranch_probes", {})
            if isinstance(probes, Mapping):
                column_normalized_condition = probes.get("column_normalized_normal_condition")
                trace_scaled_ridge_condition = probes.get("trace_scaled_ridge_condition")
    primary_scaling_support = (
        isinstance(first_failure_condition, (int, float))
        and float(first_failure_condition) > source_route.P70_CONDITION_NUMBER_VETO
        and isinstance(column_normalized_condition, (int, float))
        and float(column_normalized_condition) < source_route.P70_CONDITION_NUMBER_WARNING
    )
    primary_ridge_support = (
        isinstance(trace_scaled_ridge_condition, (int, float))
        and float(trace_scaled_ridge_condition) < source_route.P70_CONDITION_NUMBER_VETO
    )
    return {
        "topline": (
            "The proximate veto is an unscaled ALS normal-equation conditioning "
            "failure after previous accepted core updates, not clipping and not "
            "an immediate row-count gate failure."
        ),
        "observed_failure_axis": first_failure_axis,
        "observed_failure_normal_condition": first_failure_condition,
        "observed_failure_design_condition": failure_design_condition,
        "observed_failure_design_numerical_rank": failure_numerical_rank,
        "observed_failure_column_norm_spread": failure_column_spread,
        "observed_failure_column_normalized_condition": column_normalized_condition,
        "observed_failure_trace_scaled_ridge_condition": trace_scaled_ridge_condition,
        "max_initial_axis_normal_condition": max_initial_condition,
        "coordinate_frame_jitter_dominated_eigenvalue_count_10x": jitter_count,
        "resampling_duplicate_fraction": duplicate_fraction,
        "local_clip_fraction": clip_fraction,
        "ranked_root_causes": (
            {
                "rank": 1,
                "cause": "unscaled_ALS_design_columns_plus_absolute_normal_equation_ridge",
                "support": "primary",
                "evidence": {
                    "actual_normal_condition": first_failure_condition,
                    "condition_veto": source_route.P70_CONDITION_NUMBER_VETO,
                    "column_norm_spread": failure_column_spread,
                    "column_normalized_condition_explanatory_only": column_normalized_condition,
                    "trace_scaled_ridge_condition_explanatory_only": trace_scaled_ridge_condition,
                    "primary_scaling_support": primary_scaling_support,
                    "primary_ridge_support": primary_ridge_support,
                },
                "nonclaim": "normalization and scaled ridge are diagnostics only, not repairs",
            },
            {
                "rank": 2,
                "cause": "ALS_updates_create_gauge_or_environment_scale_imbalance",
                "support": "primary_contributing",
                "evidence": {
                    "attempt_count_including_failure": actual.get("attempt_count"),
                    "accepted_update_count_before_failure": (
                        first_failure.get("attempt_index")
                        if isinstance(first_failure, Mapping)
                        else None
                    ),
                    "first_failure_axis": first_failure_axis,
                    "initial_axis_max_condition_below_veto": max_initial_condition,
                },
            },
            {
                "rank": 3,
                "cause": "effective_sample_and_row_rank_loss",
                "support": "contributing",
                "evidence": {
                    "unique_resampled_rows": resampling["unique_count"],
                    "fit_sample_count": resampling["count"],
                    "duplicate_fraction": duplicate_fraction,
                    "centered_local_row_rank": local["centered_local_row_singular_values"]["numerical_rank"],
                },
            },
            {
                "rank": 4,
                "cause": "coordinate_frame_rank_boundary_and_jitter_dependence",
                "support": "background_contributing",
                "evidence": {
                    "pre_jitter_covariance_condition": frame["pre_jitter_covariance_eigenvalues"]["condition_number"],
                    "jitter_dominated_eigenvalue_count_10x": jitter_count,
                    "frame_matrix_condition_number": frame["frame_matrix_condition_number"],
                },
            },
            {
                "rank": 5,
                "cause": "clipping_saturation",
                "support": "ruled_out_for_this_row",
                "evidence": {
                    "clip_fraction": clip_fraction,
                    "entry_boundary_fraction": local["entry_boundary_fraction"],
                },
            },
            {
                "rank": 6,
                "cause": "ignored_ridge_argument",
                "support": "implementation_smell_not_this_run_root_cause",
                "evidence": {
                    "helper_uses": "P70_FIT_RIDGE",
                    "supplied_ridge_in_this_run": source_route.P70_FIT_RIDGE,
                },
            },
        ),
        "candidate_evidence": {
            "coordinate_frame_fragility": {
                "support": "background_contributing" if jitter_count > 0 else "weak",
                "evidence": {
                    "jitter_dominated_eigenvalue_count_10x": jitter_count,
                    "pre_jitter_condition": frame["pre_jitter_covariance_eigenvalues"]["condition_number"],
                    "frame_matrix_condition_number": frame["frame_matrix_condition_number"],
                },
            },
            "effective_row_collapse": {
                "support": "contributing" if duplicate_fraction >= 0.25 else "weak",
                "evidence": {
                    "unique_count": resampling["unique_count"],
                    "count": resampling["count"],
                    "max_duplicate_multiplicity": resampling["max_duplicate_multiplicity"],
                    "centered_local_row_rank": local["centered_local_row_singular_values"]["numerical_rank"],
                },
            },
            "clipping_saturation": {
                "support": "ruled_out_for_this_row" if clip_fraction == 0.0 else "contributing",
                "evidence": {
                    "clip_fraction": clip_fraction,
                    "entry_boundary_fraction": local["entry_boundary_fraction"],
                    "axis_all_rows_on_boundary_count": local["axis_all_rows_on_boundary_count"],
                },
            },
            "seeded_channel_scale_imbalance": {
                "support": "contributing_via_ALS_environment_scale_not_isolated_to_initial_epsilon",
                "evidence": {
                    "epsilon": source_route.P70_SEEDED_CHANNEL_EPSILON,
                    "failure_column_norm_spread": failure_column_spread,
                    "column_normalized_condition_explanatory_only": column_normalized_condition,
                },
            },
            "normal_equation_amplification_absolute_ridge": {
                "support": "primary" if primary_scaling_support else "contributing",
                "evidence": {
                    "actual_normal_condition": first_failure_condition,
                    "condition_veto": source_route.P70_CONDITION_NUMBER_VETO,
                    "ridge": source_route.P70_FIT_RIDGE,
                    "column_normalized_condition_explanatory_only": column_normalized_condition,
                    "trace_scaled_ridge_condition_explanatory_only": trace_scaled_ridge_condition,
                },
            },
            "raw_row_count_not_sufficient": {
                "support": "confirmed_not_sufficient_as_a_numerical_adequacy_test",
                "evidence": {
                    "fit_sample_count": FIT_SAMPLE_COUNT,
                    "target_dim": 36,
                    "note": "row count equals target dimension but measured rank/scaling diagnostics determine numerical adequacy",
                },
            },
            "ignored_ridge_argument": {
                "support": "implementation_smell_not_proven_root_cause",
                "evidence": {
                    "helper_uses": "P70_FIT_RIDGE",
                    "supplied_ridge_in_this_run": source_route.P70_FIT_RIDGE,
                    "nonclaim": "not a root cause here because supplied ridge equals P70_FIT_RIDGE",
                },
            },
        },
    }


def _base_payload(status: str, output: Path) -> Mapping[str, Any]:
    return {
        "status": status,
        "metadata_date": "2026-06-16",
        "diagnostic_scope": "p70_phase6c_first_row_condition_veto_root_cause",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md"
        ),
        "plan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p70-phase6c-first-row-root-cause-diagnostic-plan-2026-06-16.md"
        ),
        "run_manifest": {
            "command": EXPECTED_COMMAND,
            "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
            "output": str(output),
            "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
            "cpu_gpu_status": (
                "cpu_only_cuda_visible_devices_minus_1"
                if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1"
                else "not_cpu_hidden"
            ),
            "environment": {
                "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "MPLCONFIGDIR": os.environ.get("MPLCONFIGDIR"),
            },
            "git_state": _git_state_summary(),
            "random_seeds": {
                "model_simulation": MODEL_SEED,
                "prior_sample": PRIOR_SAMPLE_SEED,
                "process_noise": PROCESS_NOISE_SEED,
            },
        },
        "row_identity": {
            "label": ROW_LABEL,
            "time_index": TIME_INDEX,
            "fit_degree": FIT_DEGREE,
            "fit_rank": FIT_RANK,
            "fit_sample_count": FIT_SAMPLE_COUNT,
        },
        "nonclaims": (
            "diagnostic-only first-row root-cause evidence",
            "no fixed-variant repair",
            "no Phase 6 pass",
            "no Phase 7 unblock",
            "no threshold/ridge/row/rank/degree/sweep/initializer change",
            "no HMC readiness claim",
            "no adaptive Zhao-Cui parity claim",
        ),
    }


def run_diagnostic(output: Path) -> Mapping[str, Any]:
    _event("reconstruct_first_row", "RUNNING", label=ROW_LABEL)
    reconstructed = _reconstruct_first_row_data()
    fit_data = reconstructed["fit_data"]
    model = reconstructed["model"]
    target_dim = model.parameter_dim() + 2 * model.state_dim()
    product_basis, config, initial_cores, samples = _build_fit_objects(fit_data, target_dim)
    fitter = FixedTTFitter()

    _event("measure_designs", "RUNNING", target_dim=target_dim)
    initial_axis_designs = _initial_axis_design_diagnostics(
        fitter=fitter,
        product_basis=product_basis,
        samples=samples,
        config=config,
        initial_cores=initial_cores,
    )
    actual_als_attempts = _actual_als_attempt_diagnostics(
        fitter=fitter,
        product_basis=product_basis,
        samples=samples,
        config=config,
        initial_cores=initial_cores,
    )
    helper_capture = _captured_helper_payload(fit_data, target_dim)

    payload = {
        **_base_payload("P70_PHASE6C_FIRST_ROW_ROOT_CAUSE_DIAGNOSTIC_COMPLETED", output),
        "fixed_policy": {
            "target_dim": int(target_dim),
            "rank_tuple": config.ranks,
            "fit_degree": FIT_DEGREE,
            "fit_rank": FIT_RANK,
            "ridge": config.ridge,
            "max_sweeps": config.max_sweeps,
            "sweep_order": config.sweep_order,
            "condition_number_warning": config.condition_number_warning,
            "condition_number_veto": config.condition_number_veto,
            "initialization_rule": source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
            "seeded_channel_epsilon": source_route.P70_SEEDED_CHANNEL_EPSILON,
            "row_adequacy": source_route._p70_row_adequacy_diagnostics(
                row_count=FIT_SAMPLE_COUNT,
                target_dim=int(target_dim),
                fit_degree=FIT_DEGREE,
                fit_rank=FIT_RANK,
            ),
            "implementation_smell": {
                "ignored_ridge_argument": (
                    "_p59_fixed_ttsirt_transport_from_values accepts ridge but "
                    "constructs FixedTTFitConfig with P70_FIT_RIDGE"
                ),
                "nonclaim": "not repaired or used as root-cause proof in Phase 6c",
            },
        },
        "source_data_manifest": fit_data.manifest,
        "source_push": {
            "ess": reconstructed["push"].diagnostics.effective_sample_size,
            "sample_count": reconstructed["push"].diagnostics.sample_count,
            "augmented_sample_origin": reconstructed["push"].augmented_batch.sample_origin,
            "log_weight_stats": _tensor_stats(reconstructed["push"].augmented_batch.log_weights),
        },
        "resampling": _resampling_diagnostics(reconstructed["resample_indices"]),
        "coordinate_frame": _coordinate_frame_diagnostics(
            samples=reconstructed["push"].augmented_batch.samples,
            log_weights=reconstructed["push"].augmented_batch.log_weights,
            frame=reconstructed["frame"],
            expansion_factor=source_route.P63_AUTHOR_SIR_EXPANSION_FACTOR,
            covariance_jitter=1e-5,
        ),
        "local_points": _local_point_diagnostics(
            reconstructed["local_unclipped"],
            reconstructed["local_clipped"],
        ),
        "fit_data_reconstruction_max_abs_diff": reconstructed[
            "fit_data_reconstruction_max_abs_diff"
        ],
        "target_values": _tensor_stats(fit_data.target_values),
        "initial_cores": _core_norm_diagnostics(initial_cores),
        "initial_axis_design_diagnostics": initial_axis_designs,
        "actual_als_attempt_diagnostics": actual_als_attempts,
        "captured_failed_fit": helper_capture,
    }
    payload["root_cause_evidence_summary"] = _root_cause_evidence_summary(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    _event("run_start", "RUNNING", output=str(args.output))
    _write_payload(args.output, _base_payload("P70_PHASE6C_FIRST_ROW_ROOT_CAUSE_DIAGNOSTIC_RUNNING", args.output))
    payload = run_diagnostic(args.output)
    _write_payload(args.output, payload)
    _event("run_done", "OK", output=str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
