from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


JSON_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-results-2026-06-13.json"
)
VALUE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-value-table-2026-06-13.csv"
)
SCORE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-score-table-2026-06-13.csv"
)
CURVATURE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-curvature-table-2026-06-13.csv"
)
STATUS_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-status-table-2026-06-13.csv"
)
UNCERTAINTY_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-stochastic-uncertainty-table-2026-06-13.csv"
)
SUMMARY_MD = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8c-numeric-summary-2026-06-13.md"
)
LGSSM_ROW = "benchmark_lgssm_exact_oracle_m3_T50"
SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"
DPF_SEEDS = [81120, 81121, 81122, 81123, 81124]
RAW_PENDING_TOKENS = (
    "protocol_ready_numeric_evaluator_pending",
    "score_protocol_ready_numeric_evaluator_pending",
    "exact_lgssm_protocol_ready_numeric_pending",
    "exact_lgssm_score_protocol_ready_numeric_pending",
    "exact_lgssm_hessian_protocol_ready_numeric_pending",
    "mixture_enumeration_protocol_ready_numeric_pending",
)


def _artifact() -> dict[str, Any]:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def _cells() -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (cell["algorithm_id"], cell["model_row_id"]): cell
        for cell in _artifact()["cells"]
    }


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_p8c_numeric_artifact_is_partial_not_closeout() -> None:
    artifact = _artifact()

    assert artifact["schema_version"] == "filter_bench.p8c_numeric_results.v1"
    assert artifact["phase"] == "FILTER_BENCH_P8C_EVALUATOR_ADAPTER_AND_DPF_SEED_EXECUTION"
    assert artifact["status"] == (
        "PARTIAL_P8C_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS"
    )
    assert artifact["numeric_benchmark_status"] == (
        "partial_numeric_execution_remaining_adapter_and_callback_gaps"
    )
    assert artifact["skeptical_plan_audit"]["status"] == "PASS_P8C_AUDIT_WITH_PARTIAL_SCOPE"
    assert artifact["roster"]["full_cell_count"] == 42
    assert artifact["roster"]["executed_cell_count"] == 7
    assert artifact["roster"]["pending_or_not_applicable_cell_count"] == 35
    assert "not a filter ranking" in artifact["nonclaims"]


def test_p8c_numeric_has_no_silent_holes() -> None:
    artifact = _artifact()
    algorithms = artifact["roster"]["algorithm_ids"]
    rows = artifact["roster"]["model_row_ids"]
    cells = artifact["cells"]
    by_key = {(cell["algorithm_id"], cell["model_row_id"]): cell for cell in cells}

    assert len(cells) == len(algorithms) * len(rows)
    assert set(by_key) == {(algorithm, row) for algorithm in algorithms for row in rows}
    assert not any(
        cell["numeric_execution_status"] == "protocol_ready_numeric_evaluator_pending"
        for cell in cells
    )
    artifact_text = json.dumps(artifact, sort_keys=True)
    for token in RAW_PENDING_TOKENS:
        assert token not in artifact_text
    for cell in cells:
        label = f"{cell['algorithm_id']}::{cell['model_row_id']}"
        assert cell["numeric_execution_status"], label
        assert cell["reason_codes"], label
        assert cell["nonclaims"], label
        if cell["numeric_execution_status"].startswith("executed"):
            assert cell["value_adapter_status"].startswith("executed"), label
            assert "pending" not in cell["value_adapter_status"], label
            assert "pending" not in cell["score_adapter_status"], label
            assert "pending" not in cell["hessian_adapter_status"], label
        if cell["score"] is not None:
            assert cell["score_adapter_status"].startswith("executed"), label
            assert "pending" not in cell["score_adapter_status"], label
        if cell["hessian_min_eigenvalue_negative_log_likelihood"] is not None:
            assert cell["hessian_adapter_status"].startswith("executed"), label
            assert "pending" not in cell["hessian_adapter_status"], label


def test_p8c_lgssm_differentiated_kalman_value_score_curvature() -> None:
    cells = _cells()
    exact = cells[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]

    assert exact["numeric_execution_status"] == "executed_numeric"
    assert isinstance(exact["log_likelihood"], float)
    assert len(exact["score"]) == 5
    assert exact["score_l2_norm"] > 0.0
    assert exact["score_coordinate_system"] == "physical_theta"
    assert exact["score_derivative_provenance"] == (
        "tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta"
    )
    assert "tf_autodiff" not in exact["score_derivative_provenance"]
    assert "tf_qr" not in exact["score_derivative_provenance"]
    assert exact["curvature_status"] in {
        "observed_negative_log_likelihood_hessian_positive_definite",
        "observed_negative_log_likelihood_hessian_not_positive_definite",
    }
    assert isinstance(exact["hessian_min_eigenvalue_negative_log_likelihood"], float)


