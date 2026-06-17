# BayesFilter DPF LEDH-PFPF-OT Streaming Vs Fixed Benchmark Plan

Date: 2026-06-15

## Evidence Contract

- Question: does the new streaming GPU path improve the practical compiled
  execution profile versus the old fixed-branch experimental path on a more
  realistic synthetic LGSSM shape?
- Shape: `B=1,T=100,N=1000,state_dim=10,obs_dim=10`.
- Comparator: old fixed-branch LGSSM benchmark
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_lgssm_scale.py`.
- Candidate: new streaming LGSSM benchmark
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`.
- Shared settings: GPU:0, XLA `jit_compile=True`, active-all transport,
  `sinkhorn_iterations=4`, one compile/first call and one warm call.
- Primary pass/fail criterion: both runs emit finite GPU-placed likelihoods.
- Descriptive diagnostics: compile-plus-first-call seconds, one warm-call
  timing, GPU memory info, proposal mode, and dense transport materialization.
- Promotion vetoes: non-finite output, CPU placement during GPU run, benchmark
  crash, or missing artifact.
- What will not be concluded: no statistically supported speed ranking, no
  production readiness, no posterior validity, and no claim that `N=100000` is
  practical.

## Skeptical Plan Audit

- Wrong baseline: compare against the current fixed-branch DPF benchmark, not
  against HMC or a different OT research program.
- Proxy metric risk: warm-call timing alone cannot establish correctness or
  production readiness.
- Fair comparison: use the same synthetic shape, GPU, active transport policy,
  and Sinkhorn iteration count.
- Hidden assumption: streaming uses callback proposals and no dense transport
  matrix, while fixed-branch uses full pre-flow tensor and dense transport;
  this is the intended implementation comparison, but it means warm-call timing
  mixes execution-shape and memory-contract differences.
- Stop condition: if either run fails or emits non-finite output, do not compare
  speed.

Audit status: pass for a descriptive benchmark comparison.
