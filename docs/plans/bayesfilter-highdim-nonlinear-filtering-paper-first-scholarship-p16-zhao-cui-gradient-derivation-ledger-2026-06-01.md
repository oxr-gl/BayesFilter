# P16 Zhao-Cui Gradient Derivation Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- P15 fixed-branch implementability specification.

what_is_not_concluded:
- No adaptive-branch global derivative claim.
- No HMC convergence claim.
- No posterior accuracy claim.

## Gradient Target

Declared fixed-branch scalar:

\[
  \widehat\ell_T(\beta)=\sum_{t=1}^T \log \widehat Z_t(\beta).
\]

Here \(\beta\) is the external differentiated parameter.  It is separated from
\(\alpha\), which denotes the parameter random variable in the Zhao--Cui
posterior-learning reconstruction.

## Derived Pieces

| Piece | P16 anchor | Status |
|---|---|---|
| transformed target derivative | G2 | `DERIVED` |
| square-root target derivative | G3 | `DERIVED` |
| fixed linear-solve derivative | G4-G6 | `DERIVED` |
| normalizer derivative | G7 | `DERIVED` |
| final score | G8 | `DERIVED` |
| same-scalar proposition | Proposition 2 | `DERIVED` |

## Decision

`GRADIENT_DERIVED_FOR_FIXED_BRANCH_SCALAR_ONLY`
