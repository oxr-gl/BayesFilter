# Phase 1 Launch Blocker: Approval Timeout

Date: 2026-07-01

Status: `BLOCKED_REQUIRES_HUMAN_APPROVAL`

## What Happened

Phase 1 attempted to launch the reviewed trusted GPU/XLA smoke command.

Direct command attempt:

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

Result:

```text
Rejected("The automatic permission approval review did not finish before its deadline. Do not assume the action is unsafe based on the timeout alone. You may retry once, or ask the user for guidance or explicit approval.")
```

Wrapper repair:

- Created `scripts/run_total_vjp_gpu_xla_phase1_smoke.sh`.
- `bash -n scripts/run_total_vjp_gpu_xla_phase1_smoke.sh` passed.

Wrapper launch attempt:

```bash
bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh
```

Result:

```text
Rejected("The automatic permission approval review did not finish before its deadline. Do not assume the action is unsafe based on the timeout alone. You may retry once, or ask the user for guidance or explicit approval.")
```

## Interpretation

This is not evidence that the corrected total-VJP route failed.  It is an
approval timeout before the trusted GPU command started.

## Required Approval

Please approve running:

```bash
bash scripts/run_total_vjp_gpu_xla_phase1_smoke.sh
```

with trusted/escalated permissions.

## Nonclaims

- No Phase 1 GPU/XLA result exists yet.
- No GPU/XLA viability has been tested.
- No HMC readiness or production claim is made.
