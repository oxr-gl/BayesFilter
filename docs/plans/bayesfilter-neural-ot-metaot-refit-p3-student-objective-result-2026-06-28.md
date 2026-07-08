# P3 Result: Student And Objective Refit

Date: 2026-06-28

## Status

`PASS_P3_ONE_HALF_ROUTE_IMPLEMENTED_READY_FOR_P4`

## Decision

`PASS_P3_ONE_HALF_ROUTE_IMPLEMENTED_READY_FOR_P4`

The fixed-target retained-Sinkhorn route now has an implemented Meta OT-aligned one-half prediction path and a donor-style objective-based training route.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How should BayesFilter refit the current retained-Sinkhorn student and training path so it predicts one donor-style dual half and supports a donor-faithful objective-based route? |
| Baseline/comparator | Current `SinkhornWarmStartStudentTF` route and the P1/P2 target/data contracts. |
| Primary pass criterion | A result artifact records the code-level refit design for the student module, complementary recovery, objective-based training path, and compatibility boundary versus the old dual-pair route. |
| Veto diagnostics | Hidden full dual-pair prediction retained as the default; no donor-style objective path; corrected deployment semantics broken; route drift into annealed logic. |
| Explanatory diagnostics | Parameter counts, architectural minimalism, and training convenience only. |
| Not concluded | P3 does not yet decide final heldout success. |

## Implemented Changes

### 1. Student config now supports donor-aligned one-half prediction
Modified:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

Change:
- `RetainedTeacherWarmStartConfigTF` now includes `prediction_head`
- supported route variants include:
  - `dual_pair` (historical local route)
  - `meta_ot_log_u` (new donor-aligned route)

### 2. One-half prediction path implemented
Modified:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

Change:
- the output layer width is now conditional on `prediction_head`
- `predict_log_state()` now supports:
  - old full-pair path for historical compatibility
  - new `meta_ot_log_u` path that predicts one half and recovers the other teacher-consistently

### 3. Teacher-side complementary recovery implemented
Added in:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

New helper:
- `recover_sinkhorn_log_state_from_log_u_tf(...)`

Behavior:
- takes `canonical_log_u`, particles, weights, and epsilon
- reconstructs the complementary half with the retained teacher-side update rule under the same geometry/cost and target marginal
- returns a `SinkhornLogStateTF`

### 4. One-half prediction access helper added
Added:
- `predict_canonical_log_u_tf(...)`

This provides a donor-aligned readout path for one-half training/evaluation without forcing callers through the old full-pair interface.

### 5. Meta OT-style objective-based loss added
Added in:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`

New helper:
- `meta_ot_dual_objective_loss_tf(...)`

Behavior:
- computes a donor-aligned teacher dual objective loss from predicted `canonical_log_u`
- reconstructs the complementary half first
- evaluates a retained-teacher dual objective rather than only pair-regression loss

### 6. Heldout-eval runner switched to donor-aligned path
Modified:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`

Changes:
- the student is now instantiated with `prediction_head="meta_ot_log_u"`
- training loss route changed from pure latent-pair regression to:
  - donor-style objective loss
  - plus teacher `log_u` supervision
- artifact metadata now records:
  - `loss_route = meta_ot_log_u_dual_objective_plus_teacher_log_u`
  - `prediction_head = meta_ot_log_u`

### 7. Teacher-data manifest annotated for the refit route
Modified:
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`

Added policy fields:
- `meta_ot_refit_target_half = canonical_log_u`
- `meta_ot_refit_complementary_recovery = teacher_side_sinkhorn_update`
- `route_family = meta_ot_aligned_fixed_target_retained_sinkhorn_refit`

## Compatibility Boundary

The historical dual-pair path is not deleted.

It remains available for:
- comparison,
- regression checks,
- implementation history.

But it no longer defines the donor-aligned refit route.

The controlling donor-aligned route is now the `meta_ot_log_u` path.

## Local Verification Run

The modified files passed syntax compilation via:
- `python -m py_compile` on the updated student helper and refit runners.

The updated teacher-data runner also executed successfully and regenerated a valid artifact under the updated route manifest contract.

## What P3 Does Not Conclude

P3 does **not** conclude:
- that the new one-half route already outperforms the previous route on heldout replay,
- that the donor-style objective is already superior scientifically,
- or that donor-faithful closure is complete.

P3 concludes only that the one-half route and donor-style objective are now implemented and ready for heldout replay evaluation.

## Next Step

Advance to P4 heldout replay evaluation.
