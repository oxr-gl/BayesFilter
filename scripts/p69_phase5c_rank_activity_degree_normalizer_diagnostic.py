#!/usr/bin/env python
"""P69 Phase 5c bounded rank-activity and degree-normalizer diagnostic.

This script reconstructs only the four Phase 3 comparator rows needed by the
Phase 5c subplan.  It inspects fitted fixed-TTSIRT artifacts after assembly; it
does not alter source-route semantics, thresholds, or branch construction.
"""

from __future__ import annotations

import argparse
import json
import math
import os
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

import bayesfilter.highdim.source_route as source_route


RUN_START = time.monotonic()

ROW_SPECS = (
    ("rank_candidate_1_2_fit36", 1, 2, 36),
    ("rank_stronger_1_3_fit36", 1, 3, 36),
    ("degree_candidate_1_2_fit24", 1, 2, 24),
    ("degree_stronger_2_2_fit24", 2, 2, 24),
)


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


def _event(stage: str, status: str, **detail: Any) -> Mapping[str, Any]:
    payload = {
        "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
        "stage": stage,
        "status": status,
        **detail,
    }
    print(json.dumps({"p69_phase5c_progress": _jsonable(payload)}, sort_keys=True), flush=True)
    return payload


def _write_payload(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_jsonable(payload), indent=2, sort_keys=True) + "\n")


def _base_payload(*, rows: Mapping[str, Mapping[str, Any]], output: Path, status: str) -> Mapping[str, Any]:
    return {
        "status": status,
        "metadata_date": "2026-06-15",
        "diagnostic_scope": "bounded_four_row_phase3_reconstruction",
        "evidence_contract": {
            "question": (
                "Are rank-3 channels inactive by construction/fit, and is degree-2 "
                "instability driven by normalizer/design scaling rather than route wiring?"
            ),
            "baseline_comparator": (
                "Phase 3 rank 2 vs rank 3 row pair and degree 1 vs degree 2 row pair"
            ),
            "primary_criterion": (
                "direct diagnostics or blocker for rank-channel activity and "
                "degree-normalizer/design sensitivity without threshold changes"
            ),
            "veto_diagnostics": (
                "source_route_drift",
                "branch_identity_drift",
                "threshold_tuning",
                "adaptive_parity_claim",
                "d18_scaling_hmc_readiness_claim",
            ),
            "nonclaims": (
                "no correctness claim",
                "no scaling-readiness claim",
                "no HMC-readiness claim",
                "no adaptive Zhao-Cui parity claim",
                "no paper-failure claim",
            ),
        },
        "source_route_controls": {
            "script_role": "post_fit_readonly_diagnostic",
            "row_specs": ROW_SPECS,
            "cpu_only": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
            "thresholds_changed": False,
            "source_route_semantics_changed": False,
        },
        "rows": rows,
        "run_manifest": {
            "command": (
                "CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
                "scripts/p69_phase5c_rank_activity_degree_normalizer_diagnostic.py"
            ),
            "elapsed_seconds": round(time.monotonic() - RUN_START, 3),
            "output": str(output),
        },
    }


def _tensor_stats(values: tf.Tensor) -> Mapping[str, Any]:
    tensor = tf.reshape(tf.convert_to_tensor(values, dtype=tf.float64), [-1])
    return {
        "count": int(tensor.shape[0]),
        "min": float(tf.reduce_min(tensor).numpy()),
        "max": float(tf.reduce_max(tensor).numpy()),
        "mean": float(tf.reduce_mean(tensor).numpy()),
        "rms": float(tf.sqrt(tf.reduce_mean(tf.square(tensor))).numpy()),
        "std": float(tf.math.reduce_std(tensor).numpy()),
        "l2_norm": float(tf.linalg.norm(tensor).numpy()),
        "max_abs": float(tf.reduce_max(tf.abs(tensor)).numpy()),
    }


