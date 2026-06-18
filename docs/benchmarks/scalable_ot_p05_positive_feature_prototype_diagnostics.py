"""Phase 5 diagnostics for the positive-feature transport prototype."""

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
from experiments.dpf_implementation.tf_tfp.resampling import positive_feature_transport_tf
from experiments.dpf_implementation.tf_tfp.resampling.annealed_transport_tf import (
    annealed_transport_resample_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling.positive_feature_transport_tf import (
    positive_feature_transport_resample_tf,
)


DTYPE = tf.float64
annealed_transport_tf.DTYPE = DTYPE
positive_feature_transport_tf.DTYPE = DTYPE

VALIDITY_ROW_COLUMN_THRESHOLD = 5.0e-2
NONCLAIMS = (
    "Phase 5 positive-feature semantic-replacement diagnostics only",
    "no dense Gibbs equivalence claim",
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
    parser.add_argument("--feature-max-iterations", type=int, default=120)
    parser.add_argument("--feature-convergence-threshold", type=float, default=1.0e-4)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--num-features", type=int, default=128)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    if args.num_features <= 0:
        raise ValueError("num_features must be positive")
    if args.baseline_max_iterations <= 0 or args.feature_max_iterations <= 0:
        raise ValueError("iteration counts must be positive")
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


def _run_positive_feature(
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
        result = positive_feature_transport_resample_tf(
            particles,
            log_weights,
            num_features=args.num_features,
            epsilon=args.epsilon,
            max_iterations=args.feature_max_iterations,
            convergence_threshold=args.feature_convergence_threshold,
            denominator_floor=args.denominator_floor,
        )
    wall_time = time.perf_counter() - start
    candidate_particles = tf.convert_to_tensor(result.particles, dtype=DTYPE)
    diff = candidate_particles - dense_particles
    max_error = tf.reduce_max(tf.abs(diff))
    rms_error = tf.sqrt(tf.reduce_mean(tf.square(diff)))
    diagnostics = dict(result.diagnostics)
    row_residual = float(diagnostics["max_row_residual"])
    column_residual = float(diagnostics["max_column_residual"])
    validity_pass = bool(
        bool(diagnostics["finite_particles"])
        and bool(diagnostics["finite_features"])
        and bool(diagnostics["positive_features"])
        and candidate_particles.shape == dense_particles.shape
        and row_residual <= VALIDITY_ROW_COLUMN_THRESHOLD
        and column_residual <= VALIDITY_ROW_COLUMN_THRESHOLD
        and np.isfinite(_float(max_error))
        and np.isfinite(_float(rms_error))
    )
    return {
        "num_features": args.num_features,
        "wall_time_seconds": wall_time,
        "particles_shape": candidate_particles.shape.as_list(),
        "transport_object": {
            "kind": "kernel_factors",
            "materialized": False,
            "factor_shapes": diagnostics["factor_shapes"],
        },
        "finite_particles": bool(diagnostics["finite_particles"]),
        "finite_features": bool(diagnostics["finite_features"]),
        "positive_features": bool(diagnostics["positive_features"]),
        "max_row_residual": row_residual,
        "max_column_residual": column_residual,
        "dense_reference_max_abs_particle_error_explanatory": _float(max_error),
        "dense_reference_rms_particle_error_explanatory": _float(rms_error),
        "validity_pass": validity_pass,
        "diagnostics": diagnostics,
    }


def _candidate_schema_record(result: dict[str, Any]) -> dict[str, Any]:
    max_particles = max(
        fixture["input_shape"]["particles"][1]
        for fixture in result["fixtures"].values()
    )
    num_features = int(result["settings"]["num_features"])
    record = CandidateResultRecord(
        candidate_id="phase5_positive_feature_semantic_replacement_transport",
        source_status="source_locked",
        semantic_class="semantic_replacement",
        source_route="fixed_hmc_adaptation",
        baseline_comparator="phase1_dense_streaming_baseline_2026_06_17",
        transport_object=TransportObjectRecord(
            kind="kernel_factors",
            materialized=False,
            factor_shapes={
                "left_features": [max_particles, num_features],
                "right_features": [max_particles, num_features],
                "scaling_u": [max_particles],
                "scaling_v": [max_particles],
            },
            not_materialized_reason="positive_feature_factors_nonmaterialized",
            semantic_output="semantic_replacement_feature_kernel_particles",
        ),
        diagnostics={
            "phase5_status": result["phase5_status"],
            "hard_vetoes": result["hard_vetoes"],
            "validity_pass": result["validity_pass"],
            "max_row_residual": result["summary"]["max_row_residual"],
            "max_column_residual": result["summary"]["max_column_residual"],
            "max_dense_reference_particle_error_explanatory": result["summary"]["max_dense_reference_particle_error_explanatory"],
            "max_dense_reference_rms_error_explanatory": result["summary"]["max_dense_reference_rms_error_explanatory"],
            "thresholds": result["thresholds"],
            "source_route_components": result["source_route_components"],
        },
        diagnostic_roles={
            "validity_pass": "hard_veto",
            "max_row_residual": "hard_veto",
            "max_column_residual": "hard_veto",
            "hard_vetoes": "continuation_veto",
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
        feature_row = _run_positive_feature(
            particles_np,
            log_weights_np,
            args,
            dense_particles=dense_particles,
        )
        rows.append(feature_row)
        fixture_results[fixture_name] = {
            "input_shape": {
                "particles": list(particles_np.shape),
                "log_weights": list(log_weights_np.shape),
            },
            "dense": dense_record,
            "positive_feature": feature_row,
        }
    hard_vetoes = []
    for fixture_name, fixture in fixture_results.items():
        if not fixture["dense"]["finite_particles"] or not fixture["dense"]["finite_transport_matrix"]:
            hard_vetoes.append(f"{fixture_name}:dense_baseline_nonfinite")
        if not fixture["positive_feature"]["validity_pass"]:
            hard_vetoes.append(f"{fixture_name}:positive_feature_validity_failed")
    validity_pass = not hard_vetoes
    phase5_status = (
        "PHASE_5_POSITIVE_FEATURE_PROTOTYPE_PASSED_SEMANTIC_REPLACEMENT"
        if validity_pass
        else "PHASE_5_POSITIVE_FEATURE_PROTOTYPE_FAILED_HARD_VETO"
    )
    summary = {
        "max_row_residual": max(row["max_row_residual"] for row in rows),
        "max_column_residual": max(row["max_column_residual"] for row in rows),
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
        "command": "scalable_ot_p05_positive_feature_prototype_diagnostics.py",
        "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-p05-positive-feature-prototype-subplan-2026-06-17.md",
    }
    result: dict[str, Any] = {
        "phase5_status": phase5_status,
        "status": "PASS" if validity_pass else "FAIL",
        "validity_pass": validity_pass,
        "semantic_class": "semantic_replacement",
        "hard_vetoes": hard_vetoes,
        "summary": summary,
        "thresholds": {
            "row_column_residual_hard_veto": VALIDITY_ROW_COLUMN_THRESHOLD,
            "dense_reference_error_role": "explanatory_only_for_semantic_replacement",
        },
        "source_route_components": {
            "positive_feature_factorization": "source_faithful",
            "linear_feature_scaling": "source_faithful",
            "filterflow_cost_scaling_adapter": "fixed_hmc_adaptation",
            "deterministic_feature_basis": "fixed_hmc_adaptation",
        },
        "settings": {
            "epsilon": args.epsilon,
            "baseline_scaling": args.baseline_scaling,
            "baseline_convergence_threshold": args.baseline_convergence_threshold,
            "baseline_max_iterations": args.baseline_max_iterations,
            "feature_max_iterations": args.feature_max_iterations,
            "feature_convergence_threshold": args.feature_convergence_threshold,
            "denominator_floor": args.denominator_floor,
            "num_features": args.num_features,
        },
        "manifest": manifest,
        "fixtures": fixture_results,
        "nonclaims": list(NONCLAIMS),
    }
    result["candidate_record"] = _candidate_schema_record(result)
    return result


def _write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Phase 5 Positive-Feature Prototype Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase 5 status: `{result['phase5_status']}`",
        f"- Semantic class: `{result['semantic_class']}`",
        f"- Validity pass: `{result['validity_pass']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| max row residual | `{result['summary']['max_row_residual']:.6e}` |",
        f"| max column residual | `{result['summary']['max_column_residual']:.6e}` |",
        f"| max dense-reference particle error, explanatory | `{result['summary']['max_dense_reference_particle_error_explanatory']:.6e}` |",
        f"| max dense-reference RMS error, explanatory | `{result['summary']['max_dense_reference_rms_error_explanatory']:.6e}` |",
        "",
        "## Fixture Rows",
        "",
        "| Fixture | Features | Valid | Row residual | Column residual | Max dense error, explanatory | RMS dense error, explanatory |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for fixture_name, fixture in result["fixtures"].items():
        row = fixture["positive_feature"]
        lines.append(
            "| {fixture} | {features} | `{valid}` | `{row_res:.6e}` | `{col_res:.6e}` | `{max_err:.6e}` | `{rms_err:.6e}` |".format(
                fixture=fixture_name,
                features=row["num_features"],
                valid=row["validity_pass"],
                row_res=row["max_row_residual"],
                col_res=row["max_column_residual"],
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
