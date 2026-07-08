# P2 Subplan: Teacher-Data And Manifest Refit

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How should the current retained-Sinkhorn teacher-data path be refit so it supports Meta OT-aligned one-half training while preserving BayesFilter manifests, heldout splits, and replay diagnostics? |
| Baseline/comparator | Current teacher-data runner and the P1 one-half target/recovery contract. |
| Primary pass criterion | A result artifact freezes the updated teacher-data fields, manifest fields, split policy, and replay/recovery checks required before student refit. |
| Veto diagnostics | Losing teacher replay artifacts; losing manifests or reproducibility digests; keeping only pair-regression-oriented targets; ambiguous relation between stored half-target and recovered complementary half. |
| Explanatory diagnostics | Dataset size, file layout, and compactness only. |
| Not concluded | P2 does not yet refit the student module. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-metaot-refit-p2-teacher-data-result-2026-06-27.md` |

## Required Actions

1. Update the teacher-data contract from dual-pair emphasis to one-half donor-aligned emphasis.
2. Preserve enough information to recover and replay the corrected teacher route.
3. Keep BayesFilter reproducibility manifests and heldout split rules explicit.
4. State any compatibility bridge needed so older local pair-based artifacts are not confused with the refit route.

## Gate

P2 passes only when teacher-data artifacts are specified tightly enough to support P3 student/objective refit.
