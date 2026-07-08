# Master Result: Source-Scope SGQF Family Unlocks And Analytical-Gradient Gates

metadata_date: 2026-06-24
master_program: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
status: PARTIAL_PASS_SOURCE_SCOPE_SGQF_MASTER_PROGRAM_WITH_ROW_SPECIFIC_ADVANCES

## Program summary

This pass established a unified source-scope SGQF admission ledger, promoted the
KSC surrogate T1000 source row to SGQF value execution, repaired the highdim
leaderboard so SGQF is no longer blanket-blocked, and added the missing
family-by-family analytical-gradient ledger.

## Current source-scope SGQF family states

### Value states
- `benchmark_lgssm_exact_oracle_m3_T50` → `value_only_executed`
- `zhao_cui_sv_actual_nongaussian_T1000` → `blocked_not_same_target`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` → `value_only_executed`
- `zhao_cui_spatial_sir_austria_j9_T20` → `blocked_missing_value_route`
- `zhao_cui_predator_prey_T20` → `value_only_executed`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values` → `blocked_missing_value_route`

### Score states
- `benchmark_lgssm_exact_oracle_m3_T50` → `blocked_missing_analytical_route`
- `zhao_cui_sv_actual_nongaussian_T1000` → `blocked_not_same_target`
- `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` → `diagnostic_score_only`
- `zhao_cui_spatial_sir_austria_j9_T20` → `blocked_no_free_theta`
- `zhao_cui_predator_prey_T20` → `analytical_score_admitted`
- `zhao_cui_generalized_sv_synthetic_from_estimated_values` → `blocked_missing_analytical_route`

## Artifacts written or refreshed
- `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`
- `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.json`
- `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-06-24.md`

## Verification run

Focused contract / score-gate verification completed in smaller chunks after a
larger combined run was killed by the environment:
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`

Observed:
- contract tests passed,
- KSC SGQF score-focused tests passed,
- SGQF predator-prey score-focused tests passed.

## Remaining real blockers
- actual transformed SV still needs a same-target SGQF evaluator.
- generalized SV still needs a same-target SGQF evaluator.
- spatial SIR still needs route-development work before source-scope SGQF value execution is honest.

## Next justified action
Proceed into the actual-transformed-SV and generalized-SV value-evaluator phases,
and only then revisit whether a deeper spatial-SIR route milestone can be landed.
