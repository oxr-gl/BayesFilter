# P49-M6 Subplan: Smoothing Boundary And Backward Conditionals

metadata_date: 2026-06-09
phase: P49-M6
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R7 by preventing filtering results from implying source-style smoothing,
and by defining the separate work needed for backward conditional maps.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are smoothing claims excluded or separately tested with source-style backward conditionals? |
| Baseline/comparator | Source `full_sol.smooth`, `pre_sol.smooth`, `smooth_t`; BayesFilter transport helpers. |
| Primary pass criterion | Artifacts forbid smoothing claims unless a dedicated smoother test passes; if implemented, conditional map round-trip and smoothing marginal tests exist. |
| Veto diagnostics | Filtering likelihood pass promoted to smoothing pass; backward weights omitted. |
| Not concluded | No smoothing implementation is required for filtering closeout unless explicitly scoped. |

## Planned Work

1. Add smoothing non-claim checks to route-governance artifacts.
2. Specify backward conditional map data requirements.
3. If implementing, start with tiny linear-Gaussian smoother references.

## Repair Loop

If smoothing is out of scope for a run, write an explicit blocked/deferred row
instead of silently implying it is covered.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m6-smoothing-boundary-result-2026-06-09.md`
