# Phase 3 Result: Code/Test/Benchmark Boundary Audit

Date: 2026-06-29

## Status

`PASSED_LOCAL_ROUTE_CLASSIFICATION`

## Phase Objective

Classify every relevant actual-SV code path, test surface, and benchmark artifact
as same-target, surrogate, diagnostic-only, KSC-only, or blocked pending new
derivation, so later implementation/rewrite work cannot drift by inertia.

## Local Checks Run

```bash
rg -n "exact transformed|same-target|Gaussian-closure|not exact transformed same-target admission|not direct actual-SV likelihood quadrature|KSC|lane_id|target" bayesfilter/highdim/sv_mixture_cut4.py tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py tests/test_actual_sv_two_lane_benchmark_script.py docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py
```

## Route-classification table

| Surface | Route class | Reason |
| --- | --- | --- |
| `exact_transformed_sv_scalar_dense_reference(...)` and panel dense reference in `sv_mixture_cut4.py` | `SAME_TARGET_ACTUAL_SV` | diagnostics target is exact transformed log-chi-square / factorized coordinatewise exact transformed SV |
| `exact_transformed_sv_independent_panel_fixed_sgqf_filter(...)` and score wrapper | `SAME_TARGET_ACTUAL_SV` | docstring and diagnostics say same-target direct likelihood reweighting; `lane_id` is `lane_a_direct_likelihood_quadrature` |
| `exact_transformed_sv_independent_panel_zhaocui_tt_filter(...)` and score wrapper | `SAME_TARGET_ACTUAL_SV` | wrapper consumes transformed observations with `ExactTransformedSVSSM`; diagnostics target is factorized coordinatewise exact transformed SV |
| `actual_transformed_sv_independent_panel_augmented_noise_fixed_sgqf_filter(...)` | `SURROGATE_OR_GAUSSIAN_CLOSURE` | target string is raw actual-SV augmented-noise Gaussian-closure approximate likelihood; non-claims explicitly deny same-target admission |
| `actual_transformed_sv_independent_panel_augmented_noise_dense_gaussian_closure_reference(...)` | `SURROGATE_OR_GAUSSIAN_CLOSURE` | dense Gaussian-closure scalar only; `lane_id` is `lane_b_augmented_noise_gaussian_closure` |
| `actual_transformed_sv_independent_panel_augmented_noise_ukf_filter(...)` and score wrappers | `SURROGATE_OR_GAUSSIAN_CLOSURE` | historical / Gaussian-closure approximate likelihood, not exact transformed same-target admission |
| `KSCMixtureTransformedSVSSM` and factorized KSC wrappers | `KSC_ONLY` | target string explicitly names finite Gaussian-mixture transformed-SV target; non-claims deny exact native SV likelihood |
| `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py` same-target SGQF and Zhao--Cui checks | `SAME_TARGET_ACTUAL_SV` | asserts exact-transformed target scopes for dense/SGQF/Zhao--Cui surfaces |
| `tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py` augmented-noise SGQF / dense checks | `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` | assertions themselves encode non-claims like `not exact transformed same-target admission` and `not direct actual-SV likelihood quadrature` |
| `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` KSC same-target surrogate evidence test | `KSC_ONLY` | test name and target are explicitly same-target only within the KSC surrogate family |
| `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` Lane A score checks | `SAME_TARGET_ACTUAL_SV` | `lane_id` asserted as `lane_a_direct_likelihood_quadrature` |
| `tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py` Lane B score checks | `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` | `lane_id` asserted as Gaussian closure; does not establish actual-SV same-target identity |
| `tests/test_actual_sv_two_lane_benchmark_script.py` | `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` | schema lock for historical two-lane script; keeps KSC rows separate but still preserves old lane framing for historical output |
| `docs/benchmarks/benchmark_actual_sv_two_lane_comparison.py` | `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` | explicit “Lane B augmented-noise Gaussian-closure” and separate KSC surrogate rows; historical comparison harness, not live same-target benchmark authority |

## What Phase 3 settled

- Current code surfaces already separate same-target exact-transformed routes from
  Gaussian-closure surrogate routes and from KSC-only routes at the diagnostic
  string level.
- The actual risk of drift is now concentrated in:
  - historical Lane-B test assertions being misread as promotion evidence;
  - historical benchmark harnesses being mistaken for same-target benchmark
    authority;
  - older comments and wrappers being reused without contract-aware relabeling.

## What Phase 3 did not conclude

- It did not decide whether any corrected same-target augmented route exists;
  that is Phase 4.
- It did not validate same-target values or gradients.
- It did not rewrite tests or benchmarks yet.

## Handoff conditions check

Phase 4 may start because:
- every relevant surface inspected in Phase 3 now has a route class;
- the route inventory distinguishes same-target, surrogate, KSC-only, and
  diagnostic-only evidence cleanly enough to support a route decision;
- the Phase 4 subplan already exists for refresh and review.

## Decision

`ADVANCE_TO_PHASE4_ROUTE_DECISION`
