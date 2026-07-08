# Phase 2 Subplan: Predator-Prey T20 SGQF Row Completion

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the exact SGQF row contract for `zhao_cui_predator_prey_T20` and either
implement or precisely block the source-scope predator-prey value/analytical-
score pair.

## Entry Conditions Inherited From Previous Phase

- Phase 1 closed the SIR SGQF row status.
- Lower-rung predator-prey SGQF evidence remains context only until revalidated
  against the T20 source-scope row.

## Required Artifacts

- SGQF predator-prey row contract:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-row-contract-2026-07-01.md`
- optional executable refresh, required only if the row contract admits a code/
  runtime path:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-executable-refresh-2026-07-01.md`
- Phase 2 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md`
- refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-01.md`
- exact authority inputs:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`
  - `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`
  - `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`
  - `tests/highdim/test_p47_predator_prey_filtering.py`
- any focused implementation/test artifacts required by the reviewed executable refresh

## Required Checks/Tests/Reviews

This phase requires a reviewed row contract before any implementation or
runtime. If implementation/runtime is admitted after the row contract is frozen,
this phase also requires a reviewed executable refresh before any code edit or
runtime.

Required read-only Claude reviews:

- SGQF predator-prey row contract,
- optional executable refresh if runtime/implementation is admitted,
- Phase 2 result,
- refreshed Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 SGQF row be tied to a reviewed same-row value/analytical-score evaluator, or must it remain blocked with a precise target/evaluator/derivative gap? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `tests/highdim/test_filtering_value_gradient_benchmark_source_paper_scope.py`, `docs/plans/bayesfilter-source-scope-sgqf-admission-ledger-2026-06-24.md`, `docs/plans/bayesfilter-source-scope-sgqf-analytical-gradient-ledger-2026-06-24.md`, and `tests/highdim/test_p47_predator_prey_filtering.py`. |
| Primary criterion | The row becomes `executed_value_score` only with a reviewed T20 source-row evaluator, finite value, analytical/manual score provenance tied to the same declared scalar, and an explicit reviewed statement of whether the admitted row is exact-target or approximate-but-explained; otherwise it remains blocked with a precise reason. |
| Veto diagnostics | lower-rung diagnostic evidence promoted as T20 row admission; autodiff admitted as analytical; wrong-target scalar promotion; wrong-target score promotion; or finite-difference / same-scalar evidence failing to support the admitted analytical score claim. |
| Explanatory diagnostics | value magnitude, score norm, runtime, and row-specific gap notes. Finite-difference residuals are explanatory only when the row contract explicitly records why they are not a validity gate; otherwise FD inconsistency is a repair trigger for analytical-score admission. |
| Not concluded | No HMC readiness, no production/default claim, and no broad SGQF claim beyond the reviewed T20 row. |
| Artifact | Phase 2 result and refreshed Phase 3 subplan. |

## Forbidden Claims And Actions

- Do not report lower-rung predator-prey evidence as the T20 source-scope row.
- Do not admit autodiff provenance as analytical.
- Do not promote a value-only row as gradient evidence.

## Analytical/Manual Provenance Rule

For this row, admitted analytical/manual score provenance must be supported by a
reviewed artifact that does all of the following:

- names the declared scalar being differentiated for the exact T20 row,
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

Advance to Phase 3 only if the predator-prey SGQF row is either honestly
admitted or honestly blocked with a precise next implementation gap.
