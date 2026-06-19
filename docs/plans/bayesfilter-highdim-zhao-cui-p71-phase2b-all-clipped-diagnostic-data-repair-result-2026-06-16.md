# P71 Phase 2b Result: All-Clipped Diagnostic Data Repair

metadata_date: 2026-06-16
status: PHASE2B_BLOCKED_BRANCH_FIT_ROW_ADEQUACY_FAILED
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2b

## Decision

Phase 2b repaired the first Phase 2 blocker but did not close Phase 2.

The all-clipped holdout/replay diagnostic-data path is now treated as an
unavailable post-fit diagnostic channel rather than as a fatal execution-only
exception.  This preserves the boundary that all-clipped diagnostics are not
valid holdout/replay validation evidence.

After that repair, the focused P59 execution-only pytest exposed the next
blocker:

```text
ValueError: branch_fit_row_adequacy_failed
```

The shared cause is that the old execution-only fixture requested
`fit_sample_count=2`, while the already-reviewed P70 row-adequacy rule requires
at least `n_hard=max(4, ceil(36/4), max_core_columns)=9` rows for the d18,
degree-0, rank-1 branch.  This is a stale test/harness budget issue under the
current P70 contract, not evidence against SIR d18 accuracy.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can all-clipped post-fit diagnostic data be represented without crashing the execution-only ladder or pretending the diagnostic is valid? |
| Primary criterion | Partially met: the diagnostic-data exception no longer stops construction, but the focused Phase 2 test still fails on a downstream row-adequacy veto. |
| Veto diagnostics | No clipped diagnostic data is promoted to valid holdout/replay evidence. No source-route semantics, thresholds, ranks, degree, ridge, sweep policy, or seeds were changed. |
| Explanatory diagnostics | Missing holdout/replay diagnostics remain diagnostic-only and nonclaim-bearing. |
| Not concluded | No d18 accuracy, no holdout/replay validation, no rank convergence, no d50/d100 scaling, no HMC readiness. |
| Artifact | This result plus the Phase 2c row-adequacy repair subplan. |

## Local Checks

CPU-only checks after the Phase 2b implementation:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py
git diff --check -- bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2b-all-clipped-diagnostic-data-repair-subplan-2026-06-16.md
```

Result: passed.

Focused CPU-only pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result:

```text
5 failed, 1 passed, 2 warnings
ValueError: branch_fit_row_adequacy_failed
```

## Claude Review

The first broad Phase 2b Claude review prompt stalled.  A tiny trusted Claude
probe succeeded, so the prompt was redesigned to be smaller and path-bounded.
The smaller read-only review returned:

```text
VERDICT: AGREE
```

Claude was used only as read-only reviewer.  Claude did not authorize
execution, edits, threshold changes, or scientific claims.

## Interpretation

Phase 2b found a second execution-only gate mismatch.  The next repair should
not weaken `branch_fit_row_adequacy_failed`.  It should make the Phase 2
execution-only harness and tests request an admissible row budget under the
frozen P70 rule, and it should preserve explicit nonclaims.

## Stop-Rule Compliance

Phase 2b did not:

- run d18 accuracy;
- run same-route rank convergence as a pass criterion;
- run d50/d100;
- run GPU or HMC commands;
- weaken the P70 condition-number or row-adequacy thresholds;
- treat all-clipped diagnostics as valid holdout/replay evidence.

## Next Handoff

Do not proceed to Phase 3.

Draft and review Phase 2c before any code patch or Phase 2 rerun.  Phase 2c
must resolve the stale `fit_sample_count=2` harness against the P70 hard
row-adequacy rule.
