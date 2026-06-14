#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DEFAULT_JSON = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.json"
)
DEFAULT_MD = ROOT / (
    "docs/plans/"
    "bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md"
)


def build_spec() -> dict[str, Any]:
    gamma_unit_mean = 20.0 / 21.5
    gamma_prior_mean = 2.0 * gamma_unit_mean - 1.0
    sigma_prior_center = 0.12533141373155002
    z_gamma_prior_mean = 1.0824113944610982
    log_sigma_prior_center = -2.076793740349318
    source_paths = {
        "paper_pdf": ".local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf",
        "sp500_driver": "third_party/audit/zhao_cui_tensor_ssm_p10/source/eg2_sv/mainscriptSP500.m",
        "setup": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/setup.m",
        "ftt2true": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/ftt2true.m",
        "true2ftt": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/true2ftt.m",
        "transition": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/transition.m",
        "state_simulator": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/st_process.m",
        "observation_simulator": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/ob_process.m",
        "likelihood": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/like.m",
        "prior": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/priorpdf.m",
        "prior_sampler": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/svmodels/priorsam.m",
        "weighted_stats": "third_party/audit/zhao_cui_tensor_ssm_p10/source/models/stats_weighted.m",
    }
    return {
        "schema_version": "filter_bench.generalized_sv.testing_spec.v1",
        "metadata_date": "2026-06-12",
        "phase": "FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC",
        "status": "PASS_FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC_CONTRACT",
        "numeric_status": (
            "PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING"
        ),
        "row_id": "zhao_cui_generalized_sv_synthetic_from_estimated_values",
        "purpose": (
            "Finish the generalized stochastic-volatility testing specification "
            "for the filtering value/gradient benchmark after the user amended "
            "the target to use the Zhao-Cui S&P 500 prior-center test case."
        ),
        "source_support_summary": {
            "model_route_found": True,
            "route_name": "svmodels",
            "sp500_prior_distribution_found": True,
            "prior_mean_test_point_materialized": True,
            "local_numeric_posterior_estimated_values_found": False,
            "local_gap": (
                "The local paper text and author mirror expose the svmodels route "
                "and S&P 500 prior distribution. The benchmark now uses the "
                "finite prior-center convention below rather than waiting for a "
                "posterior estimate table."
            ),
            "author_defaults_status": "configuration_defaults_not_test_truth",
            "source_paths": source_paths,
        },
        "source_prior_contract": {
            "paper_section": "Zhao-Cui Section 6.2 S&P 500 index",
            "paper_horizon": 1008,
            "paper_parameter_order": ["gamma", "sigma", "beta"],
            "paper_priors": {
                "(gamma+1)/2": "Beta(20, 1.5)",
                "sigma_squared": "IG(zeta/2, S_sigma/2) with zeta=2 and S_sigma=0.01",
                "log_beta_given_sigma": "Normal(beta0, sigma^2/q0) with beta0=0 and q0=0.8",
                "initial_state": "X0 | gamma, sigma ~ Normal(0, sigma^2 / (1 - gamma^2))",
            },
            "paper_transform": {
                "theta_prime": "(Phi^{-1}(gamma), log(sigma), log(beta)/sigma)",
                "state_prime": "X_t / sigma",
            },
            "author_code_coordinate_caveat": (
                "The mirrored svmodels code names the third active coordinate mu "
                "and maps it as mu = z_mu * tau. At the prior center, z_mu and "
                "log(beta)/sigma both equal zero, so the test point is invariant "
                "to this label/factor convention; score-coordinate interpretation "
                "still requires a separate evaluator contract."
            ),
        },
        "prior_mean_test_point": {
            "status": "ready",
            "mean_convention": (
                "Use finite prior centers in the source-route testing coordinates: "
                "E[(gamma+1)/2], E[sigma], and E[log(beta)/sigma]=0. Do not claim "
                "that every original physical coordinate has a finite ordinary mean."
            ),
            "derived_values": {
                "E_beta_unit_for_gamma": gamma_unit_mean,
                "E_gamma": gamma_prior_mean,
                "E_sigma": sigma_prior_center,
                "E_log_beta": 0.0,
                "beta_log_center_or_median": 1.0,
            },
            "source_route_physical_values": {
                "gamma": gamma_prior_mean,
                "tau_or_sigma": sigma_prior_center,
                "mu_or_log_beta_center_coordinate": 0.0,
                "phi": 0.0,
                "a": 0.0,
                "delta": 0.0,
                "nu1": "inf",
                "nu2": "inf",
            },
            "active_transformed_values": {
                "z_gamma": z_gamma_prior_mean,
                "log_tau_or_log_sigma": log_sigma_prior_center,
                "z_mu_or_log_beta_over_sigma_center": 0.0,
            },
            "finite_mean_derivation": {
                "gamma": "2 * 20 / (20 + 1.5) - 1",
                "sigma": (
                    "For sigma^2 ~ IG(alpha=1, scale=0.005), "
                    "E[sigma] = sqrt(0.005) * Gamma(1/2) / Gamma(1)"
                ),
                "third_coordinate": "E[log(beta) | sigma] = 0, hence E[log(beta)/sigma | sigma] = 0",
            },
            "nonfinite_mean_caveats": [
                "E[sigma^2] is infinite because the inverse-gamma shape is 1.",
                "The ordinary unconditional E[beta] is not used as the test point.",
                "This is not a posterior estimate from the S&P 500 returns.",
            ],
        },
        "target_identity": {
            "model_family": "zhao_cui_svmodels_generalized_stochastic_volatility",
            "state_dim": 1,
            "observation_dim": 1,
            "latent_state": (
                "x_t is the source svmodels latent volatility state used inside "
                "boxcoxinv(tau * x_t, delta)"
            ),
            "variance_transform": "v_t = boxcoxinv(tau * x_t, delta)",
            "transition_law": (
                "x_t = mu + gamma * (x_{t-1} - mu) "
                "+ phi * y_{t-1} / sqrt(v_{t-1}) + a * y_{t-1}^2 + eta_t"
            ),
            "transition_innovation": "eta_t follows Student-t(df=nu1); nu1=inf is a Gaussian-limit case",
            "initial_previous_observation": "y_0 = 0 in the source st_process/transition route",
            "observation_law": "y_t = sqrt(v_t) * epsilon_t, epsilon_t follows Student-t(df=nu2)",
            "likelihood_density": "tpdf(y_t / sqrt(v_t), nu2) / sqrt(v_t)",
            "boxcox_inverse": {
                "delta_zero": "boxcoxinv(z, 0) = exp(z)",
                "delta_nonzero": "boxcoxinv(z, delta) = (1 + delta * z)^(1 / delta)",
                "invalid_region": "source code returns NaN when the Box-Cox inverse is outside its domain",
            },
        },
        "parameter_contract": {
            "physical_parameter_order": [
                "gamma",
                "tau",
                "mu",
                "phi",
                "a",
                "delta",
                "nu1",
                "nu2",
            ],
            "active_estimated_indices_one_based": [1, 2, 3],
            "active_estimated_parameters": ["gamma", "tau", "mu"],
            "fixed_context_parameters": ["phi", "a", "delta", "nu1", "nu2"],
            "source_transform": {
                "gamma": "physical gamma = normcdf(z_gamma)",
                "tau": "physical tau = exp(z_tau)",
                "mu": "physical mu = z_mu * tau when mu is estimated",
                "phi": "physical phi = z_phi * tau when phi is estimated; fixed otherwise",
                "a": "physical a = z_a * tau when a is estimated; fixed otherwise",
                "delta": "physical delta = 4 * (normcdf(z_delta) - 0.5) when estimated",
                "nu": "physical nu = 5 * z_nu + 20 when estimated",
            },
            "author_code_defaults_not_estimates": {
                "gamma": 0.95,
                "tau_expression": "sqrt(3/64)",
                "tau_value": 0.21650635094610965,
                "mu": 0.0,
                "phi": 0.0,
                "a": 0.0,
                "delta": 0.0,
                "nu1": "inf",
                "nu2": "inf",
            },
        },
        "estimate_materialization_contract": {
            "current_status": "superseded_by_prior_mean_test_point",
            "accepted_routes": [
                "paper_sp500_prior_mean_convention_recorded_in_this_spec",
            ],
            "required_estimate_artifact_fields": [
                "test_point_route",
                "source_anchor",
                "statistic_used_as_truth",
                "physical_parameter_order",
                "physical_values",
                "transformed_active_values",
                "fixed_context_parameters",
                "mean_convention_and_nonfinite_mean_caveats",
                "SP500_input_role",
                "derivation_or_computation_procedure",
                "random_seeds_or_reason_not_applicable",
                "review_status",
            ],
            "allowed_statistics": [
                "finite_prior_center",
            ],
            "preferred_statistic": "finite_prior_center",
            "forbidden_substitutes": [
                "author_code_defaults_not_estimates",
                "BayesFilter_native_generalized_sv_fixture",
                "simple_SV_synthetic_truth_gamma_0p6_beta_0p4",
                "SP500_returns_as_benchmark_observations",
                "ordinary_mean_of_sigma_squared_or_beta_when_nonfinite",
            ],
        },
        "synthetic_generation_contract": {
            "benchmark_data_policy": "generate_synthetic_observations_from_sp500_prior_mean_test_point",
            "SP500_role": "source_estimation_input_only_not_benchmark_data",
            "core_horizon": 1008,
            "core_horizon_rationale": (
                "Match the Zhao-Cui SP500 estimation horizon unless the later "
                "benchmark-runner plan records a reviewed horizon-calibration exception."
            ),
            "seed_policy": (
                "multi-seed synthetic datasets; every dataset artifact records "
                "truth vector, fixed context, horizon, RNG seed, and simulator implementation"
            ),
            "admissible_pre_run_state": (
                "Synthetic data may be generated from the prior-mean test point "
                "only when the finite-mean convention and nonfinite-coordinate "
                "caveats are carried in the dataset artifact."
            ),
        },
        "benchmark_metrics_contract": {
            "primary_reported_quantities": [
                "log_likelihood_at_truth",
                "average_log_likelihood_at_truth_per_time",
                "score_norm_at_truth",
                "score_component_max_at_truth",
                "score_component_min_at_truth",
                "componentwise_score_at_truth",
            ],
            "replication_quantities": [
                "mean_across_datasets",
                "standard_error_across_datasets",
                "failure_rate",
                "nonfinite_rate",
                "runtime_summary",
            ],
            "curvature_quantities": [
                "Hessian_or_observed_information_when_available",
                "minimum_eigenvalue_status_when_available",
                "not_available_status_with_reason_when_not_available",
            ],
            "filter_policy": (
                "Attempt all benchmark filters where the adapter can express the "
                "target. UKF, SVD, CUT4, Zhao-Cui, and DPF rows may approximate "
                "non-Gaussian likelihoods. Kalman may appear only as a declared "
                "surrogate or structured not-applicable cell outside LGSSM."
            ),
        },
        "implementation_requirements": [
            "TensorFlow/TFP implementation for BayesFilter-owned generator and evaluator",
            "source-route transform parity tests for true2ftt/ftt2true semantics",
            "density tie-out tests against the source formulas on fixed probe points",
            "synthetic dataset manifest before benchmark execution",
            "score coordinate contract for active estimated parameters",
            "clear status for fixed context parameters in gradient tables",
        ],
        "nonclaims": [
            "not a numeric benchmark result",
            "not evidence that generalized-SV posterior estimated values have been extracted",
            "not permission to use author defaults as test truth",
            "not a direct SP500 benchmark-data row",
            "not a claim that sigma^2 or beta has a finite ordinary prior mean",
            "not a production generalized-SV readiness claim",
            "not a CUT4/Zhao-Cui/DPF correctness claim",
        ],
    }


