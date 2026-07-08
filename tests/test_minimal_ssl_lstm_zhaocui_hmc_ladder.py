from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from pathlib import Path

import pytest
import tensorflow as tf


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT / "docs/benchmarks/benchmark_minimal_ssl_lstm_zhaocui_hmc_ladder_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "minimal_ssl_lstm_zhaocui_hmc_ladder",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_phase1_adapter_returns_finite_deterministic_value_and_score() -> None:
    harness = _load_harness()
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)
    theta = harness.initial_offset_state(1.0e-3)

    value, score = adapter.log_prob_and_grad(theta)
    repeated_value, repeated_score = adapter.log_prob_and_grad(tf.identity(theta))

    assert value.shape == ()
    assert score.shape == (24,)
    assert bool(tf.reduce_all(tf.math.is_finite(value)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(score)).numpy())
    assert float(tf.reduce_max(tf.abs(value - repeated_value)).numpy()) <= 1.0e-12
    assert float(tf.reduce_max(tf.abs(score - repeated_score)).numpy()) <= 1.0e-12


def test_phase1_adapter_batch_shape_and_capability_metadata() -> None:
    harness = _load_harness()
    adapter = harness.MinimalZhaoCuiHMCTargetAdapter(prior_scale=5.0)
    theta = harness.initial_offset_state(1.0e-3)
    batch = tf.stack([theta, theta], axis=0)

    values, scores = adapter.log_prob_and_grad(batch)
    capability = adapter.value_score_capability()

    assert values.shape == (2,)
    assert scores.shape == (2, 24)
    assert bool(tf.reduce_all(tf.math.is_finite(values)).numpy())
    assert bool(tf.reduce_all(tf.math.is_finite(scores)).numpy())
    assert capability.value_score_authority == "graph_native"
    assert capability.runtime_backend == "tensorflow"
    assert capability.target_scope == adapter.target_scope
    assert capability.full_chain_xla_diagnostic_ready is True
    assert "not HMC convergence evidence" in capability.nonclaims


def test_phase1_artifact_records_debug_reference_boundaries() -> None:
    harness = _load_harness()
    artifact = harness.build_phase1_adapter_artifact(command=("pytest", "phase1-adapter"))

    assert artifact["status"] == "passed"
    assert artifact["phase"] == "PHASE1"
    assert artifact["artifact_role"] == "target_adapter_debug_reference"
    assert artifact["filter_name"] == "zhaocui_fixed"
    assert artifact["fixture"]["latent_dim"] == 1
    assert artifact["fixture"]["hidden_dim"] == 1
    assert artifact["fixture"]["observation_dim"] == 1
    assert artifact["fixture"]["horizon"] == 2
    assert artifact["fixture"]["parameter_dim"] == 24
    assert artifact["hard_vetoes"] == []
    assert artifact["target_diagnostics"]["value_finite"] is True
    assert artifact["target_diagnostics"]["score_finite"] is True
    assert artifact["target_diagnostics"]["score_shape"] == [24]
    assert artifact["target_diagnostics"]["batch_score_shape"] == [2, 24]
    assert artifact["target_diagnostics"]["determinism_passed"] is True
    assert artifact["capability"]["value_score_authority"] == "graph_native"
    assert artifact["run_manifest"]["jit_compile"] is False
    assert "not an HMC sample or canary result" in artifact["nonclaims"]
    assert "not default-readiness evidence" in artifact["nonclaims"]


def test_phase1_cli_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase1_adapter.json"
    markdown_output = tmp_path / "phase1_adapter.md"

    exit_code = harness.main(
        [
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
        ]
    )

    assert exit_code == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert payload["status"] == "passed"
    assert payload["target_diagnostics"]["score_shape"] == [24]
    assert math.isfinite(float(payload["target_diagnostics"]["log_prob"]))
    assert "CPU-hidden non-JIT Phase 1 adapter admission" in payload["run_manifest"]["debug_reference_exception"]
    assert "Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 1" in summary


