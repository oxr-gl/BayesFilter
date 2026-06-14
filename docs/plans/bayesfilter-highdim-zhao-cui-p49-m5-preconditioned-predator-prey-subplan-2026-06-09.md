# P49-M5 Subplan: Preconditioned Predator-Prey Repair

metadata_date: 2026-06-09
phase: P49-M5
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R6 by treating P47 M5b as a fixed-design route failure, then building a
scientific ladder for the source-style preconditioned/residual route.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a source-style full/preconditioned route repair the predator-prey gap relative to fixed-design BayesFilter? |
| Baseline/comparator | P47 M5b fixed-design result; source `pre_sol.m`; dense/high-order references at short horizon. |
| Primary pass criterion | Horizon and ablation ladder separates route mismatch, tuning failure, and evidence against the idea. |
| Veto diagnostics | P47 fixed-design failure interpreted as source failure; preconditioner target equality unchecked; tolerance loosened after results. |
| Not concluded | No paper-scale predator-prey production token unless the ladder passes. |

## Planned Work

1. Specify supported preconditioner variant order.
2. Add target-equality checks for preconditioner and residual target.
3. Run short-horizon dense/reference comparisons before longer ladders.
4. Compare fixed branch, full source-faithful route, and preconditioned route.

## Repair Loop

Condition-number or tuning failures are engineering blockers, not scientific
negative results.  Write a repair amendment and get Claude review before
changing windows, ranks, or tolerances.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m5-preconditioned-predator-prey-result-2026-06-09.md`
