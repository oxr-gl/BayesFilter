#!/usr/bin/env bash
set -euo pipefail

python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --manual-reverse-compiler xla \
  --num-particles 16 \
  --time-steps 1 \
  --batch-seeds 81120,81121 \
  --candidate-steps 10 \
  --theta 0.02,-0.01,0.01 \
  --base-step 0.001 \
  --regression-offsets=-3,-2,-1,0,1,2,3 \
  --trim-extreme-values 0 \
  --transport-policy active-all \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --row-chunk-size 16 \
  --col-chunk-size 16 \
  --particle-chunk-size 16 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase3-gpu-xla-smoke-2026-06-30.md
