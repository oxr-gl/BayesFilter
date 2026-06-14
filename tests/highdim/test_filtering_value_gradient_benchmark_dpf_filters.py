from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


COVERAGE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-coverage-2026-06-10.json"
)
SMOKE_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-filter-smoke-payloads-2026-06-10.json"
)
MATRIX_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-dpf-minimal-matrix-2026-06-10.json"
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
ALG1_PATH = Path("experiments/dpf_implementation/tf_tfp/filters/ledh_pfpf_alg1_ukf_tf.py")
BOOTSTRAP_PATH = Path("experiments/dpf_implementation/tf_tfp/filters/bootstrap_pf_tf.py")


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
            label = f"{algorithm['algorithm_id']}::{row_id}"
            assert row_id not in cells, label
            cells[row_id] = group
    return cells


def test_filter_bench_dpf_coverage_has_full_current_algorithm_by_target_matrix() -> None:
    coverage = _load(COVERAGE_PATH)
    registry = _load(REGISTRY_PATH)
    references = _load(REFERENCE_PATH)

    required_rows = set(registry["required_row_ids"])
    reference_rows = {row["registry_row_id"] for row in references["rows"]}
    assert coverage["schema_version"] == "filter_bench.dpf_filter_coverage.v1"
    assert coverage["phase"] == "FILTER_BENCH_P5"
    assert coverage["target_registry"] == str(REGISTRY_PATH)
    assert coverage["reference_oracles"] == str(REFERENCE_PATH)
    assert coverage["adapter_schema"] == str(SCHEMA_PATH)
    assert coverage["smoke_payloads"] == str(SMOKE_PATH)
    assert coverage["minimal_matrix"] == str(MATRIX_PATH)
    assert coverage["current_algorithm_ids"] == [
        "bootstrap_dpf_current",
        "ledh_pfpf_alg1_ukf_current",
    ]
    assert required_rows == reference_rows

    valid_statuses = set(coverage["cell_status_vocabulary"])
    valid_reasons = set(coverage["reason_code_vocabulary"])
    for algorithm in coverage["algorithms"]:
        assert algorithm["algorithm_id"] in coverage["current_algorithm_ids"]
        cells = _expanded_cells(algorithm)
        assert set(cells) == required_rows, algorithm["algorithm_id"]
        assert algorithm["adapter_paths"], algorithm["algorithm_id"]
        assert algorithm["nonclaims"], algorithm["algorithm_id"]
        for row_id, cell in cells.items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            assert cell["cell_status"] in valid_statuses, label
            assert cell["value_status_when_run"], label
            assert cell["gradient_status_when_run"], label
            assert set(cell["reason_codes"]).issubset(valid_reasons), label
            assert cell["reason_codes"], label
            assert cell["required_diagnostics"], label
            assert cell["evidence_tests"], label
            assert all(_test_nodeid_exists(nodeid) for nodeid in cell["evidence_tests"]), label


def test_filter_bench_dpf_coverage_statuses_preserve_gradient_and_blocker_meaning() -> None:
    coverage = _load(COVERAGE_PATH)

    for algorithm in coverage["algorithms"]:
        cells = _expanded_cells(algorithm)
        for row_id, cell in cells.items():
            label = f"{algorithm['algorithm_id']}::{row_id}"
            status = cell["cell_status"]
            if status == "READY_VALUE_WITH_STOCHASTIC_GRADIENT_STATUS":
                assert cell["value_status_when_run"] == "VALID", label
                assert cell["gradient_status_when_run"] == "RESAMPLING_GRADIENT_NOT_VALID", label
                assert "RESAMPLING_GRADIENT_NOT_VALID" in cell["reason_codes"], label
                assert "mc_standard_error" in cell["required_diagnostics"], label
            elif status == "READY_FIXED_BRANCH_DIAGNOSTIC":
                assert cell["value_status_when_run"] == "VALID", label
                assert cell["gradient_status_when_run"] == "FIXED_BRANCH_GRADIENT_DIAGNOSTIC", label
                assert "FIXED_BRANCH_GRADIENT_DIAGNOSTIC" in cell["reason_codes"], label
                assert "route_identifiers" in cell["required_diagnostics"], label
            elif status == "READY_DIAGNOSTIC_ONLY":
                assert "DIAGNOSTIC_ROW_NOT_PROMOTION" in cell["reason_codes"], label
            elif status == "ADAPTER_REQUIRED_WITH_REASON":
                assert cell["value_status_when_run"] == "NOT_RUN", label
                assert cell["gradient_status_when_run"] == "NOT_RUN", label
                assert any(code.startswith("ADAPTER_REQUIRED") for code in cell["reason_codes"]), label
            elif status == "BLOCKED_VALUE_ROUTE":
                assert row_id == "spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"
                assert "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION" in cell["reason_codes"], label


