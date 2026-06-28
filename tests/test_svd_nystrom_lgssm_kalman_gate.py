from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_svd_nystrom_lgssm_kalman_gate as bench


def _small_args(tmp_path: Path):
    return bench._parse_args_from_list_for_test(
        [
            "--case-ids",
            "lgssm_small_exact_ref",
            "--seeds",
            "91001",
            "--num-particles",
            "16",
            "--time-steps",
            "1",
            "--nystrom-rank",
            "4",
            "--nystrom-max-iterations",
            "20",
            "--nystrom-core-solver",
            "svd_truncated",
            "--nystrom-core-rcond",
            "1e-6",
            "--nystrom-kernel-mode",
            "raw",
            "--nystrom-scaling-normalization",
            "none",
            "--particle-chunk-size",
            "8",
            "--warmups",
            "0",
            "--repeats",
            "1",
            "--dtype",
            "float32",
            "--tf32-mode",
            "disabled",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "lgssm-svd-nystrom.json"),
            "--markdown-output",
            str(tmp_path / "lgssm-svd-nystrom.md"),
        ]
    )


def test_small_cpu_hidden_command_shape_emits_exact_kalman_metrics(tmp_path: Path) -> None:
    args = _small_args(tmp_path)
    result = bench.build_result(args)

    assert result["schema_version"] == "svd_nystrom_lgssm_kalman_gate.v1"
    assert result["evidence_class"] == "cpu_hidden_command_shape_debug_only"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    assert result["candidate"]["candidate_id"] == "r32_eps0p5_raw_none_svd_rcond1e-6"
    assert result["candidate"]["core_solver"] == "svd_truncated"
    assert result["candidate"]["core_rcond"] == 1.0e-6
    assert result["candidate"]["kernel_mode"] == "raw"
    assert result["candidate"]["scaling_normalization"] == "none"
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["case_id"] == "lgssm_small_exact_ref"
    assert row["seed"] == 91001
    assert row["route"] == "svd_nystrom"
    assert row["transport_matrix_materialized"] is False
    assert row["transport_object_kind"] == "nystrom_kernel_factors"
    assert row["kalman_reference_finite"] is True
    assert row["finite_output"] is True
    assert row["finite_factors"] is True
    assert row["finite_particles"] is True
    assert row["route_invocations"] == row["active_resampling_mask_count"] == 1
    assert isinstance(row["mean_rmse"], float)
    assert isinstance(row["variance_rmse"], float)
    assert isinstance(row["loglik_abs_delta"], float)
    assert "no HMC readiness claim" in result["nonclaims"]
    assert result["inference_status"]["default_readiness"] == "NO"


def test_rejects_rank_above_particle_count(tmp_path: Path) -> None:
    try:
        bench._parse_args_from_list_for_test(
            [
                "--case-ids",
                "lgssm_small_exact_ref",
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
        assert "nystrom_rank must be <= num_particles" in str(exc)
    else:
        raise AssertionError("rank above particle count should fail validation")


def test_can_disable_nystrom_diagnostics(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--case-ids",
            "lgssm_small_exact_ref",
            "--seeds",
            "91001",
            "--num-particles",
            "16",
            "--time-steps",
            "1",
            "--nystrom-rank",
            "4",
            "--no-nystrom-diagnostics",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "lgssm-svd-nystrom.json"),
        ]
    )

    assert args.nystrom_diagnostics is False


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "lgssm-svd-nystrom.json"
    markdown = tmp_path / "lgssm-svd-nystrom.md"
    argv = [
        "benchmark_svd_nystrom_lgssm_kalman_gate.py",
        "--case-ids",
        "lgssm_small_exact_ref",
        "--seeds",
        "91001",
        "--num-particles",
        "16",
        "--time-steps",
        "1",
        "--nystrom-rank",
        "4",
        "--nystrom-max-iterations",
        "20",
        "--particle-chunk-size",
        "8",
        "--warmups",
        "0",
        "--repeats",
        "1",
        "--dtype",
        "float32",
        "--tf32-mode",
        "disabled",
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
    assert loaded["rows"][0]["route"] == "svd_nystrom"
    assert loaded["rows"][0]["transport_matrix_materialized"] is False
    assert loaded["rows"][0]["kalman_reference_finite"] is True
    assert loaded["candidate"]["core_solver"] == "svd_truncated"
    assert markdown.exists()
