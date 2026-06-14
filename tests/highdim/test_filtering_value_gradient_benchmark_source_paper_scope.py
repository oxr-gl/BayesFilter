from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


CONTRACT_PATH = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)
SUMMARY_CSV_PATH = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.csv"
)
SUMMARY_MD_PATH = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-summary-2026-06-11.md"
)


def _load() -> dict[str, Any]:
    return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))


def _rows_by_id() -> dict[str, dict[str, Any]]:
    contract = _load()
    return {row["row_id"]: row for row in contract["promoted_or_replacement_source_rows"]}


def test_source_paper_scope_contract_status_and_nonclaims() -> None:
    contract = _load()

    assert contract["schema_version"] == "filter_bench.source_paper_scope.v1"
    assert contract["phase"] == "FILTER_BENCH_SOURCE_PAPER_BLOCKER_CLOSURE"
    assert contract["status"] == "PASS_FILTER_BENCH_SOURCE_PAPER_SCOPE_CONTRACT"
    assert (
        contract["numeric_benchmark_status"]
        == "BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING"
    )
    assert contract["scope_policy"]["old_p8_roster_mutated_in_place"] is False
    assert contract["scope_policy"]["future_promoted_numeric_tables_use_this_scope"] is True
    assert contract["scope_policy"]["preflight_or_smoke_values_are_performance_evidence"] is False
    assert contract["role_contract"]["supervisor_and_executor"] == "Codex in this dialogue"
    assert contract["role_contract"]["reviewer"] == "Claude Code read-only"
    assert contract["role_contract"]["detached_agent_allowed"] is False
    assert "not a numeric benchmark result" in contract["nonclaims"]


def test_p44_diagnostic_rows_are_removed_from_promoted_source_scope() -> None:
    contract = _load()
    source_scope = set(contract["source_scope_row_ids"])
    promoted = set(contract["promoted_source_row_ids"])
    replacement_required = set(contract["replacement_required_source_row_ids"])
    estimates_pending = set(contract["estimated_values_pending_source_row_ids"])
    removed = set(contract["p44_diagnostic_rows_removed_from_promoted_scope"])
    excluded = {row["row_id"]: row for row in contract["excluded_or_historical_rows"]}

    expected_p44 = {
        "p44_cubic_additive_gaussian_dim_1_2_3",
        "p44_quadratic_observation_dim_1_2_3",
        "p44_nonlinear_transition_h2_dim_1_2_3",
        "p44_nonlinear_transition_h4_cut4_extension_dim_1_2_3",
    }
    assert removed == expected_p44
    assert source_scope.isdisjoint(expected_p44)
    assert promoted.isdisjoint(expected_p44)
    assert replacement_required == set()
    assert estimates_pending == set()
    assert "zhao_cui_generalized_sv_synthetic_from_estimated_values" in promoted
    for row_id in expected_p44:
        assert excluded[row_id]["disposition"] == "excluded_from_promoted_source_paper_scope"
        assert "not a checked author-paper/code benchmark model" in excluded[row_id]["reason"]


def test_lgssm_exact_oracle_uses_explicit_identifiable_benchmark_values() -> None:
    row = _rows_by_id()["benchmark_lgssm_exact_oracle_m3_T50"]
    values = row["truth_or_test_values"]

    assert row["promotion_status"] == "promoted_exact_oracle_benchmark_row"
    assert row["source_status"] == "USER_AMENDED_EXACT_ORACLE_BENCHMARK"
    assert "lgssm_exact_kalman_dim_1_2_3" in row["replaces_or_supersedes"]
    assert values["state_dim"] == 3
    assert values["observation_dim"] == 3
    assert values["horizon"] == 50
    assert values["truth"] == {
        "phi1": 0.72,
        "phi2": 0.55,
        "phi3": 0.35,
        "q_scale": 0.35,
        "r_scale": 0.45,
    }
    assert values["transition_matrix"] == [
        [0.72, 0.0, 0.0],
        [0.0, 0.55, 0.0],
        [0.0, 0.0, 0.35],
    ]
    assert values["observation_matrix"] == [
        [1.0, 0.25, -0.15],
        [0.2, 1.1, 0.3],
        [-0.1, 0.35, 0.9],
    ]
    assert values["identifiability_diagnostics"]["observation_matrix_full_rank"] is True
    assert "MATLAB rng(0)" in values["benchmark_policy"]
    assert not any(anchor.endswith("models/kalman/setup.m") for anchor in row["source_anchors"])


def test_sv_actual_and_ksc_rows_share_source_truth_but_have_distinct_target_labels() -> None:
    rows = _rows_by_id()
    actual = rows["zhao_cui_sv_actual_nongaussian_T1000"]
    ksc = rows["zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000"]

    for row in (actual, ksc):
        values = row["truth_or_test_values"]
        assert values["horizon"] == 1000
        assert values["fixed_sigma"] == 1.0
        assert values["truth"] == {"gamma": 0.6, "beta": 0.4}
        assert values["prior"]["lower"] == {"gamma": 0.1, "beta": 0.1}
        assert values["prior"]["upper"] == {"gamma": 0.9, "beta": 0.9}
        assert any(anchor.endswith("models/sv/setup.m") for anchor in row["source_anchors"])

    assert actual["model_family"] == "stochastic_volatility_transformed_actual_nongaussian"
    assert ksc["model_family"] == "stochastic_volatility_ksc_gaussian_mixture_surrogate"
    assert ksc["source_status"] == "SOURCE_VALUES_FOUND_MIXTURE_DETAILS_SOURCE_GAP"
    assert "Gaussian-mixture observation target" in ksc["truth_or_test_values"]["surrogate_policy"]


