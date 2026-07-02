# Streaming Manual VJP Phase 6 Result: Local Parity Ladder

date: 2026-06-23
phase: S6-LOCAL-PARITY-LADDER
status: PASSED

## Objective

Run the CPU-hidden local parity ladder for the opt-in streaming blockwise
manual VJP route before any GPU, P82 FD, or large-`N` experiment.

## Implementation Summary

Added one focused high-level smoke:

- `test_s6_blockwise_manual_streaming_value_and_score_tiny_opt_in_smoke` in
  `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`.

The smoke mirrors the existing manual streaming value-and-score tiny smoke and
explicitly selects:

- `MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE`;
- `transport_plan_mode="streaming"`;
- `transport_ad_mode="stabilized"`;
- scalar epsilon through the default value path;
- `sinkhorn_iterations=2`;
- `row_chunk_size=2`, `col_chunk_size=2` on the local `N=4` fixture.

It checks finite eager value/score output and graph/eager equality.  It does
not use finite difference and does not change any default route.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does the new streaming blockwise manual VJP route pass local primitive, route, and tiny value-and-score parity/boundary checks before GPU work? |
| Baseline/comparator | Dense manual tiny fixtures, old streaming replay route for value parity only, and tiny TensorFlow autodiff diagnostics; Zhao-Cui is not a comparator. |
| Primary pass criterion | All listed CPU-hidden local tests pass; new route value/gradient parity stays within existing local tolerances; tiny value-and-score smoke is finite and graph/eager consistent; source-scan classification confirms no `GradientTape` in the new blockwise route backward. |
| Veto diagnostics | Any local nonfinite value/gradient; blockwise route value/gradient parity failure; tiny value-and-score smoke failure; route mismatch; source scan finds `GradientTape` in the new blockwise route backward; hidden dense streaming transport matrix; unsupported mode accepted; GPU/P82/`N=10000` command launched. |
| Explanatory only | Runtime, tolerance maxima, graph/eager deltas, high-level value-and-score `GradientTape`, and source-scan locations outside the new route backward. |
| Not concluded | No GPU memory success, no `N=10000` feasibility, no P82 FD agreement, no HMC/default readiness, no production readiness, no scientific superiority. |

## Checks Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "streaming_softmin or streaming_transport_from_potentials or streaming_sinkhorn_recursion or blockwise_route" -q
```

Output:

```text
10 passed, 19 deselected in 12.67s
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_experimental_batched_ledh_pfpf_ot_tf.py -k "m6_manual_streaming_value_and_score_tiny_opt_in_smoke or s6_blockwise_manual_streaming_value_and_score_tiny_opt_in_smoke" -q
```

Output:

```text
2 passed, 25 deselected in 64.86s (0:01:04)
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Review aid:

```text
rg -n "manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys|GradientTape|\[B,N,N\]" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py
```

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py tests/test_experimental_batched_ledh_pfpf_ot_tf.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-subplan-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-claude-review-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-execution-ledger-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-result-2026-06-23.md docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-visible-stop-handoff-2026-06-23.md
```

No GPU, P82 FD, or `N=10000` command was run.

## Source-Scan Classification

- New route string appears at
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:57`
  and in route tests at
  `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py:1665`.
- No `GradientTape` appears inside
  `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`
  or its nested custom-gradient `grad` at
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2016`.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1988`
  is the pre-existing old replay route
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2166`
  is the pre-existing dense/filterflow custom-op transport-matrix route.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1111`
  is the high-level value-and-score API used for local score diagnostics, not
  the new route backward.
- `GradientTape` matches in
  `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py` and
  `tests/test_experimental_batched_ledh_pfpf_ot_tf.py` are local tests or
  assertions about the diagnostic value-and-score API.
- No scan hit for retained global `[B,N,N]` appeared.

## Veto Operationalization

- `test_blockwise_route_matches_dense_and_preserves_streaming_metadata` passed
  as part of the first pytest command.  This test checks new-route value and
  gradient parity and confirms streaming transport metadata remains empty.
- `test_blockwise_route_rejects_unsupported_combinations_and_preserves_defaults`
  passed as part of the first pytest command.  This test confirms the new route
  rejects dense plan, warmstart, `transport_ad_mode="full"`, and vector epsilon
  combinations, while preserving route/default metadata.
- The new high-level value-and-score smoke passed and confirmed finite eager
  output plus graph/eager equality for the opt-in blockwise route.

## Decision Table

| Field | Status |
|---|---|
| Decision | S6 passed after bounded Claude result review returned `VERDICT: AGREE`. |
| Primary criterion status | Passed: all listed CPU-hidden local tests and compile/diff checks passed. |
| Veto diagnostic status | Passed locally: no nonfinite local value/gradient, route parity tests passed, high-level smoke passed, no `GradientTape` in new blockwise route backward, streaming transport matrix remains empty, unsupported modes reject, no GPU/P82/`N=10000` command launched. |
| Main uncertainty | Local parity and tiny value-and-score smoke do not establish GPU memory behavior or `N=10000` feasibility. |
| Next justified action | Refresh/review S7 GPU memory ladder subplan. |
| What is not concluded | No GPU memory success, no `N=10000` feasibility, no P82 FD agreement, no HMC/default readiness, no production readiness, no scientific superiority. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in Checks Run. |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU evidence collected. |
| Dtype | `tf.float64` in focused tests. |
| Seeds | N/A; deterministic local fixtures. |
| Wall time | Pytest reported `12.67s` for primitive/route ladder and `64.86s` for value-and-score smoke selector. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase6-local-parity-ladder-result-2026-06-23.md` |
| Touched files | `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`; S6/S5/ledger plan artifacts. |

## Handoff

This result passed bounded Claude review.  S7 may proceed only after the S7
subplan is refreshed/reviewed.  S7 is the first phase allowed to run GPU work,
and GPU commands must use trusted/elevated execution.  S8/P82 FD remains
blocked until S7 produces a valid `N=10000` actual-gradient artifact.
