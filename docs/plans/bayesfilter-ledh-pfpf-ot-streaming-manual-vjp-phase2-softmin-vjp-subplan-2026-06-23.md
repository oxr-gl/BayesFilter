# Streaming Manual VJP Phase 2 Subplan: Blockwise Softmin VJP

status: DRAFT_REFRESHED_AFTER_S1
date: 2026-06-23
phase: S2-SOFTMIN-VJP

## Phase Objective

Implement and test a blockwise VJP for `_filterflow_streaming_softmin` that
matches the dense/manual and tiny autodiff references without materializing a
full `[B,N,N]` cost/probability tensor.

## Entry Conditions

- S1 derivation contract passed local checks and bounded Claude review.
- Route and stopped/frozen semantics are fixed.
- No large-N or GPU claim is in scope.
- The S1 clarification is inherited: `scaled_x` in the outer transport route
  and local `x` in the Sinkhorn recursion are the same differentiated state
  under different local names.

## Required Artifacts

- Implementation diff in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Focused tests in `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` or a
  new focused test file.
- S2 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-result-2026-06-23.md`
- S2 blocker, only if needed:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-blocker-2026-06-23.md`
- Refreshed S3 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md`

## Required Checks/Tests/Reviews

Tolerance rule:

- default dtype for focused tests: `tf.float64`;
- value parity tolerance if tested: absolute error `<= 1.0e-10`;
- VJP parity tolerance: max absolute error `<= 1.0e-8`;
- tiny autodiff diagnostics may use the same `1.0e-8` VJP tolerance but remain
  diagnostic only.

- CPU-hidden pytest for softmin VJP on exact chunks and padded chunks.
- Tiny dense/autodiff parity for `d_query`, optional stopped/unstopped `d_key`,
  and `d_values`.
- Tests must include at least one fixture where `N` is divisible by both chunk
  sizes and one fixture where padding is required.
- Tests must include stopped-key semantics because S4 recursion depends on
  query-only cost gradients.
- Source scan showing no `GradientTape` in the new softmin VJP helper.
- Source scan showing the new softmin VJP helper does not materialize a full
  `[B,N,N]` cost/probability tensor outside tiny tests.
- `py_compile` for touched Python files.
- `git diff --check`.
- Claude one-path review of S2 result if implementation is nontrivial.

Exact local commands, adjusted only if file names change during implementation:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "softmin" -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
rg -n "GradientTape|\\[B,N,N\\]|tf\\.einsum\\(|tf\\.matmul\\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md
```

The `rg` command is a review aid: matches are not automatically failures
because existing dense/tiny comparator code may legitimately contain dense
operations.  The S2 result must classify each relevant match as either existing
comparator/test code or new helper code and veto any new-helper `GradientTape`
or large-N dense retained state.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the blockwise softmin VJP match the dense/tiny oracle within stated tolerances while preserving chunked memory behavior? |
| Baseline/comparator | `_filterflow_manual_dense_finite_softmin_vjp` and tiny TensorFlow autodiff. |
| Primary pass criterion | All softmin VJP tests pass with max absolute VJP error `<= 1.0e-8` on exact and padded chunk fixtures, including stopped-key behavior. |
| Veto diagnostics | Any dense full-cost/probability tensor in the block helper; any `GradientTape` in the helper; nonfinite gradients; padding mismatch; stopped-key gradients leaking into `d_key`. |
| Explanatory only | Runtime, chunk sizes, and shape traces. |
| Not concluded | No transport VJP correctness, no Sinkhorn recursion correctness, no P82 readiness. |

## Forbidden Claims/Actions

- Do not wire the route into P82.
- Do not run GPU jobs.
- Do not claim memory success beyond the primitive helper.
- Do not alter dense manual VJP semantics except for necessary shared helpers.
- Do not use tiny autodiff as a large-N oracle.
- Do not implement transport-from-potentials or finite Sinkhorn recursion VJPs
  in S2 except for test scaffolding needed to isolate softmin.

## Exact Next-Phase Handoff Conditions

Advance to S3 only if:

- softmin VJP tests pass;
- S2 result records tolerances, exact fixtures, commands, environment, run
  manifest, decision table, and classified source-scan findings;
- source scans record no `GradientTape` and no large-N dense `[B,N,N]` retained
  state in the new helper;
- S3 subplan identifies the two-pass transport-from-potentials adjoint design.

## Stop Conditions

Stop if:

- softmin VJP cannot match the dense oracle;
- block accumulation requires dense retained `[B,N,N]` state;
- source scan finds `GradientTape` in the new primitive.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S2 result or blocker.
3. Draft or refresh S3.
4. Review S3 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

The S2 result must include a decision table with: decision, primary criterion
status, veto diagnostic status, main uncertainty, next justified action, and
what is not being concluded.  It must also include a run manifest with: git
commit, command, environment, CPU/GPU status, dtype, seeds if any, wall time if
available, output artifact paths, plan file, result file, and touched files.
