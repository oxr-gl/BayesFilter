# P8d Numeric Benchmark Execution Summary

status: `PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS`
numeric_benchmark_status: `partial_numeric_execution_remaining_adapter_and_callback_gaps`

## Value Table

| algorithm | benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_predator_prey_T20 | zhao_cui_generalized_sv_synthetic_from_estimated_values |
| --- | --- | --- | --- | --- | --- | --- |
| kalman_exact_or_mixture_enumeration | -2.721519497 | structured_not_applicable | -2.284632147 | structured_not_applicable | structured_not_applicable | structured_not_applicable |
| ukf | -2.721519497 | -1.46070219 | -2.284632147 | -36.83200742 | -8.568275874 | -1.428934153 |
| svd_sigma_point | -2.721519497 | -1.46070219 | -2.284632147 | -36.83714962 | -8.568349354 | -1.428934153 |
| cut4 | -2.721519497 | -1.041683033 | -2.284632147 | blocked_p8d_deterministic_smoke_failed | -8.568434667 | -1.42886464 |
| zhao_cui_scalar_or_multistate | blocked_model_specific_evaluator_adapter_required | -0.7150968569 | -2.015085166 | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required |
| bootstrap_dpf_current | -2.981235945 | -0.7993231692 | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | -13.65697934 | -1.430300626 |
| ledh_pfpf_alg1_ukf_current | -2.777627635 | blocked_dpf_five_seed_execution_failed | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | -9.152450072 | blocked_dpf_five_seed_execution_failed |

## Score Norm Table

| algorithm | benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_predator_prey_T20 | zhao_cui_generalized_sv_synthetic_from_estimated_values |
| --- | --- | --- | --- | --- | --- | --- |
| kalman_exact_or_mixture_enumeration | 8.331768521 | not_applicable_outside_lgssm_or_declared_mixture_surrogate | 5.436270495 | not_applicable_outside_lgssm_or_declared_mixture_surrogate | not_applicable_outside_lgssm_or_declared_mixture_surrogate | not_applicable_outside_lgssm_or_declared_mixture_surrogate |
| ukf | 8.331768521 | 1916.10876 | 5.436270495 | not_applicable_no_free_theta | 270.1187755 | 1.26278726 |
| svd_sigma_point | 8.331768521 | 1916.10876 | 5.436270495 | not_applicable_no_free_theta | 270.1276808 | 1.26278726 |
| cut4 | 8.331768521 | 141.231528 | 5.436270495 | not_applicable_no_free_theta | 270.1325979 | 0.7957695824 |
| zhao_cui_scalar_or_multistate | blocked_model_specific_score_evaluator_adapter_required | 6.218900604 | 679.86814 | not_applicable_no_free_theta | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required |
| bootstrap_dpf_current | not_certified_for_main_score_without_mc_and_fixed_branch_review | not_certified_for_main_score_without_mc_and_fixed_branch_review | blocked_model_specific_dpf_callbacks_before_score_review | not_applicable_no_free_theta | not_certified_for_main_score_without_mc_and_fixed_branch_review | not_certified_for_main_score_without_mc_and_fixed_branch_review |
| ledh_pfpf_alg1_ukf_current | not_certified_for_main_score_without_mc_and_fixed_branch_review | not_certified_for_main_score_without_mc_and_fixed_branch_review | blocked_model_specific_dpf_callbacks_before_score_review | not_applicable_no_free_theta | not_certified_for_main_score_without_mc_and_fixed_branch_review | not_certified_for_main_score_without_mc_and_fixed_branch_review |

## Tokens

```text
PARTIAL_P8D_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS
partial_numeric_execution_remaining_adapter_and_callback_gaps
```

## Nonclaims

- partial numeric artifact, not full Phase 8 completion
- not a filter ranking
- not Bayesian-estimation readiness
- not DPF gradient certification
- old LEDH-PFPF-OT evidence is not current evidence
