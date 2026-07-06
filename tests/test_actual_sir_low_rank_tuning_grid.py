from __future__ import annotations

import json
import subprocess
from pathlib import Path

from docs.benchmarks import run_actual_sir_low_rank_tuning_grid as grid


def _dry_args(tmp_path: Path, *extra: str):
    return grid._parse_args_from_list_for_test(
        [
            "--mode",
            "dry-run",
            "--num-particles",
            "32",
            "--time-steps",
            "1",
            "--batch-seeds",
            "81120",
            "--low-rank-ranks",
            "4,8",
            "--low-rank-assignment-epsilons",
            "0.25,0.125",
            "--low-rank-max-projection-iterations-list",
            "10",
            "--device-scope",
            "cpu",
            "--device",
            "/CPU:0",
            "--expect-device-kind",
            "cpu",
            "--tf32-mode",
            "disabled",
            "--output",
            str(tmp_path / "grid.json"),
            "--markdown-output",
            str(tmp_path / "grid.md"),
            *extra,
        ]
    )


def test_default_certification_grid_defaults_lock_candidate(tmp_path: Path) -> None:
    args = grid._parse_args_from_list_for_test(
        [
            "--mode",
            "dry-run",
            "--output",
            str(tmp_path / "default_grid.json"),
            "--markdown-output",
            str(tmp_path / "default_grid.md"),
        ]
    )

    assert grid.PLAN_PATH.endswith(
        "bayesfilter-dpf-ledh-pfpf-ot-actual-sir-low-rank-default-certification-"
        "master-program-2026-06-24.md"
    )
    assert args.route == "both"
    assert args.low_rank_ranks == [16]
    assert args.low_rank_assignment_epsilons == [0.25]
    assert args.low_rank_alphas == [1.0e-8]
    assert args.low_rank_max_projection_iterations_list == [120]

    result = grid.build_result(args)

    assert result["plan_path"] == grid.PLAN_PATH
    assert result["summary"]["num_candidates"] == 1
    assert result["rows"][0]["candidate"]["candidate_id"] == "r16_eps0p25_alpha1em08_it120"
    assert result["rows"][0]["request_signature"]["route"] == "both"


def test_dry_run_enumerates_bounded_grid(tmp_path: Path) -> None:
    args = _dry_args(tmp_path)
    result = grid.build_result(args)

    assert result["schema_version"] == "actual_sir_low_rank_tuning_grid.v1"
    assert result["status"] == "DRY_RUN"
    assert result["summary"]["num_candidates"] == 4
    assert result["shape"]["state_dim"] == 18
    assert result["shape"]["obs_dim"] == 9
    for row in result["rows"]:
        assert row["status"] == "DRY_RUN"
        assert row["candidate"]["low_rank_rank"] <= result["shape"]["num_particles"]
        assert "--low-rank-rank" in row["command"]
        assert "--low-rank-timing-source" in row["command"]
        assert "compiled_core" in row["command"]
        assert "--jit-compile" in row["command"]
        assert row["request_signature"]["low_rank_timing_source"] == "compiled_core"
        assert row["request_signature"]["jit_compile"] is True
        assert row["row_json"].endswith(".json")
        assert row["row_log"].endswith(".log")


def test_candidate_ids_filter_executes_exact_requested_candidates(tmp_path: Path) -> None:
    args = _dry_args(
        tmp_path,
        "--candidate-ids",
        "r8_eps0p125_alpha1em08_it10,r4_eps0p25_alpha1em08_it10",
    )

    result = grid.build_result(args)

    assert result["status"] == "DRY_RUN"
    assert result["summary"]["num_candidates"] == 2
    assert result["grid"]["candidate_ids"] == [
        "r8_eps0p125_alpha1em08_it10",
        "r4_eps0p25_alpha1em08_it10",
    ]
    assert [row["candidate"]["candidate_id"] for row in result["rows"]] == [
        "r8_eps0p125_alpha1em08_it10",
        "r4_eps0p25_alpha1em08_it10",
    ]


