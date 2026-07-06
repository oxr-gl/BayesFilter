# Phase 6 Result: Leaderboard Reassembly And Row Test Expansion

Date: 2026-07-06

Status: `COMPLETE_NO_NEW_FULL_HIGHDIM_LEDH_SCORE_ROWS_ADMITTED`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Do not rewrite the LEDH-inclusive leaderboard as a new all-model score leaderboard. Phases 1-5 admitted no additional full highdim LEDH leaderboard score rows, so Phase 6 preserves the existing admitted/blocked split and closes the runbook. |
| Primary criterion status | Passed by truthful closeout: every row is enumerated, admitted score-route evidence is separated from blocked full-row score status, and no blocked row is silently promoted. |
| Veto diagnostic status | Passed: no scoped SIR diagnostic was treated as the fixed full-row SIR score, no callback existence was treated as row admission, no autodiff score was admitted, and no runtime or memory result was used as a substitute for score correctness. |
| Main uncertainty | The next repair program must decide whether to bridge existing candidate adapter surfaces or replace them with fresh same-target GPU/XLA TF32 adapters row by row. |
| Next justified action | Start a new row-specific implementation program for the remaining blockers, beginning with the smallest bridge that can admit an actual same-target value route before any score work. |
| What is not concluded | No all-model LEDH score readiness, no full highdim LEDH leaderboard rerun, no HMC readiness, no posterior correctness claim, and no scientific superiority claim. |

## Why The Runbook Stops Here

This is a proper stop, unlike a phase-boundary pause.

Phase 6 asked whether the leaderboard could be reassembled with newly admitted
rows after the row-specific repair phases. The answer is no: Phases 1-5 closed
by precise blockers, not by row admissions. Reassembling the leaderboard as if
those rows were repaired would be wrong relative to the stated evidence
contract.

Therefore Phase 6 closes the program with a truthful status ledger instead of
launching a misleading full leaderboard run.

## Admitted Score-Route Evidence After This Program

These are the only LEDH score routes with current `N=10000` no-autodiff
correctness/memory guardrail evidence:

| Row | Scope | Evidence | Admission meaning |
| --- | --- | --- | --- |
| `benchmark_lgssm_exact_oracle_m3_T50` | main observed-data filtering row | `docs/plans/ledh-score-memory-test-suite-result-2026-07-05.md` | Compact no-autodiff same-scalar LGSSM score route passed the `N=10000` score/memory suite. |
| `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale` | scoped local-complete-data component row | `docs/plans/ledh-score-memory-test-suite-result-2026-07-05.md` | Manual no-autodiff scoped component score passed the `N=10000` score/memory suite, but it is not the fixed full-row observed-data SIR score. |

The LGSSM status changed relative to the July 3 closeout because the later
July 5 score/memory suite supplied the compact no-autodiff score evidence. The
parameterized SIR evidence remains scoped and must not be promoted into the
fixed full-row SIR leaderboard row.

## Rows That Remain Blocked For Full Highdim LEDH Score Admission

| Row | Phase | Final status | Remaining blocker |
| --- | ---: | --- | --- |
| `zhao_cui_spatial_sir_austria_j9_T20` | 1 | blocked full-row score | The fixed full-row source-parity SIR row has `no_free_theta`; the parameterized SIR score is a different scoped target. |
| `zhao_cui_sv_actual_nongaussian_T1000` | 2 | blocked value and score | The current raw-likelihood-corrected LEDH runner is not the old Gaussian-closure scalar, but the reviewed bridge to the declared transformed actual-SV row target is still missing. |
| `zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000` | 3 | blocked value and score | No KSC-specific current LEDH adapter surface exists. Existing KSC same-target routes are non-LEDH comparators. |
| `zhao_cui_predator_prey_T20` | 4 | blocked value and score | Predator-prey LEDH code surfaces exist, but no reviewed bridge admits any of them as the current same-target GPU/XLA TF32 leaderboard route. |
| `zhao_cui_generalized_sv_synthetic_from_estimated_values` | 5 | blocked value and score | The row target is frozen and a generalized-SV LEDH callback exists, but no reviewed source-row adapter bridge admits it as same-target evidence. |

## Leaderboard Reassembly Decision

No new full highdim LEDH leaderboard score row is added by this program.

The current leaderboard artifacts remain status artifacts, not an all-model
LEDH score leaderboard:

- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`
- `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`

They should not be rewritten as a promoted all-row score leaderboard until each
blocked row has:

1. a reviewed same-target value adapter for the exact row;
2. a no-tape total derivative of the executed scalar;
3. tiny correctness evidence;
4. `N=10000` correctness and memory evidence;
5. row-specific review and result artifacts.

## Checks Run

```bash
git diff --check -- \
  docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-result-2026-07-05.md \
  docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md \
  docs/reviews/ledh-highdim-row-score-admission-phase6-review-bundle-2026-07-06.md
```

Result: pending until the Phase 6 patch is complete, then rerun.

```bash
rg -n "COMPLETE_NO_NEW_FULL_HIGHDIM_LEDH_SCORE_ROWS_ADMITTED|benchmark_lgssm_exact_oracle_m3_T50|zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale|zhao_cui_sv_actual_nongaussian_T1000|zhao_cui_sv_ksc_gaussian_mixture_surrogate_T1000|zhao_cui_predator_prey_T20|zhao_cui_generalized_sv_synthetic_from_estimated_values" \
  docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-result-2026-07-05.md \
  docs/plans/bayesfilter-ledh-highdim-row-score-admission-visible-execution-ledger-2026-07-05.md \
  docs/reviews/ledh-highdim-row-score-admission-phase6-review-bundle-2026-07-06.md
```

Result: pending until the Phase 6 patch is complete, then rerun.

## Evidence Contract Result

| Field | Status |
| --- | --- |
| Question | Answered directly: no full all-model LEDH score leaderboard can be produced from the current evidence. |
| Baseline/comparator | Passed: July 3 LEDH-inclusive leaderboard, Phase 1-5 results, and July 5 score-memory suite agree on the admitted/blocked split. |
| Primary criterion | Passed: every row is enumerated and no row is promoted without row-specific same-target and no-tape score evidence. |
| Veto diagnostics | Passed: no blocked row, scoped row, callback existence, or memory-only success was promoted. |
| Explanatory diagnostics | Runtime, memory, callback, and diagnostic surfaces remain useful inputs for the next row-specific repair program. |
| Not concluded | No all-model score readiness, no leaderboard score promotion, no HMC readiness, and no scientific superiority claim. |

## Final Closeout

The row-score admission program is complete as a blocker triage and closeout
program.

Final state:

- admitted no-tape score-route evidence: LGSSM compact score and scoped
  parameterized SIR component score;
- full highdim LEDH score rows newly admitted by this program: none;
- blocked full rows: fixed spatial SIR, actual SV, KSC SV, predator-prey, and
  generalized SV;
- next work: create a new implementation runbook for row-specific same-target
  adapter bridges before any additional score-route promotion.
