# Source-Scope SGQF Analytical-Gradient Ledger

metadata_date: 2026-06-24
master_program: `docs/plans/bayesfilter-source-scope-sgqf-family-unlocks-master-program-2026-06-24.md`
status: PASS_P5_SOURCE_SCOPE_SGQF_ANALYTICAL_GRADIENT_LEDGER_WRITTEN

## Purpose

This ledger records the current source-scope SGQF analytical-gradient /
analytical-score state family by family.

## Row-by-row score ledger

| Row | Current SGQF value status | Current SGQF score status | Evidence basis | Promotion interpretation |
| --- | --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | `value_only_executed` | `blocked_missing_analytical_route` | direct affine SGQF value route exists in the highdim leaderboard packet, but no source-scope SGQF score route is emitted there | keep value-only until a reviewed source-scope SGQF score route is wired |
| `zhao_cui_sv_actual_nongaussian_T1000` | `blocked_not_same_target` | `blocked_not_same_target` | current SGQF support is the KSC surrogate route, not the actual transformed target | stay blocked |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | `value_only_executed` | `diagnostic_score_only` | SGQF KSC wrapper score has explicit finite-difference tests in `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`, but the reviewed evidence is still tiny-fixture-oriented rather than source-scope-promoted | keep diagnostic-score-only until the source-scope score promotion gate is reviewed |
| `zhao_cui_spatial_sir_austria_j9_T20` | `blocked_missing_value_route` | `blocked_no_free_theta` | no reviewed SGQF source-scope route and the row has no free theta | keep blocked / no-free-theta |
| `zhao_cui_predator_prey_T20` | `value_only_executed` | `analytical_score_admitted` | explicit SGQF derivative route and same-branch finite-difference tests in `tests/highdim/test_p47_predator_prey_filtering.py` | may be treated as analytical-score-admitted under the current reviewed family evidence |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | `blocked_missing_value_route` | `blocked_missing_analytical_route` | no reviewed same-target SGQF source-row evaluator exists yet | stay blocked |

## Why score tests were missing from some unlock plans

The current family unlock sequence is value-first. Rows that do not yet have a
reviewed same-target SGQF **value** evaluator cannot honestly receive an
analytical-score gate yet.

This is why score work is currently meaningful only for:
- the KSC SGQF route as diagnostic-score-only,
- predator-prey as analytical-score-admitted,
- and not yet for actual transformed SV, generalized SV source row, or spatial
  SIR.

## Audit

This ledger keeps score promotion narrower than value promotion and prevents the
repo from silently over-reading tiny-fixture or autodiff evidence as
source-scope analytical-score admission.
