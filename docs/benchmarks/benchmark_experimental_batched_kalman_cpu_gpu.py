"""Benchmark the experimental batched Kalman value+score kernel.

This is a standalone diagnostic harness for the additive experimental module in
``bayesfilter.linear.experimental_batched_kalman_tf``.  It deliberately avoids
importing pytest helpers because those helpers hide GPUs for deterministic CPU
tests.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any

_pre_parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_pre_parser.add_argument(
    "--device-scope",
    choices=("cpu", "visible"),
    default="visible",
    help="Hide GPU for CPU timing or leave configured devices visible.",
)
_pre_parser.add_argument(
    "--cuda-visible-devices",
    default=None,
    help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
)
_pre_args, _ = _pre_parser.parse_known_args()
if _pre_args.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _pre_args.cuda_visible_devices
elif _pre_args.device_scope == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import tensorflow as tf

from bayesfilter.linear.experimental_batched_kalman_tf import (
    tf_batched_kalman_value_and_score,
)
from bayesfilter.linear.kalman_qr_derivatives_tf import tf_qr_sqrt_kalman_score


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--mode",
        choices=("timing", "compiled-timing", "scalar-compiled-loop"),
        default="timing",
    )
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--time-steps", type=int, default=200)
    parser.add_argument("--state-dim", type=int, default=10)
    parser.add_argument("--obs-dim", type=int, default=10)
    parser.add_argument("--parameter-dim", type=int, default=2)
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument(
        "--device-scope",
        choices=("cpu", "visible"),
        default=_pre_args.device_scope,
        help="Hide GPU for CPU timing or leave configured devices visible.",
    )
    parser.add_argument(
        "--cuda-visible-devices",
        default=_pre_args.cuda_visible_devices,
        help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
    )
    parser.add_argument(
        "--expect-device-kind",
        choices=("any", "cpu", "gpu"),
        default="any",
        help="Fail closed if value/score tensors are not placed as expected.",
    )
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def _configure_gpus() -> tuple[list[str], list[str]]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return ([str(device) for device in physical_gpus], [str(device) for device in logical_gpus])


def _stable_fixture(
    *,
    batch_size: int,
    time_steps: int,
    state_dim: int,
    obs_dim: int,
    parameter_dim: int,
) -> dict[str, np.ndarray]:
    if parameter_dim != 2:
        raise ValueError("this diagnostic fixture currently expects parameter_dim=2")
    if obs_dim != state_dim:
        raise ValueError("this diagnostic fixture currently expects obs_dim=state_dim")

    t_grid = np.arange(time_steps, dtype=np.float64)[:, None]
    obs_grid = np.arange(obs_dim, dtype=np.float64)[None, :]
    observations = 0.10 * np.sin(0.031 * t_grid + 0.17 * obs_grid)
    observations += 0.05 * np.cos(0.047 * t_grid - 0.11 * obs_grid)

    batch_grid = np.linspace(-1.0, 1.0, batch_size, dtype=np.float64)
    theta0 = 0.35 * batch_grid
    theta1 = -1.10 + 0.12 * batch_grid
    transition_scale = 0.58 + 0.10 * np.tanh(theta0)
    d_transition_scale = 0.10 * (1.0 - np.tanh(theta0) ** 2)
    observation_variance = np.exp(2.0 * theta1)
    d_observation_variance = 2.0 * observation_variance

    state_index = np.arange(state_dim, dtype=np.float64)
    superdiag = np.zeros((state_dim, state_dim), dtype=np.float64)
    superdiag[:-1, 1:] = 0.012
    state_wave = np.diag(0.015 * np.sin(0.23 * state_index))
    base_drift = superdiag + state_wave
    observation_cross = np.zeros((obs_dim, state_dim), dtype=np.float64)
    observation_cross[:, :] = 0.003 / float(max(1, state_dim))
    np.fill_diagonal(observation_cross, 1.0)

    transition_matrix = np.empty((batch_size, state_dim, state_dim), dtype=np.float64)
    d_transition_matrix = np.zeros(
        (batch_size, parameter_dim, state_dim, state_dim),
        dtype=np.float64,
    )
    observation_covariance = np.empty((batch_size, obs_dim, obs_dim), dtype=np.float64)
    d_observation_covariance = np.zeros(
        (batch_size, parameter_dim, obs_dim, obs_dim),
        dtype=np.float64,
    )
    eye_state = np.eye(state_dim, dtype=np.float64)
    eye_obs = np.eye(obs_dim, dtype=np.float64)
    for batch_index in range(batch_size):
        transition_matrix[batch_index] = transition_scale[batch_index] * eye_state + base_drift
        d_transition_matrix[batch_index, 0] = d_transition_scale[batch_index] * eye_state
        observation_covariance[batch_index] = observation_variance[batch_index] * eye_obs
        d_observation_covariance[batch_index, 1] = d_observation_variance[batch_index] * eye_obs

    zeros_bp_n = np.zeros((batch_size, parameter_dim, state_dim), dtype=np.float64)
    zeros_bp_nn = np.zeros((batch_size, parameter_dim, state_dim, state_dim), dtype=np.float64)
    zeros_bp_m = np.zeros((batch_size, parameter_dim, obs_dim), dtype=np.float64)
    zeros_bp_mn = np.zeros((batch_size, parameter_dim, obs_dim, state_dim), dtype=np.float64)

    return {
        "observations": observations,
        "transition_offset": np.full((batch_size, state_dim), 0.01, dtype=np.float64),
        "transition_matrix": transition_matrix,
        "transition_covariance": np.broadcast_to(
            0.04 * eye_state,
            (batch_size, state_dim, state_dim),
        ).copy(),
        "observation_offset": np.full((batch_size, obs_dim), 0.02, dtype=np.float64),
        "observation_matrix": np.broadcast_to(
            observation_cross,
            (batch_size, obs_dim, state_dim),
        ).copy(),
        "observation_covariance": observation_covariance,
        "initial_state_mean": np.broadcast_to(
            0.02 * np.sin(0.19 * state_index),
            (batch_size, state_dim),
        ).copy(),
        "initial_state_covariance": np.broadcast_to(
            0.35 * eye_state,
            (batch_size, state_dim, state_dim),
        ).copy(),
        "d_initial_state_mean": zeros_bp_n,
        "d_initial_state_covariance": zeros_bp_nn,
        "d_transition_offset": zeros_bp_n,
        "d_transition_matrix": d_transition_matrix,
        "d_transition_covariance": zeros_bp_nn,
        "d_observation_offset": zeros_bp_m,
        "d_observation_matrix": zeros_bp_mn,
        "d_observation_covariance": d_observation_covariance,
    }


def _to_tensors(fixture: dict[str, np.ndarray]) -> dict[str, tf.Tensor]:
    return {name: tf.constant(value, dtype=tf.float64) for name, value in fixture.items()}


def _batched_value_and_score_from_tensors(
    tensors: dict[str, tf.Tensor],
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    value, score = tf_batched_kalman_value_and_score(
        observations,
        transition_offset=tensors["transition_offset"],
        transition_matrix=tensors["transition_matrix"],
        transition_covariance=tensors["transition_covariance"],
        observation_offset=tensors["observation_offset"],
        observation_matrix=tensors["observation_matrix"],
        observation_covariance=tensors["observation_covariance"],
        initial_state_mean=tensors["initial_state_mean"],
        initial_state_covariance=tensors["initial_state_covariance"],
        d_initial_state_mean=tensors["d_initial_state_mean"],
        d_initial_state_covariance=tensors["d_initial_state_covariance"],
        d_transition_offset=tensors["d_transition_offset"],
        d_transition_matrix=tensors["d_transition_matrix"],
        d_transition_covariance=tensors["d_transition_covariance"],
        d_observation_offset=tensors["d_observation_offset"],
        d_observation_matrix=tensors["d_observation_matrix"],
        d_observation_covariance=tensors["d_observation_covariance"],
        jitter=tf.constant(1.0e-9, dtype=tf.float64),
    )
    return value, score


def _materialized_call(tensors: dict[str, tf.Tensor]) -> tuple[tf.Tensor, tf.Tensor]:
    value, score = _batched_value_and_score_from_tensors(
        tensors,
        tensors["observations"],
    )
    _ = value.numpy()
    _ = score.numpy()
    return value, score


def _timed_call(tensors: dict[str, tf.Tensor]) -> tuple[float, tf.Tensor, tf.Tensor]:
    start = time.perf_counter()
    value, score = _materialized_call(tensors)
    return time.perf_counter() - start, value, score


def _compiled_materialized_call(
    compiled_call: Any,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    value, score = compiled_call(observations)
    _ = value.numpy()
    _ = score.numpy()
    return value, score


def _timed_compiled_call(
    compiled_call: Any,
    observations: tf.Tensor,
) -> tuple[float, tf.Tensor, tf.Tensor]:
    start = time.perf_counter()
    value, score = _compiled_materialized_call(compiled_call, observations)
    return time.perf_counter() - start, value, score


@tf.function(jit_compile=True)
def _compiled_scalar_row_call(
    observations: tf.Tensor,
    transition_offset: tf.Tensor,
    transition_matrix: tf.Tensor,
    transition_covariance: tf.Tensor,
    observation_offset: tf.Tensor,
    observation_matrix: tf.Tensor,
    observation_covariance: tf.Tensor,
    initial_state_mean: tf.Tensor,
    initial_state_covariance: tf.Tensor,
    d_initial_state_mean: tf.Tensor,
    d_initial_state_covariance: tf.Tensor,
    d_transition_offset: tf.Tensor,
    d_transition_matrix: tf.Tensor,
    d_transition_covariance: tf.Tensor,
    d_observation_offset: tf.Tensor,
    d_observation_matrix: tf.Tensor,
    d_observation_covariance: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    return tf_qr_sqrt_kalman_score(
        observations=observations,
        transition_offset=transition_offset,
        transition_matrix=transition_matrix,
        transition_covariance=transition_covariance,
        observation_offset=observation_offset,
        observation_matrix=observation_matrix,
        observation_covariance=observation_covariance,
        initial_state_mean=initial_state_mean,
        initial_state_covariance=initial_state_covariance,
        d_initial_state_mean=d_initial_state_mean,
        d_initial_state_covariance=d_initial_state_covariance,
        d_transition_offset=d_transition_offset,
        d_transition_matrix=d_transition_matrix,
        d_transition_covariance=d_transition_covariance,
        d_observation_offset=d_observation_offset,
        d_observation_matrix=d_observation_matrix,
        d_observation_covariance=d_observation_covariance,
        jitter=tf.constant(1.0e-9, dtype=tf.float64),
    )


def _scalar_loop_materialized_call(
    tensors: dict[str, tf.Tensor],
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    values = []
    scores = []
    for row in range(int(tensors["initial_state_mean"].shape[0])):
        value, score = _compiled_scalar_row_call(
            observations,
            tensors["transition_offset"][row],
            tensors["transition_matrix"][row],
            tensors["transition_covariance"][row],
            tensors["observation_offset"][row],
            tensors["observation_matrix"][row],
            tensors["observation_covariance"][row],
            tensors["initial_state_mean"][row],
            tensors["initial_state_covariance"][row],
            tensors["d_initial_state_mean"][row],
            tensors["d_initial_state_covariance"][row],
            tensors["d_transition_offset"][row],
            tensors["d_transition_matrix"][row],
            tensors["d_transition_covariance"][row],
            tensors["d_observation_offset"][row],
            tensors["d_observation_matrix"][row],
            tensors["d_observation_covariance"][row],
        )
        values.append(value)
        scores.append(score)
    value_batch = tf.stack(values, axis=0)
    score_batch = tf.stack(scores, axis=0)
    _ = value_batch.numpy()
    _ = score_batch.numpy()
    return value_batch, score_batch


def _timed_scalar_loop_call(
    tensors: dict[str, tf.Tensor],
    observations: tf.Tensor,
) -> tuple[float, tf.Tensor, tf.Tensor]:
    start = time.perf_counter()
    value, score = _scalar_loop_materialized_call(tensors, observations)
    return time.perf_counter() - start, value, score


def _summary(values: list[float]) -> dict[str, float]:
    return {
        "min_seconds": min(values),
        "median_seconds": statistics.median(values),
        "mean_seconds": statistics.fmean(values),
        "max_seconds": max(values),
    }


def _validate_device(
    *,
    expect_device_kind: str,
    physical_gpus: list[str],
    value: tf.Tensor,
    score: tf.Tensor,
) -> None:
    value_is_gpu = "GPU" in value.device.upper()
    score_is_gpu = "GPU" in score.device.upper()
    value_is_cpu = "CPU" in value.device.upper()
    score_is_cpu = "CPU" in score.device.upper()
    if expect_device_kind == "gpu":
        if not physical_gpus:
            raise RuntimeError("expected a GPU run, but TensorFlow sees no physical GPUs")
        if not (value_is_gpu and score_is_gpu):
            raise RuntimeError(
                f"expected GPU tensor placement, got value={value.device}, score={score.device}"
            )
    if expect_device_kind == "cpu" and not (value_is_cpu and score_is_cpu):
        raise RuntimeError(
            f"expected CPU tensor placement, got value={value.device}, score={score.device}"
        )


def _base_result(
    args: argparse.Namespace,
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    return {
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python": platform.python_version(),
        "tensorflow": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "device_arg": args.device,
        "device_scope": args.device_scope,
        "expect_device_kind": args.expect_device_kind,
        "physical_gpus": physical_gpus,
        "logical_gpus": logical_gpus,
        "shape": {
            "batch_size": args.batch_size,
            "time_steps": args.time_steps,
            "state_dim": args.state_dim,
            "obs_dim": args.obs_dim,
            "parameter_dim": args.parameter_dim,
        },
        "notes": [
            "Single-shape diagnostic only; not a production benchmark.",
            "The experimental kernel hardcasts tensors to float64.",
            "Time remains sequential; the batch axis parallelizes independent parameter rows.",
        ],
    }


def _finish_timing_result(
    *,
    args: argparse.Namespace,
    physical_gpus: list[str],
    logical_gpus: list[str],
    mode: str,
    value: tf.Tensor,
    score: tf.Tensor,
    timings: list[float],
    timing_policy: dict[str, Any],
    compiler: dict[str, Any] | None = None,
) -> dict[str, Any]:
    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )
    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": mode,
            "timing_policy": timing_policy,
            "warm_call_summary": _summary(timings),
            "per_filter_warm_median_seconds": statistics.median(timings) / args.batch_size,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "finite_outputs": finite,
        }
    )
    if compiler is not None:
        result["compiler"] = compiler
    return result


def _run_timing(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")

    with tf.device(args.device):
        first_call_seconds, value, score = _timed_call(tensors)
        for _ in range(args.warmups):
            _materialized_call(tensors)
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score = _timed_call(tensors)
            timings.append(elapsed)

    result = _finish_timing_result(
        args=args,
        physical_gpus=physical_gpus,
        logical_gpus=logical_gpus,
        mode="timing",
        value=value,
        score=score,
        timings=timings,
        timing_policy={
            "first_call_includes_trace_and_initialization": True,
            "warmups": args.warmups,
            "repeats": args.repeats,
            "materialization": "value.numpy() and score.numpy() after each call",
        },
    )
    result["first_call_seconds"] = first_call_seconds
    return result


def _run_compiled_timing(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")

    @tf.function(jit_compile=True)
    def compiled_call(observations: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return _batched_value_and_score_from_tensors(tensors, observations)

    with tf.device(args.device):
        compile_and_first_call_seconds, value, score = _timed_compiled_call(
            compiled_call,
            tensors["observations"],
        )
        for _ in range(args.warmups):
            _compiled_materialized_call(compiled_call, tensors["observations"])
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score = _timed_compiled_call(
                compiled_call,
                tensors["observations"],
            )
            timings.append(elapsed)

    return _finish_timing_result(
        args=args,
        physical_gpus=physical_gpus,
        logical_gpus=logical_gpus,
        mode="compiled-timing",
        value=value,
        score=score,
        timings=timings,
        compiler={
            "tf_function": True,
            "jit_compile": True,
            "compile_and_first_call_seconds": compile_and_first_call_seconds,
            "warm_calls_exclude_compile": True,
            "compiled_unit": "batched_value_score",
        },
        timing_policy={
            "first_call_includes_trace_compile_and_initialization": True,
            "warmups": args.warmups,
            "repeats": args.repeats,
            "materialization": "value.numpy() and score.numpy() after each compiled call",
        },
    )


def _run_scalar_compiled_loop(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")

    with tf.device(args.device):
        compile_start = time.perf_counter()
        value, score = _scalar_loop_materialized_call(
            tensors,
            tensors["observations"],
        )
        compile_and_first_call_seconds = time.perf_counter() - compile_start
        for _ in range(args.warmups):
            _scalar_loop_materialized_call(tensors, tensors["observations"])
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score = _timed_scalar_loop_call(
                tensors,
                tensors["observations"],
            )
            timings.append(elapsed)

    result = _finish_timing_result(
        args=args,
        physical_gpus=physical_gpus,
        logical_gpus=logical_gpus,
        mode="scalar-compiled-loop",
        value=value,
        score=score,
        timings=timings,
        compiler={
            "tf_function": True,
            "jit_compile": True,
            "compile_and_first_call_seconds": compile_and_first_call_seconds,
            "warm_calls_exclude_compile": True,
            "compiled_unit": "one_scalar_value_score_row",
            "python_loop_over_rows_in_benchmark_harness": True,
        },
        timing_policy={
            "first_call_includes_trace_compile_and_initialization": True,
            "warmups": args.warmups,
            "repeats": args.repeats,
            "materialization": "stacked value.numpy() and score.numpy() after scalar compiled row loop",
        },
    )
    result["notes"] = [
        *result["notes"],
        "Scalar-loop mode is a benchmark comparator; it is not an HMC-jittable production implementation.",
    ]
    return result


def main() -> None:
    args = _parse_args()
    physical_gpus, logical_gpus = _configure_gpus()
    fixture = _stable_fixture(
        batch_size=args.batch_size,
        time_steps=args.time_steps,
        state_dim=args.state_dim,
        obs_dim=args.obs_dim,
        parameter_dim=args.parameter_dim,
    )
    tensors = _to_tensors(fixture)
    if args.mode == "timing":
        result = _run_timing(args, tensors, physical_gpus, logical_gpus)
    elif args.mode == "compiled-timing":
        result = _run_compiled_timing(args, tensors, physical_gpus, logical_gpus)
    else:
        result = _run_scalar_compiled_loop(args, tensors, physical_gpus, logical_gpus)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
