# P8 Ch34 Gradient Obligation Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: P8 plan, rewritten `ch34`, `ch18_svd_sigma_point.tex`, P7 gradient
ledger, MathDevMCP diagnostics, and the scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude exact nonlinear likelihood
gradients, HMC convergence, posterior accuracy, production readiness, or
machine-certified proof validity.

## Gradient Obligations

| Obligation | `ch34` anchor | Status | Support class | Notes |
|---|---|---|---|---|
| Name the approximate scalar \(\widehat\ell_t\). | Eq. `bf-hd-gq-loglik` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Gaussian innovation scalar; not exact nonlinear likelihood in general. |
| Derive fixed-rule point derivative \(\dot\chi\). | Eq. `bf-hd-gq-point-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Requires fixed offsets/weights and differentiable factor branch. |
| Derive \(\dot z\) by chain rule. | Eq. `bf-hd-gq-point-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Requires differentiable \(h_\theta\). |
| Derive \(\dot{\bar z}\). | Eq. `bf-hd-gq-point-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Weighted sum derivative. |
| Derive \(\dot S\). | Eq. `bf-hd-gq-S-v-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Product rule on centered outer products. |
| Derive \(\dot v\). | Eq. `bf-hd-gq-S-v-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION` | Recorded data gives \(\dot y=0\). |
| Derive solve-form approximate innovation score. | Prop. `bf-hd-gq-score` | `FULL_DERIVATION_READY` | `PROJECT_DERIVATION`; narrow MCP diagnostic attempted | Uses log-det and inverse derivative identities. |
| Label EKF/IEKF branch smoothness. | Section `bf-hd-derivative-filters`; HMC table | `BRANCH_DISCIPLINE_RECORDED` | `PROJECT_DERIVATION` | Iteration/convergence branches are not globally smooth. |
| Label UT/CKF/high-degree/GHQ fixed-rule HMC status. | Method sections; HMC table | `APPROXIMATE_TARGET_ONLY` | `PROJECT_DERIVATION` | No convergence claim. |
| Label SGQF/ASGHF adaptive status. | Sections `bf-hd-sgqf`, `bf-hd-asghf`; HMC table | `CASE_SPLIT_RECORDED` | `PROJECT_DERIVATION` | Fixed nonadaptive admissible; frozen adaptive branch-local; live adaptive not admissible until smoothed. |

## Same-Scalar Contract

Every HMC-admissible label in `ch34` is conditional on:

- the scalar being exactly \(\widehat\ell_t\) in Eq. `bf-hd-gq-loglik`;
- the gradient being exactly the derivative of that scalar on the declared
  branch;
- positive definite \(S_t\);
- fixed quadrature offsets/weights or explicitly differentiated tuning
  parameters;
- differentiable covariance factor and observation map;
- no hidden clipping, pruning, floor, pivot, active-subspace, or adaptive
  index-set change along the HMC trajectory.

## What Remains Human-Reviewed

The gradient derivation is a project derivation with narrow MathDevMCP
diagnostics only.  It is not broad machine certification of the chapter or of
any HMC algorithm.
