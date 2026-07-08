# Two-Lane Highdim Leaderboard Result

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`.

## Executed / status cells

| Row | Algorithm | Status | Score status | Avg loglik | Runtime s | MC SE | Reason |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | fixed_sgqf | executed_value_only | blocked_missing_analytical_route | -2.721519 | n/a | n/a | direct affine SGQF value route exists, but no reviewed source-scope SGQF score route is emitted |
| benchmark_lgssm_exact_oracle_m3_T50 | ukf | executed_value_score |  | -2.721519 | n/a | n/a |  |
| benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  | n/a | n/a | n/a | P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED |
| zhao_cui_sv_actual_nongaussian_T1000 | fixed_sgqf | blocked | blocked_not_same_target | n/a | n/a | n/a | blocked_not_same_target under current additive-state SGQF lane |
| zhao_cui_sv_actual_nongaussian_T1000 | ukf | executed_value_score |  | -1.460702 | 15.014870 | n/a |  |
| zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_scalar_or_multistate | executed_value_score |  | -0.715097 | 17.155709 | n/a |  |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | fixed_sgqf | executed_value_only | diagnostic_score_only | -2.284632 | n/a | n/a | existing SGQF score evidence is tiny-fixture-only and not yet promoted to source-scope analytical-score admission |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | ukf | executed_value_score |  | -2.284632 | 38.668817 | n/a |  |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_scalar_or_multistate | executed_value_score |  | -2.015085 | 22.661457 | n/a |  |
| zhao_cui_spatial_sir_austria_j9_T20 | fixed_sgqf | blocked | blocked_no_free_theta | n/a | n/a | n/a | no reviewed SGQF source-scope spatial SIR route is wired |
| zhao_cui_spatial_sir_austria_j9_T20 | ukf | executed_value_only |  | -36.832007 | 0.684872 | n/a |  |
| zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  | n/a | n/a | n/a | P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED |
| zhao_cui_predator_prey_T20 | fixed_sgqf | executed_value_only | analytical_score_admitted | -3.255563 | n/a | n/a | family tests provide explicit analytical derivatives plus same-branch finite-difference validation |
| zhao_cui_predator_prey_T20 | ukf | executed_value_score |  | -8.568276 | 5.479427 | n/a |  |
| zhao_cui_predator_prey_T20 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  | n/a | n/a | n/a | P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | fixed_sgqf | blocked | blocked_missing_analytical_route | n/a | n/a | n/a | no reviewed SGQF source-scope generalized-SV evaluator is wired |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ukf | executed_value_score |  | -1.428934 | 15.095921 | n/a |  |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | zhao_cui_scalar_or_multistate | blocked_or_status_only |  | n/a | n/a | n/a | P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED |

## Row readiness summary

| Row | Executed algorithms | Full three-way ready | Blocked / missing algorithms |
| --- | --- | --- | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | fixed_sgqf, ukf | False | zhao_cui_scalar_or_multistate |
| zhao_cui_sv_actual_nongaussian_T1000 | ukf, zhao_cui_scalar_or_multistate | False | fixed_sgqf |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | fixed_sgqf, ukf, zhao_cui_scalar_or_multistate | True | none |
| zhao_cui_spatial_sir_austria_j9_T20 | ukf | False | fixed_sgqf, zhao_cui_scalar_or_multistate |
| zhao_cui_predator_prey_T20 | fixed_sgqf, ukf | False | zhao_cui_scalar_or_multistate |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ukf | False | fixed_sgqf, zhao_cui_scalar_or_multistate |

## Nonclaims

- This highdim packet combines the reviewed P8d numeric artifact with direct SGQF row routes where already supported in code/tests.
- CUT4 is excluded from the highdim lane by contract.
- Actual transformed SV and KSC surrogate SV remain separate rows and must not be merged.
- Rows with blocked or missing algorithms are not full three-way leaderboard rows.
- This is not a production-GPU timing packet.
