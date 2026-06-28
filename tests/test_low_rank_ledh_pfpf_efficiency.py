from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import scalable_ot_low_rank_ledh_pfpf_efficiency as harness


def test_small_efficiency_harness_records_both_routes_and_comparability(tmp_path: Path) -> None:
    output = tmp_path / "small.json"
    markdown = tmp_path / "small.md"
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "small",
            "--particle-counts",
            "16",
            "--batch-size",
            "1",
            "--time-steps",
            "1",
            "--state-dim",
            "2",
            "--obs-dim",
            "1",
            "--rank",
            "4",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ]
    )

    result = harness.build_result(args)
    output.write_text(json.dumps(harness._json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    harness.write_markdown(result, markdown, output)
    loaded = json.loads(output.read_text(encoding="utf-8"))

    assert loaded["phase"] == "LOW_RANK_LEDH_EFFICIENCY_P01"
    assert loaded["mode"] == "small"
    assert {row["route"] for row in loaded["rows"]} == {"streaming", "low_rank"}
    assert loaded["paired_efficiency"]["paired_rows"][0]["comparability"]["status"] in {"PASS", "FAIL"}
    assert loaded["run_manifest"]["cuda_visible_devices"] == "-1"
    assert loaded["run_manifest"]["same_physical_gpu_required_for_paired_claim"] is True
    assert "no posterior correctness claim" in loaded["nonclaims"]
    assert markdown.exists()


def test_paired_gpu_defaults_encode_fixed_ladder_and_timeout(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "paired-gpu",
            "--particle-counts",
            "1024",
            "--output",
            str(tmp_path / "paired.json"),
            "--markdown-output",
            str(tmp_path / "paired.md"),
        ]
    )

    assert args.particle_counts == [1024]
    assert args.row_timeout_seconds == harness.P02_ROW_TIMEOUT_SECONDS
    assert args.stop_streaming_after_failure is True
    assert args.tf32_mode == "enabled"
    assert args.device_scope == "visible"
    assert args.routes == "both"


def test_large_n_defaults_are_low_rank_only_with_fixed_timeout(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "large-n",
            "--particle-counts",
            "50000",
            "--output",
            str(tmp_path / "large.json"),
            "--markdown-output",
            str(tmp_path / "large.md"),
        ]
    )

    assert args.routes == "low-rank"
    assert args.row_timeout_seconds == harness.P03_ROW_TIMEOUT_SECONDS
    assert args.tf32_mode == "enabled"
    assert args.device_scope == "visible"


def test_comparability_veto_blocks_output_incomparable_rows() -> None:
    streaming = {
        "status": "PASS",
        "shape": {"num_particles": 16},
        "finite_output": True,
        "output_log_weight_normalization_residual": 0.0,
        "ess_fraction_min": 0.5,
        "state_mean": [[0.0, 0.0]],
    }
    low_rank = {
        "status": "PASS",
        "shape": {"num_particles": 16},
        "finite_output": True,
        "output_log_weight_normalization_residual": 0.0,
        "ess_fraction_min": 0.5,
        "state_mean": [[10.0, 0.0]],
    }

    result = harness._paired_comparability(streaming, low_rank)

    assert result["status"] == "FAIL"
    assert "state_mean_proxy_l2_threshold" in result["hard_vetoes"]


def test_timeout_row_writes_route_fired_sidecar(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "paired-gpu",
            "--particle-counts",
            "1024",
            "--row-timeout-seconds",
            "1",
            "--output",
            str(tmp_path / "paired.json"),
            "--markdown-output",
            str(tmp_path / "paired.md"),
        ]
    )
    row_json = tmp_path / "paired-row-streaming-n1024.json"
    row = harness._timeout_row(
        args,
        1024,
        "streaming",
        row_json,
        0.0,
        subprocess.TimeoutExpired(cmd=["synthetic"], timeout=1),
    )

    assert row["status"] == "TIMEOUT"
    loaded = json.loads(row_json.read_text(encoding="utf-8"))
    assert loaded["artifact_role"] == "parent_enforced_row_timeout_sidecar"
    assert loaded["rows"][0]["timeout_status"] == "timeout_enforced"
    assert row_json.with_suffix(".md").exists()
