# Phase 8 Subplan: Final Regeneration And Closeout

Date: 2026-07-04

Status: `DRAFT_PENDING_PLAN_REVIEW`

## Phase Objective

Regenerate the combined leaderboard if all prior phases have settled, then
write the final closeout/reset artifacts with explicit admitted and blocked
rows.

## Entry Conditions Inherited From The Previous Phase

- Phases 0-7 have each either passed or recorded precise blockers for their
  targeted family.
- The row-family-specific blockers and admissions are explicit.
- Phase 7 has produced an honest UKF cleanup result or blocker.

## Required Artifacts

- Phase 8 result:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-phase8-final-regeneration-closeout-result-2026-07-04.md`
- Regenerated combined leaderboard JSON and Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-04.json`
  and
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-04.md`,
  or an explicit unchanged-leaderboard blocker note.
- Final visible stop handoff.
- Final reset memo:
  `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-reset-memo-2026-07-04.md`
  if needed.
- Visible execution ledger update.

## Required Checks, Tests, And Reviews

- Regenerate or explicitly preserve the combined leaderboard with blocker note.
- Confirm that no row silently changes target or family.
- Confirm that admitted rows have same-target provenance and blocked rows keep
  precise reasons.
- Run `git diff --check` on touched files.
- Claude review of the final result if any row admission status changes or the
  closeout wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the combined highdim leaderboard be regenerated with honest admitted and blocked rows after the blocker-by-blocker repairs? |
| Baseline/comparator | The July 3 combined leaderboard JSON/Markdown and the phase-local results from phases 0-7. |
| Primary criterion | The regenerated combined leaderboard preserves explicit blockers, admitted rows, and plain-language status without silent target drift. |
| Veto diagnostics | Silent row promotion, autodiff score admitted as analytical/manual, target drift, or missing blocker reason. |
| Explanatory diagnostics | Final row counts, residual blocker list, and any remaining runtime notes. |
| Not concluded | Posterior correctness, HMC readiness, or GPU superiority. |

## Forbidden Claims/Actions

- Do not silently drop blocked rows.
- Do not admit autodiff scores as analytical/manual scores.
- Do not rename a row target to make it pass.

## Exact Next-Phase Handoff Conditions

This is the final phase. Handoff is complete when:

- the combined leaderboard is regenerated or explicitly left unchanged with a
  precise blocker note;
- the closeout result exists;
- remaining blockers are explicit;
- the visible ledger is updated.

## Stop Conditions

Stop if:

- any row changes target without a result artifact explaining it;
- a score is admitted without same-target provenance;
- the final leaderboard cannot be regenerated without silent omissions.

## Phase-End Duties

At the end of Phase 8:

1. run the required local checks;
2. write the Phase 8 result / close record;
3. write the final closeout or reset memo at
   `docs/plans/bayesfilter-highdim-leaderboard-blocker-by-blocker-reset-memo-2026-07-04.md`;
4. review the final handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
