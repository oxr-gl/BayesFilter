# Phase 6 Subplan: Final Leaderboard Regeneration And Closeout

Date: 2026-07-01

Status: `DRAFT_PENDING_PHASE5_REVIEW`

## Phase Objective

Regenerate the highdim leaderboard, write the final Zhao-Cui completion result,
and close the visible runbook with unresolved blockers and nonclaims explicit.

## Entry Conditions Inherited From Previous Phase

- Phase 5 closed batched/GPU/calibration statuses.
- All Zhao-Cui rows are admitted or precisely blocked.
- No SGQF work was pulled into this program.

## Required Artifacts

- Regenerated highdim leaderboard JSON/Markdown.
- Final Phase 6 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-leaderboard-completion-phase6-final-regeneration-result-2026-07-01.md`
- Reset/closeout memo if row statuses materially changed.
- Updated Claude review ledger.
- Updated visible execution ledger.
- Final visible stop handoff.

## Required Checks, Tests, Reviews

- Leaderboard regeneration command.
- JSON validity check.
- Contract assertions: no autodiff score admitted for Zhao-Cui; no source
  faithfulness claim without anchors; blocked rows not ranked.
- `git diff --check` on touched files.
- Claude read-only final result review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the Zhao-Cui leaderboard completion program internally consistent and ready to hand off? |
| Baseline/comparator | Phase 0 inventory and phase results. |
| Primary criterion | Final leaderboard and closeout agree on admitted rows, blocked rows, evidence, and nonclaims. |
| Veto diagnostics | Autodiff analytical score; missing blocker reason; SGQF status changed by this program without scope; GPU claim without trusted evidence; exact likelihood or posterior claim. |
| Explanatory diagnostics | Runtime, row counts, score norms, calibration summaries. |
| Not concluded | Exact likelihood correctness, posterior correctness, HMC convergence, universal GPU speedup, release/default readiness. |
| Artifact | Final result, regenerated leaderboard, stop handoff. |

## Forbidden Claims And Actions

- Do not commit or push unless the user asks.
- Do not modify defaults, release, tag, or CI.
- Do not state "complete leaderboard" unless every intended Zhao-Cui cell is
  admitted or explicitly blocked as non-admissible.

## Exact Next-Phase Handoff Conditions

No next phase. Close the runbook with final status and safest next action.

## Stop Conditions

Stop if final artifacts disagree, if a row status cannot be supported by
evidence, or if Claude and Codex do not converge after five review rounds.

## End-of-Subplan Protocol

1. Run the required local checks.
2. Write the Phase 6 result / close record.
3. Refresh the stop handoff.
4. Review the final result for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