def _step_sqrt_tt(step: Any) -> Any:
    transport = step.retained_object.transport_object
    density = getattr(transport, "density", None)
    sqrt_tt = getattr(density, "sqrt_tt", None)
    if sqrt_tt is None:
        raise RuntimeError("step transport does not expose density.sqrt_tt")
    return sqrt_tt


def _rank_channel_summary(sqrt_tt: Any, fit_rank: int) -> Mapping[str, Any]:
    rank = int(fit_rank)
    extra_channel = rank - 1 if rank > 1 else None
    rows = []
    core_total_norms = []
    active_channel_indices = set()
    extra_slice_norms = []
    extra_nonzero_slices = 0
    for axis, core in enumerate(sqrt_tt.cores):
        values = tf.convert_to_tensor(core.values, dtype=tf.float64)
        core_total_norm = float(tf.linalg.norm(tf.reshape(values, [-1])).numpy())
        core_total_norms.append(core_total_norm)
        left_norms = tuple(
            float(tf.linalg.norm(tf.reshape(values[left_index, :, :], [-1])).numpy())
            for left_index in range(core.left_rank)
        )
        right_norms = tuple(
            float(tf.linalg.norm(tf.reshape(values[:, :, right_index], [-1])).numpy())
            for right_index in range(core.right_rank)
        )
        diagonal_norms = tuple(
            float(tf.linalg.norm(values[index, :, index]).numpy())
            for index in range(min(core.left_rank, core.right_rank))
        )
        active_left = tuple(index for index, norm in enumerate(left_norms) if norm > 0.0)
        active_right = tuple(index for index, norm in enumerate(right_norms) if norm > 0.0)
        active_channel_indices.update(active_left)
        active_channel_indices.update(active_right)
        extra_left_norm = (
            None
            if extra_channel is None or extra_channel >= core.left_rank
            else float(tf.linalg.norm(tf.reshape(values[extra_channel, :, :], [-1])).numpy())
        )
        extra_right_norm = (
            None
            if extra_channel is None or extra_channel >= core.right_rank
            else float(tf.linalg.norm(tf.reshape(values[:, :, extra_channel], [-1])).numpy())
        )
        if extra_left_norm is not None:
            extra_slice_norms.append(extra_left_norm)
            if extra_left_norm > 0.0:
                extra_nonzero_slices += 1
        if extra_right_norm is not None:
            extra_slice_norms.append(extra_right_norm)
            if extra_right_norm > 0.0:
                extra_nonzero_slices += 1
        rows.append(
            {
                "axis": int(axis),
                "shape": (core.left_rank, core.basis_dim, core.right_rank),
                "total_norm": core_total_norm,
                "nonzero_entries": int(tf.math.count_nonzero(values).numpy()),
                "left_slice_norms": left_norms,
                "right_slice_norms": right_norms,
                "diagonal_channel_norms": diagonal_norms,
                "active_left_channels": active_left,
                "active_right_channels": active_right,
                "extra_channel_index": extra_channel,
                "extra_left_slice_norm": extra_left_norm,
                "extra_right_slice_norm": extra_right_norm,
            }
        )
    active_declared_channels = tuple(
        index for index in range(rank) if index in active_channel_indices
    )
    inactive_declared_channels = tuple(
        index for index in range(rank) if index not in active_channel_indices
    )
    return {
        "rank_tuple": sqrt_tt.rank_tuple(),
        "declared_internal_rank": rank,
        "core_count": len(sqrt_tt.cores),
        "core_total_norm_min": min(core_total_norms),
        "core_total_norm_max": max(core_total_norms),
        "active_declared_channels": active_declared_channels,
        "inactive_declared_channels": inactive_declared_channels,
        "active_channel_count": len(active_declared_channels),
        "extra_channel_index": extra_channel,
        "extra_channel_nonzero_slice_count": extra_nonzero_slices,
        "extra_channel_max_slice_norm": (
            max(extra_slice_norms) if extra_slice_norms else None
        ),
        "extra_channel_norms_all_zero": (
            None if not extra_slice_norms else all(norm == 0.0 for norm in extra_slice_norms)
        ),
        "core_channel_rows": rows,
    }


