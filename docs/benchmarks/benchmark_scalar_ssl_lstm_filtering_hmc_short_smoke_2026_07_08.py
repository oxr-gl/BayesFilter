"""Scalar SSL-LSTM filtering short HMC smoke.

This benchmark extends the Phase 3 mechanics canary to a tiny fixed-kernel HMC
smoke. It checks only finite retained samples and finite target/acceptance
telemetry under the repaired Phase 3 coordinate composition. It does not claim
posterior correctness, convergence, tuning, ranking, or default readiness.
"""

from __future__ import annotations

import argparse
import importlib.util
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
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

import numpy as np
import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.inference import FullChainHMCConfig, run_full_chain_tfp_hmc  # noqa: E402


SCRIPT_NAME = "benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py"
SCHEMA_VERSION = "scalar_ssl_lstm.filtering_hmc_short_smoke.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md"
)
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase4-short-hmc-smoke-result-2026-07-08.md"
)
DEFAULT_GEOMETRY_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_MASS_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json"
)
DEFAULT_PHASE3_PATH = (
    ROOT
    / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.md"
)
PHASE3_MODULE_PATH = (
    ROOT / "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py"
)
NONCLAIMS = (
    "short fixed-kernel HMC smoke only",
    "not HMC readiness evidence",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not a tuned kernel claim",
    "not a zero-divergence claim",
    "not sampler superiority evidence",
    "not statistical ranking evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not Zhao-Cui source-faithfulness evidence",
)


@dataclass(frozen=True)
class ShortSmokeSettings:
    """Fixed Phase 4 short-smoke settings."""

    num_leapfrog_steps: int = 4
    step_size: float = 0.3925
    num_results: int = 8
    num_burnin_steps: int = 2
    seed: tuple[int, int] = (20260708, 4401)

    def __post_init__(self) -> None:
        for name in ("num_leapfrog_steps", "num_results", "num_burnin_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        step = float(self.step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("step_size must be positive finite")
        object.__setattr__(self, "step_size", step)
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)

    @property
    def trajectory_length(self) -> float:
        return float(self.num_leapfrog_steps * self.step_size)

    def payload(self) -> Mapping[str, Any]:
        return {
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "step_size": self.step_size,
            "trajectory_length_L_times_epsilon": self.trajectory_length,
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "seed": self.seed,
            "chain_execution_mode": "eager",
            "use_xla": False,
            "adaptation_policy": "fixed_kernel_no_adaptation",
        }


def load_phase3_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_hmc_mechanics_canary_phase4_reuse",
        PHASE3_MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Phase 3 mechanics canary module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase3_artifact(phase3_payload: Mapping[str, Any]) -> Mapping[str, Any]:
    vetoes: list[str] = []
    if phase3_payload.get("schema_version") != "scalar_ssl_lstm.filtering_hmc_mechanics_canary.v1":
        vetoes.append("phase3_schema_mismatch")
    decision = phase3_payload.get("decision", {})
    if decision.get("mechanics_canary_passed") is not True:
        vetoes.append("phase3_mechanics_canary_not_passed")
    if decision.get("vetoes"):
        vetoes.append("phase3_vetoes_present")
    settings = phase3_payload.get("settings", {})
    grid = settings.get("candidate_grid", ())
    near_157 = [
        row for row in grid
        if int(row.get("num_leapfrog_steps", -1)) == 4
        and abs(float(row.get("step_size", float("nan"))) - 0.3925) <= 1.0e-12
    ]
    if not near_157:
        vetoes.append("phase3_reference_candidate_missing")
    precondition = phase3_payload.get("precondition", {})
    coordinate = precondition.get("coordinate_contract", {})
    if coordinate.get("tfp_hmc_coordinate_u") != "z = u @ chol(M_z).T":
        vetoes.append("phase3_u_to_z_contract_missing")
    if coordinate.get("base_adapter_coordinate") != "free parameter values":
        vetoes.append("phase3_base_adapter_coordinate_missing")
    return {
        "phase3_precondition_passed": not vetoes,
        "vetoes": tuple(dict.fromkeys(vetoes)),
        "phase3_reference_candidate": near_157[:1],
        "coordinate_contract": {
            "tfp_hmc_coordinate_u": coordinate.get("tfp_hmc_coordinate_u"),
            "base_adapter_coordinate": coordinate.get("base_adapter_coordinate"),
            "free_parameters_from_u": coordinate.get("free_parameters_from_u"),
        },
    }


