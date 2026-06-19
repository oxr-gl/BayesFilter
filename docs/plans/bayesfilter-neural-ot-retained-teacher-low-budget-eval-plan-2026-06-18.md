# Experiment plan: retained-teacher Sinkhorn low-budget heldout evaluation

## Question
On the current deterministic LGSSM envelope, does the minimal retained-teacher Sinkhorn warm-start student improve heldout teacher-cloud fidelity relative to zero initialization when the corrective Sinkhorn budget is intentionally small (`K_corr = 5` and `10`), i.e. in the regime where warm starts are supposed to matter?

## Mechanism being tested
This experiment keeps the same retained-teacher setup as the earlier heldout rung but changes the promotion target to the low-budget regime:
- train the minimal student on the train split of the retained-teacher dataset,
- deploy predicted canonicalized `(log_u, log_v)` as the retained Sinkhorn initialization,
- compare corrected student replay against zero-init replay on heldout clouds,
- treat low corrective budgets as the primary scientific/engineering question.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: heldout teacher-cloud fidelity at low corrective budgets
- Seed(s): training seed 20260618; teacher-data seeds inherited from upstream artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 5 minutes CPU-only
- Envelope: LGSSM teacher-data artifact from `retained_teacher_sinkhorn_teacher_data_2026-06-18.json`; heldout split only for evaluation
- Corrective budgets: primary budgets `5` and `10`; budget `20` retained as explanatory-only context

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same heldout clouds, same epsilon, same cost, and same budget-specific tolerance floor.

### Primary criterion
At budgets `K_corr = 5` and `10`, the student-warm-started corrected route should have mean heldout teacher-cloud RMSE no worse than zero-init while still satisfying the declared residual envelopes.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond the declared budget-specific tolerance floor,
- training fails to reduce train latent loss,
- student worse than zero-init on mean heldout teacher-cloud RMSE at either primary budget.

### Explanatory-only diagnostics
- budget `20` comparison,
- train/heldout latent loss,
- max teacher-cloud RMSE,
- count of heldout examples where student beats zero-init.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad deployment fitness,
- superiority at larger corrective budgets,
- or generalization beyond the current LGSSM heldout split.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at budgets `5` and `10`
- heldout max residual, student vs zero-init, at budgets `5` and `10`
- heldout student-better-or-equal count at budgets `5` and `10`

Secondary:
- budget `20` teacher-cloud RMSE comparison
- final train latent loss
- heldout latent loss

Sanity checks:
- CPU-only manifest
- deterministic heldout example count > 0
- training loss decreases from initialization
- budget-specific tolerance floors are recorded in the artifact

## Expected failure modes
- the tiny dataset is too small to support a stable benefit claim,
- the student helps only at one budget but not the other,
- replay remains numerically fine but the effect size is too small to justify a next-step claim,
- the apparent gain is driven by only one heldout example.

## What would change our mind
- If student loses at either primary budget, keep the route as plumbing-plus-diagnostic evidence only.
- If student wins at `5` but ties or loses at `10`, treat the effect as narrower than hoped.
- If student wins at both `5` and `10`, advance to a larger heldout dataset or a modest model/data expansion while keeping claims local.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_LOW_BUDGET_FOLLOWUP`

Checked risks:
1. **Moving the goalposts unfairly** — addressed by explicitly restating the engineering question as low-budget acceleration, not general superiority.
2. **Silent tolerance relaxation** — budget-specific tolerance floors are declared up front and recorded in the artifact.
3. **Proxy metric drift** — the primary metric remains teacher-cloud RMSE on heldout examples, not latent loss.
4. **Over-claiming from tiny data** — any pass remains local evidence only and justifies only a larger follow-up rung.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_tf
```

## Interpretation rule
- If student mean heldout RMSE is less than or equal to zero-init at both `K_corr = 5` and `10`, and residuals pass, the low-budget rung passes.
- If student loses at either primary budget, the low-budget rung fails.
- Budget `20` remains explanatory-only and does not veto the low-budget result.