def test_candidate_ids_filter_rejects_missing_candidate(tmp_path: Path) -> None:
    args = _dry_args(tmp_path, "--candidate-ids", "r999_eps0p25_alpha1em08_it10")

    try:
        grid.build_result(args)
    except ValueError as exc:
        assert "candidate-ids not present" in str(exc)
    else:
        raise AssertionError("expected missing candidate id to fail")


def test_candidate_ids_filter_rejects_duplicate_candidate(tmp_path: Path) -> None:
    args = _dry_args(
        tmp_path,
        "--candidate-ids",
        "r4_eps0p25_alpha1em08_it10,r4_eps0p25_alpha1em08_it10",
    )

    try:
        grid.build_result(args)
    except ValueError as exc:
        assert "must not contain duplicates" in str(exc)
    else:
        raise AssertionError("expected duplicate candidate id to fail")


def test_classifies_comparable_but_slow_candidate_without_freeze_nomination() -> None:
    row_result = {
        "status": "PASS",
        "hard_vetoes": [],
        "actual_sir_semantics_pass": True,
        "paired_comparability": {
            "log_likelihood_max_abs_delta": 1.0,
            "log_likelihood_mean_abs_delta": 0.5,
            "filtered_mean_relative_l2": 0.1,
            "filtered_mean_rms": 1.0,
            "filtered_variance_relative_l2": 0.2,
            "filtered_variance_rms": 5.0,
            "final_particle_mean_relative_l2": 0.1,
            "final_particle_mean_abs_l2": 1.0,
            "warm_median_streaming_over_low_rank": 0.5,
            "thresholds": {
                "log_likelihood_max_abs_delta": 10.0,
                "log_likelihood_mean_abs_delta": 5.0,
                "filtered_mean_relative_l2": 0.20,
                "filtered_mean_rms": 2.5,
                "filtered_variance_relative_l2": 0.75,
                "filtered_variance_rms": 25.0,
                "final_particle_mean_relative_l2": 0.20,
                "final_particle_mean_abs_l2": 25.0,
                "warm_median_streaming_over_low_rank": 1.25,
            },
        },
        "rows": [
            {"route": "streaming", "hard_vetoes": []},
            {
                "route": "low_rank",
                "hard_vetoes": [],
                "low_rank_timing_source": "compiled_core",
                "jit_compile": True,
                "low_rank_rank": 4,
                "low_rank_assignment_epsilon": 0.25,
                "low_rank_alpha": 1.0e-8,
                "low_rank_max_projection_iterations": 10,
                "low_rank_convergence_threshold": 1.0e-6,
                "low_rank_denominator_floor": 1.0e-30,
                "route_invocations": 1,
                "active_resampling_mask_count": 1,
                "max_factor_marginal_residual": 1.0e-6,
                "all_finite_factors": True,
                "all_nonnegative_factors": True,
                "all_positive_g": True,
            },
        ],
        "run_manifest": {
            "selected_physical_gpu": {"status": "cpu_hidden"},
            "streaming_timing_source": "compiled_core",
            "low_rank_timing_source": "compiled_core",
            "jit_compile": True,
            "precision": {"tf32_execution_enabled": False},
        },
    }

    classification = grid._classify_row_result(row_result)

    assert classification["candidate_label"] == "comparable-but-slow"
    assert classification["paired_comparability_pass"] is True
    assert classification["warm_time_screen_pass"] is False
    assert classification["low_rank_provenance_complete"] is True


def test_main_writes_dry_run_json_and_markdown(tmp_path: Path, monkeypatch) -> None:
    output = tmp_path / "grid.json"
    markdown = tmp_path / "grid.md"
    argv = [
        "run_actual_sir_low_rank_tuning_grid.py",
        "--mode",
        "dry-run",
        "--num-particles",
        "16",
        "--low-rank-ranks",
        "4",
        "--low-rank-assignment-epsilons",
        "0.25",
        "--low-rank-max-projection-iterations-list",
        "10",
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--tf32-mode",
        "disabled",
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
        "--quiet",
    ]
    monkeypatch.setattr(grid.sys, "argv", argv)

    grid.main()

    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["status"] == "DRY_RUN"
    assert loaded["summary"]["num_candidates"] == 1
    assert markdown.exists()


