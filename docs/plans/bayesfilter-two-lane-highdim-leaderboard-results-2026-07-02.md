# Two-Lane Highdim Leaderboard Result

Authoritative JSON artifact: `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-02.json`.

## Executed / status cells

| Row | Algorithm | Status | Score status | Batch status | GPU/XLA status | Timing rank status | Avg loglik | Runtime s | MC SE | Reason |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | fixed_sgqf | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.721519 | n/a | n/a | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| benchmark_lgssm_exact_oracle_m3_T50 | ukf | executed_value_score |  | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.721519 | n/a | n/a |  |
| benchmark_lgssm_exact_oracle_m3_T50 | zhao_cui_scalar_or_multistate | executed_value_score |  | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.721519 | n/a | n/a |  |
| zhao_cui_sv_actual_nongaussian_T1000 | fixed_sgqf | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.300911 | n/a | n/a | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| zhao_cui_sv_actual_nongaussian_T1000 | ukf | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -1.460702 | 12.228001 | n/a | actual-SV raw augmented-noise Gaussian-closure score emitted by reviewed factor-propagating SR-UKF manual route |
| zhao_cui_sv_actual_nongaussian_T1000 | zhao_cui_scalar_or_multistate | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.286226 | 754.433487 | n/a | Zhao-Cui exact-transformed SV score emitted by scalar fixed-branch TT manual parameter-score adapter |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | fixed_sgqf | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.284632 | n/a | n/a | SGQF score vector emitted by reviewed analytical fixed-branch score path |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | ukf | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.284632 | 105.305492 | n/a | UKF score vector emitted by reviewed principal-square-root analytical component score path |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | zhao_cui_scalar_or_multistate | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -2.284431 | 784.640633 | n/a | Zhao-Cui KSC transformed-mixture score emitted by scalar fixed-branch TT manual parameter-score adapter |
| zhao_cui_spatial_sir_austria_j9_T20 | fixed_sgqf | blocked | blocked_no_free_theta | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | n/a | n/a | n/a | no reviewed SGQF source-scope spatial SIR route is wired |
| zhao_cui_spatial_sir_austria_j9_T20 | ukf | executed_value_only |  | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | -36.832007 | 0.684872 | n/a |  |
| zhao_cui_spatial_sir_austria_j9_T20 | zhao_cui_scalar_or_multistate | blocked_or_status_only |  | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | n/a | n/a | n/a | P91 closes the scoped local complete-data SIR d18 component route, but the full observed-data/filtering leaderboard evaluator remains blocked by preserved source-route derivative/evaluator gaps. |
| zhao_cui_predator_prey_T20 | fixed_sgqf | blocked | blocked_target_alignment | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | n/a | n/a | n/a | blocked_target_alignment: no reviewed fixed-SGQF evaluator is wired for the source-scope T20 predator-prey observations; the available P47 two-observation lower-rung value is diagnostic-only and is not reported as this T20 row |
| zhao_cui_predator_prey_T20 | ukf | executed_value_only | blocked_autodiff_not_admitted | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | -8.568276 | 5.479427 | n/a | autodiff score provenance is diagnostic only; analytical gradient accuracy is the leaderboard benchmark |
| zhao_cui_predator_prey_T20 | zhao_cui_scalar_or_multistate | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -8.996197 | 64.602121 | n/a | Zhao-Cui predator-prey T20 score emitted by multistate fixed-design TT manual parameter-score adapter |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | fixed_sgqf | blocked | blocked_exact_source_row_evaluator_missing | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | n/a | n/a | n/a | blocked_source_row_evaluator_missing: no reviewed fixed-SGQF exact-row evaluator is wired for zhao_cui_generalized_sv_synthetic_from_estimated_values; native-oracle, precursor, auxiliary, actual-SV, and KSC evidence are not source-row admission evidence |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ukf | executed_value_only | blocked_autodiff_not_admitted | not_applicable_until_value_score_row_exists | not_applicable_until_value_score_row_exists | not_rankable_correctness_gate_open | -1.428934 | 15.095921 | n/a | autodiff score provenance is diagnostic only; analytical gradient accuracy is the leaderboard benchmark |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | zhao_cui_scalar_or_multistate | executed_value_score | analytical_score_emitted | not_claimed_no_reviewed_batched_main_row_evaluator | not_claimed_no_trusted_row_specific_gpu_xla_manifest | not_ranked_by_phase7_timing | -1.426624 | 480.188744 | n/a | Zhao-Cui generalized-SV prior-mean source row score emitted by scalar fixed-design TT manual parameter-score adapter |

## Row readiness summary

| Row | Executed algorithms | Full three-way ready | Blocked / missing algorithms |
| --- | --- | --- | --- |
| benchmark_lgssm_exact_oracle_m3_T50 | fixed_sgqf, ukf, zhao_cui_scalar_or_multistate | True | none |
| zhao_cui_sv_actual_nongaussian_T1000 | fixed_sgqf, ukf, zhao_cui_scalar_or_multistate | True | none |
| zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000 | fixed_sgqf, ukf, zhao_cui_scalar_or_multistate | True | none |
| zhao_cui_spatial_sir_austria_j9_T20 | ukf | False | fixed_sgqf, zhao_cui_scalar_or_multistate |
| zhao_cui_predator_prey_T20 | ukf, zhao_cui_scalar_or_multistate | False | fixed_sgqf |
| zhao_cui_generalized_sv_synthetic_from_estimated_values | ukf, zhao_cui_scalar_or_multistate | False | fixed_sgqf |

## Nonclaims

- This highdim packet combines the reviewed P8d numeric artifact with direct SGQF row routes where already supported in code/tests.
- CUT4 is excluded from the highdim lane by contract.
- LEDH/PFPF-OT and DPF transport rows are omitted from this non-LEDH rebuild.
- P91 Zhao-Cui SIR d18 evidence is included only as scoped local complete-data component evidence, not as full observed-data/filtering leaderboard execution.
- Actual transformed SV and KSC surrogate SV remain separate rows and must not be merged.
- Rows with blocked or missing algorithms are not full three-way leaderboard rows.
- Main leaderboard rows are not a production-GPU timing packet.
- P91 Zhao-Cui SIR d18 CPU/GPU/XLA timings are scoped local complete-data sidecar evidence and are not full observed-data/filtering leaderboard timings.
