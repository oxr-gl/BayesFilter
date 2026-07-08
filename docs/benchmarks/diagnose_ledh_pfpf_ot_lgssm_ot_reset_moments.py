"""Diagnose the LEDH-PFPF-OT LGSSM OT/reset moment gap.

This diagnostic reuses the LGSSM harness from
``tests/test_ledh_pfpf_ot_lgssm_kalman_statistical.py`` and records the
same-time pre-OT weighted cloud, post-OT uniform cloud, Kalman filtered
moments, next-increment alignment, and small shared-cloud dense/streaming
transport parity.  It is diagnostic only: it does not certify gradients,
posterior correctness, HMC readiness, or production readiness.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
HARNESS_PATH = ROOT / "tests" / "test_ledh_pfpf_ot_lgssm_kalman_statistical.py"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-ledh-pfpf-ot-lgssm-transport-normalization-step-ladder-plan-2026-06-26.md"
)


def _parse_setting(value: str) -> dict[str, Any]:
    try:
        epsilon_text, steps_text = value.split(":", maxsplit=1)
        epsilon = float(epsilon_text)
        steps = int(steps_text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "settings must have the form <epsilon>:<finite_steps>, e.g. 0.5:8"
        ) from exc
    if epsilon <= 0.0:
        raise argparse.ArgumentTypeError("epsilon must be positive")
    if steps <= 0:
        raise argparse.ArgumentTypeError("finite steps must be positive")
    return {"epsilon": epsilon, "steps": steps, "label": f"eps{epsilon:g}_steps{steps}"}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--num-particles", type=int, default=1000)
    parser.add_argument("--dense-parity-particles", type=int, default=128)
    parser.add_argument("--seed-count", type=int, default=10)
    parser.add_argument("--state-dims", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--settings", type=_parse_setting, nargs="+", default=[_parse_setting("0.5:8")])
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default="visible")
    parser.add_argument("--cuda-visible-devices", default="0")
    parser.add_argument("--xla", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--shared-parity", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--known-contract-comparator",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
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
    return args


def _configure_import_environment(args: argparse.Namespace) -> None:
    if args.device_scope == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(args.cuda_visible_devices)
    os.environ["BAYESFILTER_RUN_LEDHPFPFOT_LGSSM_N1000"] = "1"
    os.environ["BAYESFILTER_LEDHPFPFOT_LGSSM_NUM_PARTICLES"] = str(args.num_particles)
    os.environ.setdefault("TF_FORCE_GPU_ALLOW_GROWTH", "true")
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")


def _load_harness() -> Any:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("ledh_lgssm_harness", HARNESS_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load harness from {HARNESS_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _configure_tensorflow(harness: Any, args: argparse.Namespace) -> dict[str, Any]:
    tf = harness.tf
    tf.config.experimental.enable_tensor_float_32_execution(args.tf32_mode == "enabled")
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return {
        "device_scope": args.device_scope,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "physical_gpus": [str(device) for device in physical_gpus],
        "logical_gpus": [str(device) for device in logical_gpus],
        "tf32_execution_enabled": bool(
            tf.config.experimental.tensor_float_32_execution_enabled()
        ),
        "xla": bool(args.xla),
    }


def _kalman_transition_first(harness: Any, state_dim: int, observations: Any) -> dict[str, Any]:
    np = harness.np
    theta = harness.THETA.numpy().astype(np.float64)
    a = float(theta[0])
    q = float(np.exp(theta[1]))
    r = float(np.exp(theta[2]))
    y = observations.astype(np.float64)
    mean = np.zeros(state_dim, dtype=np.float64)
    covariance = 0.7 * np.eye(state_dim, dtype=np.float64)
    transition = a * np.eye(state_dim, dtype=np.float64)
    transition_covariance = q * np.eye(state_dim, dtype=np.float64)
    observation_covariance = r * np.eye(state_dim, dtype=np.float64)
    increments = []
    filtered_means = []
    filtered_covariances = []
    for obs in y:
        predicted_mean = transition @ mean
        predicted_covariance = transition @ covariance @ transition.T + transition_covariance
        innovation = obs - predicted_mean
        innovation_covariance = predicted_covariance + observation_covariance
        sign, logdet = np.linalg.slogdet(innovation_covariance)
        if sign <= 0:
            raise RuntimeError("non-positive innovation covariance")
        increments.append(
            -0.5
            * (
                state_dim * math.log(2.0 * math.pi)
                + logdet
                + innovation @ np.linalg.solve(innovation_covariance, innovation)
            )
        )
        gain = predicted_covariance @ np.linalg.inv(innovation_covariance)
        left = np.eye(state_dim, dtype=np.float64) - gain
        mean = predicted_mean + gain @ innovation
        covariance = (
            left @ predicted_covariance @ left.T
            + gain @ observation_covariance @ gain.T
        )
        filtered_means.append(mean.copy())
        filtered_covariances.append(covariance.copy())
    return {
        "increments": np.asarray(increments, dtype=np.float64),
        "prefix": np.cumsum(np.asarray(increments, dtype=np.float64)),
        "filtered_means": np.asarray(filtered_means, dtype=np.float64),
        "filtered_covariances": np.asarray(filtered_covariances, dtype=np.float64),
    }


def _make_compiled_moment_diagnostic(
    harness: Any,
    state_dim: int,
    *,
    epsilon_value: float,
    finite_steps: int,
    dense_parity_particles: int,
    xla: bool,
    shared_parity: bool,
    known_contract_comparator: bool,
):
    tf = harness.tf
    core = harness.core_ledh
    annealed = harness.annealed_transport_tf
    dtype = harness.DTYPE
    batch_size = harness.SEED_COUNT
    num_particles = harness.NUM_PARTICLES
    time_steps = harness.TIME_STEPS

    def weighted_moments(points: Any, weights: Any) -> tuple[Any, Any]:
        mean = tf.reduce_sum(weights[:, :, None] * points, axis=1)
        centered = points - mean[:, None, :]
        covariance = tf.einsum("bn,bni,bnj->bij", weights, centered, centered)
        return mean, covariance

    def uniform_moments(points: Any) -> tuple[Any, Any]:
        count = tf.cast(tf.shape(points)[1], dtype)
        weights = tf.fill([tf.shape(points)[0], tf.shape(points)[1]], 1.0 / count)
        return weighted_moments(points, weights)

    def transport_forward(post_flow: Any, normalized_log_weights: Any) -> tuple[Any, Any, Any]:
        center = tf.stop_gradient(tf.reduce_mean(post_flow, axis=1, keepdims=True))
        scale = tf.stop_gradient(annealed._filterflow_scale(post_flow))
        scaled_x = (post_flow - center) / scale[:, None, None]
        epsilon = tf.constant(epsilon_value, dtype=dtype)
        epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
        transported, row_residual = (
            annealed._filterflow_manual_streaming_finite_transport_stopped_scale_keys(
                scaled_x,
                post_flow,
                normalized_log_weights,
                epsilon,
                epsilon0,
                tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                steps=finite_steps,
                row_chunk_size=num_particles,
                col_chunk_size=num_particles,
            )
        )
        return transported, core.uniform_log_weights(batch_size, num_particles), row_residual

    def dense_streaming_parity(post_flow: Any, normalized_log_weights: Any) -> tuple[Any, ...]:
        if not shared_parity:
            return (
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(False),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(-1, dtype=tf.int32),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
                tf.constant(float("nan"), dtype=dtype),
            )
        subset_x = post_flow[:, :dense_parity_particles, :]
        subset_logw = normalized_log_weights[:, :dense_parity_particles]
        subset_logw = subset_logw - tf.reduce_logsumexp(subset_logw, axis=1, keepdims=True)
        center = tf.stop_gradient(tf.reduce_mean(subset_x, axis=1, keepdims=True))
        scale = tf.stop_gradient(annealed._filterflow_scale(subset_x))
        scaled_x = (subset_x - center) / scale[:, None, None]
        epsilon = tf.constant(epsilon_value, dtype=dtype)
        epsilon0 = tf.stop_gradient(annealed._filterflow_epsilon_start(scaled_x))
        transport_matrix = (
            annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
                scaled_x,
                subset_logw,
                epsilon,
                epsilon0,
                tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                steps=finite_steps,
            )
        )
        dense_particles = tf.linalg.matmul(transport_matrix, subset_x)
        streaming_particles, streaming_row_residual = (
            annealed._filterflow_manual_streaming_finite_transport_value_stopped_scale_keys(
                scaled_x,
                subset_x,
                subset_logw,
                epsilon,
                epsilon0,
                tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                steps=finite_steps,
                row_chunk_size=dense_parity_particles,
                col_chunk_size=dense_parity_particles,
            )
        )
        dense_row_residual = tf.reduce_max(
            tf.abs(tf.reduce_sum(transport_matrix, axis=2) - 1.0)
        )
        source_weights = tf.exp(subset_logw)
        dense_column_mass = tf.reduce_sum(transport_matrix, axis=1)
        dense_column_target = source_weights * tf.cast(dense_parity_particles, dtype)
        dense_column_residual = tf.reduce_max(
            tf.abs(dense_column_mass - dense_column_target)
        )
        max_abs_diff = tf.reduce_max(tf.abs(dense_particles - streaming_particles))
        mean_abs_diff = tf.reduce_mean(tf.abs(dense_particles - streaming_particles))

        comparator_steps = 100
        if known_contract_comparator and finite_steps == comparator_steps:
            comparator_threshold = tf.constant(1.0e-3, dtype=dtype)
            comparator_matrix, comparator_iterations = annealed._filterflow_exact_transport_matrix(
                scaled_x,
                subset_logw,
                epsilon,
                tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                comparator_threshold,
                tf.constant(comparator_steps, dtype=tf.int32),
                tf.shape(subset_x)[1],
                transport_ad_mode="stabilized",
            )
            comparator_particles = tf.linalg.matmul(comparator_matrix, subset_x)
            comparator_row_residual = tf.reduce_max(
                tf.abs(tf.reduce_sum(comparator_matrix, axis=2) - 1.0)
            )
            comparator_column_mass = tf.reduce_sum(comparator_matrix, axis=1)
            comparator_column_residual = tf.reduce_max(
                tf.abs(comparator_column_mass - dense_column_target)
            )
            fixed100_matrix = (
                annealed._filterflow_manual_dense_finite_transport_matrix_value_stopped_scale_keys(
                    scaled_x,
                    subset_logw,
                    epsilon,
                    epsilon0,
                    tf.constant(harness.ANNEALED_SCALING, dtype=dtype),
                    steps=comparator_steps,
                )
            )
            fixed100_particles = tf.linalg.matmul(fixed100_matrix, subset_x)
            fixed100_row_residual = tf.reduce_max(
                tf.abs(tf.reduce_sum(fixed100_matrix, axis=2) - 1.0)
            )
            fixed100_column_mass = tf.reduce_sum(fixed100_matrix, axis=1)
            fixed100_column_residual = tf.reduce_max(
                tf.abs(fixed100_column_mass - dense_column_target)
            )
            comparator_fixed100_max_abs_diff = tf.reduce_max(
                tf.abs(comparator_particles - fixed100_particles)
            )
            comparator_fixed100_mean_abs_diff = tf.reduce_mean(
                tf.abs(comparator_particles - fixed100_particles)
            )
            comparator_enabled = tf.constant(True)
        else:
            comparator_enabled = tf.constant(False)
            comparator_row_residual = tf.constant(float("nan"), dtype=dtype)
            comparator_column_residual = tf.constant(float("nan"), dtype=dtype)
            comparator_iterations = tf.constant(-1, dtype=tf.int32)
            fixed100_row_residual = tf.constant(float("nan"), dtype=dtype)
            fixed100_column_residual = tf.constant(float("nan"), dtype=dtype)
            comparator_fixed100_max_abs_diff = tf.constant(float("nan"), dtype=dtype)
            comparator_fixed100_mean_abs_diff = tf.constant(float("nan"), dtype=dtype)
        return (
            max_abs_diff,
            mean_abs_diff,
            dense_row_residual,
            dense_column_residual,
            streaming_row_residual,
            comparator_enabled,
            comparator_row_residual,
            comparator_column_residual,
            comparator_iterations,
            fixed100_row_residual,
            fixed100_column_residual,
            comparator_fixed100_max_abs_diff,
            comparator_fixed100_mean_abs_diff,
        )

    @tf.function(
        input_signature=[
            tf.TensorSpec([batch_size, 3], dtype),
            tf.TensorSpec([batch_size, num_particles, state_dim], dtype),
            tf.TensorSpec([batch_size, time_steps, num_particles, state_dim], dtype),
            tf.TensorSpec([time_steps, state_dim], dtype),
        ],
        jit_compile=xla,
        reduce_retracing=True,
    )
    def compiled(
        values: Any,
        initial_particles: Any,
        transition_noise: Any,
        observations: Any,
    ) -> dict[str, Any]:
        transition_matrix, transition_covariance, observation_covariance = (
            harness._theta_to_lgssm(values, state_dim)
        )
        transition_std = tf.sqrt(tf.linalg.diag_part(transition_covariance))
        h_jac = tf.tile(
            tf.eye(state_dim, dtype=dtype)[None, None, :, :],
            [batch_size, num_particles, 1, 1],
        )
        particles = initial_particles
        log_weights = core.uniform_log_weights(batch_size, num_particles)
        increments = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )
        pre_means = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size, state_dim]),
        )
        pre_covariances = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size, state_dim, state_dim]),
        )
        post_means = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size, state_dim]),
        )
        post_covariances = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size, state_dim, state_dim]),
        )
        ess_values = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([batch_size]),
        )
        row_residuals = tf.TensorArray(
            dtype=dtype,
            size=time_steps,
            element_shape=tf.TensorShape([]),
        )

        def cond(time_index: Any, *_loop_vars: Any) -> Any:
            return time_index < tf.constant(time_steps, dtype=tf.int32)

        def body(
            time_index: Any,
            current_particles: Any,
            current_log_weights: Any,
            increment_acc: Any,
            pre_mean_acc: Any,
            pre_covariance_acc: Any,
            post_mean_acc: Any,
            post_covariance_acc: Any,
            ess_acc: Any,
            row_residual_acc: Any,
            parity_max_abs_diff: Any,
            parity_mean_abs_diff: Any,
            parity_dense_row_residual: Any,
            parity_dense_column_residual: Any,
            parity_streaming_row_residual: Any,
            known_contract_enabled: Any,
            known_contract_row_residual: Any,
            known_contract_column_residual: Any,
            known_contract_iterations: Any,
            known_contract_fixed100_row_residual: Any,
            known_contract_fixed100_column_residual: Any,
            known_contract_fixed100_max_abs_diff: Any,
            known_contract_fixed100_mean_abs_diff: Any,
        ) -> tuple[Any, ...]:
            observation = observations[time_index]
            prior_mean = tf.einsum("bnj,bdj->bnd", current_particles, transition_matrix)
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
                current_log_weights
                + transition_log_density
                + observation_log_density
                - flow.pre_flow_log_density
                + flow.forward_log_det
            )
            weights, increment = core._normalize_log_weights(corrected_log_weights)
            normalized_log_weights = tf.math.log(tf.maximum(weights, core._log_weight_floor()))
            pre_mean, pre_covariance = weighted_moments(post_flow, weights)
            ess = 1.0 / tf.reduce_sum(weights * weights, axis=1)
            transported, next_log_weights, row_residual = transport_forward(
                post_flow,
                normalized_log_weights,
            )
            post_mean, post_covariance = uniform_moments(transported)

            parity_values = tf.cond(
                tf.equal(time_index, tf.constant(0, dtype=tf.int32)),
                lambda: dense_streaming_parity(post_flow, normalized_log_weights),
                lambda: (
                    parity_max_abs_diff,
                    parity_mean_abs_diff,
                    parity_dense_row_residual,
                    parity_dense_column_residual,
                    parity_streaming_row_residual,
                    known_contract_enabled,
                    known_contract_row_residual,
                    known_contract_column_residual,
                    known_contract_iterations,
                    known_contract_fixed100_row_residual,
                    known_contract_fixed100_column_residual,
                    known_contract_fixed100_max_abs_diff,
                    known_contract_fixed100_mean_abs_diff,
                ),
            )

            return (
                time_index + 1,
                transported,
                next_log_weights,
                increment_acc.write(time_index, increment),
                pre_mean_acc.write(time_index, pre_mean),
                pre_covariance_acc.write(time_index, pre_covariance),
                post_mean_acc.write(time_index, post_mean),
                post_covariance_acc.write(time_index, post_covariance),
                ess_acc.write(time_index, ess),
                row_residual_acc.write(time_index, row_residual),
                *parity_values,
            )

        (
            _time_index,
            _final_particles,
            _final_log_weights,
            increments,
            pre_means,
            pre_covariances,
            post_means,
            post_covariances,
            ess_values,
            row_residuals,
            parity_max_abs_diff,
            parity_mean_abs_diff,
            parity_dense_row_residual,
            parity_dense_column_residual,
            parity_streaming_row_residual,
            known_contract_enabled,
            known_contract_row_residual,
            known_contract_column_residual,
            known_contract_iterations,
            known_contract_fixed100_row_residual,
            known_contract_fixed100_column_residual,
            known_contract_fixed100_max_abs_diff,
            known_contract_fixed100_mean_abs_diff,
        ) = tf.while_loop(
            cond,
            body,
            loop_vars=(
                tf.constant(0, dtype=tf.int32),
                particles,
                log_weights,
                increments,
                pre_means,
                pre_covariances,
                post_means,
                post_covariances,
                ess_values,
                row_residuals,
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(False),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0, dtype=tf.int32),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
                tf.constant(0.0, dtype=dtype),
            ),
            parallel_iterations=1,
            maximum_iterations=time_steps,
        )
        return {
            "increments": tf.transpose(increments.stack(), [1, 0]),
            "pre_means": pre_means.stack(),
            "pre_covariances": pre_covariances.stack(),
            "post_means": post_means.stack(),
            "post_covariances": post_covariances.stack(),
            "ess": tf.transpose(ess_values.stack(), [1, 0]),
            "row_residuals": row_residuals.stack(),
            "parity_max_abs_diff": parity_max_abs_diff,
            "parity_mean_abs_diff": parity_mean_abs_diff,
            "parity_dense_row_residual": parity_dense_row_residual,
            "parity_dense_column_residual": parity_dense_column_residual,
            "parity_streaming_row_residual": parity_streaming_row_residual,
            "known_contract_enabled": known_contract_enabled,
            "known_contract_row_residual": known_contract_row_residual,
            "known_contract_column_residual": known_contract_column_residual,
            "known_contract_iterations": known_contract_iterations,
            "known_contract_fixed100_row_residual": known_contract_fixed100_row_residual,
            "known_contract_fixed100_column_residual": known_contract_fixed100_column_residual,
            "known_contract_fixed100_max_abs_diff": known_contract_fixed100_max_abs_diff,
            "known_contract_fixed100_mean_abs_diff": known_contract_fixed100_mean_abs_diff,
        }

    return compiled


def _mean_sd_mcse(samples: Any) -> tuple[float, float, float]:
    count = samples.shape[0]
    mean = float(samples.mean())
    sd = float(samples.std(ddof=1)) if count > 1 else 0.0
    mcse = sd / math.sqrt(count) if count > 0 else float("nan")
    return mean, sd, mcse


def _summarize_setting(
    harness: Any,
    raw: dict[str, Any],
    kalman: dict[str, Any],
    *,
    state_dim: int,
    setting: dict[str, Any],
    dense_parity_particles: int,
) -> dict[str, Any]:
    np = harness.np
    increments = raw["increments"].numpy().astype(np.float64)
    pre_means = raw["pre_means"].numpy().astype(np.float64)
    post_means = raw["post_means"].numpy().astype(np.float64)
    pre_covariances = raw["pre_covariances"].numpy().astype(np.float64)
    post_covariances = raw["post_covariances"].numpy().astype(np.float64)
    ess = raw["ess"].numpy().astype(np.float64)
    row_residuals = raw["row_residuals"].numpy().astype(np.float64)

    kalman_increments = kalman["increments"]
    kalman_prefix = kalman["prefix"]
    kalman_means = kalman["filtered_means"]
    kalman_covariances = kalman["filtered_covariances"]
    prefix = np.cumsum(increments, axis=1)

    time_records = []
    for time_index in range(increments.shape[1]):
        pre_mean = pre_means[time_index].mean(axis=0)
        post_mean = post_means[time_index].mean(axis=0)
        kalman_mean = kalman_means[time_index]
        pre_cov = pre_covariances[time_index].mean(axis=0)
        post_cov = post_covariances[time_index].mean(axis=0)
        kalman_cov = kalman_covariances[time_index]
        pre_trace = float(np.trace(pre_cov))
        post_trace = float(np.trace(post_cov))
        kalman_trace = float(np.trace(kalman_cov))
        inc_mean, inc_sd, inc_mcse = _mean_sd_mcse(increments[:, time_index])
        prefix_mean, prefix_sd, prefix_mcse = _mean_sd_mcse(prefix[:, time_index])
        if time_index + 1 < increments.shape[1]:
            next_mean, next_sd, next_mcse = _mean_sd_mcse(increments[:, time_index + 1])
            next_kalman = float(kalman_increments[time_index + 1])
        else:
            next_mean = next_sd = next_mcse = None
            next_kalman = None
        time_records.append(
            {
                "time_index": time_index,
                "increment_mean": inc_mean,
                "increment_sd": inc_sd,
                "increment_mcse": inc_mcse,
                "kalman_increment": float(kalman_increments[time_index]),
                "increment_delta_to_kalman": inc_mean - float(kalman_increments[time_index]),
                "next_increment_mean": next_mean,
                "next_increment_sd": next_sd,
                "next_increment_mcse": next_mcse,
                "next_kalman_increment": next_kalman,
                "next_increment_delta_to_kalman": (
                    None if next_mean is None else next_mean - next_kalman
                ),
                "prefix_mean": prefix_mean,
                "prefix_sd": prefix_sd,
                "prefix_mcse": prefix_mcse,
                "kalman_prefix": float(kalman_prefix[time_index]),
                "prefix_delta_to_kalman": prefix_mean - float(kalman_prefix[time_index]),
                "pre_ot_weighted_mean": pre_mean.tolist(),
                "post_ot_uniform_mean": post_mean.tolist(),
                "kalman_filtered_mean": kalman_mean.tolist(),
                "pre_to_post_mean_l2": float(np.linalg.norm(post_mean - pre_mean)),
                "pre_to_kalman_mean_l2": float(np.linalg.norm(pre_mean - kalman_mean)),
                "post_to_kalman_mean_l2": float(np.linalg.norm(post_mean - kalman_mean)),
                "pre_ot_weighted_covariance": pre_cov.tolist(),
                "post_ot_uniform_covariance": post_cov.tolist(),
                "kalman_filtered_covariance": kalman_cov.tolist(),
                "pre_ot_weighted_cov_trace": pre_trace,
                "post_ot_uniform_cov_trace": post_trace,
                "kalman_filtered_cov_trace": kalman_trace,
                "post_pre_cov_trace_ratio": post_trace / pre_trace if pre_trace != 0.0 else None,
                "pre_kalman_cov_trace_ratio": pre_trace / kalman_trace if kalman_trace != 0.0 else None,
                "post_kalman_cov_trace_ratio": post_trace / kalman_trace if kalman_trace != 0.0 else None,
                "ess_mean": float(ess[:, time_index].mean()),
                "ess_min": float(ess[:, time_index].min()),
                "transport_row_residual": float(row_residuals[time_index]),
            }
        )

    total_mean, total_sd, total_mcse = _mean_sd_mcse(prefix[:, -1])
    parity = {
        "shared_cloud": {
            "state_dim": state_dim,
            "seed_batch_size": int(increments.shape[0]),
            "time_index": 0,
            "particle_subset": int(dense_parity_particles),
            "renormalized_subset_log_weights": True,
            "epsilon": float(setting["epsilon"]),
            "finite_steps": int(setting["steps"]),
        },
        "max_abs_dense_streaming_particle_diff": float(raw["parity_max_abs_diff"].numpy()),
        "mean_abs_dense_streaming_particle_diff": float(raw["parity_mean_abs_diff"].numpy()),
        "dense_row_residual": float(raw["parity_dense_row_residual"].numpy()),
        "dense_column_residual": float(raw["parity_dense_column_residual"].numpy()),
        "streaming_row_residual": float(raw["parity_streaming_row_residual"].numpy()),
    }
    known_contract_comparator = {
        "shared_cloud": {
            "state_dim": state_dim,
            "seed_batch_size": int(increments.shape[0]),
            "time_index": 0,
            "particle_subset": int(dense_parity_particles),
            "renormalized_subset_log_weights": True,
            "epsilon": float(setting["epsilon"]),
            "scaling": float(harness.ANNEALED_SCALING),
            "convergence_threshold": 1.0e-3,
            "max_iter": 100,
            "transport_ad_mode": "stabilized",
        },
        "exact_thresholded_row_residual": float(
            raw["known_contract_row_residual"].numpy()
        ),
        "exact_thresholded_column_residual": float(
            raw["known_contract_column_residual"].numpy()
        ),
        "exact_thresholded_iterations": int(
            raw["known_contract_iterations"].numpy()
        ),
        "manual_fixed100_row_residual": float(
            raw["known_contract_fixed100_row_residual"].numpy()
        ),
        "manual_fixed100_column_residual": float(
            raw["known_contract_fixed100_column_residual"].numpy()
        ),
        "max_abs_exact_thresholded_to_manual_fixed100_particle_diff": float(
            raw["known_contract_fixed100_max_abs_diff"].numpy()
        ),
        "mean_abs_exact_thresholded_to_manual_fixed100_particle_diff": float(
            raw["known_contract_fixed100_mean_abs_diff"].numpy()
        ),
    }
    return {
        "state_dim": state_dim,
        "setting": setting,
        "total_mean": total_mean,
        "total_sd": total_sd,
        "total_mcse": total_mcse,
        "kalman_total": float(kalman_prefix[-1]),
        "total_delta_to_kalman": total_mean - float(kalman_prefix[-1]),
        "seed_values": prefix[:, -1].tolist(),
        "dense_streaming_parity": parity,
        "known_contract_comparator": known_contract_comparator,
        "time_records": time_records,
    }


def _run_state_setting(
    harness: Any,
    state_dim: int,
    setting: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    tf = harness.tf
    observations_tf = harness._observations(state_dim)
    initial_noise, transition_noise = harness._stateless_seeded_normals_batch(state_dim)
    initial_particles = tf.sqrt(tf.constant(0.7, harness.DTYPE)) * initial_noise
    theta_batch = tf.tile(harness.THETA[None, :], [harness.SEED_COUNT, 1])
    compiled = _make_compiled_moment_diagnostic(
        harness,
        state_dim,
        epsilon_value=float(setting["epsilon"]),
        finite_steps=int(setting["steps"]),
        dense_parity_particles=int(args.dense_parity_particles),
        xla=bool(args.xla),
        shared_parity=bool(args.shared_parity),
        known_contract_comparator=bool(args.known_contract_comparator),
    )
    raw = compiled(theta_batch, initial_particles, transition_noise, observations_tf)
    kalman = _kalman_transition_first(
        harness,
        state_dim,
        observations_tf.numpy().astype(harness.np.float64),
    )
    return _summarize_setting(
        harness,
        raw,
        kalman,
        state_dim=state_dim,
        setting=setting,
        dense_parity_particles=int(args.dense_parity_particles),
    )


def _interpret(payload: dict[str, Any]) -> tuple[dict[str, str], list[str]]:
    def max_time_row_residual(record: dict[str, Any]) -> float:
        return max(
            float(time_record["transport_row_residual"])
            for time_record in record["time_records"]
        )

    items = []
    vetoes = []
    h3_evidence = []
    setting_by_state: dict[int, list[dict[str, Any]]] = {}
    for result in payload["results"]:
        setting_by_state.setdefault(int(result["state_dim"]), []).append(result)
        parity = result["dense_streaming_parity"]
        comparator = result["known_contract_comparator"]
        veto_bad = (
            parity["max_abs_dense_streaming_particle_diff"] > 1.0e-4
            or parity["dense_column_residual"] > 1.0e-3
            or comparator["exact_thresholded_column_residual"] > 1.0e-3
        )
        if veto_bad:
            vetoes.append(
                f"state_dim={result['state_dim']} setting={result['setting']['label']}"
            )
        first = result["time_records"][0]
        second = result["time_records"][1] if len(result["time_records"]) > 1 else None
        h3_like = (
            first["pre_to_post_mean_l2"] < 1.0e-3
            and first["post_pre_cov_trace_ratio"] is not None
            and first["post_pre_cov_trace_ratio"] < 0.8
            and second is not None
            and abs(second["increment_delta_to_kalman"]) > abs(first["increment_delta_to_kalman"])
        )
        if h3_like:
            h3_evidence.append(
                f"state_dim={result['state_dim']} setting={result['setting']['label']}"
            )
        items.append(
            "state_dim="
            f"{result['state_dim']} setting={result['setting']['label']}: "
            f"total_delta={result['total_delta_to_kalman']:.6f}, "
            f"t0_pre_post_mean_l2={first['pre_to_post_mean_l2']:.3e}, "
            f"t0_post_pre_cov_trace_ratio={first['post_pre_cov_trace_ratio']:.6f}, "
            f"t1_increment_delta="
            f"{None if second is None else second['increment_delta_to_kalman']:.6f}, "
            f"parity_max_diff={parity['max_abs_dense_streaming_particle_diff']:.3e}, "
            f"dense_row_resid={parity['dense_row_residual']:.3e}, "
            f"max_time_row_resid={max_time_row_residual(result):.3e}, "
            f"dense_col_resid={parity['dense_column_residual']:.3e}, "
            f"known_contract_row_resid="
            f"{comparator['exact_thresholded_row_residual']:.3e}, "
            f"known_contract_iters={comparator['exact_thresholded_iterations']}."
        )

    h_items = []
    state_decisions = []
    for state_dim, records in setting_by_state.items():
        records = sorted(records, key=lambda item: int(item["setting"]["steps"]))
        by_steps = {int(record["setting"]["steps"]): record for record in records}
        highest_record = records[-1]
        best_row_record = min(records, key=max_time_row_residual)
        record100 = by_steps.get(100)
        record80 = by_steps.get(80)
        record100_all_time_row = (
            None if record100 is None else max_time_row_residual(record100)
        )
        record80_all_time_row = (
            None if record80 is None else max_time_row_residual(record80)
        )
        best_all_time_row = max_time_row_residual(best_row_record)
        high_budget_pass = best_all_time_row <= 1.0e-3
        comparator_record = record100 if record100 is not None else highest_record
        fixed100_row = comparator_record["known_contract_comparator"][
            "manual_fixed100_row_residual"
        ]
        known_contract_row = comparator_record["known_contract_comparator"][
            "exact_thresholded_row_residual"
        ]
        known_contract_pass = (
            math.isfinite(known_contract_row) and known_contract_row <= 1.0e-3
        )
        if high_budget_pass:
            label = "H1"
            state_decisions.append(
                f"state_dim={state_dim}: H1 under-converged finite Sinkhorn; high-budget all-time fixed-step row residual passed."
            )
        elif best_all_time_row > 1.0e-3:
            label = "mixed"
            state_decisions.append(
                f"state_dim={state_dim}: mixed H1/H2; low-step under-convergence is clear, but high-budget all-time row residual still failed."
            )
        elif fixed100_row > 1.0e-3 and known_contract_pass:
            label = "H4"
            state_decisions.append(
                f"state_dim={state_dim}: H4 manual finite route differs from thresholded annealed contract."
            )
        elif fixed100_row > 1.0e-3 and not known_contract_pass:
            label = "H2"
            state_decisions.append(
                f"state_dim={state_dim}: H2 transport normalization/formula remains live; both fixed-step and known-contract rows failed."
            )
        else:
            label = "mixed"
            state_decisions.append(
                f"state_dim={state_dim}: mixed outcome; inspect full ladder before patching."
            )
        if high_budget_pass and any(
            record["time_records"][0]["post_pre_cov_trace_ratio"] is not None
            and record["time_records"][0]["post_pre_cov_trace_ratio"] < 0.8
            for record in records
        ):
            state_decisions.append(
                f"state_dim={state_dim}: H3 also remains live because covariance contraction persists after a passing row residual."
            )
        row80_text = (
            "N/A"
            if record80 is None
            else f"{record80['dense_streaming_parity']['dense_row_residual']:.3e}"
        )
        row80_all_time_text = (
            "N/A" if record80_all_time_row is None else f"{record80_all_time_row:.3e}"
        )
        row100_all_time_text = (
            "N/A" if record100_all_time_row is None else f"{record100_all_time_row:.3e}"
        )
        h_items.append(
            f"state_dim={state_dim}: selected={label}, "
            f"row8={by_steps.get(8, records[0])['dense_streaming_parity']['dense_row_residual']:.3e}, "
            f"row80={row80_text}, "
            f"all_time_row80={row80_all_time_text}, "
            f"all_time_row100={row100_all_time_text}, "
            f"best_all_time_row={best_all_time_row:.3e} at "
            f"steps={best_row_record['setting']['steps']}, "
            f"fixed100_row={fixed100_row:.3e}, "
            f"known_contract_row={known_contract_row:.3e}."
        )
        if len(records) < 2:
            continue
        base = records[0]
        tighter = highest_record
        base_abs = abs(base["total_delta_to_kalman"])
        tight_abs = abs(tighter["total_delta_to_kalman"])
        if base_abs > 0.0:
            improvement = (base_abs - tight_abs) / base_abs
        else:
            improvement = 0.0
        base_ratio = base["time_records"][0]["post_pre_cov_trace_ratio"]
        tight_ratio = tighter["time_records"][0]["post_pre_cov_trace_ratio"]
        h_items.append(
            f"state_dim={state_dim}: steps {base['setting']['steps']}->"
            f"{tighter['setting']['steps']} total-delta improvement="
            f"{improvement:.3f}, t0 cov ratio {base_ratio:.6f}->{tight_ratio:.6f}."
        )

    if vetoes:
        decision = "VETO: dense/streaming parity, column mass, or known-contract column diagnostic failed."
        next_action = "Inspect transport application on the shared cloud before production-code patching."
        primary_status = f"FAIL veto diagnostics: {', '.join(vetoes)}"
    elif any("H4" in item for item in state_decisions):
        decision = "H4 is the recommended next target: manual finite route differs from the thresholded annealed contract."
        next_action = "Patch manual finite route parity with the thresholded annealed contract before changing row normalization."
        primary_status = "; ".join(state_decisions)
    elif any("H2" in item for item in state_decisions):
        decision = "H2 remains live: both fixed-step and known-contract row residuals failed."
        next_action = "Run a row-normalized diagnostic arm and inspect transport-from-potentials normalization before any production patch."
        primary_status = "; ".join(state_decisions)
    elif any("mixed H1/H2" in item for item in state_decisions):
        decision = "Mixed result: low-step transport is under-converged, but high-budget all-time row residuals still fail."
        next_action = "Run a focused worst-time row-residual budget diagnostic before changing production transport or the LGSSM statistical harness."
        primary_status = "; ".join(state_decisions)
    elif any("H1" in item for item in state_decisions):
        decision = "H1 is supported: the low-step LGSSM harness is under-converged and high-budget all-time row residuals pass."
        if h3_evidence or any("H3" in item for item in state_decisions):
            next_action = "Update the harness budget/gate only after a follow-up reset covariance diagnostic, because H3 remains live."
        else:
            next_action = "Update the LGSSM harness and finite-route validation to use a converged budget or convergence gate."
        primary_status = "; ".join(state_decisions)
    else:
        decision = "No single hypothesis is decisively supported by this diagnostic."
        next_action = "Inspect time records and add the smallest discriminating follow-up."
        primary_status = "AMBIGUOUS"
    items.extend(h_items)
    return (
        {
            "decision": decision,
            "primary_criterion_status": primary_status,
            "veto_diagnostic_status": "PASS" if not vetoes else "FAIL",
            "main_uncertainty": (
                "Whether tighter Sinkhorn changes the qualitative reset-moment pattern "
                "or merely attenuates the same barycentric contraction."
            ),
            "next_justified_action": next_action,
            "not_concluded": (
                "No gradient correctness, SIR correctness, HMC readiness, posterior "
                "correctness, production readiness, or broad scientific validity."
            ),
        },
        items,
    )


def _write_markdown(path: Path, payload: dict[str, Any]) -> None:
    def fmt(value: Any, format_spec: str) -> str:
        if value is None:
            return "N/A"
        return format(value, format_spec)

    lines = [
        "# LEDH-PFPF-OT LGSSM OT-Reset Moment Diagnostic Result",
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
        "time_steps",
        "xla",
        "device_scope",
        "cuda_visible_devices",
        "tf32_execution_enabled",
        "runtime_seconds",
    ):
        lines.append(f"| {key} | `{manifest.get(key)}` |")
    lines.extend(
        [
            "",
            "## Decision Table",
            "",
            "| Field | Status |",
            "|---|---|",
        ]
    )
    decision = payload["decision"]
    for key in (
        "decision",
        "primary_criterion_status",
        "veto_diagnostic_status",
        "main_uncertainty",
        "next_justified_action",
        "not_concluded",
    ):
        lines.append(f"| {key} | {decision[key]} |")

    lines.extend(
        [
            "",
            "## Summary",
            "",
            "| State dim | Setting | Total mean | Kalman | Delta | SD | MCSE | t0 cov ratio | t0 mean shift | t1 inc delta | Parity max diff | Dense col residual |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for result in payload["results"]:
        first = result["time_records"][0]
        second = result["time_records"][1] if len(result["time_records"]) > 1 else None
        parity = result["dense_streaming_parity"]
        lines.append(
            "| "
            f"{result['state_dim']} | {result['setting']['label']} | "
            f"{result['total_mean']:.6f} | {result['kalman_total']:.6f} | "
            f"{result['total_delta_to_kalman']:.6f} | "
            f"{result['total_sd']:.6f} | {result['total_mcse']:.6f} | "
            f"{first['post_pre_cov_trace_ratio']:.6f} | "
            f"{first['pre_to_post_mean_l2']:.3e} | "
            f"{fmt(None if second is None else second['increment_delta_to_kalman'], '.6f')} | "
            f"{parity['max_abs_dense_streaming_particle_diff']:.3e} | "
            f"{parity['dense_column_residual']:.3e} |"
        )
    lines.extend(
        [
            "",
            "## Known-Contract Comparator",
            "",
            "| State dim | Setting | Exact row residual | Exact col residual | Iterations | Manual fixed100 row residual | Manual fixed100 col residual | Max particle diff | Mean particle diff |",
            "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for result in payload["results"]:
        comparator = result["known_contract_comparator"]
        lines.append(
            "| "
            f"{result['state_dim']} | {result['setting']['label']} | "
            f"{comparator['exact_thresholded_row_residual']:.3e} | "
            f"{comparator['exact_thresholded_column_residual']:.3e} | "
            f"{comparator['exact_thresholded_iterations']} | "
            f"{comparator['manual_fixed100_row_residual']:.3e} | "
            f"{comparator['manual_fixed100_column_residual']:.3e} | "
            f"{comparator['max_abs_exact_thresholded_to_manual_fixed100_particle_diff']:.3e} | "
            f"{comparator['mean_abs_exact_thresholded_to_manual_fixed100_particle_diff']:.3e} |"
        )
    lines.extend(["", "## Per-Time Records", ""])
    for result in payload["results"]:
        lines.extend(
            [
                f"### state_dim={result['state_dim']}, setting={result['setting']['label']}",
                "",
                "| t | inc delta | next inc delta | prefix delta | pre trace | post trace | Kalman trace | post/pre trace | pre-post mean L2 | ESS mean | row residual |",
                "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for record in result["time_records"]:
            lines.append(
                "| "
                f"{record['time_index']} | "
                f"{record['increment_delta_to_kalman']:.6f} | "
                f"{fmt(record['next_increment_delta_to_kalman'], '.6f')} | "
                f"{record['prefix_delta_to_kalman']:.6f} | "
                f"{record['pre_ot_weighted_cov_trace']:.6f} | "
                f"{record['post_ot_uniform_cov_trace']:.6f} | "
                f"{record['kalman_filtered_cov_trace']:.6f} | "
                f"{record['post_pre_cov_trace_ratio']:.6f} | "
                f"{record['pre_to_post_mean_l2']:.3e} | "
                f"{record['ess_mean']:.3f} | "
                f"{record['transport_row_residual']:.3e} |"
            )
        lines.append("")

    lines.extend(["## Interpretation", ""])
    for item in payload["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = _parse_args()
    _configure_import_environment(args)
    start = time.perf_counter()
    harness = _load_harness()
    device_manifest = _configure_tensorflow(harness, args)
    results = []
    for state_dim in args.state_dims:
        for setting in args.settings:
            results.append(_run_state_setting(harness, state_dim, setting, args))
    runtime = time.perf_counter() - start
    payload = {
        "timestamp": _dt.datetime.now(_dt.UTC).isoformat(),
        "plan": PLAN_PATH,
        "source_harness": str(HARNESS_PATH.relative_to(ROOT)),
        "manifest": {
            "git_commit": _git_commit(),
            "command": " ".join(sys.argv),
            "output": str(args.output),
            "markdown_output": args.markdown_output,
            "python": sys.version,
            "platform": platform.platform(),
            "num_particles": int(args.num_particles),
            "dense_parity_particles": int(args.dense_parity_particles),
            "seed_count": int(args.seed_count),
            "time_steps": int(harness.TIME_STEPS),
            "state_dims": [int(value) for value in args.state_dims],
            "settings": args.settings,
            "xla": bool(args.xla),
            "shared_parity": bool(args.shared_parity),
            "known_contract_comparator": bool(args.known_contract_comparator),
            "tf32_mode": args.tf32_mode,
            "runtime_seconds": runtime,
            **device_manifest,
        },
        "results": results,
    }
    decision, interpretation = _interpret(payload)
    payload["decision"] = decision
    payload["interpretation"] = interpretation

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if args.markdown_output:
        markdown_path = Path(args.markdown_output)
        markdown_path.parent.mkdir(parents=True, exist_ok=True)
        _write_markdown(markdown_path, payload)


def _git_commit() -> str:
    head = ROOT / ".git" / "HEAD"
    try:
        text = head.read_text(encoding="utf-8").strip()
        if text.startswith("ref: "):
            ref = ROOT / ".git" / text.split(" ", maxsplit=1)[1]
            return ref.read_text(encoding="utf-8").strip()
        return text
    except OSError:
        return "unknown"


if __name__ == "__main__":
    main()
