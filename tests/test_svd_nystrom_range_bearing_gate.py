from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

import numpy as np
import pytest
import tensorflow as tf

from docs.benchmarks import benchmark_svd_nystrom_range_bearing_gate as bench
from experiments.dpf_implementation.fixtures import range_bearing


def _tiny_args(tmp_path: Path):
    return bench._parse_args_from_list_for_test(
        [
            "--route",
            "both",
            "--seed",
            "84000",
            "--time-steps",
            "2",
            "--num-particles",
            "16",
            "--transport-policy",
            "active-all",
            "--sinkhorn-iterations",
            "2",
            "--row-chunk-size",
            "16",
            "--col-chunk-size",
            "16",
            "--particle-chunk-size",
            "16",
            "--nystrom-rank",
            "4",
            "--nystrom-max-iterations",
            "20",
            "--nystrom-diagnostics",
            "--nystrom-core-solver",
            "svd_truncated",
            "--nystrom-core-rcond",
            "1e-6",
            "--nystrom-kernel-mode",
            "raw",
            "--nystrom-scaling-normalization",
            "none",
            "--history-mode",
            "full",
            "--paired-threshold-mode",
            "gate",
            "--warmups",
            "0",
            "--repeats",
            "1",
            "--dtype",
            "float64",
            "--tf32-mode",
            "disabled",
            "--no-jit-compile",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "range-bearing.json"),
            "--markdown-output",
            str(tmp_path / "range-bearing.md"),
        ]
    )


def test_range_bearing_tf_observation_and_residual_match_fixture_numpy() -> None:
    points_np = np.array(
        [[1.2, 0.7, 0.1, -0.2], [-0.5, 0.25, 0.0, 0.1]],
        dtype=np.float64,
    )
    observed_np = np.array([1.0, -3.12], dtype=np.float64)

    obs_tf = bench._range_bearing_observation_tf(tf.constant(points_np, dtype=tf.float64))
    expected_obs = range_bearing.range_bearing_observation(points_np)
    np.testing.assert_allclose(obs_tf.numpy(), expected_obs, atol=1e-12)

    residual_tf = bench._observation_residual_tf(
        obs_tf[tf.newaxis, :, :],
        tf.constant(observed_np, dtype=tf.float64),
    )
    expected_residual = range_bearing.observation_residual(expected_obs, observed_np)
    np.testing.assert_allclose(residual_tf.numpy()[0], expected_residual, atol=1e-6)


def test_tiny_cpu_hidden_route_smoke_records_metadata_and_nonclaims(tmp_path: Path) -> None:
    args = _tiny_args(tmp_path)
    result = bench.build_result(args)

    assert result["schema_version"] == "svd_nystrom_range_bearing_gate.v1"
    assert result["status"] == "PASS"
    assert result["hard_vetoes"] == []
    assert result["shape"] == {
        "batch_size": 1,
        "time_steps": 2,
        "num_particles": 16,
        "state_dim": 4,
        "obs_dim": 2,
    }
    assert result["fixture"]["fixture_id"] == "range_bearing_gaussian_moderate"
    assert result["fixture"]["model_checksum"]
    assert result["fixture"]["observation_checksum"]
    assert result["transport"]["nystrom_rank"] == 4
    assert result["transport"]["nystrom_core_solver"] == "svd_truncated"
    assert result["transport"]["nystrom_kernel_mode"] == "raw"
    assert result["transport"]["nystrom_scaling_normalization"] == "none"
    assert result["thresholds"]["paired_threshold_mode"] == "gate"
    assert result["thresholds"]["normalized_abs_log_likelihood_delta_role"] == "hard_veto"
    assert result["precision"]["dtype"] == "float64"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    by_route = {row["route"]: row for row in result["rows"]}
    assert set(by_route) == {"streaming", "nystrom"}
    assert by_route["streaming"]["status"] == "PASS"
    assert by_route["nystrom"]["status"] == "PASS"
    assert by_route["nystrom"]["transport_matrix_materialized"] is False
    assert by_route["nystrom"]["transport_object_kind"] == "nystrom_kernel_factors"
    assert by_route["nystrom"]["finite_factors"] is True
    assert by_route["nystrom"]["finite_particles"] is True
    assert result["paired_comparability"]["normalized_max_abs_delta"] <= result["thresholds"]["normalized_abs_log_likelihood_delta"]
    assert "no HMC readiness claim" in result["nonclaims"]
    assert result["inference_status"]["default_readiness"] == "NO"


