"""Tiny SIR active-transport total-derivative diagnostic.

This diagnostic separates three mathematical objects:

1. the stabilized/stopped-gradient active-transport score used by the manual
   reverse route;
2. the manual total-derivative finite-Sinkhorn route; and
3. the derivative of that same finite-Sinkhorn value, measured by finite
   differences and TensorFlow tape with ``transport_ad_mode='full'``.

It is CPU-only float64 local evidence.  It is not material GPU/TF32 evidence
and it does not certify SIR gradient correctness or HMC readiness.
"""

from __future__ import annotations

import argparse
import copy
import datetime as _dt
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any


_PRE_PARSER = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE_PARSER.add_argument("--device-scope", choices=("cpu",), default="cpu")
_PRE_ARGS, _UNKNOWN = _PRE_PARSER.parse_known_args()
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf

from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p


DEFAULT_MANUAL_TAPE_ATOL = 1.0e-8
DEFAULT_FD_TAPE_ATOL = 1.0e-4
DEFAULT_NO_RESAMPLING_FD_ATOL = 1.0e-4
DEFAULT_ACTIVE_GAP_MIN = 1.0

NONCLAIMS = (
    "CPU float64 tiny comparator-contract diagnostic only",
    "not material GPU/TF32 evidence",
    "tiny SIR total-derivative score repair check only",
    "not HMC readiness",
    "not posterior correctness",
    "not production/default-policy change",
)


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
    parser.add_argument("--batch-seeds", default="81120,81121,81122")
    parser.add_argument("--time-steps", type=int, default=3)
    parser.add_argument("--num-particles", type=int, default=3)
    parser.add_argument("--theta", default="0.02,-0.01,0.01")
    parser.add_argument("--fd-step", type=float, default=1.0e-5)
    parser.add_argument("--sinkhorn-iterations", type=int, default=5)
    parser.add_argument("--sinkhorn-epsilon", type=float, default=1.0)
    parser.add_argument("--annealed-scaling", type=float, default=0.9)
    parser.add_argument("--annealed-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument("--manual-tape-atol", type=float, default=DEFAULT_MANUAL_TAPE_ATOL)
    parser.add_argument("--fd-tape-atol", type=float, default=DEFAULT_FD_TAPE_ATOL)
    parser.add_argument("--no-resampling-fd-atol", type=float, default=DEFAULT_NO_RESAMPLING_FD_ATOL)
    parser.add_argument("--active-gap-min", type=float, default=DEFAULT_ACTIVE_GAP_MIN)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    args.batch_seeds = _parse_int_csv(args.batch_seeds)
    args.theta_values = _parse_float_csv(args.theta, expected=3)
    if args.time_steps <= 0:
        raise ValueError("time-steps must be positive")
    if args.num_particles <= 1:
        raise ValueError("num-particles must be greater than one")
    if args.fd_step <= 0.0:
        raise ValueError("fd-step must be positive")
    if args.sinkhorn_iterations <= 0:
        raise ValueError("sinkhorn-iterations must be positive")
    if args.sinkhorn_epsilon <= 0.0:
        raise ValueError("sinkhorn-epsilon must be positive")
    if not 0.0 < args.annealed_scaling <= 1.0:
        raise ValueError("annealed-scaling must be in (0, 1]")
    for name in ("manual_tape_atol", "fd_tape_atol", "no_resampling_fd_atol", "active_gap_min"):
        if getattr(args, name) < 0.0:
            raise ValueError(f"{name} must be nonnegative")
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


def _base_route_args(args: argparse.Namespace, *, transport_policy: str) -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=list(args.batch_seeds),
        time_steps=int(args.time_steps),
        num_particles=int(args.num_particles),
        theta_values=list(args.theta_values),
        transport_policy=transport_policy,
        sinkhorn_iterations=int(args.sinkhorn_iterations),
        sinkhorn_epsilon=float(args.sinkhorn_epsilon),
        annealed_scaling=float(args.annealed_scaling),
        annealed_convergence_threshold=float(args.annealed_convergence_threshold),
        transport_plan_mode="streaming",
        transport_gradient_mode=p8p.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        transport_ad_mode="stabilized",
        row_chunk_size=int(args.num_particles),
        col_chunk_size=int(args.num_particles),
        particle_chunk_size=int(args.num_particles),
        dtype="float64",
        tf32_mode="disabled",
        device="/CPU:0",
        device_scope="cpu",
        cuda_visible_devices=None,
        expect_device_kind="cpu",
        output="/tmp/not-written.json",
        fd_step=float(args.fd_step),
        fd_step_ladder_values=[float(args.fd_step)],
        repeat_evaluations=1,
        repeat_atol=1.0e-8,
        theta_zero_parity_atol=1.0e-8,
        diagnostic_components="all",
        check_isolated_observation_noise=False,
        check_theta_zero_p8j_parity=False,
        no_fail_on_veto=True,
    )


