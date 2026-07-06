from __future__ import annotations

import inspect
import json
import os

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

import bayesfilter
from bayesfilter.inference import (
    RetainedSampleHMCArchiveConfig,
    ValueScoreCapability,
    build_retained_sample_hmc_archive_runner,
)


class ReviewedBatchedGaussianAdapter:
    parameter_dim = 2

    def adapter_signature(self) -> str:
        return "retained-sample-archive-reviewed-batched-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_retained_sample_archive_runner.py",
            target_scope="retained_sample_archive_hmc_gaussian",
            nonclaims=("tiny retained-sample archive HMC engineering fixture only",),
            full_chain_xla_diagnostic_ready=True,
        )

    def log_prob_and_grad(self, theta: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        values = tf.convert_to_tensor(theta, dtype=tf.float64)
        return -0.5 * tf.reduce_sum(tf.square(values), axis=-1), -values


class TargetOnlyXLAGaussianAdapter(ReviewedBatchedGaussianAdapter):
    def adapter_signature(self) -> str:
        return "retained-sample-archive-target-only-xla-gaussian-v1"

    def value_score_capability(self) -> ValueScoreCapability:
        return ValueScoreCapability(
            value_score_authority="graph_native",
            xla_hmc_ready=True,
            runtime_backend="tensorflow",
            evidence_path="tests/test_hmc_retained_sample_archive_runner.py",
            target_scope="retained_sample_archive_hmc_target_only",
            nonclaims=("target-only XLA fixture; no full-chain XLA authority",),
        )


def _initial_state() -> tf.Tensor:
    return tf.constant(
        [[0.1, -0.2], [0.2, 0.1], [-0.1, 0.3]],
        dtype=tf.float64,
    )


def _config(*, use_xla: bool = False) -> RetainedSampleHMCArchiveConfig:
    return RetainedSampleHMCArchiveConfig(
        num_results=4,
        num_burnin_steps=1,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260624, 30),
        use_xla=use_xla,
        target_scope="retained_sample_archive_hmc_gaussian",
        chain_execution_mode="tf_function",
    )


def test_retained_sample_archive_runner_writes_one_private_sample_shard(tmp_path) -> None:
    runner = build_retained_sample_hmc_archive_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False),
    )

    result = runner.run(
        archive_dir=tmp_path / "samples",
        archive_label="unit",
        metadata={"run_id": "unit-test"},
        seed=(20260624, 31),
        overwrite=True,
    )

    assert not hasattr(result, "samples")
    assert result.final_state.shape == (3, 2)
    assert result.final_target_log_prob.shape == (3,)
    assert int(result.final_index.numpy()) == 4
    assert bool(result.diagnostics["retained_samples_all_finite"].numpy())
    assert bool(result.diagnostics["final_state_all_finite"].numpy())
    assert bool(result.diagnostics["final_index_matches_num_results"].numpy())
    assert int(result.diagnostics["valid_sample_count"].numpy()) == 4
    assert int(result.diagnostics["nonfinite_retained_sample_count"].numpy()) == 0
    assert result.diagnostics["returns_samples"] is False
    assert result.diagnostics["uses_sample_chain"] is False
    assert result.diagnostics["hmc_execution_call_count"] == 1
    assert result.diagnostics["macrofinance_visible_chunk_count"] == 0
    assert result.diagnostics["sampler_diagnostics_policy"] == "public_safe_summary"
    assert np.isfinite(float(result.diagnostics["acceptance_rate"].numpy()))
    assert 0.0 <= float(result.diagnostics["acceptance_rate"].numpy()) <= 1.0
    assert tuple(result.diagnostics["acceptance_rate_by_chain"].shape) == (3,)
    sampler_health = result.diagnostics["sampler_health_diagnostics"]
    assert sampler_health["available"] is True
    assert sampler_health["diagnostic_role"] == (
        "hmc_health_diagnostics_not_native_divergence"
    )
    assert int(sampler_health["acceptance_decision_count"].numpy()) == 12
    assert int(sampler_health["log_accept_ratio"]["finite_count"].numpy()) == 12
    assert int(sampler_health["log_accept_ratio"]["nonfinite_count"].numpy()) == 0
    assert int(sampler_health["target_log_prob"]["finite_count"].numpy()) == 12
    assert int(sampler_health["target_log_prob"]["nonfinite_count"].numpy()) == 0
    assert result.diagnostics["divergence_status"] in {
        "available",
        "not_exposed_by_kernel",
    }
    if result.diagnostics["divergence_status"] == "available":
        assert result.diagnostics["divergence_source"] == (
            "native_boolean_tfp_kernel_result"
        )
    else:
        assert result.diagnostics["divergence_count"] is None

    metadata = dict(result.metadata)
    assert metadata["single_call_retained_archive_runner"] is True
    assert metadata["hmc_execution_call_count"] == 1
    assert metadata["uses_sample_chain"] is False
    assert metadata["returns_samples"] is False
    assert metadata["macrofinance_visible_chunk_count"] == 0
    assert metadata["private_archive_shard_count"] == 1
    assert metadata["compile_trace_count"] == 1
    assert metadata["sampler_diagnostics_policy"] == "public_safe_summary"
    assert metadata["sampler_health_telemetry"] == "public_safe_aggregate_counts"
    assert metadata["dynamic_inputs"] == (
        "current_state",
        "seed",
        "kernel_step_scalar",
    )

    summary = dict(result.archive_summary)
    assert summary["artifact_type"] == "bayesfilter_retained_sample_hmc_archive_summary"
    assert summary["private_archive_shard_count"] == 1
    assert summary["sample_shard_count"] == 1
    assert summary["non_sample_sidecar_count"] == 3
    assert summary["retained_sample_count"] == 4
    assert summary["total_nonfinite_valid_sample_count"] == 0
    assert summary["private_paths_publicized"] is False
    assert summary["private_sample_or_state_descriptors_publicized"] is False
    assert summary["public_summary_contains_raw_values"] is False
    assert summary["public_summary_contains_kernel_payload"] is False
    assert summary["privacy_contract"]["public_summary_contains_step_size"] is False
    assert summary["privacy_contract"]["public_summary_contains_leapfrog_count"] is False
    assert summary["privacy_contract"]["public_summary_contains_mass_matrix"] is False

    forbidden = (
        "retained_samples.tftensor",
        "final_state.tftensor",
        "final_target_log_prob.tftensor",
        "\"path\"",
        "\"shape\"",
        "\"dtype\"",
        "\"sample_sha256\"",
        "\"final_state_sha256\"",
        "\"step_size\"",
        "\"num_leapfrog_steps\"",
        "\"mass_matrix\"",
    )
    summary_text = json.dumps(summary, sort_keys=True)
    assert not any(token in summary_text for token in forbidden)

    private_manifest_path = tmp_path / "samples" / "unit_private_manifest.json"
    private_manifest = json.loads(private_manifest_path.read_text(encoding="utf-8"))
    assert private_manifest["sample_shard_count"] == 1
    assert len(private_manifest["sample_shards"]) == 1
    private_diagnostics = private_manifest["diagnostics_private_metadata"]
    assert private_diagnostics["sampler_health_diagnostics"]["available"] is True
    assert private_diagnostics["sampler_health_diagnostics"][
        "acceptance_decision_count"
    ] == 12
    assert private_diagnostics["divergence_status"] in {
        "available",
        "not_exposed_by_kernel",
    }
    assert (tmp_path / "samples" / "unit_retained_samples.tftensor").exists()
    assert (tmp_path / "samples" / "unit_final_state.tftensor").exists()
    assert (tmp_path / "samples" / "unit_final_target_log_prob.tftensor").exists()


