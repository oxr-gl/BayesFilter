# Streaming Manual VJP Phase 1 Result: Derivation Contract

date: 2026-06-23
phase: S1-DERIVATION-CONTRACT
status: PASSED

## Objective

Write a derivation contract for the streaming/blockwise manual VJP route before
any implementation changes.  The contract covers softmin VJP,
transport-from-potentials VJP, finite Sinkhorn recursion VJP, stopped-scale/key
semantics, padding/mask behavior, and hidden-memory exclusions.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the blockwise VJP equations and stopped/frozen boundaries precise enough to implement without falling back to autodiff replay or dense retained matrices? |
| Baseline/comparator | Existing dense manual VJP functions and streaming forward functions in `annealed_transport_tf.py`. |
| Primary pass criterion | The derivation specifies inputs, outputs, block accumulation rules, stopped quantities, retained quantities, exact comparators, and implementation exclusions. |
| Veto diagnostics | Ambiguous scalar; missing column-normalizer adjoint; missing cost-to-query/key handling; hidden dense memory; missing padding/mask policy; authorizing `GradientTape` backward. |
| Explanatory only | Algebra notes, shape tables, and estimated memory formulas. |
| Not concluded | No code correctness, no performance, no P82 readiness. |

## Artifacts

- Derivation contract:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-derivation-contract-2026-06-23.md`
- S1 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase1-derivation-contract-subplan-2026-06-23.md`

## Local Checks

Passed:

- Static required-term scan against the derivation contract:
  `softmin`, `transport-from-potentials`, `finite Sinkhorn recursion`,
  `column normalizer`, `cost-to-query/key handling`, `block accumulation`,
  `retained quantities`, `stopped keys`, `stopped scale`, `exact scalar`,
  `padding/mask policy`, `no hidden dense retained state`, `exact comparators`,
  `implementation exclusions`, and `GradientTape`.
- Static exact-comparator scan against the derivation contract:
  `_filterflow_manual_dense_finite_softmin_vjp`,
  `_filterflow_manual_dense_finite_sinkhorn_vjp`,
  `_filterflow_manual_dense_finite_transport_matrix_vjp_stopped_scale_keys`,
  `_filterflow_streaming_softmin`,
  `_filterflow_streaming_transport_from_potentials`, and
  `manual_streaming_finite_sinkhorn_stopped_scale_keys`.
- `git diff --check` on S1 artifacts.

## Manual Checklist

Softmin VJP:

- Inputs and outputs specified: yes.
- Block accumulation rules specified: yes.
- Stopped quantities specified: yes, including stopped-key option.
- Retained quantities and no hidden dense retained state specified: yes.
- Exact scalar/boundary convention specified: yes.
- Padding/mask semantics specified: yes.
- Exact comparators specified: yes.
- Implementation exclusions specified: yes.

Transport-from-potentials VJP:

- Inputs and outputs specified: yes.
- Block accumulation rules specified: yes, including two-pass/recompute option.
- Stopped quantities specified: yes, with fixed `eps` and `float_n`.
- Retained quantities and no hidden dense retained state specified: yes.
- Exact scalar/boundary convention specified: yes.
- Padding/mask semantics specified: yes.
- Exact comparators specified: yes.
- Implementation exclusions specified: yes.
- Column-normalizer adjoint specified: yes.
- Cost-to-query/key handling specified: yes, with both final-transport sides.

Finite Sinkhorn recursion VJP:

- Inputs and outputs specified: yes.
- Block accumulation rules specified: yes, via reverse recursion over vector
  states and blockwise softmin VJPs.
- Stopped quantities specified: yes, with stopped keys and stopped scale.
- Retained quantities and no hidden dense retained state specified: yes.
- Exact scalar/boundary convention specified: yes.
- Padding/mask semantics specified: yes, inherited from softmin VJP.
- Exact comparators specified: yes.
- Implementation exclusions specified: yes.
- Cost-to-query/key handling specified: yes, query-only for stopped-key
  recursion costs.

## Claude Review

Claude one-path read-only review of the derivation contract returned:

```text
VERDICT: AGREE
```

Non-blocking implementation note from review: `scaled_x` in the outer transport
route and local `x` in the Sinkhorn recursion should be treated as the same
differentiated state under different local names.

## Decision

S1 passes.  The derivation contract passed local checks and bounded Claude
review.  Implementation remains unauthorized until S2 entry conditions are
satisfied and the S2 subplan is reviewed/refreshed for consistency.

## Nonclaims

This result does not conclude implementation correctness, performance,
large-N memory feasibility, FD agreement, P82 readiness, HMC/default readiness,
production readiness, or scientific validity.
