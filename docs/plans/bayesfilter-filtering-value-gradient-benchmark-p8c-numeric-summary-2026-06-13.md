# P8c Numeric Benchmark Execution Summary

status: `PARTIAL_P8C_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS`
numeric_benchmark_status: `partial_numeric_execution_remaining_adapter_and_callback_gaps`

## Value Table

| algorithm | benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_predator_prey_T20 | zhao_cui_generalized_sv_synthetic_from_estimated_values |
| --- | --- | --- | --- | --- | --- | --- |
| kalman_exact_or_mixture_enumeration | -2.721519497 | structured_not_applicable | -2.284632147 | structured_not_applicable | structured_not_applicable | structured_not_applicable |
| ukf | -2.721519497 | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required |
| svd_sigma_point | -2.721519497 | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required |
| cut4 | -2.721519497 | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required |
| zhao_cui_scalar_or_multistate | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required | blocked_model_specific_evaluator_adapter_required |
| bootstrap_dpf_current | -2.981235945 | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks |
| ledh_pfpf_alg1_ukf_current | -2.777627635 | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks | blocked_pending_model_specific_dpf_callbacks |

## Score Norm Table

| algorithm | benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_predator_prey_T20 | zhao_cui_generalized_sv_synthetic_from_estimated_values |
| --- | --- | --- | --- | --- | --- | --- |
| kalman_exact_or_mixture_enumeration | 8.331768521 | not_applicable_outside_lgssm_or_declared_mixture_surrogate | not_executed_value_only_ksc_mixture_score_adapter | not_applicable_outside_lgssm_or_declared_mixture_surrogate | not_applicable_outside_lgssm_or_declared_mixture_surrogate | not_applicable_outside_lgssm_or_declared_mixture_surrogate |
| ukf | 8.331768521 | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required | not_applicable_no_free_theta | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required |
| svd_sigma_point | 8.331768521 | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required | not_applicable_no_free_theta | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required |
| cut4 | 8.331768521 | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required | not_applicable_no_free_theta | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required |
| zhao_cui_scalar_or_multistate | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required | not_applicable_no_free_theta | blocked_model_specific_score_evaluator_adapter_required | blocked_model_specific_score_evaluator_adapter_required |
| bootstrap_dpf_current | not_certified_for_main_score_without_mc_and_fixed_branch_review | blocked_model_specific_dpf_callbacks_before_score_review | blocked_model_specific_dpf_callbacks_before_score_review | not_applicable_no_free_theta | blocked_model_specific_dpf_callbacks_before_score_review | blocked_model_specific_dpf_callbacks_before_score_review |
| ledh_pfpf_alg1_ukf_current | not_certified_for_main_score_without_mc_and_fixed_branch_review | blocked_model_specific_dpf_callbacks_before_score_review | blocked_model_specific_dpf_callbacks_before_score_review | not_applicable_no_free_theta | blocked_model_specific_dpf_callbacks_before_score_review | blocked_model_specific_dpf_callbacks_before_score_review |

## Tokens

```text
PARTIAL_P8C_NUMERIC_BENCHMARK_RUNNER_WITH_EXPLICIT_REMAINING_GAPS
partial_numeric_execution_remaining_adapter_and_callback_gaps
```

## Nonclaims

- partial numeric artifact, not full Phase 8 completion
- not a filter ranking
- not Bayesian-estimation readiness
- not DPF gradient certification
- old LEDH-PFPF-OT evidence is not current evidence
