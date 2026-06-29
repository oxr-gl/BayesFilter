# P82 Phase 6 Result: Tiny Manual-Streaming GPU Smoke

status: REVIEWED_PASSED_CLAUDE_AGREE
date: 2026-06-23
phase: P6-TINY-MANUAL-STREAMING-GPU-SMOKE

## Question

Can the P5-wired manual streaming transport-gradient route execute on a tiny
SIR d18 GPU/TF32 actual-gradient smoke without using the known-bad full-AD
route?

## Decision

Yes for the P6 backend/mechanics question.  Trusted GPU preflight passed,
TensorFlow saw `GPU:0`, the tiny `ad-only` smoke exited 0 with finite objective
and finite gradient components, and one-path Claude execution review returned
`VERDICT: AGREE`.

This is not P82 validation.  It does not establish FD agreement, N10000
feasibility, N1000 regression-FD behavior, posterior correctness, HMC/default
readiness, production readiness, scientific superiority, or Zhao-Cui comparator
readiness.

## Evidence Contract Outcome

| Field | Outcome |
|---|---|
| Primary criterion | Passed locally: trusted GPU preflight succeeded; smoke exited 0; JSON records GPU placement, `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `regression_fd.fd_mode=ad-only`, finite objective, and finite gradients. |
| Veto diagnostics | No non-escalated GPU evidence used; no GPU placement failure; no wrong route metadata; no `transport_ad_mode=full`; no FD line run; no N10000/N1000 governed work launched; no OOM or timeout observed. |
| Main uncertainty | Whether the route scales to five-seed N10000 actual-gradient feasibility remains untested. |
| Next justified action | P7 actual-gradient feasibility may begin under its reviewed subplan. |

## Run Manifest

| Field | Value |
|---|---|
| Git commit | `a463bb012df35bb120a9b232df067e69bf915add` |
| Python / TensorFlow | Python `3.11.14`, TensorFlow `2.19.1` |
| CPU/GPU status | Trusted/escalated GPU run; no `CUDA_VISIBLE_DEVICES=-1` hiding for GPU preflight or smoke. |
| GPU preflight | `nvidia-smi` saw NVIDIA GeForce RTX 4080 SUPER-class GPU, driver `591.86`, CUDA `13.1`, 16376 MiB memory. |
| TensorFlow device probe | TensorFlow saw `[CPU:0, GPU:0]` and `[GPU:0]`; plugin-registration warnings appeared but did not veto this smoke. |
| Seeds | `81120` |
| Shape | `time_steps=1`, `num_particles=8`, `state_dim=18`, `obs_dim=9`, `parameter_dim=3` |
| Route | `transport_plan_mode=streaming`, `gradient_mode=manual_streaming_finite_sinkhorn_stopped_scale_keys`, `transport_ad_mode=stabilized`, `regression_fd.fd_mode=ad-only` |
| Precision | `dtype=float32`, TF32 enabled |
| Wall time | `1.9384818370017456` seconds reported by benchmark |
| JSON artifact | `docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-2026-06-23.json` |

## Commands Run

Local CPU-hidden checks:

```bash
CUDA_VISIBLE_DEVICES=-1 python -m pytest tests/highdim/test_p82_regression_fd_harness_protocol.py -q
CUDA_VISIBLE_DEVICES=-1 python -m py_compile docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py
git diff --check -- docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py docs/benchmarks/benchmark_p8p_parameterized_sir_gradient.py experiments/dpf_implementation/tf_tfp/filters/experimental_batched_ledh_pfpf_ot_streaming_tf.py tests/highdim/test_p82_regression_fd_harness_protocol.py docs/plans/bayesfilter-highdim-zhao-cui-p82-p6-p8-completion-plan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase7-actual-gradient-feasibility-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase8-governed-fd-consistency-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-phase9-closeout-subplan-2026-06-23.md docs/plans/bayesfilter-highdim-zhao-cui-p82-claude-review-ledger-2026-06-22.md docs/plans/bayesfilter-highdim-zhao-cui-p82-visible-execution-ledger-2026-06-22.md
```

Observed local results:

- focused pytest: `11 passed, 2 warnings in 7.06s`;
- py_compile: passed;
- diff hygiene: passed.

Trusted GPU preflight:

```bash
nvidia-smi
MPLCONFIGDIR=/tmp python -c "import tensorflow as tf; print(tf.__version__); print(tf.config.list_physical_devices()); print(tf.config.list_physical_devices('GPU'))"
```

Trusted GPU smoke:

```bash
MPLCONFIGDIR=/tmp timeout 900 python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible --expect-device-kind gpu --device /GPU:0 \
  --time-steps 1 --num-particles 8 \
  --batch-seeds 81120 \
  --seed-microbatch-size 1 \
  --ad-evaluation-mode reverse-gradient \
  --fd-mode ad-only \
  --theta 0.02,-0.01,0.01 \
  --phase-label "P82 Phase 6 tiny manual streaming transport-gradient GPU smoke" \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --sinkhorn-iterations 2 --sinkhorn-epsilon 1.0 \
  --row-chunk-size 8 --col-chunk-size 8 --particle-chunk-size 8 \
  --dtype float32 --tf32-mode enabled \
  --basis-set raw \
  --output docs/plans/bayesfilter-highdim-zhao-cui-p82-phase6-tiny-manual-streaming-gpu-smoke-2026-06-23.json
```

## Observed Smoke Values

| Quantity | Value |
|---|---|
| Objective | `-36.267765045166016` |
| `log_kappa_scale` gradient | `-9.514933586120605` |
| `log_nu_scale` gradient | `3.485823154449463` |
| `log_obs_noise_scale` gradient | `4.861774921417236` |
| Output devices | `GPU:0` for objective and gradient tensors |

## Non-Claims

P6 does not claim FD agreement, N10000 feasibility, N1000 regression-FD
behavior, exact likelihood correctness, posterior validity, HMC readiness,
default readiness, production readiness, scientific superiority, or Zhao-Cui
source-faithfulness/comparator readiness.

## Claude Review

One-path Claude execution review of this result returned `VERDICT: AGREE`.
Claude found no material scope creep, confirmed the route-execution evidence
was present in this file, and found no unsafe handoff.

## Handoff

P7 may run the reviewed actual-gradient feasibility ladder.  P7 remains
feasibility-only until it produces a valid N10000 artifact; P8 remains blocked
until then.
