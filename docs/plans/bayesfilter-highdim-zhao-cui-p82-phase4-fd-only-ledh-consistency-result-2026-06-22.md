# P82 Phase 4 Result: FD-Only LEDH Consistency Check

status: BLOCKED_RUNTIME_FEASIBILITY_N10000_FULL_TRANSPORT_ADONLY
date: 2026-06-22
phase: P4-FD-ONLY

## Question

Under the FD-only amendment, does the differentiable LEDH-PFPF-OT SIR d=18
gradient agree with regression-FD slopes of the same LEDH scalar in raw theta
directions?

## Short Answer

Not answered.  The tiny trusted-GPU mechanics smoke passed, but the governed
N=10000 five-seed actual-gradient gate with `transport_ad_mode=full` did not
produce an artifact in the bounded window and was interrupted.

This is a runtime-feasibility blocker for the current N=10000 full-transport
AD-only route.  It is not evidence that the LEDH gradient is mathematically
wrong, and it is not a regression-FD mismatch because the N=1000 FD run was not
launched after the N=10000 gate failed.

## Scope

Zhao-Cui was not used as comparator evidence.  The active comparator for this
amended P82 scope is regression FD of the same LEDH scalar only.  Regression FD
remains a noisy diagnostic comparator, not an oracle.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Question | Not answered beyond mechanics smoke. |
| Baseline/comparator | N=1000 13-point regression FD was planned but not launched because N=10000 actual-gradient gate failed first. |
| Primary criterion | Failed by missing N=10000 AD-only artifact. |
| Veto status | Vetoed by unbounded runtime / no progress artifact for N=10000 full-transport AD-only. |
| Explanatory diagnostics | Tiny smoke passed; interrupted stack was inside streaming Sinkhorn softmin forward-JVP path. |
| Not concluded | No LEDH-vs-FD consistency result, no posterior correctness, no exact likelihood correctness, no HMC readiness, no default readiness, no Zhao-Cui comparator readiness, no manual-adjoint correctness. |

## Commands And Observations

### Local Checks

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-*
```

Observed:

- pytest: `7 passed, 2 warnings`;
- py_compile: passed;
- diff check: passed.

### Trusted GPU Preflight

```bash
nvidia-smi
```

Observed before GPU runs:

- NVIDIA GeForce RTX 4080 SUPER;
- driver `591.86`, CUDA `13.1`;
- GPU memory around `4383 MiB / 16376 MiB`;
- no running processes listed.

### Tiny Mechanics Smoke

Command:

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 1 --num-particles 8 \
  --batch-seeds 81120 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode enabled \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only tiny LEDH mechanics smoke" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 --col-chunk-size 8 --particle-chunk-size 8 \
  --dtype float32 --tf32-mode enabled \
  --base-step-mode fixed \
  --base-step 0.001 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --basis-set raw \
  --direction-filter log_obs_noise_scale \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-tiny-smoke-gpu-tf32-2026-06-22.json
```

Artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-tiny-smoke-gpu-tf32-2026-06-22.json`

Observed:

- elapsed seconds: about `2.72`;
- GPU output devices present;
- `tf32_execution_enabled = true`;
- `transport_ad_mode = full`;
- `num_particles = 8`;
- `trim_extreme_mode = value`;
- smoke objective and gradient finite;
- smoke FD line was only a mechanics check, not P82 evidence.

### N=10000 AD-Only Gate

Command:

```bash
env MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 3 --num-particles 10000 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode forward-jvp \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 FD-only LEDH N10000 AD-only GPU TF32" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-ad-mode full \
  --sinkhorn-iterations 10 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 512 --col-chunk-size 512 --particle-chunk-size 512 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --progress-output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-progress-2026-06-22.json \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-ledh-n10000-adonly-gpu-tf32-2026-06-22.json