def test_cpu_hidden_candidate_is_not_freeze_nominated() -> None:
    row_result = {
        "status": "PASS",
        "hard_vetoes": [],
        "actual_sir_semantics_pass": True,
        "paired_comparability": {
            "log_likelihood_max_abs_delta": 1.0,
            "log_likelihood_mean_abs_delta": 0.5,
            "filtered_mean_relative_l2": 0.1,
            "filtered_mean_rms": 1.0,
            "filtered_variance_relative_l2": 0.2,
            "filtered_variance_rms": 5.0,
            "final_particle_mean_relative_l2": 0.1,
            "final_particle_mean_abs_l2": 1.0,
            "warm_median_streaming_over_low_rank": 2.0,
        },
        "rows": [
            {"route": "streaming", "hard_vetoes": []},
            {
                "route": "low_rank",
                "hard_vetoes": [],
                "low_rank_timing_source": "compiled_core",
                "jit_compile": True,
                "low_rank_rank": 4,
                "low_rank_assignment_epsilon": 0.25,
                "low_rank_alpha": 1.0e-8,
                "low_rank_max_projection_iterations": 10,
                "low_rank_convergence_threshold": 1.0e-6,
                "low_rank_denominator_floor": 1.0e-30,
                "route_invocations": 1,
                "active_resampling_mask_count": 1,
                "max_factor_marginal_residual": 1.0e-6,
                "all_finite_factors": True,
                "all_nonnegative_factors": True,
                "all_positive_g": True,
            },
        ],
        "run_manifest": {
            "device_scope": "cpu",
            "expect_device_kind": "cpu",
            "selected_physical_gpu": {"status": "cpu_hidden"},
            "streaming_timing_source": "compiled_core",
            "low_rank_timing_source": "compiled_core",
            "jit_compile": True,
            "precision": {"tf32_execution_enabled": False, "tf32_mode": "disabled", "dtype": "float32"},
        },
    }

    classification = grid._classify_row_result(row_result)

    assert classification["paired_comparability_pass"] is True
    assert classification["warm_time_screen_pass"] is True
    assert classification["low_rank_provenance_complete"] is True
    assert classification["gpu_tf32_provenance_complete"] is False
    assert classification["candidate_label"] == "schema-valid-nonpromotional"


def test_gpu_tf32_candidate_can_be_freeze_nominated() -> None:
    row_result = {
        "status": "PASS",
        "hard_vetoes": [],
        "actual_sir_semantics_pass": True,
        "paired_comparability": {
            "log_likelihood_max_abs_delta": 1.0,
            "log_likelihood_mean_abs_delta": 0.5,
            "filtered_mean_relative_l2": 0.1,
            "filtered_mean_rms": 1.0,
            "filtered_variance_relative_l2": 0.2,
            "filtered_variance_rms": 5.0,
            "final_particle_mean_relative_l2": 0.1,
            "final_particle_mean_abs_l2": 1.0,
            "warm_median_streaming_over_low_rank": 2.0,
        },
        "rows": [
            {"route": "streaming", "hard_vetoes": []},
            {
                "route": "low_rank",
                "hard_vetoes": [],
                "low_rank_timing_source": "compiled_core",
                "jit_compile": True,
                "low_rank_rank": 4,
                "low_rank_assignment_epsilon": 0.25,
                "low_rank_alpha": 1.0e-8,
                "low_rank_max_projection_iterations": 10,
                "low_rank_convergence_threshold": 1.0e-6,
                "low_rank_denominator_floor": 1.0e-30,
                "route_invocations": 1,
                "active_resampling_mask_count": 1,
                "max_factor_marginal_residual": 1.0e-6,
                "all_finite_factors": True,
                "all_nonnegative_factors": True,
                "all_positive_g": True,
            },
        ],
        "run_manifest": {
            "device_scope": "visible",
            "expect_device_kind": "gpu",
            "selected_physical_gpu": {"status": "selected", "uuid": "GPU-test"},
            "streaming_timing_source": "compiled_core",
            "low_rank_timing_source": "compiled_core",
            "jit_compile": True,
            "precision": {"tf32_execution_enabled": True, "tf32_mode": "enabled", "dtype": "float32"},
        },
    }

    classification = grid._classify_row_result(row_result)

    assert classification["paired_comparability_pass"] is True
    assert classification["warm_time_screen_pass"] is True
    assert classification["low_rank_provenance_complete"] is True
    assert classification["gpu_tf32_provenance_complete"] is True
    assert classification["candidate_label"] == "freeze-nominated"


