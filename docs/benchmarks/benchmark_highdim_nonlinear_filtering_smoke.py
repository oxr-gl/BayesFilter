"""CPU-only diagnostic harness for high-dimensional nonlinear filtering chapters.

The harness is intentionally narrow.  It records exact tested-cell execution
metadata for existing BayesFilter nonlinear sigma-point paths and block
high-dimensional fixtures.  It is not a production benchmark, not a posterior
accuracy test, and not evidence for a default backend change.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

_PRE_PARSER = argparse.ArgumentParser(add_help=False)
_PRE_PARSER.add_argument(
    "--requested-device",
    choices=("cpu",),
    default="cpu",
    help="This harness is CPU-only and hides GPU before TensorFlow import.",
)
_PRE_ARGS, _ = _PRE_PARSER.parse_known_args()
if _PRE_ARGS.requested_device == "cpu":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-bayesfilter")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf  # noqa: E402

from bayesfilter.nonlinear.cut_tf import tf_cut4g_sigma_point_rule  # noqa: E402
from bayesfilter.nonlinear.sigma_points_tf import (  # noqa: E402
    tf_svd_sigma_point_log_likelihood,
    tf_unit_sigma_point_rule,
)
from bayesfilter.nonlinear.svd_cut_tf import tf_svd_cut4_log_likelihood  # noqa: E402
from bayesfilter.structural import StatePartition, StructuralFilterConfig  # noqa: E402
from bayesfilter.structural_tf import TFStructuralStateSpace  # noqa: E402
from bayesfilter.testing import (  # noqa: E402
    make_nonlinear_accumulation_model_tf,
    model_b_observations_tf,
)


NON_IMPLICATION_TEXT = (
    "P8 smoke rows are BayesFilter execution diagnostics only. They do not "
    "certify high-dimensional filtering validity, HMC readiness, NAWM "
    "readiness, GPU speedup, XLA readiness, posterior accuracy, or production "
    "default policy."
)


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def _git_dirty() -> bool:
    try:
        return bool(
            subprocess.check_output(
                ["git", "status", "--short"],
                cwd=ROOT,
                text=True,
            ).strip()
        )
    except Exception:
        return True


def _max_rss_mb() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def _json_safe(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    return value


def _safe_float(value: Any) -> float | None:
    number = float(value)
    return number if math.isfinite(number) else None


def _point_count(backend: str, augmented_dim: int) -> int:
    if backend == "tf_svd_cut4":
        return 2 * augmented_dim + 2**augmented_dim
    rule = "cubature" if backend == "tf_svd_cubature" else "unscented"
    return int(tf_unit_sigma_point_rule(augmented_dim, rule=rule).point_count)


def _make_block_nonlinear_accumulation_model(
    block_count: int,
) -> TFStructuralStateSpace:
    state_dim = 2 * block_count
    innovation_dim = block_count
    stochastic_indices = tuple(2 * i for i in range(block_count))
    deterministic_indices = tuple(2 * i + 1 for i in range(block_count))
    partition = StatePartition(
        state_names=tuple(
            name
            for i in range(block_count)
            for name in (f"m_{i}", f"k_{i}")
        ),
        stochastic_indices=stochastic_indices,
        deterministic_indices=deterministic_indices,
        innovation_dim=innovation_dim,
    )
    config = StructuralFilterConfig(
        integration_space="innovation",
        deterministic_completion="required",
        approximation_label="block_nonlinear_accumulation_testing_fixture",
    )
    rho = tf.constant(0.70, dtype=tf.float64)
    sigma = tf.constant(0.25, dtype=tf.float64)
    alpha = tf.constant(0.55, dtype=tf.float64)
    beta = tf.constant(0.80, dtype=tf.float64)

    def _as_points(value: tf.Tensor) -> tf.Tensor:
        tensor = tf.convert_to_tensor(value, dtype=tf.float64)
        if tensor.shape.rank == 1:
            return tensor[tf.newaxis, :]
        return tensor

    def transition_fn(previous_state: tf.Tensor, innovation: tf.Tensor) -> tf.Tensor:
        was_vector = tf.convert_to_tensor(previous_state).shape.rank == 1
        previous = _as_points(previous_state)
        eps = _as_points(innovation)
        states = []
        for i in range(block_count):
            previous_m = previous[:, 2 * i]
            previous_k = previous[:, 2 * i + 1]
            m_next = rho * previous_m + sigma * eps[:, i]
            k_next = alpha * previous_k + beta * tf.math.tanh(m_next)
            states.extend([m_next, k_next])
        next_points = tf.stack(states, axis=1)
        return next_points[0] if was_vector else next_points

    def observation_fn(state_points: tf.Tensor) -> tf.Tensor:
        was_vector = tf.convert_to_tensor(state_points).shape.rank == 1
        points = _as_points(state_points)
        observations = []
        for i in range(block_count):
            observations.append(points[:, 2 * i] + points[:, 2 * i + 1])
        obs = tf.stack(observations, axis=1)
        return obs[0] if was_vector else obs

    def residual_fn(
        previous_state: tf.Tensor,
        innovation: tf.Tensor,
        next_state: tf.Tensor,
    ) -> tf.Tensor:
        del innovation
        previous = _as_points(previous_state)
        next_points = _as_points(next_state)
        residuals = []
        for i in range(block_count):
            expected = alpha * previous[:, 2 * i + 1] + beta * tf.math.tanh(
                next_points[:, 2 * i]
            )
            residuals.append(next_points[:, 2 * i + 1] - expected)
        return tf.stack(residuals, axis=1)

    return TFStructuralStateSpace(
        partition=partition,
        config=config,
        initial_mean=tf.zeros([state_dim], dtype=tf.float64),
        initial_covariance=tf.linalg.diag(
            tf.tile(tf.constant([0.25, 0.20], dtype=tf.float64), [block_count])
        ),
        innovation_covariance=tf.eye(innovation_dim, dtype=tf.float64),
        observation_covariance=0.09 * tf.eye(block_count, dtype=tf.float64),
        transition_fn=transition_fn,
        observation_fn=observation_fn,
        deterministic_residual_fn=residual_fn,
        name=f"block_nonlinear_accumulation_{block_count}",
    )


def _observations_for_case(case: str, block_count: int) -> tf.Tensor:
    if case == "model_b":
        return model_b_observations_tf()
    base = tf.constant([0.10, 0.04, 0.16], dtype=tf.float64)[:, tf.newaxis]
    offsets = tf.linspace(
        tf.constant(0.0, dtype=tf.float64),
        tf.constant(0.02, dtype=tf.float64),
        block_count,
    )[tf.newaxis, :]
    return base + offsets


def _model_for_case(case: str, block_count: int) -> TFStructuralStateSpace:
    if case == "model_b":
        return make_nonlinear_accumulation_model_tf()
    return _make_block_nonlinear_accumulation_model(block_count)


def _raw_metrics(
    observations: tf.Tensor,
    model: TFStructuralStateSpace,
    backend: str,
) -> tuple[tf.Tensor, tf.Tensor, tf.Tensor]:
    if backend == "tf_svd_cut4":
        value, _, _, diagnostics = tf_svd_cut4_log_likelihood(
            observations,
            model,
            return_filtered=False,
        )
    else:
        rule = "cubature" if backend == "tf_svd_cubature" else "unscented"
        value, _, _, diagnostics = tf_svd_sigma_point_log_likelihood(
            observations,
            model,
            rule=rule,
            return_filtered=False,
        )
    return (
        value,
        diagnostics["deterministic_residual"],
        diagnostics["support_residual"],
    )


def _run_filter(
    observations: tf.Tensor,
    model: TFStructuralStateSpace,
    backend: str,
    mode: str,
) -> tuple[tuple[tf.Tensor, tf.Tensor, tf.Tensor], float]:
    fn = lambda: _raw_metrics(observations, model, backend)
    if mode == "xla":
        compiled = tf.function(fn, jit_compile=True)
        compiled()
        start = time.perf_counter()
        metrics = compiled()
    else:
        fn()
        start = time.perf_counter()
        metrics = fn()
    runtime = time.perf_counter() - start
    _ = float(metrics[0].numpy())
    return metrics, runtime


def _row(
    *,
    case: str,
    block_count: int,
    backend: str,
    mode: str,
    point_cap: int,
    command: str,
    environment: dict[str, Any],
) -> dict[str, Any]:
    model = _model_for_case(case, block_count)
    observations = _observations_for_case(case, block_count)
    augmented_dim = model.partition.state_dim + model.partition.innovation_dim
    point_count = _point_count(backend, augmented_dim)
    shape = {
        "state_dim": model.partition.state_dim,
        "observation_dim": int(model.observation_dim),
        "innovation_dim": model.partition.innovation_dim,
        "timesteps": int(observations.shape[0]),
        "augmented_dim": augmented_dim,
        "point_count": point_count,
    }
    base = {
        "case": case,
        "block_count": block_count,
        "state_dim": shape["state_dim"],
        "innovation_dim": shape["innovation_dim"],
        "observation_dim": shape["observation_dim"],
        "timesteps": shape["timesteps"],
        "backend": backend,
        "mode": mode,
        "augmented_dim": shape["augmented_dim"],
        "point_count": shape["point_count"],
        "shape": shape,
        "dtype": "float64",
        "seed_policy": "deterministic_fixture_no_random_seed",
        "tolerance": "finite_and_shape_only",
        "comparator": "Existing Model B or deterministic block extension",
        "comparator_id": "existing_model_b_or_block_extension",
        "cpu_gpu_policy": "CPU-only; CUDA_VISIBLE_DEVICES=-1 set before TensorFlow import",
        "command": command,
        "environment": environment,
        "non_implication": NON_IMPLICATION_TEXT,
        "non_implication_text": NON_IMPLICATION_TEXT,
    }
    if point_count > point_cap:
        return {
            **base,
            "row_status": "skipped",
            "finite_status": "not_run",
            "shape_status": "not_run",
            "runtime_seconds": None,
            "max_rss_mb": _max_rss_mb(),
            "promotion_label": "not_promoted",
            "continuation_label": "skip_point_cap_for_scaling_diagnostic",
            "repair_label": "use_block_local_or_low_rank_rule_before_large_cut4",
            "skip_reason": f"point_count {point_count} exceeds cap {point_cap}",
        }
    try:
        metrics, runtime = _run_filter(observations, model, backend, mode)
        value = _safe_float(metrics[0].numpy())
        return {
            **base,
            "row_status": "ok",
            "finite_status": "pass" if value is not None else "fail",
            "shape_status": "pass",
            "runtime_seconds": runtime,
            "max_rss_mb": _max_rss_mb(),
            "log_likelihood": value,
            "deterministic_residual": _safe_float(metrics[1].numpy()),
            "support_residual": _safe_float(metrics[2].numpy()),
            "promotion_label": "not_promoted",
            "continuation_label": "diagnostic_only",
            "repair_label": "none",
            "skip_reason": "",
        }
    except Exception as exc:  # pragma: no cover - diagnostic artifact path.
        return {
            **base,
            "row_status": "error",
            "finite_status": "fail",
            "shape_status": "fail",
            "runtime_seconds": None,
            "max_rss_mb": _max_rss_mb(),
            "promotion_label": "not_promoted",
            "continuation_label": "diagnostic_error",
            "repair_label": "inspect_exception_before_reuse",
            "skip_reason": "",
            "error": repr(exc),
        }


def _write_markdown(output: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# High-Dimensional Nonlinear Filtering Smoke Diagnostic",
        "",
        f"JSON artifact: `{payload['artifact_path']}`",
        "",
        "Diagnostic only.  No high-dimensional filtering, HMC, GPU, XLA, NAWM, "
        "posterior-accuracy, or production-default claim is made.",
        "",
        "## Environment",
        "",
        f"- Python: `{payload['environment']['python']}`",
        f"- TensorFlow: `{payload['environment']['tensorflow']}`",
        f"- CUDA_VISIBLE_DEVICES: `{payload['environment']['cuda_visible_devices']}`",
        f"- Command: `{payload['command']}`",
        "",
        "## Rows",
        "",
        "| Case | Blocks | Backend | Mode | Aug Dim | Points | Status | Runtime s | Label |",
        "| --- | ---: | --- | --- | ---: | ---: | --- | ---: | --- |",
    ]
    for row in payload["rows"]:
        runtime = row["runtime_seconds"]
        runtime_text = "" if runtime is None else f"{runtime:.6f}"
        lines.append(
            "| {case} | {block_count} | {backend} | {mode} | {augmented_dim} | "
            "{point_count} | {row_status} | {runtime} | {continuation_label} |".format(
                runtime=runtime_text,
                **row,
            )
        )
    lines.extend(
        [
            "",
            "## Non-Implication",
            "",
            NON_IMPLICATION_TEXT,
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--point-cap", type=int, default=256)
    parser.add_argument("--modes", nargs="+", default=["eager", "xla"])
    parser.add_argument(
        "--cases",
        nargs="+",
        default=["model_b:1", "block_model_b:2", "block_model_b:4"],
    )
    args = parser.parse_args()

    command = " ".join(sys.argv)
    environment = {
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "tensorflow": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", ""),
        "logical_devices": [
            {"name": device.name, "type": device.device_type}
            for device in tf.config.list_logical_devices()
        ],
    }
    rows = []
    for case_spec in args.cases:
        case, block_text = case_spec.split(":", maxsplit=1)
        block_count = int(block_text)
        for backend in ("tf_svd_cubature", "tf_svd_ukf", "tf_svd_cut4"):
            for mode in args.modes:
                rows.append(
                    _row(
                        case=case,
                        block_count=block_count,
                        backend=backend,
                        mode=mode,
                        point_cap=args.point_cap,
                        command=command,
                        environment=environment,
                    )
                )
    output = Path(args.output)
    payload = {
        "artifact_path": str(output),
        "plan": "docs/plans/bayesfilter-highdim-nonlinear-filtering-monograph-p8-evidence-harness-plan-2026-05-27.md",
        "command": command,
        "environment": environment,
        "git_commit": _git_commit(),
        "git_dirty": _git_dirty(),
        "rows": rows,
        "non_implication": NON_IMPLICATION_TEXT,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")
    _write_markdown(Path(args.markdown_output), payload)


if __name__ == "__main__":
    main()
