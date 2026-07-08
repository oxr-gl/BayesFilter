# N10000 XLA Chunk Ladder Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | Larger row/column transport chunks materially improve compiled N10000 warm-call timing; `2048 x 2048` is fastest among tested values. |
| Primary criterion status | PASS: both `1024` and `2048` wrote JSON results with `compiler.mode=xla`, `jit_compile=true`, GPU output devices, one warm-call timing, finite objective, finite score, and allocator telemetry. |
| Veto diagnostic status | PASS: no FD, one seed only, manual-reverse route, `transport_ad_mode=stabilized`, no `transport_ad_mode=full`, fixed Sinkhorn settings, fixed `particle_chunk_size=512`. |
| Main uncertainty | Only one seed and one warm call per chunk size; compile time worsens for `2048`. |
| Next justified action | Use `2048 x 2048` as the current best N10000 compiled warm-call transport chunk setting, unless compile latency dominates the intended workflow. |
| Not concluded | FD agreement, five-seed feasibility, HMC readiness, posterior correctness, scientific validity, or production readiness. |

## Timing Comparison

| Row/col chunk | Compile + first call (s) | Warm call (s) | Speedup vs 512 warm call | TF allocator peak (GiB) |
|---:|---:|---:|---:|---:|
| 512 | 346.65965834099916 | 21.04620357499516 | 1.000x | 0.28259873390197754 |
| 1024 | 340.4686781359924 | 7.40276274298958 | 2.843x | 0.28259944915771484 |
| 2048 | 421.3336761600076 | 2.3217804890009575 | 9.065x | 0.31909871101379395 |

The `2048 x 2048` chunk setting gives the best measured steady-state time: about `2.32` seconds for one N10000 single-seed manual-reverse XLA warm call. Its compile plus first call is slower than the smaller chunks, about `421.33` seconds.

## Artifacts

- Plan: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk-ladder-plan-2026-06-24.md`
- Baseline 512 result: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-timing-result-2026-06-24.json`
- 1024 result: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk1024-result-2026-06-24.json`
- 1024 memory sidecar: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk1024-memory-samples-2026-06-24.json`
- 2048 result: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-result-2026-06-24.json`
- 2048 memory sidecar: `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-xla-chunk2048-memory-samples-2026-06-24.json`

## Interpretation

The result confirms the expected tradeoff. Larger row/column chunks reduce the number of streaming transport block pairs and substantially improve warm-call timing. For this problem and GPU, `2048` still fits comfortably in TensorFlow allocator telemetry, with peak about `0.319` GiB.

The cost is XLA compile time. If the workflow recompiles often, `2048` may feel slower wall-clock for one-off calls. If the compiled function is reused, `2048` is currently the better setting.
