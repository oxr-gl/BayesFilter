from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_low_rank_ledh_lgssm_kalman_gate as bench


def test_pinned_cases_match_reviewed_p01_contract(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--case-ids",
            "lgssm_small_exact_ref",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--output",
            str(tmp_path / "lgssm.json"),
        ]
    )

    case = bench.PINNED_CASES["lgssm_small_exact_ref"]
    assert args.low_rank_rank == 16
    assert args.low_rank_assignment_epsilon == 0.25
    assert args.low_rank_alpha == 1.0e-8
    assert args.low_rank_max_projection_iterations == 120
    assert case["state_dim"] == 4
    assert case["obs_dim"] == 3
    assert case["time_steps"] == 12
    assert case["num_particles"] == 1024
    assert case["seeds"] == (91001, 91002, 91003)
    assert case["mean_rmse_max"] == 0.25
    assert case["variance_rmse_max"] == 0.35
    assert case["loglik_abs_delta_max"] == 12.0


def test_small_cpu_hidden_command_shape_emits_exact_kalman_metrics(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--case-ids",
            "lgssm_small_exact_ref",
            "--seeds",
            "91001",
            "--route",
            "low_rank",
            "--num-particles",
            "16",
            "--time-steps",
            "1",
            "--low-rank-rank",
            "4",
            "--low-rank-max-projection-iterations",
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
            str(tmp_path / "lgssm.json"),
            "--markdown-output",
            str(tmp_path / "lgssm.md"),
        ]
    )

    result = bench.build_result(args)

    assert result["evidence_class"] == "cpu_hidden_command_shape_debug_only"
    assert result["run_manifest"]["cuda_visible_devices"] == "-1"
    assert result["candidate"]["candidate_id"] == "r16_eps0p25_alpha1em08_it120"
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["case_id"] == "lgssm_small_exact_ref"
    assert row["seed"] == 91001
    assert row["route"] == "low_rank"
    assert row["shape"] == {
        "state_dim": 4,
        "obs_dim": 3,
        "time_steps": 1,
        "num_particles": 16,
    }
    assert row["kalman_reference_finite"] is True
    assert isinstance(row["mean_rmse"], float)
    assert isinstance(row["variance_rmse"], float)
    assert isinstance(row["loglik_abs_delta"], float)
    assert row["route_invocations"] == row["active_resampling_mask_count"] == 1
    assert row["transport_matrix_materialized"] is False
    assert row["transport_object_kind"] == "low_rank_coupling_factors"
    assert row["finite_factors"] is True
    assert row["finite_particles"] is True
    assert row["nonnegative_factors"] is True
    assert row["positive_g"] is True
    assert "no model-suite promotion claim" in result["nonclaims"]


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "lgssm.json"
    markdown = tmp_path / "lgssm.md"
    argv = [
        "benchmark_low_rank_ledh_lgssm_kalman_gate.py",
        "--case-ids",
        "lgssm_small_exact_ref",
        "--seeds",
        "91001",
        "--route",
        "low_rank",
        "--num-particles",
        "16",
        "--time-steps",
        "1",
        "--low-rank-rank",
        "4",
        "--low-rank-max-projection-iterations",
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
    assert loaded["rows"][0]["route"] == "low_rank"
    assert loaded["rows"][0]["transport_matrix_materialized"] is False
    assert loaded["rows"][0]["kalman_reference_finite"] is True
    assert markdown.exists()
