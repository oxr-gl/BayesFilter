# P53-M7 Subplan: Spatial SIR d=50/d=100 Scaling Policy

metadata_date: 2026-06-10
phase: P53-M7
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Evaluate d=50 and d=100 only after d=18 has a reviewed pass or a reviewed
blocker that still justifies preflight-only scaling diagnostics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the highest dimension the repaired scaling route can reasonably test under the memory and claim-boundary policy? |
| Baseline/comparator | P53-M6 d=18 result, scaling-route metadata, rank-budget forecast, UKF scout, and same-route rank evidence. |
| Primary pass criterion | d=50 is either run as bounded filtering stress or blocked with a clear reason; d=100 is at least memory-preflighted and scout-class only unless all stronger prerequisites pass. |
| Veto diagnostics | `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` missing; d=100 filtering launched without d=18/d=50 evidence; filtering stress promoted to correctness; memory cap ignored; GPU claim from CPU-only evidence. |
| Not concluded | No exact correctness at d=50/d=100 without a separate reviewed reference strategy. |

## Planned Work

1. Translate dimensions to site counts.
2. Run memory and route-width preflight for d=50 and d=100.
3. Run UKF or block/local UKF scout as explanatory diagnostics.
4. Run d=50 bounded filtering stress only if prerequisites pass.
5. Keep d=100 scout/preflight by default.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m7-spatial-sir-d50-d100-result-2026-06-10.md`

Required token:

`PASS_P53_M7_SPATIAL_SIR_D50_D100` or
`BLOCK_P53_M7_SPATIAL_SIR_D50_D100`
