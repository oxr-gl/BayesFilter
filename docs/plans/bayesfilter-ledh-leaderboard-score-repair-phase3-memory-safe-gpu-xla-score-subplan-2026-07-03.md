# Phase 3 Subplan: Manual-VJP LGSSM Score Route Repair

Date: 2026-07-03

Status: `REFRESHED_AFTER_PHASE2_TAPE_ROUTE_RETRACTION`

## Phase Objective

Implement the same-target LGSSM LEDH score route using manual VJP only.

Tape-gradient score computation is forbidden for LEDH score repair in this
program.

The reported value and score must come from the same finite-particle scalar
route.  Phase 3 must not report a value from the value-only runner and a score
from a separate scalar route unless it first proves those are the same scalar
under the same fixed randomness and records a single route id for both.

## Entry Conditions Inherited From Previous Phase

Phase 2 produced and then retracted:

- a tape-gradient LGSSM score runner attempt;
- a CPU-hidden eager prefix diagnostic from that invalid route;
- a graph CPU-hidden failure at `tape.gradient`;
- no leaderboard score admission.

The tape-gradient runner has been removed.

## Required Artifacts

- Manual-VJP LGSSM score implementation patch or blocker note.
- Same-route value/score manifest fields:
  `value_route_id`, `score_route_id`, and
  `value_score_route_status == same_route_value_score`.
- Manual-VJP versus exact/finite-difference diagnostic JSON/MD.
- Trusted GPU/XLA tiny score smoke JSON/MD if graph repair passes.
- Logs under `docs/plans/logs/`.
- Phase result:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase3-memory-safe-gpu-xla-score-result-2026-07-03.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-ledh-leaderboard-score-repair-phase4-fixed-sir-score-target-subplan-2026-07-03.md`

## Required Checks, Tests, And Reviews

- `python -m py_compile` for edited files.
- Focused pytest proving the LEDH score route contains no `GradientTape` score
  computation.
- Static no-autodiff audit for the material score entrypoint.
- Same-route admission check proving `value_route_id == score_route_id` before
  any leaderboard merge.
- CPU-hidden manual-VJP versus same-scalar finite-difference tiny diagnostic.
- Trusted GPU probe before any material GPU run.
- Trusted GPU/XLA tiny score smoke only after manual VJP passes local checks.
- Claude read-only review for the Phase 3 repair/result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the same LGSSM total-score route be computed by manual VJP without changing the target? |
| Baseline/comparator | Exact Kalman score for the full row and same-scalar finite differences for small fixed-randomness diagnostics. |
| Primary criterion | Manual VJP tiny diagnostic agrees with same-scalar finite differences, declares one value/score route id, then a trusted GPU/XLA tiny score smoke runs with finite `[B,5]` score. |
| Veto diagnostics | Any `GradientTape` or `ForwardAccumulator` score route, target change, value/score route mismatch, partial derivative route, CPU-only material route, nonfinite score, missing target metadata. |
| Explanatory diagnostics | Compile time, runtime, memory, per-seed score variation, finite-difference step sensitivity. |
| Not concluded | Nonlinear score readiness, posterior correctness, runtime ranking. |

## Forbidden Claims And Actions

- Do not lower the row target to Contract E.
- Do not use `GradientTape` to compute LEDH scores.
- Do not use `ForwardAccumulator` to compute LEDH scores.
- Do not call the retracted tape-gradient prefix diagnostic score evidence.
- Do not use a stopped partial derivative.
- Do not mix a value from one scalar route with a score from another route.
- Do not run GPU/XLA score until manual VJP works locally.
- Do not change pass/fail criteria after seeing results.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 if:

- LGSSM score is either admitted, still blocked with an exact graph/GPU reason,
  or moved to a later manual-VJP repair phase;
- Phase 4 states whether fixed SIR has a free-theta score target or not.

## Stop Conditions

Stop if:

- memory or compile time prevents any bounded artifact from being written;
- GPU unavailable in trusted context;
- result criteria become inadequate and need human decision;
- Claude blocks a promotion and the blocker is not fixed within five rounds.

## Phase-End Duties

At the end of Phase 3:

1. run required local checks;
2. write the Phase 3 result;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
