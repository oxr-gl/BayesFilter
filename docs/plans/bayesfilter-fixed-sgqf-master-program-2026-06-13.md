# Fixed-SGQF Master Program

metadata_date: 2026-06-13
program: fixed-sgqf-implementation
status: READY_FOR_IMPLEMENTATION
supervisor: Claude Code
reviewer: user-approved scope

## Objective

Replace the over-engineered Fixed-SGQF umbrella plan with an implementation-ready program that does only three things:

1. implements the Fixed-SGQF lane faithfully to `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p47-fixed-sgqf-expanded-companion-note-focus-preserved-rewritten-2026-06-12.tex`;
2. keeps implementation code on TensorFlow / TensorFlow Probability only, with no NumPy backend;
3. delivers good unit tests and integration tests.

## What This Supersedes

This master program supersedes `docs/plans/bayesfilter-fixed-sgqf-gradient-implementation-benchmark-plan-2026-06-11.md` as the execution plan for Fixed-SGQF work.

The older document may remain as historical background, but it is no longer the implementation driver.

## Binding Rules

- The source of truth for the Fixed-SGQF lane is the p47 scholarship note, especially:
  - the fixed Gaussian-surrogate / fixed-cloud / same-scalar lane definition;
  - the standard-normal GHQ rule family;
  - the branch tuple for same-scalar differentiation;
  - the Cholesky / solve / no-state-augmentation / symmetrize-then-veto conventions.
- The fixed cloud definition must include the sparse-grid level / active-index-set / combination-coefficient policy and stored-cloud representation; these are part of the declared scalar, not mere implementation detail.
- Implementation code must use TensorFlow / TensorFlow Probability only. NumPy is allowed in tests for assertions only, not as an algorithm backend.
- The first pass is a dedicated nonlinear Fixed-SGQF lane. It does not need to solve benchmark-matrix expansion, highdim program governance, smoothing, or adaptive sparse-grid design.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter implement a dedicated Fixed-SGQF value-and-score lane that is faithful to p47, TF/TFP-only in implementation, and supported by a compact serious test ladder? |
| Baseline/comparator | p47 scholarship note; existing TF nonlinear filtering structure in `bayesfilter/nonlinear/sigma_points_tf.py` and `bayesfilter/nonlinear/svd_sigma_point_derivatives_tf.py`; existing nonlinear test patterns. |
| Primary pass criterion | A dedicated Fixed-SGQF backend exists; it follows the p47 fixed-cloud / same-scalar / Cholesky-solve-veto contract; it exposes value and score entry points on the same declared branch; and the milestone unit/integration tests pass. |
| Veto diagnostics | Adaptive cloud changes inside the value path; eigen/SVD branch substituted for the declared Cholesky branch; additive noise handled by state augmentation; silent jitter/floor/clipping repair on the declared branch; NumPy backend code in the implementation module; gradient checks that cross branch identities. |
| Explanatory diagnostics | Toy worked examples, affine exactness tieouts, dense low-dimensional TF/TFP comparisons, same-branch finite differences, branch-veto traces, eager/compiled parity. |
| Not concluded | No adaptive sparse-grid refinement, no non-Gaussian carried state, no smoothing, no automatic highdim benchmark-matrix admission, and no claim that Fixed-SGQF recovers exact nonlinear filtering. |
| Artifacts | This master program, M1-M5 subplans, implementation code, and targeted tests. |

## Skeptical Plan Audit

Status: PASS.

- Wrong-scope risk: the old plan mixed implementation with governance and benchmark-program sprawl. This replacement keeps only the implementation-critical work.
- Wrong-backend risk: existing sigma-point code is structurally useful but not automatically p47-faithful. Reuse patterns, not hidden branch conventions.
- Proxy-risk: finite values alone are not enough; the lane must pass affine tieouts, same-branch score checks, and negative-path tests.
- Drift-risk: if implementation needs adaptive cloud updates, silent repair, or non-Cholesky factorization to work, the lane has left the p47 contract and must be re-planned explicitly.

## Phase Index

| Phase | Name | Subplan | Implementation target |
| --- | --- | --- | --- |
| M1 | Fixed Cloud And Branch Contract | `docs/plans/bayesfilter-fixed-sgqf-m1-fixed-cloud-branch-subplan-2026-06-13.md` | deterministic standardized cloud, merge/order policy, branch payload |
| M2 | P47-Faithful Value Recursion | `docs/plans/bayesfilter-fixed-sgqf-m2-value-recursion-subplan-2026-06-13.md` | prediction/update/log-likelihood recursion on the declared branch |
| M3 | Same-Scalar Analytic Score | `docs/plans/bayesfilter-fixed-sgqf-m3-analytic-score-subplan-2026-06-13.md` | first-order score on the same frozen branch |
| M4 | Verification Ladder And Negative Paths | `docs/plans/bayesfilter-fixed-sgqf-m4-verification-ladder-subplan-2026-06-13.md` | compact unit/integration test ladder plus forbidden-path coverage |
| M5 | API Integration Closeout | `docs/plans/bayesfilter-fixed-sgqf-m5-api-integration-closeout-subplan-2026-06-13.md` | stable nonlinear entry points and end-to-end deterministic integration |

## Expected Code Landing Zones

Primary implementation files:
- `bayesfilter/nonlinear/fixed_sgqf_tf.py`
- `bayesfilter/nonlinear/fixed_sgqf_derivatives_tf.py`
- `bayesfilter/nonlinear/__init__.py`

Likely supporting/fixture files:
- `bayesfilter/testing/nonlinear_models_tf.py`

Primary tests:
- `tests/test_fixed_sgqf_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`
- `tests/test_fixed_sgqf_scores_tf.py`
- `tests/test_fixed_sgqf_branch_contract_tf.py`
- `tests/test_fixed_sgqf_integration_tf.py`

## Execution Rule

This program intentionally avoids a multi-round Codex / Claude debate loop. If a milestone reveals a real mathematical conflict with the p47 lane, stop and narrow or re-plan that milestone explicitly instead of expanding governance.
