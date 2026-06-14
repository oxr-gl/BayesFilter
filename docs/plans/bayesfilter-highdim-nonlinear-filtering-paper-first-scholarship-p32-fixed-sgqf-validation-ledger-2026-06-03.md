# P32 FixedSGQF Validation Ledger

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.

what_is_not_concluded:
- This ledger does not report completed large-scale experiments.
- This ledger does not conclude FixedSGQF accuracy, memory efficiency, or production readiness.
- This ledger specifies mathematical validation models and diagnostics for a future implementation.

## Validation Families To Add In P32

| family | mathematical purpose | pass/veto role |
|---|---|---|
| small linear-Gaussian model | exact Kalman reference for value and moments | added to P32 note; veto if fixed SGQF disagrees beyond numerical tolerance |
| scalar quadratic observation cell | shows Gaussian projection limitation and cloud-sensitive moments | added to P32 note; explanatory plus finite-difference diagnostic |
| nonlinear cloud-sensitive two-dimensional model | detects duplicate-merge and signed-weight bugs | added to P32 note; veto for implementation plumbing |
| moderate-dimensional product/block nonlinear model | tests memory growth and separable/nonseparable interactions | added to P32 note; explanatory/performance |
| deliberately hard all-coordinate interaction | exposes failure of low-level sparse grids | added to P32 note; rejection/stress test |
| orbit-style Jia--Xin--Cheng benchmark | source-faithful empirical context | added to P32 note; future empirical benchmark, not P32 proof |
| finite-difference ladder | tests same-scalar gradient | added to P32 note; veto for implementation |

## Default Diagnostic Fields

Future implementation reports should record:

- dimension \(b\), level \(L\), point count \(M\), and weight sums;
- minimum and maximum signed weights;
- duplicate-merge count;
- memory for saved cloud, factors, and sensitivities;
- wall time per filtering step and per gradient step;
- PD/PSD status of \(P_t^-\), \(S_t\), and \(P_t\);
- log-likelihood contribution;
- finite-difference table \(h,D(h),G,|D(h)-G|,\rho(h)\);
- branch-validity flags.

## Current Status

validation_status: `SPEC_EXPANDED_IN_NOTE_PENDING_REVIEW`
