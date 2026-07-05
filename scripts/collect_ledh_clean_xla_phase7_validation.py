#!/usr/bin/env python
"""Collect Phase 7 GPU/XLA numerical validation for the LEDH-PFPF-OT full route."""

from __future__ import annotations

import argparse
import datetime as dt
import inspect
import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf

from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as core_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf


PARAMETER_NAMES = tuple(p8p.PARAMETER_NAMES)
PHASE6_HLO_TEXT_LENGTH = 27_766_809


def _parse_int_csv(value: str) -> list[int]:
    parsed = [int(item.strip()) for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one seed")
    return parsed


def _parse_float_csv(value: str, *, expected: int | None = None) -> list[float]:
    parsed = [float(item.strip()) for item in str(value).split(",") if item.strip()]
    if expected is not None and len(parsed) != expected:
        raise ValueError(f"expected {expected} comma-separated floats")
    if not parsed:
        raise ValueError("expected at least one float")
    if not all(math.isfinite(item) for item in parsed):
        raise ValueError("all floats must be finite")
    return parsed


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="/GPU:0")
    parser.add_argument("--expect-device-kind", choices=("gpu", "cpu", "any"), default="gpu")
    parser.add_argument("--batch-seeds", default="81120")
    parser.add_argument("--time-steps", type=int, default=1)
    parser.add_argument("--num-particles", type=int, default=16)
    parser.add_argument("--theta", default="0.02,-0.01,0.01")
    parser.add_argument("--fd-steps", default="0.002,0.001,0.0005")
    parser.add_argument("--sinkhorn-iterations", type=int, default=2)
    parser.add_argument("--sinkhorn-epsilon", type=float, default=1.0)
    parser.add_argument("--annealed-scaling", type=float, default=0.9)
    parser.add_argument("--row-chunk-size", type=int, default=16)
    parser.add_argument("--col-chunk-size", type=int, default=16)
    parser.add_argument("--particle-chunk-size", type=int, default=16)
    parser.add_argument("--dtype", choices=("float32", "float64"), default="float32")
    parser.add_argument("--tf32-mode", choices=("enabled", "disabled", "default"), default="enabled")
    parser.add_argument("--repeat-atol", type=float, default=1.0e-5)
    parser.add_argument("--fd-analytic-sign-threshold", type=float, default=1.0e-4)
    parser.add_argument("--fd-absolute-floor", type=float, default=1.0e-3)
    parser.add_argument("--fd-relative-factor", type=float, default=0.02)
    parser.add_argument("--compile-timeout-seconds", type=float, default=600.0)
    parser.add_argument("--hlo-baseline-text-length", type=int, default=PHASE6_HLO_TEXT_LENGTH)
    parser.add_argument("--hlo-max-factor", type=float, default=4.0)
    parser.add_argument(
        "--plan-path",
        default=(
            "docs/plans/"
            "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-subplan-2026-07-02.md"
        ),
    )
    parser.add_argument(
        "--result-path",
        default=(
            "docs/plans/"
            "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase7-numerical-validation-result-2026-07-02.md"
        ),
    )
    parser.add_argument("--no-fail-on-veto", action="store_true")
    args = parser.parse_args()
    args.batch_seeds = _parse_int_csv(args.batch_seeds)
    args.theta_values = _parse_float_csv(args.theta, expected=3)
    args.fd_step_values = _parse_float_csv(args.fd_steps)
    if not all(step > 0.0 for step in args.fd_step_values):
        raise ValueError("FD steps must be positive")
    if args.time_steps <= 0:
        raise ValueError("time-steps must be positive")
    if args.num_particles <= 1:
        raise ValueError("num-particles must be greater than one")
    if args.sinkhorn_iterations <= 0:
        raise ValueError("sinkhorn-iterations must be positive")
    if min(args.row_chunk_size, args.col_chunk_size, args.particle_chunk_size) <= 0:
        raise ValueError("chunk sizes must be positive")
    if args.repeat_atol < 0.0:
        raise ValueError("repeat-atol must be nonnegative")
    if args.hlo_max_factor <= 0.0 or args.compile_timeout_seconds <= 0.0:
        raise ValueError("HLO factor and compile timeout must be positive")
    return args


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def _git_dirty_summary() -> dict[str, Any]:
    try:
        output = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        return {"available": False, "error": repr(exc)}
    lines = [line for line in output.splitlines() if line.strip()]
    return {
        "available": True,
        "dirty": bool(lines),
        "line_count": len(lines),
    }


