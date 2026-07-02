# Streaming Manual VJP Phase 7 Result: GPU Memory Ladder

date: 2026-06-23
phase: S7-GPU-MEMORY-LADDER
status: BLOCKED_N100_METADATA_CONTRACT

## Objective

Run a trusted GPU memory and feasibility ladder for the new opt-in streaming
blockwise manual VJP route, advancing to `N=10000` only if earlier rungs pass
their exact JSON metadata validation contract.

## Decision

S7 is blocked at the N100 smoke rung.

The N100 GPU computation exited 0, produced finite objective/gradient/MCSE
values, used GPU output tensors, and recorded the new blockwise route:

```text
manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys
```

However, the reviewed S7 subplan required exact key-based JSON validation
before advancing to the next rung.  The N100 JSON artifact is missing required
metadata keys:

- top-level `status`;
- top-level `primary_pass`;
- top-level `batch_seeds`;
- `transport.dense_transport_matrix_materialized`.

Because missing keys are a hard rung failure under the reviewed S7 subplan,
the ladder did not advance to N1000, N2500, N5000, or N10000.  S8/P82 FD
handoff remains blocked.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Failed before N10000: N100 artifact did not satisfy exact JSON validation keys. |
| N100 rung | Compute passed but artifact validation failed. |
| N1000+ rungs | Not launched. |
| Veto diagnostics | Triggered: missing required JSON metadata keys. |
| Next justified action | Stop S7, review this blocker, and require a new reviewed remediation subplan before rerunning the ladder. |
| What is not concluded | No N10000 feasibility, no GPU memory success beyond N100 smoke compute, no P82 FD agreement, no HMC/default readiness, no production readiness. |

## Checks Before GPU Work

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
```

Output:

```text
13 passed, 2 warnings in 7.24s
```

Passed:

```text
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py
```

Passed:

```text
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-subplan-2026-06-23.md
```

Harness plumbing:

- Added the new blockwise route to `--transport-gradient-mode` choices in
  `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`.
- Added protocol tests confirming the regression harness CLI accepts the new
  route and the streaming value core forwards the exact new route string.
- Defaults were not changed; the harness default remains `raw`.

## Trusted GPU Preflight

Trusted `nvidia-smi` passed:

- GPU: NVIDIA GeForce RTX 4080 SUPER;
- driver/CUDA reported by `nvidia-smi`: Driver `591.86`, CUDA `13.1`;
- memory at preflight: `2608MiB / 16376MiB`;
- no running GPU processes listed.

Trusted TensorFlow GPU probe passed:

- TensorFlow version: `2.19.1`;
- physical devices included `CPU:0` and `GPU:0`;
- GPU list contained `PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')`.

## N100 Artifact Summary

JSON:

```text
docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n100-gpu-tf32-2026-06-23.json
```

Command launched under trusted/elevated GPU permissions:

```text
MPLCONFIGDIR=/tmp timeout 1200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py --device-scope visible --expect-device-kind gpu --device /GPU:0 --time-steps 3 --num-particles 100 --batch-seeds 81120,81121,81122,81123,81124 --seed-microbatch-size 1 --ad-evaluation-mode reverse-gradient --fd-mode ad-only --theta 0.02,-0.01,0.01 --phase-label "S7 blockwise streaming actual-gradient N100 GPU TF32" --transport-policy active-all --transport-plan-mode streaming --transport-gradient-mode manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys --transport-ad-mode stabilized --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 --row-chunk-size 128 --col-chunk-size 128 --particle-chunk-size 128 --dtype float32 --tf32-mode enabled --basis-set raw --output docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n100-gpu-tf32-2026-06-23.json
```

Observed compute values:

| Quantity | Value |
|---|---|
| Elapsed seconds | `33.73789733599915` |
| Objective | `-125.5501708984375` |
| `log_kappa_scale` gradient | `-181.25650024414062` |
| `log_kappa_scale` MCSE | `15.015740394592285` |
| `log_nu_scale` gradient | `78.58741760253906` |
| `log_nu_scale` MCSE | `3.5778865814208984` |
| `log_obs_noise_scale` gradient | `47.45368194580078` |
| `log_obs_noise_scale` MCSE | `0.5832633376121521` |

Metadata that passed validation:

- `device_scope="visible"`;
- `expect_device_kind="gpu"`;
- `output_devices` contained only GPU entries;
- `shape.num_particles=100`;
- `shape.batch_size=5`;
- `shape.seed_microbatch_size=1`;
- `shape.seed_microbatch_count=5`;
- `transport.transport_plan_mode="streaming"`;
- `transport.gradient_mode="manual_streaming_blockwise_vjp_finite_sinkhorn_stopped_scale_keys"`;
- `transport.transport_ad_mode="stabilized"`;
- `regression_fd.fd_mode="ad-only"`;
- `regression_fd.ad_evaluation_mode="reverse-gradient"`;
- objective, gradient values, and MCSE values were finite.

Missing required metadata:

- top-level `status`;
- top-level `primary_pass`;
- top-level `batch_seeds`;
- `transport.dense_transport_matrix_materialized`.

## Absent Artifacts

The ladder stopped before launching larger rungs.  These artifacts are absent
by design:

- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n2500-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n5000-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-actual-gradient-n10000-progress-2026-06-23.json`

## Decision Table

| Field | Status |
|---|---|
| Decision | S7 blocked at N100 metadata validation. |
| Primary criterion status | Failed: N10000 was not reached, and N100 JSON lacked required validation keys. |
| Veto diagnostic status | Triggered: missing exact JSON metadata keys. |
| Main uncertainty | The N100 compute path looks finite on GPU, but the governed ladder cannot say whether N1000+ or N10000 would pass until the harness emits the required metadata and a new reviewed remediation reruns the ladder. |
| Next justified action | New reviewed remediation subplan to add exact metadata keys to the harness, rerun CPU-hidden harness checks, then rerun the trusted GPU ladder from N100. |
| What is not concluded | No N10000 feasibility, no P82 FD agreement, no HMC/default readiness, no production readiness, no scientific superiority. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `f4853625732f31870f7ff3fc9064b97c742c1bef` |
| Commands | Listed in this result. |
| Environment | Local repo shell; CPU-hidden checks used `CUDA_VISIBLE_DEVICES=-1`; GPU commands used trusted/elevated execution. |
| CPU/GPU status | CPU-hidden prechecks passed; trusted GPU preflight passed; N100 output tensors were on GPU. |
| Dtype | `float32`, TF32 enabled. |
| Seeds | Requested five seeds: `81120,81121,81122,81123,81124`; artifact records seed microbatch groups but lacks top-level `batch_seeds`. |
| Wall time | N100 rung reported `33.73789733599915` seconds. |
| Plan file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-subplan-2026-06-23.md` |
| Result file | `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase7-gpu-memory-ladder-result-2026-06-23.md` |
| Touched files | `docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py`; `tests/highdim/test_p82_regression_fd_harness_protocol.py`; S7/S6/ledger plan artifacts. |

## Non-Claims

This result does not claim FD agreement, P82 validation, posterior correctness,
HMC/default readiness, production readiness, scientific superiority, or
Zhao-Cui comparator readiness.  It does not prove the blockwise manual VJP
route cannot scale; it blocks this governed ladder because the N100 artifact
did not satisfy the predeclared metadata contract.

## Handoff

S8/P82 FD must not run because the required valid S7 N10000 actual-gradient
artifact does not exist.  Any further attempt must start from a new reviewed
remediation subplan that adds the exact metadata keys to the harness and reruns
the S7 ladder from the N100 rung.
