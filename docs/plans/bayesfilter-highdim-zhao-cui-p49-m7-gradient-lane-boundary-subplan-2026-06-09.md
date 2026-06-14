# P49-M7 Subplan: Deterministic Gradient-Lane Contract

metadata_date: 2026-06-09
phase: P49-M7
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R8 by giving the fixed-branch lane its own honest evidence contract:
analytical gradients, branch replay, and HMC suitability are tested as a
gradient-bearing adaptation, not as source-faithful Zhao--Cui.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What evidence is required before the fixed branch is used for HMC or score-based inference? |
| Baseline/comparator | Existing P42/P43 validation rules; autodiff directional derivatives; exact/dense/CUT4 references where available. |
| Primary pass criterion | Branch replay, value-gradient consistency, likelihood variance calibration, and adaptation labels pass. |
| Veto diagnostics | Gradient necessity used to claim source fidelity; finite-difference instability used uncritically; adaptive random branches differentiated without contract. |
| Not concluded | Gradient-lane success does not prove source-faithful filtering accuracy. |

## Planned Work

1. Audit fixed-branch labels and result artifacts.
2. Strengthen value/gradient tests with scale-aware and variance-aware metrics.
3. Define what HMC readiness would require, without claiming it prematurely.
4. Compare gradient lane against source-faithful or exact references only for
   accuracy claims.

## Repair Loop

If gradients fail, classify as autodiff bug, branch mismatch, numerical
conditioning issue, or comparator instability.  Do not collapse these into a
single pass/fail story.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m7-gradient-lane-boundary-result-2026-06-09.md`
