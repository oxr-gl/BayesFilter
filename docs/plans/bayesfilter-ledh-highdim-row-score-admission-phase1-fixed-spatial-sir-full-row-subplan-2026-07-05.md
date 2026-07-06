# Phase 1 Subplan: Fixed Spatial SIR Full-Row Score Promotion

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 1

## Phase Objective

Turn the current LEDH spatial SIR state from:

- full-row value only for `zhao_cui_spatial_sir_austria_j9_T20`, and
- scoped diagnostic score only for `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`

into a single admitted full-row fixed spatial SIR value-and-score route, if the
same-target scalar and free parameter vector can be defined and checked.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch result passed:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase0-launch-blocker-freeze-result-2026-07-05.md`
- The row meanings are frozen:
  - fixed spatial SIR full row is a main leaderboard row;
  - parameterized logscale SIR is scoped diagnostic evidence only until this
    phase proves a correct bridge.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase1-fixed-spatial-sir-full-row-result-2026-07-05.md`
- A row-target note or section inside the result that names:
  - the exact full-row scalar,
  - the exact differentiated parameter vector,
  - whether the existing parameterized diagnostic is identical to that full-row
    derivative target or not.
- Updated tests for tiny correctness and later `N=10000` admission if the row
  is repaired.

## Required Checks/Tests/Reviews

```bash
rg -n "zhao_cui_spatial_sir_austria_j9_T20|parameterized_logscale|manual_reverse_scan_no_autodiff|scoped_component_row|blocked_score_for_full_leaderboard_row" docs/plans docs/benchmarks tests
```

If code is changed later in the phase, required checks expand to:

- focused tiny same-scalar FD tests;
- no-autodiff source/runtime sentinel tests;
- row metadata tests proving value and score share the same row id and route id;
- `N=10000` score-memory test if the row becomes admitted.

Material review required:

- Claude read-only review of the Phase 1 result and the Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the current fixed spatial SIR full-row value route and the current scoped parameterized SIR score route be turned into one correct full-row same-target value-and-score row? |
| Baseline/comparator | The July 3 row ledger, the current SIR value runner, the current parameterized SIR manual score diagnostic, and same-scalar centered FD on tiny fixed-randomness fixtures. |
| Primary criterion | The phase either proves and implements a full-row same-target score route or explicitly records why the current scoped score is wrong or insufficient for the full row. |
| Veto diagnostics | Any mismatch between the full-row scalar and the scoped diagnostic scalar; any use of hidden autodiff; any claim that scoped diagnostic evidence is full-row evidence without a proof. |
| Explanatory diagnostics | Value-only `N=10000` evidence, memory notes, and local component diagnostics. |
| Not concluded | No Zhao-Cui source-faithfulness claim, no HMC readiness, and no general claim for other nonlinear rows. |

## Forbidden Claims/Actions

- Do not call the existing scoped parameterized SIR score a full-row score
  unless the scalar identity is proved.
- Do not promote a full-row score using tape gradients.
- Do not skip tiny same-scalar FD checks.
- Do not change the row target after seeing diagnostic results.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only after Phase 1 writes one of two explicit outcomes:

1. `PASS_PHASE1_FIXED_SIR_FULL_ROW_SCORE`
   - exact full-row scalar frozen;
   - exact parameter vector frozen;
   - tiny same-scalar score checks passed;
   - no-autodiff route confirmed;
   - next blocker is actual-SV target mismatch; or
2. `BLOCK_PHASE1_FIXED_SIR_FULL_ROW_SCORE`
   - precise reason the full-row bridge failed;
   - evidence that the failure is real and not just missing plumbing;
   - exact smallest next repair task or human decision.

## Stop Conditions

Stop if the phase cannot state the exact full-row scalar in mathematical terms,
or if the scoped parameterized score is shown to be a different derivative
target than the leaderboard row.
