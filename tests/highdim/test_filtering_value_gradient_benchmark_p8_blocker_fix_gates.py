from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


GATES_JSON = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.json"
)
ADAPTER_CSV = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-adapter-status-matrix-2026-06-11.csv"
)
SUMMARY_MD = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-fix-gates-2026-06-11.md"
)


def _artifact() -> dict[str, Any]:
    return json.loads(GATES_JSON.read_text(encoding="utf-8"))


def test_p8_blocker_fix_gates_status_and_nonclaims() -> None:
    artifact = _artifact()

    assert artifact["schema_version"] == "filter_bench.p8_blocker_fix_gates.v1"
    assert artifact["status"] == "PASS_P8_BLOCKER_FIX_GATES_SOURCE_ROWS_READY_NUMERIC_PENDING"
    assert artifact["numeric_benchmark_status"] == "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN"
    assert artifact["ready_for_numeric_benchmark"] is False
    assert "not a numeric benchmark result" in artifact["nonclaims"]
    assert "not a filter ranking" in artifact["nonclaims"]
    assert artifact["role_contract"]["supervisor_and_executor"] == "Codex in this dialogue"
    assert artifact["role_contract"]["detached_codex_agent_allowed"] is False


def test_p8_blocker_fix_gates_close_B3_B4_B5_as_protocol_only() -> None:
    gates = _artifact()["phase_gate_statuses"]

    assert gates["P8-B3"]["token"] == "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING"
    assert gates["P8-B3"]["numeric_horizon_calibration_run"] is False
    assert gates["P8-B4"]["token"] == "PASS_P8_B4_STOCHASTIC_PROTOCOL_READY_NUMERIC_PENDING"
    assert gates["P8-B4"]["numeric_seed_ladder_run"] is False
    assert gates["P8-B5"]["token"] == "PASS_P8_B5_ADAPTER_STATUS_MATRIX_READY_NUMERIC_PENDING"
    assert gates["P8-B5"]["numeric_evaluator_run"] is False
    assert gates["hard_source_blocks"]["token"] == "PASS_P8_SOURCE_BLOCKS_REFRESHED_NO_ROW_LEVEL_HARD_BLOCKS"


def test_p8_blocker_fix_horizon_protocol_has_source_rows_and_no_numeric_claim() -> None:
    artifact = _artifact()
    rows = {row["model_row_id"]: row for row in artifact["horizon_protocol"]["rows"]}

    assert set(rows) == {
        "benchmark_lgssm_exact_oracle_m3_T50",
        "zhao_cui_sv_actual_nongaussian_T1000",
        "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
        "zhao_cui_spatial_sir_austria_j9_T20",
        "zhao_cui_predator_prey_T20",
        "zhao_cui_generalized_sv_synthetic_from_estimated_values",
    }
    assert rows["zhao_cui_sv_actual_nongaussian_T1000"]["source_horizon"] == 1000
    assert rows["benchmark_lgssm_exact_oracle_m3_T50"]["source_horizon"] == 50
    assert rows["benchmark_lgssm_exact_oracle_m3_T50"]["dataset_status"] == "generated"
    assert rows["benchmark_lgssm_exact_oracle_m3_T50"]["blocker_token"] is None
    assert rows["benchmark_lgssm_exact_oracle_m3_T50"]["horizon_gate_status"] == (
        "exact_oracle_horizon_locked_numeric_calibration_pending"
    )
    assert rows["zhao_cui_predator_prey_T20"]["source_horizon"] == 20
    assert rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]["source_horizon"] == 1008
    assert rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]["dataset_status"] == "generated"
    assert rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]["blocker_token"] is None
    assert rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]["horizon_gate_status"] == (
        "source_prior_mean_horizon_locked_numeric_calibration_pending"
    )
    assert rows["zhao_cui_spatial_sir_austria_j9_T20"]["horizon_gate_status"] == (
        "source_horizon_locked_source_route_execution_only_ready_numeric_pending"
    )
    assert rows["zhao_cui_spatial_sir_austria_j9_T20"]["blocker_token"] is None
    for row in rows.values():
        assert row["numeric_horizon_calibration_run"] is False
        assert row["interpretation"] == "protocol_gate_only_not_numeric_horizon_calibration"


def test_p8_blocker_fix_stochastic_protocol_disables_ranking_until_mc_se() -> None:
    rows = _artifact()["stochastic_seed_protocol"]["rows"]

    assert rows
    assert {row["algorithm_id"] for row in rows} == {
        "bootstrap_dpf_current",
        "ledh_pfpf_alg1_ukf_current",
    }
    for row in rows:
        assert row["seed_ladder"] == [4, 8, 16, 32]
        assert row["ranking_enabled"] is False
        assert row["numeric_seed_ladder_run"] is False
        assert "particle_mc_standard_error" in row["required_diagnostics"]
        assert "effective_sample_size" in row["required_diagnostics"]


