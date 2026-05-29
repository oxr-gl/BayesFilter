# P8 Ch34 Source-Anchor And Claim-Support Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P8 source-reconstruction ledger, Julier--Uhlmann
1997, Arasaratnam--Haykin 2009, Jia--Xin--Cheng 2012, Jia--Xin--Cheng 2013,
Singh et al. 2018, `ch18_svd_sigma_point.tex`, P1/P7 ledgers, and the
scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude exhaustive literature
coverage, posterior accuracy, HMC convergence, production readiness, NAWM
readiness, or default readiness.

## Claim-Support Map

| `ch34` claim or construction | Chapter location | Support class | Anchor |
|---|---|---|---|
| Gaussian projection update is affine MMSE given moments. | Section "Gaussian Moment Projection"; Prop. `bf-hd-affine-projection` | `PROJECT_DERIVATION` | Local derivation; Jia 2012/2013 cited only for source-local Gaussian approximation setup. |
| EKF moment formulas follow first-order Taylor expansion. | Section "EKF and Second-Order Taylor Filters" | `PROJECT_DERIVATION` | Local Taylor derivation; Julier--Uhlmann cited only for EKF motivation/comparison. |
| Second-order Taylor mean/covariance formulas under Gaussian central moments. | Section "EKF and Second-Order Taylor Filters" | `PROJECT_DERIVATION` | Local Gaussian moment calculation. |
| UT sigma points and transformed moment formulas. | Section "Julier-Uhlmann Unscented Transform / UKF" | `PRIMARY_TECHNICAL_SUPPORT` | Julier--Uhlmann 1997 Eq. 12--14. |
| UT input point cloud matches mean/covariance. | UT section derivation | `PROJECT_DERIVATION` with source construction | Algebra from Julier--Uhlmann point set. |
| CKF point set \(\pm\sqrt n e_j\) with equal weights. | Section "Arasaratnam-Haykin Cubature Kalman Filter" | `PRIMARY_TECHNICAL_SUPPORT` | Arasaratnam--Haykin 2009 spherical--radial CKF construction. |
| CKF is third-degree moment rule, not posterior rule. | CKF section derivation | `PROJECT_DERIVATION` with source construction | Algebra from CKF point set. |
| High-degree CKF degree definition and source-local construction. | Section "Jia-Xin-Cheng High-Degree CKF" | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2013 Definition 3.1, Theorem 3.1, Proposition 3.1. |
| Fifth-degree CKF formula with \(2n^2+1\) points. | Eq. `bf-hd-fifth-degree-rule` | `PRIMARY_TECHNICAL_SUPPORT` plus notation translation | Jia 2013 Eq. 46. |
| Fixed-degree high-degree CKF point count grows polynomially. | High-degree CKF cost paragraph | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2013 Proposition 3.2. |
| Negative weights are a stability caveat. | High-degree CKF limitations paragraph | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2013 Remark 3.6. |
| Tensor-product GHQ construction and exponential point count. | Section "Tensor-Product Gauss-Hermite Filtering" | `PRIMARY_TECHNICAL_SUPPORT` for source-local construction; `PROJECT_DERIVATION` for point-count algebra | Jia 2012 Section 2.2.1. |
| SGQF sparse-grid rule. | Eq. `bf-hd-sgqf-smolyak` | `PRIMARY_TECHNICAL_SUPPORT` with notation translation | Jia 2012 Eq. 26--29. |
| SGQF exactness and UKF-as-level-2 relation. | SGQF source paragraph | `PRIMARY_TECHNICAL_SUPPORT` | Jia 2012 Theorem 3.1, Algorithm 1, Theorem 3.2. |
| ASGHF adaptive index/error-indicator construction. | Section "Adaptive Sparse-Grid Gauss-Hermite Filter" | `PRIMARY_TECHNICAL_SUPPORT` | Singh et al. 2018 Section 3, with preprint/version caveat in the source ledger. |
| Approximate Gaussian innovation scalar and score. | Section "Approximate Likelihood and Analytical Gradient"; Prop. `bf-hd-gq-score` | `PROJECT_DERIVATION` | Local derivation; patterned after `ch18`, not source theorem. |
| HMC labels by method family. | HMC table in gradient section | `PROJECT_DERIVATION` | Same-scalar contract plus branch-smoothness reasoning. |
| Limitations of methods. | Section "Limitations of These Methods" | Mixed: `PROJECT_DERIVATION`, `PRIMARY_TECHNICAL_SUPPORT`, and `SOURCE_GAP_BLOCKER` | Method-local limitations and omitted-source caveats. |

## Citation Placement Check

- Julier--Uhlmann is cited where the UT point/moment construction is introduced.
- Arasaratnam--Haykin is cited where CKF spherical--radial construction,
  square-root context, and cost caveat are discussed.
- Jia 2013 is cited where degree, fifth-degree formula, point-count growth, and
  negative-weight caveat are used.
- Jia 2012 is cited where GHQ, SGQF formula, exactness theorem, algorithm, and
  UKF-as-level-2 relation are used.
- Singh 2018 is cited where ASGHF index/error/tolerance mechanics are used.
- `ch18` is cited only as a local derivative pattern, not paper authority.

## Source-Gap Scope Notes

Smolyak, Stroud, Genz/Cools, Ito--Xiong, van der Merwe scaled UKF, and
Arasaratnam--Haykin--Elliott GHQ are not used as theorem support.  Their absence
is recorded as reviewer-risk scope, not silently ignored.
