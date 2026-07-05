from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py"
ARTIFACT = ROOT / "docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-03.json"
SIR_ROW = "zhao_cui_spatial_sir_austria_j9_T20"
_MODULE = None
_PAYLOAD = None


def _load_module():
    global _MODULE
    if _MODULE is not None:
        return _MODULE
    spec = importlib.util.spec_from_file_location("benchmark_two_lane_highdim_leaderboard", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("unable to load highdim leaderboard module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _MODULE = module
    return module


def _build_payload():
    global _PAYLOAD
    if _PAYLOAD is None:
        _PAYLOAD = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    return _PAYLOAD


def test_phase7_all_rows_have_batch_gpu_xla_status() -> None:
    payload = _build_payload()

    assert payload["rows"]
    for row in payload["rows"]:
        status = row["phase7_batch_gpu_xla_status"]
        assert status["scope"] in {"main_leaderboard_row", "scoped_component_row"}
        assert status["batch_status"]
        assert status["cpu_timing_status"]
        assert status["gpu_xla_status"]
        assert status["timing_rank_status"]


def test_phase7_blocked_or_value_only_cells_are_not_timing_rankable() -> None:
    payload = _build_payload()

    non_value_score_rows = [
        row for row in payload["rows"] if row["comparison_status"] != "executed_value_score"
    ]
    assert non_value_score_rows

    for row in non_value_score_rows:
        status = row["phase7_batch_gpu_xla_status"]
        assert status["batch_status"] == "not_applicable_until_value_score_row_exists"
        assert status["cpu_timing_status"] == "not_applicable_until_value_score_row_exists"
        assert status["gpu_xla_status"] == "not_applicable_until_value_score_row_exists"
        assert status["timing_rank_status"] == "not_rankable_correctness_gate_open"
        assert not status["evidence_paths"]


def test_phase7_p91_sidecar_timing_is_not_full_sir_row_admission() -> None:
    payload = _build_payload()
    row = next(
        item
        for item in payload["rows"]
        if item["row_id"] == SIR_ROW and item["algorithm_id"] == "zhao_cui_scalar_or_multistate"
    )

    assert row["comparison_status"] == "blocked_or_status_only"
    assert row["runtime_seconds"] is None
    main_status = row["phase7_batch_gpu_xla_status"]
    assert main_status["batch_status"] == "not_applicable_until_value_score_row_exists"
    assert main_status["gpu_xla_status"] == "not_applicable_until_value_score_row_exists"
    assert main_status["timing_rank_status"] == "not_rankable_correctness_gate_open"
    assert not main_status["evidence_paths"]

    sidecar = row["p91_scoped_evidence"]["phase7_sidecar_performance"]
    assert sidecar["namespace"] == "p91_scoped_local_complete_data_sidecar"
    assert sidecar["scope"] == "local_complete_data_zhao_cui_sir_d18_component"
    assert sidecar["admission_scope"] == "sidecar_only_not_full_observed_data_filtering_row"
    assert sidecar["excluded_from_main_leaderboard_ranking"] is True
    assert sidecar["main_row_admission_status"] == "not_full_observed_data_filtering_evidence"
    assert sidecar["status"] == "PASS_P91_PHASE6_PERFORMANCE_BENCHMARK"

    timing = sidecar["timing_by_target"]
    assert timing["cpu"]["status"] == "PASS_P91_PHASE6_CPU_BENCHMARK"
    assert timing["gpu_xla"]["status"] == "PASS_P91_PHASE6_GPU_XLA_BENCHMARK"
    assert timing["gpu_xla"]["actual_xla_status"] is True
    assert timing["cpu"]["checks"]["cpu_batched"]["steady_per_item_seconds"] is not None
    assert timing["gpu_xla"]["checks"]["gpu_xla_batched"]["steady_per_item_seconds"] is not None

    joined_nonclaims = " ".join(sidecar["nonclaims"])
    assert "not full observed-data/filtering SIR timing" in joined_nonclaims
    assert "not part of main leaderboard timing ranking" in joined_nonclaims


def test_phase7_executed_value_score_cells_do_not_gain_untrusted_gpu_claims() -> None:
    payload = _build_payload()
    rows = [
        row
        for row in payload["rows"]
        if row["comparison_status"] == "executed_value_score"
        and row.get("row_admission_status") != "scoped_component_row_admitted"
    ]

    assert rows
    for row in rows:
        status = row["phase7_batch_gpu_xla_status"]
        assert status["batch_status"] == "not_claimed_no_reviewed_batched_main_row_evaluator"
        assert status["gpu_xla_status"] == "not_claimed_no_trusted_row_specific_gpu_xla_manifest"
        assert status["timing_rank_status"] == "not_ranked_by_phase7_timing"


def test_phase7_parameterized_sir_scoped_component_is_not_full_row_timing() -> None:
    module = _load_module()
    row = module._apply_phase7_status(
        module._zhao_cui_parameterized_sir_local_complete_data_cell()
    )

    assert row["row_admission_status"] == "scoped_component_row_admitted"
    assert row["target_scope"] == "local_complete_data_zhao_cui_sir_d18_component"
    status = row["phase7_batch_gpu_xla_status"]
    assert status["scope"] == "scoped_component_row"
    assert status["batch_status"] == "p91_sidecar_batched_evidence_scoped_component_only"
    assert status["gpu_xla_status"] == "p91_sidecar_gpu_xla_scoped_component_only"
    assert status["timing_rank_status"] == "not_ranked_as_full_filtering_row"
    assert status["evidence_paths"]
    assert "not full observed-data/filtering SIR timing" in " ".join(status["nonclaims"])
