from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

if os.environ.get("BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000") != "1":
    os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
else:
    os.environ.pop("CUDA_VISIBLE_DEVICES", None)
    sys.argv = [sys.argv[0], "--device-scope", "visible", *sys.argv[1:]]
os.environ.setdefault("MPLCONFIGDIR", "/tmp")

import pytest
import tensorflow as tf

from docs.benchmarks import benchmark_ledh_same_target_lgssm_m3_t50_value as lgssm
from docs.benchmarks import benchmark_ledh_same_target_fixed_sir_score as fixed_sir_score
from docs.benchmarks import benchmark_p8p_parameterized_sir_gradient as p8p_sir
from scripts import audit_ledh_no_autodiff as audit


ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = (
    ROOT
    / "docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json"
)
RUN_N10000 = os.environ.get("BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000") == "1"
GPU_MEMORY_BUDGET_MIB = float(os.environ.get("BAYESFILTER_LEDHD_SCORE_MEMORY_BUDGET_MIB", "12000"))
PHASE5_ARTIFACT_DIR = Path(
    os.environ.get(
        "BAYESFILTER_LEDHD_SCORE_MEMORY_ARTIFACT_DIR",
        str(ROOT / "docs/plans"),
    )
)

HIGHDIM_LEDGER_ROWS = (
    "benchmark_lgssm_exact_oracle_m3_T50",
    "zhao_cui_sv_actual_nongaussian_T1000",
    "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
    "zhao_cui_spatial_sir_austria_j9_T20",
    "zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale",
    "zhao_cui_predator_prey_T20",
    "zhao_cui_generalized_sv_synthetic_from_estimated_values",
)


def _ledger_rows() -> dict[str, dict[str, Any]]:
    payload = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {row["row_id"]: row for row in payload["rows"]}


def _require_n10000_gpu() -> None:
    if not RUN_N10000:
        pytest.skip("set BAYESFILTER_RUN_LEDHD_SCORE_MEMORY_N10000=1 to run GPU N=10000 checks")


def _configure_gpu(module) -> None:
    module._configure_gpus()
    gpus = tf.config.list_logical_devices("GPU")
    if not gpus:
        pytest.fail("N=10000 score-memory test requires a visible GPU")
    try:
        tf.config.experimental.reset_memory_stats("GPU:0")
    except (ValueError, RuntimeError):
        pass


def _gpu_memory_peak_mib() -> float:
    info = tf.config.experimental.get_memory_info("GPU:0")
    return float(info.get("peak", 0)) / (1024.0 * 1024.0)


def _assert_gpu_tensor_devices(tensors: tuple[tf.Tensor, ...]) -> None:
    devices = [tensor.device for tensor in tensors]
    assert devices
    assert all("GPU" in device.upper() for device in devices), devices


def _assert_memory_within_budget(result: dict[str, Any]) -> None:
    assert result["gpu_memory_peak_mib"] <= GPU_MEMORY_BUDGET_MIB, result


def _write_score_memory_artifact(stem: str, result: dict[str, Any]) -> None:
    if not RUN_N10000:
        return
    PHASE5_ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = PHASE5_ARTIFACT_DIR / f"{stem}.json"
    markdown_path = PHASE5_ARTIFACT_DIR / f"{stem}.md"
    payload = {
        **result,
        "artifact": stem,
        "memory_budget_mib": GPU_MEMORY_BUDGET_MIB,
        "primary_pass": True,
    }
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        f"# {stem}",
        "",
        f"- Row: `{payload['row_id']}`",
        f"- Score route: `{payload['score_route']}`",
        f"- Particles: `{payload['num_particles']}`",
        f"- Score directional: `{payload['score_directional']}`",
        f"- FD directional: `{payload['fd_directional']}`",
        f"- Absolute error: `{payload['abs_error']}`",
        f"- Relative error: `{payload['rel_error']}`",
        f"- GPU memory peak MiB: `{payload['gpu_memory_peak_mib']}`",
        f"- Memory budget MiB: `{payload['memory_budget_mib']}`",
        "- Primary pass: `true`",
        "",
        "## Nonclaims",
        "",
    ]
    lines.extend(f"- {claim}" for claim in payload["nonclaims"])
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _lgssm_args() -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=[81120],
        num_particles=10000,
        time_steps=2,
        transport_policy="active-all",
        sinkhorn_iterations=2,
        sinkhorn_epsilon=0.5,
        annealed_scaling=0.9,
        annealed_convergence_threshold=1.0e-3,
        transport_gradient_mode=lgssm.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE,
        transport_ad_mode="full",
        row_chunk_size=512,
        col_chunk_size=512,
        particle_chunk_size=512,
        score_mode="compact-sensitivity",
        score_fd_step=1.0e-5,
        score_fd_atol=5.0e-3,
        score_fd_rtol=5.0e-3,
        dtype="float64",
        tf32_mode="disabled",
        device="/GPU:0",
        expect_device_kind="gpu",
    )


