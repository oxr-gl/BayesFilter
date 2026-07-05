# Phase 1 Subplan: Spatial SIR SGQF Row Contract And Evaluator Status

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Freeze the exact SGQF row contract for `zhao_cui_spatial_sir_austria_j9_T20`
and either implement or precisely block the SGQF value/analytical-score route
for the full observed-data row.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch package is reviewed closed.
- The current July 1 leaderboard artifact marks the SIR SGQF row as blocked.
- Existing local complete-data or sidecar evidence is context only and must not
  be promoted as full observed-data/filtering leaderboard admission.

## Required Artifacts

- SGQF SIR row contract:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-row-contract-2026-07-01.md`
- optional executable refresh, required only if the row contract admits a code/
  runtime path:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-executable-refresh-2026-07-01.md`
- Phase 1 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase1-sir-result-2026-07-01.md`
- refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-01.md`
- exact authority inputs:
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`
  - `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`
  - `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`
  - `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`
  - `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`
- any focused implementation/test artifacts required by the reviewed executable refresh

## Required Checks/Tests/Reviews

This phase requires a reviewed row contract before any implementation or
runtime. If implementation/runtime is admitted after the row contract is frozen,
this phase also requires a reviewed executable refresh before any code edit or
runtime.

Required read-only Claude reviews:

- SGQF SIR row contract,
- optional executable refresh if runtime/implementation is admitted,
- Phase 1 result,
- refreshed Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the spatial SIR SGQF row be tied to a real full observed-data value/analytical-score route, or must it remain blocked with a precise missing-evaluator / no-free-theta reason? |
| Baseline/comparator | `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.json`, `docs/plans/bayesfilter-two-lane-highdim-leaderboard-results-2026-07-01.md`, `docs/plans/bayesfilter-leaderboard-repair-phase5-sir-d18-row-result-2026-06-30.md`, `docs/plans/bayesfilter-filtering-value-gradient-benchmark-source-paper-scope-contract-2026-06-11.json`, and `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase9-final-decision-result-2026-06-29.md`. |
| Primary criterion | The row becomes `executed_value_score` only with finite value, reviewed full-row target/evaluator contract, free-theta declaration, and analytical/manual score provenance tied to the same declared scalar; otherwise it remains blocked with a precise reason. |
| Veto diagnostics | local complete-data evidence promoted as full filtering; no-free-theta row emitted with score; autodiff admitted as analytical; wrong-target scalar promotion; or finite-difference / same-scalar evidence failing to support the admitted analytical score claim. |
| Explanatory diagnostics | value magnitude, score norm, runtime, and row-specific gap notes. Finite-difference residuals are explanatory only when the row contract explicitly records why they are not a validity gate; otherwise FD inconsistency is a repair trigger for analytical-score admission. |
| Not concluded | No HMC readiness, no production/default claim, and no broad source-faithful SGQF claim beyond the reviewed row contract. |
| Artifact | Phase 1 result and refreshed Phase 2 subplan. |

## Forbidden Claims And Actions

- Do not treat sidecar/local-complete-data evidence as full observed-data/filtering row admission.
- Do not emit a score row if the row still has no admitted free theta / derivative contract.
- Do not admit autodiff provenance as analytical.

## Analytical/Manual Provenance Rule

For this row, admitted analytical/manual score provenance must be supported by a
reviewed artifact that does all of the following:

- names the declared scalar being differentiated for this exact row,
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

Advance to Phase 2 only if the SIR SGQF row is either honestly admitted or
honestly blocked with a precise next implementation gap.
