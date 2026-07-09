#!/usr/bin/env python
"""Benchmark QR analytical Kalman score against autodiff score.

The measured kernels are TensorFlow QR/square-root Kalman computations.  The
deterministic fixture construction is outside the timed region and keeps
parameter dimension fixed at two so the requested state/measurement dimensions
are the scaling variable.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

# Deliberate CPU debug/reference runs must hide GPU devices before TensorFlow
# import so a CPU artifact does not accidentally probe CUDA.
if any(argument == "--device=cpu" for argument in sys.argv) or (
    "--device" in sys.argv and sys.argv[sys.argv.index("--device") + 1 : sys.argv.index("--device") + 2] == ["cpu"]
):
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import tensorflow as tf


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bayesfilter.linear.kalman_qr_derivatives_tf import tf_qr_sqrt_kalman_score
from bayesfilter.linear.kalman_qr_tf import (
    tf_qr_sqrt_kalman_log_likelihood_compact,
    tf_qr_sqrt_kalman_log_likelihood_while_loop,
)


DTYPE = tf.float64
PARAMETER_DIM = 2
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-kalman-qr-analytic-vs-autodiff-score-scaling-subplan-2026-07-09.md"
)
DEFAULT_JSON = (
    "docs/benchmarks/"
    "kalman_qr_analytic_vs_autodiff_score_scaling_2026-07-09.json"
)
DEFAULT_MD = (
    "docs/benchmarks/"
    "kalman_qr_analytic_vs_autodiff_score_scaling_2026-07-09.md"
)


@dataclass(frozen=True)
class Fixture:
    state_dim: int
    observation_dim: int
    timesteps: int
    parameters: tf.Tensor
    observations: tf.Tensor
    initial_mean: tf.Tensor
    initial_covariance: tf.Tensor
    transition_offset: tf.Tensor
    base_transition_matrix: tf.Tensor
    transition_covariance: tf.Tensor
    observation_offset: tf.Tensor
    observation_matrix: tf.Tensor
    base_observation_covariance: tf.Tensor


def _json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, tf.TensorShape):
        return value.as_list()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _run_text(command: list[str]) -> str:
    try:
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception as exc:  # pragma: no cover - manifest best effort.
        return f"{type(exc).__name__}: {exc}"
    text = completed.stdout.strip()
    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        return f"returncode={completed.returncode}; stdout={text}; stderr={stderr}"
    return text


def _positive_spd_from_diagonal(diagonal: tf.Tensor) -> tf.Tensor:
    return tf.linalg.diag(tf.convert_to_tensor(diagonal, dtype=DTYPE))


def _make_base_transition(state_dim: int) -> tf.Tensor:
    indices = tf.range(state_dim, dtype=DTYPE)
    denom = tf.cast(tf.maximum(state_dim - 1, 1), DTYPE)
    diagonal = 0.72 - 0.10 * indices / denom
    base = tf.linalg.diag(diagonal)
    if state_dim > 1:
        off = 0.015 * tf.ones([state_dim - 1], dtype=DTYPE)
        base += tf.linalg.diag(off, k=1)
        base += tf.linalg.diag(off, k=-1)
    return base


def _make_observation_matrix(observation_dim: int, state_dim: int) -> tf.Tensor:
    row = tf.cast(tf.range(observation_dim)[:, tf.newaxis] + 1, DTYPE)
    col = tf.cast(tf.range(state_dim)[tf.newaxis, :] + 1, DTYPE)
    smooth = 0.025 * tf.math.cos(row * col / tf.cast(state_dim + 3, DTYPE))
    return tf.eye(observation_dim, state_dim, dtype=DTYPE) + smooth / math.sqrt(state_dim)


def _model_tensors(
    parameters: tf.Tensor,
    fixture: Fixture,
) -> tuple[tf.Tensor, ...]:
    theta0, log_measurement_noise = tf.unstack(tf.convert_to_tensor(parameters, dtype=DTYPE))
    tanh_theta0 = tf.math.tanh(theta0)
    transition_scale = 0.84 + 0.05 * tanh_theta0
    d_transition_scale = 0.05 * (1.0 - tanh_theta0**2)
    measurement_scale = tf.exp(2.0 * log_measurement_noise)

    transition_matrix = transition_scale * fixture.base_transition_matrix
    observation_covariance = measurement_scale * fixture.base_observation_covariance

    zeros_n = tf.zeros([fixture.state_dim], dtype=DTYPE)
    zeros_nn = tf.zeros([fixture.state_dim, fixture.state_dim], dtype=DTYPE)
    zeros_m = tf.zeros([fixture.observation_dim], dtype=DTYPE)
    zeros_mn = tf.zeros([fixture.observation_dim, fixture.state_dim], dtype=DTYPE)
    zeros_mm = tf.zeros([fixture.observation_dim, fixture.observation_dim], dtype=DTYPE)

    d_initial_mean = tf.zeros([PARAMETER_DIM, fixture.state_dim], dtype=DTYPE)
    d_initial_covariance = tf.zeros(
        [PARAMETER_DIM, fixture.state_dim, fixture.state_dim],
        dtype=DTYPE,
    )
    d_transition_offset = tf.stack([zeros_n, zeros_n], axis=0)
    d_transition_matrix = tf.stack(
        [d_transition_scale * fixture.base_transition_matrix, zeros_nn],
        axis=0,
    )
    d_transition_covariance = tf.zeros(
        [PARAMETER_DIM, fixture.state_dim, fixture.state_dim],
        dtype=DTYPE,
    )
    d_observation_offset = tf.stack([zeros_m, zeros_m], axis=0)
    d_observation_matrix = tf.stack([zeros_mn, zeros_mn], axis=0)
    d_observation_covariance = tf.stack(
        [zeros_mm, 2.0 * observation_covariance],
        axis=0,
    )

    return (
        fixture.transition_offset,
        transition_matrix,
        fixture.transition_covariance,
        fixture.observation_offset,
        fixture.observation_matrix,
        observation_covariance,
        fixture.initial_mean,
        fixture.initial_covariance,
        d_initial_mean,
        d_initial_covariance,
        d_transition_offset,
        d_transition_matrix,
        d_transition_covariance,
        d_observation_offset,
        d_observation_matrix,
        d_observation_covariance,
    )


def _generate_observations(fixture_without_observations: Fixture) -> tf.Tensor:
    fixture = fixture_without_observations
    tensors = _model_tensors(fixture.parameters, fixture)
    transition_offset = tensors[0]
    transition_matrix = tensors[1]
    observation_offset = tensors[3]
    observation_matrix = tensors[4]
    state = fixture.initial_mean
    obs_values = []
    obs_index = tf.cast(tf.range(fixture.observation_dim) + 1, DTYPE)
    for t in range(fixture.timesteps):
        state = transition_offset + tf.linalg.matvec(transition_matrix, state)
        deterministic_noise = 0.035 * tf.math.sin(
            tf.cast(t + 1, DTYPE) * obs_index * tf.constant(0.071, dtype=DTYPE)
        )
        obs_values.append(observation_offset + tf.linalg.matvec(observation_matrix, state) + deterministic_noise)
    return tf.stack(obs_values, axis=0)


def make_fixture(state_dim: int, observation_dim: int, timesteps: int) -> Fixture:
    if state_dim != observation_dim:
        raise ValueError("this bounded benchmark expects equal state and measurement dimensions")
    state_index = tf.cast(tf.range(state_dim), DTYPE)
    obs_index = tf.cast(tf.range(observation_dim), DTYPE)
    initial_mean = 0.03 * tf.math.sin(state_index + 1.0)
    initial_covariance = _positive_spd_from_diagonal(
        0.45 + 0.02 * tf.math.mod(state_index, 5.0)
    )
    transition_offset = 0.01 * tf.math.cos((state_index + 1.0) * 0.17)
    transition_covariance = _positive_spd_from_diagonal(
        0.08 + 0.005 * tf.math.mod(state_index, 7.0)
    )
    observation_offset = 0.02 * tf.math.sin((obs_index + 1.0) * 0.11)
    base_observation_covariance = _positive_spd_from_diagonal(
        0.12 + 0.004 * tf.math.mod(obs_index, 5.0)
    )
    empty = tf.zeros([timesteps, observation_dim], dtype=DTYPE)
    fixture = Fixture(
        state_dim=state_dim,
        observation_dim=observation_dim,
        timesteps=timesteps,
        parameters=tf.constant([0.20, -0.15], dtype=DTYPE),
        observations=empty,
        initial_mean=initial_mean,
        initial_covariance=initial_covariance,
        transition_offset=transition_offset,
        base_transition_matrix=_make_base_transition(state_dim),
        transition_covariance=transition_covariance,
        observation_offset=observation_offset,
        observation_matrix=_make_observation_matrix(observation_dim, state_dim),
        base_observation_covariance=base_observation_covariance,
    )
    return Fixture(
        **{
            **fixture.__dict__,
            "observations": _generate_observations(fixture),
        }
    )


def build_analytic_fn(
    fixture: Fixture,
    *,
    jit_compile: bool,
) -> Callable[[tf.Tensor], tuple[tf.Tensor, tf.Tensor]]:
    @tf.function(
        jit_compile=jit_compile,
        reduce_retracing=True,
        input_signature=[tf.TensorSpec([PARAMETER_DIM], DTYPE)],
    )
    def analytical_score(parameters: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        tensors = _model_tensors(parameters, fixture)
        return tf_qr_sqrt_kalman_score(
            observations=fixture.observations,
            transition_offset=tensors[0],
            transition_matrix=tensors[1],
            transition_covariance=tensors[2],
            observation_offset=tensors[3],
            observation_matrix=tensors[4],
            observation_covariance=tensors[5],
            initial_state_mean=tensors[6],
            initial_state_covariance=tensors[7],
            d_initial_state_mean=tensors[8],
            d_initial_state_covariance=tensors[9],
            d_transition_offset=tensors[10],
            d_transition_matrix=tensors[11],
            d_transition_covariance=tensors[12],
            d_observation_offset=tensors[13],
            d_observation_matrix=tensors[14],
            d_observation_covariance=tensors[15],
            jitter=tf.constant(1.0e-9, dtype=DTYPE),
            jitter_updates_filtered_covariance=True,
        )

    return analytical_score


def build_autodiff_fn(
    fixture: Fixture,
    *,
    jit_compile: bool,
    value_backend: str,
    execution: str,
) -> Callable[[tf.Tensor], tuple[tf.Tensor, tf.Tensor]]:
    def raw_value(parameters: tf.Tensor) -> tf.Tensor:
        params = tf.convert_to_tensor(parameters, dtype=DTYPE)
        tensors = _model_tensors(params, fixture)
        value_kernel = (
            tf_qr_sqrt_kalman_log_likelihood_compact.python_function
            if value_backend == "compact"
            else tf_qr_sqrt_kalman_log_likelihood_while_loop.python_function
        )
        return value_kernel(
            observations=fixture.observations,
            transition_offset=tensors[0],
            transition_matrix=tensors[1],
            transition_covariance=tensors[2],
            observation_offset=tensors[3],
            observation_matrix=tensors[4],
            observation_covariance=tensors[5],
            initial_state_mean=tensors[6],
            initial_state_covariance=tensors[7],
            jitter=tf.constant(1.0e-9, dtype=DTYPE),
            jitter_updates_filtered_covariance=True,
        )

    @tf.function(
        jit_compile=jit_compile,
        reduce_retracing=True,
        input_signature=[tf.TensorSpec([PARAMETER_DIM], DTYPE)],
    )
    def value_fn(parameters: tf.Tensor) -> tf.Tensor:
        params = tf.convert_to_tensor(parameters, dtype=DTYPE)
        tensors = _model_tensors(params, fixture)
        value_kernel = (
            tf_qr_sqrt_kalman_log_likelihood_compact
            if value_backend == "compact"
            else tf_qr_sqrt_kalman_log_likelihood_while_loop
        )
        return value_kernel(
            observations=fixture.observations,
            transition_offset=tensors[0],
            transition_matrix=tensors[1],
            transition_covariance=tensors[2],
            observation_offset=tensors[3],
            observation_matrix=tensors[4],
            observation_covariance=tensors[5],
            initial_state_mean=tensors[6],
            initial_state_covariance=tensors[7],
            jitter=tf.constant(1.0e-9, dtype=DTYPE),
            jitter_updates_filtered_covariance=True,
        )

    def autodiff_score(parameters: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        params = tf.convert_to_tensor(parameters, dtype=DTYPE)
        with tf.GradientTape() as tape:
            tape.watch(params)
            value = raw_value(params) if execution == "eager" else value_fn(params)
        score = tape.gradient(value, params)
        if score is None:
            score = tf.fill(tf.shape(params), tf.constant(float("nan"), dtype=DTYPE))
        return value, score

    return autodiff_score


def _materialize(outputs: tuple[tf.Tensor, tf.Tensor]) -> tuple[float, list[float], list[str]]:
    value, score = outputs
    value_np = value.numpy()
    score_np = score.numpy()
    return float(value_np), [float(x) for x in score_np.reshape([-1])], [value.device, score.device]


def _time_call(
    fn: Callable[[tf.Tensor], tuple[tf.Tensor, tf.Tensor]],
    parameters: tf.Tensor,
    *,
    device_name: str,
) -> tuple[float, tuple[float, list[float], list[str]]]:
    start = time.perf_counter()
    with tf.device(device_name):
        outputs = fn(parameters)
    materialized = _materialize(outputs)
    elapsed = time.perf_counter() - start
    return elapsed, materialized


def _summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {
            "count": 0,
            "mean_seconds": None,
            "median_seconds": None,
            "min_seconds": None,
            "max_seconds": None,
        }
    return {
        "count": len(values),
        "mean_seconds": float(statistics.fmean(values)),
        "median_seconds": float(statistics.median(values)),
        "min_seconds": float(min(values)),
        "max_seconds": float(max(values)),
    }


def _finite_vector(values: list[float]) -> bool:
    return all(math.isfinite(value) for value in values)


def benchmark_dimension(
    *,
    state_dim: int,
    observation_dim: int,
    timesteps: int,
    warmups: int,
    repeats: int,
    jit_compile: bool,
    autodiff_value_backend: str,
    autodiff_execution: str,
    device_name: str,
) -> dict[str, Any]:
    fixture = make_fixture(state_dim, observation_dim, timesteps)
    analytical_fn = build_analytic_fn(fixture, jit_compile=jit_compile)
    autodiff_fn = build_autodiff_fn(
        fixture,
        jit_compile=jit_compile,
        value_backend=autodiff_value_backend,
        execution=autodiff_execution,
    )
    methods = {
        "analytical_qr_score": analytical_fn,
        "autodiff_qr_score": autodiff_fn,
    }
    first_calls: dict[str, float] = {}
    warmup_calls: dict[str, list[float]] = {name: [] for name in methods}
    repeated_calls: dict[str, list[float]] = {name: [] for name in methods}
    outputs: dict[str, tuple[float, list[float], list[str]]] = {}

    for name, fn in methods.items():
        elapsed, materialized = _time_call(fn, fixture.parameters, device_name=device_name)
        first_calls[name] = elapsed
        outputs[name] = materialized

    for _ in range(warmups):
        for name, fn in methods.items():
            elapsed, materialized = _time_call(fn, fixture.parameters, device_name=device_name)
            warmup_calls[name].append(elapsed)
            outputs[name] = materialized

    method_order = list(methods.items())
    for repeat_index in range(repeats):
        ordered = method_order if repeat_index % 2 == 0 else list(reversed(method_order))
        for name, fn in ordered:
            elapsed, materialized = _time_call(fn, fixture.parameters, device_name=device_name)
            repeated_calls[name].append(elapsed)
            outputs[name] = materialized

    analytical_value, analytical_score, analytical_devices = outputs["analytical_qr_score"]
    autodiff_value, autodiff_score, autodiff_devices = outputs["autodiff_qr_score"]
    value_residual = abs(analytical_value - autodiff_value)
    score_residuals = [
        abs(analytical_score[index] - autodiff_score[index])
        for index in range(PARAMETER_DIM)
    ]
    score_max_abs_residual = max(score_residuals)
    autodiff_score_norm = math.sqrt(sum(value * value for value in autodiff_score))
    score_relative_residual = score_max_abs_residual / max(1.0, autodiff_score_norm)
    all_finite = (
        math.isfinite(analytical_value)
        and math.isfinite(autodiff_value)
        and _finite_vector(analytical_score)
        and _finite_vector(autodiff_score)
    )
    parity_passed = (
        all_finite
        and value_residual <= 1.0e-8
        and score_max_abs_residual <= 1.0e-5
    )
    analytical_summary = _summary(repeated_calls["analytical_qr_score"])
    autodiff_summary = _summary(repeated_calls["autodiff_qr_score"])
    analytical_median = analytical_summary["median_seconds"]
    autodiff_median = autodiff_summary["median_seconds"]
    speed_ratio = None
    if analytical_median and autodiff_median:
        speed_ratio = float(autodiff_median / analytical_median)
    return {
        "state_dim": state_dim,
        "observation_dim": observation_dim,
        "timesteps": timesteps,
        "parameter_dim": PARAMETER_DIM,
        "jit_compile": jit_compile,
        "autodiff_value_backend": autodiff_value_backend,
        "autodiff_execution": autodiff_execution,
        "device_name": device_name,
        "input_shapes": {
            "observations": fixture.observations.shape.as_list(),
            "parameters": fixture.parameters.shape.as_list(),
        },
        "first_call_seconds": first_calls,
        "warmup_call_seconds": warmup_calls,
        "repeated_call_seconds": repeated_calls,
        "warm_call_summary": {
            "analytical_qr_score": analytical_summary,
            "autodiff_qr_score": autodiff_summary,
        },
        "descriptive_autodiff_over_analytical_median_ratio": speed_ratio,
        "outputs": {
            "analytical_value": analytical_value,
            "analytical_score": analytical_score,
            "analytical_devices": analytical_devices,
            "autodiff_value": autodiff_value,
            "autodiff_score": autodiff_score,
            "autodiff_devices": autodiff_devices,
        },
        "agreement": {
            "all_finite": all_finite,
            "parity_passed": parity_passed,
            "value_abs_residual": value_residual,
            "score_max_abs_residual": score_max_abs_residual,
            "score_relative_residual": score_relative_residual,
        },
    }


def _select_device(requested: str) -> tuple[str, dict[str, Any]]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    logical_gpus = tf.config.list_logical_devices("GPU")
    if requested == "auto":
        selected = "/GPU:0" if logical_gpus else "/CPU:0"
    elif requested == "gpu":
        if not logical_gpus:
            raise RuntimeError("requested GPU benchmark but no logical GPU is visible")
        selected = "/GPU:0"
    elif requested == "cpu":
        selected = "/CPU:0"
    else:
        selected = requested
    return selected, {
        "requested_device": requested,
        "selected_device": selected,
        "physical_gpus": [device.name for device in physical_gpus],
        "logical_gpus": [device.name for device in logical_gpus],
        "cpu_only_exception": selected.upper().startswith("/CPU"),
        "trust_basis": (
            "owner_designated_managed_session_visible_gpu_trusted"
            if selected.upper().startswith("/GPU")
            else "cpu_debug_or_reference_exception"
        ),
    }


def _manifest(args: argparse.Namespace, device_manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "cwd": str(REPO_ROOT),
        "command": " ".join(sys.argv),
        "python": sys.version,
        "python_executable": sys.executable,
        "tensorflow_version": tf.__version__,
        "git_commit": _run_text(["git", "rev-parse", "HEAD"]),
        "git_status_short": _run_text(["git", "status", "--short"]),
        "plan_path": PLAN_PATH,
        "json_path": args.output_json,
        "markdown_path": args.output_md,
        "dimensions": args.dimensions,
        "timesteps": args.timesteps,
        "warmups": args.warmups,
        "repeats": args.repeats,
        "jit_compile": args.jit_compile,
        "autodiff_value_backend": args.autodiff_value_backend,
        "autodiff_execution": args.autodiff_execution,
        "parameter_dim": PARAMETER_DIM,
        "device_manifest": device_manifest,
        "tf32_execution_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "UNSET"),
    }


def _write_markdown(payload: dict[str, Any], path: Path) -> None:
    rows = payload["rows"]
    lines = [
        "# Kalman QR Analytic Vs Autodiff Score Scaling Result",
        "",
        f"- JSON artifact: `{payload['manifest']['json_path']}`",
        f"- Plan: `{payload['manifest']['plan_path']}`",
        f"- Command: `{payload['manifest']['command']}`",
        f"- Device: `{payload['manifest']['device_manifest']['selected_device']}`",
        f"- JIT compile: `{payload['manifest']['jit_compile']}`",
        f"- Autodiff value backend: `{payload['manifest']['autodiff_value_backend']}`",
        f"- Autodiff execution: `{payload['manifest']['autodiff_execution']}`",
        f"- Trust basis: `{payload['manifest']['device_manifest']['trust_basis']}`",
        "",
        "## Decision Table",
        "",
        "| Field | Status | Notes |",
        "| --- | --- | --- |",
        (
            "| Decision | `DESCRIPTIVE_TIMING_RECORDED` | "
            "No default, HMC, or scientific promotion claim. |"
        ),
        (
            f"| Primary criterion | `{payload['summary']['all_rows_parity_passed']}` | "
            "Finite outputs and analytical/autodiff value-score parity for reported rows. |"
        ),
        "| Veto diagnostics | `see rows` | Nonfinite outputs or parity failure invalidates a row timing ratio. |",
        "| Main uncertainty | `single-run wall timing` | Repeats are descriptive and not a statistical ranking. |",
        "| Next justified action | `optional replication` | Repeat across seeds/devices or vary parameter dimension if needed. |",
        (
            "| Not concluded | `no promotion` | No HMC readiness, posterior correctness, "
            "or universal speed superiority. |"
        ),
        "",
        "## Timing Table",
        "",
        (
            "| dims `(n,m)` | analytical median s | autodiff median s | "
            "autodiff / analytical | score max abs residual | parity |"
        ),
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        if "error" in row:
            lines.append(
                "| "
                f"({row.get('state_dim')},{row.get('observation_dim')}) "
                "| N/A | N/A | N/A | N/A "
                f"| `error: {row['error']['type']}` |"
            )
            continue
        analytical = row["warm_call_summary"]["analytical_qr_score"]["median_seconds"]
        autodiff = row["warm_call_summary"]["autodiff_qr_score"]["median_seconds"]
        ratio = row["descriptive_autodiff_over_analytical_median_ratio"]
        lines.append(
            "| "
            f"({row['state_dim']},{row['observation_dim']}) "
            f"| {analytical:.6g} "
            f"| {autodiff:.6g} "
            f"| {ratio:.3f} "
            f"| {row['agreement']['score_max_abs_residual']:.3e} "
            f"| `{row['agreement']['parity_passed']}` |"
        )
    lines.extend(
        [
            "",
            "## Inference Status",
            "",
            "| Evidence class | Status |",
            "| --- | --- |",
            (
                f"| Hard veto screen | `"
                f"{payload['summary']['all_rows_parity_passed']}` |"
            ),
            "| Statistically supported ranking | `not assessed` |",
            "| Descriptive-only differences | `warm medians and ratios only` |",
            "| Default-readiness | `not assessed` |",
            "| Next evidence needed | `replicate runs and broaden model/parameter dimensions if making a speed claim` |",
            "",
            "## Run Manifest",
            "",
            f"- Git commit: `{payload['manifest']['git_commit']}`",
            f"- TensorFlow: `{payload['manifest']['tensorflow_version']}`",
            f"- Physical GPUs: `{payload['manifest']['device_manifest']['physical_gpus']}`",
            f"- Logical GPUs: `{payload['manifest']['device_manifest']['logical_gpus']}`",
            f"- CUDA_VISIBLE_DEVICES: `{payload['manifest']['cuda_visible_devices']}`",
            "- Data version: `deterministic synthetic LGSSM fixture generated by this script`",
            "- Random seeds: `N/A deterministic fixture`",
            "",
            "## Post-Run Red Team",
            "",
            (
            "The strongest alternative explanation is device/runtime noise or XLA "
                "compile/runtime behavior specific to this two-parameter dense fixture. "
                "A result that would overturn a speed interpretation is a replicated "
                "run on the target deployment device where the warm median ratios change "
                "materially or parity fails."
            ),
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dimensions", nargs="+", type=int, default=[10, 20, 30])
    parser.add_argument("--timesteps", type=int, default=120)
    parser.add_argument("--warmups", type=int, default=2)
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--device", default="auto", help="auto, gpu, cpu, or explicit TF device")
    parser.add_argument(
        "--autodiff-value-backend",
        choices=["compact", "while_loop"],
        default="compact",
        help="QR value kernel differentiated by GradientTape for the autodiff arm.",
    )
    parser.add_argument(
        "--autodiff-execution",
        choices=["eager", "tf_function"],
        default="eager",
        help="Whether the autodiff value call is eager or wrapped in tf.function.",
    )
    parser.add_argument("--output-json", default=DEFAULT_JSON)
    parser.add_argument("--output-md", default=DEFAULT_MD)
    parser.add_argument(
        "--flush-after-row",
        action="store_true",
        help="Write JSON/Markdown artifacts after each completed dimension row.",
    )
    jit_group = parser.add_mutually_exclusive_group()
    jit_group.add_argument("--jit-compile", dest="jit_compile", action="store_true")
    jit_group.add_argument("--no-jit-compile", dest="jit_compile", action="store_false")
    parser.set_defaults(jit_compile=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.timesteps <= 0:
        raise ValueError("--timesteps must be positive")
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("--warmups must be nonnegative and --repeats positive")
    output_json = REPO_ROOT / args.output_json
    output_md = REPO_ROOT / args.output_md
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    selected_device, device_manifest = _select_device(args.device)
    manifest = _manifest(args, device_manifest)
    rows = []
    started = time.perf_counter()
    payload = {
        "schema": "kalman_qr_analytic_vs_autodiff_score_scaling_v1",
        "manifest": manifest,
        "summary": {
            "all_rows_parity_passed": False,
            "wall_time_seconds": None,
            "run_status": "running",
            "nonclaims": [
                "descriptive timing only",
                "no HMC readiness claim",
                "no posterior correctness claim",
                "no production default change",
                "no statistically supported ranking",
            ],
        },
        "rows": rows,
    }
    for dimension in args.dimensions:
        try:
            rows.append(
                benchmark_dimension(
                    state_dim=dimension,
                    observation_dim=dimension,
                    timesteps=args.timesteps,
                    warmups=args.warmups,
                    repeats=args.repeats,
                    jit_compile=args.jit_compile,
                    autodiff_value_backend=args.autodiff_value_backend,
                    autodiff_execution=args.autodiff_execution,
                    device_name=selected_device,
                )
            )
        except KeyboardInterrupt:
            payload["summary"]["run_status"] = "interrupted"
            payload["summary"]["wall_time_seconds"] = time.perf_counter() - started
            output_json.write_text(
                json.dumps(payload, indent=2, sort_keys=True, default=_json_default),
                encoding="utf-8",
            )
            _write_markdown(payload, output_md)
            raise
        except Exception as exc:  # pragma: no cover - runtime artifact path.
            rows.append(
                {
                    "state_dim": dimension,
                    "observation_dim": dimension,
                    "timesteps": args.timesteps,
                    "parameter_dim": PARAMETER_DIM,
                    "jit_compile": args.jit_compile,
                    "autodiff_value_backend": args.autodiff_value_backend,
                    "autodiff_execution": args.autodiff_execution,
                    "device_name": selected_device,
                    "error": {
                        "type": type(exc).__name__,
                        "message": str(exc),
                    },
                }
            )
        if args.flush_after_row:
            payload["summary"]["wall_time_seconds"] = time.perf_counter() - started
            payload["summary"]["all_rows_parity_passed"] = (
                bool(rows)
                and all(
                    row.get("agreement", {}).get("parity_passed", False)
                    for row in rows
                )
            )
            output_json.write_text(
                json.dumps(payload, indent=2, sort_keys=True, default=_json_default),
                encoding="utf-8",
            )
            _write_markdown(payload, output_md)
    wall_time = time.perf_counter() - started
    all_rows_parity_passed = (
        bool(rows)
        and all(row.get("agreement", {}).get("parity_passed", False) for row in rows)
    )
    payload["summary"]["all_rows_parity_passed"] = all_rows_parity_passed
    payload["summary"]["wall_time_seconds"] = wall_time
    payload["summary"]["run_status"] = "complete"
    output_json.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=_json_default),
        encoding="utf-8",
    )
    _write_markdown(payload, output_md)
    print(json.dumps({
        "json": str(output_json),
        "markdown": str(output_md),
        "all_rows_parity_passed": all_rows_parity_passed,
        "wall_time_seconds": wall_time,
    }, indent=2))
    return 0 if all_rows_parity_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
