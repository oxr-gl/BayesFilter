# BayesFilter DPF LEDH-PFPF-OT Streaming GPU Implementation Result

Date: 2026-06-15

Plan:
`docs/plans/bayesfilter-dpf-ledh-pfpf-ot-streaming-gpu-implementation-plan-2026-06-15.md`

## Decision Table

| Field | Status |
| --- | --- |
| Decision | Keep the new streaming implementation as an experimental opt-in GPU path. |
| Primary criterion | Passed tiny deterministic parity against the existing fixed-branch baseline. |
| Veto diagnostics | No veto fired: finite outputs, CPU/GPU JIT smoke, no Python time loop, no dense streaming transport output. |
| Main uncertainty | Large-scale exact OT remains all-pairs compute; 100k particles needs careful chunk tuning and may still be runtime-bound. |
| Next justified action | Run a gated scaling ladder for `D=20,50,100` and increasing `N` with memory/time artifacts. |
| Not concluded | No production readiness, no CPU/GPU superiority, no posterior validity, no active-transport finite-difference score equivalence. |

## What Changed

- Added
  `experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py`.
- Added a streaming value recursion using `tf.while_loop` over time.
- Added particle-chunked LEDH flow so per-particle `[D,D]` flow tensors are
  held only per chunk instead of across all particles.
- Added likelihood-only mode with `return_history=False`.
- Added `pre_flow_step_fn` support so production-shaped runs can generate
  proposals per step instead of requiring full `[B,T,N,D]` pre-flow storage.
- Defaulted the new path to streaming OT, which returns a `[B,0,0]` sentinel
  instead of materializing a dense `[B,N,N]` transport matrix.
- Added correctness and LGSSM scale benchmark scripts for the streaming path.

## Verification

| Check | Result |
| --- | --- |
| `pytest tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q` | 8 passed |
| `pytest tests/test_experimental_batched_benchmark_harness.py -q` | 12 passed |
| `pytest tests/test_experimental_batched_ledh_pfpf_ot_tf.py tests/test_experimental_batched_ledh_pfpf_ot_streaming_tf.py -q` | 31 passed |
| `git diff --check` on touched DPF files | Passed |
| Streaming correctness gate CPU artifact | Passed |
| Trusted GPU tiny smoke | Passed on GPU:0 |
| Trusted GPU moderate smoke | Passed on GPU:0 |

## Artifacts

- Correctness:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-correctness-cpu-b2-t3-np4-d1-2026-06-15.json`
- Correctness note:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-correctness-cpu-b2-t3-np4-d1-2026-06-15.md`
- Tiny GPU smoke:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t3-np4-d2-m2-callback-2026-06-15.json`
- Tiny GPU smoke note:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t3-np4-d2-m2-callback-2026-06-15.md`
- Moderate GPU smoke:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t20-np256-d10-m10-callback-2026-06-15.json`
- Moderate GPU smoke note:
  `docs/benchmarks/experimental-batched-ledh-pfpf-ot-streaming-lgssm-gpu0-b1-t20-np256-d10-m10-callback-2026-06-15.md`

## Inference Status

| Evidence class | Status |
| --- | --- |
| Hard veto screen | Passed for the tested tiny and moderate synthetic fixtures. |
| Statistically supported ranking | None. Timing results are descriptive single-run smoke diagnostics. |
| Descriptive-only differences | GPU warm-call timing and memory readings. |
| Default-readiness | Not ready; implementation is experimental and opt-in. |
| Next evidence needed | Gated multi-shape GPU ladder with repeated warm calls and explicit memory ceilings. |

## Notes

- This implementation removes avoidable dense transport storage in the streaming
  path; it does not remove the all-pairs OT computation.
- For `N=100000`, storing a dense transport matrix is infeasible, but chunked
  exact OT still implies very large compute. The next benchmark ladder should
  find the practical boundary before treating 100k particles as usable.
- For `D=100`, particle-chunked LEDH flow avoids persistent `[B,N,D,D]`
  storage, but each chunk still performs dense linear algebra. Chunk size is a
  real tuning parameter.
