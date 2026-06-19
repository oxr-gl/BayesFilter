from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")


ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/home/ubuntu/anaconda3/envs/tfgpu/bin/python"


def _run_benchmark(
    script: str,
    *args: str,
    output_name: str,
    state_dim: str = "2",
    obs_dim: str = "2",
    parameter_dim: str = "2",
) -> dict[str, object]:
    output = Path("/tmp") / output_name
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(ROOT / script),
        *args,
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--batch-size",
        "2",
        "--time-steps",
        "3",
        "--state-dim",
        state_dim,
        "--obs-dim",
        obs_dim,
        "--parameter-dim",
        parameter_dim,
        "--warmups",
        "1",
        "--repeats",
        "1",
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    return json.loads(output.read_text(encoding="utf-8"))


def _assert_compiled_result(result: dict[str, object], *, mode: str) -> None:
    compiler = result["compiler"]
    assert isinstance(compiler, dict)
    assert compiler["tf_function"] is True
    assert compiler["jit_compile"] is True
    assert compiler["warm_calls_exclude_compile"] is True
    assert result["mode"] == mode
    assert result["finite_outputs"] is True
    assert result["value_shape"] == [2]
    assert result["score_shape"] == [2, 2]
    assert "GPU" not in str(result["value_device"]).upper()
    assert "GPU" not in str(result["score_device"]).upper()


def test_kalman_harness_accepts_compiled_and_scalar_loop_modes() -> None:
    help_result = subprocess.run(
        [
            PYTHON,
            str(ROOT / "docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py"),
            "--help",
        ],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert "compiled-timing" in help_result.stdout
    assert "scalar-compiled-loop" in help_result.stdout


def test_kalman_compiled_timing_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py",
        "--mode",
        "compiled-timing",
        output_name="experimental-kalman-compiled-tiny.json",
    )

    _assert_compiled_result(result, mode="compiled-timing")
    assert result["compiler"]["compiled_unit"] == "batched_value_score"


def test_kalman_scalar_compiled_loop_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_kalman_cpu_gpu.py",
        "--mode",
        "scalar-compiled-loop",
        output_name="experimental-kalman-scalar-loop-tiny.json",
    )

    _assert_compiled_result(result, mode="scalar-compiled-loop")
    assert result["compiler"]["compiled_unit"] == "one_scalar_value_score_row"
    assert result["compiler"]["python_loop_over_rows_in_benchmark_harness"] is True


def test_svd_compiled_timing_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py",
        "--mode",
        "compiled-timing",
        "--backend",
        "tf_svd_ukf",
        output_name="experimental-svd-compiled-tiny.json",
    )

    _assert_compiled_result(result, mode="compiled-timing")
    assert result["compiler"]["compile_and_first_call_seconds"] >= 0.0


def test_svd_scalar_loop_mode_is_available_for_feasibility_artifacts() -> None:
    help_result = subprocess.run(
        [
            PYTHON,
            str(
                ROOT
                / "docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py"
            ),
            "--help",
        ],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert "scalar-compiled-loop" in help_result.stdout


def test_svd_harness_lists_principal_sqrt_backend_and_blocks_scalar_comparator() -> None:
    help_result = subprocess.run(
        [
            PYTHON,
            str(
                ROOT
                / "docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py"
            ),
            "--help",
        ],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert "tf_principal_sqrt_ukf" in help_result.stdout

    output = Path("/tmp") / "experimental-svd-principal-sqrt-parity-blocked.json"
    command = [
        PYTHON,
        str(ROOT / "docs/benchmarks/benchmark_experimental_batched_svd_sigma_point_cpu_gpu.py"),
        "--mode",
        "parity",
        "--backend",
        "tf_principal_sqrt_ukf",
        "--batch-size",
        "2",
        "--time-steps",
        "3",
        "--state-dim",
        "2",
        "--obs-dim",
        "2",
        "--parameter-dim",
        "2",
        "--output",
        str(output),
    ]
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)

    assert result.returncode != 0
    assert "no scalar score comparator" in result.stderr


def test_ledh_pfpf_ot_compiled_value_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py",
        "--mode",
        "compiled-value",
        "--num-particles",
        "4",
        "--transport-policy",
        "active",
        "--transport-gradient-mode",
        "raw",
        "--sinkhorn-iterations",
        "4",
        output_name="experimental-ledh-pfpf-ot-compiled-value-tiny.json",
        state_dim="1",
        obs_dim="1",
        parameter_dim="3",
    )

    compiler = result["compiler"]
    assert isinstance(compiler, dict)
    assert compiler["tf_function"] is True
    assert compiler["jit_compile"] is True
    assert result["mode"] == "compiled-value"
    assert result["finite_outputs"] is True
    assert result["output_shapes"] == [[2]]
    assert result["shape"]["parameter_dim"] == 3
    assert "GPU" not in str(result["output_devices"]).upper()


