# Phase 5 Result: Same-Target Value Validation

Date: 2026-06-29

## Status

`PARTIAL_PASS_WITH_ROUTE-SCOPED_EVIDENCE`

## Phase Objective

Validate surviving same-target actual-SV value routes against the transformed
exact target only.

## Reviewed commands run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p41_exact_transformed_sv_zhaocui_ladder.py \
  -k 'exact_transformed_fixed_sgqf_matches_dense_on_tiny_panel or exact_transformed_zhaocui_factorized_tt_matches_dense or raw_native_sv_matches_exact_transformed_dense_after_jacobian'
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  -k 'exact_transformed_zhaocui_matches_dense_value_and_diagnostic_score or lane_a_fixed_sgqf_wrapper_score_matches_centered_finite_difference or ksc_fixed_sgqf_is_value_and_analytical_score_same_target_surrogate_evidence'
```

Observed:
- focused same-target value tests in `p41` passed for:
  - exact-transformed Fixed-SGQF versus dense,
  - factorized Zhao--Cui TT versus dense,
  - raw native SV versus exact-transformed dense after the explicit Jacobian relation;
- focused `p43` checks passed for:
  - exact-transformed Zhao--Cui value/diagnostic-score against dense,
  - Lane A Fixed-SGQF wrapper score against centered finite difference,
  - KSC fixed-SGQF value/analytical-score same-target evidence within the KSC surrogate family.

One broader command was attempted earlier across the full `p41` and `p43` files
and was killed with exit code 137. The focused reviewed subset above was used as
the smallest same-target value/gradient evidence path that completed within the
current environment.

## Decision table

| Route / evidence surface | Route class | Primary criterion status | Veto status | Decision |
| --- | --- | --- | --- | --- |
| dense exact-transformed reference | `SAME_TARGET_ACTUAL_SV` | anchor only | no veto seen | retained truth anchor |
| direct-likelihood Fixed-SGQF exact-transformed route | `SAME_TARGET_ACTUAL_SV` | focused same-target dense checks passed | no target-mismatch veto seen | value-pass on focused reviewed subset |
| factorized scalar Zhao--Cui exact-transformed route | `SAME_TARGET_ACTUAL_SV` | focused same-target dense checks passed | no target-mismatch veto seen | value-pass on focused reviewed subset |
| raw native SV after explicit Jacobian relation | `SAME_TARGET_ACTUAL_SV` within the tested relation | focused reviewed check passed | no target-mismatch veto seen | relation supported on focused reviewed subset |
| current augmented Gaussian-closure family | `SURROGATE_OR_GAUSSIAN_CLOSURE` | not part of same-target Phase 5 validation set | excluded by contract | no same-target value decision |
| KSC transformed family | `KSC_ONLY` | surrogate-family evidence passed in focused reviewed subset | not comparable to actual-SV same-target criterion | remains separate |

## What Phase 5 settled

- The surviving same-target comparator set from Phase 4 has focused reviewed
  value evidence against the transformed exact target.
- The contract-driven exclusion of the current augmented Gaussian-closure family
  from same-target value validation was preserved.
- The KSC family remains separate; its passing focused test is surrogate-family
  evidence only, not actual-SV same-target promotion evidence.

## What Phase 5 did not conclude

- This is not a full-file pass of all `p41` and `p43` tests.
- It is not a broad performance or scalability statement.
- It is not same-target evidence for the current augmented Gaussian-closure family.
- It does not by itself settle the Phase 6 gradient program beyond the focused
  reviewed subset already exercised.

## Handoff conditions check

Phase 6 may start because:
- the underlying same-target value routes have focused reviewed pass evidence;
- the excluded surrogate/diagnostic route classes remain excluded;
- the remaining uncertainty is about breadth/completeness of gradient coverage,
  not scalar identity of the surviving same-target routes.

## Decision

`ADVANCE_TO_PHASE6_SAME_TARGET_GRADIENT_VALIDATION_WITH_FOCUSED_REVIEWED_SUBSET`
