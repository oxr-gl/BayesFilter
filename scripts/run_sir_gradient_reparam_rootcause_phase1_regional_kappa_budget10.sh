#!/usr/bin/env bash
set -euo pipefail

python docs/benchmarks/benchmark_p8p_regional_kappa_gradient_decomposition.py \
  --phase-label "SIR regional kappa decomposition budget10 diagnostic" \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --dtype float32 \
  --tf32-mode enabled \
  --num-particles 64 \
  --time-steps 3 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --seed-microbatch-size 1 \
  --sinkhorn-iterations 10 \
  --theta 0.02,-0.01,0.01 \
  --fd-step 0.001 \
  --transport-policy active-all \
  --transport-plan-mode streaming \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode stabilized \
  --row-chunk-size 64 \
  --col-chunk-size 64 \
  --particle-chunk-size 64 \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-sir-gradient-reparam-rootcause-phase1-regional-kappa-budget10-2026-07-01.json
