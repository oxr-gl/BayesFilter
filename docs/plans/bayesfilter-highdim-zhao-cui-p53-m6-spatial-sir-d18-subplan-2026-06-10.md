# P53-M6 Subplan: Spatial SIR d=18 Calibration Row

metadata_date: 2026-06-10
phase: P53-M6
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Run the first production-like spatial SIR row at `d = 18` only after the
scaling route and rank integration pass.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repaired scaling route run the P51/P52-blocked d=18 spatial SIR row under the 32 GB practical memory contract? |
| Baseline/comparator | P53-M4D scaling-route admission, P53-M5 rank selection, P52 memory budget, P52 UKF scout, and feasible higher-rank same-route comparator. |
| Primary pass criterion | d=18 completes or blocks the declared rank ladder with finite values, available gradient diagnostics, deterministic replay, memory metadata, and explicit claim class. |
| Veto diagnostics | `PASS_P53_M4D_SCALING_ROUTE_ADMISSION` missing; dense all-pairs route used; memory cap exceeded; UKF used as truth; finite value alone promoted to correctness; HMC readiness claimed. |
| Not concluded | No production HMC readiness and no exact posterior correctness. |

## Planned Work

1. Preflight scaling route and memory metadata for `d=18`.
2. Run UKF scout only as scale/center sanity.
3. Run candidate ranks truncated by `r_max`.
4. Compare to lower-rung evidence and feasible same-route higher-rank
   deterministic comparator.
5. Emit selected rank or blocker.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m6-spatial-sir-d18-result-2026-06-10.md`

Required token:

`PASS_P53_M6_SPATIAL_SIR_D18` or `BLOCK_P53_M6_SPATIAL_SIR_D18`
