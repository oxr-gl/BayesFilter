# P8 Ch34 Source-Reconstruction Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Julier--Uhlmann 1997, Arasaratnam--Haykin 2009,
Jia--Xin--Cheng 2012, Jia--Xin--Cheng 2013, Singh et al. 2018, P1R/P1S/P1U
source ledgers, P7 source-anchor ledger, current `ch34`,
`docs/references.bib`, and `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: This ledger does not conclude posterior accuracy, HMC
convergence, production readiness, NAWM readiness, GPU/XLA readiness, default
readiness, exhaustive cubature history, or machine-certified proofs.

## Decision

`SOURCE_LOCAL_RECONSTRUCTION_READY_FOR_REVIEW`.

## Source-Support Rows

| Source | Local artifact | Status | Checked anchors | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|
| Julier, Uhlmann, "A New Extension of the Kalman Filter to Nonlinear Systems", 1997 | `.local_sources/highdim_nonlinear_filtering/julier_uhlmann_new_extension_1997.pdf` | `PRIMARY_TECHNICAL_SUPPORT`; local full text extracted; no local quarantine signal from P1S | Eq. 12 sigma points; Eq. 13 transformed mean; Eq. 14 transformed covariance; UKF prediction/update boxes | UT/UKF sigma-point construction and transformed moment formulas | General posterior accuracy, scaled/square-root variants not checked here, HMC convergence |
| Arasaratnam, Haykin, "Cubature Kalman Filters", 2009 | `.local_sources/highdim_nonlinear_filtering/Cubature Kalman Filters Arasarantnam(09).pdf` | `PRIMARY_TECHNICAL_SUPPORT`; local full text extracted in P8; filename has author typo only | Section IV spherical--radial third-degree cubature; CKF update algorithm; square-root CKF discussion; comments on \(2n\) evaluations and dense cubic algebra | Third-degree CKF point rule, Gaussian integral interpretation, CKF moment update, square-root/numerical-stability context | Complete cure for high dimensionality, posterior accuracy, production readiness |
| Jia, Xin, Cheng, "High-Degree Cubature Kalman Filter", 2013 | `.local_sources/highdim_nonlinear_filtering/High-degree cubature Kalman filter Jia(13).pdf` | `PRIMARY_TECHNICAL_SUPPORT`; local full text and DOI metadata checked in P1R/P1S | Definition 3.1; Theorem 3.1; Proposition 3.1; third-degree rule; fifth-degree rule Eq. 46; Proposition 3.2; Remark 3.6 | Source-local high-degree CKF construction, fifth-degree rule, polynomial point-count growth for fixed degree, negative-weight caveat | Independent Stroud/Genz/Cools theorem support, global nonlinear accuracy, non-Gaussian filtering claims |
| Jia, Xin, Cheng, "Sparse-Grid Quadrature Nonlinear Filtering", 2012 | `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf` | `PRIMARY_TECHNICAL_SUPPORT`; local full text and DOI metadata checked in P1R/P1S | Gaussian filtering equations; GHQ Section 2.2.1; SGQ formula Eq. 26--29; Theorem 3.1; Algorithm 1; Theorem 3.2; Proposition 3.1; Appendix point-count examples | Source-local GHQ, SGQF construction, UKF-as-level-2 relation, fixed-level sparse-grid point-growth discussion | Independent Smolyak theorem support, arbitrary nonlinear/non-Gaussian filtering, NAWM-scale practicality |
| Singh, Radhakrishnan, Bhaumik, Date, "Adaptive Sparse-Grid Gauss-Hermite Filter", 2018 | `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf` | `PRIMARY_TECHNICAL_SUPPORT`; local full text checked in P1R; preprint/version caveat applies | Section 2 SGHF; Section 3 notation, admissible index set, local error indicator, active/old sets, tolerance, adaptive algorithm | Adaptive sparse-grid GHQ algorithm and computational-budget competitor role | Theorem-level convergence beyond paper scope, broad industrial validation, smooth HMC gradients through live adaptation |
| `ch18_svd_sigma_point.tex` | `docs/chapters/ch18_svd_sigma_point.tex` | `PROJECT_DERIVATION` | Sigma-point point/moment derivative recursion and solve-form Gaussian innovation score | Local notation pattern for approximate Gaussian innovation score | Source theorem for ch34 methods or machine certification |

## Backward Snowball Coverage

| Seed | Backward candidates recorded from prior P1/P7 ledgers | P8 action |
|---|---|---|
| Julier--Uhlmann UT/UKF | EKF, Julier/Uhlmann companion work, van der Merwe scaled sigma-point thesis | Use Julier--Uhlmann 1997 for baseline UT only; scaled UKF variants remain omitted/scope-limited unless separately checked. |
| Arasaratnam--Haykin CKF | UKF, CDKF, QKF/GHQ, cubature foundations, square-root filtering | Use CKF source locally; do not expand QKF/GHQ history beyond Jia 2012 source-local GHQ construction. |
| Jia 2013 high-degree CKF | Genz, Stroud, Cools, Mysovskikh, CKF, GHQF, UKF | Use Jia 2013 for source-local high-degree rules; keep broader cubature foundations as omitted-source risk. |
| Jia 2012 SGQF | Smolyak, Heiss--Winschel, Ito--Xiong, GHQF, UKF, CKF | Use Jia 2012 for SGQF and GHQ construction; keep Smolyak/Ito--Xiong as omitted-source risks. |
| Singh 2018 ASGHF | Gerstner--Griebel adaptive sparse grids, SGHF/GHF references, CKF/UKF/PF competitors | Use Singh 2018 for ASGHF mechanics only; broader adaptive sparse-grid theory not reopened. |

## Forward Snowball Coverage

No new network lookup was run in P8.  Existing P1S/P1T metadata is inherited:

- Jia 2012 SGQF: OpenAlex exact DOI record and citing-work query were recorded
  in P1S.
- Jia 2013 high-degree CKF: OpenAlex exact DOI record and citing-work query
  were recorded in P1S.
- Singh 2018 ASGHF: forward exact metadata remained incomplete in P1S.
- Arasaratnam--Haykin CKF: P1S metadata search was unreliable, but P8 now has
  local full text for technical support.

Status: `FORWARD_SNOWBALL_BLOCKED_NO_NEW_NETWORK`.  This is a coverage
limitation, not a claim that no later follow-up papers exist.

## Omission And Reviewer-Risk Register

| Omitted or scoped source | Risk | P8 handling |
|---|---|---|
| Smolyak 1963 original sparse-grid paper | Reviewer may ask for original sparse-grid theorem | Not used as support.  P8 cites Jia 2012's source-local SGQF formula only. |
| Stroud/Genz/Cools/Mysovskikh cubature foundations | Reviewer may ask for independent cubature exactness foundations | Not used as independent theorem support.  P8 derives only Jia 2013 source-local rules. |
| Ito--Xiong Gaussian filters/GHQF | Reviewer may ask for Gaussian approximation filter foundation | Not used as independent theorem support.  P8 uses Jia 2012/2013 source-local Gaussian approximation setup. |
| van der Merwe scaled/square-root UKF | Scaled UKF variants may be expected | P8 does not derive scaled variants; Julier--Uhlmann baseline UT only. |
| Arasaratnam--Haykin--Elliott GHQ paper | Reviewer may ask for GHQF history | P8 uses Jia 2012 Section 2.2.1 for GHQ construction and marks tensor GHQ as mathematical reference, not broad GHQF survey. |

## Quarantine

No quarantined/retracted paper is used for chapter 34 support.  Quarantined
transport sources from other chapters remain irrelevant to P8 and cannot support
claims here.
