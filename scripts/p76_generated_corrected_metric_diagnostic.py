#!/usr/bin/env python
"""Tiny CPU-only generated-sample diagnostic for the P76 corrected metric."""

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
from bayesfilter.highdim import stochastic_density_training as p76_metric
import scripts.p76_bounded_ukf_minibatch_pilot as phase6


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
STATUS_COMPLETED = "P76_PHASE10_GENERATED_CORRECTED_METRIC_DIAGNOSTIC_COMPLETED"
STATUS_BRIDGE_BLOCKED = "P76_PHASE10_BLOCKED_UKF_FRAME_BRIDGE"
STATUS_SEED_BLOCKED = "P76_PHASE10_BLOCKED_SEED_OVERLAP"
STATUS_METRIC_BLOCKED = "P76_PHASE10_BLOCKED_METRIC_EVALUATION"
SCHEMA_VERSION = "p76.phase10.generated_corrected_metric_diagnostic.v1"
MASTER_PROGRAM = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-ukf-warm-start-minibatch-master-program-2026-06-18.md"
)
PHASE10_SUBPLAN = (
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-subplan-2026-06-19.md"
)
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p76-phase10-generated-corrected-metric-diagnostic-2026-06-19.json"
)
NONCLAIMS = (
    "generated-sample metric-only diagnostic",
    "not training evidence",
    "not fit-quality evidence",
    "not lower-gate repair evidence",
    "not validation evidence",
    "not HMC readiness evidence",
    "not scaling evidence",
    "not source-faithful Zhao-Cui",
    "not UKF success or rejection evidence",
    "not final rank or sample policy",
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sample-count", type=int, default=32)
    parser.add_argument("--degree", type=int, default=2)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7610)
    args = parser.parse_args(argv)

    payload = generated_corrected_metric_diagnostic_payload(
        output=args.output,
        sample_count=args.sample_count,
        degree=args.degree,
        rank=args.rank,
        seed=args.seed,
    )
    _write_payload(args.output, payload)
    return 0


def generated_corrected_metric_diagnostic_payload(
    *,
    output: Path,
    sample_count: int,
    degree: int,
    rank: int,
    seed: int,
) -> Mapping[str, Any]:
    _validate_bounds(sample_count=sample_count, degree=degree, rank=rank)
    run_manifest = _initial_run_manifest(output=output)
    context = _build_context(
        degree=int(degree),
        rank=int(rank),
        sample_count=int(sample_count),
        seed=int(seed),
    )
    bridge = context["ukf_frame_bridge"]
    base = _base_payload(
        output=output,
        run_manifest=run_manifest,
        sample_count=int(sample_count),
        degree=int(degree),
        rank=int(rank),
        seed=int(seed),
        context=context,
    )
    if bridge["status"] != "pass":
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_BRIDGE_BLOCKED,
                "ukf_frame_bridge": bridge,
                "metric_batches": {},
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": tuple(bridge.get("blockers", ())),
                    "bridge_status": bridge["status"],
                    "training_started": False,
                    "metric_evaluated": False,
                },
            }
        )

    seed_manifest = _seed_manifest(bridge_training_present=bool(context["train_data_sequence"]))
    if not seed_manifest["pairwise_disjoint_roles"]:
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_SEED_BLOCKED,
                "seed_manifest": seed_manifest,
                "ukf_frame_bridge": bridge,
                "metric_batches": {},
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": ("seed_overlap",),
                    "bridge_status": bridge["status"],
                    "training_started": False,
                    "metric_evaluated": False,
                },
            }
        )

    try:
        trainer = p76_metric.TrainableFunctionalTT(
            context["trainer_config"],
            initial_cores=context["initializer"].cores,
        )
        holdout_data, replay_data = tuple(context["audit_data_sequence"])
        metric_batches = {
            "holdout": _metric_payload(
                trainer=trainer,
                data=holdout_data,
                label="phase10_holdout",
                role="heldout_metric",
            ),
            "replay": _metric_payload(
                trainer=trainer,
                data=replay_data,
                label="phase10_replay",
                role="audit_metric",
            ),
        }
    except (tf.errors.InvalidArgumentError, ValueError, RuntimeError) as exc:
        return _with_final_wall_time(
            {
                **base,
                "status": STATUS_METRIC_BLOCKED,
                "seed_manifest": seed_manifest,
                "ukf_frame_bridge": bridge,
                "metric_batches": {},
                "metric_exception": str(exc),
                "gate_summary": {
                    "overall_status": "block",
                    "blockers": ("metric_evaluation_exception",),
                    "bridge_status": bridge["status"],
                    "training_started": False,
                    "metric_evaluated": False,
                },
            }
        )

    finite_metric_values = all(
        batch_payload["all_primary_values_finite"] for batch_payload in metric_batches.values()
    )
    ce_reconstructs = all(
        batch_payload["heldout_cross_entropy_reconstruction_abs_error"] <= 1e-10
        for batch_payload in metric_batches.values()
    )
    target_alpha_mass = all(
        abs(float(batch_payload["metric_payload"]["alpha_sum"]) - 1.0) <= 1e-10
        for batch_payload in metric_batches.values()
    )
    blockers = []
    if not finite_metric_values:
        blockers.append("nonfinite_metric_quantity")
    if not ce_reconstructs:
        blockers.append("ce_reconstruction_mismatch")
    if not target_alpha_mass:
        blockers.append("target_only_alpha_mass_not_one")

    return _with_final_wall_time(
        {
            **base,
            "status": STATUS_COMPLETED,
            "seed_manifest": seed_manifest,
            "ukf_frame_bridge": bridge,
            "metric_batches": metric_batches,
            "gate_summary": {
                "overall_status": "pass" if not blockers else "block",
                "blockers": tuple(blockers),
                "bridge_status": bridge["status"],
                "training_started": False,
                "metric_evaluated": True,
                "finite_metric_values": finite_metric_values,
                "ce_reconstructs_from_json_values": ce_reconstructs,
                "target_only_alpha_mass": target_alpha_mass,
                "not fit-quality": True,
                "not validation": True,
                "not lower-gate repair": True,
            },
        }
    )


