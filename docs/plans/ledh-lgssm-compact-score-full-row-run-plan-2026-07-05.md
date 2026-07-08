# LEDH LGSSM Compact Score Full-Row Run Plan

Date: 2026-07-05

## Question

Does the repaired compact no-autodiff forward-sensitivity LEDH-PFPF-OT score
run on the full LGSSM leaderboard row and pass a same-scalar finite-difference
check on GPU?

## Baseline / Comparator

- Value comparator: exact Kalman log likelihood on the same LGSSM observations
  and model.
- Score comparator: central finite difference of the same LEDH-PFPF-OT scalar,
  not the exact Kalman likelihood.

## Primary Pass Criteria

- The run uses the full row identity: batch seeds
  `81120,81121,81122,81123,81124`, `N=1000`, `T=50`,
  `active-all`, 10 Sinkhorn iterations, epsilon `0.5`.
- Value tensors and compact score tensors are placed on GPU.
- Output values are finite.
- Compact score route is
  `compact_forward_sensitivity_no_autodiff_same_scalar_lgssm_ledh_pfpf_ot`.
- Same-scalar finite difference status is `pass`.
- `score_admission_status` is `admitted_same_target_compact_score`.

## Veto Diagnostics

- Any non-finite value or score vetoes admission.
- CPU placement for either value or score vetoes material GPU admission.
- Failed same-scalar finite difference vetoes score admission.
- OOM or runtime failure leaves the full row unresolved.

## Explanatory Diagnostics

- Exact Kalman value error is explanatory for the LEDH value row; it is not a
  score correctness criterion.
- Warm-call timing and GPU memory are explanatory only.

## Nonclaims

- This does not prove exact Kalman score correctness.
- This does not prove posterior correctness.
- This does not prove HMC/NUTS readiness.
- This does not rank LEDH against other algorithms.
- This does not validate nonlinear rows.

## Skeptical Audit

The plan avoids the earlier overclaiming error: full-row admission is tied to
seeds, particle count, horizon, transport policy, Sinkhorn settings, GPU device
placement for both value and score, and same-scalar finite-difference pass.
The finite-difference step defaults to `1e-3` for float32/TF32 after the GPU
smoke showed that `1e-5` fails from roundoff rather than a mathematical mismatch.

## Command

```bash
MPLCONFIGDIR=/tmp python docs/benchmarks/benchmark_ledh_same_target_lgssm_m3_t50_value.py \
  --device-scope visible \
  --expect-device-kind gpu \
  --device /GPU:0 \
  --batch-seeds 81120,81121,81122,81123,81124 \
  --num-particles 1000 \
  --time-steps 50 \
  --transport-policy active-all \
  --sinkhorn-iterations 10 \
  --sinkhorn-epsilon 0.5 \
  --transport-gradient-mode manual_streaming_finite_sinkhorn_stopped_scale_keys \
  --transport-ad-mode full \
  --row-chunk-size 512 \
  --col-chunk-size 512 \
  --particle-chunk-size 256 \
  --score-mode compact-sensitivity \
  --dtype float32 \
  --tf32-mode enabled \
  --history-mode value-only \
  --output docs/plans/ledh-lgssm-compact-score-full-row-2026-07-05.json \
  --markdown-output docs/plans/ledh-lgssm-compact-score-full-row-2026-07-05.md
```
