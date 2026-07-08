#!/usr/bin/env bash
set -euo pipefail

python docs/benchmarks/benchmark_p8p_regression_fd_reparameterization.py \
  --phase-label "SIR budget10 whitened reparameterization diagnostic" \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --ad-evaluation-mode manual-reverse \
  --manual-reverse-compiler xla \
  --fd-mode enabled \
  --basis-set whitened \
  --num-particles 64 \
  --time-steps 3 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --sinkhorn-iterations 10 \
  --theta 0.02,-0.01,0.01 \
  --base-step 0.001 \
  --base-step-ladder "" \
  --regression-offsets=-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6 \
  --trim-extreme-offsets 1 \
  --trim-extreme-mode value \
  --fd-evaluation-mode batched-theta \
  --theta-offset-batch-size 2 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --memory-sample-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-memory-2026-07-01.json \
  --memory-sample-interval-seconds 30 \
  --progress-output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-progress-2026-07-01.json \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-whitened-budget10-2026-07-01.json
