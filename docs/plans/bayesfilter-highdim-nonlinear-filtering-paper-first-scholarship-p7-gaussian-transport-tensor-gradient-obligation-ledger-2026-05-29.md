# P7 Gaussian/Transport/Tensor Gradient Obligation Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P7 plan, P6 result, `ch18_svd_sigma_point.tex`, `ch34`, `ch35`,
`ch36`, `ch37`, prior P1--P6 high-dimensional nonlinear filtering artifacts,
and the scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude exact posterior-gradient
validity, HMC convergence, production readiness, tensor-method validation,
transport-method validation, or machine-certified proof validity.

## Gradient Obligations

| Obligation | Chapter anchor | Status | Support |
|---|---|---|---|
| Name the approximate scalar for Gaussian/quadrature filters. |
`ch34`, eq. `bf-hd-gq-loglik` | `FULL_DERIVATION_READY` | Project derivation
using Gaussian innovation likelihood. |
| Derive deterministic quadrature point derivatives
\(\dot\chi,\dot z,\dot{\bar z}\). | `ch34`, eq. `bf-hd-gq-point-score` |
`FULL_DERIVATION_READY` | Project chain-rule derivation, patterned after
`ch18` sigma-point derivative treatment. |
| Derive \(\dot S\) and \(\dot v\). | `ch34`, eq. `bf-hd-gq-S-v-score` |
`FULL_DERIVATION_READY` | Product rule for covariance outer products. |
| Derive approximate Gaussian innovation score. | `ch34`,
Prop. `bf-hd-gq-score` | `FULL_DERIVATION_READY` | Project derivation;
MathDevMCP scalar check verified after explicit substitution. |
| Distinguish exact likelihood gradient from approximate Gaussian innovation
gradient. | `ch34`, `ch36` | `FULL_DERIVATION_READY` | Project derivation and
P5 same-scalar contract. |
| EKF/IEKF/second-order EKF HMC label. | `ch34`, derivative-filter table |
`NEEDS_BRANCH_DISCIPLINE` | Branch/convergence conditions explicitly labeled. |
| UKF/CKF/high-degree CKF/tensor-product GHQ fixed-rule HMC label. | `ch34`,
HMC label table | `FULL_DERIVATION_READY_FOR_APPROXIMATE_TARGET` | Same scalar
and score apply only on fixed smooth branches. |
| Sparse-grid/adaptive sparse-grid HMC label. | `ch34`, sparse-grid section |
`CASE_SPLIT_REPAIRED_AFTER_CLAUDE_REVIEW` | Nonadaptive fixed index set can be
admissible for a declared smooth scalar; a frozen adaptive branch is local
only; active adaptive changes are not ordinary smooth HMC gradients. |
| Particle filter likelihood-gradient boundary. | `ch35`, particle-collapse
section | `REMOVE_OR_WEAKEN_EXACT_HMC_CLAIM` | Ordinary resampling is labeled
not HMC-admissible until smoothed; fixed no-resampling branches are local only. |
| Transport proposal correction and transformed HMC scalar. | `ch35`,
transport section | `FULL_DERIVATION_READY` | Change-of-variables and
importance correction derivations; MathDevMCP scalar correction identity
verified. |
| TT density/operator scalar-gradient contract. | `ch35`, TT density section |
`DIAGNOSTIC_ONLY_UNTIL_CONCRETE_SCALAR_EXISTS` | P7 demotes TT/PDE HMC language:
requires declared \(\widehat Z_t\), fixed differentiable branch, and
rank/pivot/truncation policy before any operational HMC claim. |
| TN covariance/factor HMC boundary. | `ch35`, TN section |
`DIAGNOSTIC_ONLY_UNLESS_EMBEDDED_IN_FIXED_GAUSSIAN_SCALAR` | PSD/factor gate
and Gaussian score inheritance stated. |

## Main Gradient Formula Added

For fixed deterministic Gaussian rule,
\[
  \widehat\ell_t
  =
  -\frac12\{\log\det S_t+v_t^\top S_t^{-1}v_t+n_y\log(2\pi)\},
\]
with \(S_tw_t=v_t\),
\[
  \partial_i\widehat\ell_t
  =
  -\frac12
  \left[
    \tr(S_t^{-1}\dot S_t^{(i)})
    +2\dot v_t^{(i)\top}w_t
    -w_t^\top\dot S_t^{(i)}w_t
  \right].
\]

This is the derivative of the declared approximate Gaussian innovation scalar.
It is not the exact nonlinear filtering likelihood gradient except in exact
Gaussian cases or under a separate exact-correction proof.
