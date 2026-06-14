# P49-M1 Subplan: Source Route Contract

metadata_date: 2026-06-09
phase: P49-M1
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R2--R5 at the design-contract level before writing production code.
Specify the clean-room source-faithful route: augmented state, sample
propagation, ESS, recentering, TT/SIRT density/transport object, proposal
correction, and log-normalizer update.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact clean-room algorithm must BayesFilter implement to be source-faithful enough for filtering claims? |
| Baseline/comparator | Zhao--Cui source `full_sol.m`, `pre_sol.m`, `TTFun.cross`, `TTSIRT.marginalise`; P48 ledger. |
| Primary pass criterion | A source-route specification exists with operation order, data structures, shape contracts, normalizer accounting, and non-claims. |
| Veto diagnostics | Any design that keeps all-axes pairwise grids as the paper-scale route; any copied MATLAB code; any omitted determinant/proposal-correction term. |
| Not concluded | No numerical accuracy claim. |

## Planned Work

1. Build a source-to-clean-room operation table.
2. Define data classes and function boundaries for a future TF/TFP
   implementation.
3. Mark which parts are differentiable, non-differentiable, or adaptation-only.
4. Define exact/dense/Kalman reference tests for one-step validation.

## Repair Loop

If a source step cannot be mapped cleanly, mark it `test_required` or
`blocked_for_design`, then ask Claude to review whether this is honest.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m1-source-route-contract-result-2026-06-09.md`