def test_aggregate_existing_rejects_missing_markdown(tmp_path: Path) -> None:
    args = _dry_args(tmp_path, "--mode", "aggregate-existing")
    candidate = grid._candidate_grid(args)[0]
    row_json, _row_md, _row_log = grid._row_paths(args, candidate)
    row_json.parent.mkdir(parents=True, exist_ok=True)
    row_json.write_text("{}", encoding="utf-8")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "MISSING"
    assert row["classification"]["hard_vetoes"] == ["row_markdown_missing"]


def test_row_artifact_names_are_bounded_for_long_n2048_request(tmp_path: Path) -> None:
    args = grid._parse_args_from_list_for_test(
        [
            "--mode",
            "dry-run",
            "--route",
            "both",
            "--batch-seeds",
            "81133,81134",
            "--time-steps",
            "20",
            "--num-particles",
            "2048",
            "--low-rank-ranks",
            "16",
            "--low-rank-assignment-epsilons",
            "0.25,0.125",
            "--low-rank-max-projection-iterations-list",
            "120",
            "--candidate-ids",
            "r16_eps0p25_alpha1em08_it120,r16_eps0p125_alpha1em08_it120",
            "--warmups",
            "1",
            "--repeats",
            "2",
            "--dtype",
            "float32",
            "--tf32-mode",
            "enabled",
            "--device-scope",
            "visible",
            "--cuda-visible-devices",
            "1",
            "--device",
            "/GPU:0",
            "--expect-device-kind",
            "gpu",
            "--jit-compile",
            "--row-timeout-seconds",
            "5400",
            "--output",
            str(tmp_path / "actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.json"),
            "--markdown-output",
            str(tmp_path / "actual-sir-low-rank-n2048-minimal-rank-validation-2026-06-23.md"),
        ]
    )

    result = grid.build_result(args)

    assert result["status"] == "DRY_RUN"
    assert result["grid"]["candidate_ids"] == [
        "r16_eps0p25_alpha1em08_it120",
        "r16_eps0p125_alpha1em08_it120",
    ]
    assert len(result["rows"]) == 2
    row_json_paths = [row["row_json"] for row in result["rows"]]
    row_markdown_paths = [row["row_markdown"] for row in result["rows"]]
    row_log_paths = [row["row_log"] for row in result["rows"]]
    assert len(set(row_json_paths)) == len(row_json_paths)
    assert len(set(row_markdown_paths)) == len(row_markdown_paths)
    assert len(set(row_log_paths)) == len(row_log_paths)
    for row in result["rows"]:
        paths = [Path(row["row_json"]), Path(row["row_markdown"]), Path(row["row_log"])]
        assert all(len(path.name) <= grid.MAX_ARTIFACT_FILENAME_COMPONENT_LENGTH for path in paths)
        assert all("-h" in path.stem for path in paths)
        assert row["request_signature"]["num_particles"] == 2048
        assert row["request_signature"]["batch_seeds"] == [81133, 81134]

    repeated = grid.build_result(args)
    assert [row["row_json"] for row in repeated["rows"]] == [row["row_json"] for row in result["rows"]]


def test_aggregate_existing_rejects_missing_json(tmp_path: Path) -> None:
    args = _dry_args(tmp_path, "--mode", "aggregate-existing")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "MISSING"
    assert row["classification"]["hard_vetoes"] == ["row_json_missing"]


