#!/usr/bin/env python
"""Collect Phase 6 GPU/XLA compiler metrics for the LEDH-PFPF-OT full route."""

from __future__ import annotations

import argparse
import datetime as dt
import inspect
import json
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


PARAMETER_NAMES = ("log_kappa_scale", "log_nu_scale", "log_obs_noise_scale")


def _parse_int_csv(value: str) -> list[int]:
    parsed = [int(item.strip()) for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one seed")
    return parsed


def _parse_float_csv(value: str, *, expected: int) -> list[float]:
    parsed = [float(item.strip()) for item in str(value).split(",") if item.strip()]
    if len(parsed) != expected:
        raise ValueError(f"expected {expected} comma-separated floats")
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
    parser.add_argument("--sinkhorn-iterations", type=int, default=2)
    parser.add_argument("--sinkhorn-epsilon", type=float, default=1.0)
    parser.add_argument("--annealed-scaling", type=float, default=0.9)
    parser.add_argument("--row-chunk-size", type=int, default=16)
    parser.add_argument("--col-chunk-size", type=int, default=16)
    parser.add_argument("--particle-chunk-size", type=int, default=16)
    parser.add_argument("--dtype", choices=("float32", "float64"), default="float32")
    parser.add_argument("--tf32-mode", choices=("enabled", "disabled", "default"), default="enabled")
    parser.add_argument(
        "--plan-path",
        default=(
            "docs/plans/"
            "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-subplan-2026-07-02.md"
        ),
    )
    parser.add_argument(
        "--result-path",
        default=(
            "docs/plans/"
            "bayesfilter-ledh-pfpf-ot-clean-xla-jit-phase6-compiler-metrics-gate-result-2026-07-02.md"
        ),
    )
    args = parser.parse_args()
    args.batch_seeds = _parse_int_csv(args.batch_seeds)
    args.theta_values = _parse_float_csv(args.theta, expected=3)
    if args.time_steps <= 0:
        raise ValueError("time-steps must be positive")
    if args.num_particles <= 1:
        raise ValueError("num-particles must be greater than one")
    if args.sinkhorn_iterations <= 0:
        raise ValueError("sinkhorn-iterations must be positive")
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
    p8p_args = argparse.Namespace(
        dtype=args.dtype,
        tf32_mode=args.tf32_mode,
    )
    precision = p8p._configure_precision(p8p_args)  # noqa: SLF001
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


def _route_call_path_evidence() -> dict[str, Any]:
    return {
        "route_kind": "source_anchored_static_call_path_for_compiled_fixture",
        "full_route_required": True,
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
        "negative_control": (
            "stopped-key helpers are present only on non-full/stabilized branches "
            "and are not score evidence"
        ),
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


def main() -> None:
    args = _parse_args()
    runtime = _configure_runtime(args)
    p8p_args = _build_p8p_args(args)
    if p8p_args.transport_ad_mode != "full":
        raise RuntimeError("Phase 6 must run transport_ad_mode='full'")
    if p8p_args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise RuntimeError("Phase 6 must run the manual streaming finite transport mode")
    tensors, sir_semantics = p8p._build_base_tensors(p8p_args)  # noqa: SLF001
    route_evidence = _route_call_path_evidence()
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
    objective, log_likelihood, gradient, per_seed_gradient = compiled(theta0)
    first_seconds = time.perf_counter() - first_start
    warm_start = time.perf_counter()
    warm_outputs = compiled(tf.identity(theta0))
    warm_seconds = time.perf_counter() - warm_start
    hlo_start = time.perf_counter()
    hlo_text = compiled.experimental_get_compiler_ir(theta0)(stage="hlo")
    hlo_seconds = time.perf_counter() - hlo_start
    wall_seconds = time.perf_counter() - wall_start

    output_devices = _validate_devices(
        (objective, log_likelihood, gradient, per_seed_gradient),
        args.expect_device_kind,
    )
    warm_devices = _validate_devices(warm_outputs, args.expect_device_kind)
    finite_outputs = bool(
        tf.reduce_all(
            tf.stack(
                [
                    tf.reduce_all(tf.math.is_finite(objective)),
                    tf.reduce_all(tf.math.is_finite(log_likelihood)),
                    tf.reduce_all(tf.math.is_finite(gradient)),
                    tf.reduce_all(tf.math.is_finite(per_seed_gradient)),
                ]
            )
        ).numpy()
    )
    concrete_function_count = len(compiled._list_all_concrete_functions_for_serialization())
    hlo = _hlo_metrics(hlo_text)
    primary_pass = bool(
        finite_outputs
        and output_devices
        and warm_devices
        and hlo["has_while_marker"]
        and concrete_function_count == 1
    )

    result = {
        "schema_version": "ledh_clean_xla_phase6_compiler_metrics.v1",
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
            "warm_output_devices": warm_devices,
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
        "route_call_path_evidence": route_evidence,
        "compiler": {
            "jit_compile": True,
            "cold_compile_plus_first_call_seconds": first_seconds,
            "warm_call_seconds": warm_seconds,
            "hlo_retrieval_seconds": hlo_seconds,
            "wall_seconds": wall_seconds,
            "concrete_function_count": concrete_function_count,
            "unexpected_retrace": concrete_function_count != 1,
            "hlo": hlo,
        },
        "outputs": {
            "objective": float(objective.numpy()),
            "log_likelihood": _to_float_list(log_likelihood),
            "gradient": _to_float_list(gradient),
            "per_seed_gradient": [row for row in tf.convert_to_tensor(per_seed_gradient).numpy().tolist()],
            "finite": finite_outputs,
        },
        "plan_path": args.plan_path,
        "result_path": args.result_path,
        "output_path": args.output,
        "primary_pass": primary_pass,
        "decision": "PASS_TINY_FULL_ROUTE_GPU_XLA_COMPILER_METRICS" if primary_pass else "FAIL_PHASE6_COMPILER_METRICS",
        "nonclaims": [
            "tiny trusted GPU/XLA full-route fixture only",
            "not FD correctness evidence",
            "not statistical validity evidence",
            "not HMC readiness evidence",
            "not broad production readiness",
            "stopped-key partial derivatives are not scores",
        ],
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not primary_pass:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
