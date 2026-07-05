# Phase 3 Subplan: Generalized-SV Exact Source-Row Zhao-Cui Evaluator

Date: 2026-07-01

Status: `DRAFT_PENDING_PHASE2_REVIEW`

## Phase Objective

Freeze the exact source-row target for
`zhao_cui_generalized_sv_synthetic_from_estimated_values` and build or
precisely block its Zhao-Cui value/score evaluator.

## Entry Conditions Inherited From Previous Phase

- Phase 2 closed predator-prey Zhao-Cui status.
- Existing generalized-SV artifacts are context only until revalidated against
  this exact source-row target.
- Native oracle, precursor, auxiliary, actual-SV, and KSC evidence are not
  source-row admission evidence.

## Required Artifacts

- Exact generalized-SV source-row target contract.
- Evaluator route classification and implementation or blocker.
- Tests for target identity and score provenance.
- Regenerated leaderboard if row status changes.
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase3-generalized-sv-result-2026-07-01.md`
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- Target contract review before implementation.
- Finite value check if an evaluator exists.
- Manual analytical score tests if a derivative route exists.
- FD consistency and expected-score calibration if generated-data truth is
  available.
- Claude read-only review of target contract/result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the generalized-SV source row be tied to an exact Zhao-Cui evaluator and manual score route? |
| Baseline/comparator | Exact source-row target contract, not precursor/native-oracle/auxiliary/actual-SV/KSC evidence. |
| Primary criterion | Row is exact-source-row executed with finite value plus optional admitted manual score, or blocked with exact missing target/evaluator/derivative reason. |
| Veto diagnostics | Unsupported same-target claim; score without theta; autodiff analytical score; nonfinite value; stale generalized-SV assumptions. |
| Explanatory diagnostics | Value magnitude, score norm, FD residual, runtime. |
| Not concluded | No broad generalized-SV production readiness. |
| Artifact | Phase 3 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not promote auxiliary generalized-SV evidence as leaderboard admission.
- Do not use actual-SV or KSC evidence to admit this source row.
- Do not call a tape/autodiff score analytical.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 if generalized-SV has a reviewed target/evaluator status and
remaining blockers are precise enough for final leaderboard reporting.

## Stop Conditions

Stop if the target cannot be fixed without user scientific direction or if
older artifacts are too stale to support a safe target contract.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 3 result / close record.
3. Draft or refresh the Phase 4 subplan.
4. Review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
