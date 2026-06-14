# P31 Fixed-SGQF Source Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not certify exact posterior accuracy, HMC convergence, production readiness, or exhaustive sparse-grid history.
- This ledger does not use Smolyak's original paper or Stroud/Genz foundations as direct technical support.
- This ledger does not claim that adaptive sparse-grid selection is differentiable during HMC.

## Local Sources

| source | local artifact | inspected anchors | allowed claims | forbidden claims |
|---|---|---|---|---|
| Jia--Xin--Cheng 2012 | `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf` | State-space model Eq. (1)--(2); Bayesian prediction/update Eq. (3)--(4); Gaussian approximation filter Eq. (15)--(23); sparse-grid rule Eq. (26)--(29); Theorem 3.1; Algorithm 1; Theorem 3.2; Proposition 3.1--3.2; numerical examples | SGQF construction, sparse-grid point/weight generation, polynomial exactness under stated quadrature conditions, UKF-as-level-2 relation, fixed-level point-count growth | exact nonlinear posterior accuracy; arbitrary non-Gaussian filtering; global high-dimensional practicality for large \(b\) without point budget checks |
| Singh et al. 2018 | `.local_sources/highdim_nonlinear_filtering/adaptive_sparse_grid_gauss_hermite_1803.09272.pdf` | Section 2 sparse-grid GH filter; Section 3 definitions of forward/backward/admissible indices, local error indicator, active/old sets, global error estimate, tolerance; algorithmic steps; simulations | adaptive sparse-grid GH as an offline grid-design competitor; admissible-index and indicator mechanics; tolerance and error-weighting tradeoff | theorem-level convergence beyond source scope; live differentiability of adaptive selection |
| Zhao--Cui 2024 | `.local_sources/highdim_nonlinear_filtering/zhao_cui_tt_sequential_learning_jmlr_23-0743.pdf` | P17--P30 ledgers and companion note; Section 1--5; Algorithm 2/5; squared TT and fixed-branch derivative extension | comparison point: richer non-Gaussian density approximation proposal and separate fixed-branch derivative lane | evidence that SGQF is non-Gaussian or exact posterior filtering |

## P31 Claim Support Map

| P31 claim | support class | source/project anchor |
|---|---|---|
| FixedSGQF is a Gaussian projection filter: it stores mean/covariance, not the full posterior. | `PRIMARY_TECHNICAL_SUPPORT` plus `PROJECT_DERIVATION` | Jia--Xin--Cheng 2012 Eq. (15)--(23); ch34 affine projection derivation |
| Sparse-grid rule is a signed combination of tensor-product one-dimensional rules over a level band. | `PRIMARY_TECHNICAL_SUPPORT` | Jia--Xin--Cheng 2012 Eq. (26)--(29), Algorithm 1 |
| Duplicate nodes must have accumulated weights. | `PRIMARY_TECHNICAL_SUPPORT` plus implementation expansion | Jia--Xin--Cheng 2012 Algorithm 1 |
| FixedSGQF approximate scalar is differentiable only when the cloud, weights, factor branch, and stabilization policy are fixed. | `PROJECT_DERIVATION` | ch34 P9 fixed-SGQF gradient derivation and same-scalar contract |
| The analytical gradient differentiates the declared approximate Gaussian innovation scalar, not the exact likelihood. | `PROJECT_DERIVATION` | P9 gradient ledger; local derivation in P31 |
| Adaptive sparse-grid selection is useful before inference but not as a live differentiable HMC target. | `PRIMARY_TECHNICAL_SUPPORT` plus `PROJECT_DERIVATION` | Singh et al. 2018 Section 3; same-scalar branch argument |
| FixedSGQF and Zhao--Cui are complementary high-dimensional proposals. | `PROJECT_SYNTHESIS` | P31 comparison section; P30 Zhao--Cui note; P31 FixedSGQF note |

## Source Status

source_status: `LOCAL_PRIMARY_ANCHORS_AVAILABLE`

P31 can proceed using checked local primary-source anchors for SGQF mechanics and project derivations for the fixed scalar and gradient.  It must avoid broad sparse-grid history claims unless additional sources are inspected.