def _configure_runtime(args: argparse.Namespace) -> dict[str, Any]:
    precision = p8p._configure_precision(  # noqa: SLF001
        argparse.Namespace(dtype=args.dtype, tf32_mode=args.tf32_mode)
    )
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return {
        "precision": precision,
        "physical_gpus": [str(device) for device in physical_gpus],
        "logical_gpus": [str(device) for device in logical_gpus],
    }


def _build_p8p_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=args.batch_seeds,
        time_steps=args.time_steps,
        num_particles=args.num_particles,
        theta_values=args.theta_values,
        transport_policy="active-all",
        sinkhorn_iterations=args.sinkhorn_iterations,
        sinkhorn_epsilon=args.sinkhorn_epsilon,
        annealed_scaling=args.annealed_scaling,
        annealed_convergence_threshold=1.0e-3,
        transport_plan_mode="streaming",
        transport_gradient_mode=core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        transport_ad_mode="full",
        row_chunk_size=args.row_chunk_size,
        col_chunk_size=args.col_chunk_size,
        particle_chunk_size=args.particle_chunk_size,
        dtype=args.dtype,
        tf32_mode=args.tf32_mode,
        device=args.device,
        device_scope="visible",
        cuda_visible_devices=os.environ.get("CUDA_VISIBLE_DEVICES"),
        expect_device_kind=args.expect_device_kind,
        seed_microbatch_size=0,
    )


def _source_anchor(func: Any, needle: str) -> dict[str, Any]:
    source_lines, start_line = inspect.getsourcelines(func)
    path = Path(inspect.getsourcefile(func) or "").resolve()
    for offset, text in enumerate(source_lines):
        if needle in text:
            return {
                "path": str(path.relative_to(ROOT)),
                "symbol": func.__name__,
                "line": start_line + offset,
                "needle": needle,
                "text": text.strip(),
            }
    raise RuntimeError(f"needle not found in {func.__name__}: {needle}")


def _runtime_route_manifest(p8p_args: argparse.Namespace) -> dict[str, Any]:
    selected_full_helper = (
        p8p_args.transport_ad_mode == "full"
        and p8p_args.transport_gradient_mode
        == core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    )
    return {
        "manifest_kind": "runtime_emitted_source_anchored_route_manifest",
        "exact_executed_scalar": True,
        "transport_plan_mode": p8p_args.transport_plan_mode,
        "transport_gradient_mode": p8p_args.transport_gradient_mode,
        "transport_ad_mode": p8p_args.transport_ad_mode,
        "score_route": "manual_reverse_scan_no_autodiff",
        "selected_full_route_helper": (
            "_filterflow_manual_streaming_finite_transport_total_vjp"
            if selected_full_helper
            else None
        ),
        "stopped_key_helper_selected_for_score_evidence": False,
        "stopped_key_helpers_classified_as": "partial_derivative_helpers_not_scores",
        "fd_scalar_route": "same_compiled_manual_value_and_score_function_objective",
        "fd_randomness": "fixed observations, fixed resampling mask, fixed initial particles, fixed stateless transition noise",
        "anchors": [
            _source_anchor(p8p._manual_transport_vjp_tf, 'args.transport_ad_mode == "full"'),
            _source_anchor(
                p8p._manual_transport_vjp_tf,
                "_filterflow_manual_streaming_finite_transport_total_vjp",
            ),
            _source_anchor(p8p._manual_forward_transport_tf, 'args.transport_ad_mode == "full"'),
            _source_anchor(
                p8p._manual_forward_transport_tf,
                "_filterflow_manual_streaming_finite_transport_total_vjp",
            ),
            _source_anchor(
                core_tf.batched_annealed_transport_core_tf,
                "_filterflow_manual_streaming_finite_transport_total_vjp",
            ),
        ],
    }