def _degree_activity_summary(sqrt_tt: Any) -> Mapping[str, Any]:
    rows = []
    degree_channel_norms = {}
    for axis, core in enumerate(sqrt_tt.cores):
        values = tf.convert_to_tensor(core.values, dtype=tf.float64)
        basis_norms = tuple(
            float(tf.linalg.norm(tf.reshape(values[:, basis_index, :], [-1])).numpy())
            for basis_index in range(core.basis_dim)
        )
        for basis_index, norm in enumerate(basis_norms):
            degree_channel_norms.setdefault(basis_index, []).append(norm)
        rows.append(
            {
                "axis": int(axis),
                "basis_dim": core.basis_dim,
                "basis_channel_norms": basis_norms,
                "active_basis_channels": tuple(
                    index for index, norm in enumerate(basis_norms) if norm > 0.0
                ),
            }
        )
    return {
        "basis_dim": sqrt_tt.cores[0].basis_dim,
        "basis_channel_norm_max_by_index": {
            str(index): max(norms) for index, norms in degree_channel_norms.items()
        },
        "basis_channel_active_axis_count_by_index": {
            str(index): sum(1 for norm in norms if norm > 0.0)
            for index, norms in degree_channel_norms.items()
        },
        "core_basis_rows": rows,
    }


def _condition_summary(fit_quality: Mapping[str, Any]) -> Mapping[str, Any]:
    records = tuple(fit_quality.get("per_core_update_statuses", ()))
    numeric_conditions = [
        float(record["condition_number"])
        for record in records
        if isinstance(record.get("condition_number"), (int, float))
    ]
    n_cols = [
        int(record["n_cols"])
        for record in records
        if isinstance(record.get("n_cols"), (int, float))
    ]
    n_rows = [
        int(record["n_rows"])
        for record in records
        if isinstance(record.get("n_rows"), (int, float))
    ]
    return {
        "record_count": len(records),
        "finite_condition_count": len(numeric_conditions),
        "condition_number_min": min(numeric_conditions) if numeric_conditions else None,
        "condition_number_max": max(numeric_conditions) if numeric_conditions else None,
        "condition_warning_core_indices": tuple(
            record.get("core_index")
            for record in records
            if bool(record.get("condition_warning", False))
        ),
        "condition_veto_core_indices": tuple(
            record.get("core_index")
            for record in records
            if str(record.get("status")) == source_route.HighDimStatus.CONDITION_NUMBER_VETO.value
        ),
        "n_cols_min": min(n_cols) if n_cols else None,
        "n_cols_max": max(n_cols) if n_cols else None,
        "n_rows_min": min(n_rows) if n_rows else None,
        "n_rows_max": max(n_rows) if n_rows else None,
        "row_to_max_column_ratio": (
            None if not n_rows or not n_cols else min(n_rows) / max(n_cols)
        ),
    }


