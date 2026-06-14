# P16 Zhao-Cui Claim-Support Ledger

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui JMLR 2024.
- P15 fixed-branch implementability specification.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global adaptive-gradient claim.
- No production-readiness claim.

## Claims

| Claim | Support class | Support |
|---|---|---|
| State-space recursion creates a three-block target in \((x_t,\alpha,x_{t-1})\). | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (9)--(11); P16 derivation BF-9--BF-11. |
| TT representation makes marginalization a sequence of core contractions. | `PROJECT_DERIVATION` | P16 TT-4--TT-5. |
| Algorithm 1 can produce negative approximations. | `PRIMARY_TECHNICAL_SUPPORT` + mathematical explanation | Zhao--Cui Section 2.3 discussion; P16 nonnegativity section. |
| Squared-TT plus defensive reference gives a nonnegative density. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eq. (13); P16 S1--S3. |
| Squared-TT marginals use mass matrices and square-root factors. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eq. (14); P16 M1--M6. |
| Conditional KR maps follow from marginal ratios. | `PROJECT_DERIVATION` | P16 K1--K5. |
| Forward and backward importance weights are computable when conditional proposal densities are evaluable. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (21)--(26); P16 F1--F4, B1--B5. |
| Preconditioning changes variables and fits a flatter pushforward ratio. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (30)--(35); P16 P1--P7. |
| Fixed-branch recursion is normalized for its declared approximation. | `PROJECT_DERIVATION` | P16 Proposition 1. |
| Fixed-branch derivative differentiates the declared scalar. | `PROJECT_DERIVATION` | P16 Proposition 2. |

## Gaps

- The P16 note does not yet include a complete runnable program; it specifies
  the minimal example and relies on P15 for an executed reference example.
