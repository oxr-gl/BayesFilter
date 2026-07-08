# N10000 XLA Chunk3334 Timing Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | `3334 x 3334` is a valid compiled GPU timing run, but it does not improve over the current `2048 x 2048` timing baseline. |
| Primary criterion status | PASS: JSON result reports `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostic status | PASS: no FD run, one seed only, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, fixed Sinkhorn settings, and fixed `particle_chunk_size=512`. |
| Main uncertainty | One seed and one warm call only; timing noise and XLA code generation effects may move small differences. |
| Next justified action | Keep `2048 x 2048` as the current best tested N10000 row/column chunk setting unless a later bounded ladder tests `2500` or `5000`. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Comparison

| Row/col chunk | Block pairs | Effective padded pair slots | Compile + first call (s) | Warm call (s) | TF allocator peak (GiB) |
|---:|---:|---:|---:|---:|---:|
| 2048 | 25 | 104857600 | 421.3336761600076 | 2.3217804890009575 | 0.31909871101379395 |
| 3334 | 9 | 100040004 | 426.22349167799985 | 2.3859367769910023 | 0.384676456451416 |

Relative to `2048 x 2048`, `3334 x 3334` was about `2.8%` slower on the measured warm call and about `1.2%` slower on compile plus first call. Its TensorFlow allocator peak was also higher, about `0.385` GiB versus `0.319` GiB.

The result is plausible even though `3334` uses only `3 x 3 = 9` block pairs. Its larger per-block shape changes the compiled kernel/memory behavior, and the small reduction in padded pair slots did not translate into faster observed warm-call time.

## Run Manifest

| Field | Value |
|---|---|
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-plan-2026-06-24.md` |
| Result JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.json` |
| Memory sidecar | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-memory-samples-2026-06-24.json` |
| Comparator JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json` |
| Git commit recorded by benchmark | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Host | `DESKTOP-RF1Q5IJ` |
| TensorFlow | `2.19.1` |
| Device | `/GPU:0`, NVIDIA GeForce RTX 4080 SUPER |
| Seeds | `81120` |
| Shape | `N=10000`, `T=3`, `state_dim=18`, `obs_dim=9`, `parameter_dim=3` |
| Precision | `float32`, TF32 enabled |
| Transport | streaming, `manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0` |

## Command Actually Run

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk3334 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 3334 --col-chunk-size 3334 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.json
```

## Post-Run Red-Team Note

The strongest alternative explanation is timing noise from one warm call or XLA generating a less favorable kernel for this exact chunk shape. A repeated warm-call run could move a small `2.8%` gap. However, the current result is enough to avoid replacing `2048` with `3334` as the best tested setting.
