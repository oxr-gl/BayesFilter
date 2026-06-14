# P32 FixedSGQF Gradient Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not conclude exact likelihood gradients.
- This ledger does not conclude differentiability through live adaptive grid selection, Cholesky pivots, clipping, pruning, covariance repair, or level changes.
- This ledger does not certify numerical stability for all models.

## Declared Scalar

P32 differentiates the fixed sparse-grid Gaussian projection scalar
\[
  \widehat\ell_T^{\rm FSGQ}(\theta)
  =
  \sum_{t=1}^T
  -\frac12\{\log\det S_t(\theta)
  +v_t(\theta)^\top S_t(\theta)^{-1}v_t(\theta)
  +n_y\log(2\pi)\}.
\]

The objects \(S_t(\theta)\) and \(v_t(\theta)\) are produced by one frozen standardized sparse-grid cloud, one declared covariance factor branch, one declared symmetrize-then-veto stabilization policy, and fixed observations/preprocessing.

## Same-Scalar Contract

Value and gradient paths must use identical:

- observations \(y_{1:T}\), preprocessing, and missing-data policy;
- initial law \(m_0(\theta),P_0(\theta)\) and sensitivities;
- sparse-grid index set or fixed level;
- one-dimensional node/weight family;
- duplicate-node merge tolerance and accumulated signed weights;
- covariance square-root map and active differentiable branch;
- symmetrize-then-veto policy;
- model maps \(f_\theta,h_\theta,Q_\theta,R_\theta\) and derivative routines;
- failure exits for non-PD factors, indefinite innovation covariance, or broken branch parity.

## Required Derivative Blocks

| block | P32 status |
|---|---|
| square-root branch derivative | `EXPANDED_IN_NOTE_PENDING_MCP_AND_CLAUDE` |
| prediction point derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| transition map derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| prediction mean/covariance derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| observation point derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| observation mean/residual/covariance derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| cross-covariance derivative | `EXPANDED_IN_NOTE_PENDING_CLAUDE` |
| innovation log-likelihood derivative | `EXPANDED_IN_NOTE_PENDING_MCP_AND_CLAUDE` |
| gain/posterior derivative | `EXPANDED_IN_NOTE_PENDING_MCP_AND_CLAUDE` |
| finite-difference same-scalar check | `EXPANDED_IN_NOTE_PENDING_MCP_AND_CLAUDE` |

## Current Status

gradient_status: `EXPANDED_PENDING_VALIDATION`

P32 must make the gradient derivation teachable before it becomes formal: the note should first explain the chain of saved objects and then write the equations beside the value path.

P32 note anchors:
- gradient story: Section `The Story Of The Derivative`, Eq. `p32-gradient-chain`;
- formal branch derivative: Eqs. `p31-chol-A`--`p31-chol-check`;
- prediction derivatives: Eqs. `p31-dot-pred-place`--`p31-dot-pred-cov`;
- observation derivatives: Eqs. `p31-dot-obs-place`--`p31-dot-Cxz`;
- innovation score: Proposition `Fixed Gaussian innovation score`;
- propagation: Eqs. `p31-dot-K`--`p31-dot-P`;
- end-to-end algorithm: Section `End-To-End Mathematical Algorithm`.
