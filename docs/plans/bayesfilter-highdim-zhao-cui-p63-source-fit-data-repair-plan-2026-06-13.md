# P63 Plan: Source Fit-Data And computeL Repair

metadata_date: 2026-06-13
status: CREATED_FOR_EXECUTION
executor: Codex
reviewer: none; Claude intentionally left alone
predecessor: docs/plans/bayesfilter-highdim-zhao-cui-p62-defensive-tau-repair-result-2026-06-13.md

## Objective

Repair the next source-route discrepancy after P62: P59/P60 must derive the
affine coordinate frame and fixed-TTSIRT fit data from author-style propagated
weighted samples, not from an artificial local reference grid.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does replacing artificial reference-grid fit data with source-style pushed, weighted, recentered, resampled local fit data remove or move the P60 d=18 comparator blockers? |
| Baseline/comparator | Author `full_sol.m:21-130`, especially `push_samples`, `computeL`, `datasample`, `samples_unweighted`, `samples_debug`, `samples_init`, and `TTSIRT(..., 'var', deb)`. |
| Primary criterion | P59/P60 manifests show source-derived augmented samples, source `computeL` recentering, deterministic weighted resampling, local fit/debug split, and positive P62 defensive mass. Focused tests pass and d=18 comparator reruns. |
| Veto diagnostics | Continuing to fit from `_p59_author_sir_reference_points`; claiming algebraic-map parity; changing P60 thresholds to pass; treating one bounded low-sample diagnostic as paper-scale d=18 correctness. |
| Explanatory diagnostics | P60 log-marginal delta, normalizer-increment delta, probe-density delta, retained-density delta, ESS by step, fit-data manifest fields. |
| Nonclaims | No full `AlgebraicMapping(1)` domain parity, no adaptive Zhao-Cui parity, no full d=18 correctness, no d=50/d=100 scaling, no HMC production readiness. |

## Source Anchors

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:22-30`
  initializes prior samples, calls `push_samples`, and augments
  `[theta, x_t, x_{t-1}]`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:49-66`
  uses the propagated weighted `sam_new`, calls `computeL(sam_new, w2)`,
  and then `datasample(..., 'Weights', w2)`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84-99`
  applies `L_temp*x + mu_temp`, includes `-log(abs(det(L_temp)))`, computes
  `const`, maps resampled physical samples to local coordinates, splits
  `samples_debug` and `samples_init`, and passes `InputData` into `TTSIRT`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:1-35`
  defines weighted mean, weighted covariance, Cholesky jitter, optional
  quantile scale, and final `L`.
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/ssmodel.m:45-55`
  defines `push_samples`: process push, log-likelihood weight update, max
  subtraction, exponentiation, NaN-to-zero, and normalization.

## Skeptical Pre-Execution Audit

status: PASSED_FOR_SOURCE_FIT_DATA_REPAIR_ONLY

This plan targets the executable source dataflow around the fixed TTSIRT fit.
It does not claim the bounded fixed route is fully equivalent to the author's
`AlgebraicMapping(1)` domain.  It also does not weaken P60 thresholds.  A pass
means the immediate artificial-fit-data drift is removed; a remaining P60 block
will be recorded as the next source-fidelity or rank/capacity issue.

## Execution Steps

1. Add deterministic author-SIR source sample helpers:
   - prior sample batch from `model.initial_mean + chol(initial_covariance) * z`;
   - process push from `transition_push_from_standard_normal`;
   - observation likelihood weight update;
   - augmented `[theta, x_t, x_{t-1}]` batch.
2. Add deterministic weighted resampling for fixed-HMC replay:
   - equivalent role to source `datasample(..., 'Weights', w2)`;
   - deterministic quantile/systematic rule for branch stability;
   - manifest states it is a fixed-variant deterministic replacement for random
     MATLAB resampling.
3. Use `source_route_recenter` on the augmented physical samples:
   - `expansion_factor=4.0`, matching `epd_Lag = 4` in `eg3_sir/mainscript.m`;
   - keep current bounded fixed route and record nonclaim for algebraic domain.
4. Fit P59/P60 fixed TTSIRT from local resampled points:
   - `local = L^{-1}(sam_resampled - mu)`;
   - clip local points into the bounded basis domain only for this bounded
     fixed route and record clipping diagnostics;
   - compute target values at those local points using the recentered target.
5. Preserve P62 positive defensive tau.
6. Update tests and manifests.
7. Run focused CPU-only checks and d=18 comparator.

## Stop Conditions

Stop and record a blocker if:

- source-derived fit points are nonfinite;
- recentering fails Cholesky or determinant checks;
- all local points require clipping to the bounded domain;
- P60 high candidate again fails normalization;
- TensorFlow runtime prevents CPU-only tests from running.

