# Phase 0 Result: Primitive Target And Math Freeze

Date: 2026-07-04

Status: `PASS_PRIMITIVE_TARGET_FREEZE`

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Freeze the no-tape total VJP target as the current finite streaming Sinkhorn transport value route. |
| Primary criterion status | Passed: the target brief names the scalar, differentiated inputs, reverse obligations, and current wrong routes. |
| Veto diagnostic status | No implementation edit was made; stopped partial derivatives are classified as wrong relative to the unstopped target. |
| Main uncertainty | Whether the existing softmin VJP supports epsilon cotangents needed for `epsilon0`; Phase 1 must verify or repair this. |
| Next justified action | Implement a candidate no-tape primitive VJP in Phase 1. |
| Not concluded | No implementation correctness, no runtime viability, no downstream score correctness, no HMC readiness. |

## Evidence Contract Result

Question:

- What exact finite transport scalar must the no-tape VJP differentiate?

Answer:

- The target is the same finite streaming transport value computed by
  `_filterflow_manual_streaming_finite_transport_value_total_vjp` and used by
  `_filterflow_manual_streaming_finite_transport_total_vjp`.

Differentiated inputs for the current primitive route:

- `scaled_x`;
- `particles`;
- `logw`;
- `epsilon0`.

Intentionally constant inputs for the current primitive route:

- `eps`;
- `scaling`;
- finite `steps`;
- chunk sizes.

If a later model row makes `eps` or `scaling` parameter-dependent, that row is
not admitted until those derivatives are added or the row target explicitly
freezes them.

## Code Anchors Inspected

- `_filterflow_streaming_softmin`;
- `_filterflow_streaming_softmin_vjp`;
- `_filterflow_streaming_finite_sinkhorn_potentials_total_vjp`;
- `_filterflow_manual_streaming_finite_transport_value_total_vjp`;
- `_filterflow_manual_streaming_finite_transport_total_vjp`.

## Artifacts

- Primitive brief:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-primitive-target-brief-2026-07-04.md`
- Phase 1 subplan:
  `docs/plans/bayesfilter-ledh-no-tape-total-sinkhorn-vjp-phase1-primitive-implementation-subplan-2026-07-04.md`

## Checks Run

- Inspected current code anchors in `annealed_transport_tf.py`.
- Local content check for differentiated inputs and wrong-route classification:
  passed.

## Handoff To Phase 1

Phase 1 may begin implementation only under the frozen target above.  It must
verify whether `_filterflow_streaming_softmin_vjp` needs epsilon cotangent
support before claiming total VJP for `epsilon0`.
