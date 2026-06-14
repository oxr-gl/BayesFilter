from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


JSON_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-results-2026-06-12.json"
)
VALUE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-value-table-2026-06-12.csv"
)
SCORE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-score-table-2026-06-12.csv"
)
CURVATURE_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-curvature-table-2026-06-12.csv"
)
STATUS_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-status-table-2026-06-12.csv"
)
UNCERTAINTY_CSV = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-stochastic-uncertainty-table-2026-06-12.csv"
)
SUMMARY_MD = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8b-numeric-summary-2026-06-12.md"
)


def _artifact() -> dict[str, Any]:
    return json.loads(JSON_PATH.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_p8b_numeric_artifact_is_partial_not_closeout() -> None:
    artifact = _artifact()

    assert artifact["schema_version"] == "filter_bench.p8b_numeric_results.v1"
    assert artifact["phase"] == "FILTER_BENCH_P8B_NUMERIC_EXECUTION_AND_TABLES"
    assert artifact["status"] == (
        "PARTIAL_P8_B7_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS"
    )
    assert artifact["numeric_benchmark_status"] == (
        "partial_numeric_execution_remaining_adapter_and_seed_ladder_gaps"
    )
    assert artifact["roster"]["full_cell_count"] == 42
    assert artifact["roster"]["executed_cell_count"] >= 5
    assert artifact["roster"]["pending_or_not_applicable_cell_count"] > 0
    assert "partial numeric artifact, not full Phase 8 completion" in artifact["nonclaims"]


def test_p8b_numeric_has_no_silent_holes() -> None:
    artifact = _artifact()
    algorithms = artifact["roster"]["algorithm_ids"]
    rows = artifact["roster"]["model_row_ids"]
    cells = artifact["cells"]
    by_key = {(cell["algorithm_id"], cell["model_row_id"]): cell for cell in cells}

    assert len(cells) == len(algorithms) * len(rows)
    assert set(by_key) == {(algorithm, row) for algorithm in algorithms for row in rows}
    for cell in cells:
        label = f"{cell['algorithm_id']}::{cell['model_row_id']}"
        assert cell["numeric_execution_status"], label
        assert cell["reason_codes"], label
        assert cell["nonclaims"], label


def test_p8b_lgssm_exact_kalman_has_value_score_and_curvature() -> None:
    cell = {
        (row["algorithm_id"], row["model_row_id"]): row
        for row in _artifact()["cells"]
    }[("kalman_exact_or_mixture_enumeration", "benchmark_lgssm_exact_oracle_m3_T50")]

    assert cell["numeric_execution_status"] == "executed_numeric"
    assert isinstance(cell["log_likelihood"], float)
    assert isinstance(cell["average_log_likelihood"], float)
    assert len(cell["score"]) == 5
    assert cell["score_l2_norm"] > 0.0
    assert cell["score_coordinate_system"] == "physical_theta"
    assert cell["score_derivative_provenance"] == "tf_autodiff_kalman_physical_theta"
    assert cell["curvature_status"] in {
        "observed_negative_log_likelihood_hessian_positive_definite",
        "observed_negative_log_likelihood_hessian_not_positive_definite",
    }
    assert isinstance(cell["hessian_min_eigenvalue_negative_log_likelihood"], float)


def test_p8b_lgssm_sigma_point_cells_have_value_and_score_against_kalman() -> None:
    cells = {
        (row["algorithm_id"], row["model_row_id"]): row
        for row in _artifact()["cells"]
    }
    exact = cells[("kalman_exact_or_mixture_enumeration", "benchmark_lgssm_exact_oracle_m3_T50")]

    for algorithm in ("ukf", "svd_sigma_point", "cut4"):
        cell = cells[(algorithm, "benchmark_lgssm_exact_oracle_m3_T50")]
        assert cell["numeric_execution_status"] == "executed_numeric_lgssm_score"
        assert isinstance(cell["log_likelihood"], float)
        assert abs(cell["reference_log_likelihood"] - exact["log_likelihood"]) < 1e-7
        assert cell["absolute_value_gap_to_kalman"] < 1e-7
        assert len(cell["score"]) == 5
        assert cell["score_l2_norm"] > 0.0
        assert cell["score_coordinate_system"] == "physical_theta"
        assert cell["absolute_score_l2_gap_to_kalman"] < 1e-9
        assert cell["score"] == cell["reference_score"]
        assert cell["sigma_point_derivative_attempt_status"] in {
            "analytic_score_executed",
            "analytic_score_branch_blocked_lgssm_affine_equivalence_fallback",
        }
        provenance = cell["score_derivative_provenance"]
        assert (
            "analytic_first_order" in provenance
            or provenance.endswith(
                "lgssm_affine_equivalence_to_tf_autodiff_kalman_physical_theta_after_sigma_value_tieout"
            )
        )
        if cell["sigma_point_derivative_attempt_status"].startswith("analytic_score_branch_blocked"):
            assert cell["sigma_point_derivative_blocker"]


def test_p8b_ksc_surrogate_cell_is_labeled_not_native_sv_truth() -> None:
    cell = {
        (row["algorithm_id"], row["model_row_id"]): row
        for row in _artifact()["cells"]
    }[
        (
            "kalman_exact_or_mixture_enumeration",
            "zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000",
        )
    ]

    assert cell["numeric_execution_status"] == "executed_value_only_declared_surrogate"
    assert isinstance(cell["log_likelihood"], float)
    assert cell["score"] is None
    assert cell["score_coordinate_system"] == "synthetic_unconstrained_theta"
    assert cell["score_derivative_provenance"] == "not_run_fast_score_adapter_pending"
    assert "declared KSC Gaussian-mixture surrogate, not native SV likelihood" in cell["nonclaims"]


def test_p8b_dpf_cells_require_seed_ladders_before_ranking() -> None:
    for cell in _artifact()["cells"]:
        if cell["algorithm_id"] in {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}:
            assert cell["numeric_execution_status"] == "blocked_pending_dpf_seed_ladder_and_mc_se"
            assert cell["mc_standard_error"] is None
            assert cell["seed_count"] is None
            assert "DPF_SEED_LADDER_AND_MC_SE_REQUIRED_BEFORE_RANKING" in cell["reason_codes"]


def test_p8b_outputs_have_consistent_table_lengths() -> None:
    artifact = _artifact()
    expected = artifact["roster"]["full_cell_count"]

    for path in (VALUE_CSV, SCORE_CSV, CURVATURE_CSV, STATUS_CSV, UNCERTAINTY_CSV):
        rows = _csv_rows(path)
        assert len(rows) == expected, path

    summary = SUMMARY_MD.read_text(encoding="utf-8")
    assert "PARTIAL_P8_B7_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS" in summary
    assert "not full Phase 8 completion" in summary


def test_p8b_emitter_regenerates_artifacts(tmp_path: Path) -> None:
    output_json = tmp_path / "p8b.json"
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
    assert regenerated["status"] == committed["status"]
    assert regenerated["roster"]["full_cell_count"] == committed["roster"]["full_cell_count"]
    assert regenerated["roster"]["executed_cell_count"] == committed["roster"]["executed_cell_count"]
    assert len(_csv_rows(value_csv)) == regenerated["roster"]["full_cell_count"]
    assert markdown.read_text(encoding="utf-8").startswith("# P8b Numeric Benchmark")
