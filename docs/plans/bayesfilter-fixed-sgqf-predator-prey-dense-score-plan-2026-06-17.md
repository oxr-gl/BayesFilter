# Fixed-SGQF Predator-Prey Dense Score Plan

metadata_date: 2026-06-17
program_id: fixed-sgqf-predator-prey-dense-score
status: EXECUTION_READY

## Purpose

This plan governs the addition of a same-target dense predator-prey
value-and-score oracle so that we can measure:
- fixed-SGQF value and score vs dense value and score,
- UKF value and score vs dense value and score,
- and optionally SGQF vs UKF value/score as explanatory comparisons.

## Governing references

- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_native_generalized_sv_reference.py`
- `bayesfilter/highdim/score_api.py`
- current predator-prey SGQF/UKF comparison and calibrated-check artifacts under
  `docs/plans/`

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_DENSE_SCORE_IMPLEMENTATION`

Main risks:
1. autodiff through the dense predator-prey lower-rung reference may be noisy or
   unstable;
2. the repo’s broader benchmark metadata still does not treat predator-prey
   gradients as benchmark-grade exposed rows;
3. value/score direct SGQF-vs-UKF agreement must not be treated as truth without
   dense anchoring.

## Evidence contract

Question:

On the same predator-prey lower-rung target, how far are fixed-SGQF and UKF in
both value and score from the same-target dense lower-rung reference?

### Primary value comparator
- dense predator-prey lower-rung value from `_dense_reference(order=7)`.

### Primary score comparator
- dense predator-prey lower-rung score computed from the same dense scalar using
  TensorFlow autodiff.

### Promotion conditions
- same target,
- same observations,
- same parameterization `(r, K, a, s, u, v)`,
- same dense scalar for dense score,
- explicit absolute/relative value and score gaps,
- no target-changing surrogates.

### What will not be concluded
- no production predator-prey SGQF/UKF claim,
- no HMC readiness claim,
- no benchmark-grade promotion unless broader policy artifacts are revised,
- no broader family admission claim.

## Files to modify

Primary:
- `tests/highdim/test_p47_predator_prey_filtering.py`

## Execution order

1. Write this plan artifact.
2. Add a dense predator-prey value-and-score helper.
3. Add SGQF-vs-dense score comparison rows.
4. Add UKF-vs-dense score comparison rows.
5. Add SGQF-vs-UKF score comparison row if useful.
6. Run the focused predator-prey tests.
7. Write the result artifact.
