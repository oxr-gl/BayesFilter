"""Minimal SSL-LSTM Zhao-Cui HMC validity Phase 3 longer diagnostic.

This harness runs the reviewed modest trusted GPU/XLA HMC diagnostic for the
internal minimal scalar-dimension ``zhaocui_fixed`` target. It separates
artifact validity from sampler-setting promotion: a valid artifact may still
record R-hat, ESS, reference, or native-divergence promotion vetoes. It does not
claim full posterior correctness, broad HMC convergence, ranking, readiness,
source-faithful Zhao-Cui parity, or LEDH evidence.
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
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any


os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BENCHMARK_DIR = Path(__file__).resolve().parent
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402
import tensorflow_probability as tfp  # noqa: E402

from bayesfilter.inference import (  # noqa: E402
    FullChainHMCConfig,
    run_full_chain_tfp_hmc,
    stable_adapter_signature,
    value_score_capability,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MinimalZhaoCuiHMCTargetAdapter,
    initial_minimal_ssl_lstm_hmc_state,
    minimal_ssl_lstm_fixture_payload,
    minimal_ssl_lstm_observations,
    minimal_ssl_lstm_theta,
)
from bayesfilter.runtime import atomic_write_json  # noqa: E402
from benchmark_minimal_ssl_lstm_zhaocui_hmc_oracle_2026_07_06 import (  # noqa: E402
    VALUE_ATOL,
    VALUE_RTOL,
    materialize_replay_noise,
    reference_log_prob_np,
    relative_error,
)


DATE_STAMP = "2026-07-06"
SCRIPT_NAME = "benchmark_minimal_ssl_lstm_zhaocui_hmc_validity_phase3_2026_07_06.py"
DEFAULT_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.json"
)
DEFAULT_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase3_longer_gpu_xla_2026-07-06.md"
)
QUIET_LOG_PATH = (
    "docs/benchmarks/logs/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_gaps_2026-07-06/"
    "phase3_longer_gpu_xla_2026-07-06.log"
)
MASTER_PROGRAM_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-master-program-2026-07-06.md"
)
PHASE2_JSON_PATH = (
    "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_validity_phase2_oracle_cpu_hidden_2026-07-06.json"
)
PHASE2_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase2-"
    "oracle-implementation-result-2026-07-06.md"
)
PHASE3_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-"
    "longer-hmc-diagnostics-subplan-2026-07-06.md"
)
PHASE3_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase3-"
    "longer-hmc-diagnostics-result-2026-07-06.md"
)
PHASE4_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-validity-gaps-phase4-"
    "divergence-telemetry-subplan-2026-07-06.md"
)
MECHANICS_BASELINE_JSON_PATH = (
    "docs/benchmarks/"
    "minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json"
)

REVIEWED_CHAIN_COUNT = 4
REVIEWED_NUM_RESULTS = 64
REVIEWED_NUM_BURNIN_STEPS = 32
REVIEWED_STEP_SIZE = 1.0e-5
REVIEWED_NUM_LEAPFROG_STEPS = 1
REVIEWED_HMC_SEED = (20260706, 6301)
REVIEWED_PRIOR_SCALE = 5.0
REVIEWED_INITIAL_OFFSET_SCALE = 1.0e-3
REVIEWED_CHAIN_START_SPREAD = 0.03
REVIEWED_RHAT_THRESHOLD = 1.2
REVIEWED_ESS_THRESHOLD = 16.0
SAMPLED_STATE_DRAW_ROLES = ("first", "middle", "final")

NONCLAIMS = (
    "Phase 3 modest longer HMC diagnostic only",
    "minimal scalar-dimension zhaocui_fixed target only",
    "not full posterior correctness evidence",
    "not broad HMC convergence evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not public API or package readiness evidence",
    "not LEDH evidence",
)


@dataclass(frozen=True)
class Phase3Settings:
    chain_count: int = REVIEWED_CHAIN_COUNT
    num_results: int = REVIEWED_NUM_RESULTS
    num_burnin_steps: int = REVIEWED_NUM_BURNIN_STEPS
    step_size: float = REVIEWED_STEP_SIZE
    num_leapfrog_steps: int = REVIEWED_NUM_LEAPFROG_STEPS
    seed: tuple[int, int] = REVIEWED_HMC_SEED
    prior_scale: float = REVIEWED_PRIOR_SCALE
    initial_offset_scale: float = REVIEWED_INITIAL_OFFSET_SCALE
    chain_start_spread: float = REVIEWED_CHAIN_START_SPREAD
    use_xla: bool = True
    require_gpu: bool = True
    trace_policy: str = "standard"
    adaptation_policy: str = "fixed_kernel_no_adaptation"
    chain_execution_mode: str = "tf_function"
    rhat_threshold: float = REVIEWED_RHAT_THRESHOLD
    ess_threshold: float = REVIEWED_ESS_THRESHOLD
    artifact_mode: str = "reviewed_trusted_gpu_xla"

    def __post_init__(self) -> None:
        for name in ("chain_count", "num_results", "num_burnin_steps", "num_leapfrog_steps"):
            value = int(getattr(self, name))
            if value <= 0:
                raise ValueError(f"{name} must be positive")
            object.__setattr__(self, name, value)
        step_size = float(self.step_size)
        if not math.isfinite(step_size) or step_size <= 0.0:
            raise ValueError("step_size must be positive and finite")
        object.__setattr__(self, "step_size", step_size)
        for name in ("prior_scale", "chain_start_spread", "rhat_threshold", "ess_threshold"):
            value = float(getattr(self, name))
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be positive and finite")
            object.__setattr__(self, name, value)
        initial_offset_scale = float(self.initial_offset_scale)
        if not math.isfinite(initial_offset_scale):
            raise ValueError("initial_offset_scale must be finite")
        object.__setattr__(self, "initial_offset_scale", initial_offset_scale)
        seed = tuple(int(item) for item in self.seed)
        if len(seed) != 2:
            raise ValueError("seed must contain exactly two integers")
        object.__setattr__(self, "seed", seed)
        trace_policy = str(self.trace_policy)
        if trace_policy != "standard":
            raise ValueError("Phase 3 requires trace_policy='standard'")
        object.__setattr__(self, "trace_policy", trace_policy)
        if str(self.adaptation_policy) != "fixed_kernel_no_adaptation":
            raise ValueError("Phase 3 uses fixed_kernel_no_adaptation only")
        if str(self.chain_execution_mode) != "tf_function":
            raise ValueError("Phase 3 uses chain_execution_mode='tf_function'")
        object.__setattr__(self, "use_xla", bool(self.use_xla))
        object.__setattr__(self, "require_gpu", bool(self.require_gpu))
        object.__setattr__(self, "artifact_mode", str(self.artifact_mode))

    def payload(self) -> dict[str, Any]:
        return {
            "chain_count": self.chain_count,
            "num_results": self.num_results,
            "num_burnin_steps": self.num_burnin_steps,
            "step_size": self.step_size,
            "num_leapfrog_steps": self.num_leapfrog_steps,
            "seed": list(self.seed),
            "prior_scale": self.prior_scale,
            "initial_offset_scale": self.initial_offset_scale,
            "chain_start_spread": self.chain_start_spread,
            "use_xla": self.use_xla,
            "jit_compile": self.use_xla,
            "require_gpu": self.require_gpu,
            "trace_policy": self.trace_policy,
            "adaptation_policy": self.adaptation_policy,
            "chain_execution_mode": self.chain_execution_mode,
            "rhat_threshold": self.rhat_threshold,
            "ess_threshold": self.ess_threshold,
            "artifact_mode": self.artifact_mode,
        }


def reviewed_phase3_settings() -> Phase3Settings:
    return Phase3Settings()


def test_cpu_phase3_settings(
    *,
    num_results: int = 4,
    num_burnin_steps: int = 1,
    chain_count: int = 2,
) -> Phase3Settings:
    """Return a tiny CPU-hidden setting for focused tests, not the runbook CLI."""

    return Phase3Settings(
        chain_count=chain_count,
        num_results=num_results,
        num_burnin_steps=num_burnin_steps,
        seed=(20260706, 6399),
        use_xla=False,
        require_gpu=False,
        rhat_threshold=100.0,
        ess_threshold=1.0,
        artifact_mode="focused_cpu_hidden_test_helper",
    )


def deterministic_chain_initial_state(
    base_state: tf.Tensor,
    *,
    chain_count: int,
    spread: float,
) -> tf.Tensor:
    """Return deterministic dispersed starts with shape [chain, parameter]."""

    base = tf.reshape(tf.convert_to_tensor(base_state, dtype=tf.float64), [-1])
    dim = int(base.shape[0])
    offsets = tf.linspace(
        tf.constant(-float(spread), dtype=tf.float64),
        tf.constant(float(spread), dtype=tf.float64),
        int(chain_count),
    )
    parity = tf.cast(tf.math.floormod(tf.range(dim, dtype=tf.int32), 2), tf.float64)
    pattern = tf.constant(1.0, dtype=tf.float64) - tf.constant(2.0, dtype=tf.float64) * parity
    return tf.expand_dims(base, axis=0) + tf.expand_dims(offsets, axis=-1) * pattern


def selected_draw_indices(num_results: int) -> list[tuple[str, int]]:
    middle = int(num_results) // 2
    indices = [
        ("first", 0),
        ("middle", middle),
        ("final", int(num_results) - 1),
    ]
    deduped: list[tuple[str, int]] = []
    seen: set[int] = set()
    for role, index in indices:
        if index not in seen:
            deduped.append((role, index))
            seen.add(index)
    return deduped


def diagnostic_summary(values: Any, *, threshold: float, direction: str) -> dict[str, Any]:
    array = np.asarray(values, dtype=np.float64).reshape(-1)
    finite = np.isfinite(array)
    finite_values = array[finite]
    finite_count = int(np.sum(finite))
    nonfinite_count = int(array.size - finite_count)
    if finite_count:
        min_value = float(np.min(finite_values))
        max_value = float(np.max(finite_values))
    else:
        min_value = None
        max_value = None
    if direction == "le":
        passed = bool(finite_count == array.size and max_value is not None and max_value <= float(threshold))
    elif direction == "ge":
        passed = bool(finite_count == array.size and min_value is not None and min_value >= float(threshold))
    else:
        raise ValueError("direction must be 'le' or 'ge'")
    return {
        "passed": passed,
        "threshold": float(threshold),
        "direction": direction,
        "finite_count": finite_count,
        "nonfinite_count": nonfinite_count,
        "min": min_value,
        "max": max_value,
        "values": [None if not np.isfinite(value) else float(value) for value in array],
    }


def compute_rhat_ess_summaries(
    samples: np.ndarray,
    *,
    rhat_threshold: float,
    ess_threshold: float,
) -> dict[str, Any]:
    sample_tensor = tf.convert_to_tensor(np.asarray(samples, dtype=np.float64), dtype=tf.float64)
    rhat = tfp.mcmc.potential_scale_reduction(
        sample_tensor,
        independent_chain_ndims=1,
        split_chains=True,
    )
    ess = tfp.mcmc.effective_sample_size(sample_tensor, cross_chain_dims=1)
    return {
        "rhat": diagnostic_summary(
            rhat.numpy(),
            threshold=float(rhat_threshold),
            direction="le",
        ),
        "ess": diagnostic_summary(
            ess.numpy(),
            threshold=float(ess_threshold),
            direction="ge",
        ),
        "method": {
            "rhat": "tfp.mcmc.potential_scale_reduction(split_chains=True)",
            "ess": "tfp.mcmc.effective_sample_size(cross_chain_dims=1)",
            "sample_shape_convention": "[draw, chain, parameter]",
        },
    }


def sampled_state_reference_check(
    adapter: MinimalZhaoCuiHMCTargetAdapter,
    samples: np.ndarray,
    *,
    prior_scale: float,
) -> dict[str, Any]:
    theta_center = np.asarray(minimal_ssl_lstm_theta().numpy(), dtype=np.float64)
    observations = np.asarray(minimal_ssl_lstm_observations().numpy(), dtype=np.float64)
    noise = materialize_replay_noise()
    rows: list[dict[str, Any]] = []
    max_abs_error = 0.0
    max_rel_error = 0.0
    all_passed = True
    all_finite = True
    sample_array = np.asarray(samples, dtype=np.float64)
    for role, draw_index in selected_draw_indices(sample_array.shape[0]):
        for chain_index in range(sample_array.shape[1]):
            state = sample_array[int(draw_index), int(chain_index), :]
            target_value, _score = adapter.log_prob_and_grad(tf.constant(state, dtype=tf.float64))
            target_float = float(target_value.numpy())
            reference_float = float(
                reference_log_prob_np(
                    state,
                    observations,
                    noise,
                    prior_center=theta_center,
                    prior_scale=float(prior_scale),
                )
            )
            abs_error = abs(target_float - reference_float)
            rel_error = relative_error(abs_error, target_float, reference_float)
            passed = bool(abs_error <= VALUE_ATOL or rel_error <= VALUE_RTOL)
            finite = bool(math.isfinite(target_float) and math.isfinite(reference_float))
            all_passed = bool(all_passed and passed)
            all_finite = bool(all_finite and finite)
            max_abs_error = max(max_abs_error, float(abs_error))
            max_rel_error = max(max_rel_error, float(rel_error))
            rows.append(
                {
                    "draw_role": role,
                    "draw_index": int(draw_index),
                    "chain_index": int(chain_index),
                    "target_value": target_float,
                    "reference_value": reference_float,
                    "abs_error": float(abs_error),
                    "rel_error": float(rel_error),
                    "passed": passed,
                    "finite": finite,
                }
            )
    return {
        "passed": bool(all_passed and all_finite),
        "all_values_finite": bool(all_finite),
        "checked_state_count": len(rows),
        "value_atol": VALUE_ATOL,
        "value_rtol": VALUE_RTOL,
        "max_abs_error": float(max_abs_error),
        "max_rel_error": float(max_rel_error),
        "rows": rows,
        "reference_source": "Phase 2 independent NumPy replay functions",
    }


def sample_summary(samples: np.ndarray) -> dict[str, Any]:
    array = np.asarray(samples, dtype=np.float64)
    flat = np.reshape(array, (-1, array.shape[-1]))
    return {
        "shape": [int(dim) for dim in array.shape],
        "overall_mean": float(np.mean(array)),
        "overall_std": float(np.std(array)),
        "overall_min": float(np.min(array)),
        "overall_max": float(np.max(array)),
        "coordinate_mean": [float(value) for value in np.mean(flat, axis=0)],
        "coordinate_std": [float(value) for value in np.std(flat, axis=0)],
        "raw_samples_publicized": False,
    }


def _nested_get(mapping: Mapping[str, Any], path: Sequence[str]) -> Any:
    value: Any = mapping
    for key in path:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def _as_int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    try:
        return int(np.asarray(value).reshape(()))
    except Exception:  # noqa: BLE001
        return None


def _as_float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    try:
        result = float(np.asarray(value).reshape(()))
    except Exception:  # noqa: BLE001
        return None
    return result if math.isfinite(result) else result


def _as_bool_or_none(value: Any) -> bool | None:
    if value is None:
        return None
    if hasattr(value, "numpy"):
        value = value.numpy()
    try:
        return bool(np.asarray(value).reshape(()))
    except Exception:  # noqa: BLE001
        return None


def continuation_vetoes_from_hmc_diagnostics(diagnostics: Mapping[str, Any]) -> list[str]:
    vetoes: list[str] = []
    nonfinite_samples = _as_int_or_none(diagnostics.get("nonfinite_sample_count"))
    if nonfinite_samples is None or nonfinite_samples != 0:
        vetoes.append("nonfinite_hmc_samples")
    log_accept_nonfinite = _as_int_or_none(
        _nested_get(
            diagnostics,
            ("hmc_health_diagnostics", "log_accept_ratio", "nonfinite_count"),
        )
    )
    if log_accept_nonfinite is None or log_accept_nonfinite != 0:
        vetoes.append("nonfinite_log_accept_ratio")
    target_finite = _as_bool_or_none(
        _nested_get(
            diagnostics,
            ("hmc_health_diagnostics", "target_log_prob", "finite"),
        )
    )
    if target_finite is not True:
        vetoes.append("nonfinite_trace_target_log_prob")
    return vetoes


def promotion_vetoes_from_summaries(
    *,
    rhat_summary: Mapping[str, Any] | None,
    ess_summary: Mapping[str, Any] | None,
    reference_check: Mapping[str, Any] | None,
    diagnostics: Mapping[str, Any],
) -> list[str]:
    vetoes: list[str] = []
    if rhat_summary is None or not bool(rhat_summary.get("passed")):
        vetoes.append("split_rhat_threshold_failed")
    if ess_summary is None or not bool(ess_summary.get("passed")):
        vetoes.append("ess_threshold_failed")
    if reference_check is None or not bool(reference_check.get("passed")):
        vetoes.append("sampled_state_reference_check_failed")
    divergence_status = str(diagnostics.get("divergence_status"))
    divergence_count = _as_int_or_none(diagnostics.get("divergence_count"))
    if divergence_status == "not_exposed_by_kernel":
        vetoes.append("native_divergence_telemetry_not_exposed")
    elif divergence_count is not None and divergence_count > 0:
        vetoes.append("native_divergence_detected")
    return list(dict.fromkeys(vetoes))


def phase2_status() -> dict[str, Any]:
    path = ROOT / PHASE2_JSON_PATH
    if not path.exists():
        return {"path": PHASE2_JSON_PATH, "exists": False, "status": None, "passed": False}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {
            "path": PHASE2_JSON_PATH,
            "exists": True,
            "status": None,
            "passed": False,
            "error": f"{type(exc).__name__}: {exc}",
        }
    status = payload.get("status")
    return {
        "path": PHASE2_JSON_PATH,
        "exists": True,
        "status": status,
        "passed": status == "passed",
        "schema_version": payload.get("schema_version"),
    }


def build_phase3_longer_hmc_artifact(
    *,
    trusted_gpu_xla_approval: bool,
    settings: Phase3Settings | None = None,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run or preflight the Phase 3 longer HMC diagnostic."""

    started = time.perf_counter()
    settings = reviewed_phase3_settings() if settings is None else settings
    adapter = MinimalZhaoCuiHMCTargetAdapter(
        prior_scale=settings.prior_scale,
        evidence_path=PHASE3_SUBPLAN_PATH,
    )
    base_state = initial_minimal_ssl_lstm_hmc_state(settings.initial_offset_scale)
    initial_state = deterministic_chain_initial_state(
        base_state,
        chain_count=settings.chain_count,
        spread=settings.chain_start_spread,
    )
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    device_summary = _tf_device_summary(
        trust_basis=(
            "explicit_user_approved_trusted_gpu_xla_phase3_longer_hmc"
            if settings.require_gpu
            else "cpu_hidden_focused_test_helper_no_gpu_claim"
        )
    )
    phase2 = phase2_status()
    capability = value_score_capability(adapter)

    continuation_vetoes: list[str] = []
    if not phase2["passed"]:
        continuation_vetoes.append("phase2_oracle_artifact_not_passed")
    if settings.require_gpu and not bool(trusted_gpu_xla_approval):
        continuation_vetoes.append("missing_trusted_gpu_xla_approval")
    if settings.require_gpu and os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
        continuation_vetoes.append("gpu_hidden_for_trusted_phase3")
    if settings.require_gpu and not device_summary["gpu_devices"]:
        continuation_vetoes.append("gpu_device_not_visible")
    initial_value_finite = bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy())
    initial_score_finite = bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy())
    if not initial_value_finite:
        continuation_vetoes.append("initial_target_value_nonfinite")
    if not initial_score_finite:
        continuation_vetoes.append("initial_target_score_nonfinite")

    hmc_error = None
    not_run_reason = None
    diagnostics: Mapping[str, Any] = {}
    metadata: Mapping[str, Any] = {}
    samples_np: np.ndarray | None = None
    rhat_ess: Mapping[str, Any] | None = None
    reference_check: Mapping[str, Any] | None = None
    samples_summary: Mapping[str, Any] | None = None
    hmc_runtime_s = 0.0

    if continuation_vetoes:
        not_run_reason = "preflight_continuation_veto"
    else:
        hmc_config = FullChainHMCConfig(
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
        hmc_start = time.perf_counter()
        try:
            hmc_result = run_full_chain_tfp_hmc(adapter, initial_state, hmc_config)
        except Exception as exc:  # noqa: BLE001
            hmc_error = f"{type(exc).__name__}: {exc}"
            continuation_vetoes.append("hmc_runtime_exception")
        else:
            diagnostics = dict(hmc_result.diagnostics)
            metadata = dict(hmc_result.metadata)
            samples = tf.convert_to_tensor(hmc_result.samples, dtype=tf.float64)
            samples_np = np.asarray(samples.numpy(), dtype=np.float64)
            if not np.all(np.isfinite(samples_np)):
                continuation_vetoes.append("nonfinite_hmc_samples")
            continuation_vetoes.extend(continuation_vetoes_from_hmc_diagnostics(diagnostics))
            if not continuation_vetoes:
                rhat_ess = compute_rhat_ess_summaries(
                    samples_np,
                    rhat_threshold=settings.rhat_threshold,
                    ess_threshold=settings.ess_threshold,
                )
                reference_check = sampled_state_reference_check(
                    adapter,
                    samples_np,
                    prior_scale=settings.prior_scale,
                )
                samples_summary = sample_summary(samples_np)
        hmc_runtime_s = time.perf_counter() - hmc_start

    promotion_vetoes = promotion_vetoes_from_summaries(
        rhat_summary=None if rhat_ess is None else rhat_ess["rhat"],
        ess_summary=None if rhat_ess is None else rhat_ess["ess"],
        reference_check=reference_check,
        diagnostics=diagnostics,
    )
    artifact_valid = not continuation_vetoes
    promotion_passed = bool(artifact_valid and not promotion_vetoes)
    total_runtime_s = time.perf_counter() - started
    artifact = {
        "schema_version": "minimal_ssl_lstm_zhaocui_hmc_validity.phase3_longer_hmc.v1",
        "status": "passed" if artifact_valid else "failed",
        "promotion_screen_status": "passed" if promotion_passed else "failed",
        "date": DATE_STAMP,
        "phase": "PHASE3",
        "artifact_role": "longer_hmc_convergence_reference_diagnostic",
        "filter_name": "zhaocui_fixed",
        "fixture": minimal_ssl_lstm_fixture_payload(),
        "evidence_contract": {
            "question": (
                "Does a modest longer trusted GPU/XLA fixed-kernel HMC run on the "
                "minimal target produce valid artifacts, finite samples, sampled-state "
                "target/reference agreement, and minimal R-hat/ESS screen evidence?"
            ),
            "baseline_comparator": (
                f"{PHASE2_JSON_PATH} plus {MECHANICS_BASELINE_JSON_PATH}"
            ),
            "primary_artifact_criterion": (
                "Exact command runs or records a preflight blocker and writes valid "
                "JSON/Markdown/log artifacts with diagnostic roles."
            ),
            "promotion_criterion": (
                "No continuation vetoes, sampled-state reference check passes, "
                f"split R-hat <= {settings.rhat_threshold}, cross-chain ESS >= "
                f"{settings.ess_threshold}, and native divergence telemetry is "
                "available with no positive divergences."
            ),
            "continuation_vetoes": (
                "Runtime exception preventing diagnostics, nonfinite samples/target "
                "values, invalid Phase 2 comparator, GPU/XLA provenance failure for "
                "trusted run, invalid artifact, or unsupported claim."
            ),
            "promotion_vetoes": (
                "Failed R-hat/ESS/reference checks, positive or unavailable native "
                "divergence telemetry, or written diagnostic evidence against the "
                "current fixed-kernel setting."
            ),
            "not_concluded": NONCLAIMS,
        },
        "phase2_oracle_status": phase2,
        "predeclared_settings": settings.payload(),
        "runtime_boundary": {
            "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
            "user_approval_record": "user approved longer-HMC boundary on 2026-07-06",
            "review_required_before_runtime": True,
            "command_locked_by_cli": True,
        },
        "initial_target": {
            "log_prob": _json_ready(initial_value),
            "score_norm": float(tf.linalg.norm(initial_score).numpy()),
            "value_finite": initial_value_finite,
            "score_finite": initial_score_finite,
            "initial_state_shape": [int(dim) for dim in initial_state.shape.as_list()],
            "base_state_offset_scale": settings.initial_offset_scale,
            "chain_start_spread": settings.chain_start_spread,
        },
        "hmc_runtime": {
            "runtime_s": float(hmc_runtime_s),
            "error": hmc_error,
            "not_run_reason": not_run_reason,
            "sample_shape": None if samples_np is None else [int(dim) for dim in samples_np.shape],
            "samples_all_finite": None if samples_np is None else bool(np.all(np.isfinite(samples_np))),
            "diagnostics": _json_ready(diagnostics),
            "metadata": _json_ready(metadata),
        },
        "sample_summary": None if samples_summary is None else _json_ready(samples_summary),
        "rhat_ess": None if rhat_ess is None else _json_ready(rhat_ess),
        "sampled_state_reference_check": (
            None if reference_check is None else _json_ready(reference_check)
        ),
        "native_divergence_interpretation": (
            "native divergence status 'not_exposed_by_kernel' is telemetry "
            "unavailability, not zero divergences"
        ),
        "continuation_vetoes": list(dict.fromkeys(continuation_vetoes)),
        "promotion_vetoes": list(dict.fromkeys(promotion_vetoes)),
        "hard_vetoes": list(dict.fromkeys(continuation_vetoes)),
        "promotion_screen": {
            "status": "passed" if promotion_passed else "failed",
            "artifact_valid": artifact_valid,
            "continuation_vetoes": list(dict.fromkeys(continuation_vetoes)),
            "promotion_vetoes": list(dict.fromkeys(promotion_vetoes)),
            "interpretation": (
                "Promotion failure rejects only the current fixed-kernel sampler "
                "setting unless a continuation veto invalidates the artifact."
            ),
        },
        "capability": {
            "value_score_authority": capability.value_score_authority,
            "xla_hmc_ready": bool(capability.xla_hmc_ready),
            "full_chain_xla_diagnostic_ready": bool(
                capability.full_chain_xla_diagnostic_ready
            ),
            "runtime_backend": capability.runtime_backend,
            "target_scope": capability.target_scope,
            "evidence_path": capability.evidence_path,
            "nonclaims": list(capability.nonclaims),
        },
        "adapter_signature": stable_adapter_signature(adapter),
        "run_manifest": {
            "git_commit": _git_commit(),
            "git_dirty_summary": _git_dirty_summary(),
            "command": list(command or (sys.executable, str(Path(__file__).resolve()))),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "tensorflow_probability_version": tfp.__version__,
            "cpu_gpu_status": device_summary,
            "compile_mode": settings.chain_execution_mode,
            "jit_compile": bool(settings.use_xla),
            "use_xla": bool(settings.use_xla),
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "trust_basis": device_summary["trust_basis"],
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE3_SUBPLAN_PATH,
            "result_file": PHASE3_RESULT_PATH,
            "next_subplan_file": PHASE4_SUBPLAN_PATH,
            "quiet_log_path": QUIET_LOG_PATH,
            "random_seeds": {
                "hmc_seed": [int(item) for item in settings.seed],
                "zhaocui_initial_seed": [20260705, 41],
                "zhaocui_process_seed": [20260705, 43],
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
            "runtime_s": float(total_runtime_s),
        },
        "metric_roles": {
            "continuation_vetoes": "continuation_veto_evidence",
            "promotion_vetoes": "sampler_setting_promotion_veto_evidence",
            "rhat": "promotion_screen_for_minimal_target_only",
            "ess": "promotion_screen_for_minimal_target_only",
            "sampled_state_reference_check": "promotion_screen_not_full_posterior_proof",
            "native_divergence_status": (
                "promotion_veto_if_unavailable_or_positive; missing telemetry is not zero divergences"
            ),
            "acceptance_rate": "explanatory_only_unless_finite_log_diagnostic_missing",
            "runtime": "explanatory_only",
            "sample_summary": "explanatory_only",
        },
        "inference_status": {
            "artifact_validity": "passed" if artifact_valid else "failed",
            "minimal_sampler_promotion_screen": (
                "passed" if promotion_passed else "failed"
            ),
            "hard_veto_screen": (
                "no continuation veto" if artifact_valid else "continuation veto recorded"
            ),
            "statistically_supported_ranking": "not_claimed",
            "descriptive_only_differences": (
                "Acceptance, runtime, trace summaries, and sample summaries are descriptive only."
            ),
            "default_readiness": "not_checked",
            "posterior_correctness": "not_established",
            "next_evidence_needed": (
                "Native divergence telemetry investigation and tuning/mass diagnostics "
                "before any broader convergence or readiness claim."
            ),
        },
        "decision_table": {
            "decision": (
                "valid_artifact_continue_to_phase4"
                if artifact_valid
                else "blocked_by_continuation_veto"
            ),
            "primary_criterion_status": "passed" if artifact_valid else "failed",
            "veto_diagnostic_status": (
                "promotion vetoes: " + ", ".join(promotion_vetoes)
                if promotion_vetoes
                else "no promotion vetoes"
            ),
            "main_uncertainty": (
                "This is a modest fixed-kernel diagnostic on a minimal target; it "
                "does not establish full posterior correctness or broad HMC convergence."
            ),
            "next_justified_action": (
                "write Phase 3 result and refresh Phase 4 divergence telemetry subplan"
                if artifact_valid
                else "repair continuation veto before additional HMC diagnostics"
            ),
            "what_is_not_being_concluded": (
                "No full posterior correctness, broad HMC convergence, ranking, "
                "default readiness, production readiness, source-faithful parity, "
                "public API/package readiness, or LEDH result."
            ),
        },
        "post_run_red_team": {
            "strongest_alternative_explanation": (
                "A passing or nearly passing minimal screen may reflect the tiny "
                "fixture and conservative step size rather than robust sampler behavior."
            ),
            "result_that_would_overturn": (
                "A reproduced nonfinite sample/target, invalid artifact, GPU/XLA "
                "provenance failure, target/reference mismatch, or positive native divergence."
            ),
            "weakest_part_of_evidence": (
                "Conditional and sampled-state value checks do not prove the full "
                "24-dimensional posterior, and the fixed kernel is not tuned."
            ),
        },
        "nonclaims": NONCLAIMS,
    }
    return artifact


def render_markdown(artifact: Mapping[str, Any]) -> str:
    settings = artifact["predeclared_settings"]
    runtime = artifact["hmc_runtime"]
    rhat_ess = artifact.get("rhat_ess") or {}
    reference = artifact.get("sampled_state_reference_check") or {}
    device = artifact["run_manifest"]["cpu_gpu_status"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Validity Phase 3 Longer Diagnostic",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Promotion screen: `{artifact['promotion_screen_status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- CUDA_VISIBLE_DEVICES: `{device.get('cuda_visible_devices')}`",
        f"- GPU devices: `{device.get('gpu_devices')}`",
        f"- XLA/JIT: `{settings['use_xla']}` / `{settings['jit_compile']}`",
        f"- Chain count: `{settings['chain_count']}`",
        f"- Draws per chain: `{settings['num_results']}`",
        f"- Burn-in per chain: `{settings['num_burnin_steps']}`",
        f"- HMC error: `{runtime.get('error')}`",
        f"- Not-run reason: `{runtime.get('not_run_reason')}`",
        f"- Sample shape: `{runtime.get('sample_shape')}`",
        f"- Samples all finite: `{runtime.get('samples_all_finite')}`",
        "",
        "## Promotion Screen",
        "",
        f"- R-hat passed: `{(rhat_ess.get('rhat') or {}).get('passed')}`",
        f"- R-hat max: `{(rhat_ess.get('rhat') or {}).get('max')}`",
        f"- ESS passed: `{(rhat_ess.get('ess') or {}).get('passed')}`",
        f"- ESS min: `{(rhat_ess.get('ess') or {}).get('min')}`",
        f"- Reference check passed: `{reference.get('passed')}`",
        f"- Reference max abs error: `{reference.get('max_abs_error')}`",
        f"- Reference max rel error: `{reference.get('max_rel_error')}`",
        f"- Continuation vetoes: `{artifact['continuation_vetoes']}`",
        f"- Promotion vetoes: `{artifact['promotion_vetoes']}`",
        "",
        "## Inference Status",
        "",
        "| field | value |",
        "| --- | --- |",
    ]
    for key, value in artifact["inference_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Decision Table", "", "| field | value |", "| --- | --- |"])
    for key, value in artifact["decision_table"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Native Divergence", ""])
    diagnostics = runtime.get("diagnostics") or {}
    lines.append(f"- Divergence status: `{diagnostics.get('divergence_status')}`")
    lines.append(f"- Divergence count: `{diagnostics.get('divergence_count')}`")
    lines.append(f"- Interpretation: `{artifact['native_divergence_interpretation']}`")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE3_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE3_RESULT_PATH}`")
    return "\n".join(lines) + "\n"


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


def _tf_device_summary(*, trust_basis: str) -> dict[str, Any]:
    physical = tf.config.list_physical_devices()
    return {
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>"),
        "physical_devices": [device.name for device in physical],
        "gpu_devices": [device.name for device in tf.config.list_physical_devices("GPU")],
        "trust_basis": trust_basis,
    }


def _json_ready(value: Any) -> Any:
    if hasattr(value, "numpy"):
        return _json_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return _json_ready(value.tolist())
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, (bool, int, float, str)) or value is None:
        return value
    return str(value)


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON_OUTPUT)
    parser.add_argument("--markdown-output", type=Path, default=DEFAULT_MARKDOWN_OUTPUT)
    parser.add_argument("--trusted-gpu-xla-approval", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)
    started = time.perf_counter()
    if not args.trusted_gpu_xla_approval:
        raise RuntimeError("Phase 3 reviewed GPU/XLA runtime requires --trusted-gpu-xla-approval")
    artifact = build_phase3_longer_hmc_artifact(
        trusted_gpu_xla_approval=True,
        settings=reviewed_phase3_settings(),
        command=tuple(sys.argv),
    )
    artifact["run_manifest"]["wall_time_s"] = float(time.perf_counter() - started)
    artifact["run_manifest"]["timestamp"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    atomic_write_json(args.output, artifact)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.write_text(render_markdown(artifact), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": artifact["status"],
                "promotion_screen_status": artifact["promotion_screen_status"],
                "json_output": str(args.output),
                "markdown_output": str(args.markdown_output),
                "continuation_vetoes": artifact["continuation_vetoes"],
                "promotion_vetoes": artifact["promotion_vetoes"],
            },
            sort_keys=True,
        )
    )
    return 0 if artifact["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