def test_retained_sample_archive_runner_xla_compiles_tiny_contract(tmp_path) -> None:
    runner = build_retained_sample_hmc_archive_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=True),
    )

    result = runner.run(
        archive_dir=tmp_path / "xla",
        archive_label="unit_xla",
        seed=(20260624, 32),
        overwrite=True,
    )

    assert result.metadata["jit_compile"] is True
    assert result.metadata["compile_trace_count"] == 1
    assert result.metadata["hmc_execution_call_count"] == 1
    assert bool(result.diagnostics["final_index_matches_num_results"].numpy())


def test_retained_sample_archive_runner_rejects_invalid_contracts_and_inputs(tmp_path) -> None:
    with pytest.raises(ValueError, match="num_results"):
        RetainedSampleHMCArchiveConfig(
            num_results=0,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
        )
    with pytest.raises(ValueError, match="chain_execution_mode"):
        RetainedSampleHMCArchiveConfig(
            num_results=2,
            num_burnin_steps=0,
            step_size=0.05,
            num_leapfrog_steps=1,
            seed=(1, 2),
            use_xla=True,
            chain_execution_mode="eager",
        )

    runner = build_retained_sample_hmc_archive_runner(
        ReviewedBatchedGaussianAdapter(),
        _initial_state(),
        _config(use_xla=False),
    )
    with pytest.raises(ValueError, match="current_state shape"):
        runner.run(archive_dir=tmp_path / "bad_state", archive_label="bad", current_state=tf.zeros((2, 2), dtype=tf.float64))
    with pytest.raises(ValueError, match="seed"):
        runner.run(archive_dir=tmp_path / "bad_seed", archive_label="bad", seed=(1, 2, 3))
    with pytest.raises(ValueError, match="step_size"):
        runner.run(archive_dir=tmp_path / "bad_step", archive_label="bad", step_size=tf.ones((1,), dtype=tf.float64))


def test_retained_sample_archive_runner_preserves_xla_authority_gate() -> None:
    config = RetainedSampleHMCArchiveConfig(
        num_results=2,
        num_burnin_steps=0,
        step_size=0.05,
        num_leapfrog_steps=1,
        seed=(20260624, 33),
        use_xla=True,
        target_scope="retained_sample_archive_hmc_target_only",
    )

    with pytest.raises(ValueError, match="target-only XLA readiness is not sufficient"):
        build_retained_sample_hmc_archive_runner(
            TargetOnlyXLAGaussianAdapter(),
            _initial_state(),
            config,
        )


def test_retained_sample_archive_runner_public_exports_and_no_sample_chain_dependency() -> None:
    import bayesfilter.inference.hmc as hmc_module

    assert bayesfilter.RetainedSampleHMCArchiveConfig is RetainedSampleHMCArchiveConfig
    assert (
        bayesfilter.build_retained_sample_hmc_archive_runner
        is build_retained_sample_hmc_archive_runner
    )
    assert "RetainedSampleHMCArchiveConfig" in bayesfilter.__all__
    assert "build_retained_sample_hmc_archive_runner" in bayesfilter.__all__

    source = inspect.getsource(hmc_module.RetainedSampleHMCArchiveRunner)
    assert "tf.while_loop" in source
    assert "sample_chain(" not in source
