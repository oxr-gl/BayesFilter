# Fixed-SGQF Predator-Prey UKF Comparison Plan

metadata_date: 2026-06-16
program_id: fixed-sgqf-predator-prey-ukf-comparison
status: EXECUTION_READY

## Purpose

This plan governs same-target predator-prey lower-rung comparison rows for fixed
SGQF vs UKF vs dense reference, for both value and gradient as far as the
current repo infrastructure truly supports.

## Governing references

- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p44_predator_prey_diagnostic.py`
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_p30_fixed_branch_gradient_tables.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_SGQF_UKF_COMPARISON`

Risks:
1. using UKF as the truth row instead of the dense same-target reference;
2. comparing SGQF-vs-UKF gradients before each side has its own admissible local
   gradient contract;
3. overpromoting local comparator success into production or universal ranking
   claims;
4. losing same-target semantics by drifting away from the current predator-prey
   lower-rung closure.

## Evidence contract

Question:

On the same predator-prey lower-rung target, how do fixed SGQF and UKF compare
against the dense same-target reference for value, and how should their gradient
comparisons be scoped under the repo’s current fixed-branch and FD-testing
contracts?

### Primary value comparator
- `_dense_reference(order=7)` in `tests/highdim/test_p47_predator_prey_filtering.py`

### Primary gradient comparators
- SGQF: centered FD of the same fixed-SGQF scalar under the accepted branch.
- UKF: current local CUT4-style autodiff/FD diagnostic only if explicitly kept as
  diagnostic and not promoted to reference-gradient truth.

### What will not be concluded
- no production predator-prey fixed-SGQF claim,
- no HMC readiness claim,
- no benchmark-grade reference-gradient promotion,
- no broader family admission claim.

## Files modified
- `tests/highdim/test_p47_predator_prey_filtering.py`

## Execution order

1. Write this plan artifact.
2. Add same-target UKF value rows against the dense reference.
3. Add SGQF-vs-UKF direct value row.
4. Keep gradient comparison scoped to what the current infrastructure supports.
5. Run the focused predator-prey tests.
6. Write the result artifact.
