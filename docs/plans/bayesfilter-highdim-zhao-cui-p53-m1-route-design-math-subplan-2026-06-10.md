# P53-M1 Subplan: Route Design, Math, And P30 Amendment

metadata_date: 2026-06-10
phase: P53-M1
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Choose and document the concrete spatial SIR transition route before coding.
This phase must update the P30 companion note or create a reviewed amendment so
the implementation cannot drift into an ad hoc route.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which memory-bounded transition route should BayesFilter implement first, and what equations define its target, memory model, and claim boundary? |
| Baseline/comparator | P52-M4 dense-route blocker, current spatial SIR transition density, P30 notation, lower-rung dense route, and P52 rank/memory policy. |
| Primary pass criterion | A reviewed design artifact selects a concrete route and documents equations, deterministic replay identity, `R_eff` or route-width metadata, memory forecast, and claim class. |
| Veto diagnostics | Route choice deferred to implementation; streaming dense-equivalent route promoted to high-dimensional scalability; local/TT approximation introduced without a lower-rung tie-out plan; P30 not updated or amended. |
| Not concluded | No implementation correctness, no filtering correctness, and no HMC readiness. |

## Planned Work

1. Write the route-design section in the P30 note or a P30 amendment.
2. Select the first implementation route:
   - blocked streaming dense-equivalent route for lower-rung tie-out;
   - local-neighborhood sparse route; or
   - TT-MPO factorized contraction route.
3. State exact formulas for the predictive update and where approximation
   enters.
4. State memory equations and the metadata that P53-M2 must emit.
5. State which later claims are allowed from this route and which are blocked.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m1-route-design-math-result-2026-06-10.md`

Required token:

`PASS_P53_M1_ROUTE_DESIGN_MATH` or `BLOCK_P53_M1_ROUTE_DESIGN_MATH`