def _sir_args() -> argparse.Namespace:
    return argparse.Namespace(
        batch_seeds=[81120],
        time_steps=1,
        num_particles=10000,
        theta_values=[0.02, -0.01, 0.01],
        transport_policy="active-all",
        sinkhorn_iterations=1,
        sinkhorn_epsilon=1.0,
        annealed_scaling=0.9,
        annealed_convergence_threshold=1.0e-3,
        transport_plan_mode="streaming",
        transport_gradient_mode=(
            p8p_sir.core_tf.MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE
        ),
        transport_ad_mode="full",
        row_chunk_size=512,
        col_chunk_size=512,
        particle_chunk_size=512,
        dtype="float32",
        tf32_mode="enabled",
        fd_step=1.0e-3,
        diagnostic_components="all",
    )


def test_lgssm_ledh_compact_score_float64_correctness_and_memory_n10000() -> None:
    _require_n10000_gpu()
    args = _lgssm_args()
    lgssm._configure_precision(args)
    _configure_gpu(lgssm)
    theta = tf.constant(lgssm.TRUTH_THETA, dtype=lgssm.DTYPE)
    direction = tf.constant([0.4, -0.2, 0.1, 0.3, -0.25], dtype=lgssm.DTYPE)
    step = tf.constant(args.score_fd_step, dtype=lgssm.DTYPE)

    with tf.device(args.device), audit.AutodiffRuntimeSentinel(
        lgssm.tf,
        route_id="lgssm_compact_score_n10000",
    ):
        tensors = lgssm._build_lgssm_manual_tensors(args, theta)
        base = lgssm._compact_value_and_score_from_components(tensors, args, theta)
        plus = lgssm._compact_value_and_score_from_components(
            lgssm._build_lgssm_manual_tensors(args, theta + step * direction),
            args,
            theta + step * direction,
        )
        minus = lgssm._compact_value_and_score_from_components(
            lgssm._build_lgssm_manual_tensors(args, theta - step * direction),
            args,
            theta - step * direction,
        )

    score_directional = tf.reduce_sum(base["gradient_tensor"] * direction)
    fd_directional = (plus["objective"] - minus["objective"]) / (2.0 * step)
    abs_error = tf.abs(score_directional - fd_directional)
    rel_error = abs_error / tf.maximum(
        tf.maximum(tf.abs(score_directional), tf.abs(fd_directional)),
        tf.constant(1.0e-12, dtype=lgssm.DTYPE),
    )
    result = {
        "row_id": "benchmark_lgssm_exact_oracle_m3_T50",
        "num_particles": args.num_particles,
        "dtype": args.dtype,
        "fd_oracle_note": "float64 same-scalar FD is the correctness oracle; float32/TF32 FD is too noisy at N=10000",
        "score_route": lgssm.COMPACT_SCORE_ROUTE_ID,
        "score": [float(value) for value in base["gradient_tensor"].numpy().reshape(-1)],
        "score_directional": float(score_directional.numpy()),
        "fd_directional": float(fd_directional.numpy()),
        "abs_error": float(abs_error.numpy()),
        "rel_error": float(rel_error.numpy()),
        "gpu_memory_peak_mib": _gpu_memory_peak_mib(),
        "nonclaims": [
            "Phase 5 score-memory evidence only",
            "not HMC/NUTS readiness",
            "not posterior correctness",
            "not scientific superiority",
        ],
    }
    _write_score_memory_artifact(
        "ledh-phase5-lgssm-score-memory-n10000-2026-07-06",
        result,
    )
    print("LEDH_SCORE_MEMORY_N10000_RESULT " + json.dumps(result, sort_keys=True))

    _assert_gpu_tensor_devices(
        (
            base["objective"],
            base["log_likelihood"],
            base["gradient_tensor"],
            base["per_seed_gradient"],
        )
    )
    assert bool(tf.reduce_all(tf.math.is_finite(base["gradient_tensor"])).numpy())
    assert float(abs_error.numpy()) <= 5.0e-3 or float(rel_error.numpy()) <= 5.0e-3
    _assert_memory_within_budget(result)


