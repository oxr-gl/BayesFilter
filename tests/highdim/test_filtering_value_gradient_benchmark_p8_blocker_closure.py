from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


STATUS_JSON = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.json"
)
STATUS_CSV = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.csv"
)
STATUS_MD = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-p8-blocker-closure-status-2026-06-11.md"
)


def _artifact() -> dict[str, Any]:
    return json.loads(STATUS_JSON.read_text(encoding="utf-8"))


def test_p8_blocker_closure_manifest_status_and_role_contract() -> None:
    artifact = _artifact()

    assert artifact["schema_version"] == "filter_bench.p8_blocker_closure_status.v1"
    assert artifact["status"] == "PASS_P8_BLOCKER_CLOSURE_STATUS_MANIFEST_WITH_REMAINING_BLOCKERS"
    assert artifact["numeric_benchmark_status"] == "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN"
    assert artifact["ready_for_numeric_benchmark"] is False
    assert artifact["role_contract"]["supervisor_and_executor"] == "Codex in this dialogue"
    assert artifact["role_contract"]["reviewer"] == "Claude Code read-only"
    assert artifact["role_contract"]["detached_codex_agent_allowed"] is False


def test_p8_source_truth_manifest_accepts_available_rows_and_generalized_sv_prior_mean() -> None:
    artifact = _artifact()
    rows = {row["model_row_id"]: row for row in artifact["truth_manifest"]}

    accepted_rows = {
        "benchmark_lgssm_exact_oracle_m3_T50",
        "zhao_cui_sv_actual_nongaussian_T1000",
        "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
        "zhao_cui_spatial_sir_austria_j9_T20",
        "zhao_cui_predator_prey_T20",
    }
    for row_id in accepted_rows:
        assert rows[row_id]["truth_status"] == "accepted_source_truth_available"
        assert rows[row_id]["blocker_token"] is None
        assert rows[row_id]["source_anchors"]

    generalized = rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]
    assert generalized["truth_status"] == (
        "accepted_source_prior_mean_test_point_available"
    )
    assert generalized["blocker_token"] is None
    assert "author defaults are not accepted truth" in generalized["nonclaims"]
    assert "SP500 returns are not benchmark observations" in generalized["nonclaims"]


def test_p8_blocker_closure_refreshes_sir_execution_only_status() -> None:
    artifact = _artifact()
    blocks = artifact["row_level_blocks"]
    sir = artifact["sir_d18_execution_only_status"]

    assert blocks == {}
    assert "benchmark_lgssm_exact_oracle_m3_T50" not in blocks
    assert "zhao_cui_lgssm_kalman_m3_T50" not in blocks
    assert "zhao_cui_generalized_sv_synthetic_from_estimated_values" not in blocks
    assert "zhao_cui_spatial_sir_austria_j9_T20" not in blocks
    sir_truth = {
        row["model_row_id"]: row for row in artifact["truth_manifest"]
    }["zhao_cui_spatial_sir_austria_j9_T20"]
    assert sir_truth["numeric_readiness"] == (
        "source_route_execution_only_ready_numeric_pending"
    )
    assert sir_truth["source_scope_numeric_readiness"] == (
        "blocked_value_route_pending_rank_selection_repair"
    )

    assert artifact["generalized_sv_prior_mean_status"]["status"] == (
        "PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING"
    )
    assert "not a posterior estimate from SP500 returns" in artifact[
        "generalized_sv_prior_mean_status"
    ]["nonclaims"]

    assert sir["status"] == "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED"
    assert sir["missing_phases"] == []
    assert all(row["passed"] for row in sir["artifact_statuses"].values())
    assert "not d18 filtering accuracy evidence" in sir["nonclaims"]
    assert "not same-route rank convergence evidence" in sir["nonclaims"]


