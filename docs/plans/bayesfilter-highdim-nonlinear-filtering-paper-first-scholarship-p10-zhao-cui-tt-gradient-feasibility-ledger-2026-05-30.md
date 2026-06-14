# P10 Zhao-Cui TT Gradient Feasibility Ledger

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui JMLR 2024.
- Cui and Dolgov squared inverse Rosenblatt transport paper.
- Companion code `TTFun`, `TTSIRT`, `TTIRT`, `full_sol`, `pre_sol`.

what_is_not_concluded:
- No complete analytical gradient for Zhao-Cui TT filtering is claimed.
- No HMC readiness is claimed.
- No autodiff implementation is claimed.
- No BayesFilter implementation is claimed.

## Target

For a fixed-branch approximation, the candidate scalar is
\[
  \widehat\ell_T^{\rm TT}(\theta)
  =
  \sum_{t=1}^T \log \widehat Z_t^{\rm TT}(\theta).
\]

The formal score contract is
\[
  \nabla_\theta \widehat\ell_T^{\rm TT}(\theta)
  =
  \sum_{t=1}^T
  \frac{\nabla_\theta \widehat Z_t^{\rm TT}(\theta)}
       {\widehat Z_t^{\rm TT}(\theta)}.
\]

If a squared TT represents
\[
  \widehat q_t(u;\theta)
  =
  \phi_t(u;\theta)^2 + \tau_t\lambda(u),
\]
with fixed \(\tau_t\) and reference density \(\lambda\), then under dominated
differentiation:
\[
  \partial_i \widehat Z_t^{\rm TT}
  =
  \int 2\,\phi_t(u;\theta)\,\partial_i\phi_t(u;\theta)\,du.
\]

## Operation Classification

Smooth when fixed:
- transition and likelihood density evaluations;
- fixed basis evaluations;
- fixed affine transform \(u=L^{-1}(x-\mu)\) if \(L,\mu\) are smooth and
  branches fixed;
- finite TT coefficient contractions;
- fixed squared-TT normalizer contractions;
- fixed triangular-map Jacobian evaluation.

Piecewise smooth with branch constraints:
- Cholesky or SVD/QR factors used for preconditioning and marginalization;
- TT core SVD truncation if rank and active singular subspace are fixed;
- inverse-CDF root solves if monotonicity and bracket remain fixed.

Adaptive/discrete:
- TT-cross interpolation point selection;
- random enrichment samples;
- rank adaptation and `max_rank` clipping;
- `local_tol` truncation decisions;
- ESS-triggered resampling/reapproximation;
- `const = min(...)` random grid shift in `full_sol` and `pre_sol`;
- switching preconditioner options;
- hard safeguards such as `max(...,0)` in tensor convolution helpers.

Unsupported for full analytical HMC today:
- derivative of learned TT cores with respect to state-space parameters across
  adaptive cross/rank decisions;
- derivative of the random/debug sample design with respect to parameters;
- derivative of branch-changing preconditioned maps;
- derivative of smoothing/path-estimation weights as a fixed scalar used by
  ordinary HMC.

## Minimal Fixed-Branch Derivative Formula

If all TT branch objects are frozen, write the approximation as
\[
  \phi_t(u;\theta)
  =
  G_1(u_1;\theta)\cdots G_D(u_D;\theta),
\]
where the core dimensions and interpolation/basis choices are fixed.  Then
\[
  \partial_i \phi_t(u;\theta)
  =
  \sum_{k=1}^D
  G_1(u_1;\theta)\cdots
  \partial_iG_k(u_k;\theta)\cdots
  G_D(u_D;\theta).
\]
Substitution into the normalizer derivative gives the fixed-branch score.

This formula is useful but incomplete for production implementation unless
each \(\partial_iG_k\) is derived from the TT construction algorithm and
implemented for fixed interpolation sets and fixed ranks.

## Decision

`FIXED_BRANCH_GRADIENT_CONTRACT_STATED_COMPLETE_HMC_GRADIENT_NOT_EARNED`

Zhao-Cui should be promoted as a high-dimensional filtering and transport
candidate, not as a ready HMC likelihood backend.  HMC use requires a later
implementation phase that freezes or smooths branches and derives/tests the
same-scalar gradient.
