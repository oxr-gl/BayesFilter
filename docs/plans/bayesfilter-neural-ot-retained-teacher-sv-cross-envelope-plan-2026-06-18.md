# Experiment plan: retained-teacher Sinkhorn stochastic-volatility cross-envelope evaluation

## Question
Does the retained-teacher Sinkhorn warm-start effect observed on the LGSSM envelope survive the first cross-envelope expansion to the stochastic-volatility fixture family, under the same low-budget heldout evaluation contract?

## Mechanism being tested
This experiment keeps the retained-teacher warm-start architecture and evaluation logic fixed while changing the fixture family from LGSSM to stochastic volatility:
- generate a retained-teacher SV dataset,
- train the same minimal warm-start student,
- evaluate heldout teacher-cloud fidelity at low corrective budgets,
- compare student-warm-start replay against zero-init replay.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: first cross-envelope robustness check on a nonlinear observation model
- Seed(s): deterministic train and heldout seed sets declared in the artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 10 minutes CPU-only
- Envelope: stochastic-volatility fixture family only
- Corrective budgets: primary budgets `5` and `10`; `20` explanatory-only

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same heldout SV clouds, same epsilon, same cost, same budget-specific tolerance floors.

### Primary criterion
At budgets `K_corr = 5` and `10`, student-warm-started replay should have mean heldout teacher-cloud RMSE no worse than zero-init while satisfying the residual envelopes on the SV heldout split.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond budget-specific tolerance floors,
- training fails to reduce train latent loss,
- student worse than zero-init at either primary budget,
- artifact captures too few heldout SV examples to count as a real family expansion.

### Explanatory-only diagnostics
- budget `20` comparison,
- train/heldout latent loss,
- heldout student-better-or-equal count,
- runtime.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad cross-model generalization,
- or success on range-bearing / structural families.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at budgets `5` and `10`
- heldout max residual, student vs zero-init, at budgets `5` and `10`
- heldout student-better-or-equal count at budgets `5` and `10`

Secondary:
- budget `20` comparison
- final train latent loss
- heldout latent loss
- train/heldout example counts for the SV artifact

Sanity checks:
- CPU-only manifest
- deterministic heldout example count > 0
- train loss decreases from initialization
- budget-specific tolerance floors are recorded

## Expected failure modes
- the low-budget effect was specific to LGSSM and disappears on SV,
- SV teacher clouds are noisier and the tiny student underfits,
- heldout split is too small to support a robust claim,
- residuals remain fine but teacher-cloud improvement vanishes.

## What would change our mind
- If the student wins at both primary budgets, the retained-teacher effect has survived a meaningful first family expansion.
- If it loses at one or both budgets, keep the route as an LGSSM-local success only.
- If it ties exactly, treat that as encouraging but weaker than a positive improvement claim.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_FIRST_CROSS_ENVELOPE_RUNG`

Checked risks:
1. **Too large a family jump** — SV is chosen specifically because it changes observation nonlinearity without adding angle wrapping or deterministic completion structure.
2. **Changing model and contract simultaneously** — the retained-teacher route and low-budget contract stay fixed.
3. **Over-claiming from one extra family** — a pass on SV still does not justify broader nonlinear generalization claims.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_teacher_data_sv_tf
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_sv_tf
```

## Interpretation rule
- If student mean heldout RMSE is less than or equal to zero-init at both `K_corr = 5` and `10`, the first cross-envelope SV rung passes.
- If student loses at either primary budget, the cross-envelope rung fails.
- Budget `20` remains explanatory-only.
