# Fixed-SGQF M1 Subplan: Fixed Cloud And Branch Contract

metadata_date: 2026-06-13
phase: M1
status: READY_FOR_IMPLEMENTATION

## Objective

Define the fixed sparse-grid cloud substrate and deterministic branch payload before the filtering recursion is implemented.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we build a deterministic standardized-Gaussian Fixed-SGQF cloud with stable merge/order semantics and a branch payload that freezes the same scalar before evaluation? |
| Baseline/comparator | p47 fixed-lane definition, GHQ-family discussion, merged-cloud construction, and same-scalar branch tuple; structural validation patterns from `bayesfilter/nonlinear/sigma_points_tf.py`. |
| Primary pass criterion | A dedicated TF module constructs the declared GHQ-family cloud, applies deterministic duplicate-merge / zero-weight / ordering rules, and emits a stable branch payload without any NumPy backend path. |
| Veto diagnostics | Rule family differs from the declared GHQ ladder; merge/order policy is implicit or data-dependent; branch payload omits structure needed for same-scalar checks; NumPy backend logic appears in implementation code. |
| Not concluded | No filtering recursion, no score path, and no end-to-end correctness claim. |

## Tasks

1. Create `bayesfilter/nonlinear/fixed_sgqf_tf.py` as the dedicated Fixed-SGQF implementation module.
2. Implement the standardized one-dimensional GHQ family needed for the first-pass lane, starting from the p47 ladder (`I_1`, `I_2`, `I_3`), and freeze the sparse-grid level / active-index-set / combination-coefficient policy used to assemble the stored cloud.
3. Implement deterministic duplicate-merge, zero-weight handling, node ordering, stored-cloud representation, weight-total diagnostics, and signed-weight diagnostics for the assembled cloud.
4. Define a serializable branch payload that freezes the cloud, stored representation, one-dimensional rule family, level/index policy, merge tolerance policy, zero-weight rule, node ordering, observation preprocessing policy, initial-condition policy, branch thresholds, factor convention, veto policy, and accepted/failure stage-time pattern.
5. Export the cloud/branch helpers through `bayesfilter/nonlinear/__init__.py` only after the unit checks pass.

## Required Checks

- `pytest -q tests/test_fixed_sgqf_tf.py`
- `rg -n "import numpy|from numpy" bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `rg -n "fixed_sgqf" bayesfilter/nonlinear/__init__.py tests/test_fixed_sgqf_tf.py`