def _write_markdown(path: Path, spec: dict[str, Any]) -> None:
    target = spec["target_identity"]
    estimate = spec["estimate_materialization_contract"]
    generation = spec["synthetic_generation_contract"]
    metrics = spec["benchmark_metrics_contract"]
    parameter = spec["parameter_contract"]
    source = spec["source_support_summary"]
    prior = spec["prior_mean_test_point"]
    lines = [
        "# Generalized SV Testing Specification",
        "",
        f"metadata_date: {spec['metadata_date']}",
        f"phase: {spec['phase']}",
        f"status: {spec['status']}",
        f"numeric_status: {spec['numeric_status']}",
        f"row_id: `{spec['row_id']}`",
        "",
        "## Decision",
        "",
        "Generalized SV remains in the promoted source-paper benchmark scope, but",
        "now as a synthetic row generated from the Zhao--Cui S&P 500 prior-center",
        "`svmodels` test point.  SP500 returns are source-estimation input only;",
        "they are not the benchmark observations for this row.",
        "",
        "The usable prior-center convention is finite-coordinate based: use",
        "`E[gamma]`, `E[sigma]`, and the zero center of `log(beta)/sigma`.",
        "`E[sigma^2]` and the ordinary unconditional `E[beta]` are not used.",
        "",
        "## Source Support",
        "",
        "| Field | Status |",
        "| --- | --- |",
        f"| Model route found | `{source['model_route_found']}` |",
        f"| Route name | `{source['route_name']}` |",
        f"| S&P prior found | `{source['sp500_prior_distribution_found']}` |",
        f"| Prior-mean test point materialized | `{source['prior_mean_test_point_materialized']}` |",
        f"| Numeric posterior estimated values found locally | `{source['local_numeric_posterior_estimated_values_found']}` |",
        f"| Author defaults | `{source['author_defaults_status']}` |",
        "",
        source["local_gap"],
        "",
        "## Prior-Center Test Point",
        "",
        f"Mean convention: {prior['mean_convention']}",
        "",
        "| Coordinate | Value |",
        "| --- | ---: |",
        f"| `E[(gamma+1)/2]` | `{prior['derived_values']['E_beta_unit_for_gamma']}` |",
        f"| `E[gamma]` | `{prior['derived_values']['E_gamma']}` |",
        f"| `E[sigma]` / source `tau` | `{prior['derived_values']['E_sigma']}` |",
        f"| `E[log(beta)]` center | `{prior['derived_values']['E_log_beta']}` |",
        f"| `z_gamma` | `{prior['active_transformed_values']['z_gamma']}` |",
        f"| `log_tau_or_log_sigma` | `{prior['active_transformed_values']['log_tau_or_log_sigma']}` |",
        "",
        "Caveats:",
        "",
        *[f"- {item}" for item in prior["nonfinite_mean_caveats"]],
        "",
        "## Target Equations",
        "",
        f"- State dimension: `{target['state_dim']}`",
        f"- Observation dimension: `{target['observation_dim']}`",
        f"- Variance transform: `{target['variance_transform']}`",
        f"- Transition: `{target['transition_law']}`",
        f"- Transition innovation: `{target['transition_innovation']}`",
        f"- Initial previous observation: `{target['initial_previous_observation']}`",
        f"- Observation law: `{target['observation_law']}`",
        f"- Likelihood density: `{target['likelihood_density']}`",
        "",
        "## Parameter Contract",
        "",
        "| Item | Value |",
        "| --- | --- |",
        f"| Physical order | `{parameter['physical_parameter_order']}` |",
        f"| Active estimated one-based indices | `{parameter['active_estimated_indices_one_based']}` |",
        f"| Active estimated parameters | `{parameter['active_estimated_parameters']}` |",
        f"| Fixed context parameters | `{parameter['fixed_context_parameters']}` |",
        "",
        "Author-code defaults are recorded only under",
        "`author_code_defaults_not_estimates` and must not be used as the truth",
        "vector for the amended benchmark.",
        "",
        "## Test-Point Materialization Gate",
        "",
        f"Current status: `{estimate['current_status']}`.",
        "",
        "Accepted routes:",
        "",
        *[f"- `{item}`" for item in estimate["accepted_routes"]],
        "",
        "Required fields in the test-point artifact:",
        "",
        *[f"- `{item}`" for item in estimate["required_estimate_artifact_fields"]],
        "",
        "Forbidden substitutes:",
        "",
        *[f"- `{item}`" for item in estimate["forbidden_substitutes"]],
        "",
        "## Synthetic Generation",
        "",
        f"- Policy: `{generation['benchmark_data_policy']}`",
        f"- SP500 role: `{generation['SP500_role']}`",
        f"- Core horizon: `{generation['core_horizon']}`",
        f"- Seed policy: `{generation['seed_policy']}`",
        f"- Pre-run state: `{generation['admissible_pre_run_state']}`",
        "",
        "## Benchmark Metrics",
        "",
        "Primary reported quantities:",
        "",
        *[f"- `{item}`" for item in metrics["primary_reported_quantities"]],
        "",
        "Replication quantities:",
        "",
        *[f"- `{item}`" for item in metrics["replication_quantities"]],
        "",
        "Curvature quantities:",
        "",
        *[f"- `{item}`" for item in metrics["curvature_quantities"]],
        "",
        f"Filter policy: {metrics['filter_policy']}",
        "",
        "## Nonclaims",
        "",
        *[f"- {item}" for item in spec["nonclaims"]],
        "",
        "Required tokens:",
        "",
        "```text",
        spec["status"],
        spec["numeric_status"],
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--output-markdown", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    spec = build_spec()
    args.output_json.write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    _write_markdown(args.output_markdown, spec)
    print(f"wrote {args.output_json}")
    print(f"wrote {args.output_markdown}")
    print(f"status {spec['status']}")
    print(f"numeric_status {spec['numeric_status']}")


if __name__ == "__main__":
    main()
