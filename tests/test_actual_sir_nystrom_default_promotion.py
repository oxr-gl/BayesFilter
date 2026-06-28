from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_actual_sir_nystrom_default_promotion as bench


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
            "--nystrom-rank",
            "4",
            "--nystrom-max-iterations",
            "20",
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
            "--dtype",
            "float64",
            "--output",
            str(tmp_path / "actual_sir_nystrom.json"),
            "--markdown-output",
            str(tmp_path / "actual_sir_nystrom.md"),
            *extra,
        ]
    )


def test_parse_args_rejects_nystrom_rank_above_particles(tmp_path: Path) -> None:
    try:
        _small_args(tmp_path, "--nystrom-rank", "9")
    except ValueError as exc:
        assert "nystrom_rank must be <= num_particles" in str(exc)
    else:
        raise AssertionError("expected Nystrom rank validation failure")


def test_small_actual_sir_streaming_and_nystrom_emit_required_diagnostics(tmp_path: Path) -> None:
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
    assert result["routes_executed"] == ["streaming", "nystrom"]
    assert len(result["rows"]) == 2
    by_route = {row["route"]: row for row in result["rows"]}
    assert by_route["streaming"]["route_invocations"] == 1
    assert by_route["nystrom"]["route_invocations"] == 1
    assert by_route["nystrom"]["transport_matrix_materialized"] is False
    assert all(shape[-2:] == [0, 0] for shape in by_route["nystrom"]["transport_matrix_shapes"])
    assert by_route["nystrom"]["transport_object_kind"] == "nystrom_kernel_factors"
    assert by_route["nystrom"]["all_finite_factors"] is True
    assert by_route["nystrom"]["all_finite_resampled_particles"] is True
    assert by_route["nystrom"]["max_row_residual"] <= bench.NYSTROM_RESIDUAL_THRESHOLD
    assert result["paired_comparability"] is not None
    assert result["run_manifest"]["device_scope"] == "cpu"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    assert result["inference_status"]["default_readiness"] == "NO"


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "actual_sir_nystrom.json"
    markdown = tmp_path / "actual_sir_nystrom.md"
    argv = [
        "benchmark_actual_sir_nystrom_default_promotion.py",
        "--route",
        "nystrom",
        "--batch-seeds",
        "81120",
        "--time-steps",
        "1",
        "--num-particles",
        "8",
        "--nystrom-rank",
        "4",
        "--nystrom-max-iterations",
        "20",
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
        "--dtype",
        "float64",
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
    ]
    monkeypatch.setattr(bench.sys, "argv", argv)

    bench.main()

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["routes_executed"] == ["nystrom"]
    assert loaded["rows"][0]["route"] == "nystrom"
    assert loaded["rows"][0]["transport_matrix_materialized"] is False
    assert markdown.exists()

