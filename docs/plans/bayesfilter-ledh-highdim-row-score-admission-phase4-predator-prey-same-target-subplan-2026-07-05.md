# Phase 4 Subplan: Predator-Prey Same-Target Adapter And Score

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 4

## Phase Objective

Admit a current same-target GPU/XLA LEDH predator-prey row and its no-tape
total-derivative score, without relying on legacy callback existence or lower
rung diagnostic closures.

## Entry Conditions Inherited From Previous Phase

- Phase 3 finished.
- Predator-prey remains blocked because no reviewed current same-target LEDH
  adapter is admitted for the leaderboard row.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase4-predator-prey-same-target-result-2026-07-05.md`
- A predator-prey row-target note naming:
  - the exact T20 scalar;
  - the exact differentiated parameter vector;
  - the current LEDH adapter or replacement.
- Tests:
  - tiny same-target value tests;
  - tiny score FD tests;
  - no-autodiff sentinels;
  - later `N=10000` score-memory test if admitted.

## Required Checks/Tests/Reviews

```bash
rg -n "predator_prey|blocked_no_reviewed_current_gpu_xla_ledh_row_adapter|blocked_target_alignment|same-target|diagnostic-only" docs/plans docs/benchmarks bayesfilter tests
```

Material review required:

- Claude read-only review of the Phase 4 result and the Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 row be executed as a current same-target LEDH scalar with a no-tape total derivative, rather than as legacy or diagnostic evidence? |
| Baseline/comparator | The July 2 blocker inventory, any reviewed predator-prey target note, and tiny same-scalar FD checks. |
| Primary criterion | The phase either admits a same-target current LEDH predator-prey row and score or writes a precise blocker proving why the current route is still wrong or missing. |
| Veto diagnostics | Treating diagnostic closures as leaderboard proof; treating legacy callback existence as current adapter proof; using autodiff score as admission evidence. |
| Explanatory diagnostics | Lower-rung fixtures and diagnostic closure notes. |
| Not concluded | No generalized-SV claim, no HMC claim, no source-faithfulness claim beyond the reviewed row target. |

## Forbidden Claims/Actions

- Do not use lower-rung diagnostic closure evidence as T20 leaderboard proof.
- Do not use legacy route existence as current same-target proof.
- Do not admit the score before the current value route is admitted.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin only after Phase 4 records either a passed predator-prey row
or a precise blocker that does not blur the row target.

## Stop Conditions

Stop if the phase cannot freeze the exact T20 target or if all current candidate
routes are shown to be diagnostic only.
