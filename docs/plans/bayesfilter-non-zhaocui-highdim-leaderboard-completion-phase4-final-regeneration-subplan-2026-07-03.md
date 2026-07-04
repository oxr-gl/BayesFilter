# Phase 4 Subplan: Final Non-Zhao-Cui Regeneration And Closeout

Date: 2026-07-03

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Regenerate the authoritative highdim leaderboard pair and close the non-Zhao-
Cui completion program with the final SGQF/UKF decision table for all relevant
rows.

## Entry Conditions Inherited From Previous Phase

- Phases 1-3 have closed the remaining non-Zhao-Cui row states as admitted,
  blocked, or value-only with precise reasons.
- The already-complete baseline rows remain preserved.

## Required Artifacts

- Phase 4 result:
  `docs/plans/bayesfilter-non-zhaocui-highdim-leaderboard-completion-phase4-final-regeneration-result-2026-07-03.md`
- regenerated leaderboard JSON and Markdown
- updated execution ledger, review ledger, and stop handoff

## Required Checks/Tests/Reviews

This phase requires a reviewed executable refresh before any regeneration
command.

Required read-only Claude reviews:

- Phase 4 result,
- final stop handoff / closeout state.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the authoritative highdim leaderboard be regenerated so SGQF and UKF are reported honestly for every non-Zhao-Cui tested row under the reviewed value/score contract? |
| Baseline/comparator | current July 3 leaderboard artifacts plus reviewed non-Zhao-Cui row results from this program. |
| Primary criterion | The regenerated leaderboard faithfully reflects the reviewed SGQF/UKF admissions and blockers for all non-Zhao-Cui tested rows, with no silent status upgrades. |
| Veto diagnostics | stale blocker retained after reviewed admission; blocked row emitted as executed; value-only row emitted as value+score; autodiff score emitted as analytical; unexplained gap hidden from the row notes. |
| Explanatory diagnostics | regenerated row table, row status summary, runtime/status notes, and final nonclaims. |
| Not concluded | No HMC readiness, no top-level API promotion, and no production/default claim. |
| Artifact | final leaderboard artifacts, Phase 4 result, updated ledgers, and stop handoff. |

## Forbidden Claims And Actions

- Do not silently upgrade any row status while regenerating the table.
- Do not use the final table as HMC or production evidence.
- Do not claim broad exactness beyond the reviewed per-row contracts.
