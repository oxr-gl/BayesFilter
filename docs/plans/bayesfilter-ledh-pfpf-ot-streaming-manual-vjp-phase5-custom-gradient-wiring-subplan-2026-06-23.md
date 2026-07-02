# Streaming Manual VJP Phase 5 Subplan: Custom-Gradient Wiring

status: DRAFT_REFRESHED_AFTER_S4
date: 2026-06-23
phase: S5-CUSTOM-GRADIENT-WIRING

## Phase Objective

Wire a new opt-in streaming manual VJP route whose custom-gradient backward pass
uses the blockwise manual VJPs from S2-S4 and does not replay the streaming
value under `tf.GradientTape`.

## Entry Conditions

- S4 passed.
- Primitive block VJPs have result artifacts and tests.
- Existing P82 route remains blocked until this phase and S6/S7 pass.
- The old `manual_streaming_finite_sinkhorn_stopped_scale_keys` replay route
  must remain available and behavior-preserving unless the new route is
  explicitly selected.
- The new route must compose the S3 transport-from-potentials VJP and S4
  finite Sinkhorn recursion VJP.  It must not call `GradientTape` in its
  custom-gradient backward pass.

## Required Artifacts

- Implementation diff adding a new route name, for example
  `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`.
- Tests proving unsupported modes reject and old routes keep their behavior.
- Source scan artifact showing the new route backward contains no
  `GradientTape`.
- S5 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-result-2026-06-23.md`
- S5 blocker, only if needed:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-blocker-2026-06-23.md`
- Refreshed S6 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-subplan-2026-06-23.md`

## Required Checks/Tests/Reviews

- Tolerance rule:
  - default dtype for focused tests: `tf.float64`;
  - value parity tolerance: absolute error `<= 1.0e-10`;
  - gradient parity tolerance: max absolute error `<= 1.0e-8`;
  - tiny autodiff diagnostics remain diagnostic only.
- CPU-hidden focused pytest for route selection, unsupported modes, gradients,
  graph/eager parity, and source scan.
- Tests must show the new route output and gradients match the old replay route
  and/or dense manual tiny references on exact and padded chunk fixtures.
- Tests must verify the old route still has its existing behavior and the new
  route is opt-in only.
- Tests must verify unsupported transport modes reject for the new route.
- Tests must verify returned transport matrix remains empty for streaming route
  metadata and the default route is unchanged.
- `py_compile` and `git diff --check`.
- Claude one-path review of S5 result.

Exact local commands, adjusted only if file names change during implementation:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "blockwise_route" -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
rg -n "manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys|GradientTape|\\[B,N,N\\]" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md
```

The `rg` command is a review aid.  The S5 result must classify the old replay
route `GradientTape` separately from the new blockwise route and veto any
`GradientTape` in the new route backward.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the new opt-in route wired to the full transport core with a truly manual streaming backward pass? |
| Baseline/comparator | Existing streaming value route, dense manual route on tiny fixtures, and S2-S4 primitive results. |
| Primary pass criterion | New route passes local value/gradient parity and source scan; old routes remain unchanged; unsupported modes reject; default route remains unchanged. |
| Veto diagnostics | `GradientTape` in new route backward; old route silently changed; unsupported route accepted; default route changed; dense matrix returned for streaming route; P82/FD/GPU launched. |
| Explanatory only | Function anchors, route metadata, graph retrace count, and timing. |
| Not concluded | No large-N feasibility, no P82 FD agreement. |

## Forbidden Claims/Actions

- Do not replace the old route as default.
- Do not run GPU jobs in S5.
- Do not modify benchmark pass/fail criteria.
- Do not claim P82 is fixed.
- Do not delete or rewrite the old replay route.
- Do not run P82 FD or any N10000 feasibility claim in S5.

## Exact Next-Phase Handoff Conditions

Advance to S6 only if:

- new route exists and is opt-in;
- source scan proves no `GradientTape` in the new route backward;
- local route tests pass;
- S5 result records exact route name, value/gradient fixtures, unsupported-mode
  checks, old-route/default-preservation checks, commands, environment, run
  manifest, decision table, and classified source scan;
- S6 subplan defines the local parity ladder.

## Stop Conditions

Stop if:

- new route cannot be isolated from existing route behavior;
- source scan cannot distinguish old replay route from new manual route;
- local gradient parity fails.
- route wiring requires changing the default or P82 entry criteria.
- new route backward needs `GradientTape`.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S5 result or blocker.
3. Draft or refresh S6.
4. Review S6 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

The S5 result must include a decision table with: decision, primary criterion
status, veto diagnostic status, main uncertainty, next justified action, and
what is not being concluded.  It must also include a run manifest with: git
commit, command, environment, CPU/GPU status, dtype, seeds if any, wall time if
available, output artifact paths, plan file, result file, and touched files.
