# Phase 2 Subplan: Dataset Row Contract Repair

Date: 2026-07-02

Status: `READY_AFTER_PHASE1`

## Phase Objective

Implement the reviewed parameterized SIR dataset row contract while preserving
the old fixed/no-free-theta row as fixed-target evidence unless Phase 1
explicitly authorizes replacement.

## Entry Conditions Inherited From Previous Phase

- Phase 1 target contract is reviewed and accepted.
- Theta coordinate and truth value are unambiguous.
- Source/adaptation classification is recorded.
- Phase 1 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase1-source-theta-contract-result-2026-07-02.md`.

## Required Artifacts

- Updated dataset generator/tests as needed.
- Regenerated dataset manifest if the generator owns the checked artifact.
- Dataset row id:
  `zhao_cui_spatial_sir_austria_j9_T20_parameterized_logscale`.
- Semantic binding refresh:
  `docs/plans/bayesfilter-parameterized-sir-semantic-binding-2026-07-02.md`.
- Phase 2 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase2-dataset-row-contract-result-2026-07-02.md`
- Refreshed Phase 3 subplan.

## Required Checks/Tests/Reviews

- Focused dataset manifest tests for both fixed and parameterized SIR rows.
- Static search proving no old `no_free_theta` expectation is silently applied
  to the new parameterized row.
- Emitter regeneration equality test must pass against committed/generated
  dataset manifest artifacts.
- Claude read-only review of the Phase 2 result if row semantics changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the dataset layer expose a parameterized SIR row with free theta without hiding the old fixed row? |
| Baseline/comparator | Phase 1 target contract and pre-repair P8 dataset manifest. |
| Primary pass criterion | New or repaired row has declared theta coordinate, truth theta, physical truth payload, and tests that fail if it regresses to `no_free_theta`. |
| Veto diagnostics | Old fixed row silently mutated without authorization; parameterized row missing truth theta; new row uses `no_free_theta`; manifest and tests disagree; dataset status count not updated. |
| Explanatory diagnostics | JSON summary hashes and domain diagnostics. |
| Not concluded | No evaluator score admission or leaderboard ranking. |
| Artifact | Phase 2 result and changed code/test paths. |

## Forbidden Claims/Actions

- Do not claim full filtering score is available from row-contract changes.
- Do not delete old fixed-row evidence unless explicitly authorized.
- Do not regenerate broad leaderboards unless required by the subplan.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if the parameterized row is generated and test-protected,
if the old fixed-row semantics are preserved, and if the semantic-binding draft
records the dataset row artifact fields needed for later admission.

## Stop Conditions

Stop if adding a row breaks downstream schemas, if current tests require a
human choice between replacement and addition, or if unrelated dirty changes
conflict with the dataset generator.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 2 result or blocker.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