def _row_payload(label: str, degree: int, rank: int, fit_sample_count: int) -> Mapping[str, Any]:
    _event("row_start", "RUNNING", label=label, degree=degree, rank=rank, fit_sample_count=fit_sample_count)
    result = source_route.p59_author_sir_step_spec_assembly(
        sample_count=1,
        fit_sample_count=int(fit_sample_count),
        fit_degree=int(degree),
        fit_rank=int(rank),
    )
    if result.sequential_result is None:
        _event("row_done", "BLOCKED", label=label, blockers=result.blockers)
        return {
            "label": label,
            "status": result.status,
            "blockers": result.blockers,
        }
    normalizer_terms = source_route._p64_normalizer_terms_by_step(result.sequential_result)
    core_diagnostics = source_route._p65_sqrt_tt_core_diagnostics_by_step(result.sequential_result)
    fit_quality = tuple(result.manifest.get("fit_quality_diagnostics_by_step", ()))
    holdout_replay = tuple(result.manifest.get("holdout_replay_diagnostics_by_step", ()))
    fit_manifests = tuple(result.manifest.get("fit_data_manifests", ()))
    step_rows = []
    for step_index, step in enumerate(result.sequential_result.steps):
        sqrt_tt = _step_sqrt_tt(step)
        fit_manifest = fit_manifests[step_index] if step_index < len(fit_manifests) else {}
        quality = fit_quality[step_index] if step_index < len(fit_quality) else {}
        step_rows.append(
            {
                "time_index": int(step.time_index),
                "sqrt_tt_branch_hash": sqrt_tt.branch_identity.hash.value,
                "rank_channel_summary": _rank_channel_summary(sqrt_tt, rank),
                "degree_activity_summary": _degree_activity_summary(sqrt_tt),
                "fit_target_stats": _tensor_stats(
                    sqrt_tt.branch_identity.manifest.payload["samples"]["target_values"]
                ),
                "fit_weight_stats": _tensor_stats(
                    sqrt_tt.branch_identity.manifest.payload["samples"]["weights"]
                ),
                "fit_manifest_target_value_summary": fit_manifest.get("target_value_summary"),
                "fit_manifest_shift_constant": fit_manifest.get("shift_constant"),
                "fit_manifest_coordinate_frame_hash": fit_manifest.get("coordinate_frame_hash"),
                "fit_quality": quality,
                "condition_summary": _condition_summary(quality),
                "holdout_replay_diagnostics": (
                    holdout_replay[step_index] if step_index < len(holdout_replay) else {}
                ),
                "normalizer_terms": normalizer_terms[step_index],
                "core_diagnostics": core_diagnostics[step_index],
            }
        )
    _event("row_done", "OK", label=label)
    return {
        "label": label,
        "status": result.status,
        "blockers": result.blockers,
        "degree": int(degree),
        "rank": int(rank),
        "fit_sample_count": int(fit_sample_count),
        "rank_tuple": result.manifest.get("rank_tuple"),
        "fit_branch_hashes": result.manifest.get("fit_branch_hashes"),
        "density_branch_hashes": result.manifest.get("density_branch_hashes"),
        "fit_initialization_rule": result.manifest.get("fit_initialization_rule"),
        "fixed_branch_adaptation_class": result.manifest.get("fixed_branch_adaptation_class"),
        "sample_adequacy": source_route.p66_fixed_branch_sample_adequacy(
            fit_degree=int(degree),
            fit_rank=int(rank),
            fit_sample_count=int(fit_sample_count),
        ),
        "normalizer_terms_by_step": normalizer_terms,
        "core_diagnostics_by_step": core_diagnostics,
        "holdout_replay_diagnostics_by_step": holdout_replay,
        "step_diagnostics": step_rows,
    }


