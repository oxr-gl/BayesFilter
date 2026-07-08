"""Minimal scalar SSL-LSTM Zhao-Cui HMC ladder harness.

This harness admits an internal target adapter for the frozen scalar
``zhaocui_fixed`` fixture and, when explicitly requested, runs the Phase 2 tiny
CPU-hidden HMC canary. It does not claim convergence, posterior correctness,
ranking, GPU/XLA production readiness, default readiness, source-faithful
parity, or LEDH evidence.
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
from collections.abc import Mapping
from pathlib import Path
from typing import Any


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
BENCHMARK_DIR = Path(__file__).resolve().parent
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

import tensorflow as tf  # noqa: E402

from bayesfilter.inference import (  # noqa: E402
    FullChainHMCConfig,
    run_full_chain_tfp_hmc,
    stable_adapter_signature,
    value_score_capability,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_hmc_minimal import (  # noqa: E402
    MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS,
    MinimalZhaoCuiHMCTargetAdapter,
    initial_minimal_ssl_lstm_hmc_state,
    minimal_ssl_lstm_config,
    minimal_ssl_lstm_fixture_payload,
    minimal_ssl_lstm_observations,
    minimal_ssl_lstm_theta,
    minimal_ssl_lstm_zhaocui_manifest,
)
from bayesfilter.runtime import atomic_write_json  # noqa: E402


DATE_STAMP = "2026-07-06"
DEFAULT_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.json"
)
DEFAULT_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_adapter_cpu_hidden_2026-07-06.md"
)
DEFAULT_CANARY_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.json"
)
DEFAULT_CANARY_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_canary_cpu_hidden_2026-07-06.md"
)
DEFAULT_LADDER_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.json"
)
DEFAULT_LADDER_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_short_ladder_cpu_hidden_2026-07-06.md"
)
DEFAULT_GPU_XLA_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.json"
)
DEFAULT_GPU_XLA_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase3_gpu_xla_smoke_2026-07-06.md"
)
DEFAULT_PHASE5_GPU_XLA_JSON_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json"
)
DEFAULT_PHASE5_GPU_XLA_MARKDOWN_OUTPUT = (
    ROOT
    / "docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.md"
)
MASTER_PROGRAM_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-master-program-2026-07-06.md"
)
PHASE1_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-subplan-2026-07-06.md"
)
PHASE1_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase1-target-adapter-result-2026-07-06.md"
)
PHASE2_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-subplan-2026-07-06.md"
)
PHASE2_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase2-cpu-hidden-canary-result-2026-07-06.md"
)
PHASE4_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-subplan-2026-07-06.md"
)
PHASE4_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase4-short-replicated-ladder-result-2026-07-06.md"
)
PHASE3_GPU_XLA_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-subplan-2026-07-06.md"
)
PHASE3_GPU_XLA_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase3-gpu-xla-smoke-result-2026-07-06.md"
)
PHASE5_LONGER_DIAGNOSTICS_SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-subplan-2026-07-06.md"
)
PHASE5_LONGER_DIAGNOSTICS_RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-phase5-longer-diagnostics-execution-result-2026-07-06.md"
)
ZHAOCUI_EVIDENCE_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-zhaocui-first-phase2-"
    "zhaocui-fixed-adapter-implementation-result-2026-07-05.md"
)
NONCLAIMS = MINIMAL_SSL_LSTM_ZHAOCUI_HMC_NONCLAIMS
PHASE2_NONCLAIMS = (
    "Phase 2 tiny HMC canary only",
    "CPU-hidden non-JIT debug/reference exception only",
    "not HMC convergence evidence",
    "not R-hat or ESS evidence",
    "not posterior correctness evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not LEDH evidence",
)
PHASE4_NONCLAIMS = (
    "Phase 4 short replicated debug ladder only",
    "CPU-hidden non-JIT debug/reference exception only",
    "not HMC convergence evidence",
    "not R-hat or ESS evidence",
    "not posterior correctness evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not LEDH evidence",
)
PHASE3_GPU_XLA_NONCLAIMS = (
    "Phase 3 trusted GPU/XLA launch smoke only",
    "not HMC convergence evidence",
    "not R-hat or ESS evidence",
    "not posterior correctness evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not LEDH evidence",
)
PHASE5_GPU_XLA_NONCLAIMS = (
    "Phase 5 longer trusted GPU/XLA hard-veto diagnostic ladder only",
    "not HMC convergence evidence",
    "not R-hat or ESS evidence",
    "not posterior correctness evidence",
    "not a method ranking or superiority claim",
    "not source-faithful SSL-LSTM Zhao-Cui parity evidence",
    "not GPU/XLA production-readiness evidence",
    "not default-readiness evidence",
    "not public API or package readiness evidence",
    "not LEDH evidence",
)
PHASE2_HMC_SEED = (20260706, 2201)
PHASE3_GPU_XLA_HMC_SEED = (20260706, 3301)
PHASE5_GPU_XLA_HMC_SEEDS = (
    (20260706, 5101),
    (20260706, 5102),
    (20260706, 5103),
)
PHASE4_HMC_SEEDS = (
    (20260706, 2401),
    (20260706, 2402),
    (20260706, 2403),
)
PHASE4_NUM_RESULTS = 2
PHASE4_NUM_BURNIN_STEPS = 1
PHASE4_STEP_SIZE = 1.0e-5
PHASE4_NUM_LEAPFROG_STEPS = 1
PHASE5_NUM_RESULTS = 8
PHASE5_NUM_BURNIN_STEPS = 4
PHASE5_STEP_SIZE = 1.0e-5
PHASE5_NUM_LEAPFROG_STEPS = 1
PHASE5_PRIOR_SCALE = 5.0
PHASE5_INITIAL_OFFSET_SCALE = 1.0e-3
PHASE4_QUIET_LOG_PATH = (
    "docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_ladder_2026-07-06/"
    "phase4_short_ladder_cpu_hidden_2026-07-06.log"
)
PHASE5_QUIET_LOG_PATH = (
    "docs/benchmarks/logs/minimal_ssl_lstm_zhaocui_hmc_next_2026-07-06/"
    "phase5_longer_gpu_xla_ladder_2026-07-06.log"
)

def initial_offset_state(offset_scale: float = 1.0e-3) -> tf.Tensor:
    """Return a deterministic near-center initial state for later HMC phases."""

    return initial_minimal_ssl_lstm_hmc_state(offset_scale)


def build_phase1_adapter_artifact(
    *,
    prior_scale: float = PHASE5_PRIOR_SCALE,
    initial_offset_scale: float = PHASE5_INITIAL_OFFSET_SCALE,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Evaluate deterministic value/score checks for the Phase 1 adapter."""

    adapter = MinimalZhaoCuiHMCTargetAdapter(
        prior_scale=prior_scale,
        evidence_path=PHASE1_SUBPLAN_PATH,
    )
    theta = initial_offset_state(initial_offset_scale)
    repeated_theta = tf.identity(theta)
    batch_theta = tf.stack([theta, repeated_theta], axis=0)

    start = time.perf_counter()
    value, score = adapter.log_prob_and_grad(theta)
    repeated_value, repeated_score = adapter.log_prob_and_grad(repeated_theta)
    batch_value, batch_score = adapter.log_prob_and_grad(batch_theta)
    runtime_s = time.perf_counter() - start

    capability = value_score_capability(adapter)
    signature = stable_adapter_signature(adapter)
    value_finite = bool(tf.reduce_all(tf.math.is_finite(value)).numpy())
    score_finite = bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    repeated_delta = tf.reduce_max(
        tf.abs(
            tf.concat(
                [
                    tf.reshape(value - repeated_value, [1]),
                    tf.reshape(score - repeated_score, [-1]),
                ],
                axis=0,
            )
        )
    )
    batch_value_delta = tf.reduce_max(tf.abs(batch_value - tf.stack([value, value])))
    batch_score_delta = tf.reduce_max(tf.abs(batch_score - tf.stack([score, score])))
    deterministic = bool(repeated_delta.numpy() <= 1.0e-12)
    batch_consistent = bool(max(float(batch_value_delta.numpy()), float(batch_score_delta.numpy())) <= 1.0e-12)
    fixture = _fixture_payload()
    hard_vetoes: list[str] = []
    if fixture["latent_dim"] != 1 or fixture["hidden_dim"] != 1:
        hard_vetoes.append("fixture_not_scalar")
    if fixture["observation_dim"] != 1 or fixture["horizon"] != 2:
        hard_vetoes.append("fixture_shape_mismatch")
    if fixture["parameter_dim"] != 24:
        hard_vetoes.append("parameter_dim_not_24")
    if tuple(score.shape.as_list()) != (24,):
        hard_vetoes.append("score_shape_mismatch")
    if tuple(batch_score.shape.as_list()) != (2, 24):
        hard_vetoes.append("batch_score_shape_mismatch")
    if not value_finite:
        hard_vetoes.append("target_value_nonfinite")
    if not score_finite:
        hard_vetoes.append("target_score_nonfinite")
    if not deterministic:
        hard_vetoes.append("target_nondeterministic")
    if not batch_consistent:
        hard_vetoes.append("batch_path_inconsistent")
    if capability.value_score_authority != "graph_native":
        hard_vetoes.append("value_score_authority_not_graph_native")
    artifact = {
        "schema_version": "minimal_ssl_lstm_zhaocui_hmc_ladder.phase1_adapter.v1",
        "status": "passed" if not hard_vetoes else "failed",
        "date": DATE_STAMP,
        "phase": "PHASE1",
        "artifact_role": "target_adapter_debug_reference",
        "filter_name": "zhaocui_fixed",
        "fixture": fixture,
        "evidence_contract": {
            "question": (
                "Can the scalar zhaocui_fixed value/score be wrapped as an "
                "internal BayesFilter HMC target adapter without changing the "
                "manual target score path?"
            ),
            "baseline_comparator": (
                "Completed minimal scalar smoke fixture and existing Phase 7 "
                "SSL-LSTM HMC adapter pattern."
            ),
            "primary_pass_criterion": (
                "Finite deterministic scalar log prob, gradient shape (24,), "
                "batch shape (2, 24), graph-native capability metadata, and no "
                "target-path autodiff/NumPy bridge."
            ),
            "veto_diagnostics": (
                "Nonfinite value/score, wrong shape, nondeterminism, invalid "
                "ValueScoreCapability, target-path autodiff/NumPy, public API "
                "change, or unsupported claim."
            ),
            "explanatory_diagnostics": (
                "Initial log prob, score norm, prior scale, offset scale, "
                "runtime, and metadata signature."
            ),
            "not_concluded": NONCLAIMS,
        },
        "target_diagnostics": {
            "log_prob": float(value.numpy()),
            "score_norm": float(tf.linalg.norm(score).numpy()),
            "score_min": float(tf.reduce_min(score).numpy()),
            "score_max": float(tf.reduce_max(score).numpy()),
            "score_shape": list(score.shape.as_list()),
            "value_shape": list(value.shape.as_list()),
            "batch_value_shape": list(batch_value.shape.as_list()),
            "batch_score_shape": list(batch_score.shape.as_list()),
            "value_finite": value_finite,
            "score_finite": score_finite,
            "determinism_max_abs_delta": float(repeated_delta.numpy()),
            "determinism_passed": deterministic,
            "batch_consistency_max_abs_delta": max(
                float(batch_value_delta.numpy()),
                float(batch_score_delta.numpy()),
            ),
            "batch_consistency_passed": batch_consistent,
            "prior_scale": float(prior_scale),
            "initial_offset_scale": float(initial_offset_scale),
            "runtime_s": float(runtime_s),
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
        "adapter_signature": signature,
        "zhaocui_fixed_manifest": _json_ready(adapter.manifest.as_dict()),
        "gradient_path": adapter._components.protocol.gradient_path,
        "value_score_authority": capability.value_score_authority,
        "run_manifest": {
            "git_commit": _git_commit(),
            "git_dirty_summary": _git_dirty_summary(),
            "command": list(command or (sys.executable, str(Path(__file__).resolve()))),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "cpu_gpu_status": _tf_device_summary(),
            "compile_mode": "eager",
            "jit_compile": False,
            "debug_reference_exception": (
                "CPU-hidden non-JIT Phase 1 adapter admission; not BayesFilter "
                "default GPU/XLA or default-readiness evidence."
            ),
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE1_SUBPLAN_PATH,
            "result_file": PHASE1_RESULT_PATH,
            "random_seeds": {
                "zhaocui_initial_seed": list(adapter.manifest.initial_seed),
                "zhaocui_process_seed": list(adapter.manifest.process_seed),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
        },
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "value_finite": "hard_veto_evidence",
            "score_finite": "hard_veto_evidence",
            "score_shape": "hard_veto_evidence",
            "determinism": "hard_veto_evidence",
            "batch_consistency": "hard_veto_evidence",
            "score_norm": "explanatory_only",
            "runtime": "explanatory_only",
        },
        "hard_vetoes": hard_vetoes,
        "nonclaims": NONCLAIMS,
    }
    return artifact


def build_phase2_canary_artifact(
    *,
    prior_scale: float = 5.0,
    initial_offset_scale: float = 1.0e-3,
    num_results: int = 2,
    num_burnin_steps: int = 1,
    step_size: float = 1.0e-5,
    num_leapfrog_steps: int = 1,
    seed: tuple[int, int] = PHASE2_HMC_SEED,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run the tiny CPU-hidden Phase 2 HMC canary."""

    adapter = MinimalZhaoCuiHMCTargetAdapter(
        prior_scale=prior_scale,
        evidence_path=PHASE2_SUBPLAN_PATH,
    )
    initial_state = initial_offset_state(initial_offset_scale)
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    capability = value_score_capability(adapter)
    hmc_config = FullChainHMCConfig(
        num_results=int(num_results),
        num_burnin_steps=int(num_burnin_steps),
        step_size=float(step_size),
        num_leapfrog_steps=int(num_leapfrog_steps),
        seed=tuple(int(item) for item in seed),
        use_xla=False,
        trace_policy="standard",
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope=adapter.target_scope,
        chain_execution_mode="tf_function",
    )
    hard_vetoes: list[str] = []
    error_message = None
    hmc_result = None
    initial_value_finite = bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy())
    initial_score_finite = bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy())
    if not initial_value_finite:
        hard_vetoes.append("initial_target_value_nonfinite")
    if not initial_score_finite:
        hard_vetoes.append("initial_target_score_nonfinite")
    start = time.perf_counter()
    try:
        hmc_result = run_full_chain_tfp_hmc(adapter, initial_state, hmc_config)
    except Exception as exc:  # noqa: BLE001
        error_message = f"{type(exc).__name__}: {exc}"
        hard_vetoes.append("hmc_runtime_exception")
    runtime_s = time.perf_counter() - start

    diagnostics: Mapping[str, Any] = {}
    metadata: Mapping[str, Any] = {}
    sample_shape: list[int] | None = None
    samples_all_finite = None
    if hmc_result is not None:
        diagnostics = dict(hmc_result.diagnostics)
        metadata = dict(hmc_result.metadata)
        samples = tf.convert_to_tensor(hmc_result.samples, dtype=tf.float64)
        sample_shape = [int(dim) for dim in samples.shape.as_list()]
        samples_all_finite = bool(tf.reduce_all(tf.math.is_finite(samples)).numpy())
        nonfinite_sample_count = diagnostics.get("nonfinite_sample_count")
        if nonfinite_sample_count is not None:
            if int(tf.convert_to_tensor(nonfinite_sample_count).numpy()) > 0:
                hard_vetoes.append("nonfinite_hmc_samples")
        if not samples_all_finite:
            hard_vetoes.append("nonfinite_hmc_samples")
        divergence_count = diagnostics.get("divergence_count")
        if divergence_count is not None:
            if int(tf.convert_to_tensor(divergence_count).numpy()) > 0:
                hard_vetoes.append("native_divergence_detected")

    status = "passed" if not hard_vetoes else "failed"
    artifact = {
        "schema_version": "minimal_ssl_lstm_zhaocui_hmc_ladder.phase2_canary.v1",
        "status": status,
        "date": DATE_STAMP,
        "phase": "PHASE2",
        "artifact_role": "tiny_hmc_canary_debug_reference",
        "filter_name": "zhaocui_fixed",
        "fixture": _fixture_payload(),
        "evidence_contract": {
            "question": (
                "Can the scalar zhaocui_fixed target run through BayesFilter "
                "run_full_chain_tfp_hmc without hard-veto failure in a tiny "
                "CPU-hidden non-JIT debug canary?"
            ),
            "baseline_comparator": (
                "Phase 1 adapter and existing run_full_chain_tfp_hmc "
                "launch-smoke pattern."
            ),
            "primary_pass_criterion": (
                "Finite initial value/score, no HMC runtime exception, no "
                "nonfinite samples, and a valid canary artifact."
            ),
            "veto_diagnostics": (
                "Nonfinite initial value/score, HMC runtime exception, "
                "nonfinite samples, invalid artifact, wrong fixture, "
                "unsupported claim, missing debug/reference exception label, "
                "or evidence-class mismatch."
            ),
            "explanatory_diagnostics": (
                "Acceptance rate, runtime, initial score norm, sample finite "
                "counts, and TensorFlow CUDA startup warnings under "
                "CPU-hidden execution."
            ),
            "not_concluded": PHASE2_NONCLAIMS,
        },
        "initial_target": {
            "log_prob": float(initial_value.numpy()),
            "score_norm": float(tf.linalg.norm(initial_score).numpy()),
            "value_finite": initial_value_finite,
            "score_finite": initial_score_finite,
            "score_shape": list(initial_score.shape.as_list()),
            "initial_offset_scale": float(initial_offset_scale),
        },
        "hmc_settings": {
            "num_results": int(num_results),
            "num_burnin_steps": int(num_burnin_steps),
            "step_size": float(step_size),
            "num_leapfrog_steps": int(num_leapfrog_steps),
            "seed": [int(item) for item in seed],
            "use_xla": False,
            "jit_compile": False,
            "chain_execution_mode": "tf_function",
            "trace_policy": "standard",
            "adaptation_policy": "fixed_kernel_no_adaptation",
            "target_scope": adapter.target_scope,
        },
        "hmc_runtime": {
            "runtime_s": float(runtime_s),
            "error": error_message,
            "sample_shape": sample_shape,
            "samples_all_finite": samples_all_finite,
            "diagnostics": _json_ready(diagnostics),
            "metadata": _json_ready(metadata),
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
            "cpu_gpu_status": _tf_device_summary(),
            "compile_mode": "tf_function",
            "jit_compile": False,
            "use_xla": False,
            "debug_reference_exception": (
                "CPU-hidden non-JIT Phase 2 HMC canary; not BayesFilter "
                "default GPU/XLA or default-readiness evidence."
            ),
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE2_SUBPLAN_PATH,
            "result_file": PHASE2_RESULT_PATH,
            "random_seeds": {
                "hmc_seed": [int(item) for item in seed],
                "zhaocui_initial_seed": list(adapter.manifest.initial_seed),
                "zhaocui_process_seed": list(adapter.manifest.process_seed),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
        },
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "initial_value_finite": "hard_veto_evidence",
            "initial_score_finite": "hard_veto_evidence",
            "hmc_runtime_exception": "hard_veto_evidence",
            "nonfinite_sample_count": "hard_veto_evidence",
            "native_divergence_count": "hard_veto_evidence_when_available",
            "acceptance_rate": "explanatory_only_in_tiny_canary",
            "runtime": "explanatory_only",
            "rhat": "not_computed_in_tiny_canary",
            "ess": "not_computed_in_tiny_canary",
        },
        "hard_vetoes": list(dict.fromkeys(hard_vetoes)),
        "nonclaims": PHASE2_NONCLAIMS,
    }
    return artifact


def build_phase3_gpu_xla_smoke_artifact(
    *,
    trusted_gpu_xla_approval: bool,
    prior_scale: float = 5.0,
    initial_offset_scale: float = 1.0e-3,
    num_results: int = 2,
    num_burnin_steps: int = 1,
    step_size: float = 1.0e-5,
    num_leapfrog_steps: int = 1,
    seed: tuple[int, int] = PHASE3_GPU_XLA_HMC_SEED,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run or fail-close the trusted GPU/XLA Phase 3 launch smoke."""

    adapter = MinimalZhaoCuiHMCTargetAdapter(
        prior_scale=prior_scale,
        evidence_path=PHASE3_GPU_XLA_SUBPLAN_PATH,
    )
    initial_state = initial_offset_state(initial_offset_scale)
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    capability = value_score_capability(adapter)
    device_summary = _tf_device_summary(
        trust_basis="explicit_user_approved_trusted_gpu_xla_hmc_runtime"
    )
    hmc_config = FullChainHMCConfig(
        num_results=int(num_results),
        num_burnin_steps=int(num_burnin_steps),
        step_size=float(step_size),
        num_leapfrog_steps=int(num_leapfrog_steps),
        seed=tuple(int(item) for item in seed),
        use_xla=True,
        trace_policy="standard",
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope=adapter.target_scope,
        chain_execution_mode="tf_function",
    )
    hard_vetoes: list[str] = []
    error_message = None
    hmc_result = None
    initial_value_finite = bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy())
    initial_score_finite = bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy())
    if not bool(trusted_gpu_xla_approval):
        hard_vetoes.append("missing_trusted_gpu_xla_approval")
    if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
        hard_vetoes.append("gpu_hidden_for_trusted_gpu_xla_smoke")
    if not device_summary["gpu_devices"]:
        hard_vetoes.append("gpu_device_not_visible")
    if not initial_value_finite:
        hard_vetoes.append("initial_target_value_nonfinite")
    if not initial_score_finite:
        hard_vetoes.append("initial_target_score_nonfinite")

    diagnostics: Mapping[str, Any] = {}
    metadata: Mapping[str, Any] = {}
    sample_shape: list[int] | None = None
    samples_all_finite = None
    runtime_s = 0.0
    not_run_reason = None
    if hard_vetoes:
        not_run_reason = "preflight_hard_veto"
    else:
        start = time.perf_counter()
        try:
            hmc_result = run_full_chain_tfp_hmc(adapter, initial_state, hmc_config)
        except Exception as exc:  # noqa: BLE001
            error_message = f"{type(exc).__name__}: {exc}"
            hard_vetoes.append("hmc_runtime_exception")
        runtime_s = time.perf_counter() - start

    if hmc_result is not None:
        diagnostics = dict(hmc_result.diagnostics)
        metadata = dict(hmc_result.metadata)
        samples = tf.convert_to_tensor(hmc_result.samples, dtype=tf.float64)
        sample_shape = [int(dim) for dim in samples.shape.as_list()]
        samples_all_finite = bool(tf.reduce_all(tf.math.is_finite(samples)).numpy())
        nonfinite_sample_count = diagnostics.get("nonfinite_sample_count")
        if nonfinite_sample_count is not None:
            if int(tf.convert_to_tensor(nonfinite_sample_count).numpy()) > 0:
                hard_vetoes.append("nonfinite_hmc_samples")
        if not samples_all_finite:
            hard_vetoes.append("nonfinite_hmc_samples")
        divergence_count = diagnostics.get("divergence_count")
        if divergence_count is not None:
            if int(tf.convert_to_tensor(divergence_count).numpy()) > 0:
                hard_vetoes.append("native_divergence_detected")

    status = "passed" if not hard_vetoes else "failed"
    return {
        "schema_version": "minimal_ssl_lstm_zhaocui_hmc_next.phase3_gpu_xla_smoke.v1",
        "status": status,
        "date": DATE_STAMP,
        "phase": "PHASE3",
        "artifact_role": "trusted_gpu_xla_runtime_smoke",
        "filter_name": "zhaocui_fixed",
        "fixture": _fixture_payload(),
        "evidence_contract": {
            "question": (
                "Can the extracted scalar zhaocui_fixed target launch through "
                "the trusted GPU/XLA HMC runtime path without hard-veto failure?"
            ),
            "baseline_comparator": (
                "Phase 2 CPU-hidden regression and predecessor CPU-hidden ladder."
            ),
            "primary_pass_criterion": (
                "Explicit approval, visible GPU provenance, use_xla=True, "
                "jit_compile=True, no runtime exception, finite samples, and "
                "a valid smoke artifact."
            ),
            "veto_diagnostics": (
                "Missing approval, hidden/missing GPU, CUDA/XLA runtime exception, "
                "nonfinite target/sample, invalid artifact, or unsupported claim."
            ),
            "explanatory_diagnostics": (
                "Acceptance rate, runtime, device names, TF32 setting, and "
                "TensorFlow CUDA/XLA warnings."
            ),
            "not_concluded": PHASE3_GPU_XLA_NONCLAIMS,
        },
        "initial_target": {
            "log_prob": float(initial_value.numpy()),
            "score_norm": float(tf.linalg.norm(initial_score).numpy()),
            "value_finite": initial_value_finite,
            "score_finite": initial_score_finite,
            "score_shape": list(initial_score.shape.as_list()),
            "initial_offset_scale": float(initial_offset_scale),
        },
        "hmc_settings": {
            "num_results": int(num_results),
            "num_burnin_steps": int(num_burnin_steps),
            "step_size": float(step_size),
            "num_leapfrog_steps": int(num_leapfrog_steps),
            "seed": [int(item) for item in seed],
            "use_xla": True,
            "jit_compile": True,
            "chain_execution_mode": "tf_function",
            "trace_policy": "standard",
            "adaptation_policy": "fixed_kernel_no_adaptation",
            "target_scope": adapter.target_scope,
            "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
        },
        "hmc_runtime": {
            "runtime_s": float(runtime_s),
            "error": error_message,
            "not_run_reason": not_run_reason,
            "sample_shape": sample_shape,
            "samples_all_finite": samples_all_finite,
            "diagnostics": _json_ready(diagnostics),
            "metadata": _json_ready(metadata),
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
            "cpu_gpu_status": device_summary,
            "compile_mode": "tf_function",
            "jit_compile": True,
            "use_xla": True,
            "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
            "trust_basis": "explicit_user_approved_trusted_gpu_xla_hmc_runtime",
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE3_GPU_XLA_SUBPLAN_PATH,
            "result_file": PHASE3_GPU_XLA_RESULT_PATH,
            "random_seeds": {
                "hmc_seed": [int(item) for item in seed],
                "zhaocui_initial_seed": list(adapter.manifest.initial_seed),
                "zhaocui_process_seed": list(adapter.manifest.process_seed),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
        },
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "trusted_gpu_xla_approval": "hard_veto_evidence",
            "gpu_devices": "hard_veto_evidence",
            "initial_value_finite": "hard_veto_evidence",
            "initial_score_finite": "hard_veto_evidence",
            "hmc_runtime_exception": "hard_veto_evidence",
            "nonfinite_sample_count": "hard_veto_evidence",
            "native_divergence_count": "hard_veto_evidence_when_available",
            "acceptance_rate": "explanatory_only_in_launch_smoke",
            "runtime": "explanatory_only",
            "rhat": "not_computed_in_launch_smoke",
            "ess": "not_computed_in_launch_smoke",
        },
        "hard_vetoes": list(dict.fromkeys(hard_vetoes)),
        "nonclaims": PHASE3_GPU_XLA_NONCLAIMS,
    }


