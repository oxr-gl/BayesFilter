# P37-M6 Claude Review Ledger: Fixed-Branch Gradient First Gate

metadata_date: 2026-06-06
phase: P37-M6 fixed-branch gradient first gate

review_scope:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-phase6-fixed-branch-gradient-subplan-2026-06-05.md`

governing_sources:
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-overnight-gated-self-recovery-runbook-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-p30-model-suite-test-master-program-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-zhao-cui-traceability-ledger-2026-06-05.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

## Iterations

### Plan Gate Iteration 1

worker: `highdim-p37-m6-plan-review-iter1`

status: `PASS_M6_PLAN`

raw_response:

```text
PASS_M6_PLAN
```

## Current Status

`PASS_M6_CODE_GOVERNANCE`.

### Code/Governance Gate Iteration 1

worker: `highdim-p37-m6-code-governance-review-iter1`

status: `BLOCKED_M6_CODE_GOVERNANCE`

raw_response:

```text
BLOCKED_M6_CODE_GOVERNANCE
1. In `bayesfilter/highdim/derivatives.py:347-356`, `DERIVATIVE_PASSED` only
requires a nonempty valid subset plus one stable window. The P37-M6 first-gate
contract says a passed LGSSM fixture must have **all** finite-difference rows
branch compatible; reject passed manifests whenever any row is
`INVALID_BRANCH_MISMATCH` or `INVALID_NONFINITE_VALUE`.
2. In `bayesfilter/highdim/derivatives.py:314-327,347-371`,
`stable_window_status` is only required to be nonempty text and can disagree
with the computed evidence. Add validation so the allowed status vocabulary is
enforced and the declared status matches the actual stable-window outcome /
`row_decision`.
3. In `bayesfilter/highdim/derivatives.py:336-345`, `finite_difference_h` is
checked only for positivity and finiteness; it is not verified against
`finite_difference_table.rows[*].h`. Enforce that the declared perturbation
ladder matches the actual table rows so the manifest cannot misstate the
tested `h` ladder.
```

accepted_fix:

```text
Blocker classification: fixable code-governance consistency issue.  Repair
requires every row to be valid for `DERIVATIVE_PASSED`, validates
`stable_window_status` against an allowed vocabulary and row decision, enforces
that the declared `finite_difference_h` ladder matches table-row `h` values,
and adds regression tests for the three issues.
```

### Code/Governance Gate Iteration 2

worker: `highdim-p37-m6-code-governance-review-iter2`

status: `BLOCKED_M6_CODE_GOVERNANCE`

raw_response:

```text
BLOCKED_M6_CODE_GOVERNANCE
1. In `bayesfilter/highdim/derivatives.py:363-385`,
`stable_window_status` still does not have to equal the computed outcome; it
is only checked against an allowed set plus coarse `row_decision` rules. A
manifest with `value_prerequisite_status="PASS_*"`, all-valid rows, **no**
adjacent stable window, and `stable_window_status="BLOCKED_VALUE_OR_BRANCH_CONTRACT"`
is still accepted even though the computed status is `FAIL_NO_STABLE_WINDOW`.
Compute the expected status from prerequisite/row validity/stable-window
evidence and require an exact match.
```

accepted_fix:

```text
Blocker classification: fixable code-governance consistency issue.  Repair
computes the expected stable-window status from value prerequisite, row
validity, row presence, and stable-window evidence, then requires the declared
status to match exactly.  Regression tests cover valid unstable rows mislabeled
as blocked and accepted rows labeled `FAIL_NO_STABLE_WINDOW`.
```

### Code/Governance Gate Iteration 3

worker: `highdim-p37-m6-code-governance-review-iter3`

status: `PASS_M6_CODE_GOVERNANCE`

raw_response:

```text
PASS_M6_CODE_GOVERNANCE
```
