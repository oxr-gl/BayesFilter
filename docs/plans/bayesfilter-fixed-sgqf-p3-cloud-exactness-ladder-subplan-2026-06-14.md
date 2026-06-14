# P3 Subplan: Fixed-SGQF Cloud Exactness Ladder

metadata_date: 2026-06-14
phase: P3
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P3 closes G3 by broadening cloud/construction evidence beyond the current small
set of cases into a controlled `(dim, sparse_level)` ladder with explicit moment
checks.

## Scope

P3 owns:

- weight-total checks across more cloud cells;
- symmetry/centering and covariance-reproduction rows;
- selected higher-order moment rows where appropriate;
- merge-tolerance and zero-weight-policy observations as local construction
  evidence.

P3 does not own:

- filtering-accuracy ranking;
- score promotion evidence.

## Governing Constraints

1. Exactness language must be attached to named moment rows only.
2. A passing moment ladder does not imply all-moment exactness in all
   dimensions.
3. If a selected high-order moment row is too ambitious for the rung, reduce the
   claim rather than stretch the interpretation.
4. Construction evidence must preserve `(dim, sparse_level)`, tolerance policy,
   and tested moments explicitly.

## Evidence Contract

Question:

Does the fixed-SGQF cloud construction satisfy a broader ladder of tested moment
and merge-policy checks than the current 1D and 3D level-2 rows?

Primary pass criterion:

- cover more than one nontrivial `(dim, sparse_level)` cell beyond the current
  small cases;
- preserve explicit tested-moment language;
- record merge and zero-weight behavior honestly.

Veto diagnostics:

- a passing covariance row is summarized as blanket exactness;
- the phase omits which moments were tested;
- merge-tolerance behavior is interpreted without recording the tolerance.

Explanatory-only diagnostics:

- point count;
- negative-weight count;
- merge-tolerance value;
- tested-moment table.

What will not be concluded:

- no all-dimension exactness theorem;
- no blanket sparse-grid optimality claim.

## Moment Ladder

Begin from conservative rows such as:

- weight sum;
- first moment / centering;
- covariance reproduction;
- selected fourth-order moment rows where the rung supports them.

Candidate ladder cells:

- 2D level 2;
- 3D level 3 if tractable;
- 4D level 2.

## Execution Steps

1. Reuse current construction-test patterns.
2. Select a small ladder of additional `(dim, sparse_level)` cells.
3. Add tested-moment rows incrementally.
4. Record merge and zero-weight policy observations.
5. Write a result note that states exactly which moment rows passed and what
   remains untested.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p3-claude-review-ledger-2026-06-14.md`
- Optional structured matrix:
  `docs/plans/bayesfilter-fixed-sgqf-p3-cloud-exactness-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- the tested-moment label cannot be stated precisely;
- a higher rung would require claiming more than the row actually checks;
- merge-policy conclusions cannot be tied to explicit tolerance settings.

## Exit Criteria

P3 exits with `PASS_P3_FIXED_SGQF_CLOUD_EXACTNESS_READY_FOR_P6_P7` only if it
adds broader tested-moment evidence without promoting that local ladder into a
general exactness claim.
