# SSL-LSTM Filter-HMC Phase 8 Reset Memo

Date: 2026-07-05

Status: `LAUNCH_SMOKE_BOUNDARY_REACHED`

## Current Boundary

The visible SSL-LSTM filter-HMC runbook is closed at a launch-smoke boundary.
The completed evidence shows that the admitted `fixed_sgqf` and `svd_ukf`
adapters can enter a tiny fixed-kernel HMC mechanics run and produce finite
launch-smoke artifacts. This is not replicated HMC evidence.

## Candidate State

| Candidate | State | Boundary |
| --- | --- | --- |
| `fixed_sgqf` | `passed_launch_smoke` | Tiny fixed-kernel HMC mechanics smoke only. |
| `svd_ukf` | `passed_launch_smoke` | Tiny fixed-kernel HMC mechanics smoke only. |
| `zhaocui_fixed` | `blocked` | Missing SSL-LSTM Zhao-Cui fixed adapter. |
| `ledh_streaming_ot` | `blocked` | Missing manual VJP streaming-OT score path. |

## Evidence Boundaries

- Native divergence telemetry was not exposed by the TFP kernel results; this
  must not be interpreted as zero divergences.
- Acceptance, runtime, finite samples, and finite initial value/score are
  launch-smoke diagnostics only.
- R-hat, ESS, replicated uncertainty, posterior correctness, and invariant
  estimation quality were not evaluated.
- Phase 6 heldout predictive log score remains a proxy/explanatory diagnostic,
  not a Phase 7 promotion criterion.

## Next Valid Continuations

A continuation must start from a separately reviewed plan and choose exactly one
scope:

- implement a missing Zhao-Cui fixed SSL-LSTM adapter with required
  paper/source anchors;
- implement LEDH manual VJP streaming-OT scoring;
- run a longer replicated HMC validation tier for admitted adapters;
- prepare a separate product/API/default-readiness plan.

## Nonclaims

- no method superiority
- no HMC convergence
- no R-hat or ESS evidence
- no exact posterior correctness
- no parameter identifiability
- no source-faithful Zhao-Cui or LEDH completion
- no GPU/XLA production-readiness evidence
- no default policy change