def test_filter_bench_dpf_current_route_implementations_are_guarded() -> None:
    coverage = _load(COVERAGE_PATH)
    alg1_text = ALG1_PATH.read_text(encoding="utf-8")
    bootstrap_text = BOOTSTRAP_PATH.read_text(encoding="utf-8")
    alg1_route = coverage["current_route_contract"]["ledh_pfpf_alg1_ukf_current"]

    assert "def run_bootstrap_particle_filter_tf" in bootstrap_text
    assert "stateless_categorical" in bootstrap_text
    assert "def run_ledh_pfpf_alg1_ukf_tf" in alg1_text
    assert "run_ledh_pfpf_ot_tf" not in alg1_text
    assert "ledh_pfpf_ot_tf" not in alg1_text
    assert alg1_route["method_generation"] == "li_coates_algorithm1_ukf_covariance_lifecycle"
    assert alg1_route["flow_source_route"] == "li_coates_2017_algorithm1_ledh_pfpf"
    assert alg1_route["covariance_route"] == "per_particle_ukf_prediction_update"
    assert alg1_route["flow_anchor_route"] == "zero_noise_transition"
    assert alg1_route["previous_ledh_pfpf_ot_evidence_status"] == "quarantined"


def test_filter_bench_dpf_smoke_payloads_obey_p2_schema_and_include_mc_diagnostics() -> None:
    schema = _load(SCHEMA_PATH)
    smoke = _load(SMOKE_PATH)
    registry_rows = {row["row_id"]: row for row in _load(REGISTRY_PATH)["rows"]}

    required_fields = set(schema["required_fields"])
    families = set(schema["algorithm_family_vocabulary"])
    references = set(schema["reference_type_vocabulary"])
    roles = set(schema["evidence_role_vocabulary"])
    value_statuses = set(schema["value_status_vocabulary"])
    gradient_statuses = set(schema["gradient_status_vocabulary"])
    reason_codes = set(schema["reason_code_vocabulary"])
    common_keys = set(schema["common_diagnostics_contract"]["required_common_keys"])
    payloads = smoke["payloads"]

    assert {payload["algorithm_id"] for payload in payloads if payload["evidence_role"] != "historical_only"} == {
        "bootstrap_dpf_current",
        "ledh_pfpf_alg1_ukf_current",
    }
    current_payloads = {
        payload["algorithm_id"]: payload
        for payload in payloads
        if payload["evidence_role"] != "historical_only"
    }
    assert current_payloads["bootstrap_dpf_current"]["gradient_status"] == (
        "RESAMPLING_GRADIENT_NOT_VALID"
    )
    assert "RESAMPLING_GRADIENT_NOT_VALID" in current_payloads["bootstrap_dpf_current"][
        "reason_codes"
    ]
    assert current_payloads["ledh_pfpf_alg1_ukf_current"]["gradient_status"] == (
        "FIXED_BRANCH_GRADIENT_DIAGNOSTIC"
    )
    assert "FIXED_BRANCH_GRADIENT_DIAGNOSTIC" in current_payloads[
        "ledh_pfpf_alg1_ukf_current"
    ]["reason_codes"]
    for payload in payloads:
        label = f"{payload['algorithm_id']}::{payload['registry_row_id']}"
        assert required_fields.issubset(payload), label
        assert payload["payload_schema_version"] == "filter_bench.adapter_payload.v1", label
        assert payload["algorithm_family"] in families, label
        assert payload["reference_type"] in references, label
        assert payload["evidence_role"] in roles, label
        assert payload["value_status"] in value_statuses, label
        assert payload["gradient_status"] in gradient_statuses, label
        assert payload["registry_row_id"] in registry_rows, label
        assert payload["reference_type"] == registry_rows[payload["registry_row_id"]]["reference_type"], label
        assert set(payload["reason_codes"]).issubset(reason_codes), label
        assert common_keys.issubset(payload["diagnostics"]), label
        assert payload["diagnostics"]["adapter_contract"] == "filter_bench.adapter_payload.v1", label
        assert payload["artifact_path"] == str(SMOKE_PATH), label
        assert payload["nonclaims"], label

        if payload["evidence_role"] == "historical_only":
            assert payload["diagnostics"]["current_evidence"] is False, label
            assert payload["runtime_seconds"] is None, label
            continue

        assert payload["diagnostics"]["current_evidence"] is True, label
        assert payload["value_status"] == "VALID", label
        assert isinstance(payload["value"], (int, float)), label
        assert payload["gradient"] is None, label
        assert payload["diagnostics"]["mc_standard_error"] is not None, label
        assert payload["diagnostics"]["particle_count"] > 0, label
        assert payload["diagnostics"]["seed_count"] >= 1, label
        assert payload["diagnostics"]["effective_sample_size_min"] is not None, label
        assert payload["diagnostics"]["resampling_policy"], label


