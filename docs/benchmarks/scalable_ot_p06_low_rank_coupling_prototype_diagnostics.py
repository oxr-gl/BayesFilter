"""Phase 6 diagnostics for the low-rank coupling transport prototype."""

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


_PRE_PARSER = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE_PARSER.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
_PRE_PARSER.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _UNKNOWN = _PRE_PARSER.parse_known_args()
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
from docs.benchmarks.scalable_ot_p01_baseline_fixture_diagnostics import _fixtures
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling import low_rank_coupling_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling.annealed_transport_tf import (
    annealed_transport_resample_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_transport_tf import (
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_transport_resample_tf,
)


DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE
low_rank_coupling_transport_tf.DTYPE = DTYPE

VALIDITY_RESIDUAL_THRESHOLD = 5.0e-3
NONCLAIMS = (
    "Phase 6 low-rank coupling transport-object fixture diagnostics only",
    "semantic replacement, not dense Sinkhorn equivalence",
    "not low-rank Sinkhorn solver fidelity",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no general scalability claim",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--baseline-scaling", type=float, default=0.9)
    parser.add_argument("--baseline-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument("--baseline-max-iterations", type=int, default=12)
    parser.add_argument("--assignment-epsilon", type=float, default=0.5)
    parser.add_argument("--max-iterations", type=int, default=200)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-5)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--rank", type=int, default=4)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.epsilon <= 0.0 or args.assignment_epsilon <= 0.0:
        raise ValueError("epsilon values must be positive")
    if args.baseline_max_iterations <= 0 or args.max_iterations <= 0:
        raise ValueError("iteration counts must be positive")
    if args.convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    if args.denominator_floor <= 0.0:
        raise ValueError("denominator_floor must be positive")
    if args.rank <= 0:
        raise ValueError("rank must be positive")
    return args


def _git_commit() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"
    return completed.stdout.strip()


def _float(value: Any) -> float:
    return float(np.asarray(value).reshape(-1)[0])


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    return value


def _tensor_finite(value: tf.Tensor) -> bool:
    return bool(tf.reduce_all(tf.math.is_finite(value)).numpy())


def _run_dense(
    particles_np: np.ndarray,
    log_weights_np: np.ndarray,
    args: argparse.Namespace,
) -> tuple[dict[str, Any], tf.Tensor]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    start = time.perf_counter()
    with tf.device(args.device):
        result = annealed_transport_resample_tf(
            particles,
            log_weights,
            epsilon=args.epsilon,
            scaling=args.baseline_scaling,
            convergence_threshold=args.baseline_convergence_threshold,
            max_iterations=args.baseline_max_iterations,
            transport_gradient_mode="raw",
            transport_plan_mode="dense",
        )
    wall_time = time.perf_counter() - start
    transport = tf.convert_to_tensor(result.transport_matrix, dtype=DTYPE)
    source_weights = tf.exp(log_weights)
    num_particles = tf.cast(tf.shape(log_weights)[1], DTYPE)
    row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport, axis=2) - 1.0))
    column_target = source_weights * num_particles
    column_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport, axis=1) - column_target))
    return {
        "wall_time_seconds": wall_time,
        "particles_shape": result.particles.shape.as_list(),
        "finite_particles": _tensor_finite(tf.convert_to_tensor(result.particles)),
        "finite_transport_matrix": _tensor_finite(transport),
        "max_row_residual": _float(row_residual),
        "max_column_residual": _float(column_residual),
        "diagnostics": dict(result.diagnostics),
    }, tf.convert_to_tensor(result.particles, dtype=DTYPE)