def build_phase5_longer_gpu_xla_ladder_artifact(
    *,
    trusted_gpu_xla_approval: bool,
    prior_scale: float = 5.0,
    initial_offset_scale: float = 1.0e-3,
    num_results: int = PHASE5_NUM_RESULTS,
    num_burnin_steps: int = PHASE5_NUM_BURNIN_STEPS,
    step_size: float = PHASE5_STEP_SIZE,
    num_leapfrog_steps: int = PHASE5_NUM_LEAPFROG_STEPS,
    seeds: tuple[tuple[int, int], ...] = PHASE5_GPU_XLA_HMC_SEEDS,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run the reviewed longer trusted GPU/XLA hard-veto diagnostic ladder."""

    if not math.isclose(float(prior_scale), PHASE5_PRIOR_SCALE, rel_tol=0.0, abs_tol=0.0):
        raise ValueError("Phase 5 prior_scale is fixed by the reviewed subplan")
    if not math.isclose(
        float(initial_offset_scale),
        PHASE5_INITIAL_OFFSET_SCALE,
        rel_tol=0.0,
        abs_tol=0.0,
    ):
        raise ValueError(
            "Phase 5 initial_offset_scale is fixed by the reviewed subplan"
        )
    if int(num_results) != PHASE5_NUM_RESULTS:
        raise ValueError("Phase 5 num_results is fixed by the reviewed subplan")
    if int(num_burnin_steps) != PHASE5_NUM_BURNIN_STEPS:
        raise ValueError("Phase 5 num_burnin_steps is fixed by the reviewed subplan")
    if int(num_leapfrog_steps) != PHASE5_NUM_LEAPFROG_STEPS:
        raise ValueError("Phase 5 num_leapfrog_steps is fixed by the reviewed subplan")
    if not math.isclose(float(step_size), PHASE5_STEP_SIZE, rel_tol=0.0, abs_tol=0.0):
        raise ValueError("Phase 5 step_size is fixed by the reviewed subplan")
    normalized_seeds = tuple(tuple(int(item) for item in seed) for seed in seeds)
    if normalized_seeds != PHASE5_GPU_XLA_HMC_SEEDS:
        raise ValueError("Phase 5 ladder seeds are fixed by the reviewed subplan")

    adapter = MinimalZhaoCuiHMCTargetAdapter(
        prior_scale=prior_scale,
        evidence_path=PHASE5_LONGER_DIAGNOSTICS_SUBPLAN_PATH,
    )
    initial_state = initial_offset_state(initial_offset_scale)
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    capability = value_score_capability(adapter)
    device_summary = _tf_device_summary(
        trust_basis="explicit_user_approved_trusted_gpu_xla_longer_diagnostics"
    )

    hard_vetoes: list[str] = []
    initial_value_finite = bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy())
    initial_score_finite = bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy())
    if not bool(trusted_gpu_xla_approval):
        hard_vetoes.append("missing_trusted_gpu_xla_approval")
    if os.environ.get("CUDA_VISIBLE_DEVICES") == "-1":
        hard_vetoes.append("gpu_hidden_for_trusted_gpu_xla_ladder")
    if not device_summary["gpu_devices"]:
        hard_vetoes.append("gpu_device_not_visible")
    if not initial_value_finite:
        hard_vetoes.append("initial_target_value_nonfinite")
    if not initial_score_finite:
        hard_vetoes.append("initial_target_score_nonfinite")

    preflight_hard_vetoes = list(dict.fromkeys(hard_vetoes))
    rows: list[dict[str, Any]] = []
    start = time.perf_counter()
    for seed in normalized_seeds:
        row_hard_vetoes = list(preflight_hard_vetoes)
        diagnostics: Mapping[str, Any] = {}
        metadata: Mapping[str, Any] = {}
        sample_shape: list[int] | None = None
        samples_all_finite = None
        sample_summary: Mapping[str, Any] = {}
        error_message = None
        not_run_reason = None
        runtime_s = 0.0
        if row_hard_vetoes:
            not_run_reason = "preflight_hard_veto"
        else:
            hmc_config = FullChainHMCConfig(
                num_results=PHASE5_NUM_RESULTS,
                num_burnin_steps=PHASE5_NUM_BURNIN_STEPS,
                step_size=PHASE5_STEP_SIZE,
                num_leapfrog_steps=PHASE5_NUM_LEAPFROG_STEPS,
                seed=tuple(int(item) for item in seed),
                use_xla=True,
                trace_policy="standard",
                adaptation_policy="fixed_kernel_no_adaptation",
                target_scope=adapter.target_scope,
                chain_execution_mode="tf_function",
            )
            row_start = time.perf_counter()
            try:
                hmc_result = run_full_chain_tfp_hmc(adapter, initial_state, hmc_config)
            except Exception as exc:  # noqa: BLE001
                error_message = f"{type(exc).__name__}: {exc}"
                row_hard_vetoes.append("hmc_runtime_exception")
            else:
                diagnostics = dict(hmc_result.diagnostics)
                metadata = dict(hmc_result.metadata)
                samples = tf.convert_to_tensor(hmc_result.samples, dtype=tf.float64)
                sample_shape = [int(dim) for dim in samples.shape.as_list()]
                samples_all_finite = bool(tf.reduce_all(tf.math.is_finite(samples)).numpy())
                if samples_all_finite:
                    sample_summary = {
                        "mean": float(tf.reduce_mean(samples).numpy()),
                        "std": float(tf.math.reduce_std(samples).numpy()),
                        "min": float(tf.reduce_min(samples).numpy()),
                        "max": float(tf.reduce_max(samples).numpy()),
                    }
                else:
                    sample_summary = {
                        "mean": None,
                        "std": None,
                        "min": None,
                        "max": None,
                    }
                nonfinite_sample_count = diagnostics.get("nonfinite_sample_count")
                if nonfinite_sample_count is not None:
                    if int(tf.convert_to_tensor(nonfinite_sample_count).numpy()) > 0:
                        row_hard_vetoes.append("nonfinite_hmc_samples")
                if not samples_all_finite:
                    row_hard_vetoes.append("nonfinite_hmc_samples")
                divergence_count = diagnostics.get("divergence_count")
                if divergence_count is not None:
                    if int(tf.convert_to_tensor(divergence_count).numpy()) > 0:
                        row_hard_vetoes.append("native_divergence_detected")
            runtime_s = time.perf_counter() - row_start
        rows.append(
            {
                "seed": [int(item) for item in seed],
                "status": "passed" if not row_hard_vetoes else "failed",
                "hard_vetoes": list(dict.fromkeys(row_hard_vetoes)),
                "not_run_reason": not_run_reason,
                "initial_target": {
                    "log_prob": float(initial_value.numpy()),
                    "score_norm": float(tf.linalg.norm(initial_score).numpy()),
                    "value_finite": initial_value_finite,
                    "score_finite": initial_score_finite,
                    "score_shape": list(initial_score.shape.as_list()),
                    "initial_offset_scale": float(initial_offset_scale),
                },
                "hmc_settings": {
                    "num_results": PHASE5_NUM_RESULTS,
                    "num_burnin_steps": PHASE5_NUM_BURNIN_STEPS,
                    "step_size": PHASE5_STEP_SIZE,
                    "num_leapfrog_steps": PHASE5_NUM_LEAPFROG_STEPS,
                    "seed": [int(item) for item in seed],
                    "use_xla": True,
                    "jit_compile": True,
                    "chain_execution_mode": "tf_function",
                    "trace_policy": "standard",
                    "adaptation_policy": "fixed_kernel_no_adaptation",
                    "target_scope": adapter.target_scope,
                    "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
                },
                "hmc_runtime": {
                    "runtime_s": float(runtime_s),
                    "error": error_message,
                    "sample_shape": sample_shape,
                    "samples_all_finite": samples_all_finite,
                    "sample_summary": _json_ready(sample_summary),
                    "diagnostics": _json_ready(diagnostics),
                    "metadata": _json_ready(metadata),
                },
                "adapter_signature": stable_adapter_signature(adapter),
            }
        )

    total_runtime_s = time.perf_counter() - start
    row_hard_vetoes = [
        veto for row in rows for veto in list(row["hard_vetoes"])
    ]
    hard_vetoes = list(dict.fromkeys(row_hard_vetoes))
    all_passed = all(row["status"] == "passed" and not row["hard_vetoes"] for row in rows)
    divergence_statuses = sorted(
        {
            str(row["hmc_runtime"]["diagnostics"].get("divergence_status"))
            for row in rows
            if row["hmc_runtime"]["diagnostics"].get("divergence_status") is not None
        }
    )
    return {
        "schema_version": (
            "minimal_ssl_lstm_zhaocui_hmc_next."
            "phase5_longer_gpu_xla_ladder.v1"
        ),
        "status": "passed" if all_passed else "failed",
        "date": DATE_STAMP,
        "phase": "PHASE5",
        "artifact_role": "trusted_gpu_xla_longer_hard_veto_diagnostics",
        "filter_name": "zhaocui_fixed",
        "fixture": _fixture_payload(),
        "evidence_contract": {
            "question": (
                "Does the minimally longer trusted GPU/XLA ladder avoid hard "
                "runtime/sampler vetoes under fixed settings?"
            ),
            "baseline_comparator": (
                "Phase 3 trusted GPU/XLA smoke, Phase 2 CPU regression only "
                "as non-GPU debug context, and the Phase 4 reviewed design."
            ),
            "primary_pass_criterion": (
                "All three predeclared seeds complete with GPU provenance, "
                "use_xla=True, jit_compile=True, finite samples, and no hard vetoes."
            ),
            "veto_diagnostics": (
                "Runtime exception, hidden/missing GPU, missing approval, "
                "nonfinite target/sample, invalid artifact, missing provenance, "
                "positive native divergence if exposed, post-hoc criterion change, "
                "or unsupported claim."
            ),
            "explanatory_diagnostics": (
                "Acceptance, runtime, sample shape, sample finite counts, "
                "sample summaries, per-seed rows, TensorFlow logs, and native "
                "divergence availability status when not positive. ESS/R-hat "
                "are not computed."
            ),
            "not_concluded": PHASE5_GPU_XLA_NONCLAIMS,
        },
        "initial_target": {
            "log_prob": float(initial_value.numpy()),
            "score_norm": float(tf.linalg.norm(initial_score).numpy()),
            "value_finite": initial_value_finite,
            "score_finite": initial_score_finite,
            "score_shape": list(initial_score.shape.as_list()),
            "initial_offset_scale": float(initial_offset_scale),
        },
        "predeclared_settings": {
            "prior_scale": PHASE5_PRIOR_SCALE,
            "initial_offset_scale": PHASE5_INITIAL_OFFSET_SCALE,
            "num_results": PHASE5_NUM_RESULTS,
            "num_burnin_steps": PHASE5_NUM_BURNIN_STEPS,
            "step_size": PHASE5_STEP_SIZE,
            "num_leapfrog_steps": PHASE5_NUM_LEAPFROG_STEPS,
            "seeds": [[int(item) for item in seed] for seed in normalized_seeds],
            "use_xla": True,
            "jit_compile": True,
            "chain_execution_mode": "tf_function",
            "trace_policy": "standard",
            "adaptation_policy": "fixed_kernel_no_adaptation",
            "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
        },
        "candidate_rows": rows,
        "hard_veto_summary": {
            str(tuple(row["seed"])): row["hard_vetoes"] for row in rows
        },
        "all_predeclared_seeds_passed": bool(all_passed),
        "native_divergence_statuses": divergence_statuses,
        "native_divergence_interpretation": (
            "native divergence status 'not_exposed_by_kernel' is telemetry "
            "unavailability, not zero divergences"
        ),
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
            "cpu_gpu_status": device_summary,
            "compile_mode": "tf_function",
            "jit_compile": True,
            "use_xla": True,
            "trusted_gpu_xla_approval": bool(trusted_gpu_xla_approval),
            "trust_basis": "explicit_user_approved_trusted_gpu_xla_longer_diagnostics",
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "plan_file": "docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md",
            "subplan_file": PHASE5_LONGER_DIAGNOSTICS_SUBPLAN_PATH,
            "result_file": PHASE5_LONGER_DIAGNOSTICS_RESULT_PATH,
            "quiet_log_path": PHASE5_QUIET_LOG_PATH,
            "random_seeds": {
                "hmc_seeds": [[int(item) for item in seed] for seed in normalized_seeds],
                "zhaocui_initial_seed": list(adapter.manifest.initial_seed),
                "zhaocui_process_seed": list(adapter.manifest.process_seed),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
            "runtime_s": float(total_runtime_s),
        },
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "all_predeclared_seeds_passed": "primary_hard_veto_screen",
            "trusted_gpu_xla_approval": "hard_veto_evidence",
            "gpu_devices": "hard_veto_evidence",
            "initial_value_finite": "hard_veto_evidence",
            "initial_score_finite": "hard_veto_evidence",
            "hmc_runtime_exception": "hard_veto_evidence",
            "nonfinite_sample_count": "hard_veto_evidence",
            "native_divergence_count": "hard_veto_when_available_and_positive",
            "native_divergence_status": "telemetry_availability_not_zero_divergences",
            "acceptance_rate": "explanatory_only_in_longer_ladder",
            "runtime": "explanatory_only",
            "sample_summary": "explanatory_only",
            "rhat": "not_computed_in_longer_ladder",
            "ess": "not_computed_in_longer_ladder",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if all_passed else "failed",
            "statistically_supported_ranking": "not_claimed",
            "descriptive_only_differences": (
                "Acceptance, runtime, and sample summaries are descriptive only."
            ),
            "convergence": "not_checked",
            "default_readiness": "not_checked",
            "native_divergence_telemetry": (
                ", ".join(divergence_statuses) if divergence_statuses else "not_collected"
            ),
            "next_evidence_needed": (
                "Longer chains, convergence diagnostics, posterior/reference "
                "checks, and uncertainty-aware replication before convergence, "
                "ranking, or readiness claims."
            ),
        },
        "decision_table": {
            "decision": "longer GPU/XLA hard-veto diagnostic only",
            "primary_criterion_status": "passed" if all_passed else "failed",
            "veto_diagnostic_status": (
                "no hard veto for predeclared seeds"
                if all_passed
                else "hard veto recorded for at least one seed"
            ),
            "main_uncertainty": (
                "Modest fixed-kernel ladder cannot assess convergence, posterior "
                "correctness, ranking, default readiness, or production readiness."
            ),
            "next_justified_action": "write Phase 5 result and close out Phase 6",
            "what_is_not_being_concluded": (
                "No HMC convergence, posterior correctness, R-hat/ESS, ranking, "
                "default readiness, production readiness, source-faithful parity, "
                "public API/package readiness, or LEDH result."
            ),
        },
        "post_run_red_team": {
            "strongest_alternative_explanation": (
                "A no-hard-veto result may reflect the tiny scalar target and "
                "conservative step size, not robust sampler behavior."
            ),
            "result_that_would_overturn": (
                "Any reproduced runtime exception, nonfinite sample, invalid "
                "artifact, missing provenance, or positive native divergence "
                "under the reviewed settings."
            ),
            "weakest_part_of_evidence": (
                "No ESS/R-hat, no posterior/reference comparison, no adaptation "
                "assessment, and only three short seeds."
            ),
        },
        "hard_vetoes": hard_vetoes,
        "nonclaims": PHASE5_GPU_XLA_NONCLAIMS,
    }


def build_phase4_short_ladder_artifact(
    *,
    prior_scale: float = 5.0,
    initial_offset_scale: float = 1.0e-3,
    num_results: int = PHASE4_NUM_RESULTS,
    num_burnin_steps: int = PHASE4_NUM_BURNIN_STEPS,
    step_size: float = PHASE4_STEP_SIZE,
    num_leapfrog_steps: int = PHASE4_NUM_LEAPFROG_STEPS,
    seeds: tuple[tuple[int, int], ...] = PHASE4_HMC_SEEDS,
    command: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Run a predeclared short CPU-hidden debug ladder over fixed seeds."""

    if int(num_results) != PHASE4_NUM_RESULTS:
        raise ValueError("Phase 4 num_results is fixed by the reviewed subplan")
    if int(num_burnin_steps) != PHASE4_NUM_BURNIN_STEPS:
        raise ValueError("Phase 4 num_burnin_steps is fixed by the reviewed subplan")
    if int(num_leapfrog_steps) != PHASE4_NUM_LEAPFROG_STEPS:
        raise ValueError("Phase 4 num_leapfrog_steps is fixed by the reviewed subplan")
    if not math.isclose(float(step_size), PHASE4_STEP_SIZE, rel_tol=0.0, abs_tol=0.0):
        raise ValueError("Phase 4 step_size is fixed by the reviewed subplan")
    normalized_seeds = tuple(tuple(int(item) for item in seed) for seed in seeds)
    if normalized_seeds != PHASE4_HMC_SEEDS:
        raise ValueError("Phase 4 ladder seeds are fixed by the reviewed subplan")

    rows = []
    start = time.perf_counter()
    for seed in normalized_seeds:
        row = build_phase2_canary_artifact(
            prior_scale=prior_scale,
            initial_offset_scale=initial_offset_scale,
            num_results=num_results,
            num_burnin_steps=num_burnin_steps,
            step_size=step_size,
            num_leapfrog_steps=num_leapfrog_steps,
            seed=tuple(int(item) for item in seed),
            command=command,
        )
        rows.append(
            {
                "seed": [int(item) for item in seed],
                "status": row["status"],
                "hard_vetoes": row["hard_vetoes"],
                "initial_target": row["initial_target"],
                "hmc_settings": row["hmc_settings"],
                "hmc_runtime": row["hmc_runtime"],
                "adapter_signature": row["adapter_signature"],
            }
        )
    runtime_s = time.perf_counter() - start
    all_passed = all(row["status"] == "passed" and not row["hard_vetoes"] for row in rows)
    return {
        "schema_version": "minimal_ssl_lstm_zhaocui_hmc_ladder.phase4_short_ladder.v1",
        "status": "passed" if all_passed else "failed",
        "date": DATE_STAMP,
        "phase": "PHASE4",
        "artifact_role": "short_replicated_debug_ladder",
        "filter_name": "zhaocui_fixed",
        "fixture": _fixture_payload(),
        "evidence_contract": {
            "question": (
                "Do several tiny CPU-hidden HMC canaries avoid hard vetoes "
                "under fixed predeclared settings?"
            ),
            "baseline_comparator": (
                "Phase 2/3 canary plus identical scalar target across fixed seeds."
            ),
            "primary_pass_criterion": (
                "All predeclared seeds complete without hard vetoes and the "
                "artifact preserves debug-only evidence limits."
            ),
            "veto_diagnostics": (
                "Runtime exception, nonfinite sample, native divergence if "
                "exposed and positive, invalid artifact, missing seed, changed "
                "settings after seeing results, or unsupported claim."
            ),
            "explanatory_diagnostics": (
                "Acceptance rate, runtime, finite counts, and per-seed hard-veto rows."
            ),
            "not_concluded": PHASE4_NONCLAIMS,
        },
        "predeclared_settings": {
            "num_results": PHASE4_NUM_RESULTS,
            "num_burnin_steps": PHASE4_NUM_BURNIN_STEPS,
            "step_size": PHASE4_STEP_SIZE,
            "num_leapfrog_steps": PHASE4_NUM_LEAPFROG_STEPS,
            "seeds": [[int(item) for item in seed] for seed in normalized_seeds],
            "use_xla": False,
            "jit_compile": False,
            "chain_execution_mode": "tf_function",
            "trace_policy": "standard",
            "adaptation_policy": "fixed_kernel_no_adaptation",
        },
        "candidate_rows": rows,
        "hard_veto_summary": {
            str(tuple(row["seed"])): row["hard_vetoes"] for row in rows
        },
        "all_predeclared_seeds_passed": bool(all_passed),
        "run_manifest": {
            "git_commit": _git_commit(),
            "git_dirty_summary": _git_dirty_summary(),
            "command": list(command or (sys.executable, str(Path(__file__).resolve()))),
            "python": sys.version,
            "platform": platform.platform(),
            "tensorflow_version": tf.__version__,
            "cpu_gpu_status": _tf_device_summary(),
            "compile_mode": "tf_function",
            "jit_compile": False,
            "use_xla": False,
            "debug_reference_exception": (
                "CPU-hidden non-JIT Phase 4 short debug ladder; not BayesFilter "
                "default GPU/XLA, convergence, ranking, or default-readiness evidence."
            ),
            "tf32_enabled": bool(tf.config.experimental.tensor_float_32_execution_enabled()),
            "plan_file": MASTER_PROGRAM_PATH,
            "subplan_file": PHASE4_SUBPLAN_PATH,
            "result_file": PHASE4_RESULT_PATH,
            "quiet_log_path": PHASE4_QUIET_LOG_PATH,
            "random_seeds": {
                "hmc_seeds": [[int(item) for item in seed] for seed in normalized_seeds],
                "zhaocui_initial_seed": list(
                    minimal_ssl_lstm_zhaocui_manifest().initial_seed
                ),
                "zhaocui_process_seed": list(
                    minimal_ssl_lstm_zhaocui_manifest().process_seed
                ),
            },
            "data_version": "frozen_inline_scalar_fixture_2026-07-06",
            "runtime_s": float(runtime_s),
        },
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "all_predeclared_seeds_passed": "primary_hard_veto_screen",
            "acceptance_rate": "explanatory_only_in_short_debug_ladder",
            "runtime": "explanatory_only",
            "rhat": "not_computed_in_short_debug_ladder",
            "ess": "not_computed_in_short_debug_ladder",
        },
        "inference_status": {
            "hard_veto_screen": "passed" if all_passed else "failed",
            "statistically_supported_ranking": "not_claimed",
            "descriptive_only_differences": (
                "Per-seed acceptance/runtime differences are descriptive only."
            ),
            "default_readiness": "not_checked",
            "next_evidence_needed": (
                "Longer reviewed sampler diagnostics before any convergence, "
                "posterior, ranking, or default-readiness claim."
            ),
        },
        "decision_table": {
            "decision": "short debug ladder hard-veto classification only",
            "primary_criterion_status": "passed" if all_passed else "failed",
            "veto_diagnostic_status": (
                "no hard veto for predeclared seeds"
                if all_passed
                else "hard veto recorded for at least one seed"
            ),
            "main_uncertainty": (
                "tiny seed ladder cannot assess convergence, posterior "
                "correctness, ranking, or default readiness"
            ),
            "next_justified_action": "write Phase 4 result and review Phase 5 boundary",
            "what_is_not_being_concluded": (
                "No HMC convergence, posterior correctness, R-hat/ESS, ranking, "
                "GPU/XLA readiness, default readiness, source-faithful parity, or LEDH result."
            ),
        },
        "hard_vetoes": [] if all_passed else ["phase4_seed_hard_veto"],
        "nonclaims": PHASE4_NONCLAIMS,
    }


