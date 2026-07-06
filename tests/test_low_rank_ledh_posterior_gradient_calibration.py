from __future__ import annotations

import json
import os
from pathlib import Path


os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")

from docs.benchmarks import benchmark_low_rank_ledh_posterior_gradient_calibration as bench


def test_p01_contract_defaults_are_xla_tensorflow_and_fixed_probe() -> None:
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
            "unused.json",
        ]
    )

    assert args.jit_compile is True
    assert args.theta_probe_radius == 0.05
    assert args.theta_prior_scale == 0.50
    assert args.low_rank_rank == 16
    assert args.low_rank_assignment_epsilon == 0.25
    assert args.low_rank_alpha == 1.0e-8
    assert args.low_rank_max_projection_iterations == 120


def test_small_cpu_hidden_low_rank_smoke_emits_value_gradient_peak_metrics(tmp_path: Path) -> None:
    args = bench._parse_args_from_list_for_test(
        [
            "--case-ids",
            "lgssm_small_exact_ref",
            "--seeds",
            "91001",
            "--route",
            "low_rank",
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
            str(tmp_path / "p01.json"),
            "--markdown-output",
            str(tmp_path / "p01.md"),
        ]
    )

    result = bench.build_result(args)

    assert result["schema_version"] == "low_rank_ledh_posterior_gradient_calibration.v1"
    assert result["evidence_class"] == "cpu_hidden_command_shape_debug_only"
    assert "no calibrated threshold claim" in result["nonclaims"]
    assert len(result["rows"]) == 1
    row = result["rows"][0]
    assert row["case_id"] == "lgssm_small_exact_ref"
    assert row["seed"] == 91001
    assert row["route"] == "low_rank"
    assert row["theta_parameterization"]["peak_scope"] == "fixed_predeclared_probe_neighborhood_not_global_map"
    assert len(row["diagnostic_repeat_summaries"]) == 1
    assert "center_factor_marginal_residual" in row["diagnostic_repeat_summaries"][0]
    assert len(row["probe_rows"]) == 7
    center = row["probe_rows"][0]
    assert center["probe_label"] == "center"
    assert center["theta"] == [0.0, 0.0]
    assert isinstance(center["exact"]["posterior_value"], float)
    assert len(center["exact"]["gradient"]) == 2
    assert len(center["route"]["gradient"]) == 2
    assert isinstance(center["value_abs_error"], float)
    assert isinstance(center["gradient_relative_norm_error"], float)
    assert center["route_diagnostics"]["transport_matrix_materialized"] is False
    assert "max_factor_marginal_residual" in center["route_diagnostics"]
    assert "max_value_abs_error_over_probes" in row["peak_neighborhood"]
    assert "gradient_relative_norm_error_max" in row["gradient_summary"]


def test_main_writes_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "p01.json"
    markdown = tmp_path / "p01.md"
    argv = [
        "benchmark_low_rank_ledh_posterior_gradient_calibration.py",
        "--case-ids",
        "lgssm_small_exact_ref",
        "--seeds",
        "91001",
        "--route",
        "low_rank",
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
    assert loaded["rows"][0]["probe_rows"][0]["exact"]["finite_value_gradient"] is True
    assert loaded["rows"][0]["probe_rows"][0]["route_diagnostics"]["transport_matrix_materialized"] is False
    assert markdown.exists()


def test_new_harness_does_not_contain_active_numpy_markers() -> None:
    source = Path(bench.__file__).read_text(encoding="utf-8")
    assert "import " + "numpy" not in source
    assert "from " + "numpy" not in source
    assert "." + "numpy(" not in source
