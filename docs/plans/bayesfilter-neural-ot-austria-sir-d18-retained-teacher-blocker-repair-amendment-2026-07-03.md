# Austria SIR d18 Retained-Teacher Teacher-Generation Blocker-Repair Amendment

Date: 2026-07-03

## Status

`DRAFT_FOR_VISIBLE_EXECUTION`

## Trigger

The first governed Austria SIR d18 retained-teacher smoke-test execution failed
before any zero-init probe or donor-aligned replay evaluation could run:
- `FloatingPointError: Sinkhorn row residual exceeded tolerance envelope`
- raised during teacher coupling generation in
  `experiments/dpf_implementation/tf_tfp/runners/run_retained_teacher_sinkhorn_teacher_data_austria_sir_d18_tf.py`

This blocks the smoke-test plan at the teacher-generation stage and requires a
reviewed repair amendment before further execution.

## Blocker Classification

`AUSTRIA_SIR_D18_TEACHER_GENERATION_OT_NUMERICAL_STABILITY_BLOCKER`

The current blocker is interpreted as a teacher-generation / Sinkhorn numerical
stability issue on the Austria SIR d18 family, not as evidence against the
retained-teacher idea, not as a student-training failure, and not as a
large-scale negative result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the Austria SIR d18 retained-teacher teacher-data artifact be made numerically stable by a bounded Sinkhorn teacher-generation repair without changing the model or over-claiming the result? |
| Baseline/comparator | The current failed Austria SIR d18 teacher-data runner with nominal settings (`epsilon=0.75`, `max_iterations=90`, `tolerance=1e-8`) and the prior SIR d18 Sinkhorn tuning blocker evidence from P8j. |
| Primary pass criterion | A result artifact either (a) identifies a bounded reviewed teacher-generation repair that yields a finite teacher-data artifact, or (b) preserves the blocker with exact first-failure diagnostics and the next justified human decision point. |
| Veto diagnostics | Changing the Austria SIR model/data; jumping ahead to student replay evaluation; silently relaxing tolerances; claiming usefulness, large-`N`, or production evidence from the repair itself; changing multiple repair knobs at once without a diagnostic baseline. |
| Explanatory diagnostics | State scale, pairwise cost scale, ESS ratio, source-weight perplexity, nominal residuals, runtime, and the first event at which failure appears. |
| Not concluded | No donor-aligned student usefulness claim, no `N=10000` claim, no GPU scaling claim, no production-readiness claim, and no parameterized-SIR claim. |
| Required artifact | `docs/plans/bayesfilter-neural-ot-austria-sir-d18-retained-teacher-blocker-repair-result-2026-07-03.md` |

## Prior Evidence To Reuse

The repo already contains a related SIR d18 Sinkhorn blocker-repair diagnostic in
P8j, where a scale-adaptive Sinkhorn epsilon emerged as a plausible repair
candidate after recording first-event cost statistics and residual behavior:
- `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8j-phase5b-sir-tuning-blocker-repair-result-2026-06-17.md`

This amendment may reuse that diagnostic logic as prior evidence for the repair
ordering, but it must not claim that the earlier LEDH OT repair is already
validated for retained-teacher teacher generation.

## Required Actions

1. **Add a diagnostic-first Austria SIR d18 teacher-generation probe.**
   The probe must stop at the first failing resampling event and record:
   - seed and time index,
   - ESS and ESS ratio,
   - source weight min/max,
   - source-weight perplexity,
   - state-dispersion summary,
   - pairwise cost mean and max,
   - nominal epsilon, tolerance, max iterations,
   - and, if a bounded probe succeeds, the resulting row/column residuals.

2. **Preserve the nominal baseline settings for the first diagnostic record.**
   The first recorded attempt must use the current nominal teacher settings so we
   know what failed before any repair is attempted.

3. **Test bounded repair candidates one at a time, in this order.**
   a. scale-adaptive epsilon tied to a documented cost statistic;
   b. larger Sinkhorn iteration cap;
   c. explicitly reviewed tolerance relaxation.

4. **Do not combine multiple new repair ideas in the first repair attempt.**
   The diagnostic should isolate the smallest change that plausibly explains the
   blocker.

5. **If a bounded repair yields a finite teacher coupling on the first failing event,**
   rerun the teacher-data generator under that reviewed repair and stop there.
   Do not proceed to zero-init probe or replay evaluation until the teacher-data
   artifact is successfully regenerated and recorded.

## Skeptical Audit Before Execution

Status: `PASSED_FOR_DIAGNOSTIC_FIRST_REPAIR`

Checked risks:
1. **Silent tolerance laundering** — prevented by recording the nominal failure
   first and requiring explicit documentation for any tolerance change.
2. **Changing too many knobs at once** — prevented by ordered single-candidate
   repair attempts.
3. **Drifting into model changes** — prevented by freezing Austria SIR d18 model,
   data-generation path, and student architecture.
4. **Overclaiming from a numerical repair** — prevented by treating any repair as
   teacher-generation stability evidence only until the teacher artifact exists.
5. **Losing the first-failure signature** — prevented by requiring a diagnostic
   artifact before implementing the repair.

## Command

```bash
# Stage A: diagnostic-first blocker characterization
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_generation_diagnostic_austria_sir_d18_tf

# Stage B: only if the diagnostic identifies a bounded reviewed repair candidate
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_austria_sir_d18_tf
```

## Interpretation rule
- If the nominal diagnostic already succeeds, the original blocker is reclassified
  as non-reproducible and the teacher-data runner may be rerun immediately.
- If the nominal diagnostic fails but a single bounded repair candidate succeeds,
  the next step is to rerun teacher-data generation under that exact repair.
- If no bounded repair candidate succeeds on the first diagnostic event, preserve
  the blocker and stop for a further reviewed amendment.
- In no case should this amendment by itself be interpreted as retained-teacher
  usefulness evidence.
