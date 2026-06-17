# Phase 4 Subplan: Batched Value+Score

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_PRECHECK`

## Phase Objective

Add batched value+score evaluation for the relaxed LEDH-PFPF-OT objective and
validate finite scores with finite-difference diagnostics.

## Entry Conditions Inherited From Previous Phase

- Batched value recursion passed scalar-stack parity for B=1 and B=20.
- Relaxed objective semantics are locked to fixed initial particles, fixed
  pre-flow particles, fixed resampling masks, fixed observations, and
  deterministic TensorFlow callbacks.
- The score target is the TensorFlow autodiff gradient of the sum of row-local
  relaxed batched values with respect to `theta_batch`.

## Required Artifacts

- Batched value+score wrapper returning `value: [B]` and `score: [B,p]`.
- Gradient tests, finite-difference tests, row-independence gradient tests.
- Phase 4 result.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, And Reviews

- CPU-only pytest for value+score shape, finite score, row independence.
- Tiny central finite-difference gradient check on the deterministic DPF
  no-resampling fixture with row-local parameterization.
- Active-transport fixture check for finite scores and row-locality only.
- CPU `tf.function` compile smoke.
- Claude review of gradient claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does TensorFlow autodiff produce finite row-local scores for the relaxed batched LEDH-PFPF-OT objective? |
| Baseline/comparator | Batched value recursion plus central finite differences on tiny deterministic no-resampling DPF fixture with identical fixed tensors/masks. |
| Primary pass criterion | Score shape `[B,p]`, finite scores, row-locality, CPU graph smoke, and no-resampling finite-difference diagnostic within `rtol=2e-4, atol=2e-4`. |
| Veto diagnostics | Nonfinite scores; cross-row gradient leakage; no-resampling finite-difference mismatch outside tolerance; categorical PF gradient claim. |
| Explanatory diagnostics | Active-transport finite-difference delta, per-parameter gradient deltas, max score norm, transport-gradient mode. |
| Not concluded | No categorical PF score, no HMC readiness, no large-model validity. |
| Artifact preserving result | Phase 4 result and gradient artifacts. |

## Forbidden Claims And Actions

- Do not claim score is classical PF likelihood gradient.
- Do not use finite-difference passing as posterior correctness.
- Do not benchmark GPU in Phase 4.
- Do not use active annealed transport to claim finite-difference equivalence
  without a separate reviewed transport-gradient boundary. The Phase 4
  finite-difference equivalence test uses a no-resampling fixture.
- Do not treat active-transport finite-difference mismatch as a continuation
  veto if no-resampling finite differences, active-transport finiteness, and
  row-locality pass; record it as explanatory transport-gradient evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if value+score correctness gates pass and Phase 5
benchmark plan predeclares JIT-only CPU/GPU commands, comparators, and memory
limits.

## Stop Conditions

Stop if gradients are nonfinite, row-cross-coupled, or cannot be checked
against finite differences on the no-resampling tiny fixture.

## End-Of-Phase Procedure

Run checks, write result, refresh Phase 5 subplan, and review Phase 5.