def test_p8c_lgssm_sigma_point_cells_use_affine_equivalence_not_native_score() -> None:
    cells = _cells()
    exact = cells[("kalman_exact_or_mixture_enumeration", LGSSM_ROW)]

    for algorithm in ("ukf", "svd_sigma_point", "cut4"):
        cell = cells[(algorithm, LGSSM_ROW)]
        assert cell["numeric_execution_status"] == "executed_numeric_lgssm_score"
        assert abs(cell["reference_log_likelihood"] - exact["log_likelihood"]) < 1e-7
        assert cell["absolute_value_gap_to_kalman"] < 1e-7
        assert cell["reference_score"] == exact["score"]
        assert cell["score"] == exact["score"]
        assert cell["absolute_score_l2_gap_to_kalman"] < 1e-12
        assert cell["score_coordinate_system"] == "physical_theta"
        provenance = cell["score_derivative_provenance"]
        assert provenance == (
            f"{algorithm}_lgssm_affine_equivalence_to_"
            "tf_covariance_differentiated_kalman_reference_cholesky_solve_physical_theta"
        )
        assert "tf_autodiff" not in provenance
        assert "tf_qr" not in provenance
        assert (
            cell["sigma_point_derivative_attempt_status"]
            == "native_sigma_point_score_branch_blocked_differentiated_kalman_affine_equivalence_used"
        )
        assert cell["sigma_point_derivative_blocker"]
        assert "not native sigma-point placement derivative" in cell["nonclaims"][0]


def test_p8c_dpf_lgssm_cells_have_five_seeds_and_mc_se() -> None:
    cells = _cells()

    for algorithm in ("bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"):
        cell = cells[(algorithm, LGSSM_ROW)]
        assert cell["numeric_execution_status"] == "executed_numeric_dpf_5seed_value"
        assert cell["particle_count"] == 8
        assert cell["seed_count"] == 5
        assert cell["seed_list"] == DPF_SEEDS
        assert len(cell["per_seed_results"]) == 5
        assert [entry["seed"] for entry in cell["per_seed_results"]] == DPF_SEEDS
        assert math.isfinite(cell["log_likelihood"])
        assert math.isfinite(cell["average_log_likelihood"])
        assert math.isfinite(cell["sample_standard_deviation"])
        assert math.isfinite(cell["mc_standard_error"])
        assert cell["mc_standard_error"] > 0.0
        assert cell["score_derivative_provenance"] == (
            "not_promoted_dpf_gradient_requires_reviewed_contract"
        )
        assert cell["score"] is None
        assert "not a DPF gradient certification" in cell["nonclaims"]


def test_p8c_non_lgssm_dpf_cells_are_structured_callback_blockers() -> None:
    for cell in _artifact()["cells"]:
        if (
            cell["algorithm_id"] in {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}
            and cell["model_row_id"] != LGSSM_ROW
        ):
            assert cell["numeric_execution_status"] == "blocked_pending_model_specific_dpf_callbacks"
            assert cell["mc_standard_error"] is None
            assert cell["seed_count"] is None
            assert cell["reason_codes"] == [
                "P8C_MODEL_SPECIFIC_DPF_CALLBACKS_REQUIRED_BEFORE_5SEED_AGGREGATION"
            ]


def test_p8c_spatial_sir_scores_remain_not_applicable_no_free_theta() -> None:
    for cell in _artifact()["cells"]:
        if cell["model_row_id"] == SIR_ROW:
            if cell["algorithm_id"] == "kalman_exact_or_mixture_enumeration":
                assert cell["numeric_execution_status"] == "structured_not_applicable"
            else:
                assert cell["score_adapter_status"] == "not_applicable_no_free_theta"
                assert cell["score"] is None
                assert cell["score_l2_norm"] is None


def test_p8c_outputs_have_consistent_table_lengths_and_summary() -> None:
    artifact = _artifact()
    expected = artifact["roster"]["full_cell_count"]

    for path in (VALUE_CSV, SCORE_CSV, CURVATURE_CSV, STATUS_CSV, UNCERTAINTY_CSV):
        assert len(_csv_rows(path)) == expected, path
        text = path.read_text(encoding="utf-8")
        for token in RAW_PENDING_TOKENS:
            assert token not in text, path

    summary = SUMMARY_MD.read_text(encoding="utf-8")
    assert summary.startswith("# P8c Numeric Benchmark Execution Summary")
    assert "PARTIAL_P8C_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS" in summary
    assert "not a filter ranking" in summary
    for token in RAW_PENDING_TOKENS:
        assert token not in summary


def test_p8c_emitter_regenerates_artifacts(tmp_path: Path) -> None:
    output_json = tmp_path / "p8c.json"
    value_csv = tmp_path / "value.csv"
    score_csv = tmp_path / "score.csv"
    curvature_csv = tmp_path / "curvature.csv"
    status_csv = tmp_path / "status.csv"
    uncertainty_csv = tmp_path / "uncertainty.csv"
    markdown = tmp_path / "summary.md"

    subprocess.run(
        [
            sys.executable,
            "scripts/filtering_value_gradient_benchmark_run_p8_numeric.py",
            "--output-json",
            str(output_json),
            "--value-csv",
            str(value_csv),
            "--score-csv",
            str(score_csv),
            "--curvature-csv",
            str(curvature_csv),
            "--status-csv",
            str(status_csv),
            "--uncertainty-csv",
            str(uncertainty_csv),
            "--markdown",
            str(markdown),
        ],
        check=True,
    )

    regenerated = json.loads(output_json.read_text(encoding="utf-8"))
    committed = _artifact()
    assert regenerated["schema_version"] == "filter_bench.p8c_numeric_results.v1"
    assert regenerated["status"] == committed["status"]
    assert regenerated["roster"]["full_cell_count"] == committed["roster"]["full_cell_count"]
    assert regenerated["roster"]["executed_cell_count"] == committed["roster"]["executed_cell_count"]
    assert len(_csv_rows(value_csv)) == regenerated["roster"]["full_cell_count"]
    assert markdown.read_text(encoding="utf-8").startswith("# P8c Numeric Benchmark")
