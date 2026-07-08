# Phase 8 Subplan: Closeout And Reset Memo

Date: 2026-07-03

Status: `REFRESHED_AFTER_NO_OP_MERGE`

## Phase Objective

Write the final closeout and reset memo for the LEDH leaderboard score-repair
program, preserving the no-admission result and the remaining technical
blockers.

## Entry Conditions Inherited From Previous Phase

Phase 7 recorded:

- no leaderboard merge was needed;
- the July 3 LEDH-inclusive leaderboard contains `7` LEDH rows and `0`
  admitted LEDH score rows;
- LGSSM score remains blocked by
  `blocked_total_transport_vjp_needs_no_tape_repair`;
- fixed SIR remains value-only;
- nonlinear rows remain blocked, target-mismatched, or scoped-only.

## Required Artifacts

- Closeout:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-result-2026-07-03.md`
- Reset memo:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-reset-memo-2026-07-03.md`
- Updated visible execution ledger.

## Required Checks, Tests, And Reviews

- Local content check that every LEDH row has a final score status.
- Local content check that the closeout states zero admitted LEDH score rows.
- `git diff --check` for touched runbook artifacts.
- Claude read-only final review is optional because no row status changed and
  no scientific claim is promoted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the final LEDH score-repair state and what should the next agent know? |
| Baseline/comparator | Phase 7 no-op merge result and all prior phase results. |
| Primary criterion | Closeout states admitted rows, blocked rows, evidence artifacts, checks, and nonclaims plainly. |
| Veto diagnostics | Unsupported score claim; missing row; evasive language; hidden blocker; missing reset memo. |
| Explanatory diagnostics | Future repair direction and review status. |
| Not concluded | Anything not supported by row-specific evidence. |
| Artifact preserving result | Phase 8 closeout and reset memo. |

## Forbidden Claims And Actions

- Do not soften wrong-target or partial-derivative issues with ambiguous
  language.
- Do not claim HMC readiness unless a separate HMC plan passed.
- Do not claim rows are fixed when only value evidence exists.
- Do not describe stopped partial derivatives as scores for MLE/HMC unless the
  stopped scalar is explicitly the target.

## Exact Next-Phase Handoff Conditions

This is the final phase.  The handoff is complete when:

- closeout and reset memo exist;
- final checks are recorded;
- any remaining blockers are explicit;
- the visible ledger status is closed.

## Stop Conditions

Stop if:

- final row statuses cannot be reconciled;
- a final review blocker remains unresolved after five rounds;
- a human direction decision is needed.

## Phase-End Duties

At the end of Phase 8:

1. run required local checks;
2. write closeout and reset memo;
3. mark the visible ledger closed;
4. report final artifact paths and remaining blockers.
