#!/usr/bin/env python
"""Bounded BayesFilter-only nonlinear SSM JIT/HMC engineering canary."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

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
from bayesfilter.nonlinear import (
    stable_nonlinear_filter_value_path_signature,
    tensorflow_nonlinear_value_path_contract,
    tf_svd_cut4_filter,
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
    make_nonlinear_accumulation_model_tf,
    model_b_observations_tf,
)


TARGET_SCOPE = "phase6_model_b_nonlinear_canary"
PROGRAM_SIGNATURE = "bayesfilter-phase6-nonlinear-ssm-jit-hmc-canary-v1"


class Phase6ModelBAdapter:
    parameter_dim = 3

    def __init__(self) -> None:
        self.target = ModelBNonlinearSVDTarget.default()

    def adapter_signature(self) -> str:
        return "phase6-model-b-nonlinear-svd-target-v1"

    def parameter_names(self) -> tuple[str, str, str]:
        return ("rho", "sigma", "beta")

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="scripts/run_nonlinear_ssm_phase6_engineering_canary.py",
            target_scope=TARGET_SCOPE,
            nonclaims=(
                "tiny BayesFilter engineering canary only",
                "not sampler convergence evidence",
                "not posterior validity evidence",
            ),
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return self.target.target_log_prob_and_grad(theta)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", required=True)
    parser.add_argument("--num-results", type=int, default=2)
    parser.add_argument("--num-burnin-steps", type=int, default=1)
    parser.add_argument("--step-size", type=float, default=0.0005)
    parser.add_argument("--num-leapfrog-steps", type=int, default=1)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    artifact_root = Path(args.artifact_root)
    if artifact_root.exists() and any(artifact_root.iterdir()) and not args.force:
        raise SystemExit(f"artifact root is nonempty; use --force: {artifact_root}")
    artifact_root.mkdir(parents=True, exist_ok=True)

    paths = {
        "manifest": artifact_root / "worker_manifest.json",
        "events": artifact_root / "stage_events.jsonl",
        "partial": artifact_root / "partial_snapshot.json",
        "result": artifact_root / "worker_result.json",
        "reducer": artifact_root / "reducer_status.json",
        "summary": artifact_root / "summary.json",
    }
    started = time.perf_counter()
    command = tuple(sys.argv if argv is None else [sys.argv[0], *argv])
    git_commit = _git_commit()
    normalized_config = {
        "fixture": "ModelBNonlinearSVDTarget.default",
        "target_scope": TARGET_SCOPE,
        "backend": "tf_svd_cut4",
        "num_results": int(args.num_results),
        "num_burnin_steps": int(args.num_burnin_steps),
        "step_size": float(args.step_size),
        "num_leapfrog_steps": int(args.num_leapfrog_steps),
        "seed": (20260608, 6),
        "cpu_only": True,
        "jit_compile": True,
        "trace_policy": "standard",
    }
    device_policy = {
        "mode": "cpu_only",
        "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "tensorflow_visible_gpus_after_import": [
            str(device) for device in tf.config.list_physical_devices("GPU")
        ],
    }
    thread_caps = {
        "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
        "TF_NUM_INTRAOP_THREADS": os.environ.get("TF_NUM_INTRAOP_THREADS"),
        "TF_NUM_INTEROP_THREADS": os.environ.get("TF_NUM_INTEROP_THREADS"),
    }
    worker_config = {
        "worker_kind": "phase6_engineering_canary",
        "worker_id": "phase6_cpu_canary",
        "budget": {
            "num_results": int(args.num_results),
            "num_burnin_steps": int(args.num_burnin_steps),
            "num_leapfrog_steps": int(args.num_leapfrog_steps),
        },
    }
    manifest = build_worker_manifest(
        worker_id="phase6_cpu_canary",
        command=command,
        pid=os.getpid(),
        git_commit=git_commit,
        artifact_root=artifact_root,
        normalized_config=normalized_config,
        program_signature=PROGRAM_SIGNATURE,
        device_policy=device_policy,
        thread_caps=thread_caps,
        worker_config=worker_config,
        environment={"CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES")},
    )
    write_worker_manifest(paths["manifest"], manifest)
    append_stage_event(
        paths["events"],
        stage="start",
        status="ok",
        timestamp=_timestamp(),
        payload={"git_commit": git_commit, "program_signature": PROGRAM_SIGNATURE},
    )

    try:
        summary = _run_canary(paths, manifest, args)
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
        atomic_write_json(paths["reducer"], reducer)
        summary["worker_runtime_s"] = runtime_s
        summary["reducer_status"] = reducer.status
        summary["reducer_reason"] = reducer.reason
        atomic_write_json(paths["summary"], summary)
        append_stage_event(
            paths["events"],
            stage="complete",
            status="ok",
            timestamp=_timestamp(),
            payload={"reducer_status": reducer.status, "runtime_s": runtime_s},
        )
        if reducer.status != "complete":
            raise RuntimeError(f"canary reducer status is {reducer.status!r}")
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
        append_stage_event(
            paths["events"],
            stage="failed",
            status="failed",
            timestamp=_timestamp(),
            payload={"error_type": type(exc).__name__, "error": str(exc)},
        )
        raise


def _run_canary(paths: dict[str, Path], manifest: Any, args: argparse.Namespace) -> dict[str, Any]:
    observations = model_b_observations_tf()
    model = make_nonlinear_accumulation_model_tf()
    contract = tensorflow_nonlinear_value_path_contract(
        fixture_name="phase6_model_b_value_fixture",
        observations=observations,
        model=model,
        backend="tf_svd_cut4",
        return_filtered=True,
    )

    @tf.function(jit_compile=True, reduce_retracing=True)
    def compiled_filter(obs: tf.Tensor):
        result = tf_svd_cut4_filter(
            obs,
            model,
            innovation_floor=tf.constant(1e-12, dtype=tf.float64),
            return_filtered=True,
        )
        regularization = result.diagnostics.regularization
        return (
            result.log_likelihood,
            tf.cast(regularization.floor_count, tf.float64),
            regularization.psd_projection_residual,
            result.filtered_means,
            result.filtered_covariances,
        )

    value_started = time.perf_counter()
    (
        value_log_likelihood_tensor,
        floor_count_tensor,
        psd_projection_residual_tensor,
        filtered_means,
        filtered_covariances,
    ) = compiled_filter(observations)
    value_s = time.perf_counter() - value_started
    value_log_likelihood = float(value_log_likelihood_tensor.numpy())
    if not np.isfinite(value_log_likelihood):
        raise RuntimeError("nonfinite compiled value-path log likelihood")
    append_heartbeat(
        paths["events"],
        worker_id=manifest.worker_id,
        stage="compiled_value",
        timestamp=_timestamp(),
        payload={"log_likelihood": value_log_likelihood},
    )
    write_partial_result_snapshot(
        paths["partial"],
        PartialResultSnapshot(
            worker_id=manifest.worker_id,
            stage="compiled_value",
            status="ok",
            payload={"log_likelihood": value_log_likelihood},
            nonfinite_count=0,
        ),
    )

    adapter = Phase6ModelBAdapter()
    chain = tf.constant(
        [
            [0.70, 0.25, 0.80],
            [0.68, 0.24, 0.78],
        ],
        dtype=tf.float64,
    )

    @tf.function(jit_compile=True, reduce_retracing=True)
    def chain_value_score(values: tf.Tensor):
        return static_unroll_chain_value_and_score(
            adapter,
            values,
            use_xla=True,
            target_scope=TARGET_SCOPE,
        )

    score_started = time.perf_counter()
    chain_values, chain_scores = chain_value_score(chain)
    value_score_s = time.perf_counter() - score_started
    chain_values_np = chain_values.numpy()
    chain_scores_np = chain_scores.numpy()
    if not np.all(np.isfinite(chain_values_np)) or not np.all(np.isfinite(chain_scores_np)):
        raise RuntimeError("nonfinite chain value/score")
    append_heartbeat(
        paths["events"],
        worker_id=manifest.worker_id,
        stage="chain_value_score",
        timestamp=_timestamp(),
        payload={"chain_count": int(chain.shape[0])},
    )
    write_partial_result_snapshot(
        paths["partial"],
        PartialResultSnapshot(
            worker_id=manifest.worker_id,
            stage="chain_value_score",
            status="ok",
            payload={
                "chain_value_count": int(chain_values.shape[0]),
                "chain_score_shape": tuple(int(dim) for dim in chain_scores.shape),
            },
            nonfinite_count=0,
        ),
    )

    hmc_config = FullChainHMCConfig(
        num_results=int(args.num_results),
        num_burnin_steps=int(args.num_burnin_steps),
        step_size=float(args.step_size),
        num_leapfrog_steps=int(args.num_leapfrog_steps),
        seed=(20260608, 6),
        use_xla=True,
        trace_policy="standard",
        adaptation_policy="fixed_kernel_no_adaptation",
        target_scope=TARGET_SCOPE,
    )
    hmc_started = time.perf_counter()
    hmc = run_full_chain_tfp_hmc(
        adapter,
        adapter.target.initial_parameters,
        hmc_config,
    )
    hmc_s = time.perf_counter() - hmc_started
    nonfinite_sample_count = int(hmc.diagnostics["nonfinite_sample_count"].numpy())
    finite_sample_count = int(hmc.diagnostics["finite_sample_count"].numpy())
    if nonfinite_sample_count != 0:
        raise RuntimeError(f"nonfinite HMC samples: {nonfinite_sample_count}")
    append_heartbeat(
        paths["events"],
        worker_id=manifest.worker_id,
        stage="full_chain_hmc",
        timestamp=_timestamp(),
        payload={"finite_sample_count": finite_sample_count},
    )
    write_partial_result_snapshot(
        paths["partial"],
        PartialResultSnapshot(
            worker_id=manifest.worker_id,
            stage="full_chain_hmc",
            status="ok",
            payload={
                "finite_sample_count": finite_sample_count,
                "sample_shape": tuple(int(dim) for dim in hmc.samples.shape),
            },
            nonfinite_count=nonfinite_sample_count,
        ),
    )

    timing_buckets = [
        make_timing_bucket("filter", value_s),
        make_timing_bucket("value_score", value_score_s),
        make_timing_bucket("hmc_kernel", hmc_s),
        make_timing_bucket("artifact_overhead", 0.0),
    ]
    return {
        "artifact_type": "bayesfilter_phase6_engineering_canary_summary",
        "program_signature": PROGRAM_SIGNATURE,
        "stale_match_payload": manifest.stale_match_payload,
        "cpu_gpu_status": {
            "CUDA_VISIBLE_DEVICES": os.environ.get("CUDA_VISIBLE_DEVICES"),
            "tensorflow_visible_gpus": [
                str(device) for device in tf.config.list_physical_devices("GPU")
            ],
        },
        "value_path": {
            "signature": stable_nonlinear_filter_value_path_signature(contract),
            "fixture_name": contract.fixture_name,
            "backend": contract.backend,
            "static_shape": contract.static_shape.signature_payload(),
            "log_likelihood": value_log_likelihood,
            "floor_count": float(floor_count_tensor.numpy()),
            "psd_projection_residual": float(psd_projection_residual_tensor.numpy()),
            "filtered_mean_shape": tuple(int(dim) for dim in filtered_means.shape),
            "filtered_covariance_shape": tuple(int(dim) for dim in filtered_covariances.shape),
        },
        "value_score": {
            "authority": adapter.value_score_capability().value_score_authority,
            "target_scope": adapter.value_score_capability().target_scope,
            "chain_values": chain_values_np.tolist(),
            "chain_score_shape": tuple(int(dim) for dim in chain_scores.shape),
            "nonfinite_count": 0,
        },
        "hmc": {
            "runtime": hmc.metadata["runtime"],
            "jit_compile": hmc.metadata["jit_compile"],
            "target_scope": hmc.metadata["target_scope"],
            "program_signature": hmc.metadata["program_signature"],
            "sample_shape": tuple(int(dim) for dim in hmc.samples.shape),
            "finite_sample_count": finite_sample_count,
            "nonfinite_sample_count": nonfinite_sample_count,
            "acceptance_rate": _maybe_float_tensor(hmc.diagnostics.get("acceptance_rate")),
            "divergence_status": hmc.diagnostics["divergence_status"],
            "divergence_count": hmc.diagnostics["divergence_count"],
            "nonclaims": hmc.metadata["nonclaims"],
        },
        "timing_buckets": [bucket.__dict__ for bucket in timing_buckets],
        "summary_signature": program_signature(
            {
                "program_signature": PROGRAM_SIGNATURE,
                "value_path_signature": stable_nonlinear_filter_value_path_signature(contract),
                "hmc_program_signature": hmc.metadata["program_signature"],
            }
        ),
        "nonclaims": (
            "bounded BayesFilter engineering canary only",
            "no sampler convergence claim",
            "no posterior validity claim",
            "no DSGE readiness claim",
            "no GPU readiness claim",
            "no performance superiority claim",
        ),
    }


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


def _timestamp() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def _maybe_float_tensor(value: Any) -> float | None:
    if value is None:
        return None
    if hasattr(value, "numpy"):
        return float(value.numpy())
    return float(value)


if __name__ == "__main__":
    raise SystemExit(main())
