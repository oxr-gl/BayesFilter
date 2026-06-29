from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


COVERAGE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-coverage-2026-06-10.json"
)
SMOKE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-deterministic-filter-smoke-payloads-2026-06-10.json"
)
SCHEMA_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json"
)
REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)
REFERENCE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-reference-oracles-2026-06-10.json"
)


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


def _expanded_cells(algorithm: dict[str, Any]) -> dict[str, dict[str, Any]]:
    cells: dict[str, dict[str, Any]] = {}
    for group in algorithm["row_groups"]:
        for row_id in group["row_ids"]:
            assert row_id not in cells, f"duplicate cell for {algorithm['algorithm_id']}::{row_id}"
            cells[row_id] = group
    return cells


def test_filter_bench_deterministic_coverage_has_full_algorithm_by_target_matrix() -> None:
    coverage = _load(COVERAGE_PATH)
    registry = _load(REGISTRY_PATH)
    references = _load(REFERENCE_PATH)

    required_rows = set(registry["required_row_ids"])
    reference_rows = {row["registry_row_id"] for row in references["rows"]}
    assert coverage["schema_version"] == "filter_bench.deterministic_filter_coverage.v1"
    assert coverage["phase"] == "FILTER_BENCH_P4"
    assert coverage["target_registry"] == str(REGISTRY_PATH)
    assert coverage["reference_oracles"] == str(REFERENCE_PATH)
    assert coverage["smoke_payloads"] == str(SMOKE_PATH)
    assert required_rows == reference_rows
    assert [algorithm["algorithm_id"] for algorithm in coverage["algorithms"]] == coverage[
        "algorithm_ids"
    ]

    valid_statuses = set(coverage["cell_status_vocabulary"])
    valid_reasons = set(coverage["reason_code_vocabulary"])
    for algorithm in coverage["algorithms"]:
        cells = _expanded_cells(algorithm)
        assert set(cells) == required_rows, algorithm["algorithm_id"]
        assert algorithm["adapter_paths"], algorithm["algorithm_id"]
        assert algorithm["nonclaims"], algorithm["algorithm_id"]
        for row_id, cell in cells.items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            assert cell["cell_status"] in valid_statuses, label
            assert set(cell["reason_codes"]).issubset(valid_reasons), label
            assert cell["reason_codes"], label
            assert cell["value_status_when_run"], label
            assert cell["gradient_status_when_run"], label
            assert cell["evidence_tests"], label
            assert all(_test_nodeid_exists(nodeid) for nodeid in cell["evidence_tests"]), label


def test_filter_bench_deterministic_coverage_statuses_are_machine_readable() -> None:
    coverage = _load(COVERAGE_PATH)

    for algorithm in coverage["algorithms"]:
        cells = _expanded_cells(algorithm)
        for row_id, cell in cells.items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            status = cell["cell_status"]
            if status in {"READY_VALUE_GRADIENT", "READY_SURROGATE_VALUE_GRADIENT"}:
                assert cell["value_status_when_run"] == "VALID", label
                assert cell["gradient_status_when_run"] == "VALID", label
                assert cell["reason_codes"] == ["NONE"], label
            elif status == "READY_VALUE_ONLY":
                assert cell["value_status_when_run"] == "VALID", label
                assert cell["gradient_status_when_run"] in {
                    "GRADIENT_NOT_EXPOSED",
                    "NO_THETA_GRADIENT_DIM0",
                }, label
                assert "NONE" not in cell["reason_codes"], label
            elif status == "READY_DIAGNOSTIC_ONLY":
                assert cell["value_status_when_run"] == "VALID", label
                assert "NONE" not in cell["reason_codes"], label
            elif status == "SCOUT_ONLY_NOT_TRUTH":
                assert cell["value_status_when_run"] == "NOT_RUN", label
                assert cell["gradient_status_when_run"] == "NOT_RUN", label
                assert "UKF_SCOUT_NOT_TRUTH" in cell["reason_codes"], label
            elif status == "ADAPTER_REQUIRED_WITH_REASON":
                assert cell["value_status_when_run"] == "NOT_RUN", label
                assert cell["gradient_status_when_run"] == "NOT_RUN", label
            elif status == "UNSUPPORTED_WITH_REASON":
                assert cell["value_status_when_run"] == "UNSUPPORTED_BY_TARGET", label
                assert cell["gradient_status_when_run"] == "UNSUPPORTED_BY_TARGET", label
            elif status == "BLOCKED_VALUE_ROUTE":
                assert cell["value_status_when_run"] == "BLOCKED_VALUE_ROUTE", label
                assert cell["gradient_status_when_run"] == "BLOCKED_VALUE_ROUTE", label
                assert "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION" in cell["reason_codes"], label


