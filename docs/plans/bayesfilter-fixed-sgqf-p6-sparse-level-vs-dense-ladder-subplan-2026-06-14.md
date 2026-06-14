# P6 Subplan: Fixed-SGQF Sparse-Level Versus Dense Ladder

metadata_date: 2026-06-14
phase: P6
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P6 closes G8 by comparing fixed-SGQF sparse levels against the same dense
numerical comparator on selected tractable nonlinear fixtures.

## Scope

P6 owns:

- sparse-level ladders on selected fixtures already justified by P1/P3;
- accuracy summaries versus the same dense comparator;
- careful interpretation of how accuracy changes with sparse level on those
  fixtures.

P6 does not own:

- general convergence claims;
- baseline ranking against other filter families.

## Governing Constraints

1. Every level ladder must use the same dense comparator within a fixture row.
2. The phase may report improvement, plateau, or irregularity, but must not call
   any local pattern a general theorem.
3. If a higher level becomes too expensive, stop at the last credible rung and
   report the limit explicitly.

## Evidence Contract

Question:

How does fixed-SGQF behave across sparse levels on selected fixtures when judged
against the same dense numerical comparator?

Primary pass criterion:

- at least one fixture has a usable sparse-level ladder with stable labeling;
- the result records whether accuracy improves, plateaus, or behaves irregularly
  on that selected ladder.

Veto diagnostics:

- different comparators are mixed inside one ladder;
- a local improvement pattern is promoted into a general convergence claim;
- a failed high rung is silently dropped from the summary.

Explanatory-only diagnostics:

- point count by level;
- runtime by level;
- mismatch by level;
- horizon and dimension of each ladder row.

What will not be concluded:

- no general sparse-level convergence theorem;
- no default sparse-level recommendation beyond the selected fixtures.

## Ladder Design

Candidate sparse levels:

- level 1;
- level 2;
- level 3;
- level 4 only if still tractable and interpretable.

Preferred fixtures should be inherited from P1 or justified by a reviewed
amendment.

## Execution Steps

1. Reuse one or more dense-reference fixtures from P1.
2. Evaluate fixed-SGQF at increasing sparse levels.
3. Compare each level against the same dense comparator.
4. Record point-count and accuracy trade-offs.
5. Write a result note that keeps interpretation local to the tested fixtures.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p6-claude-review-ledger-2026-06-14.md`
- Optional structured matrix:
  `docs/plans/bayesfilter-fixed-sgqf-p6-sparse-level-vs-dense-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- the same dense comparator cannot be held fixed within a ladder;
- a higher level becomes too expensive to remain a credible row;
- interpretation begins to exceed the local evidence.

## Exit Criteria

P6 exits with `PASS_P6_FIXED_SGQF_SPARSE_LEVEL_LADDER_READY_FOR_P8` only if it
produces at least one honest sparse-level ladder against a fixed dense
comparator and preserves local-scope interpretation.