def _gradient_tape_objective_only(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> tuple[tf.Tensor, tf.Tensor]:
    theta_components = p8p._theta_components(args.theta_values)
    with tf.GradientTape() as tape:
        for component in theta_components:
            tape.watch(component)
        objective, _value = p8p._objective_from_components(tensors, args, theta_components)
    gradients = tape.gradient(objective, theta_components)
    gradient_values = [
        tf.constant(float("nan"), dtype=p8p.DTYPE) if gradient is None else gradient
        for gradient in gradients
    ]
    return objective, tf.stack(gradient_values)


def _fd_gradient(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> tf.Tensor:
    fd = p8p._finite_difference_diagnostic(tensors, args, args.theta_values)
    return tf.constant([float(item["central_difference"]) for item in fd], dtype=p8p.DTYPE)


def _max_abs(lhs: tf.Tensor, rhs: tf.Tensor) -> float:
    return float(tf.reduce_max(tf.abs(tf.convert_to_tensor(lhs) - tf.convert_to_tensor(rhs))).numpy())


def _to_float_list(value: tf.Tensor) -> list[float]:
    return [float(item) for item in tf.convert_to_tensor(value).numpy().tolist()]


def _to_float_matrix(value: tf.Tensor) -> list[list[float]]:
    return [
        [float(item) for item in row]
        for row in tf.convert_to_tensor(value).numpy().tolist()
    ]


def _run_policy(args: argparse.Namespace, *, transport_policy: str) -> dict[str, Any]:
    route_args = _base_route_args(args, transport_policy=transport_policy)
    p8p._configure_precision(route_args)
    tensors, _semantics = p8p._build_base_tensors(route_args)

    stopped_manual = p8p._manual_gradient_diagnostic(
        tensors,
        route_args,
        route_args.theta_values,
    )
    stopped_objective, stopped_tape = _gradient_tape_objective_only(tensors, route_args)
    literal_fd = _fd_gradient(tensors, route_args)

    total_args = copy.copy(route_args)
    total_args.transport_ad_mode = "full"
    total_manual = p8p._manual_gradient_diagnostic(
        tensors,
        total_args,
        total_args.theta_values,
    )
    total_objective, total_tape = _gradient_tape_objective_only(tensors, total_args)
    total_fd = _fd_gradient(tensors, total_args)

    raw_full_args = copy.copy(route_args)
    raw_full_args.transport_gradient_mode = "raw"
    raw_full_args.transport_ad_mode = "full"
    raw_full_objective, raw_full_tape = _gradient_tape_objective_only(tensors, raw_full_args)
    raw_full_fd = _fd_gradient(tensors, raw_full_args)

    stopped_gradient = tf.convert_to_tensor(stopped_manual["gradient_tensor"], dtype=p8p.DTYPE)
    stopped_per_seed = tf.convert_to_tensor(stopped_manual["per_seed_gradient"], dtype=p8p.DTYPE)
    total_gradient = tf.convert_to_tensor(total_manual["gradient_tensor"], dtype=p8p.DTYPE)
    total_per_seed = tf.convert_to_tensor(total_manual["per_seed_gradient"], dtype=p8p.DTYPE)
    stopped_gap = _max_abs(stopped_gradient, stopped_tape)
    total_vs_tape_gap = _max_abs(total_gradient, total_tape)
    total_vs_fd_gap = _max_abs(total_gradient, total_fd)
    literal_gap = _max_abs(total_tape, total_fd)
    raw_full_literal_gap = _max_abs(raw_full_tape, raw_full_fd)
    stopped_vs_literal_gap = _max_abs(stopped_gradient, literal_fd)
    no_resampling_fd_gap = _max_abs(total_gradient, literal_fd)

    manual_tape_pass = stopped_gap <= args.manual_tape_atol
    total_tape_pass = total_vs_tape_gap <= args.manual_tape_atol
    total_fd_pass = total_vs_fd_gap <= args.fd_tape_atol
    full_fd_pass = literal_gap <= args.fd_tape_atol
    if transport_policy == "no-resampling":
        policy_pass = (
            total_tape_pass
            and full_fd_pass
            and total_fd_pass
            and no_resampling_fd_gap <= args.no_resampling_fd_atol
        )
    else:
        policy_pass = (
            total_tape_pass
            and full_fd_pass
            and total_fd_pass
        )

    return {
        "transport_policy": transport_policy,
        "objective_stopped_route": float(stopped_manual["objective"].numpy()),
        "objective_stopped_tape": float(stopped_objective.numpy()),
        "objective_manual_total_route": float(total_manual["objective"].numpy()),
        "objective_manual_total_tape": float(total_objective.numpy()),
        "objective_raw_full": float(raw_full_objective.numpy()),
        "manual_stopped_gradient": _to_float_list(stopped_gradient),
        "manual_total_gradient": _to_float_list(total_gradient),
        "tensorflow_tape_stopped_gradient": _to_float_list(stopped_tape),
        "literal_fd_gradient_stopped_route_value": _to_float_list(literal_fd),
        "tensorflow_tape_manual_total_gradient": _to_float_list(total_tape),
        "literal_fd_manual_total_gradient": _to_float_list(total_fd),
        "tensorflow_tape_raw_full_gradient": _to_float_list(raw_full_tape),
        "literal_fd_raw_full_gradient": _to_float_list(raw_full_fd),
        "per_seed_manual_stopped_gradient": _to_float_matrix(stopped_per_seed),
        "per_seed_manual_total_gradient": _to_float_matrix(total_per_seed),
        "manual_vs_stopped_tape_max_abs": stopped_gap,
        "manual_total_vs_tape_max_abs": total_vs_tape_gap,
        "manual_total_vs_raw_full_tape_max_abs": _max_abs(total_gradient, raw_full_tape),
        "manual_total_vs_literal_fd_max_abs": total_vs_fd_gap,
        "manual_total_tape_vs_literal_fd_max_abs": literal_gap,
        "raw_full_tape_vs_literal_fd_max_abs": raw_full_literal_gap,
        "manual_stopped_vs_literal_fd_max_abs": stopped_vs_literal_gap,
        "manual_tape_pass": bool(manual_tape_pass),
        "manual_total_tape_pass": bool(total_tape_pass),
        "manual_total_fd_pass": bool(total_fd_pass),
        "raw_full_fd_pass": bool(full_fd_pass),
        "policy_pass": bool(policy_pass),
        "interpretation": (
            "no_resampling_total_derivative_matches_literal_fd"
            if transport_policy == "no-resampling"
            else "active_transport_manual_total_derivative_matches_literal_fd"
        ),
    }


def run_diagnostic(args: argparse.Namespace) -> dict[str, Any]:
    route_for_precision = _base_route_args(args, transport_policy="no-resampling")
    precision = p8p._configure_precision(route_for_precision)
    policies = [
        _run_policy(args, transport_policy="no-resampling"),
        _run_policy(args, transport_policy="active-all"),
    ]
    passed = all(bool(policy["policy_pass"]) for policy in policies)
    failure_reasons: list[str] = []
    for policy in policies:
        if not policy["manual_tape_pass"]:
            failure_reasons.append(f"{policy['transport_policy']}: stopped manual route differs from same-route tape")
        if not policy["manual_total_tape_pass"]:
            failure_reasons.append(f"{policy['transport_policy']}: manual total route differs from same finite-route tape")
        if not policy["manual_total_fd_pass"]:
            failure_reasons.append(f"{policy['transport_policy']}: manual total route differs from literal FD")
        if not policy["raw_full_fd_pass"]:
            failure_reasons.append(f"{policy['transport_policy']}: raw/full tape differs from literal FD")
        if not policy["policy_pass"]:
            failure_reasons.append(f"{policy['transport_policy']}: policy-specific comparator contract failed")
    return {
        "schema_version": "filter_bench.p8p_sir_active_transport_comparator_contract.v1",
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_version": platform.python_version(),
        "tensorflow_version": tf.__version__,
        "git_commit": _git_commit(),
        "status": "PASS" if passed else "FAIL",
        "passed": bool(passed),
        "failure_reasons": failure_reasons,
        "environment": {
            "device_scope": "cpu",
            "visible_cuda_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "precision": precision,
            "intentional_cpu_only": True,
        },
        "shape": {
            "batch_size": len(args.batch_seeds),
            "time_steps": int(args.time_steps),
            "num_particles": int(args.num_particles),
            "state_dim": 18,
            "obs_dim": 9,
        },
        "theta": dict(
            zip(p8p.PARAMETER_NAMES, [float(item) for item in args.theta_values], strict=True)
        ),
        "batch_seeds": [int(seed) for seed in args.batch_seeds],
        "finite_difference_step": float(args.fd_step),
        "tolerances": {
            "manual_tape_atol": float(args.manual_tape_atol),
            "fd_tape_atol": float(args.fd_tape_atol),
            "no_resampling_fd_atol": float(args.no_resampling_fd_atol),
            "active_gap_min": float(args.active_gap_min),
        },
        "policies": policies,
        "decision": (
            "The active-transport manual total route agrees with same finite-route "
            "tape and literal FD for this tiny CPU float64 diagnostic.  The old "
            "stopped route remains a partial derivative and is not the score."
            if passed
            else "Comparator-contract diagnostic failed; inspect failure_reasons."
        ),
        "nonclaims": list(NONCLAIMS),
    }


def main() -> None:
    args = _parse_args()
    payload = run_diagnostic(args)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    if not payload["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
