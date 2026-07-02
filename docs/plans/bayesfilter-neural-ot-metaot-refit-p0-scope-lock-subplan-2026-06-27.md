# P0 Subplan: Scope Lock And Baseline Freeze

Date: 2026-06-27

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter freeze the exact donor, route boundary, baseline implementation, and out-of-scope branches before starting the Meta OT-aligned refit? |
| Baseline/comparator | The completed source-faithful closure program, especially the P5/P6 verdicts, plus the current fixed-target retained-Sinkhorn implementation files and current annealed branch artifacts. |
| Primary pass criterion | A result artifact states the donor, the fixed-target route boundary, the baseline files, the current route classification, and the out-of-scope branches for this implementation program. |
| Veto diagnostics | Silent drift back to the annealed route; ambiguous donor; ambiguous baseline; treating public-distribution questions as settled by this program; treating current fixed-target route as already donor-faithful. |
| Explanatory diagnostics | File inventory and route labels only. |
| Not concluded | P0 does not yet change code or prove the one-half route works. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-metaot-refit-p0-scope-lock-result-2026-06-27.md` |

## Required Actions

1. Lock `Meta OT` as the donor for this program.
2. Lock the route boundary to the **fixed-target retained-Sinkhorn route only**.
3. Name the baseline files for the current route:
   - `experiments/dpf_implementation/tf_tfp/resampling/sinkhorn_warmstart_student_tf.py`
   - `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_tf.py`
   - `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_heldout_eval_tf.py`
4. Record the current classification from the completed closure program:
   - fixed-target retained-Sinkhorn = `fixed_adaptation with major extension components`
   - annealed four-potential route = `extension_or_invention`
5. Explicitly mark as out of scope:
   - annealed route refit,
   - UNOT switch,
   - direct-map / dynamic-path alternatives,
   - public-distribution licensing conclusions.

## Skeptical Audit

| Risk | Control |
| --- | --- |
| The program silently resumes work on the annealed branch | Route boundary explicitly names fixed-target retained Sinkhorn only. |
| Baseline confusion between current local route and donor route | Record current route classification verbatim from the source-faithful closure result. |
| Scope creep into policy or legal conclusions | Mark public-distribution questions out of scope; keep internal academic porting boundary only. |

## Gate

P0 passes only when the result artifact explicitly freezes donor, route, baseline files, and out-of-scope branches.
