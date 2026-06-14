# P52-M6 Subplan: Spatial SIR d=18 Calibration Row

metadata_date: 2026-06-10
phase: P52-M6
status: PLAN_REVIEW_CONVERGED

## Objective

Run the first production-like spatial SIR row at `d = 18` (`J = 9`) only after
P52-M2 through P52-M5 have established memory budget, UKF scout, factorized
route, and fixed-rank selection protocol.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repaired fixed-rank factorized route run the P51-blocked d=18 spatial SIR target under the 32 GB practical memory contract? |
| Baseline/comparator | P51-M3 d=18 blocker, P52-M2 memory forecast, P52-M3 UKF scout, P52-M5 rank protocol, lower-rung dense spatial SIR references, and higher-rank deterministic run if feasible. |
| Primary pass criterion | d=18 completes the declared rank ladder or selects a fixed rank under cap with finite value, available gradient diagnostics, deterministic replay, calibrated comparison evidence, and explicit satisfaction of the P52 rank-ladder stop rules. |
| Veto diagnostics | Dense all-pairs route used; memory cap exceeded; rank grows beyond `r_max`; UKF used as truth; finite value alone promoted to correctness; HMC readiness claimed. |
| Not concluded | No production HMC readiness and no exact posterior correctness. |

## Planned Work

1. Preflight d=18 with memory budget and route checks.
2. Run UKF scout and record centers/scales/effective dimension.
3. Run rank ladder `{2, 4, 8, 16, 32}` truncated by `r_max`.
4. Compare against lower-rung references and the best feasible fixed-rank
   deterministic reference.
5. Record selected rank or blocker with memory, value, gradient, and replay
   evidence.

## d=18 Stop Conditions

This row must stop rather than continue rank growth when:

- `r_max` removes all candidate ranks;
- dense all-pairs transition construction appears in the execution path;
- no same-target dense/exact reference exists and no feasible higher-rank
  deterministic comparator remains under cap;
- two consecutive ranks produce nonfinite values, nonfinite gradients, memory
  vetoes, or diagnostics that worsen by more than a factor of two;
- the implementation route differs from the P30 documented route created by
  P52-M1.

If the row passes only against a higher-rank deterministic comparator, its claim
class is `rank_self_convergence`, not exact correctness.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m6-spatial-sir-d18-result-2026-06-10.md`

Required token:

`PASS_P52_M6_SPATIAL_SIR_D18` or
`BLOCK_P52_M6_SPATIAL_SIR_D18`
