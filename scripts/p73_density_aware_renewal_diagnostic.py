#!/usr/bin/env python
"""P73 density-aware renewal diagnostic.

The default command runs the bounded Phase-5 P73-A renewal diagnostic.  The
``--schema-only`` and ``--smoke-only`` paths remain tiny implementation checks
and must not be read as Phase-5 evidence.
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

from bayesfilter.highdim import source_route
from bayesfilter.highdim.bases import BoundedInterval, LegendreBasis1D, ProductBasis
from bayesfilter.highdim.fitting import FixedTTFitter
from scripts import p72_support_certified_lower_gate_diagnostic as p72


RUN_START = time.monotonic()
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_OUTPUT = Path(
    "docs/plans/"
    "bayesfilter-highdim-zhao-cui-p73-bounded-renewal-diagnostic-2026-06-17.json"
)
EXPECTED_COMMAND = (
    "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
    "scripts/p73_density_aware_renewal_diagnostic.py"
)
NONCLAIMS = (
    "no P73 lower-gate pass claim",
    "no repaired P72 diagnostic claim",
    "no d18 validation claim",
    "no HMC readiness claim",
    "no rank or degree promotion",
    "no scaling claim",
    "no adaptive Zhao-Cui source-faithful parity claim",
)
P73_PHASE5_PASS_STATUS = "P73_PHASE5_DENSITY_AWARE_RENEWAL_PASSED"
P73_PHASE5_BLOCK_STATUS = "P73_PHASE5_DENSITY_AWARE_RENEWAL_BLOCKED"
P73_PHASE5_COMPLETED_STATUS = "P73_PHASE5_DENSITY_AWARE_RENEWAL_COMPLETED"
P73_ROW_SPECS = (("rank_candidate_1_2_fit36", 1, 2, 36),)
P73_SEEDS = {
    "round0_guard": {
        "step1_prior": 7321,
        "step1_process": 7601,
        "step2_process": 7602,
    },
    "round1_fresh": {
        "step1_prior": 7331,
        "step1_process": 7611,
        "step2_process": 7612,
    },
    "round1_guard": {
        "step1_prior": 7341,
        "step1_process": 7621,
        "step2_process": 7622,
    },
    "round1_audit_holdout": {
        "step1_prior": 7351,
        "step1_process": 7631,
        "step2_process": 7632,
    },
    "round1_audit_replay": {
        "step1_prior": 7361,
        "step1_process": 7641,
        "step2_process": 7642,
    },
}


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


def p73_phase4_schema_payload(output: Path) -> Mapping[str, Any]:
    policy = source_route.p73_density_aware_renewal_policy()
    optimizer = source_route.p73_density_aware_optimizer_status()
    return {
        "status": "P73_PHASE4_SCHEMA_READY_PHASE5_NOT_EXECUTED",
        "metadata_date": "2026-06-17",
        "diagnostic_scope": "p73_phase4_schema_only_not_phase5_evidence",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md"
        ),
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p73-phase4-optin-implementation-subplan-2026-06-17.md"
        ),
        "evidence_contract": {
            "question": (
                "Do the Phase-4 P73 surfaces expose renewal, audit exclusion, "
                "and density-aware objective schema without running Phase 5?"
            ),
            "baseline_comparator": "P73 Phase 2 design and Phase 3 implementation surface map.",
            "primary_criterion": (
                "Schema records P73-A, P73-B blocked status, renewal provenance, "
                "NO_AUDIT_COEFFICIENT_SELECTION, and nonclaims."
            ),
            "veto_diagnostics": (
                "phase5 diagnostic executed",
                "P73-B marked runnable despite blocked optimizer",
                "audit data allowed into coefficient selection",
                "source-faithfulness overclaim",
            ),
            "explanatory_only": ("schema field presence", "toy smoke payload"),
            "nonclaims": NONCLAIMS,
        },
        "source_route_controls": {
            "script_role": "p73_phase4_schema_not_phase5_execution",
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "thresholds_changed": False,
            "source_route_semantics_changed": False,
            "phase5_diagnostic_executed": False,
            "smoke_only_not_phase5_evidence": True,
            "policy": policy,
        },
        "arms": {
            "p73_a_renewal_only": {
                "status": "schema_ready_not_executed",
                "phase5_runnable": True,
                "training_rule": "coefficients_selected_from_F_1_only",
            },
            "p73_b_density_aware_optin": {
                "status": optimizer["status"],
                "phase5_runnable": optimizer["phase5_runnable"],
                "density_aware_objective_status": optimizer[
                    "density_aware_objective_status"
                ],
            },
        },
        "run_manifest": {
            "command": EXPECTED_COMMAND,
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
                "renewal_count": source_route.P73_RENEWAL_COUNT,
                "phase4_schema_only": True,
            },
        },
        "gate_summary": {
            "overall_status": "not_executed",
            "phase5_diagnostic_executed": False,
            "smoke_only_not_phase5_evidence": True,
            "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
        },
        "nonclaims": NONCLAIMS,
    }


def p73_smoke_payload(output: Path, command: str) -> Mapping[str, Any]:
    fit_hash = "fit-cloud-hash"
    audit_hash = "audit-cloud-hash"
    fit_records = (
        source_route.p73_renewal_role_record(
            point_id="f1-0",
            cloud_hash=fit_hash,
            role="fit",
            created_round=1,
            entered_training_round=1,
            audit_round=None,
            source_channel="fit",
            seed_or_constructor_label="phase4-smoke",
        ),
        source_route.p73_renewal_role_record(
            point_id="f1-1",
            cloud_hash=fit_hash,
            role="fresh",
            created_round=1,
            entered_training_round=1,
            audit_round=None,
            source_channel="fresh",
            seed_or_constructor_label="phase4-smoke",
        ),
    )
    audit_records = (
        source_route.p73_renewal_role_record(
            point_id="a1-0",
            cloud_hash=audit_hash,
            role="audit",
            created_round=1,
            entered_training_round=None,
            audit_round=1,
            source_channel="audit",
            seed_or_constructor_label="phase4-smoke",
        ),
    )
    predicate = source_route.p73_no_audit_coefficient_selection(
        renewal_round=1,
        coefficient_records=fit_records,
        audit_records=audit_records,
        coefficient_cloud_hashes=(fit_hash,),
        audit_cloud_hashes=(audit_hash,),
    )
    batch, batch_manifest = source_route.p73_training_batch_from_renewed_fit(
        fit_points=tf.constant([[-0.5, 0.5]], dtype=tf.float64),
        fit_target_values=tf.constant([1.0, 1.25], dtype=tf.float64),
        fit_weights=tf.ones([2], dtype=tf.float64),
        fit_records=fit_records,
    )
    row = {
        "status": "P73_PHASE4_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE",
        "phase5_diagnostic_executed": False,
        "smoke_only_not_phase5_evidence": True,
        "renewal_rounds": {
            "R": source_route.P73_RENEWAL_COUNT,
            "first_certifiable_fit": "F_1",
        },
        "no_audit_coefficient_selection": predicate,
        "training_batch_manifest": batch_manifest,
        "training_batch_shape": {
            "rows": int(batch.points.shape[0]),
            "dimension": int(batch.points.shape[1]),
        },
        "arms": {
            "p73_a_renewal_only": {
                "status": "smoke_schema_ready_not_fitted",
                "phase5_runnable": True,
            },
            "p73_b_density_aware_optin": source_route.p73_density_aware_optimizer_status(),
        },
        "nonclaims": NONCLAIMS,
    }
    payload = p73_phase4_schema_payload(output)
    return {
        **payload,
        "status": "P73_PHASE4_SMOKE_COMPLETED_NOT_PHASE5_EVIDENCE",
        "diagnostic_scope": "p73_phase4_smoke_not_phase5_evidence",
        "run_manifest": {**payload["run_manifest"], "command": command},
        "rows": {"p73_smoke_row": row},
        "gate_summary": {
            **payload["gate_summary"],
            "row_count": 1,
            "all_rows_phase5_diagnostic_executed": False,
        },
    }


def _seed_for(*, channel: str, time_index: int, part: str) -> int:
    key = f"step{int(time_index)}_{part}"
    return int(P73_SEEDS[channel][key])


def _cloud_hash(label: str, points: tf.Tensor) -> str:
    return source_route._p69_hash_tensor(f"p73_{label}_cloud_hash.v1", points)


def _records_for_cloud(
    *,
    points: tf.Tensor,
    cloud_hash: str,
    role: str,
    created_round: int,
    entered_training_round: int | None,
    audit_round: int | None,
    source_channel: str,
    prefix: str,
) -> tuple[Mapping[str, object], ...]:
    point_count = int(tf.convert_to_tensor(points, dtype=tf.float64).shape[1])
    return tuple(
        source_route.p73_renewal_role_record(
            point_id=f"{prefix}-{index}",
            cloud_hash=cloud_hash,
            role=role,
            created_round=int(created_round),
            entered_training_round=entered_training_round,
            audit_round=audit_round,
            source_channel=source_channel,
            seed_or_constructor_label=prefix,
        )
        for index in range(point_count)
    )


def _line_records_for_cloud(
    *,
    line_points: tf.Tensor,
    cloud_hash: str,
    role: str,
    source_channel: str,
    prefix: str,
    audit_round: int | None,
) -> tuple[Mapping[str, object], ...]:
    return _records_for_cloud(
        points=line_points,
        cloud_hash=cloud_hash,
        role=role,
        created_round=1,
        entered_training_round=None,
        audit_round=audit_round,
        source_channel=source_channel,
        prefix=prefix,
    )


def _select_round0_enrichment(
    *,
    fit_data,
    guard_data,
    round0_fitted_tt,
    components,
    previous_retained_object,
    target_scale: float,
) -> Mapping[str, Any]:
    line_points, line_manifest = source_route.p72_guard_line_points(
        fit_points=fit_data.local_fit_points,
        guard_points=guard_data.local_fit_points,
    )
    line_targets = p72._target_values_for_points(
        points=line_points,
        frame=fit_data.frame,
        shift_constant=fit_data.shift_constant,
        time_index=fit_data.time_index,
        components=components,
        previous_retained_object=previous_retained_object,
    )
    guard_points = tf.convert_to_tensor(guard_data.local_fit_points, dtype=tf.float64)
    guard_targets = tf.convert_to_tensor(guard_data.target_values, dtype=tf.float64)
    guard_weights = tf.convert_to_tensor(guard_data.fit_weights, dtype=tf.float64)
    guard_predictions = tf.convert_to_tensor(
        round0_fitted_tt.evaluate(tf.transpose(guard_points)),
        dtype=tf.float64,
    )
    guard_residual = tf.abs(guard_predictions - guard_targets)
    guard_rms = p72._weighted_rms(guard_predictions, guard_targets, guard_weights)
    scale = max(float(target_scale), 1e-300)
    guard_failed = tf.logical_or(
        guard_residual > source_route.P72_RESIDUAL_RMS_REL_VETO * scale,
        guard_residual > source_route.P72_RESIDUAL_MAX_REL_VETO * scale,
    )
    guard_failed_indices = tuple(int(index) for index in tf.reshape(tf.where(guard_failed), [-1]).numpy())
    guard_selected = (
        tf.gather(guard_points, guard_failed_indices, axis=1)
        if guard_failed_indices
        else tf.zeros([int(guard_points.shape[0]), 0], dtype=tf.float64)
    )
    guard_selected_targets = (
        tf.gather(guard_targets, guard_failed_indices, axis=0)
        if guard_failed_indices
        else tf.zeros([0], dtype=tf.float64)
    )
    guard_selected_weights = (
        tf.gather(guard_weights, guard_failed_indices, axis=0)
        if guard_failed_indices
        else tf.zeros([0], dtype=tf.float64)
    )
    endpoint_indices = tuple(int(value) for value in line_manifest["line_start_indices"])
    center = tf.reduce_mean(fit_data.local_fit_points, axis=1, keepdims=True)
    start_predictions = round0_fitted_tt.evaluate(
        tf.transpose(tf.repeat(center, repeats=3, axis=1))
    )
    line_gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=round0_fitted_tt,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=start_predictions,
        line_start_indices=line_manifest["line_start_indices"],
        target_scale=scale,
    )
    line_failed = line_gate["status"] == "block"
    endpoint_points = (
        tf.gather(guard_points, endpoint_indices, axis=1)
        if line_failed
        else tf.zeros([int(guard_points.shape[0]), 0], dtype=tf.float64)
    )
    endpoint_targets = (
        tf.gather(guard_targets, endpoint_indices, axis=0)
        if line_failed
        else tf.zeros([0], dtype=tf.float64)
    )
    endpoint_weights = (
        tf.gather(guard_weights, endpoint_indices, axis=0)
        if line_failed
        else tf.zeros([0], dtype=tf.float64)
    )
    selected_line_points = (
        line_points
        if line_failed
        else tf.zeros([int(line_points.shape[0]), 0], dtype=tf.float64)
    )
    selected_line_targets = (
        line_targets
        if line_failed
        else tf.zeros([0], dtype=tf.float64)
    )
    selected_line_weights = tf.ones([int(selected_line_points.shape[1])], dtype=tf.float64)
    enrichment_points = tf.concat([guard_selected, endpoint_points, selected_line_points], axis=1)
    enrichment_targets = tf.concat([guard_selected_targets, endpoint_targets, selected_line_targets], axis=0)
    enrichment_weights = tf.concat([guard_selected_weights, endpoint_weights, selected_line_weights], axis=0)
    enrichment_hash = _cloud_hash("E0_guard_and_guard_line", enrichment_points)
    records = _records_for_cloud(
        points=guard_selected,
        cloud_hash=enrichment_hash,
        role="enrichment",
        created_round=0,
        entered_training_round=1,
        audit_round=None,
        source_channel="guard",
        prefix=f"t{int(fit_data.time_index)}-E0-guard-failure",
    ) + _records_for_cloud(
        points=endpoint_points,
        cloud_hash=enrichment_hash,
        role="enrichment",
        created_round=0,
        entered_training_round=1,
        audit_round=None,
        source_channel="guard",
        prefix=f"t{int(fit_data.time_index)}-E0-guard-line-endpoint",
    ) + _records_for_cloud(
        points=selected_line_points,
        cloud_hash=enrichment_hash,
        role="enrichment",
        created_round=0,
        entered_training_round=1,
        audit_round=None,
        source_channel="guard_line",
        prefix=f"t{int(fit_data.time_index)}-E0-guard-line",
    )
    boundary = source_route.p73_validate_enrichment_boundary(
        enrichment_records=records,
    )
    return {
        "points": enrichment_points,
        "targets": enrichment_targets,
        "weights": enrichment_weights,
        "records": records,
        "hash": enrichment_hash,
        "line_points": line_points,
        "line_targets": line_targets,
        "line_manifest": line_manifest,
        "round0_guard_residual_gate": {
            "rms_relative": guard_rms / scale,
            "max_relative": float(tf.reduce_max(guard_residual).numpy()) / scale,
            "failed_indices": guard_failed_indices,
            "selected_point_count": int(guard_selected.shape[1]),
            "selection_thresholds": {
                "rms_relative_veto": source_route.P72_RESIDUAL_RMS_REL_VETO,
                "max_relative_veto": source_route.P72_RESIDUAL_MAX_REL_VETO,
            },
        },
        "round0_guard_line_gate": {
            **line_gate,
            "selected_for_enrichment": bool(line_failed),
        },
        "boundary": boundary,
        "selection_rule": (
            "E0 contains only guard points whose round-0 residual exceeds a "
            "frozen residual gate plus guard-line endpoints/probes when the "
            "round-0 guard-line gate blocks."
        ),
    }


def _make_p73_config(*, target_dim: int, fit_degree: int, fit_rank: int, row_budget: int):
    return p72._make_config(
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        row_budget=int(row_budget),
    )


def _fit_p73_renewed_step(
    *,
    fit_data,
    round0_guard_data,
    fresh_data,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
    branch_seed: str,
    convention,
    components,
    previous_retained_object,
) -> Mapping[str, Any]:
    f0_hash = _cloud_hash(f"t{int(fit_data.time_index)}_F0", fit_data.local_fit_points)
    f0_records = _records_for_cloud(
        points=fit_data.local_fit_points,
        cloud_hash=f0_hash,
        role="fit",
        created_round=0,
        entered_training_round=0,
        audit_round=None,
        source_channel="fit",
        prefix=f"t{int(fit_data.time_index)}-F0",
    )
    f0_batch, f0_training_manifest = source_route.p73_training_batch_from_renewed_fit(
        fit_points=fit_data.local_fit_points,
        fit_target_values=fit_data.target_values,
        fit_weights=fit_data.fit_weights,
        fit_records=f0_records,
        coefficient_cloud_hashes=(f0_hash,),
        renewal_round=0,
    )
    product_basis = ProductBasis(
        [LegendreBasis1D(BoundedInterval(-1.0, 1.0), int(fit_degree)) for _ in range(int(target_dim))],
        convention,
    )
    f0_config = _make_p73_config(
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        row_budget=int(f0_batch.points.shape[0]),
    )
    f0_initial_cores = source_route._source_route_seeded_channel_initial_cores(
        ranks=f0_config.ranks,
        basis_dim=int(fit_degree) + 1,
        constant_value=tf.reduce_sum(f0_batch.weights * f0_batch.target_values) / tf.reduce_sum(f0_batch.weights),
    )
    f0_result = FixedTTFitter().fit(
        product_basis=product_basis,
        samples=f0_batch,
        config=f0_config,
        initial_cores=f0_initial_cores,
        branch_seed=f"{branch_seed}-round0",
        measure_convention=convention,
        initialization_rule=source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
    )
    f0_target_scale = max(
        p72._weighted_rms(
            fit_data.target_values,
            tf.zeros_like(fit_data.target_values),
            fit_data.fit_weights,
        ),
        1e-300,
    )
    enrichment = _select_round0_enrichment(
        fit_data=fit_data,
        guard_data=round0_guard_data,
        round0_fitted_tt=f0_result.fitted_tt,
        components=components,
        previous_retained_object=previous_retained_object,
        target_scale=f0_target_scale,
    )
    n1_hash = _cloud_hash(f"t{int(fit_data.time_index)}_N1", fresh_data.local_fit_points)
    f1_points = tf.concat(
        [fit_data.local_fit_points, enrichment["points"], fresh_data.local_fit_points],
        axis=1,
    )
    f1_targets = tf.concat(
        [fit_data.target_values, enrichment["targets"], fresh_data.target_values],
        axis=0,
    )
    f1_weights = tf.concat(
        [
            tf.convert_to_tensor(fit_data.fit_weights, dtype=tf.float64),
            tf.convert_to_tensor(enrichment["weights"], dtype=tf.float64),
            tf.convert_to_tensor(fresh_data.fit_weights, dtype=tf.float64),
        ],
        axis=0,
    )
    f1_hash = _cloud_hash(f"t{int(fit_data.time_index)}_F1", f1_points)
    fresh_records = _records_for_cloud(
        points=fresh_data.local_fit_points,
        cloud_hash=n1_hash,
        role="fresh",
        created_round=1,
        entered_training_round=1,
        audit_round=None,
        source_channel="fresh",
        prefix=f"t{int(fit_data.time_index)}-N1",
    )
    f1_records = (
        tuple({**dict(record), "cloud_hash": f1_hash} for record in f0_records)
        + tuple({**dict(record), "cloud_hash": f1_hash} for record in enrichment["records"])
        + tuple({**dict(record), "cloud_hash": f1_hash} for record in fresh_records)
    )
    batch, training_manifest = source_route.p73_training_batch_from_renewed_fit(
        fit_points=f1_points,
        fit_target_values=f1_targets,
        fit_weights=f1_weights,
        fit_records=f1_records,
        coefficient_cloud_hashes=(f1_hash,),
        renewal_round=1,
    )
    config = _make_p73_config(
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        row_budget=int(batch.points.shape[0]),
    )
    initial_cores = source_route._source_route_seeded_channel_initial_cores(
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
        initialization_rule=source_route.P70_FIXED_BRANCH_INITIALIZATION_RULE,
    )
    return {
        "product_basis": product_basis,
        "config": config,
        "initial_cores": initial_cores,
        "round0_product_basis": product_basis,
        "round0_config": f0_config,
        "round0_initial_cores": f0_initial_cores,
        "round0_result": f0_result,
        "round0_training_batch": f0_batch,
        "round0_training_manifest": f0_training_manifest,
        "result": result,
        "training_batch": batch,
        "training_manifest": training_manifest,
        "F0": {
            "points": fit_data.local_fit_points,
            "targets": fit_data.target_values,
            "weights": fit_data.fit_weights,
            "hash": f0_hash,
            "records": f0_records,
        },
        "E0": enrichment,
        "N1": {
            "points": fresh_data.local_fit_points,
            "targets": fresh_data.target_values,
            "weights": fresh_data.fit_weights,
            "hash": n1_hash,
            "records": fresh_records,
        },
        "F1": {
            "points": f1_points,
            "targets": f1_targets,
            "weights": f1_weights,
            "hash": f1_hash,
            "records": f1_records,
        },
    }


def _support_gate_for_points(
    *,
    role: str,
    points: tf.Tensor,
    fit_points: tf.Tensor,
    data,
) -> Mapping[str, Any]:
    return source_route.p72_support_clipping_coverage(
        role=role,
        points=points,
        fit_points=fit_points,
        clip_fraction=data.manifest.get("local_clip_fraction"),
        local_max_abs_before_clip=data.manifest.get("local_max_abs_before_clip"),
    )


def _normalizer_terms_for_fit(fitted_tt, product_basis: ProductBasis, convention) -> Mapping[str, Any]:
    return p72._normalizer_terms(fitted_tt, product_basis, convention)


def _condition_records_from_fit(fit: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    return p72._condition_records_from_fit(fit)


def _line_gate_for_endpoint_data(
    *,
    role: str,
    fitted_tt,
    fit_points: tf.Tensor,
    endpoint_data,
    frame,
    shift_constant,
    time_index: int,
    components,
    previous_retained_object,
    target_scale: float,
) -> Mapping[str, Any]:
    line_points, manifest = source_route.p72_guard_line_points(
        fit_points=fit_points,
        guard_points=endpoint_data.local_fit_points,
    )
    line_targets = p72._target_values_for_points(
        points=line_points,
        frame=frame,
        shift_constant=shift_constant,
        time_index=int(time_index),
        components=components,
        previous_retained_object=previous_retained_object,
    )
    center = tf.reduce_mean(fit_points, axis=1, keepdims=True)
    starts = fitted_tt.evaluate(tf.transpose(tf.repeat(center, repeats=3, axis=1)))
    gate = source_route.p72_line_probe_diagnostics(
        fitted_tt=fitted_tt,
        line_points=line_points,
        line_target_values=line_targets,
        start_prediction_values=starts,
        line_start_indices=manifest["line_start_indices"],
        target_scale=target_scale,
    )
    line_hash = _cloud_hash(f"t{int(time_index)}_{role}_line", line_points)
    return {
        **gate,
        "line_points": line_points,
        "line_targets": line_targets,
        "line_manifest": manifest,
        "line_hash": line_hash,
        "line_records": _line_records_for_cloud(
            line_points=line_points,
            cloud_hash=line_hash,
            role=role,
            source_channel=role,
            prefix=f"t{int(time_index)}-{role}",
            audit_round=1 if role == "audit_line" else None,
        ),
        "line_role": role,
    }


def _density_for_fit(fit: Mapping[str, Any], convention):
    return p72._transport_from_fit(fit, convention).density


def _p73_step_gate_row(
    *,
    fit_data,
    round0_guard_data,
    fresh_data,
    guard_data,
    audit_holdout_data,
    audit_replay_data,
    fit: Mapping[str, Any],
    components,
    previous_retained_object,
    target_dim: int,
    fit_degree: int,
    fit_rank: int,
) -> Mapping[str, Any]:
    fitted_tt = fit["result"].fitted_tt
    f1 = fit["F1"]
    target_scale = max(
        p72._weighted_rms(
            f1["targets"],
            tf.zeros_like(f1["targets"]),
            f1["weights"],
        ),
        1e-300,
    )
    fit_gate = p72._cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=f1["points"],
        target_values=f1["targets"],
        weights=f1["weights"],
        target_scale=target_scale,
    )
    guard_gate = p72._cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=guard_data.local_fit_points,
        target_values=guard_data.target_values,
        weights=guard_data.fit_weights,
        target_scale=target_scale,
    )
    audit_holdout_gate = p72._cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=audit_holdout_data.local_fit_points,
        target_values=audit_holdout_data.target_values,
        weights=audit_holdout_data.fit_weights,
        target_scale=target_scale,
    )
    audit_replay_gate = p72._cloud_residual_gate(
        fitted_tt=fitted_tt,
        points=audit_replay_data.local_fit_points,
        target_values=audit_replay_data.target_values,
        weights=audit_replay_data.fit_weights,
        target_scale=target_scale,
    )
    residual_gates = {
        "rms_relative": max(
            fit_gate["rms_relative"],
            guard_gate["rms_relative"],
            audit_holdout_gate["rms_relative"],
            audit_replay_gate["rms_relative"],
        ),
        "max_relative": max(
            fit_gate["max_relative"],
            guard_gate["max_relative"],
            audit_holdout_gate["max_relative"],
            audit_replay_gate["max_relative"],
        ),
        "fit": fit_gate,
        "fresh_guard": guard_gate,
        "fresh_audit_holdout": audit_holdout_gate,
        "fresh_audit_replay": audit_replay_gate,
    }
    support_gates = {
        "fit": source_route.p72_support_clipping_coverage(
            role="fit",
            points=f1["points"],
            fit_points=f1["points"],
            clip_fraction=0.0,
            local_max_abs_before_clip=float(tf.reduce_max(tf.abs(f1["points"])).numpy()),
        ),
        "round0_guard_enrichment": _support_gate_for_points(
            role="round0_guard_enrichment",
            points=round0_guard_data.local_fit_points,
            fit_points=f1["points"],
            data=round0_guard_data,
        ),
        "fresh": _support_gate_for_points(
            role="fresh",
            points=fresh_data.local_fit_points,
            fit_points=f1["points"],
            data=fresh_data,
        ),
        "fresh_guard": _support_gate_for_points(
            role="fresh_guard",
            points=guard_data.local_fit_points,
            fit_points=f1["points"],
            data=guard_data,
        ),
        "fresh_audit_holdout": _support_gate_for_points(
            role="fresh_audit_holdout",
            points=audit_holdout_data.local_fit_points,
            fit_points=f1["points"],
            data=audit_holdout_data,
        ),
        "fresh_audit_replay": _support_gate_for_points(
            role="fresh_audit_replay",
            points=audit_replay_data.local_fit_points,
            fit_points=f1["points"],
            data=audit_replay_data,
        ),
    }
    guard_line = _line_gate_for_endpoint_data(
        role="guard_line",
        fitted_tt=fitted_tt,
        fit_points=f1["points"],
        endpoint_data=guard_data,
        frame=fit_data.frame,
        shift_constant=fit_data.shift_constant,
        time_index=fit_data.time_index,
        components=components,
        previous_retained_object=previous_retained_object,
        target_scale=target_scale,
    )
    audit_line = _line_gate_for_endpoint_data(
        role="audit_line",
        fitted_tt=fitted_tt,
        fit_points=f1["points"],
        endpoint_data=audit_holdout_data,
        frame=fit_data.frame,
        shift_constant=fit_data.shift_constant,
        time_index=fit_data.time_index,
        components=components,
        previous_retained_object=previous_retained_object,
        target_scale=target_scale,
    )
    line_gates = {"guard_line": guard_line, "audit_line": audit_line}
    line_status = "block" if any(gate.get("status") == "block" for gate in line_gates.values()) else "pass"
    audit_hashes = (
        _cloud_hash(f"t{int(fit_data.time_index)}_A1_holdout", audit_holdout_data.local_fit_points),
        _cloud_hash(f"t{int(fit_data.time_index)}_A1_replay", audit_replay_data.local_fit_points),
    )
    audit_records = _records_for_cloud(
        points=audit_holdout_data.local_fit_points,
        cloud_hash=audit_hashes[0],
        role="audit",
        created_round=1,
        entered_training_round=None,
        audit_round=1,
        source_channel="audit",
        prefix=f"t{int(fit_data.time_index)}-A1-holdout",
    ) + _records_for_cloud(
        points=audit_replay_data.local_fit_points,
        cloud_hash=audit_hashes[1],
        role="audit",
        created_round=1,
        entered_training_round=None,
        audit_round=1,
        source_channel="audit",
        prefix=f"t{int(fit_data.time_index)}-A1-replay",
    )
    no_audit = source_route.p73_no_audit_coefficient_selection(
        renewal_round=1,
        coefficient_records=f1["records"],
        audit_records=audit_records,
        audit_line_records=audit_line["line_records"],
        coefficient_cloud_hashes=(f1["hash"],),
        audit_cloud_hashes=audit_hashes,
        audit_line_cloud_hashes=(audit_line["line_hash"],),
        enrichment_records=fit["E0"]["records"],
    )
    density = _density_for_fit(fit, fit["product_basis"].convention)
    density_aware = source_route.p73_density_aware_cross_entropy(
        density=density,
        support_points=f1["points"],
        target_values=f1["targets"],
        support_weights=f1["weights"],
        point_records=f1["records"],
        audit_records=audit_records,
        audit_line_records=audit_line["line_records"],
        coefficient_cloud_hashes=(f1["hash"],),
        audit_cloud_hashes=audit_hashes,
        audit_line_cloud_hashes=(audit_line["line_hash"],),
    )
    normalizer_gate = source_route.p72_full_normalizer_gate(
        _normalizer_terms_for_fit(fitted_tt, fit["product_basis"], fit["product_basis"].convention)
    )
    condition_gate = source_route.p72_condition_effective_rank_gate(
        _condition_records_from_fit(fit)
    )
    rank_activity_raw = source_route._p70_channel_activity_diagnostics(
        cores=fitted_tt.cores,
        target_dim=int(target_dim),
        fit_rank=int(fit_rank),
    )
    rank_activity = {
        **rank_activity_raw,
        "status": "ok" if rank_activity_raw.get("status") == "rank_channel_activity_pass" else rank_activity_raw.get("status"),
    }
    line_points_all = tf.concat([guard_line["line_points"], audit_line["line_points"]], axis=1)
    provenance = {
        "policy_id": "p73_provenance_manifest.v1",
        "branch_identity": fit["result"].branch_hash.value,
        "target_hash": source_route._p69_hash_tensor("p73_provenance_target_hash.v1", f1["targets"]),
        "frame_hash": source_route._p69_frame_hash(fit_data.frame),
        "shift_constant": float(tf.convert_to_tensor(fit_data.shift_constant, dtype=tf.float64).numpy()),
        "F0_hash": fit["F0"]["hash"],
        "E0_hash": fit["E0"]["hash"],
        "N1_hash": fit["N1"]["hash"],
        "F1_hash": fit["F1"]["hash"],
        "G1_hash": _cloud_hash(f"t{int(fit_data.time_index)}_G1", guard_data.local_fit_points),
        "A1_hashes": audit_hashes,
        "guard_line_hash": guard_line["line_hash"],
        "audit_line_hash": audit_line["line_hash"],
        "audit_exclusion_provenance": "P73 coefficient selection uses F1 only; A1 and audit-line records are excluded",
        "no_audit_coefficient_selection": no_audit,
        "classification": "extension_or_invention_for_renewal_and_audit_gates",
        "nonclaims": (
            "P73 renewal provenance is not source-faithful Zhao-Cui evidence",
            "provenance hashes are not validation evidence",
        ),
    }
    p72_provenance_compat = {
        "branch_identity": provenance["branch_identity"],
        "target_hash": provenance["target_hash"],
        "frame_hash": provenance["frame_hash"],
        "shift_constant": provenance["shift_constant"],
        "fit_cloud_hash": provenance["F1_hash"],
        "guard_cloud_hash": provenance["G1_hash"],
        "audit_cloud_hash": "|".join(audit_hashes),
        "line_hash": source_route._p69_hash_tensor("p73_all_line_points_hash.v1", line_points_all),
        "audit_exclusion_provenance": provenance["audit_exclusion_provenance"],
    }
    summary = source_route.p72_gate_summary(
        residual_gates=residual_gates,
        support_gates=support_gates,
        normalizer_gate=normalizer_gate,
        line_gate={"status": line_status, "channels": line_gates},
        condition_gate=condition_gate,
        rank_activity=rank_activity,
        provenance=p72_provenance_compat,
    )
    reasons = list(summary["reasons"])
    if no_audit["status"] != "pass":
        reasons.append("no_audit_coefficient_selection_block")
    if fit["E0"]["boundary"]["status"] != "pass":
        reasons.append("enrichment_boundary_block")
    if density_aware["status"] != "pass":
        reasons.append("density_aware_evaluator_block")
    p73_status = source_route.P73_BLOCK_STATUS if reasons else source_route.P73_PASS_STATUS
    return {
        "time_index": int(fit_data.time_index),
        "fit_status": fit["result"].status.value,
        "fit_termination_reason": fit["result"].termination_reason,
        "degree": int(fit_degree),
        "rank": int(fit_rank),
        "fit_point_count": int(f1["points"].shape[1]),
        "F0_point_count": int(fit["F0"]["points"].shape[1]),
        "E0_point_count": int(fit["E0"]["points"].shape[1]),
        "N1_point_count": int(fit["N1"]["points"].shape[1]),
        "G1_point_count": int(guard_data.local_fit_points.shape[1]),
        "A1_point_count": int(audit_holdout_data.local_fit_points.shape[1] + audit_replay_data.local_fit_points.shape[1]),
        "training_batch_manifest": fit["training_manifest"],
        "renewal_provenance": provenance,
        "no_audit_coefficient_selection": no_audit,
        "enrichment_boundary": fit["E0"]["boundary"],
        "density_aware_objective": density_aware,
        "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
        "residual_gates": residual_gates,
        "support_gates": support_gates,
        "normalizer_gate": normalizer_gate,
        "line_gates": line_gates,
        "condition_effective_rank_gate": condition_gate,
        "rank_activity": rank_activity,
        "gate_summary": {**summary, "status": p73_status, "reasons": tuple(dict.fromkeys(reasons))},
        "status": p73_status,
        "nonclaims": NONCLAIMS,
    }


def _skipped_p73_step_after_prior_block(
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
        "fit_sample_count": int(fit_sample_count),
        "fit_status": "not_fit_prior_step_gate_blocked",
        "status": source_route.P73_BLOCK_STATUS,
        "skip_reason": "prior_step_gate_blocked_no_retained_object",
        "skipped_after_time_index": int(skipped_after_time_index),
        "prior_step_reasons": tuple(skipped_reasons),
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
        "gate_summary": {
            "status": source_route.P73_BLOCK_STATUS,
            "reasons": ("prior_step_gate_blocked_no_retained_object",),
            "prior_step_reasons": tuple(skipped_reasons),
        },
        "nonclaims": NONCLAIMS,
    }


def _diagnostic_data(
    *,
    model,
    observations,
    time_index: int,
    sample_count: int,
    frame,
    shift_constant,
    channel: str,
    construction: str,
    previous_retained_object=None,
):
    kwargs: dict[str, Any] = {
        "model": model,
        "observations": observations,
        "time_index": int(time_index),
        "diagnostic_sample_count": int(sample_count),
        "frame": frame,
        "shift_constant": shift_constant,
        "previous_retained_object": previous_retained_object,
        "construction": construction,
    }
    if int(time_index) == 1:
        kwargs["prior_seed"] = _seed_for(channel=channel, time_index=1, part="prior")
        kwargs["process_noise_seed"] = _seed_for(channel=channel, time_index=1, part="process")
    else:
        kwargs["process_noise_seed"] = _seed_for(channel=channel, time_index=2, part="process")
    return source_route._p69_author_sir_source_diagnostic_data_for_step(**kwargs)


def _build_p73_row(
    *,
    label: str,
    fit_degree: int,
    fit_rank: int,
    fit_sample_count: int,
) -> Mapping[str, Any]:
    model = source_route.zhao_cui_sir_austria_model()
    observations = model.simulate(final_time=2, seed=5901)[1]
    d = model.parameter_dim()
    m = model.state_dim()
    target_dim = d + 2 * m
    convention = source_route._p59_reference_convention()
    prior_log_density, transition_log_density, likelihood_t1 = source_route._p59_author_sir_source_density_callbacks(
        model,
        observations[1],
    )
    _, _, likelihood_t2 = source_route._p59_author_sir_source_density_callbacks(model, observations[2])
    components1 = source_route.SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_t1,
        prior_log_density_fn=prior_log_density,
    )
    components2 = source_route.SourceRouteSequentialDensityComponents(
        parameter_dim=d,
        state_dim=m,
        transition_log_density_fn=transition_log_density,
        likelihood_log_density_fn=likelihood_t2,
        prior_log_density_fn=None,
    )
    fit_data1 = source_route._p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=1,
        fit_sample_count=int(fit_sample_count),
    )
    round0_guard1 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=1,
        sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        channel="round0_guard",
        construction="p73_round0_step1_guard_enrichment_seed",
    )
    fresh1 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=1,
        sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        channel="round1_fresh",
        construction="p73_round1_step1_fresh_support_seed",
    )
    guard1 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=1,
        sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        channel="round1_guard",
        construction="p73_round1_step1_fresh_guard_seed",
    )
    audit_holdout1 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=1,
        sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        channel="round1_audit_holdout",
        construction="p73_round1_step1_fresh_audit_holdout_seed",
    )
    audit_replay1 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=1,
        sample_count=int(fit_sample_count),
        frame=fit_data1.frame,
        shift_constant=fit_data1.shift_constant,
        channel="round1_audit_replay",
        construction="p73_round1_step1_fresh_audit_replay_seed",
    )
    fit1 = _fit_p73_renewed_step(
        fit_data=fit_data1,
        round0_guard_data=round0_guard1,
        fresh_data=fresh1,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        branch_seed=f"p73-phase5-step1-{label}",
        convention=convention,
        components=components1,
        previous_retained_object=None,
    )
    step1 = _p73_step_gate_row(
        fit_data=fit_data1,
        round0_guard_data=round0_guard1,
        fresh_data=fresh1,
        guard_data=guard1,
        audit_holdout_data=audit_holdout1,
        audit_replay_data=audit_replay1,
        fit=fit1,
        components=components1,
        previous_retained_object=None,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
    )
    if step1["status"] != source_route.P73_PASS_STATUS:
        step2 = _skipped_p73_step_after_prior_block(
            time_index=2,
            fit_degree=fit_degree,
            fit_rank=fit_rank,
            fit_sample_count=fit_sample_count,
            skipped_after_time_index=1,
            skipped_reasons=tuple(step1.get("gate_summary", {}).get("reasons", ())),
        )
        return {
            "label": str(label),
            "degree": int(fit_degree),
            "rank": int(fit_rank),
            "fit_sample_count": int(fit_sample_count),
            "status": source_route.P73_BLOCK_STATUS,
            "phase5_diagnostic_executed": True,
            "smoke_only_not_phase5_evidence": False,
            "arms": {
                "p73_a_renewal_only": {
                    "status": source_route.P73_BLOCK_STATUS,
                    "steps": (step1, step2),
                },
                "p73_b_density_aware_optin": source_route.p73_density_aware_optimizer_status(),
            },
            "sequential_status": "not_run_prior_step_gate_blocked",
            "sequential_log_marginal_likelihood": None,
            "row_block_reason": "step1_gate_blocked_no_retained_object",
            "nonclaims": NONCLAIMS,
        }
    retained1 = p72._retained_from_p72_fit(
        fit=fit1,
        fit_data=fit_data1,
        components=components1,
        convention=convention,
        target_dim=target_dim,
        retained_sample_count=int(fit_sample_count),
    )
    fit_data2 = source_route._p59_author_sir_source_fit_data_for_step(
        model=model,
        observations=observations,
        time_index=2,
        fit_sample_count=int(fit_sample_count),
        previous_retained_object=retained1,
    )
    round0_guard2 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=2,
        sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        channel="round0_guard",
        construction="p73_round0_step2_guard_enrichment_seed",
    )
    fresh2 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=2,
        sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        channel="round1_fresh",
        construction="p73_round1_step2_fresh_support_seed",
    )
    guard2 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=2,
        sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        channel="round1_guard",
        construction="p73_round1_step2_fresh_guard_seed",
    )
    audit_holdout2 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=2,
        sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        channel="round1_audit_holdout",
        construction="p73_round1_step2_fresh_audit_holdout_seed",
    )
    audit_replay2 = _diagnostic_data(
        model=model,
        observations=observations,
        time_index=2,
        sample_count=int(fit_sample_count),
        frame=fit_data2.frame,
        shift_constant=fit_data2.shift_constant,
        previous_retained_object=retained1,
        channel="round1_audit_replay",
        construction="p73_round1_step2_fresh_audit_replay_seed",
    )
    fit2 = _fit_p73_renewed_step(
        fit_data=fit_data2,
        round0_guard_data=round0_guard2,
        fresh_data=fresh2,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
        branch_seed=f"p73-phase5-step2-{label}",
        convention=convention,
        components=components2,
        previous_retained_object=retained1,
    )
    step2 = _p73_step_gate_row(
        fit_data=fit_data2,
        round0_guard_data=round0_guard2,
        fresh_data=fresh2,
        guard_data=guard2,
        audit_holdout_data=audit_holdout2,
        audit_replay_data=audit_replay2,
        fit=fit2,
        components=components2,
        previous_retained_object=retained1,
        target_dim=target_dim,
        fit_degree=fit_degree,
        fit_rank=fit_rank,
    )
    row_status = (
        source_route.P73_PASS_STATUS
        if step1["status"] == source_route.P73_PASS_STATUS and step2["status"] == source_route.P73_PASS_STATUS
        else source_route.P73_BLOCK_STATUS
    )
    return {
        "label": str(label),
        "degree": int(fit_degree),
        "rank": int(fit_rank),
        "fit_sample_count": int(fit_sample_count),
        "status": row_status,
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "arms": {
            "p73_a_renewal_only": {
                "status": row_status,
                "steps": (step1, step2),
            },
            "p73_b_density_aware_optin": source_route.p73_density_aware_optimizer_status(),
        },
        "sequential_status": "not_run_gate_failed" if row_status != source_route.P73_PASS_STATUS else "eligible_for_later_validation_plan",
        "sequential_log_marginal_likelihood": None,
        "nonclaims": NONCLAIMS,
    }


def p73_phase5_rows() -> Mapping[str, Mapping[str, Any]]:
    rows: dict[str, Mapping[str, Any]] = {}
    for label, degree, rank, fit_count in P73_ROW_SPECS:
        try:
            rows[label] = _build_p73_row(
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
                "status": source_route.P73_BLOCK_STATUS,
                "phase5_diagnostic_executed": True,
                "smoke_only_not_phase5_evidence": False,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
                "block_reason": "p73_phase5_row_exception_fail_closed",
                "arms": {
                    "p73_a_renewal_only": {"status": source_route.P73_BLOCK_STATUS},
                    "p73_b_density_aware_optin": source_route.p73_density_aware_optimizer_status(),
                },
                "nonclaims": NONCLAIMS,
            }
    return rows


def p73_phase5_payload(output: Path, command: str) -> Mapping[str, Any]:
    rows = p73_phase5_rows()
    failed = tuple(
        label
        for label, row in rows.items()
        if row.get("status") != source_route.P73_PASS_STATUS
    )
    gate_summary = {
        "overall_status": "pass" if not failed else "block",
        "failed_row_labels": failed,
        "phase5_diagnostic_executed": True,
        "smoke_only_not_phase5_evidence": False,
        "schema_only_sentinel_present": False,
        "baseline_comparator": "P72 Phase 5 blocked rank_candidate_1_2_fit36 row",
        "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
        "nonclaims": NONCLAIMS,
    }
    policy = source_route.p73_density_aware_renewal_policy()
    return {
        "status": P73_PHASE5_PASS_STATUS if not failed else P73_PHASE5_BLOCK_STATUS,
        "metadata_date": "2026-06-17",
        "diagnostic_scope": "p73_phase5_bounded_renewal_real_p73_a_rows",
        "master_program": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p73-density-aware-renewed-support-master-program-2026-06-17.md"
        ),
        "subplan": (
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p73-phase5-bounded-renewal-diagnostic-subplan-2026-06-17.md"
        ),
        "evidence_contract": {
            "question": (
                "Does one-renewal P73-A reduce or clear the P72 lower-gate blockers "
                "under fresh guard/audit certification without training on same-round audit data?"
            ),
            "baseline_comparator": (
                "P72 Phase 5 blocked diagnostic row rank_candidate_1_2_fit36."
            ),
            "primary_criterion": (
                "P73-A row must pass fit, fresh guard, fresh audit, guard-line, "
                "audit-line, support, normalizer, condition/effective-rank, "
                "rank-activity, and NO_AUDIT_COEFFICIENT_SELECTION gates."
            ),
            "veto_diagnostics": (
                "audit or audit-line points in coefficient selection",
                "certification on newly added training points",
                "nonfinite values",
                "residual/line/support/normalizer/condition/rank block",
                "threshold drift",
                "P73-B executed despite blocked optimizer",
            ),
            "explanatory_only": (
                "training loss",
                "fit-cloud cross-entropy",
                "runtime",
                "condition spectra beyond frozen gate",
            ),
            "nonclaims": NONCLAIMS,
        },
        "source_route_controls": {
            "script_role": "p73_phase5_real_bounded_renewal_diagnostic_runner",
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "thresholds_changed": False,
            "source_route_semantics_changed": False,
            "phase5_diagnostic_executed": True,
            "smoke_only_not_phase5_evidence": False,
            "schema_only_default_path": False,
            "policy": policy,
            "p73_b_optimizer_status": source_route.P73_B_OPTIMIZER_BLOCKED,
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
            "random_seeds": {
                "model_simulation": 5901,
                "p73": P73_SEEDS,
            },
            "row_specs": P73_ROW_SPECS,
            "cpu_only_intent": "CUDA_VISIBLE_DEVICES=-1",
        },
        "rows": rows,
        "gate_summary": gate_summary,
        "nonclaims": NONCLAIMS,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--schema-only", action="store_true")
    parser.add_argument(
        "--smoke-only",
        action="store_true",
        help="emit a tiny Phase-4 smoke payload; still not Phase-5 evidence",
    )
    args = parser.parse_args(argv)
    command = EXPECTED_COMMAND
    if args.output != DEFAULT_OUTPUT:
        command = f"{command} --output {args.output}"
    if args.schema_only:
        command = f"{command} --schema-only"
    if args.smoke_only:
        command = f"{command} --smoke-only"
    payload = (
        p73_phase4_schema_payload(args.output)
        if args.schema_only
        else p73_smoke_payload(args.output, command)
        if args.smoke_only
        else p73_phase5_payload(args.output, command)
    )
    _write_payload(args.output, payload)
    print(json.dumps({"p73_status": payload["status"], "gate_summary": _jsonable(payload["gate_summary"])}, sort_keys=True))
    return 0 if payload["gate_summary"].get("overall_status") in {"pass", "block", "not_executed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