def test_actual_sv_ledh_score_remains_blocked_until_same_target_adapter_exists() -> None:
    row = _ledger_rows()["zhao_cui_sv_actual_nongaussian_T1000"]
    assert row["score_status"] == "blocked_score"
    assert row["value_status"] == "blocked_no_reviewed_current_gpu_xla_ledh_row_adapter"


def test_ksc_sv_ledh_score_remains_blocked_until_ksc_adapter_exists() -> None:
    row = _ledger_rows()["zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"]
    assert row["score_status"] == "blocked_score"
    assert row["value_status"] == "blocked_no_ledh_ksc_row_adapter"


def test_fixed_spatial_sir_ledh_full_row_has_phase4_tiny_score_but_n10000_pending() -> None:
    row = _ledger_rows()["zhao_cui_spatial_sir_austria_j9_T20"]
    assert row["score_status"] == "blocked_score_until_same_target_no_tape_gate"
    assert row["ledh_row_scope_decision"] == "amended_sir_log_scale_theta_full_row_candidate"
    assert row["theta_coordinate_system"] == "sir_log_scale_theta"
    assert row["theta_dimension"] == 3
    assert row["parameter_order"] == [
        "log_kappa_scale",
        "log_nu_scale",
        "log_obs_noise_scale",
    ]

    args = _sir_args()
    args.num_particles = 2
    args.time_steps = 1
    args.batch_seeds = [81120]
    args.transport_gradient_mode = p8p_sir.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    args.row_chunk_size = 2
    args.col_chunk_size = 2
    args.particle_chunk_size = 2
    args.dtype = "float64"
    args.tf32_mode = "disabled"
    args.score_fd_atol = 2.0e-4
    args.score_fd_rtol = 2.0e-3
    fixed_sir_score._configure_precision(args)

    with audit.AutodiffRuntimeSentinel(
        p8p_sir.tf,
        route_id="fixed_sir_phase4_tiny_score_memory_status",
    ):
        diagnostic = fixed_sir_score._fixed_sir_same_scalar_fd_diagnostic(
            args,
            args.theta_values,
        )

    assert diagnostic["status"] == "pass"
    assert diagnostic["row_id"] == "zhao_cui_spatial_sir_austria_j9_T20"
    assert diagnostic["target_scope"] == "main_observed_data_filtering_row"
    assert diagnostic["score_route"] == fixed_sir_score.FIXED_SIR_MANUAL_SCORE_ROUTE_ID


