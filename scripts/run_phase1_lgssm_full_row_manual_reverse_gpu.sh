#!/usr/bin/env bash
set -euo pipefail

# The score gate is the runner's manual-reverse route plus its emitted
# same-scalar FD check.  The transport AD mode is the runner-required internal
# transport setting for total VJP; it is not score provenance.
python docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --num-particles 10000 \
  --time-steps 50 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 0.5 \
  --annealed-scaling 0.9 \
  --annealed-convergence-threshold 0.001 \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --score-mode manual-reverse \
  --history-mode full \
  --warmups 0 \
  --repeats 1 \
  --dtype float32 \
  --tf32-mode enabled \
  --device /GPU:0 \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --expect-device-kind gpu \
  --output docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-run-2026-07-04.json \
  --markdown-output docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase1-lgssm-full-row-run-2026-07-04.md
