"""Minimal SSL-LSTM quadratic initializer artifact smoke.

This diagnostic runs the reusable quadratic MAP-covariance initializer on the
minimal scalar ``zhaocui_fixed`` target.  It writes finite/SPD and coordinate
metadata for a later HMC-geometry-only phase.  It does not initialize HMC
geometry, run HMC, or establish sampler readiness.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.inference import (  # noqa: E402
    LowRankSPDQuadraticGeometryConfig,
    QuadraticMapCovarianceLocatorConfig,
    QuadraticMapCovarianceMassConfig,
    QUADRATIC_MAP_COVARIANCE_NONCLAIMS,
    estimate_quadratic_map_covariance,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS,
    MinimalZhaoCuiHMCTargetAdapter,
    initial_minimal_ssl_lstm_hmc_state,
    minimal_ssl_lstm_fixture_payload,
)


SCRIPT_NAME = "benchmark_minimal_ssl_lstm_quadratic_initializer_artifact_2026_07_08.py"
SCHEMA_VERSION = "minimal_ssl_lstm.quadratic_initializer_artifact.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase1-initializer-artifact-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase1-initializer-artifact-result-2026-07-08.md"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.md"
)
NONCLAIMS = (
    "Phase 1 initializer artifact smoke only",
    "CPU-hidden debug/reference exception only",
    "not an HMC geometry initialization result",
    "not an HMC runtime result",
    "not HMC readiness evidence",
    "not posterior correctness evidence",
    "not sampler convergence evidence",
    "not sampler superiority evidence",
    "not default-readiness evidence",
    "not GPU/XLA production-readiness evidence",
    "not source-faithful Zhao-Cui parity evidence",
)


@dataclass(frozen=True)
class MinimalQuadraticInitializerSettings:
    """Settings for the Phase 1 initializer smoke."""

    seed: tuple[int, int] = (20260708, 4101)
    initial_offset_scale: float = 1.0e-3
    locator_enabled: bool = False
    locator_max_iterations: int = 25
    locator_tolerance: float = 1.0e-7
    low_rank_rank: int = 4
    low_rank_sample_count: int = 220
    low_rank_min_samples_per_parameter: int = 5
    low_rank_trust_radius: float = 0.05
    low_rank_pilot_radius: float = 0.02
    low_rank_pilot_direction_count: int = 512
    low_rank_eigenvalue_floor: float = 1.0
    low_rank_max_condition_number: float = 1.0e3
    low_rank_holdout_rmse_abs_tolerance: float = 0.25
    low_rank_holdout_rmse_rel_tolerance: float = 0.10
    mass_jitter: float = 1.0e-9
    mass_eigenvalue_floor: float = 0.04
    mass_max_condition_number: float = 1.0e6

    def __post_init__(self) -> None:
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        object.__setattr__(self, "locator_enabled", bool(self.locator_enabled))
        for name in (
            "locator_max_iterations",
            "low_rank_rank",
            "low_rank_sample_count",
            "low_rank_min_samples_per_parameter",
            "low_rank_pilot_direction_count",
        ):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        for name in (
            "initial_offset_scale",
            "locator_tolerance",
            "low_rank_trust_radius",
            "low_rank_pilot_radius",
            "low_rank_eigenvalue_floor",
            "low_rank_max_condition_number",
            "low_rank_holdout_rmse_abs_tolerance",
            "low_rank_holdout_rmse_rel_tolerance",
            "mass_jitter",
            "mass_eigenvalue_floor",
            "mass_max_condition_number",
        ):
            value = float(getattr(self, name))
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if name == "mass_jitter":
                if value < 0.0:
                    raise ValueError(f"{name} must be non-negative")
            elif value <= 0.0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)

    @property
    def effective_low_rank_rank(self) -> int:
        dim = int(minimal_ssl_lstm_fixture_payload()["parameter_dim"])
        return min(self.low_rank_rank, max(dim - 1, 0))

    @property
    def regression_parameter_count(self) -> int:
        dim = int(minimal_ssl_lstm_fixture_payload()["parameter_dim"])
        return 1 + dim + 1 + self.effective_low_rank_rank

    @property
    def required_finite_samples(self) -> int:
        return self.low_rank_min_samples_per_parameter * self.regression_parameter_count

    def payload(self) -> Mapping[str, Any]:
        return {
            "seed": self.seed,
            "initial_offset_scale": self.initial_offset_scale,
            "locator_enabled": self.locator_enabled,
            "locator_max_iterations": self.locator_max_iterations,
            "locator_tolerance": self.locator_tolerance,
            "low_rank_rank": self.low_rank_rank,
            "effective_low_rank_rank": self.effective_low_rank_rank,
            "low_rank_sample_count": self.low_rank_sample_count,
            "low_rank_min_samples_per_parameter": self.low_rank_min_samples_per_parameter,
            "low_rank_trust_radius": self.low_rank_trust_radius,
            "low_rank_pilot_radius": self.low_rank_pilot_radius,
            "low_rank_pilot_direction_count": self.low_rank_pilot_direction_count,
            "low_rank_eigenvalue_floor": self.low_rank_eigenvalue_floor,
            "low_rank_max_condition_number": self.low_rank_max_condition_number,
            "low_rank_holdout_rmse_abs_tolerance": (
                self.low_rank_holdout_rmse_abs_tolerance
            ),
            "low_rank_holdout_rmse_rel_tolerance": (
                self.low_rank_holdout_rmse_rel_tolerance
            ),
            "mass_jitter": self.mass_jitter,
            "mass_eigenvalue_floor": self.mass_eigenvalue_floor,
            "mass_max_condition_number": self.mass_max_condition_number,
            "regression_parameter_count": self.regression_parameter_count,
            "required_finite_samples": self.required_finite_samples,
        }


def default_settings() -> MinimalQuadraticInitializerSettings:
    return MinimalQuadraticInitializerSettings()


def run_initializer_artifact(
    settings: MinimalQuadraticInitializerSettings | None = None,
    *,
    command: Sequence[str] | None = None,
) -> Mapping[str, Any]:
    cfg = default_settings() if settings is None else settings
    started_wall = datetime.now(UTC)
    started_perf = time.perf_counter()
    command_tuple = tuple(sys.argv if command is None else command)
    vetoes: list[str] = []
    errors: list[str] = []

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        vetoes.append("cpu_hidden_execution_not_confirmed")

    adapter = MinimalZhaoCuiHMCTargetAdapter(evidence_path=PLAN_PATH)
    initial_position = initial_minimal_ssl_lstm_hmc_state(cfg.initial_offset_scale)
    initial_value, initial_score = adapter.log_prob_and_grad(initial_position)
    initial_value_finite = bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy())
    initial_score_finite = bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy())
    if not initial_value_finite:
        vetoes.append("initial_target_value_nonfinite")
    if not initial_score_finite:
        vetoes.append("initial_target_score_nonfinite")

    result_payload: Mapping[str, Any] | None = None
    decision: dict[str, Any] = {}
    result = None
    if not vetoes:
        try:
            scale = np.full(int(adapter.parameter_dim), float(adapter.prior_scale), dtype=float)
            result = estimate_quadratic_map_covariance(
                adapter.log_prob_and_grad,
                initial_position,
                scale=scale,
                locator_config=QuadraticMapCovarianceLocatorConfig(
                    enabled=cfg.locator_enabled,
                    max_iterations=cfg.locator_max_iterations,
                    tolerance=cfg.locator_tolerance,
                    log_prob_tolerance=cfg.locator_tolerance,
                ),
                quadratic_config=LowRankSPDQuadraticGeometryConfig(
                    rank=cfg.low_rank_rank,
                    sample_count=cfg.low_rank_sample_count,
                    min_samples_per_parameter=cfg.low_rank_min_samples_per_parameter,
                    trust_radius=cfg.low_rank_trust_radius,
                    pilot_radius=cfg.low_rank_pilot_radius,
                    pilot_direction_count=cfg.low_rank_pilot_direction_count,
                    eigenvalue_floor=cfg.low_rank_eigenvalue_floor,
                    max_condition_number=cfg.low_rank_max_condition_number,
                    holdout_rmse_abs_tolerance=cfg.low_rank_holdout_rmse_abs_tolerance,
                    holdout_rmse_rel_tolerance=cfg.low_rank_holdout_rmse_rel_tolerance,
                    seed=cfg.seed,
                ),
                mass_config=QuadraticMapCovarianceMassConfig(
                    jitter=cfg.mass_jitter,
                    eigenvalue_floor=cfg.mass_eigenvalue_floor,
                    max_condition_number=cfg.mass_max_condition_number,
                ),
            )
            result_payload = result.payload(include_arrays=True)
        except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
            vetoes.append("initializer_runtime_exception")
            errors.append(f"{type(exc).__name__}: {exc}")

    if result is not None:
        if not result.accepted:
            vetoes.append(f"initializer_rejected_{result.status}")
        else:
            precision_summary = result_payload.get("precision_eigen_summary", {}) if result_payload else {}
            covariance_summary = result_payload.get("covariance_eigen_summary", {}) if result_payload else {}
            diagnostics = result_payload.get("diagnostics", {}) if result_payload else {}
            if not bool(precision_summary.get("finite", False)):
                vetoes.append("precision_eigenvalues_nonfinite")
            if not bool(precision_summary.get("positive", False)):
                vetoes.append("precision_not_spd")
            if not bool(covariance_summary.get("finite", False)):
                vetoes.append("covariance_eigenvalues_nonfinite")
            if not bool(covariance_summary.get("positive", False)):
                vetoes.append("covariance_not_spd")
            if diagnostics.get("mass_precision_coordinate_system") != "theta":
                vetoes.append("mass_precision_not_theta_coordinate")
            if diagnostics.get("mass_covariance_coordinate_system") != "theta":
                vetoes.append("mass_covariance_not_theta_coordinate")
            if result_payload.get("reports_hmc_runtime_readiness") is True:
                vetoes.append("unsupported_hmc_runtime_readiness_claim")

    initializer_passed = bool(result is not None and result.accepted and not vetoes)
    decision.update(
        {
            "initializer_artifact_passed": initializer_passed,
            "vetoes": tuple(dict.fromkeys(vetoes)),
            "errors": tuple(errors),
            "next_justified_action": (
                "draft Phase 2 HMC geometry-initialization-only subplan"
                if initializer_passed
                else "repair initializer artifact before HMC geometry initialization"
            ),
        }
    )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_minimal_ssl_lstm_quadratic_initializer_artifact",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "result_path": RESULT_PATH,
        "classification": "extension_or_invention",
        "target_scope": adapter.target_scope,
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "target": {
            "adapter_signature": adapter.adapter_signature(),
            "parameter_dim": int(adapter.parameter_dim),
            "prior_scale": float(adapter.prior_scale),
            "fixture": minimal_ssl_lstm_fixture_payload(),
            "initial_value_finite": initial_value_finite,
            "initial_score_finite": initial_score_finite,
            "initial_score_norm": (
                float(np.linalg.norm(initial_score.numpy()))
                if initial_score_finite
                else None
            ),
        },
        "initializer": result_payload,
        "decision": decision,
        "inference_status": {
            "hard_veto_screen": "passed" if not decision["vetoes"] else "failed",
            "statistically_supported_ranking": "none; single diagnostic target",
            "descriptive_only_differences": (
                "condition numbers, residuals, and locator diagnostics are explanatory only"
            ),
            "default_readiness": "not assessed",
            "next_evidence_needed": (
                "Phase 2 geometry initialization only, then a separate bounded mechanics smoke"
            ),
        },
        "run_manifest": {
            "git_commit": git_payload()["commit"],
            "command": " ".join(str(item) for item in command_tuple),
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
            "cpu_gpu_status": "CPU-hidden debug/reference exception",
            "data_version": "minimal_ssl_lstm_zhaocui_fixed_horizon2_v1",
            "random_seeds": cfg.seed,
            "started_at_utc": started_wall.isoformat(),
            "wall_time_seconds": float(time.perf_counter() - started_perf),
            "output_artifacts": (
                str(DEFAULT_JSON_PATH.relative_to(ROOT)),
                str(DEFAULT_MARKDOWN_PATH.relative_to(ROOT)),
            ),
            "plan_file": PLAN_PATH,
            "result_file": RESULT_PATH,
        },
        "nonclaims": (
            NONCLAIMS
            + tuple(QUADRATIC_MAP_COVARIANCE_NONCLAIMS)
            + tuple(MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS)
        ),
        "hmc_geometry_invoked": False,
        "hmc_runtime_invoked": False,
    }
    return json_ready(payload)


def environment_payload() -> Mapping[str, Any]:
    return {
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>"),
        "cpu_hidden": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
        "tf_version": tf.__version__,
        "tf_physical_gpus": [device.name for device in tf.config.list_physical_devices("GPU")],
        "trust_basis": "cpu_hidden_debug_reference_exception",
    }


def git_payload() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:  # noqa: BLE001 - provenance best effort.
        commit = "unavailable"
    return {"commit": commit}


def write_artifacts(
    payload: Mapping[str, Any],
    *,
    json_path: Path = DEFAULT_JSON_PATH,
    markdown_path: Path = DEFAULT_MARKDOWN_PATH,
) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, indent=2, sort_keys=True)
        handle.write("\n")
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")


def render_markdown(payload: Mapping[str, Any]) -> str:
    decision = payload["decision"]
    initializer = payload.get("initializer") or {}
    diagnostics = initializer.get("diagnostics", {})
    precision = initializer.get("precision_eigen_summary", {})
    covariance = initializer.get("covariance_eigen_summary", {})
    lines = [
        "# Minimal SSL-LSTM Quadratic Initializer Artifact - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- initializer_artifact_passed: `{decision['initializer_artifact_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Coordinate Status",
        "",
        f"- geometry precision coordinates: `{diagnostics.get('geometry_precision_coordinate_system')}`",
        f"- mass precision coordinates: `{diagnostics.get('mass_precision_coordinate_system')}`",
        f"- mass covariance coordinates: `{diagnostics.get('mass_covariance_coordinate_system')}`",
        f"- transform: `{diagnostics.get('precision_transform')}`",
        "",
        "## Eigen Summaries",
        "",
        f"- precision positive: `{precision.get('positive')}`",
        f"- precision condition number: `{precision.get('condition_number')}`",
        f"- covariance positive: `{covariance.get('positive')}`",
        f"- covariance condition number: `{covariance.get('condition_number')}`",
        "",
        "## Boundary",
        "",
        f"- HMC geometry invoked: `{payload['hmc_geometry_invoked']}`",
        f"- HMC runtime invoked: `{payload['hmc_runtime_invoked']}`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["nonclaims"])
    lines.append("")
    return "\n".join(lines)


def json_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return json_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    parser.add_argument("--sample-count", type=int, default=default_settings().low_rank_sample_count)
    parser.add_argument("--trust-radius", type=float, default=default_settings().low_rank_trust_radius)
    parser.add_argument("--pilot-radius", type=float, default=default_settings().low_rank_pilot_radius)
    parser.add_argument("--enable-locator", action="store_true")
    parser.add_argument(
        "--pilot-direction-count",
        type=int,
        default=default_settings().low_rank_pilot_direction_count,
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    settings = MinimalQuadraticInitializerSettings(
        low_rank_sample_count=int(args.sample_count),
        low_rank_trust_radius=float(args.trust_radius),
        low_rank_pilot_radius=float(args.pilot_radius),
        low_rank_pilot_direction_count=int(args.pilot_direction_count),
        locator_enabled=bool(args.enable_locator),
    )
    payload = run_initializer_artifact(
        settings,
        command=(
            "CUDA_VISIBLE_DEVICES=-1",
            "python",
            f"docs/benchmarks/{SCRIPT_NAME}",
        ),
    )
    write_artifacts(
        payload,
        json_path=Path(args.json_path),
        markdown_path=Path(args.markdown_path),
    )
    print(json.dumps(payload["decision"], sort_keys=True))
    return 0 if payload["decision"]["initializer_artifact_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