def test_filter_bench_deterministic_coverage_preserves_route_boundaries() -> None:
    algorithms = {algorithm["algorithm_id"]: algorithm for algorithm in _load(COVERAGE_PATH)["algorithms"]}

    kalman = _expanded_cells(algorithms["kalman_exact_or_mixture_enumeration"])
    assert kalman["lgssm_exact_kalman_dim_1_2_3"]["cell_status"] == "READY_VALUE_GRADIENT"
    assert kalman["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"]["cell_status"] == (
        "READY_SURROGATE_VALUE_GRADIENT"
    )
    assert kalman["sv_exact_transformed_actual_nongaussian_dim_1_2_3"]["cell_status"] == (
        "UNSUPPORTED_WITH_REASON"
    )

    ukf = _expanded_cells(algorithms["ukf"])
    assert ukf["p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3"][
        "cell_status"
    ] == "READY_DIAGNOSTIC_ONLY"
    assert ukf["spatial_sir_lower_rung_j1_dim_2"]["gradient_status_when_run"] == (
        "NO_THETA_GRADIENT_DIM0"
    )
    assert ukf["spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"][
        "cell_status"
    ] == "SCOUT_ONLY_NOT_TRUTH"
    assert "UKF_SCOUT_NOT_TRUTH" in ukf[
        "spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"
    ]["reason_codes"]

    svd = _expanded_cells(algorithms["svd_sigma_point"])
    cut4 = _expanded_cells(algorithms["cut4"])
    for cells in (svd, cut4):
        assert cells["p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3"][
            "cell_status"
        ] == "READY_DIAGNOSTIC_ONLY"
        assert cells["spatial_sir_lower_rung_j1_dim_2"]["gradient_status_when_run"] == (
            "NO_THETA_GRADIENT_DIM0"
        )

    zhao_cui = _expanded_cells(algorithms["zhao_cui_scalar_or_multistate"])
    assert zhao_cui["lgssm_exact_kalman_dim_1_2_3"]["reason_codes"] == [
        "ZHAOCUI_LGSSM_DIAGNOSTIC_NOT_ORACLE"
    ]
    assert zhao_cui["p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3"][
        "cell_status"
    ] == "UNSUPPORTED_WITH_REASON"
    assert "ZHAOCUI_H4_SCALAR_HELPER_NONCLAIM" in zhao_cui[
        "p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3"
    ]["reason_codes"]
    assert zhao_cui["native_generalized_sv_dense_lower_rung_dim_2"]["cell_status"] == (
        "UNSUPPORTED_WITH_REASON"
    )
    assert zhao_cui["spatial_sir_lower_rung_j1_dim_2"]["gradient_status_when_run"] == (
        "NO_THETA_GRADIENT_DIM0"
    )


def test_filter_bench_deterministic_smoke_payloads_obey_p2_schema() -> None:
    schema = _load(SCHEMA_PATH)
    smoke = _load(SMOKE_PATH)
    coverage = _load(COVERAGE_PATH)
    registry_rows = {row["row_id"]: row for row in _load(REGISTRY_PATH)["rows"]}

    required_fields = set(schema["required_fields"])
    reason_codes = set(schema["reason_code_vocabulary"])
    common_keys = set(schema["common_diagnostics_contract"]["required_common_keys"])
    payloads = smoke["payloads"]
    assert {payload["algorithm_id"] for payload in payloads} == set(coverage["algorithm_ids"])

    for payload in payloads:
        label = f"{payload['algorithm_id']}::{payload['registry_row_id']}"
        assert required_fields.issubset(payload), label
        assert payload["payload_schema_version"] == "filter_bench.adapter_payload.v1", label
        assert payload["registry_row_id"] in registry_rows, label
        assert payload["reference_type"] == registry_rows[payload["registry_row_id"]]["reference_type"], label
        assert set(payload["reason_codes"]).issubset(reason_codes), label
        assert common_keys.issubset(payload["diagnostics"]), label
        assert payload["diagnostics"]["adapter_contract"] == "filter_bench.adapter_payload.v1", label
        assert payload["diagnostics"]["current_evidence"] is False, label
        assert payload["artifact_path"] == str(SMOKE_PATH), label
        if payload["value_status"] == "VALID":
            assert isinstance(payload["value"], (int, float)), label
        else:
            assert payload["value"] is None, label
        if payload["gradient_status"] == "VALID":
            assert isinstance(payload["gradient"], list), label
            assert len(payload["gradient"]) == payload["theta_dimension"], label
        else:
            assert payload["gradient"] is None, label
        assert payload["nonclaims"], label


def test_filter_bench_deterministic_coverage_excludes_stale_blockers_and_old_dpf() -> None:
    text = json.dumps(_load(COVERAGE_PATH))

    assert "blocked_current_scalar_nonlinear_route_requires_state_dim_1" not in text
    assert "LEDH-PFPF-OT" not in text
    assert "ledh_pfpf_ot" not in text.lower()
    assert "adaptive MATLAB TT-cross/SIRT reproduction" in text
    assert "No Zhao-Cui row is an exact oracle." in text


def test_filter_bench_deterministic_coverage_encodes_two_lane_comparison_boundary() -> None:
    coverage = _load(COVERAGE_PATH)
    contract = coverage["two_lane_comparison_contract"]
    algorithms = {algorithm["algorithm_id"]: algorithm for algorithm in coverage["algorithms"]}
    fixed_sgqf = _expanded_cells(algorithms["fixed_sgqf"])
    cut4 = _expanded_cells(algorithms["cut4"])

    assert contract["comparison_program_master"].endswith(
        "bayesfilter-two-lane-filter-comparison-master-program-2026-06-24.md"
    )
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
    assert contract["highdim_source_scope"]["actual_and_surrogate_sv_must_remain_separate"] is True
    assert "tiny_same_target_surrogate_fixture_only" in contract["lowdim_same_target"][
        "sgqf_scope_qualifier"
    ]

    assert fixed_sgqf["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"]["cell_status"] == (
        "READY_SURROGATE_VALUE_GRADIENT"
    )
    for row_id in contract["highdim_source_scope"]["blocked_fixed_sgqf_lowdim_replacement_rows"]:
        assert fixed_sgqf[row_id]["cell_status"] == "ADAPTER_REQUIRED_WITH_REASON"

    assert cut4["sv_ksc_gaussian_mixture_surrogate_dim_1_2_3"]["cell_status"] == (
        "READY_SURROGATE_VALUE_GRADIENT"
    )
