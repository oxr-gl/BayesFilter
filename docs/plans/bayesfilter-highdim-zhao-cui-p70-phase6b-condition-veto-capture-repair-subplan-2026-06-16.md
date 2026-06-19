# P70 Phase 6b Subplan: Condition-Veto Capture And Repair Planning

metadata_date: 2026-06-16
status: READY_AFTER_CLAUDE_AGREE_PENDING_USER_APPROVAL
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p70-ukf-guided-fixed-branch-master-program-2026-06-16.md
phase: 6b
executor: Codex
reviewer: Claude Opus max effort, read-only and bounded

## Phase Objective

Repair the diagnostic surface exposed by the Phase 6 failure without rerunning
the four-row diagnostic.  The immediate problem is that the repaired fixed fit
hits `HighDimStatus.CONDITION_NUMBER_VETO` on the first row, but the current
source-route helper raises before preserving the failed fit's per-core
condition-number records, design shapes, and P70 policy payload.

Phase 6b should make condition-veto failures diagnosable.  It is not a
threshold-tuning phase and not a second Phase 6 diagnostic run.

## Entry Conditions Inherited From Phase 6

Phase 6b may begin only after Phase 6 has produced:

- `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md`;
- partial JSON artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostics-2026-06-16.json`;
- evidence that the exact approved Phase 6 command failed on
  `fixed_ttsirt_fit_status_CONDITION_NUMBER_VETO`;
- no rerun, retuning, or second diagnostic variant under the Phase 6 approval.

## Required Artifacts

- Phase 6b result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-result-2026-06-16.md`.
- Focused code/test patch only if needed.
- Updated P70 visible execution ledger.
- Updated P70 Claude review ledger.
- Refreshed Phase 6c or Phase 7 subplan only after the Phase 6b gate is
  reviewed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the diagnostic path preserve enough failed-fit information to distinguish ill-conditioning mechanisms after a P70 condition-number veto? |
| Baseline/comparator | Phase 6 failed first row, where `_p59_fixed_ttsirt_transport_from_values` raised before returning per-core failed-fit diagnostics. |
| Primary pass criterion | A focused patch and tests demonstrate that condition-veto failures can be represented in a diagnostic artifact or exception payload with fit status, per-core update statuses, condition thresholds, row/design dimensions, P70 policy payload when available, and nonclaims, without changing fitting thresholds or treating the failed fit as admissible. |
| Veto diagnostics | Any patch that changes Phase 6 thresholds; suppresses `CONDITION_NUMBER_VETO`; treats a failed fit as `HighDimStatus.OK`; runs the four-row diagnostic; runs a rank/degree ladder; changes row/rank/degree/sweep/ridge/initializer after observing Phase 6 output; or claims the bug is fixed. |
| Explanatory diagnostics | Per-core condition numbers, warning/veto indices, design matrix row/column counts, row adequacy, channel activity if fitted cores exist, target scales, and residual fields if available. |
| Not concluded | No repaired diagnostic pass, no validation, no rank/degree promotion, no scaling, no HMC readiness, no adaptive Zhao--Cui parity, no source-faithful claim for the seeded initializer. |
| Artifact preserving result | Phase 6b result note plus focused test output. |

## Required Checks/Tests/Reviews

Before any code edit:

```bash
rg -n "fixed_ttsirt_fit_status_|CONDITION_NUMBER_VETO|fit_quality_diagnostics|p70_fixed_fitting_policy" bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py
rg -n "PHASE6_BLOCKED_CONDITION_NUMBER_VETO_FIRST_ROW|CONDITION_NUMBER_VETO" docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6-rank-channel-normalizer-diagnostic-result-2026-06-16.md
```

If code is patched, focused checks must include:

```bash
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp python -m compileall -q bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py
CUDA_VISIBLE_DEVICES=-1 MPLCONFIGDIR=/tmp pytest -q tests/highdim/test_p70_phase6_diagnostic_script.py
git diff --check -- bayesfilter/highdim/source_route.py scripts/p70_phase6_rank_channel_normalizer_diagnostic.py tests/highdim/test_p70_phase6_diagnostic_script.py docs/plans/bayesfilter-highdim-zhao-cui-p70-phase6b-condition-veto-capture-repair-subplan-2026-06-16.md
```

Claude review must check:

- no threshold/row/rank/degree/sweep/ridge/initializer retuning;
- failed fits remain failed;
- diagnostic capture is sufficient to plan the next repair;
- no Phase 6 rerun is authorized by Phase 6b itself.

## Forbidden Claims/Actions

- Do not rerun `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`.
- Do not run any P69/P70 four-row diagnostic command.
- Do not change P70 thresholds after observing the Phase 6 failure.
- Do not make the condition-number veto nonblocking.
- Do not claim that seeded channels failed or succeeded; Phase 6 did not get
  far enough to answer that.
- Do not proceed to Phase 7 ladder.

## Exact Next-Phase Handoff Conditions

Phase 6b success does not unblock Phase 7.  It only restores observability for
failed P70 condition-veto fits.

Phase 6c or a repaired Phase 6 rerun may be proposed only if Phase 6b produces:

- a reviewed Phase 6b result;
- focused test evidence for condition-veto diagnostic capture;
- a clear diagnosis of what information is still missing;
- a refreshed subplan with a frozen evidence contract;
- Claude `VERDICT: AGREE`;
- explicit user approval for any future diagnostic command.

## Stop Conditions

Stop and write a blocker if:

- the failed-fit diagnostics cannot be captured without changing fitter
  semantics;
- capturing diagnostics would require rerunning the four-row Phase 6 command;
- the only available repair is threshold/ridge/sweep/row retuning after seeing
  Phase 6 output;
- a focused failing-path test or equivalent harness cannot demonstrate that
  veto failures serialize the intended diagnostics;
- Claude and Codex do not converge after five material review rounds.

## Skeptical Plan Audit

The main risk is turning a condition-number veto into an invitation to loosen
the condition threshold.  Phase 6b is not allowed to do that.  It may only
improve observability of the failed fit so the next plan can distinguish
between design-rank underdetermination, seeded-channel scaling, normal-equation
conditioning, row coverage, and implementation bugs.
