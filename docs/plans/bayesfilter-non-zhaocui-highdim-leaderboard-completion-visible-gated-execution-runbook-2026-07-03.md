# Non-Zhao-Cui Highdim Leaderboard Completion Visible Runbook

Date: 2026-07-03

## Status

`ACTIVE_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

No detached, hidden, or copied-workspace execution is allowed. Continue
phase-by-phase unless a real reviewed blocker or explicit human-required
boundary appears.

## Program

- master program:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-master-program-2026-07-03.md`
- execution ledger:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-execution-ledger-2026-07-03.md`
- review ledger:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-claude-review-ledger-2026-07-03.md`
- stop handoff:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-visible-stop-handoff-2026-07-03.md`

## Visible State Machine

1. `PRECHECK`
2. `REVIEW_SUBPLAN`
3. `EXECUTE_MINIMAL`
4. `ASSESS_GATE`
5. `PASS_REVIEW`
6. `REPAIR_LOOP`
7. `ADVANCE_OR_STOP`

## Execution Rule

- Continue phase-by-phase unless a reviewed blocker or human-required boundary
  appears.
- Fixable issues should be repaired within the current phase rather than causing
  unnecessary stop/start drift.
- Do not ask the user to choose row semantics, exact-vs-approximate status, or
  analytical-score policy when those are already fixed by the reviewed row
  contracts and this master program.
- Every phase advance requires a reviewed subplan, reviewed result/blocker, and
  refreshed reviewed next-phase subplan.

## Stop Conditions

- wrong-target scalar promoted;
- autodiff score promoted as analytical;
- value-only row promoted as gradient evidence;
- sidecar/local-complete-data evidence promoted as main-row evidence;
- unexplained approximation gap at the reviewed claim level;
- review nonconvergence after five rounds for the same blocker;
- human-required boundary.
