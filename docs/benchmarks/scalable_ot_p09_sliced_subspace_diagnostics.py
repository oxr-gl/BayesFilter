"""Phase 9 sliced/subspace semantic-replacement diagnostics.

This script runs a deterministic TensorFlow projection diagnostic on the Phase
1 fixtures.  It computes one-dimensional monotone weighted-quantile maps along
fixed projection directions and reconstructs full-state particles by averaging
projection displacements.

The output is a semantic-replacement diagnostic.  It is not dense entropic OT,
not a sparse solver, and not Mini-batch/BoMb execution.
"""

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
from experiments.dpf_implementation.tf_tfp.resampling.annealed_transport_tf import (
    annealed_transport_resample_tf,
)


DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE

PROJECTED_RECONSTRUCTION_TOLERANCE = 1.0e-8
NONCLAIMS = (
    "Phase 9 sliced/subspace semantic-replacement diagnostic only",
    "not dense entropic OT equivalence",
    "not a sparse solver implementation",
    "Mini-batch/BoMb remains blocked and unexecuted",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC-readiness claim",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--scaling", type=float, default=0.9)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument("--max-iterations", type=int, default=12)
    parser.add_argument("--num-projections", type=int, default=4)
    parser.add_argument("--projection-tolerance", type=float, default=PROJECTED_RECONSTRUCTION_TOLERANCE)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if not 0.0 < args.scaling <= 1.0:
        raise ValueError("scaling must be in (0, 1]")
    if args.convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    if args.max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if args.num_projections <= 0:
        raise ValueError("num_projections must be positive")
    if args.projection_tolerance <= 0.0:
        raise ValueError("projection_tolerance must be positive")
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
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def _tensor_finite(value: tf.Tensor) -> bool:
    return bool(tf.reduce_all(tf.math.is_finite(value)).numpy())


def _deterministic_directions(state_dim: int, num_projections: int) -> tf.Tensor:
    indices = tf.cast(tf.range(state_dim), DTYPE)[:, None]
    columns = []
    for projection in range(num_projections):
        frequency = tf.cast(projection + 1, DTYPE)
        col = tf.sin(0.37 * frequency * (indices[:, 0] + 1.0))
        col = col + tf.cos(0.19 * (frequency + 1.0) * (indices[:, 0] + 1.0))
        if projection < state_dim:
            col = col + tf.one_hot(projection, state_dim, dtype=DTYPE)
        columns.append(col)
    matrix = tf.stack(columns, axis=1)
    q, _ = tf.linalg.qr(matrix)
    directions = tf.transpose(q[:, :num_projections])
    return tf.math.l2_normalize(directions, axis=1)


def _weighted_quantile_source_values(
    sorted_values: tf.Tensor,
    sorted_weights: tf.Tensor,
    quantiles: tf.Tensor,
) -> tf.Tensor:
    cumulative = tf.cumsum(sorted_weights)
    indices = tf.searchsorted(cumulative, quantiles, side="left")
    indices = tf.minimum(indices, tf.shape(sorted_values)[0] - 1)
    return tf.gather(sorted_values, indices)


def _projected_transform_one_batch(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    directions: tf.Tensor,
) -> tuple[tf.Tensor, dict[str, tf.Tensor]]:
    num_particles = tf.shape(particles)[0]
    n_float = tf.cast(num_particles, DTYPE)
    weights = tf.exp(log_weights)
    target_quantiles = (tf.cast(tf.range(num_particles), DTYPE) + 0.5) / n_float
    displacement = tf.zeros_like(particles)
    projected_errors = []
    monotone_violations = []
    for direction_index in range(int(directions.shape[0])):
        direction = directions[direction_index]
        projected = tf.linalg.matvec(particles, direction)
        target_order = tf.argsort(projected, stable=True)
        source_order = tf.argsort(projected, stable=True)
        sorted_projected = tf.gather(projected, source_order)
        sorted_weights = tf.gather(weights, source_order)
        source_values = _weighted_quantile_source_values(
            sorted_projected,
            sorted_weights,
            target_quantiles,
        )
        target_projected = tf.gather(projected, target_order)
        delta_sorted = source_values - target_projected
        delta = tf.scatter_nd(target_order[:, None], delta_sorted, [num_particles])
        displacement = displacement + delta[:, None] * direction[None, :]
        reconstructed_projection = projected + delta
        sorted_reconstructed = tf.gather(reconstructed_projection, target_order)
        projected_errors.append(tf.reduce_max(tf.abs(sorted_reconstructed - source_values)))
        monotone_violations.append(
            tf.reduce_sum(
                tf.cast(sorted_reconstructed[1:] + 1.0e-12 < sorted_reconstructed[:-1], DTYPE)
            )
        )
    reconstructed_particles = particles + displacement / tf.cast(tf.shape(directions)[0], DTYPE)
    return reconstructed_particles, {
        "max_projected_reconstruction_error": tf.reduce_max(tf.stack(projected_errors)),
        "monotone_violation_count": tf.reduce_sum(tf.stack(monotone_violations)),
    }


