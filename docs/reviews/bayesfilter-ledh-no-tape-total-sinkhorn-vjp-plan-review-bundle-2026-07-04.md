# Review Bundle: LEDH No-Tape Total Sinkhorn VJP Plan

Date: 2026-07-04

## Role

Claude is read-only reviewer.  Do not edit files, run commands, launch agents,
or change state.  Codex remains supervisor and executor.

## Objective

Review the plan for implementing a reusable no-`GradientTape`,
no-`ForwardAccumulator` manual total VJP for finite streaming Sinkhorn
transport.

## Exact Artifacts

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-master-program-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-visible-gated-execution-runbook-2026-07-04.md`
- Phase subplans:
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-subplan-2026-07-04.md`
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-subplan-2026-07-04.md`
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-subplan-2026-07-04.md`
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-subplan-2026-07-04.md`
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-subplan-2026-07-04.md`
  - `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-subplan-2026-07-04.md`

## Plan Summary

Baseline:

- stopped-scale/key helpers are no-tape but compute stopped partial
  derivatives;
- `_filterflow_manual_streaming_finite_transport_total_vjp` targets the finite
  total-derivative transport map but still opens `tf.GradientTape`;
- P8p SIR d18 has scoped total-derivative diagnostic evidence but is not a full
  leaderboard score admission;
- LGSSM is the first same-target leaderboard score admission candidate because
  exact Kalman score exists.

Phase order:

1. freeze primitive target and math obligations;
2. implement no-tape primitive;
3. validate primitive against tape-backed total helper and same-scalar FD;
4. regress P8p SIR scoped diagnostic;
5. test LGSSM same-target score admission;
6. close with reset memo and generalization boundary.

Round-1 repair:

- Phase 3 now hands off to Phase 4 only if P8p regression checks pass.
- A failed Phase 3 requires a blocker result and a new human-approved exception
  plan before any LGSSM admission attempt.
- Phase 4 entry now requires a passed Phase 3 gate unless a separate
  human-approved exception plan changes that entry condition.

## Required Review Questions

1. Does the plan preserve the distinction between stopped partial derivatives
   and the unstopped total derivative?
2. Does it avoid promoting P8p SIR scoped evidence to full leaderboard score
   evidence?
3. Are the phase gates ordered correctly: primitive target, implementation,
   primitive validation, SIR regression, LGSSM admission, closeout?
4. Does each phase have objective, entry conditions, required artifacts,
   checks/reviews, evidence contract, forbidden claims/actions, handoff, and
   stop conditions?
5. Are any proxy metrics such as runtime, compile success, or finite smoke
   incorrectly used as score correctness?
6. Are Claude and GPU boundaries correctly preserved?

## Forbidden Claims

- Do not claim the no-tape total VJP is already implemented.
- Do not claim LEDH score admission before Phase 4.
- Do not claim HMC readiness, posterior correctness, runtime superiority, or
  nonlinear adapter correctness.
- Do not describe stopped partial derivatives as scores.

## Verdict

Return findings first, then end with exactly one of:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