def test_p8_blocker_fix_adapter_matrix_has_no_silent_holes() -> None:
    artifact = _artifact()
    matrix = artifact["adapter_status_matrix"]
    rows = matrix["rows"]

    assert matrix["expected_cell_count"] == 42
    assert matrix["actual_cell_count"] == 42
    assert len(rows) == 42
    labels = {(row["algorithm_id"], row["model_row_id"]) for row in rows}
    assert len(labels) == 42

    by_label = {(row["algorithm_id"], row["model_row_id"]): row for row in rows}
    kalman_lgssm = by_label[
        ("kalman_exact_or_mixture_enumeration", "benchmark_lgssm_exact_oracle_m3_T50")
    ]
    assert kalman_lgssm["target_contract_status"] == "exact_lgssm_only"
    assert kalman_lgssm["value_adapter_status"] == (
        "exact_lgssm_protocol_ready_numeric_pending"
    )
    assert kalman_lgssm["not_available_reason"] == ""

    kalman_sv = by_label[
        ("kalman_exact_or_mixture_enumeration", "zhao_cui_sv_actual_nongaussian_T1000")
    ]
    assert kalman_sv["target_contract_status"] == "structured_not_applicable"
    assert "KALMAN_REMOVED_OUTSIDE_LGSSM" in kalman_sv["not_available_reason"]

    dpf_predator = by_label[("ledh_pfpf_alg1_ukf_current", "zhao_cui_predator_prey_T20")]
    assert dpf_predator["value_adapter_status"] == "protocol_ready_numeric_evaluator_pending"
    assert dpf_predator["score_adapter_status"] == (
        "not_certified_for_main_score_without_mc_and_fixed_branch_review"
    )

    sir_zc = by_label[
        ("zhao_cui_scalar_or_multistate", "zhao_cui_spatial_sir_austria_j9_T20")
    ]
    assert sir_zc["target_contract_status"] == "source_route_target_compatible_execution_only_ready"
    assert sir_zc["value_adapter_status"] == (
        "source_route_execution_only_ready_numeric_evaluator_pending"
    )
    assert sir_zc["not_available_reason"] == ""

    dpf_generalized_sv = by_label[
        ("bootstrap_dpf_current", "zhao_cui_generalized_sv_synthetic_from_estimated_values")
    ]
    assert dpf_generalized_sv["dataset_status"] == "generated"
    assert dpf_generalized_sv["value_adapter_status"] == "protocol_ready_numeric_evaluator_pending"
    assert dpf_generalized_sv["not_available_reason"] == ""


def test_p8_blocker_fix_refreshes_hard_source_blocks_and_guardrails() -> None:
    artifact = _artifact()
    blocks = artifact["row_level_hard_blocks"]
    guardrails = artifact["promotion_guardrails"]
    sir = artifact["sir_d18_execution_only_status"]

    assert blocks == {}
    assert "benchmark_lgssm_exact_oracle_m3_T50" not in blocks
    assert "zhao_cui_lgssm_kalman_m3_T50" not in blocks
    assert "zhao_cui_generalized_sv_synthetic_from_estimated_values" not in blocks
    assert "zhao_cui_spatial_sir_austria_j9_T20" not in blocks
    assert sir["status"] == "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED"
    assert sir["missing_phases"] == []
    assert all(row["passed"] for row in sir["artifact_statuses"].values())
    assert "not d18 filtering accuracy evidence" in sir["nonclaims"]
    assert "not same-route rank convergence evidence" in sir["nonclaims"]
    assert artifact["generalized_sv_prior_mean_status"]["status"] == (
        "PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING"
    )
    assert "author_code_defaults_not_estimates" in artifact[
        "generalized_sv_prior_mean_status"
    ]["forbidden_substitutes"]
    assert guardrails == {
        "p44_rows_promoted": False,
        "author_defaults_as_generalized_sv_truth_allowed": False,
        "sp500_returns_as_benchmark_observations_allowed": False,
        "zhao_cui_lgssm_matlab_C_claim_allowed": False,
        "old_ledh_pfpf_ot_current_evidence_allowed": False,
        "old_sir_local_operator_route_allowed": False,
        "dpf_ranking_before_mc_se_allowed": False,
        "protocol_gate_counts_as_numeric_benchmark_allowed": False,
    }


def test_p8_blocker_fix_adapter_csv_and_summary_markdown_are_written() -> None:
    artifact = _artifact()
    with ADAPTER_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    text = SUMMARY_MD.read_text(encoding="utf-8")

    assert len(rows) == artifact["adapter_status_matrix"]["expected_cell_count"]
    assert set(rows[0]) == {
        "algorithm_id",
        "model_row_id",
        "dataset_status",
        "target_contract_status",
        "value_adapter_status",
        "score_adapter_status",
        "hessian_adapter_status",
        "numeric_execution_status",
        "not_available_reason",
    }
    assert text.startswith("# P8 Blocker Fix Gates")
    assert "PASS_P8_B3_HORIZON_PROTOCOL_READY_NUMERIC_PENDING" in text
    assert "PASS_P8_SOURCE_BLOCKS_REFRESHED_NO_ROW_LEVEL_HARD_BLOCKS" in text
    assert "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED" in text
    assert "BLOCK_GENERALIZED_SV_NUMERIC_RUN_ESTIMATED_VALUES_PENDING" not in text
    assert "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE" not in text


def test_p8_blocker_fix_emitter_regenerates_artifacts(tmp_path: Path) -> None:
    output_json = tmp_path / "gates.json"
    adapter_csv = tmp_path / "adapter.csv"
    summary_md = tmp_path / "summary.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/filtering_value_gradient_benchmark_emit_p8_blocker_fix_gates.py",
            "--output-json",
            str(output_json),
            "--adapter-csv",
            str(adapter_csv),
            "--summary-markdown",
            str(summary_md),
        ],
        check=True,
    )

    regenerated = json.loads(output_json.read_text(encoding="utf-8"))
    committed = _artifact()
    with adapter_csv.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))

    assert regenerated["status"] == committed["status"]
    assert regenerated["numeric_benchmark_status"] == committed["numeric_benchmark_status"]
    assert regenerated["phase_gate_statuses"] == committed["phase_gate_statuses"]
    assert regenerated["row_level_hard_blocks"] == committed["row_level_hard_blocks"]
    assert regenerated["promotion_guardrails"] == committed["promotion_guardrails"]
    assert len(csv_rows) == committed["adapter_status_matrix"]["expected_cell_count"]
    assert summary_md.read_text(encoding="utf-8").startswith("# P8 Blocker Fix Gates")