def _sliced_subspace_resample_tf(
    particles: tf.Tensor,
    log_weights: tf.Tensor,
    *,
    num_projections: int,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, Any]]:
    x = tf.cast(particles, DTYPE)
    logw = tf.cast(log_weights, DTYPE)
    original_particle_rank = len(x.shape)
    original_weight_rank = len(logw.shape)
    if original_particle_rank == 2:
        x = x[None, :, :]
    if original_weight_rank == 1:
        logw = logw[None, :]
    if len(x.shape) != 3 or len(logw.shape) != 2:
        raise ValueError("particles must be [N,D] or [B,N,D]; log_weights must be [N] or [B,N]")
    state_dim = int(x.shape[2])
    if num_projections > state_dim:
        num_projections = state_dim
    directions = _deterministic_directions(state_dim, num_projections)
    outputs = []
    projected_errors = []
    monotone_violations = []
    for batch_index in range(int(x.shape[0])):
        particles_b, diagnostics_b = _projected_transform_one_batch(
            x[batch_index],
            logw[batch_index],
            directions,
        )
        outputs.append(particles_b)
        projected_errors.append(diagnostics_b["max_projected_reconstruction_error"])
        monotone_violations.append(diagnostics_b["monotone_violation_count"])
    out_particles = tf.stack(outputs, axis=0)
    uniform_log = tf.fill(
        tf.shape(logw),
        -tf.math.log(tf.cast(tf.shape(logw)[1], DTYPE)),
    )
    diagnostics = {
        "component_id": "sliced_subspace_projection_diagnostic_tf",
        "semantic_class": "semantic_replacement",
        "source_route": "extension_or_invention",
        "transport_object_kind": "projected_output",
        "num_projections": int(num_projections),
        "direction_shape": directions.shape.as_list(),
        "max_projected_reconstruction_error": _float(tf.reduce_max(tf.stack(projected_errors))),
        "monotone_violation_count": _float(tf.reduce_sum(tf.stack(monotone_violations))),
        "finite_particles": _tensor_finite(out_particles),
        "finite_directions": _tensor_finite(directions),
        "mini_batch_bomb_status": "blocked_unexecuted_source_partial_user_needed",
        "backend": "tensorflow",
    }
    if not diagnostics["finite_particles"] or not diagnostics["finite_directions"]:
        raise FloatingPointError("sliced/subspace diagnostic emitted non-finite values")
    result_particles = out_particles[0] if original_particle_rank == 2 else out_particles
    result_log_weights = uniform_log[0] if original_weight_rank == 1 else uniform_log
    return result_particles, result_log_weights, diagnostics


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
            scaling=args.scaling,
            convergence_threshold=args.convergence_threshold,
            max_iterations=args.max_iterations,
            transport_gradient_mode="raw",
            transport_plan_mode="dense",
        )
    wall_time = time.perf_counter() - start
    transport = tf.convert_to_tensor(result.transport_matrix, dtype=DTYPE)
    source_weights = tf.exp(log_weights)
    num_particles = tf.cast(tf.shape(log_weights)[1], DTYPE)
    row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport, axis=2) - 1.0))
    column_residual = tf.reduce_max(tf.abs(tf.reduce_sum(transport, axis=1) - source_weights * num_particles))
    return {
        "wall_time_seconds": wall_time,
        "particles_shape": result.particles.shape.as_list(),
        "transport_matrix_shape": transport.shape.as_list(),
        "finite_particles": _tensor_finite(tf.convert_to_tensor(result.particles)),
        "finite_transport_matrix": _tensor_finite(transport),
        "max_row_residual": _float(row_residual),
        "max_column_residual": _float(column_residual),
        "diagnostics": dict(result.diagnostics),
    }, tf.convert_to_tensor(result.particles, dtype=DTYPE)