def _validate_devices(tensors: tuple[tf.Tensor, ...], expect_device_kind: str) -> list[str]:
    devices = [tensor.device for tensor in tensors]
    if expect_device_kind == "gpu" and not all("GPU" in device.upper() for device in devices):
        raise RuntimeError(f"expected GPU outputs, got {devices}")
    if expect_device_kind == "cpu" and not all("CPU" in device.upper() for device in devices):
        raise RuntimeError(f"expected CPU outputs, got {devices}")
    return devices


def _hlo_metrics(hlo_text: str) -> dict[str, Any]:
    lowered = hlo_text.lower()
    markers = {
        "while_lower": lowered.count("while"),
        "while_region": hlo_text.count("WhileRegion"),
        "fusion": lowered.count("fusion"),
    }
    return {
        "available": True,
        "text_length": len(hlo_text),
        "line_count": len(hlo_text.splitlines()),
        "markers": markers,
        "has_while_marker": markers["while_lower"] > 0 or markers["while_region"] > 0,
    }


def _to_float_list(value: tf.Tensor) -> list[float]:
    return [float(item) for item in tf.reshape(value, [-1]).numpy().tolist()]


def _to_float_matrix(value: tf.Tensor) -> list[list[float]]:
    tensor = tf.convert_to_tensor(value)
    if tensor.shape.rank != 2:
        raise ValueError("expected rank-2 tensor")
    return [[float(item) for item in row] for row in tensor.numpy().tolist()]


def _finite_outputs(outputs: tuple[tf.Tensor, ...]) -> bool:
    checks = [tf.reduce_all(tf.math.is_finite(item)) for item in outputs]
    return bool(tf.reduce_all(tf.stack(checks)).numpy())


def _max_abs_delta(left: tf.Tensor, right: tf.Tensor) -> float:
    return float(tf.reduce_max(tf.abs(tf.convert_to_tensor(left) - tf.convert_to_tensor(right))).numpy())


def _fd_tolerance(fd_value: float, fd_mcse: float | None, args: argparse.Namespace) -> float:
    if fd_mcse is not None and math.isfinite(fd_mcse):
        return float(2.0 * fd_mcse)
    return float(args.fd_absolute_floor + args.fd_relative_factor * max(1.0, abs(fd_value)))