def test_phase2_canary_builder_records_tiny_hmc_debug_boundaries() -> None:
    harness = _load_harness()
    artifact = harness.build_phase2_canary_artifact(
        num_results=2,
        num_burnin_steps=1,
        step_size=1.0e-5,
        num_leapfrog_steps=1,
        seed=(20260706, 2201),
        command=("pytest", "phase2-canary"),
    )

    assert artifact["phase"] == "PHASE2"
    assert artifact["artifact_role"] == "tiny_hmc_canary_debug_reference"
    assert artifact["filter_name"] == "zhaocui_fixed"
    assert artifact["hmc_settings"]["use_xla"] is False
    assert artifact["hmc_settings"]["jit_compile"] is False
    assert artifact["hmc_settings"]["chain_execution_mode"] == "tf_function"
    assert artifact["hmc_settings"]["seed"] == [20260706, 2201]
    assert artifact["initial_target"]["value_finite"] is True
    assert artifact["initial_target"]["score_finite"] is True
    assert artifact["initial_target"]["score_shape"] == [24]
    assert artifact["metric_roles"]["acceptance_rate"] == "explanatory_only_in_tiny_canary"
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert "not R-hat or ESS evidence" in artifact["nonclaims"]
    if artifact["status"] == "passed":
        assert artifact["hard_vetoes"] == []
        assert artifact["hmc_runtime"]["samples_all_finite"] is True
        assert artifact["hmc_runtime"]["sample_shape"] == [2, 24]


