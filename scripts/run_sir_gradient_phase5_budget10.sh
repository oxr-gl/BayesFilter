#!/usr/bin/env bash
set -euo pipefail

python docs/benchmarks/diagnose_p8p_sir_sinkhorn_budget.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --manual-reverse-compiler xla \
  --num-particles 64 \
  --time-steps 3 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --candidate-steps 10 \
  --theta 0.02,-0.01,0.01 \
  --base-step 0.001 \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --theta-offset-batch-size 2 \
  --trim-extreme-values 1 \
  --transport-policy active-all \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --progress-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-progress-2026-06-30.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-hmc-direction-phase5-budget10-2026-06-30.md
