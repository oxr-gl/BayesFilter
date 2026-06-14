# P18 Zhao--Cui Fixed-Branch Gradient Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P15 fixed-branch implementation contract.

what_is_not_concluded:
- No claim that Zhao--Cui's adaptive algorithm is globally differentiable.
- No claim that fixed-branch approximation is exact posterior filtering.

## Boundary

The P18 note contains the required hard section boundary:

`End of Zhao--Cui Annotation and Start of BayesFilter Fixed-Branch Extension`

All fixed-branch derivative material appears after this boundary.

## Gradient Contract

- Forward scalar: \(\widehat\ell_T(\beta)=\sum_t\log\widehat Z_t(\beta)\).
- Branch-fixed objects: domains, maps, fitting points, weights, ranks, basis,
  sweep order, ridge, defensive masses, scaling shifts, and linear-solve path.
- Differentiated objects: target evaluations, square-root targets, design
  matrices, core solves, mass contractions, normalizers, carried filters.
- Test protocol: same-branch central finite difference; rebuilding branch at
  perturbed parameters is explicitly not the same-scalar test.

Decision: `FIXED_BRANCH_GRADIENT_CONTRACT_PRESENT_FOR_REVIEW`.
