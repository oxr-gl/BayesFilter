# Phase 0 Subplan: Launch And Blocker Freeze

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 0

## Phase Objective

Freeze the execution order, row meanings, and scientific boundaries before any
 new model-specific score repair work begins.

## Entry Conditions Inherited From Previous Phase

- No prior phase is required; this is the launch phase.
- The July 3 row-admission ledger and July 5 LEDH `N=10000` score-memory suite
  are the governing starting evidence.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-result-2026-07-05.md`
- Visible execution ledger:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md`
- Visible stop handoff:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-stop-handoff-2026-07-05.md`
- Refreshed Phase 1 subplan if Phase 0 review or local checks require edits.

## Required Checks/Tests/Reviews

```bash
rg -n "benchmark_lgssm_exact_oracle_m3_T50|zhao_cui_spatial_sir_austria_j9_T20|zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values" docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase6-closeout-result-2026-07-03.md tests/test_ledh_score_memory_n10000.py
git diff --check -- docs/plans/bayesfilter-ledh-highdim-row-score-admission-*
```

Material review required:

- Claude read-only review of the master program, runbook, Phase 0 result, and
  Phase 1 subplan; if Claude is unavailable after probe/retry, replace with a
  fresh Codex review packet.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the program order scientifically correct, and does it preserve the current blocked-row truth without smuggling in unsupported score claims? |
| Baseline/comparator | The July 3 row-admission ledger, July 3 closeout result, and July 5 `N=10000` score-memory suite. |
| Primary criterion | Phase 0 result states the exact order, exact row meanings, exact admitted-vs-blocked split, and exact launch boundaries without contradiction. |
| Veto diagnostics | Treating the scoped SIR score as the full-row SIR score; treating any blocked row as admitted; changing row meaning or pass criteria during launch. |
| Explanatory diagnostics | Extra historical notes and older blocked-run artifacts. |
| Not concluded | No row repair, no new score admission, no leaderboard rerun, and no scientific validity claim beyond the current admitted rows. |

## Forbidden Claims/Actions

- Do not change row scope.
- Do not claim any blocked row is now score-ready.
- Do not begin model-specific implementation in this phase.
- Do not describe scoped parameterized SIR evidence as the fixed full-row
  leaderboard score.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if Phase 0 records:

1. the exact program order;
2. the exact reason fixed spatial SIR is first;
3. the exact reason actual SV must precede KSC;
4. the exact admitted-vs-blocked row list;
5. a refreshed Phase 1 subplan that still respects those boundaries.

## Stop Conditions

Stop if the row ledger, closeout result, and current test suite disagree on row
status, or if review finds the sequence logically unsound.
