# Phase 1 Result: Single-Target Scalar Contract Freeze

Date: 2026-06-29

## Status

`PASSED_REVIEW_PENDING_FINAL_PHASE1_REVIEW_ENTRY`

## Phase Objective

Freeze the reviewed single-target scalar contract so later phases cannot drift
back to old two-lane wording, mutable code-label authority, or passing tests on
the wrong scalar.

## Local Checks Run

```bash
rg -n "Governing Scalar|Same-Target Comparator Class|Surrogate / Diagnostic / Historical Class|Explicit Veto Conditions|TESTS_PASSED_BUT_WRONG_QUESTION|Comparator Separation Rule" docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md docs/plans/bayesfilter-actual-sv-single-target-phase1-single-target-contract-*.md docs/plans/bayesfilter-actual-sv-single-target-visible-execution-ledger-2026-06-29.md docs/plans/bayesfilter-actual-sv-single-target-claude-review-ledger-2026-06-29.md
```

Observed:
- the contract contains the required scalar, comparator-class, surrogate-class,
  veto, and separation sections;
- the literal veto tag `TESTS_PASSED_BUT_WRONG_QUESTION` is present;
- formatting checks are clean for the contract and current Phase 1 artifacts.

## Review trail

Phase 1 review-hardening history now records:

- mutable code labels are demoted to explanatory-only alignment evidence and may
  not override the contract;
- the execution ledger is now an explicit required artifact for Phase 1 because
  it must record the contract as active scalar authority;
- the forbidden-actions language now blocks Phase 2 or later work before the
  contract passes;
- the end-of-phase checklist now explicitly includes review of the Phase 1 result
  itself.

## What Phase 1 settled

- one governing actual-SV scalar is now frozen in a standalone contract artifact;
- same-target comparator status now requires both target-form agreement and a
  reviewed derivation/result proof hook;
- every future test, benchmark, result note, and route manifest in this program
  must declare both route class and scalar family;
- if a future artifact evaluates a different scalar family, it must carry the
  literal veto tag `TESTS_PASSED_BUT_WRONG_QUESTION`;
- surrogate/KSC/diagnostic evidence is now explicitly separated from same-target
  actual-SV promotion evidence.

## What Phase 1 did not conclude

- It did not reconcile all mathematical and chapter statements; that is Phase 2.
- It did not classify current code/tests/benchmarks; that is Phase 3.
- It did not decide whether any corrected same-target augmented route exists;
  that is Phase 4.
- It did not validate same-target values or gradients.

## Handoff conditions check

Phase 2 may start because:
- the contract has been hardened and the local contract-shape checks passed;
- the Phase 1 result records the wording and authority changes made during the
  freeze;
- the execution ledger can now record the contract as the active scalar
  authority;
- the Phase 2 subplan already exists for refresh and review.

## Decision

`ADVANCE_TO_PHASE2_DERIVATION_AND_CHAPTER_RECONCILIATION`
