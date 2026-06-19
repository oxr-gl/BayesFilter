# P70 Phase 6b Result: Condition-Veto Diagnostic Capture

metadata_date: 2026-06-16
status: PHASE6B_PASSED_CLAUDE_EXECUTION_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Decision

Phase 6b implemented the observability repair authorized by the reviewed
condition-veto capture plan.  Failed fixed-TTSIRT fits that return a non-OK
`HighDimStatus` now carry diagnostic information through a typed exception
before the source-route helper stops the row.

This is not a numerical repair.  It does not loosen the condition-number veto,
does not change row/rank/degree/ridge/sweep/initializer policy, does not rerun
the Phase 6 four-row diagnostic, and does not unblock Phase 7.

## Code Surfaces Touched

- `bayesfilter/highdim/source_route.py`
  - Added `P70FixedFitDiagnosticError`, a diagnostic carrier for failed fixed
    fits.
  - Changed `_p59_fixed_ttsirt_transport_from_values` so a non-OK fit raises
    `P70FixedFitDiagnosticError` with the same message pattern
    `fixed_ttsirt_fit_status_<STATUS>`.
  - The failed path preserves fit diagnostics but returns no transport,
    density, or success payload.
- `bayesfilter/highdim/__init__.py`
  - Exposes `P70FixedFitDiagnosticError` at the `bayesfilter.highdim`
    subpackage level only.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`
  - Catches `P70FixedFitDiagnosticError` at the row boundary.
  - Writes a failed-row payload with row identity, requested degree/rank/sample
    count, blockers, failed-fit diagnostics, and nonclaims.
  - Writes top-level status
    `P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT`, returns exit status `1`,
    and stops before later rows.
- `tests/highdim/test_p70_phase6_diagnostic_script.py`
  - Adds focused failing-path tests without running the four-row diagnostic.

## Diagnostics Now Preserved

For a condition-veto failed fit, the captured payload includes:

- status and status-derived message;
- termination reason and stop condition when available;
- `fit_quality_diagnostics`;
- per-core update records, including core index, sweep index, row/column
  counts, condition number, and condition-veto threshold when present;
- P70 fixed-fitting policy payload, including row adequacy and channel
  activity diagnostics when available;
- branch hash, rank tuple, fit degree, fit rank, target dimension,
  initialization rule, ridge, max sweeps, sweep order, warning/veto thresholds;
- explicit markers that the failed fit remains inadmissible and that no
  transport was returned.

The P70 diagnostic wrapper now serializes a failed row instead of losing this
information to an uncaught `ValueError`.

## Local Checks

Pre-edit/readiness anchor checks were run:

```bash
rg -n "fixed_ttsirt_fit_status_|CONDITION_NUMBER_VETO|fit_quality_diagnostics|p70_fixed_fitting_policy" bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
rg -n "PHASE6_BLOCKED_CONDITION_NUMBER_VETO_FIRST_ROW|CONDITION_NUMBER_VETO" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md
```

Focused post-edit checks were run:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py bayesfilter/highdim/__init__.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
```

Results:

- compileall passed with no output;
- focused pytest: `8 passed, 2 warnings in 5.42s`.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can failed P70 condition-number-veto fits carry enough diagnostics for the next repair-planning phase? |
| Baseline/comparator | Phase 6 failed first row with `ValueError: fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO` and no failed-row JSON payload. |
| Primary criterion | Passed locally: focused tests show a failed fit is represented as a failed row with diagnostics, remains failed, returns exit status `1`, and halts before the next row. |
| Veto diagnostics | No Phase 6 diagnostic rerun occurred; no threshold/ridge/sweep/rank/degree/row/initializer retuning was made; failed fits remain inadmissible. |
| Explanatory diagnostics | Captured condition and fit records are now available for a future reviewed repair-planning phase. |
| Not concluded | No Phase 6 pass, no rank-channel activation result, no normalizer result, no validation, no scaling, no HMC readiness, no bug-fixed claim. |

## What Remains Unknown

Phase 6b does not yet diagnose why the first repaired row is ill-conditioned.
It only ensures that a future approved diagnostic can preserve the information
needed to separate candidate causes such as design-rank underdetermination,
seeded-channel scaling, normal-equation conditioning, row coverage, or an
implementation bug.

## Next Handoff

Claude reviewed this Phase 6b execution and returned `VERDICT: AGREE`.  The
next safe action is to draft a new Phase 6c repair-planning subplan.  Any
future P70 four-row diagnostic rerun requires a new reviewed subplan and
explicit user approval.
