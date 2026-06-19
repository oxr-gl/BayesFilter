# P8j TF32 Batched Actual-SIR N10000 Feasibility Plan

metadata_date: 2026-06-17
status: EXECUTION_PLAN
lane: P8j DPF SIR d18
executor: Codex

## Question

Does the reviewed TF32/GPU batched actual-SIR d18 adapter execute at
`N=10000` particles?

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the experimental batched TF32/GPU actual-SIR streaming adapter execute `N=10000` for SIR d18 without nonfinite output, CPU fallback, or artifact failure? |
| Comparator | Prior `B=5,T=20,D=18,M=9,N=64` actual-SIR probe with finite GPU/TF32 output and mean warm-call time `0.16590180969797075s`. |
| Primary pass criterion | A trusted-GPU artifact for `N=10000` is written, output is finite, output tensor device is GPU, TF32 is enabled, and the actual-SIR semantics block is present. |
| Veto diagnostics | Nonfinite output, trusted GPU unavailable, CPU fallback, out-of-memory, timeout before an artifact is written, missing actual-SIR semantics metadata, or route metadata implying scalar Algorithm 1 UKF covariance-lifecycle parity. |
| Explanatory diagnostics | Compile time, warm-call time, memory info, ESS, log likelihood, output shapes, chunk sizes, and runtime scaling versus `N=64`. |
| Not concluded | No particle-count adequacy, no MC-SE adequacy, no leaderboard completion, no exact likelihood correctness, no DPF gradient correctness, no HMC/NUTS readiness, no Zhao-Cui TT/SIRT or MATLAB parity, no production/default readiness. |

## Execution Ladder

1. Run a trusted GPU `B=1,T=20,N=10000` smoke with `active-all`, no warmup, one
   timed repeat.  This answers whether the core shape is feasible.
2. If the smoke passes quickly enough, run the requested full five-seed
   `B=5,T=20,N=10000` probe with one timed repeat.  Skip extra warmups to avoid
   spending runtime on repeated all-pairs OT before knowing scaling.
3. If either run fails, write a blocker result with the exact failure class.

## Commands

Trusted GPU smoke:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 512 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b1-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b1-probe-2026-06-17.md
```

Trusted GPU full five-seed probe:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 512 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-tf32-batched-actual-sir-n10000-b5-probe-2026-06-17.md
```

## Stop Conditions

Stop after the first failed trusted GPU run if the failure is OOM, timeout,
nonfinite output, CPU fallback, or artifact failure.  Do not run the full
five-seed probe if the one-seed smoke is already blocked.
