# Streaming Manual VJP Phase 2 Result: Blockwise Softmin VJP

date: 2026-06-23
phase: S2-SOFTMIN-VJP
status: PASSED

## Objective

Implement and test a blockwise VJP for `_filterflow_streaming_softmin` without
retaining a dense large-N `[B,N,N]` cost/probability tensor and without using
`GradientTape` in the new helper.

## Implementation Summary

Added:

- `_scatter_axis1_add_2d` and `_scatter_axis1_add_3d` in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- `_filterflow_streaming_softmin_vjp` in
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.
- Focused exact-chunk, padded-chunk, stopped-key, dense/manual, and tiny
  autodiff diagnostic tests in
  `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`.

The helper uses a two-pass row-block design:

1. recompute column chunks to recover the full row logsum;
2. recompute column chunks again to accumulate block probabilities,
   `d_query`, optional `d_key`, and `d_values`.

This fixed the initial local bug where the first implementation normalized each
column chunk independently rather than over all columns.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the blockwise softmin VJP match dense/manual and tiny autodiff diagnostics within tolerance while preserving chunked memory behavior? |
| Baseline/comparator | `_filterflow_manual_dense_finite_softmin_vjp` logic and tiny TensorFlow autodiff diagnostics. |
| Primary pass criterion | All softmin VJP tests pass with max absolute VJP error `<= 1.0e-8` on exact and padded chunk fixtures, including stopped-key behavior. |
| Veto diagnostics | New-helper dense full-cost/probability tensor; new-helper `GradientTape`; nonfinite gradients; padding mismatch; stopped-key gradients leaking into `d_key`. |
| Explanatory only | Runtime, chunk sizes, source-scan locations, and tiny autodiff diagnostics. |
| Not concluded | No transport VJP correctness, no Sinkhorn recursion correctness, no large-N memory success, no P82 readiness. |

## Checks Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "softmin" -q
```

Output:

```text
3 passed, 19 deselected in 3.53s
```

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md
```

Review aid:

```text
rg -n "GradientTape|\[B,N,N\]|tf\.einsum\(|tf\.matmul\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Source-scan classification:

- `tf.einsum` matches are existing tiny barycentric test helpers.
- `GradientTape` matches in the test file are tiny diagnostic/autodiff
  comparators, including the new softmin diagnostic test.
- `GradientTape` matches in `annealed_transport_tf.py` are pre-existing
  custom-gradient/replay routes outside the new softmin VJP helper.
- `tf.matmul` matches in `annealed_transport_tf.py` are existing block-local
  pairwise cost/transport operations.
- No `GradientTape` appears in `_filterflow_streaming_softmin_vjp`.
- No large-N dense retained `[B,N,N]` cost/probability tensor is introduced by
  `_filterflow_streaming_softmin_vjp`; it uses block-local
  `[B,row_chunk,col_chunk]` temporaries and full-size vector/tensor accumulators
  for returned gradients.

## Repair Note

The first focused pytest failed.  Root cause: the initial implementation used
`tf.nn.softmax` inside each column chunk, which normalized over the chunk rather
than over all columns.  The helper was repaired to compute the full row logsum
across column chunks first, then recompute block probabilities as
`exp(logits - row_logsum)`.

## Decision Table

| Field | Status |
|---|---|
| Decision | S2 locally passes; ready for Claude one-path review of this result. |
| Primary criterion status | Passed: `pytest -k "softmin"` returned `3 passed`. |
| Veto diagnostic status | Passed locally: no new-helper `GradientTape`, no dense retained `[B,N,N]`, finite gradients, padding fixtures pass, stopped-key leakage within tolerance. |
| Main uncertainty | The helper is not yet wired into transport-from-potentials or finite Sinkhorn recursion VJPs. |
| Next justified action | Claude review of this S2 result, then refresh/review S3 transport-from-potentials subplan. |
| What is not concluded | No transport VJP correctness, no Sinkhorn recursion correctness, no large-N memory feasibility, no P82/FD readiness, no HMC/default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in Checks Run. |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU evidence collected. |
| Dtype | `tf.float64` in focused tests. |
| Seeds | N/A; deterministic tensor fixtures, no RNG. |
| Wall time | Pytest reported `3.53s`; py_compile and scans were short local checks. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase2-softmin-vjp-result-2026-06-23.md` |
| Touched files | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`; `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`; S2/S1/ledger plan artifacts. |

## Handoff

Claude one-path review returned `VERDICT: AGREE`.

S3 may proceed only after this result passes bounded Claude review and the S3
subplan is refreshed/reviewed.  S3 must implement the blockwise
transport-from-potentials VJP, including the column normalizer adjoint, without
reusing tiny autodiff as an implementation mechanism.
