# Streaming Manual VJP Phase 5 Result: Custom-Gradient Wiring

date: 2026-06-23
phase: S5-CUSTOM-GRADIENT-WIRING
status: PASSED

## Objective

Wire a new opt-in streaming manual VJP route whose custom-gradient backward
pass uses the reviewed blockwise manual VJPs from S2-S4 and does not replay the
streaming value under `tf.GradientTape`.

## Implementation Summary

Added low-level route helper:

- `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`
  in `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

Added opt-in route constant and dispatch:

- `MANUAL_STREAMING_BLOCKWISE_VJP_FINITE_TRANSPORT_GRADIENT_MODE`
  with value `manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`
  in `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`.

The old replay route remains:

- `MANUAL_STREAMING_FINITE_TRANSPORT_GRADIENT_MODE`
  with value `manual_streaming_finite_sinkhorn_stopped_scale_keys`.

The new custom-gradient backward composes:

- S3 `_filterflow_streaming_transport_from_potentials_vjp`;
- S4 `_filterflow_streaming_finite_sinkhorn_potentials_vjp_stopped_scale_keys`;
- existing streaming finite transport forward value.

No default route was changed.  The new route is reached only when callers
explicitly set `transport_gradient_mode` to
`manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys`; the core
function signature still defaults to `transport_gradient_mode="filterflow_clipped"`
and `transport_plan_mode="dense"`, so the dispatch default does not select the
new branch.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the new opt-in route wired to the full transport core with a truly manual streaming backward pass? |
| Baseline/comparator | Existing streaming value/replay route, dense manual tiny fixtures, and S2-S4 primitive results. |
| Primary pass criterion | New route passes local value/gradient parity and source scan; old routes remain unchanged; unsupported modes reject; default route remains unchanged. |
| Veto diagnostics | `GradientTape` in new route backward; old route silently changed; unsupported route accepted; default route changed; dense matrix returned for streaming route; P82/FD/GPU launched. |
| Explanatory only | Function anchors, route metadata, graph/eager behavior, and timing. |
| Not concluded | No large-N feasibility, no P82 FD agreement, no default readiness. |

## Checks Run

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "blockwise_route" -q
```

Output:

```text
3 passed, 26 deselected in 7.93s
```

Repair rerun after Claude R1 requested a clearer default-dispatch boundary:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py -k "blockwise_route" -q
```

Output:

```text
3 passed, 26 deselected in 8.09s
```

Passed:

```text
git diff --check -- experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md
```

Review aid:

```text
rg -n "manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys|GradientTape|\[B,N,N\]" experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py
```

Source-scan classification:

- New route helper anchor:
  `_filterflow_manual_streaming_blockwise_vjp_finite_transport_stopped_scale_keys`
  starts at `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2016`.
- No `GradientTape` appears inside the new blockwise route backward.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:1988`
  is the pre-existing old replay route
  `_filterflow_manual_streaming_finite_transport_stopped_scale_keys`.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py:2166`
  is the pre-existing dense/filterflow custom-op transport-matrix route, not
  the new blockwise route backward.
- The `GradientTape` match at
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py:1111`
  is the separate value-and-score API, not the new route backward.
- `GradientTape` matches in the test file are local tiny diagnostics.
- No large-N dense retained `[B,N,N]` tensor is introduced by the new route;
  streaming routes return an empty transport matrix with size zero in focused
  tests.

The R1 repair also reran py-compile, the review-aid source scan, and
`git diff --check` on S5 code/test/result/review-ledger artifacts; all passed.

## Test Coverage

Focused tests verify:

- new route value parity against the old streaming value route and dense manual
  tiny reference;
- new route gradient parity against dense manual tiny reference;
- streaming route transport matrix remains empty;
- old streaming route constant value is unchanged;
- new route is opt-in and has a distinct route string;
- default transport dispatch remains on the existing
  `transport_gradient_mode="filterflow_clipped"` / `transport_plan_mode="dense"`
  path unless the new route string is explicitly requested;
- default execution target remains `gpu`;
- unsupported dense plan, warmstart, `transport_ad_mode="full"`, and vector
  epsilon combinations reject for the new route.

No GPU, P82 FD, or `N=10000` feasibility commands were run.

## Decision Table

| Field | Status |
|---|---|
| Decision | S5 passed after bounded Claude review R2 returned `VERDICT: AGREE`. |
| Primary criterion status | Passed: `pytest -k "blockwise_route"` returned `3 passed` before review and after the R1 repair. |
| Veto diagnostic status | Passed locally: no `GradientTape` in new route backward, old route string preserved, new route opt-in, default dispatch remains `filterflow_clipped`/`dense`, unsupported modes reject, default execution target unchanged, streaming transport matrix empty. |
| Main uncertainty | Local route wiring is not yet exercised by the broader S6 parity ladder or S7 GPU memory ladder. |
| Next justified action | Refresh and review S6 local parity ladder subplan. |
| What is not concluded | No large-N feasibility, no P82 FD agreement, no GPU memory success, no HMC/default readiness, no production readiness. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in Checks Run. |
| Environment | Local repo shell; CPU-hidden commands used `CUDA_VISIBLE_DEVICES=-1`. |
| CPU/GPU status | CPU-only by explicit device hiding; no GPU evidence collected. |
| Dtype | `tf.float64` in focused tests. |
| Seeds | N/A; deterministic tensor fixtures, no RNG. |
| Wall time | Pytest reported `7.93s`; py_compile and scans were short local checks. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase5-custom-gradient-wiring-result-2026-06-23.md` |
| Touched files | `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`; `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`; `tests/test_ledh_pfpf_ot_manual_adjoint_primitives.py`; S5/S4/ledger plan artifacts. |

## Handoff

This result passed bounded Claude review on R2 after a targeted R1 repair to
the default-dispatch evidence.  S6 may proceed only after the S6 subplan is
refreshed/reviewed.  S6 must run the local parity ladder for the new opt-in
route without GPU, P82 FD, or `N=10000` claims.
