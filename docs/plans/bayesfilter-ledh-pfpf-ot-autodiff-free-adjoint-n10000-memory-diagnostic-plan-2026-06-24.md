# N10000 Memory Diagnostic Plan

date: 2026-06-24
status: READY_FOR_SINGLE_RUN

## Question

For the exact LEDH-PFPF-OT `manual-reverse` route that blocked at P9 N10000,
what does TensorFlow report as in-process GPU allocator `current` and `peak`
memory for one N10000 seed microbatch?

## Scope

Run exactly one N10000 seed, not the full five-seed P9 ladder.  P9 already used
`seed-microbatch-size=1`, so this diagnostic measures the same per-seed
microbatch size while avoiding the full five-seed runtime.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | What are TensorFlow allocator `current` and `peak` memory readings for one N10000 seed microbatch on the audited manual-reverse route? |
| Comparator | P9 `nvidia-smi` reservation snapshots are explanatory only, not the memory oracle. |
| Primary criterion | The run writes a sidecar memory sampler JSON with at least one TensorFlow `get_memory_info("GPU:0")` sample and either writes a final benchmark JSON or records timeout/blocker status with the sidecar present. |
| Veto diagnostics | Wrong route, FD launched, more than one seed, CPU placement, missing memory sidecar, `transport_ad_mode=full`, diagnostic autodiff mode, or treating this single-seed diagnostic as five-seed feasibility. |
| Explanatory only | `nvidia-smi`, runtime, objective/gradient if the run completes. |
| Not concluded | Five-seed N10000 feasibility, FD agreement, posterior correctness, HMC readiness, production default, or scientific validity. |

## Command

Run with trusted GPU permissions:

```bash
MPLCONFIGDIR=/tmp /usr/bin/timeout 3600 /home/chakwong/anaconda3/envs/tf-gpu/bin/python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 10000 --batch-seeds 81120 --seed-microbatch-size 1 --ad-evaluation-mode manual-reverse --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "N10000 single-seed TF allocator memory diagnostic" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 --dtype float32 --tf32-mode enabled --basis-set raw --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-samples-2026-06-24.json --memory-sample-interval-seconds 30 --output docs/plans/bayesfilter-ledh-pfpf-ot-autodiff-free-adjoint-n10000-single-seed-memory-diagnostic-2026-06-24.json
```

## Stop Conditions

- Stop after this single run completes or times out.
- Do not run FD.
- Do not run five seeds.
- Do not tune chunks or timeout inside this diagnostic.
- If the memory sidecar is missing, write a blocker result instead of
  interpreting memory.
