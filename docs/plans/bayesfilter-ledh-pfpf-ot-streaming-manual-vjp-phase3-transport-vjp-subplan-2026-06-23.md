# Streaming Manual VJP Phase 3 Subplan: Transport-From-Potentials VJP

status: DRAFT_REFRESHED_AFTER_S2
date: 2026-06-23
phase: S3-TRANSPORT-VJP

## Phase Objective

Implement and test a blockwise manual VJP for
`_filterflow_streaming_transport_from_potentials`, including the column
normalizer adjoint, barycentric particle adjoint, potential adjoints, log-weight
adjoint, and cost-to-state adjoints.

## Entry Conditions

- S2 softmin VJP passed.
- S1 derivation contract identifies column-normalizer and padding policy.
- The S3 implementation must use the S1 code-defined scalar: upstream
  contraction with `_filterflow_streaming_transport_from_potentials` output,
  with `eps` and `float_n` fixed.
- The S1 clarification is inherited: outer `scaled_x` and local recursion `x`
  are the same differentiated state under different local names.

## Required Artifacts

- Implementation diff for streaming transport VJP helpers in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Focused tests in `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` or a
  new focused test file.
- S3 result:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-result-2026-06-23.md`
- S3 blocker, only if needed:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-blocker-2026-06-23.md`
- Refreshed S4 subplan:
  `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md`

## Required Checks/Tests/Reviews

- Tolerance rule:
  - default dtype for focused tests: `tf.float64`;
  - value parity tolerance if tested: absolute error `<= 1.0e-10`;
  - VJP parity tolerance: max absolute error `<= 1.0e-8`;
  - tiny autodiff diagnostics remain diagnostic only.
- CPU-hidden pytest comparing blockwise transport VJP to tiny dense/manual and
  tiny autodiff references.
- Tests must include exact chunks and padded chunks.
- Tests must include `scaled_x != particles` because final transport has a
  payload adjoint through `particles` and cost adjoints through `scaled_x`.
- Tests must explicitly check the code-defined `d_g = 0` cancellation from the
  column normalizer.
- At least one `d_g = 0` fixture must be nondegenerate: non-uniform/nontrivial
  `g`, active column normalization, generic upstream cotangent, and both
  padded and unpadded coverage across the fixture set.
- Tests must check `d_scaled_x`, `d_particles`, `d_f`, `d_g`, and `d_logw`.
- Source scan for forbidden `GradientTape` and dense retained matrices in the
  new helper.
- `py_compile` and `git diff --check`.
- Claude one-path review of S3 result.

Exact local commands, adjusted only if file names change during implementation:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "transport_from_potentials" -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
rg -n "GradientTape|\\[B,N,N\\]|tf\\.einsum\\(|tf\\.matmul\\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md
```

The `rg` command is a review aid: existing dense/tiny comparator matches are
not automatic failures.  The S3 result must classify each relevant match and
veto any new-helper `GradientTape` or large-N dense retained state.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the blockwise transport-from-potentials VJP recover all required adjoints without dense retained transport matrices? |
| Baseline/comparator | Dense manual transport VJP and tiny TensorFlow autodiff diagnostic. |
| Primary pass criterion | Transport-from-potentials VJP tests pass with max absolute VJP error `<= 1.0e-8` on exact/padded fixtures, including `scaled_x != particles` and code-defined `d_g = 0`. |
| Veto diagnostics | Missing column-normalizer adjoint; wrong `logw` adjoint; nonzero code-defined `d_g`; incorrect cost-to-state adjoint; hidden dense matrix; nonfinite gradients. |
| Explanatory only | Runtime, chunk sizes, and max componentwise errors. |
| Not concluded | No full Sinkhorn recursion correctness, no P82 readiness. |

## Forbidden Claims/Actions

- Do not integrate into the full custom gradient yet.
- Do not run GPU jobs.
- Do not use autodiff as promotion beyond tiny diagnostic parity.
- Do not implement finite Sinkhorn recursion VJP in S3 except for test
  scaffolding needed to isolate transport-from-potentials.
- Do not reinterpret `g` as differentiable for the code-defined scalar after
  the column normalizer cancellation.

## Exact Next-Phase Handoff Conditions

Advance to S4 only if:

- transport VJP tests pass;
- S3 result records all adjoint components, tolerances, exact fixtures,
  commands, environment, run manifest, decision table, and classified
  source-scan findings;
- S4 subplan names finite recursion state retention and reverse-step tests.

## Stop Conditions

Stop if:

- the column-normalizer adjoint cannot be made blockwise;
- the implementation requires retaining dense `[B,N,N]` state;
- tests expose a scalar mismatch with the existing streaming value path.
- `d_g` cannot be shown to cancel for the code-defined normalized transport
  scalar.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S3 result or blocker.
3. Draft or refresh S4.
4. Review S4 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.

The S3 result must include a decision table with: decision, primary criterion
status, veto diagnostic status, main uncertainty, next justified action, and
what is not being concluded.  It must also include a run manifest with: git
commit, command, environment, CPU/GPU status, dtype, seeds if any, wall time if
available, output artifact paths, plan file, result file, and touched files.
