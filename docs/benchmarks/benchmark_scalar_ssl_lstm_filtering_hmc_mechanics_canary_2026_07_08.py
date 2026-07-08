"""Scalar SSL-LSTM filtering HMC mechanics canary.

This script runs a tiny fixed-grid HMC mechanics canary for the scalar
filtering-likelihood target. It applies the Phase 2 mass handoff explicitly as
an affine preconditioner from an internal unit coordinate ``u`` into the Phase 1
whitened coordinate ``z``. It is not a posterior validation, convergence run,
or tuning claim.
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

from bayesfilter.inference import (  # noqa: E402
    FullChainHMCConfig,
    LatentAffineBatchValueScoreAdapter,
    LatentAffineHMCTransform,
    ValueScoreCapability,
    run_full_chain_tfp_hmc,
    stable_adapter_signature,
)


SCRIPT_NAME = "benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py"
SCHEMA_VERSION = "scalar_ssl_lstm.filtering_hmc_mechanics_canary.v1"
PLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md"
)
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-subplan-2026-07-08.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase3-mechanics-canary-result-2026-07-08.md"
)
DEFAULT_GEOMETRY_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_geometry_cpu_hidden_2026-07-08.json"
)
DEFAULT_MASS_PATH = (
    ROOT / "docs/benchmarks/scalar_ssl_lstm_filtering_mass_handoff_cpu_hidden_2026-07-08.json"
)
DEFAULT_JSON_PATH = (
    ROOT
    / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.json"
)
DEFAULT_MARKDOWN_PATH = (
    ROOT
    / "docs/benchmarks/scalar_ssl_lstm_filtering_hmc_mechanics_canary_cpu_hidden_2026-07-08.md"
)
PHASE1_HARNESS_PATH = (
    ROOT / "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_geometry_2026_07_08.py"
)
EXACT_CANDIDATE_GRID = (
    (1, 0.10),
    (2, 0.25),
    (4, 0.3925),
)
NONCLAIMS = (
    "HMC mechanics canary only",
    "not HMC readiness evidence",
    "not HMC convergence evidence",
    "not posterior correctness evidence",
    "not a tuned step-size claim",
    "not a zero-divergence claim",
    "not sampler superiority evidence",
    "not statistical ranking evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not Zhao-Cui source-faithfulness evidence",
)


@dataclass(frozen=True)
class MechanicsCanarySettings:
    """Fixed Phase 3 mechanics-canary settings."""

    candidate_grid: tuple[tuple[int, float], ...] = EXACT_CANDIDATE_GRID
    num_results: int = 2
    num_burnin_steps: int = 1
    seed: tuple[int, int] = (20260708, 3301)

    def __post_init__(self) -> None:
        grid = []
        for leapfrogs, step_size in self.candidate_grid:
            leapfrogs = int(leapfrogs)
            step_size = float(step_size)
            if leapfrogs <= 0:
                raise ValueError("candidate leapfrog count must be positive")
            if not np.isfinite(step_size) or step_size <= 0.0:
                raise ValueError("candidate step size must be positive finite")
            grid.append((leapfrogs, step_size))
        object.__setattr__(self, "candidate_grid", tuple(grid))
        for name in ("num_results", "num_burnin_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)

    def payload(self) -> Mapping[str, Any]:
        return {
            "candidate_grid": [
                {
                    "num_leapfrog_steps": leapfrogs,
                    "step_size": step_size,
                    "trajectory_length": leapfrogs * step_size,
                }
                for leapfrogs, step_size in self.candidate_grid
            ],
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "seed": self.seed,
            "chain_execution_mode": "eager",
            "use_xla": False,
        }


class ScalarFilteringFreeParameterAdapter:
    """Adapter for the Phase 1 free-parameter filtering target."""

    def __init__(self, target: Any, *, evidence_path: str) -> None:
        self.target = target
        self.parameter_dim = len(target.free_indices)
        self.target_scope = "scalar_ssl_lstm:svd_ukf_filtering_geometry:phase3_mechanics_z"
        self.evidence_path = str(evidence_path)
        self.free_parameter_names = tuple(str(name) for name in target.free_parameter_names)

    def adapter_signature(self) -> str:
        payload = {
            "target_scope": self.target_scope,
            "parameter_dim": self.parameter_dim,
            "free_parameter_names": self.free_parameter_names,
            "horizon": int(self.target.config.horizon),
            "filter_name": self.target.settings.filter_name,
            "evidence_path": self.evidence_path,
        }
        return stable_json_hash(payload)

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=False,
            full_chain_xla_diagnostic_ready=False,
            runtime_backend="docs.benchmarks.scalar_filtering_hmc_mechanics_canary",
            evidence_path=self.evidence_path,
            target_scope=self.target_scope,
            nonclaims=(
                "Phase 3 mechanics canary target only",
                "CPU-hidden non-XLA debug/reference execution",
                "no HMC convergence claim",
                "no posterior correctness claim",
            ),
        )

    def log_prob_and_grad(self, free_values: Any) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(free_values, dtype=tf.float64)
        if values.shape.rank == 1:
            return self.target.value_and_score(values)
        if values.shape.rank == 2:
            result_values = []
            result_scores = []
            for index in range(int(values.shape[0])):
                value, score = self.target.value_and_score(values[index])
                result_values.append(tf.convert_to_tensor(value, dtype=tf.float64))
                result_scores.append(tf.convert_to_tensor(score, dtype=tf.float64))
            return tf.stack(result_values), tf.stack(result_scores)
        raise ValueError("free_values must have rank 1 or rank 2")


def stable_json_hash(payload: Mapping[str, Any]) -> str:
    import hashlib

    return hashlib.sha256(
        json.dumps(json_ready(payload), sort_keys=True).encode("utf-8")
    ).hexdigest()


def load_phase1_harness() -> Any:
    spec = importlib.util.spec_from_file_location(
        "scalar_ssl_lstm_filtering_geometry_phase1",
        PHASE1_HARNESS_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load Phase 1 filtering-geometry harness")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_phase3_adapter(
    geometry_payload: Mapping[str, Any],
    mass_payload: Mapping[str, Any],
) -> tuple[Any, Mapping[str, Any]]:
    vetoes: list[str] = []
    if geometry_payload.get("schema_version") != "scalar_ssl_lstm.filtering_geometry.v1":
        vetoes.append("phase1_schema_mismatch")
    if geometry_payload.get("decision", {}).get("geometry_sanity_passed") is not True:
        vetoes.append("phase1_geometry_not_passed")
    if geometry_payload.get("decision", {}).get("vetoes"):
        vetoes.append("phase1_vetoes_present")
    if mass_payload.get("schema_version") != "scalar_ssl_lstm.filtering_mass_handoff.v1":
        vetoes.append("phase2_schema_mismatch")
    if mass_payload.get("decision", {}).get("mass_handoff_passed") is not True:
        vetoes.append("phase2_mass_handoff_not_passed")
    if mass_payload.get("decision", {}).get("vetoes"):
        vetoes.append("phase2_vetoes_present")

    contract = mass_payload.get("coordinate_contract", {})
    convention = mass_payload.get("matrix_convention", {})
    if contract.get("coordinate_system") != "whitened_center_plus_scale_times_z":
        vetoes.append("coordinate_system_mismatch")
    if contract.get("theta_from_z") != "theta = center + scale * z":
        vetoes.append("theta_from_z_mismatch")
    if convention.get("hmc_handoff_matrix") != "M_z":
        vetoes.append("hmc_handoff_matrix_mismatch")
    if convention.get("inverse_mass_for_formula") != "K_z":
        vetoes.append("inverse_mass_convention_mismatch")
    if bool(contract.get("refined_center_used")):
        vetoes.append("refined_center_unexpectedly_used")

    center = np.asarray(geometry_payload.get("center", {}).get("free_parameter_values"), dtype=float)
    scale = np.asarray(contract.get("scale"), dtype=float)
    factor = np.asarray(mass_payload.get("mass_handoff", {}).get("factor"), dtype=float)
    covariance = np.asarray(
        mass_payload.get("mass_handoff", {}).get("mass_covariance_M_z"),
        dtype=float,
    )
    precision = np.asarray(
        mass_payload.get("mass_handoff", {}).get("regularized_precision_K_z"),
        dtype=float,
    )
    if center.shape != (4,):
        vetoes.append("center_shape_mismatch")
    if scale.shape != (4,) or not np.all(np.isfinite(scale)) or np.any(scale <= 0.0):
        vetoes.append("scale_shape_or_value_mismatch")
    for name, matrix in (
        ("factor", factor),
        ("mass_covariance_M_z", covariance),
        ("regularized_precision_K_z", precision),
    ):
        if matrix.shape != (4, 4) or not np.all(np.isfinite(matrix)):
            vetoes.append(f"{name}_shape_or_finiteness_mismatch")
    if not vetoes:
        reconstruction_error = float(np.max(np.abs(factor @ factor.T - covariance)))
        identity_error = float(np.max(np.abs(precision @ covariance - np.eye(4))))
        if reconstruction_error > 1.0e-8:
            vetoes.append("mass_factor_reconstruction_failed")
        if identity_error > 1.0e-8:
            vetoes.append("precision_mass_identity_failed")
    else:
        reconstruction_error = None
        identity_error = None

    if vetoes:
        return None, {
            "precondition_passed": False,
            "vetoes": tuple(dict.fromkeys(vetoes)),
            "coordinate_contract": contract,
            "matrix_convention": convention,
        }

    harness = load_phase1_harness()
    settings = harness.default_settings()
    target = harness.build_filtering_geometry_target(settings)
    target_center = np.asarray(target.truth_free.numpy(), dtype=float)
    target_scale = np.asarray(target.scale.numpy(), dtype=float)
    if not np.allclose(target_center, center, rtol=0.0, atol=1.0e-12):
        vetoes.append("rebuilt_target_center_mismatch")
    if not np.allclose(target_scale, scale, rtol=0.0, atol=1.0e-12):
        vetoes.append("rebuilt_target_scale_mismatch")
    if tuple(target.free_parameter_names) != tuple(contract.get("free_parameter_names")):
        vetoes.append("rebuilt_target_parameter_names_mismatch")
    if vetoes:
        return None, {
            "precondition_passed": False,
            "vetoes": tuple(dict.fromkeys(vetoes)),
            "coordinate_contract": contract,
            "matrix_convention": convention,
        }

    base_adapter = ScalarFilteringFreeParameterAdapter(target, evidence_path=SUBPLAN_PATH)
    # The base adapter evaluates free parameter values. Compose the reviewed
    # Phase 2 u->z preconditioner with the Phase 1 z->free-parameter map:
    # z = u @ chol(M_z).T, free = center + scale * z.
    free_factor = scale[:, np.newaxis] * factor
    transform = LatentAffineHMCTransform(
        center=center,
        factor=free_factor,
        covariance_provenance="phase2_M_z_cholesky_composed_with_phase1_scale",
        log_jacobian_convention="constant_omitted",
        nonclaims=(
            "Phase 3 affine mass preconditioner only",
            "no posterior convergence claim",
            "no tuned mass claim",
        ),
    )
    adapter = LatentAffineBatchValueScoreAdapter(
        base_adapter=base_adapter,
        transform=transform,
        target_scope="scalar_ssl_lstm:svd_ukf_filtering_geometry:phase3_mechanics_u",
        evidence_path=SUBPLAN_PATH,
        xla_hmc_ready=False,
        full_chain_xla_diagnostic_ready=False,
        nonclaims=(
            "Phase 3 mass-preconditioned mechanics canary only",
            "TFP HMC coordinate u is not Phase 1 z",
            "Phase 2 mass is applied by z = u @ chol(M_z).T",
            "no HMC convergence claim",
            "no posterior correctness claim",
        ),
    )
    audit = {
        "precondition_passed": True,
        "vetoes": (),
        "coordinate_contract": {
            "phase1_target_coordinate_z": "theta = center + scale * z",
            "tfp_hmc_coordinate_u": "z = u @ chol(M_z).T",
            "base_adapter_coordinate": "free parameter values",
            "free_parameters_from_u": "free = center + scale * (u @ chol(M_z).T)",
            "center_role": contract.get("center_role"),
            "refined_center_used": False,
            "free_parameter_names": contract.get("free_parameter_names"),
            "free_parameter_indices": contract.get("free_parameter_indices"),
        },
        "matrix_convention": {
            "M_z": convention.get("M_z"),
            "K_z": convention.get("K_z"),
            "hmc_handoff_matrix": convention.get("hmc_handoff_matrix"),
            "tfp_dense_mass_handling": (
                "stock TFP HMC identity kinetic energy; dense mass represented by affine u->z transform"
            ),
        },
        "mass_audit": {
            "factor_shape": factor.shape,
            "factor_reconstructs_M_z_max_abs_error": reconstruction_error,
            "K_z_times_M_z_identity_max_abs_error": identity_error,
            "M_z_eigen_summary": eigen_summary(covariance),
            "K_z_eigen_summary": eigen_summary(precision),
            "free_parameter_covariance_eigen_summary": eigen_summary(
                np.diag(scale) @ covariance @ np.diag(scale)
            ),
        },
        "adapter_signature": stable_adapter_signature(adapter),
        "base_adapter_signature": stable_adapter_signature(base_adapter),
    }
    return adapter, json_ready(audit)


def run_candidate(
    adapter: Any,
    *,
    settings: MechanicsCanarySettings,
    candidate_index: int,
    num_leapfrog_steps: int,
    step_size: float,
) -> Mapping[str, Any]:
    start = time.perf_counter()
    hard_vetoes: list[str] = []
    error_message = None
    initial_state = tf.zeros((adapter.parameter_dim,), dtype=tf.float64)
    initial_value = None
    initial_score = None
    result = None
    diagnostics: Mapping[str, Any] = {}
    metadata: Mapping[str, Any] = {}
    try:
        initial_value_tensor, initial_score_tensor = adapter.log_prob_and_grad(initial_state)
        initial_value = float(tf.convert_to_tensor(initial_value_tensor, dtype=tf.float64).numpy())
        initial_score = np.asarray(
            tf.reshape(tf.convert_to_tensor(initial_score_tensor, dtype=tf.float64), [-1]).numpy(),
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
            step_size=float(step_size),
            num_leapfrog_steps=int(num_leapfrog_steps),
            seed=(settings.seed[0], settings.seed[1] + int(candidate_index)),
            use_xla=False,
            trace_policy="standard",
            adaptation_policy="fixed_kernel_no_adaptation",
            target_scope=adapter.target_scope,
            chain_execution_mode="eager",
        )
        result = run_full_chain_tfp_hmc(adapter, initial_state, config)
    except Exception as exc:  # noqa: BLE001 - fail-closed mechanics artifact.
        error_message = f"{type(exc).__name__}: {exc}"
        hard_vetoes.append("hmc_runtime_exception")

    if result is not None:
        diagnostics = dict(result.diagnostics)
        metadata = dict(result.metadata)
        nonfinite_count = scalar_int(diagnostics.get("nonfinite_sample_count"))
        if nonfinite_count is None or nonfinite_count > 0:
            hard_vetoes.append("nonfinite_hmc_samples")
        health = diagnostics.get("hmc_health_diagnostics", {})
        log_accept = health.get("log_accept_ratio", {}) if isinstance(health, Mapping) else {}
        if isinstance(log_accept, Mapping):
            nonfinite_log_accept = scalar_int(log_accept.get("nonfinite_count"))
            if nonfinite_log_accept is None or nonfinite_log_accept > 0:
                hard_vetoes.append("nonfinite_log_accept_ratio")
        target_health = health.get("target_log_prob", {}) if isinstance(health, Mapping) else {}
        if isinstance(target_health, Mapping) and target_health.get("available"):
            if scalar_bool(target_health.get("finite")) is not True:
                hard_vetoes.append("nonfinite_target_log_prob_trace")
        divergence_count = scalar_int(diagnostics.get("divergence_count"))
        if divergence_count is not None and divergence_count > 0:
            hard_vetoes.append("native_divergence_detected")

    samples_summary = summarize_samples(result.samples) if result is not None else {}
    trace_summary = summarize_trace(result.trace) if result is not None else {}
    status = "passed_mechanics_canary" if not hard_vetoes else "failed_mechanics_canary"
    return json_ready(
        {
            "candidate_index": int(candidate_index),
            "num_leapfrog_steps": int(num_leapfrog_steps),
            "step_size": float(step_size),
            "trajectory_length_L_times_epsilon": float(num_leapfrog_steps * step_size),
            "status": status,
            "hard_vetoes": tuple(dict.fromkeys(hard_vetoes)),
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
                "status": "primary_phase3_mechanics_pass_fail",
                "hard_vetoes": "hard_veto_evidence",
                "initial_value_finite": "hard_veto_evidence",
                "initial_score_finite": "hard_veto_evidence",
                "nonfinite_hmc_samples": "hard_veto_evidence",
                "acceptance_rate": "explanatory_mechanics_only",
                "log_accept_ratio": "explanatory_mechanics_only",
                "trajectory_length_L_times_epsilon": "explanatory_mechanics_only",
                "runtime_seconds": "explanatory_only",
                "native_divergence": "hard_veto_if_available_positive; unavailable is not zero divergences",
            },
            "nonclaims": (
                "candidate mechanics telemetry only",
                "not HMC convergence evidence",
                "not posterior correctness evidence",
                "not a tuned kernel claim",
            ),
        }
    )


def run_mechanics_canary(
    geometry_payload: Mapping[str, Any],
    mass_payload: Mapping[str, Any],
    settings: MechanicsCanarySettings | None = None,
) -> Mapping[str, Any]:
    cfg = MechanicsCanarySettings() if settings is None else settings
    start = time.perf_counter()
    adapter, precondition = build_phase3_adapter(geometry_payload, mass_payload)
    rows = []
    vetoes = list(precondition.get("vetoes", ()))
    if adapter is not None:
        for index, (num_leapfrog_steps, step_size) in enumerate(cfg.candidate_grid):
            rows.append(
                run_candidate(
                    adapter,
                    settings=cfg,
                    candidate_index=index,
                    num_leapfrog_steps=num_leapfrog_steps,
                    step_size=step_size,
                )
            )
    else:
        vetoes.append("phase3_precondition_failed")

    passed_rows = [row for row in rows if row.get("status") == "passed_mechanics_canary"]
    if not rows:
        vetoes.append("no_candidate_rows")
    if not passed_rows:
        vetoes.append("no_candidate_with_finite_mechanics_telemetry")
    for row in rows:
        for veto in row.get("hard_vetoes", ()):
            vetoes.append(f"candidate_{row['candidate_index']}_{veto}")
    unique_vetoes = tuple(dict.fromkeys(vetoes))
    phase_passed = bool(not unique_vetoes and passed_rows)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "artifact_role": "cpu_hidden_scalar_filtering_hmc_mechanics_canary",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "script": f"docs/benchmarks/{SCRIPT_NAME}",
        "plan_path": PLAN_PATH,
        "subplan_path": SUBPLAN_PATH,
        "result_path": RESULT_PATH,
        "classification": "extension_or_invention",
        "target_scope": (
            None if adapter is None else adapter.target_scope
        ),
        "settings": cfg.payload(),
        "environment": environment_payload(),
        "git": git_payload(),
        "source_artifacts": {
            "geometry_json": str(DEFAULT_GEOMETRY_PATH.relative_to(ROOT)),
            "mass_json": str(DEFAULT_MASS_PATH.relative_to(ROOT)),
        },
        "precondition": precondition,
        "candidate_rows": rows,
        "decision": {
            "mechanics_canary_passed": phase_passed,
            "vetoes": unique_vetoes,
            "passed_candidate_count": len(passed_rows),
            "candidate_count": len(rows),
            "viable_for_phase4_short_hmc_smoke": phase_passed,
            "next_justified_action": (
                "draft and review Phase 4 short HMC smoke subplan"
                if phase_passed
                else "write Phase 3 blocker/repair result before any short HMC smoke"
            ),
        },
        "metric_roles": {
            "mechanics_canary_passed": "primary_phase3_pass_fail",
            "candidate_hard_vetoes": "hard_veto_evidence",
            "finite_initial_value_score": "hard_veto_evidence",
            "finite_hmc_samples": "hard_veto_evidence",
            "native_divergence": "hard_veto_if_available_positive",
            "acceptance_rate": "explanatory_mechanics_only",
            "log_accept_ratio": "explanatory_mechanics_only",
            "trajectory_length_L_times_epsilon": "explanatory_mechanics_only",
            "runtime": "explanatory_only",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if phase_passed else "failed",
            "statistically_supported_ranking": "none; fixed tiny mechanics grid",
            "descriptive_only_differences": (
                "acceptance, log accept ratio, target log-prob range, trajectory length, and runtime"
            ),
            "default_readiness": "not assessed",
            "hmc_readiness": "not assessed; mechanics canary only",
            "next_evidence_needed": (
                "reviewed Phase 4 short HMC smoke only if Phase 3 passes"
            ),
        },
        "run_manifest": {
            "command": (
                "timeout 180 env CUDA_VISIBLE_DEVICES=-1 python "
                "docs/benchmarks/benchmark_scalar_ssl_lstm_filtering_hmc_mechanics_canary_2026_07_08.py"
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


def summarize_samples(samples: Any) -> Mapping[str, Any]:
    array = np.asarray(tf.convert_to_tensor(samples, dtype=tf.float64).numpy(), dtype=float)
    finite = np.all(np.isfinite(array), axis=-1)
    return {
        "shape": array.shape,
        "finite_sample_count": int(np.sum(finite)),
        "nonfinite_sample_count": int(np.sum(~finite)),
        "final_u": array[-1],
        "max_abs_u": float(np.max(np.abs(array))) if array.size else None,
    }


def summarize_trace(trace: Mapping[str, Any]) -> Mapping[str, Any]:
    summary: dict[str, Any] = {}
    if "is_accepted" in trace:
        accepted = np.asarray(tf.convert_to_tensor(trace["is_accepted"]).numpy(), dtype=bool)
        summary["is_accepted"] = accepted
        summary["acceptance_rate"] = float(np.mean(accepted.astype(float))) if accepted.size else None
    if "log_accept_ratio" in trace:
        log_accept = np.asarray(
            tf.convert_to_tensor(trace["log_accept_ratio"], dtype=tf.float64).numpy(),
            dtype=float,
        )
        finite = np.isfinite(log_accept)
        summary["log_accept_ratio"] = {
            "values": log_accept,
            "finite_count": int(np.sum(finite)),
            "nonfinite_count": int(np.sum(~finite)),
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
            "values": target_log_prob,
            "finite": bool(np.all(finite)),
            "min": float(np.min(target_log_prob)) if target_log_prob.size else None,
            "max": float(np.max(target_log_prob)) if target_log_prob.size else None,
        }
    if "divergence" in trace:
        divergence = np.asarray(tf.convert_to_tensor(trace["divergence"]).numpy(), dtype=bool)
        summary["native_divergence"] = {
            "available": True,
            "count": int(np.sum(divergence)),
            "values": divergence,
        }
    else:
        summary["native_divergence"] = {
            "available": False,
            "status": "not_exposed_by_kernel",
            "nonclaim": "unavailable native divergence telemetry is not zero divergences",
        }
    return json_ready(summary)


def eigen_summary(matrix: Any) -> Mapping[str, Any]:
    values = np.linalg.eigvalsh(0.5 * (np.asarray(matrix, dtype=float) + np.asarray(matrix, dtype=float).T))
    finite = bool(np.all(np.isfinite(values)))
    positive = bool(finite and np.min(values) > 0.0)
    return {
        "finite": finite,
        "positive": positive,
        "min": float(np.min(values)) if finite else float("nan"),
        "max": float(np.max(values)) if finite else float("nan"),
        "condition_number": float(np.max(values) / np.min(values)) if positive else float("inf"),
        "eigenvalues": tuple(float(value) for value in values),
    }


def scalar_bool(value: Any) -> bool | None:
    if value is None:
        return None
    try:
        array = np.asarray(tf.convert_to_tensor(value).numpy())
    except Exception:  # noqa: BLE001
        array = np.asarray(value)
    if array.shape != ():
        return None
    return bool(array.item())


def scalar_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        array = np.asarray(tf.convert_to_tensor(value).numpy())
    except Exception:  # noqa: BLE001
        array = np.asarray(value)
    if array.shape != ():
        return None
    return int(array.item())


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
    lines = [
        "# Scalar SSL-LSTM Filtering HMC Mechanics Canary - 2026-07-08",
        "",
        "## Decision",
        "",
        f"- mechanics_canary_passed: `{decision['mechanics_canary_passed']}`",
        f"- vetoes: `{decision['vetoes']}`",
        f"- passed_candidate_count: `{decision['passed_candidate_count']}` / `{decision['candidate_count']}`",
        f"- next_justified_action: {decision['next_justified_action']}",
        "",
        "## Coordinate And Mass Convention",
        "",
        "- Phase 1 target coordinate: `theta = center + scale * z`.",
        "- TFP HMC coordinate: `u`.",
        "- Phase 2 mass use: `z = u @ chol(M_z).T`.",
        "- Stock TFP HMC dense mass handling: represented through the affine transform, not a direct dense-mass API.",
        "",
        "## Candidate Rows",
        "",
        "| candidate | L | step size | L*epsilon | status | vetoes | acceptance | max_abs_u |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload.get("candidate_rows", ()):
        diagnostics = row.get("diagnostics", {})
        acceptance = diagnostics.get("acceptance_rate")
        samples = row.get("samples_summary", {})
        lines.append(
            "| {idx} | {L} | {eps} | {tau} | {status} | {vetoes} | {acc} | {max_abs} |".format(
                idx=row.get("candidate_index"),
                L=row.get("num_leapfrog_steps"),
                eps=row.get("step_size"),
                tau=row.get("trajectory_length_L_times_epsilon"),
                status=row.get("status"),
                vetoes=", ".join(row.get("hard_vetoes", ())) or "none",
                acc=acceptance,
                max_abs=samples.get("max_abs_u"),
            )
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
    parser.add_argument("--json-path", type=Path, default=DEFAULT_JSON_PATH)
    parser.add_argument("--markdown-path", type=Path, default=DEFAULT_MARKDOWN_PATH)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    geometry_payload = load_json(args.geometry_json)
    mass_payload = load_json(args.mass_json)
    payload = run_mechanics_canary(geometry_payload, mass_payload)
    payload["source_artifacts"] = {
        "geometry_json": str(args.geometry_json),
        "mass_json": str(args.mass_json),
    }
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_path.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    args.markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
