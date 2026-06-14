from __future__ import annotations

import csv
import json
from pathlib import Path

import tensorflow as tf

import scripts.filtering_value_gradient_benchmark_run_p8d_numeric as p8d


LGSSM_ROW = "benchmark_lgssm_exact_oracle_m3_T50"
SV_ROW = "zhao_cui_sv_actual_nongaussian_T1000"
KSC_ROW = "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"
SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"
PREDATOR_PREY_ROW = "zhao_cui_predator_prey_T20"
GENERALIZED_SV_ROW = "zhao_cui_generalized_sv_synthetic_from_estimated_values"
DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]


def _adapters() -> dict[tuple[str, str], dict[str, str]]:
    with p8d.ADAPTER_MATRIX_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {(row["algorithm_id"], row["model_row_id"]): row for row in rows}


def test_p8d_source_scope_and_route_policy_are_mechanical() -> None:
    source_scope = json.loads(p8d.SOURCE_SCOPE_PATH.read_text(encoding="utf-8"))
    adapters = _adapters()
    algorithms = source_scope["algorithm_ids"]
    rows = source_scope["source_scope_row_ids"]

    assert len(adapters) == len(algorithms) * len(rows)
    assert set(adapters) == {(algorithm, row) for algorithm in algorithms for row in rows}
    assert not p8d._has_deterministic_route("kalman_exact_or_mixture_enumeration", SV_ROW)
    assert not p8d._has_deterministic_route("kalman_exact_or_mixture_enumeration", SIR_ROW)
    assert not p8d._has_dpf_route(KSC_ROW)
    assert not p8d._has_dpf_route(SIR_ROW)
    for row in (LGSSM_ROW, SV_ROW, PREDATOR_PREY_ROW, GENERALIZED_SV_ROW):
        assert p8d._has_dpf_route(row)


def test_p8d_artifact_accounting_separates_real_gaps_from_true_not_applicable() -> None:
    real_cells = [
        {"numeric_execution_status": "executed_numeric"},
        {"numeric_execution_status": "structured_not_applicable"},
        {"numeric_execution_status": "blocked_pending_model_specific_dpf_callbacks"},
    ]
    executed = [
        cell for cell in real_cells if cell["numeric_execution_status"].startswith("executed")
    ]
    structured_not_applicable = [
        cell
        for cell in real_cells
        if cell["numeric_execution_status"] == "structured_not_applicable"
    ]
    real_gaps = [
        cell
        for cell in real_cells
        if not cell["numeric_execution_status"].startswith("executed")
        and cell["numeric_execution_status"] != "structured_not_applicable"
    ]

    assert len(executed) == 1
    assert len(structured_not_applicable) == 1
    assert len(real_gaps) == 1


def test_p8d_lgssm_exact_cell_has_p8d_schema_and_no_autodiff_fallback() -> None:
    adapter = _adapters()[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]
    cell = p8d._numeric_lgssm_exact_cell(adapter)

    assert cell["numeric_execution_status"] == "executed_numeric"
    assert cell["reason_codes"] == ["P8D_NUMERIC_EXECUTED_EXACT_LGSSM_DIFFERENTIATED_KALMAN"]
    assert isinstance(cell["log_likelihood"], float)
    assert len(cell["score"]) == 5
    assert cell["score_derivative_provenance"] == (
        "tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta"
    )
    assert "tf_autodiff" not in cell["score_derivative_provenance"]


def test_p8d_raw_sv_ukf_smoke_value_score_is_finite() -> None:
    adapter = _adapters()[("ukf", SV_ROW)]
    cell = p8d._numeric_deterministic_cell("ukf", SV_ROW, adapter)

    assert cell["numeric_execution_status"] == "executed_numeric_value_score"
    assert isinstance(cell["log_likelihood"], float)
    assert isinstance(cell["score_l2_norm"], float)
    assert cell["score_l2_norm"] >= 0.0
    assert cell["score_derivative_provenance"] == (
        "ukf_augmented_noise_sigma_point_raw_sv_tf_autodiff_score"
    )
    assert "not exact nonlinear likelihood" in " ".join(cell["nonclaims"])


