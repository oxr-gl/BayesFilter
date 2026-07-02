# P6 Subplan: Closeout And Extension Boundary

Date: 2026-06-27

## Status

`DRAFT_SCAFFOLD_AWAITING_P5`

## Dependency

This subplan must not be finalized until P5 produces the faithfulness audit verdict.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | After donor audit, port/decomposition, adapter design, and faithfulness audit, what exactly has BayesFilter closed, and what extension work is now allowed or still blocked? |
| Baseline/comparator | P5 faithfulness audit result and all prior program artifacts. |
| Primary pass criterion | A closeout result states one route verdict, one extension boundary, and one list of still-blocked claims/actions. |
| Veto diagnostics | Ambiguous verdict; reopening annealed extension or custom invention without a faithfulness classification; usefulness claims that outrun the audit verdict. |
| Explanatory diagnostics | Local metrics, engineering convenience, and follow-on experiment ideas. |
| Not concluded | P6 does not by itself prove the paper's effectiveness on all BayesFilter routes. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p6-closeout-result-2026-06-27.md` |

## Required Actions

1. State the final route verdict:
   - `SOURCE_FAITHFUL_ROUTE_CLOSED`
   - `FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`
   - `CUSTOM_EXTENSION_REQUIRED_SOURCE_FAITHFUL_CLOSURE_FAILED`
2. State what future work is allowed next.
3. State what claims remain blocked.

## Gate

P6 finalizes only after P5 resolves the route classification.
