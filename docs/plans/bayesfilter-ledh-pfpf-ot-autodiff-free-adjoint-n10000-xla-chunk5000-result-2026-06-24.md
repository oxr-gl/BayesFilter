# N10000 XLA Chunk5000 Timing Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | `5000 x 5000` is valid but much slower than `2500 x 2500`; keep `2500 x 2500` as the current best tested N10000 row/column chunk setting. |
| Primary criterion status | PASS: JSON result reports `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostic status | PASS: no FD run, one seed only, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, fixed Sinkhorn settings, fixed `particle_chunk_size=512`, and allocator peak remained below 1 GiB. |
| Main uncertainty | One seed and one warm call only; this is a timing diagnostic, not a correctness or FD agreement result. |
| Next justified action | Do not promote `5000`; use `2500` for subsequent bounded N10000 timing or FD-consistency work unless a separate repeated-warm ladder reopens chunk tuning. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Comparison

| Row/col chunk | Block pairs | Effective padded pair slots | Compile + first call (s) | Warm call (s) | Warm speedup vs 2500 | TF allocator peak (GiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 2048 | 25 | 104857600 | 421.3336761600076 | 2.3217804890009575 | 0.676x | 0.31909871101379395 |
| 2500 | 16 | 100000000 | 340.6117727160163 | 1.5704608989763074 | 1.000x | 0.3162567615509033 |
| 3334 | 9 | 100040004 | 426.22349167799985 | 2.3859367769910023 | 0.658x | 0.384676456451416 |
| 5000 | 4 | 100000000 | 374.984015738999 | 10.04070115898503 | 0.156x | 0.5389814376831055 |

`5000 x 5000` is about `6.39x` slower than `2500 x 2500` on the measured warm call, despite having the same exact no-padding effective pair-slot count. It also uses a higher TensorFlow allocator peak, about `0.539` GiB versus `0.316` GiB.

## Interpretation

This result rules out a simple "fewer block pairs is always better" story for the current implementation and GPU. `5000` reduces the loop to only `2 x 2 = 4` block pairs, but the per-block kernel shape is much larger and performs poorly here. The current ladder indicates that `2500 x 2500` is a better balance: exact no-padding coverage, moderate block size, and substantially faster compiled warm-call timing.

## Run Manifest

| Field | Value |
|---|---|
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-plan-2026-06-24.md` |
| Result JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-result-2026-06-24.json` |
| Memory sidecar | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-memory-samples-2026-06-24.json` |
| Comparator JSONs | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json`, `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.json`, `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.json` |
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
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk5000 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 5000 --col-chunk-size 5000 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk5000-result-2026-06-24.json
```

## Post-Run Red-Team Note

The strongest alternative explanation is timing noise from a single warm call, but the gap is too large to explain away casually: `5000` is over six times slower than `2500` in this diagnostic. A repeated-warm run could refine the exact ratio, but it would not justify promoting `5000` from this result.
