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
   - Owner: Codex.
   - Entry condition: current phase artifacts and required inherited authorities
     are identified.
   - Required action: run the phase's allowed local prechecks and confirm no
     forbidden runtime or promotion action is being attempted.
   - Exit: move to `REVIEW_SUBPLAN` if prechecks pass; otherwise repair within
     document/code scope or stop if the failure is a substantive blocker.

2. `REVIEW_SUBPLAN`
   - Owner: Claude reviewer on one bounded path at a time; Codex applies any
     approved repairs.
   - Entry condition: the current phase subplan exists and is the active
     execution authority for the phase.
   - Required action: obtain a bounded read-only review verdict for the subplan.
   - Exit: move to `EXECUTE_MINIMAL` only after `VERDICT: AGREE`; move to
     `REPAIR_LOOP` on `VERDICT: REVISE`.

3. `EXECUTE_MINIMAL`
   - Owner: Codex.
   - Entry condition: the phase subplan is reviewed `AGREE`.
   - Required action: perform only the minimum actions authorized by the phase
     subplan, preserving all stated nonclaims and runtime boundaries.
   - Exit: move to `ASSESS_GATE` after execution artifacts are written.

4. `ASSESS_GATE`
   - Owner: Codex first-pass assessment, later confirmed by Claude review of the
     result artifact.
   - Entry condition: current-phase actions are complete and a result or blocker
     artifact has been written.
   - Required action: classify the outcome as pass, blocker, precursor-only,
     diagnostic-only, or stop-worthy according to the phase evidence contract.
   - Exit: move to `PASS_REVIEW` with a refreshed next-phase subplan for pass,
     precursor-only, or diagnostic-only outcomes; move to `PASS_REVIEW` with the
     blocker artifact plus stop handoff for blocker, stop-worthy, or human-
     boundary outcomes.

5. `PASS_REVIEW`
   - Owner: Claude reviewer on the result artifact and next-phase subplan, or on
     the blocker artifact and stop handoff.
   - Entry condition: either:
     - a current-phase result artifact plus refreshed next-phase subplan exists,
       or
     - a current-phase blocker artifact plus stop handoff exists.
   - Required action: review the current-phase result/blocker artifact first,
     then review the refreshed next-phase subplan or stop handoff, one bounded
     path at a time.
   - Exit: move to `ADVANCE_OR_STOP` if the reviewed artifacts receive
     `VERDICT: AGREE`; move to `REPAIR_LOOP` on `VERDICT: REVISE`.

6. `REPAIR_LOOP`
   - Owner: Codex.
   - Entry condition: Claude identified a fixable issue, or Codex identified a
     local repair that stays within the current phase boundary.
   - Required action: patch only the current-phase artifact(s), rerun the phase's
     allowed local checks if needed, and resubmit the repaired artifact for fresh
     bounded review.
   - Exit: return to `REVIEW_SUBPLAN` or `PASS_REVIEW` as appropriate.

7. `ADVANCE_OR_STOP`
   - Owner: Codex, with Claude-confirmed reviewed artifacts.
   - Entry condition: current-phase reviewed artifacts are closed.
   - Required action: either advance to the next phase using the already-
     reviewed refreshed next-phase subplan, or stop using the already-reviewed
     stop handoff if a substantive blocker or human-required boundary has been
     reached.
   - Exit: next phase `PRECHECK`, or program stop.

## Execution Rule

- Continue phase-by-phase unless a reviewed blocker or human-required boundary
  appears.
- A reviewed blocker means either:
  - Claude identified a blocking issue in a bounded review and the issue is not
    repairable within the current phase scope, or
  - Codex found a substantive contract violation and recorded it in the current
    phase result/blocker artifact before stopping.
- A human-required boundary means a decision that would change the governed row,
  target family, truth/test-point convention, comparator family, default policy,
  publication/release state, or other authority reserved beyond the current
  reviewed phase scope.
- Fixable issues should be repaired within the current phase rather than causing
  unnecessary stop/start drift.
- No implementation, benchmark mutation, or source-row promotion work may begin
  before the target/truth/source-scope contract passes.
- Every phase advance requires a reviewed subplan, reviewed result/blocker, and
  refreshed reviewed next-phase subplan.

## Stop Conditions

- wrong target identity;
- actual-SV and generalized-SV confusion;
- KSC surrogate promoted as generalized-SV;
- native reference and source-row evaluator blended;
- wrong truth/test point;
- missing source-scope evaluator when promotion is attempted;
- review nonconvergence after five rounds for the same blocker;
- human-required boundary.

## Review-Round And Repair Semantics

- A review round is one bounded Claude review of one artifact path.
- The same blocker means materially the same unresolved issue across repeated
  review rounds for the same artifact.
- Every repair must stay within the current phase boundary and must receive a
  fresh bounded review before the phase may advance.
- If a repair would require changing the row identity, target identity,
  truth/test-point convention, comparator family, or phase scope, stop and write
  the stop handoff instead of repairing through the boundary.