def test_spatial_sir_source_row_promotes_j9_and_keeps_route_block_explicit() -> None:
    row = _rows_by_id()["zhao_cui_spatial_sir_austria_j9_T20"]
    values = row["truth_or_test_values"]
    fixed = values["fixed_parameters"]

    assert row["promotion_status"] == "promoted_source_paper_row_route_repair_required"
    assert row["numeric_readiness"] == "blocked_value_route_pending_rank_selection_repair"
    assert values["J"] == 9
    assert values["state_dim"] == 18
    assert values["observation_dim"] == 9
    assert values["horizon"] == 20
    assert values["theta_dimension"] == 0
    assert fixed["kappa"] == [0.1] * 9
    assert fixed["nu"] == [18.0] * 9
    assert fixed["initial_mean"][:4] == [486.0, 14.0, 487.0, 13.0]
    assert fixed["initial_mean"][-4:] == [493.0, 7.0, 494.0, 6.0]
    assert "spatial_sir_lower_rung_j1_dim_2" in row["replaces_or_supersedes"]


def test_predator_prey_source_row_uses_T20_and_physical_paper_values() -> None:
    row = _rows_by_id()["zhao_cui_predator_prey_T20"]
    values = row["truth_or_test_values"]

    assert row["promotion_status"] == "promoted_source_paper_row"
    assert values["horizon"] == 20
    assert values["initial_state"] == [50.0, 5.0]
    assert values["process_covariance"] == "4 * identity_2x2"
    assert values["observation_covariance"] == "4 * identity_2x2"
    assert values["paper_physical_truth"] == {
        "r": 0.6,
        "K": 114.0,
        "a": 25.0,
        "s": 0.3,
        "u": 0.5,
        "v": 0.5,
    }
    assert values["author_code_normalized_truth"] == [0.6, 1.2, 0.5, 0.3, 0.5, 0.5]
    assert "predator_prey_production_tuned_h25_dim_2" in row["replaces_or_supersedes"]


def test_generalized_sv_is_synthetic_from_sp500_prior_mean_test_point() -> None:
    row = _rows_by_id()["zhao_cui_generalized_sv_synthetic_from_estimated_values"]
    values = row["truth_or_test_values"]
    prior = values["prior_mean_test_point"]
    contract = _load()
    excluded = {item["row_id"]: item for item in contract["excluded_or_historical_rows"]}

    assert row["promotion_status"] == "promoted_source_paper_synthetic_row_prior_mean"
    assert row["numeric_readiness"] == "reviewed_evaluator_pending"
    assert row["source_status"] == "SOURCE_MODEL_AND_SP500_PRIOR_FOUND_PRIOR_MEAN_TEST_POINT_READY"
    assert "synthetic data" in values["benchmark_data_policy"]
    assert "do not use SP500 returns" in values["benchmark_data_policy"]
    assert values["source_author_route"] == "svmodels"
    assert values["horizon"] == 1008
    assert values["parameter_order"] == [
        "gamma",
        "tau",
        "mu",
        "phi",
        "a",
        "delta",
        "nu1",
        "nu2",
    ]
    assert values["estimated_parameters"] == ["gamma", "tau", "mu"]
    assert prior["status"] == "ready"
    assert prior["physical_values"]["gamma"] == 0.8604651162790697
    assert prior["physical_values"]["tau_or_sigma"] == 0.12533141373155002
    assert prior["physical_values"]["mu_or_log_beta_center_coordinate"] == 0.0
    assert prior["transformed_active_values"] == [
        1.0824113944610982,
        -2.076793740349318,
        0.0,
    ]
    assert any("E[sigma^2] is infinite" in item for item in prior["nonfinite_mean_caveats"])
    assert values["author_code_defaults_not_estimates"]["gamma"] == 0.95
    assert (
        values["author_code_defaults_not_estimates"]["tau"]["expression"]
        == "sqrt(3/64)"
    )
    assert values["estimated_indices"] == [1, 2, 3]
    assert (
        excluded["native_generalized_sv_dense_lower_rung_dim_2"]["disposition"]
        == "excluded_project_fixture_replacement_required"
    )
    assert (
        excluded["zhao_cui_generalized_sv_sp500_author_code"]["disposition"]
        == "superseded_by_synthetic_prior_mean_amendment"
    )


def test_source_paper_scope_summary_tables_are_status_tables() -> None:
    contract = _load()
    with SUMMARY_CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    md = SUMMARY_MD_PATH.read_text(encoding="utf-8")

    assert len(rows) == len(contract["promoted_or_replacement_source_rows"]) + len(
        contract["excluded_or_historical_rows"]
    )
    assert "p44_cubic_additive_gaussian_dim_1_2_3" in {row["row_id"] for row in rows}
    assert "zhao_cui_predator_prey_T20" in {row["row_id"] for row in rows}
    assert md.startswith("| row_id | scope_class |")
    assert "excluded_from_promoted_source_paper_scope" in md
    assert "BLOCK_FILTER_BENCH_SOURCE_PAPER_NUMERIC_RUN_PENDING" not in md
