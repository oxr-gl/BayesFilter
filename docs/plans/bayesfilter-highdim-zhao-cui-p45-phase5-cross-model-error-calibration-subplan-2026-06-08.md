# P45-M5 Subplan: Cross-Model Error Calibration

metadata_date: 2026-06-08
phase: P45-M5

## Decision Target

Quantify value and gradient gaps for all P45 rows that reached same-target
comparison, and preserve blocker/nonclaim rows for those that did not.

## Evidence Contract

Question: are observed CUT4--Zhao-Cui differences small relative to reference
error, directional-gradient residuals, and likelihood-scale variability for
the declared tiny fixtures?

Primary criteria:

- every same-target row reports value gap, absolute score gap, relative score
  error, directional residuals, reference-refinement estimate, and claim
  class;
- every diagnostic-only row reports why equality metrics are absent;
- likelihood-scale or simulation-variance measures are explanatory unless a
  phase-specific statistical contract elevates them.

Veto diagnostics:

- likelihood variance is used to excuse systematic same-target bias without a
  reference check;
- finite-difference noise is treated as proof that gradients agree;
- long/high-dimensional conclusions are drawn from tiny fixtures.

## Implementation Steps

1. Collect M2--M4 comparison outputs.
2. Apply P42 value/gradient rule table.
3. Write a cross-model calibration result and update manifests.

## Required Artifacts

- Result note:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-result-2026-06-08.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-claude-review-ledger-2026-06-08.md`
- Evidence manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p45-phase5-cross-model-error-calibration-evidence-manifest-<run_id>.json`
- Command logs:
  `docs/plans/logs/<run_id>-P45-M5-command0.log` and subsequent command logs.
- Phase gate:
  `python scripts/p45_phase_gate.py --root /home/chakwong/BayesFilter --phase P45-M5 --token PASS_P45_M5_CODE_GOVERNANCE --run-id <run_id>`

## Claim Boundary

M5 interprets errors for tiny fixtures only.  It does not create HMC readiness
or production score API readiness.
