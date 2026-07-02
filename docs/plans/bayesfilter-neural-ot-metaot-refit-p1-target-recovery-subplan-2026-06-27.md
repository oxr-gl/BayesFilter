# P1 Subplan: One-Half Target And Recovery Contract

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact one-half latent target should BayesFilter predict to stay as close as possible to the Meta OT donor-core route, and how will the complementary half be recovered teacher-consistently? |
| Baseline/comparator | Meta OT donor-core decomposition from the completed source-faithful closure program and the current BayesFilter dual-pair retained-Sinkhorn route. |
| Primary pass criterion | A result artifact freezes the one-half target, the gauge/canonicalization policy, the complementary-half recovery path, and the new route vocabulary for teacher-data and deployment. |
| Veto diagnostics | Ambiguous target half; no explicit recovery path; hidden fallback to free prediction of both halves; gauge convention left unspecified. |
| Explanatory diagnostics | Convenience of one half vs the other, implementation aesthetics, and latent-loss convenience only. |
| Not concluded | P1 does not yet update code or train the new route. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-metaot-refit-p1-target-recovery-result-2026-06-27.md` |

## Required Actions

1. Choose the exact one-half latent target (`log_u` or `log_v`, or donor-equivalent notation).
2. Define the gauge/canonicalization rule under BayesFilter conventions.
3. Define the teacher-side complementary recovery path.
4. State what teacher-data fields remain necessary after the one-half refit.
5. State what deployment path must remain unchanged.

## Gate

P1 passes only when the target half and recovery rule are explicit enough for data-manifest and student-code refits.
