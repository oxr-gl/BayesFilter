# Phase 1 Result: Tiny GPU/XLA Full-Route Smoke

Date: 2026-07-01

Status: `PASS`

## Decision

Phase 1 passed.  The corrected manual total-derivative finite-Sinkhorn route
ran in trusted GPU/XLA/TF32 mode at the tiny SIR size and returned finite value,
finite gradient components, and finite seed-gradient MCSE values.

This is a GPU/XLA viability smoke only.  It does not prove HMC readiness,
posterior correctness, exact nonlinear likelihood correctness, or material
particle-count scalability.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the corrected `transport_ad_mode="full"` manual route run under trusted GPU/XLA/TF32 at tiny SIR size? |
| Primary criterion | Passed. |
| Veto diagnostics | No veto triggered. |
| Not concluded | No material particle-count viability, no HMC readiness, no posterior correctness, no production promotion. |

## Command

The reviewed wrapper was launched with trusted GPU permissions:

```bash
bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh
```

The wrapper runs:

```bash
python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode ad-only \
  --batch-seeds 81120,81121 \
  --time-steps 1 \
  --num-particles 16 \
  --theta 0.02,-0.01,0.01 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json
```

## Artifact

JSON output:

`docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json`

## Gate Check

Local JSON gate:

```text
PHASE1_JSON_GATE_PASS
status pass
primary_pass True
device /GPU:0
output_devices /job:localhost/replica:0/task:0/device:GPU:0, /job:localhost/replica:0/task:0/device:GPU:0
compiler_mode xla
jit_compile True
transport_ad_mode full
objective -36.1256103515625
gradient_values [-9.37370777130127, 3.432502508163452, 4.548910617828369]
mcse_finite True
```

The Phase 0 static dispatch proof remains part of this gate: the legacy CLI
selector name `manual_streaming_finite_sinkhorn_stopped_scale_keys` is not the
derivative claim.  The derivative claim is the recorded
`transport_ad_mode="full"` route plus the Phase 0 code anchors proving this
selector pair reaches `_filterflow_manual_streaming_finite_transport_total_vjp`.

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `ef119f8bdb17b206339de92d722344a448eea745` |
| Host | `DESKTOP-RF1Q5IJ` |
| Python | `3.11.14` |
| TensorFlow | `2.19.1` |
| GPU | NVIDIA GeForce RTX 4080 SUPER, `/device:GPU:0` |
| Execution target | trusted GPU/XLA/TF32 |
| Dtype | `float32` |
| TF32 | enabled |
| Seeds | `81120,81121` |
| Time steps | `1` |
| Particles | `16` |
| Compiler | XLA, `jit_compile=True`, unit `manual_reverse_seed_microbatch_value_score` |
| Elapsed | `48.501640795962885` seconds |
| Output artifact | `docs/plans/bayesfilter-ledh-pfpf-ot-total-vjp-gpu-xla-validation-phase1-tiny-gpu-xla-smoke-2026-07-01.json` |

## Plain Scientific Classification

- Target computed: finite fixed-Sinkhorn active-transport scalar used by the
  P8p regression-FD diagnostic.
- Derivative classification: corrected manual total derivative route.
- What passed: trusted GPU execution, XLA compilation, full-route metadata,
  finite objective, finite gradient, finite MCSE, connected manual score route.
- What was not checked: finite-difference agreement, particle-count scaling,
  HMC direction quality, posterior correctness.

## Next-Phase Handoff

Phase 2 harness repair is not needed because the existing harness exercised the
corrected full route.  Write a Phase 2 skipped result, refresh the Phase 3
particle ladder subplan, and send this close record plus the Phase 3 subplan to
Claude for bounded read-only review.
