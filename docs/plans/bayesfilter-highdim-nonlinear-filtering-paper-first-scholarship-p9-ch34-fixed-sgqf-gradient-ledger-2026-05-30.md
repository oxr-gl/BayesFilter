# P9 Ch34 Fixed-SGQF Gradient Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P9 plan, `ch18_svd_sigma_point.tex`, P8 gradient
ledger, MathDevMCP diagnostics, and the scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude exact likelihood
gradients, HMC convergence, posterior accuracy, live adaptive-grid
differentiability, production readiness, or machine-certified correctness.

## Selected Scalar

\[
  \widehat\ell_T^{\rm FSGQ}(\theta)
  =
  \sum_{t=1}^T \widehat\ell_t^{\rm FSGQ}(\theta)
\]

where each contribution is produced by the fixed sparse-grid Gaussian
projection filter with a frozen standardized cloud
\(\{(\xi^{(r)},w_r)\}_{r=1}^M\).  The cloud, duplicate-node merge, covariance
factor branch, and stabilization policy are part of the scalar contract.

## Gradient Obligations

| Obligation | Chapter anchor | Status | Support class | Notes |
|---|---|---|---|---|
| Declare fixed sparse-grid scalar. | Eq. `bf-hd-fsgq-total-likelihood` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Approximate scalar only. |
| Default Cholesky square-root derivative. | Eq. `bf-hd-fsgq-cholesky-derivative` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Strictly positive-definite unpivoted branch only. |
| Prediction point sensitivity \(\dot\chi_{t-1}\). | Eq. `bf-hd-fsgq-pred-point-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Uses default Cholesky derivative or a declared replacement. |
| Transition sensitivity \(\dot a_t\). | Eq. `bf-hd-fsgq-transition-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Chain rule with \(D_x f_\theta\) and \(\partial_i f_\theta\). |
| Prediction mean/covariance sensitivities. | Eqs. `bf-hd-fsgq-pred-mean-score`, `bf-hd-fsgq-pred-cov-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Fixed weights; includes \(\dot Q_\theta\). |
| Observation point and map sensitivities. | Eq. `bf-hd-fsgq-obs-point-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Requires \(D_x h_\theta\), \(\partial_i h_\theta\). |
| Innovation mean/residual sensitivities. | Eq. `bf-hd-fsgq-z-v-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Recorded data gives \(\dot y_t=0\). |
| Innovation covariance sensitivity. | Eq. `bf-hd-fsgq-S-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Includes \(\dot R_\theta\). |
| Cross-covariance sensitivity. | Eq. `bf-hd-fsgq-cross-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Needed for posterior sensitivity propagation. |
| Fixed-SGQF score. | Eq. `bf-hd-fsgq-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION`; narrow MCP diagnostics | Solve-form Gaussian innovation score. |
| Posterior sensitivity propagation. | Eq. `bf-hd-fsgq-update-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Needed to feed next time step. |
| Value-and-score pseudocode. | Algorithm `bf-hd-fsgq-score` | `IMPLEMENTABLE` | `PROJECT_DERIVATION` | Requires factor derivative routine. |

## Same-Scalar Conditions

- Fixed sparse-grid index set, nodes, weights, and duplicate-node merging.
- Differentiable model maps and covariance functions.
- Differentiable square-root branch; default is unpivoted Cholesky with
  Eq. `bf-hd-fsgq-cholesky-derivative`.
- No hidden clipping, pruning, floor, pivot, level change, or live adaptation.
- Positive-definite \(S_t\) and acceptable PSD status for propagated covariance.
