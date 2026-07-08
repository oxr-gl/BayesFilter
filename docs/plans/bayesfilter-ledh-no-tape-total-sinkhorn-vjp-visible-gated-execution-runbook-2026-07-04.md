# LEDH No-Tape Total Sinkhorn VJP Visible Gated Execution Runbook

Date: 2026-07-04

## Status

`CLOSED`

## Role Contract

Codex in the current conversation is the supervisor and executor.

Claude is a read-only reviewer only.

This runbook uses visible, recoverable execution inside the current
conversation.  It must not launch detached or nested agents.

## Program

Master program:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-master-program-2026-07-04.md`

Execution ledger:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-visible-execution-ledger-2026-07-04.md`

Stop handoff:

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-visible-stop-handoff-2026-07-04.md`

## Phase Index

| Phase | Name | Subplan | Required result artifact |
| --- | --- | --- | --- |
| 0 | Primitive Target And Math Freeze | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-result-2026-07-04.md` |
| 1 | Primitive No-Tape VJP Implementation | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-result-2026-07-04.md` |
| 2 | Primitive Parity And FD Validation | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase2-primitive-validation-result-2026-07-04.md` |
| 3 | P8p SIR Regression Integration | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-result-2026-07-04.md` |
| 4 | LGSSM Same-Target Score Admission | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-result-2026-07-04.md` |
| 5 | Generalization Boundary And Closeout | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-subplan-2026-07-04.md` | `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase5-closeout-result-2026-07-04.md` |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the LEDH finite streaming Sinkhorn total VJP be made no-tape/manual and validated enough for reuse? |
| Baseline/comparator | Tape-backed total helper, same-scalar finite differences, P8p SIR scoped diagnostic, LGSSM Kalman score. |
| Primary pass criterion | Primitive no-tape total VJP passes parity/FD checks and downstream gates in the declared order. |
| Veto diagnostics | Tape/ForwardAccumulator in production score route; stopped partial derivative called score; wrong scalar target; value/score route mismatch; trusted GPU requirement violated. |
| Explanatory diagnostics | Runtime, compile time, memory, MCSE, residuals. |
| Not concluded | HMC readiness, posterior correctness, nonlinear adapter readiness, scientific superiority. |
| Artifacts | Phase results, logs, JSON outputs, review records, reset memo. |

## Quiet Visible Execution Pattern

Commands expected to produce large output must redirect stdout/stderr to a log
file named in the phase subplan.  The chat should receive only bounded
summaries, exit status, and artifact paths.

## Skeptical Plan Audit

Before each phase, Codex must check for wrong baselines, proxy metrics promoted
to pass criteria, missing stop conditions, unfair comparisons, hidden
assumptions, stale context, environment mismatch, and commands whose artifacts
would not answer the phase question.

## Visible State Machine

For each phase:

1. `PRECHECK`: read subplan, confirm prerequisites, restate evidence contract.
2. `EXECUTE_MINIMAL`: run only the smallest required visible command/edit.
3. `ASSESS_GATE`: compare outputs to criteria and write phase result.
4. `PASS_REVIEW`: use Claude read-only review for material plans/results.
5. `REPAIR_LOOP`: patch fixable findings and rerun focused checks, max five
   rounds for the same blocker.
6. `ADVANCE_OR_STOP`: advance only after the gate passes; otherwise write a
   stop handoff.

## Plain-Language Gate

Every result must say directly whether a derivative is correct for the stated
target, wrong relative to the stated target, unsupported, not checked, or
heuristic only.  Do not describe stopped partial derivatives as scores.

## Human-Required Stop Conditions

Stop if continuing would require package installation, network fetches,
destructive git/filesystem action, changing pass criteria after seeing results,
changing default policy, modifying unrelated dirty work, or interpreting GPU
results without trusted execution.
