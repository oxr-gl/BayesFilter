from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_actual_sir_low_rank_route_validation as bench


def test_default_certification_harness_defaults_lock_low_rank_candidate(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "actual_sir_default.json"),
        ]
    )

    assert bench.PLAN_PATH.endswith(
        "bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-"
        "master-program-2026-06-24.md"
    )
    assert args.route == "low_rank"
    assert args.low_rank_rank == 16
    assert args.low_rank_assignment_epsilon == 0.25
    assert args.low_rank_alpha == 1.0e-8
    assert args.low_rank_max_projection_iterations == 120
    assert args.low_rank_convergence_threshold == 1.0e-6
    assert args.low_rank_denominator_floor == 1.0e-30


def test_streaming_and_paired_routes_remain_explicitly_selectable(tmp_path: Path) -> None:
    streaming = bench._parse_args_from_list_for_test(
        [
            "--route",
            "streaming",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "streaming.json"),
        ]
    )
    paired = bench._parse_args_from_list_for_test(
        [
            "--route",
            "both",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "both.json"),
        ]
    )

    assert streaming.route == "streaming"
    assert paired.route == "both"


def _small_args(tmp_path: Path, *extra: str):
    return bench._parse_args_from_list_for_test(
        [
            "--route",
            "both",
            "--batch-seeds",
            "81120",
            "--time-steps",
            "1",
            "--num-particles",
            "8",
            "--transport-policy",
            "active-all",
            "--sinkhorn-iterations",
            "2",
            "--row-chunk-size",
            "8",
            "--col-chunk-size",
            "8",
            "--particle-chunk-size",
            "8",
            "--low-rank-rank",
            "4",
            "--low-rank-assignment-epsilon",
            "0.25",
            "--low-rank-max-projection-iterations",
            "80",
            "--warmups",
            "0",
            "--repeats",
            "1",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--tf32-mode",
            "disabled",
            "--output",
            str(tmp_path / "actual_sir_routes.json"),
            "--markdown-output",
            str(tmp_path / "actual_sir_routes.md"),
            *extra,
        ]
    )


def test_parse_args_rejects_low_rank_rank_above_particles(tmp_path: Path) -> None:
    try:
        _small_args(tmp_path, "--low-rank-rank", "9")
    except ValueError as exc:
        assert "low_rank_rank must be <= num_particles" in str(exc)
    else:
        raise AssertionError("expected low-rank rank validation failure")


def test_small_actual_sir_both_routes_emit_required_diagnostics(tmp_path: Path) -> None:
    args = _small_args(tmp_path)
    result = bench.build_result(args)

    assert result["actual_sir_semantics_pass"] is True
    assert result["shape"] == {
        "batch_size": 1,
        "time_steps": 1,
        "num_particles": 8,
        "state_dim": 18,
        "obs_dim": 9,
    }
    assert result["routes_executed"] == ["streaming", "low_rank"]
    assert len(result["rows"]) == 2
    by_route = {row["route"]: row for row in result["rows"]}
    assert by_route["streaming"]["streaming_timing_source"] == "compiled_core"
    assert by_route["streaming"]["jit_compile"] is True
    assert by_route["streaming"]["route_invocations"] == 1
    assert by_route["low_rank"]["low_rank_timing_source"] == "compiled_core"
    assert by_route["low_rank"]["jit_compile"] is True
    assert by_route["low_rank"]["route_invocations"] == 1
    assert by_route["low_rank"]["active_resampling_mask_count"] == 1
    assert by_route["low_rank"]["transport_matrix_materialized"] is False
    assert all(shape[-2:] == [0, 0] for shape in by_route["low_rank"]["transport_matrix_shapes"])
    assert by_route["low_rank"]["transport_object_kind"] == "low_rank_coupling_factors"
    assert by_route["low_rank"]["all_finite_factors"] is True
    assert by_route["low_rank"]["all_nonnegative_factors"] is True
    assert by_route["low_rank"]["all_positive_g"] is True
    assert by_route["low_rank"]["max_factor_marginal_residual"] <= bench.FACTOR_RESIDUAL_THRESHOLD
    assert result["paired_comparability"] is not None
    assert result["run_manifest"]["device_scope"] == "cpu"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    assert result["run_manifest"]["streaming_timing_source"] == "compiled_core"
    assert result["run_manifest"]["low_rank_timing_source"] == "compiled_core"
    assert result["run_manifest"]["jit_compile"] is True


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "actual_sir_routes.json"
    markdown = tmp_path / "actual_sir_routes.md"
    argv = [
        "benchmark_actual_sir_low_rank_route_validation.py",
        "--route",
        "low_rank",
        "--batch-seeds",
        "81120",
        "--time-steps",
        "1",
        "--num-particles",
        "8",
        "--low-rank-rank",
        "4",
        "--low-rank-assignment-epsilon",
        "0.25",
        "--low-rank-max-projection-iterations",
        "80",
        "--warmups",
        "0",
        "--repeats",
        "1",
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--tf32-mode",
        "disabled",
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
    ]
    monkeypatch.setattr(bench.sys, "argv", argv)

    bench.main()

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["routes_executed"] == ["low_rank"]
    assert loaded["rows"][0]["route"] == "low_rank"
    assert loaded["rows"][0]["low_rank_timing_source"] == "compiled_core"
    assert loaded["rows"][0]["jit_compile"] is True
    assert loaded["rows"][0]["transport_matrix_materialized"] is False
    assert markdown.exists()


def test_diagnostic_loop_timing_source_is_rejected(tmp_path: Path) -> None:
    try:
        _small_args(tmp_path, "--low-rank-timing-source", "diagnostic_loop")
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected argparse to reject diagnostic low-rank timing")


def test_no_jit_compile_escape_is_rejected(tmp_path: Path) -> None:
    try:
        _small_args(tmp_path, "--no-jit-compile")
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError("expected argparse to reject disabling XLA")
