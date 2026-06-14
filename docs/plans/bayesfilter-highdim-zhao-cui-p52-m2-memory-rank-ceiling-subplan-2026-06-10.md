# P52-M2 Subplan: Memory-Bounded Rank Ceiling Protocol

metadata_date: 2026-06-10
phase: P52-M2
status: PLAN_REVIEW_CONVERGED

## Objective

Implement a deterministic memory and rank-ceiling protocol before any spatial
SIR high-dimensional filtering run.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we compute a hard rank ceiling from a 32 GB practical memory cap before running a rank ladder? |
| Baseline/comparator | P51-M3 all-pairs count, P52 master memory policy, and existing TensorFlow/TFP backend constraints. |
| Primary pass criterion | A rank-ceiling implementation returns reproducible `r_max`, memory forecasts, and pass/block classifications for d=18, d=50, and d=100. |
| Veto diagnostics | Rank ladder allowed to grow beyond memory cap; state-core memory used as sole estimate; unknown `R_eff` ignored; d=100 run launched without preflight. |
| Not concluded | Memory feasibility does not prove accuracy, correctness, or HMC readiness. |

## Planned Work

1. Add a rank-budget data structure with fields for dimension, order, dtype
   bytes, `R_eff`, workspace multiplier, physical cap, algorithm cap, and
   single-step cap.
2. Implement deterministic formulas for `M_state`, `M_step`, and `r_max`.
3. Add conservative defaults: physical cap 32 GB, algorithm cap 16 GB,
   single-step cap 8 GB, rank candidates `{2, 4, 8, 16, 32}`.
4. Require an explicit `R_eff` source: measured lower-rung estimate, operator
   core estimate, or conservative declared bound.
5. Add tests for monotonicity: higher `d`, `R_eff`, or `omega` cannot increase
   `r_max`.
6. Emit a JSON rank-budget manifest for d=18/d=50/d=100.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m2-memory-rank-ceiling-result-2026-06-10.md`

Required token:

`PASS_P52_M2_MEMORY_RANK_CEILING` or
`BLOCK_P52_M2_MEMORY_RANK_CEILING`
