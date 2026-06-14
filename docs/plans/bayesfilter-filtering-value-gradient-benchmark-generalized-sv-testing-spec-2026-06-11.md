# Generalized SV Testing Specification

metadata_date: 2026-06-12
phase: FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC
status: PASS_FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC_CONTRACT
numeric_status: PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING
row_id: `zhao_cui_generalized_sv_synthetic_from_estimated_values`

## Decision

Generalized SV remains in the promoted source-paper benchmark scope, but
now as a synthetic row generated from the Zhao--Cui S&P 500 prior-center
`svmodels` test point.  SP500 returns are source-estimation input only;
they are not the benchmark observations for this row.

The usable prior-center convention is finite-coordinate based: use
`E[gamma]`, `E[sigma]`, and the zero center of `log(beta)/sigma`.
`E[sigma^2]` and the ordinary unconditional `E[beta]` are not used.

## Source Support

| Field | Status |
| --- | --- |
| Model route found | `True` |
| Route name | `svmodels` |
| S&P prior found | `True` |
| Prior-mean test point materialized | `True` |
| Numeric posterior estimated values found locally | `False` |
| Author defaults | `configuration_defaults_not_test_truth` |

The local paper text and author mirror expose the svmodels route and S&P 500 prior distribution. The benchmark now uses the finite prior-center convention below rather than waiting for a posterior estimate table.

## Prior-Center Test Point

Mean convention: Use finite prior centers in the source-route testing coordinates: E[(gamma+1)/2], E[sigma], and E[log(beta)/sigma]=0. Do not claim that every original physical coordinate has a finite ordinary mean.

| Coordinate | Value |
| --- | ---: |
| `E[(gamma+1)/2]` | `0.9302325581395349` |
| `E[gamma]` | `0.8604651162790697` |
| `E[sigma]` / source `tau` | `0.12533141373155002` |
| `E[log(beta)]` center | `0.0` |
| `z_gamma` | `1.0824113944610982` |
| `log_tau_or_log_sigma` | `-2.076793740349318` |

Caveats:

- E[sigma^2] is infinite because the inverse-gamma shape is 1.
- The ordinary unconditional E[beta] is not used as the test point.
- This is not a posterior estimate from the S&P 500 returns.

## Target Equations

- State dimension: `1`
- Observation dimension: `1`
- Variance transform: `v_t = boxcoxinv(tau * x_t, delta)`
- Transition: `x_t = mu + gamma * (x_{t-1} - mu) + phi * y_{t-1} / sqrt(v_{t-1}) + a * y_{t-1}^2 + eta_t`
- Transition innovation: `eta_t follows Student-t(df=nu1); nu1=inf is a Gaussian-limit case`
- Initial previous observation: `y_0 = 0 in the source st_process/transition route`
- Observation law: `y_t = sqrt(v_t) * epsilon_t, epsilon_t follows Student-t(df=nu2)`
- Likelihood density: `tpdf(y_t / sqrt(v_t), nu2) / sqrt(v_t)`

## Parameter Contract

| Item | Value |
| --- | --- |
| Physical order | `['gamma', 'tau', 'mu', 'phi', 'a', 'delta', 'nu1', 'nu2']` |
| Active estimated one-based indices | `[1, 2, 3]` |
| Active estimated parameters | `['gamma', 'tau', 'mu']` |
| Fixed context parameters | `['phi', 'a', 'delta', 'nu1', 'nu2']` |

Author-code defaults are recorded only under
`author_code_defaults_not_estimates` and must not be used as the truth
vector for the amended benchmark.

## Test-Point Materialization Gate

Current status: `superseded_by_prior_mean_test_point`.

Accepted routes:

- `paper_sp500_prior_mean_convention_recorded_in_this_spec`

Required fields in the test-point artifact:

- `test_point_route`
- `source_anchor`
- `statistic_used_as_truth`
- `physical_parameter_order`
- `physical_values`
- `transformed_active_values`
- `fixed_context_parameters`
- `mean_convention_and_nonfinite_mean_caveats`
- `SP500_input_role`
- `derivation_or_computation_procedure`
- `random_seeds_or_reason_not_applicable`
- `review_status`

Forbidden substitutes:

- `author_code_defaults_not_estimates`
- `BayesFilter_native_generalized_sv_fixture`
- `simple_SV_synthetic_truth_gamma_0p6_beta_0p4`
- `SP500_returns_as_benchmark_observations`
- `ordinary_mean_of_sigma_squared_or_beta_when_nonfinite`

## Synthetic Generation

- Policy: `generate_synthetic_observations_from_sp500_prior_mean_test_point`
- SP500 role: `source_estimation_input_only_not_benchmark_data`
- Core horizon: `1008`
- Seed policy: `multi-seed synthetic datasets; every dataset artifact records truth vector, fixed context, horizon, RNG seed, and simulator implementation`
- Pre-run state: `Synthetic data may be generated from the prior-mean test point only when the finite-mean convention and nonfinite-coordinate caveats are carried in the dataset artifact.`

## Benchmark Metrics

Primary reported quantities:

- `log_likelihood_at_truth`
- `average_log_likelihood_at_truth_per_time`
- `score_norm_at_truth`
- `score_component_max_at_truth`
- `score_component_min_at_truth`
- `componentwise_score_at_truth`

Replication quantities:

- `mean_across_datasets`
- `standard_error_across_datasets`
- `failure_rate`
- `nonfinite_rate`
- `runtime_summary`

Curvature quantities:

- `Hessian_or_observed_information_when_available`
- `minimum_eigenvalue_status_when_available`
- `not_available_status_with_reason_when_not_available`

Filter policy: Attempt all benchmark filters where the adapter can express the target. UKF, SVD, CUT4, Zhao-Cui, and DPF rows may approximate non-Gaussian likelihoods. Kalman may appear only as a declared surrogate or structured not-applicable cell outside LGSSM.

## Nonclaims

- not a numeric benchmark result
- not evidence that generalized-SV posterior estimated values have been extracted
- not permission to use author defaults as test truth
- not a direct SP500 benchmark-data row
- not a claim that sigma^2 or beta has a finite ordinary prior mean
- not a production generalized-SV readiness claim
- not a CUT4/Zhao-Cui/DPF correctness claim

Required tokens:

```text
PASS_FILTER_BENCH_GENERALIZED_SV_TESTING_SPEC_CONTRACT
PASS_GENERALIZED_SV_PRIOR_MEAN_TEST_CASE_READY_NUMERIC_EVALUATOR_PENDING
```
