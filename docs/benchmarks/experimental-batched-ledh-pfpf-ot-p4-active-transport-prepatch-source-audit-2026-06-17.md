# Active Transport Pre-Patch Source Audit - 2026-06-17

## Status

`PREPATCH_SOURCE_AUDIT_PASSED_ALLOWED_REPAIR_SURFACE`

## Question

Before editing gradient-bearing active transport code, is the first observed
active-transport score/JIT TensorList blocker inside
`annealed_transport_tf.py` and in the allowed construct set for the Phase 4
repair subplan?

## Evidence

Failing diagnostic log:

- `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.log`

The log reports:

- `XLA compilation requires a fixed tensor list size`
- failing node:
  `while/cond/while/cond/while_10/Minimum_0/accumulator`
- stack frames through:
  - `streaming_batched_ledh_pfpf_ot_value_core_tf`
  - the active transport conditional in the streaming filter
  - active transport helper calls in
    `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`

Source searches used:

```bash
rg -n "tf\\.while_loop|TensorArray|tf\\.scan|tf\\.map_fn|for .* in|\\.numpy\\(|bool\\(" \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

```bash
rg -n "def batched_annealed_transport_core_tf|application_mode|annealed_transport_resample_tf" \
  experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py \
  experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py \
  tests docs/benchmarks
```

## Candidate TensorList Sources

| Construct | Source evidence | Active score/JIT relevance | Decision |
| --- | --- | --- | --- |
| `tf.while_loop` | Present in `annealed_transport_tf.py` at streaming softmin, streaming Sinkhorn, streaming column normalizer, streaming transport-from-potentials, and exact Sinkhorn loop sites. | Relevant. The active-odd diagnostic enters active transport through `batched_annealed_transport_core_tf`, which imports these helpers from `annealed_transport_tf.py`. | Allowed repair surface. Add fixed `maximum_iterations` where needed. |
| `tf.TensorArray` | Present in `annealed_transport_tf.py` streaming chunk accumulators. | Relevant. The XLA error is a TensorList/TensorArray fixed-size error in the active branch. | Allowed repair surface. Bound the enclosing loops and record cap derivations. |
| `tf.scan` | No occurrence found in the audited active path. | Not applicable. | Absent construct. |
| `tf.map_fn` | No occurrence found in the audited active path. | Not applicable. | Absent construct. |
| AutoGraph-lowered Python loops | No Python `for` loop in `annealed_transport_tf.py` active helpers; Python loops found in tests/fixtures/harness reporting only. | Not part of TensorFlow-traced active transport implementation. | Absent from active repair surface. |
| Eager `.numpy()` / Python `bool(...)` diagnostics | Present in `annealed_transport_tf.py`, notably diagnostics and active-row eager branch. | May block graph/JIT if reached. The streaming filter route uses `batched_annealed_transport_core_tf`, which avoids `annealed_transport_resample_tf` eager active-row branching, but `_transport_active` diagnostics may still need tensorization if traced. | Allowed only as narrow graph-safety repair if it blocks after loop-bound repair. |

## First Blocker Classification

The first observed blocker is a TensorList fixed-size XLA error reached through
the active transport branch and consistent with explicit `tf.while_loop` /
`tf.TensorArray` sites in `annealed_transport_tf.py`.

This is inside the allowed repair surface:

- file: `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- construct classes: explicit `tf.while_loop` and `tf.TensorArray`

## Stop/Revise Check

No evidence was found that the first observed blocker is:

- outside `annealed_transport_tf.py`;
- a `tf.scan`;
- a `tf.map_fn`;
- an AutoGraph-lowered Python loop;
- a broader API or algorithmic redesign issue.

If a later JIT diagnostic exposes one of those cases, the repair must stop and
the subplan must be revised before widening the patch.

## Nonclaims

This audit does not prove active-transport score correctness, HMC readiness,
posterior validity, production readiness, or performance improvement.
