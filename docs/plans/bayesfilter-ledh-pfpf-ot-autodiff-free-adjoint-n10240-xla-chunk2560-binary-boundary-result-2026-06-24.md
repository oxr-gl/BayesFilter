# N10240 XLA Chunk2560 Binary-Boundary Timing Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | The binary-friendly exact-tiling shape `N=10240`, `2560 x 2560` does not beat `N=10000`, `2500 x 2500`; keep `2500 x 2500` as the current best tested shape for N10000-style runs. |
| Primary criterion status | PASS: JSON result reports `status=pass`, `primary_pass=true`, `compiler.mode=xla`, `jit_compile=true`, one warm-call timing, GPU output devices, finite objective, finite score, and allocator telemetry. |
| Veto diagnostic status | PASS: no FD run, one seed only, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, fixed Sinkhorn settings, fixed `particle_chunk_size=512`, and allocator peak remained below 1 GiB. |
| Raw-time status | FAIL to beat comparator: `N=10240/chunk=2560` warm call is `1.7404677319864277` seconds versus `1.5704608989763074` seconds for `N=10000/chunk=2500`. |
| Normalized-throughput status | FAIL to beat comparator: seconds per effective pair slot is about `1.659839374529293e-08` versus `1.5704608989763073e-08`. |
| Main uncertainty | One seed and one warm call only; this is a timing diagnostic, not a correctness or FD agreement result. |
| Next justified action | Do not switch to `N=10240/chunk=2560` for timing reasons. If N must remain exactly 10000, `2500` remains the best tested row/column chunk size. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Comparison

| Case | Block pairs | Effective padded pair slots | Compile + first call (s) | Warm call (s) | Pair slots / second | Seconds / pair slot | TF allocator peak (GiB) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `N=10000`, chunk `2500` | 16 | 100000000 | 340.6117727160163 | 1.5704608989763074 | 63675574.51776368 | 1.5704608989763073e-08 | 0.3162567615509033 |
| `N=10240`, chunk `2560` | 16 | 104857600 | 352.64430643300875 | 1.7404677319864277 | 60246793.47563893 | 1.659839374529293e-08 | 0.3317444324493408 |

`N=10240/chunk=2560` is about `10.8%` slower in raw warm-call time and about `5.7%` slower after normalizing by effective pair slots. Its effective pair-slot count is `4.8576%` larger, so the slowdown is not just extra work; normalized throughput is also worse.

## Interpretation

An exact binary-friendly boundary does not appear to help this compiled route. Both cases use `4 x 4 = 16` block pairs and exact tiling. The `10240/2560` case has powers-of-two-friendly sizes, but the measured kernel behavior is slightly worse than `10000/2500` both absolutely and per pair slot.

The current evidence favors the empirical `2500 x 2500` shape over a binary-boundary heuristic.

## Run Manifest

| Field | Value |
|---|---|
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-binary-boundary-plan-2026-06-24.md` |
| Result JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-result-2026-06-24.json` |
| Memory sidecar | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-memory-samples-2026-06-24.json` |
| Comparator JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2500-result-2026-06-24.json` |
| Git commit recorded by benchmark | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Host | `DESKTOP-RF1Q5IJ` |
| TensorFlow | `2.19.1` |
| Device | `/GPU:0`, NVIDIA GeForce RTX 4080 SUPER |
| Seeds | `81120` |
| Shape | `N=10240`, `T=3`, `state_dim=18`, `obs_dim=9`, `parameter_dim=3` |
| Precision | `float32`, TF32 enabled |
| Transport | streaming, `manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `sinkhorn_iterations=10`, `sinkhorn_epsilon=1.0` |

## Command Actually Run

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10240 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --manual-reverse-warmups 0 --manual-reverse-repeats 1 --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10240 single-seed manual reverse XLA chunk2560 binary-boundary timing diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 2560 --col-chunk-size 2560 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10240-xla-chunk2560-result-2026-06-24.json
```

## Post-Run Red-Team Note

The strongest alternative explanation is timing noise from one warm call. The observed gap is moderate, so a repeated-warm timing run could refine the exact percentage. Still, this single bounded probe gives no evidence that binary-friendly exact boundaries beat the empirical `2500` shape.
