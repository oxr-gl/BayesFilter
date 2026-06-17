# BayesFilter DPF LEDH-PFPF-OT Streaming T100 D20 N10000 Stress Plan

Date: 2026-06-15

## Evidence Contract

- Question: can the new streaming LEDH-PFPF-OT path run a larger synthetic
  LGSSM-shaped GPU case with `T=100`, `state_dim=20`, `obs_dim=20`, and
  `N=10000` particles?
- Candidate: streaming benchmark
  `docs/benchmarks/benchmark_experimental_batched_ledh_pfpf_ot_streaming_lgssm.py`.
- Configuration: `B=1,T=100,N=10000,D=20,M=20`, GPU:0, XLA
  `jit_compile=True`, callback proposals, no dense transport matrix,
  active-all transport, `sinkhorn_iterations=4`.
- Primary pass/fail criterion: benchmark emits a finite GPU-placed likelihood
  before timeout.
- Vetoes: non-finite output, CPU placement, benchmark crash, or timeout.
- Explanatory diagnostics: compile-plus-first-call seconds, one warm-call
  timing, GPU allocator memory, and chunk sizes.
- What will not be concluded: no production readiness, no posterior validity,
  no statistical speed ranking, and no claim that `N=100000` is practical.

## Skeptical Plan Audit

- Wrong baseline risk: this is not a dense-vs-streaming comparison; it tests
  whether the streaming route can run at the requested larger shape.
- Proxy metric risk: memory and timing alone do not validate the algorithm.
- Missing stop condition: use a bounded timeout so an all-pairs exact OT run
  cannot consume the session indefinitely.
- Hidden assumption: active-all transport makes this a worst-case exact OT
  stress. If it times out, active-odd or ESS-triggered policies may still be
  viable.
- Environment mismatch: run in trusted GPU context; sandbox GPU failures would
  not be interpreted as machine failures.

Audit status: pass for a bounded descriptive GPU stress run.
