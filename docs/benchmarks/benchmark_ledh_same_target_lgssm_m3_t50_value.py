"""Same-target LEDH-PFPF-OT value/score runner for the highdim LGSSM row.

This runner targets the existing leaderboard row
``benchmark_lgssm_exact_oracle_m3_T50`` with ``D=3``, ``T=50``, dataset seed
``81100``, and theta ``[0.72, 0.55, 0.35, 0.35, 0.45]``.  The admitted score
route is the compact no-autodiff forward-sensitivity derivative of the same
LEDH-PFPF-OT scalar computed by the value path.

It must not import ``benchmark_two_lane_highdim_leaderboard.py`` because that
module hides CUDA devices at import time.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import platform
import statistics
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

from bayesfilter.linear.kalman_tf import tf_kalman_log_likelihood
from bayesfilter.highdim.ledh_forward_contract import (
    make_lgssm_m3_t50_forward_contract,
)
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_streaming_tf as streaming_tf,
)
from experiments.dpf_implementation.tf_tfp.filters import (
    experimental_batched_ledh_pfpf_ot_tf as core_tf,
)
from experiments.dpf_implementation.tf_tfp.resampling import annealed_transport_tf
from scripts.filtering_value_gradient_benchmark_generate_p8_datasets import (
    _lgssm_benchmark_model,
    _lgssm_dataset,
)


ROW_ID = "benchmark_lgssm_exact_oracle_m3_T50"
DATASET_SEED = 81100
TRUTH_THETA = [0.72, 0.55, 0.35, 0.35, 0.45]
PARAMETER_NAMES = ("phi1", "phi2", "phi3", "q_scale", "r_scale")
FULL_ROW_BATCH_SEEDS = (81120, 81121, 81122, 81123, 81124)
FULL_ROW_NUM_PARTICLES = 1000
FULL_ROW_TIME_STEPS = 50
FULL_ROW_TRANSPORT_POLICY = "active-all"
FULL_ROW_SINKHORN_ITERATIONS = 10
FULL_ROW_SINKHORN_EPSILON = 0.5
STATE_DIM = 3
OBS_DIM = 3
DTYPE = tf.float32
HISTORICAL_MANUAL_SCORE_ROUTE_ID = (
    "historical_diagnostic_manual_reverse_scan_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot"
)
MANUAL_SCORE_ROUTE_ID = HISTORICAL_MANUAL_SCORE_ROUTE_ID
COMPACT_SCORE_ROUTE_ID = (
    "compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot"
)
SAME_SCALAR_ROUTE_ID = "same_target_lgssm_m3_t50_ledh_pfpf_ot_streaming_manual_total"
NONCLAIMS = (
    "not exact Kalman score evidence",
    "not HMC/NUTS readiness evidence",
    "not posterior correctness evidence",
    "not runtime-rankable against frozen non-LEDH rows",
    "not evidence for nonlinear rows",
)


def _parse_int_csv(value: str) -> list[int]:
    parsed = [item.strip() for item in str(value).split(",") if item.strip()]
    if not parsed:
        raise ValueError("expected at least one integer seed")
    return [int(item) for item in parsed]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--batch-seeds", default=",".join(str(seed) for seed in FULL_ROW_BATCH_SEEDS))
    parser.add_argument("--num-particles", type=int, default=FULL_ROW_NUM_PARTICLES)
    parser.add_argument("--time-steps", type=int, default=FULL_ROW_TIME_STEPS)
    parser.add_argument(
        "--transport-policy",
        choices=("active-all", "active-odd", "no-resampling"),
        default=FULL_ROW_TRANSPORT_POLICY,
    )
    parser.add_argument("--sinkhorn-iterations", type=int, default=FULL_ROW_SINKHORN_ITERATIONS)
    parser.add_argument("--sinkhorn-epsilon", type=float, default=FULL_ROW_SINKHORN_EPSILON)
    parser.add_argument("--annealed-scaling", type=float, default=0.9)
    parser.add_argument("--annealed-convergence-threshold", type=float, default=1.0e-3)
    parser.add_argument(
        "--transport-gradient-mode",
        choices=(
            "raw",
            core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
            core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE,
        ),
        default="raw",
    )
    parser.add_argument(
        "--transport-ad-mode",
        choices=("stabilized", "full"),
        default="stabilized",
    )
    parser.add_argument("--row-chunk-size", type=int, default=512)
    parser.add_argument("--col-chunk-size", type=int, default=512)
    parser.add_argument("--particle-chunk-size", type=int, default=256)
    parser.add_argument(
        "--score-mode",
        choices=("none", "compact-sensitivity", "manual-reverse"),
        default="none",
    )
    parser.add_argument("--score-fd-step", type=float, default=None)
    parser.add_argument("--score-fd-atol", type=float, default=5.0e-3)
    parser.add_argument("--score-fd-rtol", type=float, default=5.0e-3)
    parser.add_argument(
        "--history-mode",
        choices=("full", "value-only"),
        default="full",
    )
    parser.add_argument("--warmups", type=int, default=0)
    parser.add_argument("--repeats", type=int, default=1)
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
    parser.add_argument("--markdown-output", default=None)
    args = parser.parse_args()
    args.batch_seeds = _parse_int_csv(args.batch_seeds)
    if args.time_steps <= 0 or args.time_steps > FULL_ROW_TIME_STEPS:
        raise ValueError("time_steps must be in 1..50")
    if args.num_particles <= 1:
        raise ValueError("num_particles must be greater than one")
    if args.sinkhorn_iterations <= 0:
        raise ValueError("sinkhorn_iterations must be positive")
    if args.row_chunk_size <= 0 or args.col_chunk_size <= 0 or args.particle_chunk_size <= 0:
        raise ValueError("chunk sizes must be positive")
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be nonnegative and repeats must be positive")
    if args.score_mode in {"compact-sensitivity", "manual-reverse"}:
        if args.score_fd_step is None:
            args.score_fd_step = 1.0e-5 if args.dtype == "float64" else 1.0e-3
        if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
            raise ValueError(
                f"{args.score_mode} score requires "
                f"transport-gradient-mode={core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE}"
            )
        if args.transport_ad_mode != "full":
            raise ValueError(f"{args.score_mode} score requires transport-ad-mode=full")
        if args.score_fd_step <= 0.0:
            raise ValueError("score-fd-step must be positive")
    elif args.score_fd_step is None:
        args.score_fd_step = 1.0e-5 if args.dtype == "float64" else 1.0e-3
    return args


def _configure_precision(args: argparse.Namespace) -> dict[str, Any]:
    global DTYPE
    DTYPE = tf.float64 if args.dtype == "float64" else tf.float32
    core_tf.DTYPE = DTYPE
    streaming_tf.DTYPE = DTYPE
    annealed_transport_tf.DTYPE = DTYPE
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


def _seed_pair(seed: int, salt: tf.Tensor | int) -> tf.Tensor:
    salt_tensor = tf.cast(salt, tf.int32)
    return tf.stack(
        [
            tf.constant(int(seed) % 2147483647, dtype=tf.int32),
            tf.math.floormod(salt_tensor, tf.constant(2147483647, dtype=tf.int32)),
        ]
    )


def _summary(timings: list[float]) -> dict[str, float]:
    if not timings:
        return {}
    return {
        "min": min(timings),
        "median": statistics.median(timings),
        "mean": statistics.fmean(timings),
        "max": max(timings),
    }


def _sample_sd(values: list[float]) -> float | None:
    if len(values) < 2:
        return None
    mean = statistics.fmean(values)
    return math.sqrt(sum((value - mean) ** 2 for value in values) / (len(values) - 1))


def _validate_device(outputs: tuple[tf.Tensor, ...], expect_device_kind: str) -> list[str]:
    devices = [tensor.device for tensor in outputs]
    if expect_device_kind == "gpu":
        if not all("GPU" in device.upper() for device in devices):
            raise RuntimeError(f"expected GPU outputs, got {devices}")
    elif expect_device_kind == "cpu":
        if not all("CPU" in device.upper() for device in devices):
            raise RuntimeError(f"expected CPU outputs, got {devices}")
    return devices


def _materialize(*tensors: tf.Tensor) -> None:
    for tensor in tensors:
        tensor.numpy()


def _batched_gaussian_logpdf(residuals: tf.Tensor, covariance: tf.Tensor) -> tf.Tensor:
    residuals = tf.convert_to_tensor(residuals, dtype=DTYPE)
    covariance = tf.convert_to_tensor(covariance, dtype=DTYPE)
    chol = tf.linalg.cholesky(covariance)
    solved = tf.linalg.matrix_transpose(
        tf.linalg.cholesky_solve(chol, tf.linalg.matrix_transpose(residuals))
    )
    quad = tf.reduce_sum(solved * residuals, axis=-1)
    logdet = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(chol)), axis=-1)
    dim = tf.cast(residuals.shape[-1], DTYPE)
    return -0.5 * (
        dim * tf.math.log(tf.constant(2.0 * math.pi, dtype=DTYPE))
        + logdet[:, None]
        + quad
    )


def _batched_gaussian_logpdf_jvp(
    residuals: tf.Tensor,
    covariance: tf.Tensor,
    d_residuals: tf.Tensor,
    d_covariance: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    residuals = tf.convert_to_tensor(residuals, dtype=DTYPE)
    covariance = tf.convert_to_tensor(covariance, dtype=DTYPE)
    d_residuals = tf.convert_to_tensor(d_residuals, dtype=DTYPE)
    d_covariance = tf.convert_to_tensor(d_covariance, dtype=DTYPE)
    chol = tf.linalg.cholesky(covariance)
    precision = tf.linalg.cholesky_solve(
        chol,
        tf.eye(int(covariance.shape[-1]), dtype=DTYPE)[tf.newaxis, :, :],
    )
    solved = tf.einsum("bij,bnj->bni", precision, residuals)
    value = _batched_gaussian_logpdf(residuals, covariance)
    precision_residual_outer = tf.einsum("bni,bnj->bnij", solved, solved)
    covariance_bar_per_particle = 0.5 * (
        precision_residual_outer - precision[:, tf.newaxis, :, :]
    )
    tangent = (
        -tf.reduce_sum(solved[:, :, :, tf.newaxis] * d_residuals, axis=2)
        + tf.reduce_sum(
            covariance_bar_per_particle[:, :, :, :, tf.newaxis]
            * d_covariance[:, tf.newaxis, :, :, :],
            axis=[2, 3],
        )
    )
    return value, tangent


def _normalize_log_weights_jvp(
    corrected_log_weights: tf.Tensor,
    d_corrected_log_weights: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    corrected_log_weights = tf.convert_to_tensor(corrected_log_weights, dtype=DTYPE)
    d_corrected_log_weights = tf.convert_to_tensor(d_corrected_log_weights, dtype=DTYPE)
    weights, incremental = core_tf._normalize_log_weights(corrected_log_weights)  # noqa: SLF001
    d_incremental = tf.reduce_sum(weights[:, :, None] * d_corrected_log_weights, axis=1)
    normalized_log_weights = tf.math.log(
        tf.maximum(weights, core_tf._log_weight_floor())  # noqa: SLF001
    )
    floor_active = weights <= core_tf._log_weight_floor()  # noqa: SLF001
    d_normalized = tf.where(
        floor_active[:, :, None],
        tf.zeros_like(d_corrected_log_weights),
        d_corrected_log_weights - d_incremental[:, None, :],
    )
    return normalized_log_weights, d_normalized, incremental, d_incremental


def _cholesky_jvp_matrix(matrix: tf.Tensor, d_matrix: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
    matrix = tf.convert_to_tensor(matrix, dtype=DTYPE)
    d_matrix = tf.convert_to_tensor(d_matrix, dtype=DTYPE)
    chol = tf.linalg.cholesky(matrix)
    tangent_columns = []
    param_dim = int(d_matrix.shape[-1])
    for index in range(param_dim):
        tangent = d_matrix[..., index]
        inner = tf.linalg.triangular_solve(
            chol,
            tangent,
            lower=True,
        )
        inner = tf.linalg.triangular_solve(
            chol,
            tf.linalg.matrix_transpose(inner),
            lower=True,
        )
        inner = tf.linalg.matrix_transpose(inner)
        lower = tf.linalg.band_part(inner, -1, 0)
        diag = tf.linalg.diag(tf.linalg.diag_part(lower) * 0.5)
        phi = lower - tf.linalg.diag(tf.linalg.diag_part(lower)) + diag
        tangent_columns.append(tf.matmul(chol, phi))
    return chol, tf.stack(tangent_columns, axis=-1)


def _lgssm_component_tangents(theta: tf.Tensor, batch_size: int) -> dict[str, tf.Tensor]:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])
    phi = theta[:3]
    q_scale = theta[3]
    r_scale = theta[4]
    param_dim = len(PARAMETER_NAMES)
    eye_state = tf.eye(STATE_DIM, dtype=DTYPE)
    eye_obs = tf.eye(OBS_DIM, dtype=DTYPE)
    d_transition_matrix_single = tf.stack(
        [tf.linalg.diag(tf.one_hot(index, STATE_DIM, dtype=DTYPE)) for index in range(STATE_DIM)]
        + [tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE), tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE)],
        axis=-1,
    )
    d_transition_covariance_single = tf.stack(
        [
            tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE),
            tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE),
            tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE),
            2.0 * q_scale * eye_state,
            tf.zeros([STATE_DIM, STATE_DIM], dtype=DTYPE),
        ],
        axis=-1,
    )
    d_observation_covariance_single = tf.stack(
        [
            tf.zeros([OBS_DIM, OBS_DIM], dtype=DTYPE),
            tf.zeros([OBS_DIM, OBS_DIM], dtype=DTYPE),
            tf.zeros([OBS_DIM, OBS_DIM], dtype=DTYPE),
            tf.zeros([OBS_DIM, OBS_DIM], dtype=DTYPE),
            2.0 * r_scale * eye_obs,
        ],
        axis=-1,
    )
    initial_std = q_scale / tf.sqrt(1.0 - tf.square(phi))
    d_initial_std = tf.zeros([STATE_DIM, param_dim], dtype=DTYPE)
    phi_derivative = q_scale * phi / tf.pow(1.0 - tf.square(phi), 1.5)
    d_initial_std += tf.concat(
        [
            tf.linalg.diag(phi_derivative),
            tf.zeros([STATE_DIM, 2], dtype=DTYPE),
        ],
        axis=1,
    )
    q_derivative = 1.0 / tf.sqrt(1.0 - tf.square(phi))
    d_initial_std += tf.concat(
        [
            tf.zeros([STATE_DIM, 3], dtype=DTYPE),
            q_derivative[:, None],
            tf.zeros([STATE_DIM, 1], dtype=DTYPE),
        ],
        axis=1,
    )
    d_transition_scale = tf.constant([0.0, 0.0, 0.0, 1.0, 0.0], dtype=DTYPE)
    return {
        "d_transition_matrix": tf.tile(
            d_transition_matrix_single[tf.newaxis, :, :, :],
            [batch_size, 1, 1, 1],
        ),
        "d_transition_covariance": tf.tile(
            d_transition_covariance_single[tf.newaxis, :, :, :],
            [batch_size, 1, 1, 1],
        ),
        "d_observation_covariance": tf.tile(
            d_observation_covariance_single[tf.newaxis, :, :, :],
            [batch_size, 1, 1, 1],
        ),
        "d_initial_std": d_initial_std,
        "d_transition_scale": d_transition_scale,
    }


def _lgssm_components(theta: tf.Tensor, batch_size: int) -> dict[str, tf.Tensor]:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])
    phi = theta[:3]
    q_scale = theta[3]
    r_scale = theta[4]
    eye_state = tf.eye(STATE_DIM, dtype=DTYPE)
    eye_obs = tf.eye(OBS_DIM, dtype=DTYPE)
    observation_matrix = tf.constant(
        [
            [1.0, 0.25, -0.15],
            [0.2, 1.1, 0.3],
            [-0.1, 0.35, 0.9],
        ],
        dtype=DTYPE,
    )
    transition_matrix_single = tf.linalg.diag(phi)
    transition_covariance_single = tf.square(q_scale) * eye_state
    observation_covariance_single = tf.square(r_scale) * eye_obs
    initial_std = q_scale / tf.sqrt(1.0 - tf.square(phi))
    transition_chol_single = q_scale * eye_state
    return {
        "theta": theta,
        "phi": phi,
        "q_scale": q_scale,
        "r_scale": r_scale,
        "initial_std": initial_std,
        "transition_matrix_single": transition_matrix_single,
        "transition_covariance_single": transition_covariance_single,
        "observation_matrix": observation_matrix,
        "observation_covariance_single": observation_covariance_single,
        "transition_chol_single": transition_chol_single,
        "transition_matrix": tf.tile(
            transition_matrix_single[tf.newaxis, :, :],
            [batch_size, 1, 1],
        ),
        "transition_covariance": tf.tile(
            transition_covariance_single[tf.newaxis, :, :],
            [batch_size, 1, 1],
        ),
        "observation_covariance": tf.tile(
            observation_covariance_single[tf.newaxis, :, :],
            [batch_size, 1, 1],
        ),
    }


def _filterflow_epsilon_start_vjp(
    scaled_x: tf.Tensor,
    d_epsilon0: tf.Tensor,
) -> tf.Tensor:
    scaled_x = tf.convert_to_tensor(scaled_x, dtype=DTYPE)
    d_epsilon0 = tf.reshape(tf.convert_to_tensor(d_epsilon0, dtype=DTYPE), [-1])
    max_value = tf.reduce_max(scaled_x, axis=[1, 2])
    min_value = tf.reduce_min(scaled_x, axis=[1, 2])
    coordinate_range = max_value - min_value
    active = tf.cast(
        coordinate_range * coordinate_range >= tf.constant(1.0e-6, DTYPE),
        DTYPE,
    )
    max_mask = tf.cast(scaled_x == max_value[:, None, None], DTYPE)
    min_mask = tf.cast(scaled_x == min_value[:, None, None], DTYPE)
    max_count = tf.reduce_sum(max_mask, axis=[1, 2], keepdims=True)
    min_count = tf.reduce_sum(min_mask, axis=[1, 2], keepdims=True)
    common = 2.0 * coordinate_range * d_epsilon0 * active
    return (
        common[:, None, None] * max_mask / max_count
        - common[:, None, None] * min_mask / min_count
    )


def _filterflow_scale_vjp(
    particles: tf.Tensor,
    d_scale: tf.Tensor,
) -> tf.Tensor:
    particles = tf.convert_to_tensor(particles, dtype=DTYPE)
    d_scale = tf.reshape(tf.convert_to_tensor(d_scale, dtype=DTYPE), [-1])
    num_particles = tf.cast(tf.shape(particles)[1], DTYPE)
    dimension = tf.cast(tf.shape(particles)[2], DTYPE)
    mean = tf.reduce_mean(particles, axis=1, keepdims=True)
    centered = particles - mean
    variance = tf.reduce_mean(centered * centered, axis=1)
    std = tf.sqrt(variance)
    diameter = tf.reduce_max(std, axis=1)
    active_diameter = tf.cast(diameter != 0.0, DTYPE)
    max_mask = tf.cast(std == diameter[:, None], DTYPE)
    max_count = tf.reduce_sum(max_mask, axis=1, keepdims=True)
    d_std = (
        d_scale[:, None]
        * tf.sqrt(dimension)
        * active_diameter[:, None]
        * max_mask
        / max_count
    )
    safe_std = tf.where(std > 0.0, std, tf.ones_like(std))
    d_variance = tf.where(std > 0.0, d_std / (2.0 * safe_std), tf.zeros_like(d_std))
    return (2.0 / num_particles) * centered * d_variance[:, None, :]


def _filterflow_scale_jvp(
    particles: tf.Tensor,
    d_particles: tf.Tensor,
) -> tf.Tensor:
    particles = tf.convert_to_tensor(particles, dtype=DTYPE)
    d_particles = tf.convert_to_tensor(d_particles, dtype=DTYPE)
    num_particles = tf.cast(tf.shape(particles)[1], DTYPE)
    dimension = tf.cast(tf.shape(particles)[2], DTYPE)
    mean = tf.reduce_mean(particles, axis=1, keepdims=True)
    d_mean = tf.reduce_mean(d_particles, axis=1, keepdims=True)
    centered = particles - mean
    d_centered = d_particles - d_mean
    variance = tf.reduce_mean(centered * centered, axis=1)
    d_variance = (2.0 / num_particles) * tf.reduce_sum(
        centered[:, :, :, None] * d_centered,
        axis=1,
    )
    std = tf.sqrt(variance)
    safe_std = tf.where(std > 0.0, std, tf.ones_like(std))
    d_std = tf.where(
        std[:, :, None] > 0.0,
        d_variance / (2.0 * safe_std[:, :, None]),
        tf.zeros_like(d_variance),
    )
    diameter = tf.reduce_max(std, axis=1)
    max_mask = tf.cast(std == diameter[:, None], DTYPE)
    max_count = tf.reduce_sum(max_mask, axis=1, keepdims=True)
    d_diameter = tf.reduce_sum(
        d_std * max_mask[:, :, None] / max_count[:, :, None],
        axis=1,
    )
    active = tf.cast(diameter != 0.0, DTYPE)
    return tf.sqrt(dimension) * d_diameter * active[:, None]


def _filterflow_epsilon_start_jvp(
    scaled_x: tf.Tensor,
    d_scaled_x: tf.Tensor,
) -> tf.Tensor:
    scaled_x = tf.convert_to_tensor(scaled_x, dtype=DTYPE)
    d_scaled_x = tf.convert_to_tensor(d_scaled_x, dtype=DTYPE)
    max_value = tf.reduce_max(scaled_x, axis=[1, 2])
    min_value = tf.reduce_min(scaled_x, axis=[1, 2])
    coordinate_range = max_value - min_value
    max_mask = tf.cast(scaled_x == max_value[:, None, None], DTYPE)
    min_mask = tf.cast(scaled_x == min_value[:, None, None], DTYPE)
    max_count = tf.reduce_sum(max_mask, axis=[1, 2], keepdims=True)
    min_count = tf.reduce_sum(min_mask, axis=[1, 2], keepdims=True)
    d_max = tf.reduce_sum(
        d_scaled_x * max_mask[:, :, :, None] / max_count[:, :, :, None],
        axis=[1, 2],
    )
    d_min = tf.reduce_sum(
        d_scaled_x * min_mask[:, :, :, None] / min_count[:, :, :, None],
        axis=[1, 2],
    )
    active = tf.cast(
        coordinate_range * coordinate_range >= tf.constant(1.0e-6, DTYPE),
        DTYPE,
    )
    return 2.0 * coordinate_range[:, None] * (d_max - d_min) * active[:, None]


def _scaled_centered_particles_vjp(
    particles: tf.Tensor,
    center: tf.Tensor,
    scale: tf.Tensor,
    d_scaled_x: tf.Tensor,
) -> tf.Tensor:
    particles = tf.convert_to_tensor(particles, dtype=DTYPE)
    scale = tf.reshape(tf.convert_to_tensor(scale, dtype=DTYPE), [-1])
    d_scaled_x = tf.convert_to_tensor(d_scaled_x, dtype=DTYPE)
    centered = particles - center
    d_centered = d_scaled_x / scale[:, None, None]
    d_scale = -tf.reduce_sum(
        d_scaled_x * centered / (scale[:, None, None] * scale[:, None, None]),
        axis=[1, 2],
    )
    return (
        d_centered
        - tf.reduce_mean(d_centered, axis=1, keepdims=True)
        + _filterflow_scale_vjp(particles, d_scale)
    )


def _manual_forward_transport_tf(
    *,
    post_flow: tf.Tensor,
    normalized_log_weights: tf.Tensor,
    mask: tf.Tensor,
    args: argparse.Namespace,
) -> tuple[tf.Tensor, tf.Tensor]:
    if args.transport_policy == "no-resampling":
        return post_flow, normalized_log_weights
    if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise ValueError("manual LGSSM score requires manual streaming finite transport")
    if args.transport_ad_mode != "full":
        raise ValueError("manual LGSSM score requires transport_ad_mode='full'")
    batch_size, num_particles, _state_dim = core_tf._static_shape(  # noqa: SLF001
        post_flow,
        "post_flow",
    )
    center = tf.reduce_mean(post_flow, axis=1, keepdims=True)
    scale = annealed_transport_tf._filterflow_scale(post_flow)  # noqa: SLF001
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon = tf.convert_to_tensor(args.sinkhorn_epsilon, dtype=DTYPE)
    epsilon0 = annealed_transport_tf._filterflow_epsilon_start(scaled_x)  # noqa: SLF001
    scaling = tf.convert_to_tensor(args.annealed_scaling, dtype=DTYPE)
    steps = core_tf._manual_dense_finite_steps(args.sinkhorn_iterations)  # noqa: SLF001
    transported, _row_residual = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_total_vjp(  # noqa: SLF001
            scaled_x,
            post_flow,
            normalized_log_weights,
            epsilon,
            epsilon0,
            scaling,
            steps=steps,
            row_chunk_size=args.row_chunk_size,
            col_chunk_size=args.col_chunk_size,
        )
    )
    uniform_log_weights = core_tf.uniform_log_weights(batch_size, num_particles)
    next_particles = tf.where(mask[:, None, None], transported, post_flow)
    next_log_weights = tf.where(mask[:, None], uniform_log_weights, normalized_log_weights)
    return next_particles, next_log_weights


def _compact_forward_transport_jvp_tf(
    *,
    post_flow: tf.Tensor,
    normalized_log_weights: tf.Tensor,
    d_post_flow: tf.Tensor,
    d_normalized_log_weights: tf.Tensor,
    mask: tf.Tensor,
    args: argparse.Namespace,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor, tf.Tensor]:
    if args.transport_policy == "no-resampling":
        return post_flow, normalized_log_weights, d_post_flow, d_normalized_log_weights
    if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise ValueError("compact LGSSM score requires manual streaming finite transport")
    if args.transport_ad_mode != "full":
        raise ValueError("compact LGSSM score requires transport_ad_mode='full'")
    batch_size, num_particles, _state_dim = core_tf._static_shape(  # noqa: SLF001
        post_flow,
        "post_flow",
    )
    center = tf.reduce_mean(post_flow, axis=1, keepdims=True)
    d_center = tf.reduce_mean(d_post_flow, axis=1, keepdims=True)
    scale = annealed_transport_tf._filterflow_scale(post_flow)  # noqa: SLF001
    d_scale = _filterflow_scale_jvp(post_flow, d_post_flow)
    scaled_x = (post_flow - center) / scale[:, None, None]
    d_scaled_x = (
        (d_post_flow - d_center) / scale[:, None, None, None]
        - (post_flow - center)[:, :, :, None]
        * d_scale[:, None, None, :]
        / (scale[:, None, None, None] * scale[:, None, None, None])
    )
    epsilon = tf.convert_to_tensor(args.sinkhorn_epsilon, dtype=DTYPE)
    epsilon0 = annealed_transport_tf._filterflow_epsilon_start(scaled_x)  # noqa: SLF001
    d_epsilon0 = _filterflow_epsilon_start_jvp(scaled_x, d_scaled_x)
    scaling = tf.convert_to_tensor(args.annealed_scaling, dtype=DTYPE)
    steps = core_tf._manual_dense_finite_steps(args.sinkhorn_iterations)  # noqa: SLF001
    transported, d_transported, _row_residual = (
        annealed_transport_tf._filterflow_manual_streaming_finite_transport_value_and_jvp_total(  # noqa: SLF001
            scaled_x,
            post_flow,
            normalized_log_weights,
            d_scaled_x,
            d_post_flow,
            d_normalized_log_weights,
            d_epsilon0,
            epsilon,
            epsilon0,
            scaling,
            steps=steps,
            row_chunk_size=args.row_chunk_size,
            col_chunk_size=args.col_chunk_size,
        )
    )
    uniform_log_weights = core_tf.uniform_log_weights(batch_size, num_particles)
    d_uniform = tf.zeros_like(d_normalized_log_weights)
    next_particles = tf.where(mask[:, None, None], transported, post_flow)
    next_log_weights = tf.where(mask[:, None], uniform_log_weights, normalized_log_weights)
    next_d_particles = tf.where(mask[:, None, None, None], d_transported, d_post_flow)
    next_d_log_weights = tf.where(
        mask[:, None, None],
        d_uniform,
        d_normalized_log_weights,
    )
    return next_particles, next_log_weights, next_d_particles, next_d_log_weights


def _manual_transport_vjp_tf(
    *,
    post_flow: tf.Tensor,
    normalized_log_weights: tf.Tensor,
    mask: tf.Tensor,
    args: argparse.Namespace,
    upstream_particles: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    if args.transport_policy == "no-resampling":
        return tf.zeros_like(post_flow), tf.zeros_like(normalized_log_weights)
    if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise ValueError("manual LGSSM score requires manual streaming finite transport")
    if args.transport_ad_mode != "full":
        raise ValueError("manual LGSSM score requires transport_ad_mode='full'")
    active_upstream = tf.where(
        mask[:, None, None],
        upstream_particles,
        tf.zeros_like(upstream_particles),
    )
    center = tf.reduce_mean(post_flow, axis=1, keepdims=True)
    scale = annealed_transport_tf._filterflow_scale(post_flow)  # noqa: SLF001
    scaled_x = (post_flow - center) / scale[:, None, None]
    epsilon = tf.convert_to_tensor(args.sinkhorn_epsilon, dtype=DTYPE)
    epsilon0 = annealed_transport_tf._filterflow_epsilon_start(scaled_x)  # noqa: SLF001
    scaling = tf.convert_to_tensor(args.annealed_scaling, dtype=DTYPE)
    steps = core_tf._manual_dense_finite_steps(args.sinkhorn_iterations)  # noqa: SLF001
    (
        d_scaled_x,
        d_particles,
        d_logw,
        d_epsilon0,
    ) = annealed_transport_tf._filterflow_manual_streaming_finite_transport_total_pullback(  # noqa: SLF001
        scaled_x,
        post_flow,
        normalized_log_weights,
        epsilon,
        epsilon0,
        scaling,
        active_upstream,
        steps=steps,
        row_chunk_size=args.row_chunk_size,
        col_chunk_size=args.col_chunk_size,
    )
    d_scaled_x += _filterflow_epsilon_start_vjp(scaled_x, d_epsilon0)
    d_post_flow = d_particles + _scaled_centered_particles_vjp(
        post_flow,
        center,
        scale,
        d_scaled_x,
    )
    return d_post_flow, d_logw


def _make_fixed_resampling_mask(batch_size: int, time_steps: int, policy: str) -> tf.Tensor:
    if policy == "active-all":
        return tf.ones([batch_size, time_steps], dtype=tf.bool)
    if policy == "active-odd":
        active = tf.equal(tf.math.floormod(tf.range(time_steps), 2), 1)
        return tf.tile(active[tf.newaxis, :], [batch_size, 1])
    return tf.zeros([batch_size, time_steps], dtype=tf.bool)


def _exact_kalman_value(observations: tf.Tensor) -> float:
    model = _lgssm_benchmark_model()
    value = tf_kalman_log_likelihood(
        observations=tf.convert_to_tensor(observations, dtype=tf.float64),
        transition_offset=model.transition_offset,
        transition_matrix=model.transition_matrix,
        transition_covariance=model.transition_covariance,
        observation_offset=model.observation_offset,
        observation_matrix=model.observation_matrix,
        observation_covariance=model.observation_covariance,
        initial_state_mean=model.initial_mean,
        initial_state_covariance=model.initial_covariance,
    )
    return float(value.numpy())


def _build_lgssm_tensors(args: argparse.Namespace) -> tuple[dict[str, tf.Tensor], dict[str, Any]]:
    dataset = _lgssm_dataset(DATASET_SEED)
    model = _lgssm_benchmark_model()
    observations64 = tf.convert_to_tensor(dataset["observations"], dtype=tf.float64)[: args.time_steps]
    batch_size = len(args.batch_seeds)
    full_leaderboard_row = (
        tuple(args.batch_seeds) == FULL_ROW_BATCH_SEEDS
        and args.num_particles == FULL_ROW_NUM_PARTICLES
        and args.time_steps == FULL_ROW_TIME_STEPS
        and args.transport_policy == FULL_ROW_TRANSPORT_POLICY
        and args.sinkhorn_iterations == FULL_ROW_SINKHORN_ITERATIONS
        and math.isclose(
            float(args.sinkhorn_epsilon),
            FULL_ROW_SINKHORN_EPSILON,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )
    )
    transition_matrix = tf.cast(model.transition_matrix, DTYPE)
    transition_covariance = tf.cast(model.transition_covariance, DTYPE)
    observation_matrix = tf.cast(model.observation_matrix, DTYPE)
    observation_covariance = tf.cast(model.observation_covariance, DTYPE)
    initial_chol = tf.linalg.cholesky(tf.cast(model.initial_covariance, DTYPE))
    transition_chol = tf.linalg.cholesky(transition_covariance)
    initial_mean = tf.cast(model.initial_mean, DTYPE)

    initial_particles = tf.stack(
        [
            initial_mean
            + tf.random.stateless_normal(
                [args.num_particles, STATE_DIM],
                seed=_seed_pair(seed, 100),
                dtype=DTYPE,
            )
            @ tf.transpose(initial_chol)
            for seed in args.batch_seeds
        ],
        axis=0,
    )
    tensors = {
        "observations": tf.cast(observations64, DTYPE),
        "initial_particles": initial_particles,
        "fixed_resampling_mask": _make_fixed_resampling_mask(
            batch_size,
            args.time_steps,
            args.transport_policy,
        ),
        "transition_matrix": tf.tile(transition_matrix[tf.newaxis, :, :], [batch_size, 1, 1]),
        "transition_covariance": tf.tile(
            transition_covariance[tf.newaxis, :, :],
            [batch_size, 1, 1],
        ),
        "observation_covariance": tf.tile(
            observation_covariance[tf.newaxis, :, :],
            [batch_size, 1, 1],
        ),
        "observation_matrix": observation_matrix,
        "transition_chol": transition_chol,
    }
    exact_total_value = _exact_kalman_value(observations64)
    exact_average_value = exact_total_value / float(args.time_steps)
    forward_contract = make_lgssm_m3_t50_forward_contract(
        truth_theta=TRUTH_THETA,
        time_steps=args.time_steps,
        num_particles=args.num_particles,
        batch_seeds=args.batch_seeds,
        full_leaderboard_row=full_leaderboard_row,
    ).to_manifest()
    target_identity = {
        "row_id": ROW_ID,
        "row_scope": "main_observed_data_filtering_row",
        "forward_contract": forward_contract,
        "target_scalar": forward_contract["target_scalar"],
        "target_output_tensor_field": forward_contract["output_tensor_field"],
        "target_density_fields": forward_contract["target_density_fields"],
        "proposal_flow_fields": forward_contract["proposal_flow_fields"],
        "correction_formula": forward_contract["correction_formula"],
        "dataset_seed": DATASET_SEED,
        "truth_theta": list(TRUTH_THETA),
        "time_steps": args.time_steps,
        "num_particles": args.num_particles,
        "batch_seeds": [int(seed) for seed in args.batch_seeds],
        "transport_policy": args.transport_policy,
        "sinkhorn_iterations": args.sinkhorn_iterations,
        "sinkhorn_epsilon": args.sinkhorn_epsilon,
        "full_row_expected": {
            "batch_seeds": list(FULL_ROW_BATCH_SEEDS),
            "num_particles": FULL_ROW_NUM_PARTICLES,
            "time_steps": FULL_ROW_TIME_STEPS,
            "transport_policy": FULL_ROW_TRANSPORT_POLICY,
            "sinkhorn_iterations": FULL_ROW_SINKHORN_ITERATIONS,
            "sinkhorn_epsilon": FULL_ROW_SINKHORN_EPSILON,
        },
        "state_dim": STATE_DIM,
        "obs_dim": OBS_DIM,
        "full_leaderboard_row": full_leaderboard_row,
        "same_target_status": (
            "same_target_ledh_value_score_capable"
            if full_leaderboard_row
            else "prefix_diagnostic_not_full_leaderboard_row"
        ),
        "dataset_source": (
            "scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:"
            "_lgssm_dataset"
        ),
        "model_source": (
            "scripts/filtering_value_gradient_benchmark_generate_p8_datasets.py:"
            "_lgssm_benchmark_model"
        ),
        "exact_value_comparator": "tf_kalman_log_likelihood on same observations/model",
        "exact_total_log_likelihood": exact_total_value,
        "exact_average_log_likelihood": exact_average_value,
        "score_status": "not_run_score_mode_none",
    }
    return tensors, target_identity


def _build_lgssm_manual_tensors(args: argparse.Namespace, theta: tf.Tensor) -> dict[str, tf.Tensor]:
    dataset = _lgssm_dataset(DATASET_SEED)
    observations64 = tf.convert_to_tensor(dataset["observations"], dtype=tf.float64)[: args.time_steps]
    batch_size = len(args.batch_seeds)
    components = _lgssm_components(theta, batch_size)
    initial_particles = tf.stack(
        [
            tf.random.stateless_normal(
                [args.num_particles, STATE_DIM],
                seed=_seed_pair(seed, 100),
                dtype=DTYPE,
            )
            * components["initial_std"][tf.newaxis, :]
            for seed in args.batch_seeds
        ],
        axis=0,
    )
    transition_noise = tf.stack(
        [
            tf.stack(
                [
                    tf.random.stateless_normal(
                        [args.num_particles, STATE_DIM],
                        seed=_seed_pair(
                            seed,
                            tf.constant(1000, dtype=tf.int32) + tf.constant(t, dtype=tf.int32),
                        ),
                        dtype=DTYPE,
                    )
                    for t in range(args.time_steps)
                ],
                axis=0,
            )
            for seed in args.batch_seeds
        ],
        axis=0,
    )
    return {
        "observations": tf.cast(observations64, DTYPE),
        "initial_particles": initial_particles,
        "initial_noise": initial_particles / components["initial_std"][tf.newaxis, tf.newaxis, :],
        "transition_noise": transition_noise,
        "fixed_resampling_mask": _make_fixed_resampling_mask(
            batch_size,
            args.time_steps,
            args.transport_policy,
        ),
    }


def _lgssm_theta_score(
    *,
    theta: tf.Tensor,
    bar_initial_particles: tf.Tensor,
    initial_noise: tf.Tensor,
    transition_noise: tf.Tensor,
    bar_transition_noise_scale: tf.Tensor,
    bar_transition_matrix: tf.Tensor,
    bar_transition_covariance: tf.Tensor,
    bar_observation_covariance: tf.Tensor,
) -> tf.Tensor:
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])
    phi = theta[:3]
    q_scale = theta[3]
    r_scale = theta[4]
    initial_std = q_scale / tf.sqrt(1.0 - tf.square(phi))
    d_initial_std_d_phi = q_scale * phi / tf.pow(1.0 - tf.square(phi), 1.5)
    d_initial_std_d_q = 1.0 / tf.sqrt(1.0 - tf.square(phi))
    phi_score = tf.reduce_sum(
        bar_initial_particles * initial_noise * d_initial_std_d_phi[None, None, :],
        axis=1,
    )
    diag_transition_matrix_bar = tf.linalg.diag_part(bar_transition_matrix)
    phi_score += diag_transition_matrix_bar
    q_score = tf.reduce_sum(
        bar_initial_particles * initial_noise * d_initial_std_d_q[None, None, :],
        axis=[1, 2],
    )
    q_score += tf.reduce_sum(bar_transition_noise_scale * transition_noise, axis=[1, 2])
    q_score += 2.0 * q_scale * tf.linalg.trace(bar_transition_covariance)
    r_score = 2.0 * r_scale * tf.linalg.trace(bar_observation_covariance)
    return tf.stack(
        [
            phi_score[:, 0],
            phi_score[:, 1],
            phi_score[:, 2],
            q_score,
            r_score,
        ],
        axis=1,
    )


def _manual_value_and_score_from_components(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta: tf.Tensor,
) -> dict[str, tf.Tensor]:
    if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise ValueError("manual LGSSM score requires manual streaming finite transport")
    if args.transport_ad_mode != "full":
        raise ValueError("manual LGSSM score requires transport_ad_mode='full'")
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])
    observations = tf.convert_to_tensor(tensors["observations"], dtype=DTYPE)
    fixed_resampling_mask = tf.convert_to_tensor(tensors["fixed_resampling_mask"], dtype=tf.bool)
    initial_particles = tf.convert_to_tensor(tensors["initial_particles"], dtype=DTYPE)
    initial_noise = tf.convert_to_tensor(tensors["initial_noise"], dtype=DTYPE)
    transition_noise = tf.convert_to_tensor(tensors["transition_noise"], dtype=DTYPE)
    batch_size, num_particles, state_dim = core_tf._static_shape(  # noqa: SLF001
        initial_particles,
        "initial_particles",
    )
    time_steps_tensor = tf.shape(observations)[0]
    components = _lgssm_components(theta, batch_size)
    transition_matrix = components["transition_matrix"]
    transition_covariance = components["transition_covariance"]
    observation_covariance = components["observation_covariance"]
    observation_matrix = components["observation_matrix"]
    transition_chol = components["transition_chol_single"]
    transition_scale = components["q_scale"]
    h_jac_full = tf.tile(
        observation_matrix[tf.newaxis, tf.newaxis, :, :],
        [batch_size, num_particles, 1, 1],
    )

    scalar_keys = (
        "ancestors",
        "prior_means",
        "pre_flow",
        "post_flow",
        "predicted_observation",
        "observation",
        "corrected_log_weights",
        "normalized_log_weights",
        "transition_noise",
    )
    bool_keys = ("mask",)
    flow_keys = (
        "x0",
        "prior_means",
        "observation_jacobian",
        "observation_residual",
        "transition_covariance",
        "observation_covariance",
        "transition_covariance_stable",
        "observation_covariance_stable",
        "prior_chol",
        "prior_precision",
        "obs_precision",
        "pseudo_observation",
        "post_precision",
        "post_precision_stable",
        "post_covariance_unstabilized",
        "post_covariance",
        "post_chol",
        "prior_inv",
        "affine_transform",
        "delta",
        "info",
    )
    scalar_tas = {
        key: tf.TensorArray(DTYPE, size=time_steps_tensor, infer_shape=False)
        for key in scalar_keys
    }
    bool_tas = {
        key: tf.TensorArray(tf.bool, size=time_steps_tensor, infer_shape=False)
        for key in bool_keys
    }
    flow_tas = {
        key: tf.TensorArray(DTYPE, size=time_steps_tensor, infer_shape=False)
        for key in flow_keys
    }

    def write_tensor_dict(tas, index, values):
        return {key: tas[key].write(index, values[key]) for key in tas}

    def forward_body(
        time_index: tf.Tensor,
        running_particles: tf.Tensor,
        running_log_weights: tf.Tensor,
        running_log_likelihood: tf.Tensor,
        running_scalar_tas,
        running_bool_tas,
        running_flow_tas,
    ):
        observation = observations[time_index]
        ancestors = running_particles
        prior_means = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
        noise = transition_noise[:, time_index, :, :]
        pre_flow = prior_means + noise * transition_scale
        predicted_pre_flow = tf.einsum("md,bnd->bnm", observation_matrix, pre_flow)
        residual = observation[tf.newaxis, tf.newaxis, :] - predicted_pre_flow
        flow, flow_aux = core_tf._batched_ledh_linearized_flow_with_aux_tf(  # noqa: SLF001
            pre_flow_particles=pre_flow,
            prior_means=prior_means,
            observation_jacobian=h_jac_full,
            observation_residual=residual,
            transition_covariance=transition_covariance,
            observation_covariance=observation_covariance,
        )
        post_flow = flow.post_flow_particles
        transition_log_density = core_tf._batched_gaussian_logpdf(  # noqa: SLF001
            post_flow - prior_means,
            transition_covariance,
        )
        predicted_observation = tf.einsum("md,bnd->bnm", observation_matrix, post_flow)
        observation_log_density = core_tf._batched_gaussian_logpdf(  # noqa: SLF001
            predicted_observation - observation[tf.newaxis, tf.newaxis, :],
            observation_covariance,
        )
        corrected_log_weights = (
            running_log_weights
            + transition_log_density
            + observation_log_density
            - flow.pre_flow_log_density
            + flow.forward_log_det
        )
        weights, incremental = core_tf._normalize_log_weights(corrected_log_weights)  # noqa: SLF001
        normalized_log_weights = tf.math.log(
            tf.maximum(weights, core_tf._log_weight_floor())  # noqa: SLF001
        )
        mask = fixed_resampling_mask[:, time_index]
        next_particles, next_log_weights = _manual_forward_transport_tf(
            post_flow=post_flow,
            normalized_log_weights=normalized_log_weights,
            mask=mask,
            args=args,
        )
        scalar_values = {
            "ancestors": ancestors,
            "prior_means": prior_means,
            "pre_flow": pre_flow,
            "post_flow": post_flow,
            "predicted_observation": predicted_observation,
            "observation": observation,
            "corrected_log_weights": corrected_log_weights,
            "normalized_log_weights": normalized_log_weights,
            "transition_noise": noise,
        }
        bool_values = {"mask": mask}
        flow_values = {key: getattr(flow_aux, key) for key in flow_keys}
        return (
            time_index + 1,
            next_particles,
            next_log_weights,
            running_log_likelihood + incremental,
            write_tensor_dict(running_scalar_tas, time_index, scalar_values),
            write_tensor_dict(running_bool_tas, time_index, bool_values),
            write_tensor_dict(running_flow_tas, time_index, flow_values),
        )

    (
        _,
        particles,
        log_weights,
        log_likelihood,
        scalar_tas,
        bool_tas,
        flow_tas,
    ) = tf.while_loop(
        lambda time_index, *_: time_index < time_steps_tensor,
        forward_body,
        (
            tf.constant(0, dtype=tf.int32),
            initial_particles,
            core_tf.uniform_log_weights(batch_size, num_particles),
            tf.zeros([batch_size], dtype=DTYPE),
            scalar_tas,
            bool_tas,
            flow_tas,
        ),
    )

    def reverse_body(
        time_index: tf.Tensor,
        running_bar_particles: tf.Tensor,
        running_bar_log_weights: tf.Tensor,
        running_score: tf.Tensor,
    ):
        mask = bool_tas["mask"].read(time_index)
        mask.set_shape([batch_size])
        post_flow = scalar_tas["post_flow"].read(time_index)
        post_flow.set_shape([batch_size, num_particles, state_dim])
        normalized_log_weights = scalar_tas["normalized_log_weights"].read(time_index)
        normalized_log_weights.set_shape([batch_size, num_particles])
        bar_post_transport, bar_normalized_from_transport = _manual_transport_vjp_tf(
            post_flow=post_flow,
            normalized_log_weights=normalized_log_weights,
            mask=mask,
            args=args,
            upstream_particles=running_bar_particles,
        )
        inactive = tf.logical_not(mask)
        bar_post = bar_post_transport + tf.where(
            inactive[:, None, None],
            running_bar_particles,
            tf.zeros_like(running_bar_particles),
        )
        bar_normalized_log_weights = bar_normalized_from_transport + tf.where(
            inactive[:, None],
            running_bar_log_weights,
            tf.zeros_like(running_bar_log_weights),
        )
        bar_corrected, _weights, _incremental, _floor_active = (
            core_tf._normalize_log_weights_with_floor_vjp(  # noqa: SLF001
                tf.ensure_shape(
                    scalar_tas["corrected_log_weights"].read(time_index),
                    [batch_size, num_particles],
                ),
                bar_normalized_log_weights,
                tf.ones([batch_size], dtype=DTYPE),
            )
        )
        correction_bars = core_tf._log_weight_correction_vjp(bar_corrected)  # noqa: SLF001
        next_bar_log_weights = correction_bars["current_log_weights"]

        prior_means = scalar_tas["prior_means"].read(time_index)
        prior_means.set_shape([batch_size, num_particles, state_dim])
        transition_vjp = core_tf._transition_gaussian_log_density_vjp(  # noqa: SLF001
            post_flow,
            prior_means,
            transition_covariance,
            correction_bars["transition_log_density"],
        )
        predicted_observation = scalar_tas["predicted_observation"].read(time_index)
        predicted_observation.set_shape([batch_size, num_particles, OBS_DIM])
        observation = scalar_tas["observation"].read(time_index)
        observation.set_shape([OBS_DIM])
        observation_vjp = core_tf._observation_gaussian_log_density_vjp(  # noqa: SLF001
            predicted_observation,
            observation,
            observation_covariance,
            correction_bars["observation_log_density"],
            residual_convention="model_minus_observation",
        )
        bar_post += transition_vjp["x_next"]
        bar_post += tf.einsum(
            "md,bnm->bnd",
            observation_matrix,
            observation_vjp["predicted_observation"],
        )
        flow_values = {key: flow_tas[key].read(time_index) for key in flow_keys}
        for key in ("x0", "prior_means", "delta", "info"):
            flow_values[key].set_shape([batch_size, num_particles, state_dim])
        for key in ("observation_residual", "pseudo_observation"):
            flow_values[key].set_shape([batch_size, num_particles, OBS_DIM])
        flow_values["observation_jacobian"].set_shape(
            [batch_size, num_particles, OBS_DIM, state_dim]
        )
        for key in (
            "transition_covariance",
            "transition_covariance_stable",
            "prior_chol",
            "prior_precision",
            "prior_inv",
        ):
            flow_values[key].set_shape([batch_size, state_dim, state_dim])
        for key in ("observation_covariance", "observation_covariance_stable", "obs_precision"):
            flow_values[key].set_shape([batch_size, OBS_DIM, OBS_DIM])
        for key in (
            "post_precision",
            "post_precision_stable",
            "post_covariance_unstabilized",
            "post_covariance",
            "post_chol",
            "affine_transform",
        ):
            flow_values[key].set_shape([batch_size, num_particles, state_dim, state_dim])
        flow_aux = core_tf._BatchedLEDHLinearizedFlowAux(  # noqa: SLF001
            **flow_values
        )
        flow_vjp = core_tf._batched_ledh_linearized_flow_vjp(  # noqa: SLF001
            flow_aux,
            bar_post,
            correction_bars["pre_flow_log_density"],
            correction_bars["forward_log_det"],
        )
        bar_pre_flow = flow_vjp.pre_flow_particles - tf.einsum(
            "md,bnm->bnd",
            observation_matrix,
            flow_vjp.observation_residual,
        )
        bar_prior_means = transition_vjp["transition_mean"] + flow_vjp.prior_means + bar_pre_flow
        ancestors = scalar_tas["ancestors"].read(time_index)
        ancestors.set_shape([batch_size, num_particles, state_dim])
        noise = scalar_tas["transition_noise"].read(time_index)
        noise.set_shape([batch_size, num_particles, state_dim])
        bar_transition_matrix = tf.einsum("bnd,bne->bde", bar_prior_means, ancestors)
        bar_previous_particles = tf.einsum("bnd,bdj->bnj", bar_prior_means, transition_matrix)
        bar_transition_noise_scale = bar_pre_flow
        step_score = _lgssm_theta_score(
            theta=theta,
            bar_initial_particles=tf.zeros_like(initial_particles),
            initial_noise=tf.zeros_like(initial_noise),
            transition_noise=noise,
            bar_transition_noise_scale=bar_transition_noise_scale,
            bar_transition_matrix=bar_transition_matrix,
            bar_transition_covariance=(
                transition_vjp["transition_covariance"] + flow_vjp.transition_covariance
            ),
            bar_observation_covariance=(
                observation_vjp["observation_covariance"] + flow_vjp.observation_covariance
            ),
        )
        return (
            time_index - 1,
            bar_previous_particles,
            next_bar_log_weights,
            running_score + step_score,
        )

    (
        _,
        bar_initial_particles,
        _bar_log_weights,
        per_seed_score_without_initial,
    ) = tf.while_loop(
        lambda time_index, *_: time_index >= 0,
        reverse_body,
        (
            time_steps_tensor - 1,
            tf.zeros_like(particles),
            tf.zeros_like(log_weights),
            tf.zeros([batch_size, len(PARAMETER_NAMES)], dtype=DTYPE),
        ),
    )
    initial_score = _lgssm_theta_score(
        theta=theta,
        bar_initial_particles=bar_initial_particles,
        initial_noise=initial_noise,
        transition_noise=tf.zeros_like(initial_noise),
        bar_transition_noise_scale=tf.zeros_like(initial_noise),
        bar_transition_matrix=tf.zeros([batch_size, state_dim, state_dim], dtype=DTYPE),
        bar_transition_covariance=tf.zeros([batch_size, state_dim, state_dim], dtype=DTYPE),
        bar_observation_covariance=tf.zeros([batch_size, OBS_DIM, OBS_DIM], dtype=DTYPE),
    )
    per_seed_score = per_seed_score_without_initial + initial_score
    return {
        "objective": tf.reduce_mean(log_likelihood),
        "log_likelihood": log_likelihood,
        "gradient_tensor": tf.reduce_mean(per_seed_score, axis=0),
        "per_seed_gradient": per_seed_score,
        "score_route": tf.constant(MANUAL_SCORE_ROUTE_ID),
    }


def _compact_value_and_score_from_components(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
    theta: tf.Tensor,
) -> dict[str, tf.Tensor]:
    if args.transport_gradient_mode != core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE:
        raise ValueError("compact LGSSM score requires manual streaming finite transport")
    if args.transport_ad_mode != "full":
        raise ValueError("compact LGSSM score requires transport_ad_mode='full'")
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])
    observations = tf.convert_to_tensor(tensors["observations"], dtype=DTYPE)
    fixed_resampling_mask = tf.convert_to_tensor(tensors["fixed_resampling_mask"], dtype=tf.bool)
    initial_particles = tf.convert_to_tensor(tensors["initial_particles"], dtype=DTYPE)
    initial_noise = tf.convert_to_tensor(tensors["initial_noise"], dtype=DTYPE)
    transition_noise = tf.convert_to_tensor(tensors["transition_noise"], dtype=DTYPE)
    batch_size, num_particles, state_dim = core_tf._static_shape(  # noqa: SLF001
        initial_particles,
        "initial_particles",
    )
    time_steps_tensor = tf.shape(observations)[0]
    param_dim = len(PARAMETER_NAMES)
    components = _lgssm_components(theta, batch_size)
    tangents = _lgssm_component_tangents(theta, batch_size)
    transition_matrix = components["transition_matrix"]
    transition_covariance = components["transition_covariance"]
    observation_covariance = components["observation_covariance"]
    observation_matrix = components["observation_matrix"]
    h_jac_full = tf.tile(
        observation_matrix[tf.newaxis, tf.newaxis, :, :],
        [batch_size, num_particles, 1, 1],
    )
    transition_scale = components["q_scale"]
    d_transition_matrix = tangents["d_transition_matrix"]
    d_transition_covariance = tangents["d_transition_covariance"]
    d_observation_covariance = tangents["d_observation_covariance"]
    d_transition_scale = tangents["d_transition_scale"]

    d_initial_particles = initial_noise[:, :, :, None] * tangents["d_initial_std"][
        None,
        None,
        :,
        :,
    ]

    prior_chol = tf.linalg.cholesky(transition_covariance)
    prior_precision = tf.linalg.cholesky_solve(
        prior_chol,
        tf.eye(state_dim, dtype=DTYPE)[tf.newaxis, :, :],
    )
    obs_chol = tf.linalg.cholesky(observation_covariance)
    obs_precision = tf.linalg.cholesky_solve(
        obs_chol,
        tf.eye(OBS_DIM, dtype=DTYPE)[tf.newaxis, :, :],
    )
    d_prior_precision = -tf.einsum(
        "bij,bjkq,bkl->bilq",
        prior_precision,
        d_transition_covariance,
        prior_precision,
    )
    d_obs_precision = -tf.einsum(
        "bij,bjkq,bkl->bilq",
        obs_precision,
        d_observation_covariance,
        obs_precision,
    )
    base_post_precision = prior_precision[:, None, :, :] + tf.einsum(
        "od,boq,qe->bde",
        observation_matrix,
        obs_precision,
        observation_matrix,
    )[:, None, :, :]
    post_covariance = tf.linalg.inv(base_post_precision)
    d_post_precision = d_prior_precision[:, None, :, :, :] + tf.einsum(
        "od,boqk,qe->bdek",
        observation_matrix,
        d_obs_precision,
        observation_matrix,
    )[:, None, :, :, :]
    d_post_covariance = -tf.einsum(
        "bnij,bnjkq,bnkl->bnilq",
        post_covariance,
        d_post_precision,
        post_covariance,
    )
    post_covariance = tf.tile(post_covariance, [1, num_particles, 1, 1])
    d_post_covariance = tf.tile(d_post_covariance, [1, num_particles, 1, 1, 1])
    post_chol, d_post_chol = _cholesky_jvp_matrix(post_covariance, d_post_covariance)
    prior_inv = tf.linalg.triangular_solve(
        prior_chol,
        tf.eye(state_dim, dtype=DTYPE)[tf.newaxis, :, :],
    )
    d_prior_chol = tf.zeros([batch_size, state_dim, state_dim, param_dim], dtype=DTYPE)
    d_prior_chol += tf.concat(
        [
            tf.zeros([batch_size, state_dim, state_dim, 3], dtype=DTYPE),
            tf.eye(state_dim, dtype=DTYPE)[tf.newaxis, :, :, None]
            * tf.ones([batch_size, 1, 1, 1], dtype=DTYPE),
            tf.zeros([batch_size, state_dim, state_dim, 1], dtype=DTYPE),
        ],
        axis=-1,
    )
    d_prior_inv = -tf.einsum(
        "bij,bjkq,bkl->bilq",
        prior_inv,
        d_prior_chol,
        prior_inv,
    )
    affine_transform = tf.einsum("bnij,bjk->bnik", post_chol, prior_inv)
    d_affine_transform = (
        tf.einsum("bnijq,bjk->bnikq", d_post_chol, prior_inv)
        + tf.einsum("bnij,bjkq->bnikq", post_chol, d_prior_inv)
    )
    logdet_prior_chol = tf.reduce_sum(tf.math.log(tf.linalg.diag_part(prior_chol)), axis=-1)
    d_logdet_prior_chol = tf.reduce_sum(
        tf.einsum("biiq->biq", d_prior_chol)
        / tf.linalg.diag_part(prior_chol)[:, :, None],
        axis=1,
    )
    logdet_post_chol = tf.reduce_sum(tf.math.log(tf.linalg.diag_part(post_chol)), axis=-1)
    d_logdet_post_chol = tf.reduce_sum(
        tf.einsum("bniiq->bniq", d_post_chol)
        / tf.linalg.diag_part(post_chol)[:, :, :, None],
        axis=2,
    )
    forward_log_det = logdet_post_chol - logdet_prior_chol[:, None]
    d_forward_log_det = d_logdet_post_chol - d_logdet_prior_chol[:, None, :]

    def forward_body(
        time_index: tf.Tensor,
        running_particles: tf.Tensor,
        running_log_weights: tf.Tensor,
        running_d_particles: tf.Tensor,
        running_d_log_weights: tf.Tensor,
        running_log_likelihood: tf.Tensor,
        running_d_log_likelihood: tf.Tensor,
    ):
        observation = observations[time_index]
        ancestors = running_particles
        d_ancestors = running_d_particles
        prior_means = tf.einsum("bnj,bdj->bnd", ancestors, transition_matrix)
        d_prior_means = (
            tf.einsum("bnjq,bdj->bndq", d_ancestors, transition_matrix)
            + tf.einsum("bnj,bdjq->bndq", ancestors, d_transition_matrix)
        )
        noise = transition_noise[:, time_index, :, :]
        pre_flow = prior_means + noise * transition_scale
        d_pre_flow = d_prior_means + noise[:, :, :, None] * d_transition_scale[
            None,
            None,
            None,
            :,
        ]
        predicted_pre_flow = tf.einsum("md,bnd->bnm", observation_matrix, pre_flow)
        residual = observation[tf.newaxis, tf.newaxis, :] - predicted_pre_flow
        d_residual = -tf.einsum("md,bndq->bnmq", observation_matrix, d_pre_flow)
        pseudo_observation = tf.einsum("md,bnd->bnm", observation_matrix, pre_flow) + residual
        d_pseudo_observation = tf.einsum("md,bndq->bnmq", observation_matrix, d_pre_flow) + d_residual
        info = tf.einsum("bde,bne->bnd", prior_precision, prior_means) + tf.einsum(
            "bnod,boq,bnq->bnd",
            h_jac_full,
            obs_precision,
            pseudo_observation,
        )
        d_info = (
            tf.einsum("bdeq,bne->bndq", d_prior_precision, prior_means)
            + tf.einsum("bde,bneq->bndq", prior_precision, d_prior_means)
            + tf.einsum("bnod,boqk,bnq->bndk", h_jac_full, d_obs_precision, pseudo_observation)
            + tf.einsum("bnod,boq,bnqk->bndk", h_jac_full, obs_precision, d_pseudo_observation)
        )
        post_mean = tf.einsum("bnde,bne->bnd", post_covariance, info)
        d_post_mean = (
            tf.einsum("bndeq,bne->bndq", d_post_covariance, info)
            + tf.einsum("bnde,bneq->bndq", post_covariance, d_info)
        )
        delta = pre_flow - prior_means
        d_delta = d_pre_flow - d_prior_means
        post_flow = post_mean + tf.einsum("bnij,bnj->bni", affine_transform, delta)
        d_post_flow = (
            d_post_mean
            + tf.einsum("bnijq,bnj->bniq", d_affine_transform, delta)
            + tf.einsum("bnij,bnjq->bniq", affine_transform, d_delta)
        )
        transition_log_density, d_transition_log_density = _batched_gaussian_logpdf_jvp(
            post_flow - prior_means,
            transition_covariance,
            d_post_flow - d_prior_means,
            d_transition_covariance,
        )
        pre_flow_log_density, d_pre_flow_log_density = _batched_gaussian_logpdf_jvp(
            pre_flow - prior_means,
            transition_covariance,
            d_pre_flow - d_prior_means,
            d_transition_covariance,
        )
        predicted_observation = tf.einsum("md,bnd->bnm", observation_matrix, post_flow)
        d_predicted_observation = tf.einsum("md,bndq->bnmq", observation_matrix, d_post_flow)
        observation_log_density, d_observation_log_density = _batched_gaussian_logpdf_jvp(
            predicted_observation - observation[tf.newaxis, tf.newaxis, :],
            observation_covariance,
            d_predicted_observation,
            d_observation_covariance,
        )
        corrected_log_weights = (
            running_log_weights
            + transition_log_density
            + observation_log_density
            - pre_flow_log_density
            + forward_log_det
        )
        d_corrected_log_weights = (
            running_d_log_weights
            + d_transition_log_density
            + d_observation_log_density
            - d_pre_flow_log_density
            + d_forward_log_det
        )
        (
            normalized_log_weights,
            d_normalized_log_weights,
            incremental,
            d_incremental,
        ) = _normalize_log_weights_jvp(corrected_log_weights, d_corrected_log_weights)
        mask = fixed_resampling_mask[:, time_index]
        next_particles, next_log_weights, next_d_particles, next_d_log_weights = (
            _compact_forward_transport_jvp_tf(
                post_flow=post_flow,
                normalized_log_weights=normalized_log_weights,
                d_post_flow=d_post_flow,
                d_normalized_log_weights=d_normalized_log_weights,
                mask=mask,
                args=args,
            )
        )
        return (
            time_index + 1,
            next_particles,
            next_log_weights,
            next_d_particles,
            next_d_log_weights,
            running_log_likelihood + incremental,
            running_d_log_likelihood + d_incremental,
        )

    (
        _,
        _particles,
        _log_weights,
        _d_particles,
        _d_log_weights,
        log_likelihood,
        per_seed_score,
    ) = tf.while_loop(
        lambda time_index, *_: time_index < time_steps_tensor,
        forward_body,
        (
            tf.constant(0, dtype=tf.int32),
            initial_particles,
            core_tf.uniform_log_weights(batch_size, num_particles),
            d_initial_particles,
            tf.zeros([batch_size, num_particles, param_dim], dtype=DTYPE),
            tf.zeros([batch_size], dtype=DTYPE),
            tf.zeros([batch_size, param_dim], dtype=DTYPE),
        ),
    )
    return {
        "objective": tf.reduce_mean(log_likelihood),
        "log_likelihood": log_likelihood,
        "gradient_tensor": tf.reduce_mean(per_seed_score, axis=0),
        "per_seed_gradient": per_seed_score,
        "score_route": tf.constant(COMPACT_SCORE_ROUTE_ID),
    }


def _manual_score_diagnostic(
    args: argparse.Namespace,
    theta: tf.Tensor,
) -> dict[str, Any]:
    tensors = _build_lgssm_manual_tensors(args, theta)
    if args.score_mode == "manual-reverse":
        manual = _manual_value_and_score_from_components(tensors, args, theta)
        score_mode = "manual-reverse"
        score_route = MANUAL_SCORE_ROUTE_ID
        derivative_provenance = "historical_diagnostic_manual_total_reverse_scan_no_tape_same_scalar_fd_checked"
    else:
        manual = _compact_value_and_score_from_components(tensors, args, theta)
        score_mode = "compact-sensitivity"
        score_route = COMPACT_SCORE_ROUTE_ID
        derivative_provenance = "compact_forward_sensitivity_no_tape_same_scalar_fd_checked"
    step = tf.convert_to_tensor(args.score_fd_step, dtype=DTYPE)
    theta = tf.reshape(tf.convert_to_tensor(theta, dtype=DTYPE), [len(PARAMETER_NAMES)])

    def value_at(candidate: tf.Tensor) -> tf.Tensor:
        candidate_tensors = _build_lgssm_manual_tensors(args, candidate)
        if args.score_mode == "manual-reverse":
            return _manual_value_and_score_from_components(
                candidate_tensors,
                args,
                candidate,
            )["objective"]
        return _compact_value_and_score_from_components(
            candidate_tensors,
            args,
            candidate,
        )["objective"]

    fd_entries = []
    fd_values = []
    for index, name in enumerate(PARAMETER_NAMES):
        direction = tf.one_hot(index, len(PARAMETER_NAMES), dtype=DTYPE)
        plus = value_at(theta + step * direction)
        minus = value_at(theta - step * direction)
        fd = (plus - minus) / (2.0 * step)
        analytic = manual["gradient_tensor"][index]
        abs_error = tf.abs(analytic - fd)
        rel_error = abs_error / tf.maximum(
            tf.maximum(tf.abs(analytic), tf.abs(fd)),
            tf.constant(1.0e-12, dtype=DTYPE),
        )
        fd_values.append(fd)
        fd_entries.append(
            {
                "parameter": name,
                "manual_score": float(analytic.numpy()),
                "finite_difference": float(fd.numpy()),
                "abs_error": float(abs_error.numpy()),
                "relative_error": float(rel_error.numpy()),
            }
        )
    fd_tensor = tf.stack(fd_values)
    abs_residual = tf.abs(manual["gradient_tensor"] - fd_tensor)
    rel_residual = abs_residual / tf.maximum(
        tf.maximum(tf.abs(manual["gradient_tensor"]), tf.abs(fd_tensor)),
        tf.constant(1.0e-12, dtype=DTYPE),
    )
    max_abs_error = float(tf.reduce_max(abs_residual).numpy())
    max_relative_error = float(tf.reduce_max(rel_residual).numpy())
    fd_pass = bool(
        max_abs_error <= float(args.score_fd_atol)
        or max_relative_error <= float(args.score_fd_rtol)
    )
    score_output_devices = sorted(
        {
            manual["objective"].device,
            manual["log_likelihood"].device,
            manual["gradient_tensor"].device,
            manual["per_seed_gradient"].device,
        }
    )
    return {
        "score_mode": score_mode,
        "score_route": score_route,
        "value_route_id": SAME_SCALAR_ROUTE_ID,
        "score_route_id": SAME_SCALAR_ROUTE_ID,
        "value_score_route_status": "same_route_value_score",
        "value_score_same_transport_algorithm": True,
        "score_derivative_provenance": derivative_provenance,
        "old_full_history_route_status": (
            "historical_diagnostic_only" if args.score_mode != "manual-reverse" else "executed_historical_diagnostic"
        ),
        "parameter_names": list(PARAMETER_NAMES),
        "objective": float(manual["objective"].numpy()),
        "log_likelihood_by_seed": [
            float(value) for value in manual["log_likelihood"].numpy().reshape(-1)
        ],
        "score": [float(value) for value in manual["gradient_tensor"].numpy().reshape(-1)],
        "per_seed_score": manual["per_seed_gradient"].numpy().tolist(),
        "score_output_devices": score_output_devices,
        "same_scalar_fd": {
            "status": "pass" if fd_pass else "fail",
            "step": float(args.score_fd_step),
            "atol": float(args.score_fd_atol),
            "rtol": float(args.score_fd_rtol),
            "max_abs_error": max_abs_error,
            "max_relative_error": max_relative_error,
            "parameters": fd_entries,
        },
        "no_autodiff_score_route": True,
        "transport": {
            "plan_mode": "streaming",
            "gradient_mode": args.transport_gradient_mode,
            "ad_mode": args.transport_ad_mode,
            "sinkhorn_iterations": args.sinkhorn_iterations,
            "sinkhorn_epsilon": args.sinkhorn_epsilon,
            "annealed_scaling": args.annealed_scaling,
        },
    }


def _score_admission_decision(
    *,
    score_mode: str,
    fd_status: str,
    same_target_full_row: bool,
    runtime_gate_applicable: bool,
) -> dict[str, str]:
    if score_mode == "compact-sensitivity":
        if fd_status == "pass" and same_target_full_row and runtime_gate_applicable:
            return {
                "score_status": "executed_same_target_compact_score_fd_pass_gpu_material",
                "score_admission_status": "admitted_same_target_compact_score",
                "nonclaim": (
                    "score evidence is for the LEDH-PFPF-OT scalar, not the exact Kalman likelihood"
                ),
            }
        if fd_status == "pass":
            return {
                "score_status": "executed_compact_score_fd_pass_but_material_gate_blocked",
                "score_admission_status": "blocked_material_gate_not_full_gpu_row",
                "nonclaim": (
                    "compact total score passed same-scalar FD on this run but is not admitted "
                    "as a full GPU leaderboard score"
                ),
            }
        return {
            "score_status": "blocked_compact_score_same_scalar_fd_failed",
            "score_admission_status": "blocked_same_scalar_fd_failed",
            "nonclaim": (
                "compact total score ran but is blocked because the same-scalar FD check failed"
            ),
        }
    if score_mode == "manual-reverse":
        if fd_status == "pass":
            return {
                "score_status": "executed_historical_manual_reverse_score_fd_pass_not_admitted",
                "score_admission_status": "blocked_historical_manual_reverse_not_default",
                "nonclaim": (
                    "historical manual-reverse score passed same-scalar FD but is diagnostic only"
                ),
            }
        return {
            "score_status": "blocked_historical_manual_reverse_score_same_scalar_fd_failed",
            "score_admission_status": "blocked_same_scalar_fd_failed",
            "nonclaim": (
                "historical manual-reverse score ran but is blocked because the same-scalar FD check failed"
            ),
        }
    raise ValueError(f"unsupported score mode for admission decision: {score_mode}")


def _make_lgssm_callbacks(
    tensors: dict[str, tf.Tensor],
    seeds: list[int],
    num_particles: int,
):
    batch_size = len(seeds)
    transition_matrix = tensors["transition_matrix"]
    transition_covariance = tensors["transition_covariance"]
    observation_covariance = tensors["observation_covariance"]
    observation_matrix = tensors["observation_matrix"]
    transition_chol = tensors["transition_chol"]

    def pre_flow_step_fn(particles: tf.Tensor, time_index: tf.Tensor) -> tf.Tensor:
        mean = tf.einsum("bnj,bdj->bnd", particles, transition_matrix)
        noise_rows = []
        for seed in seeds:
            noise_rows.append(
                tf.random.stateless_normal(
                    [num_particles, STATE_DIM],
                    seed=_seed_pair(seed, tf.constant(1000, dtype=tf.int32) + time_index),
                    dtype=DTYPE,
                )
            )
        noise = tf.stack(noise_rows, axis=0)
        return mean + tf.einsum("bnd,ed->bne", noise, transition_chol)

    def observation_fn(points: tf.Tensor) -> tf.Tensor:
        return tf.einsum("md,bnd->bnm", observation_matrix, points)

    def observation_jacobian_fn(points: tf.Tensor) -> tf.Tensor:
        chunk_particles = points.shape[1]
        if chunk_particles is None:
            raise ValueError("LGSSM value runner requires static particle chunk dimension")
        return tf.tile(
            observation_matrix[tf.newaxis, tf.newaxis, :, :],
            [batch_size, int(chunk_particles), 1, 1],
        )

    def observation_residual_fn(h_ref: tf.Tensor, observation: tf.Tensor) -> tf.Tensor:
        return observation[tf.newaxis, tf.newaxis, :] - h_ref

    def transition_log_density_fn(
        x_next: tf.Tensor,
        x_prev: tf.Tensor,
        time_index: tf.Tensor,
    ) -> tf.Tensor:
        del time_index
        mean = tf.einsum("bnj,bdj->bnd", x_prev, transition_matrix)
        return _batched_gaussian_logpdf(x_next - mean, transition_covariance)

    def observation_log_density_fn(
        x: tf.Tensor,
        observation: tf.Tensor,
        time_index: tf.Tensor,
    ) -> tf.Tensor:
        del time_index
        predicted = observation_fn(x)
        return _batched_gaussian_logpdf(
            predicted - observation[tf.newaxis, tf.newaxis, :],
            observation_covariance,
        )

    return {
        "pre_flow_step_fn": pre_flow_step_fn,
        "observation_fn": observation_fn,
        "observation_jacobian_fn": observation_jacobian_fn,
        "observation_residual_fn": observation_residual_fn,
        "transition_log_density_fn": transition_log_density_fn,
        "observation_log_density_fn": observation_log_density_fn,
    }


def _write_markdown(path: Path, result: dict[str, Any], json_path: Path) -> None:
    total_value = result["total_log_likelihood_estimate"]
    average_value = result["average_log_likelihood_estimate"]
    comparison = result["exact_value_comparison"]
    lines = [
        "# Same-Target LEDH LGSSM m3 T50 Value Runner",
        "",
        f"- JSON artifact: `{json_path}`",
        f"- Row: `{result['row_id']}`",
        f"- Target identity: `{result['target_identity']}`",
        f"- Comparison status: `{result['comparison_status']}`",
        f"- Value status: `{result['value_status']}`",
        f"- Score status: `{result['score_status']}`",
        f"- Shape: `{result['shape']}`",
        f"- Output devices: `{result['output_devices']}`",
        f"- Precision: `{result['precision']}`",
        f"- Compile plus first call seconds: `{result['compile_and_first_call_seconds']}`",
        f"- Warm-call timing summary seconds: `{result['warm_call_timing_summary_seconds']}`",
        f"- Total log likelihood mean: `{total_value['mean']}`",
        f"- Total log likelihood SD: `{total_value['sample_sd']}`",
        f"- Total log likelihood MCSE: `{total_value['mcse']}`",
        f"- Average log likelihood mean: `{average_value['mean']}`",
        f"- Average log likelihood MCSE: `{average_value['mcse']}`",
        f"- Exact Kalman total log likelihood: `{comparison['exact_total_log_likelihood']}`",
        f"- Exact Kalman average log likelihood: `{comparison['exact_average_log_likelihood']}`",
        f"- Average delta to exact: `{comparison['average_delta_mean_minus_exact']}`",
        f"- Average relative error: `{comparison['average_relative_error_abs']}`",
        f"- Finite output: `{result['finite_output']}`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in result["nonclaims"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    precision = _configure_precision(args)
    physical_gpus, logical_gpus = _configure_gpus()
    tensors, target_identity = _build_lgssm_tensors(args)
    callbacks = _make_lgssm_callbacks(tensors, args.batch_seeds, args.num_particles)
    return_history = args.history_mode == "full"

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_outputs() -> tuple[tf.Tensor, ...]:
        value = streaming_tf.streaming_batched_ledh_pfpf_ot_value_core_tf(
            observations=tensors["observations"],
            initial_particles=tensors["initial_particles"],
            fixed_resampling_mask=tensors["fixed_resampling_mask"],
            transition_matrix=tensors["transition_matrix"],
            transition_covariance=tensors["transition_covariance"],
            observation_covariance=tensors["observation_covariance"],
            observation_fn=callbacks["observation_fn"],
            observation_jacobian_fn=callbacks["observation_jacobian_fn"],
            observation_residual_fn=callbacks["observation_residual_fn"],
            transition_log_density_fn=callbacks["transition_log_density_fn"],
            observation_log_density_fn=callbacks["observation_log_density_fn"],
            pre_flow_step_fn=callbacks["pre_flow_step_fn"],
            sinkhorn_epsilon=args.sinkhorn_epsilon,
            annealed_scaling=args.annealed_scaling,
            annealed_convergence_threshold=args.annealed_convergence_threshold,
            sinkhorn_iterations=args.sinkhorn_iterations,
            transport_gradient_mode=args.transport_gradient_mode,
            transport_plan_mode="streaming",
            transport_ad_mode=args.transport_ad_mode,
            row_chunk_size=args.row_chunk_size,
            col_chunk_size=args.col_chunk_size,
            particle_chunk_size=args.particle_chunk_size,
            return_history=return_history,
        )
        return (
            value.log_likelihood,
            value.filtered_means,
            value.filtered_variances,
            value.ess_by_time,
            value.final_particles,
            value.max_row_residual,
            value.max_column_residual,
        )

    with tf.device(args.device):
        memory_before = _gpu_memory_info()
        start = time.perf_counter()
        outputs = compiled_outputs()
        _materialize(*outputs)
        compile_and_first = time.perf_counter() - start
        for _ in range(args.warmups):
            _materialize(*compiled_outputs())
        timings: list[float] = []
        for _ in range(args.repeats):
            start = time.perf_counter()
            outputs = compiled_outputs()
            _materialize(*outputs)
            timings.append(time.perf_counter() - start)
        memory_after = _gpu_memory_info()

    (
        log_likelihood,
        filtered_means,
        filtered_variances,
        ess_by_time,
        final_particles,
        max_row_residual,
        max_column_residual,
    ) = outputs
    output_devices = _validate_device((log_likelihood,), args.expect_device_kind)
    total_values = [float(value) for value in log_likelihood.numpy().reshape(-1)]
    average_values = [value / float(args.time_steps) for value in total_values]
    total_mean = statistics.fmean(total_values)
    total_sd = _sample_sd(total_values)
    total_mcse = total_sd / math.sqrt(len(total_values)) if total_sd is not None else None
    average_mean = statistics.fmean(average_values)
    average_sd = _sample_sd(average_values)
    average_mcse = (
        average_sd / math.sqrt(len(average_values)) if average_sd is not None else None
    )
    exact_total_value = float(target_identity["exact_total_log_likelihood"])
    exact_average_value = float(target_identity["exact_average_log_likelihood"])
    total_delta = total_mean - exact_total_value
    average_delta = average_mean - exact_average_value
    total_rel_error = abs(total_delta) / max(abs(exact_total_value), 1.0e-12)
    average_rel_error = abs(average_delta) / max(abs(exact_average_value), 1.0e-12)
    finite_output = bool(
        tf.reduce_all(tf.math.is_finite(log_likelihood)).numpy()
        and tf.reduce_all(tf.math.is_finite(final_particles)).numpy()
    )
    if return_history:
        finite_output = bool(
            finite_output
            and tf.reduce_all(tf.math.is_finite(filtered_means)).numpy()
            and tf.reduce_all(tf.math.is_finite(filtered_variances)).numpy()
            and tf.reduce_all(tf.math.is_finite(ess_by_time)).numpy()
        )
    runtime_gate_applicable = bool(
        args.expect_device_kind == "gpu"
        and all("GPU" in device.upper() for device in output_devices)
    )
    same_target_full_row = bool(target_identity["full_leaderboard_row"])
    score_diagnostic = None
    score_status = target_identity["score_status"]
    score_derivative_provenance = None
    value_score_route_status = "value_only_score_not_run"
    score_admission_status = "blocked_score_not_run"
    score_runtime_gate_applicable = False
    result_nonclaims = list(NONCLAIMS)
    if args.score_mode in {"compact-sensitivity", "manual-reverse"}:
        with tf.device(args.device):
            score_diagnostic = _manual_score_diagnostic(
                args,
                tf.constant(TRUTH_THETA, dtype=DTYPE),
            )
        fd_status = score_diagnostic["same_scalar_fd"]["status"]
        value_score_route_status = score_diagnostic["value_score_route_status"]
        score_derivative_provenance = score_diagnostic["score_derivative_provenance"]
        score_runtime_gate_applicable = bool(
            args.expect_device_kind == "gpu"
            and all(
                "GPU" in device.upper()
                for device in score_diagnostic["score_output_devices"]
            )
        )
        decision = _score_admission_decision(
            score_mode=args.score_mode,
            fd_status=fd_status,
            same_target_full_row=same_target_full_row,
            runtime_gate_applicable=runtime_gate_applicable and score_runtime_gate_applicable,
        )
        score_status = decision["score_status"]
        score_admission_status = decision["score_admission_status"]
        result_nonclaims.append(decision["nonclaim"])
        target_identity = {
            **target_identity,
            "score_status": score_status,
            "score_admission_status": score_admission_status,
        }
    result: dict[str, Any] = {
        "schema_version": "filter_bench.ledh_same_target_lgssm_m3_t50_value.v2",
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python_version": platform.python_version(),
        "tensorflow_version": tf.__version__,
        "git_commit": _git_commit(),
        "row_id": ROW_ID,
        "algorithm_id": "ledh_pfpf_ot",
        "comparison_status": (
            "executed_value_score"
            if score_admission_status == "admitted_same_target_compact_score"
            else "executed_value_only_score_blocked"
            if same_target_full_row
            else "executed_prefix_value_diagnostic_score_blocked"
        ),
        "value_status": (
            "executed_same_target_value"
            if same_target_full_row
            else "executed_prefix_value_not_full_row"
        ),
        "score_status": score_status,
        "score_admission_status": score_admission_status,
        "score_derivative_provenance": score_derivative_provenance,
        "score_route": (
            score_diagnostic["score_route"] if score_diagnostic is not None else None
        ),
        "value_route_id": (
            SAME_SCALAR_ROUTE_ID if score_diagnostic is not None else None
        ),
        "score_route_id": (
            SAME_SCALAR_ROUTE_ID if score_diagnostic is not None else None
        ),
        "value_score_route_status": value_score_route_status,
        "score": score_diagnostic["score"] if score_diagnostic is not None else None,
        "score_parameter_names": list(PARAMETER_NAMES) if score_diagnostic is not None else None,
        "manual_score_diagnostic": score_diagnostic,
        "score_runtime_gate_applicable": score_runtime_gate_applicable,
        "score_output_devices": (
            score_diagnostic["score_output_devices"] if score_diagnostic is not None else None
        ),
        "runtime_rankable_with_frozen_non_ledh": False,
        "target_identity": target_identity,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "physical_gpus": physical_gpus,
        "logical_gpus": logical_gpus,
        "device": args.device,
        "device_scope": args.device_scope,
        "expect_device_kind": args.expect_device_kind,
        "precision": precision,
        "shape": {
            "batch_size": len(args.batch_seeds),
            "batch_seed_count": len(args.batch_seeds),
            "time_steps": args.time_steps,
            "num_particles": args.num_particles,
            "state_dim": STATE_DIM,
            "obs_dim": OBS_DIM,
        },
        "batch_seeds": [int(seed) for seed in args.batch_seeds],
        "history_mode": args.history_mode,
        "return_history": return_history,
        "transport_policy": args.transport_policy,
        "transport": {
            "plan_mode": "streaming",
            "gradient_mode": args.transport_gradient_mode,
            "ad_mode": args.transport_ad_mode,
            "row_chunk_size": args.row_chunk_size,
            "col_chunk_size": args.col_chunk_size,
            "particle_chunk_size": args.particle_chunk_size,
            "sinkhorn_iterations": args.sinkhorn_iterations,
            "sinkhorn_epsilon": args.sinkhorn_epsilon,
            "annealed_scaling": args.annealed_scaling,
            "annealed_convergence_threshold": args.annealed_convergence_threshold,
            "dense_transport_matrix_materialized": False,
        },
        "jit_compile": True,
        "compiled_unit": "streaming_batched_ledh_pfpf_ot_value_core_tf",
        "compile_and_first_call_seconds": compile_and_first,
        "warmups": args.warmups,
        "repeats": args.repeats,
        "warm_call_timings_seconds": timings,
        "warm_call_timing_summary_seconds": _summary(timings),
        "gpu_memory_info_before": memory_before,
        "gpu_memory_info_after": memory_after,
        "output_devices": output_devices,
        "output_shape": list(log_likelihood.numpy().shape),
        "history_shapes": {
            "filtered_means": list(filtered_means.numpy().shape),
            "filtered_variances": list(filtered_variances.numpy().shape),
            "ess_by_time": list(ess_by_time.numpy().shape),
            "final_particles": list(final_particles.numpy().shape),
        },
        "total_log_likelihood_by_seed": total_values,
        "average_log_likelihood_by_seed": average_values,
        "total_log_likelihood_estimate": {
            "mean": total_mean,
            "sample_sd": total_sd,
            "mcse": total_mcse,
            "seed_count": len(total_values),
        },
        "average_log_likelihood_estimate": {
            "mean": average_mean,
            "sample_sd": average_sd,
            "mcse": average_mcse,
            "seed_count": len(average_values),
        },
        "exact_value_comparison": {
            "exact_total_log_likelihood": exact_total_value,
            "exact_average_log_likelihood": exact_average_value,
            "total_delta_mean_minus_exact": total_delta,
            "total_absolute_delta": abs(total_delta),
            "total_relative_error_abs": total_rel_error,
            "average_delta_mean_minus_exact": average_delta,
            "average_absolute_delta": abs(average_delta),
            "average_relative_error_abs": average_rel_error,
        },
        "ess_min_by_seed": (
            [float(value) for value in tf.reduce_min(ess_by_time, axis=0).numpy().reshape(-1)]
            if return_history
            else None
        ),
        "ess_summary_available": return_history,
        "max_row_residual": float(max_row_residual.numpy()),
        "max_column_residual": float(max_column_residual.numpy()),
        "finite_output": finite_output,
        "runtime_gate_applicable": runtime_gate_applicable,
        "primary_pass_same_target_value_execution": bool(
            finite_output and same_target_full_row and runtime_gate_applicable
        ),
        "nonclaims": result_nonclaims,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.markdown_output is not None:
        _write_markdown(Path(args.markdown_output), result, output)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
