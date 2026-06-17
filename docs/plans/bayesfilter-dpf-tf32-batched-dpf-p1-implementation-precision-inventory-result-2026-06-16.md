# Phase 1 Result - Implementation And Precision Inventory - 2026-06-16

## Status

`PHASE_1_PASSED`

## Objective

Inventory the current TF32 batched DPF implementation, precision controls, JIT
boundaries, benchmark scripts, and score-path blockers before further
implementation.

No algorithm, benchmark, or test code was changed in this phase.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What exact code paths and precision knobs currently define the TF32 batched DPF lane, and what must Phase 2 use or avoid? |
| Baseline/comparator | Current repository files plus the 2026-06-15 TF32 default, MC-noise, capacity, and reset artifacts. |
| Primary pass criterion | Passed. This result records the file/function inventory, precision-lane table, score/JIT boundary, dirty-worktree boundary, and Phase 2 handoff. |
| Veto diagnostics | No active veto. Streaming implementation path, precision controls, and FP64/FP32-no-TF32 reference lanes are present. No implementation edit was made. |
| Explanatory diagnostics | Source inventory only. No runtime, speed, memory, or GPU conclusion is made here. |
| Not concluded | No speed ranking, no correctness proof, no HMC readiness, no production default, no public API readiness. |

## Implementation Inventory

| Path | Role | Phase 2 relevance |
| --- | --- | --- |
| `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Experimental streaming GPU-oriented value path. Uses `tf.while_loop`, particle chunking, streaming OT, optional `return_history=False`, and `pre_flow_step_fn` callback. Also exposes a GradientTape value+score wrapper. | Primary target for Phase 2 single-GPU batched value work. Use value path first; do not promote score/HMC from this phase. |
| `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py` | Existing fixed-branch batched core, shape contracts, precision metadata, fixed `[B,T,N,D]` pre-flow path, dense/streaming transport adapter, value and value+score wrappers. | Baseline/reference and precision-policy source. Avoid replacing it during Phase 2 unless a later repair subplan authorizes it. |
| `experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py` | Annealed transport implementation. Supports `transport_plan_mode="dense"` and `"streaming"`. Streaming mode returns an empty transport matrix and supports raw gradients only. | Phase 2 must use streaming transport for large value runs and must not claim dense `[N,N]` storage is materialized. |
| `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` | JIT-compiled LGSSM-shaped benchmark harness for the streaming value path. Defaults to `float32` and TF32 enabled. Supports callback proposal mode and records precision/device metadata. | Phase 2 benchmark/runner baseline. Use bounded shapes first and preserve descriptive-only timing language. |
| `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py` | Streaming correctness gate comparing streaming value path to existing fixed-branch baseline on tiny fixtures. Has optional JIT smoke and optional score finite-difference check. | Phase 2 local correctness gate for value path; score checks are not Phase 2 promotion evidence. |
| `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_pf_mc_error_vs_precision.py` | Aggregates FP64, FP32-no-TF32, and FP32+TF32 child runs for value/score drift versus PF MC variability. | Reference for later precision/HMC phases, not a Phase 2 value batching gate. |
| `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_gradient_structure.py` | HMC-facing value/score structure diagnostic with explicit dtype and TF32 controls. | Phase 4/5 material only. Do not use for Phase 2 pass/fail. |
| `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py` | Unit tests for streaming flow parity, value parity, likelihood-only history omission, callback versus tensor proposal, streaming transport no dense matrix, JIT smoke, and no-resampling score finite difference. | Useful small local check before Phase 2 edits/runs. |
| `tests/test_experimental_batched_ledh_pfpf_ot_tf.py` | Unit tests for fixed-branch core, streaming transport parity, value path, value+score finite behavior, and no-resampling finite-difference score. | Reference-path guardrail. |
| `tests/test_experimental_batched_benchmark_harness.py` | Harness-level tests, including streaming correctness and streaming benchmark tiny CPU JSON cases. | Lightweight harness regression check for Phase 2 if touched. |

## Precision Lane Inventory

| Lane | Current support | Status |
| --- | --- | --- |
| FP64 reference | Explicit `--dtype float64`; correctness script defaults to FP64 for fixed-branch checks; precision comparison includes `fp64`. | Required reference/comparator lane. |
| FP32 without TF32 | Explicit `--dtype float32 --tf32-mode disabled`; precision comparison includes `fp32_no_tf32`. | Required comparison lane. |
| FP32 with TF32 | Scoped default for experimental LEDH-PFPF-OT GPU/performance lane via `DEFAULT_DTYPE = tf.float32`, `DEFAULT_TF32_MODE = "enabled"`, and benchmark defaults. | Phase 2 performance default candidate only, not global BayesFilter policy. |

The core metadata source is `precision_policy_metadata()` in
`experimental_batched_ledh_pfpf_ot_tf.py`. Benchmark scripts update module-level
`DTYPE` in the core, streaming, and transport modules, and call
`tf.config.experimental.enable_tensor_float_32_execution(...)` when a nondefault
TF32 mode is supplied.

## JIT And Score Boundary

- The streaming value core uses `tf.while_loop` over time and particle chunks.
- `benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py` wraps the
  streaming value call in `tf.function(jit_compile=True)`.
- The streaming score wrapper exists through TensorFlow `GradientTape`, but
  score/HMC remains outside Phase 2. Prior reset/result notes say the HMC-facing
  score path still needs JIT-safe validation.
- Streaming transport supports raw gradients only. Active-transport finite
  difference equivalence is not a Phase 2 claim.

## Dirty Worktree Boundary

The relevant DPF implementation, benchmark, and tests are currently untracked
artifacts in the working tree:

- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_tf.py`
- `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`
- `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py`
- `docs/benchmarks/compare_experimental_batched_ledh_pfpf_ot_pf_mc_error_vs_precision.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py`
- `tests/test_experimental_batched_ledh_pfpf_ot_tf.py`

Treat them as existing session/user artifacts. Do not delete, consolidate, or
revert them without explicit instruction.

## Phase 2 Handoff

Phase 2 may begin. It should target the streaming value path only:

- primary implementation path:
  `experimental_batched_ledh_pfpf_ot_streaming_tf.py`;
- primary runner/harness:
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`;
- primary correctness gate:
  `docs/benchmarks/check_experimental_batched_ledh_pfpf_ot_streaming_correctness.py`;
- precision default for performance runs: `float32` with TF32 enabled;
- mandatory reference/comparison lanes to preserve: FP64 and FP32-no-TF32;
- forbidden Phase 2 claims: score JIT readiness, HMC readiness, production
  readiness, public API readiness, and single-filter particle-cloud sharding.

## Next Action

Execute Phase 2 from:

- `docs/plans/bayesfilter-dpf-tf32-batched-dpf-p2-single-gpu-batched-value-subplan-2026-06-16.md`
