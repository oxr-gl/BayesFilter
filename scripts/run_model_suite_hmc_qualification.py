#!/usr/bin/env python
"""Bounded BayesFilter model-suite HMC qualification ladder."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bayesfilter.runtime import ensure_cpu_only_env

ensure_cpu_only_env()

import numpy as np
import tensorflow as tf

from bayesfilter.inference import (
    FullChainHMCConfig,
    ValueScoreCapability,
    program_signature,
    run_full_chain_tfp_hmc,
    static_unroll_chain_value_and_score,
)
from bayesfilter.runtime import (
    PartialResultSnapshot,
    WorkerRecord,
    append_heartbeat,
    append_stage_event,
    atomic_write_json,
    build_worker_manifest,
    make_timing_bucket,
    record_worker_result,
    reduce_worker_artifacts,
    write_partial_result_snapshot,
    write_worker_manifest,
)
from bayesfilter.testing import (
    ModelBNonlinearSVDTarget,
    QRStaticLGSSMTarget,
    dense_projection_first_step,
    make_affine_gaussian_structural_oracle_tf,
    make_univariate_nonlinear_growth_first_derivatives_tf,
    make_univariate_nonlinear_growth_model_tf,
    model_a_observations_tf,
    model_c_observations_tf,
    nonlinear_sigma_point_score_branch_summary,
)
from bayesfilter.nonlinear import tf_svd_cut4_score


PROGRAM_SIGNATURE = "bayesfilter-model-suite-hmc-qualification-v1"
EXPECTED_ARTIFACT_FILES = {
    "worker_manifest.json",
    "stage_events.jsonl",
    "partial_snapshot.json",
    "worker_result.json",
    "reducer_status.json",
    "summary.json",
}
MODEL_ORDER = ("A", "QR", "B", "C")
VISIBLE_GPUS_AFTER_IMPORT = [str(device) for device in tf.config.list_physical_devices("GPU")]
if VISIBLE_GPUS_AFTER_IMPORT:
    raise RuntimeError(
        "CPU-only qualification requires TensorFlow visible GPUs []; got "
        f"{VISIBLE_GPUS_AFTER_IMPORT!r}"
    )


class ModelAAdapter:
    """Graph-native exact quadratic target grounded by the Model A fixture."""

    parameter_dim = 2
    target_scope = "model_a_affine_gaussian_structural_oracle"

    def __init__(self) -> None:
        model = make_affine_gaussian_structural_oracle_tf()
        self.center = tf.stack(
            [
                tf.convert_to_tensor(model.transition_matrix[0, 0], dtype=tf.float64),
                tf.sqrt(tf.convert_to_tensor(model.observation_covariance[0, 0], dtype=tf.float64)),
            ]
        )
        self.prior_scale = tf.constant([0.20, 0.10], dtype=tf.float64)
        self.initial_parameters = tf.identity(self.center)

    def adapter_signature(self) -> str:
        return "model-a-affine-gaussian-structural-oracle-quadratic-v1"

    def parameter_names(self) -> tuple[str, str]:
        return ("rho_anchor", "observation_sigma_anchor")

    def value_score_capability(self) -> ValueScoreCapability:
        return _capability(
            target_scope=self.target_scope,
            evidence_path="scripts/run_model_suite_hmc_qualification.py:ModelAAdapter",
            extra_nonclaims=(
                "Model A HMC target is an exact quadratic engineering target grounded by fixture constants",
                "not a parameterized Model A posterior claim",
            ),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        params = tf.convert_to_tensor(theta, dtype=tf.float64)
        scaled = (params - self.center) / self.prior_scale
        value = -0.5 * tf.reduce_sum(tf.square(scaled))
        score = -(params - self.center) / tf.square(self.prior_scale)
        return value, score


class QRAdapter:
    parameter_dim = 2
    target_scope = "qr_static_lgssm"

    def __init__(self) -> None:
        self.target = QRStaticLGSSMTarget.default()
        self.initial_parameters = self.target.initial_parameters

    def adapter_signature(self) -> str:
        return "qr-static-lgssm-analytic-score-target-v1"

    def parameter_names(self) -> tuple[str, str]:
        return ("rho_unconstrained", "log_measurement_noise")

    def value_score_capability(self) -> ValueScoreCapability:
        return _capability(
            target_scope=self.target_scope,
            evidence_path="scripts/run_model_suite_hmc_qualification.py:QRAdapter",
            extra_nonclaims=("QR target uses analytic score, not old HMC smoke helper output",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        params = tf.convert_to_tensor(theta, dtype=tf.float64)
        result = self.target.analytic_score_hessian(params)
        prior_quadratic = tf.reduce_sum(tf.square(params / self.target.prior_scale))
        prior_score = -(params / tf.square(self.target.prior_scale))
        return result.log_likelihood - 0.5 * prior_quadratic, result.score + prior_score


class ModelBAdapter:
    parameter_dim = 3
    target_scope = "model_b_nonlinear_accumulation_svd_cut4"

    def __init__(self) -> None:
        self.target = ModelBNonlinearSVDTarget.default()
        self.initial_parameters = self.target.initial_parameters

    def adapter_signature(self) -> str:
        return "model-b-nonlinear-svd-cut4-analytic-score-target-v1"

    def parameter_names(self) -> tuple[str, str, str]:
        return ("rho", "sigma", "beta")

    def value_score_capability(self) -> ValueScoreCapability:
        return _capability(
            target_scope=self.target_scope,
            evidence_path="scripts/run_model_suite_hmc_qualification.py:ModelBAdapter",
            extra_nonclaims=("Model B target uses analytic SVD-CUT4 score through consolidated HMC",),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return self.target.target_log_prob_and_grad(theta)

    def branch_summary(self) -> Mapping[str, Any]:
        return self.target.branch_summary()


class ModelCAdapter:
    parameter_dim = 3
    target_scope = "model_c_autonomous_nonlinear_growth_svd_cut4_fixed_support"

    def __init__(self) -> None:
        constrained = tf.constant([1.0, 1.0, 0.20], dtype=tf.float64)
        self.initial_parameters = tf.math.log(constrained)
        self.prior_mean = tf.identity(self.initial_parameters)
        self.prior_scale = tf.constant([0.25, 0.25, 0.35], dtype=tf.float64)
        self.observations = model_c_observations_tf()

    def adapter_signature(self) -> str:
        return "model-c-autonomous-growth-svd-cut4-fixed-support-log-params-v1"

    def parameter_names(self) -> tuple[str, str, str]:
        return ("log_process_sigma", "log_observation_sigma", "log_initial_variance")

    def value_score_capability(self) -> ValueScoreCapability:
        return _capability(
            target_scope=self.target_scope,
            evidence_path="scripts/run_model_suite_hmc_qualification.py:ModelCAdapter",
            extra_nonclaims=(
                "Model C uses the structural fixed-support branch with allow_fixed_null_support=True",
                "unconstrained log-parameter target is an engineering HMC target, not a posterior claim",
            ),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        params = tf.convert_to_tensor(theta, dtype=tf.float64)
        constrained = tf.exp(params)
        model = make_univariate_nonlinear_growth_model_tf(
            process_sigma=constrained[0],
            observation_sigma=constrained[1],
            initial_variance=constrained[2],
        )
        derivatives = make_univariate_nonlinear_growth_first_derivatives_tf(
            process_sigma=constrained[0],
            observation_sigma=constrained[1],
        )
        result = tf_svd_cut4_score(
            self.observations,
            model,
            derivatives,
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
            spectral_gap_tolerance=tf.constant(1e-8, dtype=tf.float64),
            allow_fixed_null_support=True,
        )
        centered = params - self.prior_mean
        prior_quadratic = tf.reduce_sum(tf.square(centered / self.prior_scale))
        prior_score = -(centered / tf.square(self.prior_scale))
        score = result.score * constrained + prior_score
        return result.log_likelihood - 0.5 * prior_quadratic, score

    def branch_summary(self) -> Mapping[str, Any]:
        grid = tf.constant(
            [
                [0.90, 0.90, 0.16],
                [1.00, 1.00, 0.20],
                [1.10, 1.10, 0.24],
            ],
            dtype=tf.float64,
        )
        return nonlinear_sigma_point_score_branch_summary(
            self.observations,
            tf.math.log(grid),
            lambda row: make_univariate_nonlinear_growth_model_tf(
                process_sigma=tf.exp(row[0]),
                observation_sigma=tf.exp(row[1]),
                initial_variance=tf.exp(row[2]),
            ),
            lambda row: make_univariate_nonlinear_growth_first_derivatives_tf(
                process_sigma=tf.exp(row[0]),
                observation_sigma=tf.exp(row[1]),
            ),
            backend="tf_svd_cut4",
            spectral_gap_tolerance=tf.constant(1e-8, dtype=tf.float64),
            allow_fixed_null_support=True,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--num-results", type=int, default=2)
    parser.add_argument("--num-burnin-steps", type=int, default=1)
    parser.add_argument("--num-leapfrog-steps", type=int, default=1)
    parser.add_argument("--stop-after", choices=MODEL_ORDER, default="C")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    artifact_root = Path(args.artifact_root)
    paths = _prepare_artifact_root(artifact_root, force=bool(args.force))
    started = time.perf_counter()
    command = tuple(sys.argv if argv is None else [sys.argv[0], *argv])
    git_commit = _git_commit()
    git_dirty_state = _git_dirty_state()
    normalized_config = {
        "ladder": MODEL_ORDER,
        "stop_after": args.stop_after,
        "artifact_contract": "single_worker_model_suite_qualification",
        "num_results": int(args.num_results),
        "num_burnin_steps": int(args.num_burnin_steps),
        "num_leapfrog_steps": int(args.num_leapfrog_steps),
        "step_sizes": _step_sizes(),
        "seed_base": [20260608, 70],
        "cpu_only": True,
        "jit_compile": True,
        "trace_policy": "standard",
        "old_smoke_helpers_final_evidence": False,
    }
    device_policy = {
        "mode": "cpu_only",
        "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_visible_gpus_after_import": VISIBLE_GPUS_AFTER_IMPORT,
    }
    thread_caps = {
        "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
        "TF_NUM_INTRAOP_THREADS": os.environ.get("TF_NUM_INTRAOP_THREADS"),
        "TF_NUM_INTEROP_THREADS": os.environ.get("TF_NUM_INTEROP_THREADS"),
    }
    worker_config = {
        "worker_kind": "bayesfilter_model_suite_hmc_qualification",
        "worker_id": "bayesfilter_model_suite_cpu_qualification",
        "budget": {
            "num_results": int(args.num_results),
            "num_burnin_steps": int(args.num_burnin_steps),
            "num_leapfrog_steps": int(args.num_leapfrog_steps),
        },
        "evidence_path": "consolidated_run_full_chain_tfp_hmc",
    }
    manifest = build_worker_manifest(
        worker_id="bayesfilter_model_suite_cpu_qualification",
        command=command,
        pid=os.getpid(),
        git_commit=git_commit,
        artifact_root=artifact_root,
        normalized_config=normalized_config,
        program_signature=PROGRAM_SIGNATURE,
        device_policy=device_policy,
        thread_caps=thread_caps,
        worker_config=worker_config,
        environment={
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "git_dirty_state": git_dirty_state,
        },
    )
    write_worker_manifest(paths["manifest"], manifest)
    append_stage_event(
        paths["events"],
        stage="start",
        status="ok",
        timestamp=_timestamp(),
        payload={
            "git_commit": git_commit,
            "git_dirty_state": git_dirty_state,
            "program_signature": PROGRAM_SIGNATURE,
        },
    )

    summary: dict[str, Any] | None = None
    try:
        summary = _run_suite(paths, manifest, args, git_commit, git_dirty_state)
        runtime_s = time.perf_counter() - started
        record_worker_result(
            paths["result"],
            WorkerRecord(
                worker_id=manifest.worker_id,
                command=command,
                config_hash=manifest.config_hash,
                return_code=0,
                runtime_s=runtime_s,
                timed_out=False,
                pid=os.getpid(),
                status="ok",
                device_policy=device_policy,
                thread_caps=thread_caps,
                worker_config_hash=manifest.worker_config_hash,
            ),
        )
        reducer = reduce_worker_artifacts(
            worker_id=manifest.worker_id,
            expected_stale_payload=manifest.stale_match_payload,
            manifest_path=paths["manifest"],
            result_path=paths["result"],
            partial_path=paths["partial"],
        )
        summary["worker_runtime_s"] = runtime_s
        summary["reducer_status"] = reducer.status
        summary["reducer_reason"] = reducer.reason
        atomic_write_json(paths["reducer"], reducer)
        atomic_write_json(paths["summary"], summary)
        append_stage_event(
            paths["events"],
            stage="complete",
            status="ok",
            timestamp=_timestamp(),
            payload={"reducer_status": reducer.status, "runtime_s": runtime_s},
        )
        if reducer.status != "complete":
            raise RuntimeError(f"model-suite reducer status is {reducer.status!r}")
        return 0
    except BaseException as exc:
        runtime_s = time.perf_counter() - started
        record_worker_result(
            paths["result"],
            WorkerRecord(
                worker_id=manifest.worker_id,
                command=command,
                config_hash=manifest.config_hash,
                return_code=1,
                runtime_s=runtime_s,
                timed_out=False,
                pid=os.getpid(),
                status="failed",
                device_policy=device_policy,
                thread_caps=thread_caps,
                worker_config_hash=manifest.worker_config_hash,
            ),
        )
        reducer = reduce_worker_artifacts(
            worker_id=manifest.worker_id,
            expected_stale_payload=manifest.stale_match_payload,
            manifest_path=paths["manifest"],
            result_path=paths["result"],
            partial_path=paths["partial"],
        )
        atomic_write_json(paths["reducer"], reducer)
        failure_summary = {
            "artifact_type": "bayesfilter_model_suite_hmc_qualification_summary",
            "program_signature": PROGRAM_SIGNATURE,
            "status": "failed",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "partial_summary": summary,
            "git": {"commit": git_commit, "dirty_state": git_dirty_state},
            "reducer_status": reducer.status,
            "reducer_reason": reducer.reason,
            "nonclaims": _nonclaims(),
        }
        atomic_write_json(paths["summary"], failure_summary)
        append_stage_event(
            paths["events"],
            stage="failed",
            status="failed",
            timestamp=_timestamp(),
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        raise


def _run_suite(
    paths: Mapping[str, Path],
    manifest: Any,
    args: argparse.Namespace,
    git_commit: str,
    git_dirty_state: Mapping[str, Any],
) -> dict[str, Any]:
    model_records: list[dict[str, Any]] = []
    skipped_models: list[dict[str, Any]] = []
    timing_buckets = []

    model_a_value = _model_a_value_sanity()
    adapters: list[tuple[str, Any]] = [
        ("A", ModelAAdapter()),
        ("QR", QRAdapter()),
        ("B", ModelBAdapter()),
    ]
    for index, (model_id, adapter) in enumerate(adapters):
        record, bucket = _run_model(paths, manifest, model_id, adapter, args, seed_offset=index)
        if model_id == "A":
            record["value_path_sanity"] = model_a_value
        model_records.append(record)
        timing_buckets.append(bucket)
        if record["status"] != "passed":
            raise RuntimeError(f"required model {model_id} failed: {record['veto_reasons']}")
        if model_id == args.stop_after:
            break

    if _should_run_model_c(model_records, args.stop_after):
        try:
            record, bucket = _run_model(paths, manifest, "C", ModelCAdapter(), args, seed_offset=3)
        except BaseException as exc:
            record = {
                "model_id": "C",
                "status": "failed",
                "veto_reasons": [f"{type(exc).__name__}: {exc}"],
                "stress_target_failure_only": True,
            }
            bucket = make_timing_bucket("hmc_kernel", 0.0)
        model_records.append(record)
        timing_buckets.append(bucket)
        if record["status"] != "passed":
            raise RuntimeError(f"Model C stress target failed: {record['veto_reasons']}")
    elif args.stop_after != "C":
        skipped_models.append({"model_id": "C", "reason": f"stop_after_{args.stop_after}"})
    else:
        skipped_models.append({"model_id": "C", "reason": "model_b_not_passed"})

    final_status = "passed"
    if args.stop_after != "C":
        final_status = "passed_bounded_stop_after"
    nonfinite_counts = {
        record["model_id"]: {
            "value_score": record.get("value_score", {}).get("nonfinite_count"),
            "hmc_samples": record.get("hmc", {}).get("nonfinite_sample_count"),
        }
        for record in model_records
    }
    write_partial_result_snapshot(
        paths["partial"],
        PartialResultSnapshot(
            worker_id=manifest.worker_id,
            stage="model_suite_complete",
            status=final_status,
            payload={
                "executed_model_order": [record["model_id"] for record in model_records],
                "skipped_models": skipped_models,
            },
            nonfinite_count=sum(
                int(value or 0)
                for row in nonfinite_counts.values()
                for value in row.values()
                if value is not None
            ),
        ),
    )
    return {
        "artifact_type": "bayesfilter_model_suite_hmc_qualification_summary",
        "program_signature": PROGRAM_SIGNATURE,
        "status": final_status,
        "stale_match_payload": manifest.stale_match_payload,
        "git": {"commit": git_commit, "dirty_state": git_dirty_state},
        "cpu_gpu_status": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "tensorflow_visible_gpus": VISIBLE_GPUS_AFTER_IMPORT,
        },
        "execution_design": {
            "final_hmc_evidence_path": "bayesfilter.inference.run_full_chain_tfp_hmc",
            "full_chain_config": "bayesfilter.inference.FullChainHMCConfig",
            "robust_artifacts": True,
            "old_smoke_helpers_final_evidence": False,
            "old_smoke_helper_functions_not_called": [
                "run_qr_static_lgssm_hmc_smoke",
                "run_model_b_nonlinear_svd_cut4_hmc_smoke",
            ],
        },
        "planned_model_order": list(MODEL_ORDER),
        "executed_model_order": [record["model_id"] for record in model_records],
        "skipped_models": skipped_models,
        "models": model_records,
        "nonfinite_counts": nonfinite_counts,
        "timing_buckets": [bucket.__dict__ for bucket in timing_buckets],
        "summary_signature": program_signature(
            {
                "program_signature": PROGRAM_SIGNATURE,
                "model_order": [record["model_id"] for record in model_records],
                "model_statuses": [record["status"] for record in model_records],
            }
        ),
        "nonclaims": _nonclaims(),
    }


def _run_model(
    paths: Mapping[str, Path],
    manifest: Any,
    model_id: str,
    adapter: Any,
    args: argparse.Namespace,
    *,
    seed_offset: int,
) -> tuple[dict[str, Any], Any]:
    append_stage_event(
        paths["events"],
        stage=f"model_{model_id}_start",
        status="ok",
        timestamp=_timestamp(),
        payload={"target_scope": adapter.value_score_capability().target_scope},
    )
    started = time.perf_counter()
    veto_reasons: list[str] = []
    branch = _branch_summary(adapter)
    if branch is not None and branch["ok_count"] != branch["total_count"]:
        veto_reasons.append("branch_summary_not_all_ok")

    chain_state = _chain_points(adapter)

    @tf.function(jit_compile=True, reduce_retracing=True)
    def chain_value_score(values: tf.Tensor):
        return static_unroll_chain_value_and_score(
            adapter,
            values,
            use_xla=True,
            target_scope=adapter.value_score_capability().target_scope,
        )

    value_started = time.perf_counter()
    chain_values, chain_scores = chain_value_score(chain_state)
    value_score_s = time.perf_counter() - value_started
    chain_values_np = chain_values.numpy()
    chain_scores_np = chain_scores.numpy()
    value_score_nonfinite = int(
        np.size(chain_values_np)
        - np.count_nonzero(np.isfinite(chain_values_np))
        + np.size(chain_scores_np)
        - np.count_nonzero(np.isfinite(chain_scores_np))
    )
    if value_score_nonfinite:
        veto_reasons.append("nonfinite_value_score")
    append_heartbeat(
        paths["events"],
        worker_id=manifest.worker_id,
        stage=f"model_{model_id}_value_score",
        timestamp=_timestamp(),
        payload={"nonfinite_count": value_score_nonfinite},
    )

    hmc_config = FullChainHMCConfig(
        num_results=int(args.num_results),
        num_burnin_steps=int(args.num_burnin_steps),
        step_size=_step_sizes()[model_id],
        num_leapfrog_steps=int(args.num_leapfrog_steps),
        seed=(20260608, 70 + seed_offset),
        use_xla=True,
        trace_policy="standard",
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope=adapter.value_score_capability().target_scope,
    )
    hmc_started = time.perf_counter()
    hmc = run_full_chain_tfp_hmc(adapter, adapter.initial_parameters, hmc_config)
    hmc_s = time.perf_counter() - hmc_started
    nonfinite_sample_count = int(hmc.diagnostics["nonfinite_sample_count"].numpy())
    finite_sample_count = int(hmc.diagnostics["finite_sample_count"].numpy())
    if nonfinite_sample_count:
        veto_reasons.append("nonfinite_hmc_samples")
    append_heartbeat(
        paths["events"],
        worker_id=manifest.worker_id,
        stage=f"model_{model_id}_full_chain_hmc",
        timestamp=_timestamp(),
        payload={
            "finite_sample_count": finite_sample_count,
            "nonfinite_sample_count": nonfinite_sample_count,
        },
    )
    status = "passed" if not veto_reasons else "failed"
    record = {
        "model_id": model_id,
        "status": status,
        "target_scope": adapter.value_score_capability().target_scope,
        "adapter_signature": adapter.adapter_signature(),
        "parameter_names": list(adapter.parameter_names()),
        "value_score_authority": adapter.value_score_capability().value_score_authority,
        "branch_summary": branch,
        "value_score": {
            "chain_values": chain_values_np.tolist(),
            "chain_score_shape": list(chain_scores_np.shape),
            "nonfinite_count": value_score_nonfinite,
            "runtime_s": value_score_s,
        },
        "hmc": {
            "runtime": hmc.metadata["runtime"],
            "jit_compile": hmc.metadata["jit_compile"],
            "target_scope": hmc.metadata["target_scope"],
            "program_signature": hmc.metadata["program_signature"],
            "sample_shape": [int(dim) for dim in hmc.samples.shape],
            "finite_sample_count": finite_sample_count,
            "nonfinite_sample_count": nonfinite_sample_count,
            "acceptance_rate": _maybe_float_tensor(hmc.diagnostics.get("acceptance_rate")),
            "divergence_status": hmc.diagnostics["divergence_status"],
            "divergence_count": hmc.diagnostics["divergence_count"],
            "nonclaims": hmc.metadata["nonclaims"],
        },
        "veto_reasons": veto_reasons,
        "runtime_s": time.perf_counter() - started,
    }
    write_partial_result_snapshot(
        paths["partial"],
        PartialResultSnapshot(
            worker_id=manifest.worker_id,
            stage=f"model_{model_id}_complete",
            status=status,
            payload={
                "model_id": model_id,
                "finite_sample_count": finite_sample_count,
                "veto_reasons": veto_reasons,
            },
            nonfinite_count=value_score_nonfinite + nonfinite_sample_count,
            first_failure={"veto_reasons": veto_reasons} if veto_reasons else None,
        ),
    )
    append_stage_event(
        paths["events"],
        stage=f"model_{model_id}_complete",
        status=status,
        timestamp=_timestamp(),
        payload={"veto_reasons": veto_reasons},
    )
    return record, make_timing_bucket("hmc_kernel", hmc_s)


def _model_a_value_sanity() -> Mapping[str, Any]:
    observations = model_a_observations_tf()
    model = make_affine_gaussian_structural_oracle_tf()
    step = dense_projection_first_step(model, observations[0])
    value = float(step.log_likelihood.numpy())
    deterministic_residual = float(step.deterministic_residual.numpy())
    if not np.isfinite(value) or not np.isfinite(deterministic_residual):
        raise RuntimeError("Model A value sanity produced nonfinite diagnostics")
    return {
        "fixture": "model_a_affine_gaussian_structural_oracle",
        "role": "exact-value structural sanity, not posterior evidence",
        "first_observation_log_likelihood": value,
        "deterministic_residual": deterministic_residual,
        "nonfinite_count": 0,
    }


def _branch_summary(adapter: Any) -> dict[str, Any] | None:
    branch_fn = getattr(adapter, "branch_summary", None)
    if branch_fn is None:
        return None
    branch = branch_fn()
    payload = {
        "total_count": _to_int(_branch_get(branch, "total_count")),
        "ok_count": _to_int(_branch_get(branch, "ok_count")),
        "active_floor_count": _to_int(_branch_get(branch, "active_floor_count")),
        "weak_spectral_gap_count": _to_int(_branch_get(branch, "weak_spectral_gap_count")),
        "nonfinite_count": _to_int(_branch_get(branch, "nonfinite_count")),
        "failure_labels": list(_branch_get(branch, "failure_labels")),
        "max_deterministic_residual": _to_float(
            _branch_get(branch, "max_deterministic_residual")
        ),
        "max_support_residual": _to_float(_branch_get(branch, "max_support_residual")),
    }
    for optional in (
        "other_blocked_count",
        "max_structural_null_covariance_residual",
        "max_fixed_null_derivative_residual",
        "max_structural_null_count",
    ):
        marker = object()
        value = _branch_get(branch, optional, default=marker)
        if value is not marker:
            payload[optional] = _to_float(value)
    return payload


def _branch_get(branch: Any, key: str, *, default: Any = None) -> Any:
    if isinstance(branch, Mapping):
        if key in branch:
            return branch[key]
        return default
    if hasattr(branch, key):
        return getattr(branch, key)
    return default


def _chain_points(adapter: Any) -> tf.Tensor:
    initial = tf.convert_to_tensor(adapter.initial_parameters, dtype=tf.float64)
    delta = tf.fill(tf.shape(initial), tf.constant(0.01, dtype=tf.float64))
    return tf.stack([initial, initial + delta], axis=0)


def _should_run_model_c(model_records: list[Mapping[str, Any]], stop_after: str) -> bool:
    if stop_after != "C":
        return False
    for record in model_records:
        if record.get("model_id") == "B":
            return record.get("status") == "passed"
    return False


def _prepare_artifact_root(artifact_root: Path, *, force: bool) -> dict[str, Path]:
    artifact_root.mkdir(parents=True, exist_ok=True)
    entries = list(artifact_root.iterdir())
    unknown = [entry for entry in entries if entry.name not in EXPECTED_ARTIFACT_FILES]
    if unknown:
        names = ", ".join(sorted(entry.name for entry in unknown))
        raise SystemExit(f"artifact root has unknown entries; refusing cleanup: {names}")
    if entries and not force:
        raise SystemExit(f"artifact root is nonempty; use --force: {artifact_root}")
    if force:
        for entry in entries:
            if not entry.is_file():
                raise SystemExit(f"expected artifact path is not a file: {entry}")
            entry.unlink()
    return {
        "manifest": artifact_root / "worker_manifest.json",
        "events": artifact_root / "stage_events.jsonl",
        "partial": artifact_root / "partial_snapshot.json",
        "result": artifact_root / "worker_result.json",
        "reducer": artifact_root / "reducer_status.json",
        "summary": artifact_root / "summary.json",
    }


def _capability(
    *,
    target_scope: str,
    evidence_path: str,
    extra_nonclaims: tuple[str, ...] = (),
) -> ValueScoreCapability:
    return ValueScoreCapability(
        value_score_authority="graph_native",
        xla_hmc_ready=True,
        runtime_backend="tensorflow",
        evidence_path=evidence_path,
        target_scope=target_scope,
        nonclaims=(
            "bounded BayesFilter model-suite engineering qualification only",
            "not sampler convergence evidence",
            "not posterior validity evidence",
            *extra_nonclaims,
        ),
    )


def _step_sizes() -> dict[str, float]:
    return {"A": 0.02, "QR": 0.01, "B": 0.0005, "C": 0.0005}


def _nonclaims() -> tuple[str, ...]:
    return (
        "bounded BayesFilter model-suite engineering qualification only",
        "no sampler convergence claim",
        "no posterior validity claim",
        "no DSGE readiness claim",
        "no real-NK readiness claim",
        "no GPU readiness claim",
        "no score-matching readiness claim",
        "no performance superiority claim",
    )


def _git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "unknown"
    return result.stdout.strip()


def _git_dirty_state() -> Mapping[str, Any]:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--untracked-files=all"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        return {"available": False, "error": str(exc), "is_dirty": None, "short_status": []}
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return {
        "available": True,
        "is_dirty": bool(lines),
        "entry_count": len(lines),
        "short_status": lines,
    }


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _maybe_float_tensor(value: Any) -> float | None:
    if value is None:
        return None
    if hasattr(value, "numpy"):
        return float(value.numpy())
    return float(value)


def _to_float(value: Any) -> float:
    if hasattr(value, "numpy"):
        return float(value.numpy())
    return float(value)


def _to_int(value: Any) -> int:
    if hasattr(value, "numpy"):
        return int(value.numpy())
    return int(value)


if __name__ == "__main__":
    raise SystemExit(main())
