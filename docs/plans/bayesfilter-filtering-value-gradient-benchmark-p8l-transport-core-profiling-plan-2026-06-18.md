# P8l Plan: Transport-Core GPU Profiling For Batched DPF

metadata_date: 2026-06-18
status: READY_FOR_EXECUTION
executor: Codex
reviewer: Claude read-only if material design or claim boundary changes are proposed

## Objective

Profile the generic OT/Sinkhorn transport contribution in the experimental
batched TF32/GPU LEDH-PFPF-OT actual-SIR stress harness without changing the
algorithm implementation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Scientific/engineering question | Is trusted-GPU runtime at `N=10000`, `B=5`, `T=20`, SIR d18 primarily explained by active transport, and how sensitive is it to Sinkhorn iteration count? |
| Baseline/comparator | Current experimental batched actual-SIR harness with `transport-policy active-all`, `history-mode value-only`, TF32 enabled, `N=10000`, `sinkhorn_iterations=10`, row/col chunks 2048, particle chunk 1024. |
| Primary criterion | Trusted-GPU artifacts are finite, metadata-complete, and show warm-call timing for matched no-transport and active-transport rungs.  Iteration rungs are interpreted only as runtime/log-likelihood sensitivity diagnostics. |
| Veto diagnostics | CPU fallback, nonfinite output, OOM, missing configuration metadata, changing code before profiling, treating speed as particle adequacy, or claiming exact internal kernel attribution from whole-call timings. |
| Explanatory diagnostics | Compile time, warm-call timing, log likelihood vector, memory counter, transport policy, Sinkhorn iteration count, chunk sizes, ESS if available. |
| Not concluded | Particle-count adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or that a lower Sinkhorn iteration count is scientifically acceptable. |

## Skeptical Plan Audit

Potential failure modes:

- Whole-call timing cannot isolate every internal kernel.  Mitigation: treat
  no-transport versus active-all as a coarse attribution only.
- `no-resampling` changes algorithm semantics.  Mitigation: use it as a
  runtime lower-bound diagnostic, not as a candidate replacement.
- Lower Sinkhorn iterations may change filter values.  Mitigation: record log
  likelihood sensitivity and do not promote any lower iteration count.
- One-repeat timings are noisy.  Mitigation: use them only to identify the next
  optimization target, not to establish a production speed claim.

Audit status: `PASS_FOR_NONINVASIVE_PROFILE`.

## Required Artifacts

- This plan.
- JSON and markdown artifacts for executed rungs under
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-*`.
- Result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-transport-core-profiling-result-2026-06-18.md`

## Commands

All TensorFlow GPU commands must be run in trusted/escalated context.

Preflight:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Baseline active transport:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode value-only --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-2026-06-18.md
```

No-transport lower-bound diagnostic:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy no-resampling --history-mode value-only --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-no-resampling-n10000-it10-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-no-resampling-n10000-it10-2026-06-18.md
```

Sinkhorn iteration sensitivity, active transport:

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode value-only --sinkhorn-iterations 5 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-2026-06-18.md
```

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py --batch-seeds 81120,81121,81122,81123,81124 --time-steps 20 --num-particles 10000 --dtype float32 --tf32-mode enabled --transport-policy active-all --history-mode value-only --sinkhorn-iterations 20 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 1024 --warmups 0 --repeats 1 --device /GPU:0 --expect-device-kind gpu --output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it20-2026-06-18.json --markdown-output docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it20-2026-06-18.md
```

## Stop Conditions

- Stop immediately on CPU fallback, OOM, nonfinite output, or missing artifact.
- Stop before expensive additional rungs unless the executed rungs identify a
  concrete next profile question.
- If single-repeat Sinkhorn iteration timings are nonmonotone or otherwise
  unstable, run at most two focused stability rungs with one warmup and two
  repeats.  These rungs are explanatory only and do not authorize iteration
  count promotion.
- Do not make particle-adequacy, leaderboard, HMC, default, or scientific
  validity claims from this profile.

## Handoff

The result should identify the next optimization target as one of:

- transport/Sinkhorn exact implementation work;
- Sinkhorn iteration/epsilon tuning as a separate statistical validation lane;
- chunk scheduling profile;
- instrumentation upgrade for internal timing;
- or stop if transport is not the dominant factor.
