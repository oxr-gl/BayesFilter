# P71 Phase 1 Result: Condition-Veto Capture And Repair Gate

metadata_date: 2026-06-16
status: PHASE1_PASSED_PHASE2_PRECHECK_READY
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 1
git_head: 94069066a70df6f1f0f2b53d32b9d452bd67f891

## Decision

Phase 1 passed local checks and Claude read-only review.

The current dirty worktree already contained the narrow diagnostic-capture
repair surface needed by the P71 Phase 1 gate:

- `bayesfilter/highdim/source_route.py` defines `P70FixedFitDiagnosticError`.
- `_p59_fixed_ttsirt_transport_from_values` raises that structured error for
  non-OK fixed fits, with fit status, stop condition, per-core update records,
  P70 policy metadata, thresholds, branch hash, rank/degree dimensions, and
  explicit nonclaims.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py` catches that
  structured error, writes a failed-row payload, aborts the diagnostic, returns
  exit status `1`, and records that execution did not continue after the
  failed row.
- `tests/highdim/test_p70_phase6_diagnostic_script.py` covers captured
  failed-fit gate behavior, abort serialization, and source-route error
  payload preservation.

The only additional code change made in this Phase 1 execution was exporting
`P70FixedFitDiagnosticError` from `bayesfilter.highdim` so downstream focused
tests and scripts can use the public highdim subpackage surface consistently.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the condition-number-veto path preserve actionable diagnostics without weakening the veto? |
| Baseline/comparator | P70 Phase 6 failed first row: `rank_candidate_1_2_fit36`, degree 1, rank 2, fit count 36. |
| Primary criterion | Locally passed: a condition-veto fit is represented by a structured blocked error/payload containing fit status, condition records, design dimensions, P70 policy metadata, thresholds, and nonclaims. |
| Veto diagnostics | No threshold weakening, no fit admitted as OK, no four-row diagnostic rerun, no rank/degree/row/ridge/sweep/initializer retuning. |
| Explanatory diagnostics | Captured per-core update statuses include `condition_number`, `n_rows`, `n_cols`, condition thresholds, `fit_status`, and `stop_condition_triggered` when the fitter supplies them. |
| Not concluded | No d18 validation, no rank-channel repair success, no accuracy, no HMC readiness, no d50/d100 scaling, no adaptive Zhao-Cui parity. |
| Artifact | This result note plus focused local check output and the updated visible execution ledger. |

## Implementation Summary

Relevant current-code anchors:

- `bayesfilter/highdim/source_route.py:35-41` defines
  `P70FixedFitDiagnosticError`.
- `bayesfilter/highdim/source_route.py:3292-3326` raises the structured error
  on non-OK fit status while preserving diagnostic payload fields.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py:300-315` treats a
  `failed_fit_diagnostics` row as a gate failure.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py:410-429` builds the
  failed-row payload.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py:432-452` builds the
  aborted diagnostic artifact.
- `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py:455-505` stops row
  execution after a captured failed fit and returns nonzero exit status.
- `bayesfilter/highdim/__init__.py` now exports
  `P70FixedFitDiagnosticError`.

## Local Checks

CPU-only checks were run with `CUDA_VISIBLE_DEVICES=-1` and
`MPLCONFIGDIR=/tmp`.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  scripts/p70_phase6_rank_channel_normalizer_diagnostic.py \
  tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result: passed.

```bash
git diff --check -- \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  scripts/p70_phase6_rank_channel_normalizer_diagnostic.py \
  tests/highdim/test_p70_phase6_diagnostic_script.py \
  docs/plans/bayesfilter-highdim-zhao-cui-p71-phase0-governance-current-evidence-reset-result-2026-06-16.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-execution-ledger-2026-06-16.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-gated-overnight-execution-runbook-2026-06-16.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p71-visible-stop-handoff-2026-06-16.md \
  docs/plans/bayesfilter-highdim-zhao-cui-p71-runbook-claude-review-ledger-2026-06-16.md
```

Result: passed.

```bash
rg -n "P70FixedFitDiagnosticError|failed_fit_diagnostics|P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT|failed_fit_remains_inadmissible|CONDITION_NUMBER_VETO|no threshold retuning" \
  bayesfilter/highdim/source_route.py \
  bayesfilter/highdim/__init__.py \
  scripts/p70_phase6_rank_channel_normalizer_diagnostic.py \
  tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result: passed.

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
```

Result: passed, `8 passed, 2 warnings in 3.91s`.

## Stop-Rule Compliance

Phase 1 did not:

- rerun the P70 four-row diagnostic;
- lower or reinterpret `P70_CONDITION_NUMBER_VETO`;
- change row/rank/degree/sweep/ridge/initializer settings;
- treat a condition-veto fit as admissible;
- run d18 validation;
- launch GPU/HMC commands;
- make accuracy, rank-convergence, scaling, HMC-readiness, adaptive-parity, or
  author-code failure claims.

## Phase 2 Handoff

Claude read-only review agreed with this Phase 1 gate.  Phase 2 may begin
from:

`docs/plans/bayesfilter-highdim-zhao-cui-p71-phase2-execution-only-reproduction-subplan-2026-06-16.md`

The handoff is only to execution-only reproduction.  It is not a handoff to
accuracy, rank convergence, scaling, or HMC readiness.

## Claude Review

Claude Opus max read-only review worker:
`p71-phase1-impl-review-iter1`.

Claude returned `VERDICT: AGREE`.

Findings summary:

- Condition-veto failures remain failed and inadmissible.
- No threshold, row, rank, degree, sweep, ridge, initializer, or source-route
  retuning was found in the reviewed surface.
- Failed-fit diagnostics preserve fit status, termination/stop condition,
  per-core update records, design metadata, P70 policy payload, and nonclaims.
- The P70 four-row diagnostic is not rerun or authorized by this gate.
- Phase 2 handoff is limited to execution-only reproduction.
