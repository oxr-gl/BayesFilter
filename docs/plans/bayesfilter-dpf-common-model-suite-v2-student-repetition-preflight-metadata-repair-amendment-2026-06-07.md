# DPF Common Model Suite V2 Student Repetition Preflight Metadata Repair Amendment

metadata_date: 2026-06-07
status: CLAUDE_REVIEWED_PASS_IMPLEMENTED

## Blocker

The student repetition runner currently blocks before executing any student
surface because it requires the frozen V2 JSON artifacts to carry their final
phase `decision` strings.  The V2 phase result ledgers, Claude review ledgers,
and final overnight closeout record reviewed PASS closure through P7, but the
machine JSON artifacts still retain stale top-level `PENDING_CLAUDE_REVIEW`
metadata.

This is a metadata preflight blocker.  It is not a density/path/gradient
mismatch and it does not justify changing any frozen V2 value, fixture, scalar,
branch, tolerance, comparator, or student classification.

## Evidence Contract

Question: can the student repetition preflight recognize already reviewed V2
phase closure without weakening the frozen V2 scientific contract?

Primary criterion:

- P2, P3, P4, and P5 are accepted as closed only when the expected PASS
  decision appears in the phase result ledger, the corresponding Claude review
  ledger, and the final V2 overnight closeout.

Veto diagnostics:

- using stale JSON `PENDING_CLAUDE_REVIEW` as a PASS by itself;
- accepting a phase when either the result ledger, Claude ledger, or final
  closeout is missing the expected PASS decision;
- modifying frozen V2 numerical artifacts, fixtures, tolerances, scalars,
  branches, comparators, or gradient contracts;
- running a student command before this repair is reviewed;
- treating BayesFilter, FilterFlow, either student repository, TT/SIRT, dense
  quadrature, simulated truth, or paper tables as an oracle.

Explanatory-only diagnostics:

- the stale JSON `decision` fields;
- phase artifact checksums;
- command stderr from CPU-only TensorFlow imports.

Not concluded:

- no filter correctness claim;
- no BayesFilter, FilterFlow, or student correctness claim;
- no new BF/FF tie-out claim beyond the already reviewed V2 closeout;
- no student match/mismatch/failure claim before the student runner executes.

## Allowed Repair

Patch only
`experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_student_repetition_tf.py`
so `_preflight_closed_artifacts()`:

1. still requires the final V2 closeout to contain
   `PASS_OVERNIGHT_EXECUTION_CLOSED_THROUGH_P7`;
2. still requires the manifest model ids to equal `EXPECTED_V2_MODEL_IDS`;
3. for each closed V2 phase artifact P2--P5, accepts final closure only when
   both its result ledger and Claude review ledger contain the expected PASS
   decision and the final closeout contains the same decision;
4. records no new numerical or scientific conclusion from the JSON top-level
   decision field.

No vendored student source may be edited.  No `.localsource/filterflow` mutation
is allowed.  No tolerance or fixture may be changed.

## Planned Evidence After Repair

Commands:

```bash
python -m py_compile experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_student_repetition_tf.py
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_student_repetition_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_common_model_suite_v2_student_repetition_tf --validate-only
```

The first student command may run only after Claude reviews this amendment to
PASS.

## Decision State

review_round: 1
open_material_blockers: none
next_allowed_action: run repaired student repetition evidence and validation

## Claude Review

Claude worker review returned `PASS`.

Review summary:

- the repair is safe as scoped because stale JSON decisions are accepted only
  when the phase result ledger, Claude review ledger, and final closeout contain
  the expected PASS decision;
- the repair does not weaken tolerance, fixture, scalar, branch, comparator,
  gradient, student, or oracle boundaries;
- the numerical runner logic downstream remains under the frozen V2 contracts.

## Implementation

Implemented in
`experiments/dpf_implementation/tf_tfp/runners/run_common_model_suite_v2_student_repetition_tf.py`.

The patch changed only preflight closure verification.  It added reviewed phase
ledger paths and requires the expected phase PASS string in the result ledger,
Claude review ledger, and final overnight closeout.
