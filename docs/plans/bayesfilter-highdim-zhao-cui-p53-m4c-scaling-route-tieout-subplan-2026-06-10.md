# P53-M4C Subplan: Scaling Route Lower-Rung Tie-Out

metadata_date: 2026-06-10
phase: P53-M4C
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Tie out the implemented `C_scale` route from P53-M4B on lower-rung spatial SIR
fixtures before any admission to rank selection.  This phase may not start
unless P53-M4B emits `PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the selected `C_scale` route reproduce its declared lower-rung target on J=1/J=2/J=3 under predeclared tolerances? |
| Baseline/comparator | P53-M4A tie-out target, P53-M4B implementation, dense retained-grid route, and/or P53-M2 `C_low` route as declared by M4A. |
| Primary pass criterion | J=1/J=2/J=3 value, replay, metadata, and gradient checks pass under M4A-declared tolerances; deviations are reported by model dimension and route metadata. |
| Veto diagnostics | M4B pass token absent; tie-out target changed after seeing results; tolerances changed after seeing results; only smoke tests run; failing dimensions hidden; lower-rung tie-out promoted to d=18/d=50/d=100 correctness. |
| Not concluded | Passing M4C does not prove rank selection, d=18/d=50/d=100 correctness, production HMC readiness, or GPU readiness. |

## Planned Work

1. Load the M4A tie-out contract and tolerances.
2. Run J=1/J=2/J=3 spatial SIR lower-rung comparisons.
3. Check values, gradients where applicable, replay identity, route-width
   metadata, and memory forecast.
4. Record all tolerances and deviations in a manifest.
5. Emit either pass or a precise blocker by dimension and diagnostic.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m4c-scaling-route-tieout-result-2026-06-10.md`

Required token:

`PASS_P53_M4C_SCALING_ROUTE_TIEOUT` or
`BLOCK_P53_M4C_SCALING_ROUTE_TIEOUT`
