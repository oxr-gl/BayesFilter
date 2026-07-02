# N10000 XLA Chunk2500 Timing Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | `2500 x 2500` is the fastest tested row/column chunk setting so far for the compiled single-seed N10000 manual-reverse timing diagnostic. |
| Primary criterion status | PASS: JSON result reports `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostic status | PASS: no FD run, one seed only, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, fixed Sinkhorn settings, and fixed `particle_chunk_size=512`. |
| Main uncertainty | One seed and one warm call only; this is a timing diagnostic, not a correctness or FD agreement result. |
| Next justified action | Use `2500 x 2500` as the current best tested N10000 row/column chunk setting for warm-call timing, subject to later repeated-warm or five-seed validation if this setting becomes part of a larger run. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Comparison

| Row/col chunk | Block pairs | Effective padded pair slots | Compile + first call (s) | Warm call (s) | Warm speedup vs 2048 | TF allocator peak (GiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 2048 | 25 | 104857600 | 421.3336761600076 | 2.3217804890009575 | 1.000x | 0.31909871101379395 |
| 2500 | 16 | 100000000 | 340.6117727160163 | 1.5704608989763074 | 1.478x | 0.3162567615509033 |
| 3334 | 9 | 100040004 | 426.22349167799985 | 2.3859367769910023 | 0.973x | 0.384676456451416 |

`2500 x 2500` improves the measured warm call by about `1.48x` versus `2048 x 2048`, and about `1.52x` versus `3334 x 3334`. It also compiled faster than both larger-shape candidates in this run.

## Padding Interpretation

Less padding appears helpful, but the result is not purely a padding story.

`2500` has exact tiling: `10000 / 2500 = 4`, so it uses `4 x 4 = 16` block pairs and exactly `100000000` effective pair slots. This removes the modest padding overhead present in `2048`, which uses `25` block pairs and `104857600` effective pair slots.

However, `3334` has almost the same effective pair-slot count as `2500` (`100040004` versus `100000000`) and still ran slower. That means block shape, kernel occupancy, memory behavior, and XLA code generation are also important. The current evidence says that `2500` is the better tested shape for this route, not that no-padding alone explains the improvement.

## Run Manifest

| Field | Value |
|---|---|
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-plan-2026-06-24.md` |
| Result JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.json` |
| Memory sidecar | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-memory-samples-2026-06-24.json` |
| Comparator JSONs | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json`, `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk3334-result-2026-06-24.json` |
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
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed manual reverse XLA chunk2500 timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2500 --col-chunk-size 2500 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.json
```

## Post-Run Red-Team Note

The strongest alternative explanation is timing noise from a single warm call. That said, the gap from `2500` to `2048` is large enough in this diagnostic to justify treating `2500` as the current best tested chunk size for subsequent bounded checks. A later repeated-warm timing run would be the right confirmation before making broader runtime claims.
