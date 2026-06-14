# P31 Fixed-SGQF Gradient Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not conclude exact likelihood gradients.
- This ledger does not conclude differentiability through live adaptive grid selection, Cholesky pivots, clipping, pruning, or rank/level changes.
- This ledger does not certify numerical stability for all models.

## Declared Scalar

The scalar differentiated in P31 is
\[
  \widehat\ell_T^{\rm FSGQ}(\theta)
  =
  \sum_{t=1}^T
  -\frac12\{\log\det S_t(\theta)
  +v_t(\theta)^\top S_t(\theta)^{-1}v_t(\theta)
  +n_y\log(2\pi)\},
\]
where \(S_t\) and \(v_t\) are produced by the fixed sparse-grid Gaussian projection recursion using one frozen standardized cloud \(\{(\xi^{(r)},w_r)\}_{r=1}^M\).

## Same-Scalar Contract

The following objects are part of the scalar definition and must be identical in the value and gradient paths:

- observations \(y_{1:T}\), observation preprocessing, and missing-data policy if any;
- initial distribution policy \(m_0(\theta),P_0(\theta)\), including whether and how \(\dot m_0,\dot P_0\) are propagated;
- sparse-grid index set or fixed level;
- one-dimensional node/weight family;
- duplicate-node merging tolerance;
- accumulated standardized nodes and signed weights;
- covariance factor map and active differentiable branch;
- symmetrize-then-veto policy for the differentiable branch;
- model maps \(f_\theta,h_\theta\), covariance maps \(Q_\theta,R_\theta\), and their derivatives;
- veto policy for non-positive-definite \(P_t^-\), \(S_t\), or stabilized covariance objects.

The P31 note deliberately narrows the differentiable branch to symmetrize then
veto.  Adaptive jitter, eigenvalue floors, covariance clipping, Cholesky
pivots, point pruning, and live grid changes are different scalars unless a
separate differentiable map or stop rule is supplied.

## Derivative Obligations

| obligation | support status | planned P31 location |
|---|---|---|
| derivative of Gaussian innovation log scalar | `PROJECT_DERIVATION`; narrow MCP planned | Proposition "Gaussian innovation score" |
| derivative of fixed cloud points \(\chi=m+C\xi\) | `PROJECT_DERIVATION` | Fixed cloud sensitivity section |
| Cholesky branch derivative | `PROJECT_DERIVATION`; narrow MCP planned | Square-root branch subsection |
| transition mean/covariance derivatives | `PROJECT_DERIVATION` | Prediction sensitivity recursion |
| observation mean/covariance/cross-covariance derivatives | `PROJECT_DERIVATION` | Observation sensitivity recursion |
| Kalman gain, mean, covariance update derivatives | `PROJECT_DERIVATION`; narrow MCP planned | Posterior sensitivity propagation |
| finite-difference same-scalar protocol | `IMPLEMENTATION_DIAGNOSTIC_SPEC` | Validation section |
| adaptive-to-frozen grid separation | `PROJECT_DERIVATION` | Adaptive grid design section |

## Current Status

gradient_status: `READY_FOR_STANDALONE_EXPANSION`

P31 should present the derivative as a derivative of the fixed approximate scalar only.  It must not claim to differentiate exact filtering likelihoods or live adaptive sparse-grid algorithms.
