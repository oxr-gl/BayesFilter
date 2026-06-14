# P7 Subplan: Fixed-SGQF Baseline Comparison Ladder

metadata_date: 2026-06-14
phase: P7
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P7 closes G7 by positioning fixed-SGQF against same-target repo baseline routes
without letting comparison convenience turn into unsupported ranking claims.

## Scope

P7 owns:

- same-target comparison panels against eligible repo baselines;
- comparator eligibility rules for UKF / CUT4 / SVD sigma-point rows;
- exact-reference, dense-reference, and baseline-only row separation in the
  final tables.

P7 does not own:

- universal ranking claims;
- cross-target comparisons;
- replacement of exact-reference evidence.

## Governing Constraints

1. A baseline route is eligible only if it evaluates the same target scalar on
   the same fixture semantics.
2. Exact-reference rows remain anchored by P4.  Dense-reference rows remain
   anchored by P1/P6.  Baseline comparison does not redefine truth.
3. A method may be omitted from a row only with an explicit eligibility reason,
   not because the result would be inconvenient.

## Evidence Contract

Question:

On selected same-target fixtures, how does fixed-SGQF compare to existing repo
baseline filters such as UKF, CUT4, and SVD sigma-point routes?

Primary pass criterion:

- at least one same-target comparison panel is produced honestly;
- every included row states whether its comparator status is exact-reference,
  dense-reference, or baseline-only;
- omitted baseline rows are explained.

Veto diagnostics:

- different-target methods are placed in one ranking table;
- baseline-only results are summarized as truth-relative evidence without a
  proper reference row;
- an omitted method has no eligibility explanation.

Explanatory-only diagnostics:

- point count;
- runtime;
- selected-fixture error summaries;
- comparator-eligibility table.

What will not be concluded:

- no universal method ranking;
- no global superiority or inferiority claim for fixed-SGQF;
- no production-default recommendation.

## Comparator Eligibility Rules

The phase result must preserve explicit eligibility judgments for at least:

- UKF / sigma-point route;
- CUT4 route;
- SVD sigma-point route.

Each row should say whether the comparator is:

- `eligible_same_target`
- `blocked_not_same_target`
- `blocked_missing_surface`
- `diagnostic_only`

## Execution Steps

1. Inherit exact-reference and dense-reference anchor fixtures from earlier
   phases where possible.
2. Build a same-target eligibility table for candidate baseline routes.
3. Run comparison rows only for eligible methods.
4. Record omitted-method reasons explicitly.
5. Write a result note with strict interpretation boundaries.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p7-claude-review-ledger-2026-06-14.md`
- Optional structured output:
  `docs/plans/bayesfilter-fixed-sgqf-p7-baseline-comparison-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- same-target semantics cannot be established;
- the phase would need to compare different scalars or parameterizations;
- the result language begins to imply more than selected-fixture positioning.

## Exit Criteria

P7 exits with `PASS_P7_FIXED_SGQF_BASELINE_COMPARISON_READY_FOR_P8` only if it
produces a same-target comparison panel with honest eligibility labels and
strict non-overclaiming interpretation.
