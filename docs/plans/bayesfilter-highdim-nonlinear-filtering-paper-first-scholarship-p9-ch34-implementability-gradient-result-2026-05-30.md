# P9 Ch34 Implementability And Gradient Result

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P9 plan, rewritten `ch34`, P9 implementability/gradient/HMC/source
anchor/MCP/Claude ledgers, Jia--Xin--Cheng 2012, Singh et al. 2018,
`ch18_svd_sigma_point.tex`, and the scholarly literature audit policy.

what_is_not_concluded: This result does not conclude exact nonlinear filtering,
posterior accuracy, HMC convergence, production readiness, NAWM readiness,
GPU/XLA readiness, default readiness, broad machine-certified proof validity,
or that the selected approximate target is scientifically adequate for any
particular client model.

## Current Decision

`P9_CH34_IMPLEMENTABILITY_REWRITE_ACCEPTED_WITH_LIMITS`.

## Execution Summary

`ch34` was expanded from source reconstruction into an implementability
specification for the three previously weak sections:

- Tensor-product GHQF now defines one-dimensional standard-normal GHQ rules,
  tensor-product nodes and weights, placed Gaussian nodes, prediction moments,
  observation moments, likelihood scalar, update, diagnostics, cost, and
  Algorithm `bf-hd-ghqf-step`.
- Fixed SGQF now defines univariate levels, tensor component rules, the
  source-local sparse-grid level band, coefficients, duplicate-node merging,
  signed weights, fixed-grid filtering recursion, diagnostics, and Algorithms
  `bf-hd-construct-fixed-sgq` and `bf-hd-fixed-sgqf-step`.
- ASGHF now defines difference increments, admissible index sets, active/old
  frontier logic, local error/cost indicator, offline grid selection, frozen-grid
  conversion, diagnostics, and Algorithm `bf-hd-select-asghf`.
- The analytical-gradient section now derives the fixed-SGQF value-and-score
  recursion for \(\widehat\ell_T^{\rm FSGQ}\), including prediction
  sensitivities, factor sensitivities, transition sensitivities, observation
  sensitivities, \(S_t\), \(v_t\), \(C_{xz,t}\), score, and posterior
  sensitivity propagation.

## Claude Execution Review Iteration 1

Claude returned `REJECT`.  Codex agreed with all major blockers.  Repairs
applied:

- SGQF now declares a concrete default univariate level policy
  \(s_\ell=2\ell-1\) using standard-normal GHQ nodes and weights, states that
  nesting is not assumed, and defines duplicate-node merging under the chosen
  policy.
- ASGHF now defines a concrete pilot integrand vector with fixed
  column-major vectorization, normalization scales, and \(\ell_1\) norm for the
  local error indicator.
- ASGHF now has explicit `AssembleFrozenAdaptiveSparseGrid` pseudocode for
  turning a frozen admissible index set into distinct standardized nodes and
  signed weights.
- The fixed-SGQF gradient section now includes a local unpivoted Cholesky
  derivative formula as the default square-root derivative branch.

## Current Validation Status

- LaTeX build succeeded with `latexmk -cd -pdf -interaction=nonstopmode
  -halt-on-error docs/main.tex`.
- `git diff --check` passed for the P9 write set after the iteration-1
  implementability patches.
- Targeted scan of `docs/main.log` found no undefined citation/reference/rerun
  blockers after the P9 build.
- PDF text validation confirmed that the P9 GHQF, SGQF, ASGHF, fixed-SGQF
  gradient, and HMC label material appears in `docs/main.pdf`.

## Final Validation Commands

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex`
- `git diff --check`
- `rg -n "Citation .*undefined|Reference .*undefined|There were undefined references|Rerun to get cross-references right|Label\\(s\\) may have changed|undefined citations" docs/main.log`
- `pdftotext docs/main.pdf /tmp/bayesfilter-main-p9.txt`
- `rg -n "Tensor-Product Gauss-Hermite Quadrature Filtering|Jia-Xin-Cheng Sparse-Grid Quadrature Filter|Adaptive Sparse-Grid Gauss-Hermite Filter|ConstructFixedSparseGrid|RunFixedSparseGridFilterStep|SelectAdaptiveSparseGrid|AssembleFrozenAdaptiveSparseGrid|FixedSparseGridValueAndScore|Fixed-SGQF Approximate Likelihood Gradient|HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET" /tmp/bayesfilter-main-p9.txt`
- `git status --short .local_sources .localsource docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/main.pdf docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p9-ch34-*`

## Claude Final Review

Claude execution review iteration 2 returned `ACCEPT`.  Codex accepts that
decision: the previous major blockers were implementability blockers, and the
chapter now gives concrete node/weight policies, filtering recursions,
adaptive-to-frozen grid assembly, square-root derivative convention, and
fixed-SGQF value-and-score recursion.

## Residual Limits

- The fixed-SGQF gradient is a branch-local analytical derivation for the
  declared approximate scalar; it is not an exact nonlinear-filter likelihood
  gradient.
- Matrix log-determinant, Cholesky, and full recursion correctness remain
  human-reviewed/project-derived rather than broadly machine-certified.
- The ASGHF pilot integrand and scaling convention are implementation
  conventions chosen for BayesFilter; after grid selection, HMC may only use
  the frozen fixed-grid scalar.
- Numerical stability still depends on positive-definite covariance branches,
  declared jitter/factor policies, and finite same-scalar value/gradient
  validation on concrete models.
