#!/usr/bin/env python
"""Bounded CPU-only P76 UKF-frame mini-batch pilot.

This script is a dedicated P76 pilot surface. It intentionally does not expose
the failed P75 random, calibrated-constant, or source-route prefit ladders.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tensorflow as tf

from bayesfilter.highdim import source_route
from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.stochastic_density_training import (
    P75ObjectiveBatch,
    P75TrainableTTConfig,
    TrainableFunctionalTT,
    config_payload,
    make_adam_optimizer,
    terms_payload,
)
from bayesfilter.highdim.ukf_initializer import (
    P76_NONCLAIMS,
    P76UKFInitializerConfig,
    p76_build_ukf_initializer,
)
from bayesfilter.highdim.ukf_scout import UKFScoutConfig, spatial_sir_ukf_scout


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
STATUS_COMPLETED = "P76_PHASE6_BOUNDED_UKF_MINIBATCH_PILOT_COMPLETED"
STATUS_BRIDGE_BLOCKED = "P76_PHASE6_BLOCKED_UKF_FRAME_BRIDGE"
STATUS_TRAINING_BLOCKED = "P76_PHASE6_BLOCKED_TRAINING_VETO"
SCHEMA_VERSION = "p76.phase6.bounded_ukf_minibatch_pilot.v1"
MASTER_PROGRAM = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md"
)
PHASE6_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-subplan-2026-06-18.md"
)
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-phase6-bounded-minibatch-pilot-2026-06-18.json"
)
TARGET_TRAIN_PRIOR_SEED_BASE = 975_000
TARGET_TRAIN_PROCESS_SEED_BASE = 976_000
SHIFT_PRIOR_SEED = 974_001
SHIFT_PROCESS_SEED = 974_101
UKF_FRAME_BRIDGE_THRESHOLDS = {
    "reconstruction_max_abs_error": 1e-10,
    "target_tieout_max_abs_error": 1e-10,
    "training_clip_fraction_max": 0.25,
    "audit_clip_fraction_max": 0.25,
}
NONCLAIMS = P76_NONCLAIMS + (
    "P76_PHASE6_BOUNDED_UKF_MINIBATCH_PILOT is not lower-gate repair",
    "P76_PHASE6_BOUNDED_UKF_MINIBATCH_PILOT is not validation",
    "P76_PHASE6_BOUNDED_UKF_MINIBATCH_PILOT is not HMC readiness",
    "not source-faithful Zhao-Cui",
    "not scaling evidence",
    "not final rank or sample policy",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--batches", type=int, default=20)
    parser.add_argument("--max-seconds", type=float, default=600.0)
    parser.add_argument("--seed", type=int, default=7606)
    args = parser.parse_args(argv)

    output = Path(args.output)
    payload = bounded_ukf_minibatch_pilot_payload(
        output=output,
        degree=args.degree,
        rank=args.rank,
        batch_size=args.batch_size,
        batches=args.batches,
        max_seconds=args.max_seconds,
        seed=args.seed,
    )
    _write_payload(output, payload)
    return 0


def bounded_ukf_minibatch_pilot_payload(
    *,
    output: Path,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    max_seconds: float,
    seed: int,
) -> Mapping[str, Any]:
    if int(batch_size) > 1024 or int(batches) > 500:
        raise ValueError("P76 bounded pilot limits exceeded")
    if int(degree) < 2 or int(rank) < 1 or int(batch_size) < 2 or int(batches) < 1:
        raise ValueError("degree/rank/batch-size/batches must be positive and degree >= 2")
    if float(max_seconds) <= 0.0:
        raise ValueError("max_seconds must be positive")

    run_manifest = _initial_run_manifest(output=output)
    context = _target_context(
        degree=int(degree),
        rank=int(rank),
        batch_size=int(batch_size),
        batches=int(batches),
        seed=int(seed),
    )
    bridge = context["ukf_frame_bridge"]
    base = _base_payload(
        output=output,
        run_manifest=run_manifest,
        degree=int(degree),
        rank=int(rank),
        batch_size=int(batch_size),
        batches=int(batches),
        max_seconds=float(max_seconds),
        seed=int(seed),
        context=context,
    )
    if bridge["status"] != "pass":
        return _with_final_wall_time({
            **base,
            "status": STATUS_BRIDGE_BLOCKED,
            "completed_batches": 0,
            "requested_batches": int(batches),
            "ukf_frame_manifest": context["ukf_frame_manifest"],
            "initializer_manifest": dict(context["initializer"].manifest),
            "training_seed_policy": context["training_seed_policy"],
            "fresh_training_batches": False,
            "audit_data_used": False,
            "source_route_prefit_used": False,
            "default_behavior_changed": False,
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "ukf_frame_bridge": bridge,
            "gate_summary": {
                "overall_status": "block",
                "blocker": "ukf_frame_bridge",
                "blockers": bridge["blockers"],
                "optimizer_constructed": False,
                "training_started": False,
                "not lower-gate repair": True,
                "not validation": True,
                "not HMC readiness": True,
            },
            "nonclaims": NONCLAIMS,
        })

    trainer_config = context["trainer_config"]
    initializer = context["initializer"]
    trainer = TrainableFunctionalTT(trainer_config, initial_cores=initializer.cores)
    optimizer = make_adam_optimizer(trainer_config)
    trace = []
    final_terms = None
    final_train_data = None
    completed_batches = 0
    stop_reason = "max_batches_completed"

    for step, train_data in enumerate(context["train_data_sequence"]):
        elapsed = time.monotonic() - RUN_START
        if elapsed > float(max_seconds):
            stop_reason = "wall_clock_cap_reached_before_next_batch"
            break
        batch = _target_batch_from_data(train_data, label=f"p76_train_batch_{step}")
        try:
            terms = trainer.train_step(batch, optimizer)
        except (tf.errors.InvalidArgumentError, ValueError) as exc:
            return _training_blocked_payload(
                base=base,
                context=context,
                completed_batches=completed_batches,
                requested_batches=int(batches),
                stop_reason="train_step_exception_veto",
                blocker=f"train_step_exception:{exc}",
                trace=trace,
            )
        if _terms_have_nonfinite_veto(terms, trainer, batch):
            trace.append(
                {
                    "step": step + 1,
                    "terms": terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
                    "veto": "nonfinite_training_quantity",
                }
            )
            return _training_blocked_payload(
                base=base,
                context=context,
                completed_batches=completed_batches + 1,
                requested_batches=int(batches),
                stop_reason="nonfinite_training_quantity_veto",
                blocker="nonfinite_training_quantity",
                trace=trace,
                final_terms=terms,
            )
        final_terms = terms
        final_train_data = train_data
        completed_batches += 1
        if step in {0, int(batches) - 1} or (step + 1) % 10 == 0:
            trace.append(
                {
                    "step": step + 1,
                    "terms": terms_payload(terms),
                    "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
                }
            )

    if final_terms is None:
        raise RuntimeError("P76 pilot produced no training step")

    audit = _audit_payload(
        trainer=trainer,
        fit_points=(
            final_train_data.local_fit_points
            if final_train_data is not None
            else context["shift_calibration_data"].local_fit_points
        ),
        frame=context["frame"],
        shift_constant=context["shift_constant"],
        components=context["components"],
        model=context["model"],
        observations=context["observations"],
        sample_count=min(int(batch_size), 1024),
    )
    rho = trainer.rho_theta(_target_batch_from_data(final_train_data, label="p76_final").points)
    normalizer = trainer.normalizer()
    log_density = trainer.log_density(_target_batch_from_data(final_train_data, label="p76_final").points)
    finite_flags = {
        "loss": _finite_scalar(final_terms.total_loss),
        "gradient": final_terms.gradient_norm is not None
        and _finite_scalar(tf.convert_to_tensor(final_terms.gradient_norm)),
        "rho": bool(tf.reduce_all(tf.math.is_finite(rho)).numpy()),
        "normalizer": _finite_scalar(normalizer),
        "log_density": bool(tf.reduce_all(tf.math.is_finite(log_density)).numpy()),
    }
    audit_status = audit["status"]
    gate_blockers = []
    if not all(finite_flags.values()):
        gate_blockers.append("nonfinite_training_quantity")
    if completed_batches <= 0:
        gate_blockers.append("no_completed_batches")

    return _with_final_wall_time({
        **base,
        "status": STATUS_COMPLETED,
        "degree": int(degree),
        "rank": int(rank),
        "batch_size": int(batch_size),
        "requested_batches": int(batches),
        "completed_batches": int(completed_batches),
        "max_seconds": float(max_seconds),
        "stop_reason": stop_reason,
        "training_seed_policy": context["training_seed_policy"],
        "fresh_training_batches": True,
        "audit_data_used": False,
        "source_route_prefit_used": False,
        "default_behavior_changed": False,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "ukf_frame_manifest": context["ukf_frame_manifest"],
        "initializer_manifest": dict(initializer.manifest),
        "ukf_frame_bridge": bridge,
        "training_clip_fraction_max": context["training_clip_fraction_max"],
        "audit_clip_fraction_max": context["audit_clip_fraction_max"],
        "finite_flags": finite_flags,
        "step_trace": trace,
        "final_terms": terms_payload(final_terms),
        "fresh_audit": audit,
        "config": config_payload(trainer_config),
        "gate_summary": {
            "overall_status": "pass" if not gate_blockers else "block",
            "blockers": gate_blockers,
            "completed_batches": int(completed_batches),
            "stop_reason": stop_reason,
            "audit_status": audit_status,
            "audit_residual_magnitudes_explanatory_only": True,
            "audit_status_not_phase6_veto": True,
            "not lower-gate repair": True,
            "not validation": True,
            "not HMC readiness": True,
        },
        "nonclaims": NONCLAIMS,
    })


def _target_context(
    *,
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    seed: int,
) -> Mapping[str, Any]:
    model = source_route.zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    scout = spatial_sir_ukf_scout(
        model,
        config=UKFScoutConfig(horizon=1),
        observations=observations[:2],
    )
    target_dim = model.parameter_dim() + 2 * model.state_dim()
    product_basis = _product_basis(dimension=int(target_dim), degree=int(degree))
    ranks = _rank_tuple(int(target_dim), int(rank))
    initializer_config = P76UKFInitializerConfig(
        product_basis=product_basis,
        ranks=ranks,
        time_index=1,
        quadrature_order=max(16, 2 * int(degree) + 4),
    )
    initializer = p76_build_ukf_initializer(scout, initializer_config)
    frame = source_route.SourceRouteCoordinateFrame(
        mu=initializer.center,
        matrix=initializer.linear_map,
        expansion_factor=initializer_config.gamma,
    )
    components = _target_components(model, observations)
    try:
        shift_calibration_data = _diagnostic_data(
            model=model,
            observations=observations,
            frame=frame,
            shift_constant=tf.constant(0.0, dtype=tf.float64),
            sample_count=int(batch_size),
            prior_seed=SHIFT_PRIOR_SEED,
            process_noise_seed=SHIFT_PROCESS_SEED,
            construction="p76_step1_shift_calibration_training_only_ukf_frame",
        )
    except ValueError as exc:
        return _bridge_blocked_context(
            model=model,
            observations=observations,
            scout=scout,
            target_dim=int(target_dim),
            components=components,
            frame=frame,
            product_basis=product_basis,
            initializer=initializer,
            trainer_config=None,
            bridge_blocker=f"shift_calibration_data_error:{exc}",
        )
    shift_constant = tf.reduce_min(shift_calibration_data.negative_log_values)
    try:
        shift_calibration_data = _diagnostic_data(
            model=model,
            observations=observations,
            frame=frame,
            shift_constant=shift_constant,
            sample_count=int(batch_size),
            prior_seed=SHIFT_PRIOR_SEED,
            process_noise_seed=SHIFT_PROCESS_SEED,
            construction="p76_step1_shift_calibration_training_only_ukf_frame",
        )
        train_data_sequence = tuple(
            _diagnostic_data(
                model=model,
                observations=observations,
                frame=frame,
                shift_constant=shift_constant,
                sample_count=int(batch_size),
                prior_seed=TARGET_TRAIN_PRIOR_SEED_BASE + step,
                process_noise_seed=TARGET_TRAIN_PROCESS_SEED_BASE + step,
                construction=f"p76_step1_train_fresh_batch_{step}_ukf_frame",
            )
            for step in range(int(batches))
        )
        audit_holdout = _diagnostic_data(
            model=model,
            observations=observations,
            frame=frame,
            shift_constant=shift_constant,
            sample_count=min(int(batch_size), 1024),
            prior_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
            process_noise_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
            construction="p76_step1_audit_holdout_seed_ukf_frame",
        )
        audit_replay = _diagnostic_data(
            model=model,
            observations=observations,
            frame=frame,
            shift_constant=shift_constant,
            sample_count=min(int(batch_size), 1024),
            prior_seed=source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
            process_noise_seed=source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
            construction="p76_step1_audit_replay_seed_ukf_frame",
        )
    except ValueError as exc:
        return _bridge_blocked_context(
            model=model,
            observations=observations,
            scout=scout,
            target_dim=int(target_dim),
            components=components,
            frame=frame,
            product_basis=product_basis,
            initializer=initializer,
            trainer_config=None,
            bridge_blocker=f"fresh_batch_or_audit_data_error:{exc}",
        )
    bridge = _ukf_frame_bridge(
        frame=frame,
        product_basis=product_basis,
        initializer=initializer,
        components=components,
        shift_constant=shift_constant,
        train_data_sequence=train_data_sequence,
        audit_data_sequence=(audit_holdout, audit_replay),
    )
    trainer_config = P75TrainableTTConfig(
        product_basis=product_basis,
        ranks=ranks,
        tau=source_route._p59_author_sir_defensive_tau_tensor(),
        normalizer_floor=tf.constant(source_route.P72_SQRT_SQUARE_NORMALIZER_FLOOR, dtype=tf.float64),
        denominator_floor=tf.constant(source_route.P73_EPS_LOG, dtype=tf.float64),
        l2_weight=tf.constant(1e-8, dtype=tf.float64),
        learning_rate=1e-3,
        gradient_clip_norm=100.0,
        seed=int(seed),
        metadata={
            "fixture": "p76_author_sir_step1_ukf_frame_minibatch_pilot",
            "extension_or_invention": True,
            "ukf_initializer": True,
            "fresh_training_batches": True,
        },
    )
    training_clip = _clip_fraction_max(train_data_sequence)
    audit_clip = _clip_fraction_max((audit_holdout, audit_replay))
    frame_hash = source_route._p69_frame_hash(frame)
    return {
        "model": model,
        "observations": observations,
        "scout": scout,
        "target_dim": int(target_dim),
        "components": components,
        "frame": frame,
        "frame_hash": frame_hash,
        "shift_constant": shift_constant,
        "shift_calibration_data": shift_calibration_data,
        "train_data_sequence": train_data_sequence,
        "audit_data_sequence": (audit_holdout, audit_replay),
        "initializer": initializer,
        "initializer_config": initializer_config,
        "trainer_config": trainer_config,
        "ukf_frame_bridge": bridge,
        "training_clip_fraction_max": training_clip,
        "audit_clip_fraction_max": audit_clip,
        "training_seed_policy": {
            "shift_prior_seed": SHIFT_PRIOR_SEED,
            "shift_process_seed": SHIFT_PROCESS_SEED,
            "prior_seed_base": TARGET_TRAIN_PRIOR_SEED_BASE,
            "process_seed_base": TARGET_TRAIN_PROCESS_SEED_BASE,
            "audit_seed_overlap": False,
            "fresh_training_batches": True,
            "source_route_prefit_used": False,
        },
        "ukf_frame_manifest": {
            "frame_hash": frame_hash,
            "target_dimension": int(target_dim),
            "frame_dimension": int(frame.dimension),
            "product_basis_dimension": int(product_basis.dimension),
            "initializer_dimension": int(initializer.center.shape[0]),
            "center_shape": _shape_payload(frame.mu),
            "linear_map_shape": _shape_payload(frame.matrix),
            "expansion_factor": float(frame.expansion_factor),
            "log_abs_det": float(frame.log_abs_det().numpy()),
            "claim_class": scout.claim_class,
            "source_route_prefit_used": False,
            "audit_data_used": False,
        },
    }


def _bridge_blocked_context(
    *,
    model,
    observations: tf.Tensor,
    scout,
    target_dim: int,
    components,
    frame: source_route.SourceRouteCoordinateFrame,
    product_basis: ProductBasis,
    initializer,
    trainer_config,
    bridge_blocker: str,
) -> Mapping[str, Any]:
    del trainer_config
    frame_hash = source_route._p69_frame_hash(frame)
    bridge = _ukf_frame_bridge_from_blocker(
        frame=frame,
        product_basis=product_basis,
        initializer=initializer,
        bridge_blocker=bridge_blocker,
    )
    return {
        "model": model,
        "observations": observations,
        "scout": scout,
        "target_dim": int(target_dim),
        "components": components,
        "frame": frame,
        "frame_hash": frame_hash,
        "shift_constant": tf.constant(0.0, dtype=tf.float64),
        "shift_calibration_data": None,
        "train_data_sequence": (),
        "audit_data_sequence": (),
        "initializer": initializer,
        "initializer_config": None,
        "trainer_config": None,
        "ukf_frame_bridge": bridge,
        "training_clip_fraction_max": 1.0,
        "audit_clip_fraction_max": 1.0,
        "training_seed_policy": {
            "shift_prior_seed": SHIFT_PRIOR_SEED,
            "shift_process_seed": SHIFT_PROCESS_SEED,
            "prior_seed_base": TARGET_TRAIN_PRIOR_SEED_BASE,
            "process_seed_base": TARGET_TRAIN_PROCESS_SEED_BASE,
            "audit_seed_overlap": False,
            "fresh_training_batches": False,
            "source_route_prefit_used": False,
            "bridge_blocker": str(bridge_blocker),
        },
        "ukf_frame_manifest": {
            "frame_hash": frame_hash,
            "target_dimension": int(target_dim),
            "frame_dimension": int(frame.dimension),
            "product_basis_dimension": int(product_basis.dimension),
            "initializer_dimension": int(initializer.center.shape[0]),
            "center_shape": _shape_payload(frame.mu),
            "linear_map_shape": _shape_payload(frame.matrix),
            "expansion_factor": float(frame.expansion_factor),
            "log_abs_det": float(frame.log_abs_det().numpy()),
            "claim_class": scout.claim_class,
            "source_route_prefit_used": False,
            "audit_data_used": False,
        },
    }


def _diagnostic_data(
    *,
    model,
    observations: tf.Tensor,
    frame: source_route.SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    sample_count: int,
    prior_seed: int,
    process_noise_seed: int,
    construction: str,
):
    return source_route._p69_author_sir_source_diagnostic_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        diagnostic_sample_count=int(sample_count),
        frame=frame,
        shift_constant=tf.convert_to_tensor(shift_constant, dtype=tf.float64),
        prior_seed=int(prior_seed),
        process_noise_seed=int(process_noise_seed),
        construction=str(construction),
    )


def _batch_target_tieout_max_abs_error(
    *,
    data_sequence: Sequence[Any],
    frame: source_route.SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    components,
) -> float:
    if not data_sequence:
        return math.inf
    errors = []
    for data in data_sequence:
        direct_targets = _target_values_for_reference_cloud(
            local_points=data.local_fit_points,
            frame=frame,
            shift_constant=shift_constant,
            components=components,
        )
        errors.append(tf.reduce_max(tf.abs(data.target_values - direct_targets)))
    return float(tf.reduce_max(tf.stack(errors)).numpy())


def _ukf_frame_bridge(
    *,
    frame: source_route.SourceRouteCoordinateFrame,
    product_basis: ProductBasis,
    initializer,
    components,
    shift_constant: tf.Tensor,
    train_data_sequence: Sequence[Any],
    audit_data_sequence: Sequence[Any],
) -> Mapping[str, Any]:
    frame_hash = source_route._p69_frame_hash(frame)
    training_hashes = tuple(str(data.manifest["coordinate_frame_hash"]) for data in train_data_sequence)
    audit_hashes = tuple(str(data.manifest["coordinate_frame_hash"]) for data in audit_data_sequence)
    probe_points = _bridge_probe_points(int(frame.dimension))
    physical = tf.linalg.matmul(frame.matrix, probe_points) + frame.mu[:, tf.newaxis]
    reconstructed = tf.linalg.solve(frame.matrix, physical - frame.mu[:, tf.newaxis])
    reconstruction_error = float(tf.reduce_max(tf.abs(reconstructed - probe_points)).numpy())
    probe_targets = _target_values_for_reference_cloud(
        local_points=probe_points,
        frame=frame,
        shift_constant=shift_constant,
        components=components,
    )
    target_tieout_error = _batch_target_tieout_max_abs_error(
        data_sequence=tuple(train_data_sequence) + tuple(audit_data_sequence),
        frame=frame,
        shift_constant=shift_constant,
        components=components,
    )
    training_clip = _clip_fraction_max(train_data_sequence)
    audit_clip = _clip_fraction_max(audit_data_sequence)
    bridge_targets_finite = bool(
        tf.reduce_all(tf.math.is_finite(probe_targets)).numpy()
    )
    training_targets_finite = all(
        bool(tf.reduce_all(tf.math.is_finite(data.target_values)).numpy())
        for data in train_data_sequence
    )
    audit_targets_finite = all(
        bool(tf.reduce_all(tf.math.is_finite(data.target_values)).numpy())
        for data in audit_data_sequence
    )
    nonfinite_target_value_count = sum(
        _nonfinite_count(data.target_values)
        for data in tuple(train_data_sequence) + tuple(audit_data_sequence)
    )
    dimension_match = (
        int(frame.dimension)
        == int(product_basis.dimension)
        == int(initializer.center.shape[0])
    )
    blockers = []
    if not dimension_match:
        blockers.append("dimension_mismatch")
    if any(item != frame_hash for item in training_hashes + audit_hashes):
        blockers.append("frame_hash_mismatch")
    if reconstruction_error > UKF_FRAME_BRIDGE_THRESHOLDS["reconstruction_max_abs_error"]:
        blockers.append("reconstruction_max_abs_error")
    if target_tieout_error > UKF_FRAME_BRIDGE_THRESHOLDS["target_tieout_max_abs_error"]:
        blockers.append("target_tieout_max_abs_error")
    if training_clip > UKF_FRAME_BRIDGE_THRESHOLDS["training_clip_fraction_max"]:
        blockers.append("training_clip_fraction_max")
    if audit_clip > UKF_FRAME_BRIDGE_THRESHOLDS["audit_clip_fraction_max"]:
        blockers.append("audit_clip_fraction_max")
    if not bridge_targets_finite:
        blockers.append("bridge_target_values_nonfinite")
    if not training_targets_finite:
        blockers.append("training_target_values_nonfinite")
    if not audit_targets_finite:
        blockers.append("audit_target_values_nonfinite")
    if nonfinite_target_value_count != 0:
        blockers.append("nonfinite_target_value_count")
    return {
        "status": "pass" if not blockers else "block",
        "target_dimension": int(frame.dimension),
        "frame_dimension": int(frame.dimension),
        "product_basis_dimension": int(product_basis.dimension),
        "initializer_dimension": int(initializer.center.shape[0]),
        "dimension_match": dimension_match,
        "frame_hash": frame_hash,
        "training_frame_hashes": training_hashes,
        "audit_frame_hashes": audit_hashes,
        "reconstruction_max_abs_error": reconstruction_error,
        "target_tieout_max_abs_error": target_tieout_error,
        "target_tieout_source": (
            "actual_batch_target_values_vs_independent_direct_physical_density"
        ),
        "training_clip_fraction_max": training_clip,
        "audit_clip_fraction_max": audit_clip,
        "bridge_target_values_finite": bridge_targets_finite,
        "training_target_values_finite": training_targets_finite,
        "audit_target_values_finite": audit_targets_finite,
        "nonfinite_target_value_count": int(nonfinite_target_value_count),
        "thresholds": UKF_FRAME_BRIDGE_THRESHOLDS,
        "blockers": blockers,
    }


def _ukf_frame_bridge_from_blocker(
    *,
    frame: source_route.SourceRouteCoordinateFrame,
    product_basis: ProductBasis,
    initializer,
    bridge_blocker: str,
) -> Mapping[str, Any]:
    frame_hash = source_route._p69_frame_hash(frame)
    return {
        "status": "block",
        "target_dimension": int(frame.dimension),
        "frame_dimension": int(frame.dimension),
        "product_basis_dimension": int(product_basis.dimension),
        "initializer_dimension": int(initializer.center.shape[0]),
        "dimension_match": (
            int(frame.dimension)
            == int(product_basis.dimension)
            == int(initializer.center.shape[0])
        ),
        "frame_hash": frame_hash,
        "training_frame_hashes": (),
        "audit_frame_hashes": (),
        "reconstruction_max_abs_error": None,
        "target_tieout_max_abs_error": None,
        "target_tieout_source": "not_evaluated_bridge_blocker",
        "training_clip_fraction_max": 1.0,
        "audit_clip_fraction_max": 1.0,
        "bridge_target_values_finite": False,
        "training_target_values_finite": False,
        "audit_target_values_finite": False,
        "nonfinite_target_value_count": 0,
        "thresholds": UKF_FRAME_BRIDGE_THRESHOLDS,
        "blockers": (str(bridge_blocker),),
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
    frame: source_route.SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    components,
) -> tf.Tensor:
    local = tf.convert_to_tensor(local_points, dtype=tf.float64)
    if local.shape.rank != 2 or int(local.shape[0]) != int(frame.dimension):
        raise ValueError("local_points must have shape [dimension, point_count]")
    physical = tf.linalg.matmul(frame.matrix, local) + frame.mu[:, tf.newaxis]
    return _direct_target_values_for_physical_points(
        physical_points=physical,
        frame=frame,
        shift_constant=shift_constant,
        components=components,
    )


def _direct_target_values_for_physical_points(
    *,
    physical_points: tf.Tensor,
    frame: source_route.SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    components,
) -> tf.Tensor:
    physical = tf.convert_to_tensor(physical_points, dtype=tf.float64)
    if physical.shape.rank != 2 or int(physical.shape[0]) != int(frame.dimension):
        raise ValueError("physical_points must have shape [dimension, point_count]")
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


def _target_batch_from_data(data, *, label: str) -> P75ObjectiveBatch:
    point_count = int(data.local_fit_points.shape[1])
    return P75ObjectiveBatch(
        points=tf.transpose(data.local_fit_points),
        target_values=data.target_values,
        weights=data.fit_weights,
        point_records=tuple(
            {
                "point_id": f"{label}-{index}",
                "cloud_hash": str(data.manifest["coordinate_frame_hash"]),
                "role": "fit",
                "source_channel": "p76_ukf_frame_fresh_training",
            }
            for index in range(point_count)
        ),
        forbidden_audit_records=(
            {
                "point_id": "p76-audit-sentinel",
                "cloud_hash": "p76-audit-cloud",
                "role": "audit",
                "source_channel": "p76_ukf_frame_audit",
            },
        ),
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


def _terms_have_nonfinite_veto(
    terms,
    trainer: TrainableFunctionalTT,
    batch: P75ObjectiveBatch,
) -> bool:
    tensors = (
        terms.total_loss,
        terms.weighted_empirical_cross_entropy,
        terms.log_normalizer,
        terms.regularization,
        terms.normalizer,
        terms.alpha_min,
        terms.alpha_max,
        terms.alpha_sum,
        terms.rho_min,
        terms.rho_max,
    )
    if terms.gradient_norm is not None:
        tensors = tensors + (tf.convert_to_tensor(terms.gradient_norm, dtype=tf.float64),)
    if any(not bool(tf.reduce_all(tf.math.is_finite(tf.convert_to_tensor(value, dtype=tf.float64))).numpy()) for value in tensors):
        return True
    rho = trainer.rho_theta(batch.points)
    normalizer = trainer.normalizer()
    log_density = trainer.log_density(batch.points)
    return not bool(
        tf.reduce_all(tf.math.is_finite(rho)).numpy()
        and tf.math.is_finite(normalizer).numpy()
        and tf.reduce_all(tf.math.is_finite(log_density)).numpy()
    )


def _audit_payload(
    *,
    trainer: TrainableFunctionalTT,
    fit_points: tf.Tensor,
    frame: source_route.SourceRouteCoordinateFrame,
    shift_constant: tf.Tensor,
    components,
    model,
    observations,
    sample_count: int,
) -> Mapping[str, Any]:
    audit_holdout = _diagnostic_data(
        model=model,
        observations=observations,
        frame=frame,
        shift_constant=shift_constant,
        sample_count=int(sample_count),
        prior_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
        construction="p76_step1_audit_holdout_seed_ukf_frame",
    )
    audit_replay = _diagnostic_data(
        model=model,
        observations=observations,
        frame=frame,
        shift_constant=shift_constant,
        sample_count=int(sample_count),
        prior_seed=source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
        process_noise_seed=source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
        construction="p76_step1_audit_replay_seed_ukf_frame",
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
    start_predictions = ftt.evaluate(tf.transpose(tf.repeat(center, repeats=3, axis=1)))
    target_scale = max(float(holdout["target_scale"].numpy()), 1e-300)
    line_gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=ftt,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=start_predictions,
        line_start_indices=line_manifest["line_start_indices"],
        target_scale=target_scale,
    )
    reasons = []
    if float(holdout["rms_relative"].numpy()) > source_route.P72_RESIDUAL_RMS_REL_VETO:
        reasons.append("holdout_rms_relative_veto")
    if float(holdout["max_relative"].numpy()) > source_route.P72_RESIDUAL_MAX_REL_VETO:
        reasons.append("holdout_max_relative_veto")
    if float(replay["rms_relative"].numpy()) > source_route.P72_RESIDUAL_RMS_REL_VETO:
        reasons.append("replay_rms_relative_veto")
    if float(replay["max_relative"].numpy()) > source_route.P72_RESIDUAL_MAX_REL_VETO:
        reasons.append("replay_max_relative_veto")
    if line_gate.get("status") == "block":
        reasons.append("audit_line_veto")
    return {
        "status": "block" if reasons else "pass",
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


def _base_payload(
    *,
    output: Path,
    run_manifest: Mapping[str, Any],
    degree: int,
    rank: int,
    batch_size: int,
    batches: int,
    max_seconds: float,
    seed: int,
    context: Mapping[str, Any],
) -> Mapping[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata_date": "2026-06-18",
        "master_program": MASTER_PROGRAM,
        "subplan": PHASE6_SUBPLAN,
        "run_manifest": run_manifest,
        "diagnostic_scope": "p76_author_sir_step1_ukf_frame_minibatch_pilot_not_validation",
        "degree": int(degree),
        "rank": int(rank),
        "batch_size": int(batch_size),
        "requested_batches": int(batches),
        "max_seconds": float(max_seconds),
        "seed": int(seed),
        "target_dimension": int(context["target_dim"]),
        "time_index": 1,
        "fresh_training_batches": True,
        "audit_data_used": False,
        "source_route_prefit_used": False,
        "default_behavior_changed": False,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "nonclaims": NONCLAIMS,
    }


def _training_blocked_payload(
    *,
    base: Mapping[str, Any],
    context: Mapping[str, Any],
    completed_batches: int,
    requested_batches: int,
    stop_reason: str,
    blocker: str,
    trace: Sequence[Mapping[str, Any]],
    final_terms=None,
) -> Mapping[str, Any]:
    payload = {
        **dict(base),
        "status": STATUS_TRAINING_BLOCKED,
        "completed_batches": int(completed_batches),
        "requested_batches": int(requested_batches),
        "stop_reason": str(stop_reason),
        "training_seed_policy": context["training_seed_policy"],
        "fresh_training_batches": True,
        "audit_data_used": False,
        "source_route_prefit_used": False,
        "default_behavior_changed": False,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "ukf_frame_manifest": context["ukf_frame_manifest"],
        "initializer_manifest": dict(context["initializer"].manifest),
        "ukf_frame_bridge": context["ukf_frame_bridge"],
        "training_clip_fraction_max": context["training_clip_fraction_max"],
        "audit_clip_fraction_max": context["audit_clip_fraction_max"],
        "step_trace": tuple(trace),
        "optimizer_constructed": True,
        "training_started": int(completed_batches) > 0,
        "gate_summary": {
            "overall_status": "block",
            "blockers": (str(blocker),),
            "completed_batches": int(completed_batches),
            "stop_reason": str(stop_reason),
            "not lower-gate repair": True,
            "not validation": True,
            "not HMC readiness": True,
        },
        "nonclaims": NONCLAIMS,
    }
    if final_terms is not None:
        payload["final_terms"] = terms_payload(final_terms)
    return _with_final_wall_time(payload)


def _product_basis(*, dimension: int, degree: int) -> ProductBasis:
    return ProductBasis(
        [
            LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(degree))
            for _ in range(int(dimension))
        ],
        source_route._p59_reference_convention(),
    )


def _rank_tuple(dimension: int, rank: int) -> tuple[int, ...]:
    return tuple([1] + [int(rank)] * (int(dimension) - 1) + [1])


def _bridge_probe_points(dimension: int) -> tf.Tensor:
    d = int(dimension)
    columns = [tf.zeros([d], dtype=tf.float64)]
    for axis in range(d):
        pos = tf.tensor_scatter_nd_update(
            tf.zeros([d], dtype=tf.float64),
            [[axis]],
            [tf.constant(0.25, dtype=tf.float64)],
        )
        neg = tf.tensor_scatter_nd_update(
            tf.zeros([d], dtype=tf.float64),
            [[axis]],
            [tf.constant(-0.25, dtype=tf.float64)],
        )
        columns.extend([pos, neg])
    return tf.stack(columns, axis=1)


def _clip_fraction_max(sequence: Sequence[Any]) -> float:
    if not sequence:
        return 0.0
    return max(float(data.manifest["local_clip_fraction"].numpy()) for data in sequence)


def _nonfinite_count(value: tf.Tensor) -> int:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    return int(tf.reduce_sum(tf.cast(~tf.math.is_finite(tensor), tf.int32)).numpy())


def _finite_scalar(value: tf.Tensor) -> bool:
    tensor = tf.convert_to_tensor(value, dtype=tf.float64)
    return tensor.shape.rank == 0 and bool(tf.math.is_finite(tensor).numpy())


def _shape_payload(tensor: tf.Tensor) -> tuple[int, ...]:
    return tuple(int(dim) for dim in tf.convert_to_tensor(tensor).shape)


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


def _with_final_wall_time(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    updated = dict(payload)
    manifest = dict(updated.get("run_manifest", {}))
    manifest["elapsed_seconds"] = round(time.monotonic() - RUN_START, 3)
    updated["run_manifest"] = manifest
    updated["wall_time_seconds"] = manifest["elapsed_seconds"]
    return updated


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


def _initial_run_manifest(*, output: Path) -> Mapping[str, Any]:
    env_keys = ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR", "PWD")
    environment = {key: os.environ.get(key) for key in env_keys}
    python_argv = [sys.executable, *sys.argv]
    env_prefix = [
        f"{key}={value}"
        for key in ("CUDA_VISIBLE_DEVICES", "MPLCONFIGDIR")
        if (value := os.environ.get(key)) is not None
    ]
    replay_parts = [*env_prefix, *python_argv]
    return {
        "command": " ".join(shlex.quote(part) for part in replay_parts),
        "python_executable": sys.executable,
        "argv": list(sys.argv),
        "python_argv": python_argv,
        "environment": environment,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_version": tf.__version__,
        "script": str(SCRIPT_PATH.relative_to(REPO_ROOT)),
        "output": str(output),
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "git": _git_state_summary(),
    }


if __name__ == "__main__":
    sys.exit(main())
