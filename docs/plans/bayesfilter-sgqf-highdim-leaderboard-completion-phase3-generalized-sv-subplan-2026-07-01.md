# Phase 3 Subplan: Generalized-SV SGQF Source-Row Completion

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the exact SGQF row contract for
`zhao_cui_generalized_sv_synthetic_from_estimated_values` and either implement
or precisely block the source-row SGQF value/analytical-score pair.

## Entry Conditions Inherited From Previous Phase

- Phase 2 closed predator-prey SGQF row status.
- Native-oracle, precursor, auxiliary, actual-SV, and KSC evidence remain
  context only until revalidated against the exact generalized-SV source row.

## Required Artifacts

- SGQF generalized-SV row contract:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-row-contract-2026-07-01.md`
- optional executable refresh, required only if the row contract admits a code/
  runtime path:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-executable-refresh-2026-07-01.md`
- Phase 3 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-result-2026-07-01.md`
- refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase4-score-gate-subplan-2026-07-01.md`
- exact authority inputs:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`
  - `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`
  - `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md`
  - `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md`
  - `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-result-2026-07-01.md`
- any focused implementation/test artifacts required by the reviewed executable refresh

## Required Checks/Tests/Reviews

This phase requires a reviewed row contract before any implementation or
runtime. If implementation/runtime is admitted after the row contract is frozen,
this phase also requires a reviewed executable refresh before any code edit or
runtime.

Required read-only Claude reviews:

- SGQF generalized-SV row contract,
- optional executable refresh if runtime/implementation is admitted,
- Phase 3 result,
- refreshed Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generalized-SV SGQF source row be tied to a reviewed same-row value/analytical-score evaluator, or must it remain blocked with a precise target/evaluator/derivative gap? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `docs/plans/bayesfilter-filtering-value-gradient-benchmark-generalized-sv-testing-spec-2026-06-11.md`, `docs/plans/bayesfilter-generalized-sv-target-truth-source-scope-contract-2026-06-29.md`, `docs/plans/bayesfilter-generalized-sv-phase3-precursor-route-classification-result-2026-06-29.md`, `docs/plans/bayesfilter-generalized-sv-phase4-short-prefix-same-target-value-gate-result-2026-06-29.md`, and `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase8-final-decision-result-2026-07-01.md`. |
| Primary criterion | The row becomes `executed_value_score` only with a reviewed source-row evaluator, finite value, analytical/manual score provenance tied to the same declared scalar, and an honest explicit statement of whether the admitted route is exact-target or approximate-but-explained; otherwise it remains blocked with a precise reason. |
| Veto diagnostics | native-oracle/precursor/auxiliary evidence promoted as source-row admission; autodiff admitted as analytical; wrong-target scalar promotion; wrong-target score promotion; unexplained approximation gap; or finite-difference / same-scalar evidence failing to support the admitted analytical score claim. |
| Explanatory diagnostics | value magnitude, score norm, runtime, and row-specific gap explanation. Finite-difference residuals are explanatory only when the row contract explicitly records why they are not a validity gate; otherwise FD inconsistency is a repair trigger for analytical-score admission. |
| Not concluded | No HMC readiness, no production/default claim, and no source-row SGQF claim beyond the reviewed contract. |
| Artifact | Phase 3 result and refreshed Phase 4 subplan. |

## Forbidden Claims And Actions

- Do not promote native-oracle, precursor, or auxiliary evidence as source-row SGQF admission.
- Do not admit autodiff provenance as analytical.
- Do not leave a measured approximation gap unexplained at the reviewed claim level.

## Analytical/Manual Provenance Rule

For this row, admitted analytical/manual score provenance must be supported by a
reviewed artifact that does all of the following:

- names the declared scalar being differentiated for the exact source row,
- identifies the free-theta contract used by the row,
- identifies the derivative ownership route as one of:
  - hand-derived / manually coded score recurrence or formula,
  - paper-cited closed-form score mapped into repo notation,
  - manually coded derivative route checked against the same declared scalar,
- explicitly states that autodiff/`GradientTape`/finite differences are not the
  admitted score route,
- and records any supporting FD or score-at-true diagnostics only at their
  reviewed explanatory or repair-trigger role.

Negative definition alone is insufficient. A row cannot be admitted merely by
saying what the provenance is not; it must positively identify the admitted
manual/analytical route.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if the generalized-SV SGQF row is either honestly
admitted or honestly blocked with a precise next implementation gap.
