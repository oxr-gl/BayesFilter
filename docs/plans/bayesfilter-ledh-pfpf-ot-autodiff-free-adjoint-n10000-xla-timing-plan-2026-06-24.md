# N10000 XLA Timing Plan

date: 2026-06-24
status: READY_FOR_SINGLE_RUN

## Question

For the exact single-seed `N=10000`, `T=3` manual-reverse LEDH-PFPF-OT route that previously took about `27.6` minutes without full XLA compilation, what is the compiled warm-call timing when the seed-microbatch manual value/score is run with `tf.function(jit_compile=True)`?

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Does XLA compilation materially reduce single-seed N10000 manual-reverse timing for the same problem route? |
| Comparator | Previous single-seed non-XLA diagnostic: `1657.6321100650093` seconds elapsed, TensorFlow allocator peak about `3.287` GiB. |
| Primary criterion | The run writes a JSON result with `compiler.mode=xla`, `jit_compile=true`, at least one warm-call timing, GPU output devices, finite objective, and finite manual score. |
| Veto diagnostics | CPU placement, FD launched, more than one seed, diagnostic autodiff route, `transport_ad_mode=full`, non-XLA compiler mode, missing timing metadata, or missing allocator telemetry. |
| Explanatory only | Compile plus first call, objective value, gradient value, allocator peak, `nvidia-smi` reservation if observed. |
| Not concluded | FD agreement, five-seed N10000 feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Command

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-compiler xla --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-result-2026-06-24.json
```

## Stop Conditions

- Stop after this one single-seed N10000 timing run completes or times out.
- Do not run FD.
- Do not run five seeds.
- Do not tune chunks or Sinkhorn settings inside this diagnostic.
- If the result JSON is absent but the memory sidecar exists, interpret only timeout and allocator telemetry.
