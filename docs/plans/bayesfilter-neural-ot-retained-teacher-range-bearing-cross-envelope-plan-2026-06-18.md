# Experiment plan: retained-teacher Sinkhorn range-bearing cross-envelope evaluation

## Question
Does the retained-teacher Sinkhorn warm-start effect survive the next cross-envelope expansion from LGSSM/SV into the range-bearing family, under a low-budget heldout evaluation contract that respects the family’s nonlinear observation geometry?

## Mechanism being tested
This experiment keeps the retained-teacher warm-start route fixed while changing the fixture family to range-bearing:
- generate a retained-teacher range-bearing dataset,
- train the same minimal warm-start student,
- evaluate heldout teacher-cloud fidelity at low corrective budgets,
- compare student-warm-start replay against zero-init replay.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: second cross-envelope robustness check on a nonlinear geometric observation model
- Seed(s): deterministic train and heldout seed sets declared in the artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 10 minutes CPU-only
- Envelope: range-bearing fixture family only
- Primary corrective budget: to be chosen after probing the replay envelope; expected to be at least `10`
- Explanatory-only budget: a larger corrective budget for context

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same heldout range-bearing clouds, same epsilon, same cost, and family-calibrated budget/tolerance settings.

### Primary criterion
At the chosen family-calibrated low budget, student-warm-started replay should have mean heldout teacher-cloud RMSE no worse than zero-init while satisfying the residual envelope.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond the calibrated tolerance floor,
- training fails to reduce train latent loss,
- student worse than zero-init on the primary heldout teacher-cloud RMSE.

### Explanatory-only diagnostics
- larger-budget comparison,
- train/heldout latent loss,
- heldout student-better-or-equal count,
- runtime.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad nonlinear generalization,
- or validity for structural AR(1) or other families.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at the calibrated low budget
- heldout max residual, student vs zero-init, at the calibrated low budget
- heldout student-better-or-equal count at the calibrated low budget

Secondary:
- higher-budget comparison
- final train latent loss
- heldout latent loss
- train/heldout example counts for the range-bearing artifact

Sanity checks:
- CPU-only manifest
- deterministic heldout example count > 0
- train loss decreases from initialization
- calibrated tolerance floors recorded in the artifact

## Expected failure modes
- the retained-teacher effect disappears under angle-bearing geometry,
- replay envelope becomes much harsher than SV and requires more correction budget,
- heldout split is too small to support a robust claim,
- the simple student underfits the higher-dimensional state geometry.

## What would change our mind
- If student wins at the calibrated primary budget, the retained-teacher effect has survived a more demanding geometric family.
- If it loses, the current cross-envelope evidence remains limited to LGSSM and calibrated SV.
- If the envelope probe shows the family needs materially larger budgets, we should calibrate first rather than forcing a misleadingly harsh contract.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_RANGE_BEARING_PROBE_AND_RUNG`

Checked risks:
1. **Too much family complexity at once** — range-bearing is explicitly treated as a calibration-first family because of angle wrapping and 4D state geometry.
2. **Silent reuse of an LGSSM/SV budget** — the primary budget is intentionally left to the probe phase rather than assumed.
3. **Over-claiming from a pass** — even success would remain range-bearing-local evidence only.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_range_bearing_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_range_bearing_tf
```

## Interpretation rule
- If student mean heldout RMSE is less than or equal to zero-init at the calibrated primary budget and residuals pass, the range-bearing rung passes.
- If student loses at the calibrated primary budget, the range-bearing rung fails.
- Any larger budget remains explanatory-only.
