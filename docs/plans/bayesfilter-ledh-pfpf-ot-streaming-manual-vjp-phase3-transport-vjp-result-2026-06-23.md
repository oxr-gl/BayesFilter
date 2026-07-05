# Streaming Manual VJP Phase 3 Result: Transport-From-Potentials VJP

date: 2026-06-23
phase: S3-TRANSPORT-VJP
status: PASSED

## Objective

Implement and test a blockwise manual VJP for
`_filterflow_streaming_transport_from_potentials`, including the
column-normalizer adjoint, barycentric particle adjoint, potential adjoints,
log-weight adjoint, and cost-to-state adjoints.

## Implementation Summary

Added `_filterflow_streaming_transport_from_potentials_vjp` in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

The helper uses a column-block outer loop:

1. computes the existing streaming column log normalizer;
2. for each column block, makes a first row-block pass to accumulate
   `S_j = sum_i dT_ij T_ij` and the particle payload adjoint;
3. makes a second row-block pass to recompute block transports/probabilities
   and accumulate `d_scaled_x`, `d_f`, and cost-to-state adjoints;
4. returns code-defined `d_g = 0` because the column potential cancels through
   the normalizer.

Added focused tests in
`tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`.

## Fixture Construction

The S3 fixtures are deterministic and nondegenerate:

- exact chunk fixture: `B=1, N=4, D=2, row_chunk=2, col_chunk=2`;
- padded chunk fixture: `B=2, N=5, D=2, row_chunk=2, col_chunk=3`;
- `scaled_x != particles` by construction;
- `g` is nonuniform/nontrivial using a sine transform over a linspace;
- upstream cotangent is generic deterministic linspace data;
- both fixtures use active column normalization through the streaming forward
  helper and compare against tiny autodiff.

The tests assert `g_nontrivial > 1.0e-3`, `scaled_x_particles_gap > 1.0e-3`,
and `d_g` max absolute value `<= 1.0e-8`.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the blockwise transport-from-potentials VJP recover all required adjoints without dense retained transport matrices? |
| Baseline/comparator | Dense/manual code-defined normalized transport VJP and tiny TensorFlow autodiff diagnostics. |
| Primary pass criterion | Transport-from-potentials VJP tests pass with max absolute VJP error `<= 1.0e-8` on exact/padded fixtures, including `scaled_x != particles` and code-defined `d_g = 0`. |
| Veto diagnostics | Missing column-normalizer adjoint; wrong `logw` adjoint; nonzero code-defined `d_g`; incorrect cost-to-state adjoint; hidden dense matrix; nonfinite gradients. |
| Explanatory only | Runtime, chunk sizes, source-scan locations, and tiny autodiff diagnostics. |
| Not concluded | No full Sinkhorn recursion correctness, no end-to-end custom-gradient wiring, no large-N memory success, no P82 readiness. |

## Checks Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "transport_from_potentials" -q
```

Output:

```text
2 passed, 22 deselected in 6.38s
```

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md
```

Review aid:

```text
rg -n "GradientTape|\[B,N,N\]|tf\.einsum\(|tf\.matmul\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Source-scan classification:

- `tf.einsum` matches are existing tiny barycentric test helpers.
- `GradientTape` matches in the test file are tiny diagnostic/autodiff
  comparators, including the S3 transport diagnostic test.
- `GradientTape` matches in `annealed_transport_tf.py` are pre-existing
  custom-gradient/replay routes outside the new transport VJP helper.
- `tf.matmul` matches in `_filterflow_streaming_transport_from_potentials_vjp`
  are block-local particle-adjoint accumulations with shape
  `[B,col_chunk,D]`; this is allowed and is not retained global `[B,N,N]`
  state.
- Other `tf.matmul` matches in `annealed_transport_tf.py` are existing
  block-local pairwise cost/transport operations or dense comparator utilities.
- No `GradientTape` appears in `_filterflow_streaming_transport_from_potentials_vjp`.
- No large-N dense retained `[B,N,N]` transport/cost/probability tensor is
  introduced by `_filterflow_streaming_transport_from_potentials_vjp`; it uses
  block-local `[B,row_chunk,col_chunk]` temporaries plus full-size returned
  gradient accumulators.

## Decision Table

| Field | Status |
|---|---|
| Decision | S3 locally passes; ready for Claude one-path review of this result. |
| Primary criterion status | Passed: `pytest -k "transport_from_potentials"` returned `2 passed`. |
| Veto diagnostic status | Passed locally: column-normalizer adjoint included, `d_logw` tested, code-defined `d_g` zero, cost-to-state tested, no new-helper `GradientTape`, no dense retained `[B,N,N]`, finite gradients. |
| Main uncertainty | The helper is not yet wired into the finite Sinkhorn recursion VJP or full custom-gradient route. |
| Next justified action | Claude review of this S3 result, then refresh/review S4 finite Sinkhorn recursion VJP subplan. |
| What is not concluded | No full Sinkhorn recursion correctness, no end-to-end streaming custom-gradient correctness, no large-N memory feasibility, no P82/FD readiness, no HMC/default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in Checks Run. |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU evidence collected. |
| Dtype | `tf.float64` in focused tests. |
| Seeds | N/A; deterministic tensor fixtures, no RNG. |
| Wall time | Pytest reported `6.38s`; py_compile and scans were short local checks. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase3-transport-vjp-result-2026-06-23.md` |
| Touched files | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`; `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`; S3/S2/ledger plan artifacts. |

## Handoff

Claude one-path review returned `VERDICT: AGREE`.

S4 may proceed only after this result passes bounded Claude review and the S4
subplan is refreshed/reviewed.  S4 must implement the finite Sinkhorn recursion
VJP by composing the reviewed S2 softmin VJP and S3 transport VJP contracts,
without `GradientTape` in the new streaming recursion backward and without
retaining global dense `[B,N,N]` state.
