# P53-M4B Subplan: Scaling Route TensorFlow Implementation

metadata_date: 2026-06-10
phase: P53-M4B
status: DRAFT_PENDING_CLAUDE_REVIEW

## Objective

Implement the `C_scale` route selected and derived in P53-M4A as TensorFlow code.
This phase may not start unless P53-M4A emits
`PASS_P53_M4A_SCALING_ROUTE_DERIVATION`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does BayesFilter contain an executable TensorFlow implementation of the selected `C_scale` route, distinct from `C_low`, with replay and route-width metadata? |
| Baseline/comparator | P53-M4A derivation artifact, P53-M2 `C_low` implementation, current dense route, and P30 spatial SIR equations. |
| Primary pass criterion | New TensorFlow implementation follows the M4A equations, avoids dense all-pairs production semantics, preserves gradients, emits deterministic replay metadata, and exposes `R_eff` or conservative route-width/memory metadata. |
| Veto diagnostics | M4A pass token absent; implementation is a contract only; `C_low` is relabeled as `C_scale`; differentiable path uses NumPy; route silently materializes dense all-pairs transition semantics; metadata missing. |
| Not concluded | Passing M4B does not prove lower-rung tie-out, rank-selection readiness, d=18/d=50/d=100 readiness, or HMC readiness. |

## Planned Work

1. Add a route implementation module or extend `bayesfilter/highdim/transition_route.py`.
2. Keep `C_low` and `C_scale` APIs and metadata separate.
3. Implement only the M4A-selected route.
4. Add source/static tests rejecting:
   - use of `C_low` metadata as `C_scale`;
   - full dense all-pairs production transition semantics;
   - missing replay/route-width metadata.
5. Add dynamic smoke tests for finite values, deterministic replay, shape
   contracts, and TensorFlow gradient connectivity.
6. Emit an M4B manifest with route id, route class, selected design, metadata,
   and nonclaims.

## Required Result

`docs/plans/bayesfilter-highdim-zhao-cui-p53-m4b-scaling-route-implementation-result-2026-06-10.md`

Required token:

`PASS_P53_M4B_SCALING_ROUTE_IMPLEMENTATION` or
`BLOCK_P53_M4B_SCALING_ROUTE_IMPLEMENTATION`
