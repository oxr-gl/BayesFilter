# Phase 4 Subplan: LGSSM Same-Target Score Admission

Date: 2026-07-04

Status: `READY_REVIEWED`

## Phase Objective

Use the no-tape total transport VJP in the LGSSM LEDH route and test whether
the same-target leaderboard row can admit an LEDH score.

## Entry Conditions Inherited From Previous Phase

Phase 3 passed the P8p SIR regression gate with route metadata proving no-tape
total VJP use.  Phase 3/4 Claude read-only review returned
`REVIEW_STATUS=agreed`, `VERDICT=AGREE`, with summary at
`/home/chakwong/BayesFilter/.claude_reviews/20260704-035504-bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase3-phase4/status.json`.

## Required Artifacts

- LGSSM same-target value/score JSON artifacts.
- Static no-tape audit artifact.
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase4-lgssm-score-admission-result-2026-07-04.md`
- Refreshed Phase 5 closeout subplan.

## Required Checks, Tests, And Reviews

- Static audit: no `GradientTape` or `ForwardAccumulator` in LEDH production
  score route.
- Same-route check: value and score share one scalar route id.
- Same-algorithm check: value and score use the same LEDH transport algorithm,
  including the same finite streaming total VJP route.
- Exact Kalman score or same-scalar FD comparison under predeclared tolerance.
- Trusted GPU/XLA/TF32 material smoke if a production route claim is made.
- Claude read-only review before any score admission claim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does LEDH compute the total derivative of the same LGSSM leaderboard scalar without tape? |
| Baseline/comparator | Exact FP64 Kalman value/score for `benchmark_lgssm_exact_oracle_m3_T50` plus same-scalar FD when needed. |
| Primary criterion | No-tape same-route LEDH score passes exact/FD tolerance and trusted GPU/XLA evidence if production status is claimed. |
| Veto diagnostics | Tape route; stopped partial derivative; value/score route mismatch; value/score transport algorithm mismatch; wrong LGSSM row; nonfinite score; exact/FD mismatch beyond rule. |
| Explanatory diagnostics | MCSE, seed dispersion, compile/runtime/memory. |
| Not concluded | HMC readiness, posterior correctness, nonlinear row readiness, runtime superiority. |

## Forbidden Claims And Actions

- Do not use Contract E as leaderboard LGSSM score evidence.
- Do not admit a score from a CPU-only material route.
- Do not claim HMC readiness from score agreement alone.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- LGSSM row has an explicit admitted or blocked score status;
- all artifacts preserve same-route/no-tape evidence;
- Claude review agrees or a human-accepted blocker is recorded;
- Phase 5 closeout is refreshed.

## Stop Conditions

Stop if:

- score route cannot be made same-route and no-tape;
- value and score cannot be made same-algorithm;
- exact/FD evidence fails;
- material GPU execution is required but unavailable;
- Claude blocks score admission and the issue is not fixed within five rounds.

## Phase-End Duties

At the end of Phase 4:

1. run required local checks;
2. write Phase 4 result;
3. draft or refresh Phase 5 subplan;
4. review Phase 5 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