def test_ledh_pfpf_ot_compiled_value_score_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py",
        "--mode",
        "compiled-value-score",
        "--num-particles",
        "4",
        "--transport-policy",
        "no-resampling",
        "--transport-gradient-mode",
        "raw",
        "--sinkhorn-iterations",
        "4",
        output_name="experimental-ledh-pfpf-ot-compiled-value-score-tiny.json",
        state_dim="1",
        obs_dim="1",
        parameter_dim="3",
    )

    compiler = result["compiler"]
    assert isinstance(compiler, dict)
    assert compiler["tf_function"] is True
    assert compiler["jit_compile"] is True
    assert result["mode"] == "compiled-value-score"
    assert result["finite_outputs"] is True
    assert result["output_shapes"] == [[2], [2, 3]]
    assert "GPU" not in str(result["output_devices"]).upper()


def test_ledh_pfpf_ot_parity_mode_tiny_cpu_json() -> None:
    result = _run_benchmark(
        "docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_cpu_gpu.py",
        "--mode",
        "parity",
        "--num-particles",
        "4",
        "--transport-policy",
        "active",
        "--transport-gradient-mode",
        "raw",
        "--sinkhorn-iterations",
        "4",
        output_name="experimental-ledh-pfpf-ot-parity-tiny.json",
        state_dim="1",
        obs_dim="1",
        parameter_dim="3",
    )

    assert result["compiler"]["tf_function"] is True
    assert result["compiler"]["jit_compile"] is True
    assert result["mode"] == "parity"
    assert result["parity_passed"] is True
    assert result["value_max_abs_delta"] == 0.0


def test_ledh_pfpf_ot_correctness_gate_tiny_cpu_json() -> None:
    output = Path("/tmp") / "experimental-ledh-pfpf-ot-correctness-gate-tiny.json"
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(ROOT / "docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_correctness.py"),
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--batch-size",
        "2",
        "--time-steps",
        "3",
        "--num-particles",
        "4",
        "--transport-policy",
        "active",
        "--transport-gradient-mode",
        "raw",
        "--sinkhorn-iterations",
        "4",
        "--skip-jit-smoke",
        "--skip-score-fd",
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["overall_passed"] is True
    assert result["checks"][0]["name"] == "finite_outputs"
    assert result["checks"][1]["name"] == "batched_vs_scalar_value_parity"
    assert result["source_diagnostics"]["uses_python_time_loop"] is True
    assert result["source_diagnostics"]["uses_tf_while_loop"] is False


def test_ledh_pfpf_ot_efficiency_matrix_tiny_cpu_json() -> None:
    output = Path("/tmp") / "experimental-ledh-pfpf-ot-efficiency-matrix-tiny.json"
    artifact_dir = Path("/tmp") / "experimental-ledh-pfpf-ot-efficiency-matrix-children"
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(
            ROOT
            / "docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_efficiency_matrix.py"
        ),
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--shape",
        "B=2,T=3,N=4",
        "--transport-policy",
        "no-resampling",
        "--mode",
        "compiled-value",
        "--sinkhorn-iterations",
        "4",
        "--warmups",
        "0",
        "--repeats",
        "1",
        "--skip-correctness-preflight",
        "--artifact-dir",
        str(artifact_dir),
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["overall_passed"] is True
    assert result["correctness_preflight"]["skipped"] is True
    assert len(result["children"]) == 1
    assert result["children"][0]["passed"] is True
    assert result["children"][0]["finite_outputs"] is True


