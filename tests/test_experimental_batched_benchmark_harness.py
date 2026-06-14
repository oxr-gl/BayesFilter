from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")


ROOT = Path(__file__).resolve().parents[1]
PYTHON = "/home/ubuntu/anaconda3/envs/tfgpu/bin/python"


def _run_benchmark(script: str, *args: str, output_name: str) -> dict[str, object]:
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
        "2",
        "--obs-dim",
        "2",
        "--parameter-dim",
        "2",
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
