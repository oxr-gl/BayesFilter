# P86 Phase 7 Subplan: Correctness Bridge

Date: 2026-06-24

Status: `CLOSED_BLOCKER_PATH_BY_REVIEWED_PHASE6`

## Phase Objective

Build or block a source-backed same-target reference bridge for interpreting
author-route SIR correctness beyond fit and rank stability.

Because Phase 6 currently blocks rank/degree convergence, the default Phase 7
execution path is a blocker/deferral closeout rather than a correctness-bridge
runtime path. A bridge cannot promote the candidate while the convergence gate
is unresolved.

## Entry Conditions Inherited From Previous Phase

- Phase 6 produced an admissible same-route rank-5 comparator fit artifact, but
  rank convergence is not established.
- Degree convergence is blocked pending a reviewed configurable-basis execution
  path.
- Phase 7 is therefore explicitly reframed as a bridge blocker/deferral unless
  a later human-approved repair program resolves Phase 6 first.
- Target convention, observation setup, seeds, and reference-comparator scope
  are frozen.

## Required Artifacts

- Reference/bridge manifest only if a reviewed Phase 6 repair reopens the
  bridge path; otherwise no bridge runtime artifact is required.
- Correctness-bridge ledger with allowed and forbidden claims.
- Phase 7 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p86-phase7-correctness-bridge-result-2026-06-24.md`
- Updated execution ledger and refreshed Phase 8 subplan.

## Required Checks / Tests / Reviews

- Confirm the Phase 6 result status and convergence ledger.
- If Phase 6 remains blocked, run doc/claim checks only and write a blocker
  result; do not execute reference or bridge runtime commands.
- If a later reviewed Phase 6 repair passes, inspect author source and local
  target-convention code needed to identify the same SIR target before any
  bridge work.
- Claude read-only bounded review is required before any correctness-candidate
  interpretation or bridge status change.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can Phase 7 proceed to a same-target correctness bridge, or must it block because Phase 6 convergence is unresolved? |
| Baseline/comparator | Phase 6 convergence ledger, author source route, and any reviewed high-fidelity same-target reference only if Phase 6 is repaired. |
| Primary criterion | If Phase 6 is blocked, Phase 7 writes a precise blocker without runtime claims. If Phase 6 is later repaired, a bridge must be source-backed, same-convention, and predeclared before execution. |
| Veto diagnostics | Target convention mismatch; missing source anchors; weak proxy comparator; UKF/all-grid/operator route promoted as correctness; unapproved long command. |
| Explanatory diagnostics | Agreement residuals, uncertainty intervals, convention ledger, bridge limitations. |
| Not concluded | No production readiness without KR, derivative/HMC, comparator, scale, and final decision gates. |
| Artifact | Bridge manifest and Phase 7 result. |

## Forbidden Claims / Actions

- Do not use UKF or local all-grid/operator route as a correctness bridge.
- Do not claim exact likelihood or posterior correctness from proxy agreement.
- Do not run long or GPU/reference commands without exact approval.
- Do not use a correctness bridge to bypass unresolved rank/degree
  convergence.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin only if:

- correctness bridge status is precisely blocked/deferred unless Phase 6 is
  repaired first;
- current KR/transport production status is known and Phase 8 scope is
  refreshed.

## Stop Conditions

Stop if:

- Phase 6 remains blocked and the requested Phase 7 action would require a
  correctness claim or runtime bridge command;
- a same-target reference bridge cannot be anchored;
- bridge execution would require unapproved runtime or external resources;
- Claude and Codex do not converge after five review rounds.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 7 result / close record;
3. draft or refresh the Phase 8 subplan;
4. review the Phase 8 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