def _run_sliced(
    particles_np: np.ndarray,
    log_weights_np: np.ndarray,
    args: argparse.Namespace,
    *,
    dense_particles: tf.Tensor,
) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    start = time.perf_counter()
    with tf.device(args.device):
        candidate_particles, candidate_log_weights, diagnostics = _sliced_subspace_resample_tf(
            particles,
            log_weights,
            num_projections=args.num_projections,
        )
    wall_time = time.perf_counter() - start
    diff = candidate_particles - dense_particles
    max_error = tf.reduce_max(tf.abs(diff))
    rms_error = tf.sqrt(tf.reduce_mean(tf.square(diff)))
    log_weight_residual = tf.reduce_max(tf.abs(tf.reduce_logsumexp(candidate_log_weights, axis=1)))
    validity_pass = bool(
        diagnostics["finite_particles"]
        and diagnostics["finite_directions"]
        and diagnostics["max_projected_reconstruction_error"] <= args.projection_tolerance
        and diagnostics["monotone_violation_count"] == 0.0
        and _tensor_finite(diff)
        and _float(log_weight_residual) <= 1.0e-12
    )
    return {
        "wall_time_seconds": wall_time,
        "particles_shape": candidate_particles.shape.as_list(),
        "log_weights_shape": candidate_log_weights.shape.as_list(),
        "transport_object": {
            "kind": "projected_output",
            "materialized": True,
            "shape": candidate_particles.shape.as_list(),
            "orientation": "projected_monotone_maps_lifted_to_full_state_particles",
            "semantic_output": "semantic_replacement_full_state_particles_from_projection_displacements",
        },
        "finite_particles": diagnostics["finite_particles"],
        "finite_directions": diagnostics["finite_directions"],
        "max_projected_reconstruction_error": diagnostics["max_projected_reconstruction_error"],
        "monotone_violation_count": diagnostics["monotone_violation_count"],
        "projection_tolerance": args.projection_tolerance,
        "dense_reference_max_abs_particle_error_explanatory": _float(max_error),
        "dense_reference_rms_particle_error_explanatory": _float(rms_error),
        "log_weight_normalization_residual": _float(log_weight_residual),
        "validity_pass": validity_pass,
        "diagnostics": diagnostics,
    }


def _candidate_schema_record(result: dict[str, Any]) -> dict[str, Any]:
    max_particles = max(
        fixture["input_shape"]["particles"][1]
        for fixture in result["fixtures"].values()
    )
    max_dim = max(
        fixture["input_shape"]["particles"][2]
        for fixture in result["fixtures"].values()
    )
    record = CandidateResultRecord(
        candidate_id="phase9_sliced_subspace_projection_semantic_replacement",
        source_status="source_locked",
        semantic_class="semantic_replacement",
        source_route="extension_or_invention",
        baseline_comparator="phase1_dense_streaming_baseline_2026_06_17",
        transport_object=TransportObjectRecord(
            kind="projected_output",
            materialized=True,
            shape=[None, max_particles, max_dim],
            orientation="fixed_projection_monotone_maps_lifted_to_full_state_particles",
            semantic_output="semantic_replacement_full_state_particles_from_projection_displacements",
        ),
        diagnostics={
            "phase9_status": result["phase9_status"],
            "validity_pass": result["validity_pass"],
            "hard_vetoes": result["hard_vetoes"],
            "implementation_scope": result["implementation_scope"],
            "max_projected_reconstruction_error": result["summary"]["max_projected_reconstruction_error"],
            "max_dense_reference_particle_error_explanatory": result["summary"]["max_dense_reference_particle_error_explanatory"],
            "mini_batch_bomb_status": result["mini_batch_bomb_status"],
        },
        diagnostic_roles={
            "validity_pass": "hard_veto",
            "hard_vetoes": "continuation_veto",
            "max_projected_reconstruction_error": "hard_veto",
            "implementation_scope": "explanatory",
            "max_dense_reference_particle_error_explanatory": "explanatory",
            "mini_batch_bomb_status": "hard_veto",
        },
        execution_manifest=result["manifest"],
        nonclaims=list(NONCLAIMS),
    ).to_dict()
    validate_candidate_result(record)
    return record


