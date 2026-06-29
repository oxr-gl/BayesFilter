from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


P8_PATH = Path("docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-matrices-2026-06-10.json")
PREFLIGHT_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json"
)
VALUE_CSV_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.csv"
)
GRADIENT_CSV_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.csv"
)
VALUE_MD_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-value-error-matrix-2026-06-10.md"
)
GRADIENT_MD_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-gradient-error-matrix-2026-06-10.md"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.reader(handle))


def test_filter_bench_p8_runner_matrices_preserve_frozen_roster_and_block_honestly() -> None:
    p8 = _load(P8_PATH)
    preflight = _load(PREFLIGHT_PATH)

    assert p8["schema_version"] == "filter_bench.runner_matrices.v1"
    assert p8["phase"] == "FILTER_BENCH_P8"
    assert p8["status"] == "BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES"
    assert p8["blocker"]["blocked_token"] == "BLOCK_FILTER_BENCH_P8_RUNNER_MATRICES"
    assert "No reviewed full numeric benchmark runner exists" in p8["blocker"]["reason"]
    assert p8["frozen_roster"] == preflight["frozen_roster"]
    assert p8["benchmark_scope"]["matrix_emission_complete"] is True
    assert p8["benchmark_scope"]["numeric_benchmark_execution_complete"] is False
    assert p8["benchmark_scope"]["performance_answer_complete"] is False
    assert p8["benchmark_scope"]["p7_preflight_used_as_performance_evidence"] is False
    assert p8["benchmark_scope"]["smoke_fixtures_used_as_performance_evidence"] is False
    assert p8["benchmark_scope"]["old_ledh_pfpf_ot_current_evidence"] is False


def test_filter_bench_p8_runner_matrices_have_no_silent_holes() -> None:
    p8 = _load(P8_PATH)
    algorithms = p8["frozen_roster"]["algorithm_ids"]
    rows = p8["frozen_roster"]["model_columns"]

    for matrix_name in (
        "value_error_matrix",
        "gradient_error_matrix",
        "status_matrix",
        "diagnostics_matrix",
    ):
        matrix = p8[matrix_name]
        assert set(matrix) == set(algorithms), matrix_name
        for algorithm_id in algorithms:
            assert set(matrix[algorithm_id]) == set(rows), f"{matrix_name}::{algorithm_id}"

    for algorithm_id in algorithms:
        for row_id in rows:
            label = f"{algorithm_id}::{row_id}"
            value_cell = p8["value_error_matrix"][algorithm_id][row_id]
            gradient_cell = p8["gradient_error_matrix"][algorithm_id][row_id]
            status_cell = p8["status_matrix"][algorithm_id][row_id]
            diagnostics_cell = p8["diagnostics_matrix"][algorithm_id][row_id]

            assert value_cell["reason_codes"], label
            assert gradient_cell["reason_codes"], label
            assert value_cell["comparator_labels"], label
            assert gradient_cell["comparator_labels"], label
            assert status_cell["comparator_labels"], label
            assert diagnostics_cell["performance_interpretation"] == "not_performance_evidence"
            assert value_cell["performance_interpretation"] == "not_performance_evidence"
            assert gradient_cell["performance_interpretation"] == "not_performance_evidence"


def test_filter_bench_p8_runner_matrices_do_not_promote_proxy_values_to_errors() -> None:
    p8 = _load(P8_PATH)

    for algorithm_id, row_cells in p8["value_error_matrix"].items():
        for row_id, cell in row_cells.items():
            label = f"value::{algorithm_id}::{row_id}"
            assert cell["value_error_abs"] is None, label
            assert cell["value_error_rel"] is None, label
            if cell["cell_status"] == "SMOKE_FIXTURE_NOT_BENCHMARK_RESULT":
                assert "SMOKE_FIXTURE_NOT_BENCHMARK_RESULT" in cell["reason_codes"], label
                assert "P8_NUMERIC_BENCHMARK_NOT_EXECUTED" in cell["reason_codes"], label

    for algorithm_id, row_cells in p8["gradient_error_matrix"].items():
        for row_id, cell in row_cells.items():
            label = f"gradient::{algorithm_id}::{row_id}"
            assert cell["gradient_error_abs"] is None, label
            assert cell["gradient_error_rel"] is None, label
            if not cell["p8_gradient_error_eligible"]:
                assert "GRADIENT_STATUS_ONLY_BY_P6_SEMANTICS" in cell["reason_codes"], label
            if algorithm_id in {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}:
                assert cell["p8_gradient_error_eligible"] is False, label


