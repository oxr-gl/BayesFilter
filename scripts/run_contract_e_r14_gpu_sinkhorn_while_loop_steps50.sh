#!/usr/bin/env bash
set -euo pipefail

python docs/benchmarks/diagnose_ledh_pfpf_ot_contract_e_lgssm_gpu_score.py \
  --device-scope visible \
  --cuda-visible-devices 0 \
  --num-particles 1000 \
  --seed-count 10 \
  --time-steps 10 \
  --state-dims 2 1 \
  --settings 0.55:50 \
  --contract-e-reset-factorization cholesky-ridge \
  --chol-ridge-abs 1e-10 \
  --chol-ridge-rel 1e-8 \
  --chol-ridge-escalation 10 \
  --chol-ridge-max-attempts 12 \
  --tf32-mode enabled \
  --xla \
  --score-route manual-reverse-scan \
  --output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-2026-06-30.json \
  --markdown-output docs/plans/bayesfilter-ledh-pfpf-ot-contract-e-phase3-r14-gpu-xla-tf32-sinkhorn-while-loop-steps50-result-2026-06-30.md
