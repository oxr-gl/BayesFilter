# P52-M4 Subplan: Factorized Transition Route Contract

metadata_date: 2026-06-10
phase: P52-M4
status: PLAN_REVIEW_CONVERGED

## Objective

Specify and implement the first factorized transition-application contract that
replaces dense all-pairs retained-grid materialization for spatial SIR.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the spatial SIR transition be applied without materializing all `N^2` previous/current grid pairs while preserving deterministic replay and differentiability? |
| Baseline/comparator | P51-M3 dense route blocker, spatial SIR locality, existing multistate fixed-design tests, and P52-M2 memory budget. |
| Primary pass criterion | Static and dynamic route checks prove the new route does not allocate or imply dense all-pairs transition tensors for d=18, and exposes a measurable `R_eff` or conservative bound. |
| Veto diagnostics | Hidden dense pairwise tensor; nondeterministic route; non-TensorFlow implementation backend for differentiable path; no replay identity; no memory metadata. |
| Not concluded | Passing the route contract does not by itself prove filtering accuracy. |

## Planned Work

1. Inventory current all-axes route code and tests.
2. Define an allowed transition-route interface with:
   - streamed or local-neighborhood transition application;
   - TT/MPO-style operator cores or equivalent factorized contraction;
   - deterministic branch identity;
   - TensorFlow/TFP differentiability;
   - memory and `R_eff` metadata.
3. Add static tests that reject dense `N^2` route construction in production
   spatial SIR paths.
4. Add a d=18 preflight that reports projected memory below cap before any
   rank ladder.
5. Stop with a narrowed blocker if a valid factorized route cannot be specified
   without a new algorithm decision.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p52-m4-factorized-transition-route-result-2026-06-10.md`

Required token:

`PASS_P52_M4_FACTORIZED_TRANSITION_ROUTE` or
`BLOCK_P52_M4_FACTORIZED_TRANSITION_ROUTE`
