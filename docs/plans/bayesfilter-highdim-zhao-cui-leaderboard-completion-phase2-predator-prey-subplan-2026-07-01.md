# Phase 2 Subplan: Predator-Prey T20 Zhao-Cui Evaluator Adapter

Date: 2026-07-01

Status: `DRAFT_READY_AFTER_PHASE1`

## Phase Objective

Build or precisely block the Zhao-Cui evaluator adapter for
`zhao_cui_predator_prey_T20`, using the T20 source-scope target only.

## Entry Conditions Inherited From Previous Phase

- Phase 1 closed actual-SV/KSC Zhao-Cui score statuses:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase1-sv-ksc-score-result-2026-07-01.md`.
- The July 1 highdim leaderboard artifact has been regenerated with admitted
  manual Zhao-Cui scores for actual-SV T1000 and KSC T1000.
- Current predator-prey Zhao-Cui row is blocked by
  `P8D_MODEL_SPECIFIC_NUMERIC_EVALUATOR_ADAPTER_REQUIRED`.
- P47 two-observation diagnostic fixtures are not admissible as the T20 row.

## Required Artifacts

- Predator-prey T20 target contract with theta coordinates and observations.
- Zhao-Cui evaluator adapter implementation or precise blocker result.
- Tests for target alignment and score provenance.
- Regenerated leaderboard if row status changes.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase2-predator-prey-result-2026-07-01.md`
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Target-alignment check proving no P47 two-observation diagnostic is reported
  as T20.
- Finite value smoke if adapter is implemented.
- Manual analytical score checks if a score is implemented.
- FD consistency and score-at-true calibration if simulator and truth are
  available.
- Claude read-only review of target contract/result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the predator-prey T20 Zhao-Cui row be executed under its real T20 target, or must it remain blocked with a precise adapter gap? |
| Baseline/comparator | Current blocked row and source-scope T20 target, not the P47 lower-rung fixture. |
| Primary criterion | Row is finite value/value+manual-score under T20 target, or blocked with exact missing value adapter or derivative adapter reason. |
| Veto diagnostics | P47 diagnostic reported as T20; no theta; autodiff analytical score; nonfinite value; target mismatch. |
| Explanatory diagnostics | FD residual, runtime, score norm. |
| Not concluded | No broad nonlinear production readiness or HMC convergence. |
| Artifact | Phase 2 result and regenerated leaderboard if changed. |

## Forbidden Claims And Actions

- Do not report P47 lower-rung values as `zhao_cui_predator_prey_T20`.
- Do not invent a Zhao-Cui route without classification.
- Do not admit tape/autodiff score as analytical.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 if predator-prey has an honest executed or blocked
Zhao-Cui status with target/evaluator/derivative gaps separated.

## Stop Conditions

Stop if the T20 target cannot be fixed without user direction, or if the only
available route is an unapproved diagnostic that would mislabel the row.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 2 result / close record.
3. Draft or refresh the Phase 3 subplan.
4. Review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
