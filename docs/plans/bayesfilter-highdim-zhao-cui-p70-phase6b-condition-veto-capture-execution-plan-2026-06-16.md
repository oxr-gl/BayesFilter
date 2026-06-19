# P70 Phase 6b Execution Plan: Condition-Veto Diagnostic Capture

metadata_date: 2026-06-16
status: CLAUDE_R2_AGREE_READY_FOR_EXECUTION
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Objective

Implement the Phase 6b observability repair approved by the reviewed subplan:
condition-number-veto fixed fits must preserve diagnostic information before
the source-route helper raises.  This is not a numerical repair and not a
Phase 6 rerun.

## Entry Conditions

- Phase 6 result exists and records
  `PHASE6_BLOCKED_CONDITION_NUMBER_VETO_FIRST_ROW`.
- Phase 6b subplan status is
  `READY_AFTER_CLAUDE_AGREE_PENDING_USER_APPROVAL`.
- User asked Codex to create/review/execute this plan and review execution
  with Claude.
- The Phase 6 terminal rule remains binding: no four-row diagnostic rerun and
  no post-output retuning.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can failed P70 condition-number-veto fits carry enough diagnostics for the next repair-planning phase? |
| Baseline/comparator | Current failure: `_p59_fixed_ttsirt_transport_from_values` raises `fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO` after computing `fit_quality_diagnostics`, but the P70 wrapper receives only the exception and writes no row payload. |
| Primary pass criterion | Focused tests show that a condition-veto row can be represented in the P70 diagnostic artifact with row label, requested degree/rank/sample count, fit status, blockers, failed-fit diagnostics, per-core condition/update records, P70 policy payload, and nonclaims; failed fits remain failed. |
| Veto diagnostics | Any change to P70 thresholds, ridge, sweep order, row count, rank, degree, initializer, condition-veto semantics, or Phase 6 command scope; any four-row diagnostic run; any claim that the repair fixes conditioning. |
| Explanatory only | Captured condition number, row/column counts, sweep/core index, warning/veto thresholds, row adequacy, channel activity if fitted cores exist, target/weight summaries, and failed branch hash. |
| Not concluded | No Phase 6 diagnostic pass, no rank-channel activation result, no normalizer result, no validation, no scaling, no HMC readiness, no bug-fixed claim. |

## Implementation Plan

1. Add a small diagnostic exception class in `bayesfilter/highdim/source_route.py`.
   - Name: `P70FixedFitDiagnosticError`.
   - It carries `status`, `message`, and a frozen/json-ready diagnostic payload.
   - It does not subclass or alter `HighDimStatus`; it is only an observability
     carrier.

2. In `_p59_fixed_ttsirt_transport_from_values`, preserve failed-fit payload
   before raising when `fit_result.status is not HighDimStatus.OK`.
   - Include `fit_quality_diagnostics`.
   - Include `p70_fixed_fitting_policy`.
   - Include row adequacy and channel activity diagnostics already computed.
   - Include `fit_branch_hash`, `rank_tuple`, `fit_degree`, `fit_rank`,
     `target_dim`, `initialization_rule`, `ridge`, `max_sweeps`,
     `sweep_order`, condition thresholds, and nonclaims.
   - Raise `P70FixedFitDiagnosticError` with the same textual message pattern
     `fixed_ttsirt_fit_status_<STATUS>`.
   - Do not return a transport for failed fits.
   - Do not change fit thresholds or fitted cores.

3. In `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`, catch
   `P70FixedFitDiagnosticError` around each row helper call.
   - Write a failed row payload with `status: P70_PHASE6_ROW_BLOCKED`,
     row identity, requested degree/rank/fit sample count, blockers, and the
     diagnostic payload from the exception.
   - Update the JSON artifact immediately after the failed row.
   - Write a machine-readable top-level terminal status such as
     `P70_PHASE6_DIAGNOSTIC_ABORTED_ON_FAILED_FIT`.
   - Stop after the failed row; do not continue to other rows under the same
     command.
   - Provide no retry path, no success/transport artifact for the failed row,
     and no outer-driver path that treats the caught exception as recoverable.
   - Return exit status `1`.

4. Extend `p70_phase6_gate_summary` so failed rows with captured diagnostics
   produce a structured failed gate rather than an empty gate.

5. Add focused tests in `tests/highdim/test_p70_phase6_diagnostic_script.py`.
   - `_p59_fixed_ttsirt_transport_from_values` failed-fit handling raises
     `P70FixedFitDiagnosticError` on a non-OK fit-result path, using a focused
     monkeypatch or equivalent harness rather than the four-row diagnostic.
   - The raised error preserves the exact status-derived message string.
   - The raised payload contains the promised diagnostic keys.
   - Synthetic captured failed row is classified as failed.
   - Captured diagnostics preserve `CONDITION_NUMBER_VETO`, per-core update
     status, condition threshold, row/column counts, and nonclaims.
   - A mocked row helper raising `P70FixedFitDiagnosticError` causes the
     script runner/helper path to write a failed row, write a top-level
     terminal failed status, return exit status `1`, and stop without
     attempting a second row.
   - Negative coverage confirms no transport object or success payload is
     produced on the failed path.

6. Limit the code diff to diagnostic plumbing and tests only.
   - No adjacent numerical-policy edits are allowed.
   - Any threshold/ridge/sweep/rank/degree/row/initializer value appearing in
     the diff may only be copied into a diagnostic payload or assertion.

## Required Local Checks

Before edit:

```bash
rg -n "fixed_ttsirt_fit_status_|CONDITION_NUMBER_VETO|fit_quality_diagnostics|p70_fixed_fitting_policy" bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
rg -n "PHASE6_BLOCKED_CONDITION_NUMBER_VETO_FIRST_ROW|CONDITION_NUMBER_VETO" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md
```

After edit:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
git diff --check -- bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-execution-plan-2026-06-16.md
```

## Forbidden Actions

- Do not run `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`.
- Do not run P69/P70 four-row diagnostics.
- Do not change `P70_CONDITION_NUMBER_VETO`, `P70_FIT_RIDGE`,
  `P70_FIXED_BRANCH_MAX_SWEEPS`, seeded epsilon, row count, degree, rank, or
  sweep order.
- Do not make condition-number veto nonblocking.
- Do not call this a numerical repair.
- Do not emit a transport object, density object, or success payload for a
  failed fit.
- Do not continue to later rows after a captured failed row.

## Result Artifact

Write:

`docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-result-2026-06-16.md`

The result must include local checks, exact code surfaces touched, what failed
diagnostics are now captured, what remains unknown, and the nonclaim that Phase
7 remains blocked.

## Stop Conditions

Stop if:

- failed-fit diagnostics cannot be captured without changing fitter semantics;
- focused tests require running the four-row diagnostic;
- a code change would make failed fits look admissible;
- Claude returns `VERDICT: REVISE` on a nontrivial blocker that cannot be
  repaired within five focused rounds.
