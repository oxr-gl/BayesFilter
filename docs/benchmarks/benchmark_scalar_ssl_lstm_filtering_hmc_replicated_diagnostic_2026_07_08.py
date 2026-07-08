"""Scalar SSL-LSTM filtering replicated HMC diagnostic.

This benchmark runs a tiny fixed-kernel HMC diagnostic across a small fixed set
of seeds. It checks finite telemetry only and records descriptive summaries. It
does not claim posterior correctness, convergence, tuning, ranking, or default
readiness.
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

import numpy as np

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

import tensorflow as tf


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SCRIPT_NAME = "benchmark_scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_2026_07_08.py"
SCHEMA_VERSION = "scalar_ssl_lstm.filtering_hmc_replicated_diagnostic.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md"
)
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase5-replicated-scalar-hmc-result-2026-07-08.md"
)
DEFAULT_GEOMETRY_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_MASS_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json"
)
DEFAULT_PHASE4_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_short_smoke_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_replicated_diagnostic_cpu_hidden_2026-07-08.md"
)
PHASE4_MODULE_PATH = (
    ROOT / "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_short_smoke_2026_07_08.py"
)
NONCLAIMS = (
    "replicated finite-telemetry diagnostic only",
    "not HMC readiness evidence",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not a tuned kernel claim",
    "not a zero-divergence claim",
    "not sampler superiority evidence",
    "not statistically supported ranking evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not Zhao-Cui source-faithfulness evidence",
)


@dataclass(frozen=True)
class ReplicatedDiagnosticSettings:
    """Fixed Phase 5 replicated diagnostic settings."""

    num_leapfrog_steps: int = 4
    step_size: float = 0.3925
    num_results: int = 16
    num_burnin_steps: int = 4
    seeds: tuple[tuple[int, int], ...] = (
        (20260708, 5501),
        (20260708, 5502),
        (20260708, 5503),
    )

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
        seeds = tuple(tuple(int(item) for item in seed) for seed in self.seeds)
        if not seeds or any(len(seed) != 2 for seed in seeds):
            raise ValueError("seeds must be non-empty pairs")
        object.__setattr__(self, "seeds", seeds)

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
            "seeds": self.seeds,
            "chain_execution_mode": "eager",
            "use_xla": False,
            "adaptation_policy": "fixed_kernel_no_adaptation",
        }


def load_phase4_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_hmc_short_smoke_phase5_reuse",
        PHASE4_MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Phase 4 short-smoke module")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_phase4_artifact(
    phase4_payload: Mapping[str, Any],
    settings: ReplicatedDiagnosticSettings | None = None,
) -> Mapping[str, Any]:
    cfg = ReplicatedDiagnosticSettings() if settings is None else settings
    vetoes: list[str] = []
    if phase4_payload.get("schema_version") != "scalar_ssl_lstm.filtering_hmc_short_smoke.v1":
        vetoes.append("phase4_schema_mismatch")
    decision = phase4_payload.get("decision", {})
    if decision.get("short_smoke_passed") is not True:
        vetoes.append("phase4_short_smoke_not_passed")
    if decision.get("vetoes"):
        vetoes.append("phase4_vetoes_present")
    settings_payload = phase4_payload.get("settings", {})
    if int(settings_payload.get("num_leapfrog_steps", -1)) != cfg.num_leapfrog_steps:
        vetoes.append("phase4_leapfrog_mismatch")
    if abs(float(settings_payload.get("step_size", float("nan"))) - cfg.step_size) > 1.0e-12:
        vetoes.append("phase4_step_size_mismatch")
    if phase4_payload.get("phase3_gate", {}).get("phase3_precondition_passed") is not True:
        vetoes.append("phase4_phase3_gate_not_passed")
    coordinate = phase4_payload.get("phase3_gate", {}).get("coordinate_contract", {})
    if coordinate.get("tfp_hmc_coordinate_u") != "z = u @ chol(M_z).T":
        vetoes.append("phase4_u_to_z_contract_missing")
    if coordinate.get("base_adapter_coordinate") != "free parameter values":
        vetoes.append("phase4_base_adapter_coordinate_missing")
    return {
        "phase4_precondition_passed": not vetoes,
        "vetoes": tuple(dict.fromkeys(vetoes)),
        "coordinate_contract": {
            "tfp_hmc_coordinate_u": coordinate.get("tfp_hmc_coordinate_u"),
            "base_adapter_coordinate": coordinate.get("base_adapter_coordinate"),
            "free_parameters_from_u": coordinate.get("free_parameters_from_u"),
        },
    }


def run_replicated_diagnostic(
    geometry_payload: Mapping[str, Any],
    mass_payload: Mapping[str, Any],
    phase4_payload: Mapping[str, Any],
    settings: ReplicatedDiagnosticSettings | None = None,
) -> Mapping[str, Any]:
    cfg = ReplicatedDiagnosticSettings() if settings is None else settings
    start = time.perf_counter()
    phase4 = load_phase4_module()
    phase4_audit = validate_phase4_artifact(phase4_payload, cfg)
    vetoes = list(phase4_audit.get("vetoes", ()))
    adapter = None
    precondition: Mapping[str, Any] = {}
    if not vetoes:
        phase3 = phase4.load_phase3_module()
        adapter, precondition = phase3.build_phase3_adapter(geometry_payload, mass_payload)
        vetoes.extend(precondition.get("vetoes", ()))
        if adapter is None:
            vetoes.append("phase5_adapter_precondition_failed")

    seed_rows = []
    if adapter is not None:
        for seed_index, seed in enumerate(cfg.seeds):
            smoke_settings = phase4.ShortSmokeSettings(
                num_leapfrog_steps=cfg.num_leapfrog_steps,
                step_size=cfg.step_size,
                num_results=cfg.num_results,
                num_burnin_steps=cfg.num_burnin_steps,
                seed=seed,
            )
            row = phase4.run_smoke_kernel(adapter, settings=smoke_settings)
            row = dict(row)
            row["seed_index"] = seed_index
            row["seed"] = seed
            seed_rows.append(row)
            for hard_veto in row.get("hard_vetoes", ()):
                vetoes.append(f"seed_{seed_index}_{hard_veto}")
            if row.get("status") != "passed_short_smoke":
                vetoes.append(f"seed_{seed_index}_short_smoke_failed")
    else:
        vetoes.append("replicated_diagnostic_not_run")

    if len(seed_rows) != len(cfg.seeds):
        vetoes.append("seed_row_count_mismatch")
    if any(row.get("status") != "passed_short_smoke" for row in seed_rows):
        vetoes.append("at_least_one_seed_failed")
    unique_vetoes = tuple(dict.fromkeys(vetoes))
    passed = bool(not unique_vetoes and seed_rows)
    aggregate = aggregate_seed_rows(seed_rows)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_scalar_filtering_hmc_replicated_diagnostic",
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
            "phase4_json": str(DEFAULT_PHASE4_PATH.relative_to(ROOT)),
        },
        "phase4_gate": phase4_audit,
        "precondition": precondition,
        "seed_rows": seed_rows,
        "aggregate_summary": aggregate,
        "decision": {
            "replicated_diagnostic_passed": passed,
            "vetoes": unique_vetoes,
            "passed_seed_count": sum(1 for row in seed_rows if row.get("status") == "passed_short_smoke"),
            "seed_count": len(seed_rows),
            "viable_for_phase6_closeout": passed,
            "next_justified_action": (
                "draft and review Phase 6 closeout subplan"
                if passed
                else "write Phase 5 blocker/repair result before closeout"
            ),
        },
        "metric_roles": {
            "replicated_diagnostic_passed": "primary_phase5_pass_fail",
            "hard_vetoes": "hard_veto_evidence",
            "finite_retained_samples": "hard_veto_evidence",
            "finite_target_log_prob": "hard_veto_evidence",
            "finite_log_accept_ratio": "hard_veto_evidence",
            "native_divergence": "hard_veto_if_available_positive",
            "acceptance_rate": "descriptive_only",
            "target_log_prob_range": "descriptive_only",
            "sample_range": "descriptive_only",
            "between_seed_variation": "descriptive_only",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if passed else "failed",
            "statistically_supported_ranking": "none; no method comparison and no uncertainty interval",
            "descriptive_only_differences": (
                "per-seed acceptance, target-log-prob range, log-accept range, sample range, and runtime"
            ),
            "default_readiness": "not assessed",
            "hmc_readiness": "not assessed; replicated finite-telemetry diagnostic only",
            "next_evidence_needed": (
                "Phase 6 closeout may summarize boundaries; longer validation requires new reviewed plan"
            ),
        },
        "decision_table": {
            "decision": "replicated finite-telemetry diagnostic",
            "primary_criterion_status": "passed" if passed else "failed",
            "veto_diagnostic_status": "no hard vetoes" if passed else f"vetoes: {unique_vetoes}",
            "main_uncertainty": (
                "three seeds with sixteen retained samples each do not establish convergence, "
                "posterior correctness, tuning quality, or default readiness"
            ),
            "next_justified_action": (
                "draft Phase 6 closeout" if passed else "repair or stop before closeout"
            ),
            "what_is_not_being_concluded": (
                "No posterior correctness, HMC convergence, zero divergences, tuned kernel, "
                "sampler superiority, statistical ranking, default readiness, GPU/XLA readiness, "
                "or Zhao-Cui source-faithfulness."
            ),
        },
        "nonclaims": NONCLAIMS,
    }
    return json_ready(payload)


def aggregate_seed_rows(seed_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    acceptance = []
    max_abs_u = []
    target_min = []
    target_max = []
    log_accept_max_abs = []
    finite_sample_counts = []
    nonfinite_sample_counts = []
    native_divergence_statuses = []
    for row in seed_rows:
        trace = row.get("trace_summary", {})
        samples = row.get("samples_summary", {})
        if trace.get("acceptance_rate") is not None:
            acceptance.append(float(trace["acceptance_rate"]))
        if samples.get("max_abs_u") is not None:
            max_abs_u.append(float(samples["max_abs_u"]))
        target = trace.get("target_log_prob", {})
        if isinstance(target, Mapping):
            if target.get("min") is not None:
                target_min.append(float(target["min"]))
            if target.get("max") is not None:
                target_max.append(float(target["max"]))
        log_accept = trace.get("log_accept_ratio", {})
        if isinstance(log_accept, Mapping) and log_accept.get("max_abs_finite") is not None:
            log_accept_max_abs.append(float(log_accept["max_abs_finite"]))
        finite_sample_counts.append(int(samples.get("finite_sample_count", 0)))
        nonfinite_sample_counts.append(int(samples.get("nonfinite_sample_count", 0)))
        native = trace.get("native_divergence", {})
        if isinstance(native, Mapping):
            native_divergence_statuses.append(native.get("status", "available" if native.get("available") else "unknown"))
    return {
        "seed_count": len(seed_rows),
        "passed_seed_count": sum(1 for row in seed_rows if row.get("status") == "passed_short_smoke"),
        "acceptance_rates": acceptance,
        "acceptance_min": min(acceptance) if acceptance else None,
        "acceptance_max": max(acceptance) if acceptance else None,
        "max_abs_u_by_seed": max_abs_u,
        "max_abs_u_overall": max(max_abs_u) if max_abs_u else None,
        "target_log_prob_min_overall": min(target_min) if target_min else None,
        "target_log_prob_max_overall": max(target_max) if target_max else None,
        "log_accept_max_abs_by_seed": log_accept_max_abs,
        "log_accept_max_abs_overall": max(log_accept_max_abs) if log_accept_max_abs else None,
        "finite_sample_counts": finite_sample_counts,
        "nonfinite_sample_counts": nonfinite_sample_counts,
        "native_divergence_statuses": native_divergence_statuses,
        "statistical_interpretation": (
            "descriptive only; no ranking, convergence, posterior correctness, or default-readiness claim"
        ),
    }


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
    aggregate = payload.get("aggregate_summary", {})
    lines = [
        "# Scalar SSL-LSTM Filtering Replicated HMC Diagnostic - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- replicated_diagnostic_passed: `{decision['replicated_diagnostic_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- passed_seed_count: `{decision['passed_seed_count']}` / `{decision['seed_count']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Aggregate Summary",
        "",
        f"- acceptance rates: `{aggregate.get('acceptance_rates')}`",
        f"- max abs u by seed: `{aggregate.get('max_abs_u_by_seed')}`",
        f"- target log-prob overall range: `{aggregate.get('target_log_prob_min_overall')}` to `{aggregate.get('target_log_prob_max_overall')}`",
        f"- log-accept max abs by seed: `{aggregate.get('log_accept_max_abs_by_seed')}`",
        f"- native divergence statuses: `{aggregate.get('native_divergence_statuses')}`",
        f"- interpretation: {aggregate.get('statistical_interpretation')}",
        "",
        "## Seed Rows",
        "",
        "| seed index | seed | status | vetoes | acceptance | finite samples | max abs u |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload.get("seed_rows", ()):
        trace = row.get("trace_summary", {})
        samples = row.get("samples_summary", {})
        lines.append(
            f"| {row.get('seed_index')} | {row.get('seed')} | {row.get('status')} | "
            f"{', '.join(row.get('hard_vetoes', ())) or 'none'} | "
            f"{trace.get('acceptance_rate')} | {samples.get('finite_sample_count')} | "
            f"{samples.get('max_abs_u')} |"
        )
    lines.extend(
        [
            "",
            "## Inference Status",
            "",
            "| field | value |",
            "| --- | --- |",
        ]
    )
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
    parser.add_argument("--phase4-json", type=Path, default=DEFAULT_PHASE4_PATH)
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    geometry_payload = load_json(args.geometry_json)
    mass_payload = load_json(args.mass_json)
    phase4_payload = load_json(args.phase4_json)
    payload = run_replicated_diagnostic(geometry_payload, mass_payload, phase4_payload)
    payload["source_artifacts"] = {
        "geometry_json": str(args.geometry_json),
        "mass_json": str(args.mass_json),
        "phase4_json": str(args.phase4_json),
    }
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
