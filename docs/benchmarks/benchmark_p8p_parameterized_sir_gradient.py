"""P8p parameterized SIR d18 gradient diagnostic for LEDH-PFPF-OT.

This is a gated diagnostic harness, not a leaderboard runner.  It threads a
small three-parameter theta through the current actual-SIR streaming
LEDH-PFPF-OT route under fixed observations, fixed initial particles, fixed
stateless process-noise streams, and relaxed Sinkhorn OT.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


_PRE_PARSER = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE_PARSER.add_argument("--device-scope", choices=("cpu", "visible"), default="visible")
_PRE_PARSER.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _UNKNOWN = _PRE_PARSER.parse_known_args()
if _PRE_ARGS.device_scope == "cpu":
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
elif _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf

from bayesfilter import highdim
from docs.benchmarks import benchmark_p8j_tf32_batched_actual_sir as p8j_sir
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_streaming_tf as streaming_tf,
)
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as core_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from scripts.filtering_value_gradient_benchmark_run_p8d_numeric import (
    _dpf_sir_callbacks,
    _sir_observations,
)


DTYPE = tf.float32
PARAMETER_NAMES = (
    "log_kappa_scale",
    "log_nu_scale",
    "log_obs_noise_scale",
)
NONCLAIMS = (
    "P8p diagnostic parameterized SIR d18 target only",
    "not the fixed-parameter P8o leaderboard cell",
    "not stochastic PF marginal-gradient correctness",
    "not exact nonlinear likelihood correctness",
    "not HMC/NUTS readiness",
    "not posterior convergence",
    "not production/default readiness",
    "not Zhao-Cui TT/SIRT or MATLAB parity",
)


def _parse_int_csv(value: str) -> list[int]:
    parsed = [int(item.strip()) for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one integer")
    return parsed


def _parse_float_csv(value: str, *, expected: int) -> list[float]:
    parsed = [float(item.strip()) for item in str(value).split(",") if item.strip()]
    if len(parsed) != expected:
        raise ValueError(f"expected {expected} comma-separated floats")
    if not all(math.isfinite(item) for item in parsed):
        raise ValueError("theta entries must be finite")
    return parsed


def _parse_positive_float_csv(value: str) -> list[float]:
    parsed = [float(item.strip()) for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one positive float")
    if not all(math.isfinite(item) and item > 0.0 for item in parsed):
        raise ValueError("all finite-difference ladder steps must be positive and finite")
    return parsed


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--batch-seeds", default="81120")
    parser.add_argument("--time-steps", type=int, default=3)
    parser.add_argument("--num-particles", type=int, default=8)
    parser.add_argument("--theta", default="0,0,0")
    parser.add_argument("--phase-label", default="P8p diagnostic")
    parser.add_argument("--fd-step", type=float, default=1.0e-3)
    parser.add_argument("--fd-step-ladder", default="")
    parser.add_argument(
        "--diagnostic-components",
        choices=("all", "obs-noise"),
        default="all",
    )
    parser.add_argument(
        "--check-isolated-observation-noise",
        action="store_true",
    )
    parser.add_argument("--repeat-evaluations", type=int, default=2)
    parser.add_argument("--repeat-atol", type=float, default=1.0e-5)
    parser.add_argument("--theta-zero-parity-atol", type=float, default=1.0e-5)
    parser.add_argument(
        "--check-theta-zero-p8j-parity",
        action="store_true",
    )
    parser.add_argument(
        "--transport-policy",
        choices=("active-all", "active-odd", "no-resampling"),
        default="active-all",
    )
    parser.add_argument("--sinkhorn-iterations", type=int, default=10)
    parser.add_argument("--sinkhorn-epsilon", type=float, default=1.0)
    parser.add_argument("--annealed-scaling", type=float, default=0.9)
    parser.add_argument("--annealed-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument(
        "--transport-plan-mode",
        choices=("streaming", "dense"),
        default="streaming",
    )
    parser.add_argument(
        "--transport-ad-mode",
        choices=(
            "stabilized",
            "diff-scale",
            "diff-keys",
            "diff-potentials",
            "full",
        ),
        default="stabilized",
    )
    parser.add_argument("--row-chunk-size", type=int, default=8)
    parser.add_argument("--col-chunk-size", type=int, default=8)
    parser.add_argument("--particle-chunk-size", type=int, default=8)
    parser.add_argument("--dtype", choices=("float64", "float32"), default="float32")
    parser.add_argument(
        "--tf32-mode",
        choices=("default", "enabled", "disabled"),
        default="enabled",
    )
    parser.add_argument("--device", default="/GPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--expect-device-kind", choices=("any", "cpu", "gpu"), default="gpu")
    parser.add_argument("--output", required=True)
    parser.add_argument("--no-fail-on-veto", action="store_true")
    args = parser.parse_args()
    args.batch_seeds = _parse_int_csv(args.batch_seeds)
    args.theta_values = _parse_float_csv(args.theta, expected=3)
    args.fd_step_ladder_values = (
        _parse_positive_float_csv(args.fd_step_ladder)
        if args.fd_step_ladder.strip()
        else [float(args.fd_step)]
    )
    if args.time_steps <= 0:
        raise ValueError("time_steps must be positive")
    if args.time_steps > int(_sir_observations().shape[0]):
        raise ValueError("time_steps exceeds available SIR observations")
    if args.num_particles <= 1:
        raise ValueError("num_particles must be greater than one")
    if args.fd_step <= 0.0:
        raise ValueError("fd-step must be positive")
    if args.repeat_evaluations <= 0:
        raise ValueError("repeat-evaluations must be positive")
    if args.repeat_atol < 0.0 or args.theta_zero_parity_atol < 0.0:
        raise ValueError("tolerances must be nonnegative")
    if args.sinkhorn_iterations <= 0:
        raise ValueError("sinkhorn-iterations must be positive")
    if args.row_chunk_size <= 0 or args.col_chunk_size <= 0 or args.particle_chunk_size <= 0:
        raise ValueError("chunk sizes must be positive")
    return args


def _configure_precision(args: argparse.Namespace) -> dict[str, Any]:
    global DTYPE
    DTYPE = tf.float64 if args.dtype == "float64" else tf.float32
    core_tf.DTYPE = DTYPE
    streaming_tf.DTYPE = DTYPE
    annealed_transport_tf.DTYPE = DTYPE
    p8j_sir.DTYPE = DTYPE
    if args.tf32_mode != "default":
        tf.config.experimental.enable_tensor_float_32_execution(args.tf32_mode == "enabled")
    metadata = core_tf.precision_policy_metadata()
    metadata.update(
        {
            "dtype": args.dtype,
            "tf_dtype": DTYPE.name,
            "tf32_mode": args.tf32_mode,
            "tf32_execution_enabled": bool(
                tf.config.experimental.tensor_float_32_execution_enabled()
            ),
        }
    )
    return metadata


def _configure_gpus() -> tuple[list[str], list[str]]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return ([str(device) for device in physical_gpus], [str(device) for device in logical_gpus])


def _gpu_memory_info() -> dict[str, Any]:
    try:
        return dict(tf.config.experimental.get_memory_info("GPU:0"))
    except (ValueError, RuntimeError):
        return {"status": "unavailable"}


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


def _make_fixed_resampling_mask(batch_size: int, time_steps: int, policy: str) -> tf.Tensor:
    return p8j_sir._make_fixed_resampling_mask(batch_size, time_steps, policy)


def _batched_gaussian_logpdf(residuals: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    return p8j_sir._batched_gaussian_logpdf(residuals, covariance)


def _build_base_tensors(args: argparse.Namespace) -> tuple[dict[str, tf.Tensor], dict[str, Any]]:
    p8j_args = argparse.Namespace(
        time_steps=args.time_steps,
        num_particles=args.num_particles,
        batch_seeds=args.batch_seeds,
        transport_policy=args.transport_policy,
    )
    tensors, semantics = p8j_sir._build_actual_sir_tensors(p8j_args)
    return tensors, semantics


def _theta_components(theta_values: list[float]) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    return tuple(tf.constant(value, dtype=DTYPE) for value in theta_values)  # type: ignore[return-value]


def _scaled_parameters(
    theta_components: tuple[tf.Tensor, tf.Tensor, tf.Tensor],
) -> dict[str, tf.Tensor]:
    model = highdim.zhao_cui_sir_austria_model()
    log_kappa_scale, log_nu_scale, log_obs_noise_scale = theta_components
    base_kappa = tf.cast(model.kappa, DTYPE)
    base_nu = tf.cast(model.nu, DTYPE)
    base_observation_covariance = tf.cast(model.observation_covariance, DTYPE)
    return {
        "kappa": _scale_vector_parameter(base_kappa, log_kappa_scale),
        "nu": _scale_vector_parameter(base_nu, log_nu_scale),
        "observation_covariance": _scale_matrix_parameter(
            base_observation_covariance,
            log_obs_noise_scale,
        ),
    }


def _scale_vector_parameter(base: tf.Tensor, log_scale: tf.Tensor) -> tf.Tensor:
    scale = tf.exp(tf.convert_to_tensor(log_scale, dtype=DTYPE))
    base = tf.convert_to_tensor(base, dtype=DTYPE)
    if scale.shape.rank == 0:
        return base * scale
    if scale.shape.rank == 1:
        return base[tf.newaxis, :] * scale[:, tf.newaxis]
    raise ValueError("theta vector parameter scale must be scalar or rank 1")


def _scale_matrix_parameter(base: tf.Tensor, log_scale: tf.Tensor) -> tf.Tensor:
    scale = tf.exp(
        tf.constant(2.0, dtype=DTYPE) * tf.convert_to_tensor(log_scale, dtype=DTYPE)
    )
    base = tf.convert_to_tensor(base, dtype=DTYPE)
    if scale.shape.rank == 0:
        return base * scale
    if scale.shape.rank == 1:
        return base[tf.newaxis, :, :] * scale[:, tf.newaxis, tf.newaxis]
    raise ValueError("theta matrix parameter scale must be scalar or rank 1")


def _batch_vector_parameter(value: tf.Tensor) -> tf.Tensor:
    tensor = tf.convert_to_tensor(value, dtype=DTYPE)
    if tensor.shape.rank == 1:
        return tensor[tf.newaxis, tf.newaxis, :]
    if tensor.shape.rank == 2:
        return tensor[:, tf.newaxis, :]
    raise ValueError("batch vector parameter must have rank 1 or 2")


def _batch_matrix_parameter(value: tf.Tensor, batch_size: int) -> tf.Tensor:
    tensor = tf.convert_to_tensor(value, dtype=DTYPE)
    if tensor.shape.rank == 2:
        return tf.tile(tensor[tf.newaxis, :, :], [batch_size, 1, 1])
    if tensor.shape.rank == 3:
        if tensor.shape[0] is not None and int(tensor.shape[0]) != batch_size:
            raise ValueError("rank-3 matrix parameter batch dimension mismatch")
        return tensor
    raise ValueError("batch matrix parameter must have rank 2 or 3")


def _make_parameterized_callbacks(
    *,
    tensors: dict[str, tf.Tensor],
    seeds: list[int],
    args: argparse.Namespace,
    theta_components: tuple[tf.Tensor, tf.Tensor, tf.Tensor],
):
    model = highdim.zhao_cui_sir_austria_model()
    scaled = _scaled_parameters(theta_components)
    kappa = scaled["kappa"]
    nu = scaled["nu"]
    observation_covariance = scaled["observation_covariance"]
    adjacency = tf.cast(model._adjacency_matrix, DTYPE)
    neighbor_degree = tf.cast(model._neighbor_degree, DTYPE)
    substeps = int(model._rk4_substeps)
    step_size = tf.cast(model.delta, DTYPE) / tf.cast(substeps, DTYPE)
    callbacks = _dpf_sir_callbacks()
    process_chol = tf.linalg.cholesky(
        tf.cast(
            callbacks["process_noise_covariance_fn"](
                tf.zeros([18], dtype=tf.float64),
                0,
            ),
            DTYPE,
        )
    )
    selector = tf.cast(
        tf.one_hot(tf.constant(range(1, 18, 2), dtype=tf.int32), depth=18, dtype=tf.float64),
        DTYPE,
    )
    batch_size = len(seeds)
    num_particles = args.num_particles
    kappa_batch = _batch_vector_parameter(kappa)
    nu_batch = _batch_vector_parameter(nu)
    observation_covariance_batch = _batch_matrix_parameter(
        observation_covariance,
        batch_size,
    )

    def apply_sir_process_noise_policy(points: tf.Tensor) -> tf.Tensor:
        susceptible = tf.maximum(points[:, :, 0::2], tf.constant(0.0, dtype=DTYPE))
        infectious = points[:, :, 1::2]
        reshaped = tf.reshape(
            tf.stack([susceptible, infectious], axis=3),
            tf.shape(points),
        )
        reshaped.set_shape(points.shape)
        return reshaped

    def sir_rhs(points: tf.Tensor) -> tf.Tensor:
        susceptible = points[:, :, 0::2]
        infectious = points[:, :, 1::2]
        susceptible_neighbor = (
            tf.linalg.matmul(susceptible, adjacency, transpose_b=True)
            - susceptible * neighbor_degree[tf.newaxis, tf.newaxis, :]
        )
        infectious_neighbor = (
            tf.linalg.matmul(infectious, adjacency, transpose_b=True)
            - infectious * neighbor_degree[tf.newaxis, tf.newaxis, :]
        )
        infection = kappa_batch * susceptible * infectious
        d_susceptible = -infection + tf.constant(0.5, dtype=DTYPE) * susceptible_neighbor
        d_infectious = (
            infection
            - nu_batch * infectious
            + tf.constant(0.5, dtype=DTYPE) * infectious_neighbor
        )
        reshaped = tf.reshape(
            tf.stack([d_susceptible, d_infectious], axis=3),
            tf.shape(points),
        )
        reshaped.set_shape(points.shape)
        return reshaped

    def transition_mean(points: tf.Tensor, time_index: tf.Tensor) -> tf.Tensor:
        del time_index
        state = tf.cast(points, DTYPE)
        for _ in range(substeps):
            k1 = sir_rhs(state)
            k2 = sir_rhs(state + tf.constant(0.5, dtype=DTYPE) * step_size * k1)
            k3 = sir_rhs(state + tf.constant(0.5, dtype=DTYPE) * step_size * k2)
            k4 = sir_rhs(state + tf.constant(0.5, dtype=DTYPE) * step_size * k3)
            state = state + (step_size / tf.constant(6.0, dtype=DTYPE)) * (
                k1
                + tf.constant(2.0, dtype=DTYPE) * k2
                + tf.constant(2.0, dtype=DTYPE) * k3
                + k4
            )
        return state

    def pre_flow_step(points: tf.Tensor, time_index: tf.Tensor) -> tf.Tensor:
        mean = transition_mean(points, time_index)
        noise_rows = []
        for seed in seeds:
            seed_tensor = tf.stack(
                [
                    tf.constant(int(seed) % 2147483647, dtype=tf.int32),
                    tf.math.floormod(
                        tf.constant(1140, dtype=tf.int32) + time_index,
                        tf.constant(2147483647, dtype=tf.int32),
                    ),
                ]
            )
            noise_rows.append(
                tf.random.stateless_normal(
                    [num_particles, 18],
                    seed=seed_tensor,
                    dtype=DTYPE,
                )
            )
        noise_tensor = tf.stack(noise_rows, axis=0)
        pushed = mean + tf.einsum("bnd,ed->bne", noise_tensor, process_chol)
        return apply_sir_process_noise_policy(pushed)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        return tf.gather(points, list(range(1, 18, 2)), axis=2)

    def observation_jacobian_fn(points: tf.Tensor) -> tf.Tensor:
        chunk_particles = points.shape[1]
        if chunk_particles is None:
            raise ValueError("P8p SIR gradient diagnostic requires static chunk dimension")
        return tf.tile(
            selector[tf.newaxis, tf.newaxis, :, :],
            [batch_size, int(chunk_particles), 1, 1],
        )

    def observation_residual_fn(h_ref: tf.Tensor, observation: tf.Tensor) -> tf.Tensor:
        return observation[tf.newaxis, tf.newaxis, :] - h_ref

    def transition_log_density_fn(
        x_next: tf.Tensor,
        x_prev: tf.Tensor,
        time_index: tf.Tensor,
    ) -> tf.Tensor:
        residual = x_next - transition_mean(x_prev, time_index)
        return _batched_gaussian_logpdf(
            residual,
            tf.cast(tensors["transition_covariance"], DTYPE),
        )

    def observation_log_density_fn(
        x: tf.Tensor,
        observation: tf.Tensor,
        time_index: tf.Tensor,
    ) -> tf.Tensor:
        del time_index
        residual = observation_fn(x) - observation[tf.newaxis, tf.newaxis, :]
        return _batched_gaussian_logpdf(residual, observation_covariance_batch)

    return {
        "prior_mean_fn": transition_mean,
        "pre_flow_step_fn": pre_flow_step,
        "observation_fn": observation_fn,
        "observation_jacobian_fn": observation_jacobian_fn,
        "observation_residual_fn": observation_residual_fn,
        "transition_log_density_fn": transition_log_density_fn,
        "observation_log_density_fn": observation_log_density_fn,
        "observation_covariance": observation_covariance_batch,
    }


def _value_core(
    *,
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_components: tuple[tf.Tensor, tf.Tensor, tf.Tensor],
) -> streaming_tf.StreamingLEDHPFPFOTValueTensors:
    callbacks = _make_parameterized_callbacks(
        tensors=tensors,
        seeds=args.batch_seeds,
        args=args,
        theta_components=theta_components,
    )
    return streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf(
        observations=tensors["observations"],
        initial_particles=tensors["initial_particles"],
        fixed_resampling_mask=tensors["fixed_resampling_mask"],
        transition_matrix=tensors["transition_matrix"],
        transition_covariance=tensors["transition_covariance"],
        observation_covariance=callbacks["observation_covariance"],
        observation_fn=callbacks["observation_fn"],
        observation_jacobian_fn=callbacks["observation_jacobian_fn"],
        observation_residual_fn=callbacks["observation_residual_fn"],
        transition_log_density_fn=callbacks["transition_log_density_fn"],
        observation_log_density_fn=callbacks["observation_log_density_fn"],
        prior_mean_fn=callbacks["prior_mean_fn"],
        pre_flow_step_fn=callbacks["pre_flow_step_fn"],
        sinkhorn_epsilon=args.sinkhorn_epsilon,
        annealed_scaling=args.annealed_scaling,
        annealed_convergence_threshold=args.annealed_convergence_threshold,
        sinkhorn_iterations=args.sinkhorn_iterations,
        transport_plan_mode=args.transport_plan_mode,
        transport_ad_mode=args.transport_ad_mode,
        row_chunk_size=args.row_chunk_size,
        col_chunk_size=args.col_chunk_size,
        particle_chunk_size=args.particle_chunk_size,
        return_history=False,
    )


def _objective_from_components(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_components: tuple[tf.Tensor, tf.Tensor, tf.Tensor],
) -> tuple[tf.Tensor, tf.Tensor]:
    value = _value_core(
        tensors=tensors,
        args=args,
        theta_components=theta_components,
    ).log_likelihood
    objective = tf.reduce_mean(value)
    return objective, value


def _value_for_theta(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_values: list[float],
) -> tuple[tf.Tensor, tf.Tensor]:
    return _objective_from_components(tensors, args, _theta_components(theta_values))


def _gradient_diagnostic(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_values: list[float],
) -> dict[str, Any]:
    theta_components = _theta_components(theta_values)
    with tf.GradientTape(persistent=True) as tape:
        for component in theta_components:
            tape.watch(component)
        objective, value = _objective_from_components(tensors, args, theta_components)
    gradients = tape.gradient(objective, theta_components)
    jacobian_columns = [tape.jacobian(value, component) for component in theta_components]
    del tape
    connected = [gradient is not None for gradient in gradients]
    gradient_values = [
        tf.constant(float("nan"), dtype=DTYPE) if gradient is None else gradient
        for gradient in gradients
    ]
    jacobian_values = [
        tf.fill(tf.shape(value), tf.constant(float("nan"), dtype=DTYPE))
        if jacobian is None
        else jacobian
        for jacobian in jacobian_columns
    ]
    gradient_tensor = tf.stack(gradient_values)
    per_seed_gradient = tf.stack(jacobian_values, axis=1)
    return {
        "objective": objective,
        "log_likelihood": value,
        "gradient_tensor": gradient_tensor,
        "per_seed_gradient": per_seed_gradient,
        "connectivity_by_component": dict(zip(PARAMETER_NAMES, connected, strict=True)),
        "gradients_connected": bool(all(connected)),
    }


def _finite_difference_diagnostic(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_values: list[float],
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    step = float(args.fd_step)
    component_indices = (
        [PARAMETER_NAMES.index("log_obs_noise_scale")]
        if args.diagnostic_components == "obs-noise"
        else list(range(len(PARAMETER_NAMES)))
    )
    for index in component_indices:
        name = PARAMETER_NAMES[index]
        plus = list(theta_values)
        minus = list(theta_values)
        plus[index] += step
        minus[index] -= step
        plus_objective, _ = _value_for_theta(tensors, args, plus)
        minus_objective, _ = _value_for_theta(tensors, args, minus)
        central = (plus_objective - minus_objective) / tf.constant(2.0 * step, dtype=DTYPE)
        diagnostics.append(
            {
                "parameter": name,
                "fd_step": step,
                "plus_objective": float(plus_objective.numpy()),
                "minus_objective": float(minus_objective.numpy()),
                "central_difference": float(central.numpy()),
                "finite": bool(tf.reduce_all(tf.math.is_finite(central)).numpy()),
            }
        )
    return diagnostics


def _finite_difference_ladder_diagnostic(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_values: list[float],
) -> list[dict[str, Any]]:
    diagnostics: list[dict[str, Any]] = []
    component_indices = (
        [PARAMETER_NAMES.index("log_obs_noise_scale")]
        if args.diagnostic_components == "obs-noise"
        else list(range(len(PARAMETER_NAMES)))
    )
    for step in args.fd_step_ladder_values:
        for index in component_indices:
            name = PARAMETER_NAMES[index]
            plus = list(theta_values)
            minus = list(theta_values)
            plus[index] += step
            minus[index] -= step
            plus_objective, _ = _value_for_theta(tensors, args, plus)
            minus_objective, _ = _value_for_theta(tensors, args, minus)
            central = (plus_objective - minus_objective) / tf.constant(
                2.0 * step,
                dtype=DTYPE,
            )
            diagnostics.append(
                {
                    "parameter": name,
                    "fd_step": float(step),
                    "plus_objective": float(plus_objective.numpy()),
                    "minus_objective": float(minus_objective.numpy()),
                    "central_difference": float(central.numpy()),
                    "finite": bool(tf.reduce_all(tf.math.is_finite(central)).numpy()),
                }
            )
    return diagnostics


def _isolated_observation_noise_objective(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_components: tuple[tf.Tensor, tf.Tensor, tf.Tensor],
) -> tf.Tensor:
    callbacks = _make_parameterized_callbacks(
        tensors=tensors,
        seeds=args.batch_seeds,
        args=args,
        theta_components=theta_components,
    )
    initial_particles = tf.cast(tensors["initial_particles"], DTYPE)
    observations = tf.cast(tensors["observations"], DTYPE)
    log_terms = []
    for time_index in range(int(observations.shape[0])):
        observation = observations[time_index]
        log_terms.append(
            callbacks["observation_log_density_fn"](
                initial_particles,
                observation,
                tf.constant(time_index, dtype=tf.int32),
            )
        )
    # Average over batch and particles.  This isolates the Gaussian observation
    # covariance path from LEDH flow, target correction, and transport.
    return tf.reduce_mean(tf.stack(log_terms))


def _isolated_observation_noise_diagnostic(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta_values: list[float],
) -> dict[str, Any]:
    obs_index = PARAMETER_NAMES.index("log_obs_noise_scale")
    theta_components = _theta_components(theta_values)
    with tf.GradientTape() as tape:
        tape.watch(theta_components[obs_index])
        objective = _isolated_observation_noise_objective(
            tensors,
            args,
            theta_components,
        )
    gradient = tape.gradient(objective, theta_components[obs_index])
    gradient_value = (
        tf.constant(float("nan"), dtype=DTYPE)
        if gradient is None
        else tf.convert_to_tensor(gradient, dtype=DTYPE)
    )
    ladder = []
    for step in args.fd_step_ladder_values:
        plus = list(theta_values)
        minus = list(theta_values)
        plus[obs_index] += step
        minus[obs_index] -= step
        plus_objective = _isolated_observation_noise_objective(
            tensors,
            args,
            _theta_components(plus),
        )
        minus_objective = _isolated_observation_noise_objective(
            tensors,
            args,
            _theta_components(minus),
        )
        central = (plus_objective - minus_objective) / tf.constant(
            2.0 * step,
            dtype=DTYPE,
        )
        ladder.append(
            {
                "fd_step": float(step),
                "plus_objective": float(plus_objective.numpy()),
                "minus_objective": float(minus_objective.numpy()),
                "central_difference": float(central.numpy()),
                "ad_minus_fd": float((gradient_value - central).numpy()),
                "finite": bool(tf.reduce_all(tf.math.is_finite(central)).numpy()),
            }
        )
    return {
        "checked": True,
        "objective": float(objective.numpy()),
        "ad_gradient_log_obs_noise_scale": float(gradient_value.numpy()),
        "gradient_connected": gradient is not None,
        "gradient_finite": bool(tf.reduce_all(tf.math.is_finite(gradient_value)).numpy()),
        "finite_difference_ladder": ladder,
        "scope": "initial_particles_observation_log_density_only_no_flow_no_transport",
    }


def _p8j_fixed_value(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> tf.Tensor:
    callbacks = _dpf_sir_callbacks()
    adapter_callbacks = p8j_sir._make_actual_sir_callbacks(
        callbacks,
        tensors,
        args.batch_seeds,
        args,
    )
    value = streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf(
        observations=tensors["observations"],
        initial_particles=tensors["initial_particles"],
        fixed_resampling_mask=tensors["fixed_resampling_mask"],
        transition_matrix=tensors["transition_matrix"],
        transition_covariance=tensors["transition_covariance"],
        observation_covariance=tensors["observation_covariance"],
        observation_fn=adapter_callbacks["observation_fn"],
        observation_jacobian_fn=adapter_callbacks["observation_jacobian_fn"],
        observation_residual_fn=adapter_callbacks["observation_residual_fn"],
        transition_log_density_fn=adapter_callbacks["transition_log_density_fn"],
        observation_log_density_fn=adapter_callbacks["observation_log_density_fn"],
        prior_mean_fn=adapter_callbacks["prior_mean_fn"],
        pre_flow_step_fn=adapter_callbacks["pre_flow_step_fn"],
        sinkhorn_epsilon=args.sinkhorn_epsilon,
        annealed_scaling=args.annealed_scaling,
        annealed_convergence_threshold=args.annealed_convergence_threshold,
        sinkhorn_iterations=args.sinkhorn_iterations,
        transport_plan_mode=args.transport_plan_mode,
        transport_ad_mode=args.transport_ad_mode,
        row_chunk_size=args.row_chunk_size,
        col_chunk_size=args.col_chunk_size,
        particle_chunk_size=args.particle_chunk_size,
        return_history=False,
    )
    return value.log_likelihood


def _theta_zero_p8j_parity(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> dict[str, Any]:
    p8p_objective, p8p_value = _value_for_theta(tensors, args, [0.0, 0.0, 0.0])
    p8j_value = _p8j_fixed_value(tensors, args)
    delta = p8p_value - p8j_value
    max_abs = tf.reduce_max(tf.abs(delta))
    return {
        "checked": True,
        "p8p_theta_zero_log_likelihood": _to_float_list(p8p_value),
        "p8j_fixed_log_likelihood": _to_float_list(p8j_value),
        "p8p_theta_zero_objective": float(p8p_objective.numpy()),
        "value_delta": _to_float_list(delta),
        "max_abs_delta": float(max_abs.numpy()),
        "atol": float(args.theta_zero_parity_atol),
        "pass": bool(max_abs.numpy() <= args.theta_zero_parity_atol),
    }


def _repeat_diagnostics(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> dict[str, Any]:
    gradients: list[tf.Tensor] = []
    per_seed_gradients: list[tf.Tensor] = []
    values: list[tf.Tensor] = []
    objectives: list[tf.Tensor] = []
    connections: list[dict[str, bool]] = []
    for _ in range(args.repeat_evaluations):
        diag = _gradient_diagnostic(tensors, args, args.theta_values)
        gradients.append(diag["gradient_tensor"])
        per_seed_gradients.append(diag["per_seed_gradient"])
        values.append(diag["log_likelihood"])
        objectives.append(diag["objective"])
        connections.append(diag["connectivity_by_component"])
    value_stack = tf.stack(values)
    gradient_stack = tf.stack(gradients)
    per_seed_gradient_stack = tf.stack(per_seed_gradients)
    objective_stack = tf.stack(objectives)
    repeat_value_delta = (
        tf.reduce_max(tf.abs(value_stack[1:] - value_stack[:1]))
        if args.repeat_evaluations > 1
        else tf.constant(0.0, dtype=DTYPE)
    )
    repeat_gradient_delta = (
        tf.reduce_max(tf.abs(gradient_stack[1:] - gradient_stack[:1]))
        if args.repeat_evaluations > 1
        else tf.constant(0.0, dtype=DTYPE)
    )
    repeat_per_seed_gradient_delta = (
        tf.reduce_max(tf.abs(per_seed_gradient_stack[1:] - per_seed_gradient_stack[:1]))
        if args.repeat_evaluations > 1
        else tf.constant(0.0, dtype=DTYPE)
    )
    return {
        "objective": objectives[0],
        "log_likelihood": values[0],
        "gradient_tensor": gradients[0],
        "per_seed_gradient": per_seed_gradients[0],
        "connectivity_by_component": connections[0],
        "all_connectivity_repeats_match": all(item == connections[0] for item in connections),
        "repeat_objectives": _to_float_list(objective_stack),
        "repeat_evaluations": int(args.repeat_evaluations),
        "repeat_value_max_abs_delta": float(repeat_value_delta.numpy()),
        "repeat_gradient_max_abs_delta": float(repeat_gradient_delta.numpy()),
        "repeat_per_seed_gradient_max_abs_delta": float(
            repeat_per_seed_gradient_delta.numpy()
        ),
        "repeat_atol": float(args.repeat_atol),
        "repeat_pass": bool(
            repeat_value_delta.numpy() <= args.repeat_atol
            and repeat_gradient_delta.numpy() <= args.repeat_atol
            and repeat_per_seed_gradient_delta.numpy() <= args.repeat_atol
        ),
    }


def _to_float_list(value: tf.Tensor) -> list[float]:
    tensor = tf.reshape(tf.convert_to_tensor(value), [-1])
    return [float(item) for item in tensor.numpy().tolist()]


def _to_float_matrix(value: tf.Tensor) -> list[list[float]]:
    tensor = tf.convert_to_tensor(value)
    if tensor.shape.rank != 2:
        raise ValueError("matrix_output must have rank 2")
    return [[float(item) for item in row] for row in tensor.numpy().tolist()]


def _mc_noise_summary(per_seed_gradient: tf.Tensor) -> dict[str, dict[str, Any]]:
    gradient = tf.convert_to_tensor(per_seed_gradient, dtype=DTYPE)
    if gradient.shape.rank != 2:
        raise ValueError("per_seed_gradient must have rank 2")
    batch_size = int(gradient.shape[0])
    if batch_size <= 0:
        raise ValueError("per_seed_gradient must have at least one row")
    mean = tf.reduce_mean(gradient, axis=0)
    centered = gradient - mean[tf.newaxis, :]
    if batch_size > 1:
        sample_variance = tf.reduce_sum(tf.square(centered), axis=0) / tf.cast(
            batch_size - 1,
            DTYPE,
        )
    else:
        sample_variance = tf.zeros_like(mean)
    sample_sd = tf.sqrt(sample_variance)
    standard_error = sample_sd / tf.sqrt(tf.cast(batch_size, DTYPE))
    min_value = tf.reduce_min(gradient, axis=0)
    max_value = tf.reduce_max(gradient, axis=0)
    return {
        name: {
            "mean": float(mean[index].numpy()),
            "sample_sd_across_seed_contributions": float(sample_sd[index].numpy()),
            "standard_error_of_batch_mean": float(standard_error[index].numpy()),
            "min": float(min_value[index].numpy()),
            "max": float(max_value[index].numpy()),
            "batch_size": batch_size,
        }
        for index, name in enumerate(PARAMETER_NAMES)
    }


def _gradient_geometry_summary(per_seed_gradient: tf.Tensor) -> dict[str, Any]:
    gradient = tf.convert_to_tensor(per_seed_gradient, dtype=DTYPE)
    if gradient.shape.rank != 2:
        raise ValueError("per_seed_gradient must have rank 2")
    batch_size = int(gradient.shape[0])
    centered = gradient - tf.reduce_mean(gradient, axis=0, keepdims=True)
    if batch_size > 1:
        covariance = tf.matmul(centered, centered, transpose_a=True) / tf.cast(
            batch_size - 1,
            DTYPE,
        )
    else:
        covariance = tf.zeros([len(PARAMETER_NAMES), len(PARAMETER_NAMES)], dtype=DTYPE)
    sd = tf.sqrt(tf.maximum(tf.linalg.diag_part(covariance), tf.constant(0.0, DTYPE)))
    denom = sd[:, tf.newaxis] * sd[tf.newaxis, :]
    correlation = tf.where(
        denom > 0.0,
        covariance / denom,
        tf.zeros_like(covariance),
    )
    return {
        "parameter_order": list(PARAMETER_NAMES),
        "seed_gradient_covariance": _to_float_matrix(covariance),
        "seed_gradient_correlation": _to_float_matrix(correlation),
    }


def _finite_tensor(value: tf.Tensor) -> bool:
    return bool(tf.reduce_all(tf.math.is_finite(value)).numpy())


def _validate_device(tensors: tuple[tf.Tensor, ...], expect_device_kind: str) -> list[str]:
    devices = [tensor.device for tensor in tensors]
    if expect_device_kind == "gpu":
        if not all("GPU" in device.upper() for device in devices):
            raise RuntimeError(f"expected GPU tensors, got {devices}")
    elif expect_device_kind == "cpu":
        if not all("CPU" in device.upper() for device in devices):
            raise RuntimeError(f"expected CPU tensors, got {devices}")
    return devices


def main() -> None:
    args = _parse_args()
    precision = _configure_precision(args)
    physical_gpus, logical_gpus = _configure_gpus()
    tensors, sir_semantics = _build_base_tensors(args)
    memory_before = _gpu_memory_info()
    start = time.perf_counter()
    with tf.device(args.device):
        repeat = _repeat_diagnostics(tensors, args)
        fd = _finite_difference_diagnostic(tensors, args, args.theta_values)
        fd_ladder = _finite_difference_ladder_diagnostic(tensors, args, args.theta_values)
        if args.check_isolated_observation_noise:
            isolated_observation_noise = _isolated_observation_noise_diagnostic(
                tensors,
                args,
                args.theta_values,
            )
        else:
            isolated_observation_noise = {"checked": False}
        if args.check_theta_zero_p8j_parity:
            parity = _theta_zero_p8j_parity(tensors, args)
        else:
            parity = {
                "checked": False,
                "pass": False,
                "max_abs_delta": None,
                "atol": float(args.theta_zero_parity_atol),
            }
    elapsed = time.perf_counter() - start
    memory_after = _gpu_memory_info()

    objective = repeat["objective"]
    log_likelihood = repeat["log_likelihood"]
    gradient = repeat["gradient_tensor"]
    per_seed_gradient = repeat["per_seed_gradient"]
    output_devices = _validate_device(
        (objective, log_likelihood, gradient),
        args.expect_device_kind,
    )
    gradient_values = _to_float_list(gradient)
    gradient_finite = _finite_tensor(gradient)
    value_finite = _finite_tensor(log_likelihood) and _finite_tensor(objective)
    connectivity = repeat["connectivity_by_component"]
    fd_finite = all(bool(item["finite"]) for item in fd)
    zero_gradient_components = [
        name
        for name, value in zip(PARAMETER_NAMES, gradient_values, strict=True)
        if value == 0.0
    ]
    categorical_resampling_used = False
    relaxed_sinkhorn_ot_used = args.transport_policy != "no-resampling"
    resampling_mask_fixed = True
    random_streams_fixed = True
    primary_pass = bool(
        parity["checked"]
        and parity["pass"]
        and value_finite
        and gradient_finite
        and all(bool(item) for item in connectivity.values())
        and len(zero_gradient_components) == 0
        and fd_finite
        and repeat["repeat_pass"]
        and repeat["all_connectivity_repeats_match"]
        and random_streams_fixed
        and resampling_mask_fixed
        and relaxed_sinkhorn_ot_used
        and not categorical_resampling_used
    )
    result: dict[str, Any] = {
        "schema_version": "filter_bench.p8p_parameterized_sir_gradient.v1",
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_version": platform.python_version(),
        "tensorflow_version": tf.__version__,
        "git_commit": _git_commit(),
        "phase": args.phase_label,
        "status": "pass" if primary_pass else "blocked_or_failed",
        "elapsed_seconds": elapsed,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "physical_gpus": physical_gpus,
        "logical_gpus": logical_gpus,
        "device": args.device,
        "device_scope": args.device_scope,
        "expect_device_kind": args.expect_device_kind,
        "output_devices": output_devices,
        "precision": precision,
        "shape": {
            "batch_size": len(args.batch_seeds),
            "time_steps": args.time_steps,
            "num_particles": args.num_particles,
            "state_dim": 18,
            "obs_dim": 9,
            "parameter_dim": 3,
        },
        "sir_semantics": sir_semantics,
        "theta": dict(zip(PARAMETER_NAMES, [float(x) for x in args.theta_values], strict=True)),
        "theta_transform": {
            "kappa": "base_kappa * exp(log_kappa_scale)",
            "nu": "base_nu * exp(log_nu_scale)",
            "observation_covariance": (
                "base_observation_covariance * exp(2 * log_obs_noise_scale)"
            ),
        },
        "batch_seeds": [int(seed) for seed in args.batch_seeds],
        "initial_particle_seed_policy": "P8j initial_sample with fixed batch seeds",
        "process_noise_seed_policy": (
            "tf.random.stateless_normal seed=[batch_seed, 1140 + time_index], "
            "independent of theta"
        ),
        "random_streams_fixed_across_theta": random_streams_fixed,
        "repeat_evaluations": repeat["repeat_evaluations"],
        "repeat_objectives": repeat["repeat_objectives"],
        "repeat_value_max_abs_delta": repeat["repeat_value_max_abs_delta"],
        "repeat_gradient_max_abs_delta": repeat["repeat_gradient_max_abs_delta"],
        "repeat_per_seed_gradient_max_abs_delta": repeat[
            "repeat_per_seed_gradient_max_abs_delta"
        ],
        "repeat_atol": repeat["repeat_atol"],
        "repeat_pass": repeat["repeat_pass"],
        "transport_policy": args.transport_policy,
        "transport": {
            "value_core_mode": "streaming",
            "transport_plan_mode": args.transport_plan_mode,
            "transport_ad_mode": args.transport_ad_mode,
            "gradient_mode": "raw",
            "row_chunk_size": args.row_chunk_size,
            "col_chunk_size": args.col_chunk_size,
            "particle_chunk_size": args.particle_chunk_size,
            "sinkhorn_iterations": args.sinkhorn_iterations,
            "sinkhorn_epsilon": args.sinkhorn_epsilon,
            "annealed_scaling": args.annealed_scaling,
            "annealed_convergence_threshold": args.annealed_convergence_threshold,
            "dense_transport_matrix_materialized": False,
        },
        "resampling_mask_fixed": resampling_mask_fixed,
        "relaxed_sinkhorn_ot_used": relaxed_sinkhorn_ot_used,
        "categorical_resampling_used": categorical_resampling_used,
        "theta_zero_p8j_parity_checked": bool(parity["checked"]),
        "theta_zero_p8j_parity": parity,
        "theta_zero_p8j_value_delta_max_abs": parity["max_abs_delta"],
        "objective": float(objective.numpy()),
        "log_likelihood": _to_float_list(log_likelihood),
        "value_finite": value_finite,
        "connectivity_by_component": connectivity,
        "gradient": dict(zip(PARAMETER_NAMES, gradient_values, strict=True)),
        "gradient_values": gradient_values,
        "per_seed_gradient_contributions": _to_float_matrix(per_seed_gradient),
        "monte_carlo_gradient_noise": _mc_noise_summary(per_seed_gradient),
        "seed_gradient_geometry": _gradient_geometry_summary(per_seed_gradient),
        "gradient_finite": gradient_finite,
        "gradient_norm": float(tf.linalg.norm(gradient).numpy()),
        "zero_gradient_components": zero_gradient_components,
        "finite_difference_by_component": fd,
        "finite_difference_ladder": fd_ladder,
        "finite_difference_all_finite": fd_finite,
        "isolated_observation_noise_diagnostic": isolated_observation_noise,
        "gpu_memory_info_before": memory_before,
        "gpu_memory_info_after": memory_after,
        "primary_pass": primary_pass,
        "nonclaims": list(NONCLAIMS),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not primary_pass and not args.no_fail_on_veto:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
