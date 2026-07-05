# N10000 XLA Chunk Ladder Plan

date: 2026-06-24
status: READY_FOR_RUNS

## Question

For the compiled single-seed `N=10000`, `T=3` manual-reverse LEDH-PFPF-OT route, do larger streaming transport row/column chunks improve warm-call timing relative to the existing `512 x 512` baseline?

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Measure warm-call timing for `row_chunk_size=col_chunk_size=1024` and `2048`, compared with the existing `512` baseline. |
| Comparator | Existing `512 x 512` XLA result: warm call `21.04620357499516` seconds, compile plus first call `346.65965834099916` seconds. |
| Primary criterion | Each candidate writes a JSON result with `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostics | CPU placement, FD launched, more than one seed, diagnostic autodiff route, `transport_ad_mode=full`, non-XLA compiler mode, changed Sinkhorn settings, changed particle chunk size, or missing timing metadata. |
| Explanatory only | Compile plus first call, objective/gradient differences, allocator peak, and `nvidia-smi` reservation if observed. |
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
- `particle_chunk_size=512`
- `dtype=float32`
- `tf32_mode=enabled`

## Commands

Run with trusted GPU permissions.

### 1024 x 1024

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk1024 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 1024 --col-chunk-size 1024 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk1024-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk1024-result-2026-06-24.json
```

### 2048 x 2048

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk2048 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2048 --col-chunk-size 2048 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json
```

## Stop Conditions

- Stop after the two candidate runs complete or the first candidate reveals a blocker that makes the second unsafe.
- Do not run FD.
- Do not run five seeds.
- Do not tune particle chunk size or Sinkhorn settings inside this diagnostic.
