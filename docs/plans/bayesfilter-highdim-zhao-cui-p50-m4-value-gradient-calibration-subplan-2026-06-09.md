# P50-M4 Subplan: Value And Gradient Calibration Rules

metadata_date: 2026-06-09
phase: P50-M4
status: PLAN_REVIEW_CONVERGED

## Objective

Define and implement quantitative value and gradient comparison rules suitable
for HMC-facing filters, including model-generated likelihood variability and
directional-gradient diagnostics.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What error magnitudes are acceptable for values and gradients, and how are they measured without overtrusting finite differences? |
| Baseline/comparator | Exact/dense/Kalman/CUT4 references, autodiff gradients, regression-style directional finite differences, repeated-data likelihood variability. |
| Primary pass criterion | Calibration artifact and tests define value error, gradient norm error, directional cosine/error, likelihood variability normalization, veto diagnostics, and non-promotions. |
| Veto diagnostics | Single finite-difference check promoted as truth; value-only agreement promoted to gradient correctness; threshold chosen after seeing target results. |
| Not concluded | No HMC readiness or model-suite pass. |

## Planned Work

1. Write explicit value/gradient testing rules.
2. Add reusable calibration helper tests if needed.
3. Include likelihood variability normalization for generated datasets.
4. Ask Claude to critique the rules against numerical and HMC concerns.

## Repair Loop

Patch thresholds or diagnostics before using them as promotion criteria.  Stop
if the correct scientific criterion requires a new human decision.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p50-m4-value-gradient-calibration-result-2026-06-09.md`

Required token:

`PASS_P50_M4_VALUE_GRADIENT_CALIBRATION` or
`BLOCK_P50_M4_VALUE_GRADIENT_CALIBRATION`
