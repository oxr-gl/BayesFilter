# P4 Result: Heldout Replay And Residual Evaluation

Date: 2026-06-28

## Status

`FAIL_P4_METAOT_REFIT_HELDOUT_PRIMARY_BUDGET`

## Decision

`FAIL_P4_METAOT_REFIT_HELDOUT_PRIMARY_BUDGET`

The Meta OT-aligned one-half retained-Sinkhorn refit is now implemented and runnable, but it does **not** pass the current heldout primary-budget criterion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the donor-aligned one-half retained-Sinkhorn refit preserve corrected replay/residual behavior on heldout teacher-data examples strongly enough to replace the previous route under the current local heldout contract? |
| Baseline/comparator | Zero-init retained Sinkhorn under the same corrective budgets, plus the pre-refit local retained-teacher heldout result family. |
| Primary pass criterion | At the primary heldout budget, corrected student replay must be no worse than zero-init while maintaining finite corrected residual behavior. |
| Veto diagnostics | Student worse than zero-init at the primary budget; non-finite losses; non-finite corrected replay or residuals; route drift from fixed-target retained Sinkhorn. |
| Explanatory diagnostics | Low-budget improvements, train-loss decrease, and secondary heldout metrics. |
| Not concluded | No paper failure claim; no broad usefulness claim; no annealed-route implication. |

## Command Run

```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_heldout_eval_tf
```

## Observed Outcome

The run completed and wrote an updated heldout-eval artifact, but validation failed with:
- `RETAINED_TEACHER_SINKHORN_HELDOUT_EVAL_FAILED`

## Key Metrics Extracted From The Artifact

### Training contract
- `loss_route = meta_ot_log_u_dual_objective_plus_teacher_log_u`
- `prediction_head = meta_ot_log_u`
- `epochs = 250`
- `learning_rate = 1e-2`
- `train_examples = 7`
- `heldout_examples = 2`

### Losses
- `initial_train_loss = 21.180602899634405`
- `final_train_loss = -0.9566874777327402`
- `heldout_log_u_loss = 0.08974005166696339`

This means the donor-aligned objective route trains numerically and reduces the training objective sharply.

### Heldout replay at corrective budget 5
- `mean_student_teacher_cloud_rmse = 7.245550199312643e-06`
- `mean_zero_teacher_cloud_rmse = 1.3780486241526789e-04`
- `student_better_or_equal_count = 2/2`

### Heldout replay at corrective budget 10
- `mean_student_teacher_cloud_rmse = 1.029731594914381e-08`
- `mean_zero_teacher_cloud_rmse = 1.9321106545306283e-07`
- `student_better_or_equal_count = 1/2`

### Heldout replay at primary corrective budget 20
- `mean_student_teacher_cloud_rmse = 1.029731594914381e-08`
- `mean_zero_teacher_cloud_rmse = 0.0`
- `student_better_or_equal_count = 0/2`

### Residual behavior
- student residuals remained finite and small at all reported budgets
- the primary-budget failure is therefore **not** a numerical blow-up failure
- it is a **primary-budget replay competitiveness failure** against zero-init

## Interpretation

The new one-half donor-aligned route successfully restores the desired Meta OT-style semantics at the student/objective level, but under the current very small heldout teacher-data artifact it still fails the same local primary-budget issue that already existed in the earlier retained-teacher branch:
- at sufficiently large corrective budget, zero-init becomes essentially exact,
- so the student route has little room to win and currently loses at the binding primary rung.

This is not evidence that the donor-aligned route is incoherent.
It is evidence that, under the present tiny fixed-envelope dataset and the current primary-budget contract, the refit route does not yet justify replacing the baseline.

## Classification Of The Failure

This failure is best classified as:
- **local heldout primary-budget non-promotion**,
- **not** donor-route incoherence,
- **not** a residual or finite-output failure,
- **not** a paper-failure result.

## What P4 Does Not Conclude

P4 does **not** conclude:
- that Meta OT is wrong,
- that one-half prediction is worse in principle,
- that the fixed-target retained-Sinkhorn lane should be abandoned,
- or that the annealed route should be preferred instead.

It concludes only that the current donor-aligned refit does not yet pass the binding local heldout promotion rule.

## Next Step

Advance to P5 closeout.
The closeout must now decide whether the new donor-aligned route is still the correct substrate despite failing the current binding heldout budget criterion, and what the justified next action is.
