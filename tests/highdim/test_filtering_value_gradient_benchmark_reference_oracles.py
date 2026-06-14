from __future__ import annotations

import json
import ast
from pathlib import Path
from typing import Any


MANIFEST_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json"
)
REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)

BENCHMARK_CLASSES = {
    "benchmarkable_value_gradient",
    "benchmarkable_value_only",
    "diagnostic_only",
    "surrogate_approximation_lane",
    "blocked_only",
}
GRADIENT_POLICIES = {
    "reference_gradient_available",
    "reference_gradient_unavailable_but_value_benchmarkable",
    "reference_gradient_missing_blocks_gradient_benchmark",
    "blocked_value_route",
}
VALUE_POLICIES = {
    "reference_value_available",
    "diagnostic_reference_value_available",
    "surrogate_reference_value_available",
    "blocked_value_route",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _test_nodeid_exists(nodeid: str) -> bool:
    path_text, _, test_name = nodeid.partition("::")
    path = Path(path_text)
    if not path.exists():
        return False
    if not test_name:
        return True
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == test_name
        for node in ast.walk(tree)
    )


def test_filter_bench_reference_oracle_manifest_covers_every_p1_row() -> None:
    manifest = _load(MANIFEST_PATH)
    registry = _load(REGISTRY_PATH)

    assert manifest["schema_version"] == "filter_bench.reference_oracles.v1"
    assert manifest["phase"] == "FILTER_BENCH_P3"
    assert manifest["target_registry"] == str(REGISTRY_PATH)
    assert set(manifest["benchmark_class_vocabulary"]) == BENCHMARK_CLASSES
    assert set(manifest["reference_gradient_policy_vocabulary"]) == GRADIENT_POLICIES
    assert set(manifest["reference_value_policy_vocabulary"]) == VALUE_POLICIES

    manifest_rows = {row["registry_row_id"]: row for row in manifest["rows"]}
    registry_rows = {row["row_id"]: row for row in registry["rows"]}
    assert set(registry["required_row_ids"]) == set(manifest_rows)
    assert set(registry_rows).issuperset(manifest_rows)

    for row_id, manifest_row in manifest_rows.items():
        registry_row = registry_rows[row_id]
        assert manifest_row["reference_type"] == registry_row["reference_type"], row_id
        assert manifest_row["registry_row_class"] == registry_row["row_class"], row_id
        assert manifest_row["reference_route_label"] == registry_row["reference_route"]["label"], row_id
        assert manifest_row["benchmark_class"] in BENCHMARK_CLASSES, row_id
        assert manifest_row["reference_gradient_policy"] in GRADIENT_POLICIES, row_id
        assert manifest_row["reference_value_policy"] in VALUE_POLICIES, row_id
        assert manifest_row["diagnostics_required"], row_id
        assert manifest_row["evidence_tests"], row_id
        assert all(_test_nodeid_exists(nodeid) for nodeid in manifest_row["evidence_tests"]), row_id
        assert manifest_row["nonclaims"], row_id


def test_filter_bench_reference_oracle_value_and_gradient_eligibility_is_explicit() -> None:
    manifest_rows = {row["registry_row_id"]: row for row in _load(MANIFEST_PATH)["rows"]}

    for row_id, row in manifest_rows.items():
        if row["benchmark_class"] == "benchmarkable_value_gradient":
            assert row["value_error_eligible"] is True, row_id
            assert row["gradient_error_eligible"] is True, row_id
            assert row["reference_gradient_policy"] == "reference_gradient_available", row_id
            assert row["reference_gradient_status_for_cells"] == "VALID", row_id
        elif row["benchmark_class"] == "benchmarkable_value_only":
            assert row["value_error_eligible"] is True, row_id
            assert row["gradient_error_eligible"] is False, row_id
            assert row["reference_gradient_policy"] == (
                "reference_gradient_unavailable_but_value_benchmarkable"
            ), row_id
            assert row["reference_gradient_status_for_cells"] in {
                "NO_THETA_GRADIENT_DIM0",
                "GRADIENT_NOT_EXPOSED",
            }, row_id
        elif row["benchmark_class"] == "diagnostic_only":
            assert row["value_error_eligible"] is True, row_id
            assert row["gradient_error_eligible"] is True, row_id
            assert row["reference_value_policy"] == "diagnostic_reference_value_available", row_id
            assert row["reference_type"] == "diagnostic", row_id
        elif row["benchmark_class"] == "surrogate_approximation_lane":
            assert row["value_error_eligible"] is True, row_id
            assert row["gradient_error_eligible"] is True, row_id
            assert row["reference_value_policy"] == "surrogate_reference_value_available", row_id
            assert "surrogate" in row["target_scope"], row_id
        elif row["benchmark_class"] == "blocked_only":
            assert row["value_error_eligible"] is False, row_id
            assert row["gradient_error_eligible"] is False, row_id
            assert row["reference_value_policy"] == "blocked_value_route", row_id
            assert row["reference_gradient_policy"] == "blocked_value_route", row_id
            assert row["reference_gradient_status_for_cells"] == "BLOCKED_VALUE_ROUTE", row_id
            assert row["blocker"], row_id


