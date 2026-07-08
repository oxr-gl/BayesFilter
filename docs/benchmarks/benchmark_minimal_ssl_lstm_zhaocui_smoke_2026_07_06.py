"""Minimal scalar SSL-LSTM Zhao-Cui fixed mechanics smoke.

This harness materializes the one-dimensional ``zhaocui_fixed`` fixture as a
structured debug artifact.  It is a smoke runner only: it does not run HMC and
does not claim posterior correctness, source-faithful Zhao-Cui parity, ranking,
GPU/XLA production readiness, default readiness, or LEDH evidence.
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
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from typing import Any


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402

from bayesfilter.nonlinear.ssl_lstm_protocol import (  # noqa: E402
    SSLLSTMStaticConfig,
    validate_ssl_lstm_value_score_artifact,
)
from bayesfilter.nonlinear.ssl_lstm_sgqf_ukf_adapters import (  # noqa: E402
    build_ssl_lstm_debug_value_score_artifact,
    tf_ssl_lstm_fixed_sgqf_score,
    tf_ssl_lstm_svd_ukf_score,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_fixed_adapter import (  # noqa: E402
    SSLLSTMZhaoCuiFixedManifest,
    build_ssl_lstm_zhaocui_fixed_value_score_artifact,
    tf_ssl_lstm_zhaocui_fixed_score,
)
from bayesfilter.runtime import atomic_write_json  # noqa: E402


DATE_STAMP = "2026-07-06"
SCRIPT_NAME = "benchmark_minimal_ssl_lstm_zhaocui_smoke_2026_07_06.py"
DEFAULT_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.json"
)
DEFAULT_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_smoke_cpu_hidden_2026-07-06.md"
)
MASTER_PROGRAM_PATH = (
    "docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-master-program-2026-07-06.md"
)
PHASE1_SUBPLAN_PATH = (
    "docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-subplan-2026-07-06.md"
)
PHASE1_RESULT_PATH = (
    "docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase1-harness-result-2026-07-06.md"
)
ZHAOCUI_EVIDENCE_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-"
    "zhaocui-fixed-adapter-implementation-result-2026-07-05.md"
)
COMPARATOR_EVIDENCE_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-phase3-sgqf-ukf-analytic-adapters-result-2026-07-04.md"
)
FD_INDICES = (0, 4, 8, 12, 13, 14, 15, 16, 19, 22)
FD_STEP = 1.0e-5
FD_RTOL = 4.0e-3
FD_ATOL = 7.0e-4
NONCLAIMS = (
    "minimal scalar mechanics smoke only",
    "CPU-hidden debug artifact only",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not LEDH evidence",
)


def minimal_config() -> SSLLSTMStaticConfig:
    """Return the frozen scalar SSL-LSTM fixture dimensions."""

    return SSLLSTMStaticConfig(
        horizon=2,
        latent_dim=1,
        hidden_dim=1,
        observation_dim=1,
    )


def minimal_theta() -> tf.Tensor:
    """Return the frozen scalar fixture parameter vector."""

    config = minimal_config()
    values = np.zeros(config.parameter_dim, dtype=np.float64)
    values[0:4] = np.array([0.09, -0.07, 0.05, 0.04])
    values[4:8] = np.array([0.03, -0.02, 0.06, -0.05])
    values[8:12] = np.array([0.01, 0.04, -0.03, 0.02])
    values[12] = 0.35
    values[13] = -0.08
    values[14] = 0.65
    values[15] = 0.05
    values[16:19] = np.array([0.15, -0.10, 0.20])
    values[19:22] = np.array([-0.35, 0.15, 0.55])
    values[22] = 0.35
    values[-1] = -0.15
    return tf.constant(values, dtype=tf.float64)


def minimal_observations() -> tf.Tensor:
    """Return the frozen two-step scalar observation fixture."""

    return tf.constant([[0.12], [-0.03]], dtype=tf.float64)


def minimal_zhaocui_manifest() -> SSLLSTMZhaoCuiFixedManifest:
    """Return the fixed replay manifest used by the scalar test fixture."""

    return SSLLSTMZhaoCuiFixedManifest(
        reference_sample_count=9,
        initial_seed=(20260705, 41),
        process_seed=(20260705, 43),
    )


def finite_difference_subset(
    theta: tf.Tensor,
    value_fn: Callable[[tf.Tensor], tf.Tensor],
    *,
    indices: Iterable[int] = FD_INDICES,
    step: float = FD_STEP,
) -> dict[str, Any]:
    """Compute a reference finite-difference subset for a value function."""

    base = np.asarray(theta.numpy(), dtype=np.float64)
    index_tuple = tuple(int(index) for index in indices)
    values: list[float] = []
    for index in index_tuple:
        plus = base.copy()
        minus = base.copy()
        plus[index] += step
        minus[index] -= step
        plus_value = value_fn(tf.constant(plus, dtype=tf.float64))
        minus_value = value_fn(tf.constant(minus, dtype=tf.float64))
        values.append(
            float((plus_value - minus_value).numpy()) / (2.0 * float(step))
        )
    return {
        "indices": index_tuple,
        "step": float(step),
        "values": values,
    }


def _score_vector(result: Any) -> np.ndarray:
    return np.asarray(tf.reshape(tf.convert_to_tensor(result.score, dtype=tf.float64), [-1]).numpy())


def _value_float(result: Any) -> float:
    return float(tf.convert_to_tensor(result.log_likelihood, dtype=tf.float64).numpy())


def _max_fd_error(score: np.ndarray, fd: Mapping[str, Any]) -> float:
    indices = [int(index) for index in fd["indices"]]
    values = np.asarray(fd["values"], dtype=np.float64)
    return float(np.max(np.abs(score[indices] - values)))


def _score_finite(value: float, score: np.ndarray) -> bool:
    return bool(math.isfinite(value) and np.all(np.isfinite(score)))


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except Exception:  # noqa: BLE001
        return "unknown"


def _git_dirty_summary() -> dict[str, Any]:
    try:
        status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True)
    except Exception:  # noqa: BLE001
        status = ""
    lines = [line for line in status.splitlines() if line.strip()]
    return {
        "dirty": bool(lines),
        "line_count": len(lines),
        "preview": lines[:20],
    }


def _tf_device_summary() -> dict[str, Any]:
    physical = tf.config.list_physical_devices()
    return {
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>"),
        "physical_devices": [device.name for device in physical],
        "gpu_devices": [device.name for device in tf.config.list_physical_devices("GPU")],
        "trust_basis": "cpu_hidden_debug_no_gpu_claim",
    }


def evaluate_zhaocui_fixed() -> dict[str, Any]:
    """Evaluate the primary scalar ``zhaocui_fixed`` smoke row."""

    config = minimal_config()
    theta = minimal_theta()
    observations = minimal_observations()
    manifest = minimal_zhaocui_manifest()
    start = time.perf_counter()
    result, components = tf_ssl_lstm_zhaocui_fixed_score(
        observations,
        theta,
        config,
        evidence_path=ZHAOCUI_EVIDENCE_PATH,
        manifest=manifest,
    )
    repeated, _ = tf_ssl_lstm_zhaocui_fixed_score(
        observations,
        theta,
        config,
        evidence_path=ZHAOCUI_EVIDENCE_PATH,
        manifest=manifest,
    )
    runtime_s = time.perf_counter() - start

    def value_fn(theta_value: tf.Tensor) -> tf.Tensor:
        local, _components = tf_ssl_lstm_zhaocui_fixed_score(
            observations,
            theta_value,
            config,
            evidence_path=ZHAOCUI_EVIDENCE_PATH,
            manifest=manifest,
        )
        return local.log_likelihood

    score = _score_vector(result)
    repeated_score = _score_vector(repeated)
    fd = finite_difference_subset(theta, value_fn)
    fd_error = _max_fd_error(score, fd)
    artifact = dict(
        build_ssl_lstm_zhaocui_fixed_value_score_artifact(
            protocol=components.protocol,
            manifest=components.manifest,
            log_likelihood=result.log_likelihood,
            score=result.score,
            finite_difference_max_abs_error=fd_error,
            artifact_role="debug_reference",
            compile_mode="eager",
            jit_compile=False,
            device="CPU-hidden debug",
            tf32_enabled=False,
        )
    )
    validate_ssl_lstm_value_score_artifact(artifact, protocol=components.protocol)
    max_repeat_delta = max(
        abs(_value_float(result) - _value_float(repeated)),
        float(np.max(np.abs(score - repeated_score))),
    )
    fd_pass = bool(np.allclose(score[list(fd["indices"])], fd["values"], rtol=FD_RTOL, atol=FD_ATOL))
    artifact.update(
        {
            "candidate_role": "primary_filter",
            "fixture": _fixture_payload(config, theta, observations),
            "runtime_s": float(runtime_s),
            "score_norm": float(np.linalg.norm(score)),
            "determinism_check": {
                "max_abs_delta": float(max_repeat_delta),
                "passed": bool(max_repeat_delta <= 1.0e-12),
                "role": "promotion_veto_for_smoke_admission",
            },
            "finite_difference_check": {
                **artifact["finite_difference_check"],
                "indices": list(fd["indices"]),
                "step": float(fd["step"]),
                "finite_difference_values": [float(item) for item in fd["values"]],
                "analytic_subset_values": [float(score[index]) for index in fd["indices"]],
                "rtol": FD_RTOL,
                "atol": FD_ATOL,
                "passed": fd_pass,
            },
            "diagnostic_roles": {
                **dict(artifact["diagnostic_roles"]),
                "determinism_check": "promotion_veto_for_smoke_admission",
                "fixture_dimensions": "promotion_veto_for_smoke_admission",
            },
        }
    )
    return artifact


def evaluate_comparator(filter_name: str) -> dict[str, Any]:
    """Evaluate a descriptive mechanics comparator row."""

    config = minimal_config()
    theta = minimal_theta()
    observations = minimal_observations()
    start = time.perf_counter()
    if filter_name == "fixed_sgqf":
        result, components = tf_ssl_lstm_fixed_sgqf_score(
            observations,
            theta,
            config,
            evidence_path=COMPARATOR_EVIDENCE_PATH,
            sparse_level=2,
        )
    elif filter_name == "svd_ukf":
        result, components = tf_ssl_lstm_svd_ukf_score(
            observations,
            theta,
            config,
            evidence_path=COMPARATOR_EVIDENCE_PATH,
            spectral_gap_tolerance=tf.constant(1.0e-10, dtype=tf.float64),
        )
    else:
        raise ValueError(f"unknown comparator: {filter_name}")
    runtime_s = time.perf_counter() - start
    score = _score_vector(result)
    artifact = dict(
        build_ssl_lstm_debug_value_score_artifact(
            protocol=components.protocol,
            log_likelihood=result.log_likelihood,
            score=result.score,
            finite_difference_max_abs_error=0.0,
            artifact_role="debug_reference",
            compile_mode="eager",
            jit_compile=False,
            device="CPU-hidden debug",
            tf32_enabled=False,
            nonclaims=(
                "descriptive mechanics comparator only",
                "not a promotion criterion for the minimal zhaocui_fixed smoke",
                "not a ranking or superiority claim",
                "not HMC convergence evidence",
                "not posterior correctness evidence",
            ),
        )
    )
    artifact.update(
        {
            "candidate_role": "mechanics_comparator_descriptive_only",
            "runtime_s": float(runtime_s),
            "score_norm": float(np.linalg.norm(score)),
            "comparison_role": "descriptive_only_not_primary_criterion",
            "finite_difference_check": {
                **artifact["finite_difference_check"],
                "role": "explanatory",
                "note": "not recomputed in minimal smoke comparator row",
            },
            "diagnostic_roles": {
                **dict(artifact["diagnostic_roles"]),
                "finite_difference_check": "explanatory",
                "runtime": "explanatory",
                "score_norm": "explanatory",
                "comparator_value": "explanatory",
            },
        }
    )
    return artifact


def build_smoke_artifact(command: tuple[str, ...] | None = None) -> dict[str, Any]:
    """Build the complete minimal smoke artifact."""

    config = minimal_config()
    theta = minimal_theta()
    observations = minimal_observations()
    primary = evaluate_zhaocui_fixed()
    comparators = [evaluate_comparator("fixed_sgqf"), evaluate_comparator("svd_ukf")]
    fixture_ok = (
        config.latent_dim == 1
        and config.hidden_dim == 1
        and config.observation_dim == 1
        and config.horizon == 2
    )
    primary_pass = bool(
        primary["score_finite"]
        and primary["finite_difference_check"]["passed"]
        and primary["determinism_check"]["passed"]
        and fixture_ok
    )
    artifact = {
        "schema_version": "minimal_ssl_lstm_zhaocui_smoke.v1",
        "status": "passed" if primary_pass else "failed",
        "date": DATE_STAMP,
        "primary_filter": "zhaocui_fixed",
        "primary_filter_role": "promotion_criterion_for_minimal_mechanics_smoke",
        "comparator_role": "fixed_sgqf_and_svd_ukf_are_mechanics_comparators_only",
        "fixture": _fixture_payload(config, theta, observations),
        "evidence_contract": {
            "question": (
                "Can the minimal scalar SSL-LSTM zhaocui_fixed mechanics be "
                "materialized as a structured smoke artifact?"
            ),
            "baseline_comparator": (
                "Existing tests/test_ssl_lstm_zhaocui_fixed_adapter.py fixture; "
                "fixed_sgqf and svd_ukf are mechanics comparators only."
            ),
            "primary_pass_criterion": (
                "Scalar dimensions, finite deterministic zhaocui_fixed value/score, "
                "schema-valid artifact, and finite-difference subset agreement."
            ),
            "veto_diagnostics": (
                "Nonfinite value/score, nondeterminism, FD mismatch, invalid schema, "
                "wrong dimensions, target autodiff/NumPy, or unsupported claim."
            ),
            "explanatory_diagnostics": (
                "Runtime, score norm, comparator values, reference sample count, "
                "and recenter diagnostics."
            ),
            "not_concluded": NONCLAIMS,
        },
        "run_manifest": {
            "git_commit": _git_commit(),
            "git_dirty_summary": _git_dirty_summary(),
            "command": list(command or (sys.executable, str(Path(__file__).resolve()))),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "cpu_gpu_status": _tf_device_summary(),
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "compile_mode": "eager",
            "jit_compile": False,
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE1_SUBPLAN_PATH,
            "result_file": PHASE1_RESULT_PATH,
            "random_seeds": {
                "zhaocui_initial_seed": list(minimal_zhaocui_manifest().initial_seed),
                "zhaocui_process_seed": list(minimal_zhaocui_manifest().process_seed),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
        },
        "primary_result": primary,
        "comparator_rows": comparators,
        "gate_diagnostics": {
            "fixture_dimensions_passed": fixture_ok,
            "primary_score_finite": bool(primary["score_finite"]),
            "primary_determinism_passed": bool(primary["determinism_check"]["passed"]),
            "primary_fd_passed": bool(primary["finite_difference_check"]["passed"]),
            "comparator_rows_all_finite": all(
                _score_finite(float(row["log_likelihood"]), np.asarray(row["score"], dtype=np.float64))
                for row in comparators
            ),
        },
        "nonclaims": NONCLAIMS,
    }
    return artifact


def _fixture_payload(
    config: SSLLSTMStaticConfig,
    theta: tf.Tensor,
    observations: tf.Tensor,
) -> dict[str, Any]:
    return {
        "horizon": int(config.horizon),
        "latent_dim": int(config.latent_dim),
        "hidden_dim": int(config.hidden_dim),
        "observation_dim": int(config.observation_dim),
        "augmented_state_dim": int(config.augmented_state_dim),
        "parameter_dim": int(config.parameter_dim),
        "observations": [[float(value) for value in row] for row in observations.numpy()],
        "theta": [float(value) for value in tf.reshape(theta, [-1]).numpy()],
    }


def write_markdown(path: Path, artifact: Mapping[str, Any]) -> None:
    """Write a compact human-readable smoke summary."""

    primary = artifact["primary_result"]
    fd = primary["finite_difference_check"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui Smoke",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Primary filter: `{artifact['primary_filter']}`",
        f"- Primary role: `{artifact['primary_filter_role']}`",
        f"- Comparator role: `{artifact['comparator_role']}`",
        f"- Dimensions: latent `{artifact['fixture']['latent_dim']}`, hidden `{artifact['fixture']['hidden_dim']}`, observation `{artifact['fixture']['observation_dim']}`, horizon `{artifact['fixture']['horizon']}`",
        f"- Log likelihood: `{primary['log_likelihood']}`",
        f"- Score norm: `{primary['score_norm']}`",
        f"- FD max abs error: `{fd['max_abs_error']}`",
        f"- FD passed: `{fd['passed']}`",
        f"- Determinism passed: `{primary['determinism_check']['passed']}`",
        "",
        "## Comparator Rows",
        "",
        "| filter | role | score finite | log likelihood | score norm |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in artifact["comparator_rows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["filter_name"]),
                    str(row["candidate_role"]),
                    str(row["score_finite"]),
                    str(row["log_likelihood"]),
                    str(row["score_norm"]),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE1_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE1_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", default=str(DEFAULT_JSON_OUTPUT))
    parser.add_argument("--markdown-output", default=str(DEFAULT_MARKDOWN_OUTPUT))
    parser.add_argument("--require-cpu-hidden", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.require_cpu_hidden and os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise RuntimeError("minimal smoke requires CUDA_VISIBLE_DEVICES=-1")
    started = time.perf_counter()
    artifact = build_smoke_artifact(command=tuple(sys.argv))
    artifact["run_manifest"]["wall_time_s"] = float(time.perf_counter() - started)
    artifact["run_manifest"]["timestamp"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    output = Path(args.output)
    markdown_output = Path(args.markdown_output)
    atomic_write_json(output, artifact)
    write_markdown(markdown_output, artifact)
    print(
        json.dumps(
            {
                "status": artifact["status"],
                "json_output": str(output),
                "markdown_output": str(markdown_output),
                "primary_fd_max_abs_error": artifact["primary_result"]["finite_difference_check"]["max_abs_error"],
            },
            sort_keys=True,
        )
    )
    return 0 if artifact["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
