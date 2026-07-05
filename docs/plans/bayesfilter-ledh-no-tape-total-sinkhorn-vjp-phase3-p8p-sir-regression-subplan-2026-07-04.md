# Phase 3 Subplan: P8p SIR Regression Integration

Date: 2026-07-04

Status: `READY_REVIEWED`

## Phase Objective

Replace the scoped P8p SIR d18 total-route transport VJP with the no-tape
primitive and verify that prior same-scalar total-derivative diagnostics still
pass.

## Entry Conditions Inherited From Previous Phase

Phase 2 validated the primitive against raw tape and central finite differences
on a tiny same-scalar fixture.  Phase 3 starts only after the Phase 2 read-only
review gate accepts the result and this refreshed P8p regression subplan.  That
review returned `REVIEW_STATUS=agreed`, `VERDICT=AGREE`.

## Required Artifacts

- P8p SIR regression JSON/log artifacts under `docs/plans/`.
- Phase 3 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-p8p-sir-regression-result-2026-07-04.md`
- Refreshed Phase 4 subplan.

## Required Checks, Tests, And Reviews

- Focused P8p active-transport comparator test.
- Static no-tape runtime sentinel for the P8p score route.
- Route metadata must show use of the no-tape total finite streaming Sinkhorn
  primitive, not the stopped-key route and not a local tape fallback.
- Same-scalar P8p score checks must use the value route and score route with
  the same transport algorithm.
- If GPU/XLA is required, run only in trusted context with quiet logs.
- Claude read-only review of Phase 3 result and Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the no-tape primitive preserve the scoped P8p SIR total-derivative behavior? |
| Baseline/comparator | Prior P8p total-route FD/tape diagnostics and Phase 2 primitive validation. |
| Primary criterion | P8p same-scalar total-derivative checks pass with route metadata proving no-tape total VJP use. |
| Veto diagnostics | P8p route falls back to tape; stopped partial derivative used as score; value/score algorithm mismatch; scoped diagnostic promoted to full leaderboard row; same-scalar FD fails. |
| Explanatory diagnostics | Runtime, compile time, MCSE, per-coordinate errors. |
| Not concluded | Full observed-data SIR leaderboard score, HMC readiness, nonlinear adapter correctness. |

## Forbidden Claims And Actions

- Do not promote P8p scoped evidence to the fixed SIR leaderboard row.
- Do not claim HMC readiness.
- Do not run large GPU ladders unless Phase 3 explicitly gates them.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- P8p regression checks pass;
- route metadata proves no-tape total VJP use;
- Phase 4 LGSSM admission subplan is refreshed and reviewed.

A failed P8p regression does not hand off to Phase 4.  It requires a blocker
result and a new human-approved exception plan before any LGSSM score-admission
attempt.

## Stop Conditions

Stop if:

- no-tape primitive breaks P8p same-scalar checks;
- runtime sentinel detects tape/ForwardAccumulator in production route;
- value and score use different transport algorithms;
- GPU execution is needed but trusted execution is unavailable;
- P8p regression fails and no human-approved exception plan exists;
- Claude blocks the result and the issue is not fixed within five rounds.

## Phase-End Duties

At the end of Phase 3:

1. run required local checks;
2. write Phase 3 result;
3. draft or refresh Phase 4 subplan;
4. review Phase 4 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