def _run_low_rank(
    particles_np: np.ndarray,
    log_weights_np: np.ndarray,
    args: argparse.Namespace,
    *,
    dense_particles: tf.Tensor,
) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    rank = min(args.rank, int(particles_np.shape[1]))
    start = time.perf_counter()
    with tf.device(args.device):
        result = low_rank_coupling_transport_resample_tf(
            particles,
            log_weights,
            rank=rank,
            assignment_epsilon=args.assignment_epsilon,
            max_iterations=args.max_iterations,
            convergence_threshold=args.convergence_threshold,
            denominator_floor=args.denominator_floor,
        )
    wall_time = time.perf_counter() - start
    candidate_particles = tf.convert_to_tensor(result.particles, dtype=DTYPE)
    diff = candidate_particles - dense_particles
    max_error = tf.reduce_max(tf.abs(diff))
    rms_error = tf.sqrt(tf.reduce_mean(tf.square(diff)))
    diagnostics = dict(result.diagnostics)
    materialized_check = None
    if particles_np.shape[1] <= 16:
        matrix = low_rank_coupling_scaled_matrix_tf(
            result.q_factor,
            result.r_factor,
            result.g_weights,
        )
        source_weights = tf.exp(log_weights)
        num_particles = tf.cast(tf.shape(log_weights)[1], DTYPE)
        materialized_check = {
            "matrix_shape": matrix.shape.as_list(),
            "finite_matrix": _tensor_finite(matrix),
            "max_row_residual": _float(tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=2) - 1.0))),
            "max_column_residual": _float(
                tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=1) - source_weights * num_particles))
            ),
            "transported_parity_max_abs": _float(
                tf.reduce_max(tf.abs(tf.linalg.matmul(matrix, particles) - candidate_particles))
            ),
        }
    max_factor_residual = float(diagnostics["max_factor_marginal_residual"])
    max_row_residual = float(diagnostics["max_induced_row_residual"])
    max_column_residual = float(diagnostics["max_induced_column_residual"])
    validity_pass = bool(
        bool(diagnostics["finite_particles"])
        and bool(diagnostics["finite_factors"])
        and bool(diagnostics["nonnegative_factors"])
        and bool(diagnostics["positive_g"])
        and candidate_particles.shape == dense_particles.shape
        and max_factor_residual <= VALIDITY_RESIDUAL_THRESHOLD
        and max_row_residual <= VALIDITY_RESIDUAL_THRESHOLD
        and max_column_residual <= VALIDITY_RESIDUAL_THRESHOLD
        and np.isfinite(_float(max_error))
        and np.isfinite(_float(rms_error))
    )
    return {
        "rank": rank,
        "wall_time_seconds": wall_time,
        "particles_shape": candidate_particles.shape.as_list(),
        "transport_object": {
            "kind": "low_rank_coupling_factors",
            "materialized": False,
            "factor_shapes": diagnostics["factor_shapes"],
        },
        "finite_particles": bool(diagnostics["finite_particles"]),
        "finite_factors": bool(diagnostics["finite_factors"]),
        "nonnegative_factors": bool(diagnostics["nonnegative_factors"]),
        "positive_g": bool(diagnostics["positive_g"]),
        "max_factor_marginal_residual": max_factor_residual,
        "max_induced_row_residual": max_row_residual,
        "max_induced_column_residual": max_column_residual,
        "dense_reference_max_abs_particle_error_explanatory": _float(max_error),
        "dense_reference_rms_particle_error_explanatory": _float(rms_error),
        "materialized_tiny_check": materialized_check,
        "validity_pass": validity_pass,
        "diagnostics": diagnostics,
    }


def _candidate_schema_record(result: dict[str, Any]) -> dict[str, Any]:
    max_particles = max(
        fixture["input_shape"]["particles"][1]
        for fixture in result["fixtures"].values()
    )
    rank = int(result["settings"]["rank"])
    record = CandidateResultRecord(
        candidate_id="phase6_low_rank_coupling_transport_object_fixture",
        source_status="source_locked",
        semantic_class="semantic_replacement",
        source_route="extension_or_invention",
        baseline_comparator="phase1_dense_streaming_baseline_2026_06_17",
        transport_object=TransportObjectRecord(
            kind="low_rank_coupling_factors",
            materialized=False,
            factor_shapes={
                "Q": [max_particles, rank],
                "R": [max_particles, rank],
                "g": [rank],
            },
            not_materialized_reason="low_rank_coupling_factors_nonmaterialized",
            orientation="target_rows_source_columns_phase1_scaled",
            semantic_output="semantic_replacement_low_rank_coupling_particles",
        ),
        diagnostics={
            "phase6_status": result["phase6_status"],
            "hard_vetoes": result["hard_vetoes"],
            "validity_pass": result["validity_pass"],
            "implementation_scope": result["implementation_scope"],
            "max_factor_marginal_residual": result["summary"]["max_factor_marginal_residual"],
            "max_induced_row_residual": result["summary"]["max_induced_row_residual"],
            "max_induced_column_residual": result["summary"]["max_induced_column_residual"],
            "max_dense_reference_particle_error_explanatory": result["summary"]["max_dense_reference_particle_error_explanatory"],
            "max_dense_reference_rms_error_explanatory": result["summary"]["max_dense_reference_rms_error_explanatory"],
            "thresholds": result["thresholds"],
            "source_route_components": result["source_route_components"],
        },
        diagnostic_roles={
            "validity_pass": "hard_veto",
            "max_factor_marginal_residual": "hard_veto",
            "max_induced_row_residual": "hard_veto",
            "max_induced_column_residual": "hard_veto",
            "hard_vetoes": "continuation_veto",
            "implementation_scope": "explanatory",
            "max_dense_reference_particle_error_explanatory": "explanatory",
            "max_dense_reference_rms_error_explanatory": "explanatory",
            "thresholds": "explanatory",
            "source_route_components": "explanatory",
        },
        execution_manifest=result["manifest"],
        nonclaims=list(NONCLAIMS),
    ).to_dict()
    validate_candidate_result(record)
    return record