def test_p8_blocker_closure_guardrails_forbid_proxy_promotion() -> None:
    guardrails = _artifact()["promotion_guardrails"]

    assert guardrails == {
        "p44_rows_promoted": False,
        "old_ledh_pfpf_ot_current_evidence_allowed": False,
        "sir_old_local_operator_route_allowed": False,
        "generalized_sv_author_defaults_as_truth_allowed": False,
        "sp500_returns_as_benchmark_data_allowed": False,
        "dpf_ranking_before_mc_se_allowed": False,
        "uncertified_score_or_hessian_promotion_allowed": False,
        "protocol_gate_counts_as_numeric_benchmark_allowed": False,
    }


def test_p8_blocker_closure_summary_artifacts_are_status_only() -> None:
    artifact = _artifact()
    with STATUS_CSV.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    text = STATUS_MD.read_text(encoding="utf-8")

    assert len(rows) == len(artifact["blockers"])
    assert {row["blocker_id"] for row in rows} == {
        "P8-B1",
        "P8-B2",
        "P8-B3",
        "P8-B4",
        "P8-B5",
        "P8-B6",
        "P8-B7",
        "P8-B8",
    }
    rows_by_id = {row["blocker_id"]: row for row in rows}
    assert rows_by_id["P8-B3"]["status"] == "protocol_ready_numeric_pending"
    assert rows_by_id["P8-B4"]["status"] == "protocol_ready_numeric_pending"
    assert rows_by_id["P8-B5"]["status"] == "adapter_status_matrix_ready_numeric_pending"
    assert rows_by_id["P8-B6"]["status"] == "pass_execution_only_ready_numeric_pending"
    assert text.startswith("# P8 Blocker Closure Status")
    assert "BLOCK_P8_B2_LGSSM_AUTHOR_C_MATRIX_PENDING" not in text
    assert "BLOCK_P8_B6_SPATIAL_SIR_D18_SOURCE_ROUTE" not in text
    assert "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED" in text
    assert "BLOCK_P8_NUMERIC_BENCHMARK_NOT_YET_RUN" in text


def test_p8_blocker_closure_nonclaims_keep_numeric_result_blocked() -> None:
    artifact = _artifact()

    assert "not a numeric benchmark result" in artifact["nonclaims"]
    assert "not a filter ranking" in artifact["nonclaims"]
    assert "not generalized-SV evaluator correctness or performance evidence" in artifact["nonclaims"]
    assert "not SIR d=18 filtering accuracy or rank-convergence evidence" in artifact["nonclaims"]
    assert artifact["decision_table"][1]["decision"] == "keep_numeric_p8_blocked"


def test_p8_blocker_closure_emitter_regenerates_status_artifacts(tmp_path: Path) -> None:
    output_json = tmp_path / "status.json"
    output_csv = tmp_path / "status.csv"
    output_md = tmp_path / "status.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/filtering_value_gradient_benchmark_emit_p8_blocker_closure.py",
            "--output-json",
            str(output_json),
            "--summary-csv",
            str(output_csv),
            "--summary-markdown",
            str(output_md),
        ],
        check=True,
    )

    regenerated = json.loads(output_json.read_text(encoding="utf-8"))
    committed = _artifact()
    with output_csv.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    md = output_md.read_text(encoding="utf-8")

    assert regenerated["status"] == committed["status"]
    assert regenerated["numeric_benchmark_status"] == committed["numeric_benchmark_status"]
    assert regenerated["promotion_guardrails"] == committed["promotion_guardrails"]
    assert regenerated["row_level_blocks"] == committed["row_level_blocks"]
    assert regenerated["sir_d18_execution_only_status"] == committed[
        "sir_d18_execution_only_status"
    ]
    assert regenerated["truth_status_counts"] == {
        "accepted_source_truth_available": 5,
        "accepted_source_prior_mean_test_point_available": 1,
    }
    assert len(csv_rows) == len(regenerated["blockers"])
    assert md.startswith("# P8 Blocker Closure Status")
    assert "PASS_P8_B1_SOURCE_TRUTH_MANIFEST_READY" in md
    assert "PASS_P8_B2_SYNTHETIC_DATASET_MANIFEST_READY" in md
    assert "PASS_P8_B6_SPATIAL_SIR_D18_EXECUTION_ONLY_RECOGNIZED" in md
