# N10000 Memory Diagnostic Result

date: 2026-06-24
status: COMPLETE

## Decision Table

| Field | Result |
|---|---|
| Decision | Single-seed N10000 manual-reverse route completed; the observed TensorFlow allocator peak does not support a live-memory-capacity blocker diagnosis. |
| Primary criterion status | PASS: final JSON and memory sidecar were written with TensorFlow GPU allocator samples. |
| Veto diagnostic status | PASS: one seed only, GPU placement, `manual-reverse`, `streaming`, `transport_ad_mode=stabilized`, no FD sweep, no Zhao-Cui comparator, no `transport_ad_mode=full`. |
| Main uncertainty | This does not prove five-seed N10000 feasibility; runtime scaling remains the visible blocker. |
| Next justified action | Treat P9's N10000 issue as runtime/scaling unless a later allocator-telemetry run contradicts this. |
| Not concluded | FD agreement, posterior correctness, HMC readiness, five-seed feasibility, scientific validity, or production readiness. |

## Result Summary

The single N10000 seed microbatch completed on GPU.

- Wall time: `1657.6321100650093` seconds, about `27.6` minutes.
- TensorFlow allocator final current memory: `742656` bytes, about `0.00069` GiB.
- TensorFlow allocator peak memory: `3529800448` bytes, about `3.287` GiB.
- Maximum sampled current allocator memory during the run: `397079296` bytes, about `0.370` GiB.
- Final status: `pass`.
- Primary pass: `true`.

This supports the user's concern: `nvidia-smi`-style GPU memory readings are not the actual live TensorFlow allocator peak for this route. TensorFlow can reserve most of the GPU memory while reporting a much smaller in-process allocator peak through `tf.config.experimental.get_memory_info("GPU:0")`.

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `97ad05d40676f3fd15a2a2b4d45034ebb657ed97` |
| Environment | `/home/chakwong/anaconda3/envs/tf-gpu/bin/python`, TensorFlow `2.19.1` |
| Device | `/GPU:0`; physical and logical GPU detected in result JSON |
| CPU/GPU status | GPU run with visible device scope |
| Seeds | `[81120]` |
| Particle count | `10000` |
| Time steps | `3` |
| Route | `manual-reverse`, streaming plan, `transport_ad_mode=stabilized`, `manual_streaming_finite_sinkhorn_stopped_scale_keys` |
| Chunks | row `512`, column `512`, particle `512` |
| Precision | `float32`, TF32 enabled |
| Plan | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-memory-diagnostic-plan-2026-06-24.md` |
| Result JSON | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-diagnostic-2026-06-24.json` |
| Memory sidecar | `docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-samples-2026-06-24.json` |

Command:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed TF allocator memory diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-diagnostic-2026-06-24.json
```

## Post-run Red-team Note

The strongest alternative explanation is that this single-seed ad-only diagnostic avoids a memory path that would appear in a five-seed or FD run. That does not change the narrow result: for the exact one-seed manual-reverse N10000 route measured here, live TensorFlow allocator peak was about `3.287` GiB. A future five-seed run should preserve the same allocator telemetry before making a memory-capacity claim.
