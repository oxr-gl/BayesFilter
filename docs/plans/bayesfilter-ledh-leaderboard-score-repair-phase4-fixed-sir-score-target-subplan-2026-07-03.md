# Phase 4 Subplan: Fixed SIR Score Target Decision

Date: 2026-07-03

Status: `REFRESHED_AFTER_PHASE3_BLOCKED_TOTAL_TRANSPORT_VJP`

## Phase Objective

Decide whether the fixed spatial SIR leaderboard row has a legitimate LEDH
score target.  If the row has no free parameter coordinate in the current
leaderboard definition, keep it value-only and do not invent a score.

## Entry Conditions Inherited From Previous Phase

Phase 3 left LGSSM score blocked with the specific reason:

- `blocked_total_transport_vjp_needs_no_tape_repair`.

Phase 4 may classify the fixed SIR score target, but it must not claim that
LGSSM score repair is complete and must not promote any LEDH score row.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-result-2026-07-03.md`
- Optional target manifest JSON if a free-theta SIR row is approved.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, And Reviews

- Inspect current leaderboard SIR row definitions.
- Inspect parameterized SIR scoped component artifacts.
- Run local content check that no scoped diagnostic is promoted to full row.
- Confirm the Phase 3 LGSSM blocker remains recorded and no LEDH
  `executed_value_score` row is introduced.
- Claude read-only review for any target-status change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the fixed spatial SIR leaderboard row have a score target, or is it value-only by definition? |
| Baseline/comparator | Current SIR leaderboard row and scoped parameterized SIR component result. |
| Primary criterion | Phase records either `no_free_theta_value_only` or a reviewed explicit parameter target, while preserving the Phase 3 LGSSM score blocker. |
| Veto diagnostics | Invented parameterization; scoped component promoted to full observed-data score; missing source anchors for Zhao-Cui route claims. |
| Explanatory diagnostics | Existing fixed SIR value MCSE, P8p total-VJP evidence, likely score-coordinate candidates. |
| Not concluded | Full SIR observed-data score unless a target is explicitly reviewed and implemented. |

## Forbidden Claims And Actions

- Do not call a fixed-parameter row score-ready.
- Do not use P8p local complete-data diagnostics as full observed-data score.
- Do not use "faithful" for Zhao-Cui behavior without paper/source anchors.
- Do not call any LEDH row `executed_value_score` in Phase 4.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 if:

- fixed SIR score status is plainly recorded;
- no invented SIR score is admitted;
- Phase 5 lists nonlinear rows that still need same-target LEDH adapters.

## Stop Conditions

Stop if:

- SIR target authority is ambiguous and needs human decision;
- source-faithfulness claims cannot be anchored;
- Claude blocks the target classification and the blocker is not fixed within
  five rounds.

## Phase-End Duties

At the end of Phase 4:

1. run required local checks;
2. write the Phase 4 result;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
