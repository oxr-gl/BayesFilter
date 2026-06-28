from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import scalable_ot_nystrom_ledh_pfpf_effectiveness_leaderboard as harness


def test_tiny_cpu_harness_records_streaming_and_nystrom_routes(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "tiny-cpu",
            "--particle-counts",
            "8",
            "--rank",
            "2",
            "--time-steps",
            "1",
            "--state-dim",
            "3",
            "--obs-dim",
            "2",
            "--nystrom-max-iterations",
            "20",
            "--output",
            str(tmp_path / "tiny.json"),
            "--markdown-output",
            str(tmp_path / "tiny.md"),
        ]
    )

    result = harness.build_result(args)
    Path(args.output).write_text(json.dumps(harness._json_ready(result), indent=2), encoding="utf-8")
    harness.write_markdown(result, Path(args.markdown_output), Path(args.output))
    loaded = json.loads(Path(args.output).read_text(encoding="utf-8"))

    assert loaded["mode"] == "tiny-cpu"
    assert {row["route"] for row in loaded["rows"]} == {"streaming", "nystrom"}
    assert loaded["run_manifest"]["same_physical_gpu_required_for_paired_claim"] is True
    assert loaded["paired_effectiveness"]["paired_rows"][0]["comparability"]["status"] in {"PASS", "FAIL"}
    assert loaded["paired_effectiveness"]["ranking_status"] == "NOT_STATISTICALLY_SUPPORTED_SINGLE_PILOT"
    assert "no posterior correctness claim" in loaded["nonclaims"]
    assert Path(args.markdown_output).exists()


def test_paired_gpu_defaults_encode_gpu1_preferred_policy(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "paired-gpu",
            "--particle-counts",
            "1024",
            "--cuda-visible-devices",
            "1",
            "--selected-physical-gpu",
            "1",
            "--output",
            str(tmp_path / "pilot.json"),
            "--markdown-output",
            str(tmp_path / "pilot.md"),
        ]
    )

    assert args.particle_counts == [1024]
    assert args.device_scope == "visible"
    assert args.expect_device_kind == "gpu"
    assert args.tf32_mode == "enabled"
    assert args.rank == 32
    assert args.row_timeout_seconds == harness.P02_ROW_TIMEOUT_SECONDS


def test_comparability_veto_blocks_large_state_drift() -> None:
    streaming = {
        "status": "PASS",
        "shape": {"num_particles": 16},
        "finite_output": True,
        "output_log_weight_normalization_residual": 0.0,
        "ess_fraction_min": 0.5,
        "state_mean": [[0.0, 0.0]],
        "log_likelihood": [0.0],
    }
    nystrom = {
        "status": "PASS",
        "shape": {"num_particles": 16},
        "finite_output": True,
        "output_log_weight_normalization_residual": 0.0,
        "ess_fraction_min": 0.5,
        "state_mean": [[10.0, 0.0]],
        "log_likelihood": [0.0],
    }

    result = harness._paired_comparability(streaming, nystrom)

    assert result["status"] == "FAIL"
    assert "state_mean_proxy_l2_threshold" in result["hard_vetoes"]


def test_json_ready_and_markdown_include_inference_status(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "tiny-cpu",
            "--particle-counts",
            "8",
            "--rank",
            "2",
            "--nystrom-max-iterations",
            "20",
            "--output",
            str(tmp_path / "tiny.json"),
            "--markdown-output",
            str(tmp_path / "tiny.md"),
        ]
    )
    result = harness.build_result(args)
    payload = harness._json_ready(result)
    Path(args.output).write_text(json.dumps(payload), encoding="utf-8")
    harness.write_markdown(result, Path(args.markdown_output), Path(args.output))

    assert json.loads(Path(args.output).read_text(encoding="utf-8"))["inference_status"]["default_readiness"] == "NO"
    assert "Inference Status" in Path(args.markdown_output).read_text(encoding="utf-8")

