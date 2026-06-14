# P49-M4 Subplan: Recentring, Jacobian, And Normalizer Accounting

metadata_date: 2026-06-09
phase: P49-M4
status: PLAN_REVIEW_CONVERGED

## Objective

Repair R5 by verifying the source-style weighted affine recentering,
determinant/Jacobian terms, target shifting constants, and log-normalizer
updates.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are coordinate transforms and normalizers accounted for exactly in the source-faithful lane? |
| Baseline/comparator | Source `computeL`, `L_temp`, `mu_temp`, `const`, `log(sirt.z) - const`; analytic affine Gaussian tests. |
| Primary pass criterion | Affine Gaussian and nonlinear one-step tests pass moment, determinant, and log-normalizer checks. |
| Veto diagnostics | Missing `log(abs(det(L)))`; target shift changes likelihood; recentering chosen after result inspection. |
| Not concluded | No production target tuning. |

## Planned Work

1. Create analytic affine-transform fixtures.
2. Verify determinant accounting independently from TT fitting.
3. Verify source-style target shift affects numerical stability only, not the
   final likelihood.
4. Add result manifest fields for `mu`, `L`, determinant, shift constant, and
   normalizer contribution.

## Repair Loop

If determinant or shift accounting fails, stop the phase gate and repair before
running larger model phases.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p49-m4-recentering-normalizer-result-2026-06-09.md`
