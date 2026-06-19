# Experiment plan: retained-teacher Sinkhorn heldout evaluation

## Question
Does the minimal retained-teacher Sinkhorn warm-start student improve or at least preserve heldout teacher-cloud fidelity relative to zero initialization at fixed corrective Sinkhorn budgets on the current deterministic LGSSM envelope?

## Mechanism being tested
This experiment tests the full retained-teacher route on heldout teacher-data examples:
- train the minimal DeepSets-style student on the train split of the retained-teacher dataset,
- deploy its predicted canonicalized `(log_u, log_v)` as the initialization of the retained corrective Sinkhorn solver,
- compare corrected student-warm-start replay against zero-init replay on heldout clouds,
- keep the teacher barycentric cloud as the reference object.

## Scope
- Variant: retained-teacher fixed-target Sinkhorn warm-start vs zero-init comparator
- Objective: heldout teacher-cloud fidelity at fixed corrective budgets
- Seed(s): training seed 20260618; teacher-data seeds already frozen in the upstream artifact
- Training steps: 250 epochs, deterministic full-batch Adam
- HMC/MCMC settings: N/A
- XLA/JIT mode: eager / default TensorFlow execution
- Expected runtime: under 5 minutes CPU-only
- Envelope: LGSSM teacher-data artifact from `retained_teacher_sinkhorn_teacher_data_2026-06-18.json`; heldout split only for evaluation
- Corrective budgets: 5, 10, 20

## Evidence Contract

### Exact baseline
Zero-initialized retained Sinkhorn replay on the same heldout clouds, same epsilon, same tolerance, same corrective budgets.

### Primary criterion
At the highest fixed budget (`K_corr = 20`), the student-warm-started corrected route should have mean heldout teacher-cloud RMSE no worse than zero-init, while still satisfying the same residual contract.

Budget-specific residual note:
- the evaluation uses stricter budgets with tolerance floors matched to the shorter corrective budget so the rung answers the intended question instead of failing solely because a very low-iteration replay is held to the teacher-generation tolerance.
- planned tolerance floors: `K_corr=5 -> 1e-5`, `K_corr=10 -> 1e-7`, `K_corr=20 -> 1e-8`.

### Veto diagnostics
- any nonfinite student/zero-init replay output,
- any residual failure (row, column, or total-mass) beyond the declared tolerance envelope,
- training fails to reduce train latent loss relative to initialization,
- student replay materially worse than zero-init on the primary heldout metric at `K_corr = 20`.

### Explanatory-only diagnostics
- runtime,
- latent train loss,
- latent heldout loss,
- per-budget improvement at lower budgets,
- count of heldout examples where student beats zero-init.

### What will not be concluded even if the run passes
- posterior correctness,
- HMC readiness,
- generalization beyond the current LGSSM/split,
- superiority at all budgets,
- promotion of the student to replace the retained teacher.

## Diagnostics
Primary:
- heldout mean teacher-cloud RMSE, student vs zero-init, at budgets 5/10/20
- heldout max residual, student vs zero-init, at budgets 5/10/20
- heldout student-better-or-equal count at each budget

Secondary:
- final train latent loss
- heldout latent loss
- heldout max teacher-cloud RMSE

Sanity checks:
- CPU-only manifest (`CUDA_VISIBLE_DEVICES=-1` before import)
- nonzero heldout example count
- deterministic train/heldout split counts inherited from teacher-data artifact
- training loss decreases from initialization

## Expected failure modes
- the student learns the latent target poorly because the dataset is tiny,
- the latent target improves train loss but not corrected teacher-cloud replay,
- lower budgets may be too small for either method to replay the teacher well,
- numerical issues in replay due to bad initial states or tolerance mismatch.

## What would change our mind
- If student-warm-start is worse than zero-init at `K_corr = 20`, keep the route as a plumbing success only and revise the architecture/data before claiming benefit.
- If student helps only at lower budgets but ties at `K_corr = 20`, treat that as encouraging but still local evidence.
- If residuals fail, debug the replay contract before any interpretation.

## Skeptical Audit Before Execution
Status: `PASSED_FOR_HELDOUT_RUNG`

Checked risks:
1. **Wrong baseline** — fixed by comparing only against zero-init on the same heldout clouds and same corrective budgets.
2. **Proxy metric promotion** — latent loss is explanatory only; teacher-cloud RMSE at fixed budget is the primary criterion.
3. **Teacher/object drift** — replay uses the same retained Sinkhorn object and teacher epsilon/tolerance from the teacher-data artifact.
4. **Silent residual trade** — residual failure is a veto, so an apparently better RMSE with broken constraints does not count.
5. **Over-claiming from tiny data** — the result is heldout-on-this-envelope only and cannot justify broader claims.

## Command
```bash
CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_retained_teacher_sinkhorn_heldout_eval_tf
```

## Interpretation rule
- If heldout student mean RMSE at `K_corr = 20` is less than or equal to zero-init and residuals pass, the rung passes as local evidence for the retained-teacher route on this envelope.
- If student is worse than zero-init at `K_corr = 20`, the rung fails as an effectiveness check even if training loss decreased.
- If lower budgets improve but the primary budget ties, record that as explanatory-only encouragement, not a promotion claim.
