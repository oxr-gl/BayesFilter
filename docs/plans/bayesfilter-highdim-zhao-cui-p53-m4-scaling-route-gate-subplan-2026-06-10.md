# P53-M4 Subplan: Scaling Route Gate

metadata_date: 2026-06-10
phase: P53-M4
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Design, implement, and lower-rung tie out the actual high-dimensional scaling
route class before rank selection or spatial SIR d=18/d=50/d=100 phases can
run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does BayesFilter have a real scaling route, distinct from lower-rung streaming dense-equivalent tie-out infrastructure, that can support rank/scaling phases? |
| Baseline/comparator | P53-M1 route design, P53-M2 lower-rung implementation, P53-M3 dense tie-out, P52-M4 blocker, and current dense route. |
| Primary pass criterion | A `scaling_route` implementation exists, is TensorFlow differentiable, avoids dense all-pairs semantics in the production route, emits deterministic replay and `R_eff` or conservative route-width metadata, and ties out on lower-rung references or blocks with a precise reason. |
| Veto diagnostics | P53-M1-M3 passed only for `lower_rung_dense_equivalent`; scaling route is contract-only; dense all-pairs route remains the production path; no lower-rung tie-out for the scaling route; route-width/memory metadata absent. |
| Not concluded | Passing this gate does not prove rank selection, d=18 filtering, d=50/d=100 correctness, or HMC readiness. |

## Planned Work

1. Select the scaling route class: local-neighborhood sparse route or TT-MPO
   factorized contraction.
2. Document or amend the P30 route equations if the scaling route differs from
   the P53-M1 lower-rung route.
3. Implement the scaling route in TensorFlow / TensorFlow Probability.
4. Tie out against dense lower-rung references with declared tolerances.
5. Emit either `PASS_P53_M4_SCALING_ROUTE_GATE` with route metadata or
   `BLOCK_P53_M4_SCALING_ROUTE_GATE` with a precise design, implementation, or
   tie-out blocker.

## Stop Rule

If only a `lower_rung_dense_equivalent` route has passed P53-M1 through P53-M3,
this phase must block.  P53-M5 through P53-M8 must not run except for stop or
closeout bookkeeping.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m4-scaling-route-gate-result-2026-06-10.md`

Required token:

`PASS_P53_M4_SCALING_ROUTE_GATE` or `BLOCK_P53_M4_SCALING_ROUTE_GATE`

