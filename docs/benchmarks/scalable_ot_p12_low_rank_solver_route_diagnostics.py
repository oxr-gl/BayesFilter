"""P12 diagnostics for the Agent C low-rank coupling solver route."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


_PRE = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
_PRE.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _ = _PRE.parse_known_args()
if _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
elif _PRE_ARGS.device_scope == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import tensorflow as tf

from docs.benchmarks.scalable_ot_candidate_result_schema import (
    CandidateResultRecord,
    TransportObjectRecord,
    validate_candidate_result,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling import low_rank_coupling_solver_tf
from experiments.dpf_implementation.tf_tfp.resampling.annealed_transport_tf import (
    annealed_transport_resample_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_solver_resample_tf,
)


DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE
low_rank_coupling_solver_tf.DTYPE = DTYPE

VALIDITY_THRESHOLD = 5.0e-3
MATERIALIZED_PARITY_THRESHOLD = 1.0e-10
BASELINE_COMPARATOR = "phase1_dense_streaming_baseline_2026_06_17_descriptive_semantic_delta"
NONCLAIMS = (
    "Agent C P12 low-rank coupling solver-route diagnostics only",
    "semantic replacement, not dense Sinkhorn equivalence",
    "no full low-rank Sinkhorn solver-fidelity claim for extension components",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--assignment-epsilon", type=float, default=0.45)
    parser.add_argument("--alpha", type=float, default=1.0e-8)
    parser.add_argument("--rank", type=int, default=3)
    parser.add_argument("--max-projection-iterations", type=int, default=240)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-6)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--baseline-epsilon", type=float, default=0.5)
    parser.add_argument("--baseline-scaling", type=float, default=0.9)
    parser.add_argument("--baseline-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument("--baseline-max-iterations", type=int, default=12)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.rank <= 0:
        raise ValueError("rank must be positive")
    if args.assignment_epsilon <= 0.0 or args.alpha <= 0.0:
        raise ValueError("assignment_epsilon and alpha must be positive")
    if args.max_projection_iterations <= 0:
        raise ValueError("max_projection_iterations must be positive")
    if args.convergence_threshold <= 0.0 or args.denominator_floor <= 0.0:
        raise ValueError("threshold and denominator floor must be positive")
    return args


def _fixture_tiny_manual_solver() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [[[-0.40, 0.10, 0.00], [-0.15, -0.20, 0.05], [0.10, 0.18, -0.10], [0.35, -0.02, 0.15], [0.60, 0.12, -0.05]]],
        dtype=np.float64,
    )
    weights = np.array([[0.10, 0.16, 0.22, 0.25, 0.27]], dtype=np.float64)
    return particles, np.log(weights)


def _fixture_small_batch_solver() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [
            [[-0.40, 0.10, 0.00], [-0.15, -0.20, 0.05], [0.10, 0.18, -0.10], [0.35, -0.02, 0.15], [0.60, 0.12, -0.05]],
            [[-0.35, -0.15, 0.12], [-0.08, 0.02, -0.02], [0.16, 0.24, 0.05], [0.42, -0.10, -0.12], [0.68, 0.04, 0.18]],
        ],
        dtype=np.float64,
    )
    weights = np.array(
        [[0.10, 0.16, 0.22, 0.25, 0.27], [0.15, 0.18, 0.20, 0.22, 0.25]],
        dtype=np.float64,
    )
    return particles, np.log(weights)


def _fixtures() -> dict[str, tuple[np.ndarray, np.ndarray]]:
    return {
        "tiny_manual_solver": _fixture_tiny_manual_solver(),
        "small_batch_solver": _fixture_small_batch_solver(),
    }


def _git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _float(value: Any) -> float:
    return float(np.asarray(value).reshape(-1)[0])


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_ready(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(v) for v in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def _run_dense(particles_np: np.ndarray, log_weights_np: np.ndarray, args: argparse.Namespace) -> tf.Tensor:
    with tf.device(args.device):
        result = annealed_transport_resample_tf(
            tf.constant(particles_np, dtype=DTYPE),
            tf.constant(log_weights_np, dtype=DTYPE),
            epsilon=args.baseline_epsilon,
            scaling=args.baseline_scaling,
            convergence_threshold=args.baseline_convergence_threshold,
            max_iterations=args.baseline_max_iterations,
            transport_gradient_mode="raw",
            transport_plan_mode="dense",
        )
    return tf.convert_to_tensor(result.particles, dtype=DTYPE)


def _run_candidate(fixture_name: str, particles_np: np.ndarray, log_weights_np: np.ndarray, args: argparse.Namespace) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    rank = min(args.rank, int(particles_np.shape[1]))
    dense_particles = _run_dense(particles_np, log_weights_np, args)
    start = time.perf_counter()
    with tf.device(args.device):
        result = low_rank_coupling_solver_resample_tf(
            particles,
            log_weights,
            rank=rank,
            assignment_epsilon=args.assignment_epsilon,
            alpha=args.alpha,
            max_projection_iterations=args.max_projection_iterations,
            convergence_threshold=args.convergence_threshold,
            denominator_floor=args.denominator_floor,
        )
    wall_time = time.perf_counter() - start
    candidate_particles = tf.convert_to_tensor(result.particles, dtype=DTYPE)
    diff = candidate_particles - dense_particles
    matrix = low_rank_coupling_scaled_matrix_tf(result.q_factor, result.r_factor, result.g_weights)
    materialized_particles = tf.linalg.matmul(matrix, particles)
    source_weights = tf.exp(log_weights)
    num_particles = tf.cast(tf.shape(log_weights)[1], DTYPE)
    materialized_parity = tf.reduce_max(tf.abs(materialized_particles - candidate_particles))
    row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=2) - 1.0))
    column_residual = tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=1) - source_weights * num_particles))
    diag = dict(result.diagnostics)
    validity_pass = bool(
        diag["finite_factors"]
        and diag["finite_particles"]
        and diag["nonnegative_factors"]
        and diag["positive_g"]
        and diag["max_factor_marginal_residual"] <= VALIDITY_THRESHOLD
        and diag["max_induced_row_residual"] <= VALIDITY_THRESHOLD
        and diag["max_induced_column_residual"] <= VALIDITY_THRESHOLD
        and _float(materialized_parity) <= MATERIALIZED_PARITY_THRESHOLD
    )
    return {
        "fixture": fixture_name,
        "rank": rank,
        "validity_pass": validity_pass,
        "wall_time_seconds": wall_time,
        "input_shape": {"particles": list(particles_np.shape), "log_weights": list(log_weights_np.shape)},
        "factor_shapes": diag["factor_shapes"],
        "max_factor_marginal_residual": diag["max_factor_marginal_residual"],
        "max_induced_row_residual": diag["max_induced_row_residual"],
        "max_induced_column_residual": diag["max_induced_column_residual"],
        "materialized_tiny_apply_parity": _float(materialized_parity),
        "materialized_row_residual": _float(row_residual),
        "materialized_column_residual": _float(column_residual),
        "dense_reference_max_abs_particle_error_explanatory": _float(tf.reduce_max(tf.abs(diff))),
        "dense_reference_rms_particle_error_explanatory": _float(tf.sqrt(tf.reduce_mean(tf.square(diff)))),
        "diagnostics": diag,
    }


def _candidate_record(result: dict[str, Any]) -> dict[str, Any]:
    max_particles = max(row["input_shape"]["particles"][1] for row in result["rows"])
    rank = int(result["settings"]["rank"])
    record = CandidateResultRecord(
        candidate_id="phase12_low_rank_coupling_solver_route",
        source_status="source_locked",
        semantic_class="semantic_replacement",
        source_route="extension_or_invention",
        baseline_comparator=BASELINE_COMPARATOR,
        transport_object=TransportObjectRecord(
            kind="low_rank_coupling_factors",
            materialized=False,
            factor_shapes={"Q": [max_particles, rank], "R": [max_particles, rank], "g": [rank]},
            not_materialized_reason="low_rank_coupling_factors_nonmaterialized",
            orientation="target_rows_source_columns_phase1_scaled",
            semantic_output="full_state_particles",
        ),
        diagnostics={
            "phase12_status": result["phase12_status"],
            "implementation_scope": result["implementation_scope"],
            "hard_vetoes": result["hard_vetoes"],
            "validity_pass": result["validity_pass"],
            "max_factor_marginal_residual": result["summary"]["max_factor_marginal_residual"],
            "max_induced_row_residual": result["summary"]["max_induced_row_residual"],
            "max_induced_column_residual": result["summary"]["max_induced_column_residual"],
            "materialized_tiny_apply_parity": result["summary"]["max_materialized_tiny_apply_parity"],
            "dense_reference_max_abs_particle_error_explanatory": result["summary"]["max_dense_reference_particle_error_explanatory"],
            "dense_reference_rms_particle_error_explanatory": result["summary"]["max_dense_reference_rms_error_explanatory"],
            "thresholds": result["thresholds"],
            "source_route_components": result["source_route_components"],
        },
        diagnostic_roles={
            "validity_pass": "hard_veto",
            "hard_vetoes": "continuation_veto",
            "max_factor_marginal_residual": "hard_veto",
            "max_induced_row_residual": "hard_veto",
            "max_induced_column_residual": "hard_veto",
            "materialized_tiny_apply_parity": "hard_veto",
            "dense_reference_max_abs_particle_error_explanatory": "explanatory",
            "dense_reference_rms_particle_error_explanatory": "explanatory",
            "implementation_scope": "explanatory",
            "thresholds": "explanatory",
            "source_route_components": "explanatory",
        },
        execution_manifest=result["manifest"],
        nonclaims=list(NONCLAIMS),
    ).to_dict()
    validate_candidate_result(record)
    return record


def _build_result(args: argparse.Namespace) -> dict[str, Any]:
    rows = [_run_candidate(name, *fixture, args) for name, fixture in _fixtures().items()]
    hard_vetoes = [f"{row['fixture']}:validity_failed" for row in rows if not row["validity_pass"]]
    validity_pass = not hard_vetoes
    phase12_status = "LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY" if validity_pass else "LOW_RANK_SOLVER_ROUTE_COMPLETED_CANDIDATE_NOT_PROMOTED"
    summary = {
        "max_factor_marginal_residual": max(row["max_factor_marginal_residual"] for row in rows),
        "max_induced_row_residual": max(row["max_induced_row_residual"] for row in rows),
        "max_induced_column_residual": max(row["max_induced_column_residual"] for row in rows),
        "max_materialized_tiny_apply_parity": max(row["materialized_tiny_apply_parity"] for row in rows),
        "max_dense_reference_particle_error_explanatory": max(row["dense_reference_max_abs_particle_error_explanatory"] for row in rows),
        "max_dense_reference_rms_error_explanatory": max(row["dense_reference_rms_particle_error_explanatory"] for row in rows),
    }
    result = {
        "phase12_status": phase12_status,
        "status": "PASS" if validity_pass else "FAIL",
        "validity_pass": validity_pass,
        "semantic_class": "semantic_replacement",
        "implementation_scope": "solver_route_dykstra_projection_diagnostic",
        "hard_vetoes": hard_vetoes,
        "summary": summary,
        "thresholds": {
            "factor_and_induced_residual_hard_veto": VALIDITY_THRESHOLD,
            "materialized_apply_parity_hard_veto": MATERIALIZED_PARITY_THRESHOLD,
            "dense_reference_error_role": "explanatory_only_for_semantic_replacement",
        },
        "source_route_components": {
            "factored_coupling_parameterization": "source_faithful",
            "low_rank_lazy_apply": "source_faithful",
            "factor_marginal_diagnostics": "source_faithful",
            "dykstra_style_projection": "source_faithful",
            "deterministic_initialization": "fixed_hmc_adaptation",
            "fixed_iteration_schedule": "fixed_hmc_adaptation",
            "phase1_scaled_transport_adapter": "fixed_hmc_adaptation",
            "cost_nudged_assignment_kernel": "extension_or_invention",
        },
        "settings": {
            "assignment_epsilon": args.assignment_epsilon,
            "alpha": args.alpha,
            "rank": args.rank,
            "max_projection_iterations": args.max_projection_iterations,
            "convergence_threshold": args.convergence_threshold,
            "denominator_floor": args.denominator_floor,
        },
        "manifest": {
            "git_commit": _git_commit(),
            "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "device_scope": args.device_scope,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device": args.device,
            "dtype": "tf.float64",
            "command": "scalable_ot_p12_low_rank_solver_route_diagnostics.py",
            "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p12-low-rank-solver-route-subplan-2026-06-18.md",
        },
        "rows": rows,
        "nonclaims": list(NONCLAIMS),
    }
    result["candidate_record"] = _candidate_record(result)
    return result


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# P12 Low-Rank Coupling Solver Route Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase 12 status: `{result['phase12_status']}`",
        f"- Semantic class: `{result['semantic_class']}`",
        f"- Implementation scope: `{result['implementation_scope']}`",
        f"- Validity pass: `{result['validity_pass']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| max factor marginal residual | `{result['summary']['max_factor_marginal_residual']:.6e}` |",
        f"| max induced row residual | `{result['summary']['max_induced_row_residual']:.6e}` |",
        f"| max induced column residual | `{result['summary']['max_induced_column_residual']:.6e}` |",
        f"| max materialized tiny apply parity | `{result['summary']['max_materialized_tiny_apply_parity']:.6e}` |",
        f"| max dense-reference particle error, explanatory | `{result['summary']['max_dense_reference_particle_error_explanatory']:.6e}` |",
        f"| max dense-reference RMS error, explanatory | `{result['summary']['max_dense_reference_rms_error_explanatory']:.6e}` |",
        "",
        "## Rows",
        "",
        "| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Apply parity | Max dense error, explanatory |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            "| {fixture} | {rank} | `{valid}` | `{factor:.6e}` | `{row_res:.6e}` | `{col_res:.6e}` | `{parity:.6e}` | `{dense:.6e}` |".format(
                fixture=row["fixture"],
                rank=row["rank"],
                valid=row["validity_pass"],
                factor=row["max_factor_marginal_residual"],
                row_res=row["max_induced_row_residual"],
                col_res=row["max_induced_column_residual"],
                parity=row["materialized_tiny_apply_parity"],
                dense=row["dense_reference_max_abs_particle_error_explanatory"],
            )
        )
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- {item}" for item in result["nonclaims"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = _build_result(args)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _write_markdown(result, markdown)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
