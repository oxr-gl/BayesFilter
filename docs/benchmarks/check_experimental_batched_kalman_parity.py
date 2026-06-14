"""Scalar parity check for the experimental batched Kalman value+score kernel."""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

_pre_parser = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
_pre_parser.add_argument(
    "--device-scope",
    choices=("cpu", "visible"),
    default="cpu",
    help="Hide GPU for deterministic scalar parity by default.",
)
_pre_parser.add_argument(
    "--cuda-visible-devices",
    default=None,
    help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
)
_pre_args, _ = _pre_parser.parse_known_args()
if _pre_args.cuda_visible_devices is not None:
    os.environ["CUDA_VISIBLE_DEVICES"] = _pre_args.cuda_visible_devices
elif _pre_args.device_scope == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import tensorflow as tf

from bayesfilter.linear.experimental_batched_kalman_tf import (
    tf_batched_kalman_value_and_score,
)
from bayesfilter.linear.kalman_qr_derivatives_tf import tf_qr_linear_gaussian_score
from bayesfilter.linear.kalman_tf import tf_linear_gaussian_log_likelihood
from bayesfilter.linear.types_tf import (
    TFLinearGaussianStateSpace,
    TFLinearGaussianStateSpaceDerivatives,
)
from docs.benchmarks.benchmark_experimental_batched_kalman_cpu_gpu import (
    _stable_fixture,
)


