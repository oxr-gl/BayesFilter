from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import scalable_ot_nystrom_ledh_pfpf_algorithm_complete as harness


def test_parse_modes_and_defaults_preserve_device_scope() -> None:
    small = harness._parse_args_from_list_for_test(
        ["--mode", "small-reference", "--output", "/tmp/a.json", "--markdown-output", "/tmp/a.md"]
    )
    downstream = harness._parse_args_from_list_for_test(
        ["--mode", "downstream-smoke", "--output", "/tmp/a.json", "--markdown-output", "/tmp/a.md"]
    )
    gpu = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "gpu-scale",
            "--device-scope",
            "visible",
            "--cuda-visible-devices",
            "0",
            "--output",
            "/tmp/a.json",
            "--markdown-output",
            "/tmp/a.md",
        ]
    )

    assert small.device_scope == "cpu"
    assert small.device == "/CPU:0"
    assert downstream.device_scope == "cpu"
    assert downstream.device == "/CPU:0"
    assert gpu.device_scope == "visible"
    assert gpu.tf32_mode == "enabled"


def test_small_reference_fixtures_use_reviewed_counts_and_ranks() -> None:
    fixtures = harness._small_reference_fixtures()

    assert sorted(fixtures) == ["high_dim_low_rank", "ledh_specific_smoke", "small_parity", "tiny_manual"]
    for fixture_name, (expected_count, ranks) in harness.SMALL_REFERENCE_SPECS.items():
        particles, log_weights = fixtures[fixture_name]
        assert particles.shape[1] == expected_count
        assert log_weights.shape[1] == expected_count
        assert harness._rank_list("plan", fixture_name) == list(ranks)


def test_small_reference_build_result_has_required_schema_fields(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "small-reference",
            "--fixtures",
            "tiny_manual",
            "--ranks",
            "4",
            "--output",
            str(tmp_path / "small.json"),
            "--markdown-output",
            str(tmp_path / "small.md"),
        ]
    )

    result = harness.build_result(args)

    assert result["status"] == "PASS"
    for key in (
        "algorithm_family",
        "mode",
        "status",
        "hard_vetoes",
        "run_manifest",
        "source_route",
        "source_route_components",
        "semantic_class",
        "baseline_comparator",
        "transport_object_kind",
        "transport_matrix_materialized",
        "nonclaims",
    ):
        assert key in result
    assert result["mode"] == "small-reference"
    assert result["transport_object_kind"] == "kernel_factors"
    assert result["transport_matrix_materialized"] is False
    assert result["rows"][0]["transport_matrix_shape"][-2:] == [0, 0]
    assert "dense_reference_max_abs_particle_error" in result["rows"][0]
    assert any("no speedup claim" in claim for claim in result["nonclaims"])


def test_downstream_smoke_custom_tiny_row_records_nystrom_route(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "downstream-smoke",
            "--row-spec",
            "8:2:1:3:2",
            "--nystrom-max-iterations",
            "20",
            "--output",
            str(tmp_path / "downstream.json"),
            "--markdown-output",
            str(tmp_path / "downstream.md"),
        ]
    )

    result = harness.build_result(args)

    assert result["mode"] == "downstream-smoke"
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["fixture_id"] == "custom_n8_rank2"
    assert row["rank"] == 2
    assert row["transport_matrix_shapes"][0][-2:] == [0, 0]
    assert row["transport_object_kind"] == "kernel_factors"
    assert "landmark_indices" in row


def test_write_markdown_and_json_ready_roundtrip(tmp_path: Path) -> None:
    args = harness._parse_args_from_list_for_test(
        [
            "--mode",
            "small-reference",
            "--fixtures",
            "tiny_manual",
            "--ranks",
            "4",
            "--output",
            str(tmp_path / "small.json"),
            "--markdown-output",
            str(tmp_path / "small.md"),
        ]
    )
    result = harness.build_result(args)
    json_payload = harness._json_ready(result)
    Path(args.output).write_text(json.dumps(json_payload), encoding="utf-8")
    harness.write_markdown(result, Path(args.markdown_output))

    assert json.loads(Path(args.output).read_text(encoding="utf-8"))["mode"] == "small-reference"
    assert "Non-Claims" in Path(args.markdown_output).read_text(encoding="utf-8")
