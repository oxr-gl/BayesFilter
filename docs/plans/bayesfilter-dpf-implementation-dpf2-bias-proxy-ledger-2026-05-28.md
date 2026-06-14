# DPF2 Bias And Proxy Ledger

## Status

DPF2 execution artifact.  This ledger preserves the distinction between
resampling exactness, relaxed-target bias, solver approximation, gradient
finiteness, and downstream evidence.

## Ledger

| ID | Component | Direct evidence | Bias/proxy label | Required test | What must not be concluded |
| --- | --- | --- | --- | --- | --- |
| DPF2-B01 | Hard categorical resampling | DPF1 classical PF semantics | exact classical resampling law, non-pathwise | Ancestor law and conditional-unbiasedness documentation | Pathwise differentiability. |
| DPF2-B02 | Soft resampling, affine summaries | `eq:bf-dr-soft-mean-preserved`; IE5 relaxed expectation checks | affine/mean-preserving under stated assumptions | Deterministic two-particle or analytic affine summary check | Nonlinear unbiasedness or categorical-law preservation. |
| DPF2-B03 | Soft resampling, nonlinear summaries | `eq:bf-dr-soft-test-bias`; IE5 nonlinear categorical delta | nonlinear-observable biased relaxed surrogate | Nonlinear observable comparison against categorical reference | Posterior equivalence or original likelihood preservation. |
| DPF2-B04 | EOT optimizer | `eq:bf-dr-eot-primal`; EOT source spine | exact for regularized OT object | Marginal constraints, epsilon, entropy convention, cost, barycentric map | Unregularized OT or categorical equivalence. |
| DPF2-B05 | Finite Sinkhorn | `eq:bf-dr-sinkhorn-residuals`; IE5 residual pass | finite-solver approximation | Row/column/mass/nonnegativity/finite residuals under budget ladder | Exact EOT convergence unless residual/convergence criteria are separately met. |
| DPF2-B06 | Solver gradient | `ch32` gradient-object table | gradient of selected computational graph/fixed point | Same scalar/object identification and finite gradient checks | Gradient of original categorical-resampling likelihood. |
| DPF2-B07 | Learned/amortized OT | IE6 deferred no approved artifact | deferred teacher-student proxy | Teacher/student provenance, residual, distribution, checkpoint, downstream check | Any learned-OT posterior, HMC, or production claim. |
| DPF2-B08 | Student future-work finite gradients | Student usability gates | comparison-only smoke/proxy | BayesFilter-owned reproduction only if later planned | Correctness, readiness, or source authority. |

## Wording Guards

- Never write "soft resampling is unbiased" without naming the observable class.
- Never write "Sinkhorn resampling preserves the posterior" without a correction
  or posterior-error argument.
- Never write "finite gradients validate DPF-HMC."
- Never use student finite-gradient probes as BayesFilter component evidence.
