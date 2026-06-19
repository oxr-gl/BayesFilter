# Fixed-SGQF Predator-Prey Gradient Testing Plan

metadata_date: 2026-06-16
program_id: fixed-sgqf-predator-prey-gradient-testing
status: EXECUTION_READY

## Purpose

This plan governs predator-prey fixed-SGQF testing that reuses the repo’s
existing Zhao-Cui and DPF gradient-testing patterns.

The goal is to move predator-prey fixed-SGQF from:
- same-target value-path admissibility only,

to:
- same-target dense-reference value correctness,
- accepted-branch same-scalar gradient correctness against centered finite
  differences,
- explicit blocked comparability when branch identity changes,
- explicit nonclaims.

## Governing references

### Predator-prey same-target reference and comparison context
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_predator_prey_production_tuning.py`
- `docs/plans/bayesfilter-fixed-sgqf-predator-prey-comparison-result-2026-06-16.md`

### Zhao-Cui patterns to reuse
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_p30_fixed_branch_gradient_tables.py`

### DPF semantics / same-scalar patterns to reuse
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- DPF fixed-branch / FD contract artifacts under `docs/plans/`

### Fixed-SGQF same-branch contract to reuse
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_VALUE_AND_GRADIENT_TESTING`

Risks:
1. using CUT4 as the truth row instead of the same-target dense reference,
2. comparing gradients across changed branches,
3. promoting finite value or finite score into production or HMC claims,
4. duplicating predator-prey dynamics inconsistently between value and
   derivative paths.

## Evidence contract

Question:

Does predator-prey fixed-SGQF compute the same declared predator-prey filtering
scalar as the existing same-target dense lower-rung reference, and does its
analytic fixed-branch score agree with accepted-branch centered finite
differences for that same scalar?

Primary value comparator:
- `_dense_reference(order=7)` in `tests/highdim/test_p47_predator_prey_filtering.py`

Primary gradient comparator:
- centered finite difference of the exact same fixed-SGQF log-likelihood scalar.

Promotion conditions:
- scalar explicitly identified,
- same observations,
- same cloud,
- same branch config,
- same parameterization,
- same accepted branch signature for base / plus / minus rows,
- analytic score and FD agree within predeclared tolerance.

Veto / block conditions:
- branch signatures differ,
- plus or minus leaves the accepted branch,
- scalar identity changes,
- tolerances are loosened after inspecting results.

What will not be concluded:
- no production predator-prey fixed-SGQF claim,
- no HMC readiness claim,
- no nonlinear-preconditioning usefulness claim,
- no broader family admission claim.

## Files to modify

Primary:
- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`
- `tests/highdim/test_p47_predator_prey_filtering.py`

Optional only if needed:
- `tests/test_fixed_sgqf_scores_tf.py`

## Execution order

1. Write this plan artifact.
2. Add first-step and full-path predator-prey value correctness tests against the
   dense same-target reference.
3. Extend the predator-prey adapter to return `TFFixedSGQFDerivatives`.
4. Add one-parameter accepted-branch score-vs-FD test.
5. Add multistep full-vector score-vs-FD test.
6. Add FD-ladder / branch-validity test.
7. Run the focused predator-prey test suite.
8. Write the result artifact.

## Verification

Minimum verification:
- predator-prey value tests vs dense reference,
- predator-prey score tests vs accepted-branch FD,
- branch-validity / blocked-comparability test,
- rerun of `tests/highdim/test_p47_predator_prey_filtering.py` and adjacent
  predator-prey tuning tests.
