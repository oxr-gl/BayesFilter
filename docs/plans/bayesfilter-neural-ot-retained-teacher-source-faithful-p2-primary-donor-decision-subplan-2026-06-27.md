# P2 Subplan: Primary Donor Decision

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Given the audited donor evidence from P1, which single donor route should BayesFilter treat as the primary source-faithful target for retained-teacher neural OT: Meta OT or UNOT? |
| Baseline/comparator | The P1 donor-anchor audit result, the earlier fit note, and the retained-teacher chapter definition in `docs/chapters/ch32d_retained_teacher_neural_ot.tex`. |
| Primary pass criterion | A decision result chooses exactly one primary donor, explicitly defers the other, and records the reasons in terms of predicted object match, retained correction semantics, adaptation burden, and route fit. |
| Veto diagnostics | No forced donor decision; trying to keep both donors active at once; choosing on vague preference rather than the audited comparison table; silently mixing donor concepts before a decision. |
| Explanatory diagnostics | Secondary strengths of the deferred donor, optional future value, and unresolved donor-specific risks. |
| Not concluded | P2 does not yet port code or prove source faithfulness. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p2-primary-donor-decision-result-2026-06-27.md` |

## Required Actions

1. Read the P1 donor comparison table.
2. Choose one primary donor route only.
3. Explicitly defer the other donor route.
4. Record the decision with at least these fields:
   - predicted-object fit,
   - retained correction semantics fit,
   - deployment-object fit,
   - framework adaptation burden,
   - route mismatch risk,
   - justification for why the deferred donor is not first.
5. State the precise P3 target: the donor repo path to decompose or port first.

## Skeptical Audit

| Risk | Control |
| --- | --- |
| False comfort from keeping both donors alive | Force exactly one primary donor and one deferred donor. |
| Decision smuggles in BayesFilter custom design again | Use donor-audit fields only: object, correction semantics, deployment object, adaptation burden, route fit. |
| Deferred donor forgotten entirely | Record what evidence would justify returning to it later. |

## Gate

P2 passes only when a single donor is chosen and the P3 target is unambiguous.
