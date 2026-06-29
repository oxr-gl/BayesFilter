# Generalized-SV Visible Gated Execution Runbook

Date: 2026-06-29

## Status

`ACTIVE_VISIBLE_EXECUTION_RUNBOOK`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude Opus max effort is a read-only reviewer only.

No detached, hidden, or copied-workspace execution is allowed. Continue
phase-by-phase unless a real reviewed blocker appears.

## Program

- reset memo: `docs/plans/bayesfilter-generalized-sv-governed-restart-reset-memo-2026-06-29.md`
- master program: `docs/plans/bayesfilter-generalized-sv-governed-master-program-2026-06-29.md`
- contract: `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
- execution ledger: `docs/plans/bayesfilter-generalized-sv-visible-execution-ledger-2026-06-29.md`
- review ledger: `docs/plans/bayesfilter-generalized-sv-claude-review-ledger-2026-06-29.md`
- stop handoff: `docs/plans/bayesfilter-generalized-sv-visible-stop-handoff-2026-06-29.md`

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
- No implementation, benchmark mutation, or source-row promotion work may begin
  before the target/truth/source-scope contract passes.

## Stop Conditions

- wrong target identity;
- actual-SV and generalized-SV confusion;
- KSC surrogate promoted as generalized-SV;
- native reference and source-row evaluator blended;
- wrong truth/test point;
- missing source-scope evaluator when promotion is attempted;
- review nonconvergence after five rounds for the same blocker;
- human-required boundary.
