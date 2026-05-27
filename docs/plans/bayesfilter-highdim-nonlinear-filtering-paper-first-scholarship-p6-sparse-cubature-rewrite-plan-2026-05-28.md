# P6 Sparse-Grid And High-Degree Cubature Rewrite Plan

## Objective

Rewrite high-order Gaussian/quadrature competitors as real primary-source
methods rather than source-gated placeholders.

## Inputs

- P1 source ledger entries for high-degree cubature Kalman filtering,
  sparse-grid quadrature nonlinear filtering, adaptive sparse-grid
  Gauss-Hermite filtering, and existing CUT/sigma-point sources.
- Existing `ch34`.

## Execution Precondition

Execution is forbidden unless every sparse-grid, adaptive Gauss-Hermite,
high-degree cubature, CUT, and sigma-point source used by P6 is
`LOCAL_FULL_TEXT_CHECKED` in the P1 ledger with local artifact path, inspected
technical sections, inspected equation/theorem/algorithm identifiers where
available, and chapter consumers recorded.  Existing bibliography keys do not
substitute for technical inspection.

## Required Content

1. Moment-integral formulation of Gaussian projection filters.
2. High-degree cubature rule construction and exactness statement.
3. Sparse-grid/Smolyak construction from one-dimensional rules.
4. Adaptive sparse-grid Gauss-Hermite mechanism.
5. Derivation of point counts and error/interaction intuition.
6. Algorithms for block high-order cubature and adaptive sparse-grid diagnostic
   use.
7. Complexity and memory versus dimension, level, degree, block size, and
   nonlinear model evaluation cost.
8. Failure modes: exponential block growth, negative/unstable weights,
   covariance PSD failure, interaction truncation, and quadrature aliasing.
9. Paper-by-paper mapping from source equation/theorem/algorithm to chapter
   subsection and derivation/proof sketch.

## Outputs

- Rewritten `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`.
- P6 result note.
- Paper-by-paper exposition checklist and source-to-chapter mapping table.

## Stop Conditions

- Stop if sparse-grid papers are not locally inspected.
- Stop if error/exactness claims cannot be source-supported.

## Verification

- `rg -n "sparse|Smolyak|cubature|Gauss-Hermite|exactness|point count" docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/references.bib` only for checked sources consumed by P6.
- `docs/source_map.yml` only for P6 provenance entries.

## What Must Not Be Concluded

P6 does not promote sparse grids or high-degree cubature to global
high-dimensional readiness.  They are competitors and diagnostics until
downstream evidence exists.
