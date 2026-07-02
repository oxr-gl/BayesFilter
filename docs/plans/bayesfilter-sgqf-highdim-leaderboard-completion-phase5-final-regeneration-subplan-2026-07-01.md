# Phase 5 Subplan: Final Leaderboard Regeneration And Closeout

Date: 2026-07-01

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Regenerate the authoritative highdim leaderboard artifacts and close with the
final SGQF row-status decision table for all tested models.

## Entry Conditions Inherited From Previous Phase

- Phase 4 has closed the SGQF analytical score gate for every newly executed
  SGQF row.
- Every remaining SGQF row is now either admitted with value/analytical score or
  blocked/value-only with a precise reason.

## Required Artifacts

- Phase 5 result:
  `docs/plans/bayesfilter-sgqf-highdim-leaderboard-completion-phase5-final-regeneration-result-2026-07-01.md`
- regenerated leaderboard JSON and Markdown
- updated execution ledger, Claude review ledger, and stop handoff

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any leaderboard
regeneration command.

Required read-only Claude reviews:

- Phase 5 result,
- final stop handoff / closeout state.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the authoritative highdim leaderboard be regenerated so SGQF, UKF, and Zhao-Cui are reported honestly for every tested row under the reviewed value/score contract? |
| Baseline/comparator | current July 1 leaderboard artifacts plus reviewed SGQF row results from this program. |
| Primary criterion | The regenerated leaderboard faithfully reflects the reviewed SGQF admissions and blockers for all tested rows, with no silent status upgrades. |
| Veto diagnostics | stale blocker retained after reviewed admission; blocked row emitted as executed; value-only row emitted as value+score; autodiff score emitted as analytical; unexplained gap hidden from the row notes. |
| Explanatory diagnostics | regenerated row table, row status summary, runtime/status notes, and final nonclaims. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | final leaderboard artifacts, Phase 5 result, updated ledgers, and stop handoff. |

## Forbidden Claims And Actions

- Do not silently upgrade any row status while regenerating the table.
- Do not use the final table as HMC or production evidence.
- Do not claim broad SGQF exactness beyond the reviewed per-row contracts.
