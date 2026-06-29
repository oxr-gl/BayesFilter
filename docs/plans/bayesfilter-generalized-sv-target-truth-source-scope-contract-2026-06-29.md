# Generalized-SV Target / Truth / Source-Scope Contract

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Role

This artifact freezes the Generalized-SV row identity, target identity,
truth/test-point identity, comparator classes, and forbidden substitutes. No
implementation or promotion phase may advance unless this contract is reviewed
and accepted.

## Governing row identity

The active benchmark row is:

```text
zhao_cui_generalized_sv_synthetic_from_estimated_values
```

This row is governed by the reviewed Generalized-SV testing specification and
source-scope contract.

## Governing target family

The active target family for the benchmark row is the source-scope
Generalized-SV family defined by the reviewed testing specification. It is **not**:

- actual transformed SV,
- KSC transformed finite-mixture surrogate SV,
- a native generalized-SV fixture substituted in place of the source row,
- or a transformed-residual diagnostic target relabeled as same-target.

## Truth / test-point contract

The active truth/test-point convention is the reviewed synthetic prior-mean
Generalized-SV row from the testing specification.

Use:
- the finite prior-center convention recorded in the testing specification;
- SP500 only as source-estimation input role;
- the exact row id above.

Do **not** substitute:
- author-code defaults,
- BayesFilter native generalized-SV fixture truth,
- simple-SV synthetic truth,
- SP500 returns as benchmark observations,
- ordinary means for nonfinite coordinates.

## Oracle and evaluator separation rule

- The native generalized-SV dense raw-y reference is the reviewed low-dimensional
  same-target oracle/reference.
- It is a **promotion oracle**, not an automatic executed source-row evaluator.
- The source-row SGQF evaluator remains blocked or precursor-only until a later
  reviewed phase explicitly admits it.

## Comparator classes

All artifacts in this program must classify routes/results as exactly one of:

- `SOURCE_ROW_SAME_TARGET_ADMITTED`
- `NATIVE_REFERENCE_SAME_TARGET_ORACLE`
- `PRECURSOR_VALUE_ONLY`
- `KSC_ONLY`
- `DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE`
- `BLOCKED_PENDING_SOURCE_SCOPE_EVALUATOR`

## Explicit vetoes

The following are contract violations:

- promoting a precursor SGQF route as same-target admitted without a reviewed
  same-target gate result;
- treating the native dense reference as if it already executes the benchmark row;
- using actual-SV or KSC evidence as generalized-SV same-target evidence;
- changing the truth/test-point convention without a reviewed reset memo;
- emitting a leaderboard/source-row status that does not name the route class.

## What this contract does not conclude

- It does not yet admit any SGQF source-row evaluator.
- It does not yet admit analytical score/derivative work.
- It does not conclude HMC, production, or default readiness.
- It does not prove CUT4 or Zhao--Cui same-target equality for native generalized SV.
