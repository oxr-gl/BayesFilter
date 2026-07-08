from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import tensorflow as tf


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = (
    ROOT
    / "docs/benchmarks/"
    "benchmark_minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry_2026_07_06.py"
)


def _load_harness():
    spec = importlib.util.spec_from_file_location(
        "minimal_ssl_lstm_zhaocui_hmc_divergence_telemetry",
        HARNESS_PATH,
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_phase4_settings_match_subplan_contract() -> None:
    harness = _load_harness()
    settings = harness.reviewed_phase4_settings()

    assert settings.chain_count == 2
    assert settings.num_results == 4
    assert settings.num_burnin_steps == 1
    assert settings.step_size == 1.0e-5
    assert settings.num_leapfrog_steps == 1
    assert settings.seed == (20260706, 6401)
    assert settings.use_xla is False
    assert settings.trace_policy == "standard"
    assert settings.adaptation_policy == "fixed_kernel_no_adaptation"
    assert settings.payload()["artifact_mode"] == (
        "cpu_hidden_native_divergence_telemetry_inspection"
    )


def test_native_field_search_accepts_only_boolean_fields() -> None:
    harness = _load_harness()
    payload = SimpleNamespace(
        divergence=tf.constant([0.0, 1.0], dtype=tf.float64),
        proposed_results=SimpleNamespace(
            is_divergent=tf.constant([False, True], dtype=tf.bool),
        ),
        accepted_results=SimpleNamespace(
            has_divergence=tf.constant([0, 1], dtype=tf.int32),
        ),
    )

    search = harness.native_boolean_field_search(payload)
    accepted_paths = {
        item["path"] for item in search["accepted_native_boolean_fields"]
    }
    rejected_paths = {
        item["path"] for item in search["rejected_proxy_or_nonboolean_fields"]
    }

    assert "kernel_results.proposed_results.is_divergent" in accepted_paths
    assert "kernel_results.divergence" in rejected_paths
    assert "kernel_results.accepted_results.has_divergence" in rejected_paths
    assert search["available"] is True


def test_extractor_output_does_not_convert_numeric_divergence_proxy() -> None:
    harness = _load_harness()
    payload = SimpleNamespace(
        divergence=tf.constant([0.0, 1.0], dtype=tf.float64),
        proposed_results=SimpleNamespace(
            log_acceptance_correction=tf.constant([1000.0], dtype=tf.float64),
        ),
    )

    output = harness.extractor_output(payload)

    assert output["available"] is False
    assert output["status"] == "native_divergence_not_exposed_by_kernel"
    assert output["count"] is None
    assert "not zero divergences" in output["nonclaim"]


def test_phase4_artifact_records_missing_native_telemetry_without_zero_claim(monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")

    artifact = harness.build_phase4_divergence_telemetry_artifact(
        command=("pytest", "phase4-telemetry"),
    )

    assert artifact["phase"] == "PHASE4"
    assert artifact["status"] == "passed"
    assert artifact["phase3_baseline"]["phase3_preconditions_met"] is True
    assert artifact["native_divergence_telemetry_status"] in {
        "native_divergence_available",
        "native_divergence_not_exposed_by_kernel",
    }
    if artifact["native_divergence_telemetry_status"] == "native_divergence_not_exposed_by_kernel":
        assert artifact["native_divergence_count"] is None
        assert "not zero divergences" in artifact["native_divergence_interpretation"]
    health_context = artifact["bayesfilter_hmc_inspection"][
        "non_divergence_health_context"
    ]
    assert health_context["not_native_divergence"] is True
    assert "log_accept_ratio" in artifact["bayesfilter_hmc_inspection"]["trace_keys"]


def test_phase4_markdown_and_json_roundtrip(tmp_path: Path, monkeypatch) -> None:
    harness = _load_harness()
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    output = tmp_path / "phase4.json"
    markdown = tmp_path / "phase4.md"

    rc = harness.main(["--output", str(output), "--markdown-output", str(markdown)])
    payload = json.loads(output.read_text(encoding="utf-8"))
    summary = markdown.read_text(encoding="utf-8")

    assert rc == 0
    assert payload["schema_version"] == (
        "minimal_ssl_lstm_zhaocui_hmc_validity.phase4_divergence_telemetry.v1"
    )
    assert payload["status"] == "passed"
    assert "Native divergence telemetry status" in summary
    assert "missing native divergence telemetry is not zero divergences" in summary


def test_deterministic_chain_initial_state_is_finite_and_dispersed() -> None:
    harness = _load_harness()
    base = tf.zeros([24], dtype=tf.float64)
    state = harness.deterministic_chain_initial_state(base, chain_count=2, spread=0.01)
    array = state.numpy()

    assert array.shape == (2, 24)
    assert np.all(np.isfinite(array))
    assert not np.allclose(array[0], array[1])
