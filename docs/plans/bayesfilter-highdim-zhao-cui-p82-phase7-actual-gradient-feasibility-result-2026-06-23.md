# P82 Phase 7 Result: Actual-Gradient Feasibility Ladder

status: BLOCKED_N10000_GPU_RESOURCE_EXHAUSTED
date: 2026-06-23
phase: P7-ACTUAL-GRADIENT-FEASIBILITY

## Question

Can the reviewed manual streaming transport-gradient route produce finite
five-seed SIR d18 actual gradients at N10000 under GPU/TF32 without using the
known-bad full-AD route?

## Decision

No, not under the reviewed P7 command and chunk configuration.

The N1000 feasibility rung passed with five seeds, GPU placement, finite
objective, finite gradient components, and finite seed MCSE.  The N10000 rung
then failed before writing output/progress artifacts with TensorFlow
`ResourceExhaustedError: failed to allocate memory` on `GPU:0`.

P8 is blocked.  No governed N1000 regression-FD comparison was launched.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Failed at N10000: the N10000 ad-only run did not exit 0 and did not write the required JSON artifact. |
| N1000 rung | Passed: five seeds, `num_particles=1000`, GPU-visible output, finite objective, finite gradient components, finite seed MCSE, manual streaming route metadata. |
| N10000 rung | Blocked: GPU `ResourceExhaustedError` during the first N10000 seed microbatch; no N10000 JSON or progress JSON exists. |
| Veto diagnostics | Triggered: OOM / missing N10000 artifact. |
| Next justified action | Stop P82 before P8 and write closeout.  Any retry requires a new reviewed feasibility/remediation subplan. |

## N1000 Artifact Summary

JSON:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n1000-gpu-tf32-2026-06-23.json
```

Observed values:

| Quantity | Value |
|---|---|
| Elapsed seconds | `69.97849530700114` |
| Objective | `-125.59538269042969` |
| `log_kappa_scale` gradient | `-157.03306579589844` |
| `log_kappa_scale` MCSE | `6.863861560821533` |
| `log_nu_scale` gradient | `70.12858581542969` |
| `log_nu_scale` MCSE | `1.8720670938491821` |
| `log_obs_noise_scale` gradient | `47.451133728027344` |
| `log_obs_noise_scale` MCSE | `0.12426705658435822` |

N1000 metadata:

- `batch_size=5`, `seed_microbatch_size=1`, `seed_microbatch_count=5`;
- `transport_plan_mode=streaming`;
- `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`;
- `transport_ad_mode=stabilized`;
- `regression_fd.fd_mode=ad-only`;
- output tensors were on `GPU:0`.

## N10000 Failure

Command launched under trusted/escalated GPU permissions:

```bash
MPLCONFIGDIR=/tmp timeout 7200 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 7 manual streaming actual-gradient N10000 GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json
```

Observed failure:

```text
tensorflow.python.framework.errors_impl.ResourceExhaustedError:
failed to allocate memory [Op:Sub]
```

The stack placed the failure inside the manual streaming finite transport path,
specifically during `_filterflow_streaming_softmin` in
`experiments/dpf_implementation/tf_tfp/resampling/annealed_transport_tf.py`.

Absent artifacts:

- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-gpu-tf32-2026-06-23.json`
- `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-n10000-progress-2026-06-23.json`

## Checks Before GPU Work

- `CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q`:
  `11 passed, 2 warnings in 7.32s`.
- `CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py`:
  passed.
- `git diff --check`: passed.
- Trusted `nvidia-smi`: GPU visible.
- Trusted TensorFlow probe: `[CPU:0, GPU:0]` and `[GPU:0]`.

## Non-Claims

This result does not claim FD agreement, P82 validation, posterior correctness,
HMC/default readiness, production readiness, scientific superiority, or
Zhao-Cui comparator readiness.  It does not prove the manual-adjoint idea is
impossible in all configurations; it blocks the reviewed N10000 route/harness
configuration used here.

## Handoff

P8 must not run because the required valid P7 N10000 actual-gradient artifact
does not exist.  Close out P82 under the P7 blocker.  Any further attempt should
be a new reviewed remediation subplan, for example to test allocator policy,
smaller chunks, different AD evaluation, or another memory strategy.
