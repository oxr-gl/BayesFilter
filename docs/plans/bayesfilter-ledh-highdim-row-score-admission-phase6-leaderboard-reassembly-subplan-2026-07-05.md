# Phase 6 Subplan: Leaderboard Reassembly And Row Test Expansion

metadata_date: 2026-07-05
status: DRAFT
master_program: docs/plans/bayesfilter-ledh-highdim-row-score-admission-master-program-2026-07-05.md
phase: 6

## Phase Objective

Rerun and rewrite the LEDH-inclusive highdim leaderboard using only rows that
passed the earlier same-target value and no-tape score gates, while preserving
explicit blocked statuses for the remaining rows.

## Entry Conditions Inherited From Previous Phase

- Phases 1-5 are complete with explicit pass/block records.
- The admitted-row set and blocked-row set are frozen from those earlier
  results.
- Phase 5 confirmed that generalized SV remains blocked because callback
  existence is not a reviewed source-row adapter bridge.

## Required Artifacts

- Phase 6 result:
  `docs/plans/bayesfilter-ledh-highdim-row-score-admission-phase6-leaderboard-reassembly-result-2026-07-05.md`
- Updated leaderboard JSON/Markdown artifacts.
- Expanded row tests:
  - one correctness/memory test per newly admitted row;
  - one all-row integration status test.

## Required Checks/Tests/Reviews

Expected checks if the phase is executed:

- focused leaderboard JSON content checks;
- row-level correctness and memory tests;
- no-autodiff route metadata checks;
- trusted GPU runs for `N=10000` rows;
- `git diff --check` on changed leaderboard artifacts and tests.

Material review required:

- Claude read-only review of the Phase 6 result and the final closeout decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which LEDH highdim rows are genuinely admitted after the row-specific repairs, and can the leaderboard be updated without false score claims? |
| Baseline/comparator | The July 3 LEDH-inclusive leaderboard, row-specific Phase 1-5 results, and row-specific correctness/memory tests. |
| Primary criterion | The leaderboard lists each row with truthful admitted or blocked status, and every admitted score row has row-specific no-tape score evidence plus `N=10000` tests. |
| Veto diagnostics | Any row promoted without row-specific same-target and score evidence; any blocked row silently presented as admitted; any leaderboard text that confuses scoped diagnostics with full rows. |
| Explanatory diagnostics | Runtime and memory comparisons, compile notes, and frozen non-LEDH comparisons. |
| Not concluded | No runtime cross-ranking against frozen rows unless separately rerun; no HMC claim; no scientific superiority claim from the leaderboard alone. |

## Forbidden Claims/Actions

- Do not promote any row just because a neighboring family passed.
- Do not claim full all-model score readiness unless all blocked rows are
  actually repaired.
- Do not use runtime or memory success as a substitute for score correctness.

## Exact Next-Phase Handoff Conditions

There is no next repair phase in this program. The closeout decision must state:

1. the admitted rows;
2. the blocked rows;
3. the exact supporting artifacts for each admitted row;
4. the exact remaining blockers, if any.

## Stop Conditions

Stop if the phase cannot truthfully enumerate admitted and blocked rows from the
earlier phase results, or if a row lacks the required row-specific tests.
