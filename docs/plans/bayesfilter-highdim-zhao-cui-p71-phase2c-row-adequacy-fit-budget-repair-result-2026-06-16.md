# P71 Phase 2c Result: Row-Adequacy Fit-Budget Repair

metadata_date: 2026-06-16
status: PHASE2C_LOCAL_CHECKS_PASSED_PENDING_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2c

## Decision

Phase 2c locally passes.

The stale two-row execution-only fixture was replaced with an explicit
execution-only fit budget constant:

```text
P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT = 9
```

This value is the P70 hard row-adequacy minimum for D=36, degree 0, rank 1.
It is used as the default for the P59-9d runner manifest path and the P59-9e
execution-only validation ladder.  Explicit under-rowed calls with
`fit_sample_count=2` still fail closed with
`branch_fit_row_adequacy_failed`.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the d18 execution-only Phase 2 harness run with a row budget admissible under the frozen P70 hard row-adequacy rule? |
| Primary criterion | Locally passed: focused tests pass; direct P59-9d runner manifest tests pass; Phase 2 execution-only rerun writes a JSON manifest with finite values, ESS, branch hashes, row-adequacy metadata, and nonclaims. |
| Veto diagnostics | No row-adequacy lowering or bypass; explicit two-row calls fail closed; execution-only evidence is not promoted to accuracy/rank/scaling/HMC. |
| Explanatory diagnostics | Row adequacy is `diagnostic_only_below_preferred_rows` for both execution-only steps. |
| Not concluded | No d18 filtering accuracy, no same-route rank convergence, no correctness, no d50/d100 scaling, no HMC readiness. |
| Artifact | This result, code/test patch, and Phase 2 JSON manifest. |

## Implementation Summary

Touched code:

- `bayesfilter/highdim/source_route.py`
- `bayesfilter/highdim/__init__.py`
- `scripts/p59_author_sir_m9_runner_manifest.py`

Focused behavior changes:

- Added `P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT = 9`.
- Added execution-only row-adequacy reporting helpers.
- P59-9d and P59-9e manifests now expose:
  - `fit_sample_count`;
  - `fit_sample_count_by_step`;
  - `fit_sample_count_policy`;
  - `row_adequacy_by_step`;
  - P59-9e `holdout_replay_diagnostics_by_step`.
- The P59-9d script default now uses the execution-only fit budget constant.
- Tests now assert explicit `fit_sample_count=2` fails closed.
- P60 focused tests now record the high-rank condition veto instead of
  expecting rank-2 pass evidence inside the Phase 2 execution-only repair.

## Local Checks

Compile:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py scripts/p59_author_sir_m9_runner_manifest.py
```

Result: passed.

Focused pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result: `7 passed, 2 warnings in 662.37s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_runner_manifest.py
```

Result: `6 passed, 2 warnings in 649.45s`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result: `7 passed, 2 warnings in 536.01s`.

Diff hygiene:

```bash
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p59_author_sir_m9_runner_manifest.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2c-row-adequacy-fit-budget-repair-subplan-2026-06-16.md
```

Result: passed.

Phase 2 execution-only JSON rerun:

```text
status PASS_P59_9E_D18_EXECUTION_ONLY
blockers ()
fit_sample_count 9
row_adequacy_statuses ['diagnostic_only_below_preferred_rows', 'diagnostic_only_below_preferred_rows']
log_marginal_likelihood -329.0602743516211
wall_time_seconds 112.833
```

JSON artifact:

`docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json`

JSON validation: passed.

## Boundary Safety

The helper/constant does not auto-clamp explicit under-rowed user input.
Under-rowed calls still reach the P70 row-adequacy veto.

The execution-only rerun uses a hard-minimum row count, not a preferred row
count.  Both steps report `diagnostic_only_below_preferred_rows`.  Therefore
Phase 2c does not support rank promotion, degree promotion, accuracy
validation, scaling, or HMC readiness.

The P60 high-rank comparator remains blocked by `CONDITION_NUMBER_VETO`.  This
is preserved as a Phase 4 structural-ladder issue and is not hidden or repaired
inside Phase 2c.

## Next Handoff

Send this implementation/result packet to Claude for read-only review.  If
Claude returns `VERDICT: AGREE`, Phase 3 may begin as a numeric evaluator/value
finite gate only.
