# P9 Ch34 Implementability Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P9 plan, rewritten `ch34`, P8 artifacts, Jia--Xin--Cheng 2012,
Jia--Xin--Cheng 2013, Singh et al. 2018, Julier--Uhlmann 1997,
Arasaratnam--Haykin 2009, `ch18_svd_sigma_point.tex`, and the scholarly
literature audit policy.

what_is_not_concluded: This ledger does not conclude exact nonlinear filtering,
posterior accuracy, HMC convergence, production readiness, NAWM readiness,
default readiness, GPU/XLA readiness, or broad machine certification.

## Implementability Standard

The P9 standard is: a coding agent should be able to implement the method from
the chapter alone without opening the original papers.  The chapter must define
inputs, outputs, dimensions, node/weight construction, filtering recursion,
likelihood scalar, gradient status, diagnostics, and HMC admissibility.

## Method Checklist

| Method | Inputs specified | Nodes/weights specified | Filtering connection | Pseudocode | Likelihood scalar | Gradient recursion | Diagnostics | P9 status |
|---|---|---|---|---|---|---|---|---|
| Tensor-product GHQF | Yes: state mean/covariance, maps, covariances, one-dimensional size \(s\). | Yes: one-dimensional standard-normal rule, tensor product, placed nodes. | Yes: prediction mean/covariance and observation mean/covariance/cross covariance. | Algorithm `bf-hd-ghqf-step`. | Yes: Gaussian innovation scalar. | Generic fixed-rule score only; not selected high-dimensional gradient target. | Point-count veto, PD/PSD checks. | `IMPLEMENTABLE_REFERENCE` |
| Fixed SGQF | Yes: dimension \(b\), level \(L\), default level policy \(s_\ell=2\ell-1\), univariate rules, fixed cloud, model maps. | Yes: source-local level band, coefficients, non-nested default GHQ family, duplicate-node dictionary. | Yes: same Gaussian projection recursion with sparse-grid weighted sums. | Algorithms `bf-hd-construct-fixed-sgq` and `bf-hd-fixed-sgqf-step`. | Yes: fixed sparse-grid Gaussian innovation scalar. | Yes: full fixed-SGQF value-and-score recursion. | Signed-weight/PSD/PD/factor diagnostics. | `IMPLEMENTABLE_SELECTED_TARGET` |
| ASGHF | Yes: pilot Gaussian, concrete concatenated pilot integrand, tolerance, budget, active/old sets. | Yes: difference increments and explicit frozen node/weight assembly. | Yes: grid selection followed by frozen SGQF filtering. | Algorithms `bf-hd-select-asghf` and `bf-hd-assemble-frozen-asghf`; frozen filtering delegates to fixed SGQF. | Only after grid freeze. | Only after grid freeze via fixed-SGQF gradient. | Active error, point budget, duplicate cancellation, PSD/PD, finite-difference parity. | `IMPLEMENTABLE_GRID_SELECTION_ONLY` |
| Fixed-SGQF gradient | Yes: model derivatives, fixed cloud, initial sensitivities, default Cholesky square-root derivative. | Fixed cloud is part of scalar. | Differentiates prediction, observation, likelihood, and posterior propagation. | Algorithm `bf-hd-fsgq-score`. | \(\widehat\ell_T^{\rm FSGQ}=\sum_t\widehat\ell_t^{\rm FSGQ}\). | Yes: Eqs. `bf-hd-fsgq-*`, including local Cholesky derivative. | Same-scalar, factor branch, PSD/PD, finite-difference parity. | `IMPLEMENTABLE_WITH_DEFAULT_CHOLESKY_BRANCH` |

## Residual Implementability Limits

- The default derivative branch is unpivoted Cholesky on strictly
  positive-definite covariance matrices.  Other square-root branches remain
  allowed only if they supply their own same-scalar derivative.
- ASGHF is implementable as a grid selector, not as a live adaptive HMC target.
- The fixed sparse-grid construction can still be too large for a given block;
  point budget is an algorithmic veto.