def test_filter_bench_dpf_minimal_matrix_preserves_statuses_and_has_no_silent_holes() -> None:
    matrix = _load(MATRIX_PATH)
    algorithms = matrix["algorithms"]
    columns = matrix["model_columns"]

    assert algorithms == ["bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"]
    for matrix_name in ("value_error_matrix", "gradient_status_matrix"):
        block = matrix[matrix_name]
        assert set(block) == set(algorithms), matrix_name
        for algorithm_id in algorithms:
            assert set(block[algorithm_id]) == set(columns), algorithm_id
            for row_id, cell in block[algorithm_id].items():
                label = f"{matrix_name}::{algorithm_id}::{row_id}"
                assert cell["reason_codes"], label

    assert matrix["gradient_status_matrix"]["bootstrap_dpf_current"][
        "lgssm_exact_kalman_dim_1_2_3"
    ]["gradient_status"] == "resampling_gradient_not_valid"
    assert matrix["gradient_status_matrix"]["ledh_pfpf_alg1_ukf_current"][
        "p44_cubic_additive_gaussian_dim_1_2_3"
    ]["gradient_status"] == "fixed_branch_gradient_diagnostic"
    assert matrix["value_error_matrix"]["bootstrap_dpf_current"][
        "sv_exact_transformed_actual_nongaussian_dim_1_2_3"
    ]["status"] == "ADAPTER_REQUIRED_WITH_REASON"
    assert matrix["value_error_matrix"]["ledh_pfpf_alg1_ukf_current"][
        "spatial_sir_scaling_route_admitted_rank_selection_blocked_d18"
    ]["status"] == "BLOCKED_VALUE_ROUTE"


def test_filter_bench_dpf_old_ot_is_historical_only_not_current_evidence() -> None:
    coverage = _load(COVERAGE_PATH)
    smoke = _load(SMOKE_PATH)
    matrix = _load(MATRIX_PATH)

    current_text = json.dumps(
        {
            "current_route_contract": coverage["current_route_contract"],
            "algorithms": coverage["algorithms"],
            "smoke_current": [
                payload
                for payload in smoke["payloads"]
                if payload["evidence_role"] != "historical_only"
            ],
            "matrix_algorithms": matrix["algorithms"],
        }
    ).lower()
    historical_text = json.dumps(
        {
            "coverage_historical": coverage["historical_quarantine_records"],
            "smoke_historical": [
                payload
                for payload in smoke["payloads"]
                if payload["evidence_role"] == "historical_only"
            ],
            "matrix_historical": matrix["historical_only_records"],
        }
    ).lower()

    assert "ledh_pfpf_ot_historical" not in current_text
    assert "dpf_ledh_pfpf_ot" not in current_text
    assert "ledh-pfpf-ot" not in current_text
    assert "previous_ledh_pfpf_ot_evidence_status" in current_text
    assert "quarantined" in current_text
    assert "ledh_pfpf_ot_historical" in historical_text
    assert "historical_ledhpfpf_ot_superseded" in historical_text
    assert all(
        record["current_evidence"] is False
        for record in coverage["historical_quarantine_records"]
    )
