# Manual Adjoint Phase 4 Subplan: Loop-Adjoint Integration Design

status: DRAFT_READY_AFTER_M3_REVIEW
date: 2026-06-22
phase: M4-LOOP-ADJOINT-DESIGN

## Phase Objective

Design the LEDH-PFPF-OT filter-loop integration contract for the private
manual/custom-gradient route before wiring it into the recursive filter.  The
phase decides what is retained, replayed, stopped, or differentiated at each
time step.

## Entry Conditions

- M3 private dense custom-gradient prototype passes its focused tests and
  read-only review gate.
- Supported and unsupported transport modes are recorded.
- No public/default integration has occurred yet.
- M3 recorded the retained/replay handoff for:
  `manual_dense_finite_sinkhorn_stopped_scale_keys`.
- M3 R1 repair has explicit negative boundary evidence for stopped
  hyperparameter gradients and public-mode rejection.

## Required Artifacts

- Integration design note:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-loop-integration-design-2026-06-22.md`
- Phase 4 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase4-loop-adjoint-integration-design-result-2026-06-22.md`
- Refreshed M5 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-manual-adjoint-phase5-small-sir-smoke-subplan-2026-06-22.md`

## Required Checks / Tests / Reviews

- Read current streaming and dense LEDH-PFPF-OT filter paths.
- Record current tensor flow for particles, log weights, masks, flow terms,
  transport output, and likelihood accumulation.
- Define fixed-randomness and seed/replay policy.
- Define memory ledger: retained tensors versus recomputed tensors.
- Use M3 private helper names and retained/replay handoff as the starting
  ledger; do not reinterpret the existing `filterflow_custom_op` as the new
  manual route.
- Treat recomputation of `C(x, stop_gradient(x))` under the same stopped-key
  rule as the default replay contract unless M4 explicitly documents a
  same-scalar retained-state alternative.
- Claude read-only review is required because this phase sets the integration
  boundary for later implementation.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What exact filter-loop quantities must the manual/custom-gradient route retain, replay, stop, or differentiate? |
| Baseline/comparator | Current dense/streaming LEDH-PFPF-OT implementation paths and M3 private dense route. |
| Primary criterion | Design note provides an implementable integration contract with tensor shapes, route boundaries, stop-gradient policy, and test handoff for M5. |
| Veto diagnostics | Ambiguous replay policy; hidden randomness; missing masks; no memory ledger; public/default behavior change; raw full-AD N10000 route reintroduced. |
| Explanatory diagnostics | Shape tables, current code anchors, retained/replay memory estimate, and unsupported-mode list. |
| Not concluded | No implementation correctness, no streaming memory result, no SIR d18 validation, no P82 validation, no HMC/default/posterior readiness. |

## Forbidden Claims / Actions

- Do not implement filter-loop integration in M4.
- Do not change defaults.
- Do not run long GPU experiments.
- Do not claim that a design note proves memory improvement.
- Do not alter random streams or masks without explicit contract.

## Next-Phase Handoff Conditions

M5 may proceed only if M4 records:

- exact integration point(s);
- retained/replay tensor ledger;
- seed/fixed-randomness policy;
- supported route name and mode;
- private helper names and unsupported modes;
- small SIR smoke test commands and pass/fail criteria.

## Stop Conditions

Stop if the integration boundary cannot be specified without redesigning the
filter, if replay would change the scalar, if randomness cannot be fixed, or if
the memory ledger shows no plausible path to the P82 actual-gradient use case.
