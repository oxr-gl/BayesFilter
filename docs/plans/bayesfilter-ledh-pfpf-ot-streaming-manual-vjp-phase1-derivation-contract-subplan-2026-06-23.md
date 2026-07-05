# Streaming Manual VJP Phase 1 Subplan: Derivation Contract

status: DRAFT
date: 2026-06-23
phase: S1-DERIVATION-CONTRACT

## Phase Objective

Write the derivation contract for the streaming/blockwise manual VJP route:
softmin VJP, transport-from-potentials VJP, finite Sinkhorn recursion VJP, and
stopped-scale/key semantics.

## Entry Conditions

- S0 result passed and records the route inventory.
- No implementation changes have been made by this program.
- Claude has agreed that the master/runbook gate is coherent.

## Required Artifacts

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-derivation-contract-2026-06-23.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-result-2026-06-23.md`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-blocker-2026-06-23.md`, only if S1 blocks.
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md`, refreshed if S1 changes S2 entry conditions.
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md`

## Required Checks/Tests/Reviews

- Static `rg` check that the derivation contract names softmin,
  transport-from-potentials, finite Sinkhorn recursion, column normalizer,
  cost-to-query/key handling, block accumulation, retained quantities, stopped
  keys, stopped scale, exact scalar, padding/mask policy, no hidden dense
  retained state, exact comparators, implementation exclusions, and no
  `GradientTape` in streaming backward.
- Static `rg` check that exact comparator functions/routes are enumerated:
  `_filterflow_manual_dense_finite_softmin_vjp`,
  `_filterflow_manual_dense_finite_sinkhorn_vjp`,
  `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`,
  `_filterflow_streaming_softmin`,
  `_filterflow_streaming_transport_from_potentials`, and
  `manual_streaming_finite_sinkhorn_stopped_scale_keys`.
- Manual checklist in the S1 result confirming that the derivation contract
  covers inputs, outputs, block accumulation rules, stopped quantities, retained
  quantities, exact scalar/boundary convention, padding/mask semantics, no
  hidden dense retained state, exact comparators, and implementation exclusions
  for all three VJP layers.
- `git diff --check` on S1 artifacts.
- Claude one-path read-only review of the derivation contract.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the blockwise VJP equations and stopped/frozen boundaries precise enough to implement without falling back to autodiff replay or dense retained matrices? |
| Baseline/comparator | Existing dense manual VJP functions and streaming forward functions in `annealed_transport_tf.py`. |
| Primary pass criterion | The derivation specifies inputs, outputs, block accumulation rules, stopped quantities, retained quantities, exact comparators, and implementation exclusions. |
| Veto diagnostics | Ambiguous scalar; missing column-normalizer adjoint; missing cost-to-query/key handling; hidden dense memory; missing padding mask policy; authorizing `GradientTape` backward. |
| Explanatory only | Algebra notes, shape tables, and estimated memory formulas. |
| Not concluded | No code correctness, no performance, no P82 readiness. |

## Forbidden Claims/Actions

- Do not implement code in S1.
- Do not claim large-N memory success.
- Do not change route names after seeing test results.
- Do not let Claude authorize scientific or runtime claims.

## Exact Next-Phase Handoff Conditions

S2 intentionally starts with the softmin VJP primitive.  This is valid only if
the S1 derivation contract also covers the downstream transport-from-potentials
and finite Sinkhorn recursion VJPs, so that S2 can be a first implementation
slice rather than a narrowing of scope.

Advance to S2 only if:

- derivation contract passes local checks and Claude review;
- S2 subplan identifies focused softmin VJP tests and tolerances and preserves
  the S3/S4 handoff obligations for transport-from-potentials and finite
  Sinkhorn recursion VJPs;
- derivation explicitly forbids `GradientTape` inside the new streaming
  backward;
- derivation contract enumerates exact comparator functions/routes for every
  VJP layer.

## Stop Conditions

Stop if:

- the transport-from-potentials VJP cannot be specified without dense retained
  state;
- padding/masking semantics are unresolved;
- the derivation requires autodiff replay or `GradientTape` backward for the new
  streaming route;
- stopped-scale or stopped-key boundaries remain ambiguous;
- column-normalizer adjoint or cost-to-query/key handling cannot be specified
  precisely;
- Claude review identifies a material derivation gap that does not converge
  within five rounds.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S1 result or blocker.
3. Draft or refresh S2.
4. Review S2 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
