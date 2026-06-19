#!/usr/bin/env python
"""P70 Phase 6h bounded root-cause probes.

This script rebuilds the deterministic row-A and row-B inputs used by the P70
diagnostic lane and records explanatory probes only.  It does not run the full
Phase 6 four-row wrapper, tune thresholds, or modify the fitting route.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

import tensorflow as tf

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bayesfilter.highdim import fitting
from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.fitting import FixedTTFitConfig, FixedTTFitSampleBatch, FixedTTFitter
from bayesfilter.highdim.source_route import (
    P70_CONDITION_NUMBER_VETO,
    P70_CONDITION_NUMBER_WARNING,
    P70_FIT_RIDGE,
    P70_FIXED_BRANCH_INITIALIZATION_RULE,
    P70_FIXED_BRANCH_MAX_SWEEPS,
    P70_HOLDOUT_REPLAY_NORMALIZED_RESIDUAL_VETO,
    P70FixedFitDiagnosticError,
    SourceRouteSequentialDensityComponents,
    SourceRouteSequentialStepSpec,
    SourceRouteTransportProtocol,
    _p59_author_sir_source_density_callbacks,
    _p59_author_sir_source_fit_data_for_step,
    _p59_author_sir_source_route_target,
    _p59_author_sir_unit_reference_points,
    _p59_author_sir_defensive_tau_tensor,
    _p59_fixed_ttsirt_transport_from_values,
    _p59_reference_convention,
    _p59_retained_object_from_spec,
    _p69_author_sir_source_diagnostic_data_for_step,
    _p69_frame_hash,
    _p70_canonical_alternating_sweep_order,
    _source_route_rank_tuple,
    _source_route_seeded_channel_initial_cores,
    zhao_cui_sir_austria_model,
)
from bayesfilter.highdim.squared_tt import SquaredTTDensity, TensorProductReferenceDensity


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json"
)
NONCLAIMS = (
    "root-cause diagnostic only",
    "not a Phase 6 full diagnostic rerun",
    "not a repair",
    "not fixed-variant success",
    "not d18 correctness",
    "not HMC readiness",
    "Phase 7 remains blocked",
)
LINE_FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)
ROW_A = ("rank_candidate_1_2_fit36", 1, 2, 36)
ROW_B = ("rank_stronger_1_3_fit36", 1, 3, 36)


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
        return {
            "head": "unknown",
            "dirty": "unknown",
            "status_error": str(exc),
        }


def _finite_float(value: Any) -> float | None:
    if value is None or isinstance(value, bool):
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    if hasattr(value, "shape") and getattr(value, "shape", ()) == ():
        value = value.item()
    if not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _tensor_stats(value: Any) -> Mapping[str, Any]:
    tensor = tf.reshape(tf.convert_to_tensor(value, dtype=tf.float64), [-1])
    if int(tensor.shape[0]) == 0:
        return {"count": 0}
    ordered = tf.sort(tensor)
    finite = bool(tf.reduce_all(tf.math.is_finite(tensor)).numpy())
    return {
        "count": int(tensor.shape[0]),
        "finite": finite,
        "min": float(tf.reduce_min(tensor).numpy()),
        "max": float(tf.reduce_max(tensor).numpy()),
        "mean": float(tf.reduce_mean(tensor).numpy()),
        "median": float(ordered[int(tensor.shape[0]) // 2].numpy()),
        "std": float(tf.math.reduce_std(tensor).numpy()),
        "rms": float(tf.sqrt(tf.reduce_mean(tf.square(tensor))).numpy()),
        "max_abs": float(tf.reduce_max(tf.abs(tensor)).numpy()),
        "l2_norm": float(tf.linalg.norm(tensor).numpy()),
    }


def _weighted_rms(pred: tf.Tensor, target: tf.Tensor, weight: tf.Tensor) -> float:
    pred = tf.reshape(tf.convert_to_tensor(pred, dtype=tf.float64), [-1])
    target = tf.reshape(tf.convert_to_tensor(target, dtype=tf.float64), [-1])
    weight = tf.reshape(tf.convert_to_tensor(weight, dtype=tf.float64), [-1])
    return float(tf.sqrt(tf.reduce_sum(weight * tf.square(pred - target)) / tf.reduce_sum(weight)).numpy())


def _leave_one_out_nn(points_dim_by_n: tf.Tensor) -> tf.Tensor:
    points = tf.transpose(tf.convert_to_tensor(points_dim_by_n, dtype=tf.float64))
    diff = points[:, tf.newaxis, :] - points[tf.newaxis, :, :]
    dist = tf.sqrt(tf.reduce_sum(tf.square(diff), axis=-1))
    inf_diag = tf.where(
        tf.eye(int(points.shape[0]), dtype=tf.bool),
        tf.constant(float("inf"), dtype=tf.float64),
        tf.constant(0.0, dtype=tf.float64),
    )
    return tf.reduce_min(dist + inf_diag, axis=1)


def _nn_to_fit(query_dim_by_n: tf.Tensor, fit_dim_by_n: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    query = tf.transpose(tf.convert_to_tensor(query_dim_by_n, dtype=tf.float64))
    fit = tf.transpose(tf.convert_to_tensor(fit_dim_by_n, dtype=tf.float64))
    diff = query[:, tf.newaxis, :] - fit[tf.newaxis, :, :]
    dist = tf.sqrt(tf.reduce_sum(tf.square(diff), axis=-1))
    nn_distance = tf.reduce_min(dist, axis=1)
    nn_index = tf.argmin(dist, axis=1, output_type=tf.int32)
    return nn_distance, nn_index


def _effective_support(weights: tf.Tensor) -> Mapping[str, Any]:
    w = tf.reshape(tf.convert_to_tensor(weights, dtype=tf.float64), [-1])
    total = tf.reduce_sum(w)
    if not bool((total > 0.0).numpy()):
        return {"available": False, "reason": "nonpositive_weight_sum"}
    p = w / total
    ess = 1.0 / tf.reduce_sum(tf.square(p))
    max_fraction = tf.reduce_max(p)
    return {
        "available": True,
        "nominal_count": int(w.shape[0]),
        "effective_support": float(ess.numpy()),
        "effective_support_fraction": float((ess / tf.cast(tf.shape(w)[0], tf.float64)).numpy()),
        "max_weight_fraction": float(max_fraction.numpy()),
        "weight_stats": _tensor_stats(w),
    }


def _clip_summary(data) -> Mapping[str, Any]:
    manifest = data.manifest
    local = tf.convert_to_tensor(data.local_fit_points, dtype=tf.float64)
    sat = tf.abs(local) >= 1.0 - 1e-12
    return {
        "manifest_clip_fraction": _finite_float(manifest.get("local_clip_fraction")),
        "coordinate_saturation_fraction": float(tf.reduce_mean(tf.cast(sat, tf.float64)).numpy()),
        "point_any_saturated_fraction": float(tf.reduce_mean(tf.cast(tf.reduce_any(sat, axis=0), tf.float64)).numpy()),
        "local_max_abs": float(tf.reduce_max(tf.abs(local)).numpy()),
        "manifest_local_max_abs_before_clip": _finite_float(manifest.get("local_max_abs_before_clip")),
    }


def _support_audit(fit_data, holdout_data, replay_data) -> Mapping[str, Any]:
    fit_loo = _leave_one_out_nn(fit_data.local_fit_points)
    holdout_nn, holdout_argmin = _nn_to_fit(holdout_data.local_fit_points, fit_data.local_fit_points)
    replay_nn, replay_argmin = _nn_to_fit(replay_data.local_fit_points, fit_data.local_fit_points)
    return {
        "fit_leave_one_out_nn": _tensor_stats(fit_loo),
        "holdout_to_fit_nn": {
            **_tensor_stats(holdout_nn),
            "argmin_indices": holdout_argmin,
        },
        "replay_to_fit_nn": {
            **_tensor_stats(replay_nn),
            "argmin_indices": replay_argmin,
        },
        "fit_clip": _clip_summary(fit_data),
        "holdout_clip": _clip_summary(holdout_data),
        "replay_clip": _clip_summary(replay_data),
        "fit_effective_support": _effective_support(fit_data.fit_weights),
        "holdout_effective_support": _effective_support(holdout_data.fit_weights),
        "replay_effective_support": _effective_support(replay_data.fit_weights),
        "frame_hashes": {
            "fit": fit_data.manifest.get("coordinate_frame_hash"),
            "holdout": holdout_data.manifest.get("coordinate_frame_hash"),
            "replay": replay_data.manifest.get("coordinate_frame_hash"),
        },
        "shift_constants": {
            "fit": fit_data.shift_constant,
            "holdout": holdout_data.shift_constant,
            "replay": replay_data.shift_constant,
        },
    }


def _scaled_augmented_spectrum(design: tf.Tensor, target: tf.Tensor, weights: tf.Tensor, ridge: float) -> Mapping[str, Any]:
    result = fitting._solve_scaled_augmented_ridge(
        design=design,
        target_values=target,
        weights=weights,
        ridge=ridge,
    )
    singular = tf.linalg.svd(result.scaled_augmented_matrix, compute_uv=False)
    s_max = float(tf.reduce_max(singular).numpy())
    tol = max(s_max * 1e-12, 1e-300)
    effective_rank = int(tf.reduce_sum(tf.cast(singular > tol, tf.int32)).numpy())
    n_cols = int(result.scaled_augmented_matrix.shape[1])
    return {
        "scaled_augmented_condition_number": result.scaled_augmented_condition_number,
        "singular_values": singular,
        "singular_value_max": s_max,
        "singular_value_min": float(tf.reduce_min(singular).numpy()),
        "effective_rank_tol": tol,
        "effective_rank": effective_rank,
        "effective_rank_ratio": effective_rank / max(n_cols, 1),
        "n_cols": n_cols,
        "n_rows": int(result.scaled_augmented_matrix.shape[0]),
        "column_scale_min": float(tf.reduce_min(result.column_scales).numpy()),
        "column_scale_max": float(tf.reduce_max(result.column_scales).numpy()),
        "column_scale_spread": (
            float(tf.reduce_max(result.column_scales).numpy())
            / max(float(tf.reduce_min(result.column_scales).numpy()), 1e-300)
        ),
        "raw_column_norm_zero_count": int(tf.reduce_sum(tf.cast(result.raw_column_norms == 0.0, tf.int32)).numpy()),
    }


def _density_normalizer_from_tt(tt, product_basis: ProductBasis, convention) -> Mapping[str, Any]:
    defensive = TensorProductReferenceDensity(product_basis, convention)
    tau = _p59_author_sir_defensive_tau_tensor()
    normalizer_floor = tf.constant(1e-12, dtype=tf.float64)
    denominator_floor = tf.constant(1e-12, dtype=tf.float64)
    branch_identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=convention,
    )
    density = SquaredTTDensity(
        sqrt_tt=tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=convention,
        branch_identity=branch_identity,
    )
    return {
        "sqrt_square_normalizer": float(density.sqrt_square_normalizer().numpy()),
        "mixture_normalizer": float(density.normalizer().numpy()),
        "defensive_tau": float(density.tau.numpy()),
        "defensive_normalizer": float(
            density.defensive_density.normalizer(density.measure_convention.mass_measure).numpy()
        ),
    }


def _condition_system_summary(
    *,
    fitter: FixedTTFitter,
    product_basis: ProductBasis,
    points_n_by_d: tf.Tensor,
    target_values: tf.Tensor,
    weights: tf.Tensor,
    cores,
    core_index: int,
    config: FixedTTFitConfig,
) -> Mapping[str, Any]:
    design = fitter._build_design_matrix(product_basis, points_n_by_d, tuple(cores), int(core_index))
    normal, _ = fitting._normal_equations(design, target_values, weights, config.ridge)
    unscaled = fitting._condition_number(normal)
    spectrum = _scaled_augmented_spectrum(design, target_values, weights, config.ridge)
    return {
        "core_index": int(core_index),
        "design_shape": tuple(int(v) for v in design.shape),
        "unscaled_normal_condition_number": fitting._finite_number_or_text(unscaled),
        **spectrum,
    }


def _make_config(*, target_dim: int, fit_degree: int, fit_rank: int, fit_sample_count: int, ridge: float) -> FixedTTFitConfig:
    return FixedTTFitConfig(
        ranks=_source_route_rank_tuple(int(target_dim), int(fit_rank)),
        ridge=float(ridge),
        max_sweeps=P70_FIXED_BRANCH_MAX_SWEEPS,
        sweep_order=_p70_canonical_alternating_sweep_order(int(target_dim)),
        row_budget=max(int(fit_sample_count), 1),
        column_budget=(int(fit_degree) + 1) * int(fit_rank) * int(fit_rank),
        dense_matrix_byte_budget=2**22,
        normal_matrix_byte_budget=2**24,
        condition_number_warning=P70_CONDITION_NUMBER_WARNING,
        condition_number_veto=P70_CONDITION_NUMBER_VETO,
        holdout_tolerance=1e6,
    )


def _fit_with_diagnostics(
    *,
    fit_data,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
    ridge: float,
    branch_seed: str,
    convention,
) -> Mapping[str, Any]:
    product_basis = ProductBasis(
        [LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(fit_degree)) for _ in range(int(target_dim))],
        convention,
    )
    config = _make_config(
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        fit_sample_count=int(tf.shape(fit_data.local_fit_points)[1]),
        ridge=ridge,
    )
    weights = tf.convert_to_tensor(fit_data.fit_weights, dtype=tf.float64)
    target = tf.convert_to_tensor(fit_data.target_values, dtype=tf.float64)
    initial_cores = _source_route_seeded_channel_initial_cores(
        ranks=config.ranks,
        basis_dim=int(fit_degree) + 1,
        constant_value=tf.reduce_sum(weights * target) / tf.reduce_sum(weights),
    )
    result = FixedTTFitter().fit(
        product_basis=product_basis,
        samples=FixedTTFitSampleBatch(
            points=tf.transpose(fit_data.local_fit_points),
            target_values=target,
            weights=weights,
        ),
        config=config,
        initial_cores=initial_cores,
        branch_seed=branch_seed,
        measure_convention=convention,
        initialization_rule=P70_FIXED_BRANCH_INITIALIZATION_RULE,
    )
    return {
        "product_basis": product_basis,
        "config": config,
        "initial_cores": initial_cores,
        "result": result,
    }


def _raw_output_audit(tt, product_basis: ProductBasis, convention, fit_data, holdout_data, replay_data) -> Mapping[str, Any]:
    fit_points = tf.transpose(fit_data.local_fit_points)
    holdout_points = tf.transpose(holdout_data.local_fit_points)
    replay_points = tf.transpose(replay_data.local_fit_points)
    fit_pred = tt.evaluate(fit_points)
    holdout_pred = tt.evaluate(holdout_points)
    replay_pred = tt.evaluate(replay_points)
    fit_rms = _weighted_rms(fit_pred, fit_data.target_values, fit_data.fit_weights)
    holdout_rms = _weighted_rms(holdout_pred, holdout_data.target_values, holdout_data.fit_weights)
    replay_rms = _weighted_rms(replay_pred, replay_data.target_values, replay_data.fit_weights)
    target_scale = _tensor_stats(fit_data.target_values)["rms"]
    density_normalizer = _density_normalizer_from_tt(tt, product_basis, convention)
    sqrt_square_scale = max(density_normalizer["sqrt_square_normalizer"], 1e-300)
    return {
        "fit": {
            "target": _tensor_stats(fit_data.target_values),
            "prediction": _tensor_stats(fit_pred),
            "raw_residual": fit_rms,
            "target_rms_normalized_residual": fit_rms / target_scale,
            "sqrt_square_normalized_residual": fit_rms / sqrt_square_scale,
        },
        "holdout": {
            "target": _tensor_stats(holdout_data.target_values),
            "prediction": _tensor_stats(holdout_pred),
            "raw_residual": holdout_rms,
            "target_rms_normalized_residual": holdout_rms / target_scale,
            "sqrt_square_normalized_residual": holdout_rms / sqrt_square_scale,
        },
        "replay": {
            "target": _tensor_stats(replay_data.target_values),
            "prediction": _tensor_stats(replay_pred),
            "raw_residual": replay_rms,
            "target_rms_normalized_residual": replay_rms / target_scale,
            "sqrt_square_normalized_residual": replay_rms / sqrt_square_scale,
        },
        "fit_target_rms_scale": target_scale,
        "density_normalizer": density_normalizer,
    }


def _line_probe(tt, fit_data, holdout_data) -> Mapping[str, Any]:
    nn, argmin = _nn_to_fit(holdout_data.local_fit_points, fit_data.local_fit_points)
    nn_values = nn.numpy()
    order = sorted(range(len(nn_values)), key=lambda i: float(nn_values[i]))
    selected = []
    for candidate in (order[0], order[len(order) // 2], order[-1]):
        if candidate not in selected:
            selected.append(candidate)
    rows = []
    fit_points = tf.transpose(fit_data.local_fit_points)
    fit_pred = tt.evaluate(fit_points)
    fit_pred_max = max(float(tf.reduce_max(tf.abs(fit_pred)).numpy()), 1e-300)
    for holdout_index in selected:
        fit_index = int(argmin[holdout_index].numpy())
        start = tf.gather(fit_data.local_fit_points, fit_index, axis=1)
        end = tf.gather(holdout_data.local_fit_points, holdout_index, axis=1)
        values = []
        for frac in LINE_FRACTIONS:
            point = (1.0 - frac) * start + frac * end
            pred = tt.evaluate(tf.reshape(point, [1, -1]))[0]
            values.append(
                {
                    "fraction": float(frac),
                    "prediction": float(pred.numpy()),
                    "abs_prediction": float(tf.abs(pred).numpy()),
                }
            )
        max_abs = max(item["abs_prediction"] for item in values)
        rows.append(
            {
                "holdout_index": int(holdout_index),
                "nearest_fit_index": fit_index,
                "endpoint_distance": float(nn[holdout_index].numpy()),
                "values": values,
                "max_abs_prediction": max_abs,
                "growth_vs_fit_pred_max": max_abs / fit_pred_max,
            }
        )
    return {
        "fractions": LINE_FRACTIONS,
        "selection_rule": "nearest_median_farthest_holdout_to_fit",
        "pairs": rows,
    }


def _build_step1_context(*, fit_sample_count: int, fit_degree: int, fit_rank: int, ridge: float):
    model = zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    d = model.parameter_dim()
    m = model.state_dim()
    target_dim = d + 2 * m
    convention = _p59_reference_convention()
    prior_log_density, transition_log_density, likelihood_t1 = _p59_author_sir_source_density_callbacks(model, observations[1])
    fit_data1 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=fit_sample_count,
    )
    holdout_data1 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=fit_sample_count,
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        prior_seed=7301,
        process_noise_seed=7401,
        construction="p69_step1_holdout_distinct_diagnostic_seed",
    )
    replay_data1 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=fit_sample_count,
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        prior_seed=7311,
        process_noise_seed=7501,
        construction="p69_step1_replay_distinct_diagnostic_seed",
    )
    fit = _fit_with_diagnostics(
        fit_data=fit_data1,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        ridge=ridge,
        branch_seed="p70-phase6h-step1-row-a-refit",
        convention=convention,
    )
    components1 = SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_t1,
        prior_log_density_fn=prior_log_density,
    )
    transport1, _, _, _, _ = _p59_fixed_ttsirt_transport_from_values(
        local_fit_points=fit_data1.local_fit_points,
        target_values=fit_data1.target_values,
        fit_weights=fit_data1.fit_weights,
        fit_data_manifest=fit_data1.manifest,
        holdout_local_points=holdout_data1.local_fit_points,
        holdout_target_values=holdout_data1.target_values,
        holdout_weights=holdout_data1.fit_weights,
        holdout_manifest=holdout_data1.manifest,
        replay_local_points=replay_data1.local_fit_points,
        replay_target_values=replay_data1.target_values,
        replay_weights=replay_data1.fit_weights,
        replay_manifest=replay_data1.manifest,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        ridge=ridge,
        branch_seed="p59-9b-author-sir-step1-fixed-ttsirt",
        convention=convention,
    )
    spec1 = SourceRouteSequentialStepSpec(
        target=_p59_author_sir_source_route_target(
            frame=fit_data1.frame,
            shift_constant=fit_data1.shift_constant,
            time_index=1,
            components=components1,
        ),
        transport=SourceRouteTransportProtocol(transport1),
        reference_samples=_p59_author_sir_unit_reference_points(fit_sample_count, target_dim),
        measure_convention=convention,
        density_components=components1,
    )
    fit_retained1 = _p59_retained_object_from_spec(spec1)
    return {
        "model": model,
        "observations": observations,
        "target_dim": target_dim,
        "convention": convention,
        "fit_data": fit_data1,
        "holdout_data": holdout_data1,
        "replay_data": replay_data1,
        "fit": fit,
        "fit_retained": fit_retained1,
    }


def _build_step2_context(step1, *, fit_sample_count: int, fit_degree: int, fit_rank: int, ridge: float):
    model = step1["model"]
    observations = step1["observations"]
    target_dim = step1["target_dim"]
    convention = step1["convention"]
    fit_retained1 = step1["fit_retained"]
    fit_data2 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        fit_sample_count=fit_sample_count,
        previous_retained_object=fit_retained1,
    )
    holdout_data2 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        diagnostic_sample_count=fit_sample_count,
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=fit_retained1,
        process_noise_seed=7402,
        construction="p69_step2_holdout_distinct_diagnostic_seed",
    )
    replay_data2 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        diagnostic_sample_count=fit_sample_count,
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=fit_retained1,
        process_noise_seed=7502,
        construction="p69_step2_replay_distinct_diagnostic_seed",
    )
    fit = _fit_with_diagnostics(
        fit_data=fit_data2,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        ridge=ridge,
        branch_seed="p70-phase6h-step2-row-a-refit",
        convention=convention,
    )
    return {
        "target_dim": target_dim,
        "convention": convention,
        "fit_data": fit_data2,
        "holdout_data": holdout_data2,
        "replay_data": replay_data2,
        "fit": fit,
    }


def _row_a_condition_audit(context: Mapping[str, Any], *, fit_degree: int, fit_rank: int, ridge: float) -> Mapping[str, Any]:
    fit_data = context["fit_data"]
    fit = context["fit"]
    target_dim = int(context.get("target_dim", len(fit["config"].ranks) - 1))
    indices = tuple(dict.fromkeys((0, target_dim // 2, target_dim - 1)))
    fitter = FixedTTFitter()
    points = tf.transpose(fit_data.local_fit_points)
    rows = []
    for state_name, cores in (
        ("initial", fit["initial_cores"]),
        ("final", fit["result"].fitted_tt.cores),
    ):
        for core_index in indices:
            rows.append(
                {
                    "state": state_name,
                    **_condition_system_summary(
                        fitter=fitter,
                        product_basis=fit["product_basis"],
                        points_n_by_d=points,
                        target_values=fit_data.target_values,
                        weights=fit_data.fit_weights,
                        cores=cores,
                        core_index=core_index,
                        config=fit["config"],
                    ),
                }
            )
    return {
        "core_indices": indices,
        "rows": rows,
    }


def _row_a_step_audit(context: Mapping[str, Any], *, step_index: int) -> Mapping[str, Any]:
    fit_data = context["fit_data"]
    holdout_data = context["holdout_data"]
    replay_data = context["replay_data"]
    tt = context["fit"]["result"].fitted_tt
    return {
        "time_index": int(step_index),
        "fit_status": context["fit"]["result"].status.value,
        "fit_termination_reason": context["fit"]["result"].termination_reason,
        "support": _support_audit(fit_data, holdout_data, replay_data),
        "raw_output": _raw_output_audit(
            tt,
            context["fit"]["product_basis"],
            context.get("convention"),
            fit_data,
            holdout_data,
            replay_data,
        ),
        "line_stability": _line_probe(tt, fit_data, holdout_data),
        "design_conditioning": _row_a_condition_audit(context, fit_degree=1, fit_rank=2, ridge=P70_FIT_RIDGE),
        "target_shift_frame": _target_shift_frame_audit(fit_data, holdout_data, replay_data),
    }


def _target_shift_frame_audit(fit_data, holdout_data, replay_data) -> Mapping[str, Any]:
    def row(data):
        return {
            "frame_hash": data.manifest.get("coordinate_frame_hash"),
            "computed_frame_hash": _p69_frame_hash(data.frame),
            "shift_constant": float(tf.convert_to_tensor(data.shift_constant, dtype=tf.float64).numpy()),
            "manifest_shift_constant": _finite_float(data.manifest.get("shift_constant")),
            "target_min": float(tf.reduce_min(data.target_values).numpy()),
            "manifest_target_min": _finite_float(data.manifest.get("target_value_min")),
            "target_max": float(tf.reduce_max(data.target_values).numpy()),
            "manifest_target_max": _finite_float(data.manifest.get("target_value_max")),
        }
    rows = {
        "fit": row(fit_data),
        "holdout": row(holdout_data),
        "replay": row(replay_data),
    }
    return rows


def _row_b_probe() -> Mapping[str, Any]:
    label, degree, rank, fit_sample_count = ROW_B
    model = zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    target_dim = model.parameter_dim() + 2 * model.state_dim()
    convention = _p59_reference_convention()
    fit_data = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=fit_sample_count,
    )
    fit = _fit_with_diagnostics(
        fit_data=fit_data,
        target_dim=target_dim,
        fit_degree=degree,
        fit_rank=rank,
        ridge=P70_FIT_RIDGE,
        branch_seed="p70-phase6h-step1-row-b-replay",
        convention=convention,
    )
    replay = _replay_core_update_systems(
        fit_data=fit_data,
        fit=fit,
    )
    if replay["status"] == "captured_condition_veto":
        return {
            "label": label,
            "degree": int(degree),
            "rank": int(rank),
            "fit_sample_count": int(fit_sample_count),
            "fit_status": fit["result"].status.value,
            "termination_reason": fit["result"].termination_reason,
            **replay,
            "mandatory_reconstruction_status": "satisfied_by_replayed_core_update_systems",
        }
    return {
        "label": label,
        "degree": int(degree),
        "rank": int(rank),
        "fit_sample_count": int(fit_sample_count),
        "fit_status": fit["result"].status.value,
        "termination_reason": fit["result"].termination_reason,
        **replay,
        "mandatory_reconstruction_status": "failed_expected_veto_not_reproduced",
    }


def _replay_core_update_systems(*, fit_data, fit: Mapping[str, Any]) -> Mapping[str, Any]:
    fitter = FixedTTFitter()
    points = tf.transpose(fit_data.local_fit_points)
    target = tf.convert_to_tensor(fit_data.target_values, dtype=tf.float64)
    weights = tf.convert_to_tensor(fit_data.fit_weights, dtype=tf.float64)
    cores = list(fit["initial_cores"])
    records = []
    last_accepted = None
    for sweep_index in range(fit["config"].max_sweeps):
        for core_index in fit["config"].sweep_order:
            system = _condition_system_summary(
                fitter=fitter,
                product_basis=fit["product_basis"],
                points_n_by_d=points,
                target_values=target,
                weights=weights,
                cores=tuple(cores),
                core_index=int(core_index),
                config=fit["config"],
            )
            updated_core, record = fitter._fit_core_update(
                product_basis=fit["product_basis"],
                points=points,
                target_values=target,
                weights=weights,
                cores=tuple(cores),
                core_index=int(core_index),
                config=fit["config"],
                sweep_index=int(sweep_index),
            )
            summary = {
                **_row_b_record_summary(record),
                "system_spectrum": system,
            }
            records.append(summary)
            if str(record.get("status")) != "OK":
                return {
                    "status": "captured_condition_veto",
                    "record_count": len(records),
                    "last_accepted_record": last_accepted or {"available": False},
                    "failing_record": summary,
                    "condition_path_summary": _condition_path_summary(records),
                }
            cores[int(core_index)] = updated_core
            last_accepted = summary
    return {
        "status": "unexpected_no_condition_veto",
        "record_count": len(records),
        "last_accepted_record": last_accepted or {"available": False},
        "failing_record": {"available": False},
        "condition_path_summary": _condition_path_summary(records),
    }


def _row_b_record_summary(record: Mapping[str, Any]) -> Mapping[str, Any]:
    if not record:
        return {"available": False}
    return {
        "available": True,
        "sweep_index": record.get("sweep_index"),
        "core_index": record.get("core_index"),
        "n_rows": record.get("n_rows"),
        "n_cols": record.get("n_cols"),
        "status": record.get("status"),
        "termination_reason": record.get("termination_reason"),
        "scaled_augmented_condition_number": record.get("scaled_augmented_condition_number", record.get("condition_number")),
        "unscaled_normal_condition_number": record.get("unscaled_normal_condition_number"),
        "column_scale_min": record.get("column_scale_min"),
        "column_scale_max": record.get("column_scale_max"),
        "column_scale_spread": record.get("column_scale_spread"),
        "raw_column_norm_zero_count": record.get("raw_column_norm_zero_count"),
    }


def _condition_path_summary(records: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...]) -> Mapping[str, Any]:
    scaled = []
    spreads = []
    inf_unscaled = 0
    for record in records:
        value = _finite_float(record.get("scaled_augmented_condition_number", record.get("condition_number")))
        if value is not None:
            scaled.append(value)
        spread = _finite_float(record.get("column_scale_spread"))
        if spread is not None:
            spreads.append(spread)
        if str(record.get("unscaled_normal_condition_number")) == "inf":
            inf_unscaled += 1
    return {
        "record_count": len(records),
        "scaled_condition_stats": _tensor_stats(tf.constant(scaled, dtype=tf.float64)) if scaled else {"count": 0},
        "column_scale_spread_stats": _tensor_stats(tf.constant(spreads, dtype=tf.float64)) if spreads else {"count": 0},
        "unscaled_inf_count": inf_unscaled,
        "condition_veto": P70_CONDITION_NUMBER_VETO,
        "condition_warning": P70_CONDITION_NUMBER_WARNING,
    }


def _max_nested(values: list[float]) -> float | None:
    finite = [float(v) for v in values if math.isfinite(float(v))]
    return max(finite) if finite else None


def _classify(row_a_steps: list[Mapping[str, Any]], row_b: Mapping[str, Any]) -> Mapping[str, Any]:
    h2_supported = False
    h2_weakenable = True
    h4_supported = False
    h4_weakenable = True
    h7_supported = False
    h7_weakened = True
    h8_supported = False
    h8_weakenable = True
    h5_supported = False
    h5_weakenable = True
    details: dict[str, Any] = {}
    for step in row_a_steps:
        support = step["support"]
        fit_median = support["fit_leave_one_out_nn"].get("median")
        for channel in ("holdout", "replay"):
            nn = support[f"{channel}_to_fit_nn"].get("median")
            clip = support[f"{channel}_clip"].get("coordinate_saturation_fraction")
            if fit_median is not None and nn is not None and fit_median > 0 and nn >= 2.0 * fit_median:
                h2_supported = True
            if clip is not None and clip >= 0.25:
                h2_supported = True
            if not (fit_median is not None and nn is not None and fit_median > 0 and nn < 2.0 * fit_median and clip is not None and clip < 0.25):
                h2_weakenable = False
        ess = support["fit_effective_support"]
        if ess.get("available") and ess["effective_support"] < 0.5 * ess["nominal_count"]:
            h2_supported = True
        raw = step["raw_output"]
        fit_target_rms = raw["fit_target_rms_scale"]
        fit_pred_max = max(raw["fit"]["prediction"]["max_abs"], 1e-300)
        raw_max_predictions = [
            raw["holdout"]["prediction"]["max_abs"],
            raw["replay"]["prediction"]["max_abs"],
        ]
        line_max = _max_nested([pair["max_abs_prediction"] for pair in step["line_stability"]["pairs"]])
        if line_max is not None:
            raw_max_predictions.append(line_max)
        if any(v >= 1e6 * fit_target_rms or v >= 1e6 * fit_pred_max for v in raw_max_predictions):
            h4_supported = True
        if not all(v < 1e3 * fit_target_rms and v < 1e3 * fit_pred_max for v in raw_max_predictions):
            h4_weakenable = False
        for channel in ("holdout", "replay"):
            residual = raw[channel]["raw_residual"]
            normalized = raw[channel]["target_rms_normalized_residual"]
            if residual < 100.0 * fit_target_rms and normalized > P70_HOLDOUT_REPLAY_NORMALIZED_RESIDUAL_VETO:
                h7_supported = True
            if residual < 1e6 * fit_target_rms:
                h7_weakened = False
        for row in step["design_conditioning"]["rows"]:
            condition = _finite_float(row.get("scaled_augmented_condition_number"))
            er = _finite_float(row.get("effective_rank_ratio"))
            if condition is not None and condition > P70_CONDITION_NUMBER_WARNING:
                h8_supported = True
            if er is not None and er < 0.5:
                h8_supported = True
            if not (condition is not None and condition < 1e8 and er is not None and er >= 0.75):
                h8_weakenable = False
        for _, audit_row in step["target_shift_frame"].items():
            if audit_row["frame_hash"] != audit_row["computed_frame_hash"]:
                h5_supported = True
            manifest_shift = audit_row.get("manifest_shift_constant")
            if manifest_shift is not None and abs(audit_row["shift_constant"] - manifest_shift) > 1e-10:
                h5_supported = True
            for key in ("target_min", "target_max"):
                manifest_value = audit_row.get(f"manifest_{key}")
                if manifest_value is not None:
                    denom = 1.0 + abs(audit_row[key]) + abs(manifest_value)
                    if abs(audit_row[key] - manifest_value) / denom > 1e-8:
                        h5_supported = True
            if h5_supported:
                h5_weakenable = False
    failing_condition = _finite_float(row_b.get("failing_record", {}).get("scaled_augmented_condition_number"))
    if failing_condition is not None and failing_condition > P70_CONDITION_NUMBER_VETO:
        h8_supported = True
    if str(row_b.get("failing_record", {}).get("unscaled_normal_condition_number")) == "inf":
        h8_supported = True
    if row_b.get("mandatory_reconstruction_status") != "satisfied_by_replayed_core_update_systems":
        h8_weakenable = False
    classifications = {
        "H2_H6_support_effective_support": "supported" if h2_supported else ("weakened" if h2_weakenable else "unresolved"),
        "H4_off_cloud_growth": "supported" if h4_supported else ("weakened" if h4_weakenable else "unresolved"),
        "H7_metric_amplification": "supported" if h7_supported else ("weakened" if h7_weakened else "unresolved"),
        "H8_H3_conditioning": "supported" if h8_supported else ("weakened" if h8_weakenable else "unresolved"),
        "H5_target_shift_frame": "supported" if h5_supported else ("weakened" if h5_weakenable else "unresolved"),
    }
    details["decision_rules"] = {
        "support_nn_ratio": 2.0,
        "clip_fraction": 0.25,
        "effective_support_fraction": 0.5,
        "off_cloud_support_ratio": 1e6,
        "off_cloud_weaken_ratio": 1e3,
        "metric_raw_moderate_ratio": 100.0,
        "metric_raw_huge_ratio": 1e6,
        "conditioning_warning": P70_CONDITION_NUMBER_WARNING,
        "conditioning_veto": P70_CONDITION_NUMBER_VETO,
    }
    return {
        "classifications": classifications,
        "details": details,
    }


def _build_payload(output: Path, command: str) -> Mapping[str, Any]:
    step1 = _build_step1_context(fit_sample_count=36, fit_degree=1, fit_rank=2, ridge=P70_FIT_RIDGE)
    step2 = _build_step2_context(step1, fit_sample_count=36, fit_degree=1, fit_rank=2, ridge=P70_FIT_RIDGE)
    row_a_steps = [
        {**_row_a_step_audit({**step1, "target_dim": step1["target_dim"]}, step_index=1)},
        {**_row_a_step_audit({**step2, "target_dim": step1["target_dim"]}, step_index=2)},
    ]
    row_b = _row_b_probe()
    if row_b.get("mandatory_reconstruction_status") != "satisfied_by_replayed_core_update_systems":
        status = "P70_PHASE6H_BLOCKED_ROW_B_RECONSTRUCTION"
    else:
        status = "P70_PHASE6H_ROOT_CAUSE_PROBES_COMPLETED"
    return {
        "status": status,
        "metadata_date": "2026-06-17",
        "diagnostic_scope": "p70_phase6h_root_cause_probes",
        "master_program": "docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md",
        "subplan": "docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-subplan-2026-06-17.md",
        "run_manifest": {
            "command": command,
            "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
            "output": str(output),
            "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
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
                "model_simulation": 5901,
                "step1_fit_prior": 6301,
                "step1_fit_process_noise": 6401,
                "step1_holdout_prior": 7301,
                "step1_holdout_process_noise": 7401,
                "step1_replay_prior": 7311,
                "step1_replay_process_noise": 7501,
                "step2_fit_process_noise": 6402,
                "step2_holdout_process_noise": 7402,
                "step2_replay_process_noise": 7502,
            },
            "nonclaims": NONCLAIMS,
        },
        "row_a": {
            "label": ROW_A[0],
            "degree": ROW_A[1],
            "rank": ROW_A[2],
            "fit_sample_count": ROW_A[3],
            "steps": row_a_steps,
        },
        "row_b": row_b,
        "hypothesis_classification": _classify(row_a_steps, row_b),
        "nonclaims": NONCLAIMS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    command = (
        "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        f"scripts/p70_phase6h_root_cause_probes.py --output {args.output}"
    )
    payload = _build_payload(args.output, command)
    _write_payload(args.output, payload)
    print(json.dumps({"p70_phase6h_status": payload["status"], "output": str(args.output)}, sort_keys=True))
    return 0 if payload["status"] == "P70_PHASE6H_ROOT_CAUSE_PROBES_COMPLETED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
