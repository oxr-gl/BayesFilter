# Phase 2 Subplan: Predator-Prey T20 Non-Zhao-Cui Completion

Date: 2026-07-03

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Finalize the SGQF predator-prey T20 row and resolve UKF analytical-score
admission for the exact T20 row.

## Entry Conditions Inherited From Previous Phase

- Phase 1 closed the spatial SIR non-Zhao-Cui row status.
- The SGQF predator-prey row already has reviewed same-row candidate evidence.
- The UKF predator-prey row remains executed_value_only with autodiff-not-
  admitted score status in the authoritative artifact.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase2-predator-prey-result-2026-07-03.md`
- refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase3-generalized-sv-subplan-2026-07-03.md`
- exact predator-prey row contract / score provenance notes under `docs/plans`
- any focused implementation/test artifacts required by the reviewed executable refresh

## Required Checks/Tests/Reviews

This phase requires reviewed row-contract and executable-refresh artifacts before
any code edit or runtime.

Required read-only Claude reviews:

- predator-prey row contract or result artifact,
- optional executable refresh if runtime is admitted,
- refreshed Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 SGQF and UKF rows be tied to honest same-row value/analytical-score evaluators, or must one or both remain blocked/value-only with precise reasons? |
| Baseline/comparator | authoritative July 3 leaderboard artifact, reviewed predator-prey row contract, and existing SGQF/UKF predator-prey tests. |
| Primary criterion | The SGQF predator-prey row must either remain admitted at the reviewed row scope or be re-blocked precisely; the UKF predator-prey row becomes value+score only if an analytical/manual score route is admitted for the exact T20 row. |
| Veto diagnostics | lower-rung evidence promoted as T20 row admission; autodiff admitted as analytical; wrong-target scalar promotion; value-only row promoted as gradient evidence. |
| Explanatory diagnostics | value magnitude, score norm, same-branch FD checks, runtime, and row-specific gap notes. |
| Not concluded | No HMC readiness, no production/default claim, and no broad exactness claim beyond the reviewed T20 row. |
| Artifact | Phase 2 result and refreshed Phase 3 subplan. |

## Forbidden Claims And Actions

- Do not report lower-rung evidence as the T20 source-scope row.
- Do not admit autodiff provenance as analytical.
- Do not promote a value-only row as gradient evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if predator-prey SGQF/UKF statuses are either honestly
admitted or honestly blocked/value-only with precise next implementation gaps.