def test_aggregate_existing_rejects_request_drift(tmp_path: Path) -> None:
    args = _dry_args(tmp_path, "--mode", "aggregate-existing")
    candidate = grid._candidate_grid(args)[0]
    row_json, row_md, _row_log = grid._row_paths(args, candidate)
    row_json.parent.mkdir(parents=True, exist_ok=True)
    row_md.write_text("# stale row\n", encoding="utf-8")
    stale = {
        "shape": {
            "batch_size": 1,
            "time_steps": 1,
            "num_particles": 32,
        },
        "batch_seeds": [81120],
        "transport_policy": "active-all",
        "route_request": "both",
        "rows": [
            {
                "route": "streaming",
                "hard_vetoes": [],
                "streaming_timing_source": "diagnostic_loop",
                "sinkhorn_iterations": 10,
                "sinkhorn_epsilon": 1.0,
                "annealed_scaling": 0.9,
                "annealed_convergence_threshold": 1.0e-3,
            },
            {
                "route": "low_rank",
                "hard_vetoes": [],
                "low_rank_timing_source": "diagnostic_loop",
                "jit_compile": False,
                "low_rank_rank": 4,
                "low_rank_assignment_epsilon": 0.25,
                "low_rank_alpha": 1.0e-8,
                "low_rank_max_projection_iterations": 10,
                "low_rank_convergence_threshold": 1.0e-6,
                "low_rank_denominator_floor": 1.0e-30,
            },
        ],
        "run_manifest": {
            "device_scope": "cpu",
            "requested_cuda_visible_devices": None,
            "device": "/CPU:0",
            "expect_device_kind": "cpu",
            "command": "--row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64",
            "streaming_timing_source": "diagnostic_loop",
            "low_rank_timing_source": "diagnostic_loop",
            "jit_compile": False,
            "precision": {"dtype": "float32", "tf32_mode": "disabled"},
        },
    }
    row_json.write_text(json.dumps(stale), encoding="utf-8")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "MISMATCH"
    assert row["classification"]["hard_vetoes"] == ["row_request_mismatch"]
    assert "streaming_timing_source" in row["error"]
    assert "low_rank_timing_source" in row["error"]
    assert "jit_compile" in row["error"]


def test_top_level_status_fails_for_corrupt_artifact(tmp_path: Path) -> None:
    args = _dry_args(tmp_path, "--mode", "aggregate-existing")
    candidate = grid._candidate_grid(args)[0]
    row_json, row_md, _row_log = grid._row_paths(args, candidate)
    row_json.parent.mkdir(parents=True, exist_ok=True)
    row_md.write_text("# corrupt row\n", encoding="utf-8")
    row_json.write_text("{", encoding="utf-8")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "CORRUPT"
    assert row["classification"]["hard_vetoes"] == ["row_json_corrupt"]


def test_execute_mode_nonzero_exit_fails_top_level(tmp_path: Path, monkeypatch) -> None:
    args = _dry_args(tmp_path, "--mode", "execute", "--row-timeout-seconds", "1")

    def _fake_run(*_args, **_kwargs):
        return subprocess.CompletedProcess(args=["fake"], returncode=2)

    monkeypatch.setattr(grid.subprocess, "run", _fake_run)
    monkeypatch.setattr(grid, "_run_text", lambda *_args, **_kwargs: "test")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "ERROR"
    assert row["classification"]["hard_vetoes"] == ["row_subprocess_nonzero_exit"]


def test_execute_mode_timeout_fails_top_level(tmp_path: Path, monkeypatch) -> None:
    args = _dry_args(tmp_path, "--mode", "execute", "--row-timeout-seconds", "1")

    def _fake_timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired(cmd="fake", timeout=1)

    monkeypatch.setattr(grid.subprocess, "run", _fake_timeout)
    monkeypatch.setattr(grid, "_run_text", lambda *_args, **_kwargs: "test")

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "TIMEOUT"
    assert row["classification"]["hard_vetoes"] == ["row_timeout"]


