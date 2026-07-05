"""Focused worst-time LEDH-PFPF-OT LGSSM transport budget diagnostic.

This script follows the same LGSSM fixture as
``diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments.py`` but narrows the question:
on the clouds that produced the largest high-budget row residuals in the
step-ladder fallback, do larger finite Sinkhorn budgets clear the row-marginal
diagnostic?

It is diagnostic only.  It does not certify gradients, SIR correctness, HMC
readiness, posterior correctness, production readiness, GPU/XLA performance,
or broad scientific validity.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import platform
import sys
import time
from pathlib import Path
from typing import Any

import diagnose_ledh_pfpf_ot_lgssm_ot_reset_moments as base


ROOT = base.ROOT
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-lgssm-worst-time-budget-diagnostic-plan-2026-06-26.md"
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--num-particles", type=int, default=128)
    parser.add_argument("--dense-parity-particles", type=int, default=128)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--state-dims", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--candidate-steps", type=int, nargs="+", default=[100, 200, 400])
    parser.add_argument("--baseline-steps", type=int, default=100)
    parser.add_argument("--epsilon", type=float, default=0.5)
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
    parser.add_argument("--cuda-visible-devices", default="0")
    parser.set_defaults(xla=False)
    parser.add_argument("--tf32-mode", choices=("enabled", "disabled"), default="enabled")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default=None)
    args = parser.parse_args()
    if args.num_particles <= 1:
        raise ValueError("--num-particles must be greater than one")
    if args.dense_parity_particles <= 1:
        raise ValueError("--dense-parity-particles must be greater than one")
    if args.dense_parity_particles > args.num_particles:
        raise ValueError("--dense-parity-particles cannot exceed --num-particles")
    if args.seed_count != 10:
        raise ValueError("this diagnostic reuses the harness SEED_COUNT=10 contract")
    if any(dim not in (1, 2) for dim in args.state_dims):
        raise ValueError("--state-dims currently supports only 1 and 2")
    if args.baseline_steps <= 0 or any(step <= 0 for step in args.candidate_steps):
        raise ValueError("finite step counts must be positive")
    if args.epsilon <= 0.0:
        raise ValueError("--epsilon must be positive")
    return args


def _target_time(state_dim: int) -> int:
    if state_dim == 1:
        return 8
    if state_dim == 2:
        return 7
    raise ValueError(f"unsupported state_dim={state_dim}")


def _weighted_moments(tf: Any, points: Any, weights: Any) -> tuple[Any, Any]:
    mean = tf.reduce_sum(weights[:, :, None] * points, axis=1)
    centered = points - mean[:, None, :]
    covariance = tf.einsum("bn,bni,bnj->bij", weights, centered, centered)
    return mean, covariance


def _uniform_moments(tf: Any, dtype: Any, points: Any) -> tuple[Any, Any]:
    count = tf.cast(tf.shape(points)[1], dtype)
    weights = tf.fill([tf.shape(points)[0], tf.shape(points)[1]], 1.0 / count)
    return _weighted_moments(tf, points, weights)


def _transport_cloud(
    harness: Any,
    post_flow: Any,
    weights: Any,
    normalized_log_weights: Any,
    *,
    epsilon_value: float,
    steps: int,
    dense_parity_particles: int,
) -> dict[str, Any]:
    tf = harness.tf
    np = harness.np
    annealed = harness.annealed_transport_tf
    dtype = harness.DTYPE
    num_particles = int(post_flow.shape[1])
    epsilon = tf.constant(epsilon_value, dtype=dtype)
    scaling = tf.constant(harness.ANNEALED_SCALING, dtype=dtype)

    center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
    scale = tf.stop_gradient(annealed._filterflow_scale(post_flow))
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
    dense_matrix = (
        annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
            scaled_x,
            normalized_log_weights,
            epsilon,
            epsilon0,
            scaling,
            steps=steps,
        )
    )
    dense_particles = tf.linalg.matmul(dense_matrix, post_flow)
    streaming_particles, streaming_row_residual = (
        annealed._filterflow_manual_streaming_finite_transport_value_stopped_scale_keys(
            scaled_x,
            post_flow,
            normalized_log_weights,
            epsilon,
            epsilon0,
            scaling,
            steps=steps,
            row_chunk_size=num_particles,
            col_chunk_size=num_particles,
        )
    )
    source_weights = tf.exp(normalized_log_weights)
    column_target = source_weights * tf.cast(num_particles, dtype)
    column_mass = tf.reduce_sum(dense_matrix, axis=1)
    dense_row_residual = tf.reduce_max(tf.abs(tf.reduce_sum(dense_matrix, axis=2) - 1.0))
    dense_column_residual = tf.reduce_max(tf.abs(column_mass - column_target))
    max_abs_diff = tf.reduce_max(tf.abs(dense_particles - streaming_particles))
    mean_abs_diff = tf.reduce_mean(tf.abs(dense_particles - streaming_particles))

    subset_x = post_flow[:, :dense_parity_particles, :]
    subset_logw = normalized_log_weights[:, :dense_parity_particles]
    subset_logw = subset_logw - tf.reduce_logsumexp(subset_logw, axis=1, keepdims=True)
    subset_center = tf.stop_gradient(tf.reduce_mean(subset_x, axis=1, keepdims=True))
    subset_scale = tf.stop_gradient(annealed._filterflow_scale(subset_x))
    subset_scaled = (subset_x - subset_center) / subset_scale[:, None, None]
    subset_epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(subset_scaled))
    subset_matrix = (
        annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
            subset_scaled,
            subset_logw,
            epsilon,
            subset_epsilon0,
            scaling,
            steps=steps,
        )
    )
    subset_weights = tf.exp(subset_logw)
    subset_col_target = subset_weights * tf.cast(dense_parity_particles, dtype)
    subset_col_mass = tf.reduce_sum(subset_matrix, axis=1)
    subset_row_residual = tf.reduce_max(
        tf.abs(tf.reduce_sum(subset_matrix, axis=2) - 1.0)
    )
    subset_column_residual = tf.reduce_max(tf.abs(subset_col_mass - subset_col_target))

    pre_mean, pre_covariance = _weighted_moments(tf, post_flow, weights)
    post_mean, post_covariance = _uniform_moments(tf, dtype, dense_particles)
    pre_trace = tf.linalg.trace(pre_covariance)
    post_trace = tf.linalg.trace(post_covariance)
    mean_shift = tf.norm(post_mean - pre_mean, axis=1)

    return {
        "steps": int(steps),
        "dense_row_residual": float(dense_row_residual.numpy()),
        "streaming_row_residual": float(streaming_row_residual.numpy()),
        "dense_column_residual": float(dense_column_residual.numpy()),
        "dense_streaming_max_abs_particle_diff": float(max_abs_diff.numpy()),
        "dense_streaming_mean_abs_particle_diff": float(mean_abs_diff.numpy()),
        "subset_particles": int(dense_parity_particles),
        "subset_dense_row_residual": float(subset_row_residual.numpy()),
        "subset_dense_column_residual": float(subset_column_residual.numpy()),
        "pre_cov_trace_mean": float(np.asarray(pre_trace.numpy()).mean()),
        "post_cov_trace_mean": float(np.asarray(post_trace.numpy()).mean()),
        "post_pre_cov_trace_ratio_mean": float(
            (np.asarray(post_trace.numpy()) / np.asarray(pre_trace.numpy())).mean()
        ),
        "pre_to_post_mean_l2_mean": float(np.asarray(mean_shift.numpy()).mean()),
        "pre_to_post_mean_l2_max": float(np.asarray(mean_shift.numpy()).max()),
    }


def _baseline_transport(
    harness: Any,
    post_flow: Any,
    normalized_log_weights: Any,
    *,
    epsilon_value: float,
    steps: int,
) -> tuple[Any, Any]:
    tf = harness.tf
    annealed = harness.annealed_transport_tf
    core = harness.core_ledh
    dtype = harness.DTYPE
    batch_size = int(post_flow.shape[0])
    num_particles = int(post_flow.shape[1])
    center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
    scale = tf.stop_gradient(annealed._filterflow_scale(post_flow))
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon = tf.constant(epsilon_value, dtype=dtype)
    epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
    transported, _row_residual = (
        annealed._filterflow_manual_streaming_finite_transport_stopped_scale_keys(
            scaled_x,
            post_flow,
            normalized_log_weights,
            epsilon,
            epsilon0,
            tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
            steps=steps,
            row_chunk_size=num_particles,
            col_chunk_size=num_particles,
        )
    )
    return transported, core.uniform_log_weights(batch_size, num_particles)


def _target_cloud(
    harness: Any,
    state_dim: int,
    *,
    target_time: int,
    baseline_steps: int,
    epsilon_value: float,
) -> dict[str, Any]:
    tf = harness.tf
    core = harness.core_ledh
    dtype = harness.DTYPE
    observations = harness._observations(state_dim)
    initial_noise, transition_noise = harness._stateless_seeded_normals_batch(state_dim)
    particles = tf.sqrt(tf.constant(0.7, dtype)) * initial_noise
    theta_batch = tf.tile(harness.THETA[None, :], [harness.SEED_COUNT, 1])
    transition_matrix, transition_covariance, observation_covariance = (
        harness._theta_to_lgssm(theta_batch, state_dim)
    )
    transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
    h_jac = tf.tile(
        tf.eye(state_dim, dtype=dtype)[None, None, :, :],
        [harness.SEED_COUNT, harness.NUM_PARTICLES, 1, 1],
    )
    log_weights = core.uniform_log_weights(harness.SEED_COUNT, harness.NUM_PARTICLES)
    increments = []
    ess_values = []

    for time_index in range(target_time + 1):
        observation = observations[time_index]
        prior_mean = tf.einsum("bnj,bdj->bnd", particles, transition_matrix)
        noise = transition_noise[:, time_index, :, :]
        pre_flow = prior_mean + noise * transition_std[:, None, :]
        residual = observation[None, None, :] - pre_flow
        flow, _flow_aux = core._batched_ledh_linearized_flow_with_aux_tf(
            pre_flow_particles=pre_flow,
            prior_means=prior_mean,
            observation_jacobian=h_jac,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = harness._diag_gaussian_logpdf(
            post_flow - prior_mean,
            transition_covariance,
        )
        observation_log_density = harness._diag_gaussian_logpdf(
            post_flow - observation[None, None, :],
            observation_covariance,
        )
        corrected_log_weights = (
            log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, increment = core._normalize_log_weights(corrected_log_weights)
        normalized_log_weights = tf.math.log(tf.maximum(weights, core._log_weight_floor()))
        increments.append(increment)
        ess_values.append(1.0 / tf.reduce_sum(weights * weights, axis=1))
        if time_index == target_time:
            return {
                "post_flow": post_flow,
                "weights": weights,
                "normalized_log_weights": normalized_log_weights,
                "increments": tf.stack(increments, axis=1),
                "ess": tf.stack(ess_values, axis=1),
                "observations": observations,
            }
        particles, log_weights = _baseline_transport(
            harness,
            post_flow,
            normalized_log_weights,
            epsilon_value=epsilon_value,
            steps=baseline_steps,
        )
    raise RuntimeError("target time was not reached")


def _run_state_dim(harness: Any, state_dim: int, args: argparse.Namespace) -> dict[str, Any]:
    np = harness.np
    target_time = _target_time(state_dim)
    cloud = _target_cloud(
        harness,
        state_dim,
        target_time=target_time,
        baseline_steps=int(args.baseline_steps),
        epsilon_value=float(args.epsilon),
    )
    candidates = [
        _transport_cloud(
            harness,
            cloud["post_flow"],
            cloud["weights"],
            cloud["normalized_log_weights"],
            epsilon_value=float(args.epsilon),
            steps=int(steps),
            dense_parity_particles=int(args.dense_parity_particles),
        )
        for steps in args.candidate_steps
    ]
    increments = cloud["increments"].numpy().astype(np.float64)
    ess = cloud["ess"].numpy().astype(np.float64)
    kalman = base._kalman_transition_first(
        harness,
        state_dim,
        cloud["observations"].numpy().astype(np.float64),
    )
    prefix = np.cumsum(increments, axis=1)
    target_increment_mean, target_increment_sd, target_increment_mcse = (
        base._mean_sd_mcse(increments[:, target_time])
    )
    prefix_mean, prefix_sd, prefix_mcse = base._mean_sd_mcse(prefix[:, target_time])
    return {
        "state_dim": int(state_dim),
        "target_time": int(target_time),
        "baseline_steps_before_target": int(args.baseline_steps),
        "epsilon": float(args.epsilon),
        "candidate_steps": [int(value) for value in args.candidate_steps],
        "target_increment_mean": target_increment_mean,
        "target_increment_sd": target_increment_sd,
        "target_increment_mcse": target_increment_mcse,
        "target_kalman_increment": float(kalman["increments"][target_time]),
        "target_increment_delta_to_kalman": target_increment_mean
        - float(kalman["increments"][target_time]),
        "prefix_mean": prefix_mean,
        "prefix_sd": prefix_sd,
        "prefix_mcse": prefix_mcse,
        "target_kalman_prefix": float(kalman["prefix"][target_time]),
        "prefix_delta_to_kalman": prefix_mean - float(kalman["prefix"][target_time]),
        "ess_mean_at_target": float(ess[:, target_time].mean()),
        "ess_min_at_target": float(ess[:, target_time].min()),
        "candidates": candidates,
    }


def _interpret(payload: dict[str, Any]) -> dict[str, str]:
    row_failures = []
    row_passes = []
    covariance_live = []
    for result in payload["results"]:
        best = min(result["candidates"], key=lambda item: item["dense_row_residual"])
        if best["dense_row_residual"] <= 1.0e-3:
            row_passes.append(
                f"state_dim={result['state_dim']} passes at steps={best['steps']} "
                f"with row={best['dense_row_residual']:.3e}"
            )
        else:
            row_failures.append(
                f"state_dim={result['state_dim']} best steps={best['steps']} "
                f"row={best['dense_row_residual']:.3e}"
            )
        if best["post_pre_cov_trace_ratio_mean"] < 0.8:
            covariance_live.append(
                f"state_dim={result['state_dim']} best cov ratio="
                f"{best['post_pre_cov_trace_ratio_mean']:.6f}"
            )
    if row_failures:
        decision = "Focused worst-time row residuals still fail at the tested budgets."
        next_action = (
            "Inspect transport-from-potentials normalization/application before "
            "changing production transport or the LGSSM statistical harness."
        )
        primary = "; ".join(row_failures)
    elif covariance_live:
        decision = "Focused worst-time row residuals pass, but covariance contraction remains live."
        next_action = "Move to reset covariance semantics before changing the statistical harness."
        primary = "; ".join(row_passes + covariance_live)
    else:
        decision = "Focused worst-time row residuals pass at the tested budgets."
        next_action = "Consider a bounded full-propagation confirmation before harness changes."
        primary = "; ".join(row_passes)
    return {
        "decision": decision,
        "primary_criterion_status": primary,
        "veto_diagnostic_status": "PASS",
        "main_uncertainty": (
            "The target clouds are produced by baseline steps before the target; "
            "a full-propagation higher-budget run is still needed if this passes."
        ),
        "next_justified_action": next_action,
        "not_concluded": (
            "No gradient correctness, SIR correctness, GPU/XLA performance, HMC "
            "readiness, posterior correctness, production readiness, or broad "
            "scientific validity."
        ),
    }


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# LEDH-PFPF-OT LGSSM Worst-Time Budget Diagnostic Result",
        "",
        f"Date: {payload['timestamp']}",
        "",
        "## Manifest",
        "",
        "| Field | Value |",
        "|---|---|",
    ]
    manifest = payload["manifest"]
    for key in (
        "num_particles",
        "dense_parity_particles",
        "seed_count",
        "baseline_steps",
        "candidate_steps",
        "device_scope",
        "cuda_visible_devices",
        "tf32_execution_enabled",
        "runtime_seconds",
    ):
        lines.append(f"| {key} | `{manifest.get(key)}` |")
    lines.extend(["", "## Decision Table", "", "| Field | Status |", "|---|---|"])
    for key, value in payload["decision"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Candidate Residuals",
            "",
            "| State dim | Target t | Steps | Row residual | Streaming row residual | Column residual | Dense/streaming max diff | Subset row residual | Cov trace ratio | Mean shift |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for result in payload["results"]:
        for candidate in result["candidates"]:
            lines.append(
                "| "
                f"{result['state_dim']} | {result['target_time']} | "
                f"{candidate['steps']} | "
                f"{candidate['dense_row_residual']:.3e} | "
                f"{candidate['streaming_row_residual']:.3e} | "
                f"{candidate['dense_column_residual']:.3e} | "
                f"{candidate['dense_streaming_max_abs_particle_diff']:.3e} | "
                f"{candidate['subset_dense_row_residual']:.3e} | "
                f"{candidate['post_pre_cov_trace_ratio_mean']:.6f} | "
                f"{candidate['pre_to_post_mean_l2_mean']:.3e} |"
            )
    lines.extend(["", "## Target Value Context", ""])
    lines.extend(
        [
            "| State dim | Target t | Prefix mean | Kalman prefix | Prefix delta | Target increment delta | ESS mean | ESS min |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for result in payload["results"]:
        lines.append(
            "| "
            f"{result['state_dim']} | {result['target_time']} | "
            f"{result['prefix_mean']:.6f} | "
            f"{result['target_kalman_prefix']:.6f} | "
            f"{result['prefix_delta_to_kalman']:.6f} | "
            f"{result['target_increment_delta_to_kalman']:.6f} | "
            f"{result['ess_mean_at_target']:.3f} | "
            f"{result['ess_min_at_target']:.3f} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    base._configure_import_environment(args)
    start = time.perf_counter()
    harness = base._load_harness()
    device_manifest = base._configure_tensorflow(harness, args)
    results = [_run_state_dim(harness, state_dim, args) for state_dim in args.state_dims]
    runtime = time.perf_counter() - start
    payload = {
        "timestamp": _dt.datetime.now(_dt.UTC).isoformat(),
        "plan": PLAN_PATH,
        "source_harness": str(base.HARNESS_PATH.relative_to(ROOT)),
        "manifest": {
            "git_commit": base._git_commit(),
            "command": " ".join(sys.argv),
            "output": str(args.output),
            "markdown_output": args.markdown_output,
            "python": sys.version,
            "platform": platform.platform(),
            "num_particles": int(args.num_particles),
            "dense_parity_particles": int(args.dense_parity_particles),
            "seed_count": int(args.seed_count),
            "baseline_steps": int(args.baseline_steps),
            "candidate_steps": [int(value) for value in args.candidate_steps],
            "state_dims": [int(value) for value in args.state_dims],
            "epsilon": float(args.epsilon),
            "tf32_mode": args.tf32_mode,
            "runtime_seconds": runtime,
            **device_manifest,
        },
        "results": results,
    }
    payload["decision"] = _interpret(payload)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if args.markdown_output:
        markdown_path = Path(args.markdown_output)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        _write_markdown(markdown_path, payload)


if __name__ == "__main__":
    main()
