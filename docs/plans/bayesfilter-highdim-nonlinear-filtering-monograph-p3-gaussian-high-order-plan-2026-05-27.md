# P3 Classical and Higher-Order Gaussian Filters Chapter Plan

## Question

Which Gaussian projection filters remain plausible at high dimension, and where
does point-rule scaling break?

## Evidence Contract

Baseline:

- Existing sigma-point chapter and BayesFilter nonlinear sigma-point code.
- V1 nonlinear performance artifacts.

Primary criterion:

- The chapter derives moment projection, first/second-order EKF ideas, sigma
  point moment matching, CUT4 point growth, sparse-grid/block alternatives, and
  exact claim boundaries.

Veto diagnostics:

- CUT4 is proposed as an unblocked high-dimensional default.
- Approximation order is overstated without derivation or citation.
- Sparse-grid/block quadrature is promoted without downstream evidence.
- Point-rule scaling tables omit skip/blocker logic for high-dimensional rows.

Explanatory diagnostics:

- Point-count tables and high-dimensional skip labels.

Non-implications:

- Passing P3 does not promote any BayesFilter default.

Artifact:

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`

## Stop Rules

Stop P3 with a blocker if CUT4 point growth, sparse-grid assumptions, or
block-local quadrature limitations cannot be stated without implying default
readiness.

## Exit Label

`P3_GAUSSIAN_ACCEPTED` if scaling and approximation boundaries are explicit.
