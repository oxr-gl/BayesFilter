# Phase 5 Executable Refresh: Structural Adapter Narrowing

Date: 2026-07-01

## Status

`EXECUTABLE_REFRESH_PENDING_REVIEW`

## Purpose

Narrow Phase 5 to the smallest implementation step that makes measurable,
reviewable progress toward generic nonlinear-SSM likelihood / analytical-
gradient support without silently widening target or API claims.

## Exact Files To Modify

Implementation:

- `bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py`

Focused tests:

- `tests/test_nonlinear_benchmark_models_tf.py`
- `tests/test_fixed_sgqf_values_tf.py`

## Exact Implementation Scope

1. Extend `TFFixedSGQFStructuralAdapterResult` so the adapter returns explicit
   reviewed-admission metadata rather than only a boolean eligible flag.

2. Make `tf_structural_to_fixed_sgqf_model(...)` support the exact-eligible
   affine structural lane generically by converting affine structural models into
   `TFFixedSGQFAffineModel`.

3. Reclassify the existing model-C path as an **approximate-eligible structural
   Gaussian-projection lane**, not an exact-eligible lane.

4. Keep model-B structurally ineligible under the current adapter and make the
   ineligibility reason explicit rather than silent.

5. Do **not** change `tf_fixed_sgqf_filter(...)`, `tf_fixed_sgqf_score(...)`,
   `posterior_adapter.py`, or `highdim/score_api.py` in this refresh.

## Scientific / Contract Boundaries Preserved

- No new exact-target claim for model C.
- No claim that the structural adapter is now generic for every nonlinear SSM.
- No claim that direct-likelihood SGQF is wired through the generic SGQF runtime.
- No new analytical-gradient admission beyond existing reviewed seams.
- No top-level API, HMC, production, or benchmark-promotion claim.

## Focused Checks To Run

CPU-only / local checks only:

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py \
  tests/test_fixed_sgqf_integration_tf.py
```

```bash
python -m compileall -q \
  bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py
```

```bash
git diff --check -- \
  bayesfilter/nonlinear/fixed_sgqf_structural_adapter_tf.py \
  tests/test_nonlinear_benchmark_models_tf.py \
  tests/test_fixed_sgqf_values_tf.py
```

## Expected Outcomes

- Affine structural models become explicit exact-eligible adapter routes.
- Model C becomes explicit approximate-eligible, preventing silent exact-target
  overclaim.
- Model B remains blocked/ineligible under the current adapter, preserving
  fail-closed semantics.
- The adapter result itself becomes more useful for later Phase 6/7 validation
  artifacts.