def _build_result(args: argparse.Namespace) -> dict[str, Any]:
    fixture_results: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    for fixture_name, (particles_np, log_weights_np) in _fixtures().items():
        dense_record, dense_particles = _run_dense(particles_np, log_weights_np, args)
        low_rank_row = _run_low_rank(
            particles_np,
            log_weights_np,
            args,
            dense_particles=dense_particles,
        )
        rows.append(low_rank_row)
        fixture_results[fixture_name] = {
            "input_shape": {
                "particles": list(particles_np.shape),
                "log_weights": list(log_weights_np.shape),
            },
            "dense": dense_record,
            "low_rank_coupling": low_rank_row,
        }
    hard_vetoes = []
    for fixture_name, fixture in fixture_results.items():
        if not fixture["dense"]["finite_particles"] or not fixture["dense"]["finite_transport_matrix"]:
            hard_vetoes.append(f"{fixture_name}:dense_baseline_nonfinite")
        if not fixture["low_rank_coupling"]["validity_pass"]:
            hard_vetoes.append(f"{fixture_name}:low_rank_coupling_validity_failed")
    validity_pass = not hard_vetoes
    phase6_status = (
        "PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_PASSED"
        if validity_pass
        else "PHASE_6_LOW_RANK_COUPLING_TRANSPORT_OBJECT_FIXTURE_FAILED_HARD_VETO"
    )
    summary = {
        "max_factor_marginal_residual": max(row["max_factor_marginal_residual"] for row in rows),
        "max_induced_row_residual": max(row["max_induced_row_residual"] for row in rows),
        "max_induced_column_residual": max(row["max_induced_column_residual"] for row in rows),
        "max_dense_reference_particle_error_explanatory": max(
            row["dense_reference_max_abs_particle_error_explanatory"] for row in rows
        ),
        "max_dense_reference_rms_error_explanatory": max(
            row["dense_reference_rms_particle_error_explanatory"] for row in rows
        ),
    }
    manifest = {
        "git_commit": _git_commit(),
        "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "tensorflow_version": tf.__version__,
        "device_scope": args.device_scope,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "device": args.device,
        "dtype": "tf.float64",
        "command": "scalable_ot_p06_low_rank_coupling_prototype_diagnostics.py",
        "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p06-low-rank-coupling-prototype-subplan-2026-06-17.md",
    }
    result: dict[str, Any] = {
        "phase6_status": phase6_status,
        "status": "PASS" if validity_pass else "FAIL",
        "validity_pass": validity_pass,
        "semantic_class": "semantic_replacement",
        "implementation_scope": "transport_object_fixture_route",
        "hard_vetoes": hard_vetoes,
        "summary": summary,
        "thresholds": {
            "factor_and_induced_residual_hard_veto": VALIDITY_RESIDUAL_THRESHOLD,
            "dense_reference_error_role": "explanatory_only_for_semantic_replacement",
        },
        "source_route_components": {
            "factored_coupling_parameterization": "source_faithful",
            "low_rank_lazy_apply": "source_faithful",
            "factor_marginal_diagnostics": "source_faithful",
            "phase1_scaled_transport_adapter": "fixed_hmc_adaptation",
            "deterministic_latent_assignment_factors": "extension_or_invention",
        },
        "settings": {
            "epsilon": args.epsilon,
            "baseline_scaling": args.baseline_scaling,
            "baseline_convergence_threshold": args.baseline_convergence_threshold,
            "baseline_max_iterations": args.baseline_max_iterations,
            "assignment_epsilon": args.assignment_epsilon,
            "max_iterations": args.max_iterations,
            "convergence_threshold": args.convergence_threshold,
            "denominator_floor": args.denominator_floor,
            "rank": args.rank,
        },
        "manifest": manifest,
        "fixtures": fixture_results,
        "nonclaims": list(NONCLAIMS),
    }
    result["candidate_record"] = _candidate_schema_record(result)
    return result


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 6 Low-Rank Coupling Prototype Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase 6 status: `{result['phase6_status']}`",
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
        f"| max dense-reference particle error, explanatory | `{result['summary']['max_dense_reference_particle_error_explanatory']:.6e}` |",
        f"| max dense-reference RMS error, explanatory | `{result['summary']['max_dense_reference_rms_error_explanatory']:.6e}` |",
        "",
        "## Fixture Rows",
        "",
        "| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for fixture_name, fixture in result["fixtures"].items():
        row = fixture["low_rank_coupling"]
        lines.append(
            "| {fixture} | {rank} | `{valid}` | `{factor:.6e}` | `{row_res:.6e}` | `{col_res:.6e}` | `{max_err:.6e}` | `{rms_err:.6e}` |".format(
                fixture=fixture_name,
                rank=row["rank"],
                valid=row["validity_pass"],
                factor=row["max_factor_marginal_residual"],
                row_res=row["max_induced_row_residual"],
                col_res=row["max_induced_column_residual"],
                max_err=row["dense_reference_max_abs_particle_error_explanatory"],
                rms_err=row["dense_reference_rms_particle_error_explanatory"],
            )
        )
    lines.extend(["", "## Non-Claims", ""])
    for nonclaim in result["nonclaims"]:
        lines.append(f"- {nonclaim}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = _build_result(args)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown = Path(args.markdown_output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    _write_markdown(result, markdown)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
