# Two-Lane Highdim LEDH-Inclusive Leaderboard Dry Run

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-dry-run-2026-07-03.json`.

Comparator mode: `frozen_non_ledh_baseline_plus_fresh_ledh`.

Runtime cross-ranking allowed: `False`.

## Rows

| Row | Algorithm | Status | Value status | Score status | Runtime rankable | Avg loglik | MC SE | Reason |
| --- | --- | --- | --- | --- | --- | ---: | ---: | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | fixed_sgqf | executed_value_score |  | analytical_score_emitted | False | -2.72152 |  | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| benchmark_lgssm_exact_oracle_m3_T50 | ukf | executed_value_score |  |  | False | -2.72152 |  |  |
| benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_scalar_or_multistate | executed_value_score |  |  | False | -2.72152 |  |  |
| benchmark_lgssm_exact_oracle_m3_T50 | ledh_pfpf_ot | dry_run_value_candidate | candidate_value_arm_requires_phase2_runner_wiring_and_phase3_value_gate | blocked_score_until_phase3_kalman_oracle_or_same_target_fd_gate | False |  |  | value_status=candidate_value_arm_requires_phase2_runner_wiring_and_phase3_value_gate; score_status=blocked_score_until_phase3_kalman_oracle_or_same_target_fd_gate |
| zhao_cui_sv_actual_nongaussian_T1000 | fixed_sgqf | executed_value_score |  | analytical_score_emitted | False | -2.30091 |  | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| zhao_cui_sv_actual_nongaussian_T1000 | ukf | executed_value_score |  | analytical_score_emitted | False | -1.4607 |  | actual-SV raw augmented-noise Gaussian-closure score emitted by reviewed factor-propagating SR-UKF manual route |
| zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_scalar_or_multistate | executed_value_score |  | analytical_score_emitted | False | -2.28623 |  | Zhao-Cui exact-transformed SV score emitted by scalar fixed-branch TT manual parameter-score adapter |
| zhao_cui_sv_actual_nongaussian_T1000 | ledh_pfpf_ot | blocked | blocked_no_reviewed_current_gpu_xla_ledh_row_adapter | blocked_score | False |  |  | No reviewed current LEDH-inclusive leaderboard adapter proves that the GPU/XLA TF32 route computes the exact requested actual-SV row target.; value_status=blocked_no_reviewed_current_gpu_xla_ledh_row_adapter; score_status=blocked_score |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | fixed_sgqf | executed_value_score |  | analytical_score_emitted | False | -2.28463 |  | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | ukf | executed_value_score |  | analytical_score_emitted | False | -2.28463 |  | UKF score vector emitted by reviewed principal-square-root analytical component score path |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_scalar_or_multistate | executed_value_score |  | analytical_score_emitted | False | -2.28443 |  | Zhao-Cui KSC transformed-mixture score emitted by scalar fixed-branch TT manual parameter-score adapter |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | ledh_pfpf_ot | blocked | blocked_no_ledh_ksc_row_adapter | blocked_score | False |  |  | No reviewed LEDH adapter exists for the KSC transformed-mixture row target.; value_status=blocked_no_ledh_ksc_row_adapter; score_status=blocked_score |
| zhao_cui_spatial_sir_austria_j9_T20 | fixed_sgqf | blocked |  | blocked_no_free_theta | False |  |  | no reviewed SGQF source-scope spatial SIR route is wired |
| zhao_cui_spatial_sir_austria_j9_T20 | ukf | executed_value_only |  |  | False | -36.832 |  |  |
| zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  |  | False |  |  | P91 closes the scoped local complete-data SIR d18 component route, but the full observed-data/filtering leaderboard evaluator remains blocked by preserved source-route derivative/evaluator gaps. |
| zhao_cui_spatial_sir_austria_j9_T20 | ledh_pfpf_ot | dry_run_value_candidate | candidate_value_arm_existing_p8j_p8o_streaming_gpu_tf32_requires_phase4_ladder_or_explicit_carry_forward | blocked_score_for_full_leaderboard_row | False |  |  | value_status=candidate_value_arm_existing_p8j_p8o_streaming_gpu_tf32_requires_phase4_ladder_or_explicit_carry_forward; score_status=blocked_score_for_full_leaderboard_row |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | fixed_sgqf | blocked |  | not_applicable_to_scoped_component_row | False |  |  | fixed_sgqf is not admitted for the scoped Zhao-Cui parameterized SIR local complete-data component row; the scoped row is a fixed-variant Zhao-Cui manual-score component cell. |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | ukf | blocked |  | not_applicable_to_scoped_component_row | False |  |  | ukf is not admitted for the scoped Zhao-Cui parameterized SIR local complete-data component row; the scoped row is a fixed-variant Zhao-Cui manual-score component cell. |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | zhao_cui_scalar_or_multistate | executed_value_score |  | analytical_score_emitted | False | -60.4464 |  | Zhao-Cui parameterized SIR T20 local complete-data score emitted by manual parameter-score methods |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | ledh_pfpf_ot | scoped_component_status_only | scoped_or_diagnostic_only | scoped_score_diagnostic_not_full_observed_data_score | False |  |  | The parameterized SIR row is not a full observed-data/filtering row in the current baseline.; value_status=scoped_or_diagnostic_only; score_status=scoped_score_diagnostic_not_full_observed_data_score |
| zhao_cui_predator_prey_T20 | fixed_sgqf | blocked |  | blocked_target_alignment | False |  |  | blocked_target_alignment: no reviewed fixed-SGQF evaluator is wired for the source-scope T20 predator-prey observations; the available P47 two-observation lower-rung value is diagnostic-only and is not reported as this T20 row |
| zhao_cui_predator_prey_T20 | ukf | executed_value_only |  | blocked_autodiff_not_admitted | False | -8.56828 |  | autodiff score provenance is diagnostic only; analytical gradient accuracy is the leaderboard benchmark |
| zhao_cui_predator_prey_T20 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  |  | False |  |  | P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED |
| zhao_cui_predator_prey_T20 | ledh_pfpf_ot | blocked | blocked_no_reviewed_current_gpu_xla_ledh_row_adapter | blocked_score | False |  |  | No reviewed current LEDH-inclusive runner adapter proves same-target predator-prey T20 execution on the GPU/XLA TF32 route.; value_status=blocked_no_reviewed_current_gpu_xla_ledh_row_adapter; score_status=blocked_score |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | fixed_sgqf | blocked |  | blocked_exact_source_row_evaluator_missing | False |  |  | blocked_source_row_evaluator_missing: no reviewed fixed-SGQF exact-row evaluator is wired for zhao_cui_generalized_sv_synthetic_from_estimated_values; native-oracle, precursor, auxiliary, actual-SV, and KSC evidence are not source-row admission evidence |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ukf | executed_value_only |  | blocked_autodiff_not_admitted | False | -1.42893 |  | autodiff score provenance is diagnostic only; analytical gradient accuracy is the leaderboard benchmark |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | zhao_cui_scalar_or_multistate | blocked_or_status_only |  |  | False |  |  | blocked_source_row_evaluator_missing: no reviewed Zhao-Cui exact-row evaluator is wired for zhao_cui_generalized_sv_synthetic_from_estimated_values; native-oracle, precursor, auxiliary, actual-SV, and KSC evidence are not source-row admission evidence. |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ledh_pfpf_ot | blocked | blocked_no_reviewed_same_target_ledh_row_adapter | blocked_score | False |  |  | No reviewed LEDH adapter proves the requested generalized-SV source-row target.; value_status=blocked_no_reviewed_same_target_ledh_row_adapter; score_status=blocked_score |

## Row Summary

| Row | LEDH status | LEDH value status | LEDH score status | Full four-way ready |
| --- | --- | --- | --- | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | dry_run_value_candidate | candidate_value_arm_requires_phase2_runner_wiring_and_phase3_value_gate | blocked_score_until_phase3_kalman_oracle_or_same_target_fd_gate | False |
| zhao_cui_sv_actual_nongaussian_T1000 | blocked | blocked_no_reviewed_current_gpu_xla_ledh_row_adapter | blocked_score | False |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | blocked | blocked_no_ledh_ksc_row_adapter | blocked_score | False |
| zhao_cui_spatial_sir_austria_j9_T20 | dry_run_value_candidate | candidate_value_arm_existing_p8j_p8o_streaming_gpu_tf32_requires_phase4_ladder_or_explicit_carry_forward | blocked_score_for_full_leaderboard_row | False |
| zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale | scoped_component_status_only | scoped_or_diagnostic_only | scoped_score_diagnostic_not_full_observed_data_score | False |
| zhao_cui_predator_prey_T20 | blocked | blocked_no_reviewed_current_gpu_xla_ledh_row_adapter | blocked_score | False |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | blocked | blocked_no_reviewed_same_target_ledh_row_adapter | blocked_score | False |

## Nonclaims

- This is a Phase 2 schema dry-run artifact.
- No LEDH value was executed by this artifact.
- No LEDH score was executed by this artifact.
- Frozen non-LEDH rows are not rerun under the LEDH GPU/XLA harness.
- Runtime cross-ranking between frozen non-LEDH rows and LEDH rows is forbidden.
- Rows marked blocked or scoped are not full LEDH observed-data filtering admissions.
- HMC readiness, posterior correctness, and scientific superiority are not claimed.
