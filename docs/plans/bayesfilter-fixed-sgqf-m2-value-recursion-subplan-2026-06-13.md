# Fixed-SGQF M2 Subplan: P47-Faithful Value Recursion

metadata_date: 2026-06-13
phase: M2
status: READY_FOR_IMPLEMENTATION

## Objective

Implement the Fixed-SGQF prediction/update/log-likelihood recursion on the declared p47 branch.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Fixed-SGQF value path be implemented with the declared Gaussian-surrogate moments, Cholesky branch, solve-based innovation algebra, and analytic additive-noise handling? |
| Baseline/comparator | p47 Gaussian-projection/value-recursion sections, one-step value-path contract, and implementation conventions; affine reference behavior from existing TF Kalman/sigma-point tests. |
| Primary pass criterion | The value path reproduces the p47 one-step numeric oracle, matches affine Gaussian references where the approximation should collapse to exact Gaussian projection, and vetoes invalid declared branches instead of silently repairing them. |
| Veto diagnostics | Additive noise is introduced by state augmentation; explicit inverses replace solve-based innovation algebra; Cholesky branch is replaced by eigen/SVD logic; jitter/floor/clipping silently changes the declared branch. |
| Not concluded | No score correctness claim yet and no broader benchmark-program admission claim. |

## Tasks

1. Add value-path routines to `bayesfilter/nonlinear/fixed_sgqf_tf.py` for predictive moments, observation moments, innovation statistics, Gaussian update, and accumulated log likelihood.
2. Keep the value path on the p47 branch: Cholesky factors only, solve-based innovation algebra only, additive `Q`/`R` inserted analytically only, symmetrize-then-veto only, with explicit predictive/innovation branch thresholds, initial-condition policy, and observation preprocessing policy recorded in diagnostics.
3. Reuse existing structural model fixtures from `bayesfilter/testing/nonlinear_models_tf.py` where possible; add the p47 scalar one-step oracle fixture and direct numeric tieout if the current fixtures are insufficient.
4. Add affine tieout, p47 one-step numeric oracle, and small nonlinear finite-value tests in `tests/test_fixed_sgqf_values_tf.py`.
5. Add explicit branch-veto coverage for non-positive-definite symmetrized covariance and innovation matrices.

## Required Checks

- `pytest -q tests/test_fixed_sgqf_values_tf.py`
- `pytest -q tests/test_fixed_sgqf_branch_contract_tf.py -k value`
- `rg -n "chol|solve|symmetrize|veto|Q_|R_" bayesfilter/nonlinear/fixed_sgqf_tf.py`
