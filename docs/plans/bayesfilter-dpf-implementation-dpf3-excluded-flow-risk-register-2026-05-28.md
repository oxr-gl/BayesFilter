# DPF3 Excluded Flow Risk Register

## Status

DPF3 execution artifact.  This register records flow families that are deferred
or excluded from the first BayesFilter-owned PF-PF implementation lane.

## Risk Register

| Flow family | Current evidence | Risk | Decision | Required future gate |
| --- | --- | --- | --- | --- |
| Kernel PFF | Student MP3 debug gate: reduced runs complete, but every step can hit max iterations. | Completed runs can mask non-converged flow iterations. | excluded pending debug | Bounded convergence gate with hit-max fraction controlled. |
| Stochastic flow / stochastic PFF | Student usability gates: some surfaces import or smoke, but missing assumptions remain. | Noise/covariance semantics and proposal density are not specified. | deferred | Clean-room stochastic-flow spec with target/proposal/density correction. |
| Learned/neural DPF flow | Student future-work gates: finite gradients for some paths, blocked drift for others. | Gradient finiteness can be mistaken for target validity. | deferred to DPF2/DPF4 | Component/objective spec and provenance gate. |
| HMC-facing PF-PF | Monograph `ch19e` boundary and IE7 fixed-scalar-only evidence. | Proposal-corrected value path may still not be a validated HMC target. | blocked pending separate evidence | Same-scalar, posterior/reference, sampler diagnostics. |
| Production flow backend | No DPF5/DPF6 evidence exists. | Premature API/default movement. | blocked | DPF6 production-boundary review plus separate patch plan. |

## Non-Implications

Excluding or deferring a flow family is not evidence against the scientific
idea.  It records that the current DPF3 artifact cannot use that family without
overclaiming or widening scope.