def run_short_smoke(
    geometry_payload: Mapping[str, Any],
    mass_payload: Mapping[str, Any],
    phase3_payload: Mapping[str, Any],
    settings: ShortSmokeSettings | None = None,
) -> Mapping[str, Any]:
    cfg = ShortSmokeSettings() if settings is None else settings
    start = time.perf_counter()
    phase3 = load_phase3_module()
    phase3_audit = validate_phase3_artifact(phase3_payload)
    adapter = None
    precondition: Mapping[str, Any] = {}
    vetoes = list(phase3_audit.get("vetoes", ()))
    if not vetoes:
        adapter, precondition = phase3.build_phase3_adapter(geometry_payload, mass_payload)
        vetoes.extend(precondition.get("vetoes", ()))
        if adapter is None:
            vetoes.append("phase4_adapter_precondition_failed")

    row: Mapping[str, Any] | None = None
    if adapter is not None:
        row = run_smoke_kernel(adapter, settings=cfg)
        for veto in row.get("hard_vetoes", ()):
            vetoes.append(f"short_smoke_{veto}")
    else:
        vetoes.append("short_smoke_not_run")

    unique_vetoes = tuple(dict.fromkeys(vetoes))
    passed = bool(not unique_vetoes and row and row.get("status") == "passed_short_smoke")
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_scalar_filtering_hmc_short_smoke",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "subplan_path": SUBPLAN_PATH,
        "result_path": RESULT_PATH,
        "classification": "extension_or_invention",
        "target_scope": None if adapter is None else adapter.target_scope,
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "source_artifacts": {
            "geometry_json": str(DEFAULT_GEOMETRY_PATH.relative_to(ROOT)),
            "mass_json": str(DEFAULT_MASS_PATH.relative_to(ROOT)),
            "phase3_json": str(DEFAULT_PHASE3_PATH.relative_to(ROOT)),
        },
        "phase3_gate": phase3_audit,
        "precondition": precondition,
        "short_smoke_row": row,
        "decision": {
            "short_smoke_passed": passed,
            "vetoes": unique_vetoes,
            "viable_for_phase5_replicated_scalar_hmc": passed,
            "next_justified_action": (
                "draft and review Phase 5 replicated scalar HMC diagnostic subplan"
                if passed
                else "write Phase 4 blocker/repair result before replicated diagnostics"
            ),
        },
        "metric_roles": {
            "short_smoke_passed": "primary_phase4_pass_fail",
            "hard_vetoes": "hard_veto_evidence",
            "finite_retained_samples": "hard_veto_evidence",
            "finite_target_log_prob": "hard_veto_evidence",
            "finite_log_accept_ratio": "hard_veto_evidence",
            "native_divergence": "hard_veto_if_available_positive",
            "acceptance_rate": "explanatory_short_smoke_only",
            "sample_range": "explanatory_short_smoke_only",
            "runtime": "explanatory_only",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if passed else "failed",
            "statistically_supported_ranking": "none; single short-smoke kernel",
            "descriptive_only_differences": (
                "acceptance, target log-prob range, log-accept range, sample range, and runtime"
            ),
            "default_readiness": "not assessed",
            "hmc_readiness": "not assessed; short smoke only",
            "next_evidence_needed": (
                "reviewed Phase 5 replicated scalar HMC diagnostic only if Phase 4 passes"
            ),
        },
        "run_manifest": {
            "command": (
                "timeout 240 env CUDA_VISIBLE_DEVICES=-1 python "
                "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py"
            ),
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV", "N/A"),
            "cpu_gpu_status": "CPU-hidden debug/reference exception",
            "jit_compile": False,
            "tf32_mode": "disabled_by_cpu_hidden_debug_contract",
            "data_version": "stateless_simulated_scalar_ssl_lstm_filtering_path_v1",
            "random_seeds": cfg.seed,
            "wall_time_seconds": float(time.perf_counter() - start),
            "output_artifacts": (
                str(DEFAULT_JSON_PATH.relative_to(ROOT)),
                str(DEFAULT_MARKDOWN_PATH.relative_to(ROOT)),
            ),
            "plan_file": PLAN_PATH,
            "subplan_file": SUBPLAN_PATH,
            "result_file": RESULT_PATH,
        },
        "nonclaims": NONCLAIMS,
    }
    return json_ready(payload)


