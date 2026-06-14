from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SEMANTICS_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-gradient-semantics-2026-06-10.json"
)
REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)
ADAPTER_SCHEMA_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json"
)
REFERENCE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json"
)
DETERMINISTIC_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json"
)
DPF_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _expanded_cells(algorithm: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cells: dict[str, dict[str, Any]] = {}
    for group in algorithm["row_groups"]:
        for row_id in group["row_ids"]:
            assert row_id not in cells, f"duplicate cell {algorithm['algorithm_id']}::{row_id}"
            cells[row_id] = group
    return cells


def test_filter_bench_gradient_semantics_declares_required_status_contracts() -> None:
    semantics = _load(SEMANTICS_PATH)
    adapter_schema = _load(ADAPTER_SCHEMA_PATH)

    assert semantics["schema_version"] == "filter_bench.gradient_semantics.v1"
    assert semantics["phase"] == "FILTER_BENCH_P6"
    assert semantics["target_registry"] == str(REGISTRY_PATH)
    assert semantics["adapter_schema"] == str(ADAPTER_SCHEMA_PATH)
    assert semantics["reference_oracles"] == str(REFERENCE_PATH)
    assert semantics["deterministic_filter_coverage"] == str(DETERMINISTIC_PATH)
    assert semantics["dpf_filter_coverage"] == str(DPF_PATH)

    contracts = semantics["normalized_status_contracts"]
    for status in semantics["required_statuses_from_subplan"]:
        assert status in contracts, status
    for status, contract in contracts.items():
        assert isinstance(contract["gradient_error_may_be_reported"], bool), status
        assert isinstance(contract["requires_reference_gradient"], bool), status
        assert contract["matrix_gradient_error_policy"], status

    gradient_statuses = set(adapter_schema["gradient_status_vocabulary"])
    assert "RESAMPLING_GRADIENT_NOT_VALID" in gradient_statuses
    assert "FIXED_BRANCH_GRADIENT_DIAGNOSTIC" in gradient_statuses
    assert semantics["matrix_emission_rules"]["zero_fill_gradient_error_for_noneligible_cells"] is False
    assert (
        semantics["matrix_emission_rules"][
            "missing_reference_gradient_may_pass_benchmarkable_value_gradient"
        ]
        is False
    )


def test_filter_bench_reference_gradient_policies_cover_rows_without_holes() -> None:
    semantics = _load(SEMANTICS_PATH)
    registry = _load(REGISTRY_PATH)
    references = _load(REFERENCE_PATH)

    rows = {row["registry_row_id"]: row for row in references["rows"]}
    assert set(rows) == set(registry["required_row_ids"])

    policy_rules = semantics["reference_gradient_policy_rules"]
    for row_id, row in rows.items():
        policy = row["reference_gradient_policy"]
        assert policy in policy_rules, row_id
        if row["benchmark_class"] == "benchmarkable_value_gradient":
            assert policy == "reference_gradient_available", row_id
            assert row["gradient_error_eligible"] is True, row_id
            assert row["reference_gradient_status_for_cells"] == "VALID", row_id
        elif row["benchmark_class"] == "benchmarkable_value_only":
            assert policy == "reference_gradient_unavailable_but_value_benchmarkable", row_id
            assert row["gradient_error_eligible"] is False, row_id
        elif row["benchmark_class"] == "blocked_only":
            assert policy == "blocked_value_route", row_id
            assert row["gradient_error_eligible"] is False, row_id
        elif row["benchmark_class"] in {"diagnostic_only", "surrogate_approximation_lane"}:
            assert policy == "reference_gradient_available", row_id


def test_filter_bench_deterministic_gradient_cells_follow_semantics() -> None:
    semantics = _load(SEMANTICS_PATH)
    references = {row["registry_row_id"]: row for row in _load(REFERENCE_PATH)["rows"]}
    deterministic = _load(DETERMINISTIC_PATH)
    rules = semantics["coverage_cell_status_rules"]["deterministic"]

    assert deterministic["status"] == "PASS_FILTER_BENCH_P4_DETERMINISTIC_FILTERS"
    for algorithm in deterministic["algorithms"]:
        for row_id, cell in _expanded_cells(algorithm).items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            rule = rules[cell["cell_status"]]
            raw_status = cell["gradient_status_when_run"]
            assert raw_status in rule["allowed_raw_gradient_statuses"], label

            row = references[row_id]
            if rule["gradient_error_may_be_reported"]:
                assert raw_status == "VALID", label
                assert row["reference_gradient_policy"] == "reference_gradient_available", label
                assert row["gradient_error_eligible"] is True, label
            else:
                assert rule["matrix_gradient_error_policy"] == "null_with_status", label
                if raw_status == "NO_THETA_GRADIENT_DIM0":
                    assert "fixed_0" in row["theta_dimension_policy"], label
                if raw_status == "GRADIENT_NOT_EXPOSED":
                    assert rule["normalized_status"] in {
                        "algorithm_gradient_not_exposed",
                        "diagnostic_only_not_promotion",
                    }, label


def test_filter_bench_dpf_gradient_cells_are_status_only_and_current_route_only() -> None:
    semantics = _load(SEMANTICS_PATH)
    dpf = _load(DPF_PATH)
    rules = semantics["coverage_cell_status_rules"]["dpf"]

    assert dpf["status"] == "PASS_FILTER_BENCH_P5_DPF_FILTERS"
    assert dpf["current_algorithm_ids"] == [
        "bootstrap_dpf_current",
        "ledh_pfpf_alg1_ukf_current",
    ]
    assert "ledh_pfpf_ot_historical" not in dpf["current_algorithm_ids"]

    for algorithm in dpf["algorithms"]:
        for row_id, cell in _expanded_cells(algorithm).items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            rule = rules[cell["cell_status"]]
            raw_status = cell["gradient_status_when_run"]
            assert raw_status in rule["allowed_raw_gradient_statuses"], label
            assert rule["gradient_error_may_be_reported"] is False, label
            assert rule["matrix_gradient_error_policy"] == "null_with_status", label
            for reason_code in rule.get("required_reason_codes", []):
                assert reason_code in cell["reason_codes"], label

    alg1 = next(
        algorithm
        for algorithm in dpf["algorithms"]
        if algorithm["algorithm_id"] == "ledh_pfpf_alg1_ukf_current"
    )
    assert alg1["route_identifiers_required"]["flow_anchor_route"] == "zero_noise_transition"
    assert (
        alg1["route_identifiers_required"]["previous_ledh_pfpf_ot_evidence_status"]
        == "quarantined"
    )
    assert all(
        record["current_evidence"] is False for record in dpf["historical_quarantine_records"]
    )


def test_filter_bench_gradient_matrix_emission_contract_forbids_zero_filling() -> None:
    semantics = _load(SEMANTICS_PATH)
    contracts = semantics["normalized_status_contracts"]

    for status, contract in contracts.items():
        label = f"normalized::{status}"
        if contract["gradient_error_may_be_reported"]:
            assert contract["requires_reference_gradient"] is True, label
            assert contract["matrix_gradient_error_policy"].startswith("numeric_error"), label
        else:
            assert contract["matrix_gradient_error_policy"] == "null_with_status", label

    matrix_rules = semantics["matrix_emission_rules"]
    assert set(matrix_rules["status_only_null_fields"]) == {
        "gradient_error_abs",
        "gradient_error_rel",
    }
    assert "gradient_status" in matrix_rules["status_only_required_fields"]
    assert "reason_codes" in matrix_rules["status_only_required_fields"]
    assert "gradient_error_abs" in matrix_rules["numeric_gradient_error_required_fields"]
    assert "reference_gradient_norm" in matrix_rules["numeric_gradient_error_required_fields"]
    assert matrix_rules["finite_gradient_check_is_explanatory_only"] is True
    assert matrix_rules["fixed_branch_gradient_check_is_explanatory_only"] is True
