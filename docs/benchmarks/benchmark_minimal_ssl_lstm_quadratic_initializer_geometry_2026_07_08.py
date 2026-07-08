"""Minimal SSL-LSTM quadratic initializer HMC-geometry smoke.

This diagnostic consumes the Phase 1 quadratic initializer artifact and calls
``initialize_hmc_kernel_geometry`` only.  It records formula-derived step size,
leapfrog count, target trajectory, and trajectory diagnostics.  It does not run
HMC, tune a kernel, or establish sampler readiness.
"""

from __future__ import annotations

import argparse
import json
import math
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
    GEOMETRY_INITIALIZATION_NONCLAIMS,
    HMCGeometryInitializationConfig,
    initialize_hmc_kernel_geometry,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS,
    MinimalZhaoCuiHMCTargetAdapter,
)


SCRIPT_NAME = "benchmark_minimal_ssl_lstm_quadratic_initializer_geometry_2026_07_08.py"
SCHEMA_VERSION = "minimal_ssl_lstm.quadratic_initializer_geometry.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase2-geometry-initialization-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase2-geometry-initialization-result-2026-07-08.md"
)
DEFAULT_PHASE1_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_artifact_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.md"
)
NONCLAIMS = (
    "Phase 2 geometry initialization smoke only",
    "CPU-hidden debug/reference exception only",
    "not an HMC runtime result",
    "not HMC tuning success evidence",
    "not HMC readiness evidence",
    "not posterior correctness evidence",
    "not sampler convergence evidence",
    "not sampler superiority evidence",
    "not default-readiness evidence",
    "not GPU/XLA production-readiness evidence",
    "not source-faithful Zhao-Cui parity evidence",
)


@dataclass(frozen=True)
class MinimalGeometrySmokeSettings:
    """Settings for the Phase 2 geometry-only smoke."""

    seed: tuple[int, int] = (20260708, 4201)
    geometry_scaling_c: float = 0.5
    stability_guard: float = 0.8
    covariance_jitter: float = 1.0e-9
    eigenvalue_floor: float = 1.0e-9
    max_condition_number: float | None = None
    max_leapfrog_steps: int = 512
    pi_over_two_reference: float = math.pi / 2.0

    def __post_init__(self) -> None:
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        for name in (
            "geometry_scaling_c",
            "stability_guard",
            "covariance_jitter",
            "eigenvalue_floor",
            "pi_over_two_reference",
        ):
            value = float(getattr(self, name))
            if not np.isfinite(value):
                raise ValueError(f"{name} must be finite")
            if name == "covariance_jitter":
                if value < 0.0:
                    raise ValueError(f"{name} must be non-negative")
            elif value <= 0.0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        if self.max_condition_number is not None:
            condition = float(self.max_condition_number)
            if not np.isfinite(condition) or condition <= 1.0:
                raise ValueError("max_condition_number must be finite and greater than 1")
            object.__setattr__(self, "max_condition_number", condition)
        max_leapfrog_steps = int(self.max_leapfrog_steps)
        if max_leapfrog_steps <= 0:
            raise ValueError("max_leapfrog_steps must be positive")
        object.__setattr__(self, "max_leapfrog_steps", max_leapfrog_steps)

    def payload(self) -> Mapping[str, Any]:
        return {
            "seed": self.seed,
            "geometry_scaling_c": self.geometry_scaling_c,
            "stability_guard": self.stability_guard,
            "covariance_jitter": self.covariance_jitter,
            "eigenvalue_floor": self.eigenvalue_floor,
            "max_condition_number": self.max_condition_number,
            "max_leapfrog_steps": self.max_leapfrog_steps,
            "pi_over_two_reference": self.pi_over_two_reference,
        }


def default_settings() -> MinimalGeometrySmokeSettings:
    return MinimalGeometrySmokeSettings()