def test_streaming_only_request_does_not_require_low_rank_row(tmp_path: Path) -> None:
    args = _dry_args(
        tmp_path,
        "--mode",
        "aggregate-existing",
        "--route",
        "streaming",
        "--low-rank-ranks",
        "4",
        "--low-rank-assignment-epsilons",
        "0.25",
    )
    candidate = grid._candidate_grid(args)[0]
    row_json, row_md, _row_log = grid._row_paths(args, candidate)
    row_json.parent.mkdir(parents=True, exist_ok=True)
    row_md.write_text("# streaming row\n", encoding="utf-8")
    row_json.write_text(
        json.dumps(
            {
                "status": "PASS",
                "shape": {"batch_size": 1, "time_steps": 1, "num_particles": 32},
                "batch_seeds": [81120],
                "transport_policy": "active-all",
                "route_request": "streaming",
                "actual_sir_semantics_pass": True,
                "rows": [
                    {
                        "route": "streaming",
                        "hard_vetoes": [],
                        "streaming_timing_source": "compiled_core",
                        "sinkhorn_iterations": 10,
                        "sinkhorn_epsilon": 1.0,
                        "annealed_scaling": 0.9,
                        "annealed_convergence_threshold": 1.0e-3,
                    }
                ],
                "run_manifest": {
                    "device_scope": "cpu",
                    "requested_cuda_visible_devices": None,
                    "device": "/CPU:0",
                    "expect_device_kind": "cpu",
                    "command": "--row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64",
                    "streaming_timing_source": "compiled_core",
                    "low_rank_timing_source": "compiled_core",
                    "jit_compile": True,
                    "precision": {"dtype": "float32", "tf32_mode": "disabled"},
                },
            }
        ),
        encoding="utf-8",
    )

    result = grid.build_result(args)

    assert result["status"] == "PASS"
    assert result["rows"][0]["status"] == "PASS"


def test_streaming_request_rejects_missing_streaming_row(tmp_path: Path) -> None:
    args = _dry_args(
        tmp_path,
        "--mode",
        "aggregate-existing",
        "--route",
        "streaming",
        "--low-rank-ranks",
        "4",
        "--low-rank-assignment-epsilons",
        "0.25",
    )
    candidate = grid._candidate_grid(args)[0]
    row_json, row_md, _row_log = grid._row_paths(args, candidate)
    row_json.parent.mkdir(parents=True, exist_ok=True)
    row_md.write_text("# missing streaming row\n", encoding="utf-8")
    row_json.write_text(
        json.dumps(
            {
                "status": "PASS",
                "shape": {"batch_size": 1, "time_steps": 1, "num_particles": 32},
                "batch_seeds": [81120],
                "transport_policy": "active-all",
                "route_request": "streaming",
                "actual_sir_semantics_pass": True,
                "rows": [],
                "run_manifest": {
                    "device_scope": "cpu",
                    "requested_cuda_visible_devices": None,
                    "device": "/CPU:0",
                    "expect_device_kind": "cpu",
                    "command": "--row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 64",
                    "streaming_timing_source": "compiled_core",
                    "low_rank_timing_source": "compiled_core",
                    "jit_compile": True,
                    "precision": {"dtype": "float32", "tf32_mode": "disabled"},
                },
            }
        ),
        encoding="utf-8",
    )

    result = grid.build_result(args)

    assert result["status"] == "FAIL"
    row = result["rows"][0]
    assert row["status"] == "MISMATCH"
    assert "missing_streaming_row" in row["error"]


def test_route_execution_sources_have_no_numpy_barriers() -> None:
    solver = Path("experiments/dpf_implementation/tf_tfp/resampling/low_rank_coupling_solver_tf.py").read_text(
        encoding="utf-8"
    )
    harness = Path("docs/benchmarks/benchmark_actual_sir_low_rank_route_validation.py").read_text(encoding="utf-8")
    compiled_region = harness[harness.index("def _streaming_value_core(") : harness.index("def _run_streaming_compiled_core_timed(")]

    assert "import numpy" not in solver
    assert "np." not in solver
    assert ".numpy(" not in solver
    assert ".numpy(" not in compiled_region
    assert "def _run_route_loop(" not in harness
    assert "low_rank_coupling_solver_resample_tf(" not in compiled_region