```

Observed:

- TensorFlow created `/device:GPU:0` with about `13495 MB` available.
- At approximately 27.5 minutes, `ps` showed PID `461043` running with about
  `00:27:11` CPU time and about `98.6%` CPU.
- Trusted `nvidia-smi` showed memory about `15836 MiB / 16376 MiB` and GPU
  utilization about `38%`.
- Neither the output JSON nor progress JSON existed.
- The run was interrupted by Codex with Ctrl-C to avoid an unbounded run.
- Process exited with code `130`.
- Post-interrupt trusted `nvidia-smi` showed GPU memory around
  `2454 MiB / 16376 MiB`.

The interrupted stack was inside:

- `benchmark_p8p_regression_fd_reparameterization.py:_forward_jvp_diagnostic_for_contexts`;
- `benchmark_p8p_parameterized_sir_gradient.py:_objective_from_components`;
- `experimental_batched_ledh_pfpf_ot_streaming_tf.py:streaming_batched_ledh_pfpf_ot_value_core_tf`;
- `annealed_transport_tf.py:_filterflow_streaming_sinkhorn_potentials`;
- `annealed_transport_tf.py:_filterflow_streaming_softmin`;
- TensorFlow forwardprop/JVP execution.

## Decision Table

| Decision | Primary criterion status | Veto status | Main uncertainty | Next justified action | Not concluded |
|---|---|---|---|---|---|
| Accept P4 tiny mechanics smoke | Passed | GPU placement, TF32, full mode, value trim present | Tiny one-seed T=1 result has no scientific weight | Use only as mechanics evidence | No gradient validation |
| Stop before N=1000 FD | Not reached | N=10000 actual-gradient artifact missing | Whether smaller/chunked actual-gradient gate or different AD route can produce usable N=10000 evidence | Redesign actual-gradient gate before FD run | No LEDH-vs-FD comparison |
| Close P4 as runtime blocker | Failed N=10000 AD-only artifact criterion | Unbounded runtime/no progress artifact | Whether `full` streaming forward-JVP can be optimized, chunked further, or replaced by a reviewed manual/custom gradient route | Plan a narrower runtime repair: N ladder, one raw direction JVP, reduced sinkhorn/time, or manual-adjoint lane | No HMC/default/scientific claim |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `5ea363e` |
| Working directory | `/home/chakwong/BayesFilter` |
| Date/time | `2026-06-22T13:55:11+08:00` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, trusted `nvidia-smi` |
| TensorFlow | `2.19.1` in tiny smoke artifact |
| Precision | float32, TF32 enabled |
| Seeds | tiny smoke `81120`; N=10000 gate `81120,81121,81122,81123,81124` |
| Theta | `0.02,-0.01,0.01` for `log_kappa_scale,log_nu_scale,log_obs_noise_scale` |
| Tiny smoke artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p82-fdonly-tiny-smoke-gpu-tf32-2026-06-22.json` |
| N=10000 output artifact | Missing |
| N=10000 progress artifact | Missing |
| N=1000 FD artifact | Not launched |

## Handoff

P82 remains active under the FD-only amendment but blocked at the N=10000
actual-gradient runtime gate.

The next smallest safe action is not to run the full N=1000 FD comparison.
First redesign the actual-gradient gate so it can produce a bounded artifact.
Candidate routes:

- N ladder for AD-only full transport: N=1000, 2000, 5000, then 10000 only if
  progress is acceptable;
- one raw-direction forward-JVP instead of full raw-basis JVP at N=10000;
- smaller `time_steps` gate before T=3;
- transport-core optimization or manual/custom-gradient lane;
- explicitly reviewed fallback to a different transport AD contract if the
  scientific question is changed.

## Nonclaims

This result does not conclude LEDH gradient correctness, FD agreement,
posterior correctness, exact likelihood correctness, HMC/NUTS readiness,
default-gradient readiness, production readiness, Zhao-Cui comparator
readiness, manual-adjoint correctness, or scientific superiority.