def run_geometry_smoke(
    settings: MinimalGeometrySmokeSettings | None = None,
    *,
    phase1_json_path: Path = DEFAULT_PHASE1_JSON_PATH,
    command: Sequence[str] | None = None,
) -> Mapping[str, Any]:
    cfg = default_settings() if settings is None else settings
    started_wall = datetime.now(UTC)
    started_perf = time.perf_counter()
    command_tuple = tuple(sys.argv if command is None else command)
    vetoes: list[str] = []
    errors: list[str] = []
    phase1_payload: Mapping[str, Any] | None = None
    geometry_payload: Mapping[str, Any] | None = None

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        vetoes.append("cpu_hidden_execution_not_confirmed")
    try:
        phase1_payload = json.loads(Path(phase1_json_path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
        vetoes.append("phase1_artifact_unreadable")
        errors.append(f"{type(exc).__name__}: {exc}")

    initializer = {}
    phase1_decision = {}
    if phase1_payload is not None:
        phase1_decision = dict(phase1_payload.get("decision") or {})
        initializer = dict(phase1_payload.get("initializer") or {})
        if phase1_decision.get("initializer_artifact_passed") is not True:
            vetoes.append("phase1_initializer_artifact_not_passed")
        if phase1_decision.get("vetoes"):
            vetoes.append("phase1_initializer_vetoes_present")
        diagnostics = dict(initializer.get("diagnostics") or {})
        if diagnostics.get("mass_precision_coordinate_system") != "theta":
            vetoes.append("phase1_mass_precision_not_theta_coordinate")
        if diagnostics.get("mass_covariance_coordinate_system") != "theta":
            vetoes.append("phase1_mass_covariance_not_theta_coordinate")
        if phase1_payload.get("hmc_runtime_invoked") is True:
            vetoes.append("phase1_hmc_runtime_invoked")

    geometry_result = None
    if not vetoes:
        try:
            adapter = MinimalZhaoCuiHMCTargetAdapter(evidence_path=PLAN_PATH)
            position = np.asarray(
                initializer.get("map_candidate") or initializer["locator_position"],
                dtype=float,
            ).reshape([-1])
            precision = np.asarray(initializer["precision"], dtype=float)
            config = HMCGeometryInitializationConfig(
                geometry_scaling_c=cfg.geometry_scaling_c,
                stability_guard=cfg.stability_guard,
                covariance_jitter=cfg.covariance_jitter,
                eigenvalue_floor=cfg.eigenvalue_floor,
                max_condition_number=cfg.max_condition_number,
                max_leapfrog_steps=cfg.max_leapfrog_steps,
                allow_geometry_fallback=False,
                position_role=str(initializer.get("map_candidate_role", "initializer_position")),
                negative_hessian_source=str(
                    initializer.get(
                        "covariance_source",
                        "phase1_quadratic_initializer_theta_precision",
                    )
                ),
                seed=cfg.seed,
                source="bayesfilter.phase2.quadratic_initializer_geometry_smoke",
            )
            geometry_result = initialize_hmc_kernel_geometry(
                adapter=adapter,
                initial_position=position,
                negative_hessian=precision,
                config=config,
            )
            geometry_payload = geometry_result.payload(include_mass_arrays=False)
        except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
            vetoes.append("geometry_initialization_exception")
            errors.append(f"{type(exc).__name__}: {exc}")

    trajectory_diagnostics: Mapping[str, Any] = {}
    if geometry_result is not None:
        step = float(geometry_result.initial_step_size)
        leapfrogs = int(geometry_result.initial_num_leapfrog_steps)
        product = float(step * leapfrogs)
        pi_over_two = float(cfg.pi_over_two_reference)
        trajectory_diagnostics = {
            "l_times_step_size": product,
            "target_trajectory_length": float(geometry_result.target_trajectory_length),
            "pi_over_two_reference": pi_over_two,
            "l_times_step_size_minus_pi_over_two": product - pi_over_two,
            "target_trajectory_minus_pi_over_two": (
                float(geometry_result.target_trajectory_length) - pi_over_two
            ),
            "diagnostic_role": "explanatory_only",
            "pass_fail_role": "not_a_phase2_promotion_criterion",
        }
        hint = dict(geometry_result.hint_report)
        if hint.get("selected_hint") != "negative_hessian":
            vetoes.append("geometry_hint_not_negative_hessian")
        if bool(hint.get("fallback_used")):
            vetoes.append("geometry_fallback_used")
        if not np.isfinite(step) or step <= 0.0:
            vetoes.append("initial_step_size_not_positive_finite")
        if leapfrogs <= 0:
            vetoes.append("initial_num_leapfrog_steps_not_positive")
        if (
            not np.isfinite(float(geometry_result.target_trajectory_length))
            or float(geometry_result.target_trajectory_length) <= 0.0
        ):
            vetoes.append("target_trajectory_length_not_positive_finite")

    geometry_passed = bool(geometry_result is not None and not vetoes)
    decision = {
        "geometry_initialization_passed": geometry_passed,
        "vetoes": tuple(dict.fromkeys(vetoes)),
        "errors": tuple(errors),
        "next_justified_action": (
            "draft Phase 3 bounded mechanics smoke subplan"
            if geometry_passed
            else "repair geometry initialization before any HMC runtime"
        ),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_minimal_ssl_lstm_quadratic_initializer_geometry",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "result_path": RESULT_PATH,
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "phase1_artifact_path": str(Path(phase1_json_path).relative_to(ROOT)),
        "phase1_decision": phase1_decision,
        "phase1_initializer_summary": phase1_initializer_summary(initializer),
        "geometry": geometry_payload,
        "trajectory_diagnostics": trajectory_diagnostics,
        "decision": decision,
        "inference_status": {
            "hard_veto_screen": "passed" if not decision["vetoes"] else "failed",
            "statistically_supported_ranking": "none; single geometry diagnostic",
            "descriptive_only_differences": (
                "L*step_size, curvature summaries, and formula outputs are explanatory only"
            ),
            "default_readiness": "not assessed",
            "next_evidence_needed": (
                "separate bounded mechanics smoke with predeclared runtime vetoes"
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
        "hmc_geometry_invoked": geometry_result is not None,
        "hmc_runtime_invoked": False,
        "nonclaims": (
            NONCLAIMS
            + tuple(GEOMETRY_INITIALIZATION_NONCLAIMS)
            + tuple(MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS)
        ),
    }
    return json_ready(payload)


def phase1_initializer_summary(initializer: Mapping[str, Any]) -> Mapping[str, Any]:
    diagnostics = dict(initializer.get("diagnostics") or {})
    return {
        "accepted": initializer.get("accepted"),
        "status": initializer.get("status"),
        "map_candidate_role": initializer.get("map_candidate_role"),
        "covariance_source": initializer.get("covariance_source"),
        "geometry_precision_coordinate_system": diagnostics.get(
            "geometry_precision_coordinate_system"
        ),
        "mass_precision_coordinate_system": diagnostics.get(
            "mass_precision_coordinate_system"
        ),
        "mass_covariance_coordinate_system": diagnostics.get(
            "mass_covariance_coordinate_system"
        ),
        "precision_eigen_summary": initializer.get("precision_eigen_summary"),
        "covariance_eigen_summary": initializer.get("covariance_eigen_summary"),
    }


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
    geometry = payload.get("geometry") or {}
    hint = geometry.get("hint_report") or {}
    trajectory = payload.get("trajectory_diagnostics") or {}
    curvature = geometry.get("curvature_report") or {}
    lines = [
        "# Minimal SSL-LSTM Quadratic Initializer Geometry - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- geometry_initialization_passed: `{decision['geometry_initialization_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Geometry",
        "",
        f"- selected hint: `{hint.get('selected_hint')}`",
        f"- fallback used: `{hint.get('fallback_used')}`",
        f"- initial step size: `{geometry.get('initial_step_size')}`",
        f"- initial leapfrog steps: `{geometry.get('initial_num_leapfrog_steps')}`",
        f"- target trajectory length: `{geometry.get('target_trajectory_length')}`",
        f"- L * step size: `{trajectory.get('l_times_step_size')}`",
        f"- L * step size minus pi/2: `{trajectory.get('l_times_step_size_minus_pi_over_two')}`",
        "",
        "## Curvature",
        "",
        f"- omega min/median/max: `{curvature.get('omega_min')}` / `{curvature.get('omega_median')}` / `{curvature.get('omega_max')}`",
        f"- omega rms: `{curvature.get('omega_rms')}`",
        "",
        "## Boundary",
        "",
        f"- HMC geometry invoked: `{payload['hmc_geometry_invoked']}`",
        f"- HMC runtime invoked: `{payload['hmc_runtime_invoked']}`",
        f"- trajectory diagnostic role: `{trajectory.get('diagnostic_role')}`",
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
    parser.add_argument("--phase1-json-path", type=Path, default=DEFAULT_PHASE1_JSON_PATH)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_geometry_smoke(
        default_settings(),
        phase1_json_path=Path(args.phase1_json_path),
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
    return 0 if payload["decision"]["geometry_initialization_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

