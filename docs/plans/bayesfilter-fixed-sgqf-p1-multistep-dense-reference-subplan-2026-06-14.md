# P1 Subplan: Fixed-SGQF Multistep Dense-Reference Ladder

metadata_date: 2026-06-14
phase: P1
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P1 closes G1 by extending current one-step nonlinear evidence to controlled
multistep same-target comparisons against dense numerical references on
tractable low-dimensional fixtures.

## Scope

P1 owns:

- low-dimensional nonlinear fixtures with horizon greater than one;
- cumulative and, where supportable, per-step likelihood comparisons;
- filtered mean/covariance path comparisons over time;
- explicit dense-reference qualification language.

P1 does not own:

- multidimensional affine exactness;
- same-target baseline ranking versus other filters;
- general nonlinear convergence claims.

## Governing Constraints

1. Dense rows must be low-dimensional and numerically tractable.
2. The dense comparator must target the same scalar as fixed-SGQF.
3. Every result row must preserve dimension, horizon, dense-node policy, and
   tolerance policy.
4. If the dense comparator ceases to be credible at the chosen rung, reduce the
   horizon or dimension rather than weaken the label after seeing the result.

## Evidence Contract

Question:

Does fixed-SGQF track the same-target dense numerical reference with acceptable
local agreement on selected multistep nonlinear fixtures?

Primary pass criterion:

- at least one selected multistep nonlinear fixture yields a durable result with
  same-target dense-reference comparisons for likelihood and filtered path
  objects;
- the phase result records both agreement and any observed mismatch as local
  fixture evidence, not a general theorem.

Veto diagnostics:

- dense comparator is described as exact;
- fixed-SGQF and dense comparator do not evaluate the same scalar;
- the fixture becomes too expensive and the phase silently lowers quality
  without recording the amendment.

Explanatory-only diagnostics:

- node count;
- horizon length;
- per-step mismatch table;
- filtered-path mismatch summaries.

What will not be concluded:

- no general nonlinear exactness claim;
- no production-readiness claim;
- no extrapolation to high-dimensional or paper-scale rows.

## Fixture Matrix

The phase should begin with a small fixture ladder such as:

- 1D scalar quadratic horizon 2-5;
- 1D alternate smooth nonlinear fixture if already available through existing
  helpers;
- 2D fixture only if the dense comparator remains credible at the chosen horizon.

## Execution Steps

1. Reuse existing dense-reference helper patterns from current fixed-SGQF tests.
2. Select the smallest tractable multistep nonlinear fixture.
3. Add horizon ladder rows conservatively.
4. Compare cumulative likelihood and filtered path summaries.
5. Record mismatch scale and whether it is stable across the selected ladder.
6. Write a result note that states clearly that this is dense numerical reference
   evidence on selected fixtures.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p1-claude-review-ledger-2026-06-14.md`
- Optional structured output:
  `docs/plans/bayesfilter-fixed-sgqf-p1-multistep-dense-reference-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- no same-target dense comparator is credible for the attempted rung;
- the phase can only proceed by quietly changing the scalar being compared;
- the fixture becomes numerically unstable enough that the dense comparator no
  longer answers the phase question.

## Exit Criteria

P1 exits with `PASS_P1_FIXED_SGQF_MULTISTEP_DENSE_REFERENCE_READY_FOR_P3_P5_P6`
only if it preserves same-target dense-reference labeling and records at least
one meaningful multistep nonlinear evidence row durably.
