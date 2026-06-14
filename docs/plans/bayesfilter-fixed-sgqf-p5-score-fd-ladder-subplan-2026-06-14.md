# P5 Subplan: Fixed-SGQF Score and Finite-Difference Ladder

metadata_date: 2026-06-14
phase: P5
status: DRAFT_REVIEW_READY

## Date

2026-06-14

## Governing Master Program

This phase executes under:

```text
docs/plans/bayesfilter-fixed-sgqf-testing-and-comparison-master-program-2026-06-14.md
```

## Purpose

P5 closes G5 by broadening analytic score evidence from the current one-step,
one-parameter scalar case into a multi-parameter, multistep, accepted-branch
ladder.

## Scope

P5 owns:

- multi-parameter derivative rows;
- multistep accepted-branch score rows;
- same-branch-signature gating for valid finite-difference comparisons;
- step-size policy and blocked-row policy for branch-leaving FD cells.

P5 does not own:

- stochastic-score claims;
- baseline ranking against other filters.

## Governing Constraints

1. Analytic score and finite difference must target the same scalar.
2. Promotion rows require the same branch signature.
3. Branch-leaving FD rows are blocked or classified separately, not used as
   promotion evidence.
4. Step-size sensitivity is an explanatory diagnostic, not a success criterion
   by itself.

## Evidence Contract

Question:

Does the fixed-SGQF analytic score continue to agree with finite-difference
checks across broader parameter and horizon coverage when the same scalar and
same branch are preserved?

Primary pass criterion:

- at least one multi-parameter accepted-branch row passes;
- at least one multistep accepted-branch row passes;
- the result note preserves same-branch and same-scalar requirements explicitly.

Veto diagnostics:

- FD and analytic score target different scalars;
- branch mismatch is ignored;
- a branch-leaving FD row is promoted as failure of the analytic recursion
  rather than blocked comparability.

Explanatory-only diagnostics:

- FD step-size sweep;
- branch hash;
- same-branch signature;
- per-parameter mismatch summary.

What will not be concluded:

- no full stochastic-score correctness claim;
- no HMC readiness claim.

## Multi-Parameter Coverage Matrix

Candidate parameter families:

- transition parameter(s);
- observation parameter(s);
- initial mean entries;
- covariance entries only where derivative-provider semantics are explicit.

## Finite-Difference Step-Size Policy

The phase result must record:

- default step size;
- any local step-size sweep used to reject numerical artifacts;
- which rows were blocked because a stable same-branch FD check could not be
  maintained.

## Execution Steps

1. Reuse current SGQF score-fixture patterns.
2. Add one multi-parameter accepted-branch fixture first.
3. Extend to one multistep accepted-branch fixture.
4. Run FD checks with explicit same-branch gating.
5. Record blocked branch-leaving rows separately when encountered.
6. Write a result note separating promotion rows from blocked comparability rows.

## Required Artifacts

- Phase result:
  `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-ladder-result-2026-06-14.md`
- Phase review ledger:
  `docs/plans/bayesfilter-fixed-sgqf-p5-claude-review-ledger-2026-06-14.md`
- Optional structured output:
  `docs/plans/bayesfilter-fixed-sgqf-p5-score-fd-matrix-2026-06-14.json`

## Stop Rules

Stop if:

- the same scalar cannot be preserved;
- accepted-branch FD checks cannot be made stable enough to answer the question;
- the phase begins to mix accepted-branch and branch-leaving rows in one pass
  metric.

## Exit Criteria

P5 exits with `PASS_P5_FIXED_SGQF_SCORE_FD_LADDER_READY_FOR_P8` only if it adds
broader accepted-branch score evidence without confusing blocked comparability
rows for analytic-score failures.
