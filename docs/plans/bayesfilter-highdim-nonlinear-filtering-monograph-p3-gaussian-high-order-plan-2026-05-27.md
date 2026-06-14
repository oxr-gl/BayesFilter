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
- For scholarly readiness, each Gaussian or high-order method family must have
  implementation-grade pseudocode or an exclusion rationale, dimensional
  scaling, memory scaling, approximation assumptions, degeneracy/failure modes,
  and BayesFilter evidence links or blockers.

Veto diagnostics:

- CUT4 is proposed as an unblocked high-dimensional default.
- Approximation order is overstated without derivation or citation.
- Sparse-grid/block quadrature is promoted without downstream evidence.
- Point-rule scaling tables omit skip/blocker logic for high-dimensional rows.
- EKF/IEKF/second-order EKF/UKF/CKF/Gauss-Hermite/CUT4/sparse-grid claims lack
  primary-source support or derivation.
- A method is practically recommended for NAWM-like scale without explaining
  what structure would rescue it and what evidence is still missing.

Explanatory diagnostics:

- Point-count tables and high-dimensional skip labels.

Non-implications:

- Passing P3 does not promote any BayesFilter default.
- Passing P3 does not prove high-order Gaussian filtering is accurate in a
  high-dimensional nonlinear DSGE model.

Artifact:

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`

## Stop Rules

Stop P3 with a blocker if CUT4 point growth, sparse-grid assumptions, or
block-local quadrature limitations cannot be stated without implying default
readiness.

Stop P3 scholarly refinement with a blocker if any covered method lacks
pseudocode/exclusion rationale, scaling/memory analysis, source support,
failure diagnostics, and NAWM-scale relevance notes.

## Exit Label

`P3_GAUSSIAN_ACCEPTED` if scaling and approximation boundaries are explicit.

`P3_SCHOLARLY_GAUSSIAN_ACCEPTED` only if the chapter is no longer a thin
overview and each method family passes the primary-source, derivation,
algorithm, complexity, and industrial-practitioner gates.
