# P17 Zhao-Cui Section 5 Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, JMLR 2024, Section 5.
- P10 paper-code crosswalk.
- P16 annotated reconstruction.

what_is_not_concluded:
- No claim that a preconditioner improves ranks for every model.
- No claim that adaptive preconditioner construction is globally differentiable.
- No production implementation claim.

## Section 5 Reconstruction

Decision: `SECTION_5_EXPANDED_WITH_PRECONDITIONING_COMPOSITION`

P17 expands bridge density, pushforward identity, residual target, squared-TT
residual, pullback approximation, normalizer invariance, Gaussian/linear
whitening, tempering bridge, nonlinear bridge approximation, \(R_t,D,T_t\)
composition, Algorithm 5 retained marginal, and final lower conditional
composite map.

Main P16 misses repaired:

- Cholesky whitening map \(T_t^\ell(r)=L_t^{-1}(r-\mu_t)\);
- whitening log determinant;
- nonlinear bridge map composition \(T_t=D^{-1}\circ R_t\);
- residual target using \(\widehat\rho_t\);
- Algorithm 5(c.2) retained marginal formula;
- final composite lower conditional map for smoothing.

