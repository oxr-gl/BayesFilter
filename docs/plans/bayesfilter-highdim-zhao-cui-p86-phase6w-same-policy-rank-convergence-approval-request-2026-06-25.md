# P86 Phase 6W Exact-Command Approval Request: Same-Policy Rank-4 Fits

Date: 2026-06-25

Status: `READY_FOR_EXACT_HUMAN_APPROVAL_AFTER_PHASE6W_NO_FIT_REVIEW_AGREE`

This request lists the exact Phase 6W rank-4 same-policy fitting commands
frozen by:

`docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json`

The Phase 6W no-fit preflight/guard result has Claude `VERDICT: AGREE`.
Do not run these commands until the user explicitly approves these exact
commands.

## Evidence Boundary

The commands below are CPU-hidden training-base fits for the Phase 6W rank-4
same-policy L1 grid. They may support a later reviewed rank-convergence ledger.
They do not by themselves establish rank convergence, degree convergence,
Phase 7 correctness, posterior correctness, HMC readiness, GPU performance,
production readiness, or source-faithful author TT-cross training.

The audit cloud remains reserved and must not be used for L1 selection.

## Exact Commands

### rank4_lr3e-4_l1_0

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json --target-dimension 36 --fit-rank 4 --training-sample-count 364320 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-0-fit-2026-06-25.json
```

### rank4_lr3e-4_l1_3e-10

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json --target-dimension 36 --fit-rank 4 --training-sample-count 364320 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.0000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-10-fit-2026-06-25.json
```

### rank4_lr3e-4_l1_1e-9

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json --target-dimension 36 --fit-rank 4 --training-sample-count 364320 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000001 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-1e-9-fit-2026-06-25.json
```

### rank4_lr3e-4_l1_3e-9

```text
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python scripts/p86_author_lagrangep_phase5_budget_fit.py --fit --preflight-json docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-same-policy-rank-convergence-preflight-2026-06-25.json --target-dimension 36 --fit-rank 4 --training-sample-count 364320 --holdout-sample-count 65536 --audit-sample-count 65536 --seed 8606 --optimizer-batch-size 4096 --prefit-steps 0 --train-steps 512 --learning-rate 0.0003 --l1-weight 0.000000003 --l2-weight 0.00000001 --logz-anchor-weight 0.0 --max-seconds 7200 --memory-cap-mib 12288 --adaptive-training --validation-check-every 16 --plateau-patience 4 --plateau-min-delta 0.000001 --lr-reduction-factor 0.5 --min-learning-rate 0.000001 --early-stop-after-lr-drops 4 --serialize-trained-cores --train-prior-seed 8301 --train-process-seed 8401 --holdout-prior-seed 9301 --holdout-process-seed 9401 --audit-prior-seed 9311 --audit-process-seed 9501 --output docs/plans/bayesfilter-highdim-zhao-cui-p86-phase6w-rank4-lr3e-4-l1-3e-9-fit-2026-06-25.json
```

## Approval Meaning

If approved after Claude review, Codex may run the four commands above exactly
as written, sequentially, preserving the runbook stop conditions. Any command
drift, runtime/memory breach, nonfinite diagnostic, audit-tuning need, or
unsupported claim boundary stops execution and requires a blocker result.
