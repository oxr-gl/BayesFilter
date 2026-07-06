from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_low_rank_ledh_gradient_nonfinite_diagnostic as bench


def test_repair_diagnostic_defaults_to_p02_failing_probes() -> None:
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

    assert args.phase_id == "LOW_RANK_GRADIENT_REPAIR_DIAGNOSTIC"
    assert bench._seed_probe_pairs(args) == [
        (91002, "qr_plus"),
        (91003, "center"),
        (91003, "q_plus"),
        (91003, "q_minus"),
        (91003, "r_plus"),
        (91003, "r_minus"),
        (91003, "qr_plus"),
    ]


def test_small_cpu_hidden_diagnostic_writes_json_and_markdown(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--seed-probes",
            "91001:center",
            "--num-particles",
            "8",
            "--time-steps",
            "1",
            "--low-rank-rank",
            "4",
            "--low-rank-max-projection-iterations",
            "8",
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
            "--output",
            str(tmp_path / "repair.json"),
            "--markdown-output",
            str(tmp_path / "repair.md"),
        ]
    )

    result = bench.build_result(args)
    output = tmp_path / "repair.json"
    markdown = tmp_path / "repair.md"
    output.write_text(json.dumps(result), encoding="utf-8")
    bench.write_markdown(result, markdown, output)

    assert result["schema_version"] == "low_rank_ledh_gradient_nonfinite_diagnostic.v1"
    assert result["evidence_class"] == "cpu_hidden_repair_debug_only"
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["seed"] == 91001
    assert row["probe_label"] == "center"
    assert row["route_invocations"] == row["active_resampling_mask_count"] == 1
    assert "log_likelihood_gradient" in row
    assert "final_particles_sum_gradient" in row
    assert markdown.exists()
