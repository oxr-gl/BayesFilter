# P17 Zhao-Cui Fixed-Branch Derivative Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024.
- P10 filtering-scalar ledger.
- P15 fixed-branch implementability specification.
- P16 annotated reconstruction.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui code is globally differentiable.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No HMC convergence claim.

## Fixed-Branch Decision

Decision: `FIXED_BRANCH_EXTENSION_RETAINED_AND_ATTACHED_AFTER_SOURCE_RECONSTRUCTION`

P17 places the BayesFilter fixed-branch derivative after the source-paper
reconstruction.  The extension uses:

- fixed domains, basis, points, ranks, ridge, shifts, and defensive mass;
- shifted convention \(\widehat q_t=e^{-c_t}\phi_t^2+\tau_t\lambda_t\);
- normalized approximate filtering proposition for the declared density;
- same-scalar derivative proposition for
  \(\widehat\ell_T=\sum_t\log\widehat Z_t\);
- derivative through target evaluations, core solves, mass contractions,
  normalizers, and carried filters;
- same-branch finite-difference protocol.

The derivative is branch-local and differentiates the scalar computed by the
saved branch only.

