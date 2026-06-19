#!/usr/bin/env python
"""P75 stochastic density-training smoke runner.

The smoke path is synthetic and tiny.  It is not a Phase-4 target pilot and it
does not provide lower-gate, validation, HMC, rank, or scaling evidence.
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

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf

from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.diagnostics import DensityMeasure, MassMeasure, MeasureConvention
from bayesfilter.highdim import source_route
from bayesfilter.highdim.stochastic_density_training import (
    P75_NONCLAIMS,
    P75_SCHEMA_STATUS,
    P75_SMOKE_STATUS,
    P75ObjectiveBatch,
    P75TrainableTTConfig,
    TrainableFunctionalTT,
    config_payload,
    make_adam_optimizer,
    prefit_terms_payload,
    terms_payload,
)


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-smoke-2026-06-17.json"
)
P75_PHASE3_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-phase3-optin-implementation-subplan-2026-06-17.md"
)
P75_PHASE8_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p75-phase8-source-guided-prefit-implementation-subplan-2026-06-18.md"
)
EXPECTED_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p75_stochastic_density_training_pilot.py"
)
TARGET_TRAIN_PRIOR_SEED_BASE = 875_000
TARGET_TRAIN_PROCESS_SEED_BASE = 876_000
P75_RANDOM_INIT_MODE = "random"
P75_CALIBRATED_CONSTANT_INIT_MODE = "calibrated_constant"
P75_SOURCE_GUIDED_PREFIT_INIT_MODE = "source_guided_prefit"
P75_COMPARE_BASE_INIT_MODES = (P75_RANDOM_INIT_MODE, P75_CALIBRATED_CONSTANT_INIT_MODE)
P75_INIT_MODES = P75_COMPARE_BASE_INIT_MODES + (P75_SOURCE_GUIDED_PREFIT_INIT_MODE,)


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


def _as_float(value: Any) -> float:
    if hasattr(value, "numpy"):
        return float(value.numpy())
    return float(value)


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


def _convention() -> MeasureConvention:
    return MeasureConvention(
        density_measure=DensityMeasure.REFERENCE_MEASURE,
        mass_measure=MassMeasure.REFERENCE_MEASURE,
        reference_weight_name="omega",
    )


def _synthetic_config() -> P75TrainableTTConfig:
    product_basis = ProductBasis(
        [LegendreBasis1D(BoundedInterval(-1.0, 1.0), 2) for _ in range(2)],
        _convention(),
    )
    return P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=(1, 2, 1),
        tau=tf.constant(1e-6, dtype=tf.float64),
        normalizer_floor=tf.constant(1e-14, dtype=tf.float64),
        denominator_floor=tf.constant(1e-300, dtype=tf.float64),
        l2_weight=tf.constant(1e-6, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=10.0,
        seed=7501,
        metadata={
            "fixture": "p75_synthetic_smoke",
            "smoke_only_not_pilot_evidence": True,
        },
    )


def _synthetic_batch() -> P75ObjectiveBatch:
    points = tf.constant(
        [
            [-0.75, -0.25],
            [-0.25, 0.50],
            [0.25, -0.50],
            [0.75, 0.25],
        ],
        dtype=tf.float64,
    )
    target_values = tf.exp(-0.25 * tf.reduce_sum(tf.square(points), axis=1))
    weights = tf.constant([1.0, 2.0, 1.5, 0.5], dtype=tf.float64)
    records = tuple(
        {
            "point_id": f"p75-smoke-{index}",
            "cloud_hash": "p75-smoke-training-cloud",
            "role": "fit",
            "source_channel": "synthetic_smoke",
        }
        for index in range(int(points.shape[0]))
    )
    forbidden = (
        {
            "point_id": "p75-smoke-audit",
            "cloud_hash": "p75-smoke-audit-cloud",
            "role": "audit",
            "source_channel": "synthetic_smoke_audit",
        },
    )
    return P75ObjectiveBatch(
        points=points,
        target_values=target_values,
        weights=weights,
        point_records=records,
        forbidden_audit_records=forbidden,
        provenance_label="p75_synthetic_smoke_training_only",
    )


def _base_payload(output: Path, command: str) -> Mapping[str, Any]:
    return {
        "metadata_date": "2026-06-17",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p75-stochastic-density-training-master-program-2026-06-17.md"
        ),
        "subplan": (
            P75_PHASE3_SUBPLAN
        ),
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
            "cpu_only_intent": "CUDA_VISIBLE_DEVICES=-1",
        },
        "nonclaims": P75_NONCLAIMS,
    }


def schema_payload(output: Path, command: str) -> Mapping[str, Any]:
    config = _synthetic_config()
    return {
        **_base_payload(output, command),
        "status": P75_SCHEMA_STATUS,
        "diagnostic_scope": "p75_schema_only_not_training_not_pilot",
        "schema_only": True,
        "smoke_only_not_pilot_evidence": True,
        "phase4_target_pilot_executed": False,
        "config": config_payload(config),
        "smoke_bounds": {
            "synthetic_fixture_only": True,
            "max_dimension": 2,
            "max_degree": 2,
            "max_rank": 2,
            "max_batch_size": 8,
            "max_optimizer_steps": 2,
            "zhao_cui_fresh_batches_allowed": False,
        },
        "target_pilot_option": {
            "available": True,
            "executed": False,
            "default_degree": 2,
            "default_rank": 4,
            "default_batch_size": 1024,
            "default_batches": 500,
            "requires_phase4_review": True,
        },
        "p73_regression": source_route.p73_density_aware_optimizer_status(),
        "gate_summary": {
            "overall_status": "not_executed",
            "schema_only": True,
            "smoke_only_not_pilot_evidence": True,
            "phase4_target_pilot_executed": False,
        },
}


def _rank_tuple(dimension: int, rank: int) -> tuple[int, ...]:
    d = int(dimension)
    r = int(rank)
    if d <= 0 or r <= 0:
        raise ValueError("dimension and rank must be positive")
    return tuple([1] + [r] * (d - 1) + [1])


def _target_config(*, dimension: int, degree: int, rank: int, seed: int) -> P75TrainableTTConfig:
    product_basis = ProductBasis(
        [LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(degree)) for _ in range(int(dimension))],
        source_route._p59_reference_convention(),
    )
    return P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=_rank_tuple(int(dimension), int(rank)),
        tau=source_route._p59_author_sir_defensive_tau_tensor(),
        normalizer_floor=tf.constant(source_route.P72_SQRT_SQUARE_NORMALIZER_FLOOR, dtype=tf.float64),
        denominator_floor=tf.constant(source_route.P73_EPS_LOG, dtype=tf.float64),
        l2_weight=tf.constant(1e-8, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=100.0,
        seed=int(seed),
        metadata={
            "fixture": "p75_author_sir_step1_target_pilot",
            "extension_or_invention": True,
        },
    )


def _constant_path_initial_cores(config: P75TrainableTTConfig, constant_value: tf.Tensor) -> tuple[tf.Tensor, ...]:
    value = tf.convert_to_tensor(constant_value, dtype=tf.float64)
    if value.shape.rank != 0 or not bool(tf.math.is_finite(value).numpy()):
        raise ValueError("constant_value must be a finite scalar")
    if bool((value <= 0.0).numpy()):
        raise ValueError("constant_value must be positive")
    cores = []
    for axis, basis_dim in enumerate(config.product_basis.basis_dim_tuple()):
        core = tf.zeros(
            [config.ranks[axis], basis_dim, config.ranks[axis + 1]],
            dtype=tf.float64,
        )
        entry = value if axis == 0 else tf.constant(1.0, dtype=tf.float64)
        cores.append(tf.tensor_scatter_nd_update(core, [[0, 0, 0]], [entry]))
    return tuple(cores)


def _calibrated_constant_initial_cores(
    config: P75TrainableTTConfig,
    anchor_batch: P75ObjectiveBatch,
) -> tuple[tuple[tf.Tensor, ...], Mapping[str, Any]]:
    targets = tf.convert_to_tensor(anchor_batch.target_values, dtype=tf.float64)
    weights = tf.convert_to_tensor(anchor_batch.weights, dtype=tf.float64)
    if targets.shape.rank != 1 or weights.shape != targets.shape:
        raise ValueError("anchor targets and weights must be vectors")
    weighted_target_square = (
        tf.reduce_sum(weights * tf.square(targets)) / tf.reduce_sum(weights)
    )
    floor = tf.constant(1e-300, dtype=tf.float64)
    constant_value = tf.sqrt(tf.maximum(weighted_target_square, floor))
    cores = _constant_path_initial_cores(config, constant_value)
    return cores, {
        "mode": P75_CALIBRATED_CONSTANT_INIT_MODE,
        "source": "source_route_anchor_training_cloud_only",
        "uses_audit_data": False,
        "anchor_point_count": int(anchor_batch.points.shape[0]),
        "weighted_target_square_mean": weighted_target_square,
        "constant_path_value": constant_value,
    }


def _trainer_for_init_mode(
    config: P75TrainableTTConfig,
    *,
    init_mode: str,
    anchor_batch: P75ObjectiveBatch,
) -> tuple[TrainableFunctionalTT, Mapping[str, Any]]:
    mode = str(init_mode)
    if mode == P75_RANDOM_INIT_MODE:
        return TrainableFunctionalTT(config), {
            "mode": P75_RANDOM_INIT_MODE,
            "source": "stateless_random_small_cores",
            "uses_audit_data": False,
        }
    if mode == P75_CALIBRATED_CONSTANT_INIT_MODE:
        cores, payload = _calibrated_constant_initial_cores(config, anchor_batch)
        return TrainableFunctionalTT(config, initial_cores=cores), payload
    if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE:
        cores, constant_payload = _calibrated_constant_initial_cores(config, anchor_batch)
        return TrainableFunctionalTT(config, initial_cores=cores), {
            "mode": P75_SOURCE_GUIDED_PREFIT_INIT_MODE,
            "source": "source_route_training_cloud_square_root_prefit",
            "uses_audit_data": False,
            "base_initializer": constant_payload,
            "prefit_role": "training_only_warm_start_not_validation",
        }
    raise ValueError(f"unknown init mode: {mode}")


def _run_source_guided_prefit(
    trainer: TrainableFunctionalTT,
    config: P75TrainableTTConfig,
    prefit_data_sequence,
    *,
    prefit_steps: int,
    max_seconds: float,
) -> Mapping[str, Any]:
    if int(prefit_steps) <= 0:
        raise ValueError("source_guided_prefit requires prefit_steps > 0")
    if int(prefit_steps) > len(prefit_data_sequence):
        raise ValueError("prefit_steps exceeds available training guide batches")
    optimizer = make_adam_optimizer(config)
    reference_cores = tuple(tf.identity(core) for core in trainer.variables)
    trace = []
    completed = 0
    final_terms = None
    stop_reason = "prefit_steps_completed"
    for step in range(int(prefit_steps)):
        elapsed = time.monotonic() - RUN_START
        if elapsed > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_next_prefit_batch"
            break
        batch = _target_batch_from_data(
            prefit_data_sequence[step],
            label=f"p75_source_guided_prefit_batch_{step}",
        )
        terms = trainer.square_root_prefit_step(
            batch,
            optimizer,
            reference_cores=reference_cores,
            reference_l2_weight=config.l2_weight,
            scale_floor=config.denominator_floor,
        )
        final_terms = terms
        completed += 1
        if step in {0, int(prefit_steps) - 1} or (step + 1) % 10 == 0:
            trace.append(
                {
                    "step": step + 1,
                    "terms": prefit_terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
                    "batch_label": batch.provenance_label,
                }
            )
    if final_terms is None:
        raise RuntimeError("source_guided_prefit produced no prefit step")
    return {
        "requested_steps": int(prefit_steps),
        "completed_steps": int(completed),
        "stop_reason": stop_reason,
        "uses_audit_data": False,
        "guide_source": "source_route_training_clouds_only",
        "reference_regularization": "distance_to_calibrated_constant_initializer",
        "final_terms": prefit_terms_payload(final_terms),
        "trace": trace,
    }


def _target_components(model, observations):
    prior_log_density, transition_log_density, likelihood = (
        source_route._p59_author_sir_source_density_callbacks(model, observations[1])
    )
    return source_route.SourceRouteSequentialDensityComponents(
        parameter_dim=model.parameter_dim(),
        state_dim=model.state_dim(),
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood,
        prior_log_density_fn=prior_log_density,
    )


def _target_values_for_reference_cloud(
    *,
    local_points: tf.Tensor,
    frame,
    shift_constant,
    components,
) -> tf.Tensor:
    local = tf.convert_to_tensor(local_points, dtype=tf.float64)
    if local.shape.rank != 2 or int(local.shape[0]) != int(frame.dimension):
        raise ValueError("local_points must have source-route shape [dimension, point_count]")
    physical = tf.linalg.matmul(frame.matrix, local) + frame.mu[:, tf.newaxis]
    negative_log_physical = components.negative_log_physical_density(
        physical_points=physical,
        time_index=1,
        previous_retained_object=None,
    )
    local_negative_log = negative_log_physical - frame.log_abs_det()
    shifted = source_route.source_route_shifted_negative_log_target(
        negative_log_target=local_negative_log,
        shift_constant=shift_constant,
    )
    return tf.exp(-0.5 * shifted)


def _target_values_for_points(*, points: tf.Tensor, frame, shift_constant, components) -> tf.Tensor:
    local = tf.convert_to_tensor(points, dtype=tf.float64)
    if local.shape.rank != 2 or int(local.shape[1]) != int(frame.dimension):
        raise ValueError("points must have P75 batch shape [point_count, dimension]")
    return _target_values_for_reference_cloud(
        local_points=tf.transpose(local),
        frame=frame,
        shift_constant=shift_constant,
        components=components,
    )


def _target_batch_from_data(data, *, label: str) -> P75ObjectiveBatch:
    return P75ObjectiveBatch(
        points=tf.transpose(data.local_fit_points),
        target_values=data.target_values,
        weights=data.fit_weights,
        provenance_label=str(label),
    )


def _weighted_residual(predicted: tf.Tensor, target: tf.Tensor, weights: tf.Tensor) -> Mapping[str, Any]:
    pred = tf.reshape(tf.convert_to_tensor(predicted, dtype=tf.float64), [-1])
    values = tf.reshape(tf.convert_to_tensor(target, dtype=tf.float64), [-1])
    weight = tf.reshape(tf.convert_to_tensor(weights, dtype=tf.float64), [-1])
    residual = tf.abs(pred - values)
    raw_rms = tf.sqrt(tf.reduce_sum(weight * tf.square(pred - values)) / tf.reduce_sum(weight))
    target_scale = tf.maximum(
        tf.sqrt(tf.reduce_sum(weight * tf.square(values)) / tf.reduce_sum(weight)),
        tf.constant(1e-300, dtype=tf.float64),
    )
    return {
        "raw_rms": raw_rms,
        "max_abs_residual": tf.reduce_max(residual),
        "target_scale": target_scale,
        "rms_relative": raw_rms / target_scale,
        "max_relative": tf.reduce_max(residual) / target_scale,
    }


def _audit_payload(*, trainer: TrainableFunctionalTT, fit_points: tf.Tensor, frame, shift_constant, components, model, observations, sample_count: int) -> Mapping[str, Any]:
    audit_holdout = source_route._p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(sample_count),
        frame=frame,
        shift_constant=shift_constant,
        prior_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
        construction="p75_step1_audit_holdout_seed",
    )
    audit_replay = source_route._p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(sample_count),
        frame=frame,
        shift_constant=shift_constant,
        prior_seed=source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
        construction="p75_step1_audit_replay_seed",
    )
    ftt = trainer.snapshot_functional_tt()
    holdout_pred = ftt.evaluate(tf.transpose(audit_holdout.local_fit_points))
    replay_pred = ftt.evaluate(tf.transpose(audit_replay.local_fit_points))
    holdout = _weighted_residual(
        holdout_pred,
        audit_holdout.target_values,
        audit_holdout.fit_weights,
    )
    replay = _weighted_residual(
        replay_pred,
        audit_replay.target_values,
        audit_replay.fit_weights,
    )
    line_points, line_manifest = source_route.p72_guard_line_points(
        fit_points=fit_points,
        guard_points=audit_holdout.local_fit_points,
    )
    line_targets = _target_values_for_reference_cloud(
        local_points=line_points,
        frame=frame,
        shift_constant=shift_constant,
        components=components,
    )
    center = tf.reduce_mean(fit_points, axis=1, keepdims=True)
    start_predictions = ftt.evaluate(
        tf.transpose(tf.repeat(center, repeats=3, axis=1))
    )
    target_scale = max(float(holdout["target_scale"].numpy()), 1e-300)
    line_gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=ftt,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=start_predictions,
        line_start_indices=line_manifest["line_start_indices"],
        target_scale=target_scale,
    )
    status = "pass"
    reasons = []
    if float(holdout["rms_relative"].numpy()) > source_route.P72_RESIDUAL_RMS_REL_VETO:
        status = "block"
        reasons.append("holdout_rms_relative_veto")
    if float(holdout["max_relative"].numpy()) > source_route.P72_RESIDUAL_MAX_REL_VETO:
        status = "block"
        reasons.append("holdout_max_relative_veto")
    if float(replay["rms_relative"].numpy()) > source_route.P72_RESIDUAL_RMS_REL_VETO:
        status = "block"
        reasons.append("replay_rms_relative_veto")
    if float(replay["max_relative"].numpy()) > source_route.P72_RESIDUAL_MAX_REL_VETO:
        status = "block"
        reasons.append("replay_max_relative_veto")
    if line_gate.get("status") == "block":
        status = "block"
        reasons.append("audit_line_veto")
    return {
        "status": status,
        "reasons": tuple(reasons),
        "holdout": holdout,
        "replay": replay,
        "line_gate": line_gate,
        "audit_seed_policy": {
            "holdout_prior": source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
            "holdout_process": source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
            "replay_prior": source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
            "replay_process": source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
            "not_training_seeds": True,
        },
    }


def target_pilot_payload(
    output: Path,
    command: str,
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    max_seconds: float,
    seed: int,
    init_mode: str = P75_RANDOM_INIT_MODE,
    prefit_steps: int = 0,
) -> Mapping[str, Any]:
    return _target_pilot_payload_from_context(
        output,
        command,
        degree=degree,
        rank=rank,
        batch_size=batch_size,
        batches=batches,
        max_seconds=max_seconds,
        seed=seed,
        init_mode=init_mode,
        prefit_steps=prefit_steps,
    )


def _target_pilot_payload_from_context(
    output: Path,
    command: str,
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    max_seconds: float,
    seed: int,
    init_mode: str,
    prefit_steps: int = 0,
    context: Mapping[str, Any] | None = None,
) -> Mapping[str, Any]:
    mode = str(init_mode)
    if mode not in P75_INIT_MODES:
        raise ValueError(f"init_mode must be one of {P75_INIT_MODES}")
    if int(batch_size) > 4096 or int(batches) > 5000:
        raise ValueError("target pilot bounds exceeded")
    built_context = (
        _target_context(
            batch_size=int(batch_size),
            batches=int(batches),
            prefit_batches=(
                int(prefit_steps)
                if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE
                else 0
            ),
        )
        if context is None
        else context
    )
    model = built_context["model"]
    observations = built_context["observations"]
    target_dim = built_context["target_dim"]
    components = built_context["components"]
    anchor = built_context["anchor"]
    anchor_batch = built_context["anchor_batch"]
    train_data_sequence = built_context["train_data_sequence"]
    prefit_data_sequence = built_context["prefit_data_sequence"]
    config = _target_config(
        dimension=target_dim,
        degree=int(degree),
        rank=int(rank),
        seed=int(seed),
    )
    trainer, init_payload = _trainer_for_init_mode(
        config,
        init_mode=mode,
        anchor_batch=anchor_batch,
    )
    if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE:
        prefit_payload = _run_source_guided_prefit(
            trainer,
            config,
            prefit_data_sequence,
            prefit_steps=int(prefit_steps),
            max_seconds=float(max_seconds),
        )
        init_payload = {
            **dict(init_payload),
            "prefit": prefit_payload,
        }
    optimizer = make_adam_optimizer(config)
    trace = []
    final_terms = None
    final_train_data = None
    completed_batches = 0
    stop_reason = "max_batches_completed"
    for step in range(int(batches)):
        elapsed = time.monotonic() - RUN_START
        if elapsed > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_next_batch"
            break
        train_data = train_data_sequence[step]
        batch = _target_batch_from_data(train_data, label=f"p75_train_batch_{step}")
        terms = trainer.train_step(batch, optimizer)
        final_terms = terms
        final_train_data = train_data
        completed_batches += 1
        if step in {0, int(batches) - 1} or (step + 1) % 50 == 0:
            trace.append(
                {
                    "step": step + 1,
                    "terms": terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
                }
            )
    if final_terms is None:
        raise RuntimeError("target pilot produced no training step")
    audit = _audit_payload(
        trainer=trainer,
        fit_points=final_train_data.local_fit_points if final_train_data is not None else anchor.local_fit_points,
        frame=anchor.frame,
        shift_constant=anchor.shift_constant,
        components=components,
        model=model,
        observations=observations,
        sample_count=min(int(batch_size), 1024),
    )
    p73_status = source_route.p73_density_aware_optimizer_status()
    return {
        **_base_payload(output, command),
        "subplan": (
            P75_PHASE8_SUBPLAN
            if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE
            else P75_PHASE3_SUBPLAN
        ),
        "status": "P75_TARGET_PILOT_COMPLETED",
        "diagnostic_scope": "p75_author_sir_step1_target_pilot_not_validation",
        "schema_only": False,
        "smoke_only_not_pilot_evidence": False,
        "phase4_target_pilot_executed": True,
        "target_pilot": {
            "degree": int(degree),
            "rank": int(rank),
            "batch_size": int(batch_size),
            "requested_batches": int(batches),
            "completed_batches": int(completed_batches),
            "max_seconds": float(max_seconds),
            "stop_reason": stop_reason,
            "training_seed_policy": {
                "prior_seed_base": TARGET_TRAIN_PRIOR_SEED_BASE,
                "process_seed_base": TARGET_TRAIN_PROCESS_SEED_BASE,
                "audit_seed_overlap": False,
                "density_training_batches_reused_for_all_arms": True,
                "prefit_and_density_training_batches_disjoint": bool(
                    built_context.get("prefit_density_disjoint", False)
                )
                if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE
                else False,
            },
            "target_dimension": int(target_dim),
            "time_index": 1,
            "init_mode": mode,
            "initialization": init_payload,
            "prefit_steps": int(prefit_steps) if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE else 0,
            "step_trace": trace,
            "final_terms": terms_payload(final_terms),
            "fresh_audit": audit,
        },
        "config": config_payload(config),
        "p73_regression": p73_status,
        "gate_summary": {
            "overall_status": "pass" if audit["status"] == "pass" else "block",
            "target_pilot_executed": True,
            "completed_batches": int(completed_batches),
            "stop_reason": stop_reason,
            "audit_status": audit["status"],
            "audit_reasons": audit["reasons"],
            "p73_b_optimizer_status": p73_status["status"],
            "nonclaims": P75_NONCLAIMS,
        },
        "nonclaims": P75_NONCLAIMS
        + (
            "one-step target pilot is not full sequential lower-gate repair",
            "fresh-audit gates are pilot diagnostics unless reviewed in Phase 4",
        ),
    }


def _target_context(*, batch_size: int, batches: int, prefit_batches: int = 0) -> Mapping[str, Any]:
    model = source_route.zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    target_dim = model.parameter_dim() + 2 * model.state_dim()
    components = _target_components(model, observations)
    anchor = source_route._p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=int(batch_size),
    )
    train_data_sequence = tuple(
        source_route._p69_author_sir_source_diagnostic_data_for_step(
            model=model,
            observations=observations,
            time_index=1,
            diagnostic_sample_count=int(batch_size),
            frame=anchor.frame,
            shift_constant=anchor.shift_constant,
            prior_seed=TARGET_TRAIN_PRIOR_SEED_BASE + step,
            process_noise_seed=TARGET_TRAIN_PROCESS_SEED_BASE + step,
            construction=f"p75_step1_train_fresh_batch_{step}",
        )
        for step in range(int(batches))
    )
    prefit_data_sequence = tuple(
        source_route._p69_author_sir_source_diagnostic_data_for_step(
            model=model,
            observations=observations,
            time_index=1,
            diagnostic_sample_count=int(batch_size),
            frame=anchor.frame,
            shift_constant=anchor.shift_constant,
            prior_seed=TARGET_TRAIN_PRIOR_SEED_BASE + 100_000 + step,
            process_noise_seed=TARGET_TRAIN_PROCESS_SEED_BASE + 100_000 + step,
            construction=f"p75_step1_prefit_train_fresh_batch_{step}",
        )
        for step in range(int(prefit_batches))
    )
    return {
        "model": model,
        "observations": observations,
        "target_dim": int(target_dim),
        "components": components,
        "anchor": anchor,
        "anchor_batch": _target_batch_from_data(anchor, label="p75_anchor_init_training_only"),
        "train_data_sequence": train_data_sequence,
        "prefit_data_sequence": prefit_data_sequence,
        "prefit_density_disjoint": bool(prefit_data_sequence),
        "same_draws_policy": {
            "anchor_reused_for_all_arms": True,
            "training_batches_reused_for_all_arms": True,
            "prefit_batches_used_only_by_prefit_arm": bool(prefit_data_sequence),
            "prefit_batches_disjoint_from_density_training": bool(prefit_data_sequence),
            "audit_seeds_reused_for_all_arms": True,
            "audit_data_not_used_for_initialization": True,
        },
    }


def compare_init_modes_payload(
    output: Path,
    command: str,
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    max_seconds: float,
    seed: int,
    include_source_guided_prefit: bool = False,
    prefit_steps: int = 0,
) -> Mapping[str, Any]:
    if int(batch_size) > 256 or int(batches) > 4:
        raise ValueError("compare-init smoke bounds exceeded")
    if include_source_guided_prefit:
        if int(batch_size) > 64 or int(prefit_steps) > 20:
            raise ValueError("source-guided prefit smoke bounds exceeded")
        if int(prefit_steps) <= 0:
            raise ValueError("source-guided prefit comparison requires prefit_steps > 0")
    elif int(prefit_steps) != 0:
        raise ValueError("prefit_steps requires --include-source-guided-prefit")
    context = _target_context(
        batch_size=int(batch_size),
        batches=int(batches),
        prefit_batches=int(prefit_steps) if include_source_guided_prefit else 0,
    )
    arms = {}
    modes = (
        P75_COMPARE_BASE_INIT_MODES
        + ((P75_SOURCE_GUIDED_PREFIT_INIT_MODE,) if include_source_guided_prefit else ())
    )
    for mode in modes:
        arms[mode] = _target_pilot_payload_from_context(
            output,
            command,
            degree=degree,
            rank=rank,
            batch_size=batch_size,
            batches=batches,
            max_seconds=max_seconds,
            seed=seed,
            init_mode=mode,
            prefit_steps=(
                int(prefit_steps)
                if mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE
                else 0
            ),
            context=context,
        )
    random_terms = arms[P75_RANDOM_INIT_MODE]["target_pilot"]["final_terms"]
    guided_terms = arms[P75_CALIBRATED_CONSTANT_INIT_MODE]["target_pilot"]["final_terms"]
    tau = float(arms[P75_RANDOM_INIT_MODE]["config"]["tau"])
    guided_rho_max = float(guided_terms["rho_max"])
    random_rho_max = float(random_terms["rho_max"])
    guided_grad = float(guided_terms["gradient_norm"])
    random_grad = float(random_terms["gradient_norm"])
    guided_escaped = guided_rho_max > 10.0 * tau
    rho_relative_win = guided_rho_max > 10.0 * max(random_rho_max, tau)
    grad_relative_win = guided_grad > 10.0 * max(random_grad, 1e-300)
    mechanics_pass = all(
        arm["target_pilot"]["completed_batches"] == int(batches)
        for arm in arms.values()
    )
    comparison_status = "pass" if guided_escaped and rho_relative_win and grad_relative_win and mechanics_pass else "block"
    prefit_comparison = None
    if include_source_guided_prefit:
        prefit_arm = arms[P75_SOURCE_GUIDED_PREFIT_INIT_MODE]["target_pilot"]
        prefit_init = prefit_arm["initialization"]["prefit"]
        calibrated_holdout = _as_float(
            arms[P75_CALIBRATED_CONSTANT_INIT_MODE]["target_pilot"]["fresh_audit"]["holdout"]["rms_relative"]
        )
        prefit_holdout = _as_float(prefit_arm["fresh_audit"]["holdout"]["rms_relative"])
        prefit_completed = int(prefit_init["completed_steps"]) == int(prefit_steps)
        holdout_rms_relative_improved = prefit_holdout < calibrated_holdout
        prefit_mechanics_pass = prefit_completed and mechanics_pass
        prefit_status = "pass" if prefit_mechanics_pass and holdout_rms_relative_improved else "block"
        prefit_comparison = {
            "status": prefit_status,
            "primary_geometry_diagnostic": "holdout_rms_relative",
            "calibrated_constant_holdout_rms_relative": calibrated_holdout,
            "source_guided_prefit_holdout_rms_relative": prefit_holdout,
            "holdout_rms_relative_improved": holdout_rms_relative_improved,
            "prefit_completed_requested_steps": prefit_completed,
            "prefit_requested_steps": int(prefit_steps),
            "prefit_completed_steps": int(prefit_init["completed_steps"]),
            "primary_pass_rule": (
                "source_guided_prefit completes declared prefit/objective steps "
                "and has lower holdout rms_relative than calibrated_constant "
                "on identical audit draws"
            ),
            "nonclaims": P75_NONCLAIMS
            + (
                "prefit comparison is mechanism evidence only",
                "holdout improvement is not lower-gate repair unless frozen gates pass",
            ),
        }
        comparison_status = "pass" if comparison_status == "pass" and prefit_status == "pass" else "block"
    p73_status = source_route.p73_density_aware_optimizer_status()
    return {
        **_base_payload(output, command),
        "subplan": (
            P75_PHASE8_SUBPLAN
            if include_source_guided_prefit
            else P75_PHASE3_SUBPLAN
        ),
        "status": "P75_GUIDED_WARM_START_SMOKE_COMPLETED",
        "diagnostic_scope": "p75_guided_warm_start_smoke_not_validation",
        "schema_only": False,
        "smoke_only_not_pilot_evidence": False,
        "phase4_target_pilot_executed": True,
        "compare_init_modes": True,
        "include_source_guided_prefit": bool(include_source_guided_prefit),
        "same_draws_policy": context["same_draws_policy"],
        "arms": arms,
        "comparison": {
            "status": comparison_status,
            "guided_escaped_defensive_floor": guided_escaped,
            "rho_relative_win": rho_relative_win,
            "gradient_relative_win": grad_relative_win,
            "mechanics_pass": mechanics_pass,
            "tau": tau,
            "random_final_rho_max": random_rho_max,
            "guided_final_rho_max": guided_rho_max,
            "random_final_gradient_norm": random_grad,
            "guided_final_gradient_norm": guided_grad,
            "source_guided_prefit": prefit_comparison,
            "primary_pass_rule": (
                "guided rho_max > 10*tau and guided rho_max, gradient_norm "
                "materially exceed random on identical draws; if source_guided_prefit "
                "is included, it must also improve holdout rms_relative over "
                "calibrated_constant"
            ),
            "nonclaims": P75_NONCLAIMS
            + (
                "guided warm-start smoke is not full UKF initialization",
                "comparison is not validation or lower-gate repair evidence",
                "source-guided prefit is an opt-in warm start, not validation",
            ),
        },
        "p73_regression": p73_status,
        "gate_summary": {
            "overall_status": comparison_status,
            "guided_escaped_defensive_floor": guided_escaped,
            "rho_relative_win": rho_relative_win,
            "gradient_relative_win": grad_relative_win,
            "mechanics_pass": mechanics_pass,
            "source_guided_prefit_status": None if prefit_comparison is None else prefit_comparison["status"],
            "p73_b_optimizer_status": p73_status["status"],
            "nonclaims": P75_NONCLAIMS,
        },
        "nonclaims": P75_NONCLAIMS
        + (
            "guided warm-start smoke is not full UKF initialization",
            "comparison is not validation or lower-gate repair evidence",
            "source-guided prefit is an opt-in warm start, not validation",
        ),
    }


def smoke_payload(output: Path, command: str) -> Mapping[str, Any]:
    config = _synthetic_config()
    batch = _synthetic_batch()
    trainer = TrainableFunctionalTT(config)
    optimizer = make_adam_optimizer(config)
    pre_terms = trainer.objective(batch)
    before = tuple(tf.identity(core) for core in trainer.variables)
    step_terms = trainer.train_step(batch, optimizer)
    after = tuple(tf.identity(core) for core in trainer.variables)
    deltas = [tf.norm(new - old) for old, new in zip(before, after)]
    post_terms = trainer.objective(batch)
    any_changed = bool(tf.reduce_any(tf.stack(deltas) > 0.0).numpy())
    finite_deltas = bool(tf.reduce_all(tf.math.is_finite(tf.stack(deltas))).numpy())
    p73_status = source_route.p73_density_aware_optimizer_status()
    status = P75_SMOKE_STATUS if any_changed and finite_deltas else "P75_SMOKE_BLOCKED"
    return {
        **_base_payload(output, command),
        "status": status,
        "diagnostic_scope": "p75_synthetic_smoke_not_phase4_pilot",
        "schema_only": False,
        "smoke_only_not_pilot_evidence": True,
        "phase4_target_pilot_executed": False,
        "config": config_payload(config),
        "batch": {
            "point_count": int(batch.points.shape[0]),
            "dimension": int(batch.points.shape[1]),
            "provenance_label": batch.provenance_label,
            "forbidden_audit_record_count": len(batch.forbidden_audit_records),
        },
        "smoke_bounds": {
            "synthetic_fixture_only": True,
            "max_dimension": 2,
            "max_degree": 2,
            "max_rank": 2,
            "max_batch_size": 8,
            "optimizer_steps": 1,
            "max_optimizer_steps": 2,
            "zhao_cui_fresh_batches_used": False,
        },
        "terms": {
            "pre": terms_payload(pre_terms),
            "step": terms_payload(step_terms),
            "post": terms_payload(post_terms),
        },
        "parameter_delta_norms": deltas,
        "p73_regression": p73_status,
        "gate_summary": {
            "overall_status": "pass" if status == P75_SMOKE_STATUS else "block",
            "any_core_changed": any_changed,
            "finite_parameter_deltas": finite_deltas,
            "p73_b_optimizer_status": p73_status["status"],
            "smoke_only_not_pilot_evidence": True,
            "phase4_target_pilot_executed": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--target-pilot", action="store_true")
    parser.add_argument("--compare-init-modes", action="store_true")
    parser.add_argument("--include-source-guided-prefit", action="store_true")
    parser.add_argument("--init-mode", choices=P75_INIT_MODES, default=P75_RANDOM_INIT_MODE)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=1024)
    parser.add_argument("--batches", type=int, default=500)
    parser.add_argument("--prefit-steps", type=int, default=0)
    parser.add_argument("--max-seconds", type=float, default=1800.0)
    parser.add_argument("--seed", type=int, default=7501)
    args = parser.parse_args(argv)
    mode_count = sum(bool(value) for value in (args.schema_only, args.smoke_only, args.target_pilot))
    if mode_count > 1:
        parser.error("--schema-only, --smoke-only, and --target-pilot are mutually exclusive")
    command = EXPECTED_COMMAND
    if args.output != DEFAULT_OUTPUT:
        command = f"{command} --output {args.output}"
    if args.schema_only:
        command = f"{command} --schema-only"
    if args.smoke_only:
        command = f"{command} --smoke-only"
    if args.compare_init_modes and not args.target_pilot:
        parser.error("--compare-init-modes requires --target-pilot")
    if args.include_source_guided_prefit and not args.compare_init_modes:
        parser.error("--include-source-guided-prefit requires --compare-init-modes")
    if args.init_mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE and args.prefit_steps <= 0:
        parser.error("--init-mode source_guided_prefit requires --prefit-steps > 0")
    if args.prefit_steps and not (
        args.include_source_guided_prefit
        or args.init_mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE
    ):
        parser.error("--prefit-steps requires source_guided_prefit")
    if args.target_pilot:
        command = (
            f"{command} --target-pilot --degree {args.degree} --rank {args.rank} "
            f"--batch-size {args.batch_size} --batches {args.batches} "
            f"--max-seconds {args.max_seconds} --seed {args.seed}"
        )
        if args.compare_init_modes:
            command = f"{command} --compare-init-modes"
            if args.include_source_guided_prefit:
                command = f"{command} --include-source-guided-prefit --prefit-steps {args.prefit_steps}"
        elif args.init_mode != P75_RANDOM_INIT_MODE:
            command = f"{command} --init-mode {args.init_mode}"
            if args.init_mode == P75_SOURCE_GUIDED_PREFIT_INIT_MODE:
                command = f"{command} --prefit-steps {args.prefit_steps}"
    payload = (
        schema_payload(args.output, command)
        if args.schema_only
        else compare_init_modes_payload(
            args.output,
            command,
            degree=args.degree,
            rank=args.rank,
            batch_size=args.batch_size,
            batches=args.batches,
            max_seconds=args.max_seconds,
            seed=args.seed,
            include_source_guided_prefit=args.include_source_guided_prefit,
            prefit_steps=args.prefit_steps,
        )
        if args.target_pilot and args.compare_init_modes
        else target_pilot_payload(
            args.output,
            command,
            degree=args.degree,
            rank=args.rank,
            batch_size=args.batch_size,
            batches=args.batches,
            max_seconds=args.max_seconds,
            seed=args.seed,
            init_mode=args.init_mode,
            prefit_steps=args.prefit_steps,
        )
        if args.target_pilot
        else smoke_payload(args.output, command)
        if args.smoke_only
        else schema_payload(args.output, command)
    )
    _write_payload(args.output, payload)
    print(
        json.dumps(
            {
                "p75_status": payload["status"],
                "gate_summary": _jsonable(payload["gate_summary"]),
            },
            sort_keys=True,
        )
    )
    return 0 if payload["gate_summary"].get("overall_status") in {"pass", "not_executed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
