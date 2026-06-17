# Phase 4 Repair Result - Score JIT TensorArray Repair - 2026-06-16

## Status

`PHASE_4_SCORE_JIT_REPAIR_PASSED_NO_RESAMPLING`

## Objective

Repair the streaming relaxed-objective value+score path so a tiny
no-resampling score diagnostic can compile with XLA.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can a focused TensorArray/loop repair make the tiny no-resampling streaming score path XLA/JIT-safe without changing value semantics? |
| Baseline/comparator | The failing Phase 4 log and current streaming value/score tests. |
| Primary pass criterion | Passed for no-resampling. The FP64 and FP32-no-TF32 tiny score/JIT diagnostics exited 0, emitted finite/JIT artifacts, and focused streaming tests passed. |
| Veto diagnostics | No active no-resampling veto. The original XLA fixed tensor-list failure is repaired for the no-resampling score path. |
| Explanatory diagnostics | Active-transport score JIT is not yet promoted; it remains a separate Phase 4/5 gate. |
| Not concluded | No active-transport score correctness, no HMC readiness, no posterior validity, no production/public API readiness. |

## Code Changes

Patched:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Implementation changes:

- Added `maximum_iterations` to the streaming particle-chunk `tf.while_loop`.
- Split the streaming value recursion into:
  - a history path that carries TensorArrays only when `return_history=True`;
  - a likelihood-only path with no history TensorArrays when
    `return_history=False`.
- Added a static all-false no-resampling fast path so no-resampling score/JIT
  does not trace the transport branch.
- Kept the transport branch untouched for active transport.

Test changes:

- Added FP32/XLA-scale tolerances for streaming transport parity,
  compiled/eager value parity, and float32 finite-difference score checks.
- The stricter JSON correctness gates were run and passed separately.

## Diagnostics And Artifacts

Original failing log:

- `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.log`

Repair attempt 1 log, still failing inside transport branch tracing:

- `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-repair-2026-06-16.log`

Passing FP64 score/JIT artifact:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.md`
- Log:
  `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-repair2-2026-06-16.log`

Passing FP32-no-TF32 score/JIT artifact:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp32-notf32-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp32-notf32-cpu-b1-t3-np8-d2-m2-noresampling-2026-06-16.md`
- Log:
  `docs/benchmarks/logs/p4-score-jit-fp32-notf32-cpu-b1-t3-np8-d2-m2-noresampling-repair-2026-06-16.log`

Passing streaming correctness score-FD gate:

- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-correctness-score-fd-cpu-b2-t3-np4-noresampling-2026-06-16.json`
- `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-streaming-correctness-score-fd-cpu-b2-t3-np4-noresampling-2026-06-16.md`
- Log:
  `docs/benchmarks/logs/p4-streaming-correctness-score-fd-cpu-b2-t3-np4-noresampling-2026-06-16.log`

Focused tests:

- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`
  - log: `docs/benchmarks/logs/p4-pytest-streaming-tf-repair4-2026-06-16.log`
  - result: `8 passed`
- `tests/test_experimental_batched_benchmark_harness.py -k streaming_ledh_pfpf_ot`
  - log: `docs/benchmarks/logs/p4-pytest-streaming-benchmark-harness-repair-2026-06-16.log`
  - result: `3 passed, 10 deselected`

Local checks:

- `py_compile` passed for the streaming implementation.
- `git diff --check` passed for the patched implementation, tests, and repair
  subplan.

## Decision

The no-resampling streaming score path is now JIT-safe on the tiny diagnostic
ladder used in this repair.

This does not yet prove active-transport score JIT safety or HMC readiness.
The next phase should test active transport score finite/JIT behavior, then
only afterward proceed to HMC-facing value/gradient diagnostics.
