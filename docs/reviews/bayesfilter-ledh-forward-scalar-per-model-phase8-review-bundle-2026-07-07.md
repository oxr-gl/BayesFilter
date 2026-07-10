# Phase 8 Value-Only Integration Read-Only Review Bundle

metadata_date: 2026-07-07
review_scope: `bounded_phase8_result`

## Role Contract

Claude is read-only reviewer only.

Do not edit files, run experiments, launch agents, approve policy boundaries,
or change state.

Codex remains supervisor and executor.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```

## Objective

Review whether Phase 8 safely closes the forward-scalar value-only runbook by
integrating six admitted LEDH forward-scalar artifacts.

Target scalar: `observed_data_log_likelihood_estimator`.

Reported tensor field: `log_likelihood`.

Scores are out of scope.

## Fixed Paths To Review

- `docs/plans/bayesfilter-ledh-forward-scalar-per-model-phase8-integration-result-2026-07-07.md`
- `docs/plans/bayesfilter-ledh-forward-scalar-value-integration-results-2026-07-07.json`
- `docs/benchmarks/benchmark_ledh_forward_scalar_value_integration.py`
- `tests/highdim/test_ledh_phase8_value_integration_artifact.py`

Do not review the whole repo.

## Phase 8 Summary

Phase 8 wrote:

- `docs/plans/bayesfilter-ledh-forward-scalar-value-integration-results-2026-07-07.json`
- `docs/plans/bayesfilter-ledh-forward-scalar-value-integration-results-2026-07-07.md`

Top-level artifact fields:

- `schema_version =
  bayesfilter.highdim.ledh_forward_scalar_value_integration.v1`;
- `main_row_count = 6`;
- `score_integration_status = blocked_out_of_scope_forward_scalar_only`;
- `runtime_cross_ranking_allowed = false`;
- `all_algorithm_comparison_allowed = false`.

Rows:

| Row | Mean Log Likelihood | MCSE | Target Policy |
| --- | ---: | ---: | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `-135.96007385253907` | `0.005933406369186942` | `lgssm_gaussian_observation_density` |
| `zhao_cui_spatial_sir_austria_j9_T20` | `-902.8301513671875` | `0.20822211173623006` | `fixed_sir_infectious_components_gaussian_observation_density` |
| `zhao_cui_predator_prey_T20` | `-169.8675048828125` | `0.4235013715066106` | `additive_gaussian_predator_prey` |
| `zhao_cui_sv_actual_nongaussian_T1000` | `-2289.953466796875` | `0.15099991276087987` | `transformed_actual_sv_log_y_square` |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `-1438.9241943359375` | `0.02997747151555195` | `source_route_prior_mean_generalized_sv` |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `-2287.953759765625` | `0.1402306133817723` | `ksc_log_chi_square_gaussian_mixture_surrogate` |

KSC boundary:

- `target_family = ksc_finite_gaussian_mixture_surrogate`;
- `target_observation_density =
  finite_ksc_log_chi_square_gaussian_mixture_log_density`;
- `transform_offset = 1e-8`;
- `ksc_mixture_is_target_likelihood = true`;
- `actual_sv_exact_log_chi_square_target_used = false`.

Diagnostic SIR row:

- `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` is recorded as
  `excluded_from_main_value_leaderboard`.

## Local Checks Passed

Compile:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m py_compile \
  docs/benchmarks/benchmark_ledh_forward_scalar_value_integration.py \
  tests/highdim/test_ledh_phase8_value_integration_artifact.py
```

Focused replay:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase8_value_integration_artifact.py -q
```

Result: `3 passed, 2 warnings`.

Through-Phase-8 replay:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m pytest \
  tests/highdim/test_ledh_phase3_forward_admission.py \
  tests/highdim/test_ledh_forward_contract_phase2.py \
  tests/highdim/test_ledh_forward_scalar_admission_guard.py \
  tests/highdim/test_ledh_phase2_lgssm_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase3_fixed_sir_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase4_predator_prey_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase5_actual_sv_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase6_generalized_sv_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_tiny_artifact.py \
  tests/highdim/test_ledh_phase7_ksc_sv_forward_scalar_artifact.py \
  tests/highdim/test_ledh_phase8_value_integration_artifact.py -q
```

Result: `48 passed, 2 warnings`.

## Review Questions

1. Does the integration builder read only admitted Phase 2-7 forward-scalar
   artifacts and validate them with the Phase 1 schema?
2. Does the integration artifact block score integration and avoid score
   fields/admitted score statuses?
3. Does it avoid old score artifacts and avoid reusing the score-inclusive
   builder as the integration route?
4. Does it preserve row target-policy labels, especially KSC as a finite
   Gaussian-mixture surrogate target rather than exact native actual-SV?
5. Does it exclude the parameterized SIR diagnostic row from main rows?
6. Does it keep runtime and all-algorithm comparison claims out of scope?

## Pass Criteria

Return `VERDICT: AGREE` only if:

- Phase 8 local integration is internally consistent with the cited files and
  checks;
- the artifact is value-only and boundary-safe;
- no score/all-algorithm/runtime-ranking/diagnostic-row promotion creep is
  found; and
- no fixable blocker remains.

Return `VERDICT: REVISE` if any material issue remains.
