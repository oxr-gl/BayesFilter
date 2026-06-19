#!/usr/bin/env python
"""P72 support-certified lower-gate diagnostic.

The default command executes the bounded Phase 5 diagnostic rows.  The
``--smoke-only`` path remains a tiny implementation check and must not be read
as Phase 5 evidence.
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

from bayesfilter.highdim import source_route
from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.fitting import FixedTTFitConfig, FixedTTFitter
from bayesfilter.highdim import fitting
from bayesfilter.highdim.squared_tt import SquaredTTDensity, TensorProductReferenceDensity
from bayesfilter.highdim.transport import FixedTTSIRTTransport, KRCDFConfig
from scripts import p70_phase6h_root_cause_probes as p70

from bayesfilter.highdim.source_route import (
    P70_CONDITION_NUMBER_VETO,
    P70_CONDITION_NUMBER_WARNING,
    P70_FIXED_BRANCH_INITIALIZATION_RULE,
    P70_FIXED_BRANCH_MAX_SWEEPS,
    P70_FIT_RIDGE,
    SourceRouteSequentialDensityComponents,
    SourceRouteSequentialStepSpec,
    SourceRouteTransportProtocol,
    _p59_author_sir_defensive_tau_tensor,
    _p59_author_sir_source_density_callbacks,
    _p59_author_sir_source_fit_data_for_step,
    _p59_author_sir_source_route_target,
    _p59_author_sir_unit_reference_points,
    _p59_fixed_ttsirt_transport_from_values,
    _p59_reference_convention,
    _p59_retained_object_from_spec,
    _p69_author_sir_source_diagnostic_data_for_step,
    _p69_frame_hash,
    _p70_canonical_alternating_sweep_order,
    _p70_channel_activity_diagnostics,
    _source_route_rank_tuple,
    _source_route_seeded_channel_initial_cores,
    build_source_route_target,
    source_route_run_sequential_fixed_hmc,
    source_route_shifted_negative_log_target,
    zhao_cui_sir_austria_model,
)


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p72-support-certified-lower-gate-diagnostic-2026-06-17.json"
)
EXPECTED_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p72_support_certified_lower_gate_diagnostic.py"
)
NONCLAIMS = (
    "no repaired lower-gate pass claim",
    "no d18 correctness claim",
    "no rank/degree promotion",
    "no scaling claim",
    "no HMC readiness claim",
    "no adaptive Zhao-Cui parity claim",
    "no source-faithful claim for guard/audit/line gates",
)
P72_PHASE5_PASS_STATUS = "P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_PASSED"
P72_PHASE5_BLOCK_STATUS = "P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_BLOCKED"
P72_PHASE5_COMPLETED_STATUS = "P72_PHASE5_SUPPORT_CERTIFIED_LOWER_GATE_DIAGNOSTIC_COMPLETED"
PHASE5_ROW_SPECS = (
    ("rank_candidate_1_2_fit36", 1, 2, 36),
    ("rank_stronger_1_3_fit36", 1, 3, 36),
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _jsonable(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    if isinstance(value, float):
        if math.isnan(value):
            return "nan"
        if math.isinf(value):
            return "inf" if value > 0 else "-inf"
        return value
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    try:
        return float(value)
    except (TypeError, ValueError):
        return str(value)


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


def p72_diagnostic_base_payload(
    *,
    rows: Mapping[str, Mapping[str, Any]],
    output: Path,
    status: str,
    command: str,
    gate_summary: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    return {
        "status": status,
        "metadata_date": "2026-06-17",
        "diagnostic_scope": "p72_support_certified_lower_gate_schema",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p72-support-certified-fixed-fit-master-program-2026-06-17.md"
        ),
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p72-phase4-focused-implementation-subplan-2026-06-17.md"
        ),
        "evidence_contract": {
            "question": (
                "Did the P72 implementation expose the support-certified lower-gate "
                "schema needed for the Phase 5 repaired diagnostic?"
            ),
            "baseline_comparator": "P72 Phase 2 design and Phase 3 implementation surface map.",
            "primary_criterion": (
                "Schema records fit/guard/audit separation, support coverage, line, "
                "full normalizer, provenance, condition/effective-rank, and "
                "rank-activity gates without executing Phase 5."
            ),
            "veto_diagnostics": (
                "audit cloud used for training",
                "missing line target evaluation",
                "missing full normalizer gate",
                "missing provenance hashes",
                "low-level solver veto lowered from 1e14",
                "source-faithfulness overclaim",
            ),
            "explanatory_only": (
                "synthetic focused-test magnitudes",
                "schema field ordering",
            ),
            "nonclaims": NONCLAIMS,
        },
        "source_route_controls": {
            "script_role": "p72_phase4_schema_ready_not_phase5_execution",
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "thresholds_changed": False,
            "source_route_semantics_changed": False,
            "phase5_diagnostic_executed": False,
            "policy": source_route.p72_support_certified_policy(),
        },
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
            "random_seeds": source_route.p72_support_certified_policy()["guard_seeds"],
        },
        "rows": dict(rows),
        "gate_summary": {} if gate_summary is None else dict(gate_summary),
        "nonclaims": NONCLAIMS,
    }


class _SmokeFittedTT:
    def evaluate(self, points: tf.Tensor) -> tf.Tensor:
        tensor = tf.convert_to_tensor(points, dtype=tf.float64)
        return tensor[:, 0] + 2.0


def _make_config(*, target_dim: int, fit_degree: int, fit_rank: int, row_budget: int) -> FixedTTFitConfig:
    return FixedTTFitConfig(
        ranks=_source_route_rank_tuple(int(target_dim), int(fit_rank)),
        ridge=P70_FIT_RIDGE,
        max_sweeps=P70_FIXED_BRANCH_MAX_SWEEPS,
        sweep_order=_p70_canonical_alternating_sweep_order(int(target_dim)),
        row_budget=max(int(row_budget), 1),
        column_budget=(int(fit_degree) + 1) * int(fit_rank) * int(fit_rank),
        dense_matrix_byte_budget=2**22,
        normal_matrix_byte_budget=2**24,
        condition_number_warning=P70_CONDITION_NUMBER_WARNING,
        condition_number_veto=P70_CONDITION_NUMBER_VETO,
        holdout_tolerance=1e6,
    )


def _target_values_for_points(
    *,
    points: tf.Tensor,
    frame,
    shift_constant: tf.Tensor,
    time_index: int,
    components: SourceRouteSequentialDensityComponents,
    previous_retained_object,
) -> tf.Tensor:
    local = tf.convert_to_tensor(points, dtype=tf.float64)
    physical = tf.linalg.matmul(frame.matrix, local) + frame.mu[:, tf.newaxis]
    negative_log_physical = components.negative_log_physical_density(
        physical_points=physical,
        time_index=int(time_index),
        previous_retained_object=previous_retained_object,
    )
    local_negative_log = negative_log_physical - frame.log_abs_det()
    shifted = source_route_shifted_negative_log_target(
        negative_log_target=local_negative_log,
        shift_constant=shift_constant,
    )
    return tf.exp(-0.5 * shifted)


def _weighted_rms(predicted: tf.Tensor, target: tf.Tensor, weights: tf.Tensor) -> float:
    pred = tf.reshape(tf.convert_to_tensor(predicted, dtype=tf.float64), [-1])
    values = tf.reshape(tf.convert_to_tensor(target, dtype=tf.float64), [-1])
    weight = tf.reshape(tf.convert_to_tensor(weights, dtype=tf.float64), [-1])
    if pred.shape != values.shape or weight.shape != values.shape:
        raise ValueError("weighted_rms shape mismatch")
    return float(tf.sqrt(tf.reduce_sum(weight * tf.square(pred - values)) / tf.reduce_sum(weight)).numpy())


def _cloud_residual_gate(
    *,
    fitted_tt,
    points: tf.Tensor,
    target_values: tf.Tensor,
    weights: tf.Tensor,
    target_scale: float,
) -> Mapping[str, Any]:
    predictions = tf.convert_to_tensor(fitted_tt.evaluate(tf.transpose(points)), dtype=tf.float64)
    targets = tf.convert_to_tensor(target_values, dtype=tf.float64)
    residual = tf.abs(predictions - targets)
    scale = max(float(target_scale), 1e-300)
    raw_rms = _weighted_rms(predictions, targets, weights)
    max_abs = float(tf.reduce_max(residual).numpy())
    return {
        "rms_relative": raw_rms / scale,
        "max_relative": max_abs / scale,
        "raw_rms": raw_rms,
        "max_abs_residual": max_abs,
        "target_scale": scale,
        "prediction_hash": source_route._p69_hash_tensor("p72_cloud_prediction_hash.v1", predictions),
        "target_hash": source_route._p69_hash_tensor("p72_cloud_target_hash.v1", targets),
    }


def _normalizer_terms(fitted_tt, product_basis: ProductBasis, convention) -> Mapping[str, Any]:
    defensive = TensorProductReferenceDensity(product_basis, convention)
    tau = _p59_author_sir_defensive_tau_tensor()
    normalizer_floor = tf.constant(1e-12, dtype=tf.float64)
    denominator_floor = tf.constant(1e-12, dtype=tf.float64)
    identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=convention,
    )
    density = SquaredTTDensity(
        sqrt_tt=fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=normalizer_floor,
        denominator_floor=denominator_floor,
        measure_convention=convention,
        branch_identity=identity,
    )
    sqrt_square = float(density.sqrt_square_normalizer().numpy())
    tau_value = float(density.tau.numpy())
    defensive_normalizer = float(
        density.defensive_density.normalizer(density.measure_convention.mass_measure).numpy()
    )
    mixture = sqrt_square + tau_value * defensive_normalizer
    normalizer_exception = None
    transport_normalizer = None
    try:
        transport_normalizer = float(density.normalizer().numpy())
    except ValueError as exc:
        normalizer_exception = str(exc)
    log_transport = float("-inf") if mixture <= 0.0 else float(tf.math.log(tf.constant(mixture, dtype=tf.float64)).numpy())
    return {
        "sqrt_square_normalizer": sqrt_square,
        "mixture_normalizer": mixture,
        "defensive_tau": tau_value,
        "defensive_normalizer": defensive_normalizer,
        "transport_normalizer": transport_normalizer,
        "transport_normalizer_floor": float(normalizer_floor.numpy()),
        "log_transport_normalizer": log_transport,
        "normalizer_exception": normalizer_exception if normalizer_exception is not None else (
            None if mixture > 0.0 else "normalizer_floor_or_nonpositive"
        ),
    }


def _skipped_step_after_prior_gate_block(
    *,
    time_index: int,
    fit_degree: int,
    fit_rank: int,
    fit_sample_count: int,
    skipped_after_time_index: int,
    skipped_reasons: tuple[str, ...],
) -> Mapping[str, Any]:
    return {
        "time_index": int(time_index),
        "degree": int(fit_degree),
        "rank": int(fit_rank),
        "fit_point_count": int(fit_sample_count),
        "guard_point_count": 0,
        "audit_point_count": 0,
        "fit_status": "not_fit_prior_step_gate_blocked",
        "fit_termination_reason": "skipped_before_fit",
        "status": source_route.P72_BLOCK_STATUS,
        "skip_reason": "prior_step_gate_blocked_no_retained_object",
        "skipped_after_time_index": int(skipped_after_time_index),
        "prior_step_reasons": tuple(skipped_reasons),
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "gate_summary": {
            "status": source_route.P72_BLOCK_STATUS,
            "reasons": ("prior_step_gate_blocked_no_retained_object",),
            "prior_step_reasons": tuple(skipped_reasons),
            "nonclaims": (
                "step was not fitted because the previous lower-gate certificate blocked",
                "no retained-object or time-2 transport validity claim",
            ),
        },
        "normalizer_gate": {
            "status": "block",
            "reasons": ("prior_step_gate_blocked_no_transport_normalizer",),
            "normalizer_exception": "not_evaluated_prior_step_gate_blocked",
        },
        "nonclaims": NONCLAIMS,
    }


def _fit_p72_step(
    *,
    fit_data,
    guard_data,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
    branch_seed: str,
    convention,
    components: SourceRouteSequentialDensityComponents,
    previous_retained_object,
) -> Mapping[str, Any]:
    line_points, line_manifest = source_route.p72_guard_line_points(
        fit_points=fit_data.local_fit_points,
        guard_points=guard_data.local_fit_points,
    )
    guard_line_targets = _target_values_for_points(
        points=line_points,
        frame=fit_data.frame,
        shift_constant=fit_data.shift_constant,
        time_index=fit_data.time_index,
        components=components,
        previous_retained_object=previous_retained_object,
    )
    guard_points = tf.concat([guard_data.local_fit_points, line_points], axis=1)
    guard_targets = tf.concat([guard_data.target_values, guard_line_targets], axis=0)
    guard_weights = tf.concat(
        [
            tf.convert_to_tensor(guard_data.fit_weights, dtype=tf.float64),
            tf.ones([int(line_points.shape[1])], dtype=tf.float64),
        ],
        axis=0,
    )
    batch, training_manifest = source_route.p72_training_batch_from_fit_and_guard(
        fit_points=fit_data.local_fit_points,
        fit_target_values=fit_data.target_values,
        fit_weights=fit_data.fit_weights,
        guard_points=guard_points,
        guard_target_values=guard_targets,
        guard_weights=guard_weights,
    )
    product_basis = ProductBasis(
        [LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(fit_degree)) for _ in range(int(target_dim))],
        convention,
    )
    config = _make_config(
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        row_budget=int(batch.points.shape[0]),
    )
    initial_cores = _source_route_seeded_channel_initial_cores(
        ranks=config.ranks,
        basis_dim=int(fit_degree) + 1,
        constant_value=tf.reduce_sum(batch.weights * batch.target_values) / tf.reduce_sum(batch.weights),
    )
    result = FixedTTFitter().fit(
        product_basis=product_basis,
        samples=batch,
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
        "training_batch": batch,
        "training_manifest": training_manifest,
        "guard_points": guard_points,
        "guard_targets": guard_targets,
        "guard_weights": guard_weights,
        "line_points": line_points,
        "line_targets": guard_line_targets,
        "line_manifest": line_manifest,
    }


def _transport_from_fit(fit: Mapping[str, Any], convention) -> FixedTTSIRTTransport:
    defensive = TensorProductReferenceDensity(fit["product_basis"], convention)
    tau = _p59_author_sir_defensive_tau_tensor()
    identity = SquaredTTDensity.expected_branch_identity(
        sqrt_tt=fit["result"].fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
    )
    density = SquaredTTDensity(
        sqrt_tt=fit["result"].fitted_tt,
        defensive_density=defensive,
        tau=tau,
        normalizer_floor=tf.constant(1e-12, dtype=tf.float64),
        denominator_floor=tf.constant(1e-12, dtype=tf.float64),
        measure_convention=convention,
        branch_identity=identity,
    )
    return FixedTTSIRTTransport(
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


def _retained_from_p72_fit(
    *,
    fit: Mapping[str, Any],
    fit_data,
    components: SourceRouteSequentialDensityComponents,
    convention,
    target_dim: int,
    retained_sample_count: int,
    previous_axes: bool = False,
) -> Any:
    transport = _transport_from_fit(fit, convention)
    target = (
        _p59_author_sir_source_route_target(
            frame=fit_data.frame,
            shift_constant=fit_data.shift_constant,
            time_index=fit_data.time_index,
            components=components,
        )
        if int(fit_data.time_index) == 1
        else build_source_route_target(
            negative_log_physical_density_fn=lambda points: tf.zeros(
                [int(tf.shape(points)[1])],
                dtype=tf.float64,
            ),
            coordinate_frame=fit_data.frame,
            shift_constant=fit_data.shift_constant,
            time_index=fit_data.time_index,
        )
    )
    kwargs: dict[str, Any] = {}
    if previous_axes:
        kwargs["previous_marginal_keep_axes"] = tuple(range(target_dim // 2))
        kwargs["previous_marginal_input_axes"] = tuple(range(target_dim // 2, target_dim))
    spec = SourceRouteSequentialStepSpec(
        target=target,
        transport=SourceRouteTransportProtocol(transport),
        reference_samples=_p59_author_sir_unit_reference_points(int(retained_sample_count), int(target_dim)),
        measure_convention=convention,
        density_components=components,
        **kwargs,
    )
    if int(fit_data.time_index) == 1:
        return _p59_retained_object_from_spec(spec)
    return spec


def _condition_records_from_fit(fit: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    records: list[Mapping[str, Any]] = []
    fitter = FixedTTFitter()
    batch = fit["training_batch"]
    for state_name, cores in (
        ("initial", fit["initial_cores"]),
        ("final", fit["result"].fitted_tt.cores),
    ):
        for core_index in tuple(dict.fromkeys((0, len(fit["config"].ranks) // 2, len(fit["config"].ranks) - 2))):
            if core_index < 0 or core_index >= len(fit["config"].ranks) - 1:
                continue
            design = fitter._build_design_matrix(fit["product_basis"], batch.points, tuple(cores), int(core_index))
            solved = fitting._solve_scaled_augmented_ridge(
                design=design,
                target_values=batch.target_values,
                weights=batch.weights,
                ridge=fit["config"].ridge,
                column_scale_floor=fit["config"].column_scale_floor,
                stabilization_policy_id=fit["config"].stabilization_policy_id,
                solver_backend=fit["config"].solver_backend,
            )
            singular = tf.linalg.svd(solved.scaled_augmented_matrix, compute_uv=False)
            records.append(
                {
                    "state": state_name,
                    "core_index": int(core_index),
                    "scaled_augmented_condition_number": solved.scaled_augmented_condition_number,
                    "scaled_augmented_singular_values": singular,
                }
            )
    for record in fit["result"].core_update_statuses:
        records.append(dict(record))
    return tuple(records)


def _support_gate_for_data(*, role: str, data, fit_data) -> Mapping[str, Any]:
    return source_route.p72_support_clipping_coverage(
        role=role,
        points=data.local_fit_points,
        fit_points=fit_data.local_fit_points,
        clip_fraction=data.manifest.get("local_clip_fraction"),
        local_max_abs_before_clip=data.manifest.get("local_max_abs_before_clip"),
    )


def _line_gate_for_channel(
    *,
    fitted_tt,
    fit_data,
    endpoint_data,
    components: SourceRouteSequentialDensityComponents,
    previous_retained_object,
    target_scale: float,
) -> Mapping[str, Any]:
    line_points, manifest = source_route.p72_guard_line_points(
        fit_points=fit_data.local_fit_points,
        guard_points=endpoint_data.local_fit_points,
    )
    line_targets = _target_values_for_points(
        points=line_points,
        frame=fit_data.frame,
        shift_constant=fit_data.shift_constant,
        time_index=fit_data.time_index,
        components=components,
        previous_retained_object=previous_retained_object,
    )
    center = tf.reduce_mean(fit_data.local_fit_points, axis=1, keepdims=True)
    starts = fitted_tt.evaluate(tf.transpose(tf.repeat(center, repeats=3, axis=1)))
    gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=fitted_tt,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=starts,
        line_start_indices=manifest["line_start_indices"],
        target_scale=target_scale,
    )
    return {
        **gate,
        "line_points": line_points,
        "line_manifest": manifest,
        "channel_role": endpoint_data.manifest.get("diagnostic_construction", "guard"),
    }


def _step_gate_row(
    *,
    fit_data,
    guard_data,
    holdout_data,
    replay_data,
    fit: Mapping[str, Any],
    components: SourceRouteSequentialDensityComponents,
    previous_retained_object,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
) -> Mapping[str, Any]:
    fitted_tt = fit["result"].fitted_tt
    fit_target_scale = max(_weighted_rms(
        fit_data.target_values,
        tf.zeros_like(fit_data.target_values),
        fit_data.fit_weights,
    ), 1e-300)
    fit_gate = _cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=fit_data.local_fit_points,
        target_values=fit_data.target_values,
        weights=fit_data.fit_weights,
        target_scale=fit_target_scale,
    )
    guard_gate = _cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=fit["guard_points"],
        target_values=fit["guard_targets"],
        weights=fit["guard_weights"],
        target_scale=fit_target_scale,
    )
    holdout_gate = _cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=holdout_data.local_fit_points,
        target_values=holdout_data.target_values,
        weights=holdout_data.fit_weights,
        target_scale=fit_target_scale,
    )
    replay_gate = _cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=replay_data.local_fit_points,
        target_values=replay_data.target_values,
        weights=replay_data.fit_weights,
        target_scale=fit_target_scale,
    )
    residual_gates = {
        "rms_relative": max(
            fit_gate["rms_relative"],
            guard_gate["rms_relative"],
            holdout_gate["rms_relative"],
            replay_gate["rms_relative"],
        ),
        "max_relative": max(
            fit_gate["max_relative"],
            guard_gate["max_relative"],
            holdout_gate["max_relative"],
            replay_gate["max_relative"],
        ),
        "fit": fit_gate,
        "guard": guard_gate,
        "holdout": holdout_gate,
        "replay": replay_gate,
    }
    support_gates = {
        "fit": _support_gate_for_data(role="fit", data=fit_data, fit_data=fit_data),
        "guard": source_route.p72_support_clipping_coverage(
            role="guard",
            points=fit["guard_points"],
            fit_points=fit_data.local_fit_points,
            clip_fraction=guard_data.manifest.get("local_clip_fraction"),
            local_max_abs_before_clip=guard_data.manifest.get("local_max_abs_before_clip"),
        ),
        "holdout": _support_gate_for_data(role="holdout", data=holdout_data, fit_data=fit_data),
        "replay": _support_gate_for_data(role="replay", data=replay_data, fit_data=fit_data),
    }
    line_gates = {
        "guard": source_route.p72_line_probe_diagnostics(
            fitted_tt=fitted_tt,
            line_points=fit["line_points"],
            line_target_values=fit["line_targets"],
            start_prediction_values=fitted_tt.evaluate(
                tf.transpose(tf.repeat(tf.reduce_mean(fit_data.local_fit_points, axis=1, keepdims=True), repeats=3, axis=1))
            ),
            line_start_indices=fit["line_manifest"]["line_start_indices"],
            target_scale=fit_target_scale,
        ),
        "holdout": _line_gate_for_channel(
            fitted_tt=fitted_tt,
            fit_data=fit_data,
            endpoint_data=holdout_data,
            components=components,
            previous_retained_object=previous_retained_object,
            target_scale=fit_target_scale,
        ),
        "replay": _line_gate_for_channel(
            fitted_tt=fitted_tt,
            fit_data=fit_data,
            endpoint_data=replay_data,
            components=components,
            previous_retained_object=previous_retained_object,
            target_scale=fit_target_scale,
        ),
    }
    line_status = "block" if any(gate.get("status") == "block" for gate in line_gates.values()) else "pass"
    condition_gate = source_route.p72_condition_effective_rank_gate(_condition_records_from_fit(fit))
    normalizer_gate = source_route.p72_full_normalizer_gate(
        _normalizer_terms(fitted_tt, fit["product_basis"], fit["product_basis"].convention)
    )
    rank_activity = _p70_channel_activity_diagnostics(
        cores=fitted_tt.cores,
        target_dim=int(target_dim),
        fit_rank=int(fit_rank),
    )
    rank_gate = {
        **rank_activity,
        "status": "ok" if rank_activity.get("status") == "rank_channel_activity_pass" else rank_activity.get("status"),
    }
    all_line_points = tf.concat(
        [
            fit["line_points"],
            line_gates["holdout"]["line_points"],
            line_gates["replay"]["line_points"],
        ],
        axis=1,
    )
    provenance = source_route.p72_provenance_manifest(
        branch_identity=fit["result"].branch_hash.value,
        target_values=fit_data.target_values,
        frame_hash=_p69_frame_hash(fit_data.frame),
        shift_constant=fit_data.shift_constant,
        fit_points=fit_data.local_fit_points,
        guard_points=fit["guard_points"],
        audit_points=tf.concat([holdout_data.local_fit_points, replay_data.local_fit_points], axis=1),
        line_points=all_line_points,
    )
    summary = source_route.p72_gate_summary(
        residual_gates=residual_gates,
        support_gates=support_gates,
        normalizer_gate=normalizer_gate,
        line_gate={"status": line_status, "channels": line_gates},
        condition_gate=condition_gate,
        rank_activity=rank_gate,
        provenance=provenance,
    )
    return {
        "time_index": int(fit_data.time_index),
        "fit_status": fit["result"].status.value,
        "fit_termination_reason": fit["result"].termination_reason,
        "degree": int(fit_degree),
        "rank": int(fit_rank),
        "fit_point_count": int(fit_data.local_fit_points.shape[1]),
        "guard_point_count": int(fit["guard_points"].shape[1]),
        "audit_point_count": int(holdout_data.local_fit_points.shape[1] + replay_data.local_fit_points.shape[1]),
        "training_batch_manifest": fit["training_manifest"],
        "residual_gates": residual_gates,
        "support_gates": support_gates,
        "normalizer_gate": normalizer_gate,
        "line_gates": line_gates,
        "condition_effective_rank_gate": condition_gate,
        "rank_activity": rank_gate,
        "provenance": provenance,
        "gate_summary": summary,
        "status": summary["status"],
        "nonclaims": NONCLAIMS,
    }


def _smoke_clouds() -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    fit = tf.constant(
        [
            [-1.0, 0.0, 1.0],
            [-0.5, 0.0, 0.5],
        ],
        dtype=tf.float64,
    )
    guard = tf.constant(
        [
            [-0.75, 0.75],
            [-0.25, 0.25],
        ],
        dtype=tf.float64,
    )
    audit = tf.constant(
        [
            [-0.9, 0.9],
            [-0.1, 0.1],
        ],
        dtype=tf.float64,
    )
    return fit, guard, audit


def _smoke_targets(points: tf.Tensor) -> tf.Tensor:
    return _SmokeFittedTT().evaluate(tf.transpose(points))


def p72_smoke_rows() -> Mapping[str, Mapping[str, Any]]:
    fit, guard, audit = _smoke_clouds()
    fitted = _SmokeFittedTT()
    fit_targets = _smoke_targets(fit)
    guard_targets = _smoke_targets(guard)
    audit_targets = _smoke_targets(audit)
    training_batch, training_manifest = source_route.p72_training_batch_from_fit_and_guard(
        fit_points=fit,
        fit_target_values=fit_targets,
        fit_weights=tf.ones([int(fit.shape[1])], dtype=tf.float64),
        guard_points=guard,
        guard_target_values=guard_targets,
        guard_weights=tf.ones([int(guard.shape[1])], dtype=tf.float64),
    )
    line_points, line_manifest = source_route.p72_guard_line_points(
        fit_points=fit,
        guard_points=guard,
    )
    line_targets = _smoke_targets(line_points)
    support_gates = {
        role: source_route.p72_support_clipping_coverage(
            role=role,
            points=cloud,
            fit_points=fit,
            clip_fraction=0.0,
            local_max_abs_before_clip=1.0,
        )
        for role, cloud in (
            ("fit", fit),
            ("guard", guard),
            ("holdout", audit),
            ("replay", audit),
        )
    }
    normalizer_gate = source_route.p72_full_normalizer_gate(
        {
            "mixture_normalizer": 2.0,
            "sqrt_square_normalizer": 1.5,
            "defensive_tau": 1e-8,
            "defensive_normalizer": 1.0,
            "log_transport_normalizer": 0.0,
        }
    )
    line_gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=fitted,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=fitted.evaluate(
            tf.constant([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], dtype=tf.float64)
        ),
        line_start_indices=line_manifest["line_start_indices"],
        target_scale=1.0,
    )
    condition_gate = source_route.p72_condition_effective_rank_gate(
        (
            {
                "scaled_augmented_condition_number": 1e5,
                "effective_rank": 2.0,
            },
        )
    )
    provenance = source_route.p72_provenance_manifest(
        branch_identity="p72-smoke-fixed-branch",
        target_values=fit_targets,
        frame_hash="p72-smoke-frame",
        shift_constant=0.0,
        fit_points=fit,
        guard_points=guard,
        audit_points=audit,
        line_points=line_points,
    )
    predictions = fitted.evaluate(training_batch.points)
    residual = tf.abs(predictions - training_batch.target_values)
    residual_gates = {
        "rms_relative": float(tf.sqrt(tf.reduce_mean(tf.square(residual))).numpy()),
        "max_relative": float(tf.reduce_max(residual).numpy()),
    }
    gate_summary = source_route.p72_gate_summary(
        residual_gates=residual_gates,
        support_gates=support_gates,
        normalizer_gate=normalizer_gate,
        line_gate=line_gate,
        condition_gate=condition_gate,
        rank_activity={"status": "ok", "smoke_only": True},
        provenance=provenance,
    )
    return {
        "p72_smoke_row": {
            "label": "p72_smoke_row",
            "status": gate_summary["status"],
            "smoke_only_not_phase5_evidence": True,
            "fit_point_count": int(fit.shape[1]),
            "guard_point_count": int(guard.shape[1]),
            "audit_point_count": int(audit.shape[1]),
            "training_batch_manifest": training_manifest,
            "line_manifest": line_manifest,
            "support_gates": support_gates,
            "normalizer_gate": normalizer_gate,
            "line_gate": line_gate,
            "condition_effective_rank_gate": condition_gate,
            "provenance": provenance,
            "gate_summary": gate_summary,
            "nonclaims": NONCLAIMS,
        }
    }


def p72_smoke_payload(output: Path, command: str) -> Mapping[str, Any]:
    rows = p72_smoke_rows()
    failed = tuple(
        label
        for label, row in rows.items()
        if row.get("status") != source_route.P72_PASS_STATUS
    )
    gate_summary = {
        "overall_status": "pass" if not failed else "fail",
        "failed_row_labels": failed,
        "smoke_only_not_phase5_evidence": True,
        "schema_only_sentinel_present": False,
        "phase5_diagnostic_executed": False,
        "nonclaims": NONCLAIMS,
    }
    base_payload = p72_diagnostic_base_payload(
        rows=rows,
        output=output,
        status="P72_PHASE5A_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE",
        command=command,
        gate_summary=gate_summary,
    )
    return {
        **base_payload,
        "diagnostic_scope": "p72_phase5a_smoke_real_gate_path_not_phase5_evidence",
        "evidence_contract": {
            "question": (
                "Does the P72 script default gate path now emit a non-schema "
                "bounded smoke JSON artifact?"
            ),
            "baseline_comparator": "Phase 4 schema-only P72 script output.",
            "primary_criterion": (
                "Smoke JSON avoids the Phase 4 schema-only sentinel, uses the "
                "P72 gate helpers, records audit exclusion, and is explicitly "
                "labeled not Phase 5 evidence."
            ),
            "veto_diagnostics": (
                "schema-only sentinel present",
                "audit cloud used for training",
                "missing direct line target evaluation",
                "missing full normalizer gate",
                "missing provenance hashes",
                "low-level solver veto lowered from 1e14",
                "source-faithfulness overclaim",
            ),
            "explanatory_only": (
                "tiny deterministic smoke magnitudes",
                "synthetic row pass status",
            ),
            "nonclaims": NONCLAIMS,
        },
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p72-phase5a-real-diagnostic-runner-repair-subplan-2026-06-17.md"
        ),
        "source_route_controls": {
            **base_payload["source_route_controls"],
            "script_role": "p72_phase5a_smoke_real_gate_path",
            "phase5_diagnostic_executed": False,
            "smoke_only_not_phase5_evidence": True,
            "schema_only_default_path": False,
        },
        "run_manifest": {
            **base_payload["run_manifest"],
            "random_seeds": {
                "guard": source_route.p72_support_certified_policy()["guard_seeds"],
                "audit": source_route.p72_support_certified_policy()["audit_seeds"],
                "smoke": "deterministic_tiny_tensor_cloud_no_random_draws",
            },
        },
    }


def p72_phase4_schema_payload(output: Path) -> Mapping[str, Any]:
    return p72_diagnostic_base_payload(
        rows={},
        output=output,
        status="PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED",
        command=EXPECTED_COMMAND,
        gate_summary={
            "overall_status": "not_executed",
            "reason": "Phase 5 repaired lower-gate diagnostic requires a separate reviewed subplan",
        },
    )


def _build_p72_row(
    *,
    label: str,
    fit_degree: int,
    fit_rank: int,
    fit_sample_count: int,
) -> Mapping[str, Any]:
    model = zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    d = model.parameter_dim()
    m = model.state_dim()
    target_dim = d + 2 * m
    convention = _p59_reference_convention()
    prior_log_density, transition_log_density, likelihood_t1 = _p59_author_sir_source_density_callbacks(
        model,
        observations[1],
    )
    _, _, likelihood_t2 = _p59_author_sir_source_density_callbacks(model, observations[2])
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
    fit_data1 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=int(fit_sample_count),
    )
    guard_data1 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        prior_seed=source_route.P72_GUARD_STEP1_PRIOR_SEED,
        process_noise_seed=source_route.P72_GUARD_STEP1_PROCESS_SEED,
        construction="p72_step1_guard_distinct_diagnostic_seed",
    )
    holdout_data1 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        prior_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
        construction="p69_step1_holdout_distinct_diagnostic_seed",
    )
    replay_data1 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        prior_seed=source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
        construction="p69_step1_replay_distinct_diagnostic_seed",
    )
    fit1 = _fit_p72_step(
        fit_data=fit_data1,
        guard_data=guard_data1,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        branch_seed=f"p72-phase5-step1-{label}",
        convention=convention,
        components=components1,
        previous_retained_object=None,
    )
    step1 = _step_gate_row(
        fit_data=fit_data1,
        guard_data=guard_data1,
        holdout_data=holdout_data1,
        replay_data=replay_data1,
        fit=fit1,
        components=components1,
        previous_retained_object=None,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
    )
    step1_normalizer_exception = step1.get("normalizer_gate", {}).get("normalizer_exception")
    if step1_normalizer_exception not in (None, "", "None"):
        step1_reasons = tuple(step1.get("gate_summary", {}).get("reasons", ()))
        step2 = _skipped_step_after_prior_gate_block(
            time_index=2,
            fit_degree=fit_degree,
            fit_rank=fit_rank,
            fit_sample_count=fit_sample_count,
            skipped_after_time_index=1,
            skipped_reasons=step1_reasons,
        )
        return {
            "label": str(label),
            "degree": int(fit_degree),
            "rank": int(fit_rank),
            "fit_sample_count": int(fit_sample_count),
            "status": source_route.P72_BLOCK_STATUS,
            "phase5_diagnostic_executed": True,
            "smoke_only_not_phase5_evidence": False,
            "steps": (step1, step2),
            "sequential_status": "not_run_prior_step_normalizer_blocked",
            "sequential_log_marginal_likelihood": None,
            "row_block_reason": "step1_normalizer_exception_blocks_retained_object",
            "nonclaims": NONCLAIMS,
        }
    retained1 = _retained_from_p72_fit(
        fit=fit1,
        fit_data=fit_data1,
        components=components1,
        convention=convention,
        target_dim=target_dim,
        retained_sample_count=int(fit_sample_count),
    )
    fit_data2 = _p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        fit_sample_count=int(fit_sample_count),
        previous_retained_object=retained1,
    )
    guard_data2 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        process_noise_seed=source_route.P72_GUARD_STEP2_PROCESS_SEED,
        construction="p72_step2_guard_distinct_diagnostic_seed",
    )
    holdout_data2 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        process_noise_seed=source_route.P72_AUDIT_STEP2_HOLDOUT_PROCESS_SEED,
        construction="p69_step2_holdout_distinct_diagnostic_seed",
    )
    replay_data2 = _p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        diagnostic_sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        process_noise_seed=source_route.P72_AUDIT_STEP2_REPLAY_PROCESS_SEED,
        construction="p69_step2_replay_distinct_diagnostic_seed",
    )
    fit2 = _fit_p72_step(
        fit_data=fit_data2,
        guard_data=guard_data2,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        branch_seed=f"p72-phase5-step2-{label}",
        convention=convention,
        components=components2,
        previous_retained_object=retained1,
    )
    step2 = _step_gate_row(
        fit_data=fit_data2,
        guard_data=guard_data2,
        holdout_data=holdout_data2,
        replay_data=replay_data2,
        fit=fit2,
        components=components2,
        previous_retained_object=retained1,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
    )
    spec1 = SourceRouteSequentialStepSpec(
        target=_p59_author_sir_source_route_target(
            frame=fit_data1.frame,
            shift_constant=fit_data1.shift_constant,
            time_index=1,
            components=components1,
        ),
        transport=SourceRouteTransportProtocol(_transport_from_fit(fit1, convention)),
        reference_samples=_p59_author_sir_unit_reference_points(int(fit_sample_count), target_dim),
        measure_convention=convention,
        density_components=components1,
    )
    spec2 = SourceRouteSequentialStepSpec(
        target=build_source_route_target(
            negative_log_physical_density_fn=lambda points: tf.zeros(
                [int(tf.shape(points)[1])],
                dtype=tf.float64,
            ),
            coordinate_frame=fit_data2.frame,
            shift_constant=fit_data2.shift_constant,
            time_index=2,
        ),
        transport=SourceRouteTransportProtocol(_transport_from_fit(fit2, convention)),
        reference_samples=_p59_author_sir_unit_reference_points(int(fit_sample_count), target_dim),
        measure_convention=convention,
        density_components=components2,
        previous_marginal_keep_axes=tuple(range(d + m)),
        previous_marginal_input_axes=tuple(range(d + m, d + 2 * m)),
    )
    sequential_status = "not_run_gate_failed"
    sequential_log_marginal_likelihood = None
    if step1["status"] == source_route.P72_PASS_STATUS and step2["status"] == source_route.P72_PASS_STATUS:
        sequential = source_route_run_sequential_fixed_hmc(step_specs=(spec1, spec2))
        sequential_status = sequential.sequential_status
        sequential_log_marginal_likelihood = float(sequential.log_marginal_likelihood.numpy())
    row_status = (
        source_route.P72_PASS_STATUS
        if step1["status"] == source_route.P72_PASS_STATUS and step2["status"] == source_route.P72_PASS_STATUS
        else source_route.P72_BLOCK_STATUS
    )
    return {
        "label": str(label),
        "degree": int(fit_degree),
        "rank": int(fit_rank),
        "fit_sample_count": int(fit_sample_count),
        "status": row_status,
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "steps": (step1, step2),
        "sequential_status": sequential_status,
        "sequential_log_marginal_likelihood": sequential_log_marginal_likelihood,
        "nonclaims": NONCLAIMS,
    }


def p72_phase5_rows() -> Mapping[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for label, degree, rank, fit_count in PHASE5_ROW_SPECS:
        try:
            rows[label] = _build_p72_row(
                label=label,
                fit_degree=degree,
                fit_rank=rank,
                fit_sample_count=fit_count,
            )
        except Exception as exc:
            rows[label] = {
                "label": label,
                "degree": int(degree),
                "rank": int(rank),
                "fit_sample_count": int(fit_count),
                "status": source_route.P72_BLOCK_STATUS,
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "block_reason": "p72_phase5_row_exception_fail_closed",
                "nonclaims": NONCLAIMS,
            }
    return rows


def p72_phase5_payload(output: Path, command: str) -> Mapping[str, Any]:
    rows = p72_phase5_rows()
    failed = tuple(
        label
        for label, row in rows.items()
        if row.get("status") != source_route.P72_PASS_STATUS
    )
    gate_summary = {
        "overall_status": "pass" if not failed else "block",
        "failed_row_labels": failed,
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "schema_only_sentinel_present": False,
        "baseline_comparator": "P70 Phase 6h root-cause probes",
        "nonclaims": NONCLAIMS,
    }
    base = p72_diagnostic_base_payload(
        rows=rows,
        output=output,
        status=P72_PHASE5_PASS_STATUS if not failed else P72_PHASE5_BLOCK_STATUS,
        command=command,
        gate_summary=gate_summary,
    )
    return {
        **base,
        "diagnostic_scope": "p72_phase5_support_certified_lower_gate_real_bounded_rows",
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p72-phase5-repaired-lower-gate-diagnostic-subplan-2026-06-17.md"
        ),
        "evidence_contract": {
            "question": (
                "Does the support-certified fixed-fit gate reduce the P70 Phase 6h "
                "off-cloud/conditioning blocker on bounded diagnostic rows?"
            ),
            "baseline_comparator": (
                "P70 Phase 6h row A off-cloud line/residual growth and row B "
                "scaled condition-veto evidence."
            ),
            "primary_criterion": (
                "All bounded P72 rows and both time steps must pass fit/guard/audit "
                "residual, line, support, normalizer, provenance, condition/effective-rank, "
                "and rank-activity gates with audit clouds excluded from coefficient selection."
            ),
            "veto_diagnostics": (
                "nonfinite target or prediction",
                "missing direct line target",
                "audit cloud used for training",
                "support block",
                "normalizer block",
                "line block",
                "condition/effective-rank block",
                "rank activity block",
                "source-faithfulness overclaim",
            ),
            "explanatory_only": (
                "raw residual magnitudes",
                "support warning distances",
                "runtime",
            ),
            "nonclaims": NONCLAIMS,
        },
        "source_route_controls": {
            **base["source_route_controls"],
            "script_role": "p72_phase5_real_bounded_diagnostic_runner",
            "phase5_diagnostic_executed": True,
            "smoke_only_not_phase5_evidence": False,
            "schema_only_default_path": False,
            "p70_baseline_artifact": (
                "docs/plans/"
                "bayesfilter-highdim-zhao-cui-p70-phase6h-root-cause-probes-2026-06-17.json"
            ),
        },
        "run_manifest": {
            **base["run_manifest"],
            "random_seeds": {
                "model_simulation": 5901,
                "fit": {
                    "step1_prior": 6301,
                    "step1_process": 6401,
                    "step2_process": 6402,
                },
                "guard": source_route.p72_support_certified_policy()["guard_seeds"],
                "audit": source_route.p72_support_certified_policy()["audit_seeds"],
            },
            "row_specs": PHASE5_ROW_SPECS,
            "cpu_only_intent": "CUDA_VISIBLE_DEVICES=-1",
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--smoke-only", action="store_true")
    args = parser.parse_args(argv)
    command_parts = [EXPECTED_COMMAND]
    if args.output != DEFAULT_OUTPUT:
        command_parts.extend(["--output", str(args.output)])
    if args.schema_only:
        command_parts.append("--schema-only")
    if args.smoke_only:
        command_parts.append("--smoke-only")
    command = " ".join(command_parts)
    if args.schema_only:
        payload = p72_phase4_schema_payload(args.output)
    elif args.smoke_only:
        payload = p72_smoke_payload(args.output, command)
    else:
        payload = p72_phase5_payload(args.output, command)
    _write_payload(args.output, payload)
    print(json.dumps({"p72_status": payload["status"], "gate_summary": _jsonable(payload["gate_summary"])}, sort_keys=True))
    return 0 if payload["gate_summary"].get("overall_status") in {"pass", "not_executed", "block"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
