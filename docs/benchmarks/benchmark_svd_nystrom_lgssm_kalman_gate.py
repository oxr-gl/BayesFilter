"""SVD-Nystrom LGSSM exact-Kalman gate for no-HMC promotion.

This harness reuses the reviewed LGSSM fixture, Kalman reference, and LEDH
callback machinery from the low-rank LGSSM gate, but it runs only the locked
SVD-Nystrom value route.  It is a promotion-gap artifact, not a default switch
or broad scientific-validity claim.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, NamedTuple


_PRE = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE.add_argument("--device-scope", choices=("cpu", "visible"), default="visible")
_PRE.add_argument("--cuda-visible-devices", default=None)
_PRE_ARGS, _ = _PRE.parse_known_args()
if _PRE_ARGS.device_scope == "cpu":
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
elif _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf  # noqa: E402
import tensorflow_probability as tfp  # noqa: E402

from docs.benchmarks import benchmark_low_rank_ledh_lgssm_kalman_gate as lgssm_base  # noqa: E402
from experiments.dpf_implementation.tf_tfp.filters import (  # noqa: E402
    experimental_batched_ledh_pfpf_ot_streaming_tf as streaming_tf,
)
from experiments.dpf_implementation.tf_tfp.filters import (  # noqa: E402
    experimental_batched_ledh_pfpf_ot_tf as core_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling import nystrom_transport_tf  # noqa: E402
from experiments.dpf_implementation.tf_tfp.resampling.nystrom_transport_tf import (  # noqa: E402
    nystrom_transport_resample_tensors_tf,
)


PLAN_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-"
    "master-program-2026-06-25.md"
)
SUBPLAN_PATH = (
    "docs/plans/bayesfilter-dpf-ledh-pfpf-ot-svd-nystrom-nohmc-promotion-"
    "p02-lgssm-reference-subplan-2026-06-25.md"
)
NYSTROM_RESIDUAL_THRESHOLD = 5.0e-2
LOG_WEIGHT_NORMALIZATION_THRESHOLD = lgssm_base.LOG_WEIGHT_NORMALIZATION_THRESHOLD
ESS_FRACTION_MIN_THRESHOLD = lgssm_base.ESS_FRACTION_MIN_THRESHOLD
NONCLAIMS = (
    "LGSSM exact-Kalman SVD-Nystrom gate artifact only",
    "no model-suite promotion claim",
    "no statistical superiority claim",
    "no nonlinear posterior correctness claim",
    "no dense Sinkhorn equivalence claim",
    "no HMC readiness claim",
    "no package/public default readiness claim",
    "no code default switch",
)


class NystromLGSSMValueTensors(NamedTuple):
    log_likelihood: tf.Tensor
    filtered_means: tf.Tensor
    filtered_variances: tf.Tensor
    ess_by_time: tf.Tensor
    final_log_weights: tf.Tensor
    final_particle_mean: tf.Tensor
    final_logsumexp_residual: tf.Tensor
    route_invocations: tf.Tensor
    active_resampling_mask_count: tf.Tensor
    active_resampling_batch_entries: tf.Tensor
    max_row_residual: tf.Tensor
    max_column_residual: tf.Tensor
    finite_factors: tf.Tensor
    finite_particles: tf.Tensor
    iterations_used_max: tf.Tensor
    min_kernel_denominator: tf.Tensor
    denominator_floor_hits: tf.Tensor
    max_abs_log_scaling_gauge_shift: tf.Tensor
    scaling_normalization_applications: tf.Tensor
    max_factor_diag_error: tf.Tensor
    min_factor_diagonal: tf.Tensor
    max_factor_diagonal: tf.Tensor
    landmark_core_min_eigenvalue: tf.Tensor
    landmark_core_max_eigenvalue: tf.Tensor
    landmark_core_condition_proxy: tf.Tensor
    landmark_core_effective_rank_min: tf.Tensor
    left_factor_min: tf.Tensor
    left_factor_max: tf.Tensor
    core_matrix_min: tf.Tensor
    core_matrix_max: tf.Tensor
    raw_kernel_min: tf.Tensor
    projected_kernel_min: tf.Tensor
    projection_floor_hits: tf.Tensor
    scaling_u_min: tf.Tensor
    scaling_u_max: tf.Tensor
    scaling_v_min: tf.Tensor
    scaling_v_max: tf.Tensor


def _parse_int_csv(value: str) -> list[int]:
    entries = [item.strip() for item in str(value).split(",") if item.strip()]
    if not entries:
        raise ValueError("expected at least one integer")
    return [int(item) for item in entries]


def _parse_args() -> argparse.Namespace:
    return _parse_args_impl(None)


def _parse_args_from_list_for_test(argv: list[str]) -> argparse.Namespace:
    return _parse_args_impl(argv)


def _parse_args_impl(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--case-ids", nargs="+", default=["lgssm_small_exact_ref"])
    parser.add_argument("--seeds", default=None)
    parser.add_argument("--num-particles", type=int, default=None)
    parser.add_argument("--time-steps", type=int, default=None)
    parser.add_argument("--state-dim", type=int, default=None)
    parser.add_argument("--obs-dim", type=int, default=None)
    parser.add_argument("--nystrom-rank", type=int, default=32)
    parser.add_argument("--nystrom-epsilon", type=float, default=0.5)
    parser.add_argument("--nystrom-max-iterations", type=int, default=160)
    parser.add_argument("--nystrom-convergence-threshold", type=float, default=1.0e-4)
    parser.add_argument("--nystrom-cholesky-jitter", type=float, default=1.0e-8)
    parser.add_argument("--nystrom-denominator-floor", type=float, default=1.0e-30)
    parser.add_argument(
        "--nystrom-core-solver",
        choices=("cholesky", "eigh_truncated", "svd_truncated"),
        default="svd_truncated",
    )
    parser.add_argument("--nystrom-core-rcond", type=float, default=1.0e-6)
    parser.add_argument(
        "--nystrom-kernel-mode",
        choices=("raw", "positive_projected"),
        default="raw",
    )
    parser.add_argument(
        "--nystrom-scaling-normalization",
        choices=("none", "balanced"),
        default="none",
    )
    parser.add_argument("--nystrom-diagnostics", dest="nystrom_diagnostics", action="store_true", default=True)
    parser.add_argument("--no-nystrom-diagnostics", dest="nystrom_diagnostics", action="store_false")
    parser.add_argument("--particle-chunk-size", type=int, default=64)
    parser.add_argument("--warmups", type=int, default=0)
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--dtype", choices=("float32", "float64"), default="float32")
    parser.add_argument("--jit-compile", dest="jit_compile", action="store_true", default=True)
    parser.add_argument("--no-jit-compile", dest="jit_compile", action="store_false")
    parser.add_argument("--tf32-mode", choices=("default", "enabled", "disabled"), default="enabled")
    parser.add_argument("--device", default="/GPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default=_PRE_ARGS.device_scope)
    parser.add_argument("--cuda-visible-devices", default=_PRE_ARGS.cuda_visible_devices)
    parser.add_argument("--expect-device-kind", choices=("any", "cpu", "gpu"), default="gpu")
    parser.add_argument("--selected-physical-gpu", default=None)
    parser.add_argument("--gpu-selection-note", default=None)
    parser.add_argument("--phase-id", default="SVD_NYSTROM_NOHMC_PROMOTION_P02_LGSSM_REFERENCE")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", default=None)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    if args.seeds is not None:
        args.seeds = _parse_int_csv(args.seeds)
    _validate_args(args)
    return args


def _validate_args(args: argparse.Namespace) -> None:
    unknown = [case_id for case_id in args.case_ids if case_id not in lgssm_base.PINNED_CASES]
    if unknown:
        raise ValueError(f"unknown LGSSM case ids: {unknown}")
    for name in ("num_particles", "time_steps", "state_dim", "obs_dim"):
        value = getattr(args, name)
        if value is not None and value <= 0:
            raise ValueError(f"{name} must be positive")
    if args.nystrom_rank <= 0:
        raise ValueError("nystrom_rank must be positive")
    particle_floor = min(lgssm_base._case_shape(case_id, args)["num_particles"] for case_id in args.case_ids)
    if args.nystrom_rank > particle_floor:
        raise ValueError("nystrom_rank must be <= num_particles for every selected case")
    for name in (
        "nystrom_epsilon",
        "nystrom_convergence_threshold",
        "nystrom_cholesky_jitter",
        "nystrom_denominator_floor",
        "nystrom_core_rcond",
    ):
        if getattr(args, name) <= 0.0:
            raise ValueError(f"{name} must be positive")
    if args.nystrom_max_iterations <= 0:
        raise ValueError("nystrom_max_iterations must be positive")
    if args.particle_chunk_size <= 0:
        raise ValueError("particle_chunk_size must be positive")
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be nonnegative and repeats must be positive")
    if args.device_scope == "cpu" and args.expect_device_kind == "gpu":
        raise ValueError("cpu device scope cannot expect gpu outputs")


def _dtype(args: argparse.Namespace) -> tf.DType:
    return tf.float64 if args.dtype == "float64" else tf.float32


def _configure_precision(args: argparse.Namespace) -> dict[str, Any]:
    dtype = _dtype(args)
    core_tf.DTYPE = dtype
    streaming_tf.DTYPE = dtype
    nystrom_transport_tf.DTYPE = dtype
    nystrom_transport_tf.DEFAULT_DTYPE = dtype
    if args.tf32_mode == "enabled":
        tf.config.experimental.enable_tensor_float_32_execution(True)
    elif args.tf32_mode == "disabled":
        tf.config.experimental.enable_tensor_float_32_execution(False)
    try:
        tf32_recorded: bool | str = bool(tf.config.experimental.tensor_float_32_execution_enabled())
    except Exception as exc:  # noqa: BLE001
        tf32_recorded = f"unavailable:{type(exc).__name__}"
    return {
        "dtype": args.dtype,
        "tf_dtype": dtype.name,
        "tf32_requested": args.tf32_mode,
        "tf32_execution_recorded": tf32_recorded,
    }


def _configure_gpus() -> dict[str, list[str]]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return {
        "physical_gpus": [str(device) for device in physical_gpus],
        "logical_gpus": [str(device) for device in logical_gpus],
    }


def _nystrom_value_core(
    tensors: dict[str, Any],
    callbacks: dict[str, Any],
    args: argparse.Namespace,
    dtype: tf.DType,
) -> NystromLGSSMValueTensors:
    observations = tensors["observations"]
    particles = tensors["initial_particles"]
    fixed_mask = tensors["fixed_resampling_mask"]
    fixed_resampling_policy = tensors.get("fixed_resampling_policy", "dynamic")
    transition_matrix = tensors["transition_matrix"]
    transition_covariance = tensors["transition_covariance"]
    observation_covariance = tensors["observation_covariance"]
    batch_size = int(particles.shape[0])
    num_particles = int(particles.shape[1])
    state_dim = int(particles.shape[2])
    time_steps = int(observations.shape[0])
    log_weights = core_tf.uniform_log_weights(batch_size, num_particles)
    log_likelihood = tf.zeros([batch_size], dtype=dtype)
    means_ta = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([batch_size, state_dim]))
    vars_ta = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([batch_size, state_dim]))
    ess_ta = tf.TensorArray(dtype=dtype, size=time_steps, element_shape=tf.TensorShape([batch_size]))
    active_steps, active_entries = lgssm_base._active_step_counts_tensor(fixed_mask)
    route_invocations = tf.constant(0, dtype=tf.int32)
    max_row = tf.constant(0.0, dtype=dtype)
    max_col = tf.constant(0.0, dtype=dtype)
    finite_factors = tf.constant(True)
    finite_particles = tf.constant(True)
    max_iter = tf.constant(0, dtype=tf.int32)
    min_kernel_denominator = tf.constant(float("inf"), dtype=dtype)
    denominator_floor_hits = tf.constant(0.0, dtype=dtype)
    max_abs_log_scaling_gauge_shift = tf.constant(0.0, dtype=dtype)
    scaling_normalization_applications = tf.constant(0.0, dtype=dtype)
    max_factor_diag_error = tf.constant(0.0, dtype=dtype)
    min_factor_diagonal = tf.constant(float("inf"), dtype=dtype)
    max_factor_diagonal = tf.constant(float("-inf"), dtype=dtype)
    landmark_core_min_eigenvalue = tf.constant(float("inf"), dtype=dtype)
    landmark_core_max_eigenvalue = tf.constant(float("-inf"), dtype=dtype)
    landmark_core_condition_proxy = tf.constant(0.0, dtype=dtype)
    landmark_core_effective_rank_min = tf.constant(float("inf"), dtype=dtype)
    left_factor_min = tf.constant(float("inf"), dtype=dtype)
    left_factor_max = tf.constant(float("-inf"), dtype=dtype)
    core_matrix_min = tf.constant(float("inf"), dtype=dtype)
    core_matrix_max = tf.constant(float("-inf"), dtype=dtype)
    raw_kernel_min = tf.constant(float("inf"), dtype=dtype)
    projected_kernel_min = tf.constant(float("inf"), dtype=dtype)
    projection_floor_hits = tf.constant(0.0, dtype=dtype)
    scaling_u_min = tf.constant(float("inf"), dtype=dtype)
    scaling_u_max = tf.constant(float("-inf"), dtype=dtype)
    scaling_v_min = tf.constant(float("inf"), dtype=dtype)
    scaling_v_max = tf.constant(float("-inf"), dtype=dtype)

    for time_index in range(time_steps):
        time_tensor = tf.constant(time_index, dtype=tf.int32)
        observation = observations[time_index]
        ancestors = particles
        pre_flow = callbacks["pre_flow_step_fn"](particles, time_tensor)
        step_prior_mean_fn = lambda points, t=time_tensor: callbacks["prior_mean_fn"](points, t)
        flow = streaming_tf.batched_ledh_flow_streaming_particles_tf(
            pre_flow_particles=pre_flow,
            ancestors=ancestors,
            observation=observation,
            transition_matrix=transition_matrix,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
            observation_fn=callbacks["observation_fn"],
            observation_jacobian_fn=callbacks["observation_jacobian_fn"],
            observation_residual_fn=callbacks["observation_residual_fn"],
            prior_mean_fn=step_prior_mean_fn,
            particle_chunk_size=args.particle_chunk_size,
        )
        post_flow = flow.post_flow_particles
        corrected_log_weights = (
            log_weights
            + callbacks["transition_log_density_fn"](post_flow, ancestors, time_tensor)
            + callbacks["observation_log_density_fn"](post_flow, observation, time_tensor)
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, incremental = lgssm_base._normalize_log_weights(corrected_log_weights)
        log_likelihood += incremental
        ess = 1.0 / tf.reduce_sum(weights * weights, axis=1)
        mean, variance = lgssm_base._weighted_mean_and_variance(post_flow, weights)
        means_ta = means_ta.write(time_index, mean)
        vars_ta = vars_ta.write(time_index, variance)
        ess_ta = ess_ta.write(time_index, ess)
        normalized_log_weights = tf.math.log(tf.maximum(weights, lgssm_base._log_weight_floor()))
        mask = fixed_mask[:, time_index]

        def nystrom_transport():
            resampled = nystrom_transport_resample_tensors_tf(
                post_flow,
                normalized_log_weights,
                rank=args.nystrom_rank,
                epsilon=args.nystrom_epsilon,
                max_iterations=args.nystrom_max_iterations,
                convergence_threshold=args.nystrom_convergence_threshold,
                cholesky_jitter=args.nystrom_cholesky_jitter,
                denominator_floor=args.nystrom_denominator_floor,
                core_solver=args.nystrom_core_solver,
                core_rcond=args.nystrom_core_rcond,
                kernel_mode=args.nystrom_kernel_mode,
                scaling_normalization=args.nystrom_scaling_normalization,
                diagnostics_enabled=args.nystrom_diagnostics,
            )
            return (
                tf.cast(resampled.particles, dtype),
                tf.cast(resampled.log_weights, dtype),
                tf.cast(resampled.max_row_residual, dtype),
                tf.cast(resampled.max_column_residual, dtype),
                resampled.finite_factors,
                resampled.finite_particles,
                resampled.iterations_used,
                tf.constant(1, dtype=tf.int32),
                tf.cast(resampled.min_kernel_denominator, dtype),
                tf.cast(resampled.denominator_floor_hits, dtype),
                tf.cast(resampled.max_abs_log_scaling_gauge_shift, dtype),
                tf.cast(resampled.scaling_normalization_applications, dtype),
                tf.cast(resampled.max_factor_diag_error, dtype),
                tf.cast(resampled.min_factor_diagonal, dtype),
                tf.cast(resampled.max_factor_diagonal, dtype),
                tf.cast(resampled.landmark_core_min_eigenvalue, dtype),
                tf.cast(resampled.landmark_core_max_eigenvalue, dtype),
                tf.cast(resampled.landmark_core_condition_proxy, dtype),
                tf.cast(resampled.landmark_core_effective_rank, dtype),
                tf.cast(resampled.left_factor_min, dtype),
                tf.cast(resampled.left_factor_max, dtype),
                tf.cast(resampled.core_matrix_min, dtype),
                tf.cast(resampled.core_matrix_max, dtype),
                tf.cast(resampled.raw_kernel_min, dtype),
                tf.cast(resampled.projected_kernel_min, dtype),
                tf.cast(resampled.projection_floor_hits, dtype),
                tf.cast(resampled.scaling_u_min, dtype),
                tf.cast(resampled.scaling_u_max, dtype),
                tf.cast(resampled.scaling_v_min, dtype),
                tf.cast(resampled.scaling_v_max, dtype),
            )

        def skip_transport():
            nan = tf.constant(float("nan"), dtype=dtype)
            return (
                post_flow,
                normalized_log_weights,
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(True),
                tf.constant(True),
                tf.constant(0, dtype=tf.int32),
                tf.constant(0, dtype=tf.int32),
                nan,
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                nan,
                nan,
                nan,
                nan,
                nan,
                tf.constant(0.0, dtype=dtype),
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
            )

        if fixed_resampling_policy == "all_active":
            step = nystrom_transport()
        elif fixed_resampling_policy == "all_inactive":
            step = skip_transport()
        else:
            step = lgssm_base._select_transport_step(mask, nystrom_transport, skip_transport)
        (
            particles,
            log_weights,
            row_residual,
            col_residual,
            step_finite_factors,
            step_finite_particles,
            iterations_used,
            step_invocation,
            step_min_kernel_denominator,
            step_denominator_floor_hits,
            step_max_abs_log_scaling_gauge_shift,
            step_scaling_normalization_applications,
            step_max_factor_diag_error,
            step_min_factor_diagonal,
            step_max_factor_diagonal,
            step_landmark_core_min_eigenvalue,
            step_landmark_core_max_eigenvalue,
            step_landmark_core_condition_proxy,
            step_landmark_core_effective_rank,
            step_left_factor_min,
            step_left_factor_max,
            step_core_matrix_min,
            step_core_matrix_max,
            step_raw_kernel_min,
            step_projected_kernel_min,
            step_projection_floor_hits,
            step_scaling_u_min,
            step_scaling_u_max,
            step_scaling_v_min,
            step_scaling_v_max,
        ) = step
        max_row = tf.maximum(max_row, row_residual)
        max_col = tf.maximum(max_col, col_residual)
        finite_factors = tf.logical_and(finite_factors, step_finite_factors)
        finite_particles = tf.logical_and(finite_particles, step_finite_particles)
        max_iter = tf.maximum(max_iter, iterations_used)
        route_invocations += step_invocation
        min_kernel_denominator = tf.minimum(min_kernel_denominator, step_min_kernel_denominator)
        denominator_floor_hits += step_denominator_floor_hits
        max_abs_log_scaling_gauge_shift = tf.maximum(
            max_abs_log_scaling_gauge_shift,
            step_max_abs_log_scaling_gauge_shift,
        )
        scaling_normalization_applications += step_scaling_normalization_applications
        max_factor_diag_error = tf.maximum(max_factor_diag_error, step_max_factor_diag_error)
        min_factor_diagonal = tf.minimum(min_factor_diagonal, step_min_factor_diagonal)
        max_factor_diagonal = tf.maximum(max_factor_diagonal, step_max_factor_diagonal)
        landmark_core_min_eigenvalue = tf.minimum(
            landmark_core_min_eigenvalue,
            step_landmark_core_min_eigenvalue,
        )
        landmark_core_max_eigenvalue = tf.maximum(
            landmark_core_max_eigenvalue,
            step_landmark_core_max_eigenvalue,
        )
        landmark_core_condition_proxy = tf.maximum(
            landmark_core_condition_proxy,
            step_landmark_core_condition_proxy,
        )
        landmark_core_effective_rank_min = tf.minimum(
            landmark_core_effective_rank_min,
            step_landmark_core_effective_rank,
        )
        left_factor_min = tf.minimum(left_factor_min, step_left_factor_min)
        left_factor_max = tf.maximum(left_factor_max, step_left_factor_max)
        core_matrix_min = tf.minimum(core_matrix_min, step_core_matrix_min)
        core_matrix_max = tf.maximum(core_matrix_max, step_core_matrix_max)
        raw_kernel_min = tf.minimum(raw_kernel_min, step_raw_kernel_min)
        projected_kernel_min = tf.minimum(projected_kernel_min, step_projected_kernel_min)
        projection_floor_hits += step_projection_floor_hits
        scaling_u_min = tf.minimum(scaling_u_min, step_scaling_u_min)
        scaling_u_max = tf.maximum(scaling_u_max, step_scaling_u_max)
        scaling_v_min = tf.minimum(scaling_v_min, step_scaling_v_min)
        scaling_v_max = tf.maximum(scaling_v_max, step_scaling_v_max)

    filtered_means = means_ta.stack()
    filtered_variances = vars_ta.stack()
    ess_by_time = ess_ta.stack()
    final_weights = tf.exp(log_weights - tf.reduce_logsumexp(log_weights, axis=1, keepdims=True))
    final_particle_mean, _ = lgssm_base._weighted_mean_and_variance(particles, final_weights)
    final_logsumexp_residual = tf.reduce_max(tf.abs(tf.reduce_logsumexp(log_weights, axis=1)))
    return NystromLGSSMValueTensors(
        log_likelihood=log_likelihood,
        filtered_means=filtered_means,
        filtered_variances=filtered_variances,
        ess_by_time=ess_by_time,
        final_log_weights=log_weights,
        final_particle_mean=final_particle_mean,
        final_logsumexp_residual=final_logsumexp_residual,
        route_invocations=route_invocations,
        active_resampling_mask_count=active_steps,
        active_resampling_batch_entries=active_entries,
        max_row_residual=max_row,
        max_column_residual=max_col,
        finite_factors=finite_factors,
        finite_particles=finite_particles,
        iterations_used_max=max_iter,
        min_kernel_denominator=min_kernel_denominator,
        denominator_floor_hits=denominator_floor_hits,
        max_abs_log_scaling_gauge_shift=max_abs_log_scaling_gauge_shift,
        scaling_normalization_applications=scaling_normalization_applications,
        max_factor_diag_error=max_factor_diag_error,
        min_factor_diagonal=min_factor_diagonal,
        max_factor_diagonal=max_factor_diagonal,
        landmark_core_min_eigenvalue=landmark_core_min_eigenvalue,
        landmark_core_max_eigenvalue=landmark_core_max_eigenvalue,
        landmark_core_condition_proxy=landmark_core_condition_proxy,
        landmark_core_effective_rank_min=landmark_core_effective_rank_min,
        left_factor_min=left_factor_min,
        left_factor_max=left_factor_max,
        core_matrix_min=core_matrix_min,
        core_matrix_max=core_matrix_max,
        raw_kernel_min=raw_kernel_min,
        projected_kernel_min=projected_kernel_min,
        projection_floor_hits=projection_floor_hits,
        scaling_u_min=scaling_u_min,
        scaling_u_max=scaling_u_max,
        scaling_v_min=scaling_v_min,
        scaling_v_max=scaling_v_max,
    )


def _compiled_route_outputs(
    tensors: dict[str, tf.Tensor],
    callbacks: dict[str, Any],
    args: argparse.Namespace,
    dtype: tf.DType,
):
    @tf.function(jit_compile=args.jit_compile, reduce_retracing=True)
    def compiled_outputs() -> tuple[tf.Tensor, ...]:
        value = _nystrom_value_core(tensors, callbacks, args, dtype)
        return tuple(value)

    return compiled_outputs


def _materialize_tensors(*tensors: tf.Tensor) -> None:
    for tensor in tensors:
        tensor.numpy()


def _run_case(fixture: lgssm_base.LGSSMGateFixture, args: argparse.Namespace) -> dict[str, Any]:
    dtype = _dtype(args)
    shape = lgssm_base._case_shape(fixture.case_id, args)
    tensors = lgssm_base._fixture_tensors(fixture, shape["num_particles"], fixture.seed, dtype)
    callbacks = lgssm_base._callbacks(tensors, dtype)
    compiled_outputs = _compiled_route_outputs(tensors, callbacks, args, dtype)
    start = time.perf_counter()
    with tf.device(args.device):
        outputs = compiled_outputs()
        _materialize_tensors(*outputs)
        first_call_seconds = time.perf_counter() - start
        for _ in range(args.warmups):
            _materialize_tensors(*compiled_outputs())
        timings = []
        last_outputs = outputs
        for _ in range(args.repeats):
            row_start = time.perf_counter()
            last_outputs = compiled_outputs()
            _materialize_tensors(*last_outputs)
            timings.append(time.perf_counter() - row_start)
    kalman = lgssm_base.run_kalman_reference(fixture, dtype)
    loop = _loop_from_outputs(last_outputs, fixture, shape)
    errors = lgssm_base._kalman_errors(loop, kalman)
    output_devices = [last_outputs[index].device for index in range(4)]
    hard_vetoes = _hard_vetoes(loop, errors, output_devices, args)
    return {
        "case_id": fixture.case_id,
        "case_role": fixture.role,
        "seed": fixture.seed,
        "route": "svd_nystrom",
        "status": "PASS" if not hard_vetoes else "FAIL",
        "hard_vetoes": hard_vetoes,
        "shape": shape,
        "thresholds": _case_thresholds(fixture.case_id),
        "first_call_seconds": first_call_seconds,
        "warm_call_timings_seconds": timings,
        "warm_call_timing_summary_seconds": _summary(timings),
        "output_devices": output_devices,
        **loop,
        **errors,
    }


def _loop_from_outputs(
    outputs: tuple[tf.Tensor, ...],
    fixture: lgssm_base.LGSSMGateFixture,
    shape: dict[str, int],
) -> dict[str, Any]:
    diagnostics = {
        "transport_object_kind": "nystrom_kernel_factors",
        "transport_matrix_materialized": False,
        "transport_matrix_shapes": [[1, 0, 0]],
        "route_invocations": int(outputs[7].numpy()),
        "active_resampling_mask_count": int(outputs[8].numpy()),
        "active_resampling_batch_entries": int(outputs[9].numpy()),
        "max_row_residual": _float(outputs[10]),
        "max_column_residual": _float(outputs[11]),
        "finite_factors": bool(outputs[12].numpy()),
        "finite_particles": bool(outputs[13].numpy()),
        "iterations_used_max": int(outputs[14].numpy()),
        "min_kernel_denominator": _float(outputs[15]),
        "denominator_floor_hits": _float(outputs[16]),
        "max_abs_log_scaling_gauge_shift": _float(outputs[17]),
        "scaling_normalization_applications": _float(outputs[18]),
        "max_factor_diag_error": _float(outputs[19]),
        "min_factor_diagonal": _float(outputs[20]),
        "max_factor_diagonal": _float(outputs[21]),
        "landmark_core_min_eigenvalue": _float(outputs[22]),
        "landmark_core_max_eigenvalue": _float(outputs[23]),
        "landmark_core_condition_proxy": _float(outputs[24]),
        "landmark_core_effective_rank_min": _float(outputs[25]),
        "left_factor_min": _float(outputs[26]),
        "left_factor_max": _float(outputs[27]),
        "core_matrix_min": _float(outputs[28]),
        "core_matrix_max": _float(outputs[29]),
        "raw_kernel_min": _float(outputs[30]),
        "projected_kernel_min": _float(outputs[31]),
        "projection_floor_hits": _float(outputs[32]),
        "scaling_u_min": _float(outputs[33]),
        "scaling_u_max": _float(outputs[34]),
        "scaling_v_min": _float(outputs[35]),
        "scaling_v_max": _float(outputs[36]),
    }
    return {
        "fixture": {
            "case_id": fixture.case_id,
            "role": fixture.role,
            "seed": fixture.seed,
            "state_dim": fixture.state_dim,
            "obs_dim": fixture.obs_dim,
            "time_steps": fixture.horizon,
        },
        "log_likelihood": outputs[0],
        "filtered_means": outputs[1],
        "filtered_variances": outputs[2],
        "ess_by_time": outputs[3],
        "final_particle_mean": outputs[5],
        "final_logsumexp_residual": _float(outputs[6]),
        "finite_output": _finite(outputs[0]) and _finite(outputs[1]) and _finite(outputs[2]) and _finite(outputs[3]),
        "ess_min": _float(tf.reduce_min(outputs[3])),
        "ess_fraction_min": _float(tf.reduce_min(outputs[3])) / float(shape["num_particles"]),
        "filtered_means_preview": _preview(outputs[1]),
        "filtered_variances_preview": _preview(outputs[2]),
        "log_likelihood_value": _float(outputs[0]),
        "final_particle_mean_preview": _preview(outputs[5]),
        **diagnostics,
    }


def _case_thresholds(case_id: str) -> dict[str, float]:
    spec = lgssm_base.PINNED_CASES[case_id]
    return {
        "mean_rmse_max": float(spec["mean_rmse_max"]),
        "variance_rmse_max": float(spec["variance_rmse_max"]),
        "loglik_abs_delta_max": float(spec["loglik_abs_delta_max"]),
        "nystrom_residual_max": NYSTROM_RESIDUAL_THRESHOLD,
        "log_weight_normalization_max": LOG_WEIGHT_NORMALIZATION_THRESHOLD,
        "ess_fraction_min": ESS_FRACTION_MIN_THRESHOLD,
    }


def _hard_vetoes(
    loop: dict[str, Any],
    errors: dict[str, Any],
    output_devices: list[str],
    args: argparse.Namespace,
) -> list[str]:
    vetoes: list[str] = []
    thresholds = _case_thresholds(loop["fixture"]["case_id"])
    if not errors["kalman_reference_finite"]:
        vetoes.append("nonfinite_kalman_reference")
    if not loop["finite_output"]:
        vetoes.append("nonfinite_route_output")
    if loop["route_invocations"] != loop["active_resampling_mask_count"]:
        vetoes.append("route_invocation_count_mismatch")
    if loop["active_resampling_mask_count"] > 0 and loop["route_invocations"] <= 0:
        vetoes.append("route_invocations_zero")
    if loop["transport_matrix_materialized"]:
        vetoes.append("transport_matrix_materialized")
    if loop["final_logsumexp_residual"] > thresholds["log_weight_normalization_max"]:
        vetoes.append("final_logsumexp_residual_threshold")
    if loop["ess_fraction_min"] < thresholds["ess_fraction_min"]:
        vetoes.append("ess_fraction_min_threshold")
    if loop["max_row_residual"] > thresholds["nystrom_residual_max"]:
        vetoes.append("nystrom_row_residual_threshold")
    if loop["max_column_residual"] > thresholds["nystrom_residual_max"]:
        vetoes.append("nystrom_column_residual_threshold")
    if not loop["finite_factors"]:
        vetoes.append("nonfinite_nystrom_factors")
    if not loop["finite_particles"]:
        vetoes.append("nonfinite_nystrom_particles")
    if errors["mean_rmse"] > thresholds["mean_rmse_max"]:
        vetoes.append("mean_rmse_threshold")
    if errors["variance_rmse"] > thresholds["variance_rmse_max"]:
        vetoes.append("variance_rmse_threshold")
    if errors["loglik_abs_delta"] > thresholds["loglik_abs_delta_max"]:
        vetoes.append("loglik_abs_delta_threshold")
    if args.expect_device_kind == "gpu" and not all("GPU" in device.upper() for device in output_devices):
        vetoes.append("expected_gpu_outputs_missing")
    if args.expect_device_kind == "cpu" and not all("CPU" in device.upper() for device in output_devices):
        vetoes.append("expected_cpu_outputs_missing")
    return vetoes


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    tf_metadata = _configure_precision(args)
    device_metadata = _configure_gpus()
    started_at = _dt.datetime.now(tz=_dt.UTC).isoformat()
    start = time.perf_counter()
    rows = []
    for case_id in args.case_ids:
        spec = lgssm_base.PINNED_CASES[case_id]
        seeds = list(args.seeds if args.seeds is not None else spec["seeds"])
        for seed in seeds:
            fixture = lgssm_base.build_lgssm_gate_fixture(case_id, int(seed), args)
            rows.append(_run_case(fixture, args))
    ended_at = _dt.datetime.now(tz=_dt.UTC).isoformat()
    hard_vetoes = [
        f"{row['case_id']}:{row['seed']}:{row['route']}:{veto}"
        for row in rows
        for veto in row.get("hard_vetoes", [])
    ]
    if args.device_scope == "cpu":
        evidence_class = "cpu_hidden_command_shape_debug_only"
    elif args.expect_device_kind == "gpu":
        evidence_class = "trusted_gpu_exact_reference_candidate"
    else:
        evidence_class = "local_debug_only"
    return {
        "schema_version": "svd_nystrom_lgssm_kalman_gate.v1",
        "status": "PASS" if not hard_vetoes else "FAIL",
        "phase": args.phase_id,
        "evidence_class": evidence_class,
        "algorithm_family": "svd_nystrom_ledh_pfpf_ot_lgssm_exact_kalman_gate",
        "candidate": {
            "route": "svd_nystrom_ledh_pfpf_ot",
            "candidate_id": "r32_eps0p5_raw_none_svd_rcond1e-6",
            "rank": args.nystrom_rank,
            "epsilon": args.nystrom_epsilon,
            "max_iterations": args.nystrom_max_iterations,
            "convergence_threshold": args.nystrom_convergence_threshold,
            "cholesky_jitter": args.nystrom_cholesky_jitter,
            "denominator_floor": args.nystrom_denominator_floor,
            "core_solver": args.nystrom_core_solver,
            "core_rcond": args.nystrom_core_rcond,
            "kernel_mode": args.nystrom_kernel_mode,
            "scaling_normalization": args.nystrom_scaling_normalization,
            "diagnostics_enabled": args.nystrom_diagnostics,
        },
        "hard_vetoes": hard_vetoes,
        "rows": rows,
        "pinned_cases": {case_id: _json_ready(lgssm_base.PINNED_CASES[case_id]) for case_id in args.case_ids},
        "run_manifest": _run_manifest(
            args,
            started_at=started_at,
            ended_at=ended_at,
            wall_time_seconds=time.perf_counter() - start,
            tf_metadata=tf_metadata,
            device_metadata=device_metadata,
        ),
        "inference_status": {
            "hard_veto_screen": "PASS" if not hard_vetoes else "FAIL",
            "statistically_supported_ranking": "NO",
            "descriptive_only_differences": "Runtime, ESS, and per-seed magnitudes are descriptive in P02.",
            "default_readiness": "NO",
            "next_evidence_needed": "P03 actual-SIR stress only if P02 hard gate passes.",
        },
        "nonclaims": list(NONCLAIMS),
    }


def _run_manifest(
    args: argparse.Namespace,
    *,
    started_at: str,
    ended_at: str,
    wall_time_seconds: float,
    tf_metadata: dict[str, Any],
    device_metadata: dict[str, Any],
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
        "tensorflow_probability_version": tfp.__version__,
        "device_scope": args.device_scope,
        "device": args.device,
        "expect_device_kind": args.expect_device_kind,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "selected_physical_gpu": args.selected_physical_gpu,
        "gpu_selection_note": args.gpu_selection_note,
        "jit_compile": args.jit_compile,
        "warmups": args.warmups,
        "repeats": args.repeats,
        "case_ids": list(args.case_ids),
        "seeds_override": list(args.seeds) if args.seeds is not None else None,
        "plan_path": PLAN_PATH,
        "subplan_path": SUBPLAN_PATH,
        **tf_metadata,
        **device_metadata,
        "started_at": started_at,
        "ended_at": ended_at,
        "wall_time_seconds": wall_time_seconds,
    }


def _git_output(command: list[str]) -> str:
    try:
        return subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unavailable"


def _summary(values: list[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "median": None, "mean": None, "max": None}
    return {
        "min": min(values),
        "median": statistics.median(values),
        "mean": statistics.fmean(values),
        "max": max(values),
    }


def _finite(value: tf.Tensor) -> bool:
    return bool(tf.reduce_all(tf.math.is_finite(value)).numpy())


def _float(value: Any) -> float:
    return float(tf.reshape(tf.cast(value, tf.float64), [-1])[0].numpy())


def _preview(value: tf.Tensor, limit: int = 8) -> list[float]:
    flat = tf.reshape(tf.cast(value, tf.float64), [-1])
    return [float(item) for item in flat[: min(limit, int(flat.shape[0]))].numpy().tolist()]


def _json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if isinstance(value, tf.Tensor):
        return _json_ready(value.numpy())
    if hasattr(value, "tolist"):
        try:
            return _json_ready(value.tolist())
        except (TypeError, ValueError):
            pass
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            pass
    return value


def write_markdown(result: dict[str, Any], path: Path, json_path: Path | None = None) -> None:
    lines = [
        "# SVD-Nystrom LGSSM Exact-Kalman Gate",
        "",
        f"- Status: `{result['status']}`",
        f"- Phase: `{result['phase']}`",
        f"- Evidence class: `{result['evidence_class']}`",
        f"- Hard vetoes: `{result['hard_vetoes']}`",
    ]
    if json_path is not None:
        lines.append(f"- JSON artifact: `{json_path}`")
    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Row residual | Vetoes |",
            "| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in result["rows"]:
        lines.append(
            "| {case} | {seed} | `{route}` | `{status}` | {mean} | {var} | {ll} | {row_resid} | `{vetoes}` |".format(
                case=row["case_id"],
                seed=row["seed"],
                route=row["route"],
                status=row["status"],
                mean=row["mean_rmse"],
                var=row["variance_rmse"],
                ll=row["loglik_abs_delta"],
                row_resid=row["max_row_residual"],
                vetoes=row["hard_vetoes"],
            )
        )
    lines.extend(
        [
            "",
            "## Run Manifest",
            "",
            f"- Git commit: `{result['run_manifest']['git_commit']}`",
            f"- Device scope: `{result['run_manifest']['device_scope']}`",
            f"- CUDA_VISIBLE_DEVICES: `{result['run_manifest']['cuda_visible_devices']}`",
            f"- TF32 recorded: `{result['run_manifest']['tf32_execution_recorded']}`",
            f"- JIT compile: `{result['run_manifest']['jit_compile']}`",
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
    markdown = Path(args.markdown_output) if args.markdown_output else output.with_suffix(".md")
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    ready = _json_ready(result)
    output.write_text(json.dumps(ready, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(ready, markdown, output)
    if not args.quiet:
        print(json.dumps(ready, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
