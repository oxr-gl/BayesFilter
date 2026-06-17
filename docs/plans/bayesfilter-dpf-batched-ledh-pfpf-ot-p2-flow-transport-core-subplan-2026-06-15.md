# Phase 2 Subplan: Batched LEDH Flow And Transport Core

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_PRECHECK`

## Phase Objective

Implement compiled-safe batched LEDH flow and annealed-transport adapter cores
for tensors with leading parameter batch axis.

## Entry Conditions Inherited From Previous Phase

- Phase 1 shape/callback contract passed.
- Deterministic fixed inputs, callback shapes, fixed branch masks, and
  tolerance policy are locked.
- Public API/default changes remain forbidden.

## Required Artifacts

- Batched LEDH flow core in the experimental module.
- Graph-safe batched masked annealed transport core in the experimental module,
  using existing internal annealed-transport algebra where possible.
- Unit tests for shape, finite outputs, row independence, and compiled CPU
  smoke.
- Phase 2 result.
- Refreshed Phase 3 subplan.

## Required Checks, Tests, And Reviews

- CPU-only pytest for batched flow/transport core.
- `tf.function` compile smoke with small `B,N,D`.
- Row independence test by perturbing one row.
- Local marker check that Phase 2 core functions do not call `.numpy()` or
  Python RNG.
- Test that fixed resampling masks select transported rows without runtime ESS
  decisions.
- Claude read-only review if implementation semantics or transport-gradient
  policy changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the per-time LEDH flow and OT transport components run over `[B,N,D]` without eager scalar decisions? |
| Baseline/comparator | Scalar LEDH flow and existing annealed transport behavior. |
| Primary pass criterion | Core tests pass, CPU `tf.function` smoke passes, no `.numpy()` in compiled core, fixed mask semantics hold, row independence holds. |
| Veto diagnostics | Nonfinite flow/log-det/transport; row cross-talk; scalar-only Python loop in compiled core; runtime ESS branch in core; transport semantics drift. |
| Explanatory diagnostics | Log-det ranges, transport residuals, ESS mask behavior, compile smoke time. |
| Not concluded | No full filtering value parity, no score correctness, no GPU performance. |
| Artifact preserving result | Phase 2 result and test output. |

## Forbidden Claims And Actions

- Do not claim full LEDH-PFPF-OT correctness.
- Do not benchmark GPU.
- Do not implement full filtering value recursion in Phase 2.
- Do not claim scalar parity beyond one-step component parity tests.
- Do not change existing scalar implementation except for narrowly reviewed
  shared helper extraction, if required.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if the batched per-time components pass tests and Phase
3 subplan defines scalar-stack value-recursion parity protocol with fixed
inputs, fixed masks, and Phase 0 tolerances.

## Stop Conditions

Stop if batched flow cannot match scalar semantics, transport cannot be masked
without eager branching, or compiled core requires unsupported TensorFlow ops.

## End-Of-Phase Procedure

Run checks, write result, refresh Phase 3 subplan, and review Phase 3.
