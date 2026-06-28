from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import scalable_ot_low_rank_ledh_pfpf_integration_smoke as smoke


def test_small_filter_integration_records_route_execution(tmp_path: Path) -> None:
    output = tmp_path / "small.json"
    markdown = tmp_path / "small.md"
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "small",
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ]
    )
    result = smoke.build_result(args)
    output.write_text(json.dumps(smoke._json_ready(result), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    smoke.write_markdown(result, markdown)

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["status"] == "PASS"
    assert loaded["phase"] == "LR-LEDH-PFPF-INT-1"
    assert loaded["hard_vetoes"] == []
    row = loaded["rows"][0]
    assert row["low_rank_resampling_invocations"] > 0
    assert row["low_rank_resampling_invocations"] == row["active_resampling_mask_count"]
    assert row["solver_transport_matrix_materialized"] is False
    assert all(shape[-2:] == [0, 0] for shape in row["transport_matrix_shapes"])
    assert row["tiny_materialized_apply_parity"] <= smoke.TINY_MATERIALIZED_APPLY_PARITY_THRESHOLD
    assert markdown.exists()


def test_tuning_mode_preserves_bounded_grid_and_route_evidence(tmp_path: Path) -> None:
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "tuning-cpu",
            "--particle-counts",
            "32",
            "--batch-size",
            "1",
            "--time-steps",
            "1",
            "--state-dim",
            "3",
            "--obs-dim",
            "2",
            "--tuning-ranks",
            "4",
            "8",
            "--tuning-assignment-epsilons",
            "0.0625",
            "0.03125",
            "--output",
            str(tmp_path / "tuning.json"),
            "--markdown-output",
            str(tmp_path / "tuning.md"),
        ]
    )
    result = smoke.build_result(args)
    assert result["phase"] == "LR-LEDH-PFPF-INT-2"
    assert len(result["rows"]) == 4
    assert result["summary"]["num_viable_rows"] >= 1
    for row in result["rows"]:
        assert row["grid_role"] == "tuning_candidate"
        assert row["low_rank_resampling_invocations"] == row["active_resampling_mask_count"]
        assert row["solver_transport_matrix_materialized"] is False


def test_medium_defaults_are_cpu_hidden_and_nonmaterialized(tmp_path: Path) -> None:
    args = smoke._parse_args_from_list_for_test(
        [
            "--mode",
            "medium-cpu",
            "--particle-counts",
            "64",
            "--batch-size",
            "1",
            "--time-steps",
            "1",
            "--state-dim",
            "3",
            "--obs-dim",
            "2",
            "--rank",
            "8",
            "--assignment-epsilon",
            "0.03125",
            "--output",
            str(tmp_path / "medium.json"),
            "--markdown-output",
            str(tmp_path / "medium.md"),
        ]
    )
    result = smoke.build_result(args)
    row = result["rows"][0]
    assert row["status"] in {"PASS", "FAIL"}
    assert row["low_rank_resampling_invocations"] == row["active_resampling_mask_count"]
    assert row["solver_transport_matrix_materialized"] is False
    assert result["run_manifest"]["device_scope"] == "cpu"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    assert result["thresholds"]["runtime_memory_tf32_role"] == "explanatory_only"
