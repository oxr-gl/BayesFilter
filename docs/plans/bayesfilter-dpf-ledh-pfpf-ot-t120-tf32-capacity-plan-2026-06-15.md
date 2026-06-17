# BayesFilter DPF LEDH-PFPF-OT T120 TF32 Capacity Plan - 2026-06-15

## Research Intent Ledger

- Main question: With the current streaming TF32 experimental LEDH-PFPF-OT
  data structure, what `state_dim` and `num_particles` are feasible on one
  32GB RTX 4080 SUPER for `T=120`, and would two GPUs via `MirroredStrategy`
  help?
- Candidate under test: streaming callback value path with `float32` tensors,
  TF32 enabled, no dense `[N,N]` transport storage, and no full `[T,N,D]`
  pre-flow tensor.
- Expected failure mode: memory remains small, but active-all exact OT becomes
  compute-bound as `O(T N^2 D)`; high `D` also increases per-particle LEDH
  linear algebra cost.
- Promotion criterion: finite GPU-placed JIT-compiled runs for representative
  `T=120` shapes, with memory/timing sufficient to estimate a practical
  envelope.
- Promotion veto: non-finite output, GPU placement failure, OOM, timeout before
  producing a diagnostic artifact, or metadata not showing TF32 default.
- Continuation veto: do not run larger points once measured warm time and
  scaling imply multi-hour runtime for the next point.
- Repair trigger: if TF32 metadata is wrong or correctness smoke fails, stop
  and repair precision plumbing before interpreting capacity.
- Explanatory diagnostics: warm-call seconds, compile+first seconds, allocator
  memory, output device, finite flag, and scaling ratios.
- What must not be concluded: no HMC readiness, no posterior validity, no
  production default proof, no two-GPU speedup claim without an implementation
  or benchmark.

## Evidence Contract

- Engineering question: What is the practical `T=120` capacity envelope under
  current TF32 streaming implementation?
- Comparator/baseline: previous `T=100,D=20,N=10000` streaming result and new
  `T=120` TF32 runs.
- Primary criterion: a shape is "practical" only if it completes a warm call in
  a time suitable for repeated likelihood/gradient use; "memory-feasible" only
  requires finite output without OOM.
- Veto diagnostics: OOM, non-finite values, wrong device, missing TF32 metadata,
  or timeout.
- Explanatory-only diagnostics: exact timing from one run and extrapolated
  scaling for unrun larger shapes.
- Artifact preserving result: benchmark JSON/Markdown under `docs/benchmarks`
  and result note under `docs/plans`.

## Skeptical Plan Audit

- Wrong baseline: do not use dense OT capacity; current path is streaming
  memory, all-pairs compute.
- Proxy metrics: allocator memory is not a production capacity proof; nvidia
  process memory and runtime also matter.
- Missing stop conditions: stop once next point is projected to be multi-hour.
- Unfair comparison: use the same transport policy, chunks, dtype, TF32 mode,
  and proposal mode across ladder points unless the result note says otherwise.
- Hidden assumption: runtime is approximately linear in `T`, roughly quadratic
  in `N`, and at least linear in `D` for OT; LEDH per-particle matrix algebra
  adds extra `D` dependence.
- Environment mismatch: GPU commands must run in trusted context and record
  device.
- Artifact mismatch: every interpreted run must preserve precision metadata.

Audit status: passed for a bounded capacity diagnostic; not a production-scale
HMC validation.

## Planned Ladder

Use:

- `T=120`
- `proposal-mode=callback`
- `transport-policy=active-all`
- `sinkhorn-iterations=4`
- `row_chunk_size=512`
- `col_chunk_size=512`
- `particle_chunk_size=128` for `D<=50`, smaller if needed for `D=100`
- default precision, expected to be `float32` with TF32 enabled

Initial actual runs:

1. `D=20,N=10000`
2. `D=50,N=5000` if run 1 is not already too slow
3. `D=100,N=2000` if run 2 is not already too slow

Use scaling estimates rather than actual multi-hour runs for larger `N`.
