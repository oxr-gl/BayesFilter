# Phase 6 Executable Refresh: Structural Value-Gate Narrowing

Date: 2026-07-01

## Status

`EXECUTABLE_REFRESH_PENDING_REVIEW`

## Purpose

Narrow Phase 6 to the smallest value-validation step that tests the reviewed
structural-admission categories without inventing broader claims.

## Exact Scope

Validate only the structural SGQF value lanes that were explicitly classified in
Phase 5:

1. **Affine structural exact-eligible lane**
   - comparator: exact Kalman recovery
2. **Model-C approximate-eligible structural lane**
   - comparator: dense Gaussian-projection first-step reference, not exact-target
     evidence
3. **Model-B ineligible lane**
   - comparator: none; assert that it remains blocked/ineligible and is not
     silently promoted to a value lane

## Exact Files To Modify

No implementation files are required for this refresh.

Artifacts to write after runtime:

- `docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md`

## Exact Tests To Run

CPU-only focused checks only:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_integration_tf.py
```

```bash
git diff --check -- \
  docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase6-value-validation-result-2026-07-01.md \
  docs/plans/bayesfilter-generic-nonlinear-ssm-likelihood-gradient-phase7-gradient-validation-subplan-2026-07-01.md
```

## Exact Interpretation Rules

- Passing affine parity counts as **exact-target structural value evidence** for
  the reviewed affine SGQF adapter lane only.
- Passing model-C parity counts as **declared Gaussian-projection approximate
  value evidence** only. It must not be relabeled as exact-target support.
- Model-B remaining ineligible is a **pass of the fail-closed admission rule**,
  not a missing test.
- No gradient, HMC, top-level API, or production claim is allowed from this
  refresh.

## Preserved Nonclaims

- no generic direct-likelihood SGQF value claim;
- no generic nonlinear-SSM exact-target claim beyond the reviewed affine lane;
- no gradient admission;
- no HMC readiness;
- no top-level API promotion;
- no production/default claim.
