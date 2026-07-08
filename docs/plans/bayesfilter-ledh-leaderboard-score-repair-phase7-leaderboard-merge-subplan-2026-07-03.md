# Phase 7 Subplan: No-Op Leaderboard Merge

Date: 2026-07-03

Status: `REFRESHED_NO_LED_SCORE_ROWS_ADMITTED`

## Phase Objective

Close the leaderboard merge phase without changing the July 3 LEDH-inclusive
leaderboard, because no LEDH score row was admitted by the score-repair
program.

## Entry Conditions Inherited From Previous Phase

Phase 6 recorded:

- no nonlinear row entered score repair;
- no nonlinear LEDH score row was admitted;
- LGSSM score remains blocked by
  `blocked_total_transport_vjp_needs_no_tape_repair`;
- fixed SIR remains `no_free_theta_value_only`.

## Required Artifacts

- Phase 7 result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-result-2026-07-03.md`
- Refreshed Phase 8 subplan:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase8-closeout-reset-subplan-2026-07-03.md`
- Updated visible execution ledger.

## Required Checks, Tests, And Reviews

- JSON/content check that the July 3 LEDH-inclusive leaderboard admits no LEDH
  score rows.
- Content check that all carried-forward blockers appear in the Phase 7 result.
- `git diff --check` for touched runbook artifacts.
- Claude read-only review is not required because no row is promoted and no
  leaderboard data artifact is changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the refreshed leaderboard state need to change after the score-repair phases? |
| Baseline/comparator | July 3 LEDH-inclusive leaderboard plus Phase 3 through Phase 6 results. |
| Primary criterion | Preserve the existing leaderboard artifact unchanged when no LEDH score row was admitted. |
| Veto diagnostics | Hidden promoted score row; stale claim that a blocked row passed; runtime ranking against frozen rows; omitted blocker; Contract E score substitution. |
| Explanatory diagnostics | Row counts and blocker summary. |
| Not concluded | Scientific superiority, posterior correctness, HMC readiness. |
| Artifact preserving result | Phase 7 result file and updated ledger. |

## Forbidden Claims And Actions

- Do not edit the July 3 leaderboard JSON or Markdown to promote LEDH scores.
- Do not runtime-rank fresh LEDH rows against frozen non-LEDH rows.
- Do not merge diagnostic-only rows as full leaderboard rows.
- Do not omit blocked rows.

## Exact Next-Phase Handoff Conditions

Advance to Phase 8 if:

- Phase 7 result states that the merge is a no-op;
- local checks verify no LEDH score row is admitted in the July 3 leaderboard;
- all carried-forward blockers remain explicit;
- Phase 8 is refreshed as final closeout and reset memo writing.

## Stop Conditions

Stop if:

- row statuses conflict with phase results;
- the existing leaderboard contains a hidden admitted LEDH score row;
- a merge would require changing baseline policy;
- local checks fail and the fix is not obvious.

## Phase-End Duties

At the end of Phase 7:

1. run required local checks;
2. write the Phase 7 result;
3. draft or refresh the Phase 8 subplan;
4. review the Phase 8 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
