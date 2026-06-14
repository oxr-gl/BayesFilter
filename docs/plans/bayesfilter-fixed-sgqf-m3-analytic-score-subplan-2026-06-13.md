# Fixed-SGQF M3 Subplan: Same-Scalar Analytic Score

metadata_date: 2026-06-13
phase: M3
status: READY_FOR_IMPLEMENTATION

## Objective

Implement first-order parameter derivatives of the declared Fixed-SGQF scalar on the same frozen branch.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we differentiate the exact declared Fixed-SGQF scalar while holding the cloud, merge/order rules, factor family, and veto path fixed? |
| Baseline/comparator | p47 same-scalar branch tuple, saved-branch contract, and analytical-gradient sections; derivative/test organization from `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`. |
| Primary pass criterion | Analytic scores agree with same-branch finite differences on small smooth valid fixtures, and the implementation rejects comparisons that cross branch identities or invalid branches. |
| Veto diagnostics | Finite differences are compared across different branch payloads; derivative code implicitly changes cloud or factor structure; nonfinite/blocked derivatives are emitted as if valid scores. |
| Not concluded | No Hessian support, no adaptive-gradient claims, and no HMC-readiness claim. |

## Tasks

1. Create `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py` for the SGQF score lane.
2. Implement first-order propagation for the declared scalar using the same structural order as the value path, with explicit derivative prerequisites for `D_x f`, `∂_i f`, `D_x h`, `∂_i h`, `\dot Q`, `\dot R`, `\dot m_0`, and `\dot P_0`, and keep the saved-branch contract aligned with the p47 branch record.
3. Reuse branch-payload fields from M1 so score checks can enforce same-scalar comparisons.
4. Add finite-difference and branch-mismatch tests in `tests/test_fixed_sgqf_scores_tf.py` and `tests/test_fixed_sgqf_branch_contract_tf.py`.
5. Ensure blocked or branch-invalid cases emit explicit diagnostics instead of fake gradients.

## Required Checks

- `pytest -q tests/test_fixed_sgqf_scores_tf.py`
- `pytest -q tests/test_fixed_sgqf_branch_contract_tf.py -k score`
- `rg -n "fixed_sgqf_derivatives|branch" bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py tests/test_fixed_sgqf_scores_tf.py`
