# P4 Subplan: Fixed-SGQF Affine Kalman Ladder

metadata_date: 2026-06-14
phase: P4
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P4 closes G6 by extending the current 1D affine exact-vs-Kalman evidence into a
multidimensional affine ladder.

## Scope

P4 owns:

- 2D and, if tractable, 3D affine Gaussian fixtures;
- coupled transition matrices and nontrivial covariance structure;
- partial observation rows;
- exact-reference parity checks for likelihood and filtered-path objects.

P4 does not own:

- nonlinear dense-reference claims;
- baseline ranking against non-Kalman routes except as optional sanity rows.

## Governing Constraints

1. Every P4 row must remain genuinely affine Gaussian.
2. Kalman exactness must hold for the declared scalar and parameterization.
3. Exact-reference wording is allowed here because the comparator is genuinely
   exact on the declared rows.
4. Numerical tolerances must be recorded as linear-algebra parity tolerances,
   not as approximate-model tolerances.

## Evidence Contract

Question:

Does fixed-SGQF recover exact Kalman value-path behavior beyond the current 1D
affine fixture?

Primary pass criterion:

- at least one multidimensional affine fixture matches exact Kalman on the
  declared outputs within tight numeric parity tolerance;
- the result distinguishes exact-reference rows from any optional sanity-only
  baseline rows.

Veto diagnostics:

- a nonlinear fixture is included under exact-reference wording;
- parameterization mismatch changes the meaning of the compared scalar;
- exact-reference rows omit tolerance disclosure.

Explanatory-only diagnostics:

- state dimension;
- observation dimension;
- coupling structure;
- per-step parity summary.

What will not be concluded:

- no nonlinear exactness claim;
- no global performance claim.

## Fixture Ladder

Preferred fixture types:

- 2D diagonal-stable affine row;
- 2D coupled transition row;
- partial-observation row;
- 3D row only if it stays focused and readable.

## Execution Steps

1. Reuse the existing 1D affine fixed-SGQF/Kalman test structure.
2. Add multidimensional affine fixtures incrementally.
3. Compare total likelihood, filtered means, and filtered covariances.
4. Record tolerance values and any edge conditions.
5. Write a result note emphasizing exact-reference scope.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p4-affine-kalman-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p4-claude-review-ledger-2026-06-14.md`

## Stop Rules

Stop if:

- a row ceases to be affine Gaussian;
- exact scalar parity cannot be defined cleanly;
- the phase can only pass by loosening exact-reference wording.

## Exit Criteria

P4 exits with `PASS_P4_FIXED_SGQF_AFFINE_KALMAN_LADDER_READY_FOR_P7` only if it
produces multidimensional exact-reference parity evidence durably and honestly.
