# P53-M4A Subplan: Scaling Route Choice And Derivation

metadata_date: 2026-06-10
phase: P53-M4A
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Choose one real `C_scale` route before any scaling-route implementation is
attempted.  This phase exists because the original P53-M4 plan tried to choose,
derive, implement, tie out, and admit the scaling route in one phase, which was
a planning error.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which concrete scaling route should be implemented next, and what equations, approximation status, replay identity, route-width metadata, memory model, and tie-out criteria define it? |
| Baseline/comparator | P53-M1 route design, P53-M2 `C_low` implementation, P53-M3 dense tie-out, P53-M4 blocker, P30 spatial SIR equations, and current dense route. |
| Primary pass criterion | Exactly one `C_scale` design is selected: local-neighborhood sparse contraction or TT-MPO factorized contraction.  The selected design has equations detailed enough for TensorFlow implementation, explicit approximation status, deterministic replay identity, `R_eff` or conservative route-width bound, memory forecast, gradient-bearing variables, and predeclared lower-rung tie-out criteria for P53-M4C. |
| Veto diagnostics | Route choice deferred to M4B; `C_low` relabeled as `C_scale`; approximation status hidden; no implementable equations; no route-width or memory metadata; no lower-rung tie-out criteria. |
| Not concluded | Passing M4A does not implement the route, prove lower-rung tie-out, unlock rank selection, establish d=18/d=50/d=100 readiness, or prove HMC readiness. |

## Planned Work

1. Re-read P30 spatial SIR transition equations and P53 route-class amendment.
2. Compare local-neighborhood sparse contraction and TT-MPO contraction for
   near-term implementability, faithfulness, and HMC gradient compatibility.
3. Select exactly one `C_scale` route for P53-M4B.
4. Write an M4A derivation artifact, preferably as a P30 amendment if the route
   changes the mathematical story.
5. Define:
   - transition factorization/evaluation equations;
   - exact versus approximate target status;
   - replay identity;
   - route-width or `R_eff` metadata;
   - memory forecast;
   - TensorFlow gradient-bearing variables;
   - J=1/J=2/J=3 lower-rung tie-out criteria and tolerances.
6. Add static tests that prove M4A does not pass with an unchosen route or a
   `C_low` relabeling.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m4a-scaling-route-choice-derivation-result-2026-06-10.md`

Required token:

`PASS_P53_M4A_SCALING_ROUTE_DERIVATION` or
`BLOCK_P53_M4A_SCALING_ROUTE_DERIVATION`
