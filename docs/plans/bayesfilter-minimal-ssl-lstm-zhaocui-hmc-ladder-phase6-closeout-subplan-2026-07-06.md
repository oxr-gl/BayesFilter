# Phase 6 Subplan: Closeout And Reset Memo

Date: 2026-07-06

Status: `DRAFT_PENDING_PHASE5_RESULT`

## Phase Objective

Close the minimal scalar SSL-LSTM `zhaocui_fixed` HMC ladder with honest result
records, reset memo, updated handoff, and explicit evidence limits.

## Entry Conditions Inherited From Previous Phase

- Phase 5 result exists, either with GPU/XLA bridge result or explicit deferral.
- Earlier phase results classify target adapter, canary, repair, and short
  ladder outcomes.
- Remaining claims are bounded to the achieved evidence class.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-phase6-closeout-result-2026-07-06.md`
- Reset memo:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-reset-memo-2026-07-06.md`
- Updated stop handoff:
  `docs/plans/bayesfilter-minimal-ssl-lstm-zhaocui-hmc-ladder-visible-stop-handoff-2026-07-06.md`

## Required Checks, Tests, And Reviews

- Confirm phase result files exist through the final executed phase.
- Confirm generated artifacts exist for executed runtime phases.
- `git diff --check`.
- Update master program/runbook status.
- Final review, using external Claude if available and allowed, otherwise
  local Codex substitute review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Has the minimal HMC ladder produced a recoverable implementation/evidence trail and honest closeout for its stated scope? |
| Baseline/comparator | Master program, visible ledger, phase results, generated HMC artifacts, and current git status. |
| Primary pass criterion | Closeout result, reset memo, and handoff summarize files, checks, artifacts, evidence limits, failures, repairs, and next sensible work. |
| Veto diagnostics | Missing phase result, unsupported claim, stale handoff, missing artifact path, unrecorded dirty-worktree context, or evidence-class upgrade. |
| Explanatory diagnostics | File list, checks, artifact list, hard-veto summaries, and future-work notes. |
| Not concluded | Posterior correctness, HMC convergence, ranking, source-faithful parity, GPU/XLA production readiness, default readiness, or LEDH result. |

## Forbidden Claims And Actions

- Do not imply closeout upgrades evidence class.
- Do not claim broader runtime or scientific readiness than artifacts support.
- Do not modify unrelated dirty files.

## Exact Next-Phase Handoff Conditions

The master program may be closed only when:

- Phase 6 result exists;
- reset memo exists;
- stop handoff reflects final state;
- master program/runbook statuses are current;
- review path is recorded.

## Stop Conditions

Stop if a required artifact is missing, if closeout would need unsupported
claims, or if unresolved blockers remain that would confuse future continuation.

## End-Of-Phase Protocol

1. Run required closeout checks.
2. Write Phase 6 closeout result.
3. Write/update reset memo and stop handoff.
4. Record final review path and close or block the master program.
