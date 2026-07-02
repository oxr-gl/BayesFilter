# N10000 XLA Chunk3334 Timing Plan

date: 2026-06-24
status: READY_FOR_RUN

## Question

For the compiled single-seed `N=10000`, `T=3` manual-reverse LEDH-PFPF-OT route, does `row_chunk_size=col_chunk_size=3334` improve warm-call timing relative to the current `2048 x 2048` timing baseline?

## Skeptical Audit

This is a timing and allocator diagnostic only. It must not be treated as an FD agreement check, gradient-correctness result, HMC-readiness result, or production-readiness result.

The main plan risks are: comparing against a stale non-XLA baseline; mistaking TensorFlow allocator reservation for actual peak; accidentally running FD or multiple seeds; changing Sinkhorn or particle chunk settings while testing row/column chunk size; or using `transport_ad_mode=full`. The planned command avoids these by fixing the XLA manual-reverse route, one seed, `fd_mode=ad-only`, TensorFlow allocator telemetry, `transport_ad_mode=stabilized`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`, and `particle_chunk_size=512`.

The `3334` chunk size should create `ceil(10000 / 3334) = 3` chunks per axis, or `9` block pairs, with effective padded size `10002` per axis. This makes it a useful candidate against `2048`, which uses `5 x 5 = 25` block pairs but smaller blocks.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Measure `3334 x 3334` warm-call timing for the existing N10000 manual-reverse XLA route. |
| Comparator | Existing `2048 x 2048` XLA result: warm call `2.3217804890009575` seconds, compile plus first call `421.3336761600076` seconds, allocator peak `0.31909871101379395` GiB. |
| Primary criterion | The run writes a JSON result with `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostics | CPU placement, FD launched, more than one seed, diagnostic autodiff route, `transport_ad_mode=full`, non-XLA compiler mode, changed Sinkhorn settings, changed particle chunk size, missing timing metadata, or timeout. |
| Explanatory only | Compile plus first call, objective/gradient differences, allocator peak, and memory sidecar samples. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Fixed Settings

- `time_steps=3`
- `num_particles=10000`
- `batch_seeds=81120`
- `seed_microbatch_size=1`
- `ad_evaluation_mode=manual-reverse`
- `manual_reverse_compiler=xla` by default
- `fd_mode=ad-only`
- `transport_plan_mode=streaming`
- `transport_gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`
- `transport_ad_mode=stabilized`
- `sinkhorn_iterations=10`
- `sinkhorn_epsilon=1.0`
- `row_chunk_size=3334`
- `col_chunk_size=3334`
- `particle_chunk_size=512`
- `dtype=float32`
- `tf32_mode=enabled`

## Command

Run with trusted GPU permissions.

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk3334 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 3334 --col-chunk-size 3334 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.json
```

## Stop Conditions

- Stop after this single `3334` run completes.
- Stop if the run times out, reports CPU placement, or reports non-XLA compilation.
- Do not run FD.
- Do not run five seeds.
- Do not tune `particle_chunk_size`, Sinkhorn settings, or other chunk sizes inside this diagnostic.
