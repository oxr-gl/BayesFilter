"""Parity and timing diagnostics for experimental batched SVD sigma-point score.

This standalone harness exercises the additive experimental module in
``bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf``.  It keeps the
time axis sequential and batches independent parameter rows along the leading
axis.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any

_PRE_PARSER = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_PRE_PARSER.add_argument(
    "--device-scope",
    choices=("cpu", "visible"),
    default="cpu",
    help="Hide GPU for CPU/parity runs or leave configured devices visible.",
)
_PRE_PARSER.add_argument(
    "--cuda-visible-devices",
    default=None,
    help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
)
_PRE_ARGS, _ = _PRE_PARSER.parse_known_args()
if _PRE_ARGS.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _PRE_ARGS.cuda_visible_devices
elif _PRE_ARGS.device_scope == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import tensorflow as tf

from bayesfilter.nonlinear.experimental_batched_svd_sigma_point_tf import (
    TFBatchedStructuralFirstDerivatives,
    TFBatchedStructuralStateSpace,
    tf_batched_svd_sigma_point_value_and_score,
)
from bayesfilter.nonlinear.svd_sigma_point_derivatives_tf import (
    TFStructuralFirstDerivatives,
    tf_svd_cubature_score,
    tf_svd_cut4_score,
    tf_svd_ukf_score,
)
from bayesfilter.structural import StatePartition
from bayesfilter.structural_tf import make_affine_structural_tf


BACKENDS = ("tf_svd_cubature", "tf_svd_ukf", "tf_svd_cut4")


def _parse_rows(value: str, batch_size: int) -> list[int]:
    if value == "all":
        return list(range(batch_size))
    if value == "edges":
        return sorted({0, batch_size // 2, batch_size - 1})
    rows = [int(part) for part in value.split(",") if part.strip()]
    for row in rows:
        if row < 0 or row >= batch_size:
            raise ValueError(f"row {row} is outside batch size {batch_size}")
    return rows


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--mode",
        choices=(
            "parity",
            "timing",
            "first-call",
            "compiled-timing",
            "scalar-compiled-loop",
        ),
        required=True,
    )
    parser.add_argument("--backend", choices=BACKENDS, default="tf_svd_ukf")
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--time-steps", type=int, default=200)
    parser.add_argument("--state-dim", type=int, default=10)
    parser.add_argument("--obs-dim", type=int, default=10)
    parser.add_argument("--parameter-dim", type=int, default=2)
    parser.add_argument("--rows", default="all")
    parser.add_argument("--warmups", type=int, default=3)
    parser.add_argument("--repeats", type=int, default=10)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument(
        "--device-scope",
        choices=("cpu", "visible"),
        default=_PRE_ARGS.device_scope,
        help="Hide GPU for CPU/parity runs or leave configured devices visible.",
    )
    parser.add_argument(
        "--cuda-visible-devices",
        default=_PRE_ARGS.cuda_visible_devices,
        help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
    )
    parser.add_argument(
        "--expect-device-kind",
        choices=("any", "cpu", "gpu"),
        default="any",
        help="Fail closed if value/score tensors are not placed as expected.",
    )
    parser.add_argument(
        "--allow-eager-gpu-timing",
        action="store_true",
        help=(
            "Allow eager GPU timing as a placement smoke probe. "
            "Do not use this for CPU/GPU performance comparison."
        ),
    )
    parser.add_argument("--placement-floor", type=float, default=0.0)
    parser.add_argument("--innovation-floor", type=float, default=1.0e-12)
    parser.add_argument("--rank-tolerance", type=float, default=1.0e-12)
    parser.add_argument("--spectral-gap-tolerance", type=float, default=1.0e-10)
    parser.add_argument("--fixed-null-tolerance", type=float, default=1.0e-10)
    parser.add_argument("--jitter", type=float, default=0.0)
    parser.add_argument("--value-rtol", type=float, default=1.0e-8)
    parser.add_argument("--value-atol", type=float, default=1.0e-8)
    parser.add_argument("--score-rtol", type=float, default=1.0e-7)
    parser.add_argument("--score-atol", type=float, default=1.0e-7)
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def _configure_gpus() -> tuple[list[str], list[str]]:
    physical_gpus = tf.config.list_physical_devices("GPU")
    for gpu in physical_gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
        except RuntimeError:
            pass
    logical_gpus = tf.config.list_logical_devices("GPU")
    return ([str(device) for device in physical_gpus], [str(device) for device in logical_gpus])


def _stable_fixture(
    *,
    batch_size: int,
    time_steps: int,
    state_dim: int,
    obs_dim: int,
    parameter_dim: int,
) -> dict[str, np.ndarray]:
    if state_dim != obs_dim:
        raise ValueError("this diagnostic fixture currently expects obs_dim == state_dim")
    if parameter_dim != 2:
        raise ValueError("this diagnostic fixture currently expects parameter_dim == 2")

    state_index = np.arange(state_dim, dtype=np.float64)
    obs_index = np.arange(obs_dim, dtype=np.float64)
    eye_state = np.eye(state_dim, dtype=np.float64)
    eye_obs = np.eye(obs_dim, dtype=np.float64)

    t_grid = np.arange(time_steps, dtype=np.float64)[:, None]
    observations = 0.10 * np.sin(0.031 * t_grid + 0.13 * obs_index[None, :])
    observations += 0.04 * np.cos(0.047 * t_grid - 0.09 * obs_index[None, :])

    batch_grid = np.linspace(-1.0, 1.0, batch_size, dtype=np.float64)
    theta0 = 0.35 * batch_grid
    theta1 = -1.05 + 0.10 * batch_grid
    transition_scale = 0.50 + 0.07 * np.tanh(theta0)
    d_transition_scale = 0.07 * (1.0 - np.tanh(theta0) ** 2)
    observation_variance = np.exp(2.0 * theta1)
    d_observation_variance = 2.0 * observation_variance

    base_drift = np.diag(0.011 * np.sin(0.29 * state_index))
    base_drift[:-1, 1:] += 0.010
    base_drift[1:, :-1] -= 0.004
    observation_matrix_base = eye_obs + 0.0025 / float(state_dim)
    observation_scale_diagonal = 1.0 + 0.02 * obs_index
    innovation_scale_diagonal = 0.025 + 0.002 * state_index
    initial_scale_diagonal = 0.45 + 0.015 * state_index
    observation_covariance_shape = np.diag(1.0 + 0.03 * obs_index)

    transition_matrix = np.empty((batch_size, state_dim, state_dim), dtype=np.float64)
    d_transition_matrix = np.zeros(
        (batch_size, parameter_dim, state_dim, state_dim),
        dtype=np.float64,
    )
    observation_covariance = np.empty((batch_size, obs_dim, obs_dim), dtype=np.float64)
    d_observation_covariance = np.zeros(
        (batch_size, parameter_dim, obs_dim, obs_dim),
        dtype=np.float64,
    )
    for batch_index in range(batch_size):
        transition_matrix[batch_index] = (
            transition_scale[batch_index] * eye_state + base_drift
        )
        d_transition_matrix[batch_index, 0] = d_transition_scale[batch_index] * eye_state
        observation_covariance[batch_index] = (
            observation_variance[batch_index] * observation_covariance_shape
        )
        d_observation_covariance[batch_index, 1] = (
            d_observation_variance[batch_index] * observation_covariance_shape
        )

    zeros_bp_n = np.zeros((batch_size, parameter_dim, state_dim), dtype=np.float64)
    zeros_bp_nn = np.zeros(
        (batch_size, parameter_dim, state_dim, state_dim),
        dtype=np.float64,
    )
    zeros_bp_m = np.zeros((batch_size, parameter_dim, obs_dim), dtype=np.float64)
    zeros_bp_mn = np.zeros(
        (batch_size, parameter_dim, obs_dim, state_dim),
        dtype=np.float64,
    )

    return {
        "observations": observations,
        "transition_offset": np.full((batch_size, state_dim), 0.006, dtype=np.float64),
        "transition_matrix": transition_matrix,
        "innovation_matrix": np.broadcast_to(
            eye_state,
            (batch_size, state_dim, state_dim),
        ).copy(),
        "innovation_covariance": np.broadcast_to(
            np.diag(innovation_scale_diagonal),
            (batch_size, state_dim, state_dim),
        ).copy(),
        "observation_offset": np.full((batch_size, obs_dim), 0.011, dtype=np.float64),
        "observation_matrix": np.broadcast_to(
            observation_matrix_base * observation_scale_diagonal[:, None],
            (batch_size, obs_dim, state_dim),
        ).copy(),
        "observation_covariance": observation_covariance,
        "initial_mean": np.broadcast_to(
            0.02 * np.sin(0.17 * state_index),
            (batch_size, state_dim),
        ).copy(),
        "initial_covariance": np.broadcast_to(
            np.diag(initial_scale_diagonal),
            (batch_size, state_dim, state_dim),
        ).copy(),
        "d_initial_mean": zeros_bp_n,
        "d_initial_covariance": zeros_bp_nn,
        "d_innovation_covariance": zeros_bp_nn,
        "d_observation_covariance": d_observation_covariance,
        "d_transition_offset": zeros_bp_n,
        "d_transition_matrix": d_transition_matrix,
        "d_innovation_matrix": zeros_bp_nn,
        "d_observation_offset": zeros_bp_m,
        "d_observation_matrix": zeros_bp_mn,
    }


def _to_tensors(fixture: dict[str, np.ndarray]) -> dict[str, tf.Tensor]:
    return {name: tf.constant(value, dtype=tf.float64) for name, value in fixture.items()}


def _batched_model_and_derivatives(
    tensors: dict[str, tf.Tensor],
) -> tuple[TFBatchedStructuralStateSpace, TFBatchedStructuralFirstDerivatives]:
    transition_offset = tensors["transition_offset"]
    transition_matrix = tensors["transition_matrix"]
    innovation_matrix = tensors["innovation_matrix"]
    observation_offset = tensors["observation_offset"]
    observation_matrix = tensors["observation_matrix"]
    d_transition_offset = tensors["d_transition_offset"]
    d_transition_matrix = tensors["d_transition_matrix"]
    d_innovation_matrix = tensors["d_innovation_matrix"]
    d_observation_offset = tensors["d_observation_offset"]
    d_observation_matrix = tensors["d_observation_matrix"]

    def transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        return (
            transition_offset[:, tf.newaxis, :]
            + tf.einsum("bij,brj->bri", transition_matrix, previous)
            + tf.einsum("biq,brq->bri", innovation_matrix, innovation)
        )

    def observe(states: tf.Tensor) -> tf.Tensor:
        return (
            observation_offset[:, tf.newaxis, :]
            + tf.einsum("bmj,brj->brm", observation_matrix, states)
        )

    def transition_state_jacobian(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        point_count = tf.shape(previous)[1]
        return tf.broadcast_to(
            transition_matrix[:, tf.newaxis, :, :],
            [tf.shape(previous)[0], point_count, tf.shape(previous)[2], tf.shape(previous)[2]],
        )

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del previous
        point_count = tf.shape(innovation)[1]
        return tf.broadcast_to(
            innovation_matrix[:, tf.newaxis, :, :],
            [
                tf.shape(innovation)[0],
                point_count,
                tf.shape(innovation_matrix)[1],
                tf.shape(innovation)[2],
            ],
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        return (
            d_transition_offset[:, :, tf.newaxis, :]
            + tf.einsum("bpij,brj->bpri", d_transition_matrix, previous)
            + tf.einsum("bpiq,brq->bpri", d_innovation_matrix, innovation)
        )

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(states)[1]
        return tf.broadcast_to(
            observation_matrix[:, tf.newaxis, :, :],
            [
                tf.shape(states)[0],
                point_count,
                tf.shape(observation_matrix)[1],
                tf.shape(states)[2],
            ],
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return (
            d_observation_offset[:, :, tf.newaxis, :]
            + tf.einsum("bpmj,brj->bprm", d_observation_matrix, states)
        )

    model = TFBatchedStructuralStateSpace(
        initial_mean=tensors["initial_mean"],
        initial_covariance=tensors["initial_covariance"],
        innovation_covariance=tensors["innovation_covariance"],
        observation_covariance=tensors["observation_covariance"],
        transition_fn=transition,
        observation_fn=observe,
        name="experimental_batched_affine_svd_sigma_point_fixture",
    )
    derivatives = TFBatchedStructuralFirstDerivatives(
        d_initial_mean=tensors["d_initial_mean"],
        d_initial_covariance=tensors["d_initial_covariance"],
        d_innovation_covariance=tensors["d_innovation_covariance"],
        d_observation_covariance=tensors["d_observation_covariance"],
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
        name="experimental_batched_affine_svd_sigma_point_derivatives",
    )
    return model, derivatives


def _scalar_model_and_derivatives(
    tensors: dict[str, tf.Tensor],
    row: int,
) -> tuple[Any, TFStructuralFirstDerivatives]:
    state_dim = int(tensors["initial_mean"].shape[-1])
    partition = StatePartition(
        state_names=tuple(f"x{i}" for i in range(state_dim)),
        stochastic_indices=tuple(range(state_dim)),
        deterministic_indices=(),
        innovation_dim=state_dim,
    )
    transition_matrix = tensors["transition_matrix"][row]
    innovation_matrix = tensors["innovation_matrix"][row]
    observation_matrix = tensors["observation_matrix"][row]
    d_transition_offset = tensors["d_transition_offset"][row]
    d_transition_matrix = tensors["d_transition_matrix"][row]
    d_innovation_matrix = tensors["d_innovation_matrix"][row]
    d_observation_offset = tensors["d_observation_offset"][row]
    d_observation_matrix = tensors["d_observation_matrix"][row]

    model = make_affine_structural_tf(
        partition=partition,
        initial_mean=tensors["initial_mean"][row],
        initial_covariance=tensors["initial_covariance"][row],
        transition_offset=tensors["transition_offset"][row],
        transition_matrix=transition_matrix,
        innovation_matrix=innovation_matrix,
        innovation_covariance=tensors["innovation_covariance"][row],
        observation_offset=tensors["observation_offset"][row],
        observation_matrix=observation_matrix,
        observation_covariance=tensors["observation_covariance"][row],
    )

    def transition_state_jacobian(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        del innovation
        point_count = tf.shape(previous)[0]
        return tf.broadcast_to(transition_matrix[tf.newaxis, :, :], [point_count, state_dim, state_dim])

    def transition_innovation_jacobian(
        previous: tf.Tensor,
        innovation: tf.Tensor,
    ) -> tf.Tensor:
        del previous
        point_count = tf.shape(innovation)[0]
        return tf.broadcast_to(
            innovation_matrix[tf.newaxis, :, :],
            [point_count, state_dim, state_dim],
        )

    def d_transition(previous: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        return (
            d_transition_offset[:, tf.newaxis, :]
            + tf.einsum("pij,rj->pri", d_transition_matrix, previous)
            + tf.einsum("piq,rq->pri", d_innovation_matrix, innovation)
        )

    def observation_state_jacobian(states: tf.Tensor) -> tf.Tensor:
        point_count = tf.shape(states)[0]
        return tf.broadcast_to(
            observation_matrix[tf.newaxis, :, :],
            [point_count, state_dim, state_dim],
        )

    def d_observation(states: tf.Tensor) -> tf.Tensor:
        return (
            d_observation_offset[:, tf.newaxis, :]
            + tf.einsum("pmj,rj->prm", d_observation_matrix, states)
        )

    derivatives = TFStructuralFirstDerivatives(
        d_initial_mean=tensors["d_initial_mean"][row],
        d_initial_covariance=tensors["d_initial_covariance"][row],
        d_innovation_covariance=tensors["d_innovation_covariance"][row],
        d_observation_covariance=tensors["d_observation_covariance"][row],
        transition_state_jacobian_fn=transition_state_jacobian,
        transition_innovation_jacobian_fn=transition_innovation_jacobian,
        d_transition_fn=d_transition,
        observation_state_jacobian_fn=observation_state_jacobian,
        d_observation_fn=d_observation,
        name="experimental_scalar_affine_svd_sigma_point_derivatives",
    )
    return model, derivatives


def _scalar_score(
    observations: tf.Tensor,
    model: Any,
    derivatives: TFStructuralFirstDerivatives,
    *,
    backend: str,
    args: argparse.Namespace,
) -> tuple[float, np.ndarray]:
    kwargs = {
        "placement_floor": tf.constant(args.placement_floor, dtype=tf.float64),
        "innovation_floor": tf.constant(args.innovation_floor, dtype=tf.float64),
        "rank_tolerance": tf.constant(args.rank_tolerance, dtype=tf.float64),
        "spectral_gap_tolerance": tf.constant(args.spectral_gap_tolerance, dtype=tf.float64),
        "fixed_null_tolerance": tf.constant(args.fixed_null_tolerance, dtype=tf.float64),
        "jitter": tf.constant(args.jitter, dtype=tf.float64),
    }
    if backend == "tf_svd_cubature":
        result = tf_svd_cubature_score(observations, model, derivatives, **kwargs)
    elif backend == "tf_svd_ukf":
        result = tf_svd_ukf_score(observations, model, derivatives, **kwargs)
    elif backend == "tf_svd_cut4":
        result = tf_svd_cut4_score(observations, model, derivatives, **kwargs)
    else:
        raise ValueError(f"unknown backend: {backend}")
    return float(result.log_likelihood.numpy()), result.score.numpy()


def _materialized_call(
    tensors: dict[str, tf.Tensor],
    *,
    backend: str,
    args: argparse.Namespace,
) -> tuple[tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    model, derivatives = _batched_model_and_derivatives(tensors)
    value, score, diagnostics = tf_batched_svd_sigma_point_value_and_score(
        tensors["observations"],
        model,
        derivatives,
        backend=backend,
        placement_floor=tf.constant(args.placement_floor, dtype=tf.float64),
        innovation_floor=tf.constant(args.innovation_floor, dtype=tf.float64),
        rank_tolerance=tf.constant(args.rank_tolerance, dtype=tf.float64),
        spectral_gap_tolerance=tf.constant(args.spectral_gap_tolerance, dtype=tf.float64),
        fixed_null_tolerance=tf.constant(args.fixed_null_tolerance, dtype=tf.float64),
        jitter=tf.constant(args.jitter, dtype=tf.float64),
    )
    _ = value.numpy()
    _ = score.numpy()
    return value, score, dict(diagnostics)


def _compiled_materialized_call(
    compiled_call: Any,
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    value, score = compiled_call(observations)
    _ = value.numpy()
    _ = score.numpy()
    return value, score


def _timed_call(
    tensors: dict[str, tf.Tensor],
    *,
    backend: str,
    args: argparse.Namespace,
) -> tuple[float, tf.Tensor, tf.Tensor, dict[str, tf.Tensor]]:
    start = time.perf_counter()
    value, score, diagnostics = _materialized_call(tensors, backend=backend, args=args)
    return time.perf_counter() - start, value, score, diagnostics


def _timed_compiled_call(
    compiled_call: Any,
    observations: tf.Tensor,
) -> tuple[float, tf.Tensor, tf.Tensor]:
    start = time.perf_counter()
    value, score = _compiled_materialized_call(compiled_call, observations)
    return time.perf_counter() - start, value, score


def _scalar_compiled_calls(
    tensors: dict[str, tf.Tensor],
    args: argparse.Namespace,
) -> list[Any]:
    calls = []
    for row in range(int(tensors["initial_mean"].shape[0])):
        model, derivatives = _scalar_model_and_derivatives(tensors, row)

        @tf.function(jit_compile=True)
        def compiled_call(
            observations: tf.Tensor,
            *,
            model: Any = model,
            derivatives: TFStructuralFirstDerivatives = derivatives,
        ) -> tuple[tf.Tensor, tf.Tensor]:
            kwargs = {
                "placement_floor": tf.constant(args.placement_floor, dtype=tf.float64),
                "innovation_floor": tf.constant(args.innovation_floor, dtype=tf.float64),
                "rank_tolerance": tf.constant(args.rank_tolerance, dtype=tf.float64),
                "spectral_gap_tolerance": tf.constant(
                    args.spectral_gap_tolerance,
                    dtype=tf.float64,
                ),
                "fixed_null_tolerance": tf.constant(
                    args.fixed_null_tolerance,
                    dtype=tf.float64,
                ),
                "jitter": tf.constant(args.jitter, dtype=tf.float64),
            }
            if args.backend == "tf_svd_cubature":
                result = tf_svd_cubature_score(
                    observations,
                    model,
                    derivatives,
                    **kwargs,
                )
            elif args.backend == "tf_svd_ukf":
                result = tf_svd_ukf_score(
                    observations,
                    model,
                    derivatives,
                    **kwargs,
                )
            else:
                result = tf_svd_cut4_score(
                    observations,
                    model,
                    derivatives,
                    **kwargs,
                )
            return result.log_likelihood, result.score

        calls.append(compiled_call)
    return calls


def _scalar_loop_materialized_call(
    compiled_calls: list[Any],
    observations: tf.Tensor,
) -> tuple[tf.Tensor, tf.Tensor]:
    values = []
    scores = []
    for compiled_call in compiled_calls:
        value, score = compiled_call(observations)
        values.append(value)
        scores.append(score)
    value_batch = tf.stack(values, axis=0)
    score_batch = tf.stack(scores, axis=0)
    _ = value_batch.numpy()
    _ = score_batch.numpy()
    return value_batch, score_batch


def _timed_scalar_loop_call(
    compiled_calls: list[Any],
    observations: tf.Tensor,
) -> tuple[float, tf.Tensor, tf.Tensor]:
    start = time.perf_counter()
    value, score = _scalar_loop_materialized_call(compiled_calls, observations)
    return time.perf_counter() - start, value, score


def _summary(values: list[float]) -> dict[str, float]:
    return {
        "min_seconds": min(values),
        "median_seconds": statistics.median(values),
        "mean_seconds": statistics.fmean(values),
        "max_seconds": max(values),
    }


def _validate_device(
    *,
    expect_device_kind: str,
    physical_gpus: list[str],
    value: tf.Tensor,
    score: tf.Tensor,
) -> None:
    value_is_gpu = "GPU" in value.device.upper()
    score_is_gpu = "GPU" in score.device.upper()
    value_is_cpu = "CPU" in value.device.upper()
    score_is_cpu = "CPU" in score.device.upper()
    if expect_device_kind == "gpu":
        if not physical_gpus:
            raise RuntimeError("expected a GPU run, but TensorFlow sees no physical GPUs")
        if not (value_is_gpu and score_is_gpu):
            raise RuntimeError(
                f"expected GPU tensor placement, got value={value.device}, score={score.device}"
            )
    if expect_device_kind == "cpu" and not (value_is_cpu and score_is_cpu):
        raise RuntimeError(
            f"expected CPU tensor placement, got value={value.device}, score={score.device}"
        )


def _base_result(args: argparse.Namespace, physical_gpus: list[str], logical_gpus: list[str]) -> dict[str, Any]:
    return {
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python": platform.python_version(),
        "tensorflow": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "device_arg": args.device,
        "device_scope": args.device_scope,
        "expect_device_kind": args.expect_device_kind,
        "physical_gpus": physical_gpus,
        "logical_gpus": logical_gpus,
        "backend": args.backend,
        "shape": {
            "batch_size": args.batch_size,
            "time_steps": args.time_steps,
            "state_dim": args.state_dim,
            "obs_dim": args.obs_dim,
            "parameter_dim": args.parameter_dim,
        },
        "regularization": {
            "placement_floor": args.placement_floor,
            "innovation_floor": args.innovation_floor,
            "rank_tolerance": args.rank_tolerance,
            "spectral_gap_tolerance": args.spectral_gap_tolerance,
            "fixed_null_tolerance": args.fixed_null_tolerance,
            "jitter": args.jitter,
        },
        "notes": [
            "Single-shape diagnostic only; not a production benchmark.",
            "The experimental kernel hardcasts tensors to float64.",
            "Time remains sequential; the batch axis parallelizes independent parameter rows.",
            "The affine fixture uses structural SVD sigma-point filtering so scalar rows are the authority path.",
        ],
    }


def _run_parity(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    rows = _parse_rows(args.rows, args.batch_size)
    with tf.device(args.device):
        value, score, _diagnostics = _materialized_call(
            tensors,
            backend=args.backend,
            args=args,
        )
    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite batched value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )

    row_results: list[dict[str, Any]] = []
    max_abs_value_error = 0.0
    max_abs_score_error = 0.0
    max_rel_value_error = 0.0
    max_rel_score_error = 0.0
    passed = True
    for row in rows:
        model, derivatives = _scalar_model_and_derivatives(tensors, row)
        scalar_value, scalar_score = _scalar_score(
            tensors["observations"],
            model,
            derivatives,
            backend=args.backend,
            args=args,
        )
        value_error = float(abs(value_np[row] - scalar_value))
        score_errors = np.abs(score_np[row] - scalar_score)
        score_error = float(np.max(score_errors))
        value_scale = max(1.0, abs(scalar_value))
        score_scale = np.maximum(1.0, np.abs(scalar_score))
        value_rel_error = value_error / value_scale
        score_rel_error = float(np.max(score_errors / score_scale))
        value_pass = value_error <= args.value_atol + args.value_rtol * value_scale
        score_pass = bool(
            np.all(score_errors <= args.score_atol + args.score_rtol * score_scale)
        )
        row_pass = bool(value_pass and score_pass)
        passed = passed and row_pass
        max_abs_value_error = max(max_abs_value_error, value_error)
        max_abs_score_error = max(max_abs_score_error, score_error)
        max_rel_value_error = max(max_rel_value_error, value_rel_error)
        max_rel_score_error = max(max_rel_score_error, score_rel_error)
        row_results.append(
            {
                "row": row,
                "row_pass": row_pass,
                "value_pass": bool(value_pass),
                "score_pass": bool(score_pass),
                "batched_value": float(value_np[row]),
                "scalar_value": float(scalar_value),
                "value_abs_error": value_error,
                "value_rel_error": value_rel_error,
                "batched_score": score_np[row].tolist(),
                "scalar_score": scalar_score.tolist(),
                "score_abs_error_max": score_error,
                "score_rel_error_max": score_rel_error,
            }
        )

    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": "parity",
            "rows": rows,
            "passed": bool(passed),
            "finite_batched_outputs": finite,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "max_abs_value_error": max_abs_value_error,
            "max_abs_score_error": max_abs_score_error,
            "max_rel_value_error": max_rel_value_error,
            "max_rel_score_error": max_rel_score_error,
            "tolerances": {
                "value_atol": args.value_atol,
                "value_rtol": args.value_rtol,
                "score_atol": args.score_atol,
                "score_rtol": args.score_rtol,
            },
            "row_results": row_results,
        }
    )
    if not passed:
        raise RuntimeError("batched SVD sigma-point parity check failed")
    return result


def _run_timing(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")
    if args.expect_device_kind == "gpu" and not args.allow_eager_gpu_timing:
        raise ValueError(
            "GPU timing comparisons require a compiled/JIT path.  Pass "
            "--allow-eager-gpu-timing only for non-comparative placement smoke probes."
        )
    with tf.device(args.device):
        first_call_seconds, value, score, _diagnostics = _timed_call(
            tensors,
            backend=args.backend,
            args=args,
        )
        for _ in range(args.warmups):
            _materialized_call(tensors, backend=args.backend, args=args)
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score, _diagnostics = _timed_call(
                tensors,
                backend=args.backend,
                args=args,
            )
            timings.append(elapsed)

    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite batched value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )

    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": "timing",
            "timing_policy": {
                "first_call_includes_trace_and_initialization": True,
                "warmups": args.warmups,
                "repeats": args.repeats,
                "materialization": "value.numpy() and score.numpy() after each call",
            },
            "first_call_seconds": first_call_seconds,
            "warm_call_summary": _summary(timings),
            "per_filter_warm_median_seconds": statistics.median(timings) / args.batch_size,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "finite_outputs": finite,
        }
    )
    return result


def _run_first_call(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.expect_device_kind == "gpu" and not args.allow_eager_gpu_timing:
        raise ValueError(
            "GPU first-call timing requires a compiled/JIT path for benchmarking.  Pass "
            "--allow-eager-gpu-timing only for non-comparative placement smoke probes."
        )
    with tf.device(args.device):
        first_call_seconds, value, score, _diagnostics = _timed_call(
            tensors,
            backend=args.backend,
            args=args,
        )

    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite batched value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )

    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": "first-call",
            "timing_policy": {
                "first_call_includes_trace_and_initialization": True,
                "warmups": 0,
                "repeats": 0,
                "materialization": "value.numpy() and score.numpy() after first call",
            },
            "first_call_seconds": first_call_seconds,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "finite_outputs": finite,
            "notes": [
                *result["notes"],
                "First-call-only mode is a bounded capacity/timing probe, not a warm benchmark.",
            ],
        }
    )
    return result


def _run_compiled_timing(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")
    model, derivatives = _batched_model_and_derivatives(tensors)

    @tf.function(jit_compile=True)
    def compiled_call(observations: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        value, score, _diagnostics = tf_batched_svd_sigma_point_value_and_score(
            observations,
            model,
            derivatives,
            backend=args.backend,
            placement_floor=tf.constant(args.placement_floor, dtype=tf.float64),
            innovation_floor=tf.constant(args.innovation_floor, dtype=tf.float64),
            rank_tolerance=tf.constant(args.rank_tolerance, dtype=tf.float64),
            spectral_gap_tolerance=tf.constant(args.spectral_gap_tolerance, dtype=tf.float64),
            fixed_null_tolerance=tf.constant(args.fixed_null_tolerance, dtype=tf.float64),
            jitter=tf.constant(args.jitter, dtype=tf.float64),
        )
        return value, score

    with tf.device(args.device):
        compile_and_first_call_seconds, value, score = _timed_compiled_call(
            compiled_call,
            tensors["observations"],
        )
        for _ in range(args.warmups):
            _compiled_materialized_call(compiled_call, tensors["observations"])
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score = _timed_compiled_call(
                compiled_call,
                tensors["observations"],
            )
            timings.append(elapsed)

    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite compiled value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )

    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": "compiled-timing",
            "compiler": {
                "tf_function": True,
                "jit_compile": True,
                "compile_and_first_call_seconds": compile_and_first_call_seconds,
                "warm_calls_exclude_compile": True,
            },
            "timing_policy": {
                "first_call_includes_trace_compile_and_initialization": True,
                "warmups": args.warmups,
                "repeats": args.repeats,
                "materialization": "value.numpy() and score.numpy() after each compiled call",
            },
            "warm_call_summary": _summary(timings),
            "per_filter_warm_median_seconds": statistics.median(timings) / args.batch_size,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "finite_outputs": finite,
        }
    )
    return result


def _run_scalar_compiled_loop(
    args: argparse.Namespace,
    tensors: dict[str, tf.Tensor],
    physical_gpus: list[str],
    logical_gpus: list[str],
) -> dict[str, Any]:
    if args.warmups < 0 or args.repeats <= 0:
        raise ValueError("warmups must be >= 0 and repeats must be > 0")
    compiled_calls = _scalar_compiled_calls(tensors, args)

    with tf.device(args.device):
        compile_start = time.perf_counter()
        value, score = _scalar_loop_materialized_call(
            compiled_calls,
            tensors["observations"],
        )
        compile_and_first_call_seconds = time.perf_counter() - compile_start
        for _ in range(args.warmups):
            _scalar_loop_materialized_call(compiled_calls, tensors["observations"])
        timings: list[float] = []
        for _ in range(args.repeats):
            elapsed, value, score = _timed_scalar_loop_call(
                compiled_calls,
                tensors["observations"],
            )
            timings.append(elapsed)

    value_np = value.numpy()
    score_np = score.numpy()
    finite = bool(np.isfinite(value_np).all() and np.isfinite(score_np).all())
    if not finite:
        raise RuntimeError("nonfinite scalar-loop compiled value or score output")
    _validate_device(
        expect_device_kind=args.expect_device_kind,
        physical_gpus=physical_gpus,
        value=value,
        score=score,
    )

    result = _base_result(args, physical_gpus, logical_gpus)
    result.update(
        {
            "mode": "scalar-compiled-loop",
            "compiler": {
                "tf_function": True,
                "jit_compile": True,
                "compile_and_first_call_seconds": compile_and_first_call_seconds,
                "warm_calls_exclude_compile": True,
                "compiled_unit": "one_scalar_value_score_row",
                "python_loop_over_rows_in_benchmark_harness": True,
            },
            "timing_policy": {
                "first_call_includes_trace_compile_and_initialization": True,
                "warmups": args.warmups,
                "repeats": args.repeats,
                "materialization": "stacked value.numpy() and score.numpy() after scalar compiled row loop",
            },
            "warm_call_summary": _summary(timings),
            "per_filter_warm_median_seconds": statistics.median(timings) / args.batch_size,
            "value_device": value.device,
            "score_device": score.device,
            "value_shape": list(value_np.shape),
            "score_shape": list(score_np.shape),
            "value_sum": float(np.sum(value_np)),
            "score_abs_max": float(np.max(np.abs(score_np))),
            "finite_outputs": finite,
            "notes": [
                *result["notes"],
                "Scalar-loop mode is a benchmark comparator; it is not an HMC-jittable production implementation.",
            ],
        }
    )
    return result


def main() -> None:
    args = _parse_args()
    physical_gpus, logical_gpus = _configure_gpus()
    fixture = _stable_fixture(
        batch_size=args.batch_size,
        time_steps=args.time_steps,
        state_dim=args.state_dim,
        obs_dim=args.obs_dim,
        parameter_dim=args.parameter_dim,
    )
    tensors = _to_tensors(fixture)
    if args.mode == "parity":
        result = _run_parity(args, tensors, physical_gpus, logical_gpus)
    elif args.mode == "timing":
        result = _run_timing(args, tensors, physical_gpus, logical_gpus)
    elif args.mode == "first-call":
        result = _run_first_call(args, tensors, physical_gpus, logical_gpus)
    elif args.mode == "compiled-timing":
        result = _run_compiled_timing(args, tensors, physical_gpus, logical_gpus)
    else:
        result = _run_scalar_compiled_loop(args, tensors, physical_gpus, logical_gpus)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
