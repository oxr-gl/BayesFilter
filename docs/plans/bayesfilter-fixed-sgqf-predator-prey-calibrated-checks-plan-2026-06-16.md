# Fixed-SGQF Predator-Prey Calibrated Checks Plan

metadata_date: 2026-06-16
program_id: fixed-sgqf-predator-prey-calibrated-checks
status: EXECUTION_READY

## Purpose

This plan governs a follow-up tightening of predator-prey fixed-SGQF testing.
The goal is to strengthen the current lower-rung predator-prey SGQF evidence by:

1. tightening value-path checks against the same-target dense lower-rung
   reference, and
2. strengthening the gradient checks into a clearer calibrated equality-style
   diagnostic under the same-scalar, accepted-branch contract.

This remains a lower-rung diagnostic strengthening pass, not a production or HMC
promotion pass.

## Governing references

### Predator-prey target and same-target lower-rung reference
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p51_predator_prey_production_tuning.py`

### Existing local predator-prey diagnostic lane
- `tests/highdim/test_p44_predator_prey_diagnostic.py`

### Reusable gradient-testing patterns
- `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py`
- `tests/highdim/test_p47_generalized_sv_equality.py`
- `tests/highdim/test_fixed_branch_derivatives.py`
- `tests/highdim/test_p30_fixed_branch_gradient_tables.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_dpf_filters.py`
- `tests/highdim/test_filtering_value_gradient_benchmark_gradient_semantics.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`

## Skeptical plan audit

Status target: `PASS_TO_PREDATOR_PREY_CALIBRATED_CHECKS`

Risks:
1. accidentally using CUT4 as the oracle instead of the dense same-target
   predator-prey reference;
2. overpromoting local gradient equality-style diagnostics into benchmark-grade
   certified reference-gradient claims;
3. comparing finite differences across changed branches;
4. distorting FD checks by using unscaled steps on differently scaled predator-
   prey parameters.

## Evidence contract

Question:

Does predator-prey fixed-SGQF match the same-target dense lower-rung value
reference closely enough to support a tighter lower-rung value gate, and does
its analytic fixed-branch score agree with centered finite differences strongly
enough to support a calibrated gradient diagnostic?

### Primary value comparator
- `_dense_reference(order=7)` in `tests/highdim/test_p47_predator_prey_filtering.py`

### Secondary deterministic comparator
- current structural closure comparators such as CUT4 may be used as supporting
  diagnostics only, not as the primary oracle.

### Primary gradient comparator
- centered finite difference of the exact same fixed-SGQF log-likelihood scalar.

### Promotion conditions
- same target,
- same observations,
- same cloud,
- same branch config,
- same parameterization `(r, K, a, s, u, v)`,
- plus/minus/base accepted-branch signatures identical,
- predeclared componentwise / normwise / directional tolerance checks met.

### Veto / block conditions
- branch identity changes,
- plus or minus leaves the accepted branch,
- parameter perturbations leave the declared parameter box,
- tolerances are loosened after inspecting results.

### What will not be concluded
- no production predator-prey fixed-SGQF claim,
- no HMC readiness claim,
- no nonlinear-preconditioning usefulness claim,
- no benchmark-grade reference-gradient promotion,
- no broader family admission claim.

## Files to modify

Primary:
- `tests/highdim/test_p47_predator_prey_filtering.py`
- `tests/highdim/test_p44_predator_prey_diagnostic.py`

Optional only if needed:
- `tests/highdim/test_p50_spatial_sir_predator_prey_ladder.py`

The narrowest implementation should avoid changing global registry or
reference-oracle policy in this pass.

## Execution order

1. Write this plan artifact.
2. Tighten the predator-prey SGQF same-target value checks in
   `test_p47_predator_prey_filtering.py`.
3. Tighten the predator-prey gradient diagnostic in
   `test_p44_predator_prey_diagnostic.py`.
4. Run the focused predator-prey test files.
5. Write the result artifact.

## Verification

Minimum verification:
- rerun `tests/highdim/test_p47_predator_prey_filtering.py`
- rerun `tests/highdim/test_p44_predator_prey_diagnostic.py`
- rerun any touched predator-prey ladder/tuning test

## Expected outcome

After implementation, the repo should have stronger predator-prey fixed-SGQF
value and gradient evidence that still respects the repo’s same-target,
fixed-branch, and non-overclaiming discipline.
