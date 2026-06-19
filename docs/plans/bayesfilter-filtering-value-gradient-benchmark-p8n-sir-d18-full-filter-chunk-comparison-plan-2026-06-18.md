# P8n Plan: SIR d18 Full-Filter Chunk Comparison

metadata_date: 2026-06-18
status: READY_FOR_TRUSTED_GPU_EXECUTION
lane: DPF / LEDH-PFPF-OT generic transport configuration
executor: Codex

## Question

Does the generic transport-core chunk candidate `row_chunk_size=1024,
col_chunk_size=1024` make the actual SIR d18 full-filter benchmark faster than
the current `2048/2048` setting at `N=10000` and `N=50000`?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Compare actual SIR d18 full-filter wall time for `1024/1024` versus `2048/2048` chunks at `N=10000` and `N=50000`. |
| Baseline/comparator | Same harness, seeds, TF32/GPU, `transport-policy active-all`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`, `particle_chunk_size=1024`, and `history-mode full`; only row/column chunk size changes. |
| Primary criterion | Trusted-GPU artifacts are finite and GPU-backed; candidate is faster only if its warm-call mean is lower under matched settings for the same `N`. |
| Veto diagnostics | CPU fallback, nonfinite output, OOM, missing metadata, changed model/seed/Sinkhorn/particle chunk/history settings, or log-likelihood drift not attributable to the same stochastic seeds/settings. |
| Explanatory diagnostics | Compile-plus-first-call time, warm-call timings, TensorFlow GPU memory counters, speedup versus legacy scalar comparator, output log likelihoods, ESS minima. |
| Not concluded | Particle-count adequacy, MC-SE adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production readiness, or cross-model/default-policy readiness. |
| Artifact | This plan plus four JSON/markdown benchmark artifacts and a P8n result note under `docs/plans`. |

## Skeptical Audit

The plan avoids the main traps from P8m:

- It does not treat the synthetic transport-core `0.293s` timing as a
  full-filter timing.
- It does not promote memory savings alone; runtime is the primary comparison.
- It holds `particle_chunk_size=1024` fixed so row/column chunk size is the
  only chunking variable.
- It uses actual SIR d18 callbacks through the existing P8j harness, not a
  synthetic model.
- It treats single-repeat `N=50000` results as a practical diagnostic, not a
  stable default-setting proof.

The plan is acceptable for answering whether this setting looks faster on the
actual SIR d18 workload. It is not sufficient to change repository defaults.

## Commands

Trusted GPU preflight:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

`N=10000`, two repeats after one warmup:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk1024-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk1024-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 1 --repeats 2 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk2048-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n10000-chunk2048-2026-06-18.md
```

`N=50000`, one repeat and no extra warmup to keep the diagnostic bounded:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk1024-2026-06-18.md
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode full --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8n-sir-d18-n50000-chunk2048-2026-06-18.md
```

## Stop Conditions

- Stop and write a blocker result if any trusted GPU rung falls back to CPU,
  OOMs, produces nonfinite output, or writes incomplete metadata.
- Stop before default-policy claims even if `1024/1024` is faster.
- If `N=50000` runtime becomes impractical or external interruption occurs,
  preserve completed artifacts and report the partial result explicitly.
