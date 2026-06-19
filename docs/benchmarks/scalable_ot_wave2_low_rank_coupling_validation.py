"""Wave 2 validation for the low-rank coupling solver-route candidate."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
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
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_solver_resample_tf,
)


DTYPE = tf.float64
VALIDITY_THRESHOLD = 5.0e-3
MATERIALIZED_PARITY_THRESHOLD = 1.0e-10
WAVE2_STATUS_PASS = "LOW_RANK_COUPLING_VALIDATION_PASSED_DIAGNOSTIC_ONLY"
WAVE2_STATUS_FAIL = "LOW_RANK_COUPLING_VALIDATION_COMPLETED_CANDIDATE_NOT_PROMOTED"
BASELINE_COMPARATOR = "phase1_dense_streaming_baseline_context_only_not_promotion"
NONCLAIMS = (
    "Wave 2 peer-agent low-rank coupling validation only",
    "semantic replacement, not dense Sinkhorn equivalence",
    "no full low-rank Sinkhorn solver-fidelity claim for extension components",
    "no speedup claim",
    "no ranking claim",
    "no production default change",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no broad scalable-OT selection claim",
)
EXPECTED_SOURCE_ROUTE_COMPONENTS = {
    "factored_coupling_parameterization": "source_faithful",
    "low_rank_lazy_apply": "source_faithful",
    "factor_marginal_diagnostics": "source_faithful",
    "dykstra_style_projection": "source_faithful",
    "deterministic_initialization": "fixed_hmc_adaptation",
    "fixed_iteration_schedule": "fixed_hmc_adaptation",
    "phase1_scaled_transport_adapter": "fixed_hmc_adaptation",
    "cost_nudged_assignment_kernel": "extension_or_invention",
}


@dataclass(frozen=True)
class ValidationSettings:
    rank: int = 3
    assignment_epsilon: float = 0.45
    alpha: float = 1.0e-8
    max_projection_iterations: int = 240
    convergence_threshold: float = 1.0e-6
    denominator_floor: float = 1.0e-30
    device: str = "/CPU:0"
    device_scope: str = _PRE_ARGS.device_scope


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--rank", type=int, default=ValidationSettings.rank)
    parser.add_argument("--assignment-epsilon", type=float, default=ValidationSettings.assignment_epsilon)
    parser.add_argument("--alpha", type=float, default=ValidationSettings.alpha)
    parser.add_argument("--max-projection-iterations", type=int, default=ValidationSettings.max_projection_iterations)
    parser.add_argument("--convergence-threshold", type=float, default=ValidationSettings.convergence_threshold)
    parser.add_argument("--denominator-floor", type=float, default=ValidationSettings.denominator_floor)
    parser.add_argument("--device", default=ValidationSettings.device)
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    if args.rank <= 0:
        raise ValueError("rank must be positive")
    if args.assignment_epsilon <= 0.0:
        raise ValueError("assignment_epsilon must be positive")
    if args.alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if args.max_projection_iterations <= 0:
        raise ValueError("max_projection_iterations must be positive")
    if args.convergence_threshold <= 0.0:
        raise ValueError("convergence_threshold must be positive")
    if args.denominator_floor <= 0.0:
        raise ValueError("denominator_floor must be positive")
    return args


def _settings_from_args(args: argparse.Namespace) -> ValidationSettings:
    return ValidationSettings(
        rank=args.rank,
        assignment_epsilon=args.assignment_epsilon,
        alpha=args.alpha,
        max_projection_iterations=args.max_projection_iterations,
        convergence_threshold=args.convergence_threshold,
        denominator_floor=args.denominator_floor,
        device=args.device,
        device_scope=args.device_scope,
    )


def _fixture_tiny_manual() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [[[-0.40, 0.10, 0.00], [-0.15, -0.20, 0.05], [0.10, 0.18, -0.10], [0.35, -0.02, 0.15], [0.60, 0.12, -0.05]]],
        dtype=np.float64,
    )
    weights = np.array([[0.10, 0.16, 0.22, 0.25, 0.27]], dtype=np.float64)
    return particles, np.log(weights)


def _fixture_small_batch() -> tuple[np.ndarray, np.ndarray]:
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


def _fixture_wider_state() -> tuple[np.ndarray, np.ndarray]:
    particles = np.array(
        [
            [
                [-0.50, 0.10, 0.20, -0.10],
                [-0.30, -0.15, 0.05, 0.00],
                [-0.05, 0.20, -0.05, 0.15],
                [0.18, -0.08, 0.12, -0.20],
                [0.42, 0.04, -0.18, 0.08],
                [0.70, 0.18, 0.02, -0.04],
            ],
            [
                [-0.45, -0.05, 0.14, 0.12],
                [-0.22, 0.08, -0.08, -0.10],
                [0.02, 0.22, 0.04, 0.18],
                [0.27, -0.12, -0.14, -0.16],
                [0.51, 0.02, 0.16, 0.06],
                [0.76, 0.14, -0.02, -0.02],
            ],
        ],
        dtype=np.float64,
    )
    weights = np.array(
        [[0.08, 0.12, 0.17, 0.19, 0.21, 0.23], [0.10, 0.13, 0.16, 0.18, 0.20, 0.23]],
        dtype=np.float64,
    )
    return particles, np.log(weights)


def _fixtures() -> dict[str, tuple[np.ndarray, np.ndarray]]:
    return {
        "tiny_manual": _fixture_tiny_manual(),
        "small_batch": _fixture_small_batch(),
        "wider_state": _fixture_wider_state(),
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


def _run_fixture(fixture_name: str, particles_np: np.ndarray, log_weights_np: np.ndarray, settings: ValidationSettings) -> dict[str, Any]:
    particles = tf.constant(particles_np, dtype=DTYPE)
    log_weights = tf.constant(log_weights_np, dtype=DTYPE)
    rank = min(settings.rank, int(particles_np.shape[1]))
    start = time.perf_counter()
    with tf.device(settings.device):
        result = low_rank_coupling_solver_resample_tf(
            particles,
            log_weights,
            rank=rank,
            assignment_epsilon=settings.assignment_epsilon,
            alpha=settings.alpha,
            max_projection_iterations=settings.max_projection_iterations,
            convergence_threshold=settings.convergence_threshold,
            denominator_floor=settings.denominator_floor,
        )
    wall_time = time.perf_counter() - start

    matrix = low_rank_coupling_scaled_matrix_tf(result.q_factor, result.r_factor, result.g_weights)
    materialized_particles = tf.linalg.matmul(matrix, particles)
    source_weights = tf.exp(log_weights)
    num_particles = tf.cast(tf.shape(log_weights)[1], DTYPE)
    materialized_parity = tf.reduce_max(tf.abs(materialized_particles - tf.convert_to_tensor(result.particles, dtype=DTYPE)))
    row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=2) - 1.0))
    column_residual = tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=1) - source_weights * num_particles))
    diag = dict(result.diagnostics)
    component_match = diag.get("source_route_components") == EXPECTED_SOURCE_ROUTE_COMPONENTS
    route_boundary_pass = diag.get("source_route") == "extension_or_invention" and component_match
    validity_pass = bool(
        diag["finite_factors"]
        and diag["finite_particles"]
        and diag["nonnegative_factors"]
        and diag["positive_g"]
        and diag["max_factor_marginal_residual"] <= VALIDITY_THRESHOLD
        and diag["max_induced_row_residual"] <= VALIDITY_THRESHOLD
        and diag["max_induced_column_residual"] <= VALIDITY_THRESHOLD
        and _float(materialized_parity) <= MATERIALIZED_PARITY_THRESHOLD
        and route_boundary_pass
    )
    hard_vetoes: list[str] = []
    if not diag["finite_factors"] or not diag["finite_particles"]:
        hard_vetoes.append("nonfinite_values")
    if not diag["nonnegative_factors"] or not diag["positive_g"]:
        hard_vetoes.append("invalid_factor_sign_or_g")
    if diag["max_factor_marginal_residual"] > VALIDITY_THRESHOLD:
        hard_vetoes.append("factor_marginal_residual_threshold")
    if diag["max_induced_row_residual"] > VALIDITY_THRESHOLD:
        hard_vetoes.append("induced_row_residual_threshold")
    if diag["max_induced_column_residual"] > VALIDITY_THRESHOLD:
        hard_vetoes.append("induced_column_residual_threshold")
    if _float(materialized_parity) > MATERIALIZED_PARITY_THRESHOLD:
        hard_vetoes.append("materialized_apply_parity_threshold")
    if not route_boundary_pass:
        hard_vetoes.append("source_route_boundary_mismatch")

    return {
        "fixture": fixture_name,
        "validity_pass": validity_pass,
        "hard_vetoes": hard_vetoes,
        "rank": rank,
        "input_shape": {"particles": list(particles_np.shape), "log_weights": list(log_weights_np.shape)},
        "factor_shapes": diag["factor_shapes"],
        "wall_time_seconds_explanatory": wall_time,
        "finite_factors": diag["finite_factors"],
        "finite_particles": diag["finite_particles"],
        "nonnegative_factors": diag["nonnegative_factors"],
        "positive_g": diag["positive_g"],
        "max_factor_marginal_residual": diag["max_factor_marginal_residual"],
        "max_induced_row_residual": diag["max_induced_row_residual"],
        "max_induced_column_residual": diag["max_induced_column_residual"],
        "materialized_tiny_apply_parity": _float(materialized_parity),
        "materialized_row_residual": _float(row_residual),
        "materialized_column_residual": _float(column_residual),
        "projection_iterations_used": diag["projection_iterations_used"],
        "projection_error": diag["projection_error"],
        "projection_floor_hits": diag["projection_floor_hits"],
        "projection_min_denominator": diag["projection_min_denominator"],
        "min_q": diag["min_q"],
        "min_r": diag["min_r"],
        "min_g": diag["min_g"],
        "source_route": diag["source_route"],
        "source_route_components": diag["source_route_components"],
        "transport_object_kind": diag["transport_object_kind"],
        "orientation": diag["orientation"],
        "semantic_output": diag["semantic_output"],
    }


def _candidate_record(result: dict[str, Any]) -> dict[str, Any]:
    max_particles = max(row["input_shape"]["particles"][1] for row in result["rows"])
    rank = int(result["settings"]["rank"])
    record = CandidateResultRecord(
        candidate_id="wave2_low_rank_coupling_validation",
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
            "wave2_status": result["wave2_status"],
            "hard_vetoes": result["hard_vetoes"],
            "validity_pass": result["validity_pass"],
            "max_factor_marginal_residual": result["summary"]["max_factor_marginal_residual"],
            "max_induced_row_residual": result["summary"]["max_induced_row_residual"],
            "max_induced_column_residual": result["summary"]["max_induced_column_residual"],
            "materialized_tiny_apply_parity": result["summary"]["max_materialized_tiny_apply_parity"],
            "source_route_components": result["source_route_components"],
            "thresholds": result["thresholds"],
            "algorithm_complete_lane": "peer_agent_low_rank_coupling_validation",
        },
        diagnostic_roles={
            "validity_pass": "hard_veto",
            "hard_vetoes": "continuation_veto",
            "max_factor_marginal_residual": "hard_veto",
            "max_induced_row_residual": "hard_veto",
            "max_induced_column_residual": "hard_veto",
            "materialized_tiny_apply_parity": "hard_veto",
            "source_route_components": "hard_veto",
            "thresholds": "explanatory",
            "algorithm_complete_lane": "explanatory",
        },
        execution_manifest=result["manifest"],
        nonclaims=list(NONCLAIMS),
    ).to_dict()
    validate_candidate_result(record)
    return record


def build_wave2_low_rank_validation_result(settings: ValidationSettings) -> dict[str, Any]:
    rows = [_run_fixture(name, *fixture, settings) for name, fixture in _fixtures().items()]
    hard_vetoes = [f"{row['fixture']}:{veto}" for row in rows for veto in row["hard_vetoes"]]
    validity_pass = not hard_vetoes
    wave2_status = WAVE2_STATUS_PASS if validity_pass else WAVE2_STATUS_FAIL
    summary = {
        "max_factor_marginal_residual": max(row["max_factor_marginal_residual"] for row in rows),
        "max_induced_row_residual": max(row["max_induced_row_residual"] for row in rows),
        "max_induced_column_residual": max(row["max_induced_column_residual"] for row in rows),
        "max_materialized_tiny_apply_parity": max(row["materialized_tiny_apply_parity"] for row in rows),
        "max_projection_error": max(row["projection_error"] for row in rows),
        "max_projection_floor_hits": max(row["projection_floor_hits"] for row in rows),
        "min_q": min(row["min_q"] for row in rows),
        "min_r": min(row["min_r"] for row in rows),
        "min_g": min(row["min_g"] for row in rows),
        "total_wall_time_seconds_explanatory": sum(row["wall_time_seconds_explanatory"] for row in rows),
    }
    result = {
        "status": "PASS" if validity_pass else "FAIL",
        "wave2_status": wave2_status,
        "owner": "peer_agent",
        "algorithm_family": "low_rank_coupling_solver_route_validation",
        "entry_context_status": "LOW_RANK_SOLVER_ROUTE_PASSED_DIAGNOSTIC_ONLY",
        "validity_pass": validity_pass,
        "hard_vetoes": hard_vetoes,
        "semantic_class": "semantic_replacement",
        "source_route": "extension_or_invention",
        "source_route_components": dict(EXPECTED_SOURCE_ROUTE_COMPONENTS),
        "thresholds": {
            "factor_and_induced_residual_hard_veto": VALIDITY_THRESHOLD,
            "materialized_apply_parity_hard_veto": MATERIALIZED_PARITY_THRESHOLD,
            "runtime_memory_role": "explanatory_only",
        },
        "settings": {
            "rank": settings.rank,
            "assignment_epsilon": settings.assignment_epsilon,
            "alpha": settings.alpha,
            "max_projection_iterations": settings.max_projection_iterations,
            "convergence_threshold": settings.convergence_threshold,
            "denominator_floor": settings.denominator_floor,
        },
        "summary": summary,
        "rows": rows,
        "manifest": {
            "git_commit": _git_commit(),
            "timestamp_utc": _dt.datetime.now(tz=_dt.UTC).isoformat(),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "device_scope": settings.device_scope,
            "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "device": settings.device,
            "dtype": "tf.float64",
            "command": "scalable_ot_wave2_low_rank_coupling_validation.py",
            "plan_path": "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-wave2-low-rank-coupling-master-program-2026-06-19.md",
        },
        "nonclaims": list(NONCLAIMS),
    }
    result["candidate_record"] = _candidate_record(result)
    return result


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Wave 2 Low-Rank Coupling Validation Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Wave 2 status: `{result['wave2_status']}`",
        f"- Owner: `{result['owner']}`",
        f"- Algorithm family: `{result['algorithm_family']}`",
        f"- Entry context status: `{result['entry_context_status']}`",
        f"- Semantic class: `{result['semantic_class']}`",
        f"- Source route: `{result['source_route']}`",
        f"- Validity pass: `{result['validity_pass']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value | Role |",
        "| --- | ---: | --- |",
        f"| max factor marginal residual | `{result['summary']['max_factor_marginal_residual']:.6e}` | hard veto |",
        f"| max induced row residual | `{result['summary']['max_induced_row_residual']:.6e}` | hard veto |",
        f"| max induced column residual | `{result['summary']['max_induced_column_residual']:.6e}` | hard veto |",
        f"| max materialized tiny apply parity | `{result['summary']['max_materialized_tiny_apply_parity']:.6e}` | hard veto |",
        f"| max projection error | `{result['summary']['max_projection_error']:.6e}` | explanatory |",
        f"| max projection floor hits | `{result['summary']['max_projection_floor_hits']:.6e}` | explanatory |",
        f"| min Q | `{result['summary']['min_q']:.6e}` | explanatory |",
        f"| min R | `{result['summary']['min_r']:.6e}` | explanatory |",
        f"| min g | `{result['summary']['min_g']:.6e}` | explanatory |",
        f"| total wall time seconds | `{result['summary']['total_wall_time_seconds_explanatory']:.6e}` | explanatory |",
        "",
        "## Rows",
        "",
        "| Fixture | Rank | Valid | Factor residual | Row residual | Column residual | Apply parity |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in result["rows"]:
        lines.append(
            "| {fixture} | {rank} | `{valid}` | `{factor:.6e}` | `{row_res:.6e}` | `{col_res:.6e}` | `{parity:.6e}` |".format(
                fixture=row["fixture"],
                rank=row["rank"],
                valid=row["validity_pass"],
                factor=row["max_factor_marginal_residual"],
                row_res=row["max_induced_row_residual"],
                col_res=row["max_induced_column_residual"],
                parity=row["materialized_tiny_apply_parity"],
            )
        )
    lines.extend(
        [
            "",
            "## Source-Route Classification",
            "",
            "| Component | Classification |",
            "| --- | --- |",
        ]
    )
    for component, classification in result["source_route_components"].items():
        lines.append(f"| `{component}` | `{classification}` |")
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- {item}" for item in result["nonclaims"])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = build_wave2_low_rank_validation_result(_settings_from_args(args))
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result, markdown)
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