def _pair_summary(rows: Mapping[str, Mapping[str, Any]]) -> Mapping[str, Any]:
    rank_low = rows["rank_candidate_1_2_fit36"]
    rank_high = rows["rank_stronger_1_3_fit36"]
    degree_low = rows["degree_candidate_1_2_fit24"]
    degree_high = rows["degree_stronger_2_2_fit24"]
    rank_extra_all_zero = tuple(
        step["rank_channel_summary"]["extra_channel_norms_all_zero"]
        for step in rank_high["step_diagnostics"]
    )
    rank_high_active_counts = tuple(
        step["rank_channel_summary"]["active_channel_count"]
        for step in rank_high["step_diagnostics"]
    )
    degree_fit_residual_delta = tuple(
        float(high_step["fit_quality"]["fit_residual"])
        - float(low_step["fit_quality"]["fit_residual"])
        for low_step, high_step in zip(
            degree_low["step_diagnostics"],
            degree_high["step_diagnostics"],
        )
    )
    degree_log_transport_delta = tuple(
        float(high_terms["log_transport_normalizer"])
        - float(low_terms["log_transport_normalizer"])
        for low_terms, high_terms in zip(
            degree_low["normalizer_terms_by_step"],
            degree_high["normalizer_terms_by_step"],
        )
    )
    degree_log_mixture_delta = tuple(
        math.log(float(high_terms["mixture_normalizer"]))
        - math.log(float(low_terms["mixture_normalizer"]))
        for low_terms, high_terms in zip(
            degree_low["normalizer_terms_by_step"],
            degree_high["normalizer_terms_by_step"],
        )
    )
    degree_mixture_ratio = tuple(
        float(high_terms["mixture_normalizer"])
        / float(low_terms["mixture_normalizer"])
        for low_terms, high_terms in zip(
            degree_low["normalizer_terms_by_step"],
            degree_high["normalizer_terms_by_step"],
        )
    )
    degree_condition_max_delta = tuple(
        float(high_step["condition_summary"]["condition_number_max"])
        - float(low_step["condition_summary"]["condition_number_max"])
        for low_step, high_step in zip(
            degree_low["step_diagnostics"],
            degree_high["step_diagnostics"],
        )
    )
    return {
        "rank_pair": {
            "branch_hashes_differ": rank_low["fit_branch_hashes"] != rank_high["fit_branch_hashes"],
            "rank_high_extra_channel_norms_all_zero_by_step": rank_extra_all_zero,
            "rank_high_active_channel_count_by_step": rank_high_active_counts,
            "rank_high_classification": (
                "extra_channel_inactive_in_realized_fit"
                if all(value is True for value in rank_extra_all_zero)
                else "extra_channel_activity_or_gauge_hidden_unresolved"
            ),
        },
        "degree_pair": {
            "branch_hashes_differ": degree_low["fit_branch_hashes"] != degree_high["fit_branch_hashes"],
            "fit_residual_delta_high_minus_low": degree_fit_residual_delta,
            "log_transport_normalizer_delta_high_minus_low": degree_log_transport_delta,
            "log_mixture_normalizer_delta_high_minus_low": degree_log_mixture_delta,
            "mixture_normalizer_ratio_high_over_low": degree_mixture_ratio,
            "condition_number_max_delta_high_minus_low": degree_condition_max_delta,
            "degree_high_preferred_sample_gap": (
                int(degree_high["sample_adequacy"]["preferred_fit_samples"])
                - int(degree_high["fit_sample_count"])
            ),
            "degree_high_sample_status": degree_high["sample_adequacy"]["status"],
            "degree_high_classification": "normalizer_design_sensitivity_supported",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "docs/plans/"
            "bayesfilter-highdim-zhao-cui-p69-phase5c-rank-activity-degree-normalizer-diagnostics-2026-06-15.json"
        ),
    )
    args = parser.parse_args()

    _event(
        "run_start",
        "RUNNING",
        output=str(args.output),
        cpu_only=os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
    )
    rows: dict[str, Mapping[str, Any]] = {}
    _write_payload(
        args.output,
        _base_payload(
            rows=rows,
            output=args.output,
            status="P69_PHASE5C_DIAGNOSTIC_RUNNING",
        ),
    )
    for label, degree, rank, fit_sample_count in ROW_SPECS:
        rows[label] = _row_payload(label, degree, rank, fit_sample_count)
        _write_payload(
            args.output,
            _base_payload(
                rows=rows,
                output=args.output,
                status="P69_PHASE5C_DIAGNOSTIC_RUNNING",
            ),
        )
    payload = {
        **_base_payload(
            rows=rows,
            output=args.output,
            status="P69_PHASE5C_DIAGNOSTIC_COMPLETED",
        ),
        "pair_summary": _pair_summary(rows),
    }
    _write_payload(args.output, payload)
    _event("run_done", "OK", output=str(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
