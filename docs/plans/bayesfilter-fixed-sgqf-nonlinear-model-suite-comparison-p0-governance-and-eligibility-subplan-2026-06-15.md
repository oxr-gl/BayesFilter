# P0 Subplan: Fixed-SGQF Nonlinear Suite Governance And Eligibility

metadata_date: 2026-06-15
phase: P0
status: EXECUTION_READY

## Purpose

Freeze the comparator eligibility rules, SGQF level policy, and benchmark-scope
claim boundaries before integrating fixed SGQF into the existing nonlinear model
suite benchmark harnesses.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`

## Evidence Contract

Question:
- Under what rules can fixed SGQF be inserted into the existing nonlinear model
  suite and smoke harness without changing comparator meaning?

Primary pass criterion:
- define a stable level policy (`fixed_sgqf_level_2` for first integration),
- classify Model A rows as exact-reference, Model B/C rows as dense-one-step
  reference rows, and score rows as scope-audited.

## Execution Steps

1. Freeze SGQF benchmark variant as level 2 for the first leaderboard pass.
2. Record comparator class for each model family.
3. Record whether score comparison is in-scope for the main benchmark or only as
   a scope-audit note.
4. Write the P0 result if needed before moving to code integration.

## Exit Criteria

`PASS_P0_FIXED_SGQF_SUITE_COMPARISON_READY_FOR_P1`
