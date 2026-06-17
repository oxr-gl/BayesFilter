# Phase 4 Blocker Result - Active Transport Score/JIT - 2026-06-17

## Status

`PHASE_4_BLOCKED_FIXABLE_ACTIVE_TRANSPORT_SCORE_JIT`

## Objective

Test whether the active OT transport branch of the streaming relaxed-objective
score path can compile under XLA and return finite value+score on a tiny
deterministic fixture.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the active OT transport branch compile under XLA and return finite value+score on a tiny deterministic fixture? |
| Baseline/comparator | Original dense tensor arm versus streaming dense, streaming transport, and equivalent streaming callback arms in the gradient-structure harness. |
| Primary pass criterion | Failed. The active-odd FP64 CPU fixture exited nonzero before JSON/Markdown artifact creation. |
| Veto diagnostics | XLA/JIT compile failure fired. |
| Explanatory diagnostics | The log reports `XLA compilation requires a fixed tensor list size` inside the active transport branch. |
| Not concluded | No HMC readiness, no posterior validity, no active-transport score correctness, no production/public API readiness, no performance ranking. |

## Command

```bash
timeout 240 /home/ubuntu/anaconda3/envs/tfgpu/bin/python \
  docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py \
  --device-scope cpu \
  --device /CPU:0 \
  --expect-device-kind cpu \
  --batch-size 1 \
  --time-steps 3 \
  --num-particles 8 \
  --state-dim 2 \
  --obs-dim 2 \
  --transport-policy active-odd \
  --sinkhorn-iterations 3 \
  --repeats 1 \
  --dtype float64 \
  --tf32-mode disabled \
  --output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json \
  --markdown-output docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.md \
  > docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.log 2>&1
```

Exit status: `1`.

## Artifacts

Created:

- `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.log`

Not created because compilation failed before result serialization:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.md`

## Local Diagnosis

The failing log includes:

- `XLA compilation requires a fixed tensor list size. Set the max number of elements.`
- stack frames through `streaming_batched_ledh_pfpf_ot_value_core_tf`;
- a failing node under the active transport conditional:
  `while/cond/while/cond/while_10/Minimum_0/accumulator`.

Focused source inspection found active transport streaming chunk loops in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
that use `tf.TensorArray` and nested `tf.while_loop`s without fixed
`maximum_iterations`.

Candidate repair surface:

- `_filterflow_streaming_softmin`;
- `_filterflow_streaming_sinkhorn_potentials`;
- `_filterflow_streaming_column_log_normalizer`;
- `_filterflow_streaming_transport_from_potentials`;
- any exact Sinkhorn loop that is traced by the dense reference arm and lacks a
  fixed iteration bound.

The same module also contains eager-only diagnostic conversions such as
`.numpy()` and Python `bool(...)`. These may need a graph-safe path or
diagnostic deferral if they are reached by the JIT score diagnostic after the
TensorArray blocker is fixed.

## Decision

Phase 4 cannot pass yet. The active-transport score/JIT blocker is fixable in
principle and should enter a focused repair loop before any Phase 5
HMC-facing diagnostics.

## Next Required Action

Create and review a focused Phase 4 active-transport score/JIT repair subplan.
Do not edit gradient-bearing OT code until that subplan states the exact repair
scope, checks, evidence contract, forbidden claims, and stop conditions.