def write_markdown(path: Path, artifact: Mapping[str, Any]) -> None:
    """Write a compact Phase 1 adapter-admission summary."""

    diagnostics = artifact["target_diagnostics"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 1",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- Log prob: `{diagnostics['log_prob']}`",
        f"- Score norm: `{diagnostics['score_norm']}`",
        f"- Score shape: `{diagnostics['score_shape']}`",
        f"- Batch score shape: `{diagnostics['batch_score_shape']}`",
        f"- Determinism passed: `{diagnostics['determinism_passed']}`",
        f"- Batch consistency passed: `{diagnostics['batch_consistency_passed']}`",
        f"- Value/score authority: `{artifact['value_score_authority']}`",
        f"- Adapter signature: `{artifact['adapter_signature']}`",
        "",
        "## Hard Vetoes",
        "",
    ]
    vetoes = list(artifact["hard_vetoes"])
    lines.extend(f"- {item}" for item in vetoes) if vetoes else lines.append("- none")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE1_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE1_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_canary_markdown(path: Path, artifact: Mapping[str, Any]) -> None:
    """Write a compact Phase 2 HMC canary summary."""

    initial = artifact["initial_target"]
    hmc_runtime = artifact["hmc_runtime"]
    diagnostics = hmc_runtime["diagnostics"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 2 Canary",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- Initial log prob: `{initial['log_prob']}`",
        f"- Initial score norm: `{initial['score_norm']}`",
        f"- Initial score shape: `{initial['score_shape']}`",
        f"- HMC error: `{hmc_runtime['error']}`",
        f"- Sample shape: `{hmc_runtime['sample_shape']}`",
        f"- Samples all finite: `{hmc_runtime['samples_all_finite']}`",
        f"- Acceptance rate: `{diagnostics.get('acceptance_rate')}`",
        f"- Nonfinite sample count: `{diagnostics.get('nonfinite_sample_count')}`",
        f"- Divergence status: `{diagnostics.get('divergence_status')}`",
        f"- Divergence count: `{diagnostics.get('divergence_count')}`",
        "",
        "## HMC Settings",
        "",
    ]
    for key, value in artifact["hmc_settings"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Hard Vetoes", ""])
    vetoes = list(artifact["hard_vetoes"])
    lines.extend(f"- {item}" for item in vetoes) if vetoes else lines.append("- none")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE2_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE2_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_ladder_markdown(path: Path, artifact: Mapping[str, Any]) -> None:
    """Write a compact Phase 4 short-ladder summary."""

    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 4 Short Ladder",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- All predeclared seeds passed: `{artifact['all_predeclared_seeds_passed']}`",
        "",
        "## Candidate Rows",
        "",
        "| seed | status | hard vetoes | acceptance rate | nonfinite samples | sample shape |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in artifact["candidate_rows"]:
        diagnostics = row["hmc_runtime"]["diagnostics"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["seed"]),
                    str(row["status"]),
                    ", ".join(row["hard_vetoes"]) or "none",
                    str(diagnostics.get("acceptance_rate")),
                    str(diagnostics.get("nonfinite_sample_count")),
                    str(row["hmc_runtime"].get("sample_shape")),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Decision Table", "", "| field | value |", "| --- | --- |"])
    for key, value in artifact["decision_table"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Inference Status", "", "| field | value |", "| --- | --- |"])
    for key, value in artifact["inference_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE4_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE4_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_gpu_xla_smoke_markdown(path: Path, artifact: Mapping[str, Any]) -> None:
    """Write a compact Phase 3 GPU/XLA launch-smoke summary."""

    initial = artifact["initial_target"]
    hmc_runtime = artifact["hmc_runtime"]
    diagnostics = hmc_runtime["diagnostics"]
    device_summary = artifact["run_manifest"]["cpu_gpu_status"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Next Phase 3 GPU/XLA Smoke",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- Trusted approval recorded: `{artifact['hmc_settings']['trusted_gpu_xla_approval']}`",
        f"- CUDA_VISIBLE_DEVICES: `{device_summary.get('cuda_visible_devices')}`",
        f"- GPU devices: `{device_summary.get('gpu_devices')}`",
        f"- Initial log prob: `{initial['log_prob']}`",
        f"- Initial score norm: `{initial['score_norm']}`",
        f"- HMC error: `{hmc_runtime['error']}`",
        f"- Not-run reason: `{hmc_runtime['not_run_reason']}`",
        f"- Sample shape: `{hmc_runtime['sample_shape']}`",
        f"- Samples all finite: `{hmc_runtime['samples_all_finite']}`",
        f"- Acceptance rate: `{diagnostics.get('acceptance_rate')}`",
        "",
        "## HMC Settings",
        "",
    ]
    for key, value in artifact["hmc_settings"].items():
        lines.append(f"- {key}: `{value}`")
    lines.extend(["", "## Hard Vetoes", ""])
    vetoes = list(artifact["hard_vetoes"])
    lines.extend(f"- {item}" for item in vetoes) if vetoes else lines.append("- none")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(f"- Plan: `{MASTER_PROGRAM_PATH}`")
    lines.append(f"- Subplan: `{PHASE3_GPU_XLA_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE3_GPU_XLA_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_phase5_longer_gpu_xla_ladder_markdown(
    path: Path,
    artifact: Mapping[str, Any],
) -> None:
    """Write a compact Phase 5 longer GPU/XLA diagnostic summary."""

    device_summary = artifact["run_manifest"]["cpu_gpu_status"]
    lines = [
        "# Minimal SSL-LSTM Zhao-Cui HMC Next Phase 5 Longer GPU/XLA Ladder",
        "",
        f"- Status: `{artifact['status']}`",
        f"- Artifact role: `{artifact['artifact_role']}`",
        f"- Filter: `{artifact['filter_name']}`",
        f"- Trusted approval recorded: `{artifact['predeclared_settings']['trusted_gpu_xla_approval']}`",
        f"- CUDA_VISIBLE_DEVICES: `{device_summary.get('cuda_visible_devices')}`",
        f"- GPU devices: `{device_summary.get('gpu_devices')}`",
        f"- All predeclared seeds passed: `{artifact['all_predeclared_seeds_passed']}`",
        f"- Native divergence statuses: `{artifact['native_divergence_statuses']}`",
        f"- Native divergence interpretation: `{artifact['native_divergence_interpretation']}`",
        "",
        "## Candidate Rows",
        "",
        "| seed | status | hard vetoes | acceptance rate | divergence status | nonfinite samples | sample shape | runtime s |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in artifact["candidate_rows"]:
        diagnostics = row["hmc_runtime"]["diagnostics"]
        lines.append(
            "| "
            + " | ".join(
                [
                    str(row["seed"]),
                    str(row["status"]),
                    ", ".join(row["hard_vetoes"]) or "none",
                    str(diagnostics.get("acceptance_rate")),
                    str(diagnostics.get("divergence_status")),
                    str(diagnostics.get("nonfinite_sample_count")),
                    str(row["hmc_runtime"].get("sample_shape")),
                    str(row["hmc_runtime"].get("runtime_s")),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Decision Table", "", "| field | value |", "| --- | --- |"])
    for key, value in artifact["decision_table"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Inference Status", "", "| field | value |", "| --- | --- |"])
    for key, value in artifact["inference_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(["", "## Hard Vetoes", ""])
    vetoes = list(artifact["hard_vetoes"])
    lines.extend(f"- {item}" for item in vetoes) if vetoes else lines.append("- none")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    lines.extend(["", "## Artifact Paths", ""])
    lines.append(
        "- Plan: `docs/plans/"
        "bayesfilter-minimal-ssl-lstm-zhaocui-hmc-next-program-master-2026-07-06.md`"
    )
    lines.append(f"- Subplan: `{PHASE5_LONGER_DIAGNOSTICS_SUBPLAN_PATH}`")
    lines.append(f"- Result: `{PHASE5_LONGER_DIAGNOSTICS_RESULT_PATH}`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _fixture_payload() -> dict[str, Any]:
    return minimal_ssl_lstm_fixture_payload()


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


def _tf_device_summary(
    *,
    trust_basis: str = "cpu_hidden_debug_no_gpu_claim",
) -> dict[str, Any]:
    physical = tf.config.list_physical_devices()
    return {
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES", "<unset>"),
        "physical_devices": [device.name for device in physical],
        "gpu_devices": [device.name for device in tf.config.list_physical_devices("GPU")],
        "trust_basis": str(trust_basis),
    }


def _json_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return _json_ready(value.numpy())
    if isinstance(value, Mapping):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if hasattr(value, "tolist") and callable(value.tolist):
        return value.tolist()
    if hasattr(value, "item") and callable(value.item):
        try:
            return value.item()
        except Exception:  # noqa: BLE001
            return str(value)
    return value


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument(
        "--mode",
        choices=(
            "phase1-adapter",
            "phase2-canary",
            "phase3-gpu-xla-smoke",
            "phase4-short-ladder",
            "phase5-longer-gpu-xla-ladder",
        ),
        default="phase1-adapter",
    )
    parser.add_argument("--output", default=str(DEFAULT_JSON_OUTPUT))
    parser.add_argument("--markdown-output", default=str(DEFAULT_MARKDOWN_OUTPUT))
    parser.add_argument("--prior-scale", type=float, default=5.0)
    parser.add_argument("--initial-offset-scale", type=float, default=1.0e-3)
    parser.add_argument("--num-results", type=int, default=2)
    parser.add_argument("--num-burnin-steps", type=int, default=1)
    parser.add_argument("--step-size", type=float, default=1.0e-5)
    parser.add_argument("--num-leapfrog-steps", type=int, default=1)
    parser.add_argument("--seed", type=int, nargs=2, default=None)
    parser.add_argument(
        "--ladder-seeds",
        type=int,
        nargs="+",
        default=None,
    )
    parser.add_argument("--trusted-gpu-xla-approval", action="store_true")
    parser.add_argument("--require-cpu-hidden", action="store_true", default=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if (
        args.mode not in {"phase3-gpu-xla-smoke", "phase5-longer-gpu-xla-ladder"}
        and args.require_cpu_hidden
        and os.environ.get("CUDA_VISIBLE_DEVICES") != "-1"
    ):
        raise RuntimeError("minimal HMC ladder harness requires CUDA_VISIBLE_DEVICES=-1")
    if (
        args.mode in {"phase3-gpu-xla-smoke", "phase5-longer-gpu-xla-ladder"}
        and not args.trusted_gpu_xla_approval
    ):
        raise RuntimeError(
            "GPU/XLA HMC mode requires --trusted-gpu-xla-approval"
        )
    if args.mode == "phase5-longer-gpu-xla-ladder" and args.seed is not None:
        raise RuntimeError("Phase 5 ladder seeds are fixed; do not pass --seed")
    if args.mode == "phase5-longer-gpu-xla-ladder" and args.ladder_seeds is not None:
        raise RuntimeError(
            "Phase 5 ladder seeds are fixed; do not pass --ladder-seeds"
        )
    if (
        args.mode == "phase5-longer-gpu-xla-ladder"
        and not math.isclose(
            float(args.prior_scale),
            PHASE5_PRIOR_SCALE,
            rel_tol=0.0,
            abs_tol=0.0,
        )
    ):
        raise RuntimeError("Phase 5 prior scale is fixed; do not pass --prior-scale")
    if (
        args.mode == "phase5-longer-gpu-xla-ladder"
        and not math.isclose(
            float(args.initial_offset_scale),
            PHASE5_INITIAL_OFFSET_SCALE,
            rel_tol=0.0,
            abs_tol=0.0,
        )
    ):
        raise RuntimeError(
            "Phase 5 initial offset scale is fixed; do not pass "
            "--initial-offset-scale"
        )
    started = time.perf_counter()
    output = Path(args.output)
    markdown_output = Path(args.markdown_output)
    seed = (
        PHASE3_GPU_XLA_HMC_SEED
        if args.mode == "phase3-gpu-xla-smoke" and args.seed is None
        else PHASE2_HMC_SEED
        if args.seed is None
        else tuple(args.seed)
    )
    if args.mode == "phase1-adapter":
        artifact = build_phase1_adapter_artifact(
            prior_scale=args.prior_scale,
            initial_offset_scale=args.initial_offset_scale,
            command=tuple(sys.argv),
        )
        write_markdown_fn = write_markdown
    elif args.mode == "phase2-canary":
        if str(output) == str(DEFAULT_JSON_OUTPUT):
            output = DEFAULT_CANARY_JSON_OUTPUT
        if str(markdown_output) == str(DEFAULT_MARKDOWN_OUTPUT):
            markdown_output = DEFAULT_CANARY_MARKDOWN_OUTPUT
        artifact = build_phase2_canary_artifact(
            prior_scale=args.prior_scale,
            initial_offset_scale=args.initial_offset_scale,
            num_results=args.num_results,
            num_burnin_steps=args.num_burnin_steps,
            step_size=args.step_size,
            num_leapfrog_steps=args.num_leapfrog_steps,
            seed=tuple(seed),
            command=tuple(sys.argv),
        )
        write_markdown_fn = write_canary_markdown
    elif args.mode == "phase3-gpu-xla-smoke":
        if str(output) == str(DEFAULT_JSON_OUTPUT):
            output = DEFAULT_GPU_XLA_JSON_OUTPUT
        if str(markdown_output) == str(DEFAULT_MARKDOWN_OUTPUT):
            markdown_output = DEFAULT_GPU_XLA_MARKDOWN_OUTPUT
        artifact = build_phase3_gpu_xla_smoke_artifact(
            trusted_gpu_xla_approval=bool(args.trusted_gpu_xla_approval),
            prior_scale=args.prior_scale,
            initial_offset_scale=args.initial_offset_scale,
            num_results=args.num_results,
            num_burnin_steps=args.num_burnin_steps,
            step_size=args.step_size,
            num_leapfrog_steps=args.num_leapfrog_steps,
            seed=tuple(seed),
            command=tuple(sys.argv),
        )
        write_markdown_fn = write_gpu_xla_smoke_markdown
    elif args.mode == "phase4-short-ladder":
        if str(output) == str(DEFAULT_JSON_OUTPUT):
            output = DEFAULT_LADDER_JSON_OUTPUT
        if str(markdown_output) == str(DEFAULT_MARKDOWN_OUTPUT):
            markdown_output = DEFAULT_LADDER_MARKDOWN_OUTPUT
        artifact = build_phase4_short_ladder_artifact(
            prior_scale=args.prior_scale,
            initial_offset_scale=args.initial_offset_scale,
            num_results=args.num_results,
            num_burnin_steps=args.num_burnin_steps,
            step_size=args.step_size,
            num_leapfrog_steps=args.num_leapfrog_steps,
            seeds=PHASE4_HMC_SEEDS,
            command=tuple(sys.argv),
        )
        write_markdown_fn = write_ladder_markdown
    else:
        if str(output) == str(DEFAULT_JSON_OUTPUT):
            output = DEFAULT_PHASE5_GPU_XLA_JSON_OUTPUT
        if str(markdown_output) == str(DEFAULT_MARKDOWN_OUTPUT):
            markdown_output = DEFAULT_PHASE5_GPU_XLA_MARKDOWN_OUTPUT
        artifact = build_phase5_longer_gpu_xla_ladder_artifact(
            trusted_gpu_xla_approval=bool(args.trusted_gpu_xla_approval),
            prior_scale=args.prior_scale,
            initial_offset_scale=args.initial_offset_scale,
            num_results=args.num_results,
            num_burnin_steps=args.num_burnin_steps,
            step_size=args.step_size,
            num_leapfrog_steps=args.num_leapfrog_steps,
            seeds=PHASE5_GPU_XLA_HMC_SEEDS,
            command=tuple(sys.argv),
        )
        write_markdown_fn = write_phase5_longer_gpu_xla_ladder_markdown
    artifact["run_manifest"]["wall_time_s"] = float(time.perf_counter() - started)
    artifact["run_manifest"]["timestamp"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    atomic_write_json(output, artifact)
    write_markdown_fn(markdown_output, artifact)
    print(
        json.dumps(
            {
                "status": artifact["status"],
                "mode": args.mode,
                "json_output": str(output),
                "markdown_output": str(markdown_output),
                "hard_vetoes": artifact["hard_vetoes"],
            },
            sort_keys=True,
        )
    )
    return 0 if artifact["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
