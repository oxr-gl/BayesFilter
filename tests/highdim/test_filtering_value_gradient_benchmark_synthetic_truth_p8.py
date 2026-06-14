from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


P8_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-contract-2026-06-11.json"
)
PREFLIGHT_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-preflight-matrix-2026-06-10.json"
)
CROSSWALK_CSV_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.csv"
)
CROSSWALK_MD_PATH = Path(
    "docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8-synthetic-truth-capability-crosswalk-2026-06-11.md"
)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_filter_bench_p8_synthetic_truth_contract_preserves_roster_and_status() -> None:
    p8 = _load(P8_PATH)
    preflight = _load(PREFLIGHT_PATH)

    assert p8["schema_version"] == "filter_bench.synthetic_truth_p8.v1"
    assert p8["phase"] == "FILTER_BENCH_P8"
    assert p8["status"] == "PASS_FILTER_BENCH_P8_SYNTHETIC_TRUTH_CONTRACT"
    assert (
        p8["numeric_benchmark_status"]
        == "BLOCK_FILTER_BENCH_P8_SYNTHETIC_TRUTH_NUMERIC_RUN_PENDING"
    )
    assert p8["frozen_roster"] == preflight["frozen_roster"]
    assert p8["benchmark_scope"]["contract_emission_complete"] is True
    assert p8["benchmark_scope"]["numeric_benchmark_execution_complete"] is False
    assert p8["benchmark_scope"]["performance_answer_complete"] is False
    assert p8["benchmark_scope"]["accepted_truth_draws_generated"] is False
    assert p8["benchmark_scope"]["p7_preflight_used_as_performance_evidence"] is False
    assert p8["benchmark_scope"]["smoke_fixtures_used_as_performance_evidence"] is False
    assert p8["benchmark_scope"]["old_ledh_pfpf_ot_current_evidence"] is False


def test_filter_bench_p8_synthetic_truth_crosswalk_has_no_silent_holes() -> None:
    p8 = _load(P8_PATH)
    algorithms = p8["frozen_roster"]["algorithm_ids"]
    rows = p8["frozen_roster"]["model_columns"]
    crosswalk = p8["capability_crosswalk"]

    assert set(crosswalk) == set(algorithms)
    assert len(p8["capability_crosswalk_rows"]) == p8["frozen_roster"]["expected_cell_count"]

    for algorithm_id in algorithms:
        assert set(crosswalk[algorithm_id]) == set(rows), algorithm_id
        for row_id in rows:
            cell = crosswalk[algorithm_id][row_id]
            label = f"{algorithm_id}::{row_id}"
            for field in p8["capability_crosswalk_columns"]:
                assert field in cell, label
            assert cell["current_performance_status"] in {
                "pending_numeric_execution",
                "not_applicable_by_target",
                "blocked_before_numeric_execution",
            }


def test_filter_bench_p8_synthetic_truth_enforces_phi_derivative_contract() -> None:
    p8 = _load(P8_PATH)
    coordinate_contract = p8["coordinate_contract"]
    allowed_score = set(coordinate_contract["allowed_score_derivative_provenance"])
    allowed_hessian = set(coordinate_contract["allowed_hessian_derivative_provenance_or_gap"])

    assert coordinate_contract["canonical_coordinate_system"] == (
        "phi_unconstrained_benchmark_coordinates"
    )
    assert "J_tau(phi)^T g_theta" in coordinate_contract["score_chain_rule"]
    assert "sum_k" in coordinate_contract["hessian_chain_rule"]
    assert "not_available_transform_gap" in allowed_score
    assert "not_available_transform_gap" in allowed_hessian
    assert "full_chain_rule_hessian_transform" in allowed_hessian
    assert "partial_transform_diagnostic_only" in allowed_hessian

    for cell in p8["capability_crosswalk_rows"]:
        label = f"{cell['algorithm_id']}::{cell['model_row_id']}"
        assert cell["score_derivative_provenance"] in allowed_score, label
        assert cell["hessian_derivative_provenance_or_gap"] in allowed_hessian, label
        if cell["score_derivative_provenance"] in {
            "native_phi_autodiff",
            "native_phi_analytic",
            "physical_theta_chain_rule_converted_to_phi",
        }:
            assert cell["score_coordinate_system"] == "canonical_phi", label

    predator_cell = p8["capability_crosswalk"]["zhao_cui_scalar_or_multistate"][
        "predator_prey_production_tuned_h25_dim_2"
    ]
    assert (
        predator_cell["hessian_derivative_provenance_or_gap"]
        == "not_available_transform_gap"
    )
    assert "not_available_transform_gap" in predator_cell["not_available_reason"]


