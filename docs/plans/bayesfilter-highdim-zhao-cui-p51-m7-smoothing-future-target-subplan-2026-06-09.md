# P51-M7 Subplan: Smoothing Future-Target Decision

metadata_date: 2026-06-09
phase: P51-M7
status: PLAN_REVIEW_CONVERGED

## Objective

Keep smoothing separate from parameter-HMC filtering and decide whether a future
latent-path inference program is needed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Should P51 implement smoothing now, or preserve it as a future target requiring backward conditionals and weights? |
| Baseline/comparator | P50-M8 smoothing boundary, `SourceRouteSmoothingBoundary`, and P49 smoothing boundary tests. |
| Primary pass criterion | Smoothing remains deferred with explicit future requirements, or a separate future master program is drafted if latent-path inference is requested. |
| Veto diagnostics | Filtering/HMC pass tokens imply smoothing support; smoother support claimed without backward conditional maps, backward weights, and smoothing marginal checks. |
| Not concluded | No smoothing support unless a separate smoother implementation phase is approved and tested. |

## Planned Work

1. Re-audit smoothing nonclaims after P51 phases.
2. Add or update guard tests if any phase drifted.
3. Record whether smoothing remains deferred or becomes a future program.

## Repair Loop

Patch nonclaims or guard tests if smoothing drift appears. Stop for a new
human decision to implement latent-path inference now.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-result-2026-06-09.md`

Required token:

`PASS_P51_M7_SMOOTHING_FUTURE_TARGET` or `BLOCK_P51_M7_SMOOTHING_FUTURE_TARGET`

Required manifest:

`docs/plans/bayesfilter-highdim-zhao-cui-p51-m7-smoothing-future-target-manifest-2026-06-09.json`
