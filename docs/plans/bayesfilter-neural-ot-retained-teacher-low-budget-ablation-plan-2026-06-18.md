# Experiment plan: retained-teacher Sinkhorn low-budget warm-start ablation

## Question
On the expanded deterministic LGSSM teacher-data artifact, how much of the low-budget benefit comes from learning versus a simple heuristic warm-start, and does a slightly wider learned model improve on the current minimal learned student?

## Mechanism being tested
This experiment compares four warm-start regimes under the same heldout low-budget retained-teacher contract:
1. zero-init retained Sinkhorn,
2. heuristic warm-start,
3. learned-base warm-start (current minimal DeepSets student),
4. learned-wide warm-start (modestly wider DeepSets student).

All variants use the same retained teacher, same teacher-data artifact, same heldout split, and same low corrective budgets.

## Scope
- Variant: zero-init vs heuristic vs learned-base vs learned-wide
- Objective: attribute the low-budget effect and test whether a modestly wider model helps
- Seed(s): training seed 20260618; teacher-data seeds inherited from expanded artifact
- Training steps: 250 epochs, deterministic full-batch Adam for learned variants
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 10 minutes CPU-only
- Envelope: expanded LGSSM retained-teacher artifact only
- Corrective budgets: primary budgets `5` and `10`; `20` explanatory-only

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the expanded heldout split.

### Primary criterion
At budgets `K_corr = 5` and `10`, the learned-base warm-start should be no worse than both zero-init and heuristic on mean heldout teacher-cloud RMSE. The learned-wide model is exploratory and explanatory unless it clearly dominates the learned-base model at both primary budgets.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond declared budget-specific tolerance floors,
- learned variants fail to reduce train latent loss,
- learned-base worse than zero-init or heuristic at either primary budget.

### Explanatory-only diagnostics
- learned-wide vs learned-base differences,
- budget `20` comparison,
- train/heldout latent losses,
- heldout example-level better-or-equal counts.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad deployment fitness,
- cross-model generalization,
- or a universal architecture recommendation beyond this envelope.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE for zero-init / heuristic / learned-base at budgets `5` and `10`
- heldout max residual for each method at budgets `5` and `10`
- heldout example counts where learned-base is better-or-equal to zero-init and heuristic

Secondary:
- learned-wide comparison at budgets `5`, `10`, `20`
- train latent loss and heldout latent loss for learned variants
- budget `20` method ranking as explanatory context

Sanity checks:
- CPU-only manifest
- expanded artifact loaded successfully
- learned variants reduce train latent loss from initialization
- budget-specific tolerance floors are recorded

## Expected failure modes
- the heuristic explains most of the effect, leaving little learned advantage,
- the wider model overfits or offers no improvement,
- learned-base helps at `5` but not `10`,
- tiny heldout set still makes method ranking noisy.

## What would change our mind
- If heuristic matches learned-base at both primary budgets, the next step should prioritize understanding/feature ablation rather than widening the model.
- If learned-wide clearly beats learned-base, the next step can justify a modest architecture promotion within this envelope.
- If learned-base loses to heuristic or zero-init, the current learned route should not be promoted further without redesign.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_ATTRIBUTION_RUNG`

Checked risks:
1. **Changing data and model simultaneously** — avoided by reusing the expanded dataset and changing only the warm-start regime.
2. **Confusing learned benefit with heuristic benefit** — handled by including a heuristic comparator explicitly.
3. **Over-promoting a wider model** — learned-wide is explanatory unless it clearly dominates learned-base at the primary budgets.
4. **Silent criterion drift** — the primary question remains low-budget teacher-cloud fidelity on heldout examples.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_ablation_tf
```

## Interpretation rule
- If learned-base is no worse than zero-init and heuristic at both `K_corr = 5` and `10`, the learned effect remains supported.
- If heuristic ties learned-base, credit the heuristic strongly and avoid overclaiming learning-specific gains.
- If learned-wide clearly dominates learned-base at both primary budgets, it earns a local architecture-upgrade recommendation within this envelope.