def test_phase2_canary_cli_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase2_canary.json"
    markdown_output = tmp_path / "phase2_canary.md"

    exit_code = harness.main(
        [
            "--mode",
            "phase2-canary",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
            "--num-results",
            "2",
            "--num-burnin-steps",
            "1",
            "--step-size",
            "1e-5",
            "--num-leapfrog-steps",
            "1",
            "--seed",
            "20260706",
            "2201",
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert exit_code == (0 if payload["status"] == "passed" else 1)
    assert payload["phase"] == "PHASE2"
    assert payload["hmc_settings"]["use_xla"] is False
    assert payload["hmc_settings"]["jit_compile"] is False
    assert payload["run_manifest"]["random_seeds"]["hmc_seed"] == [20260706, 2201]
    assert "CPU-hidden non-JIT Phase 2 HMC canary" in payload["run_manifest"]["debug_reference_exception"]
    assert "Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 2 Canary" in summary


def test_phase4_short_ladder_records_predeclared_seed_rows() -> None:
    harness = _load_harness()
    artifact = harness.build_phase4_short_ladder_artifact(
        command=("pytest", "phase4-short-ladder"),
    )

    assert artifact["phase"] == "PHASE4"
    assert artifact["artifact_role"] == "short_replicated_debug_ladder"
    assert artifact["predeclared_settings"]["seeds"] == [
        [20260706, 2401],
        [20260706, 2402],
        [20260706, 2403],
    ]
    assert artifact["predeclared_settings"]["num_results"] == 2
    assert artifact["predeclared_settings"]["num_burnin_steps"] == 1
    assert artifact["predeclared_settings"]["num_leapfrog_steps"] == 1
    assert artifact["predeclared_settings"]["step_size"] == 1.0e-5
    assert artifact["predeclared_settings"]["use_xla"] is False
    assert artifact["predeclared_settings"]["jit_compile"] is False
    assert artifact["metric_roles"]["acceptance_rate"] == "explanatory_only_in_short_debug_ladder"
    assert artifact["inference_status"]["statistically_supported_ranking"] == "not_claimed"
    assert artifact["inference_status"]["default_readiness"] == "not_checked"
    assert artifact["run_manifest"]["quiet_log_path"].endswith("phase4_short_ladder_cpu_hidden_2026-07-06.log")
    assert "Phase 4 short replicated debug ladder only" in artifact["nonclaims"]
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert len(artifact["candidate_rows"]) == 3
    for row in artifact["candidate_rows"]:
        assert row["hmc_settings"]["use_xla"] is False
        assert row["hmc_settings"]["jit_compile"] is False
        assert row["hmc_runtime"]["sample_shape"] == [2, 24]


def test_phase3_gpu_xla_smoke_fails_closed_when_gpu_hidden(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    artifact = harness.build_phase3_gpu_xla_smoke_artifact(
        trusted_gpu_xla_approval=True,
        command=("pytest", "phase3-gpu-xla-smoke"),
    )

    assert artifact["phase"] == "PHASE3"
    assert artifact["artifact_role"] == "trusted_gpu_xla_runtime_smoke"
    assert artifact["status"] == "failed"
    assert artifact["hmc_settings"]["use_xla"] is True
    assert artifact["hmc_settings"]["jit_compile"] is True
    assert artifact["hmc_settings"]["trusted_gpu_xla_approval"] is True
    assert "gpu_hidden_for_trusted_gpu_xla_smoke" in artifact["hard_vetoes"]
    assert artifact["hmc_runtime"]["not_run_reason"] == "preflight_hard_veto"
    assert artifact["hmc_runtime"]["sample_shape"] is None
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert "not GPU/XLA production-readiness evidence" in artifact["nonclaims"]


def test_phase3_gpu_xla_cli_requires_explicit_approval(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")

    with pytest.raises(RuntimeError, match="requires --trusted-gpu-xla-approval"):
        harness.main(
            [
                "--mode",
                "phase3-gpu-xla-smoke",
                "--output",
                str(tmp_path / "phase3.json"),
                "--markdown-output",
                str(tmp_path / "phase3.md"),
            ]
        )


def test_phase4_short_ladder_cli_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase4_ladder.json"
    markdown_output = tmp_path / "phase4_ladder.md"

    exit_code = harness.main(
        [
            "--mode",
            "phase4-short-ladder",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert exit_code == (0 if payload["status"] == "passed" else 1)
    assert payload["phase"] == "PHASE4"
    assert payload["predeclared_settings"]["seeds"] == [
        [20260706, 2401],
        [20260706, 2402],
        [20260706, 2403],
    ]
    assert payload["decision_table"]["decision"] == "short debug ladder hard-veto classification only"
    assert payload["run_manifest"]["quiet_log_path"].endswith("phase4_short_ladder_cpu_hidden_2026-07-06.log")
    assert "CPU-hidden non-JIT Phase 4 short debug ladder" in payload["run_manifest"]["debug_reference_exception"]
    assert "Minimal SSL-LSTM Zhao-Cui HMC Ladder Phase 4 Short Ladder" in summary


def test_phase4_short_ladder_rejects_override_drift() -> None:
    harness = _load_harness()

    with pytest.raises(ValueError, match="Phase 4 num_results is fixed"):
        harness.build_phase4_short_ladder_artifact(num_results=3)

    with pytest.raises(ValueError, match="Phase 4 ladder seeds are fixed"):
        harness.build_phase4_short_ladder_artifact(
            seeds=((20260706, 2401), (20260706, 2402))
        )


def test_phase5_longer_gpu_xla_ladder_fails_closed_when_gpu_hidden(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    artifact = harness.build_phase5_longer_gpu_xla_ladder_artifact(
        trusted_gpu_xla_approval=True,
        command=("pytest", "phase5-longer-gpu-xla-ladder"),
    )

    assert artifact["phase"] == "PHASE5"
    assert artifact["artifact_role"] == "trusted_gpu_xla_longer_hard_veto_diagnostics"
    assert artifact["status"] == "failed"
    assert artifact["predeclared_settings"]["seeds"] == [
        [20260706, 5101],
        [20260706, 5102],
        [20260706, 5103],
    ]
    assert artifact["predeclared_settings"]["num_results"] == 8
    assert artifact["predeclared_settings"]["num_burnin_steps"] == 4
    assert artifact["predeclared_settings"]["num_leapfrog_steps"] == 1
    assert artifact["predeclared_settings"]["step_size"] == 1.0e-5
    assert artifact["predeclared_settings"]["prior_scale"] == 5.0
    assert artifact["predeclared_settings"]["initial_offset_scale"] == 1.0e-3
    assert artifact["predeclared_settings"]["use_xla"] is True
    assert artifact["predeclared_settings"]["jit_compile"] is True
    assert artifact["predeclared_settings"]["trusted_gpu_xla_approval"] is True
    assert "gpu_hidden_for_trusted_gpu_xla_ladder" in artifact["hard_vetoes"]
    assert artifact["metric_roles"]["acceptance_rate"] == "explanatory_only_in_longer_ladder"
    assert artifact["metric_roles"]["rhat"] == "not_computed_in_longer_ladder"
    assert artifact["metric_roles"]["ess"] == "not_computed_in_longer_ladder"
    assert artifact["inference_status"]["statistically_supported_ranking"] == "not_claimed"
    assert artifact["inference_status"]["convergence"] == "not_checked"
    assert artifact["native_divergence_interpretation"].endswith("not zero divergences")
    assert "not HMC convergence evidence" in artifact["nonclaims"]
    assert "not GPU/XLA production-readiness evidence" in artifact["nonclaims"]
    assert len(artifact["candidate_rows"]) == 3
    for row in artifact["candidate_rows"]:
        assert row["status"] == "failed"
        assert row["not_run_reason"] == "preflight_hard_veto"
        assert row["hmc_settings"]["use_xla"] is True
        assert row["hmc_settings"]["jit_compile"] is True
        assert row["hmc_runtime"]["sample_shape"] is None


def test_phase5_longer_gpu_xla_ladder_rejects_override_drift() -> None:
    harness = _load_harness()

    with pytest.raises(ValueError, match="Phase 5 num_results is fixed"):
        harness.build_phase5_longer_gpu_xla_ladder_artifact(
            trusted_gpu_xla_approval=True,
            num_results=7,
        )

    with pytest.raises(ValueError, match="Phase 5 ladder seeds are fixed"):
        harness.build_phase5_longer_gpu_xla_ladder_artifact(
            trusted_gpu_xla_approval=True,
            seeds=((20260706, 5101),),
        )

    with pytest.raises(ValueError, match="Phase 5 prior_scale is fixed"):
        harness.build_phase5_longer_gpu_xla_ladder_artifact(
            trusted_gpu_xla_approval=True,
            prior_scale=4.0,
        )

    with pytest.raises(ValueError, match="Phase 5 initial_offset_scale is fixed"):
        harness.build_phase5_longer_gpu_xla_ladder_artifact(
            trusted_gpu_xla_approval=True,
            initial_offset_scale=2.0e-3,
        )


def test_phase5_gpu_xla_cli_requires_approval_and_fixed_seeds(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")

    with pytest.raises(RuntimeError, match="GPU/XLA HMC mode requires"):
        harness.main(
            [
                "--mode",
                "phase5-longer-gpu-xla-ladder",
                "--output",
                str(tmp_path / "phase5.json"),
                "--markdown-output",
                str(tmp_path / "phase5.md"),
            ]
        )

    with pytest.raises(RuntimeError, match="do not pass --seed"):
        harness.main(
            [
                "--mode",
                "phase5-longer-gpu-xla-ladder",
                "--trusted-gpu-xla-approval",
                "--seed",
                "20260706",
                "9999",
                "--output",
                str(tmp_path / "phase5.json"),
                "--markdown-output",
                str(tmp_path / "phase5.md"),
            ]
        )

    with pytest.raises(RuntimeError, match="do not pass --prior-scale"):
        harness.main(
            [
                "--mode",
                "phase5-longer-gpu-xla-ladder",
                "--trusted-gpu-xla-approval",
                "--prior-scale",
                "4.0",
                "--output",
                str(tmp_path / "phase5.json"),
                "--markdown-output",
                str(tmp_path / "phase5.md"),
            ]
        )

    with pytest.raises(RuntimeError, match="do not pass --initial-offset-scale"):
        harness.main(
            [
                "--mode",
                "phase5-longer-gpu-xla-ladder",
                "--trusted-gpu-xla-approval",
                "--initial-offset-scale",
                "0.002",
                "--output",
                str(tmp_path / "phase5.json"),
                "--markdown-output",
                str(tmp_path / "phase5.md"),
            ]
        )


def test_phase5_gpu_xla_cli_writes_fail_closed_json_and_markdown(
    tmp_path: Path,
    monkeypatch,
) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase5_ladder.json"
    markdown_output = tmp_path / "phase5_ladder.md"

    exit_code = harness.main(
        [
            "--mode",
            "phase5-longer-gpu-xla-ladder",
            "--trusted-gpu-xla-approval",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown_output),
            "--num-results",
            "8",
            "--num-burnin-steps",
            "4",
            "--step-size",
            "1e-5",
            "--num-leapfrog-steps",
            "1",
        ]
    )

    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown_output.read_text(encoding="utf-8")
    assert exit_code == 1
    assert payload["phase"] == "PHASE5"
    assert payload["status"] == "failed"
    assert "gpu_hidden_for_trusted_gpu_xla_ladder" in payload["hard_vetoes"]
    assert payload["run_manifest"]["quiet_log_path"].endswith("phase5_longer_gpu_xla_ladder_2026-07-06.log")
    assert payload["run_manifest"]["trust_basis"] == "explicit_user_approved_trusted_gpu_xla_longer_diagnostics"
    assert "Minimal SSL-LSTM Zhao-Cui HMC Next Phase 5 Longer GPU/XLA Ladder" in summary
