# LEDH No-Tape Total Sinkhorn VJP Master Program

Date: 2026-07-04

Status: `CLOSED_PREFIX_SCORE_PASS_FULL_ROW_BLOCKED`

## Objective

Implement and validate a reusable no-`GradientTape`, no-`ForwardAccumulator`
manual total VJP for the finite streaming Sinkhorn transport used by LEDH.

The target is the derivative of the same finite transport scalar that the
forward route executes.  A stopped-scale/key derivative is wrong relative to
that target unless the stopped scalar is explicitly declared as the target.

## Current Baseline

Existing code has two distinct routes:

- stopped-scale/key helpers are no-tape but compute stopped partial
  derivatives;
- `_filterflow_manual_streaming_finite_transport_total_vjp` targets the finite
  total-derivative transport map but still opens `tf.GradientTape` inside its
  custom-gradient body.

The reusable primitive needed for leaderboard score admission does not yet
exist.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we replace the tape-backed total finite streaming Sinkhorn transport VJP with a no-tape manual VJP and reuse it in LEDH score routes? |
| Baseline/comparator | Current tape-backed total helper for primitive parity, same-scalar finite differences, P8p SIR d18 scoped diagnostic, and LGSSM Kalman score for same-target row admission. |
| Primary pass criterion | A no-tape total transport VJP passes primitive parity/FD checks, preserves P8p SIR same-scalar behavior, and admits the LGSSM LEDH score only after same-route value/score validation. |
| Veto diagnostics | Any production score route uses `GradientTape` or `ForwardAccumulator`; stopped partial derivative called score; value/score route mismatch; wrong scalar target; FD/exact mismatch beyond the phase rule; GPU/XLA claim without trusted execution. |
| Explanatory diagnostics | Runtime, compile time, memory, per-seed MCSE, HLO/static loop hygiene, primitive residuals. |
| Not concluded | Posterior correctness, HMC readiness, runtime superiority, nonlinear adapter correctness, scientific superiority. |
| Artifacts | Phase subplans/results, no-tape VJP tests, static audit outputs, GPU logs, Claude review records, reset memo. |

## Phase Index

| Phase | Name | Subplan | Required result |
| --- | --- | --- | --- |
| 0 | Primitive Target And Math Freeze | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-result-2026-07-04.md` |
| 1 | Primitive No-Tape VJP Implementation | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-result-2026-07-04.md` |
| 2 | Primitive Parity And FD Validation | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-result-2026-07-04.md` |
| 3 | P8p SIR Regression Integration | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-result-2026-07-04.md` |
| 4 | LGSSM Same-Target Score Admission | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-result-2026-07-04.md` |
| 5 | Generalization Boundary And Closeout | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-result-2026-07-04.md` |

## Skeptical Plan Audit

- Wrong baseline risk: controlled by separating primitive parity, P8p scoped
  regression evidence, and LGSSM leaderboard admission evidence.
- Proxy metric risk: runtime and compile metrics cannot admit a score row.
- Stop-condition risk: every phase has explicit blockers and next-phase
  handoff conditions.
- Phase-order risk: LGSSM score admission cannot start after a failed P8p SIR
  regression unless a separate human-approved exception plan changes that gate.
- Unfair comparison risk: no runtime ranking against frozen non-LEDH rows.
- Hidden assumption risk: Phase 0 must define every differentiated primitive
  input and every intentionally constant input.
- Environment mismatch risk: GPU/XLA evidence requires trusted execution.
- Artifact mismatch risk: every material command must write a result artifact
  named by the phase subplan before claims are made.

Current audit result: `PASS_TO_PLAN_REVIEW`.

## Repair Loop

For every phase:

1. run the required local checks;
2. write the phase result or blocker record;
3. draft or refresh the next subplan;
4. review the next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety;
5. use Claude only as read-only reviewer for material phases;
6. patch fixable review findings visibly and rerun focused checks;
7. stop after five review rounds for the same blocker.

Claude cannot authorize human, runtime, model-file, funding, product,
scientific-claim, or default-policy boundaries.

## Human Approval Surface

The user has requested launch after plan creation.  The following remain
trusted/escalated actions under repository policy:

- Claude Code review calls;
- GPU/CUDA/TensorFlow/XLA runs;
- long-running benchmark commands;
- destructive filesystem or git actions;
- network/package/environment changes.

This program closed after Phase 5.  It implemented and locally validated the
no-tape total VJP primitive and the tiny-prefix LGSSM manual total score route.
It did not admit a full T50 GPU leaderboard score row.
