# Phase 0 Subplan: Primitive Target And Math Freeze

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Freeze the exact finite streaming Sinkhorn transport scalar and write the
mathematical reverse-mode obligations for a no-tape total VJP.

## Entry Conditions Inherited From Previous Phase

This is the first execution phase.  It inherits the closed LEDH score-repair
blocker:

- current no-tape stopped helpers compute partial derivatives;
- current total helper uses `tf.GradientTape`;
- no LEDH score row is admitted.

## Required Artifacts

- Phase 0 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-result-2026-07-04.md`
- Math/implementation brief:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-primitive-target-brief-2026-07-04.md`
- Refreshed Phase 1 subplan.

## Required Checks, Tests, And Reviews

- Inspect current target code anchors in `annealed_transport_tf.py`.
- Static content check that the brief names differentiated inputs and
  intentionally constant inputs.
- Static content check that stopped partial derivatives are classified as
  wrong relative to the unstopped target.
- Claude read-only review of the Phase 0 result and Phase 1 implementation
  subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact finite transport scalar must the no-tape VJP differentiate? |
| Baseline/comparator | Current total helper and stopped-scale/key helpers in `annealed_transport_tf.py`. |
| Primary criterion | The brief states forward equations, differentiated inputs, constant inputs, reverse obligations, and no-tape constraints clearly enough for implementation. |
| Veto diagnostics | Ambiguous scalar target; omitted differentiated dependency; stopped partial derivative called a score; implementation begins before target freeze; no next-phase handoff. |
| Explanatory diagnostics | Code anchors, known helper names, expected tensor shapes. |
| Not concluded | No implementation correctness, no runtime viability, no downstream score correctness. |

## Forbidden Claims And Actions

- Do not edit algorithmic code in Phase 0.
- Do not run GPU/XLA material commands.
- Do not claim a no-tape total VJP exists.
- Do not call stopped partial derivatives scores for the unstopped target.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 result and primitive brief exist;
- the brief identifies all VJP inputs and reverse obligations;
- local checks pass;
- Claude review agrees or a documented human-accepted review blocker exists.

## Stop Conditions

Stop if:

- the target scalar cannot be stated unambiguously;
- differentiated inputs cannot be determined from current code;
- Claude blocks the target freeze and the issue is not fixed within five
  rounds.

## Phase-End Duties

At the end of Phase 0:

1. run required local checks;
2. write Phase 0 result;
3. draft or refresh Phase 1 subplan;
4. review Phase 1 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