def test_filter_bench_p8_synthetic_truth_requires_componentwise_score_artifact_schema() -> None:
    p8 = _load(P8_PATH)
    schemas = p8["benchmark_table_schemas"]

    assert "componentwise_score" in schemas
    componentwise = schemas["componentwise_score"]
    assert componentwise["mandatory"] is True
    required = {
        "algorithm_id",
        "model_row_id",
        "truth_draw_id",
        "parameter_coordinate",
        "signed_mean_score",
        "standard_error",
        "confidence_interval_low",
        "confidence_interval_high",
        "standardized_mean",
        "score_coordinate_system",
        "score_derivative_provenance",
        "performance_table_admission_status",
    }
    assert required.issubset(componentwise["fields"])
    assert schemas["score"]["numeric_status"] == (
        "pending_accepted_truth_draws_and_reviewed_evaluators"
    )


def test_filter_bench_p8_synthetic_truth_tuple_manifest_and_truth_design_are_frozen() -> None:
    p8 = _load(P8_PATH)
    tuple_contract = p8["tuple_level_crosswalk_contract"]
    truth = p8["truth_design_contract"]

    assert tuple_contract["status"] == "pending_accepted_truth_draws"
    assert {
        "model_row_id",
        "truth_draw_id",
        "algorithm_id",
        "truth_prior_lane",
        "accepted_draw_status",
        "truth_coordinate_system",
        "data_replicate_ids",
        "filter_seed_ids",
        "branch_veto_status",
        "failure_status",
        "performance_table_admission_status",
    }.issubset(tuple_contract["required_fields"])
    assert truth["truth_prior_lanes"] == ["core_prior", "stress_prior"]
    assert truth["horizon_calibration_ladder"]["status"] == "pending"
    assert truth["stochastic_seed_ladder"]["S"] == [4, 8, 16, 32]
    assert "0.25" in truth["stochastic_seed_ladder"]["mc_se_rule"]


def test_filter_bench_p8_synthetic_truth_dpf_and_historical_guards() -> None:
    p8 = _load(P8_PATH)

    historical = p8["historical_only_records"]
    assert historical == [
        {
            "algorithm_id": "ledh_pfpf_ot_historical",
            "current_evidence": False,
            "reason_codes": ["HISTORICAL_LEDHPFPF_OT_SUPERSEDED"],
            "admission_policy": "excluded_from_current_performance_tables",
        }
    ]

    for algorithm_id in ("bootstrap_dpf_current", "ledh_pfpf_alg1_ukf_current"):
        contract = p8["algorithm_specific_contracts"][algorithm_id]
        assert contract["stochastic_filter"] is True
        assert contract["filter_seed_ladder_required"] is True
        assert contract["mc_uncertainty_required_before_ranking"] is True
        assert "effective_sample_size" in contract["required_diagnostics"]
        assert "resampling_count" in contract["required_diagnostics"]
        assert contract["gradient_policy"] == (
            "not_certified_for_main_score_without_separate_review"
        )


def test_filter_bench_p8_synthetic_truth_csv_and_markdown_are_status_tables() -> None:
    p8 = _load(P8_PATH)
    rows = _csv_rows(CROSSWALK_CSV_PATH)
    md = CROSSWALK_MD_PATH.read_text(encoding="utf-8")

    assert len(rows) == p8["frozen_roster"]["expected_cell_count"]
    assert set(rows[0]) == set(p8["capability_crosswalk_columns"])
    assert md.startswith("| algorithm_id | model_row_id |")
    assert "pending_numeric_execution" in md
    assert "bootstrap_dpf_current" in md
    assert "ledh_pfpf_alg1_ukf_current" in md


def test_filter_bench_p8_synthetic_truth_decision_manifest_and_nonclaims() -> None:
    p8 = _load(P8_PATH)
    manifest = p8["run_manifest"]
    nonclaims = " ".join(p8["nonclaims"]).lower()
    red_team = p8["post_run_red_team_note"]

    assert len(p8["decision_table"]) == 2
    assert p8["decision_table"][0]["decision"] == "pass_revised_p8_contract_gate"
    assert p8["decision_table"][1]["decision"] == "block_full_numeric_p8_performance_closeout"
    assert manifest["output_json"] == str(P8_PATH)
    assert "No new random draws" in manifest["seeds"]
    assert "not a full numeric benchmark result" in nonclaims
    assert "not a filter ranking" in nonclaims
    assert "A contract artifact can look like progress" in red_team[
        "strongest_alternative_explanation"
    ]
