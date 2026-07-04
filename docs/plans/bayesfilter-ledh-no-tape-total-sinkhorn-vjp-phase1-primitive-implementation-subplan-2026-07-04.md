# Phase 1 Subplan: Primitive No-Tape VJP Implementation

Date: 2026-07-04

Status: `DRAFT_PENDING_PHASE0`

## Phase Objective

Implement a no-`GradientTape`, no-`ForwardAccumulator` manual total VJP for the
finite streaming Sinkhorn transport primitive.

## Entry Conditions Inherited From Previous Phase

Phase 0 must freeze the target scalar, differentiated inputs, constant inputs,
and reverse obligations.

## Required Artifacts

- Code changes in:
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- Focused primitive tests in an existing or new test file under `tests/`.
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-result-2026-07-04.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

- `python -m py_compile` for edited Python files.
- Focused static test proving the production no-tape total helper contains no
  `GradientTape`, `ForwardAccumulator`, or `.gradient(`.
- Focused implementation check proving `epsilon0` receives a total cotangent:
  either `_filterflow_streaming_softmin_vjp` is extended to return epsilon
  cotangents, or Phase 1 provides an explicit no-tape epsilon reverse path.
- Focused smoke test that the helper returns finite cotangents on tiny tensors.
- Claude read-only review of implementation diff and Phase 1 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the repository contain a candidate no-tape total transport VJP implementation? |
| Baseline/comparator | Phase 0 target brief and current tape-backed total helper. |
| Primary criterion | Candidate implementation compiles, has no tape/forward-accumulator in the production helper, returns finite primitive cotangents on tiny tensors, and includes an explicit total cotangent path for `epsilon0`. |
| Veto diagnostics | Tape remains in production helper; stopped-key VJP reused as total VJP; missing `epsilon0` cotangent path; finite smoke fails; helper changes forward scalar; broad unrelated edits. |
| Explanatory diagnostics | Static audit, tensor shapes, tiny cotangent magnitudes. |
| Not concluded | No parity with tape, no finite-difference validation, no downstream score admission. |

## Forbidden Claims And Actions

- Do not claim correctness from finite smoke alone.
- Do not remove stopped-key helpers unless required and reviewed.
- Do not edit leaderboard artifacts.
- Do not run material GPU benchmarks.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- candidate code exists;
- local compile/static/smoke checks pass;
- the Phase 1 result proves `epsilon0` has a no-tape total cotangent path or
  blocks before Phase 2;
- Phase 1 result records edited symbols and nonclaims;
- Phase 2 validation subplan is refreshed and reviewed.

## Stop Conditions

Stop if:

- a no-tape reverse recursion cannot be implemented without changing the
  forward scalar;
- `epsilon0` cotangents cannot be represented without tape;
- local static checks find tape in the production helper;
- Claude blocks the implementation and the issue is not fixed within five
  rounds.

## Phase-End Duties

At the end of Phase 1:

1. run required local checks;
2. write Phase 1 result;
3. draft or refresh Phase 2 subplan;
4. review Phase 2 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