def _same_scalar_fd_sentinel(
    *,
    compiled: Any,
    theta0: tf.Tensor,
    gradient: tf.Tensor,
    args: argparse.Namespace,
) -> dict[str, Any]:
    directions = tf.eye(len(PARAMETER_NAMES), dtype=p8p.DTYPE)
    direction_results: list[dict[str, Any]] = []
    all_pass = True
    for index, direction in enumerate(tf.unstack(directions, axis=1)):
        direction_name = PARAMETER_NAMES[index]
        analytic = tf.reduce_sum(gradient * direction)
        analytic_value = float(analytic.numpy())
        step_results: list[dict[str, Any]] = []
        sign_guard_pass = True
        tolerance_pass_any = False
        finite_all = math.isfinite(analytic_value)
        for step in sorted([float(item) for item in args.fd_step_values], reverse=True):
            step_tensor = tf.constant(step, dtype=p8p.DTYPE)
            theta_plus = theta0 + step_tensor * direction
            theta_minus = theta0 - step_tensor * direction
            plus_objective, plus_loglik, _plus_gradient, _plus_per_seed = compiled(theta_plus)
            minus_objective, minus_loglik, _minus_gradient, _minus_per_seed = compiled(theta_minus)
            central_per_seed = (plus_loglik - minus_loglik) / tf.constant(2.0 * step, dtype=p8p.DTYPE)
            central = tf.reduce_mean(central_per_seed)
            central_value = float(central.numpy())
            if int(central_per_seed.shape[0]) > 1:
                centered = central_per_seed - central
                variance = tf.reduce_sum(tf.square(centered)) / tf.cast(
                    int(central_per_seed.shape[0]) - 1,
                    p8p.DTYPE,
                )
                fd_mcse = float(
                    (tf.sqrt(tf.maximum(variance, tf.constant(0.0, p8p.DTYPE)))
                     / tf.sqrt(tf.cast(int(central_per_seed.shape[0]), p8p.DTYPE))).numpy()
                )
            else:
                fd_mcse = None
            abs_error = abs(analytic_value - central_value)
            tolerance = _fd_tolerance(central_value, fd_mcse, args)
            step_pass = bool(abs_error <= tolerance)
            tolerance_pass_any = tolerance_pass_any or step_pass
            if (
                abs(analytic_value) >= float(args.fd_analytic_sign_threshold)
                and math.isfinite(central_value)
                and central_value != 0.0
                and analytic_value * central_value < 0.0
            ):
                sign_guard_pass = False
            finite = bool(
                math.isfinite(central_value)
                and math.isfinite(abs_error)
                and _finite_outputs((plus_objective, plus_loglik, minus_objective, minus_loglik))
            )
            finite_all = finite_all and finite
            step_results.append(
                {
                    "fd_step": step,
                    "plus_objective": float(plus_objective.numpy()),
                    "minus_objective": float(minus_objective.numpy()),
                    "central_difference": central_value,
                    "central_difference_per_seed": _to_float_list(central_per_seed),
                    "fd_mcse": fd_mcse,
                    "absolute_error": abs_error,
                    "tolerance": tolerance,
                    "pass": step_pass,
                    "finite": finite,
                }
            )
        direction_pass = bool(finite_all and tolerance_pass_any and sign_guard_pass)
        all_pass = all_pass and direction_pass
        direction_results.append(
            {
                "basis_name": "raw_theta",
                "direction_name": direction_name,
                "direction_original_theta": _to_float_list(direction),
                "analytic_directional_derivative": analytic_value,
                "fd_steps": step_results,
                "tolerance_pass_any_step": bool(tolerance_pass_any),
                "sign_guard_threshold": float(args.fd_analytic_sign_threshold),
                "sign_guard_pass": bool(sign_guard_pass),
                "finite_all_steps": bool(finite_all),
                "pass": direction_pass,
            }
        )
    return {
        "rule": {
            "statistic": "directional_derivative_of_exact_executed_scalar",
            "analytic": "reported_full_route_mean_score_dot_direction",
            "finite_difference": "central_difference_same_compiled_scalar_fixed_randomness",
            "step_adjudication": (
                "at least one predeclared step passes and no tested larger-neighborhood "
                "step has opposite sign when analytic magnitude is at least threshold"
            ),
            "fallback_tolerance": (
                f"{args.fd_absolute_floor} + {args.fd_relative_factor} * max(1, abs(fd_value))"
            ),
            "mcse_tolerance": "2 * fd_mcse when fd_mcse is emitted",
        },
        "fd_steps": [float(item) for item in args.fd_step_values],
        "directions": direction_results,
        "pass": bool(all_pass),
    }