def _validate_bounds(*, sample_count: int, degree: int, rank: int) -> None:
    if int(sample_count) < 2 or int(sample_count) > 32:
        raise ValueError("Phase 10 reviewed bound requires 2 <= sample_count <= 32")
    if int(degree) != 2:
        raise ValueError("Phase 10 reviewed bound requires degree == 2")
    if int(rank) != 4:
        raise ValueError("Phase 10 reviewed bound requires rank == 4")


def _build_context(*, degree: int, rank: int, sample_count: int, seed: int) -> Mapping[str, Any]:
    return phase6._target_context(
        degree=int(degree),
        rank=int(rank),
        batch_size=int(sample_count),
        batches=1,
        seed=int(seed),
    )


def _metric_payload(
    *,
    trainer: p76_metric.TrainableFunctionalTT,
    data: Any,
    label: str,
    role: str,
) -> Mapping[str, Any]:
    batch = _metric_batch_from_data(data=data, label=label, role=role)
    terms = trainer.corrected_heldout_density_metric(batch)
    alpha = trainer.corrected_heldout_metric_weights(batch)
    rho_theta = trainer.rho_theta(batch.points)
    normalizer = trainer.normalizer()
    reconstructed_ce = -tf.reduce_sum(alpha * tf.math.log(rho_theta)) + tf.math.log(
        normalizer
    )
    reconstruction_error = tf.abs(reconstructed_ce - terms.heldout_cross_entropy)
    payload = p76_metric.corrected_heldout_metric_terms_payload(terms)
    finite_flags = dict(payload["finite_flags"])
    finite_flags.update(
        {
            "corrected_alpha": bool(tf.reduce_all(tf.math.is_finite(alpha)).numpy()),
            "rho_theta_values": bool(tf.reduce_all(tf.math.is_finite(rho_theta)).numpy()),
            "reconstructed_heldout_cross_entropy": bool(
                tf.math.is_finite(reconstructed_ce).numpy()
            ),
        }
    )
    return {
        "label": str(label),
        "role": batch.role,
        "provenance_label": batch.provenance_label,
        "point_count": int(batch.points.shape[0]),
        "cloud_hash": str(data.manifest.get("coordinate_frame_hash", "")),
        "local_clip_fraction": float(data.manifest["local_clip_fraction"].numpy()),
        "target_values_source": "reviewed_target_bridge_generated_data",
        "metric_payload": payload,
        "corrected_alpha": _tensor_list(alpha),
        "rho_theta_values": _tensor_list(rho_theta),
        "normalizer": float(normalizer.numpy()),
        "heldout_cross_entropy": float(terms.heldout_cross_entropy.numpy()),
        "reconstructed_heldout_cross_entropy": float(reconstructed_ce.numpy()),
        "heldout_cross_entropy_reconstruction_abs_error": float(
            reconstruction_error.numpy()
        ),
        "target_sqrt_values": _tensor_list(batch.target_sqrt_values),
        "integration_weights": _tensor_list(batch.integration_weights),
        "target_mass": float(
            tf.reduce_sum(batch.integration_weights * tf.square(batch.target_sqrt_values)).numpy()
        ),
        "integration_weight_mass": float(tf.reduce_sum(batch.integration_weights).numpy()),
        "corrected_alpha_sum": float(tf.reduce_sum(alpha).numpy()),
        "corrected_alpha_effective_sample_size": float(
            (1.0 / tf.reduce_sum(tf.square(alpha))).numpy()
        ),
        "finite_flags": finite_flags,
        "all_primary_values_finite": all(finite_flags.values()),
        "explanatory_only": True,
        "not_training_or_selection": True,
    }


