# Phase 3 Subplan: Full Observed-Data Evaluator

Date: 2026-07-02

Status: `DRAFT_PENDING_PHASE2`

## Phase Objective

Wire the parameterized SIR row into a full observed-data/filtering value and
analytical/manual score evaluator, starting with the smallest horizon ladder
that can expose branch, target, and complexity failures.

## Entry Conditions Inherited From Previous Phase

- Parameterized row contract is implemented and test-protected.
- The row has a declared theta coordinate and truth theta.
- Phase 2 did not admit score values.

## Required Artifacts

- Updated evaluator/adapter code and tests if needed.
- Horizon ladder artifacts for horizon 0/1 and full `T=20`, or blocker JSON
  with exact complexity failure.
- Updated semantic-binding artifact tying evaluator route, theta contract, and
  analytical score implementation to the same target.
- Phase 3 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`
- Refreshed Phase 4 subplan.

## Required Checks/Tests/Reviews

- Focused unit tests for evaluator dispatch to `ParameterizedZhaoCuiSIRSSM`.
- Horizon 0/1 smoke with finite value and finite analytical score.
- Full `T=20` run or precise blocker.
- Claude read-only review for any evaluator route change or new approximation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the parameterized SIR row compute full observed-data/filtering value and analytical/manual score? |
| Baseline/comparator | Phase 2 row contract and existing local complete-data score components. |
| Primary pass criterion | Finite value and finite analytical/manual score for the declared parameterized row at truth theta, with semantic binding to the reviewed target and evaluator route. |
| Veto diagnostics | Nonfinite outputs; branch mismatch; target mismatch; complexity gate; score uses autodiff/FD provenance; missing semantic binding; unreviewed approximation route. |
| Explanatory diagnostics | Runtime, memory, FD diagnostic table, local score tests. |
| Not concluded | No exactness claim, no rank sufficiency claim, no HMC/GPU readiness claim. |
| Artifact | Phase 3 result and evaluator outputs. |

## Forbidden Claims/Actions

- Do not call an FD or tape gradient the leaderboard score.
- Do not bypass complexity gates by increasing budgets without recording the
  scientific and engineering question.
- Do not change the target after seeing numerical results.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if a full-row value and analytical score exist, or if a
blocker result records exactly why they do not and what repair is required.

## Stop Conditions

Stop if the full evaluator needs a new mathematical route not authorized by
Phase 1, if complexity grows beyond local resources without a reviewed smaller
diagnostic, or if analytical score provenance cannot be preserved.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 3 result or blocker.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
