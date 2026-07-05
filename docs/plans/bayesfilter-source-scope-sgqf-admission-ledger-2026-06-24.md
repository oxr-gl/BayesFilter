# Source-Scope SGQF Admission Ledger

metadata_date: 2026-06-24
master_program: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
status: PASS_P0_SOURCE_SCOPE_SGQF_ADMISSION_LEDGER_WRITTEN

## Purpose

This ledger records the current SGQF source-scope family state before additional
unlock work proceeds.

## Row-by-row ledger

| Row | Target identity | SGQF value status | SGQF score status | Current implementation entry point(s) | Blocker / note |
| --- | --- | --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | exact affine LGSSM source row | `value_only_executed` | `blocked_missing_analytical_route` | direct affine SGQF path in `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py` and SGQF affine model support in `tests/test_fixed_sgqf_values_tf.py` | value route exists; no source-scope score route emitted in current packet |
| `zhao_cui_sv_actual_nongaussian_T1000` | actual transformed non-Gaussian SV | `blocked_not_same_target` | `blocked_not_same_target` | none | current SGQF support is KSC surrogate-target only, not same-target actual SV |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | declared KSC Gaussian-mixture surrogate SV target | `value_only_executed` | `diagnostic_score_only` | `bayesfilter/highdim/sv_mixture_cut4.py` via `independent_panel_sv_mixture_fixed_sgqf_filter` and existing tiny-fixture score tests | source-scope value route now emitted; existing analytical-score evidence is tiny-fixture-only, not yet promoted source-scope score admission |
| `zhao_cui_spatial_sir_austria_j9_T20` | source-scope spatial SIR fixed-parameter row | `blocked_missing_value_route` | `blocked_no_free_theta` | none | route-class blocker: no reviewed SGQF source-scope spatial SIR route wired; row also has no free theta |
| `zhao_cui_predator_prey_T20` | source-scope predator-prey row | `value_only_executed` | `analytical_score_admitted` | `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py` and `tests/highdim/test_p47_predator_prey_filtering.py` | SGQF value route exists and family tests already provide explicit analytical derivative + same-branch FD evidence |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | source-scope generalized SV synthetic prior-mean row | `blocked_missing_value_route` | `blocked_missing_analytical_route` | none | native dense same-target reference exists, but no reviewed SGQF source-scope evaluator is wired |

## Audit

The current ledger removes the earlier blanket SGQF-blocked interpretation and
replaces it with row-specific value and score states. This matches the current
executed leaderboard packets and existing family-specific SGQF tests more
faithfully.
