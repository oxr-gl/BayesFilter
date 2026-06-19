# Experiment plan: retained-teacher Sinkhorn expanded-data low-budget evaluation

## Question
Does the low-budget heldout benefit of the retained-teacher Sinkhorn warm-start student survive a modest expansion of the teacher-data artifact, using a larger train/heldout seed split on the same deterministic LGSSM envelope?

## Mechanism being tested
This experiment scales up the existing retained-teacher route without changing the mathematical object:
- generate a larger retained-teacher dataset on the same LGSSM family,
- train the same minimal DeepSets-style student,
- evaluate the same low-budget heldout criterion (`K_corr = 5` and `10`),
- check whether the earlier low-budget win persists after increasing the train and heldout seed coverage.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: robustness of the low-budget heldout effect under modest dataset expansion
- Seed(s): expanded deterministic train and heldout seed sets declared in the artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 10 minutes CPU-only
- Envelope: same LGSSM fixture family, same epsilon, same teacher object, larger train/heldout split only
- Corrective budgets: primary budgets `5` and `10`; `20` explanatory-only

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same expanded heldout clouds, same epsilon, same cost, same budget-specific tolerance floors.

### Primary criterion
At budgets `K_corr = 5` and `10`, student-warm-started replay should have mean heldout teacher-cloud RMSE no worse than zero-init while satisfying the declared residual envelopes on the expanded heldout set.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond the declared budget-specific tolerance floors,
- training fails to reduce train latent loss,
- student worse than zero-init on mean heldout teacher-cloud RMSE at either primary budget,
- expanded artifact captures too few heldout examples to be meaningfully broader than the original rung.

### Explanatory-only diagnostics
- budget `20` comparison,
- train/heldout latent loss,
- heldout example-level better-or-equal counts,
- runtime.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad deployment fitness,
- generalization beyond the current LGSSM family,
- or superiority at larger corrective budgets.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at budgets `5` and `10`
- heldout max residual, student vs zero-init, at budgets `5` and `10`
- heldout student-better-or-equal count at budgets `5` and `10`

Secondary:
- budget `20` comparison
- final train latent loss
- heldout latent loss
- expanded train/heldout example counts

Sanity checks:
- CPU-only manifest
- expanded artifact has larger heldout coverage than the original artifact
- training loss decreases from initialization
- budget-specific tolerance floors are recorded

## Expected failure modes
- the low-budget effect disappears under a slightly broader heldout split,
- the minimal student is too weak to use the extra train data effectively,
- the heldout split becomes harder and exposes overfitting to the earlier tiny artifact,
- residual envelopes remain fine but the effect size collapses.

## What would change our mind
- If the effect survives the expanded heldout split, the next justified step is a modest architecture/data ablation.
- If the effect disappears, keep the current route as a working proof-of-concept but not yet a robust low-budget result.
- If only one budget survives, narrow the claim to that budget rather than broadening it.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_MODEST_SCALE_UP`

Checked risks:
1. **Scope drift** — expansion changes only the seed coverage, not the mathematical object or baseline.
2. **Changing too many things at once** — the student architecture and training loop remain fixed.
3. **Tiny-sample over-interpretation** — the point of this rung is exactly to test whether the earlier low-budget result was fragile.
4. **Silent criterion change** — the primary criterion remains the same low-budget heldout RMSE comparison.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_expanded_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_expanded_tf
```

## Interpretation rule
- If student mean heldout RMSE is less than or equal to zero-init at both `K_corr = 5` and `10` on the expanded heldout split, the low-budget effect survives the modest scale-up.
- If student loses at either primary budget, the scaled-up robustness rung fails.
- Budget `20` remains explanatory-only.