def main() -> None:
    args = _parse_args()
    runtime = _configure_runtime(args)
    p8p_args = _build_p8p_args(args)
    if p8p_args.transport_ad_mode != "full":
        raise RuntimeError("Phase 7 must run transport_ad_mode='full'")
    if p8p_args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise RuntimeError("Phase 7 must run the manual streaming finite transport mode")
    tensors, sir_semantics = p8p._build_base_tensors(p8p_args)  # noqa: SLF001
    route_manifest = _runtime_route_manifest(p8p_args)
    theta0 = tf.constant(args.theta_values, dtype=p8p.DTYPE)

    @tf.function(
        jit_compile=True,
        reduce_retracing=True,
        input_signature=[tf.TensorSpec([3], dtype=p8p.DTYPE)],
    )
    def compiled(theta_vector: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
        theta_components = (theta_vector[0], theta_vector[1], theta_vector[2])
        with tf.device(args.device):
            diagnostic = p8p._manual_value_and_score_from_components(  # noqa: SLF001
                tensors,
                p8p_args,
                theta_components,
            )
        return (
            diagnostic["objective"],
            diagnostic["log_likelihood"],
            diagnostic["gradient_tensor"],
            diagnostic["per_seed_gradient"],
        )

    wall_start = time.perf_counter()
    first_start = time.perf_counter()
    first_outputs = compiled(theta0)
    for item in first_outputs:
        _ = item.numpy()
    first_seconds = time.perf_counter() - first_start

    warm_a_start = time.perf_counter()
    warm_a_outputs = compiled(tf.identity(theta0))
    for item in warm_a_outputs:
        _ = item.numpy()
    warm_a_seconds = time.perf_counter() - warm_a_start

    warm_b_start = time.perf_counter()
    warm_b_outputs = compiled(tf.identity(theta0))
    for item in warm_b_outputs:
        _ = item.numpy()
    warm_b_seconds = time.perf_counter() - warm_b_start

    hlo_start = time.perf_counter()
    hlo_text = compiled.experimental_get_compiler_ir(theta0)(stage="hlo")
    hlo_seconds = time.perf_counter() - hlo_start
    hlo = _hlo_metrics(hlo_text)

    fd_start = time.perf_counter()
    fd = _same_scalar_fd_sentinel(
        compiled=compiled,
        theta0=theta0,
        gradient=warm_a_outputs[2],
        args=args,
    )
    fd_seconds = time.perf_counter() - fd_start
    wall_seconds = time.perf_counter() - wall_start

    output_devices = _validate_devices(warm_a_outputs, args.expect_device_kind)
    warm_b_devices = _validate_devices(warm_b_outputs, args.expect_device_kind)
    finite_outputs = _finite_outputs(warm_a_outputs)
    repeat = {
        "protocol": "same_process_warm_call_same_concrete_signature",
        "repeat_atol": float(args.repeat_atol),
        "objective_max_abs_delta": _max_abs_delta(warm_a_outputs[0], warm_b_outputs[0]),
        "log_likelihood_max_abs_delta": _max_abs_delta(warm_a_outputs[1], warm_b_outputs[1]),
        "mean_gradient_max_abs_delta": _max_abs_delta(warm_a_outputs[2], warm_b_outputs[2]),
        "per_seed_gradient_max_abs_delta": _max_abs_delta(warm_a_outputs[3], warm_b_outputs[3]),
    }
    repeat["pass"] = bool(
        repeat["objective_max_abs_delta"] <= args.repeat_atol
        and repeat["log_likelihood_max_abs_delta"] <= args.repeat_atol
        and repeat["mean_gradient_max_abs_delta"] <= args.repeat_atol
        and repeat["per_seed_gradient_max_abs_delta"] <= args.repeat_atol
    )

    same_phase6_hlo_fixture = bool(
        args.time_steps == 1
        and args.num_particles == 16
        and args.sinkhorn_iterations == 2
    )
    hlo_limit = int(math.ceil(args.hlo_baseline_text_length * args.hlo_max_factor))
    hlo_watchpoint = {
        "phase6_baseline_field": "hlo_text_length",
        "phase6_baseline_text_length": int(args.hlo_baseline_text_length),
        "max_factor": float(args.hlo_max_factor),
        "limit_text_length": hlo_limit,
        "same_T_N_sinkhorn_iteration_fixture": same_phase6_hlo_fixture,
        "compile_timeout_seconds": float(args.compile_timeout_seconds),
        "compile_plus_first_call_seconds": first_seconds,
        "hlo_text_length": hlo["text_length"],
        "pass": bool(
            first_seconds <= args.compile_timeout_seconds
            and (
                not same_phase6_hlo_fixture
                or hlo["text_length"] <= hlo_limit
            )
        ),
    }
    concrete_function_count = len(compiled._list_all_concrete_functions_for_serialization())
    route_pass = bool(
        route_manifest["selected_full_route_helper"]
        == "_filterflow_manual_streaming_finite_transport_total_vjp"
        and not route_manifest["stopped_key_helper_selected_for_score_evidence"]
    )
    primary_pass = bool(
        finite_outputs
        and route_pass
        and repeat["pass"]
        and fd["pass"]
        and hlo_watchpoint["pass"]
    )

    result = {
        "schema_version": "ledh_clean_xla_phase7_numerical_validation.v1",
        "timestamp_utc": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "tensorflow_version": tf.__version__,
        "git_commit": _git_commit(),
        "git_dirty_summary": _git_dirty_summary(),
        "command": " ".join([sys.executable, *sys.argv]),
        "environment": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "TF_CPP_MIN_LOG_LEVEL": os.environ.get("TF_CPP_MIN_LOG_LEVEL"),
        },
        "cpu_gpu_status": {
            "expect_device_kind": args.expect_device_kind,
            "physical_gpus": runtime["physical_gpus"],
            "logical_gpus": runtime["logical_gpus"],
            "output_devices": output_devices,
            "repeat_output_devices": warm_b_devices,
        },
        "precision": runtime["precision"],
        "route_config": {
            "transport_plan_mode": p8p_args.transport_plan_mode,
            "transport_gradient_mode": p8p_args.transport_gradient_mode,
            "transport_ad_mode": p8p_args.transport_ad_mode,
            "sinkhorn_iterations": p8p_args.sinkhorn_iterations,
            "sinkhorn_epsilon": p8p_args.sinkhorn_epsilon,
            "annealed_scaling": p8p_args.annealed_scaling,
            "row_chunk_size": p8p_args.row_chunk_size,
            "col_chunk_size": p8p_args.col_chunk_size,
            "particle_chunk_size": p8p_args.particle_chunk_size,
        },
        "shape": {
            "batch_size": len(args.batch_seeds),
            "time_steps": args.time_steps,
            "num_particles": args.num_particles,
            "state_dim": 18,
            "parameter_dim": 3,
        },
        "random_seeds": {"batch_seeds": args.batch_seeds},
        "theta": dict(zip(PARAMETER_NAMES, args.theta_values, strict=True)),
        "sir_semantics": sir_semantics,
        "runtime_route_manifest": route_manifest,
        "compiler": {
            "jit_compile": True,
            "cold_compile_plus_first_call_seconds": first_seconds,
            "same_process_warm_call_a_seconds": warm_a_seconds,
            "same_process_warm_call_b_seconds": warm_b_seconds,
            "fd_sentinel_seconds": fd_seconds,
            "hlo_retrieval_seconds": hlo_seconds,
            "wall_seconds": wall_seconds,
            "concrete_function_count": concrete_function_count,
            "unexpected_retrace": concrete_function_count != 1,
            "hlo": hlo,
            "hlo_watchpoint": hlo_watchpoint,
        },
        "outputs": {
            "objective": float(warm_a_outputs[0].numpy()),
            "log_likelihood": _to_float_list(warm_a_outputs[1]),
            "gradient": _to_float_list(warm_a_outputs[2]),
            "per_seed_gradient": _to_float_matrix(warm_a_outputs[3]),
            "finite": finite_outputs,
        },
        "repeat_determinism": repeat,
        "same_scalar_fd_sentinel": fd,
        "monte_carlo_gradient_noise": p8p._mc_noise_summary(warm_a_outputs[3]),  # noqa: SLF001
        "route_pass": route_pass,
        "plan_path": args.plan_path,
        "result_path": args.result_path,
        "output_path": args.output,
        "primary_pass": primary_pass,
        "decision": "PASS_PHASE7_NUMERICAL_VALIDATION" if primary_pass else "FAIL_PHASE7_NUMERICAL_VALIDATION",
        "nonclaims": [
            "bounded trusted GPU/XLA full-route fixture only",
            "same-scalar FD sentinel only",
            "not exact nonlinear likelihood proof",
            "not posterior correctness evidence",
            "not HMC readiness evidence",
            "not all-model validation",
            "not broad production readiness",
            "stopped-key partial derivatives are not scores",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not primary_pass and not args.no_fail_on_veto:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
