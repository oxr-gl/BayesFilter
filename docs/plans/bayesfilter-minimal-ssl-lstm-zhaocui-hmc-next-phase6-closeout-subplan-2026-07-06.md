# Phase 6 Subplan: Closeout And Reset Memo

Date: 2026-07-06

Status: `READY_AFTER_PHASE5_RESULT_REVIEW`

## Phase Objective

Close the next program with an honest result inventory, reset memo, handoff,
review trail, unresolved boundaries, and explicit nonclaims.

## Entry Conditions Inherited From Previous Phase

- Prior phase has passed, failed, or been deferred with a result record.
- All executed runtime artifacts and reviews are locatable.
- Phase 5 runtime artifact exists at
  `docs/benchmarks/minimal_ssl_lstm_zhaocui_hmc_next_phase5_longer_gpu_xla_ladder_2026-07-06.json`
  and Phase 5 result review has converged or recorded a blocker.

## Required Artifacts

- Phase 6 closeout result.
- Reset memo.
- Visible stop handoff.
- Updated master/runbook status.

## Required Checks, Tests, Reviews

- Artifact existence checks.
- `git diff --check`.
- Claim-boundary scan.
- Final local or Claude review of closeout if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Has the program produced a recoverable and honest evidence trail for all three branches? |
| Baseline/comparator | Master program, phase results, runtime artifacts, review logs, and current git status. |
| Primary pass criterion | Closeout/result/reset/handoff files accurately summarize executed phases, checks, artifacts, decisions, failures, repairs, and nonclaims. |
| Veto diagnostics | Missing artifact path, unsupported claim, stale status, unrecorded boundary deferral, or evidence-class upgrade. |
| Explanatory diagnostics | Artifact list, check list, review statuses, and dirty-worktree preview. |
| Not concluded | Any claim not supported by executed phase evidence. |

## Forbidden Claims And Actions

Do not fill in results for phases that were deferred or not executed. Do not
upgrade descriptive or smoke evidence into convergence, readiness, or ranking
claims.

## Exact Next-Phase Handoff Conditions

No next phase. The handoff must state either `MASTER_PROGRAM_COMPLETE` or the
precise blocker/resume point.

## Stop Conditions

Stop if closeout cannot identify required artifacts or if review finds an
unfixed material claim/evidence mismatch.
