# Phase 5 Subplan: Compiled Benchmark Ladder

Date: 2026-06-15

## Status

`READY_FOR_LOCAL_PRECHECK_AND_GPU_APPROVAL`

## Phase Objective

Benchmark experimental value-only and value+score batched LEDH-PFPF-OT using
compiled CPU/GPU runs with scalar-stack comparators and memory/capacity notes.

## Entry Conditions Inherited From Previous Phase

- Value+score correctness gates passed with Phase 4 boundary repair.
- Active annealed transport finite-difference equivalence remains unclaimed.
- Benchmark commands and tolerances are predeclared before execution.
- Trusted GPU/CUDA approval is required before GPU runs.

## Required Artifacts

- Benchmark harness or command entry point under `docs/benchmarks` or
  `experiments/dpf_implementation`.
- JSON/MD benchmark artifacts under `docs/benchmarks`.
- Phase 5 result.
- Refreshed Phase 6 subplan.

## Required Checks, Tests, And Reviews

- CPU graph/compiled benchmark for `B=1,20,256` where feasible.
- GPU graph/compiled benchmark for `B=20,256,4096` only with trusted approval.
- Scalar-stack comparator with identical deterministic inputs for value-only
  where feasible; score scalar-stack may stop at small B if too slow.
- Device, TensorFlow version, XLA/JIT status, compile time, warm-call time, and
  GPU memory status in artifacts.
- Correctness rerun before benchmark.
- Claude review of benchmark interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What are graph/compiled CPU/GPU timing and capacity characteristics for experimental batched LEDH-PFPF-OT value and score? |
| Baseline/comparator | Scalar-stack CPU comparator where feasible and batched CPU/GPU with same deterministic inputs. |
| Primary pass criterion | GPU timings are reported only when run through a graph/compiled wrapper with device/JIT metadata, artifacts record shape/memory/status, and no speed claim exceeds evidence. |
| Veto diagnostics | Uncompiled GPU timing presented as benchmark; wrong device; OOM without classification; missing correctness rerun; missing artifact metadata. |
| Explanatory diagnostics | Compile time, warm-call time, memory/OOM, B/N/T scaling, score overhead, scalar-stack overhead. |
| Not concluded | No universal GPU speedup, no production default, no posterior validity. |
| Artifact preserving result | Phase 5 benchmark JSON/MD and result note. |

## Forbidden Claims And Actions

- Do not compare GPU if not JIT compiled.
- Do not claim speedup from CPU-only scalar comparator alone.
- Do not install packages or change GPU environment.
- Do not use benchmark results as score correctness evidence.
- Do not benchmark HMC, NeuTra, or any filtering inference adapter.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if benchmark artifacts are complete or the result
records a reviewed benchmark blocker and downgrades claims.

## Stop Conditions

Stop GPU benchmarking if trusted GPU approval is unavailable. Stop benchmark
claiming if graph/compiled mode fails for supported shapes or if artifacts
cannot record enough metadata.

## End-Of-Phase Procedure

Run checks, write result, refresh Phase 6 subplan, and review Phase 6.
