# P9 Ch34 HMC Admissibility Ledger

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Rewritten `ch34`, P9 plan, P8/P9 gradient ledgers,
`ch18_svd_sigma_point.tex`, and the scholarly literature audit policy.

what_is_not_concluded: This ledger does not conclude HMC convergence, exact
posterior correctness, production readiness, default readiness, or that any
approximate target is scientifically adequate for a client model.

## Labels

| Method family | P9 label | Reason |
|---|---|---|
| EKF under declared fixed scalar | `HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET` | Smooth fixed approximation if the branch and derivatives are declared. |
| IEKF/live iteration branches | `NOT_HMC_ADMISSIBLE_AS_STATED` | Iteration count/convergence basin can change the scalar. |
| UKF/CKF/high-degree CKF with fixed rules | `HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET` | Fixed nodes/weights and smooth factor branches define an approximate scalar. |
| Tensor-product GHQF | `DIAGNOSTIC_OR_REFERENCE_ONLY` in high dimension | Scalar is clear, but point count is the practical veto. |
| Fixed SGQF | `HMC_ADMISSIBLE_FIXED_APPROXIMATE_TARGET` | Selected approximate target; fixed sparse grid is part of scalar. |
| ASGHF grid selection followed by freeze | `HMC_ADMISSIBLE_ONLY_AFTER_GRID_FREEZE` | After freeze, it reduces to fixed SGQF. |
| Live adaptive ASGHF | `NOT_HMC_ADMISSIBLE_AS_STATED` | Discrete index-set changes are not a smooth scalar target. |

## HMC Contract

HMC may only consume a scalar and gradient pair that are the same mathematical
object.  For P9, that object is the fixed sparse-grid approximate likelihood
\(\widehat\ell_T^{\rm FSGQ}\).  Adaptive grid selection may be used before HMC
to choose the cloud; it may not run inside the HMC trajectory unless a smooth
and explicitly differentiated selection mechanism is introduced.
