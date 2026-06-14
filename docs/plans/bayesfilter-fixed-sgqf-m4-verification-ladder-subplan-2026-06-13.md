# Fixed-SGQF M4 Subplan: Verification Ladder And Negative Paths

metadata_date: 2026-06-13
phase: M4
status: READY_FOR_IMPLEMENTATION

## Objective

Encode the Fixed-SGQF claims and non-claims as a compact automated verification ladder.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the automated tests cover both the behavior the Fixed-SGQF lane claims and the behavior it explicitly forbids? |
| Baseline/comparator | p47 worked examples, same-scalar finite-difference rule, and implementation conventions; existing nonlinear TF unit/integration test patterns. |
| Primary pass criterion | The SGQF tests cover toy/worked examples, affine exactness, nonlinear finite values, same-branch score checks, branch-veto behavior, and forbidden repair/augmentation paths. |
| Veto diagnostics | Important non-claims are untested; negative-path behavior is only described in prose; tests allow hidden jitter/floor/clipping repair or additive-noise augmentation to slip through. |
| Not concluded | No production-readiness or benchmark-program admission claim. |

## Tasks

1. Add focused SGQF tests for the toy GHQ/sparse-grid examples that anchor the implementation contract.
2. Add affine exactness, the p47 one-step value-path oracle, and small nonlinear finite-value tests if not already present from M2.
3. Add same-branch finite-difference score checks if not already present from M3.
4. Add explicit negative-path tests for branch veto, forbidden repair, and no-state-augmentation behavior.
5. Keep the test ladder compact and targeted; do not explode into program-wide benchmark artifacts.

## Required Checks

- `pytest -q tests/test_fixed_sgqf_tf.py tests/test_fixed_sgqf_values_tf.py tests/test_fixed_sgqf_scores_tf.py tests/test_fixed_sgqf_branch_contract_tf.py`
- `rg -n "augmentation|jitter|floor|clip|veto" tests/test_fixed_sgqf_*.py`
