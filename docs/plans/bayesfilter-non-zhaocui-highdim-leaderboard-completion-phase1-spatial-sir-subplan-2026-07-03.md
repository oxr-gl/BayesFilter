# Phase 1 Subplan: Spatial SIR Non-Zhao-Cui Row Contract And Status

Date: 2026-07-03

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Decide whether the non-Zhao-Cui spatial SIR main row remains blocked/value-only
or can advance under a reviewed row contract without promoting sidecar evidence
as main-row evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline package is reviewed closed.
- The July 3 authoritative leaderboard artifact preserves the current SIR row
  states.
- P91 sidecar/local complete-data evidence remains context only until a reviewed
  main-row contract says otherwise.

## Required Artifacts

- Phase 1 result:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase1-spatial-sir-result-2026-07-03.md`
- refreshed Phase 2 subplan:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase2-predator-prey-subplan-2026-07-03.md`
- exact authority inputs and any row contract notes written under `docs/plans`

## Required Checks/Tests/Reviews

This phase requires a reviewed row contract before any implementation or
runtime. If a runtime path is admitted, it requires a reviewed executable
refresh before any code edit or runtime.

Required read-only Claude reviews:

- row contract or result artifact,
- optional executable refresh if runtime is admitted,
- refreshed Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the non-Zhao-Cui spatial SIR main row be tied to a real full observed-data value/analytical-score route, or must it remain blocked/value-only with a precise missing-evaluator / no-free-theta reason? |
| Baseline/comparator | authoritative July 3 leaderboard artifact, prior SIR blocker artifacts, and any reviewed main-row contract. |
| Primary criterion | The row either stays honestly blocked/value-only with precise reasons, or becomes executed only with a reviewed full-row contract and the same value-before-gradient discipline. |
| Veto diagnostics | sidecar/local complete-data evidence promoted as full row; no-free-theta row emitted with score; autodiff admitted as analytical; wrong-target scalar promotion. |
| Explanatory diagnostics | value magnitude, score norm, runtime, and row-specific gap notes. |
| Not concluded | No HMC readiness, no production/default claim, and no sidecar-to-main-row promotion without reviewed authority. |
| Artifact | Phase 1 result and refreshed Phase 2 subplan. |

## Forbidden Claims And Actions

- Do not treat local complete-data sidecar evidence as full observed-data leaderboard row admission.
- Do not emit a score row if the main row still has no admitted free-theta / derivative contract.
- Do not admit autodiff provenance as analytical.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if the spatial SIR non-Zhao-Cui row is either honestly
advanced or honestly preserved as blocked/value-only with a precise next gap.