def test_paired_threshold_record_only_mode_suppresses_paired_veto(tmp_path: Path) -> None:
    args = _tiny_args(tmp_path)
    args.paired_threshold_mode = "record-only"
    args.paired_delta_threshold = 1.0e-6

    paired = {
        "normalized_max_abs_delta": 0.5,
        "normalized_mean_abs_delta": 0.25,
    }

    assert bench._paired_vetoes(paired, args) == []
    assert bench._paired_delta_threshold_role(args) == "record_only_descriptive_not_calibrated"


def test_paired_threshold_gate_mode_retains_hard_veto(tmp_path: Path) -> None:
    args = _tiny_args(tmp_path)
    args.paired_threshold_mode = "gate"
    args.paired_delta_threshold = 1.0e-6

    paired = {
        "normalized_max_abs_delta": 0.5,
        "normalized_mean_abs_delta": 0.25,
    }

    assert bench._paired_vetoes(paired, args) == ["paired_normalized_log_likelihood_delta"]
    assert bench._paired_delta_threshold_role(args) == "hard_veto"


def test_capture_route_exceptions_records_structured_failure(tmp_path: Path, monkeypatch) -> None:
    args = _tiny_args(tmp_path)
    args.capture_route_exceptions = True

    def raising_streaming_outputs(*_args, **_kwargs):
        raise tf.errors.InvalidArgumentError(None, None, "synthetic route failure")

    monkeypatch.setattr(bench, "_streaming_outputs", raising_streaming_outputs)

    result = bench.build_result(args)

    assert result["status"] == "FAIL"
    assert "streaming:route_exception" in result["hard_vetoes"]
    by_route = {row["route"]: row for row in result["rows"]}
    assert by_route["streaming"]["status"] == "FAIL"
    assert by_route["streaming"]["hard_vetoes"] == ["route_exception"]
    assert by_route["streaming"]["exception"]["type"] == "InvalidArgumentError"
    assert "synthetic route failure" in by_route["streaming"]["exception"]["message"]
    assert "log_likelihood" not in by_route["streaming"]
    assert by_route["nystrom"]["status"] == "PASS"
    assert result["paired_comparability"] is None
    assert result["run_manifest"]["capture_route_exceptions"] is True


def test_route_exceptions_reraise_by_default(tmp_path: Path, monkeypatch) -> None:
    args = _tiny_args(tmp_path)
    args.route = "streaming"

    def raising_streaming_outputs(*_args, **_kwargs):
        raise tf.errors.InvalidArgumentError(None, None, "synthetic route failure")

    monkeypatch.setattr(bench, "_streaming_outputs", raising_streaming_outputs)

    with pytest.raises(tf.errors.InvalidArgumentError, match="synthetic route failure"):
        bench.build_result(args)


def test_rejects_rank_above_particle_count(tmp_path: Path) -> None:
    try:
        bench._parse_args_from_list_for_test(
            [
                "--num-particles",
                "8",
                "--nystrom-rank",
                "16",
                "--device-scope",
                "cpu",
                "--device",
                "/CPU:0",
                "--expect-device-kind",
                "cpu",
                "--output",
                str(tmp_path / "bad.json"),
            ]
        )
    except ValueError as exc:
        assert "nystrom_rank must be positive and <= num_particles" in str(exc)
    else:
        raise AssertionError("rank above particle count should fail validation")


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "range-bearing.json"
    markdown = tmp_path / "range-bearing.md"
    argv = [
        "benchmark_svd_nystrom_range_bearing_gate.py",
        "--route",
        "both",
        "--seed",
        "84000",
        "--time-steps",
        "2",
        "--num-particles",
        "16",
        "--nystrom-rank",
        "4",
        "--nystrom-max-iterations",
        "20",
        "--sinkhorn-iterations",
        "2",
        "--row-chunk-size",
        "16",
        "--col-chunk-size",
        "16",
        "--particle-chunk-size",
        "16",
        "--dtype",
        "float64",
        "--tf32-mode",
        "disabled",
        "--no-jit-compile",
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
        "--quiet",
    ]
    monkeypatch.setattr(bench.sys, "argv", argv)

    bench.main()

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["schema_version"] == "svd_nystrom_range_bearing_gate.v1"
    assert loaded["rows"][0]["route"] == "streaming"
    assert loaded["rows"][1]["route"] == "nystrom"
    assert loaded["rows"][1]["transport_matrix_materialized"] is False
    assert loaded["thresholds"]["paired_threshold_mode"] == "gate"
    assert markdown.exists()
