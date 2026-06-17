# Phase 3 Subplan: Batched Value Recursion And Parity

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_PRECHECK`

## Phase Objective

Implement batched LEDH-PFPF-OT value recursion and prove parity against scalar
LEDH-PFPF-OT for `B=1` and stacked `B=20` deterministic rows.

## Entry Conditions Inherited From Previous Phase

- Batched flow and transport core passed shape, finite, row independence, and
  compile smoke checks.
- Scalar-stack parity protocol must use fixed initial particles, fixed
  pre-flow particles, fixed ESS masks, and Phase 0 tolerances.
- Full value recursion may use batched callbacks from Phase 1 and one-step
  components from Phase 2 only; public API/default changes remain forbidden.

## Required Artifacts

- Batched value recursion function.
- Deterministic scalar-row comparator helper in tests using the same fixed
  inputs and fixed masks.
- Tests for B=1 parity, B=20 parity, row permutation, identical-row equality,
  fixed-mask behavior, CPU `tf.function` smoke, and no public export drift.
- Phase 3 result.
- Refreshed Phase 4 subplan.

## Required Checks, Tests, And Reviews

- CPU-only pytest for value parity.
- CPU `tf.function` compile smoke.
- Local check for `.numpy()` in value core.
- Local check that value core does not call `tf.random`, `np.random`, Python
  RNG, or runtime ESS branch decisions.
- B=20 parity must compare against scalar-stack rows built from the same fixed
  fixture, not a stochastic scalar runner.
- Claude review of parity result if any tolerance or baseline exception is
  introduced.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the batched value recursion preserve the scalar relaxed LEDH-PFPF-OT objective row by row? |
| Baseline/comparator | Fixed-contract scalar-row LEDH-PFPF-OT recursion using Phase 0 scalar semantics and Phase 1/2 fixed inputs. |
| Primary pass criterion | B=1 and B=20 scalar-stack parity pass within predeclared tolerance; row permutation, identical-row, fixed-mask, and graph-smoke tests pass. |
| Veto diagnostics | Parity failure; stochastic mismatch; row cross-talk; uncompiled-only path; runtime ESS branch; changed transport objective. |
| Explanatory diagnostics | Value deltas, ESS deltas, transport residual deltas, log-det ranges. |
| Not concluded | No score correctness, no GPU speed, no production readiness. |
| Artifact preserving result | Phase 3 result and parity artifacts. |

## Forbidden Claims And Actions

- Do not claim gradient correctness.
- Do not loosen parity tolerance after seeing results without blocker review.
- Do not compare to unrelated PF/UKF references as pass criteria.
- Do not use the eager scalar runner's runtime `.numpy()` ESS decision as the
  Phase 3 branch source.
- Do not run GPU benchmarks in Phase 3.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if value parity gates pass and Phase 4 defines the
relaxed-objective score semantics and finite-difference tolerance before
execution.

## Stop Conditions

Stop if scalar parity cannot be achieved under identical deterministic inputs or
if scalar baseline behavior is too stochastic/eager to serve as comparator, or
if value recursion requires runtime RNG/ESS branch decisions.

## End-Of-Phase Procedure

Run checks, write result, refresh Phase 4 subplan, and review Phase 4.