def run_smoke_kernel(adapter: Any, *, settings: ShortSmokeSettings) -> Mapping[str, Any]:
    start = time.perf_counter()
    hard_vetoes: list[str] = []
    error_message = None
    result = None
    initial_state = tf.zeros((adapter.parameter_dim,), dtype=tf.float64)
    initial_value = None
    initial_score = None
    try:
        value, score = adapter.log_prob_and_grad(initial_state)
        initial_value = float(tf.convert_to_tensor(value, dtype=tf.float64).numpy())
        initial_score = np.asarray(
            tf.reshape(tf.convert_to_tensor(score, dtype=tf.float64), [-1]).numpy(),
            dtype=float,
        )
        if not np.isfinite(initial_value):
            hard_vetoes.append("initial_target_value_nonfinite")
        if initial_score.shape != (adapter.parameter_dim,):
            hard_vetoes.append("initial_target_score_shape_mismatch")
        elif not np.all(np.isfinite(initial_score)):
            hard_vetoes.append("initial_target_score_nonfinite")
        config = FullChainHMCConfig(
            num_results=settings.num_results,
            num_burnin_steps=settings.num_burnin_steps,
            step_size=settings.step_size,
            num_leapfrog_steps=settings.num_leapfrog_steps,
            seed=settings.seed,
            use_xla=False,
            trace_policy="standard",
            adaptation_policy="fixed_kernel_no_adaptation",
            target_scope=adapter.target_scope,
            chain_execution_mode="eager",
        )
        result = run_full_chain_tfp_hmc(adapter, initial_state, config)
    except Exception as exc:  # noqa: BLE001 - fail-closed artifact path.
        error_message = f"{type(exc).__name__}: {exc}"
        hard_vetoes.append("hmc_runtime_exception")

    diagnostics: Mapping[str, Any] = {}
    metadata: Mapping[str, Any] = {}
    samples_summary: Mapping[str, Any] = {}
    trace_summary: Mapping[str, Any] = {}
    if result is not None:
        diagnostics = dict(result.diagnostics)
        metadata = dict(result.metadata)
        samples_summary = summarize_samples(result.samples)
        trace_summary = summarize_trace(result.trace)
        if int(samples_summary["nonfinite_sample_count"]) > 0:
            hard_vetoes.append("nonfinite_retained_samples")
        log_accept = trace_summary.get("log_accept_ratio", {})
        if isinstance(log_accept, Mapping) and int(log_accept.get("nonfinite_count", 1)) > 0:
            hard_vetoes.append("nonfinite_log_accept_ratio")
        target = trace_summary.get("target_log_prob", {})
        if isinstance(target, Mapping) and target.get("finite") is not True:
            hard_vetoes.append("nonfinite_target_log_prob_trace")
        native = trace_summary.get("native_divergence", {})
        if isinstance(native, Mapping) and native.get("available") and int(native.get("count", 0)) > 0:
            hard_vetoes.append("native_divergence_detected")

    status = "passed_short_smoke" if not hard_vetoes else "failed_short_smoke"
    return json_ready(
        {
            "status": status,
            "hard_vetoes": tuple(dict.fromkeys(hard_vetoes)),
            "num_leapfrog_steps": settings.num_leapfrog_steps,
            "step_size": settings.step_size,
            "trajectory_length_L_times_epsilon": settings.trajectory_length,
            "num_results": settings.num_results,
            "num_burnin_steps": settings.num_burnin_steps,
            "runtime_seconds": float(time.perf_counter() - start),
            "initial": {
                "u": [0.0] * int(adapter.parameter_dim),
                "value": initial_value,
                "score": None if initial_score is None else initial_score,
                "score_norm": None if initial_score is None else float(np.linalg.norm(initial_score)),
            },
            "hmc_error": error_message,
            "diagnostics": diagnostics,
            "metadata": metadata,
            "samples_summary": samples_summary,
            "trace_summary": trace_summary,
            "metric_roles": {
                "status": "primary_phase4_short_smoke_pass_fail",
                "hard_vetoes": "hard_veto_evidence",
                "retained_sample_finiteness": "hard_veto_evidence",
                "target_log_prob_finiteness": "hard_veto_evidence",
                "log_accept_ratio_finiteness": "hard_veto_evidence",
                "acceptance_rate": "explanatory_short_smoke_only",
                "native_divergence": "hard_veto_if_available_positive; unavailable is not zero divergences",
            },
            "nonclaims": (
                "short fixed-kernel HMC smoke only",
                "not HMC convergence evidence",
                "not posterior correctness evidence",
                "not a tuned kernel claim",
            ),
        }
    )


