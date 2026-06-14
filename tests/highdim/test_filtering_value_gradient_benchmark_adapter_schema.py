from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any


SCHEMA_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-schema-2026-06-10.json"
)
FIXTURES_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-adapter-fixtures-2026-06-10.json"
)
REGISTRY_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-target-registry-2026-06-10.json"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def test_filter_bench_adapter_schema_declares_uniform_contract() -> None:
    schema = _load(SCHEMA_PATH)

    assert schema["schema_version"] == "filter_bench.adapter_schema.v1"
    assert schema["phase"] == "FILTER_BENCH_P2"
    assert schema["fixture_payload_artifact"] == str(FIXTURES_PATH)
    assert schema["implementation_boundary"]["default_backend"] == (
        "tensorflow_or_tensorflow_probability"
    )
    assert schema["implementation_boundary"]["bayesfilter_owned_numpy_backend_allowed"] is False
    assert "without promotion" in schema["implementation_boundary"]["dpf_import_boundary"]

    assert set(schema["required_exercised_fixture_families"]) == {
        "kalman_or_mixture",
        "deterministic_sigma_point",
        "zhao_cui_tt",
        "particle_filter_current",
        "blocked_only",
        "historical_only",
    }
    assert "INVALID_GRADIENT_NONFINITE" in schema["gradient_status_vocabulary"]
    assert "DISCONNECTED_GRADIENT" in schema["gradient_status_vocabulary"]
    assert "STOCHASTIC_GRADIENT_DIAGNOSTIC" in schema["gradient_status_vocabulary"]
    assert "RESAMPLING_GRADIENT_NOT_VALID" in schema["gradient_status_vocabulary"]
    assert "FIXED_BRANCH_GRADIENT_DIAGNOSTIC" in schema["gradient_status_vocabulary"]
    assert "HISTORICAL_LEDHPFPF_OT_SUPERSEDED" in schema["reason_code_vocabulary"]


def test_filter_bench_adapter_fixtures_cover_required_families_and_statuses() -> None:
    schema = _load(SCHEMA_PATH)
    fixtures = _load(FIXTURES_PATH)
    payloads = fixtures["payloads"]

    families = {payload["algorithm_family"] for payload in payloads}
    assert set(schema["required_exercised_fixture_families"]).issubset(families)

    gradient_statuses = {payload["gradient_status"] for payload in payloads}
    assert "VALID" in gradient_statuses
    assert "GRADIENT_NOT_EXPOSED" in gradient_statuses
    assert "INVALID_GRADIENT_NONFINITE" in gradient_statuses
    assert "DISCONNECTED_GRADIENT" in gradient_statuses
    assert "STOCHASTIC_GRADIENT_DIAGNOSTIC" in gradient_statuses
    assert "BLOCKED_VALUE_ROUTE" in gradient_statuses
    assert "HISTORICAL_ONLY_NOT_EVIDENCE" in gradient_statuses


def test_filter_bench_adapter_fixture_payloads_obey_schema_and_registry() -> None:
    schema = _load(SCHEMA_PATH)
    fixtures = _load(FIXTURES_PATH)
    registry = _load(REGISTRY_PATH)

    required_fields = set(schema["required_fields"])
    families = set(schema["algorithm_family_vocabulary"])
    references = set(schema["reference_type_vocabulary"])
    roles = set(schema["evidence_role_vocabulary"])
    value_statuses = set(schema["value_status_vocabulary"])
    gradient_statuses = set(schema["gradient_status_vocabulary"])
    reason_codes = set(schema["reason_code_vocabulary"])
    common_keys = set(schema["common_diagnostics_contract"]["required_common_keys"])
    registry_rows = {row["row_id"]: row for row in registry["rows"]}

    for payload in fixtures["payloads"]:
        label = f"{payload.get('algorithm_id')}::{payload.get('registry_row_id')}"
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
        assert payload["reason_codes"], label
        assert common_keys.issubset(payload["diagnostics"]), label
        assert payload["diagnostics"]["adapter_contract"] == "filter_bench.adapter_payload.v1", label
        assert payload["artifact_path"] == str(FIXTURES_PATH), label
        assert payload["nonclaims"], label

        if payload["value_status"] == "VALID":
            assert _is_number(payload["value"]), label
            assert _is_number(payload["runtime_seconds"]), label
        else:
            assert payload["value"] is None, label

        if payload["gradient_status"] == "VALID":
            assert isinstance(payload["gradient"], list), label
            assert len(payload["gradient"]) == payload["theta_dimension"], label
            assert all(_is_number(item) for item in payload["gradient"]), label
        else:
            assert payload["gradient"] is None, label


def test_filter_bench_adapter_fixture_status_consistency_rules_are_enforced() -> None:
    payloads = _load(FIXTURES_PATH)["payloads"]

    for payload in payloads:
        label = f"{payload['algorithm_id']}::{payload['registry_row_id']}"
        if payload["theta_dimension"] == 0:
            assert payload["gradient_status"] in {
                "NO_THETA_GRADIENT_DIM0",
                "BLOCKED_VALUE_ROUTE",
            }, label
        if payload["evidence_role"] == "historical_only":
            assert payload["value_status"] == "HISTORICAL_ONLY_NOT_EVIDENCE", label
            assert payload["gradient_status"] == "HISTORICAL_ONLY_NOT_EVIDENCE", label
            assert payload["diagnostics"]["current_evidence"] is False, label
            assert "HISTORICAL_LEDHPFPF_OT_SUPERSEDED" in payload["reason_codes"], label
            assert payload["runtime_seconds"] is None, label
        if payload["evidence_role"] == "blocked_only":
            assert payload["value_status"] in {"BLOCKED_VALUE_ROUTE", "NOT_RUN"}, label
            assert "BLOCK_P53_M5_RANK_SELECTION_INTEGRATION" in payload["reason_codes"], label
            assert payload["runtime_seconds"] is None, label
        if payload["reason_codes"] == ["NONE"]:
            assert payload["value_status"] == "VALID", label
            assert payload["gradient_status"] == "VALID", label


def test_filter_bench_adapter_fixture_keeps_dpf_current_and_historical_distinct() -> None:
    payloads = _load(FIXTURES_PATH)["payloads"]
    current_dpf = [
        payload
        for payload in payloads
        if payload["algorithm_family"] == "particle_filter_current"
    ]
    historical = [
        payload for payload in payloads if payload["evidence_role"] == "historical_only"
    ]

    assert current_dpf
    assert {payload["algorithm_id"] for payload in current_dpf}.issubset(
        {"bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"}
    )
    assert any(
        payload["algorithm_id"] == "ledh_pfpf_alg1_ukf_current"
        and payload["gradient_status"] in {"INVALID_GRADIENT_NONFINITE", "DISCONNECTED_GRADIENT"}
        for payload in current_dpf
    )

    assert historical
    assert all(payload["algorithm_id"] == "ledh_pfpf_ot_historical" for payload in historical)
    assert all(
        payload["value_status"] == "HISTORICAL_ONLY_NOT_EVIDENCE"
        and payload["gradient_status"] == "HISTORICAL_ONLY_NOT_EVIDENCE"
        for payload in historical
    )
