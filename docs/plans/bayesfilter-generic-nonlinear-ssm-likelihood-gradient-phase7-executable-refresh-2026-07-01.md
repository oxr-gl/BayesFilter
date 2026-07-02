# Phase 7 Executable Refresh: Scoped Gradient Gate Narrowing

Date: 2026-07-01

## Status

`EXECUTABLE_REFRESH_PENDING_REVIEW`

## Purpose

Narrow Phase 7 to the smallest same-branch gradient-validation step that follows
cleanly from the Phase 6 value gate, without inventing new route claims.

## Exact Scope

Validate gradients only for lanes whose value gate passed at the reviewed claim
level:

1. **Affine structural exact-eligible lane**
   - score claim level: same-scalar analytical value/score evidence for the
     reviewed affine structural lane
   - comparator: same-branch finite differences on the same declared scalar
   - implementation backend: existing sigma-point analytical score tests for the
     affine structural fixture

2. **Model-C approximate-eligible lane**
   - score claim level: declared Gaussian-projection approximate-lane
     value/score evidence only
   - comparator: same-branch finite differences on the same declared approximate
     scalar
   - preserve explicit nonclaim: this is not exact-target gradient evidence
   - implementation backend: existing structural fixed-support sigma-point score
     tests for model C

3. **Model-B lane**
   - excluded from Phase 7 because it did not pass the Phase 6 value gate and
     remains structurally ineligible

4. **Fixed-SGQF one-step / scalar fixture lane**
   - score claim level: same-branch SGQF value/score evidence for the declared
     SGQF scalar fixtures only
   - comparator: same-branch finite differences on the same declared SGQF scalar
   - nonclaim: this is lane-local SGQF evidence, not generic direct-likelihood
     nonlinear-SSM admission

## Exact Files To Modify

No implementation files are required for this refresh.

Artifacts to write after runtime:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md`

## Exact Tests To Run

CPU-only focused checks only, narrowed to exact node IDs:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_p47_one_step_analytic_score_matches_oracle_and_fd \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_score_rejects_expected_branch_mismatch \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_same_branch_signature_tracks_failure_stage \
  tests/test_fixed_sgqf_scores_tf.py::test_fixed_sgqf_scalar_quadratic_multistep_score_matches_finite_difference_for_multiple_parameters \
  tests/test_fixed_sgqf_integration_tf.py::test_fixed_sgqf_score_api_is_deterministic_across_repeated_calls \
  tests/test_fixed_sgqf_integration_tf.py::test_fixed_sgqf_end_to_end_value_and_score_integration_on_p47_oracle \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_sigma_point_analytic_score_matches_finite_difference \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_svd_cut4_analytic_score_matches_finite_difference_and_oracle_score \
  tests/test_nonlinear_sigma_point_scores_tf.py::test_model_c_default_structural_fixed_support_score_matches_finite_difference
```

```bash
git diff --check -- \
  docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-result-2026-07-01.md
```

## Exact Interpretation Rules

- Passing affine same-branch score checks counts as **exact-target structural
  value/score evidence** for the reviewed affine structural lane only.
- Passing model-C same-branch score checks counts as **declared
  Gaussian-projection approximate value/score evidence** only. It must not be
  relabeled as exact-target gradient support.
- Passing the SGQF one-step / scalar fixture checks counts only as **lane-local
  same-branch SGQF scalar evidence**.
- Model-B remaining excluded from Phase 7 is a pass of the value-before-gradient
  and fail-closed admission rules.
- No HMC, top-level API, production, or default-policy claim is allowed from
  this refresh.

## Preserved Nonclaims

- no exact-target gradient claim for model C;
- no model-B score admission claim from this refresh;
- no generic direct-likelihood SGQF gradient claim;
- no HMC readiness;
- no top-level API promotion;
- no production/default claim.
