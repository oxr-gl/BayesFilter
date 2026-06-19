# P71 Phase 7 Subplan: Value-Gradient And HMC Diagnostic Readiness

metadata_date: 2026-06-16
status: DRAFT_PENDING_PHASE6_RESULT
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 7

## Phase Objective

Check whether the admitted d18 value path exposes finite, reproducible
gradients for the intended HMC variables, and whether a tiny fixed-kernel HMC
diagnostic can execute without production-readiness claims.

## Entry Conditions Inherited From Previous Phase

- Phase 6 passed all five seeds.
- Phase 6 identified the exact scalar value path and HMC variables.
- Any theta-free or latent-only boundary is explicitly documented.

## Required Artifacts

- Phase 7 result note.
- Gradient check artifact.
- Tiny HMC diagnostic artifact, if authorized by the gradient gate.
- Refreshed Phase 8 closeout subplan.

## Required Checks/Tests/Reviews

- Run finite-value and autodiff gradient checks on fixed inputs.
- Compare autodiff gradients to finite differences or another reviewed local
  gradient diagnostic where feasible.
- GPU/HMC commands must run in trusted/escalated context if they use GPU.
- Claude read-only review of gradient/HMC interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the d18 value path provide finite gradients and a minimal HMC diagnostic route for the intended variables? |
| Baseline/comparator | Phase 6 admitted five-seed configuration and a frozen scalar value target. |
| Primary criterion | Finite value, finite gradient, stable repeated gradient evaluation, and tiny fixed-kernel HMC execution only if gradient diagnostics pass. |
| Veto diagnostics | Nondifferentiable random path, NaN/Inf gradients, finite-difference mismatch beyond frozen tolerance, HMC divergences treated as success, or theta-free boundary hidden. |
| Explanatory diagnostics | Gradient norms, finite-difference errors, tiny HMC acceptance/divergence/energy diagnostics, runtime, device status. |
| Not concluded | No production HMC readiness, no NUTS readiness, no posterior correctness, no default sampler policy. |
| Artifact | Phase 7 result note and gradient/HMC artifacts. |

## Forbidden Claims/Actions

- Do not run HMC if the gradient gate fails.
- Do not treat a tiny fixed-kernel HMC smoke as production readiness.
- Do not introduce a new autodiff backend without reviewed exception.

## Exact Next-Phase Handoff Conditions

Phase 8 may begin after Phase 7 writes either a passed diagnostic-readiness
result or a blocker with explicit nonclaims.

## Stop Conditions

Stop if gradients are nonfinite, nondeterministic in the fixed path, or not
defined for the intended variables.
