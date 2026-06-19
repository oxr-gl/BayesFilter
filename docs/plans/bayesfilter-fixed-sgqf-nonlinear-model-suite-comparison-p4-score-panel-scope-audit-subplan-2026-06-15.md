# P4 Subplan: Fixed-SGQF Score Panel Scope Audit

metadata_date: 2026-06-15
phase: P4
status: EXECUTION_READY

## Purpose

Decide whether fixed SGQF analytical gradients should be integrated into the
same benchmark/leaderboard artifact now or remain a separate diagnostic-only
scope.

## Governing Master Program

`docs/plans/bayesfilter-fixed-sgqf-nonlinear-model-suite-comparison-master-program-2026-06-15.md`

## Evidence Contract

Question:
- Can fixed SGQF score rows be compared in the same benchmark artifact without
  violating accepted-branch / same-scalar discipline?

Primary pass criterion:
- produce an explicit scope decision table rather than forcing score rows into an
  unsuitable schema.

## Execution Steps

1. Compare current sigma-point score harness assumptions to fixed SGQF score
   contract assumptions.
2. Decide whether to:
   - include score rows now,
   - include score rows only as diagnostic rows,
   - or defer score rows to a separate artifact.
3. Record the decision in the result/closeout.

## Exit Criteria

`PASS_P4_FIXED_SGQF_SCORE_SCOPE_CLASSIFIED`