def _build_result(args: argparse.Namespace) -> dict[str, Any]:
    fixture_results: dict[str, Any] = {}
    hard_vetoes: list[str] = []
    rows: list[dict[str, Any]] = []
    for fixture_name, (particles_np, log_weights_np) in _fixtures().items():
        dense_record, dense_particles = _run_dense(particles_np, log_weights_np, args)
        sliced_row = _run_sliced(
            particles_np,
            log_weights_np,
            args,
            dense_particles=dense_particles,
        )
        rows.append(sliced_row)
        fixture_results[fixture_name] = {
            "input_shape": {
                "particles": list(particles_np.shape),
                "log_weights": list(log_weights_np.shape),
            },
            "dense": dense_record,
            "sliced_subspace": sliced_row,
        }
        if not dense_record["finite_particles"] or not dense_record["finite_transport_matrix"]:
            hard_vetoes.append(f"{fixture_name}:dense_baseline_nonfinite")
        if not sliced_row["validity_pass"]:
            hard_vetoes.append(f"{fixture_name}:sliced_subspace_validity_failed")
    validity_pass = not hard_vetoes
    phase9_status = (
        "PHASE_9_SLICED_SUBSPACE_EXPLORATORY_DIAGNOSTIC_PASSED_SEMANTIC_REPLACEMENT"
        if validity_pass
        else "PHASE_9_SLICED_SUBSPACE_EXPLORATORY_DIAGNOSTIC_FAILED_HARD_VETO"
    )
    summary = {
        "max_projected_reconstruction_error": max(
            row["max_projected_reconstruction_error"] for row in rows
        ),
        "max_dense_reference_particle_error_explanatory": max(
            row["dense_reference_max_abs_particle_error_explanatory"] for row in rows
        ),
        "max_dense_reference_rms_error_explanatory": max(
            row["dense_reference_rms_particle_error_explanatory"] for row in rows
        ),
        "max_log_weight_normalization_residual": max(
            row["log_weight_normalization_residual"] for row in rows
        ),
    }
    result: dict[str, Any] = {
        "phase9_status": phase9_status,
        "status": "PASS" if validity_pass else "FAIL",
        "validity_pass": validity_pass,
        "semantic_class": "semantic_replacement",
        "source_status": "source_locked",
        "source_route": "extension_or_invention",
        "implementation_scope": "fixed_projection_monotone_displacement_diagnostic",
        "mini_batch_bomb_status": "blocked_unexecuted_source_partial_user_needed",
        "hard_vetoes": hard_vetoes,
        "summary": summary,
        "settings": {
            "epsilon": args.epsilon,
            "scaling": args.scaling,
            "convergence_threshold": args.convergence_threshold,
            "max_iterations": args.max_iterations,
            "num_projections": args.num_projections,
            "projection_tolerance": args.projection_tolerance,
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
            "command": "scalable_ot_p09_sliced_subspace_diagnostics.py",
            "plan_path": (
                "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
                "p09-sliced-subspace-minibatch-subplan-2026-06-17.md"
            ),
        },
        "fixtures": fixture_results,
        "diagnostic_roles": {
            "finite_projected_outputs": "hard_veto",
            "projected_reconstruction_consistency": "hard_veto",
            "monotone_violation_count": "hard_veto",
            "mini_batch_bomb_status": "hard_veto",
            "dense_reference_particle_error": "explanatory",
            "wall_time_seconds": "explanatory",
        },
        "nonclaims": list(NONCLAIMS),
    }
    result["candidate_record"] = _candidate_schema_record(result)
    return result


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 9 Sliced/Subspace Diagnostic",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase 9 status: `{result['phase9_status']}`",
        f"- Semantic class: `{result['semantic_class']}`",
        f"- Implementation scope: `{result['implementation_scope']}`",
        f"- Mini-batch/BoMb status: `{result['mini_batch_bomb_status']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| max projected reconstruction error | `{result['summary']['max_projected_reconstruction_error']:.6e}` |",
        f"| max dense-reference particle error, explanatory | `{result['summary']['max_dense_reference_particle_error_explanatory']:.6e}` |",
        f"| max dense-reference RMS error, explanatory | `{result['summary']['max_dense_reference_rms_error_explanatory']:.6e}` |",
        f"| max log-weight normalization residual | `{result['summary']['max_log_weight_normalization_residual']:.6e}` |",
        "",
        "## Fixture Rows",
        "",
        "| Fixture | Valid | Projections | Projected reconstruction error | Dense max error, explanatory | Dense RMS error, explanatory |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for fixture_name, fixture in result["fixtures"].items():
        row = fixture["sliced_subspace"]
        lines.append(
            "| {fixture} | `{valid}` | {proj} | `{proj_err:.6e}` | `{max_err:.6e}` | `{rms_err:.6e}` |".format(
                fixture=fixture_name,
                valid=row["validity_pass"],
                proj=row["diagnostics"]["num_projections"],
                proj_err=row["max_projected_reconstruction_error"],
                max_err=row["dense_reference_max_abs_particle_error_explanatory"],
                rms_err=row["dense_reference_rms_particle_error_explanatory"],
            )
        )
    lines.extend(
        [
            "",
            "## Semantics",
            "",
            "- Fixed deterministic projection directions are used.",
            "- One-dimensional monotone weighted-quantile maps are lifted by averaged projection displacements.",
            "- Dense-reference discrepancy is explanatory only.",
            "- Mini-batch/BoMb remains blocked and unexecuted.",
            "",
            "## Non-Claims",
            "",
        ]
    )
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
