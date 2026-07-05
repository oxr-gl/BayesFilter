# Phase 4 Subplan: Analytical Score Validation

Date: 2026-07-02

Status: `BLOCKED_BY_PHASE3_FULL_EVALUATOR_COMPLEXITY_GATE`

## Phase Objective

Validate the admitted analytical/manual SIR score with layered diagnostics:
local score identity, FD consistency, finite full-row behavior, and
score-at-true multi-seed calibration.

## Entry Conditions Inherited From Previous Phase

- Phase 3 did not provide a finite full-row value and analytical/manual score.
- Phase 3 blocker:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase3-full-evaluator-result-2026-07-02.md`.
- Score validation must not start until a reviewed full evaluator repair
  exists.

## Required Artifacts

- Score validation JSON/MD artifacts.
- Phase 4 result:
  `docs/plans/bayesfilter-parameterized-sir-leaderboard-repair-phase4-score-validation-result-2026-07-02.md`
- Refreshed Phase 5 subplan.
- If Phase 3 remains blocked, a Phase 4 blocker result rather than validation
  outputs.

## Required Checks/Tests/Reviews

- Local analytical score tests.
- Confirm Phase 3 full evaluator admission exists before running FD,
  score-at-true, or GPU/XLA checks.
- If admission does not exist, write blocker and stop.
- Claude read-only review of the blocker or validation result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the analytical/manual SIR score consistent enough for leaderboard admission under the reviewed validation rule? |
| Baseline/comparator | Phase 3 evaluator output and Phase 1 target contract. |
| Primary pass criterion | Score-at-true mean passes the declared uncertainty rule and no veto diagnostic fails, but only after Phase 3 admits a finite full-row value and analytical/manual score. |
| Veto diagnostics | Nonfinite score; score provenance not analytical/manual; branch mismatch; failed local identity; score-at-true outside rule. |
| Explanatory diagnostics | FD consistency, runtime, GPU/XLA timing. |
| Not concluded | No proof of unbiasedness, no exact likelihood claim, no HMC posterior correctness. |
| Artifact | Phase 4 validation result. |

## Forbidden Claims/Actions

- Do not use FD agreement alone as promotion.
- Do not use one seed as production evidence.
- Do not reinterpret a failed score-at-true diagnostic after seeing results.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if Phase 4 admits the analytical/manual score or writes
a blocker that prevents leaderboard regeneration.

## Stop Conditions

Stop if score-at-true fails, if multi-seed generation is too expensive without
a smaller reviewed diagnostic, if GPU/HMC checks need external setup, or if
Phase 3 has not admitted a full-row value/score.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 4 result or blocker.
3. Draft or refresh Phase 5 subplan.
4. Review Phase 5 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