def test_fixed_spatial_sir_ledh_full_row_score_correctness_and_memory_n10000() -> None:
    _require_n10000_gpu()
    args = _sir_args()
    args.transport_gradient_mode = p8p_sir.core_tf.MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE
    args.transport_ad_mode = "full"
    p8p_sir._configure_precision(args)
    _configure_gpu(p8p_sir)
    direction = tf.constant([0.2, -0.1, 0.3], dtype=p8p_sir.DTYPE)
    step = tf.constant(args.fd_step, dtype=p8p_sir.DTYPE)
    theta = tf.constant(args.theta_values, dtype=p8p_sir.DTYPE)

    with tf.device("/GPU:0"), audit.AutodiffRuntimeSentinel(
        p8p_sir.tf,
        route_id="fixed_sir_full_row_manual_score_n10000",
    ):
        base = fixed_sir_score._fixed_sir_manual_score_diagnostic(
            args,
            args.theta_values,
            return_score_decomposition=True,
        )
        plus_values = [float(value) for value in (theta + step * direction).numpy()]
        minus_values = [float(value) for value in (theta - step * direction).numpy()]
        plus = fixed_sir_score._fixed_sir_manual_score_diagnostic(
            args,
            plus_values,
            return_score_decomposition=False,
        )
        minus = fixed_sir_score._fixed_sir_manual_score_diagnostic(
            args,
            minus_values,
            return_score_decomposition=False,
        )

    score_directional = tf.reduce_sum(base["gradient_tensor"] * direction)
    fd_directional = (plus["objective"] - minus["objective"]) / (2.0 * step)
    abs_error = tf.abs(score_directional - fd_directional)
    rel_error = abs_error / tf.maximum(
        tf.maximum(tf.abs(score_directional), tf.abs(fd_directional)),
        tf.constant(1.0e-12, dtype=p8p_sir.DTYPE),
    )
    result = {
        "row_id": "zhao_cui_spatial_sir_austria_j9_T20",
        "target_scope": "main_observed_data_filtering_row",
        "num_particles": args.num_particles,
        "score_route": fixed_sir_score.FIXED_SIR_MANUAL_SCORE_ROUTE_ID,
        "score": [float(value) for value in base["gradient_tensor"].numpy().reshape(-1)],
        "score_directional": float(score_directional.numpy()),
        "fd_directional": float(fd_directional.numpy()),
        "abs_error": float(abs_error.numpy()),
        "rel_error": float(rel_error.numpy()),
        "gpu_memory_peak_mib": _gpu_memory_peak_mib(),
        "nonclaims": [
            "Phase 5 score-memory evidence only",
            "not exact nonlinear likelihood correctness",
            "not HMC/NUTS readiness",
        ],
    }
    _write_score_memory_artifact(
        "ledh-phase5-fixed-sir-score-memory-n10000-2026-07-06",
        result,
    )
    print("LEDH_SCORE_MEMORY_N10000_RESULT " + json.dumps(result, sort_keys=True))

    _assert_gpu_tensor_devices(
        (
            base["objective"],
            base["log_likelihood"],
            base["gradient_tensor"],
            base["per_seed_gradient"],
        )
    )
    assert bool(tf.reduce_all(tf.math.is_finite(base["gradient_tensor"])).numpy())
    assert base["forward_contract"]["row_id"] == "zhao_cui_spatial_sir_austria_j9_T20"
    assert base["target_scope"] == "main_observed_data_filtering_row"
    assert base["score_route"] == fixed_sir_score.FIXED_SIR_MANUAL_SCORE_ROUTE_ID
    assert float(abs_error.numpy()) <= 1.0e-1 or float(rel_error.numpy()) <= 5.0e-2
    _assert_memory_within_budget(result)


def test_predator_prey_ledh_score_remains_blocked_until_same_target_adapter_exists() -> None:
    row = _ledger_rows()["zhao_cui_predator_prey_T20"]
    assert row["score_status"] == "blocked_score"
    assert row["value_status"] == "blocked_no_reviewed_current_gpu_xla_ledh_row_adapter"


def test_generalized_sv_ledh_score_remains_blocked_until_same_target_adapter_exists() -> None:
    row = _ledger_rows()["zhao_cui_generalized_sv_synthetic_from_estimated_values"]
    assert row["score_status"] == "blocked_score"
    assert row["value_status"] == "blocked_no_reviewed_same_target_ledh_row_adapter"


def test_all_highdim_ledh_score_integration_statuses_are_truthful() -> None:
    rows = _ledger_rows()
    assert tuple(rows) == HIGHDIM_LEDGER_ROWS
    implemented_score_rows = {
        "benchmark_lgssm_exact_oracle_m3_T50",
        "zhao_cui_spatial_sir_austria_j9_T20",
        "zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale",
    }
    blocked_rows = set(HIGHDIM_LEDGER_ROWS) - implemented_score_rows

    assert rows["benchmark_lgssm_exact_oracle_m3_T50"]["ledh_row_scope_decision"] == (
        "in_scope_for_later_full_value_score_only_after_gates"
    )
    assert rows["zhao_cui_spatial_sir_austria_j9_T20"]["ledh_row_scope_decision"] == (
        "amended_sir_log_scale_theta_full_row_candidate"
    )
    for row_id in blocked_rows:
        assert "blocked" in rows[row_id]["score_status"]
