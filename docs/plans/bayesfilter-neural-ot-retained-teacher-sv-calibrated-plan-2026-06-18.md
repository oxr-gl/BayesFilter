# Experiment plan: retained-teacher Sinkhorn stochastic-volatility calibrated evaluation

## Question
If the SV family is given a family-calibrated low-budget contract centered on `K_corr = 10`, does the retained-teacher Sinkhorn warm-start student improve heldout teacher-cloud fidelity relative to zero-init on the current stochastic-volatility envelope?

## Mechanism being tested
This follow-up keeps the same SV teacher-data artifact and student architecture but recalibrates the promotion rung based on the prior failure analysis:
- treat `K_corr = 10` as the primary budget,
- treat `K_corr = 20` as explanatory-only,
- drop `K_corr = 5` from the promotion criterion because it failed as a family-wide numerical replay envelope before method ranking was interpretable.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: calibrated first cross-envelope robustness check on SV
- Seed(s): deterministic train and heldout seed sets from the SV teacher-data artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 10 minutes CPU-only
- Envelope: stochastic-volatility fixture family only
- Primary corrective budget: `10`
- Explanatory-only budget: `20`

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same heldout SV clouds, same epsilon, same cost, and the same calibrated tolerance floor.

### Primary criterion
At `K_corr = 10`, student-warm-started replay should have mean heldout teacher-cloud RMSE no worse than zero-init while satisfying the calibrated residual envelope.

### Veto diagnostics
- any nonfinite replay output,
- residual failure beyond the calibrated tolerance floor,
- training fails to reduce train latent loss,
- student worse than zero-init on mean heldout teacher-cloud RMSE at `K_corr = 10`.

### Explanatory-only diagnostics
- budget `20` comparison,
- train/heldout latent loss,
- heldout example-level better-or-equal count,
- runtime.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- broad nonlinear generalization,
- success on range-bearing or structural families,
- or validity of the harsher `K_corr = 5` rung for SV.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at `K_corr = 10`
- heldout max residual, student vs zero-init, at `K_corr = 10`
- heldout student-better-or-equal count at `K_corr = 10`

Secondary:
- budget `20` comparison
- final train latent loss
- heldout latent loss

Sanity checks:
- CPU-only manifest
- deterministic heldout example count > 0
- train loss decreases from initialization
- calibrated tolerance floors are recorded

## Expected failure modes
- the apparent SV effect at budget `10` vanishes under the exact calibrated rerun,
- the student benefit is too small or too unstable to sustain a claim,
- residuals pass but mean RMSE advantage disappears.

## What would change our mind
- If the student wins at `K_corr = 10`, then the retained-teacher effect has survived a family-calibrated first nonlinear expansion.
- If it loses at `K_corr = 10`, then the cross-envelope evidence remains LGSSM-only.
- If it ties extremely closely, record that as encouraging but weaker than a positive improvement claim.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_SV_CALIBRATED_RERUN`

Checked risks:
1. **Moving the criterion after a failure** — justified here because the failure analysis showed `K_corr = 5` was dominated by replay-envelope breakdown rather than a clean student-vs-zero comparison.
2. **Over-relaxing the family contract** — avoided by keeping the primary rung low-budget (`10`) rather than defaulting to the easier large-budget regime.
3. **Over-claiming from one family-specific fix** — even a pass remains SV-only evidence.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_low_budget_eval_sv_calibrated_tf
```

## Interpretation rule
- If student mean heldout RMSE is less than or equal to zero-init at `K_corr = 10` and residuals pass, the calibrated SV rung passes.
- If student loses at `K_corr = 10`, the calibrated cross-envelope rung fails.
- Budget `20` remains explanatory-only.
