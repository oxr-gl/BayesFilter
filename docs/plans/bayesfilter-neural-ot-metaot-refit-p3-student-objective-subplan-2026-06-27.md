# P3 Subplan: Student And Objective Refit

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How should BayesFilter refit the current retained-Sinkhorn student and training path so it predicts one donor-style dual half and supports a donor-faithful objective-based route? |
| Baseline/comparator | Current `SinkhornWarmStartStudentTF` route and the P1/P2 target/data contracts. |
| Primary pass criterion | A result artifact records the code-level refit design for the student module, complementary recovery, objective-based training path, and compatibility boundary versus the old dual-pair route. |
| Veto diagnostics | Hidden full dual-pair prediction retained as the default; no donor-style objective path; corrected deployment semantics broken; route drift into annealed logic. |
| Explanatory diagnostics | Parameter counts, architectural minimalism, and training convenience only. |
| Not concluded | P3 does not yet decide final heldout success. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-metaot-refit-p3-student-objective-result-2026-06-27.md` |

## Required Actions

1. Define the student-module refit.
2. Define how complementary dual recovery is threaded into deployment.
3. Define the donor-faithful objective-based training path.
4. State how the old dual-pair route remains available for historical comparison but no longer defines the new donor-aligned path.

## Gate

P3 passes only when the refit design is precise enough for implementation and focused training checks.
