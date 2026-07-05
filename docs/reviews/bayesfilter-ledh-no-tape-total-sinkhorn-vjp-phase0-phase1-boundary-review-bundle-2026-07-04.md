# Review Bundle: No-Tape Total Sinkhorn VJP Phase 0/1 Boundary

Date: 2026-07-04

## Role

Claude is read-only reviewer.  Do not edit files, run commands, or change
state.

## Objective

Review whether Phase 0 correctly freezes the primitive target and whether Phase
1 is safe to start implementation.

## Exact Artifacts

- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-primitive-target-brief-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase0-primitive-target-math-result-2026-07-04.md`
- `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-subplan-2026-07-04.md`

## Packet Summary

Phase 0 freezes the primitive as the current finite streaming transport value
computed by:

- `_filterflow_manual_streaming_finite_transport_value_total_vjp`;
- `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`;
- `_filterflow_streaming_transport_from_potentials`.

The target scalar for VJP validation is:

```text
scalar = reduce_sum(transported * upstream_transported)
```

Differentiated inputs for the current primitive:

- `scaled_x`;
- `particles`;
- `logw`;
- `epsilon0`.

Constant inputs for the current primitive:

- `eps`;
- `scaling`;
- finite `steps`;
- chunk sizes.

Known Phase 1 obligation:

- verify whether `_filterflow_streaming_softmin_vjp` needs epsilon cotangent
  support before claiming total VJP for `epsilon0`.

Round-1 repair:

- Phase 1 now requires an explicit `epsilon0` total cotangent path.
- Missing `epsilon0` cotangent support is a Phase 1 veto.
- Phase 1 cannot hand off to Phase 2 unless its result proves `epsilon0` has a
  no-tape total cotangent path or blocks before Phase 2.

Forbidden:

- stopped-scale/key derivatives must not be called scores for the unstopped
  target;
- Phase 1 finite smoke must not be called correctness;
- no GPU/material score claim is authorized by Phase 0.

## Review Questions

1. Is the primitive target stated clearly enough to begin implementation?
2. Are differentiated and intentionally constant inputs explicit?
3. Does the plan correctly block stopped partial derivatives as scores?
4. Does Phase 1 preserve the need to verify/add epsilon cotangents for
   `epsilon0`?
5. Is any downstream score correctness or HMC claim made too early?

End with exactly:

`VERDICT: AGREE`

or

`VERDICT: REVISE`