def summarize_samples(samples: Any) -> Mapping[str, Any]:
    array = np.asarray(tf.convert_to_tensor(samples, dtype=tf.float64).numpy(), dtype=float)
    finite = np.all(np.isfinite(array), axis=-1)
    return {
        "shape": array.shape,
        "finite_sample_count": int(np.sum(finite)),
        "nonfinite_sample_count": int(np.sum(~finite)),
        "first_u": array[0],
        "final_u": array[-1],
        "mean_u": np.mean(array, axis=0),
        "std_u": np.std(array, axis=0),
        "max_abs_u": float(np.max(np.abs(array))) if array.size else None,
    }


def summarize_trace(trace: Mapping[str, Any]) -> Mapping[str, Any]:
    summary: dict[str, Any] = {}
    if "is_accepted" in trace:
        accepted = np.asarray(tf.convert_to_tensor(trace["is_accepted"]).numpy(), dtype=bool)
        summary["is_accepted"] = accepted
        summary["acceptance_rate"] = float(np.mean(accepted.astype(float))) if accepted.size else None
        summary["accepted_count"] = int(np.sum(accepted))
        summary["decision_count"] = int(accepted.size)
    if "log_accept_ratio" in trace:
        log_accept = np.asarray(
            tf.convert_to_tensor(trace["log_accept_ratio"], dtype=tf.float64).numpy(),
            dtype=float,
        )
        finite = np.isfinite(log_accept)
        summary["log_accept_ratio"] = {
            "finite_count": int(np.sum(finite)),
            "nonfinite_count": int(np.sum(~finite)),
            "min_finite": float(np.min(log_accept[finite])) if np.any(finite) else None,
            "max_finite": float(np.max(log_accept[finite])) if np.any(finite) else None,
            "max_abs_finite": (
                float(np.max(np.abs(log_accept[finite]))) if np.any(finite) else None
            ),
        }
    if "target_log_prob" in trace:
        target_log_prob = np.asarray(
            tf.convert_to_tensor(trace["target_log_prob"], dtype=tf.float64).numpy(),
            dtype=float,
        )
        finite = np.isfinite(target_log_prob)
        summary["target_log_prob"] = {
            "finite": bool(np.all(finite)),
            "finite_count": int(np.sum(finite)),
            "nonfinite_count": int(np.sum(~finite)),
            "min": float(np.min(target_log_prob)) if target_log_prob.size else None,
            "max": float(np.max(target_log_prob)) if target_log_prob.size else None,
        }
    if "divergence" in trace:
        divergence = np.asarray(tf.convert_to_tensor(trace["divergence"]).numpy(), dtype=bool)
        summary["native_divergence"] = {
            "available": True,
            "count": int(np.sum(divergence)),
        }
    else:
        summary["native_divergence"] = {
            "available": False,
            "status": "not_exposed_by_kernel",
            "nonclaim": "unavailable native divergence telemetry is not zero divergences",
        }
    return json_ready(summary)


