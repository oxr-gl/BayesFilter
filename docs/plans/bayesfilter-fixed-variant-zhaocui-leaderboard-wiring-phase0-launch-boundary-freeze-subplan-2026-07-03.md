# Phase 0 Subplan: Launch Boundary Freeze

Date: 2026-07-03

Status: `READY_EXECUTED_PHASE0_RESULT_WRITTEN`

## Phase Objective

Freeze the current route-governance, artifact, and leaderboard baseline before
any implementation or regeneration work.

## Entry Conditions Inherited From Previous Phase

- User directed that the generic retained-grid route is diagnostic/historical.
- Codex has added preliminary route demotion markers and focused tests.
- No phase result in this program has passed yet.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase0-launch-boundary-freeze-result-2026-07-03.md`
- Execution ledger update:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-visible-execution-ledger-2026-07-03.md`
- Refreshed Phase 1 subplan if Phase 0 changes the baseline.

## Required Checks / Tests / Reviews

- `rg` checks for retained-grid demotion markers in `AGENTS.md`,
  `bayesfilter/highdim/filtering.py`, and focused tests.
- `rg` checks for current SIR row status in July leaderboard artifacts.
- `git diff --check` on the master program and Phase 0 artifacts.
- Claude read-only review of this subplan or Phase 0 result if a material
  boundary changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the current baseline before fixed-variant leaderboard wiring begins? |
| Baseline/comparator | Current worktree, route demotion constants, current leaderboard JSON/MD, and P91 evidence artifacts. |
| Primary criterion | The result records exact current route/admission status, affected row ids, and existing P91 evidence paths. |
| Veto diagnostics | Missing retained-grid demotion marker, missing P91 artifact, stale row id not noticed, or hidden unreviewed production claim. |
| Explanatory diagnostics | Dirty worktree summary and current blocked leaderboard status. |
| Not concluded | No implementation correctness, no regenerated leaderboard, no full filtering readiness, no GPU readiness. |
| Artifact | Phase 0 result and ledger entry. |

## Forbidden Claims / Actions

- Do not claim the fixed-variant row is wired.
- Do not edit leaderboard runner code in Phase 0.
- Do not run GPU commands in Phase 0.
- Do not treat P91 local complete-data evidence as full observed-data filtering
  evidence.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if Phase 0 records:

- retained-grid demotion marker present;
- current leaderboard SIR Zhao-Cui row status;
- P91 evidence paths present or missing status explicitly recorded;
- no material baseline ambiguity requiring human direction.

## Stop Conditions

- Route demotion markers are absent and cannot be restored without conflicting
  with user work.
- Current leaderboard artifacts are missing or unreadable.
- P91 evidence artifacts are missing and no replacement source is available.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 0 result / close record.
3. Draft or refresh Phase 1 subplan.
4. Review Phase 1 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
