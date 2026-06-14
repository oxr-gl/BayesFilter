# P53-M4D Subplan: Scaling Route Admission Gate

metadata_date: 2026-06-10
phase: P53-M4D
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Admit or block the selected scaling route after separate derivation,
implementation, and lower-rung tie-out phases.  This is the only phase allowed
to emit the token that unlocks P53-M5 through P53-M8.

Only `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` may unlock P53-M5 through P53-M8.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do P53-M4A, P53-M4B, and P53-M4C together justify admitting the selected `C_scale` route for rank selection? |
| Baseline/comparator | M4A derivation, M4B implementation, M4C tie-out, P53 route-class rules, P52 rank-budget requirements, and P30 notation. |
| Primary pass criterion | All M4A-M4C pass tokens exist; route metadata is coherent across phases; no veto fired; final manifest emits `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` with explicit nonclaims and prerequisite evidence paths. |
| Veto diagnostics | Any M4A-M4C block token; inconsistent route id or metadata; lower-rung tie-out skipped; `C_low` evidence substituted for `C_scale`; no route-width bound; M5-M8 admission would rely on old `PASS_P53_M4_SCALING_ROUTE_GATE`. |
| Not concluded | Passing M4D does not prove rank selection, d=18 filtering, d=50/d=100 correctness, HMC readiness, or GPU readiness. |

## Planned Work

1. Reconcile M4A, M4B, and M4C manifests.
2. Verify route id, route class, selected design, replay identity, route-width
   metadata, and nonclaims are consistent.
3. Verify the old P53-M4 block token is historical only and cannot unlock M5.
4. Emit:
   - `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` if all admission checks pass; or
   - `BLOCK_P53_M4D_SCALING_ROUTE_ADMISSION` with precise blocker.
5. Add static admission tests proving P53-M5/M6/M7 require
   `PASS_P53_M4D_SCALING_ROUTE_ADMISSION`, and proving P53-M8 closeout cannot
   run until P53-M5, P53-M6, and P53-M7 have emitted reviewed pass tokens.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m4d-scaling-route-admission-result-2026-06-10.md`

Required token:

`PASS_P53_M4D_SCALING_ROUTE_ADMISSION` or
`BLOCK_P53_M4D_SCALING_ROUTE_ADMISSION`
