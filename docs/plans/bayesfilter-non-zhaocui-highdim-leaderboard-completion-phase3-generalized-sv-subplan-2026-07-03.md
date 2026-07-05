# Phase 3 Subplan: Generalized-SV Non-Zhao-Cui Row Contract And Status

Date: 2026-07-03

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Decide whether the non-Zhao-Cui generalized-SV row can advance honestly for SGQF
or UKF score admission, or whether it remains blocked/value-only with precise
same-row reasons.

## Entry Conditions Inherited From Previous Phase

- Phase 2 closed predator-prey non-Zhao-Cui row status.
- The SGQF generalized-SV row is currently blocked by missing same-row
  evaluator.
- The UKF generalized-SV row is currently executed_value_only with
  autodiff-not-admitted score status.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase3-generalized-sv-result-2026-07-03.md`
- refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase4-final-regeneration-subplan-2026-07-03.md`
- exact authority inputs and any generalized-SV row contract notes under `docs/plans`

## Required Checks/Tests/Reviews

This phase requires reviewed row-contract and executable-refresh artifacts before
any code edit or runtime.

Required read-only Claude reviews:

- generalized-SV row contract or result artifact,
- optional executable refresh if runtime is admitted,
- refreshed Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the non-Zhao-Cui generalized-SV row be tied to honest same-row value/analytical-score evaluators, or must SGQF remain blocked and UKF remain value-only with precise reasons? |
| Baseline/comparator | authoritative July 3 leaderboard artifact, reviewed generalized-SV target contracts, and current UKF/SGQF row states. |
| Primary criterion | The row either advances honestly with reviewed same-row value/score support, or remains blocked/value-only with exact reasons that preserve the source-row identity and approximate-vs-exact distinction. |
| Veto diagnostics | native-oracle/precursor/auxiliary evidence promoted as row admission; autodiff admitted as analytical; wrong-target scalar promotion; unexplained approximation gap. |
| Explanatory diagnostics | value magnitude, score norm, runtime, and row-specific gap explanation. |
| Not concluded | No HMC readiness, no production/default claim, and no broad generalized-SV admission beyond the reviewed row contract. |
| Artifact | Phase 3 result and refreshed Phase 4 subplan. |

## Forbidden Claims And Actions

- Do not promote native-oracle, precursor, or auxiliary evidence as main-row admission.
- Do not admit autodiff provenance as analytical.
- Do not leave a measured approximation gap unexplained at the reviewed claim level.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if the generalized-SV non-Zhao-Cui row is either
honestly advanced or honestly preserved as blocked/value-only with a precise
next gap.
