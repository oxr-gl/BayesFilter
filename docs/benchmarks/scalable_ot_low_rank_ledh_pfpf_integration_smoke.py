"""Low-rank LEDH/PFPF-OT filter-integration smoke diagnostics.

This lane-owned harness embeds the existing TensorFlow LEDH flow and
log-density correction mechanics with the experimental low-rank coupling solver
route as the resampling step.  It is diagnostic only; runtime, memory, ESS, and
TF32 metadata are explanatory and do not establish speedup, posterior
correctness, HMC readiness, public API readiness, or production/default
readiness.
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
_PRE.add_argument(
    "--mode",
    choices=("small", "tuning-cpu", "medium-cpu", "gpu-scale"),
    default="small",
)
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

import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402

try:  # noqa: E402
    import tensorflow_probability as tfp  # noqa: E402
except Exception:  # noqa: BLE001
    tfp = None

from experiments.dpf_implementation.tf_tfp.filters import experimental_batched_ledh_pfpf_ot_tf  # noqa: E402
from experiments.dpf_implementation.tf_tfp.filters.experimental_batched_ledh_pfpf_ot_tf import (  # noqa: E402
    _log_weight_floor,
    _normalize_log_weights,
    _weighted_mean_and_variance,
    batched_ledh_flow_core_tf,
    uniform_log_weights,
)
from experiments.dpf_implementation.tf_tfp.resampling import low_rank_coupling_solver_tf  # noqa: E402
from experiments.dpf_implementation.tf_tfp.resampling.low_rank_coupling_solver_tf import (  # noqa: E402
    low_rank_coupling_scaled_matrix_tf,
    low_rank_coupling_solver_resample_tf,
)


PLAN_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-"
    "master-program-2026-06-20.md"
)
P01_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-"
    "p01-harness-result-2026-06-20.md"
)
P02_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-"
    "p02-tuning-result-2026-06-20.md"
)
P03_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-"
    "p03-medium-cpu-result-2026-06-20.md"
)
P04_RESULT_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-low-rank-filter-integration-scale-"
    "p04-trusted-gpu-scale-result-2026-06-20.md"
)

FIXTURE_ID = "ledh_lgssm_forced_resampling_v1"
FACTOR_RESIDUAL_THRESHOLD = 5.0e-3
INDUCED_ROW_RESIDUAL_THRESHOLD = 5.0e-3
INDUCED_COLUMN_RESIDUAL_THRESHOLD = 5.0e-3
LOG_WEIGHT_NORMALIZATION_THRESHOLD = 1.0e-6
TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD = 1.0e-10
NONCLAIMS = (
    "low-rank LEDH/PFPF-OT filter-integration diagnostic only",
    "no speedup claim",
    "no ranking claim",
    "no superiority claim",
    "no posterior correctness claim",
    "no HMC readiness claim",
    "no public API readiness claim",
    "no production/default readiness claim",
    "no dense Sinkhorn equivalence claim",
    "no broad scalable-OT selection claim",
    "no TF32-help claim",
)


def _parse_args() -> argparse.Namespace:
    return _parse_args_impl(None)


def _parse_args_from_list_for_test(argv: list[str]) -> argparse.Namespace:
    return _parse_args_impl(argv)


def _parse_args_impl(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--mode",
        choices=("small", "tuning-cpu", "medium-cpu", "gpu-scale"),
        default=_PRE_ARGS.mode,
    )
    parser.add_argument("--particle-counts", type=int, nargs="+", default=None)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--time-steps", type=int, default=None)
    parser.add_argument("--state-dim", type=int, default=None)
    parser.add_argument("--obs-dim", type=int, default=None)
    parser.add_argument("--rank", type=int, default=None)
    parser.add_argument("--assignment-epsilon", type=float, default=None)
    parser.add_argument("--tuning-ranks", type=int, nargs="+", default=None)
    parser.add_argument("--tuning-assignment-epsilons", type=float, nargs="+", default=None)
    parser.add_argument("--dtype", choices=("float32", "float64"), default=None)
    parser.add_argument(
        "--transport-policy",
        choices=("active-all", "no-resampling"),
        default="active-all",
    )
    parser.add_argument("--alpha", type=float, default=1.0e-8)
    parser.add_argument("--max-projection-iterations", type=int, default=240)
    parser.add_argument("--convergence-threshold", type=float, default=1.0e-6)
    parser.add_argument("--denominator-floor", type=float, default=1.0e-30)
    parser.add_argument("--seed", type=int, default=20260620)
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
    args = _apply_mode_defaults(args)
    _validate_args(args)
    return args


def _apply_mode_defaults(args: argparse.Namespace) -> argparse.Namespace:
    if args.mode == "small":
        args.particle_counts = args.particle_counts or [32]
        args.batch_size = args.batch_size or 2
        args.time_steps = args.time_steps or 2
        args.state_dim = args.state_dim or 3
        args.obs_dim = args.obs_dim or 2
        args.rank = args.rank or 4
        args.assignment_epsilon = args.assignment_epsilon or 0.0625
        args.dtype = args.dtype or "float64"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    elif args.mode == "tuning-cpu":
        args.particle_counts = args.particle_counts or [512]
        args.batch_size = args.batch_size or 1
        args.time_steps = args.time_steps or 2
        args.state_dim = args.state_dim or 6
        args.obs_dim = args.obs_dim or 4
        args.rank = args.rank or 64
        args.assignment_epsilon = args.assignment_epsilon or 0.015625
        args.tuning_ranks = args.tuning_ranks or [16, 32, 64, 128]
        args.tuning_assignment_epsilons = args.tuning_assignment_epsilons or [0.0625, 0.03125, 0.015625]
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    elif args.mode == "medium-cpu":
        args.particle_counts = args.particle_counts or [4096, 8192]
        args.batch_size = args.batch_size or 1
        args.time_steps = args.time_steps or 2
        args.state_dim = args.state_dim or 8
        args.obs_dim = args.obs_dim or 6
        args.rank = args.rank or 64
        args.assignment_epsilon = args.assignment_epsilon or 0.015625
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "cpu"
        args.device = args.device or "/CPU:0"
        args.trust_context = args.trust_context or "cpu_hidden_local"
    else:
        args.particle_counts = args.particle_counts or [50000, 100000]
        args.batch_size = args.batch_size or 1
        args.time_steps = args.time_steps or 1
        args.state_dim = args.state_dim or 8
        args.obs_dim = args.obs_dim or 6
        args.rank = args.rank or 64
        args.assignment_epsilon = args.assignment_epsilon or 0.015625
        args.dtype = args.dtype or "float32"
        args.device_scope = args.device_scope or "visible"
        args.device = args.device or "/GPU:0"
        args.trust_context = args.trust_context or "trusted_gpu_escalated_required"
    return args


def _validate_args(args: argparse.Namespace) -> None:
    if any(count <= 1 for count in args.particle_counts):
        raise ValueError("particle-counts must be greater than 1")
    if args.batch_size <= 0 or args.time_steps <= 0:
        raise ValueError("batch-size and time-steps must be positive")
    if args.state_dim <= 0 or args.obs_dim <= 0:
        raise ValueError("state-dim and obs-dim must be positive")
    if args.rank <= 0:
        raise ValueError("rank must be positive")
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
    if args.mode == "gpu-scale" and args.device_scope != "visible":
        raise ValueError("gpu-scale mode requires --device-scope visible")
    if args.mode != "gpu-scale" and args.device_scope != "cpu":
        raise ValueError("small, tuning-cpu, and medium-cpu modes require --device-scope cpu")
    if args.tuning_ranks is not None and any(rank <= 0 for rank in args.tuning_ranks):
        raise ValueError("tuning-ranks must be positive")
    if args.tuning_assignment_epsilons is not None and any(eps <= 0.0 for eps in args.tuning_assignment_epsilons):
        raise ValueError("tuning-assignment-epsilons must be positive")


def _tf_dtype(dtype_name: str) -> tf.DType:
    if dtype_name == "float64":
        return tf.float64
    if dtype_name == "float32":
        return tf.float32
    raise ValueError(f"unsupported dtype: {dtype_name}")


def _configure_tf(args: argparse.Namespace) -> dict[str, Any]:
    dtype = _tf_dtype(args.dtype)
    experimental_batched_ledh_pfpf_ot_tf.DTYPE = dtype
    low_rank_coupling_solver_tf.DTYPE = dtype
    low_rank_coupling_solver_tf.DEFAULT_DTYPE = dtype
    if args.tf32_mode == "enabled":
        tf.config.experimental.enable_tensor_float_32_execution(True)
    elif args.tf32_mode == "disabled":
        tf.config.experimental.enable_tensor_float_32_execution(False)
    try:
        tf32_enabled: bool | str = bool(tf.config.experimental.tensor_float_32_execution_enabled())
    except Exception as exc:  # noqa: BLE001
        tf32_enabled = f"unavailable:{type(exc).__name__}"
    return {
        "dtype": args.dtype,
        "tf_dtype": dtype.name,
        "tf32_requested": args.tf32_mode,
        "tf32_execution_recorded": tf32_enabled,
    }


def _stable_lgssm_fixture(args: argparse.Namespace, particle_count: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(args.seed + particle_count)
    batch_size = args.batch_size
    state_dim = args.state_dim
    obs_dim = args.obs_dim
    time_steps = args.time_steps

    batch = np.arange(batch_size, dtype=np.float64)
    particle_grid = np.linspace(-1.0, 1.0, particle_count, dtype=np.float64)
    state_grid = np.linspace(-0.5, 0.5, state_dim, dtype=np.float64)
    initial_particles = (
        0.045 * rng.standard_normal((batch_size, particle_count, state_dim))
        + 0.035 * np.sin(particle_grid[None, :, None] * (np.arange(state_dim)[None, None, :] + 1.0))
        + 0.02 * state_grid[None, None, :]
        + 0.0001 * batch[:, None, None]
    )

    diagonal = 0.72 + 0.04 * np.linspace(0.0, 1.0, state_dim, dtype=np.float64)
    transition_matrix = np.zeros((batch_size, state_dim, state_dim), dtype=np.float64)
    for row in range(batch_size):
        transition_matrix[row] = np.diag(diagonal + 0.00001 * row)
        transition_matrix[row] += 0.003 * np.eye(state_dim, k=1, dtype=np.float64)
        transition_matrix[row] -= 0.002 * np.eye(state_dim, k=-1, dtype=np.float64)

    q_diag = 0.30 + 0.02 * np.linspace(0.0, 1.0, state_dim, dtype=np.float64)
    r_diag = 0.45 + 0.02 * np.linspace(0.0, 1.0, obs_dim, dtype=np.float64)
    transition_covariance = np.tile(np.diag(q_diag)[None, :, :], (batch_size, 1, 1))
    observation_covariance = np.tile(np.diag(r_diag)[None, :, :], (batch_size, 1, 1))

    observation_matrix = np.zeros((batch_size, obs_dim, state_dim), dtype=np.float64)
    for row in range(batch_size):
        for obs_index in range(obs_dim):
            state_index = obs_index % state_dim
            observation_matrix[row, obs_index, state_index] = 0.55
            if state_dim > 1:
                observation_matrix[row, obs_index, (state_index + 1) % state_dim] = 0.05

    transitioned_initial = np.einsum("bnj,bdj->bnd", initial_particles, transition_matrix)
    time_grid = np.arange(time_steps, dtype=np.float64)
    time_wave = 0.01 * np.sin(0.31 * (time_grid[:, None] + 1.0) * (np.arange(state_dim) + 1.0))
    particle_wave = 0.004 * np.cos(0.7 * particle_grid[:, None] * (np.arange(state_dim) + 1.0))
    pre_flow_particles = (
        transitioned_initial[:, None, :, :]
        + time_wave[None, :, None, :]
        + particle_wave[None, None, :, :]
    )

    observations = 0.03 * np.sin(
        0.23 * (time_grid[:, None] + 1.0) * (np.arange(obs_dim, dtype=np.float64)[None, :] + 1.0)
    )
    observations += 0.01 * np.cos(
        0.17 * (time_grid[:, None] + 1.0) * (np.arange(obs_dim, dtype=np.float64)[None, :] + 2.0)
    )

    if args.transport_policy == "active-all":
        fixed_resampling_mask = np.ones((batch_size, time_steps), dtype=bool)
    else:
        fixed_resampling_mask = np.zeros((batch_size, time_steps), dtype=bool)

    return {
        "observations": observations,
        "initial_particles": initial_particles,
        "pre_flow_particles": pre_flow_particles,
        "fixed_resampling_mask": fixed_resampling_mask,
        "transition_matrix": transition_matrix,
        "transition_covariance": transition_covariance,
        "observation_covariance": observation_covariance,
        "observation_matrix": observation_matrix,
    }


def _to_tensors(fixture: dict[str, np.ndarray], dtype: tf.DType) -> dict[str, tf.Tensor]:
    tensors: dict[str, tf.Tensor] = {}
    for name, value in fixture.items():
        tensors[name] = tf.constant(value, dtype=tf.bool if value.dtype == np.bool_ else dtype)
    return tensors


def _make_observation_fn(observation_matrix: tf.Tensor):
    def _observation(points: tf.Tensor) -> tf.Tensor:
        return tf.einsum("bmd,bnd->bnm", observation_matrix, points)

    return _observation


def _make_observation_jacobian_fn(observation_matrix: tf.Tensor):
    def _observation_jacobian(points: tf.Tensor) -> tf.Tensor:
        batch_size = points.shape[0]
        num_particles = points.shape[1]
        if batch_size is None or num_particles is None:
            raise ValueError("integration fixture requires static batch and particle dimensions")
        return tf.tile(observation_matrix[:, None, :, :], [1, num_particles, 1, 1])

    return _observation_jacobian


def _observation_residual(h_ref: tf.Tensor, observation: tf.Tensor) -> tf.Tensor:
    return observation[None, None, :] - h_ref


def _batched_gaussian_logpdf(residuals: tf.Tensor, covariance: tf.Tensor, dtype: tf.DType) -> tf.Tensor:
    chol = tf.linalg.cholesky(covariance)
    solved = tf.linalg.matrix_transpose(
        tf.linalg.cholesky_solve(chol, tf.linalg.matrix_transpose(residuals))
    )
    quad = tf.reduce_sum(solved * residuals, axis=-1)
    logdet = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)), axis=-1)
    dim = tf.cast(residuals.shape[-1], dtype)
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * np.pi, dtype))
        + logdet[:, None]
        + quad
    )


def _make_transition_log_density(transition_matrix: tf.Tensor, transition_covariance: tf.Tensor, dtype: tf.DType):
    def _transition_log_density(x_next: tf.Tensor, x_prev: tf.Tensor, _time_index: tf.Tensor) -> tf.Tensor:
        del _time_index
        mean = tf.einsum("bnj,bdj->bnd", x_prev, transition_matrix)
        return _batched_gaussian_logpdf(x_next - mean, transition_covariance, dtype)

    return _transition_log_density


def _make_observation_log_density(observation_matrix: tf.Tensor, observation_covariance: tf.Tensor, dtype: tf.DType):
    def _observation_log_density(x: tf.Tensor, observation: tf.Tensor, _time_index: tf.Tensor) -> tf.Tensor:
        del _time_index
        predicted = tf.einsum("bmd,bnd->bnm", observation_matrix, x)
        return _batched_gaussian_logpdf(predicted - observation[None, None, :], observation_covariance, dtype)

    return _observation_log_density


def _float(value: Any) -> float:
    return float(tf.reshape(tf.cast(value, tf.float64), [-1])[0].numpy())


def _bool(value: Any) -> bool:
    return bool(tf.reduce_all(tf.cast(value, tf.bool)).numpy())


def _run_filter_loop(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    *,
    rank: int,
    assignment_epsilon: float,
    dtype: tf.DType,
    allow_tiny_materialization: bool,
) -> dict[str, Any]:
    observations = tensors["observations"]
    particles = tensors["initial_particles"]
    pre_flow_particles = tensors["pre_flow_particles"]
    fixed_mask = tensors["fixed_resampling_mask"]
    transition_matrix = tensors["transition_matrix"]
    transition_covariance = tensors["transition_covariance"]
    observation_covariance = tensors["observation_covariance"]
    observation_matrix = tensors["observation_matrix"]

    batch_size = int(particles.shape[0])
    num_particles = int(particles.shape[1])
    time_steps = int(observations.shape[0])
    log_weights = uniform_log_weights(batch_size, num_particles)
    log_likelihood = tf.zeros([batch_size], dtype=dtype)
    means = []
    variances = []
    esses = []
    step_diagnostics: list[dict[str, Any]] = []
    invocation_count = 0
    tiny_apply_parity_values: list[float] = []
    transport_matrix_shapes: list[list[int]] = []

    active_step_count = 0
    mask_np = fixed_mask.numpy()
    for t in range(time_steps):
        column = mask_np[:, t]
        if bool(np.any(column)) and not bool(np.all(column)):
            raise ValueError("integration harness supports all-batch or no-batch resampling per time step")
        if bool(np.all(column)):
            active_step_count += 1

    transition_log_density = _make_transition_log_density(transition_matrix, transition_covariance, dtype)
    observation_log_density = _make_observation_log_density(observation_matrix, observation_covariance, dtype)

    for t in range(time_steps):
        observation = observations[t]
        ancestors = particles
        pre_flow = pre_flow_particles[:, t, :, :]
        flow = batched_ledh_flow_core_tf(
            pre_flow_particles=pre_flow,
            ancestors=ancestors,
            observation=observation,
            transition_matrix=transition_matrix,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
            observation_fn=_make_observation_fn(observation_matrix),
            observation_jacobian_fn=_make_observation_jacobian_fn(observation_matrix),
            observation_residual_fn=_observation_residual,
        )
        post_flow = flow.post_flow_particles
        target_transition = transition_log_density(post_flow, ancestors, tf.constant(t, dtype=tf.int32))
        target_observation = observation_log_density(post_flow, observation, tf.constant(t, dtype=tf.int32))
        corrected_log_weights = (
            log_weights
            + target_transition
            + target_observation
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, incremental = _normalize_log_weights(corrected_log_weights)
        log_likelihood = log_likelihood + incremental
        ess = 1.0 / tf.reduce_sum(weights * weights, axis=1)
        mean, variance = _weighted_mean_and_variance(post_flow, weights)
        means.append(mean)
        variances.append(variance)
        esses.append(ess)

        active = bool(np.all(mask_np[:, t]))
        if active:
            invocation_count += 1
            resample = low_rank_coupling_solver_resample_tf(
                post_flow,
                tf.math.log(tf.maximum(weights, _log_weight_floor())),
                rank=rank,
                assignment_epsilon=assignment_epsilon,
                alpha=args.alpha,
                max_projection_iterations=args.max_projection_iterations,
                convergence_threshold=args.convergence_threshold,
                denominator_floor=args.denominator_floor,
            )
            transport_matrix_shapes.append(resample.transport_matrix.shape.as_list())
            if allow_tiny_materialization:
                matrix = low_rank_coupling_scaled_matrix_tf(
                    resample.q_factor,
                    resample.r_factor,
                    resample.g_weights,
                )
                reconstructed = tf.linalg.matmul(matrix, post_flow)
                tiny_apply_parity_values.append(_float(tf.reduce_max(tf.abs(reconstructed - resample.particles))))
            step_diagnostics.append(dict(resample.diagnostics))
            particles = tf.convert_to_tensor(resample.particles, dtype=dtype)
            log_weights = tf.convert_to_tensor(resample.log_weights, dtype=dtype)
        else:
            particles = post_flow
            log_weights = tf.math.log(tf.maximum(weights, _log_weight_floor()))

    filtered_means = tf.stack(means, axis=0)
    filtered_variances = tf.stack(variances, axis=0)
    ess_by_time = tf.stack(esses, axis=0)
    output_log_weight_normalization = _float(tf.reduce_max(tf.abs(tf.reduce_logsumexp(log_weights, axis=1))))
    finite_log_likelihood = _bool(tf.math.is_finite(log_likelihood))
    finite_filtered_means = _bool(tf.math.is_finite(filtered_means))
    finite_filtered_variances = _bool(tf.math.is_finite(filtered_variances))
    finite_ess_by_time = _bool(tf.math.is_finite(ess_by_time))

    return {
        "log_likelihood": log_likelihood,
        "filtered_means": filtered_means,
        "filtered_variances": filtered_variances,
        "ess_by_time": ess_by_time,
        "final_particles": particles,
        "final_log_weights": log_weights,
        "low_rank_resampling_invocations": invocation_count,
        "active_resampling_mask_count": active_step_count,
        "active_resampling_batch_entries": int(np.sum(mask_np)),
        "step_diagnostics": step_diagnostics,
        "transport_matrix_shapes": transport_matrix_shapes,
        "tiny_materialized_apply_parity": max(tiny_apply_parity_values) if tiny_apply_parity_values else None,
        "output_log_weight_normalization_residual": output_log_weight_normalization,
        "finite_log_likelihood": finite_log_likelihood,
        "finite_filtered_means": finite_filtered_means,
        "finite_filtered_variances": finite_filtered_variances,
        "finite_ess_by_time": finite_ess_by_time,
        "ess_min_explanatory": _float(tf.reduce_min(ess_by_time)),
        "ess_max_explanatory": _float(tf.reduce_max(ess_by_time)),
        "filtered_mean_abs_max_explanatory": _float(tf.reduce_max(tf.abs(filtered_means))),
        "filtered_variance_abs_max_explanatory": _float(tf.reduce_max(tf.abs(filtered_variances))),
    }


def _max_diag(step_diagnostics: list[dict[str, Any]], key: str) -> float | None:
    values = [diag.get(key) for diag in step_diagnostics if diag.get(key) is not None]
    return max(float(value) for value in values) if values else None


def _all_diag(step_diagnostics: list[dict[str, Any]], key: str) -> bool | None:
    values = [diag.get(key) for diag in step_diagnostics if diag.get(key) is not None]
    return all(bool(value) for value in values) if values else None


def _run_row(
    args: argparse.Namespace,
    particle_count: int,
    *,
    rank_override: int | None = None,
    assignment_epsilon_override: float | None = None,
    force_skip: bool = False,
) -> dict[str, Any]:
    if force_skip:
        return {
            "particle_count": particle_count,
            "status": "SKIPPED",
            "skip_reason": "conditional_100k_requires_50k_pass",
            "hard_vetoes": ["conditional_100k_not_attempted_after_50k_failure"],
        }

    dtype = _tf_dtype(args.dtype)
    rank = int(rank_override if rank_override is not None else args.rank)
    assignment_epsilon = float(
        assignment_epsilon_override if assignment_epsilon_override is not None else args.assignment_epsilon
    )
    fixture = _stable_lgssm_fixture(args, particle_count)
    tensors = _to_tensors(fixture, dtype)

    start = time.perf_counter()
    with tf.device(args.device):
        loop = _run_filter_loop(
            tensors,
            args,
            rank=rank,
            assignment_epsilon=assignment_epsilon,
            dtype=dtype,
            allow_tiny_materialization=args.mode == "small" and particle_count <= 64,
        )
    wall_time = time.perf_counter() - start

    step_diagnostics = loop["step_diagnostics"]
    max_factor = _max_diag(step_diagnostics, "max_factor_marginal_residual")
    max_row = _max_diag(step_diagnostics, "max_induced_row_residual")
    max_col = _max_diag(step_diagnostics, "max_induced_column_residual")
    hard_vetoes: list[str] = []
    if args.transport_policy == "active-all":
        if loop["low_rank_resampling_invocations"] <= 0:
            hard_vetoes.append("low_rank_resampling_invocations_zero")
        if loop["low_rank_resampling_invocations"] != loop["active_resampling_mask_count"]:
            hard_vetoes.append("low_rank_resampling_invocation_count_mismatch")
    if not loop["finite_log_likelihood"]:
        hard_vetoes.append("nonfinite_log_likelihood")
    if not loop["finite_filtered_means"]:
        hard_vetoes.append("nonfinite_filtered_means")
    if not loop["finite_filtered_variances"]:
        hard_vetoes.append("nonfinite_filtered_variances")
    if not loop["finite_ess_by_time"]:
        hard_vetoes.append("nonfinite_ess_by_time")
    if _all_diag(step_diagnostics, "finite_factors") is False:
        hard_vetoes.append("nonfinite_factors")
    if _all_diag(step_diagnostics, "finite_particles") is False:
        hard_vetoes.append("nonfinite_particles")
    if _all_diag(step_diagnostics, "nonnegative_factors") is False:
        hard_vetoes.append("negative_factor")
    if _all_diag(step_diagnostics, "positive_g") is False:
        hard_vetoes.append("nonpositive_g")
    if max_factor is None and args.transport_policy == "active-all":
        hard_vetoes.append("missing_factor_diagnostics")
    if max_factor is not None and max_factor > FACTOR_RESIDUAL_THRESHOLD:
        hard_vetoes.append("factor_marginal_residual_threshold")
    if max_row is not None and max_row > INDUCED_ROW_RESIDUAL_THRESHOLD:
        hard_vetoes.append("induced_row_residual_threshold")
    if max_col is not None and max_col > INDUCED_COLUMN_RESIDUAL_THRESHOLD:
        hard_vetoes.append("induced_column_residual_threshold")
    if loop["output_log_weight_normalization_residual"] > LOG_WEIGHT_NORMALIZATION_THRESHOLD:
        hard_vetoes.append("output_log_weight_normalization_threshold")
    if args.mode == "small":
        parity = loop["tiny_materialized_apply_parity"]
        if args.transport_policy == "active-all" and (
            parity is None or parity > TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD
        ):
            hard_vetoes.append("tiny_materialized_apply_parity_threshold")
    for shape in loop["transport_matrix_shapes"]:
        if shape[-2:] != [0, 0]:
            hard_vetoes.append("solver_transport_matrix_materialized")
            break

    return {
        "particle_count": particle_count,
        "status": "PASS" if not hard_vetoes else "FAIL",
        "hard_vetoes": hard_vetoes,
        "fixture_id": FIXTURE_ID,
        "batch_size": args.batch_size,
        "time_steps": args.time_steps,
        "state_dim": args.state_dim,
        "obs_dim": args.obs_dim,
        "rank": rank,
        "assignment_epsilon": assignment_epsilon,
        "dtype": args.dtype,
        "transport_policy": args.transport_policy,
        "low_rank_resampling_invocations": loop["low_rank_resampling_invocations"],
        "active_resampling_mask_count": loop["active_resampling_mask_count"],
        "active_resampling_batch_entries": loop["active_resampling_batch_entries"],
        "transport_matrix_shapes": loop["transport_matrix_shapes"],
        "solver_transport_matrix_materialized": any(shape[-2:] != [0, 0] for shape in loop["transport_matrix_shapes"]),
        "tiny_materialized_apply_parity": loop["tiny_materialized_apply_parity"],
        "max_factor_marginal_residual": max_factor,
        "max_induced_row_residual": max_row,
        "max_induced_column_residual": max_col,
        "output_log_weight_normalization_residual": loop["output_log_weight_normalization_residual"],
        "finite_log_likelihood": loop["finite_log_likelihood"],
        "finite_filtered_means": loop["finite_filtered_means"],
        "finite_filtered_variances": loop["finite_filtered_variances"],
        "finite_ess_by_time": loop["finite_ess_by_time"],
        "all_finite_factors": _all_diag(step_diagnostics, "finite_factors"),
        "all_finite_particles": _all_diag(step_diagnostics, "finite_particles"),
        "all_nonnegative_factors": _all_diag(step_diagnostics, "nonnegative_factors"),
        "all_positive_g": _all_diag(step_diagnostics, "positive_g"),
        "projection_iterations_used_max_explanatory": _max_diag(step_diagnostics, "projection_iterations_used"),
        "projection_error_max_explanatory": _max_diag(step_diagnostics, "projection_error"),
        "ess_min_explanatory": loop["ess_min_explanatory"],
        "ess_max_explanatory": loop["ess_max_explanatory"],
        "filtered_mean_abs_max_explanatory": loop["filtered_mean_abs_max_explanatory"],
        "filtered_variance_abs_max_explanatory": loop["filtered_variance_abs_max_explanatory"],
        "wall_time_seconds_explanatory": wall_time,
        "memory_maxrss_kb_explanatory": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def _git_output(args: list[str]) -> str:
    try:
        return subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _device_metadata() -> dict[str, Any]:
    return {
        "physical_gpus": [device.name for device in tf.config.list_physical_devices("GPU")],
        "logical_gpus": [device.name for device in tf.config.list_logical_devices("GPU")],
    }


def _phase_result_path(args: argparse.Namespace) -> str:
    if args.phase_result_path:
        return args.phase_result_path
    return {
        "small": P01_RESULT_PATH,
        "tuning-cpu": P02_RESULT_PATH,
        "medium-cpu": P03_RESULT_PATH,
        "gpu-scale": P04_RESULT_PATH,
    }[args.mode]


def _run_manifest(
    args: argparse.Namespace,
    *,
    started_at: str,
    ended_at: str,
    wall_time_seconds: float,
    output_path: str,
    markdown_path: str,
    tf_metadata: dict[str, Any],
) -> dict[str, Any]:
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
        "device_scope": args.device_scope,
        "device": args.device,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "cpu_gpu_trust_context": args.trust_context,
        **tf_metadata,
        **_device_metadata(),
        "fixture_id": FIXTURE_ID,
        "batch_size": args.batch_size,
        "time_steps": args.time_steps,
        "state_dim": args.state_dim,
        "obs_dim": args.obs_dim,
        "particle_counts": list(args.particle_counts),
        "rank": args.rank,
        "assignment_epsilon": args.assignment_epsilon,
        "tuning_ranks": args.tuning_ranks,
        "tuning_assignment_epsilons": args.tuning_assignment_epsilons,
        "transport_policy": args.transport_policy,
        "seed": args.seed,
        "started_at": started_at,
        "ended_at": ended_at,
        "wall_time_seconds": wall_time_seconds,
        "artifact_paths": {"json": output_path, "markdown": markdown_path},
        "plan_path": PLAN_PATH,
        "phase_result_path": _phase_result_path(args),
    }


def _selected_tuned_setting(viable_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not viable_rows:
        return None
    selected = min(
        viable_rows,
        key=lambda row: (
            row["rank"],
            row["assignment_epsilon"],
            row["max_factor_marginal_residual"] or float("inf"),
        ),
    )
    return {
        "rank": selected["rank"],
        "assignment_epsilon": selected["assignment_epsilon"],
        "particle_count": selected["particle_count"],
        "max_factor_marginal_residual": selected["max_factor_marginal_residual"],
        "max_induced_row_residual": selected["max_induced_row_residual"],
        "max_induced_column_residual": selected["max_induced_column_residual"],
        "low_rank_resampling_invocations": selected["low_rank_resampling_invocations"],
        "active_resampling_mask_count": selected["active_resampling_mask_count"],
    }


def _summary(rows: list[dict[str, Any]], hard_vetoes: list[str], wall_time: float) -> dict[str, Any]:
    numeric_rows = [row for row in rows if row.get("status") != "SKIPPED"]

    def _max(key: str) -> float | int | None:
        values = [row.get(key) for row in numeric_rows if isinstance(row.get(key), (int, float))]
        return max(values) if values else None

    return {
        "num_rows": len(rows),
        "num_executed_rows": len(numeric_rows),
        "num_hard_vetoes": len(hard_vetoes),
        "num_viable_rows": sum(1 for row in rows if row.get("status") == "PASS"),
        "max_low_rank_resampling_invocations": _max("low_rank_resampling_invocations"),
        "max_active_resampling_mask_count": _max("active_resampling_mask_count"),
        "max_factor_marginal_residual": _max("max_factor_marginal_residual"),
        "max_induced_row_residual": _max("max_induced_row_residual"),
        "max_induced_column_residual": _max("max_induced_column_residual"),
        "max_output_log_weight_normalization_residual": _max("output_log_weight_normalization_residual"),
        "max_wall_time_seconds_explanatory": _max("wall_time_seconds_explanatory"),
        "total_wall_time_seconds_explanatory": wall_time,
        "max_memory_maxrss_kb_explanatory": _max("memory_maxrss_kb_explanatory"),
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    tf.random.set_seed(args.seed)
    tf_metadata = _configure_tf(args)
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
        tf_metadata=tf_metadata,
    )
    return {
        "status": "PASS" if not hard_vetoes else "FAIL",
        "phase": args.phase_id
        or {
            "small": "LR-LEDH-PFPF-INT-1",
            "tuning-cpu": "LR-LEDH-PFPF-INT-2",
            "medium-cpu": "LR-LEDH-PFPF-INT-3",
            "gpu-scale": "LR-LEDH-PFPF-INT-4",
        }[args.mode],
        "mode": args.mode,
        "algorithm_family": "low_rank_coupling_solver_route_filter_integration",
        "algorithm_under_test": "LEDH/PFPF-OT filter loop with P = Q diag(1/g) R^T lazy low-rank solver-route resampling",
        "fixture_contract": {
            "fixture_id": FIXTURE_ID,
            "resampling_policy": args.transport_policy,
            "active_resampling_count_role": "hard_route_execution_evidence_for_active_rows",
        },
        "thresholds": {
            "low_rank_resampling_invocations": "> 0 for active rows",
            "low_rank_resampling_invocations_equals_active_resampling_mask_count": True,
            "factor_marginal_residual": FACTOR_RESIDUAL_THRESHOLD,
            "induced_row_residual": INDUCED_ROW_RESIDUAL_THRESHOLD,
            "induced_column_residual": INDUCED_COLUMN_RESIDUAL_THRESHOLD,
            "output_log_weight_normalization_residual": LOG_WEIGHT_NORMALIZATION_THRESHOLD,
            "tiny_materialized_apply_parity": TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD,
            "runtime_memory_tf32_role": "explanatory_only",
        },
        "hard_vetoes": hard_vetoes,
        "summary": _summary(rows, hard_vetoes, wall_time),
        "viable_tuned_rows": viable_rows if args.mode == "tuning-cpu" else [],
        "selected_tuned_setting": _selected_tuned_setting(viable_rows) if args.mode == "tuning-cpu" else None,
        "rows": rows,
        "run_manifest": manifest,
        "nonclaims": list(NONCLAIMS),
    }


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, tf.Tensor):
        return _json_ready(value.numpy().tolist())
    return value


def write_markdown(result: dict[str, Any], path: Path) -> None:
    lines = [
        "# Low-Rank LEDH/PFPF-OT Filter Integration Smoke",
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
            "max_low_rank_resampling_invocations",
            "max_active_resampling_mask_count",
            "max_factor_marginal_residual",
            "max_induced_row_residual",
            "max_induced_column_residual",
            "max_output_log_weight_normalization_residual",
        } else "explanatory"
        lines.append(f"| {key} | `{value}` | {role} |")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| N | Rank | Epsilon | Status | Hard vetoes | Invocations | Active count | Factor residual | Row residual | Column residual | Sentinel shapes |",
            "| ---: | ---: | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["rows"]:
        lines.append(
            "| {n} | `{rank}` | `{epsilon}` | `{status}` | `{vetoes}` | `{inv}` | `{active}` | `{factor}` | `{row_res}` | `{col_res}` | `{shapes}` |".format(
                n=row["particle_count"],
                rank=row.get("rank"),
                epsilon=row.get("assignment_epsilon"),
                status=row["status"],
                vetoes=row.get("hard_vetoes", []),
                inv=row.get("low_rank_resampling_invocations"),
                active=row.get("active_resampling_mask_count"),
                factor=row.get("max_factor_marginal_residual"),
                row_res=row.get("max_induced_row_residual"),
                col_res=row.get("max_induced_column_residual"),
                shapes=row.get("transport_matrix_shapes"),
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
            f"- Fixture: `{result['run_manifest']['fixture_id']}`",
            "",
            "## Non-Claims",
            "",
        ]
    )
    lines.extend(f"- {claim}" for claim in result["nonclaims"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    result = build_result(args)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    output.write_text(json.dumps(_json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(result, markdown)


if __name__ == "__main__":
    main()
