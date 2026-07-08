# Phase 6 Result: Same-Target Gradient Validation

Date: 2026-06-29

## Status

`PARTIAL_PASS_WITH_FOCUSED_SAME-TARGET_GRADIENT_EVIDENCE`

## Phase Objective

Validate gradients only after the underlying same-target value route has passed.

## Reviewed commands run

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  -k 'lane_a_fixed_sgqf_wrapper_score_matches_centered_finite_difference'
```

```bash
CUDA_VISIBLE_DEVICES=-1 pytest -q \
  tests/highdim/test_p43_sv_value_gradient_cut4_zhaocui.py \
  -k 'exact_transformed_zhaocui_matches_dense_value_and_diagnostic_score'
```

Observed:
- a combined focused command for Lane A + Zhao--Cui same-target checks was
  attempted first and was killed with exit code 137;
- rerunning the smallest reviewed same-target checks separately succeeded;
- the Lane A focused same-target gradient test passed;
- the focused Zhao--Cui exact-transformed value/diagnostic-score test passed.

## Gradient decision table

| Route / evidence surface | Route class | Primary criterion status | Veto status | Decision |
| --- | --- | --- | --- | --- |
| Lane A direct-likelihood Fixed-SGQF wrapper score | `SAME_TARGET_ACTUAL_SV` | focused same-target gradient check passed against centered finite difference | no target-mismatch veto seen | gradient-pass on focused reviewed subset |
| factorized scalar Zhao--Cui exact-transformed route | `SAME_TARGET_ACTUAL_SV` | focused exact-transformed value/diagnostic-score check passed | no target-mismatch veto seen | retained as reviewed same-target comparator |
| current augmented Gaussian-closure gradient surfaces | `SURROGATE_OR_GAUSSIAN_CLOSURE` / `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` | excluded from same-target Phase 6 validation | excluded by contract | no same-target gradient decision |
| KSC gradient surfaces | `KSC_ONLY` | not part of actual-SV same-target Phase 6 criterion | excluded by contract | remains separate |

## What Phase 6 settled

- Focused reviewed same-target gradient evidence now exists for the Lane A direct-
  likelihood route.
- Focused reviewed exact-transformed Zhao--Cui evidence remains consistent with its
  same-target comparator role.
- The contract-driven exclusion of current augmented Gaussian-closure gradient
  surfaces from same-target promotion evidence was preserved.

## What Phase 6 did not conclude

- This is not a full-file pass of all gradient-related tests in `p43`.
- It is not same-target gradient evidence for the current augmented Gaussian-
  closure family.
- It is not HMC readiness, production readiness, or benchmark-promotion evidence.

## Handoff conditions check

Phase 7 may start because:
- the surviving same-target routes now have focused reviewed value and gradient
  evidence sufficient for a bounded final route-status handoff;
- excluded surrogate/diagnostic/KSC families remain excluded by the contract;
- remaining uncertainty is breadth/completeness of larger test coverage, not the
  scalar identity of the reviewed same-target subset.

## Decision

`ADVANCE_TO_PHASE7_FINAL_DECISION_WITH_FOCUSED_REVIEWED_SAME-TARGET_EVIDENCE`
