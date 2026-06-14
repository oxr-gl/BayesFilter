# P32 FixedSGQF Source-Support Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not certify exact posterior accuracy, production readiness, HMC convergence, or exhaustive sparse-grid literature history.
- This ledger does not use source introductions or abstracts for theorem-level support.
- This ledger does not claim adaptive sparse-grid selection is differentiable during HMC.

## Local Primary Sources

| source | local artifact | inspected anchors | allowed claims | forbidden claims |
|---|---|---|---|---|
| Jia--Xin--Cheng 2012 | `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf` | Section 2.1 state-space model and Bayesian prediction/update; Section 2.2 Gaussian approximation filters; Section 2.2.1 Gauss--Hermite rule; Section 3.1 sparse-grid rule and Theorem 3.1; Section 3.2 univariate point/weight selection; Section 3.3 Algorithm 1; Section 3.4 Theorem 3.2; Section 3.5 Propositions 3.1--3.2; numerical orbit examples | SGQF as Gaussian approximation filter; sparse-grid construction; duplicate-point accumulation; polynomial exactness under stated conditions; UKF relation; source example as empirical illustration | exact nonlinear posterior accuracy; global high-dimensional success without diagnostics; differentiability of BayesFilter fixed-gradient extension |
| Singh et al. 2018 | `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf` | Section 2 SGHF; Section 3 definitions of forward/backward/admissible index sets, local error indicator, active/old sets, global error estimate, tolerance; algorithm; examples | adaptive sparse-grid mechanics as grid-design procedure; error-weight/tolerance tradeoff; offline selection interpretation | live differentiability of adaptive selection; theorem-level posterior accuracy beyond source |
| Zhao--Cui 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | P17--P30 companion ledgers and local source Sections 1--5 | comparison point: richer non-Gaussian squared-TT density approximation and fixed-branch derivative contrast | support for SGQF exactness or Gaussian projection fidelity |

## Source-Order Reconstruction Targets

| target in P32 | support class | source anchor |
|---|---|---|
| exact nonlinear filtering recursion | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Section 2.1 |
| Gaussian approximation filter moment recursion | `PRIMARY_TECHNICAL_SUPPORT` plus `PROJECT_DERIVATION` | Jia--Xin--Cheng 2012 Section 2.2; BayesFilter affine projection proof |
| one-dimensional Gauss--Hermite and tensor-product rule | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Section 2.2.1 |
| sparse-grid/Smolyak formula | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Eq. 26--29 |
| exactness scope | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Theorem 3.1 |
| univariate point selection | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Section 3.2 |
| multidimensional point/weight generation | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Algorithm 1 |
| UKF relation | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Theorem 3.2 |
| point-count and nestedness discussion | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Propositions 3.1--3.2 and discussion |
| FixedSGQF same-scalar likelihood | `PROJECT_DERIVATION` | P9/P31 gradient ledgers and P32 derivation |
| FixedSGQF analytical gradient | `PROJECT_DERIVATION` | P9/P31 gradient ledgers and P32 derivation |
| adaptive grid as offline design | `PRIMARY_TECHNICAL_SUPPORT` plus `PROJECT_DERIVATION` | Singh et al. 2018 Section 3; same-scalar argument |

## Current Source Status

source_status: `LOCAL_PRIMARY_ANCHORS_AVAILABLE`

P32 may proceed without network lookup because the current task is a source-grounded expansion of already-local method papers.  Citation-count and venue metadata are not needed for this pass.
