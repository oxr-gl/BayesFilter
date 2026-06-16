# P71 Phase 2 Subplan: d18 Execution-Only Reproduction

metadata_date: 2026-06-16
status: DRAFT_PENDING_PHASE1_RESULT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2

## Phase Objective

Reproduce the d18 execution-only route after the Phase 1 condition-veto gate,
recording finite values, ESS, normalizer increments, correction-weight ranges,
branch hashes, and nonclaims.

## Entry Conditions Inherited From Previous Phase

- Phase 1 preserves condition-veto diagnostics or otherwise proves the current
  d18 execution-only route can run without hiding first-row failures.
- Phase 1 did not weaken source-route gates or thresholds.

## Required Artifacts

- Phase 2 result note.
- Machine-readable JSON manifest for the execution-only run.
- Updated Phase 3 subplan with exact evaluator/value commands.

## Required Checks/Tests/Reviews

- Run the smallest reviewed local command that exercises
  `p59_author_sir_validation_ladder(tier="d18_execution_only")`.
- Focused pytest for P59 execution-only ladder.
- `git diff --check` over new artifacts.
- Claude review if the run changes the Phase 3 evaluator contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the source-anchored fixed route still execute at d18 after the condition-veto capture gate? |
| Baseline/comparator | Existing P59-9e/P8-B6 execution-only evidence. |
| Primary criterion | Finite log marginal likelihood, finite normalizer increments, ESS reported for each step, branch hashes present, and nonclaims preserved. |
| Veto diagnostics | Nonfinite values, missing branch hashes, missing source anchors, missing nonclaims, or condition-veto diagnostics hidden by exception. |
| Explanatory diagnostics | ESS, correction-weight ranges, normalizer increments, wall time, memory, branch hashes. |
| Not concluded | No d18 filtering accuracy, no same-route rank convergence, no correctness, no scaling, no HMC readiness. |
| Artifact | Phase 2 result note and JSON manifest. |

## Forbidden Claims/Actions

- Do not interpret execution-only pass as accuracy or rank convergence.
- Do not run d50/d100.
- Do not change thresholds after seeing output.

## Exact Next-Phase Handoff Conditions

Phase 3 may begin only if Phase 2 records finite execution-only evidence and
explicitly preserves the nonclaims.  Otherwise Phase 3 is blocked.

## Stop Conditions

Stop if execution-only d18 fails with nonfinite values, missing source anchors,
or unpreserved diagnostic failures.
