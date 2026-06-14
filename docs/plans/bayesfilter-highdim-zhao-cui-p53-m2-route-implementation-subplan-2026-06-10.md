# P53-M2 Subplan: Lower-Rung TensorFlow Route Implementation

metadata_date: 2026-06-10
phase: P53-M2
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Implement the P53-M1 lower-rung route in TensorFlow / TensorFlow Probability
with a real callable transition application.  A contract object alone cannot
pass this phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does BayesFilter contain an executable TensorFlow lower-rung route that avoids full dense pair materialization and emits replay, memory, and route-width metadata? |
| Baseline/comparator | P53-M1 design, current dense `tf.repeat`/`tf.tile` route, and lower-rung dense route for later tie-out. |
| Primary pass criterion | New TensorFlow implementation is wired behind an explicit route interface, avoids full `N_current x N_previous` materialization in the lower-rung route, preserves gradients, and emits deterministic replay plus memory metadata. |
| Veto diagnostics | Implementation only adds a contract; differentiable path uses NumPy; hidden dense matrix allocation remains in production route; no replay identity; no route-width or memory metadata. |
| Not concluded | Passing implementation does not prove lower-rung equivalence, high-dimensional scalability, filtering correctness, or scaling-route readiness. |

## Planned Work

1. Add or extend a route implementation module under `bayesfilter/highdim`.
2. Keep the old dense route available only as a lower-rung reference.
3. Add static tests rejecting full `tf.repeat`/`tf.tile` materialization in the
   new production route.
4. Add dynamic smoke tests for shapes, finite values, gradient connectivity,
   deterministic replay, and metadata.
5. Emit a manifest with route type, claim class, `R_eff` or conservative
   route-width proxy, and memory forecast fields.

If the implemented route class is `lower_rung_dense_equivalent`, this phase may
pass only as interface/tie-out infrastructure.  It must not unlock rank
selection or spatial SIR d=18/d=50/d=100 scaling.  That requires
`PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m2-route-implementation-result-2026-06-10.md`

Required token:

`PASS_P53_M2_ROUTE_IMPLEMENTATION` or `BLOCK_P53_M2_ROUTE_IMPLEMENTATION`
