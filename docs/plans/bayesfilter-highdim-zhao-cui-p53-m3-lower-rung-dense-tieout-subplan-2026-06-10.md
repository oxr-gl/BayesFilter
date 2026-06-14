# P53-M3 Subplan: Lower-Rung Dense Tie-Out

metadata_date: 2026-06-10
phase: P53-M3
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Compare the P53-M2 route with the dense lower-rung spatial SIR route before any
rank or scaling claims are attempted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the new route reproduce the dense lower-rung transition/predictive update on tiny grids within declared numerical tolerances? |
| Baseline/comparator | Existing dense lower-rung spatial SIR route, P53-M2 implementation, and P30 route equations. |
| Primary pass criterion | Tiny-grid value tie-out passes, gradients are finite and connected where applicable, deterministic replay is exact within serialized metadata, and discrepancies are within predeclared tolerances. |
| Veto diagnostics | Dense reference is changed after seeing results; tolerances are changed after seeing results; tie-out skipped; finite smoke result promoted to equivalence; route differs from P30 design. |
| Not concluded | Lower-rung equivalence does not prove d=18/d=50/d=100 correctness or scaling-route readiness. |

## Planned Work

1. Use spatial SIR `J=1` and the smallest feasible `J=2`/`J=3` lower rungs.
2. Compare predictive log densities and one-step likelihood values against the
   dense route.
3. Check finite gradients and directional consistency where the route is
   differentiable in parameters.
4. Record numerical tolerances before executing.
5. Block if lower-rung tie-out fails without a repaired explanation.

If the tied-out route class is `lower_rung_dense_equivalent`, this phase may
pass only as a lower-rung equivalence result.  It must not unlock rank selection
or spatial SIR d=18/d=50/d=100 scaling.  That requires
`PASS_P53_M4D_SCALING_ROUTE_ADMISSION`.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m3-lower-rung-dense-tieout-result-2026-06-10.md`

Required token:

`PASS_P53_M3_LOWER_RUNG_DENSE_TIEOUT` or
`BLOCK_P53_M3_LOWER_RUNG_DENSE_TIEOUT`
