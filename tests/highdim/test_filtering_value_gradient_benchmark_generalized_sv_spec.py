from __future__ import annotations

import json
from pathlib import Path
from typing import Any


SPEC_JSON = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json"
)
SPEC_MD = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md"
)
SOURCE_SCOPE_JSON = Path(
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json"
)


def _spec() -> dict[str, Any]:
    return json.loads(SPEC_JSON.read_text(encoding="utf-8"))


def _source_scope() -> dict[str, Any]:
    return json.loads(SOURCE_SCOPE_JSON.read_text(encoding="utf-8"))


def test_generalized_sv_spec_declares_prior_mean_test_point_and_synthetic_policy() -> None:
    spec = _spec()
    generation = spec["synthetic_generation_contract"]
    prior = spec["prior_mean_test_point"]

    assert spec["schema_version"] == "filter_bench.generalized_sv.testing_spec.v1"
    assert spec["status"] == "PASS_FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC_CONTRACT"
    assert spec["numeric_status"] == (
        "PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING"
    )
    assert spec["row_id"] == "zhao_cui_generalized_sv_synthetic_from_estimated_values"
    assert generation["benchmark_data_policy"] == (
        "generate_synthetic_observations_from_sp500_prior_mean_test_point"
    )
    assert generation["SP500_role"] == "source_estimation_input_only_not_benchmark_data"
    assert generation["core_horizon"] == 1008
    assert "Synthetic data may be generated" in generation["admissible_pre_run_state"]
    assert prior["status"] == "ready"
    assert prior["derived_values"]["E_gamma"] == 0.8604651162790697
    assert prior["derived_values"]["E_sigma"] == 0.12533141373155002
    assert prior["active_transformed_values"]["z_mu_or_log_beta_over_sigma_center"] == 0.0
    assert any("E[sigma^2] is infinite" in item for item in prior["nonfinite_mean_caveats"])


def test_generalized_sv_spec_locks_source_route_equations_and_parameters() -> None:
    spec = _spec()
    target = spec["target_identity"]
    params = spec["parameter_contract"]
    transform = params["source_transform"]

    assert target["model_family"] == "zhao_cui_svmodels_generalized_stochastic_volatility"
    assert target["variance_transform"] == "v_t = boxcoxinv(tau * x_t, delta)"
    assert "phi * y_{t-1}" in target["transition_law"]
    assert "a * y_{t-1}^2" in target["transition_law"]
    assert target["initial_previous_observation"] == (
        "y_0 = 0 in the source st_process/transition route"
    )
    assert target["likelihood_density"] == "tpdf(y_t / sqrt(v_t), nu2) / sqrt(v_t)"
    assert params["physical_parameter_order"] == [
        "gamma",
        "tau",
        "mu",
        "phi",
        "a",
        "delta",
        "nu1",
        "nu2",
    ]
    assert params["active_estimated_indices_one_based"] == [1, 2, 3]
    assert params["active_estimated_parameters"] == ["gamma", "tau", "mu"]
    assert transform["gamma"] == "physical gamma = normcdf(z_gamma)"
    assert transform["mu"] == "physical mu = z_mu * tau when mu is estimated"


def test_generalized_sv_spec_forbids_defaults_and_project_fixture_as_truth() -> None:
    spec = _spec()
    estimate = spec["estimate_materialization_contract"]
    defaults = spec["parameter_contract"]["author_code_defaults_not_estimates"]

    assert estimate["current_status"] == "superseded_by_prior_mean_test_point"
    assert estimate["accepted_routes"] == [
        "paper_sp500_prior_mean_convention_recorded_in_this_spec"
    ]
    assert "physical_values" in estimate["required_estimate_artifact_fields"]
    assert "mean_convention_and_nonfinite_mean_caveats" in estimate["required_estimate_artifact_fields"]
    assert "author_code_defaults_not_estimates" in estimate["forbidden_substitutes"]
    assert "BayesFilter_native_generalized_sv_fixture" in estimate["forbidden_substitutes"]
    assert "SP500_returns_as_benchmark_observations" in estimate["forbidden_substitutes"]
    assert "ordinary_mean_of_sigma_squared_or_beta_when_nonfinite" in estimate["forbidden_substitutes"]
    assert defaults["gamma"] == 0.95
    assert defaults["tau_expression"] == "sqrt(3/64)"


def test_generalized_sv_spec_defines_reported_metrics_and_filter_policy() -> None:
    spec = _spec()
    metrics = spec["benchmark_metrics_contract"]

    assert metrics["primary_reported_quantities"] == [
        "log_likelihood_at_truth",
        "average_log_likelihood_at_truth_per_time",
        "score_norm_at_truth",
        "score_component_max_at_truth",
        "score_component_min_at_truth",
        "componentwise_score_at_truth",
    ]
    assert "standard_error_across_datasets" in metrics["replication_quantities"]
    assert "failure_rate" in metrics["replication_quantities"]
    assert "Kalman may appear only" in metrics["filter_policy"]
    assert "not a numeric benchmark result" in spec["nonclaims"]
    assert "not permission to use author defaults as test truth" in spec["nonclaims"]


def test_generalized_sv_spec_is_linked_from_source_scope_contract() -> None:
    spec = _spec()
    scope = _source_scope()
    rows = {row["row_id"]: row for row in scope["promoted_or_replacement_source_rows"]}
    row = rows["zhao_cui_generalized_sv_synthetic_from_estimated_values"]
    values = row["truth_or_test_values"]

    assert values["testing_spec"]["json"] == str(SPEC_JSON)
    assert values["testing_spec"]["markdown"] == str(SPEC_MD)
    assert row["numeric_readiness"] == "reviewed_evaluator_pending"
    assert scope["estimated_values_pending_source_row_ids"] == []
    assert values["prior_mean_test_point"]["status"] == "ready"
    assert values["prior_mean_test_point"]["physical_values"]["gamma"] == 0.8604651162790697


def test_generalized_sv_spec_markdown_contains_required_tokens_and_nonclaims() -> None:
    text = SPEC_MD.read_text(encoding="utf-8")

    assert "PASS_FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC_CONTRACT" in text
    assert "PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING" in text
    assert "SP500 returns are source-estimation input only" in text
    assert "Author-code defaults are recorded only" in text
    assert "E[sigma^2]" in text
