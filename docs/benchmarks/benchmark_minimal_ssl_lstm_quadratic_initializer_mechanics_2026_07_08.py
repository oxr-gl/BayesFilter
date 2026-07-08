"""Minimal SSL-LSTM quadratic initializer bounded HMC mechanics smoke.

This diagnostic consumes the Phase 2 geometry artifact and runs the smallest
fixed-kernel HMC mechanics smoke.  It checks finite samples, target values, and
log-acceptance diagnostics only.  It does not tune, adapt, establish
convergence, or establish HMC readiness.
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
    FullChainHMCConfig,
    HMCTuningPolicy,
    run_full_chain_tfp_hmc,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS,
    MinimalZhaoCuiHMCTargetAdapter,
)


SCRIPT_NAME = "benchmark_minimal_ssl_lstm_quadratic_initializer_mechanics_2026_07_08.py"
SCHEMA_VERSION = "minimal_ssl_lstm.quadratic_initializer_mechanics.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase3-bounded-mechanics-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-quadratic-initializer-to-minimal-hmc-readiness-"
    "phase3-bounded-mechanics-result-2026-07-08.md"
)
DEFAULT_PHASE2_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_quadratic_initializer_mechanics_cpu_hidden_2026-07-08.md"
)
NONCLAIMS = (
    "Phase 3 bounded mechanics smoke only",
    "CPU-hidden debug/reference exception only",
    "fixed-kernel tiny HMC runtime only",
    "not HMC readiness evidence",
    "not HMC tuning success evidence",
    "not posterior correctness evidence",
    "not sampler convergence evidence",
    "not sampler superiority evidence",
    "not default-readiness evidence",
    "not GPU/XLA production-readiness evidence",
    "not source-faithful Zhao-Cui parity evidence",
    "native divergence telemetry unavailable is not zero divergences",
)


@dataclass(frozen=True)
class MinimalMechanicsSmokeSettings:
    """Settings for the Phase 3 bounded mechanics smoke."""

    seed: tuple[int, int] = (20260708, 4301)
    num_results: int = 4
    num_burnin_steps: int = 1
    chain_execution_mode: str = "eager"
    use_xla: bool = False
    trace_policy: str = "standard"
    target_status_trace_policy: str = "none"

    def __post_init__(self) -> None:
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        for name in ("num_results", "num_burnin_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        mode = str(self.chain_execution_mode)
        if mode not in {"eager", "tf_function"}:
            raise ValueError("chain_execution_mode must be eager or tf_function")
        object.__setattr__(self, "chain_execution_mode", mode)
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        object.__setattr__(self, "trace_policy", str(self.trace_policy))
        object.__setattr__(
            self,
            "target_status_trace_policy",
            str(self.target_status_trace_policy),
        )

    def payload(self) -> Mapping[str, Any]:
        return {
            "seed": self.seed,
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "chain_execution_mode": self.chain_execution_mode,
            "use_xla": self.use_xla,
            "trace_policy": self.trace_policy,
            "target_status_trace_policy": self.target_status_trace_policy,
        }


def default_settings() -> MinimalMechanicsSmokeSettings:
    return MinimalMechanicsSmokeSettings()


def run_mechanics_smoke(
    settings: MinimalMechanicsSmokeSettings | None = None,
    *,
    phase2_json_path: Path = DEFAULT_PHASE2_JSON_PATH,
    command: Sequence[str] | None = None,
) -> Mapping[str, Any]:
    cfg = default_settings() if settings is None else settings
    started_wall = datetime.now(UTC)
    started_perf = time.perf_counter()
    command_tuple = tuple(sys.argv if command is None else command)
    vetoes: list[str] = []
    errors: list[str] = []
    phase2_payload: Mapping[str, Any] | None = None
    phase1_payload: Mapping[str, Any] | None = None
    hmc_payload: Mapping[str, Any] | None = None
    trace_summary: Mapping[str, Any] = {}

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        vetoes.append("cpu_hidden_execution_not_confirmed")
    try:
        phase2_payload = json.loads(Path(phase2_json_path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
        vetoes.append("phase2_artifact_unreadable")
        errors.append(f"{type(exc).__name__}: {exc}")

    geometry = {}
    phase2_decision = {}
    if phase2_payload is not None:
        phase2_decision = dict(phase2_payload.get("decision") or {})
        geometry = dict(phase2_payload.get("geometry") or {})
        if phase2_decision.get("geometry_initialization_passed") is not True:
            vetoes.append("phase2_geometry_initialization_not_passed")
        if phase2_decision.get("vetoes"):
            vetoes.append("phase2_geometry_vetoes_present")
        if phase2_payload.get("hmc_runtime_invoked") is True:
            vetoes.append("phase2_hmc_runtime_invoked")
        try:
            phase1_path = ROOT / str(phase2_payload["phase1_artifact_path"])
            phase1_payload = json.loads(phase1_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
            vetoes.append("phase1_artifact_from_phase2_unreadable")
            errors.append(f"{type(exc).__name__}: {exc}")

    run_result = None
    if not vetoes:
        try:
            adapter = MinimalZhaoCuiHMCTargetAdapter(evidence_path=PLAN_PATH)
            initializer = dict((phase1_payload or {}).get("initializer") or {})
            position = np.asarray(
                initializer.get("map_candidate") or initializer["locator_position"],
                dtype=float,
            ).reshape([-1])
            config = FullChainHMCConfig(
                num_results=cfg.num_results,
                num_burnin_steps=cfg.num_burnin_steps,
                step_size=float(geometry["initial_step_size"]),
                num_leapfrog_steps=int(geometry["initial_num_leapfrog_steps"]),
                seed=cfg.seed,
                use_xla=cfg.use_xla,
                trace_policy=cfg.trace_policy,
                target_status_trace_policy=cfg.target_status_trace_policy,
                tuning_policy=HMCTuningPolicy.fixed_kernel_screen(),
                target_scope=adapter.target_scope,
                chain_execution_mode=cfg.chain_execution_mode,
            )
            run_result = run_full_chain_tfp_hmc(adapter, tf.constant(position, dtype=tf.float64), config)
            hmc_payload = {
                "samples_shape": tuple(int(dim) for dim in run_result.samples.shape),
                "diagnostics": tensor_ready(run_result.diagnostics),
                "metadata": tensor_ready(run_result.metadata),
                "config": config.signature_payload(),
            }
            trace_summary = summarize_trace(run_result.trace)
        except Exception as exc:  # noqa: BLE001 - structured diagnostic failure.
            vetoes.append("hmc_mechanics_runtime_exception")
            errors.append(f"{type(exc).__name__}: {exc}")

    if run_result is not None:
        diagnostics = dict(hmc_payload.get("diagnostics") or {})
        if int(diagnostics.get("nonfinite_sample_count", 1)) != 0:
            vetoes.append("nonfinite_samples")
        if int(diagnostics.get("finite_sample_count", 0)) != cfg.num_results:
            vetoes.append("finite_sample_count_mismatch")
        if not np.isfinite(float(diagnostics.get("acceptance_rate", np.nan))):
            vetoes.append("acceptance_rate_nonfinite")
        if int(trace_summary.get("log_accept_ratio_nonfinite_count", 1)) != 0:
            vetoes.append("log_accept_ratio_nonfinite")
        if int(trace_summary.get("target_log_prob_nonfinite_count", 1)) != 0:
            vetoes.append("target_log_prob_nonfinite")
        if trace_summary.get("required_trace_keys_present") is not True:
            vetoes.append("required_trace_keys_missing")
        if hmc_payload["metadata"].get("adaptation_policy") != "fixed_kernel_no_adaptation":
            vetoes.append("unexpected_adaptation_policy")

    mechanics_passed = bool(run_result is not None and not vetoes)
    decision = {
        "mechanics_smoke_passed": mechanics_passed,
        "vetoes": tuple(dict.fromkeys(vetoes)),
        "errors": tuple(errors),
        "next_justified_action": (
            "write closeout and decide whether a separate short-chain plan is warranted"
            if mechanics_passed
            else "repair mechanics smoke before any short-chain validation"
        ),
    }
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_minimal_ssl_lstm_quadratic_initializer_mechanics",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "result_path": RESULT_PATH,
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "phase2_artifact_path": str(Path(phase2_json_path).relative_to(ROOT)),
        "phase2_decision": phase2_decision,
        "phase2_geometry_summary": phase2_geometry_summary(geometry),
        "phase1_initializer_summary": phase1_initializer_summary(
            (phase1_payload or {}).get("initializer") or {}
        ),
        "hmc": hmc_payload,
        "trace_summary": trace_summary,
        "decision": decision,
        "inference_status": {
            "hard_veto_screen": "passed" if not decision["vetoes"] else "failed",
            "statistically_supported_ranking": "none; single tiny mechanics smoke",
            "descriptive_only_differences": (
                "acceptance, runtime, sample movement, and log-acceptance summaries are explanatory only"
            ),
            "default_readiness": "not assessed",
            "next_evidence_needed": (
                "separate short-chain validation plan with uncertainty and native divergence policy"
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
        "hmc_runtime_invoked": run_result is not None,
        "hmc_tuning_invoked": False,
        "nonclaims": NONCLAIMS + tuple(MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS),
    }
    return json_ready(payload)


def summarize_trace(trace: Mapping[str, Any]) -> Mapping[str, Any]:
    required = ("is_accepted", "log_accept_ratio", "target_log_prob")
    summary: dict[str, Any] = {
        "keys": tuple(str(key) for key in trace.keys()),
        "required_trace_keys_present": all(key in trace for key in required),
    }
    if "is_accepted" in trace:
        accepted = np.asarray(trace["is_accepted"].numpy(), dtype=bool)
        summary["acceptance_count"] = int(np.sum(accepted))
        summary["acceptance_rate_from_trace"] = float(np.mean(accepted))
    if "log_accept_ratio" in trace:
        values = np.asarray(trace["log_accept_ratio"].numpy(), dtype=float)
        summary["log_accept_ratio_finite_count"] = int(np.sum(np.isfinite(values)))
        summary["log_accept_ratio_nonfinite_count"] = int(np.sum(~np.isfinite(values)))
        summary["log_accept_ratio_min"] = float(np.nanmin(values))
        summary["log_accept_ratio_max"] = float(np.nanmax(values))
    if "target_log_prob" in trace:
        values = np.asarray(trace["target_log_prob"].numpy(), dtype=float)
        summary["target_log_prob_finite_count"] = int(np.sum(np.isfinite(values)))
        summary["target_log_prob_nonfinite_count"] = int(np.sum(~np.isfinite(values)))
        summary["target_log_prob_min"] = float(np.nanmin(values))
        summary["target_log_prob_max"] = float(np.nanmax(values))
    summary["native_divergence_trace_present"] = "divergence" in trace
    summary["native_divergence_interpretation"] = (
        "not zero divergences; native boolean divergence field was not exposed"
        if "divergence" not in trace
        else "native divergence trace present"
    )
    return summary


def phase2_geometry_summary(geometry: Mapping[str, Any]) -> Mapping[str, Any]:
    hint = dict(geometry.get("hint_report") or {})
    mass = dict(geometry.get("mass_artifact_payload") or {})
    return {
        "selected_hint": hint.get("selected_hint"),
        "fallback_used": hint.get("fallback_used"),
        "initial_step_size": geometry.get("initial_step_size"),
        "initial_num_leapfrog_steps": geometry.get("initial_num_leapfrog_steps"),
        "target_trajectory_length": geometry.get("target_trajectory_length"),
        "position_role": mass.get("position_role"),
        "covariance_source": mass.get("covariance_source"),
    }


def phase1_initializer_summary(initializer: Mapping[str, Any]) -> Mapping[str, Any]:
    return {
        "accepted": initializer.get("accepted"),
        "status": initializer.get("status"),
        "map_candidate_role": initializer.get("map_candidate_role"),
        "covariance_source": initializer.get("covariance_source"),
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


def tensor_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return tensor_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): tensor_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [tensor_ready(item) for item in value]
    if isinstance(value, list):
        return [tensor_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    return value


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
    hmc = payload.get("hmc") or {}
    diagnostics = hmc.get("diagnostics") or {}
    trace = payload.get("trace_summary") or {}
    phase2 = payload.get("phase2_geometry_summary") or {}
    lines = [
        "# Minimal SSL-LSTM Quadratic Initializer Mechanics - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- mechanics_smoke_passed: `{decision['mechanics_smoke_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Fixed Geometry",
        "",
        f"- step size: `{phase2.get('initial_step_size')}`",
        f"- leapfrog steps: `{phase2.get('initial_num_leapfrog_steps')}`",
        f"- covariance source: `{phase2.get('covariance_source')}`",
        "",
        "## Mechanics Diagnostics",
        "",
        f"- samples shape: `{hmc.get('samples_shape')}`",
        f"- finite sample count: `{diagnostics.get('finite_sample_count')}`",
        f"- nonfinite sample count: `{diagnostics.get('nonfinite_sample_count')}`",
        f"- acceptance rate: `{diagnostics.get('acceptance_rate')}`",
        f"- log accept nonfinite count: `{trace.get('log_accept_ratio_nonfinite_count')}`",
        f"- target log prob nonfinite count: `{trace.get('target_log_prob_nonfinite_count')}`",
        f"- native divergence trace present: `{trace.get('native_divergence_trace_present')}`",
        "",
        "## Boundary",
        "",
        f"- HMC runtime invoked: `{payload['hmc_runtime_invoked']}`",
        f"- HMC tuning invoked: `{payload['hmc_tuning_invoked']}`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["nonclaims"])
    lines.append("")
    return "\n".join(lines)


def json_ready(value: Any) -> Any:
    return tensor_ready(value)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase2-json-path", type=Path, default=DEFAULT_PHASE2_JSON_PATH)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run_mechanics_smoke(
        default_settings(),
        phase2_json_path=Path(args.phase2_json_path),
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
    return 0 if payload["decision"]["mechanics_smoke_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
