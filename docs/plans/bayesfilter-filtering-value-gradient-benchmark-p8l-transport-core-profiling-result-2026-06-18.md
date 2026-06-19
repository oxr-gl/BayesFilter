# P8l Result: Transport-Core GPU Profiling For Batched DPF

metadata_date: 2026-06-18
status: PASS_PROFILE_TRANSPORT_DOMINATES_NEXT_VALIDATION_REQUIRED
plan: docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-transport-core-profiling-plan-2026-06-18.md
executor: Codex

## Decision Table

| Field | Decision |
| --- | --- |
| Decision | Active OT/Sinkhorn transport is the dominant runtime component in the coarse whole-call profile.  The next optimization target should be transport-core work, not history diagnostics or inactive-mask plumbing. |
| Primary criterion status | Passed.  Trusted-GPU artifacts are finite, GPU-backed, metadata-complete, and cover matched active-all, no-resampling, and Sinkhorn iteration sensitivity rungs. |
| Veto diagnostic status | No CPU fallback, OOM, nonfinite output, or missing artifact.  No scientific adequacy or default claim is made. |
| Main uncertainty | Whole-call timing is coarse and one-repeat rungs were noisy; kernel-level attribution still needs instrumentation if we want exact internal split. |
| Next justified action | Create a gated P8m lane for transport-core optimization: chunk scheduling/internal timing first, and a separate validation gate for any lower Sinkhorn iteration count. |
| What is not concluded | No particle adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or that `sinkhorn_iterations=5` is scientifically acceptable. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is trusted-GPU runtime at `N=10000`, `B=5`, `T=20`, SIR d18 primarily explained by active transport, and how sensitive is it to Sinkhorn iteration count? |
| Baseline/comparator | Current experimental batched actual-SIR harness with `transport-policy active-all`, `history-mode value-only`, TF32 enabled, `N=10000`, `sinkhorn_iterations=10`, row/col chunks 2048, particle chunk 1024. |
| Primary criterion | Trusted-GPU artifacts are finite, metadata-complete, and show warm-call timing for matched no-transport and active-transport rungs.  Iteration rungs are interpreted only as runtime/log-likelihood sensitivity diagnostics. |
| Veto diagnostics | CPU fallback, nonfinite output, OOM, missing configuration metadata, changing code before profiling, treating speed as particle adequacy, or claiming exact internal kernel attribution from whole-call timings. |
| Explanatory diagnostics | Compile time, warm-call timing, log likelihood vector, memory counter, transport policy, Sinkhorn iteration count, chunk sizes. |
| Not concluded | Particle-count adequacy, leaderboard completion, exact likelihood correctness, DPF gradient correctness, HMC/NUTS readiness, production/default readiness, or that a lower Sinkhorn iteration count is scientifically acceptable. |

## Checks Run

Local checks:

```bash
python -m py_compile docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py
git diff --check -- docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-transport-core-profiling-plan-2026-06-18.md docs/benchmarks/benchmark_p8j_tf32_batched_actual_sir.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
```

Both passed.

Trusted GPU preflight:

```bash
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
```

Observed device:

- NVIDIA GeForce RTX 4080 SUPER, 16376 MiB, driver 591.86.

Artifact assertion:

- all JSON artifacts below are finite;
- all expected GPU outputs are on `/device:GPU:0`;
- all artifacts preserve shape/configuration metadata.

## Artifacts

- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-no-resampling-n10000-it10-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-no-resampling-n10000-it10-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it20-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it20-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-stability-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it10-stability-2026-06-18.md`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-stability-2026-06-18.json`
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8l-active-all-n10000-it5-stability-2026-06-18.md`

## Coarse Transport Attribution

| Rung | Policy | Sinkhorn iterations | Warmups / repeats | Warm mean seconds | Compile + first seconds | Peak memory counter bytes |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| active baseline | active-all | 10 | 0 / 1 | 9.500686 | 22.553406 | 210641920 |
| no-transport lower bound | no-resampling | 10 | 0 / 1 | 1.707570 | 10.016849 | 80050176 |

Coarse active-transport delta:

```text
9.500686 - 1.707570 = 7.793116 seconds
```

Coarse active-transport fraction of active baseline warm time:

```text
7.793116 / 9.500686 = 0.820269
```

Interpretation:

- active OT/Sinkhorn transport accounts for about 82 percent of the active-all
  warm-call time in this coarse whole-call comparison;
- `no-resampling` changes algorithm semantics and is only a lower-bound
  runtime diagnostic.

## Sinkhorn Iteration Sensitivity

Single-repeat rungs:

| Rung | Sinkhorn iterations | Warm mean seconds | Compile + first seconds | Log likelihood note |
| --- | ---: | ---: | ---: | --- |
| active-all | 5 | 20.591379 | 41.520453 | finite, different from it10 |
| active-all | 10 | 9.500686 | 22.553406 | finite, baseline |
| active-all | 20 | 8.952253 | 22.296159 | finite, different from it10 |

These single-repeat timings are nonmonotone and were treated as unstable.
Following the plan stop-condition amendment, two focused stability rungs were
run with one warmup and two repeats.

Stability rungs:

| Rung | Sinkhorn iterations | Warm timings seconds | Warm mean seconds | Mean ratio to it10 |
| --- | ---: | --- | ---: | ---: |
| active-all stability | 10 | `[8.316488, 8.792221]` | 8.554354 | 1.000000 |
| active-all stability | 5 | `[4.782670, 6.594034]` | 5.688352 | 0.664966 |

Warmed iteration-5 saved about 2.866 seconds relative to warmed iteration-10 in
this diagnostic, but it also changed log likelihood values.  That makes lower
iteration count a performance candidate requiring validation, not an immediate
replacement.

## Log Likelihood Sensitivity

Iteration 10 baseline log likelihood:

```text
[-902.4534301757812, -902.7452392578125, -903.4571533203125, -903.2506713867188, -902.4193115234375]
```

Iteration 5 stability log likelihood:

```text
[-902.453125, -902.7131958007812, -903.4395751953125, -903.2227172851562, -902.444580078125]
```

Iteration 20 log likelihood:

```text
[-902.448486328125, -902.6851806640625, -903.4461669921875, -903.1961669921875, -902.3875122070312]
```

These differences are explanatory.  They do not by themselves decide which
iteration count is scientifically acceptable.

## Interpretation

The result explains why the P8k history-mode improvement did not speed up
`N=10000`: history diagnostics were not the dominant cost.  Active transport is.

The no-resampling lower bound shows the non-transport filter path is already
around 1.7 seconds for this shape.  The active-all baseline is around 8.5 to
9.5 seconds depending on warmed timing.  That leaves transport as the largest
remaining engineering target.

Lower Sinkhorn iteration count is promising for speed after warmup, but it
changes values and cannot be adopted without a separate validation contract.

## Recommended Next Lane

Create a gated P8m transport-core optimization lane with two parts:

1. Internal instrumentation or microbenchmark:
   - separate pairwise cost/logsumexp potential updates from final transport
     application;
   - test row/col chunk sizes such as 1024, 2048, 4096 with warmed repeats;
   - record XLA compile behavior separately from warm calls.

2. Exact-versus-approximate decision:
   - exact implementation optimization stays within the current Corenflos /
     entropic OT route;
   - lower iteration count, epsilon changes, top-k/sparse/local transport, or
     approximate transport must be labeled as tuning/extension and validated
     against log-likelihood and downstream diagnostics.

## Boundary

No code was changed for this profile except for the plan/result artifacts.  The
existing harness was used as-is.

The harness field `primary_pass_5x_runtime_gate` remains a legacy explanatory
field and is not used as a P8l pass criterion.

No `N=50000` run was launched.

## Post-Run Red Team

Strongest alternative explanation:

- Whole-call no-resampling versus active-all includes more than just Sinkhorn
  kernels, so the 82 percent figure is a coarse attribution rather than a
  kernel-level measurement.

What would overturn the main conclusion:

- Internal instrumentation showing pairwise OT/Sinkhorn kernels are a small
  fraction of the active-all time and another callback/flow path dominates.

Weakest part of the evidence:

- Single-process TensorFlow/XLA timings were noisy, especially before adding
  warmup.  The result is strong enough to pick the next profiling target, but
  not to promote a new numerical setting.