def test_streaming_ledh_pfpf_ot_correctness_gate_tiny_cpu_json() -> None:
    output = Path("/tmp") / "experimental-ledh-pfpf-ot-streaming-correctness-tiny.json"
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(
            ROOT
            / "docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py"
        ),
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--batch-size",
        "2",
        "--time-steps",
        "3",
        "--num-particles",
        "4",
        "--transport-policy",
        "active",
        "--sinkhorn-iterations",
        "4",
        "--row-chunk-size",
        "2",
        "--col-chunk-size",
        "2",
        "--particle-chunk-size",
        "2",
        "--skip-jit-smoke",
        "--skip-score-fd",
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["overall_passed"] is True
    assert result["checks"][0]["name"] == "finite_outputs"
    assert result["source_diagnostics"]["uses_tf_while_loop"] is True
    assert result["source_diagnostics"]["uses_python_time_loop"] is False
    assert result["transport"]["plan_mode"] == "streaming"


def test_streaming_ledh_pfpf_ot_lgssm_benchmark_tiny_cpu_json() -> None:
    output = Path("/tmp") / "experimental-ledh-pfpf-ot-streaming-lgssm-tiny.json"
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(
            ROOT
            / "docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py"
        ),
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--batch-size",
        "1",
        "--time-steps",
        "3",
        "--num-particles",
        "4",
        "--state-dim",
        "2",
        "--obs-dim",
        "2",
        "--transport-policy",
        "active-odd",
        "--proposal-mode",
        "callback",
        "--sinkhorn-iterations",
        "4",
        "--row-chunk-size",
        "2",
        "--col-chunk-size",
        "2",
        "--particle-chunk-size",
        "2",
        "--warmups",
        "0",
        "--repeats",
        "1",
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["finite_output"] is True
    assert result["proposal_mode"] == "callback"
    assert result["stores_full_pre_flow_particles"] is False
    assert result["transport"]["plan_mode"] == "streaming"
    assert result["transport"]["dense_transport_matrix_materialized"] is False
    assert result["return_history"] is False


def test_streaming_ledh_pfpf_ot_precision_comparison_tiny_cpu_json() -> None:
    output = Path("/tmp") / "experimental-ledh-pfpf-ot-streaming-precision-tiny.json"
    artifact_dir = Path("/tmp") / "experimental-ledh-pfpf-ot-streaming-precision-tiny-children"
    if output.exists():
        output.unlink()
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    command = [
        PYTHON,
        str(
            ROOT
            / "docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_streaming_precision.py"
        ),
        "--device-scope",
        "cpu",
        "--device",
        "/CPU:0",
        "--expect-device-kind",
        "cpu",
        "--batch-size",
        "1",
        "--time-steps",
        "3",
        "--num-particles",
        "4",
        "--state-dim",
        "2",
        "--obs-dim",
        "2",
        "--transport-policy",
        "active-odd",
        "--proposal-mode",
        "callback",
        "--sinkhorn-iterations",
        "4",
        "--row-chunk-size",
        "2",
        "--col-chunk-size",
        "2",
        "--particle-chunk-size",
        "2",
        "--warmups",
        "0",
        "--repeats",
        "1",
        "--artifact-dir",
        str(artifact_dir),
        "--output",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT, env=env, capture_output=True, text=True)
    result = json.loads(output.read_text(encoding="utf-8"))

    assert result["overall_passed"] is True
    assert len(result["children"]) == 3
    assert {child["arm_id"] for child in result["children"]} == {
        "fp64_reference",
        "fp32_tf32_disabled",
        "fp32_tf32_enabled",
    }
    assert len(result["comparisons"]) == 2
    for comparison in result["comparisons"]:
        assert comparison["finite_output"] is True
        assert "log_likelihood" in comparison["drift_vs_fp64"]
