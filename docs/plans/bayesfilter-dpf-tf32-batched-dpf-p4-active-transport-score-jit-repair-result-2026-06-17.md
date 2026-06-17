# Phase 4 Repair Result - Active Transport Score/JIT - 2026-06-17

## Status

`PHASE_4_ACTIVE_TRANSPORT_SCORE_JIT_BLOCKED_NONFINITE_STREAMING_SCORE`

## Objective

Repair the active OT transport score/JIT path enough that the tiny active-odd
gradient-structure diagnostic can compile under XLA and return finite
value+score for dense and streaming transport data structures.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the active OT transport score path be made XLA/JIT-safe on a tiny deterministic fixture while preserving dense-vs-streaming value/score agreement? |
| Primary criterion | Failed. The primary active-odd command now reaches JSON serialization under `jit_compile=True`, but streaming transport arms emit non-finite scores. |
| Compile blocker status | The previous fixed TensorList-size XLA error was removed by bounding the relevant loops. A later `FakeParam` variant XLA error was removed by avoiding the mixed-mask dynamic transport-skip `tf.cond`. |
| Current veto | Non-finite streaming transport score. `streaming_streaming_tensor` and `streaming_streaming_equivalent_callback` have finite values but score `[nan, nan, nan]`. |
| Regression guardrail | No-resampling FP64 score/JIT rerun passed with `overall_passed: true`, all arms finite, `jit_compile: true`, and structure tolerances passed. |
| Not concluded | No active-transport streaming score correctness, no HMC readiness, no posterior validity, no production/public API readiness, no performance ranking. |

## Code Changes

Patched:

- `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`

Implementation changes:

- Added `maximum_iterations` to active transport streaming chunk loops:
  - streaming softmin outer row and inner column loops;
  - streaming Sinkhorn loop;
  - streaming column normalizer outer column and inner row loops;
  - streaming transport-from-potentials outer row and inner column loops.
- Added `maximum_iterations=max_iter` to the dense exact Sinkhorn loop because
  the gradient-structure harness also traces the dense reference arm.
- Defined the missing `num_col_blocks` cap source in
  `_filterflow_streaming_transport_from_potentials`.
- Kept the static no-resampling fast path in the streaming filter.
- Removed the mixed active-mask dynamic `tf.cond` transport skip in the
  likelihood-only streaming path. The masked transport kernel is called
  directly for non-static no-resampling cases, avoiding XLA variant control
  flow while preserving the masked value contract.

## Audit Artifacts

- Pre-patch source audit:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-active-transport-prepatch-source-audit-2026-06-17.md`
- Loop-bound audit:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-active-transport-loop-bound-audit-2026-06-17.md`

The loop-bound audit records all patched caps as non-binding for the planned
tiny active-odd fixture. It also records absent `tf.scan`, `tf.map_fn`, and
AutoGraph-lowered Python-loop constructs in the active transport helper path.

## Diagnostics And Artifacts

Primary active-odd FP64 score/JIT artifact:

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-2026-06-17.md`
- Log:
  `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-active-odd-repair-2026-06-17.log`

Primary active-odd summary:

- `jit_compile`: `true`
- `overall_passed`: `false`
- `finite_all`: `false`
- `structure_passed`: `false`
- `original_dense_tensor`: finite score
- `streaming_dense_tensor`: finite score, matches dense reference to numerical
  precision
- `streaming_streaming_tensor`: non-finite score `[nan, nan, nan]`
- `streaming_streaming_equivalent_callback`: non-finite score `[nan, nan, nan]`

No-resampling FP64 score/JIT regression artifact:

- JSON:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.json`
- Markdown:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.md`
- Log:
  `docs/benchmarks/logs/p4-score-jit-fp64-cpu-b1-t3-np8-d2-m2-noresampling-rerun-2026-06-17.log`

No-resampling summary:

- `jit_compile`: `true`
- `overall_passed`: `true`
- `finite_all`: `true`
- `structure_passed`: `true`
- all arms finite, including streaming transport arms.

Local checks:

- `py_compile` passed for patched files.
- `git diff --check` passed for patched implementation files and audit
  artifacts.

## Decision

Phase 4 does not pass. The original active-transport score/JIT compile blocker
has been narrowed, but the memory-efficient streaming transport plan now fails
the finite-score veto on active transport.

The next repair should target the raw TensorFlow gradient of the streaming
transport plan. Dense transport score is finite and matches the dense reference;
streaming transport values match but gradients are NaN. This suggests a
backward-pass numerical issue in the streaming log-domain transport
normalization/application path, not a value-path mismatch.

## Next Required Action

Create a new focused subplan before further code edits. That subplan should
distinguish at least three routes:

- diagnose and stabilize the raw gradient of streaming transport;
- use a dense-gradient/streaming-value hybrid for tiny or HMC-facing score
  diagnostics if memory allows;
- implement a custom gradient for streaming transport that avoids the NaN
  backward path.

Do not start Phase 5 HMC-facing diagnostics until active transport score has a
finite, reviewed path or the user explicitly changes the research target.
