"""Low-rank coupling solver-route scale smoke diagnostics.

This lane-owned diagnostic exercises the existing TensorFlow low-rank
coupling solver-route on frozen LEDH/PFPF-shaped particle clouds.  Runtime,
memory, and TF32 metadata are explanatory only.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


_PRE = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE.add_argument("--mode", choices=("small", "medium-cpu", "tuning-cpu", "gpu-scale"), default="small")
_PRE.add_argument("--device-scope", choices=("cpu", "visible"), default=None)
_PRE.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _ = _PRE.parse_known_args()
if _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
elif _PRE_ARGS.device_scope == "cpu" or (_PRE_ARGS.device_scope is None and _PRE_ARGS.mode != "gpu-scale"):
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf  # noqa: E402

try:  # noqa: E402
    import tensorflow_probability as tfp  # noqa: E402
except Exception:  # noqa: BLE001
    tfp = None

from experiments.dpf_implementation.tf_tfp.resampling import low_rank_coupling_solver_tf  # noqa: E402
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (  # noqa: E402
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_solver_resample_tf,
)


PLAN_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-master-program-2026-06-20.md"
)
P01_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p01-harness-invariants-result-2026-06-20.md"
)
P02_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p02-medium-cpu-result-2026-06-20.md"
)
P02A_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p02a-tuning-result-2026-06-20.md"
)
P02B_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p02b-focused-tuning-result-2026-06-20.md"
)
P02C_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p02c-medium-cpu-tuned-result-2026-06-20.md"
)
P03_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-"
    "low-rank-tf32-scale-smoke-p03-trusted-gpu-scale-result-2026-06-20.md"
)

FIXTURE_ID = "bounded_smooth_v1"
FACTOR_RESIDUAL_THRESHOLD = 5.0e-3
INDUCED_ROW_RESIDUAL_THRESHOLD = 5.0e-3
INDUCED_COLUMN_RESIDUAL_THRESHOLD = 5.0e-3
TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD = 1.0e-10
LOG_WEIGHT_NORMALIZATION_THRESHOLD = 1.0e-6
WEIGHTED_MEAN_ABS_ERROR_THRESHOLD = 2.5e-2
WEIGHTED_SECOND_MOMENT_ABS_ERROR_THRESHOLD = 7.5e-2
NONCLAIMS = (
    "low-rank TF32 scale-smoke diagnostic only",
    "no speedup claim",
    "no ranking claim",
    "no superiority claim",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no production/default readiness claim",
    "no dense Sinkhorn equivalence claim",
    "no full low-rank Sinkhorn solver-fidelity claim",
    "no broad scalable-OT selection claim",
    "no TF32-help claim",
)


def _parse_args() -> argparse.Namespace:
    return _parse_args_impl(None)


def _parse_args_from_list_for_test(argv: list[str]) -> argparse.Namespace:
    return _parse_args_impl(argv)


def _parse_args_impl(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--mode", choices=("small", "medium-cpu", "tuning-cpu", "gpu-scale"), default=_PRE_ARGS.mode)
    parser.add_argument("--particle-counts", type=int, nargs="+", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--state-dim", type=int, default=None)
    parser.add_argument("--rank", type=int, default=None)
    parser.add_argument("--tuning-ranks", type=int, nargs="+", default=None)
    parser.add_argument("--tuning-assignment-epsilons", type=float, nargs="+", default=None)
    parser.add_argument("--dtype", choices=("float32", "float64"), default=None)
    parser.add_argument("--fixture-id", default=FIXTURE_ID)
    parser.add_argument("--seed", type=int, default=20260620)
    parser.add_argument("--assignment-epsilon", type=float, default=0.5)
    parser.add_argument("--alpha", type=float, default=1.0e-8)
    parser.add_argument("--max-projection-iterations", type=int, default=240)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-6)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--conditional-100k", action="store_true")
    parser.add_argument("--device", default=None)
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--tf32-mode", choices=("default", "enabled", "disabled"), default="default")
    parser.add_argument("--trust-context", default=None)
    parser.add_argument("--phase-id", default=None)
    parser.add_argument("--phase-result-path", default=None)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args(argv)
    if args.fixture_id != FIXTURE_ID:
        raise ValueError(f"fixture-id must be {FIXTURE_ID}")
    if args.assignment_epsilon <= 0.0:
        raise ValueError("assignment-epsilon must be positive")
    if args.alpha <= 0.0:
        raise ValueError("alpha must be positive")
    if args.max_projection_iterations <= 0:
        raise ValueError("max-projection-iterations must be positive")
    if args.convergence_threshold <= 0.0:
        raise ValueError("convergence-threshold must be positive")
    if args.denominator_floor <= 0.0:
        raise ValueError("denominator-floor must be positive")
    args = _apply_mode_defaults(args)
    if args.rank <= 0:
        raise ValueError("rank must be positive")
    if args.batch_size <= 0 or args.state_dim <= 0:
        raise ValueError("batch-size and state-dim must be positive")
    if any(count <= 0 for count in args.particle_counts):
        raise ValueError("particle-counts must be positive")
    if args.mode == "gpu-scale" and args.device_scope != "visible":
        raise ValueError("gpu-scale mode requires --device-scope visible")
    if args.mode != "gpu-scale" and args.device_scope != "cpu":
        raise ValueError("small, medium-cpu, and tuning-cpu modes require --device-scope cpu")
    if args.tuning_ranks is not None and any(rank <= 0 for rank in args.tuning_ranks):
        raise ValueError("tuning-ranks must be positive")
    if args.tuning_assignment_epsilons is not None and any(eps <= 0.0 for eps in args.tuning_assignment_epsilons):
        raise ValueError("tuning-assignment-epsilons must be positive")
    return args


def _apply_mode_defaults(args: argparse.Namespace) -> argparse.Namespace:
    if args.mode == "small":
        args.particle_counts = args.particle_counts or [32]
        args.batch_size = args.batch_size or 2
        args.state_dim = args.state_dim or 4
        args.rank = args.rank or 8
        args.dtype = args.dtype or "float64"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    elif args.mode == "medium-cpu":
        args.particle_counts = args.particle_counts or [4096, 8192]
        args.batch_size = args.batch_size or 2
        args.state_dim = args.state_dim or 8
        args.rank = args.rank or 64
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    elif args.mode == "tuning-cpu":
        args.particle_counts = args.particle_counts or [4096]
        args.batch_size = args.batch_size or 2
        args.state_dim = args.state_dim or 8
        args.rank = args.rank or 64
        args.tuning_ranks = args.tuning_ranks or [64, 128, 256, 512]
        args.tuning_assignment_epsilons = args.tuning_assignment_epsilons or [0.5, 0.25, 0.125, 0.0625]
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    else:
        args.particle_counts = args.particle_counts or [50000, 100000]
        args.batch_size = args.batch_size or 2
        args.state_dim = args.state_dim or 8
        args.rank = args.rank or 128
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "visible"
        args.device = args.device or "/GPU:0"
        args.trust_context = args.trust_context or "trusted_gpu_escalated_required"
    return args


def _configure_tf32(tf32_mode: str) -> dict[str, Any]:
    requested = tf32_mode
    if tf32_mode == "enabled":
        tf.config.experimental.enable_tensor_float_32_execution(True)
    elif tf32_mode == "disabled":
        tf.config.experimental.enable_tensor_float_32_execution(False)
    try:
        enabled = bool(tf.config.experimental.tensor_float_32_execution_enabled())
    except Exception as exc:  # noqa: BLE001
        enabled = f"unavailable:{type(exc).__name__}"
    return {
        "tf32_requested": requested,
        "tf32_execution_recorded": enabled,
    }


def _tf_dtype(dtype_name: str) -> tf.DType:
    if dtype_name == "float32":
        return tf.float32
    if dtype_name == "float64":
        return tf.float64
    raise ValueError(f"unsupported dtype: {dtype_name}")


def _fixture_bounded_smooth(batch_size: int, particle_count: int, state_dim: int, dtype: tf.DType) -> tuple[tf.Tensor, tf.Tensor]:
    base = tf.linspace(tf.constant(-1.0, dtype), tf.constant(1.0, dtype), particle_count)
    dim = tf.cast(tf.range(1, state_dim + 1), dtype)
    batch = tf.cast(tf.range(batch_size), dtype)
    phase = batch[:, None, None] * tf.constant(0.17, dtype)
    x = base[None, :, None]
    d = dim[None, None, :]
    raw = tf.sin((d + 0.5) * x * tf.constant(3.141592653589793, dtype) + phase)
    raw += tf.constant(0.35, dtype) * tf.cos((d + 1.5) * x * tf.constant(1.5707963267948966, dtype) - phase)
    raw_max = tf.reduce_max(tf.abs(raw), axis=[1, 2], keepdims=True)
    scaled = tf.constant(0.86, dtype) * raw / tf.maximum(raw_max, tf.constant(1.0e-12, dtype))
    offsets = (batch[:, None, None] - tf.reduce_mean(batch)) * tf.constant(0.04, dtype)
    particles = scaled + offsets

    logits = tf.constant(0.80, dtype) * tf.sin(base[None, :] * tf.constant(6.283185307179586, dtype) + batch[:, None] * 0.13)
    logits += tf.constant(0.35, dtype) * tf.cos(base[None, :] * tf.constant(15.707963267948966, dtype) - batch[:, None] * 0.07)
    logits -= tf.reduce_mean(logits, axis=1, keepdims=True)
    max_abs = tf.reduce_max(tf.abs(logits), axis=1, keepdims=True)
    logits = tf.constant(1.25, dtype) * logits / tf.maximum(max_abs, tf.constant(1.0, dtype))
    log_weights = tf.nn.log_softmax(logits, axis=1)
    return particles, log_weights


def _weighted_moments(particles: tf.Tensor, log_weights: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    weights = tf.exp(log_weights)
    mean = tf.reduce_sum(weights[:, :, None] * particles, axis=1)
    second = tf.reduce_sum(weights[:, :, None] * tf.square(particles), axis=1)
    return mean, second


def _uniform_moments(particles: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    return tf.reduce_mean(particles, axis=1), tf.reduce_mean(tf.square(particles), axis=1)


def _float(value: Any) -> float:
    return float(tf.reshape(tf.cast(value, tf.float64), [-1])[0].numpy())


def _bool(value: Any) -> bool:
    return bool(tf.reduce_all(tf.cast(value, tf.bool)).numpy())


def _run_row(
    args: argparse.Namespace,
    particle_count: int,
    *,
    force_skip: bool = False,
    rank_override: int | None = None,
    assignment_epsilon_override: float | None = None,
) -> dict[str, Any]:
    if force_skip:
        return {
            "particle_count": particle_count,
            "status": "SKIPPED",
            "skip_reason": "conditional_100k_requires_50k_pass",
            "hard_vetoes": ["conditional_100k_not_attempted_after_50k_failure"],
            "dense_transport_materialized": False,
        }

    dtype = _tf_dtype(args.dtype)
    row_rank = int(rank_override if rank_override is not None else args.rank)
    row_assignment_epsilon = float(
        assignment_epsilon_override if assignment_epsilon_override is not None else args.assignment_epsilon
    )
    low_rank_coupling_solver_tf.DTYPE = dtype
    low_rank_coupling_solver_tf.DEFAULT_DTYPE = dtype
    particles, log_weights = _fixture_bounded_smooth(args.batch_size, particle_count, args.state_dim, dtype)
    input_mean, input_second = _weighted_moments(particles, log_weights)
    naive_mean, naive_second = _uniform_moments(particles)

    start = time.perf_counter()
    with tf.device(args.device):
        result = low_rank_coupling_solver_resample_tf(
            particles,
            log_weights,
            rank=row_rank,
            assignment_epsilon=row_assignment_epsilon,
            alpha=args.alpha,
            max_projection_iterations=args.max_projection_iterations,
            convergence_threshold=args.convergence_threshold,
            denominator_floor=args.denominator_floor,
        )
    wall_time = time.perf_counter() - start

    transported = tf.convert_to_tensor(result.particles, dtype=dtype)
    out_log_weights = tf.convert_to_tensor(result.log_weights, dtype=dtype)
    output_mean, output_second = _uniform_moments(transported)
    mean_abs_error = _float(tf.reduce_max(tf.abs(output_mean - input_mean)))
    second_abs_error = _float(tf.reduce_max(tf.abs(output_second - input_second)))
    naive_mean_abs_error = _float(tf.reduce_max(tf.abs(naive_mean - input_mean)))
    naive_second_abs_error = _float(tf.reduce_max(tf.abs(naive_second - input_second)))
    log_weight_normalization = _float(tf.reduce_max(tf.abs(tf.reduce_logsumexp(out_log_weights, axis=1))))
    diag = dict(result.diagnostics)
    dense_materialized = False
    materialized_parity: float | None = None
    materialized_row_residual: float | None = None
    materialized_column_residual: float | None = None

    if args.mode == "small":
        dense_materialized = True
        matrix = low_rank_coupling_scaled_matrix_tf(result.q_factor, result.r_factor, result.g_weights)
        reconstructed = tf.linalg.matmul(matrix, particles)
        source_weights = tf.exp(log_weights)
        materialized_parity = _float(tf.reduce_max(tf.abs(reconstructed - transported)))
        materialized_row_residual = _float(tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=2) - 1.0)))
        materialized_column_residual = _float(
            tf.reduce_max(tf.abs(tf.reduce_sum(matrix, axis=1) - source_weights * tf.cast(particle_count, dtype)))
        )

    hard_vetoes: list[str] = []
    if not diag["finite_factors"] or not diag["finite_particles"] or not _bool(tf.math.is_finite(transported)):
        hard_vetoes.append("nonfinite_values")
    if not diag["nonnegative_factors"]:
        hard_vetoes.append("negative_factor")
    if not diag["positive_g"]:
        hard_vetoes.append("nonpositive_g")
    if diag["max_factor_marginal_residual"] > FACTOR_RESIDUAL_THRESHOLD:
        hard_vetoes.append("factor_marginal_residual_threshold")
    if diag["max_induced_row_residual"] > INDUCED_ROW_RESIDUAL_THRESHOLD:
        hard_vetoes.append("induced_row_residual_threshold")
    if diag["max_induced_column_residual"] > INDUCED_COLUMN_RESIDUAL_THRESHOLD:
        hard_vetoes.append("induced_column_residual_threshold")
    if log_weight_normalization > LOG_WEIGHT_NORMALIZATION_THRESHOLD:
        hard_vetoes.append("output_log_weight_normalization_threshold")
    enforce_moment_thresholds = args.mode != "small"
    if enforce_moment_thresholds and mean_abs_error > WEIGHTED_MEAN_ABS_ERROR_THRESHOLD:
        hard_vetoes.append("weighted_mean_abs_error_threshold")
    if enforce_moment_thresholds and second_abs_error > WEIGHTED_SECOND_MOMENT_ABS_ERROR_THRESHOLD:
        hard_vetoes.append("weighted_second_moment_abs_error_threshold")
    if args.mode == "small" and (materialized_parity is None or materialized_parity > TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD):
        hard_vetoes.append("tiny_materialized_apply_parity_threshold")
    if args.mode != "small" and dense_materialized:
        hard_vetoes.append("dense_transport_materialized_in_scale_mode")
    if tuple(result.transport_matrix.shape.as_list()[-2:]) != (0, 0):
        hard_vetoes.append("solver_result_materialized_transport_matrix")

    return {
        "particle_count": particle_count,
        "status": "PASS" if not hard_vetoes else "FAIL",
        "hard_vetoes": hard_vetoes,
        "fixture_id": args.fixture_id,
        "batch_size": args.batch_size,
        "state_dim": args.state_dim,
        "rank": row_rank,
        "assignment_epsilon": row_assignment_epsilon,
        "dtype": args.dtype,
        "particles_shape": transported.shape.as_list(),
        "q_shape": result.q_factor.shape.as_list(),
        "r_shape": result.r_factor.shape.as_list(),
        "g_shape": result.g_weights.shape.as_list(),
        "transport_matrix_shape": result.transport_matrix.shape.as_list(),
        "dense_transport_materialized": dense_materialized,
        "dense_materialization_role": "tiny_invariant_only" if args.mode == "small" else "forbidden_not_used",
        "finite_particles": diag["finite_particles"],
        "finite_factors": diag["finite_factors"],
        "nonnegative_factors": diag["nonnegative_factors"],
        "positive_g": diag["positive_g"],
        "max_factor_marginal_residual": diag["max_factor_marginal_residual"],
        "max_induced_row_residual": diag["max_induced_row_residual"],
        "max_induced_column_residual": diag["max_induced_column_residual"],
        "output_log_weight_normalization_residual": log_weight_normalization,
        "weighted_mean_abs_error": mean_abs_error,
        "weighted_second_moment_abs_error": second_abs_error,
        "moment_threshold_role": "explanatory_in_small_mode" if args.mode == "small" else "hard_veto",
        "naive_uniform_mean_abs_error_explanatory": naive_mean_abs_error,
        "naive_uniform_second_moment_abs_error_explanatory": naive_second_abs_error,
        "tiny_materialized_apply_parity": materialized_parity,
        "tiny_materialized_row_residual": materialized_row_residual,
        "tiny_materialized_column_residual": materialized_column_residual,
        "projection_iterations_used": diag["projection_iterations_used"],
        "projection_error_explanatory": diag["projection_error"],
        "projection_floor_hits_explanatory": diag["projection_floor_hits"],
        "projection_min_denominator_explanatory": diag["projection_min_denominator"],
        "min_q_explanatory": diag["min_q"],
        "min_r_explanatory": diag["min_r"],
        "min_g_explanatory": diag["min_g"],
        "wall_time_seconds_explanatory": wall_time,
        "memory_maxrss_kb_explanatory": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "source_route": diag["source_route"],
        "source_route_components": diag["source_route_components"],
        "solver_fidelity": diag["solver_fidelity"],
        "transport_object_kind": diag["transport_object_kind"],
        "transport_matrix_materialized_by_solver": diag["transport_matrix_materialized"],
    }


def _git_output(args: list[str]) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _device_metadata() -> dict[str, Any]:
    gpu_devices = [device.name for device in tf.config.list_physical_devices("GPU")]
    metadata: dict[str, Any] = {
        "gpu_devices": gpu_devices,
        "visible_logical_gpus": [device.name for device in tf.config.list_logical_devices("GPU")],
    }
    try:
        metadata["gpu0_memory_info"] = tf.config.experimental.get_memory_info("GPU:0") if gpu_devices else None
    except Exception as exc:  # noqa: BLE001
        metadata["gpu0_memory_info"] = f"unavailable:{type(exc).__name__}"
    return metadata


def _run_manifest(
    args: argparse.Namespace,
    *,
    started_at: str,
    ended_at: str,
    wall_time_seconds: float,
    output_path: str,
    markdown_path: str,
    tf32_metadata: dict[str, Any],
) -> dict[str, Any]:
    phase_result = args.phase_result_path or {
        "small": P01_RESULT_PATH,
        "medium-cpu": P02_RESULT_PATH,
        "tuning-cpu": P02A_RESULT_PATH,
        "gpu-scale": P03_RESULT_PATH,
    }[args.mode]
    return {
        "git_commit": _git_output(["git", "rev-parse", "HEAD"]),
        "git_status_short": _git_output(["git", "status", "--short"]),
        "command": " ".join(sys.argv),
        "working_directory": str(ROOT),
        "python_executable": sys.executable,
        "python_version": sys.version,
        "platform": platform.platform(),
        "tensorflow_version": tf.__version__,
        "tensorflow_probability_version": getattr(tfp, "__version__", "unavailable"),
        "device_mode": args.mode,
        "device_scope": args.device_scope,
        "device": args.device,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "cpu_gpu_trust_context": args.trust_context,
        **tf32_metadata,
        **_device_metadata(),
        "fixture_id": args.fixture_id,
        "batch_size": args.batch_size,
        "state_dim": args.state_dim,
        "particle_counts": list(args.particle_counts),
        "rank": args.rank,
        "tuning_ranks": args.tuning_ranks,
        "tuning_assignment_epsilons": args.tuning_assignment_epsilons,
        "assignment_epsilon": args.assignment_epsilon,
        "dtype": args.dtype,
        "seed": args.seed,
        "started_at": started_at,
        "ended_at": ended_at,
        "wall_time_seconds": wall_time_seconds,
        "artifact_paths": {"json": output_path, "markdown": markdown_path},
        "plan_path": PLAN_PATH,
        "phase_result_path": phase_result,
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    tf.random.set_seed(args.seed)
    tf32_metadata = _configure_tf32(args.tf32_mode)
    started_at = _dt.datetime.now(tz=_dt.UTC).isoformat()
    start = time.perf_counter()

    rows: list[dict[str, Any]] = []
    if args.mode == "tuning-cpu":
        for particle_count in args.particle_counts:
            for rank in args.tuning_ranks:
                for epsilon in args.tuning_assignment_epsilons:
                    row = _run_row(
                        args,
                        particle_count,
                        rank_override=rank,
                        assignment_epsilon_override=epsilon,
                    )
                    row["grid_role"] = "tuning_candidate"
                    rows.append(row)
    else:
        skip_remaining = False
        for index, particle_count in enumerate(args.particle_counts):
            force_skip = bool(args.mode == "gpu-scale" and args.conditional_100k and index > 0 and skip_remaining)
            row = _run_row(args, particle_count, force_skip=force_skip)
            rows.append(row)
            if args.mode == "gpu-scale" and args.conditional_100k and index == 0 and row["hard_vetoes"]:
                skip_remaining = True

    viable_rows = [row for row in rows if row.get("status") == "PASS"]
    if args.mode == "tuning-cpu":
        hard_vetoes = [] if viable_rows else ["tuning_grid_no_viable_setting"]
    else:
        hard_vetoes = [f"N={row['particle_count']}:{veto}" for row in rows for veto in row.get("hard_vetoes", [])]
    ended_at = _dt.datetime.now(tz=_dt.UTC).isoformat()
    wall_time = time.perf_counter() - start
    output_path = str(Path(args.output))
    markdown_path = str(Path(args.markdown_output))
    manifest = _run_manifest(
        args,
        started_at=started_at,
        ended_at=ended_at,
        wall_time_seconds=wall_time,
        output_path=output_path,
        markdown_path=markdown_path,
        tf32_metadata=tf32_metadata,
    )
    summary = _summary(rows, hard_vetoes, wall_time)
    return {
        "status": "PASS" if not hard_vetoes else "FAIL",
        "phase": args.phase_id
        or {"small": "LR-TF32-1", "medium-cpu": "LR-TF32-2", "tuning-cpu": "LR-TF32-2A", "gpu-scale": "LR-TF32-3"}[
            args.mode
        ],
        "mode": args.mode,
        "algorithm_family": "low_rank_coupling_solver_route_scale_smoke",
        "algorithm_under_test": "P = Q diag(1/g) R^T lazy low-rank solver-route resampling",
        "fixture_contract": {
            "fixture_id": FIXTURE_ID,
            "particle_coordinate_abs_bound": 1.0,
            "log_weight_logit_abs_bound": 1.25,
            "batch_offset_abs_bound": 0.10,
        },
        "thresholds": {
            "factor_marginal_residual": FACTOR_RESIDUAL_THRESHOLD,
            "induced_row_residual": INDUCED_ROW_RESIDUAL_THRESHOLD,
            "induced_column_residual": INDUCED_COLUMN_RESIDUAL_THRESHOLD,
            "tiny_materialized_apply_parity": TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD,
            "output_log_weight_normalization_residual": LOG_WEIGHT_NORMALIZATION_THRESHOLD,
            "weighted_mean_abs_error": WEIGHTED_MEAN_ABS_ERROR_THRESHOLD,
            "weighted_second_moment_abs_error": WEIGHTED_SECOND_MOMENT_ABS_ERROR_THRESHOLD,
            "runtime_memory_tf32_role": "explanatory_only",
        },
        "hard_vetoes": hard_vetoes,
        "summary": summary,
        "viable_tuned_rows": viable_rows,
        "selected_tuned_setting": _selected_tuned_setting(viable_rows),
        "rows": rows,
        "run_manifest": manifest,
        "nonclaims": list(NONCLAIMS),
    }


def _summary(rows: list[dict[str, Any]], hard_vetoes: list[str], wall_time: float) -> dict[str, Any]:
    numeric_rows = [row for row in rows if row.get("status") != "SKIPPED"]
    def _max(key: str) -> float | None:
        values = [row.get(key) for row in numeric_rows if row.get(key) is not None]
        return max(values) if values else None

    return {
        "num_rows": len(rows),
        "num_executed_rows": len(numeric_rows),
        "num_hard_vetoes": len(hard_vetoes),
        "num_viable_rows": sum(1 for row in rows if row.get("status") == "PASS"),
        "max_factor_marginal_residual": _max("max_factor_marginal_residual"),
        "max_induced_row_residual": _max("max_induced_row_residual"),
        "max_induced_column_residual": _max("max_induced_column_residual"),
        "max_output_log_weight_normalization_residual": _max("output_log_weight_normalization_residual"),
        "max_weighted_mean_abs_error": _max("weighted_mean_abs_error"),
        "max_weighted_second_moment_abs_error": _max("weighted_second_moment_abs_error"),
        "max_tiny_materialized_apply_parity": _max("tiny_materialized_apply_parity"),
        "max_wall_time_seconds_explanatory": _max("wall_time_seconds_explanatory"),
        "total_wall_time_seconds_explanatory": wall_time,
        "max_memory_maxrss_kb_explanatory": _max("memory_maxrss_kb_explanatory"),
    }


def _selected_tuned_setting(viable_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not viable_rows:
        return None
    selected = min(
        viable_rows,
        key=lambda row: (
            row["rank"],
            row["assignment_epsilon"],
            row["weighted_second_moment_abs_error"],
        ),
    )
    return {
        "rank": selected["rank"],
        "assignment_epsilon": selected["assignment_epsilon"],
        "particle_count": selected["particle_count"],
        "weighted_second_moment_abs_error": selected["weighted_second_moment_abs_error"],
        "weighted_mean_abs_error": selected["weighted_mean_abs_error"],
        "max_factor_marginal_residual": selected["max_factor_marginal_residual"],
        "max_induced_row_residual": selected["max_induced_row_residual"],
        "max_induced_column_residual": selected["max_induced_column_residual"],
    }


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, (tf.Tensor,)):
        return _json_ready(value.numpy().tolist())
    return value


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Low-Rank TF32 Scale Smoke Diagnostics",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase: `{result['phase']}`",
        f"- Mode: `{result['mode']}`",
        f"- Algorithm: `{result['algorithm_under_test']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
        "",
        "## Summary",
        "",
        "| Metric | Value | Role |",
        "| --- | ---: | --- |",
    ]
    for key, value in result["summary"].items():
        role = "hard veto" if key in {
            "num_hard_vetoes",
            "max_factor_marginal_residual",
            "max_induced_row_residual",
            "max_induced_column_residual",
            "max_output_log_weight_normalization_residual",
            "max_weighted_mean_abs_error",
            "max_weighted_second_moment_abs_error",
            "max_tiny_materialized_apply_parity",
        } else "explanatory"
        lines.append(f"| {key} | `{value}` | {role} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| N | Rank | Epsilon | Status | Hard vetoes | Factor residual | Row residual | Column residual | Mean error | Second error | Dense materialized |",
            "| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["rows"]:
        lines.append(
            "| {n} | `{rank}` | `{epsilon}` | `{status}` | `{vetoes}` | `{factor}` | `{row_res}` | `{col_res}` | `{mean}` | `{second}` | `{dense}` |".format(
                n=row["particle_count"],
                rank=row.get("rank"),
                epsilon=row.get("assignment_epsilon"),
                status=row["status"],
                vetoes=row.get("hard_vetoes", []),
                factor=row.get("max_factor_marginal_residual"),
                row_res=row.get("max_induced_row_residual"),
                col_res=row.get("max_induced_column_residual"),
                mean=row.get("weighted_mean_abs_error"),
                second=row.get("weighted_second_moment_abs_error"),
                dense=row.get("dense_transport_materialized"),
            )
        )
    lines.extend(
        [
            "",
            "## Run Manifest",
            "",
            f"- Git commit: `{result['run_manifest']['git_commit']}`",
            f"- Command: `{result['run_manifest']['command']}`",
            f"- Device scope: `{result['run_manifest']['device_scope']}`",
            f"- CUDA_VISIBLE_DEVICES: `{result['run_manifest']['cuda_visible_devices']}`",
            f"- TF32 requested: `{result['run_manifest']['tf32_requested']}`",
            f"- TF32 execution recorded: `{result['run_manifest']['tf32_execution_recorded']}`",
            f"- Fixture: `{result['run_manifest']['fixture_id']}`",
            "",
            "## Non-Claims",
            "",
        ]
    )
    lines.extend(f"- {nonclaim}" for nonclaim in result["nonclaims"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = build_result(args)
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
