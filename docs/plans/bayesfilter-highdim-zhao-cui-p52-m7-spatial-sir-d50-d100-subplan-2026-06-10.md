# P52-M7 Subplan: Spatial SIR d=50/d=100 Scaling Policy

metadata_date: 2026-06-10
phase: P52-M7
status: PLAN_REVIEW_CONVERGED

## Objective

Evaluate how far the repaired route can reasonably scale beyond d=18 under the
32 GB practical memory contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are d=50 and d=100 reasonable filtering targets for the repaired route, and what claims can each row support? |
| Baseline/comparator | P52-M6 d=18 result, rank budget forecasts, UKF scout diagnostics, and route metadata. |
| Primary pass criterion | d=50 is either run as a bounded filtering stress row under cap or blocked with a clear memory/factorization reason; d=100 is at least preflighted and UKF-scouted, and only promoted to bounded filtering stress if all preconditions pass. |
| Veto diagnostics | d=100 run launched without d=18/d=50 evidence; memory forecast ignored; filtering stress promoted to correctness; rank increased beyond contract; GPU claims from CPU-only evidence. |
| Not concluded | No exact correctness at d=50/d=100 unless a separate reviewed reference strategy exists. |

## Planned Work

1. Translate dimensions to site counts: `d=50 -> J=25`, `d=100 -> J=50`.
2. Run memory-rank preflight for both dimensions.
3. Run UKF or block/local UKF scout for both dimensions.
4. For d=50, run bounded-horizon filtering stress only if P52-M6 passed and
   rank/memory caps clear.
5. For d=100, default to scout plus memory preflight.  Actual filtering is
   allowed only if d=18 and d=50 pass, the projected memory is below cap, and
   the result is labeled scaling stress rather than correctness.
6. Record the reasonable maximum tested dimension with claim class.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m7-spatial-sir-d50-d100-result-2026-06-10.md`

Required token:

`PASS_P52_M7_SPATIAL_SIR_D50_D100` or
`BLOCK_P52_M7_SPATIAL_SIR_D50_D100`