def test_filter_bench_reference_oracles_keep_sv_actual_and_surrogate_distinct() -> None:
    rows = {row["registry_row_id"]: row for row in _load(MANIFEST_PATH)["rows"]}
    actual = rows["sv_exact_transformed_actual_nongaussian_dim_1_2_3"]
    surrogate = rows["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"]

    assert actual["benchmark_class"] == "benchmarkable_value_gradient"
    assert actual["reference_type"] == "transformed_actual_nongaussian"
    assert actual["reference_oracle_id"] == "exact_transformed_sv_dense_actual_nongaussian"
    assert "actual" in actual["target_scope"]
    assert "not KSC Gaussian mixture surrogate" in actual["nonclaims"]

    assert surrogate["benchmark_class"] == "surrogate_approximation_lane"
    assert surrogate["reference_type"] == "gaussian_mixture_surrogate"
    assert surrogate["reference_oracle_id"] == "ksc_sv_gaussian_mixture_kalman_enumeration"
    assert "surrogate" in surrogate["target_scope"]
    assert "not exact transformed actual non-Gaussian target" in surrogate["nonclaims"]


def test_filter_bench_reference_oracles_do_not_promote_approximate_filters_to_truth() -> None:
    manifest_rows = {row["registry_row_id"]: row for row in _load(MANIFEST_PATH)["rows"]}
    forbidden_oracle_text = json.dumps(
        [
            {
                "reference_oracle_id": row["reference_oracle_id"],
                "reference_route_label": row["reference_route_label"],
            }
            for row in manifest_rows.values()
        ]
    ).lower()

    assert "ukf" not in forbidden_oracle_text
    assert "cut4" not in forbidden_oracle_text
    assert "zhao_cui" not in forbidden_oracle_text
    assert "zhaocui" not in forbidden_oracle_text

    diagnostic = manifest_rows["p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3"]
    assert diagnostic["benchmark_class"] == "diagnostic_only"
    assert diagnostic["reference_type"] == "diagnostic"
    assert diagnostic["reference_value_policy"] == "diagnostic_reference_value_available"
    assert "not a Zhao-Cui horizon-4 promotion" in diagnostic["nonclaims"]


def test_filter_bench_reference_oracles_retain_blocked_spatial_sir_and_value_only_rows() -> None:
    rows = {row["registry_row_id"]: row for row in _load(MANIFEST_PATH)["rows"]}

    blocked = rows["spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"]
    assert blocked["benchmark_class"] == "blocked_only"
    assert blocked["blocker"] == "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION"
    assert "not_performance_cell" in blocked["diagnostics_required"]

    sir_lower = rows["spatial_sir_lower_rung_j1_dim_2"]
    predator_lower = rows["predator_prey_lower_rung_dim_2"]
    predator_production = rows["predator_prey_production_tuned_h25_dim_2"]
    assert sir_lower["reference_gradient_status_for_cells"] == "NO_THETA_GRADIENT_DIM0"
    assert predator_lower["reference_gradient_status_for_cells"] == "GRADIENT_NOT_EXPOSED"
    assert predator_production["reference_gradient_status_for_cells"] == "GRADIENT_NOT_EXPOSED"
    assert predator_production["reference_value_policy"] == "reference_value_available"
