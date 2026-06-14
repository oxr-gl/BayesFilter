# DPF LGSSM Student Tie-Out Diagnostic Parameter Filter Repair Amendment

metadata_date: 2026-06-07
status: CLAUDE_REVIEWED_PASS_IMPLEMENTED

## Blocker

The first LGSSM student/FilterFlow evidence run stopped before writing result
artifacts because the diagnostic-only APF jitter mirror attempted to convert all
entries in `spec.parameters` to `float64`.  The V2 LGSSM parameter dictionary
also contains checksum/metadata strings, so this raised:

```text
ValueError: could not convert string to float
```

This is a local diagnostic implementation bug.  It is not evidence for or
against APF, MLCOE, FilterFlow, or BayesFilter.

## Allowed Repair

Patch only
`experiments/dpf_implementation/tf_tfp/runners/run_lgssm_student_filterflow_value_gradient_tieout_tf.py`
so the diagnostic APF jitter mirror reads only the numeric LGSSM parameters
needed for the mirror:

- `A`
- `C`
- `P0`
- `Q`
- `R`
- `m0`

No strict V2 comparator, tolerance, fixture, branch timing, scalar,
classification rule, or gradient knob may change.  No vendored student file may
be edited.

## Evidence After Repair

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_lgssm_student_filterflow_value_gradient_tieout_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_student_filterflow_value_gradient_tieout_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_student_filterflow_value_gradient_tieout_tf --validate-only
```

## Decision State

review_round: 1
open_material_blockers: none
next_allowed_action: rerun evidence and validation

## Claude Review

Claude worker review returned `PASS`.

Review summary:

- safe if confined to selecting numeric LGSSM keys `{A, C, P0, Q, R, m0}` in
  the two diagnostic mirror parameter reads;
- diagnostic mirrors cannot create strict `MATCHED` status;
- no strict comparator, tolerance, fixture, branch, scalar, classification,
  gradient, or student-code path should change.

## Implementation

Implemented in
`experiments/dpf_implementation/tf_tfp/runners/run_lgssm_student_filterflow_value_gradient_tieout_tf.py`.

The patch adds `_numeric_lgssm_parameters()` and uses it only in the APF
diagnostic jitter mirror functions.
