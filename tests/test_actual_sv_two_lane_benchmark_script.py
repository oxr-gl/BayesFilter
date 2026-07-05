from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/home/chakwong/anaconda3/envs/tf-gpu/bin/python"
SCRIPT = ROOT / "docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py"


def test_actual_sv_two_lane_benchmark_tiny_cpu_emits_expected_schema(tmp_path: Path) -> None:
    output = tmp_path / "actual-sv-two-lane.json"
    markdown = tmp_path / "actual-sv-two-lane.md"
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(SCRIPT),
        "--dims",
        "1",
        "--include-ksc",
        "--include-controls",
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)

    payload = json.loads(output.read_text(encoding="utf-8"))
    markdown_text = markdown.read_text(encoding="utf-8")

    assert payload["schema_version"] == "actual_sv_two_lane.v1"
    assert payload["dims"] == [1]
    assert payload["include_ksc"] is True
    assert payload["include_controls"] is True
    assert payload["lane_a_sparse_level"] == 2
    assert payload["lane_b_sparse_level"] == 4
    assert len(payload["actual_sv_rows"]) == 1
    assert len(payload["ksc_rows"]) == 1
    assert len(payload["control_rows"]) == 6

    row = payload["actual_sv_rows"][0]
    assert row["dim"] == 1
    assert row["lane_a"]["value_gap"] >= 0.0
    assert row["lane_b"]["sgqf_value_gap"] >= 0.0
    assert row["lane_b"]["ukf_value_gap"] >= 0.0
    assert row["lane_b"]["sgqf_gradient_relative_error_to_dense"] >= 0.0
    assert row["lane_b"]["ukf_gradient_relative_error_to_dense"] >= 0.0
    assert row["lane_b"]["sgqf_gradient_abs_gap_norm_to_dense"] >= 0.0
    assert row["lane_b"]["ukf_gradient_abs_gap_norm_to_dense"] >= 0.0
    assert row["lane_b"]["sgqf_gradient_relative_error_to_dense"] < row["lane_b"]["ukf_gradient_relative_error_to_dense"]

    assert "Actual-SV Two-Lane Comparison" in markdown_text
    assert "KSC surrogate rows" in markdown_text
    assert "Control rows" in markdown_text
