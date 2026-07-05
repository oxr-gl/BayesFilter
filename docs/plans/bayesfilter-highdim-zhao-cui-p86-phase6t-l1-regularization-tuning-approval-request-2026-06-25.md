# P86 Phase 6T Approval Request: L1 Regularization Diagnostic

Date: 2026-06-25

Status: `PENDING_HUMAN_APPROVAL_AFTER_CLAUDE_RESULT_REVIEW`

## Request

Approve the exact Phase 6T diagnostic command below only after Claude reviews
and agrees with:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-result-2026-06-25.md`

## Exact Command

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000001 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6t-l1-regularization-tuning-diagnostic-2026-06-25.json
```

## Scope

This is a CPU-hidden, non-production, single diagnostic run. It tests whether a
conservative LR and explicit L1 regularization improve the rank-5
validation/normalizer pathology seen in Phase 6S.

## Nonclaims

- This is not a grid search.
- This does not use audit data for tuning.
- This does not establish rank convergence by itself.
- This does not establish posterior correctness, KR closure, HMC readiness,
  LEDH comparison, GPU performance, source-faithful TT-cross training, or
  production readiness.
