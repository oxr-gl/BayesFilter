# Phase 6 Subplan: Nonlinear Score Repair Skipped

Date: 2026-07-03

Status: `SKIPPED_NO_ADMITTED_NONLINEAR_ROWS`

## Phase Objective

Close Phase 6 without running nonlinear score repair because Phase 5 admitted no
nonlinear row as same-target adapter-ready.

## Entry Conditions Inherited From Previous Phase

Phase 5 recorded:

- actual SV: `adapter_missing`;
- KSC SV: `target_mismatch`;
- predator-prey: `adapter_missing`;
- generalized SV: `adapter_missing`;
- fixed SIR remains excluded as `no_free_theta_value_only`;
- LGSSM score remains blocked by
  `blocked_total_transport_vjp_needs_no_tape_repair`.

No nonlinear row is allowed to enter score repair in this phase.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase6-nonlinear-score-repair-result-2026-07-03.md`
- Refreshed Phase 7 subplan:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase7-leaderboard-merge-subplan-2026-07-03.md`
- Updated visible execution ledger:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-visible-execution-ledger-2026-07-03.md`

## Required Checks, Tests, And Reviews

- Local content check that this subplan does not contain admitted nonlinear
  score-repair language.
- Local content check that the Phase 5 result and adapter ledger classify all
  four nonlinear rows.
- `git diff --check` for touched runbook artifacts.
- Claude read-only review is required only if Phase 6 attempts to promote a
  nonlinear row.  This skipped phase promotes no row.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can Phase 6 run nonlinear LEDH score repair under the current evidence? |
| Baseline/comparator | Phase 5 nonlinear adapter-admission result and the July 3 LEDH-inclusive leaderboard. |
| Primary criterion | Phase 6 must skip execution when no nonlinear row is `adapter_ready`. |
| Veto diagnostics | Any nonlinear score row is promoted; a target-mismatched row is repaired as if same-target; KSC surrogate evidence is used for native SV; a blocked row is hidden; fixed SIR is reintroduced as a score target. |
| Explanatory diagnostics | Row-by-row blocker reasons from Phase 5. |
| Not concluded | No nonlinear LEDH score correctness, no HMC readiness, no scientific superiority, no source-faithfulness claim. |
| Artifact preserving result | Phase 6 result file and updated ledger. |

## Forbidden Claims And Actions

- Do not run GPU/XLA nonlinear score diagnostics in this phase.
- Do not claim any nonlinear LEDH score row is admitted.
- Do not change row targets to create an adapter-ready row.
- Do not use a scoped component diagnostic as a full observed-data leaderboard
  score.
- Do not soften a wrong-target or missing-adapter blocker with ambiguous
  language.

## Exact Next-Phase Handoff Conditions

Advance to Phase 7 only after:

- Phase 6 result records `SKIPPED_NO_ADMITTED_NONLINEAR_ROWS`;
- all Phase 5 row classifications are preserved;
- the LGSSM blocker and fixed-SIR value-only classification are preserved;
- Phase 7 is refreshed as a no-admission/no-op merge unless a separately
  approved adapter target exists.

## Stop Conditions

Stop if:

- any artifact implies a nonlinear row is score-ready;
- the Phase 5 row classifications cannot be reconciled;
- a human target decision is required to continue;
- local content checks fail and the fix is not obvious.

## Phase-End Duties

At the end of Phase 6:

1. run required local checks;
2. write the Phase 6 result;
3. draft or refresh the Phase 7 subplan;
4. review the Phase 7 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
