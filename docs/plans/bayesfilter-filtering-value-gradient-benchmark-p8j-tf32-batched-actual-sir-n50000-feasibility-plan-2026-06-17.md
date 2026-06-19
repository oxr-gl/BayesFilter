# P8j TF32 Batched Actual-SIR N50000 Feasibility Plan

metadata_date: 2026-06-17
status: EXECUTION_PLAN
lane: P8j DPF SIR d18
executor: Codex

## Question

Does the experimental batched TF32/GPU actual-SIR d18 streaming adapter execute
at `N=50000` particles?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the actual-SIR d18 batched TF32/GPU streaming adapter execute `N=50000` without OOM, nonfinite output, CPU fallback, or artifact failure? |
| Comparator | Prior `B=5,T=20,N=10000` actual-SIR probe: finite, GPU/TF32, warm call `7.375597111880779s`. |
| Primary pass criterion | Trusted-GPU artifact for `N=50000` is written, output is finite, tensor output device is GPU, TF32 is enabled, and actual-SIR semantics metadata is present. |
| Veto diagnostics | OOM, timeout before artifact, nonfinite output, CPU fallback, missing semantics metadata, or route metadata implying scalar Algorithm 1 UKF covariance-lifecycle parity. |
| Explanatory diagnostics | Compile time, warm-call time, GPU memory info, ESS, log likelihood, chunk sizes, and scaling versus `N=10000`. |
| Not concluded | No particle-count adequacy, no MC-SE adequacy, no leaderboard completion, no exact likelihood correctness, no gradient/HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## Execution Ladder

1. Run trusted GPU `B=1,T=20,N=50000`, no warmup, one timed repeat.
2. If the smoke passes, run trusted GPU `B=5,T=20,N=50000`, no warmup, one
   timed repeat.
3. Stop at the first OOM, timeout, nonfinite output, CPU fallback, or artifact
   failure.

## Commands

`B=1` smoke:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b1-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b1-probe-2026-06-17.md
```

`B=5` full five-seed probe:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 50000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n50000-b5-probe-2026-06-17.md
```
