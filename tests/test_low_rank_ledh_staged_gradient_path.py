from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_low_rank_ledh_staged_gradient_path as bench


def test_p02b_r_defaults_and_stage_expectations() -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            "unused.json",
        ]
    )

    assert args.phase_id == "LOW_RANK_STAGED_GRADIENT_PATH_P02B_R3_XLA_GRAPH_REDUCTION"
    assert args.readout_mode == "staged-only"
    assert bench._seed_probe_pairs(args) == [(91003, "center"), (91002, "qr_plus")]
    assert bench.STAGE_SPEC_BY_NAME["pre_flow_t0"].expected_connected is False
    assert bench.STAGE_SPEC_BY_NAME["resampled_log_weights_t0"].expected_connected is False
    assert bench.STAGE_SPEC_BY_NAME["next_incremental_log_likelihood_t1"].expected_connected is True


def test_small_cpu_hidden_p02b_r_writes_staged_schema(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--seed-probes",
            "91001:center",
            "--num-particles",
            "8",
            "--time-steps",
            "2",
            "--low-rank-rank",
            "4",
            "--low-rank-max-projection-iterations",
            "4",
            "--particle-chunk-size",
            "4",
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
            "--no-jit-compile",
            "--output",
            str(tmp_path / "p02b-r.json"),
            "--markdown-output",
            str(tmp_path / "p02b-r.md"),
        ]
    )

    result = bench.build_result(args)
    output = tmp_path / "p02b-r.json"
    markdown = tmp_path / "p02b-r.md"
    output.write_text(json.dumps(result), encoding="utf-8")
    bench.write_markdown(result, markdown, output)

    assert result["schema_version"] == "low_rank_ledh_staged_gradient_path.v1"
    assert result["evidence_class"] == "cpu_hidden_debug_only"
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["seed"] == 91001
    assert row["probe_label"] == "center"
    assert row["readout_mode"] == "staged-only"
    assert "route_summary" in row
    assert "same_tape" not in row
    assert "p02a_style_separated_tape" not in row
    assert row["ab_comparison"] is None
    assert row["route_summary"]["route_outputs_finite"] is True
    assert "staged_compiled_call_seconds" in row["timing_seconds"]
    assert "scaled_Q" in row["staged_checkpoints"]
    assert "pre_flow_t0" in row["staged_checkpoints"]
    assert "next_incremental_log_likelihood_t1" in row["staged_checkpoints"]
    assert row["staged_checkpoints"]["pre_flow_t0"]["expected_connected"] is False
    assert row["staged_checkpoints"]["resampled_log_weights_t0"]["expected_connected"] is False
    assert "whole_sum_gradient" in row["staged_checkpoints"]["scaled_Q"]
    assert row["staged_checkpoints"]["scaled_Q"]["value_summary"]["readout_mode"] == "compiled_compact_value_summary"
    assert result["h6_sir_inventory"]["answer"].startswith("No.")
    assert markdown.exists()