def test_filter_bench_p8_runner_matrices_include_comparator_labels_and_dpf_mc_diagnostics() -> None:
    p8 = _load(P8_PATH)
    labels = set(p8["comparator_label_vocabulary"])

    assert {
        "exact_LGSSM",
        "exact_or_dense_numerical",
        "transformed_actual_nongaussian",
        "gaussian_mixture_surrogate",
        "approximate_nongaussian",
        "no_reference",
        "invalid_gradient",
        "historical_only",
    }.issubset(labels)

    seen_cell_labels = set()
    for matrix in (p8["value_error_matrix"], p8["gradient_error_matrix"]):
        for row_cells in matrix.values():
            for cell in row_cells.values():
                seen_cell_labels.update(cell["comparator_labels"])
    assert {"exact_LGSSM", "exact_or_dense_numerical", "gaussian_mixture_surrogate"}.issubset(
        seen_cell_labels
    )
    assert "invalid_gradient" in seen_cell_labels

    bootstrap_lgssm = p8["diagnostics_matrix"]["bootstrap_dpf_current"][
        "lgssm_exact_kalman_dim_1_2_3"
    ]
    assert bootstrap_lgssm["mc_standard_error"] is not None
    assert bootstrap_lgssm["particle_count"] is not None
    assert bootstrap_lgssm["effective_sample_size_min"] is not None
    assert bootstrap_lgssm["resampling_policy"]

    historical = p8["historical_only_records"]
    assert historical == [
        {
            "algorithm_id": "ledh_pfpf_ot_historical",
            "comparator_labels": ["historical_only"],
            "current_evidence": False,
            "reason_codes": ["HISTORICAL_LEDHPFPF_OT_SUPERSEDED"],
        }
    ]


def test_filter_bench_p8_runner_matrices_emit_readable_csv_and_markdown_tables() -> None:
    p8 = _load(P8_PATH)
    rows = p8["frozen_roster"]["model_columns"]
    algorithms = p8["frozen_roster"]["algorithm_ids"]

    for path in (VALUE_CSV_PATH, GRADIENT_CSV_PATH):
        table = _csv_rows(path)
        assert table[0] == ["algorithm_id", *rows]
        assert [line[0] for line in table[1:]] == algorithms
        assert all(len(line) == len(rows) + 1 for line in table)

    for path in (VALUE_MD_PATH, GRADIENT_MD_PATH):
        text = path.read_text(encoding="utf-8")
        assert text.startswith("| algorithm |")
        assert "bootstrap_dpf_current" in text
        assert "ledh_pfpf_alg1_ukf_current" in text
        assert "SMOKE_FIXTURE_NOT_BENCHMARK_RESULT" in text or "adapter_required" in text


def test_filter_bench_p8_runner_manifest_and_red_team_note_are_present() -> None:
    p8 = _load(P8_PATH)
    manifest = p8["run_manifest"]
    red_team = p8["post_run_red_team_note"]
    nonclaims = " ".join(p8["nonclaims"]).lower()

    required_manifest_fields = {
        "git_commit",
        "dirty_state_summary",
        "command",
        "environment",
        "conda_env",
        "cpu_gpu_status",
        "dtype",
        "seeds",
        "plan_file",
        "result_file",
        "output_json",
        "value_csv",
        "gradient_csv",
        "value_markdown",
        "gradient_markdown",
        "registry_artifact",
        "adapter_schema_artifact",
        "reference_oracle_artifact",
    }
    assert required_manifest_fields.issubset(manifest)
    assert manifest["output_json"] == str(P8_PATH)
    assert "strongest_alternative_explanation" in red_team
    assert "would_overturn_blocker" in red_team
    assert "weakest_part_of_evidence" in red_team
    assert "not a filter ranking" in nonclaims
    assert "does not contain full numeric benchmark errors" in nonclaims


def test_filter_bench_p8_runner_matrices_carry_two_lane_comparison_contract() -> None:
    p8 = _load(P8_PATH)
    scope = p8["benchmark_scope"]
    contract = p8["two_lane_comparison_contract"]

    assert scope["coverage_roster_is_broader_than_two_lane_comparison"] is True
    assert contract["comparison_program_master"].endswith(
        "bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md"
    )
    assert contract["coverage_roster_is_not_comparison_roster"] is True
    assert contract["lowdim_same_target"]["comparison_algorithm_ids"] == [
        "fixed_sgqf",
        "ukf",
        "cut4",
        "zhao_cui_scalar_or_multistate",
    ]
    assert contract["highdim_source_scope"]["comparison_algorithm_ids"] == [
        "fixed_sgqf",
        "ukf",
        "zhao_cui_scalar_or_multistate",
    ]
    assert contract["highdim_source_scope"]["excluded_algorithm_ids"] == ["cut4"]
