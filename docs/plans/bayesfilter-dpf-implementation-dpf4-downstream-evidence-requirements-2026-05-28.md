# DPF4 Downstream Evidence Requirements

## Status

DPF4 execution artifact.  This register states what evidence is required before
objective/gradient artifacts can support stronger filtering, posterior, HMC, or
production claims.

## Evidence Requirements

| Claim sought | Minimum additional evidence |
| --- | --- |
| Gradient-valid component | Same-scalar value/gradient parity for the named component scalar. |
| Relaxed-target filtering candidate | DPF1 reference checks, DPF2 component residuals, same-scalar gradient check, posterior/reference sensitivity label. |
| PF-PF research candidate | DPF3 proposal/Jacobian/corrected-weight parity, finite-particle variance, same-scalar gradient, controlled nonlinear fixture. |
| Learned-surrogate candidate | Teacher/student provenance, residuals on declared distribution, OOD stress, downstream filtering effect, non-implication text. |
| Pseudo-marginal candidate | Nonnegative unbiased estimator evidence and extended-space target construction; not smooth surrogate HMC. |
| HMC research candidate | Named scalar target, same-scalar gradient, finite/repeatability checks, posterior/reference comparison, sampler diagnostics. |
| Bank-facing or model-risk claim | Model-class stress tests, challenger comparisons, reproducible artifacts, independent review, governance controls. |
| Production API candidate | DPF5 validation plus DPF6 production-boundary review and separate production patch plan. |

## Diagnostics That Can Veto

- target-status ambiguity;
- same-scalar failure;
- Jacobian/log-det mismatch for PF-PF;
- Sinkhorn residual or stabilization failure;
- learned teacher/student provenance absence;
- posterior/reference disagreement beyond declared tolerance;
- HMC divergences, bad R-hat/ESS/MCSE, or energy diagnostics under a sampler
  plan;
- production API/dependency/device instability.

## Explanatory-Only Diagnostics

- runtime speedups;
- finite output/gradient smokes without parity;
- student same-regime comparisons;
- heldout MSE for learned maps without downstream check;
- ESS or RMSE proxy rows without independent reference status;
- one-seed or short-chain sampler behavior.

## DPF4 Consequence

The next phases may design validation harnesses and production boundary reviews.
No DPF4 artifact authorizes an HMC posterior claim, production movement, or
banking/model-risk conclusion.
