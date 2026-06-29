# Phase 2 Result: Derivation And Chapter Reconciliation

Date: 2026-06-29

## Status

`PASSED_LOCAL_RECONCILIATION`

## Phase Objective

Reconcile the reset memos, derivation note, and corrected chapter statements so
later code/test phases inherit one consistent actual-SV target description.

## Local Checks Run

```bash
rg -n "same-target|wrong scalar|Gaussian-closure|surrogate scalar|not a same-target approximation|actual-SV target and are therefore not acceptable stand-ins|same target as the transformed exact likelihood" docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex docs/chapters/ch28_nonlinear_ssm_validation.tex docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md
```

Observed:
- `ch33` states one transformed actual-SV target and explicitly rejects the
  Gaussian-closure route as same-target evidence while allowing it only as a
  surrogate scalar under stated local conditions;
- `ch35b` treats the Gaussian innovation scalar as a Gaussian-projection scalar
  and explicitly says its older actual-SV standalone use was wrong;
- `ch28` states that Gaussian-closure/additive-observation stand-ins are not
  acceptable actual-SV substitutes;
- the derivation note and chapter language align on:
  - one transformed target,
  - dense/direct-likelihood/Zhao--Cui same-target status,
  - augmented Gaussian-closure as a different scalar,
  - no claim that a corrected same-target augmented route already exists.

## Statement-classification table

| Artifact | Status | Reason |
| --- | --- | --- |
| `docs/plans/bayesfilter-actual-sv-single-target-lane-reset-memo-2026-06-28.md` | governing | freezes the one-target rule and demotes current Gaussian-closure Lane B |
| `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md` | compatible governing derivation | proves the transformed-law route distinctions in markdown artifact form |
| `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex` | governing | now contains the explicit transformed target derivation and surrogate-likelihood qualifier |
| `docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex` | compatible downstream method chapter | keeps Gaussian-projection scalar but denies same-target standing for the old actual-SV use |
| `docs/chapters/ch28_nonlinear_ssm_validation.tex` | compatible admission boundary | rejects Gaussian-closure/additive stand-ins for actual-SV validation |
| older two-lane / precursor artifacts | historical / diagnostic only | useful for traceability and mismatch evidence, but not live scalar authority |

## What Phase 2 settled

- There is no remaining contradiction among the live governing artifacts about the
  intended actual-SV scalar.
- The live mathematical story is now:
  - one transformed exact target,
  - same-target direct-likelihood and Zhao--Cui comparators,
  - Gaussian-closure route allowed only as a surrogate scalar under bounded local
    assumptions, not as same-target inference evidence.
- Later phases may classify code/tests/benchmarks against this reconciled story.

## What Phase 2 did not conclude

- It did not classify every current code/test/benchmark surface; that is Phase 3.
- It did not decide whether any corrected same-target augmented route exists; that
  is Phase 4.
- It did not validate value or gradient behavior.

## Handoff conditions check

Phase 3 may start because:
- no unresolved governing contradiction remains among the reset memo, derivation
  note, and corrected chapter statements;
- the mathematical role of Gaussian closure is now reconciled as surrogate, not
  same-target;
- the Phase 3 subplan already exists for refresh and review.

## Decision

`ADVANCE_TO_PHASE3_CODE_TEST_BENCHMARK_BOUNDARY_AUDIT`