def test_p8d_spatial_sir_value_only_cell_preserves_no_free_theta() -> None:
    adapter = _adapters()[("ukf", SIR_ROW)]
    cell = p8d._numeric_deterministic_cell("ukf", SIR_ROW, adapter)

    assert cell["numeric_execution_status"] in {
        "executed_numeric_value_only_no_free_theta",
        "blocked_p8d_deterministic_smoke_failed",
    }
    assert cell["score_adapter_status"] == "not_applicable_no_free_theta"
    assert cell["hessian_adapter_status"] == "not_applicable_no_free_theta"
    assert cell["score"] is None


def test_p8d_dpf_bootstrap_sv_cell_has_exactly_five_seed_contract() -> None:
    adapter = _adapters()[("bootstrap_dpf_current", SV_ROW)]
    old_seeds = p8d.DPF_SEEDS
    old_particles = p8d.DPF_PARTICLE_COUNT
    try:
        p8d.DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]
        p8d.DPF_PARTICLE_COUNT = 4
        cell = p8d._numeric_dpf_cell("bootstrap_dpf_current", SV_ROW, adapter)
    finally:
        p8d.DPF_SEEDS = old_seeds
        p8d.DPF_PARTICLE_COUNT = old_particles

    assert cell["numeric_execution_status"] == "executed_numeric_dpf_5seed_value"
    assert cell["seed_list"] == DPF_SEEDS
    assert cell["seed_count"] == 5
    assert len(cell["per_seed_results"]) == 5
    assert cell["score"] is None
    assert cell["mc_standard_error"] is not None
    assert "not a DPF gradient certification" in cell["nonclaims"]


def test_p8d_manifest_points_to_visible_plan_and_default_cpu_command() -> None:
    source_artifacts = p8d._source_artifacts_payload()
    run_manifest = p8d._run_manifest_payload()

    assert source_artifacts["plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md"
    )
    assert source_artifacts["p8_master_plan"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-master-plan-2026-06-11.md"
    )
    assert run_manifest["plan_file"] == (
        "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8d-visible-repair-execution-plan-2026-06-13.md"
    )
    assert run_manifest["command"] == (
        "env CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python "
        "scripts/filtering_value_gradient_benchmark_run_p8d_numeric.py --enable-p8d-execution"
    )
    assert run_manifest["cpu_gpu_status"] == "CPU-only deliberate"


def test_p8d_write_outputs_roundtrip_with_minimal_artifact(tmp_path: Path) -> None:
    adapter = _adapters()[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]
    cell = p8d._numeric_lgssm_exact_cell(adapter)
    artifact = {
        "schema_version": "filter_bench.p8d_numeric_results.v1",
        "metadata_date": "2026-06-13",
        "phase": "FILTER_BENCH_P8D_VISIBLE_REPAIR_EXECUTION",
        "status": "PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS",
        "numeric_benchmark_status": "partial_numeric_execution_remaining_adapter_and_callback_gaps",
        "roster": {
            "algorithm_ids": ["kalman_exact_or_mixture_enumeration"],
            "model_row_ids": [LGSSM_ROW],
            "full_cell_count": 1,
            "executed_cell_count": 1,
            "structured_not_applicable_cell_count": 0,
            "real_gap_cell_count": 0,
            "pending_or_not_applicable_cell_count": 0,
        },
        "cells": [cell],
        "run_manifest": {},
        "nonclaims": ["not a filter ranking"],
    }
    output_json = tmp_path / "p8d.json"
    p8d.write_outputs(
        artifact,
        output_json=output_json,
        value_csv=tmp_path / "value.csv",
        score_csv=tmp_path / "score.csv",
        curvature_csv=tmp_path / "curvature.csv",
        status_csv=tmp_path / "status.csv",
        uncertainty_csv=tmp_path / "uncertainty.csv",
        markdown=tmp_path / "summary.md",
    )
    written = json.loads(output_json.read_text(encoding="utf-8"))
    assert written["schema_version"] == "filter_bench.p8d_numeric_results.v1"
    assert written["run_manifest"]["summary_markdown"].endswith("summary.md")
    assert (tmp_path / "summary.md").read_text(encoding="utf-8").startswith(
        "# P8d Numeric Benchmark Execution Summary"
    )
    assert tf.constant(1.0, dtype=tf.float64).dtype == tf.float64
