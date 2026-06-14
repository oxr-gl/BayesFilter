# DPF2 Deferred Neural And Learned Path Register

## Status

DPF2 execution artifact.  Learned/amortized OT and neural resampling are
deferred from implementation authority in this lane until their own
BayesFilter-owned component specs and provenance gates exist.

## Deferred Paths

| Path | Current evidence | Required before inclusion | Status |
| --- | --- | --- | --- |
| Learned/amortized OT resampler | Monograph chapter `ch19d`; IE6 deferred; student docs report finite gradients/speedups. | Teacher variant, epsilon/budget/stabilization, training distribution, architecture, checkpoint provenance, residual metrics, downstream filter effect, non-implications. | deferred |
| Set Transformer / neural resampler | References `zaheer2017deep`, `lee2019set`; student MLCOE transformer gate blocked by environment drift. | Objective semantics, permutation contract, artifact provenance, debug gate, finite output/gradient, downstream bias/proxy contract. | deferred/debug gate |
| Differentiable PF with learned resampler | Student future-work gates mark some smokes ok, some blocked. | BayesFilter-owned DPF clean-room spec and DPF4 objective contract. | deferred to DPF4/DPF5 |
| Neural OT inside HMC | Student docs/notebooks overclaim validation language. | Named scalar target, same-scalar value/gradient, posterior/reference diagnostics, sampler diagnostics, and correction/error argument. | blocked pending separate evidence |

## Quarantine Rules

- Student checkpoints, notebook outputs, and README claims are not accepted as
  BayesFilter-owned teacher/student artifacts.
- Speedup, heldout MSE, finite gradients, or same-regime proxy results do not
  promote learned/neural resampling.
- A future learned/neural implementation plan must cite the exact paper
  sections or local derivations used for its teacher and architecture claims.

## Next Authorized Action

The next authorized action is to carry these deferred rows into DPF4 and DPF5
as evidence requirements.  No learned/neural component implementation is
authorized by DPF2.
