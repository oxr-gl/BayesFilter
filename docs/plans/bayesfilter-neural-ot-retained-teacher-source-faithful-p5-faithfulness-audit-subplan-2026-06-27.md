# P5 Subplan: Faithfulness Audit

Date: 2026-06-27

## Status

`DRAFT_SCAFFOLD_AWAITING_P4`

## Dependency

This subplan must not be finalized until P4 freezes the BayesFilter adapter boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the resulting BayesFilter retained-teacher route count as source-faithful, fixed adaptation, or extension/invention relative to the chosen donor? |
| Baseline/comparator | Paper anchors, donor repo anchors, and the P4 adapter design. |
| Primary pass criterion | A paper→repo→BayesFilter obligation table classifies every implementation-relevant deviation and supports a single route verdict. |
| Veto diagnostics | Missing donor anchors; missing deviation table; calling the route faithful while major semantic deviations remain unlabeled. |
| Explanatory diagnostics | Local training results, runtime, and convenience differences. |
| Not concluded | P5 does not yet claim broad usefulness or production readiness. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p5-faithfulness-audit-result-2026-06-27.md` |

## Required Actions

1. Build the paper→repo→BayesFilter obligation table.
2. For each deviation classify:
   - `source_faithful`
   - `fixed_adaptation`
   - `extension_or_invention`
3. Record any unresolved blockers that prevent full source-faithful closure.

## Gate

No source-faithful closeout without the full deviation ledger.
