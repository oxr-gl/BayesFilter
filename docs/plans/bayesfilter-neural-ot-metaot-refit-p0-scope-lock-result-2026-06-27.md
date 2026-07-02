# P0 Result: Scope Lock And Baseline Freeze

Date: 2026-06-27

## Status

`PASS_P0_SCOPE_LOCK_READY_FOR_P1`

## Decision

`PASS_P0_SCOPE_LOCK_READY_FOR_P1`

The Meta OT-aligned implementation refit program is now locked to the correct donor, route boundary, baseline files, and exclusion set.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter freeze the exact donor, route boundary, baseline implementation, and out-of-scope branches before starting the Meta OT-aligned refit? |
| Baseline/comparator | The completed source-faithful closure program, especially the P5/P6 verdicts, plus the current fixed-target retained-Sinkhorn implementation files and current annealed branch artifacts. |
| Primary pass criterion | A result artifact states the donor, the fixed-target route boundary, the baseline files, the current route classification, and the out-of-scope branches for this implementation program. |
| Veto diagnostics | Silent drift back to the annealed route; ambiguous donor; ambiguous baseline; treating public-distribution questions as settled by this program; treating current fixed-target route as already donor-faithful. |
| Explanatory diagnostics | File inventory and route labels only. |
| Not concluded | P0 does not yet change code or prove the one-half route works. |

## Locked Donor

The donor for this implementation program is:
- **Meta OT**

This donor choice is inherited from:
- `docs/plans/bayesfilter-neural-ot-retained-teacher-source-faithful-p2-primary-donor-decision-result-2026-06-27.md`

UNOT is deferred and is not part of this implementation program unless a later explicit blocker reopens donor choice.

## Locked Route Boundary

This implementation program is limited to:
- the **fixed-target retained-Sinkhorn route only**.

It is explicitly **not** an annealed-route implementation program.

The governing boundary inherited from the completed closure program is:
- fixed-target retained-Sinkhorn is the correct Meta OT adaptation substrate,
- annealed four-potential work is a later extension branch.

## Baseline Files Frozen For Refit

The baseline local implementation files for this refit are:
- `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`
- `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`

These files define the current BayesFilter-native retained-Sinkhorn student, teacher-data, and heldout replay path that will be refit toward the Meta OT donor-core contract.

## Current Baseline Classification

Inherited from the completed source-faithful closure program:

- **current fixed-target retained-Sinkhorn route:** `FIXED_ADAPTATION_ROUTE_CLOSED_BUT_NOT_FULLY_SOURCE_FAITHFUL`
- **current annealed four-potential route:** `CUSTOM_EXTENSION_REQUIRED_SOURCE_FAITHFUL_CLOSURE_FAILED`

This means the current fixed-target route is the correct starting substrate, but it must not be mistaken for already donor-faithful Meta OT.

## Out Of Scope For This Program

The following are explicitly out of scope:

1. **Annealed route refit**
   - no work on the annealed four-potential learned-warmstart route inside this program.

2. **UNOT donor switch**
   - donor choice remains fixed unless a later explicit blocker forces reconsideration.

3. **Direct-map or dynamic-path alternatives**
   - OT-ICNN, FlowOT, TrajectoryNet, and related alternatives remain outside this program.

4. **Public-distribution license conclusions**
   - this program operates under the user-cleared internal academic modification/porting boundary only.
   - it does not settle public redistribution policy.

5. **Broad usefulness / production claims**
   - this program is about donor-aligned refit of the fixed-target route, not final deployment or production default decisions.

## Immediate Program Target

The implementation target is now narrowly defined:
- refit the current fixed-target retained-Sinkhorn route away from a BayesFilter-native full dual-pair default,
- toward a Meta OT-aligned one-half latent prediction route with teacher-side complementary recovery and donor-faithful objective-based training.

## What P0 Does Not Conclude

P0 does **not** conclude:
- that the current student is already close enough,
- that the one-half route will work well empirically,
- that the donor-style objective path will be easy to add,
- or that the route will become source-faithful automatically once code changes begin.

P0 only locks the correct scope so the program stops drifting.

## Next Step

Advance to:
- `docs/plans/bayesfilter-neural-ot-metaot-refit-p1-target-recovery-subplan-2026-06-27.md`

P1 will freeze the exact one-half target, gauge/canonicalization rule, and teacher-side complementary recovery contract before the student/data refit proceeds.
