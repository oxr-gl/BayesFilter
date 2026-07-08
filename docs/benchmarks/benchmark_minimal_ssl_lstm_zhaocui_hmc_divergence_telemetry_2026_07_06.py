"""Inspect native divergence telemetry for the minimal SSL-LSTM HMC target.

This Phase 4 harness answers only whether TensorFlow Probability HMC kernel
results expose a native boolean divergence field that BayesFilter's extractor
can consume.  Acceptance, log-acceptance, target log-probability, R-hat, ESS,
and energy-like values are recorded only as non-divergence health context.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bayesfilter.inference import FullChainHMCConfig, run_full_chain_tfp_hmc  # noqa: E402
import bayesfilter.inference.hmc as hmc_module  # noqa: E402
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MinimalZhaoCuiHMCTargetAdapter,
    initial_minimal_ssl_lstm_hmc_state,
    minimal_ssl_lstm_config,
    minimal_ssl_lstm_fixture_payload,
)


SCRIPT_NAME = "benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py"
PHASE = "PHASE4"
SCHEMA_VERSION = "minimal_ssl_lstm_zhaocui_hmc_validity.phase4_divergence_telemetry.v1"
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-"
    "phase4-divergence-telemetry-subplan-2026-07-06.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-"
    "phase4-divergence-telemetry-result-2026-07-06.md"
)
PHASE3_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase4_divergence_telemetry_cpu_hidden_2026-07-06.md"
)

NATIVE_DIVERGENCE_FIELD_NAMES = (
    "is_divergent",
    "has_divergence",
    "divergence",
    "divergences",
)
EXTRACTOR_REACHABLE_OBJECTS = ("kernel_results", "proposed_results", "accepted_results")
NONCLAIMS = (
    "native divergence telemetry inspection only",
    "missing native divergence telemetry is not zero divergences",
    "acceptance/log-accept/target-log-prob diagnostics are not native divergence telemetry",
    "no HMC convergence claim",
    "no posterior correctness claim",
    "no sampler ranking or superiority claim",
    "no source-faithful Zhao-Cui parity claim",
    "no default-readiness claim",
    "no production-readiness claim",
    "no public API or package readiness claim",
    "no LEDH evidence",
)


@dataclass(frozen=True)
class TelemetryInspectionSettings:
    chain_count: int = 2
    num_results: int = 4
    num_burnin_steps: int = 1
    step_size: float = 1.0e-5
    num_leapfrog_steps: int = 1
    seed: tuple[int, int] = (20260706, 6401)
    use_xla: bool = False
    trace_policy: str = "standard"
    adaptation_policy: str = "fixed_kernel_no_adaptation"
    chain_execution_mode: str = "tf_function"
    initial_offset_scale: float = 1.0e-3
    chain_spread: float = 0.015

    def __post_init__(self) -> None:
        for name in ("chain_count", "num_results", "num_burnin_steps", "num_leapfrog_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        step = float(self.step_size)
        if not np.isfinite(step) or step <= 0.0:
            raise ValueError("step_size must be positive and finite")
        object.__setattr__(self, "step_size", step)
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        if str(self.trace_policy) != "standard":
            raise ValueError("Phase 4 divergence telemetry inspection requires standard trace")
        if str(self.adaptation_policy) != "fixed_kernel_no_adaptation":
            raise ValueError("Phase 4 does not inspect adaptive HMC kernels")
        object.__setattr__(self, "trace_policy", str(self.trace_policy))
        object.__setattr__(self, "adaptation_policy", str(self.adaptation_policy))
        object.__setattr__(self, "chain_execution_mode", str(self.chain_execution_mode))
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        spread = float(self.chain_spread)
        if not np.isfinite(spread) or spread < 0.0:
            raise ValueError("chain_spread must be finite and non-negative")
        object.__setattr__(self, "chain_spread", spread)
        offset = float(self.initial_offset_scale)
        if not np.isfinite(offset) or offset < 0.0:
            raise ValueError("initial_offset_scale must be finite and non-negative")
        object.__setattr__(self, "initial_offset_scale", offset)

    def payload(self) -> Mapping[str, Any]:
        return {
            "chain_count": self.chain_count,
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": self.seed,
            "use_xla": self.use_xla,
            "jit_compile": self.use_xla,
            "trace_policy": self.trace_policy,
            "adaptation_policy": self.adaptation_policy,
            "chain_execution_mode": self.chain_execution_mode,
            "initial_offset_scale": self.initial_offset_scale,
            "chain_spread": self.chain_spread,
            "artifact_mode": "cpu_hidden_native_divergence_telemetry_inspection",
        }


def reviewed_phase4_settings() -> TelemetryInspectionSettings:
    return TelemetryInspectionSettings()


def deterministic_chain_initial_state(
    base_state: tf.Tensor,
    *,
    chain_count: int,
    spread: float,
) -> tf.Tensor:
    base = tf.reshape(tf.convert_to_tensor(base_state, dtype=tf.float64), [1, -1])
    dim = int(base.shape[-1])
    offsets = tf.linspace(
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(1.0, dtype=tf.float64),
        int(chain_count),
    )[:, None]
    direction = tf.linspace(
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(1.0, dtype=tf.float64),
        dim,
    )[None, :]
    return base + tf.constant(float(spread), dtype=tf.float64) * offsets * direction


def load_phase3_baseline(path: Path = PHASE3_JSON_PATH) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    continuation_vetoes = tuple(str(item) for item in payload.get("continuation_vetoes", ()))
    promotion_vetoes = tuple(str(item) for item in payload.get("promotion_vetoes", ()))
    return {
        "path": str(path.relative_to(ROOT)),
        "schema_version": payload.get("schema_version"),
        "status": payload.get("status"),
        "continuation_vetoes": continuation_vetoes,
        "promotion_screen_status": payload.get("promotion_screen_status"),
        "promotion_vetoes": promotion_vetoes,
        "native_divergence_status": payload.get("diagnostics", {}).get(
            "native_divergence_status"
        ),
        "native_divergence_veto_present": (
            "native_divergence_telemetry_not_exposed" in promotion_vetoes
        ),
        "phase3_preconditions_met": (
            payload.get("status") == "passed"
            and continuation_vetoes == tuple()
            and "native_divergence_telemetry_not_exposed" in promotion_vetoes
        ),
    }


def inspect_tfp_kernel_result_tree(
    adapter: MinimalZhaoCuiHMCTargetAdapter,
    initial_state: tf.Tensor,
    settings: TelemetryInspectionSettings,
) -> Mapping[str, Any]:
    target_log_prob_fn = hmc_module._make_tfp_target_log_prob_fn(  # noqa: SLF001
        adapter,
        dtype=tf.float64,
    )
    kernel = tfp.mcmc.HamiltonianMonteCarlo(
        target_log_prob_fn=target_log_prob_fn,
        step_size=tf.constant(settings.step_size, dtype=tf.float64),
        num_leapfrog_steps=int(settings.num_leapfrog_steps),
    )
    bootstrap_results = kernel.bootstrap_results(initial_state)
    try:
        _next_state, one_step_results = kernel.one_step(
            initial_state,
            bootstrap_results,
            seed=tf.constant(settings.seed, dtype=tf.int32),
        )
    except TypeError:
        _next_state, one_step_results = kernel.one_step(initial_state, bootstrap_results)

    bootstrap_search = native_boolean_field_search(bootstrap_results)
    one_step_search = native_boolean_field_search(one_step_results)
    bootstrap_extractor = extractor_output(bootstrap_results)
    one_step_extractor = extractor_output(one_step_results)
    return {
        "runtime": "tfp.mcmc.HamiltonianMonteCarlo.bootstrap_results_and_one_step",
        "kernel_class": type(kernel).__name__,
        "kernel_module": type(kernel).__module__,
        "field_names_considered_native_only_if_boolean": NATIVE_DIVERGENCE_FIELD_NAMES,
        "extractor_reachable_objects": EXTRACTOR_REACHABLE_OBJECTS,
        "bootstrap_results": {
            "object_tree": summarize_object_tree(bootstrap_results),
            "native_boolean_field_search": bootstrap_search,
            "extractor_output": bootstrap_extractor,
        },
        "one_step_results": {
            "object_tree": summarize_object_tree(one_step_results),
            "native_boolean_field_search": one_step_search,
            "extractor_output": one_step_extractor,
        },
        "native_divergence_available_by_direct_search": bool(
            bootstrap_search["accepted_native_boolean_fields"]
            or one_step_search["accepted_native_boolean_fields"]
        ),
        "native_divergence_available_by_bayesfilter_extractor": bool(
            bootstrap_extractor["available"] or one_step_extractor["available"]
        ),
        "nonclaims": NONCLAIMS,
    }


def run_bayesfilter_hmc_inspection(
    adapter: MinimalZhaoCuiHMCTargetAdapter,
    initial_state: tf.Tensor,
    settings: TelemetryInspectionSettings,
) -> Mapping[str, Any]:
    config = FullChainHMCConfig(
        num_results=settings.num_results,
        num_burnin_steps=settings.num_burnin_steps,
        step_size=settings.step_size,
        num_leapfrog_steps=settings.num_leapfrog_steps,
        seed=settings.seed,
        use_xla=settings.use_xla,
        trace_policy=settings.trace_policy,
        adaptation_policy=settings.adaptation_policy,
        target_scope=adapter.target_scope,
        chain_execution_mode=settings.chain_execution_mode,
    )
    started = time.perf_counter()
    result = run_full_chain_tfp_hmc(adapter, initial_state, config)
    runtime_s = time.perf_counter() - started
    trace = dict(result.trace)
    diagnostics = dict(result.diagnostics)
    metadata = dict(result.metadata)
    trace_fields = {
        key: tensor_summary(value)
        for key, value in trace.items()
    }
    health = diagnostics.get("hmc_health_diagnostics", {})
    return {
        "runtime": "bayesfilter.inference.run_full_chain_tfp_hmc",
        "runtime_s": float(runtime_s),
        "sample_shape": tensor_shape(result.samples),
        "trace_keys": tuple(sorted(trace)),
        "trace_fields": trace_fields,
        "diagnostics": {
            "native_divergence_status": diagnostics.get("native_divergence_status"),
            "divergence_status": diagnostics.get("divergence_status"),
            "divergence_count": tensor_or_plain_to_json(diagnostics.get("divergence_count")),
            "divergence_source": diagnostics.get("divergence_source"),
            "finite_sample_count": tensor_or_plain_to_json(
                diagnostics.get("finite_sample_count")
            ),
            "nonfinite_sample_count": tensor_or_plain_to_json(
                diagnostics.get("nonfinite_sample_count")
            ),
            "acceptance_rate": tensor_or_plain_to_json(diagnostics.get("acceptance_rate")),
            "hmc_health_diagnostics": tensor_or_plain_to_json(health),
            "nonclaims": diagnostics.get("nonclaims"),
        },
        "metadata": {
            "trace_policy": metadata.get("trace_policy"),
            "trace_unavailability": metadata.get("trace_unavailability"),
            "use_xla": metadata.get("use_xla"),
            "chain_execution_mode": metadata.get("chain_execution_mode"),
            "target_scope": metadata.get("target_scope"),
        },
        "non_divergence_health_context": {
            "diagnostic_role": "hmc_health_diagnostics_not_native_divergence",
            "health_context_keys": tuple(sorted(health)) if isinstance(health, Mapping) else (),
            "not_native_divergence": True,
            "nonclaims": (
                "acceptance/log-accept/target-log-prob are not native divergence telemetry",
                "health context cannot establish zero divergences",
            ),
        },
    }


def build_phase4_divergence_telemetry_artifact(
    *,
    settings: TelemetryInspectionSettings | None = None,
    command: Sequence[str] | None = None,
) -> Mapping[str, Any]:
    settings = reviewed_phase4_settings() if settings is None else settings
    command_tuple = tuple(sys.argv if command is None else command)
    started_wall = datetime.now(UTC)
    started_perf = time.perf_counter()
    hard_vetoes: list[str] = []
    errors: list[str] = []

    phase3 = load_phase3_baseline()
    if not phase3["phase3_preconditions_met"]:
        hard_vetoes.append("phase3_baseline_preconditions_not_met")

    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        hard_vetoes.append("cpu_hidden_execution_not_confirmed")

    adapter = MinimalZhaoCuiHMCTargetAdapter(evidence_path=SUBPLAN_PATH)
    base_state = initial_minimal_ssl_lstm_hmc_state(settings.initial_offset_scale)
    initial_state = deterministic_chain_initial_state(
        base_state,
        chain_count=settings.chain_count,
        spread=settings.chain_spread,
    )
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    if not bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy()):
        hard_vetoes.append("initial_target_value_nonfinite")
    if not bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy()):
        hard_vetoes.append("initial_target_score_nonfinite")

    tfp_tree: Mapping[str, Any] = {}
    bayesfilter_inspection: Mapping[str, Any] = {}
    if not hard_vetoes:
        try:
            tfp_tree = inspect_tfp_kernel_result_tree(adapter, initial_state, settings)
        except Exception as exc:  # noqa: BLE001
            hard_vetoes.append("tfp_kernel_result_tree_inspection_exception")
            errors.append(f"{type(exc).__name__}: {exc}")
        try:
            bayesfilter_inspection = run_bayesfilter_hmc_inspection(
                adapter,
                initial_state,
                settings,
            )
        except Exception as exc:  # noqa: BLE001
            hard_vetoes.append("bayesfilter_hmc_inspection_exception")
            errors.append(f"{type(exc).__name__}: {exc}")

    extractor_available = bool(
        tfp_tree.get("native_divergence_available_by_bayesfilter_extractor", False)
    )
    bayesfilter_status = (
        bayesfilter_inspection.get("diagnostics", {}).get("native_divergence_status")
        if isinstance(bayesfilter_inspection.get("diagnostics"), Mapping)
        else None
    )
    if extractor_available or bayesfilter_status == "available":
        native_status = "native_divergence_available"
    else:
        native_status = "native_divergence_not_exposed_by_kernel"

    if bayesfilter_status not in (None, "available", "not_exposed_by_kernel"):
        hard_vetoes.append("unexpected_bayesfilter_native_divergence_status")

    runtime_s = time.perf_counter() - started_perf
    artifact = {
        "schema_version": SCHEMA_VERSION,
        "phase": PHASE,
        "status": "failed" if hard_vetoes else "passed",
        "native_divergence_telemetry_status": native_status,
        "native_divergence_count": (
            bayesfilter_inspection.get("diagnostics", {}).get("divergence_count")
            if native_status == "native_divergence_available"
            else None
        ),
        "hard_vetoes": tuple(dict.fromkeys(hard_vetoes)),
        "errors": tuple(errors),
        "phase3_baseline": phase3,
        "predeclared_settings": settings.payload(),
        "tfp_kernel_result_inspection": tfp_tree,
        "bayesfilter_hmc_inspection": bayesfilter_inspection,
        "evidence_contract": {
            "question": (
                "Does the current TFP HMC kernel result structure expose a native "
                "boolean divergence field reachable by the BayesFilter extractor "
                "for the minimal HMC target?"
            ),
            "primary_pass_criterion": (
                "Artifact records inspected result-object tree, exact native "
                "boolean field search, extractor output, and status."
            ),
            "veto_diagnostics": (
                "runtime exception",
                "nonfinite target/value",
                "missing field-tree artifact",
                "proxy divergence substitution",
                "zero-divergence claim from missing telemetry",
                "invalid artifact",
            ),
            "explanatory_only": (
                "acceptance",
                "log_accept_ratio",
                "target_log_prob",
                "runtime",
            ),
            "not_concluded": (
                "zero divergences unless native boolean divergence is exposed",
                "HMC convergence",
                "posterior correctness",
                "ranking or superiority",
                "source-faithful parity",
                "default readiness",
                "production readiness",
            ),
        },
        "decision_table": {
            "decision": (
                "native divergence telemetry available"
                if native_status == "native_divergence_available"
                else "native divergence telemetry remains unavailable"
            ),
            "primary_criterion_status": "passed" if not hard_vetoes else "failed",
            "veto_diagnostic_status": (
                "no hard vetoes" if not hard_vetoes else ", ".join(hard_vetoes)
            ),
            "main_uncertainty": (
                "This is a result-structure inspection, not a long HMC diagnostic."
            ),
            "next_justified_action": (
                "Refresh and execute Phase 5 tuning/mass diagnostics; do not "
                "reinterpret missing telemetry as zero divergences."
            ),
            "what_is_not_being_concluded": (
                "No zero-divergence, posterior correctness, convergence, ranking, "
                "default-readiness, or production-readiness claim."
            ),
        },
        "inference_status": {
            "hard_veto_screen": "passed" if not hard_vetoes else "failed",
            "statistically_supported_ranking": "not_applicable",
            "descriptive_only_differences": (
                "acceptance/log-accept/target-log-prob health context only"
            ),
            "default_readiness": "not_checked",
            "next_evidence_needed": (
                "Phase 5 tuning/mass diagnostics with Phase 4 status carried as "
                "available native telemetry or unavailable telemetry."
            ),
        },
        "native_divergence_interpretation": (
            "native divergence not_exposed_by_kernel is telemetry unavailability, "
            "not zero divergences"
            if native_status == "native_divergence_not_exposed_by_kernel"
            else "native boolean divergence field was exposed and counted"
        ),
        "run_manifest": {
            "command": command_tuple,
            "cwd": str(ROOT),
            "script": f"docs/benchmarks/{SCRIPT_NAME}",
            "started_at_utc": started_wall.isoformat(),
            "finished_at_utc": datetime.now(UTC).isoformat(),
            "runtime_s": float(runtime_s),
            "environment": {
                "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "cpu_hidden": os.environ.get("CUDA_VISIBLE_DEVICES") == "-1",
                "tensorflow_version": tf.__version__,
                "tensorflow_probability_version": tfp.__version__,
            },
            "random_seed": settings.seed,
            "output_artifact": str(DEFAULT_JSON_PATH.relative_to(ROOT)),
            "markdown_artifact": str(DEFAULT_MARKDOWN_PATH.relative_to(ROOT)),
            "plan_file": SUBPLAN_PATH,
            "result_file": RESULT_PATH,
        },
        "fixture": minimal_ssl_lstm_fixture_payload(),
        "nonclaims": NONCLAIMS,
    }
    return json_ready(artifact)


def native_boolean_field_search(kernel_results: Any) -> Mapping[str, Any]:
    candidate_records: list[Mapping[str, Any]] = []
    accepted: list[Mapping[str, Any]] = []
    rejected_proxy: list[Mapping[str, Any]] = []

    for path, field_name, value in iter_named_fields(kernel_results, max_depth=3):
        if field_name not in NATIVE_DIVERGENCE_FIELD_NAMES:
            continue
        summary = {
            "path": ".".join(path + (field_name,)),
            "field_name": field_name,
            "summary": tensor_summary(value),
        }
        is_bool = summary["summary"].get("dtype") == "bool"
        record = {
            **summary,
            "accepted_as_native_boolean_divergence": bool(is_bool),
            "rejected_reason": None if is_bool else "not_boolean_native_field",
        }
        candidate_records.append(record)
        if is_bool:
            accepted.append(record)
        else:
            rejected_proxy.append(record)

    return {
        "field_names": NATIVE_DIVERGENCE_FIELD_NAMES,
        "candidate_fields": tuple(candidate_records),
        "accepted_native_boolean_fields": tuple(accepted),
        "rejected_proxy_or_nonboolean_fields": tuple(rejected_proxy),
        "available": bool(accepted),
        "nonclaims": (
            "only boolean fields with native divergence names are accepted",
            "numeric divergence-like fields are rejected as proxies",
        ),
    }


def extractor_output(kernel_results: Any) -> Mapping[str, Any]:
    tensor = hmc_module._extract_native_divergence_tensor(kernel_results)  # noqa: SLF001
    if tensor is None:
        return {
            "available": False,
            "status": "native_divergence_not_exposed_by_kernel",
            "count": None,
            "shape": None,
            "dtype": None,
            "source": None,
            "nonclaim": "missing native divergence telemetry is not zero divergences",
        }
    tensor = tf.convert_to_tensor(tensor, dtype=tf.bool)
    return {
        "available": True,
        "status": "native_divergence_available",
        "count": int(tf.reduce_sum(tf.cast(tensor, tf.int32)).numpy()),
        "shape": tensor_shape(tensor),
        "dtype": tensor.dtype.name,
        "source": "native_boolean_tfp_kernel_result",
    }


def summarize_object_tree(value: Any, *, max_depth: int = 3) -> Mapping[str, Any]:
    return summarize_object_tree_at(value, path=("kernel_results",), max_depth=max_depth)


def summarize_object_tree_at(
    value: Any,
    *,
    path: tuple[str, ...],
    max_depth: int,
) -> Mapping[str, Any]:
    summary: dict[str, Any] = {
        "path": ".".join(path),
        "class_name": type(value).__name__,
        "module": type(value).__module__,
    }
    if is_tensor_like(value):
        summary.update(tensor_summary(value))
        return summary
    fields = public_field_names(value)
    summary["public_fields"] = fields
    summary["tensor_fields"] = tuple(
        {
            "field_name": name,
            "summary": tensor_summary(getattr_or_mapping(value, name)),
        }
        for name in fields
        if is_tensor_like(getattr_or_mapping(value, name))
    )
    summary["candidate_divergence_fields"] = tuple(
        {
            "field_name": name,
            "summary": tensor_summary(getattr_or_mapping(value, name)),
            "accepted_as_native_boolean_divergence": (
                tensor_summary(getattr_or_mapping(value, name)).get("dtype") == "bool"
            ),
        }
        for name in fields
        if name in NATIVE_DIVERGENCE_FIELD_NAMES
    )
    if max_depth > 0:
        children = []
        for name in fields:
            child = getattr_or_mapping(value, name)
            if is_tensor_like(child) or child is None or is_scalar_like(child):
                continue
            child_fields = public_field_names(child)
            if not child_fields:
                continue
            children.append(
                summarize_object_tree_at(
                    child,
                    path=path + (name,),
                    max_depth=max_depth - 1,
                )
            )
        summary["children"] = tuple(children)
    return summary


def iter_named_fields(
    value: Any,
    *,
    path: tuple[str, ...] = ("kernel_results",),
    max_depth: int,
) -> tuple[tuple[tuple[str, ...], str, Any], ...]:
    rows: list[tuple[tuple[str, ...], str, Any]] = []
    if max_depth < 0:
        return tuple(rows)
    for name in public_field_names(value):
        child = getattr_or_mapping(value, name)
        rows.append((path, name, child))
        if child is None or is_tensor_like(child) or is_scalar_like(child):
            continue
        rows.extend(iter_named_fields(child, path=path + (name,), max_depth=max_depth - 1))
    return tuple(rows)


def public_field_names(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, Mapping):
        return tuple(str(key) for key in value.keys())
    fields = getattr(value, "_fields", None)
    if fields is not None:
        return tuple(str(item) for item in fields)
    if isinstance(value, SimpleNamespace):
        return tuple(str(key) for key in vars(value).keys())
    return tuple()


def getattr_or_mapping(value: Any, name: str) -> Any:
    if isinstance(value, Mapping):
        return value[name]
    return getattr(value, name)


def is_tensor_like(value: Any) -> bool:
    if isinstance(value, (Mapping, tuple, list, SimpleNamespace)):
        return False
    try:
        tf.convert_to_tensor(value)
    except Exception:  # noqa: BLE001
        return False
    return not isinstance(value, (str, bytes))


def is_scalar_like(value: Any) -> bool:
    return value is None or isinstance(value, (str, bytes, int, float, bool, np.number))


def tensor_summary(value: Any) -> Mapping[str, Any]:
    try:
        tensor = tf.convert_to_tensor(value)
    except Exception as exc:  # noqa: BLE001
        return {
            "convertible_to_tensor": False,
            "class_name": type(value).__name__,
            "module": type(value).__module__,
            "conversion_error_type": type(exc).__name__,
            "conversion_error_message": str(exc),
        }
    summary: dict[str, Any] = {
        "convertible_to_tensor": True,
        "dtype": tensor.dtype.name,
        "shape": tensor_shape(tensor),
        "rank": tensor.shape.rank,
        "is_boolean": tensor.dtype == tf.bool,
    }
    if tensor.dtype.is_bool:
        summary["true_count"] = int(tf.reduce_sum(tf.cast(tensor, tf.int32)).numpy())
        summary["element_count"] = int(tf.size(tensor).numpy())
    elif tensor.dtype.is_floating or tensor.dtype.is_integer:
        numeric = tf.cast(tensor, tf.float64)
        finite = tf.math.is_finite(numeric)
        finite_count = int(tf.reduce_sum(tf.cast(finite, tf.int32)).numpy())
        summary["finite_count"] = finite_count
        summary["nonfinite_count"] = int(tf.size(numeric).numpy()) - finite_count
    return summary


def tensor_shape(value: Any) -> tuple[int, ...]:
    tensor = tf.convert_to_tensor(value)
    return tuple(int(dim) for dim in tensor.shape)


def tensor_or_plain_to_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): tensor_or_plain_to_json(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return tuple(tensor_or_plain_to_json(item) for item in value)
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    try:
        tensor = tf.convert_to_tensor(value)
    except (TypeError, ValueError):
        return str(value)
    array = tensor.numpy()
    if np.asarray(array).shape == ():
        item = np.asarray(array).item()
        if isinstance(item, (np.bool_, bool)):
            return bool(item)
        if isinstance(item, (np.integer, int)):
            return int(item)
        if isinstance(item, (np.floating, float)):
            return float(item)
    return np.asarray(array).tolist()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if hasattr(value, "numpy"):
        return json_ready(value.numpy())
    return value


def atomic_write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def render_markdown(artifact: Mapping[str, Any]) -> str:
    diagnostics = artifact.get("bayesfilter_hmc_inspection", {}).get("diagnostics", {})
    trace_keys = artifact.get("bayesfilter_hmc_inspection", {}).get("trace_keys", ())
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 4",
        "",
        "## Summary",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Native divergence telemetry status: `{artifact['native_divergence_telemetry_status']}`",
        f"- Divergence count: `{artifact['native_divergence_count']}`",
        f"- Hard vetoes: `{artifact['hard_vetoes']}`",
        f"- Interpretation: `{artifact['native_divergence_interpretation']}`",
        "",
        "## BayesFilter Extractor Output",
        "",
        f"- diagnostics.native_divergence_status: `{diagnostics.get('native_divergence_status')}`",
        f"- diagnostics.divergence_status: `{diagnostics.get('divergence_status')}`",
        f"- diagnostics.divergence_count: `{diagnostics.get('divergence_count')}`",
        f"- diagnostics.divergence_source: `{diagnostics.get('divergence_source')}`",
        f"- trace keys: `{trace_keys}`",
        "",
        "## Decision Table",
        "",
        "| Field | Value |",
        "| --- | --- |",
    ]
    for key, value in artifact["decision_table"].items():
        lines.append(f"| {key} | `{value}` |")
    lines.extend(
        [
            "",
            "## Inference Status",
            "",
            "| Field | Value |",
            "| --- | --- |",
        ]
    )
    for key, value in artifact["inference_status"].items():
        lines.append(f"| {key} | `{value}` |")
    lines.extend(
        [
            "",
            "## Nonclaims",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- Subplan: `{SUBPLAN_PATH}`",
            f"- Result: `{RESULT_PATH}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_PATH)
    args = parser.parse_args(argv)

    artifact = build_phase4_divergence_telemetry_artifact(command=sys.argv)
    atomic_write_json(args.output, artifact)
    atomic_write_text(args.markdown_output, render_markdown(artifact))
    if artifact["status"] != "passed":
        raise RuntimeError(f"Phase 4 divergence telemetry inspection failed: {artifact['hard_vetoes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
