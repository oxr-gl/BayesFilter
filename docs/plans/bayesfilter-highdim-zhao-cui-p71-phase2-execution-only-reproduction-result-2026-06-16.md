# P71 Phase 2 Result: d18 Execution-Only Reproduction

metadata_date: 2026-06-16
status: PHASE2_PASSED_AFTER_PHASE2B_2C_REPAIRS
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 2
git_head: 94069066a70df6f1f0f2b53d32b9d452bd67f891

## Decision

Phase 2 now passes the d18 execution-only gate after two visible repair
subphases:

- Phase 2b: all-clipped post-fit diagnostic data is represented as an
  unavailable diagnostic-only channel rather than as a fatal execution-only
  exception.
- Phase 2c: the execution-only runner/validation harness now uses the frozen
  P70 hard row-adequacy minimum for D=36, degree 0, rank 1:
  `fit_sample_count=9`.

The Phase 2 JSON artifact was written at:

`docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json`

This is execution-only evidence.  It is not d18 filtering accuracy, rank
convergence, scaling, correctness, or HMC-readiness evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the source-anchored fixed route still execute at d18 after the condition-veto capture gate? |
| Baseline/comparator | Existing P59-9e/P8-B6 execution-only evidence and P70 fixed row-adequacy contract. |
| Primary criterion | Passed after repairs: finite log marginal likelihood, finite normalizer increments, ESS by step, branch hashes, row-adequacy metadata, and nonclaims are in the JSON manifest. |
| Veto diagnostics | No nonfinite execution-only values; no missing branch hashes; no hidden diagnostic-data exception; no row-adequacy bypass; no accuracy/rank/scaling/HMC claim. |
| Explanatory diagnostics | `fit_sample_count=9`, row adequacy `diagnostic_only_below_preferred_rows` for both steps, ESS, correction-weight ranges, normalizer increments, wall time, branch hashes. |
| Not concluded | No d18 filtering accuracy, no same-route rank convergence, no correctness, no d50/d100 scaling, no HMC readiness. |
| Artifact | Phase 2 JSON manifest plus Phase 2b/2c repair results. |

## Initial Blocker History

The first Phase 2 attempt failed before writing the JSON manifest:

```text
ValueError: diagnostic_data_all_local_entries_clipped
```

Focused pytest failed on the same path.  Phase 2b repaired this by making
all-clipped diagnostic data unavailable and diagnostic-only, not valid
holdout/replay validation evidence.

After Phase 2b, focused pytest reached the next blocker:

```text
ValueError: branch_fit_row_adequacy_failed
```

Phase 2c repaired the harness by replacing the stale two-row execution-only
fixture with the prior P70 hard minimum `fit_sample_count=9`.  Explicit
under-rowed calls with `fit_sample_count=2` still fail closed.

## Final Rerun Evidence

CPU-only command with CUDA hidden:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python - <<'PY'
import json
import time
from pathlib import Path
import bayesfilter.highdim as highdim

out = Path('docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json')
start = time.time()
result = highdim.p59_author_sir_validation_ladder(
    tier='d18_execution_only',
    sample_count=1,
    fit_sample_count=highdim.P59_D18_EXECUTION_ONLY_FIT_SAMPLE_COUNT,
)
...
PY
```

Terminal summary:

```text
status PASS_P59_9E_D18_EXECUTION_ONLY
blockers ()
fit_sample_count 9
row_adequacy_statuses ['diagnostic_only_below_preferred_rows', 'diagnostic_only_below_preferred_rows']
log_marginal_likelihood -329.0602743516211
wall_time_seconds 112.833
```

JSON validation:

```bash
python -m json.tool docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-2026-06-16.json
```

Result: passed.

## Local Checks

CPU-only compile:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py scripts/p59_author_sir_m9_runner_manifest.py
```

Result: passed.

Focused CPU-only pytest:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_validation_ladder.py
```

Result:

```text
7 passed, 2 warnings in 662.37s
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p59_author_sir_runner_manifest.py
```

Result:

```text
6 passed, 2 warnings in 649.45s
```

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p60_author_sir_rank_comparator.py
```

Result:

```text
7 passed, 2 warnings in 536.01s
```

Diff hygiene:

```bash
git diff --check -- bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p59_author_sir_m9_runner_manifest.py tests/highdim/test_p59_author_sir_validation_ladder.py tests/highdim/test_p59_author_sir_runner_manifest.py tests/highdim/test_p60_author_sir_rank_comparator.py docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2c-row-adequacy-fit-budget-repair-subplan-2026-06-16.md
```

Result: passed.

## Boundary Notes

The row-adequacy status is `diagnostic_only_below_preferred_rows`, not `ok`.
Therefore Phase 2 proves only that the d18 execution-only route can run with a
predeclared hard-minimum row budget.  It does not authorize rank/degree
promotion, d18 accuracy validation, d50/d100 scaling, or HMC readiness.

The P60 high-rank comparator remains condition-vetoed under the focused tests.
That is not a Phase 2 execution-only failure; it is a Phase 4 structural-ladder
blocker unless separately repaired under a reviewed Phase 4 subplan.

## Stop-Rule Compliance

Phase 2 and its repair subphases did not:

- lower or bypass P70 row adequacy;
- retune condition-number thresholds;
- change the SIR model, observations, density callbacks, rank, degree, ridge,
  sweep policy, or seeds after seeing output;
- treat all-clipped diagnostics as validation evidence;
- run d18 accuracy;
- run d50/d100;
- make HMC-readiness claims;
- use GPU evidence.

## Next Handoff

Phase 3 may begin only after the Phase 2c implementation/result packet passes
Claude read-only review.  Phase 3 remains a finite numeric evaluator/value gate
only; it cannot make accuracy, rank-convergence, scaling, or HMC claims.
