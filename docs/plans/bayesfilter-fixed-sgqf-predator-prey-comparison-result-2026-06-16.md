# Fixed-SGQF Predator-Prey Comparison Result

metadata_date: 2026-06-16
plan_reference: `docs/plans/bayesfilter-fixed-sgqf-predator-prey-comparison-plan-2026-06-16.md`
status: EXECUTION_COMPLETE

## Question

Can the repaired fixed-SGQF lane be admitted as a same-target comparison method
for the literature-backed predator-prey T20 family?

## Implemented result

### Adapter extension
Updated:
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`

Added:
- `tf_predator_prey_to_fixed_sgqf_model(...)`

This adapter:
- accepts the repo’s `PredatorPreySSM` family,
- preserves the target semantics already used by the lower-rung same-target
  deterministic comparison path,
- maps predator-prey into the current repaired additive-state fixed-SGQF lane as:
  - deterministic nonlinear transition mean `transition_mean(theta, x_prev)`,
  - additive Gaussian `process_covariance`,
  - direct state observation with Gaussian `observation_covariance`.

### Focused predator-prey comparison tests
Updated:
- `tests/highdim/test_p47_predator_prey_filtering.py`

Added a new same-target fixed-SGQF diagnostic value test for the predator-prey
T20 family.

## Verification run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p47_predator_prey_filtering.py \
  tests/highdim/test_p51_predator_prey_production_tuning.py
```

Observed:
- `11 passed, 2 warnings`

## What is now supported

1. The repaired fixed-SGQF lane now has one admitted literature-backed nonlinear
   family beyond affine:
   - **predator-prey T20**.
2. The predator-prey adapter is same-target in the value-path sense used by the
   current lower-rung deterministic comparison stack.
3. Fixed SGQF can now be discussed alongside the existing predator-prey
   lower-rung deterministic reference/closure evidence without changing target
   semantics.

## What is not yet supported

1. No production predator-prey fixed-SGQF claim.
2. No fixed-SGQF predator-prey gradient/score comparison claim yet.
3. No statement that predator-prey admission implies admission for spatial SIR,
   generalized SV, actual SV, or the DPF/range-bearing streams.

## Interpretation

Predator-prey T20 was the right first literature-backed family beyond affine.
It is low-dimensional, genuinely nonlinear, and structurally aligned with the
repaired additive-state fixed-SGQF lane. The adapter could therefore be added
without weakening target semantics.

This makes predator-prey the first clear non-affine literature family where
fixed SGQF is now admitted honestly.

## Decision table
| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| admit predator-prey T20 as the first literature-backed non-affine fixed-SGQF family | satisfied | no target-change veto triggered | gradient/production-scope follow-up remains open | use predator-prey as the next family anchor in the broader fixed-SGQF comparison program | no broader family admission or production claim |

## Recommended next step
The next clean expansion after predator-prey is likely **KSC SV surrogate** or a
similarly well-scaffolded literature-backed family, not the full blocked roster.
Predator-prey should now be carried into the broader fixed-SGQF comparison
closeout as the first admitted non-affine literature-backed family.
