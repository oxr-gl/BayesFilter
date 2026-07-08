# Phase 5 Subplan: Leaderboard Regeneration

Date: 2026-07-02

Status: `DRAFT_PENDING_PHASE4`

## Phase Objective

Regenerate the high-dimensional two-lane leaderboard so the parameterized SIR
row appears with admitted analytical/manual score evidence and correct
nonclaims.

## Entry Conditions Inherited From Previous Phase

- Phase 4 admits the analytical/manual score.
- Existing ready rows must be preserved unless current tests prove a real
  regression.

## Required Artifacts

- Updated leaderboard JSON/MD.
- Preservation-check JSON.
- Final semantic-binding artifact tying leaderboard row id, theta contract,
  evaluator route, and analytical/manual score provenance.
- Phase 5 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase5-leaderboard-regeneration-result-2026-07-02.md`
- Refreshed Phase 6 subplan.

## Required Checks/Tests/Reviews

- Leaderboard schema tests.
- Analytical-score provenance tests.
- Preservation tests for LGSSM, actual-SV, and KSC ready rows.
- Claude read-only review of final leaderboard result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the regenerated leaderboard correctly include the parameterized SIR analytical-score row without damaging existing admissions? |
| Baseline/comparator | July 2 leaderboard plus Phase 4 SIR validation artifacts. |
| Primary pass criterion | Final leaderboard and semantic-binding artifact contain the reviewed parameterized SIR row id, reviewed theta coordinate, reviewed truth theta, admitted analytical/manual score provenance, finite full observed-data/filtering value and score, binding to the reviewed target/evaluator route, and preservation of existing ready rows. |
| Veto diagnostics | Missing score provenance; FD/autodiff score admitted; old fixed row mislabeled; parameterized row has wrong id/theta/provenance; missing semantic binding; existing ready rows regress without explanation. |
| Explanatory diagnostics | Runtime and row summary tables. |
| Not concluded | No SGQF/UKF completion beyond tested rows, no HMC readiness unless separately reported. |
| Artifact | Final leaderboard JSON/MD and Phase 5 result. |

## Forbidden Claims/Actions

- Do not overwrite the old fixed row history without explicit decision.
- Do not rank rows whose correctness gate remains open.
- Do not compare the fixed source-parity SIR row and parameterized inference
  SIR row as the same target.
- Do not hide unresolved SGQF/UKF gaps.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if final leaderboard artifacts are generated, checked,
and reviewed, or if a blocker result identifies exactly what remains.

## Stop Conditions

Stop if regeneration changes unrelated rows unexpectedly, if tests reveal a
schema conflict, or if Claude and Codex do not converge on the final artifact.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 5 result or blocker.
3. Draft or refresh Phase 6 subplan.
4. Review Phase 6 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
