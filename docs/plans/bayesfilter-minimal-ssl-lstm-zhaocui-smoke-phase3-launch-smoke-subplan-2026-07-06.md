# Phase 3 Subplan: Optional Launch-Smoke Bridge

Date: 2026-07-06

Status: `DRAFT_READY_FOR_DECISION`

## Phase Objective

Decide whether an additional launch-smoke bridge is still needed for the
minimal scalar SSL-LSTM smoke program, or whether it would exceed the narrow
question already answered by Phases 1 and 2.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result exists and records passing focused local checks.
- The minimal scalar CPU-hidden smoke artifact exists and preserves role
  boundaries and nonclaims.
- No broader HMC, GPU/XLA production, source-faithful parity, or default
  readiness claim is in scope.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase3-launch-smoke-result-2026-07-06.md`
- Draft/refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-smoke-phase4-closeout-subplan-2026-07-06.md`

## Required Checks, Tests, And Reviews

- Read the master program objective and Phase 1/Phase 2 results.
- Audit whether a launch-smoke command would answer a remaining required
  question.
- If a launch bridge is still required, stop and request any needed runtime
  approvals before execution.
- If no launch bridge is required, record the decision explicitly and advance to
  closeout.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is an additional launch-smoke bridge necessary to answer the minimal scalar smoke question? |
| Baseline/comparator | Master program objective plus Phase 1 and Phase 2 results/artifacts. |
| Primary pass criterion | The phase either justifies a needed launch bridge with explicit evidence burden and approvals, or records that no such bridge is needed for the stated scope. |
| Veto diagnostics | Broadening the question by inertia, treating launch smoke as proof of posterior/HMC/default readiness, or running new runtime scope without approval. |
| Explanatory diagnostics | Existing artifact coverage, residual uncertainty, and approval requirements if a bridge were pursued. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Forbidden Claims And Actions

- Do not claim that skipping launch smoke proves broader readiness.
- Do not run additional launch, GPU, detached, or long commands in this phase
  without a newly justified need and approval.
- Do not reinterpret the existing CPU-hidden smoke as production-target
  evidence.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only when:

- Phase 3 result exists;
- the phase states directly whether launch smoke was needed or not needed;
- any decision to skip or defer launch smoke is grounded in the program's
  stated objective and evidence contract;
- Phase 4 closeout subplan exists.

## Stop Conditions

Stop if a real remaining question requires broader runtime evidence, if that
evidence would need unapproved runtime scope, or if the decision cannot be made
without changing the program objective.

## End-Of-Phase Protocol

1. Audit whether launch smoke is still needed.
2. Write Phase 3 result/close record.
3. Draft or refresh Phase 4 closeout subplan.
4. Review Phase 4 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
