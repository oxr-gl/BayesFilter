from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_low_rank_ledh_route_internal_gradient_connectivity as bench


def test_p02b_defaults_to_required_reviewed_probes() -> None:
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

    assert args.phase_id == "LOW_RANK_ROUTE_INTERNAL_GRADIENT_CONNECTIVITY"
    assert bench._seed_probe_pairs(args) == [(91003, "center"), (91002, "qr_plus")]
    assert "next_pre_flow_t1" in bench.REQUIRED_TENSORS
    assert "final_log_likelihood" in bench.REQUIRED_TENSORS


def test_small_cpu_hidden_p02b_writes_ab_internal_schema(tmp_path: Path) -> None:
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
            str(tmp_path / "p02b.json"),
            "--markdown-output",
            str(tmp_path / "p02b.md"),
        ]
    )

    result = bench.build_result(args)
    output = tmp_path / "p02b.json"
    markdown = tmp_path / "p02b.md"
    output.write_text(json.dumps(result), encoding="utf-8")
    bench.write_markdown(result, markdown, output)

    assert result["schema_version"] == "low_rank_ledh_route_internal_gradient_connectivity.v1"
    assert result["evidence_class"] == "cpu_hidden_debug_only"
    assert result["h5_decidable"] is True
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["seed"] == 91001
    assert row["probe_label"] == "center"
    assert "same_tape" in row
    assert "p02a_style_separated_tape" in row
    assert "ab_comparison" in row
    assert row["same_tape"]["missing_required_checkpoints"] == []
    assert "pre_flow_t0" in row["same_tape"]["checkpoints"]
    assert "next_incremental_log_likelihood_t1" in row["same_tape"]["checkpoints"]
    assert "whole_sum_gradient" in row["same_tape"]["checkpoints"]["pre_flow_t0"]
    assert "selected_scalar_gradients" in row["same_tape"]["checkpoints"]["pre_flow_t0"]
    assert "block_sum_gradients" in row["same_tape"]["checkpoints"]["pre_flow_t0"]
    assert markdown.exists()