def _metric_batch_from_data(
    *,
    data: Any,
    label: str,
    role: str,
) -> p76_metric.P76CorrectedHeldoutMetricBatch:
    point_count = int(data.local_fit_points.shape[1])
    return p76_metric.P76CorrectedHeldoutMetricBatch(
        points=tf.transpose(data.local_fit_points),
        target_sqrt_values=data.target_values,
        integration_weights=data.fit_weights,
        role=str(role),
        provenance_label="reviewed_target_bridge",
        point_records=tuple(
            {
                "point_id": f"{label}-{index}",
                "cloud_hash": str(data.manifest.get("coordinate_frame_hash", "")),
                "role": str(role),
                "provenance_label": "reviewed_target_bridge",
            }
            for index in range(point_count)
        ),
    )


def _seed_manifest(*, bridge_training_present: bool) -> Mapping[str, Any]:
    role_seed_pairs: dict[str, Mapping[str, int]] = {
        "shift_calibration": {
            "prior_seed": phase6.SHIFT_PRIOR_SEED,
            "process_noise_seed": phase6.SHIFT_PROCESS_SEED,
        },
        "holdout_metric": {
            "prior_seed": source_route.P72_AUDIT_STEP1_HOLDOUT_PRIOR_SEED,
            "process_noise_seed": source_route.P72_AUDIT_STEP1_HOLDOUT_PROCESS_SEED,
        },
        "replay_metric": {
            "prior_seed": source_route.P72_AUDIT_STEP1_REPLAY_PRIOR_SEED,
            "process_noise_seed": source_route.P72_AUDIT_STEP1_REPLAY_PROCESS_SEED,
        },
    }
    if bridge_training_present:
        role_seed_pairs["bridge_training_bookkeeping_only"] = {
            "prior_seed": phase6.TARGET_TRAIN_PRIOR_SEED_BASE,
            "process_noise_seed": phase6.TARGET_TRAIN_PROCESS_SEED_BASE,
        }
    seen: dict[int, list[str]] = {}
    for role, pair in role_seed_pairs.items():
        for name, seed in pair.items():
            seen.setdefault(int(seed), []).append(f"{role}.{name}")
    overlaps = {
        str(seed): labels for seed, labels in seen.items() if len(labels) > 1
    }
    return {
        "role_seed_pairs": role_seed_pairs,
        "bridge_training_present": bool(bridge_training_present),
        "bridge_training_role_is_bookkeeping_only": True,
        "pairwise_disjoint_roles": not overlaps,
        "overlapping_seed_values": overlaps,
        "stop_on_overlap": True,
    }


def _base_payload(
    *,
    output: Path,
    run_manifest: Mapping[str, Any],
    sample_count: int,
    degree: int,
    rank: int,
    seed: int,
    context: Mapping[str, Any],
) -> Mapping[str, Any]:
    shift_data = context.get("shift_calibration_data")
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata_date": "2026-06-19",
        "master_program": MASTER_PROGRAM,
        "subplan": PHASE10_SUBPLAN,
        "run_manifest": run_manifest,
        "diagnostic_scope": "p76_generated_ukf_frame_corrected_metric_only",
        "requested_bounds": {
            "sample_count": int(sample_count),
            "degree": int(degree),
            "rank": int(rank),
            "seed": int(seed),
            "reviewed_sample_count_max": 32,
            "reviewed_degree": 2,
            "reviewed_rank": 4,
        },
        "target_dimension": int(context["target_dim"]),
        "time_index": 1,
        "train_step_count": 0,
        "optimizer_used": False,
        "optimizer_constructed": False,
        "generated_sample_metric_only": True,
        "generated_target_cloud_used": True,
        "source_route_prefit_used": False,
        "fit_quality_claimed": False,
        "default_behavior_changed": False,
        "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "ukf_frame_manifest": context["ukf_frame_manifest"],
        "initializer_manifest": dict(context["initializer"].manifest),
        "shift_manifest": {
            "shift_constant": float(tf.convert_to_tensor(context["shift_constant"]).numpy()),
            "source": "shift_calibration_cloud_only",
            "not_selected_from_metric_values": True,
            "not_selected_from_holdout_or_replay": True,
            "cloud_present": shift_data is not None,
            "cloud_hash": (
                None
                if shift_data is None
                else str(shift_data.manifest.get("coordinate_frame_hash", ""))
            ),
            "local_clip_fraction": (
                None
                if shift_data is None
                else float(shift_data.manifest["local_clip_fraction"].numpy())
            ),
        },
        "bridge_training_cloud_policy": {
            "present": bool(context["train_data_sequence"]),
            "bookkeeping_only": True,
            "never_passed_to_corrected_heldout_density_metric": True,
            "never_used_for_training_stopping_selection_tuning_or_interpretation": True,
        },
        "nonclaims": NONCLAIMS,
        "output": str(output),
    }


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


def _tensor_list(value: tf.Tensor) -> list[float]:
    return [float(item) for item in tf.reshape(tf.convert_to_tensor(value), [-1]).numpy()]


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


if __name__ == "__main__":
    sys.exit(main())
