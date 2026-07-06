from __future__ import annotations

import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_actual_sir_nystrom_compiled_redo as redo


def _tiny_args(tmp_path: Path):
    return redo._parse_args_from_list_for_test(
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
            "--nystrom-rank",
            "4",
            "--nystrom-diagnostics",
            "--nystrom-core-solver",
            "svd_truncated",
            "--nystrom-core-rcond",
            "1e-5",
            "--nystrom-kernel-mode",
            "positive_projected",
            "--nystrom-max-iterations",
            "20",
            "--history-mode",
            "value-only",
            "--warmups",
            "0",
            "--repeats",
            "1",
            "--dtype",
            "float64",
            "--tf32-mode",
            "disabled",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "redo.json"),
            "--markdown-output",
            str(tmp_path / "redo.md"),
        ]
    )


def test_compiled_redo_tiny_cpu_rows_pass(tmp_path: Path) -> None:
    args = _tiny_args(tmp_path)
    result = redo.build_result(args)

    assert result["status"] == "PASS"
    assert result["hard_vetoes"] == []
    assert result["schema_version"] == "actual_sir_nystrom_compiled_redo.v1"
    assert result["jit_compile"] is True
    assert result["routes_executed"] == ["streaming", "nystrom"]
    by_route = {row["route"]: row for row in result["rows"]}
    assert by_route["streaming"]["status"] == "PASS"
    assert by_route["nystrom"]["status"] == "PASS"
    assert by_route["nystrom"]["route_invocations"] == 1
    assert by_route["nystrom"]["nystrom_diagnostics_enabled"] is True
    assert by_route["nystrom"]["nystrom_core_solver"] == "svd_truncated"
    assert by_route["nystrom"]["nystrom_core_rcond"] == 1.0e-5
    assert by_route["nystrom"]["nystrom_kernel_mode"] == "positive_projected"
    assert by_route["nystrom"]["nystrom_scaling_normalization"] == "none"
    assert by_route["nystrom"]["max_abs_log_scaling_gauge_shift"] == 0.0
    assert by_route["nystrom"]["scaling_normalization_applications"] == 0.0
    assert "min_kernel_denominator" in by_route["nystrom"]
    assert "denominator_floor_hits" in by_route["nystrom"]
    assert by_route["nystrom"]["denominator_floor_hits"] >= 0.0
    assert by_route["nystrom"]["projection_floor_hits"] >= 0.0
    assert by_route["nystrom"]["landmark_core_effective_rank_min"] > 0.0
    assert by_route["nystrom"]["max_row_residual"] <= redo.NYSTROM_RESIDUAL_THRESHOLD
    assert result["paired_comparability"]["log_likelihood_max_abs_delta"] <= 10.0
    assert result["inference_status"]["default_readiness"] == "NO"
    assert result["transport"]["nystrom_diagnostics_enabled"] is True
    assert result["transport"]["nystrom_core_solver"] == "svd_truncated"
    assert result["transport"]["nystrom_kernel_mode"] == "positive_projected"
    assert result["transport"]["nystrom_scaling_normalization"] == "none"


def test_compiled_redo_propagates_balanced_scaling_normalization(tmp_path: Path) -> None:
    args = redo._parse_args_from_list_for_test(
        [
            "--route",
            "nystrom",
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
            "--nystrom-rank",
            "4",
            "--nystrom-kernel-mode",
            "raw",
            "--nystrom-scaling-normalization",
            "balanced",
            "--nystrom-max-iterations",
            "20",
            "--history-mode",
            "value-only",
            "--warmups",
            "0",
            "--repeats",
            "1",
            "--dtype",
            "float64",
            "--tf32-mode",
            "disabled",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "redo-balanced.json"),
            "--markdown-output",
            str(tmp_path / "redo-balanced.md"),
        ]
    )

    result = redo.build_result(args)

    assert result["transport"]["nystrom_kernel_mode"] == "raw"
    assert result["transport"]["nystrom_scaling_normalization"] == "balanced"
    by_route = {row["route"]: row for row in result["rows"]}
    assert by_route["nystrom"]["nystrom_kernel_mode"] == "raw"
    assert by_route["nystrom"]["nystrom_scaling_normalization"] == "balanced"
    assert by_route["nystrom"]["max_abs_log_scaling_gauge_shift"] > 0.0
    assert by_route["nystrom"]["scaling_normalization_applications"] > 0.0
