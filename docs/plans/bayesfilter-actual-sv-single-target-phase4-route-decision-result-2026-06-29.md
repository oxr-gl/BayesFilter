# Phase 4 Result: Lane-B Route Decision

Date: 2026-06-29

## Status

`PASSED_RETIRED_AUGMENTED_INFERENCE_LANE`

## Phase Objective

Make one reviewed route decision for augmented-noise actual-SV inference under
the single-target rule.

## Local Checks Run

```bash
rg -n "same-target|wrong scalar|surrogate scalar|not exact transformed same-target admission|not direct actual-SV likelihood quadrature" bayesfilter/highdim/sv_mixture_cut4.py docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex
```

Observed:
- the current exact-transformed dense reference, direct-likelihood Fixed-SGQF
  route, and factorized scalar Zhao--Cui wrapper remain the only reviewed
  same-target comparator candidates;
- the current augmented-noise SGQF, dense Gaussian-closure, and historical UKF
  wrappers all explicitly deny exact transformed same-target admission and direct
  actual-SV likelihood quadrature;
- the current derivation note explicitly rejects same-target status for the
  augmented Gaussian-closure route and explicitly does **not** prove that a
  corrected same-target augmented route exists.

## Route-decision table

| Outcome candidate | Status | Reason |
| --- | --- | --- |
| Distinct same-target augmented route already exists | rejected | no reviewed artifact shows that a current augmented implementation approximates the transformed exact target |
| Distinct same-target augmented route should be presumed and implemented later by default | rejected | presumption would violate the single-target contract and Phase 4 anti-drift boundary |
| Current augmented Gaussian-closure route survives as inference-facing Lane B | rejected | current wrappers are explicitly surrogate / Gaussian-closure only |
| Augmented route collapses into Lane A implementation variant today | not established | no reviewed artifact proves an implemented same-target augmented route that can be collapsed |
| Current augmented-lane inference is retired for now; only Lane A + Zhao--Cui remain inference-facing same-target routes | accepted | this is the only outcome supported by the reviewed derivation, chapter reconciliation, and route-classification artifacts |

## Decision

The reviewed Phase 4 route decision is:

```text
AUGMENTED_LANE_INFERENCE_RETIRED_UNTIL_NEW_SAME_TARGET_DERIVATION
```

Operational meaning:
- Lane A direct-likelihood transformed route remains the current same-target
  truth-anchor.
- The current factorized scalar Zhao--Cui wrapper remains a same-target
  comparator within its stated scope.
- The current augmented-noise Gaussian-closure family remains surrogate or
  diagnostic evidence only and may not be used as inference-facing actual-SV
  same-target evidence.
- Any future attempt to revive an augmented actual-SV inference lane requires a
  new reviewed derivation/result artifact proving same-target status before code,
  test, or benchmark promotion is allowed.

## What Phase 4 settled

- The program will not proceed as if a corrected same-target Lane B already
  exists.
- The surviving inference-facing same-target comparator set is now:
  - dense exact-transformed reference,
  - direct-likelihood Fixed-SGQF transformed route,
  - factorized scalar Zhao--Cui comparator.
- Historical two-lane benchmark/test artifacts may remain for traceability, but
  only as non-promotional evidence.

## What Phase 4 did not conclude

- It did not prove that no same-target augmented route can ever exist.
- It did not rewrite code, tests, or benchmarks yet.
- It did not validate same-target values or gradients; those remain later phases.

## Handoff conditions check

Phase 5 may start because:
- the surviving same-target comparator set is explicit;
- the route-decision outcome is consistent with the contract and prior phases;
- the program can now validate same-target values without route ambiguity.

## Decision artifact classification

- surviving inference-facing same-target routes: `SAME_TARGET_ACTUAL_SV`
- current augmented Gaussian-closure family: `SURROGATE_OR_GAUSSIAN_CLOSURE`
- historical two-lane benchmark/test framing: `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE`
- future augmented same-target revival: `BLOCKED_PENDING_NEW_DERIVATION`

## Decision

`ADVANCE_TO_PHASE5_SAME_TARGET_VALUE_VALIDATION_WITHOUT_AUGMENTED_INFERENCE_LANE`
