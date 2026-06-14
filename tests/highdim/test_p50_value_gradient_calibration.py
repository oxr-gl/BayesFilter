from __future__ import annotations

import json
from pathlib import Path


CALIBRATION_PATH = Path(
    "docs/plans/bayesfilter-highdim-zhao-cui-p50-value-gradient-calibration-rules-2026-06-09.json"
)


def _calibration() -> dict[str, object]:
    return json.loads(CALIBRATION_PATH.read_text(encoding="utf-8"))


def test_p50_m4_calibration_schema_is_predeclared_before_model_ladders() -> None:
    calibration = _calibration()

    assert calibration["schema_version"] == "p50.value_gradient_calibration.v1"
    assert calibration["phase"] == "P50-M4"
    assert calibration["status"] == "PREDECLARED_FOR_P50_M5_M6"
    assert (
        calibration["threshold_source"]
        == "predeclared_before_p50_m5_m6_model_ladder_results"
    )


def test_p50_m4_value_and_gradient_metrics_are_separate_requirements() -> None:
    calibration = _calibration()
    value_metrics = set(calibration["value_metrics"])
    gradient_metrics = set(calibration["gradient_metrics"])
    acceptance_rule = calibration["acceptance_rule"]

    assert {
        "absolute_error",
        "relative_error",
        "per_step_error",
        "paired_same_data_gap",
        "likelihood_variability_normalized_gap",
    }.issubset(value_metrics)
    assert {
        "absolute_norm_error",
        "relative_norm_error",
        "directional_residuals",
        "directional_scaled_residual",
        "directional_cosine",
        "componentwise_finite_check",
    }.issubset(gradient_metrics)
    assert (
        acceptance_rule["promoted_same_target_pass"]
        == "requires_value_metrics_and_gradient_metrics_and_all_veto_diagnostics"
    )
    assert (
        acceptance_rule["value_only_rule"]
        == "value_only_agreement_is_diagnostic_not_gradient_correctness"
    )


def test_p50_m4_default_same_target_thresholds_are_finite_and_not_posthoc() -> None:
    calibration = _calibration()
    tolerances = calibration["default_same_target_tolerances"]
    acceptance_rule = calibration["acceptance_rule"]

    assert tolerances["scope"].startswith("small_float64_same_target")
    assert tolerances["value_abs_error_atol"] == 1e-6
    assert tolerances["value_rel_error_rtol"] == 1e-8
    assert tolerances["value_per_step_error_atol"] == 1e-7
    assert tolerances["gradient_norm_rel_error_rtol"] == 1e-5
    assert tolerances["directional_scaled_residual_rtol"] == 1e-5
    assert tolerances["directional_cosine_min"] == 0.999999
    assert "may_not_be_loosened_after_target_results" in acceptance_rule["threshold_change_rule"]


def test_p50_m4_likelihood_variability_is_explanatory_not_a_bias_excuse() -> None:
    policy = _calibration()["likelihood_variability_policy"]

    assert policy["role"] == "explanatory_only_not_bias_excuse"
    assert {
        "reference_replicate_mean",
        "reference_replicate_standard_deviation",
        "paired_same_data_algorithm_gap",
        "gap_to_replicate_sd_ratio",
    }.issubset(set(policy["required_reporting"]))
    assert "cannot_turn_a_failed_same_data" in policy["promotion_boundary"]


def test_p50_m4_finite_difference_policy_respects_user_numerical_concern() -> None:
    policy = _calibration()["finite_difference_policy"]

    assert policy["role"] == "diagnostic_only_not_sole_truth"
    assert policy["minimum_step_count_for_stable_window"] >= 4
    assert {
        "finite_values",
        "branch_identity_compatible",
        "measure_compatible",
        "complexity_gate_passed",
    }.issubset(set(policy["required_row_validity_checks"]))
    assert "stable_branch_compatible_finite" in policy["veto_boundary"]
    assert "inconclusive_not_proof_autodiff_is_wrong" in policy["inconclusive_boundary"]


def test_p50_m4_direction_policy_and_autodiff_checks_are_hmc_facing_but_not_hmc_readiness() -> None:
    calibration = _calibration()
    direction_policy = calibration["direction_policy"]
    autodiff_policy = calibration["autodiff_policy"]
    nonclaims = set(calibration["nonclaims"])

    assert direction_policy["minimum_direction_count"] >= 5
    assert {
        "coordinate_directions",
        "mixed_positive_direction",
        "mixed_alternating_direction",
    }.issubset(set(direction_policy["required_direction_families"]))
    assert {
        "finite_value",
        "finite_gradient",
        "no_hidden_stop_gradient_or_unreviewed_clipping",
        "deterministic_branch_replay_when_branch_fixed",
        "paired_same_target_reference_for_promoted_claims",
    }.issubset(set(autodiff_policy["required_checks"]))
    assert "long horizons and high dimensions" in autodiff_policy["long_high_dimensional_warning"]
    assert "no HMC readiness" in nonclaims


def test_p50_m4_nonclaims_remove_known_non_goals_from_future_gaps() -> None:
    calibration = _calibration()
    non_goals = set(calibration["explicit_non_goals"])
    nonclaims = set(calibration["nonclaims"])
    vetoes = set(calibration["veto_diagnostics"])

    assert "adaptive TT/SIRT source-faithful filtering" in non_goals
    assert "S&P 500 reproduction" in non_goals
    assert "no source-faithful adaptive TT/SIRT filtering" in nonclaims
    assert "no S&P 500 reproduction" in nonclaims
    assert "likelihood_variability_used_to_excuse_systematic_same_data_bias" in vetoes
    assert "single_finite_difference_check_promoted_as_truth" in vetoes
