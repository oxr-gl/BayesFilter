# DPF5 Benchmark Ladder Matrix

## Status

DPF5 execution artifact.  This matrix defines the benchmark ladder; it does not
run benchmarks.

## Matrix

| Rung | Candidate(s) | Comparator | Metrics | Promotion criterion | Veto diagnostics | Not concluded |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | Import boundary | N/A | `rg` import search | no student imports in production/tests | any student-baseline import | No numerical claim. |
| L1 | Bootstrap/SIR PF | Kalman LGSSM | mean/variance/log-likelihood residuals, MCSE | residuals finite and within declared tolerance/uncertainty | non-finite weights, ambiguous likelihood object | No differentiable DPF claim. |
| L2 | Affine flow/PF-PF | Analytic affine density ratio | forward/inverse/log-det/corrected-weight residuals | deterministic residuals within tolerance | sign or normalization mismatch | No nonlinear flow correctness. |
| L3 | Soft resampling | Closed-form soft reference and categorical comparison | affine residual, nonlinear delta | affine residual pass; nonlinear bias labeled | "unbiased" without observable scope | No posterior preservation. |
| L4 | Sinkhorn/EOT | Manual balanced marginal reference | row/column/mass/nonnegative/finite residuals | final-budget residual pass | missing epsilon/budget/stabilization | No categorical equivalence. |
| L5 | Same-scalar gradient | Analytic or finite-difference scalar | value repeat, gradient repeat, FD residual | same-scalar parity pass | mismatched scalar/value path | No HMC convergence. |
| L6 | PF-PF controlled nonlinear | Range-bearing fixture | finite outputs, proxy RMSE, ESS, runtime | finite structured rows after lower vetoes pass | treating proxy as correctness | No posterior/production claim. |
| L7 | Student/controlled comparison | Frozen aggregate rows | same qualitative regime | explanatory only | student agreement used as validation | No BayesFilter correctness. |
| L8 | Runtime envelope | Candidate methods after veto pass | wall time, memory, device | bounded runtime under stated setup | runtime-only ranking after veto fail | No default-readiness. |

## Baseline Ladder Principle

Any future method comparison should include:

- naive/classical baseline where applicable;
- best tuned classical baseline available under the same fixture;
- plain proposed DPF component;
- enhanced proposed DPF component only after the plain component passes vetoes.

Weak or convenient-only baselines must be justified in the phase plan.