def environment_payload() -> Mapping[str, Any]:
    return {
        "python": sys.version.split()[0],
        "tensorflow": tf.__version__,
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tf_physical_devices": [
            {"name": device.name, "device_type": device.device_type}
            for device in tf.config.list_physical_devices()
        ],
        "tf_logical_gpus": [device.name for device in tf.config.list_logical_devices("GPU")],
    }


def git_payload() -> Mapping[str, Any]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            text=True,
        ).strip()
    except Exception:  # noqa: BLE001
        commit = "unknown"
    try:
        status = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=ROOT,
            text=True,
        )
    except Exception:  # noqa: BLE001
        status = ""
    lines = [line for line in status.splitlines() if line.strip()]
    return {
        "commit": commit,
        "dirty": bool(lines),
        "dirty_line_count": len(lines),
        "dirty_preview": lines[:20],
    }


def render_markdown(payload: Mapping[str, Any]) -> str:
    decision = payload["decision"]
    row = payload.get("short_smoke_row") or {}
    trace = row.get("trace_summary", {})
    samples = row.get("samples_summary", {})
    lines = [
        "# Scalar SSL-LSTM Filtering Short HMC Smoke - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- short_smoke_passed: `{decision['short_smoke_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Fixed Kernel",
        "",
        f"- leapfrog steps: `{payload['settings']['num_leapfrog_steps']}`",
        f"- step size: `{payload['settings']['step_size']}`",
        f"- trajectory length: `{payload['settings']['trajectory_length_L_times_epsilon']}`",
        f"- retained samples: `{payload['settings']['num_results']}`",
        f"- burn-in steps: `{payload['settings']['num_burnin_steps']}`",
        "",
        "## Smoke Telemetry",
        "",
        f"- row status: `{row.get('status')}`",
        f"- row vetoes: `{row.get('hard_vetoes')}`",
        f"- acceptance: `{trace.get('acceptance_rate')}`",
        f"- target log prob: `{trace.get('target_log_prob')}`",
        f"- log accept ratio: `{trace.get('log_accept_ratio')}`",
        f"- native divergence: `{trace.get('native_divergence')}`",
        f"- max abs u: `{samples.get('max_abs_u')}`",
        "",
        "## Inference Status",
        "",
        "| field | value |",
        "| --- | --- |",
    ]
    for key, value in payload["inference_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in payload["nonclaims"])
    return "\n".join(lines) + "\n"


def json_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return json_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, Path):
        return str(value)
    return value


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--geometry-json", type=Path, default=DEFAULT_GEOMETRY_PATH)
    parser.add_argument("--mass-json", type=Path, default=DEFAULT_MASS_PATH)
    parser.add_argument("--phase3-json", type=Path, default=DEFAULT_PHASE3_PATH)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    geometry_payload = load_json(args.geometry_json)
    mass_payload = load_json(args.mass_json)
    phase3_payload = load_json(args.phase3_json)
    payload = run_short_smoke(geometry_payload, mass_payload, phase3_payload)
    payload["source_artifacts"] = {
        "geometry_json": str(args.geometry_json),
        "mass_json": str(args.mass_json),
        "phase3_json": str(args.phase3_json),
    }
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
