"""SSL-LSTM Phase 7 bounded HMC launch smoke.

This script uses the admitted SSL-LSTM filter value/score adapters from Phase 6
as a tiny fixed-kernel HMC mechanics smoke. It is launch-only evidence:
hard-veto classification, target-path validity, and artifact integrity.
It does not claim convergence, ranking, or invariant-metric promotion.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "1")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import tensorflow as tf  # noqa: E402

from bayesfilter.inference import FullChainHMCConfig, ValueScoreCapability, run_full_chain_tfp_hmc  # noqa: E402
from bayesfilter.nonlinear.ssl_lstm_protocol import SSLLSTMStaticConfig  # noqa: E402
from bayesfilter.nonlinear.ssl_lstm_sgqf_ukf_adapters import (  # noqa: E402
    make_ssl_lstm_fixed_sgqf_components,
    make_ssl_lstm_svd_ukf_components,
    ssl_lstm_observation,
    ssl_lstm_transition,
    tf_ssl_lstm_fixed_sgqf_score,
    tf_ssl_lstm_svd_ukf_score,
    unpack_ssl_lstm_parameters,
)
from bayesfilter.nonlinear.ssl_lstm_zhaocui_fixed_adapter import (  # noqa: E402
    SSLLSTMZhaoCuiFixedManifest,
    make_ssl_lstm_zhaocui_fixed_components,
    tf_ssl_lstm_zhaocui_fixed_score,
)
from bayesfilter.runtime import atomic_write_json  # noqa: E402


PLAN_PATH = "docs/plans/bayesfilter-ssl-lstm-filter-hmc-master-program-2026-07-04.md"
SUBPLAN_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-subplan-2026-07-04.md"
)
RESULT_PATH = (
    "docs/plans/"
    "bayesfilter-ssl-lstm-filter-hmc-phase7-hmc-evidence-ladder-result-2026-07-04.md"
)
PHASE6_ARTIFACT_PATH = (
    "docs/benchmarks/"
    "ssl_lstm_filter_hmc_phase6_shared_benchmark_cpu_hidden_2026-07-04.json"
)
GPU_TRUST_BASIS = "owner_designated_managed_session_visible_gpu_trusted"
ADMITTED_FILTERS = ("fixed_sgqf", "svd_ukf", "zhaocui_fixed")
BLOCKED_FILTERS = ("ledh_streaming_ot",)
NONCLAIMS = (
    "launch-tier HMC mechanics smoke only",
    "not a sampler convergence claim",
    "not R-hat or ESS evidence",
    "not posterior correctness evidence",
    "not filter sufficiency evidence",
    "not parameter-recovery evidence",
    "not a ranking claim",
    "not default-readiness evidence",
    "Phase 6 heldout predictive log score remains explanatory proxy only",
)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--device", default="/CPU:0")
    parser.add_argument("--device-scope", choices=("cpu", "visible"), default="cpu")
    parser.add_argument("--expect-device-kind", choices=("any", "cpu", "gpu"), default="cpu")
    parser.add_argument("--seed", type=int, default=20260705)
    parser.add_argument("--horizon", type=int, default=4)
    parser.add_argument("--latent-dim", type=int, default=2)
    parser.add_argument("--hidden-dim", type=int, default=2)
    parser.add_argument("--observation-dim", type=int, default=1)
    parser.add_argument("--heldout-start", type=int, default=3)
    parser.add_argument("--sparse-level", type=int, default=2)
    parser.add_argument("--num-results", type=int, default=2)
    parser.add_argument("--num-burnin-steps", type=int, default=1)
    parser.add_argument("--step-size", type=float, default=1.0e-5)
    parser.add_argument("--num-leapfrog-steps", type=int, default=1)
    parser.add_argument("--prior-scale", type=float, default=5.0)
    parser.add_argument("--initial-offset-scale", type=float, default=1.0e-3)
    parser.add_argument("--jit-compile", dest="jit_compile", action="store_true", default=False)
    parser.add_argument("--no-jit-compile", dest="jit_compile", action="store_false")
    parser.add_argument("--phase6-artifact", default=PHASE6_ARTIFACT_PATH)
    return parser.parse_args()


def _validate_args(args: argparse.Namespace) -> None:
    if args.device_scope == "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        tf.config.experimental.enable_tensor_float_32_execution(False)
    if args.horizon <= 1:
        raise ValueError("horizon must be greater than one")
    if args.heldout_start <= 0 or args.heldout_start >= args.horizon:
        raise ValueError("heldout_start must split the horizon")
    for name in ("latent_dim", "hidden_dim", "observation_dim", "sparse_level", "num_results", "num_burnin_steps", "num_leapfrog_steps"):
        if int(getattr(args, name)) <= 0:
            raise ValueError(f"{name} must be positive")
    for name in ("step_size", "prior_scale", "initial_offset_scale"):
        if float(getattr(args, name)) <= 0.0:
            raise ValueError(f"{name} must be positive")


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
    return {"dirty": bool(lines), "line_count": len(lines), "preview": lines[:20]}


def _json_ready(value: Any) -> Any:
    if isinstance(value, tf.Tensor):
        return _json_ready(value.numpy())
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_ready(item) for item in value]
    if hasattr(value, "tolist") and callable(value.tolist):
        return value.tolist()
    if hasattr(value, "item") and callable(value.item):
        try:
            return value.item()
        except Exception:  # noqa: BLE001
            return str(value)
    return value


def _truth_theta(config: SSLLSTMStaticConfig) -> tf.Tensor:
    values = [0.0] * config.parameter_dim
    cursor = 0
    values[cursor : cursor + 4 * config.hidden_dim * config.latent_dim] = [
        0.11,
        -0.07,
        0.05,
        0.02,
        -0.03,
        0.04,
        -0.06,
        0.08,
        0.03,
        -0.02,
        0.04,
        -0.05,
        0.01,
        -0.01,
        0.02,
        -0.03,
    ]
    cursor += 4 * config.hidden_dim * config.latent_dim
    values[cursor : cursor + 4 * config.hidden_dim * config.hidden_dim] = [
        0.02,
        -0.03,
        0.01,
        -0.02,
        0.04,
        -0.01,
        0.03,
        -0.04,
        0.05,
        -0.06,
        0.02,
        -0.01,
        0.03,
        -0.02,
        0.04,
        -0.05,
    ]
    cursor += 4 * config.hidden_dim * config.hidden_dim
    values[cursor : cursor + 4 * config.hidden_dim] = [
        0.01,
        -0.02,
        0.03,
        -0.01,
        0.02,
        -0.03,
        0.04,
        -0.04,
    ]
    cursor += 4 * config.hidden_dim
    values[cursor : cursor + config.latent_dim * config.hidden_dim] = [0.2, -0.15, 0.07, 0.09]
    cursor += config.latent_dim * config.hidden_dim
    values[cursor : cursor + config.latent_dim] = [0.03, -0.02]
    cursor += config.latent_dim
    values[cursor : cursor + config.observation_dim * config.latent_dim] = [0.5, -0.35]
    cursor += config.observation_dim * config.latent_dim
    values[cursor : cursor + config.observation_dim] = [0.05]
    cursor += config.observation_dim
    values[cursor : cursor + config.augmented_state_dim] = [0.0, 0.1, -0.05, 0.02, -0.03, 0.04]
    cursor += config.augmented_state_dim
    values[cursor : cursor + config.augmented_state_dim] = [-2.0, -1.5, -1.2, -1.0, -0.8, -0.6]
    cursor += config.augmented_state_dim
    values[cursor : cursor + config.latent_dim] = [-1.8, -1.4]
    cursor += config.latent_dim
    values[cursor : cursor + config.observation_dim] = [-1.6]
    return tf.constant(values, dtype=tf.float64)


class _Phase7HMCAdapter:
    """Tiny HMC adapter that adds a Gaussian prior to an analytic filter score."""

    def __init__(
        self,
        *,
        filter_name: str,
        observations: tf.Tensor,
        config: SSLLSTMStaticConfig,
        evidence_path: str,
        prior_center: tf.Tensor,
        prior_scale: float,
        sparse_level: int,
    ) -> None:
        self.filter_name = filter_name
        self.observations = tf.convert_to_tensor(observations, dtype=tf.float64)
        self.config = config
        self.evidence_path = evidence_path
        self.prior_center = tf.convert_to_tensor(prior_center, dtype=tf.float64)
        self.prior_scale = float(prior_scale)
        self.sparse_level = int(sparse_level)
        self.parameter_dim = int(config.parameter_dim)
        self.target_scope = f"ssl_lstm_filter_hmc:{filter_name}:phase7_launch_smoke"
        self.zhaocui_manifest = SSLLSTMZhaoCuiFixedManifest(
            reference_sample_count=9,
            initial_seed=(20260705, 7103),
            process_seed=(20260705, 7104),
        )
        theta = self.prior_center
        if filter_name == "fixed_sgqf":
            self._components = make_ssl_lstm_fixed_sgqf_components(
                theta,
                config,
                evidence_path=evidence_path,
                sparse_level=sparse_level,
            )
        elif filter_name == "svd_ukf":
            self._components = make_ssl_lstm_svd_ukf_components(
                theta,
                config,
                evidence_path=evidence_path,
            )
        elif filter_name == "zhaocui_fixed":
            self._components = make_ssl_lstm_zhaocui_fixed_components(
                theta,
                config,
                evidence_path=evidence_path,
                manifest=self.zhaocui_manifest,
            )
        else:
            raise ValueError(f"unsupported filter: {filter_name}")

    def adapter_signature(self) -> str:
        payload = {
            "filter_name": self.filter_name,
            "horizon": self.config.horizon,
            "parameter_dim": self.parameter_dim,
            "prior_scale": self.prior_scale,
            "evidence_path": self.evidence_path,
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def value_score_capability(self):
        base = self._components.protocol.contract.value_score
        return ValueScoreCapability(
            value_score_authority=base.value_score_authority,
            xla_hmc_ready=True,
            full_chain_xla_diagnostic_ready=True,
            runtime_backend=base.runtime_backend,
            evidence_path=self.evidence_path,
            target_scope=self.target_scope,
            nonclaims=base.nonclaims + (
                "Phase 7 launch-smoke target scope",
                "no convergence claim",
                "no ranking claim",
            ),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        theta = tf.convert_to_tensor(theta, dtype=tf.float64)
        if theta.shape.rank == 2:
            values = []
            scores = []
            for index in range(int(theta.shape[0])):
                value, score = self._scalar_log_prob_and_grad(theta[index])
                values.append(value)
                scores.append(score)
            return tf.stack(values), tf.stack(scores)
        return self._scalar_log_prob_and_grad(theta)

    def _scalar_log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        if self.filter_name == "fixed_sgqf":
            result, _ = tf_ssl_lstm_fixed_sgqf_score(
                self.observations,
                theta,
                self.config,
                evidence_path=self.evidence_path,
                sparse_level=self.sparse_level,
            )
        elif self.filter_name == "svd_ukf":
            result, _ = tf_ssl_lstm_svd_ukf_score(
                self.observations,
                theta,
                self.config,
                evidence_path=self.evidence_path,
            )
        elif self.filter_name == "zhaocui_fixed":
            result, _ = tf_ssl_lstm_zhaocui_fixed_score(
                self.observations,
                theta,
                self.config,
                evidence_path=self.evidence_path,
                manifest=self.zhaocui_manifest,
            )
        else:
            raise ValueError(f"unsupported filter: {self.filter_name}")
        delta = theta - self.prior_center
        variance = tf.constant(self.prior_scale * self.prior_scale, dtype=tf.float64)
        prior_value = -0.5 * tf.reduce_sum(tf.square(delta) / variance)
        prior_score = -delta / variance
        return result.log_likelihood + prior_value, tf.convert_to_tensor(result.score, dtype=tf.float64) + prior_score


def _simulate_fixture(config: SSLLSTMStaticConfig, theta: tf.Tensor) -> dict[str, tf.Tensor]:
    params = unpack_ssl_lstm_parameters(theta, config)
    state = tf.convert_to_tensor(params.initial_mean, dtype=tf.float64)
    states = [state]
    observations = []
    for _ in range(config.horizon):
        state = ssl_lstm_transition(params, state[tf.newaxis, :])[0]
        states.append(state)
        observations.append(ssl_lstm_observation(params, state[tf.newaxis, :])[0])
    return {"states": tf.stack(states, axis=0), "observations": tf.stack(observations, axis=0)}


def _run_candidate(args: argparse.Namespace, filter_name: str, config: SSLLSTMStaticConfig, observations: tf.Tensor, theta: tf.Tensor) -> dict[str, Any]:
    adapter = _Phase7HMCAdapter(
        filter_name=filter_name,
        observations=observations[: args.heldout_start],
        config=config,
        evidence_path=SUBPLAN_PATH,
        prior_center=theta,
        prior_scale=args.prior_scale,
        sparse_level=args.sparse_level,
    )
    initial_state = theta + tf.cast(args.initial_offset_scale, tf.float64) * tf.linspace(
        tf.constant(-1.0, dtype=tf.float64),
        tf.constant(1.0, dtype=tf.float64),
        config.parameter_dim,
    )
    initial_value, initial_score = adapter.log_prob_and_grad(initial_state)
    hard_vetoes: list[str] = []
    if not bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy()):
        hard_vetoes.append("initial_target_value_nonfinite")
    if not bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy()):
        hard_vetoes.append("initial_target_score_nonfinite")
    result = None
    error_message = None
    start = time.perf_counter()
    try:
        hmc_config = FullChainHMCConfig(
            num_results=args.num_results,
            num_burnin_steps=args.num_burnin_steps,
            step_size=args.step_size,
            num_leapfrog_steps=args.num_leapfrog_steps,
            seed=(int(args.seed), {"fixed_sgqf": 7101, "svd_ukf": 7102, "zhaocui_fixed": 7103}[filter_name]),
            use_xla=bool(args.jit_compile),
            trace_policy="standard",
            adaptation_policy="fixed_kernel_no_adaptation",
            target_scope=adapter.target_scope,
            chain_execution_mode="eager",
        )
        result = run_full_chain_tfp_hmc(adapter, initial_state, hmc_config)
    except Exception as exc:  # noqa: BLE001
        error_message = f"{type(exc).__name__}: {exc}"
        hard_vetoes.append("hmc_runtime_exception")
    runtime_s = time.perf_counter() - start
    diagnostics: dict[str, Any] = {}
    metadata: dict[str, Any] = {}
    if result is not None:
        diagnostics = dict(result.diagnostics)
        metadata = dict(result.metadata)
        if int(tf.convert_to_tensor(diagnostics.get("nonfinite_sample_count", 0)).numpy()) > 0:
            hard_vetoes.append("nonfinite_hmc_samples")
        if diagnostics.get("divergence_count") not in (None, 0):
            divergence_count = int(tf.convert_to_tensor(diagnostics["divergence_count"]).numpy())
            if divergence_count > 0:
                hard_vetoes.append("native_divergence_detected")
    status = "passed_launch_smoke" if not hard_vetoes else "failed_launch_smoke"
    return {
        "filter_name": filter_name,
        "status": status,
        "hard_vetoes": tuple(dict.fromkeys(hard_vetoes)),
        "target_scope": adapter.target_scope,
        "gradient_path": {
            "fixed_sgqf": "analytic_first_order_fixed_sgqf",
            "svd_ukf": "analytic_first_order_svd_ukf",
            "zhaocui_fixed": "analytic_first_order_zhaocui_fixed",
        }[filter_name],
        "value_score_authority": "graph_native",
        "initial_value_finite": bool(tf.reduce_all(tf.math.is_finite(initial_value)).numpy()),
        "initial_score_finite": bool(tf.reduce_all(tf.math.is_finite(initial_score)).numpy()),
        "initial_score_norm": float(tf.linalg.norm(initial_score).numpy()),
        "hmc_runtime_s": runtime_s,
        "hmc_error": error_message,
        "hmc_diagnostics": _json_ready(diagnostics),
        "hmc_metadata": _json_ready(metadata),
        "diagnostic_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "initial_value_finite": "hard_veto_evidence",
            "initial_score_finite": "hard_veto_evidence",
            "acceptance_rate": "explanatory_only_in_launch_smoke",
            "runtime": "explanatory_only",
            "rhat": "not_computed_in_launch_smoke",
            "ess": "not_computed_in_launch_smoke",
        },
        "nonclaims": (
            "launch-tier HMC mechanics smoke only",
            "not a sampler convergence claim",
            "not R-hat or ESS evidence",
            "not ranking evidence",
        ),
    }


def build_result(args: argparse.Namespace) -> dict[str, Any]:
    _validate_args(args)
    config = SSLLSTMStaticConfig(
        horizon=args.horizon,
        latent_dim=args.latent_dim,
        hidden_dim=args.hidden_dim,
        observation_dim=args.observation_dim,
    )
    theta = _truth_theta(config)
    fixture = _simulate_fixture(config, theta)
    observations = fixture["observations"]
    candidate_rows = [
        _run_candidate(args, "fixed_sgqf", config, observations, theta),
        _run_candidate(args, "svd_ukf", config, observations, theta),
        _run_candidate(args, "zhaocui_fixed", config, observations, theta),
        {
            "filter_name": "ledh_streaming_ot",
            "status": "blocked",
            "hard_vetoes": ("missing_manual_vjp_streaming_ot_score_path",),
            "gradient_path": "manual_vjp_streaming_ot",
            "target_scope": None,
            "value_score_authority": None,
            "nonclaims": ("status-only blocked row", "not an HMC result"),
        },
    ]
    admitted_rows = [row for row in candidate_rows if row["filter_name"] in ADMITTED_FILTERS]
    launch_pass_count = sum(1 for row in admitted_rows if row["status"] == "passed_launch_smoke")
    status = (
        "PHASE7_LAUNCH_SMOKE_PASSED"
        if launch_pass_count == len(ADMITTED_FILTERS)
        else "PHASE7_LAUNCH_SMOKE_HARD_VETO_RECORDED"
    )
    return {
        "schema_version": "ssl_lstm.filter_hmc.phase7_hmc_smoke.v1",
        "phase": "PHASE7",
        "tier": "launch_smoke",
        "status": status,
        "plan_file": PLAN_PATH,
        "subplan_file": SUBPLAN_PATH,
        "result_file": RESULT_PATH,
        "phase6_artifact": args.phase6_artifact,
        "run_manifest": {
            "git_commit": _git_commit(),
            "dirty_state_summary": _git_dirty_summary(),
            "command": tuple(sys.argv),
            "environment": {
                "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
                "TF_CPP_MIN_LOG_LEVEL": os.environ.get("TF_CPP_MIN_LOG_LEVEL"),
            },
            "conda_env": os.environ.get("CONDA_DEFAULT_ENV"),
            "cpu_gpu_status": {
                "device_scope": args.device_scope,
                "device": args.device,
                "logical_gpus": [str(device) for device in tf.config.list_logical_devices("GPU")],
            },
            "dtype": "float64",
            "seeds": {"fixture": int(args.seed)},
            "output_json": str(Path(args.output)),
            "markdown_output": str(Path(args.markdown_output)),
            "gpu_trust_basis": GPU_TRUST_BASIS if args.device_scope != "cpu" else "cpu_hidden_debug",
            "jit_compile": bool(args.jit_compile),
            "tf32_mode": "disabled" if args.device_scope == "cpu" else "default",
        },
        "dataset_manifest": {
            "schema_version": "ssl_lstm.filter_hmc.dataset_manifest.v1",
            "source": "phase6_shared_fixture_rebuilt_deterministically",
            "seed": int(args.seed),
            "horizon": int(args.horizon),
            "latent_dim": int(args.latent_dim),
            "hidden_dim": int(args.hidden_dim),
            "observation_dim": int(args.observation_dim),
            "heldout_start": int(args.heldout_start),
            "train_count": int(args.heldout_start),
            "heldout_count": int(args.horizon - args.heldout_start),
            "truth_theta_signature": hashlib.sha256(
                json.dumps(_json_ready(theta), sort_keys=True).encode("utf-8")
            ).hexdigest(),
        },
        "candidate_rows": candidate_rows,
        "admitted_filters": ADMITTED_FILTERS,
        "blocked_filters": BLOCKED_FILTERS,
        "hard_veto_summary": {row["filter_name"]: row["hard_vetoes"] for row in candidate_rows},
        "metric_roles": {
            "hard_vetoes": "hard_veto_evidence",
            "initial_value_finite": "hard_veto_evidence",
            "initial_score_finite": "hard_veto_evidence",
            "acceptance_rate": "explanatory_only_in_launch_smoke",
            "runtime": "explanatory_only",
            "rhat": "not_computed_in_launch_smoke",
            "ess": "not_computed_in_launch_smoke",
            "heldout_predictive_log_score": "not_computed_in_phase7_launch_smoke",
        },
        "inference_status": {
            "hard_veto_screen": (
                "passed_for_admitted_launch_smoke"
                if launch_pass_count == len(ADMITTED_FILTERS)
                else "failed_for_at_least_one_admitted_launch_smoke"
            ),
            "statistically_supported_ranking": "not_claimed",
            "descriptive_only_differences": "not_interpreted",
            "default_readiness": "not_checked",
            "next_evidence_needed": "Phase 7 warmup/short-chain replicated tier with predeclared R-hat/ESS and uncertainty evidence before any ranking",
        },
        "decision_table": {
            "decision": "launch smoke classification only",
            "primary_criterion_status": "launch_smoke_artifact_written",
            "veto_diagnostic_status": (
                "no launch hard veto for admitted filters"
                if launch_pass_count == len(ADMITTED_FILTERS)
                else "hard veto recorded"
            ),
            "main_uncertainty": "tiny fixed-kernel smoke cannot assess convergence, R-hat/ESS, ranking, or invariant estimation quality",
            "next_justified_action": "write Phase 7 result and decide whether to plan a longer replicated HMC tier",
            "what_is_not_being_concluded": (
                "No method superiority, no exact posterior correctness, no parameter identifiability, "
                "no production/default readiness, and no full Phase 7 replicated-evidence pass."
            ),
        },
        "parameter_matching_primary_criterion": False,
        "ranking_supported": False,
        "rhat_ess_computed": False,
        "nonclaims": NONCLAIMS,
    }


def _write_markdown(path: Path, artifact: dict[str, Any]) -> None:
    lines = [
        "# SSL-LSTM Phase 7 HMC Launch Smoke",
        "",
        f"- Schema: `{artifact['schema_version']}`",
        f"- Status: `{artifact['status']}`",
        f"- Tier: `{artifact['tier']}`",
        f"- Git commit: `{artifact['run_manifest']['git_commit']}`",
        f"- Device scope: `{artifact['run_manifest']['cpu_gpu_status']['device_scope']}`",
        f"- JIT compile: `{artifact['run_manifest']['jit_compile']}`",
        "",
        "## Candidate Status",
        "",
        "| filter | status | hard vetoes | target scope |",
        "| --- | --- | --- | --- |",
    ]
    for row in artifact["candidate_rows"]:
        lines.append(
            f"| {row['filter_name']} | {row['status']} | {', '.join(row['hard_vetoes']) or 'none'} | {row.get('target_scope')} |"
        )
    lines.extend(
        [
            "",
            "## Decision Table",
            "",
            "| field | value |",
            "| --- | --- |",
        ]
    )
    for key, value in artifact["decision_table"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Inference Status",
            "",
            "| field | value |",
            "| --- | --- |",
        ]
    )
    for key, value in artifact["inference_status"].items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Hard Veto Summary",
            "",
            "| filter | vetoes |",
            "| --- | --- |",
        ]
    )
    for key, value in artifact["hard_veto_summary"].items():
        lines.append(f"| {key} | {', '.join(value) or 'none'} |")
    lines.extend(["", "## Nonclaims", ""])
    lines.extend(f"- {item}" for item in artifact["nonclaims"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = _parse_args()
    start = time.perf_counter()
    artifact = build_result(args)
    artifact["runtime_s"] = time.perf_counter() - start
    artifact["timestamp_utc"] = _dt.datetime.now(tz=_dt.timezone.utc).isoformat()
    artifact["host"] = platform.node()
    artifact["python_version"] = platform.python_version()
    artifact["tensorflow_version"] = tf.__version__
    artifact["cuda_visible_devices"] = os.environ.get("CUDA_VISIBLE_DEVICES")
    artifact["tf32_enabled"] = bool(tf.config.experimental.tensor_float_32_execution_enabled())
    artifact["device_list"] = [
        {"name": device.name, "device_type": device.device_type}
        for device in tf.config.list_physical_devices()
    ]
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_json(output, artifact)
    markdown = Path(args.markdown_output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    _write_markdown(markdown, artifact)


if __name__ == "__main__":
    main()
