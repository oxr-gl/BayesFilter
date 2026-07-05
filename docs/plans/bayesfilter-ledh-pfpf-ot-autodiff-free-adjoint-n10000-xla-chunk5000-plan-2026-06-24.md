# N10000 XLA Chunk5000 Timing Plan

date: 2026-06-24
status: READY_FOR_RUN

## Question

For the compiled single-seed `N=10000`, `T=3` manual-reverse LEDH-PFPF-OT route, does `row_chunk_size=col_chunk_size=5000` improve warm-call timing relative to the current best tested `2500 x 2500` timing result?

## Skeptical Audit

This is a timing and allocator diagnostic only. It must not be treated as an FD agreement check, gradient-correctness result, HMC-readiness result, or production-readiness result.

The main plan risks are: assuming fewer block pairs must be faster; comparing against a stale non-XLA baseline; mistaking TensorFlow allocator reservation for actual peak; accidentally running FD or multiple seeds; changing Sinkhorn or particle chunk settings while testing row/column chunk size; or using `transport_ad_mode=full`. The planned command avoids these by fixing the XLA manual-reverse route, one seed, `fd_mode=ad-only`, TensorFlow allocator telemetry, `transport_ad_mode=stabilized`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0`, and `particle_chunk_size=512`.

The `5000` chunk size creates `10000 / 5000 = 2` chunks per axis, or `4` block pairs, with exact no-padding coverage. It has the same effective pair-slot count as `2500` (`100000000`), so this run isolates the tradeoff between fewer/larger blocks and more/moderate blocks better than the previous padding probes.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Measure `5000 x 5000` warm-call timing for the existing N10000 manual-reverse XLA route. |
| Comparator | Current best tested `2500 x 2500` XLA result: warm call `1.5704608989763074` seconds, compile plus first call `340.6117727160163` seconds, allocator peak `0.3162567615509033` GiB. |
| Primary criterion | The run writes a JSON result with `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostics | CPU placement, FD launched, more than one seed, diagnostic autodiff route, `transport_ad_mode=full`, non-XLA compiler mode, changed Sinkhorn settings, changed particle chunk size, missing timing metadata, timeout, or allocator peak suggesting this shape is unsafe for the route. |
| Explanatory only | Compile plus first call, objective/gradient differences, allocator peak, block-count arithmetic, and memory sidecar samples. |
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
- `row_chunk_size=5000`
- `col_chunk_size=5000`
- `particle_chunk_size=512`
- `dtype=float32`
- `tf32_mode=enabled`

## Command

Run with trusted GPU permissions.

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk5000 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 5000 --col-chunk-size 5000 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-result-2026-06-24.json
```

## Stop Conditions

- Stop after this single `5000` run completes.
- Stop if the run times out, reports CPU placement, reports non-XLA compilation, or shows unsafe allocator pressure.
- Do not run FD.
- Do not run five seeds.
- Do not tune `particle_chunk_size`, Sinkhorn settings, or other chunk sizes inside this diagnostic.
