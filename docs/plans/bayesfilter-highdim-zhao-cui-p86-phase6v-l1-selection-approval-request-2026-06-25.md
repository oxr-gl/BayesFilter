# P86 Phase 6V Approval Request: L1 Selection Fitting Arms

Date: 2026-06-25

Status: `PENDING_HUMAN_APPROVAL_AFTER_CLAUDE_REVIEW`

## Request

After Claude agrees the Phase 6V no-fit preflight/guard result, approve the
following three CPU-hidden fitting commands exactly as written.

These commands are local Phase 6V selection diagnostics only. They do not use
the audit cloud for tuning and do not establish rank convergence, HMC
readiness, GPU performance, or production readiness.

## Commands

Arm A, `l1_weight=0.0`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-0-fit-2026-06-25.json
```

Arm B, `l1_weight=3e-10`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-10-fit-2026-06-25.json
```

Arm D, `l1_weight=3e-9`:

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-preflight-2026-06-25.json --target-dimension 36 --fit-rank 5 --training-sample-count 567600 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6v-l1-selection-rank5-lr3e-4-l1-3e-9-fit-2026-06-25.json
```

## Boundaries

- The existing Phase 6T `l1_weight=1e-9` artifact is reused; it is not rerun.
- The audit cloud is reserved and not used for tuning.
- CPU-hidden TensorFlow logs are not GPU evidence.
- A Phase 6V selection ledger must be written after the runs.
- Phase 7 remains blocked until a later reviewed same-policy rank/degree
  convergence gate passes or is explicitly reframed with owner approval.
