# Phase 2 Subplan: Same-Target LGSSM Score Repair

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE1`

## Phase Objective

Implement and validate a same-target LEDH score route for
`benchmark_lgssm_exact_oracle_m3_T50`.

The score target is the total derivative of the same finite-particle LEDH
likelihood estimator used by the same-target LGSSM row, compared against the
exact Kalman score for the row.

## Entry Conditions Inherited From Previous Phase

Phase 1 must establish:

- LGSSM row target is `D=3,T=50`, dataset seed `81100`, theta
  `[0.72, 0.55, 0.35, 0.35, 0.45]`;
- existing LEDH evidence for this row is value-only;
- exact Kalman score comparator is available;
- Contract E is not a substitute for this row.

## Required Artifacts

- Updated or new same-target LGSSM score runner under `docs/benchmarks/`.
- Focused tests under `tests/`.
- Score diagnostic JSON/MD under `docs/plans/`.
- Phase result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase2-lgssm-score-repair-result-2026-07-03.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-subplan-2026-07-03.md`

## Required Checks, Tests, And Reviews

- `python -m py_compile` for any edited runner/source/test files.
- Focused pytest for schema and score target classification.
- Trusted GPU/XLA/TF32 smoke for a small same-target LGSSM score run.
- Exact Kalman score comparison at a small material particle count.
- Claude read-only review of implementation diff and Phase 2 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does LEDH compute a total-derivative score for the same LGSSM leaderboard row target? |
| Baseline/comparator | Exact FP64 Kalman value and score for `benchmark_lgssm_exact_oracle_m3_T50`. |
| Primary criterion | A small trusted GPU/XLA score run produces finite value/score, correct target metadata, and every score coordinate passes the predeclared exact-score gate or remains blocked with reason. |
| Veto diagnostics | Contract E target; partial derivative route; missing total dependency through LEDH flow/transport/reset; CPU-only material route; nonfinite score; exact-score mismatch beyond rule. |
| Explanatory diagnostics | Compile time, memory, MCSE, per-seed score variation, particle count trend. |
| Not concluded | Full production-scale score admission, HMC readiness, nonlinear row correctness. |

## Forbidden Claims And Actions

- Do not claim leaderboard score admission from a tiny smoke only.
- Do not use CPU diagnostics as production GPU/XLA evidence.
- Do not claim HMC readiness from score agreement.
- Do not silently change the finite scalar target to make gradients easier.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- Phase 2 has either a finite GPU/XLA total-score smoke or a blocker proving
  why the route cannot yet run;
- target metadata in the output matches the leaderboard LGSSM row;
- the score route is labeled total derivative or blocked, never ambiguous;
- Phase 3 states memory-safe scaling and chunking requirements.

## Stop Conditions

Stop if:

- implementing the score route would require changing the target without a new
  reviewed objective;
- no exact comparator can be produced for the row;
- GPU route fails before a CPU diagnostic can isolate implementation vs
  environment;
- Claude blocks the implementation/result and the blocker is not fixed within
  five rounds.

## Phase-End Duties

At the end of Phase 2:

1. run the required local checks;
2. write the Phase 2 result;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
