from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PREFLIGHT_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json"
)
REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)
SEMANTICS_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json"
)
DETERMINISTIC_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json"
)
DPF_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def test_filter_bench_preflight_matrix_freezes_full_algorithm_model_roster() -> None:
    preflight = _load(PREFLIGHT_PATH)
    registry = _load(REGISTRY_PATH)
    deterministic = _load(DETERMINISTIC_PATH)
    dpf = _load(DPF_PATH)

    expected_algorithms = deterministic["algorithm_ids"] + dpf["current_algorithm_ids"]
    expected_rows = registry["required_row_ids"]
    roster = preflight["frozen_roster"]

    assert preflight["schema_version"] == "filter_bench.preflight_matrix.v1"
    assert preflight["phase"] == "FILTER_BENCH_P7"
    assert preflight["target_registry"] == str(REGISTRY_PATH)
    assert preflight["gradient_semantics"] == str(SEMANTICS_PATH)
    assert preflight["deterministic_filter_coverage"] == str(DETERMINISTIC_PATH)
    assert preflight["dpf_filter_coverage"] == str(DPF_PATH)
    assert roster["algorithm_ids"] == expected_algorithms
    assert roster["model_columns"] == expected_rows
    assert roster["expected_cell_count"] == len(expected_algorithms) * len(expected_rows)
    assert len(preflight["preflight_cells"]) == roster["expected_cell_count"]
    assert "ledh_pfpf_ot_historical" not in roster["algorithm_ids"]
    assert roster["historical_algorithm_ids_excluded_from_current_roster"] == [
        "ledh_pfpf_ot_historical"
    ]


def test_filter_bench_preflight_matrix_has_no_silent_holes_or_empty_reasons() -> None:
    preflight = _load(PREFLIGHT_PATH)
    algorithms = preflight["frozen_roster"]["algorithm_ids"]
    rows = preflight["frozen_roster"]["model_columns"]
    expected_pairs = {(algorithm_id, row_id) for algorithm_id in algorithms for row_id in rows}
    seen_pairs = set()

    for cell in preflight["preflight_cells"]:
        pair = (cell["algorithm_id"], cell["registry_row_id"])
        assert pair not in seen_pairs, pair
        seen_pairs.add(pair)
        assert cell["source_status"], pair
        assert cell["cell_kind"], pair
        assert cell["value_status"], pair
        assert cell["raw_gradient_status"], pair
        assert cell["normalized_gradient_status"], pair
        assert cell["p8_gradient_error_policy"], pair
        assert cell["reason_codes"], pair
        assert cell["performance_interpretation"] == "not_performance_evidence", pair
        if cell["cell_kind"] == "smoke_fixture_available":
            assert cell["smoke_payload"] is not None, pair
        else:
            assert cell["smoke_payload"] is None, pair

    assert seen_pairs == expected_pairs


def test_filter_bench_preflight_matrices_match_cells_and_keep_status_only_gradients_null() -> None:
    preflight = _load(PREFLIGHT_PATH)
    value_matrix = preflight["value_status_matrix"]
    gradient_matrix = preflight["gradient_status_matrix"]
    rows = set(preflight["frozen_roster"]["model_columns"])
    cells = {
        (cell["algorithm_id"], cell["registry_row_id"]): cell
        for cell in preflight["preflight_cells"]
    }

    assert set(value_matrix) == set(preflight["frozen_roster"]["algorithm_ids"])
    assert set(gradient_matrix) == set(preflight["frozen_roster"]["algorithm_ids"])
    for algorithm_id in preflight["frozen_roster"]["algorithm_ids"]:
        assert set(value_matrix[algorithm_id]) == rows
        assert set(gradient_matrix[algorithm_id]) == rows
        for row_id in rows:
            cell = cells[(algorithm_id, row_id)]
            value_cell = value_matrix[algorithm_id][row_id]
            gradient_cell = gradient_matrix[algorithm_id][row_id]
            assert value_cell["status"] == cell["value_status"]
            assert value_cell["reason_codes"] == cell["reason_codes"]
            assert gradient_cell["raw_gradient_status"] == cell["raw_gradient_status"]
            assert gradient_cell["normalized_gradient_status"] == cell[
                "normalized_gradient_status"
            ]
            assert gradient_cell["reason_codes"] == cell["reason_codes"]
            assert gradient_cell["performance_interpretation"] == "not_performance_evidence"
            if not gradient_cell["p8_gradient_error_eligible"]:
                assert gradient_cell["preflight_gradient_error_abs"] is None
                assert gradient_cell["preflight_gradient_error_rel"] is None


def test_filter_bench_preflight_matrix_obeys_p6_gradient_semantics() -> None:
    preflight = _load(PREFLIGHT_PATH)
    semantics = _load(SEMANTICS_PATH)

    normalized_contracts = semantics["normalized_status_contracts"]
    coverage_rules = semantics["coverage_cell_status_rules"]
    for cell in preflight["preflight_cells"]:
        label = f"{cell['algorithm_id']}::{cell['registry_row_id']}"
        normalized = cell["normalized_gradient_status"]
        contract = normalized_contracts[normalized]
        source_rule = coverage_rules[cell["source_kind"]][cell["source_status"]]
        assert cell["p8_gradient_error_eligible"] == contract[
            "gradient_error_may_be_reported"
        ], label
        assert cell["p8_gradient_error_policy"] == source_rule[
            "matrix_gradient_error_policy"
        ], label
        if source_rule["matrix_gradient_error_policy"] != contract["matrix_gradient_error_policy"]:
            assert source_rule["matrix_gradient_error_policy"] == (
                "numeric_error_against_declared_surrogate_reference"
            ), label
            assert contract["matrix_gradient_error_policy"] == (
                "numeric_error_against_reference"
            ), label
        if cell["source_kind"] == "dpf":
            assert cell["p8_gradient_error_eligible"] is False, label
            assert cell["p8_gradient_error_policy"] == "null_with_status", label
            assert cell["raw_gradient_status"] != "VALID", label
        if cell["raw_gradient_status"] in {"GRADIENT_NOT_EXPOSED", "NO_THETA_GRADIENT_DIM0"}:
            assert cell["p8_gradient_error_eligible"] is False, label


def test_filter_bench_preflight_matrix_nonclaims_and_manifest_are_explicit() -> None:
    preflight = _load(PREFLIGHT_PATH)
    scope = preflight["preflight_scope"]
    manifest = preflight["run_manifest"]
    nonclaims = " ".join(preflight["nonclaims"]).lower()

    assert scope["preflight_values_are_performance_evidence"] is False
    assert scope["stochastic_preflight_values_are_rankable"] is False
    assert "no_silent_holes_policy" in scope
    assert scope["coverage_roster_is_broader_than_two_lane_comparison"] is True
    assert manifest["plan_file"].endswith("p7-preflight-matrix-subplan-2026-06-10.md")
    assert manifest["result_file"].endswith("p7-preflight-matrix-result-2026-06-10.md")
    assert manifest["preflight_output_path"] == str(PREFLIGHT_PATH)
    assert "not benchmark values" in nonclaims
    assert "no filter ranking" in nonclaims
    assert "no dpf gradient certification" in nonclaims


def test_filter_bench_preflight_matrix_carries_two_lane_comparison_contract() -> None:
    preflight = _load(PREFLIGHT_PATH)
    contract = preflight["two_lane_comparison_contract"]

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
