# N10000 XLA Timing Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | XLA compilation materially fixes the single-seed N10000 manual-reverse timing problem. |
| Primary criterion status | PASS: result JSON has `compiler.mode=xla`, `jit_compile=true`, GPU output devices, finite objective, finite manual score, allocator telemetry, and one warm-call timing. |
| Veto diagnostic status | PASS: one seed only, no FD, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, TF32 enabled, GPU placement confirmed. |
| Main uncertainty | Compile latency is large, and this is still single-seed only. |
| Next justified action | Use compiled warm-call timing for N10000 feasibility estimates; if needed, run five seeds as five compiled warm calls after a compile/warm cache strategy is explicit. |
| Not concluded | FD agreement, five-seed N10000 feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Result

Single-seed N10000 manual-reverse XLA timing completed successfully.

- Shape: `T=3`, `N=10000`, one seed.
- Route: `manual-reverse`, streaming transport, `transport_ad_mode=stabilized`.
- Precision/device: `float32`, TF32 enabled, `/GPU:0`.
- Compiler: `tf.function(jit_compile=True)`.
- Compile plus first call: `346.65965834099916` seconds.
- Warm-call timing: `21.04620357499516` seconds.
- Total run elapsed including compile, one warm call, JSON, and telemetry: `368.9544040530018` seconds.

The previous non-XLA single-seed N10000 diagnostic took `1657.6321100650093` seconds. The comparable steady-state number after XLA compilation is the warm call, about `21.05` seconds. This is roughly a `78.8x` reduction relative to the earlier total non-XLA run time, with the caveat that compile time is still about `5.78` minutes for this shape.

## Memory Result

- TensorFlow allocator peak: `303438080` bytes, about `0.283` GiB.
- TensorFlow allocator final current memory: `745984` bytes.

This reinforces the earlier conclusion that the N10000 problem was not live TensorFlow allocator capacity. It was execution-path/compilation/runtime structure.

## Artifacts

- Plan: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-plan-2026-06-24.md`
- Result JSON: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-result-2026-06-24.json`
- Memory sidecar: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-memory-samples-2026-06-24.json`

Command:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-compiler xla --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-result-2026-06-24.json
```

## Post-run Red-team Note

The strongest alternative explanation is that the single warm call benefits from compile caching and does not include compile cost. That is intentional: the question was whether the actual repeated manual score computation is intrinsically too slow once compiled. It is not, based on this single-seed diagnostic. Any production or five-seed plan still needs an explicit compile-cache/warm-call policy so compile latency is not confused with per-evaluation cost.
