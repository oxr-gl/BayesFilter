# Streaming Manual VJP Phase 4 Result: Sinkhorn Recursion VJP

date: 2026-06-23
phase: S4-SINKHORN-RECURSION-VJP
status: PASSED

## Objective

Implement and test the streaming finite Sinkhorn recursion VJP by mirroring the
dense manual reverse recursion while replacing dense softmin VJPs with the S2
blockwise softmin VJP.

## Implementation Summary

Added `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`
in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

The helper:

- returns `(d_log_alpha, d_log_beta, d_x_from_sinkhorn_cost)`;
- accepts upstreams for the two streaming finite potential outputs `(alpha,
  beta)`;
- uses `_filterflow_streaming_softmin_vjp(..., stop_keys=True)` for all
  recursion softmin adjoints;
- stores only per-step vector state `(running, a_y, b_x, a_x, b_y)` for the
  static finite `steps` count;
- treats `epsilon`, `epsilon0`, `scaling`, and `steps` as fixed;
- does not wire the full transport custom gradient route.

Added focused recursion tests in
`tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`.

## Fixture Construction

The S4 fixtures are deterministic:

- exact chunk fixture: `B=1, N=4, D=2, steps=0, row_chunk=2, col_chunk=2`;
- padded chunk fixture: `B=2, N=5, D=2, steps=2, row_chunk=2, col_chunk=3`;
- deterministic log potentials from normalized linspace tensors;
- deterministic upstream cotangents for both `alpha` and `beta`;
- scalar `epsilon`, vector `epsilon0`, scalar `scaling`, and static integer
  `steps`.

The tests compare:

- streaming recursion VJP against dense/manual recursion plus stopped-key
  query-side cost adjoints;
- streaming recursion VJP against tiny autodiff diagnostics;
- directional JVP/VJP dot product on tiny fixtures;
- a tiny custom-gradient wrapper confirming `epsilon`, `epsilon0`, and
  `scaling` receive zero gradients.  `steps` is static and non-differentiable.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the streaming finite Sinkhorn recursion VJP match the dense manual reverse recursion without dense retained state? |
| Baseline/comparator | `_filterflow_manual_dense_finite_sinkhorn_vjp` and tiny autodiff diagnostics. |
| Primary pass criterion | Recursion VJP and directional checks pass within `1.0e-8` tolerance for exact and padded chunks, including `steps=0` and `steps>=2`. |
| Veto diagnostics | Wrong reverse-state order; missing final/initial softmin adjoint; key-side stopped-gradient leakage; stopped-scale gradient leakage; hidden dense cost/probability/trajectory state; `GradientTape` fallback; nonfinite adjoints. |
| Explanatory only | Retained vector states, runtime, chunk sizes, source-scan locations, and tiny autodiff diagnostics. |
| Not concluded | No full custom-gradient route correctness, no end-to-end filter-loop correctness, no GPU memory success, no P82 readiness. |

## Checks Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "sinkhorn_recursion" -q
```

Output:

```text
2 passed, 24 deselected in 11.20s
```

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md
```

Review aid:

```text
rg -n "GradientTape|\[B,N,N\]|tf\.einsum\(|tf\.matmul\(" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Source-scan classification:

- `tf.einsum` matches are existing tiny barycentric test helpers.
- `GradientTape` matches in the test file are tiny diagnostic/autodiff
  comparators, including the S4 recursion diagnostic and stopped-scale wrapper
  test.
- `GradientTape` matches in `annealed_transport_tf.py` are pre-existing
  custom-gradient/replay routes outside the new recursion VJP helper.
- `tf.matmul` matches in `annealed_transport_tf.py` are existing block-local
  pairwise cost/transport operations, the S3 block-local transport VJP payload
  adjoint, or dense comparator utilities.
- No `GradientTape` appears in
  `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`.
- No large-N dense retained `[B,N,N]` cost/probability/transport tensor is
  introduced by the new recursion VJP helper.

Retained-state classification:

- Allowed retained state: Python-list entries of per-step vector tensors
  `(running, a_y, b_x, a_x, b_y)`.
- Allowed temporaries: block-local `[B,row_chunk,col_chunk]` costs/logits and
  probabilities recomputed inside the S2 softmin VJP.
- Forbidden retained state: full cost/probability/trajectory tensors.  None are
  introduced by S4.

## Decision Table

| Field | Status |
|---|---|
| Decision | S4 locally passes; ready for Claude one-path review of this result. |
| Primary criterion status | Passed: `pytest -k "sinkhorn_recursion"` returned `2 passed`. |
| Veto diagnostic status | Passed locally: dense/manual parity, tiny autodiff parity, directional JVP/VJP, stopped-scale no-gradient wrapper, finite adjoints, no new-helper `GradientTape`, no dense retained `[B,N,N]`. |
| Main uncertainty | The helper is not yet wired into the full streaming transport custom-gradient route. |
| Next justified action | Claude review of this S4 result, then refresh/review S5 custom-gradient wiring subplan. |
| What is not concluded | No full custom-gradient route correctness, no filter-loop correctness, no large-N memory feasibility, no P82/FD readiness, no HMC/default readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in Checks Run. |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU evidence collected. |
| Dtype | `tf.float64` in focused tests. |
| Seeds | N/A; deterministic tensor fixtures, no RNG. |
| Wall time | Pytest reported `11.20s`; py_compile and scans were short local checks. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase4-sinkhorn-recursion-vjp-result-2026-06-23.md` |
| Touched files | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`; `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`; S4/S3/ledger plan artifacts. |

## Handoff

Claude one-path review returned `VERDICT: AGREE`.

S5 may proceed only after this result passes bounded Claude review and the S5
subplan is refreshed/reviewed.  S5 must wire a new opt-in route that composes
the reviewed S2-S4 helpers and must not change the old replay route, the
default route, or P82 entry conditions.
