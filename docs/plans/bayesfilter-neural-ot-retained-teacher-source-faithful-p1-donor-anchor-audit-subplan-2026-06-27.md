# P1 Subplan: Donor Source Anchor Audit

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter audit Meta OT and UNOT at the paper+official-repo level tightly enough to identify the exact learned object, retained correction mechanism, training/inference split, donor modules/functions, and major adaptation blockers before any further custom retained-teacher implementation proceeds? |
| Baseline/comparator | Current donor evidence in `docs/plans/bayesfilter-neural-ot-source-code-availability-ledger-2026-06-18.md`, `docs/plans/bayesfilter-neural-ot-implementation-fit-note-2026-06-18.md`, and conceptual route notes in `docs/chapters/ch32d_retained_teacher_neural_ot.tex`. |
| Primary pass criterion | A P1 result artifact records, for both Meta OT and UNOT, a paper anchor table, official repo anchor table, predicted object, retained correction/deployment semantics, training/inference split, framework/license/runability notes, and a first BayesFilter fit classification. |
| Veto diagnostics | No official repo anchor; no distinction between paper-level claim and repo-level implementation; no explicit predicted-object entry; no distinction between core algorithm and benchmark scaffolding; no license/framework notes. |
| Explanatory diagnostics | Repo layout, dependency stack, benchmark assets, model-weight availability, and convenience comments only. |
| Not concluded | P1 does not choose the primary donor and does not yet port code. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p1-donor-anchor-audit-result-2026-06-27.md` |

## Required Actions

1. Audit `Meta OT` and `UNOT` separately.
2. For each donor, record:
   - paper anchor(s),
   - official repo URL,
   - relevant source modules/functions,
   - exact learned/predicted object,
   - teacher/corrective mechanism,
   - deployment object,
   - training vs inference split,
   - framework/runtime assumptions,
   - available license / runability notes when visible,
   - first BayesFilter fit classification.
3. Distinguish clearly between:
   - paper claim,
   - repo implementation,
   - BayesFilter inference about portability.
4. Produce a side-by-side donor comparison table to feed P2.

## Skeptical Audit

| Risk | Control |
| --- | --- |
| Audit becomes abstract survey prose again | Require paper anchors and repo/module anchors in the same table. |
| Donor repos treated as monoliths | Separate core algorithm from benchmark/reproduction scaffolding. |
| Portability handwaving | Require explicit notes on framework, object, route, and license/runability constraints. |
| Hidden donor preference | Delay donor choice to P2; P1 is audit only. |

## Gate

P1 passes only when the result artifact provides a side-by-side donor table precise enough to support a forced donor choice in P2.