def _parse_rows(value: str, batch_size: int) -> list[int]:
    if value == "edges":
        return sorted({0, batch_size // 2, batch_size - 1})
    rows = [int(part) for part in value.split(",") if part.strip()]
    for row in rows:
        if row < 0 or row >= batch_size:
            raise ValueError(f"row {row} is outside batch size {batch_size}")
    return rows


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--time-steps", type=int, default=200)
    parser.add_argument("--state-dim", type=int, default=10)
    parser.add_argument("--obs-dim", type=int, default=10)
    parser.add_argument("--parameter-dim", type=int, default=2)
    parser.add_argument("--rows", default="edges")
    parser.add_argument("--value-rtol", type=float, default=1.0e-9)
    parser.add_argument("--value-atol", type=float, default=1.0e-9)
    parser.add_argument("--score-rtol", type=float, default=5.0e-8)
    parser.add_argument("--score-atol", type=float, default=5.0e-8)
    parser.add_argument("--jitter", type=float, default=1.0e-9)
    parser.add_argument(
        "--device-scope",
        choices=("cpu", "visible"),
        default=_pre_args.device_scope,
        help="Hide GPU for deterministic scalar parity by default.",
    )
    parser.add_argument(
        "--cuda-visible-devices",
        default=_pre_args.cuda_visible_devices,
        help="Set CUDA_VISIBLE_DEVICES before TensorFlow import.",
    )
    parser.add_argument("--output", required=True)
    return parser.parse_args()


def _to_tensors(fixture: dict[str, np.ndarray]) -> dict[str, tf.Tensor]:
    return {name: tf.constant(value, dtype=tf.float64) for name, value in fixture.items()}


def _batched_value_score(
    tensors: dict[str, tf.Tensor],
    *,
    jitter: float,
) -> tuple[np.ndarray, np.ndarray]:
    value, score = tf_batched_kalman_value_and_score(
        tensors["observations"],
        transition_offset=tensors["transition_offset"],
        transition_matrix=tensors["transition_matrix"],
        transition_covariance=tensors["transition_covariance"],
        observation_offset=tensors["observation_offset"],
        observation_matrix=tensors["observation_matrix"],
        observation_covariance=tensors["observation_covariance"],
        initial_state_mean=tensors["initial_state_mean"],
        initial_state_covariance=tensors["initial_state_covariance"],
        d_initial_state_mean=tensors["d_initial_state_mean"],
        d_initial_state_covariance=tensors["d_initial_state_covariance"],
        d_transition_offset=tensors["d_transition_offset"],
        d_transition_matrix=tensors["d_transition_matrix"],
        d_transition_covariance=tensors["d_transition_covariance"],
        d_observation_offset=tensors["d_observation_offset"],
        d_observation_matrix=tensors["d_observation_matrix"],
        d_observation_covariance=tensors["d_observation_covariance"],
        jitter=tf.constant(jitter, dtype=tf.float64),
    )
    return value.numpy(), score.numpy()


def _scalar_model_and_derivatives(
    tensors: dict[str, tf.Tensor],
    row: int,
) -> tuple[TFLinearGaussianStateSpace, TFLinearGaussianStateSpaceDerivatives]:
    model = TFLinearGaussianStateSpace(
        initial_mean=tensors["initial_state_mean"][row],
        initial_covariance=tensors["initial_state_covariance"][row],
        transition_offset=tensors["transition_offset"][row],
        transition_matrix=tensors["transition_matrix"][row],
        transition_covariance=tensors["transition_covariance"][row],
        observation_offset=tensors["observation_offset"][row],
        observation_matrix=tensors["observation_matrix"][row],
        observation_covariance=tensors["observation_covariance"][row],
    )
    zeros_pp_n = tf.zeros(
        [
            tensors["d_initial_state_mean"].shape[1],
            tensors["d_initial_state_mean"].shape[1],
            tensors["d_initial_state_mean"].shape[2],
        ],
        dtype=tf.float64,
    )
    zeros_pp_nn = tf.zeros(
        [
            tensors["d_initial_state_covariance"].shape[1],
            tensors["d_initial_state_covariance"].shape[1],
            tensors["d_initial_state_covariance"].shape[2],
            tensors["d_initial_state_covariance"].shape[3],
        ],
        dtype=tf.float64,
    )
    zeros_pp_m = tf.zeros(
        [
            tensors["d_observation_offset"].shape[1],
            tensors["d_observation_offset"].shape[1],
            tensors["d_observation_offset"].shape[2],
        ],
        dtype=tf.float64,
    )
    zeros_pp_mn = tf.zeros(
        [
            tensors["d_observation_matrix"].shape[1],
            tensors["d_observation_matrix"].shape[1],
            tensors["d_observation_matrix"].shape[2],
            tensors["d_observation_matrix"].shape[3],
        ],
        dtype=tf.float64,
    )
    zeros_pp_mm = tf.zeros(
        [
            tensors["d_observation_covariance"].shape[1],
            tensors["d_observation_covariance"].shape[1],
            tensors["d_observation_covariance"].shape[2],
            tensors["d_observation_covariance"].shape[3],
        ],
        dtype=tf.float64,
    )
    derivatives = TFLinearGaussianStateSpaceDerivatives(
        d_initial_mean=tensors["d_initial_state_mean"][row],
        d_initial_covariance=tensors["d_initial_state_covariance"][row],
        d_transition_offset=tensors["d_transition_offset"][row],
        d_transition_matrix=tensors["d_transition_matrix"][row],
        d_transition_covariance=tensors["d_transition_covariance"][row],
        d_observation_offset=tensors["d_observation_offset"][row],
        d_observation_matrix=tensors["d_observation_matrix"][row],
        d_observation_covariance=tensors["d_observation_covariance"][row],
        d2_initial_mean=zeros_pp_n,
        d2_initial_covariance=zeros_pp_nn,
        d2_transition_offset=zeros_pp_n,
        d2_transition_matrix=zeros_pp_nn,
        d2_transition_covariance=zeros_pp_nn,
        d2_observation_offset=zeros_pp_m,
        d2_observation_matrix=zeros_pp_mn,
        d2_observation_covariance=zeros_pp_mm,
    )
    return model, derivatives


def _scalar_value_score(
    tensors: dict[str, tf.Tensor],
    row: int,
    *,
    jitter: float,
) -> tuple[float, np.ndarray]:
    model, derivatives = _scalar_model_and_derivatives(tensors, row)
    value = tf_linear_gaussian_log_likelihood(
        tensors["observations"],
        model,
        jitter=tf.constant(jitter, dtype=tf.float64),
    ).log_likelihood
    score_result = tf_qr_linear_gaussian_score(
        tensors["observations"],
        model,
        derivatives,
        jitter=tf.constant(jitter, dtype=tf.float64),
    )
    return float(value.numpy()), score_result.score.numpy()


def main() -> None:
    args = _parse_args()
    fixture = _stable_fixture(
        batch_size=args.batch_size,
        time_steps=args.time_steps,
        state_dim=args.state_dim,
        obs_dim=args.obs_dim,
        parameter_dim=args.parameter_dim,
    )
    tensors = _to_tensors(fixture)
    rows = _parse_rows(args.rows, args.batch_size)
    batched_value, batched_score = _batched_value_score(tensors, jitter=args.jitter)

    row_results: list[dict[str, Any]] = []
    max_abs_value_error = 0.0
    max_abs_score_error = 0.0
    max_rel_value_error = 0.0
    max_rel_score_error = 0.0
    passed = True
    for row in rows:
        scalar_value, scalar_score = _scalar_value_score(tensors, row, jitter=args.jitter)
        value_error = float(abs(batched_value[row] - scalar_value))
        score_errors = np.abs(batched_score[row] - scalar_score)
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
                "batched_value": float(batched_value[row]),
                "scalar_value": scalar_value,
                "value_abs_error": value_error,
                "value_rel_error": value_rel_error,
                "value_pass": bool(value_pass),
                "batched_score": batched_score[row].tolist(),
                "scalar_score": scalar_score.tolist(),
                "score_abs_error_max": score_error,
                "score_rel_error_max": score_rel_error,
                "score_pass": score_pass,
                "row_pass": row_pass,
            }
        )

    finite = bool(np.isfinite(batched_value).all() and np.isfinite(batched_score).all())
    result: dict[str, Any] = {
        "timestamp_utc": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        "host": platform.node(),
        "python": platform.python_version(),
        "tensorflow": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "shape": {
            "batch_size": args.batch_size,
            "time_steps": args.time_steps,
            "state_dim": args.state_dim,
            "obs_dim": args.obs_dim,
            "parameter_dim": args.parameter_dim,
        },
        "rows": rows,
        "tolerances": {
            "value_rtol": args.value_rtol,
            "value_atol": args.value_atol,
            "score_rtol": args.score_rtol,
            "score_atol": args.score_atol,
        },
        "finite_batched_outputs": finite,
        "passed": bool(passed and finite),
        "max_abs_value_error": max_abs_value_error,
        "max_rel_value_error": max_rel_value_error,
        "max_abs_score_error": max_abs_score_error,
        "max_rel_score_error": max_rel_score_error,
        "row_results": row_results,
        "notes": [
            "Compares selected batched rows against existing scalar value and QR analytic score APIs.",
            "This is a row-sample parity check, not exhaustive parity across every batch row.",
        ],
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
