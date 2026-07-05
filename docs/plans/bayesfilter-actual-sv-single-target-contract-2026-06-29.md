# Actual-SV Single-Target Contract

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Role

This artifact freezes the scalar identity and comparator boundaries for the
actual-SV correction program.  No implementation, test, or benchmark phase may
advance unless this contract is reviewed and accepted.

## Governing Scalar

There is one intended actual-SV likelihood target for this program:

\[
\ell_T(\theta)=\log p(y_{1:T}\mid\theta)=\sum_{t=1}^T \log Z_t(\theta),
\]

with transformed observations
\[
  z_t=\log(y_t^2),
  \qquad
  z_t-\log(\beta^2)-h_t\sim \log(\chi_1^2),
\]
and one-step transformed normalizer
\[
  Z_t(\theta)=\int g_\theta(z_t\mid h_t)p_\theta(h_t\mid z_{1:t-1})\,dh_t.
\]

## Same-Target Comparator Class

A route may be compared as same-target actual-SV evidence only if **both** of the
following are true:

1. it consumes the transformed observations \(z_t\) and the exact transformed
   observation law above; and
2. a reviewed derivation/result artifact in this program explicitly records why
   the route computes or approximates that same scalar.

Under that rule, the currently intended same-target comparator candidates are:

- dense exact-transformed reference, subject to the reviewed derivation/result
  artifact hook above;
- direct-likelihood fixed-cloud / Fixed-SGQF reweighting route, subject to the
  reviewed derivation/result artifact hook above;
- current factorized scalar Zhao--Cui comparator, subject to the reviewed
  derivation/result artifact hook above;
- any future corrected augmented route only after a reviewed artifact proves it
  approximates this same scalar.

## Surrogate / Diagnostic / Historical Class

The following do **not** belong to the same-target comparator class:

- current augmented-noise Gaussian-closure Lane-B wrappers;
- current Gaussian innovation scalar routes that replace the transformed
  observation density by predictive observation moments and a Gaussian
  innovation likelihood;
- KSC mixture / surrogate transformed routes when the question is the actual-SV
  exact transformed target.

These artifacts may remain useful as:

- surrogate-likelihood evidence,
- diagnostic mismatch evidence,
- historical traceability evidence,
- implementation scaffolding pending explicit re-derivation,

but not as same-target promotion evidence for actual SV.

## Explicit Veto Conditions

The following statements are forbidden and count as contract violations:

- “Lane B passed its tests, therefore it is valid for actual-SV inference.”
- “The Gaussian-closure route is close enough, so it counts as the same target.”
- “KSC evidence supports actual-SV same-target claims.”
- “A gradient/FD pass on the surrogate scalar validates the actual-SV target.”
- “Tests passed, therefore the target question is settled.”

The literal veto tag is:

```text
TESTS_PASSED_BUT_WRONG_QUESTION
```

## Comparator Separation Rule

All artifacts in this program must classify any result or route as exactly one
of:

- `SAME_TARGET_ACTUAL_SV`
- `SURROGATE_OR_GAUSSIAN_CLOSURE`
- `KSC_ONLY`
- `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE`
- `BLOCKED_PENDING_NEW_DERIVATION`

In addition, every test, benchmark, result note, and route manifest in this
program must declare **both**:

1. its route-class tag from the list above; and
2. the exact scalar family it evaluates.

If the declared scalar family does not match the governing scalar, the artifact
must carry the literal veto tag
`TESTS_PASSED_BUT_WRONG_QUESTION`.

Interpretation rule:

- `SURROGATE_OR_GAUSSIAN_CLOSURE` means the scalar may be useful for local
  approximation, surrogate, or implementation diagnostics, but it is **not**
  same-target evidence for the governing actual-SV likelihood.
- `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE` means the artifact may document a
  mismatch, failure, or historical route, but it may not be used to justify
  inference-lane promotion.
- `BLOCKED_PENDING_NEW_DERIVATION` means no implementation, test rewrite,
  benchmark promotion, or route-retention claim may proceed until a reviewed
  derivation/result artifact resolves the block.

No artifact may silently omit or blur this classification.

## Phase Consequences

- Phase 2 must reconcile all mathematical and chapter statements to this
  contract.
- Phase 3 must classify every relevant code/test/benchmark surface to one of the
  route classes above.
- Phase 4 may decide whether any corrected Lane-B route survives, but until then
  no surviving same-target Lane B is presumed.
- Phases 5 and 6 may compare only same-target quantities.

## What This Contract Does Not Conclude

- It does not prove a corrected same-target augmented route exists.
- It does not retire surrogate code automatically; it only fixes how it may be
  interpreted.
- It does not authorize gradient or benchmark promotion by itself.
- It does not make any production/default/HMC claim.

## Decision

`FREEZE_SINGLE_TARGET_BEFORE_ANY_IMPLEMENTATION_OR_TEST_REWRITE_PHASE`
