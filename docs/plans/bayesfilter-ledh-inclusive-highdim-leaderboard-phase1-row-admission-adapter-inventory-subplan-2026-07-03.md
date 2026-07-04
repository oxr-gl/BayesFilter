# Phase 1 Subplan: Row Admission And Adapter Inventory

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE0`

## Phase Objective

Create a row-by-row LEDH admission ledger that says what LEDH computes for each
highdim row, whether that target matches the row target, and which callbacks or
adapters are required before execution.

## Entry Conditions Inherited From Previous Phase

- Phase 0 froze the baseline and row set.
- Phase 0 result confirms LEDH was excluded from the July 3 leaderboard.
- No code implementation has been accepted yet.

## Required Artifacts

- Row admission ledger:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-ledger-2026-07-03.json`.
- Phase 1 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase1-row-admission-adapter-inventory-result-2026-07-03.md`.
- Refreshed Phase 2 subplan if inventory changes runner scope.

## Required Checks, Tests, Reviews

- Search existing LEDH callbacks, runners, and benchmark scripts.
- For every row, record:
  - transition callback availability;
  - observation callback availability;
  - Jacobian or derivative availability;
  - parameter transform;
  - value target;
  - score target;
  - same-target status.
- For every potential score row, record the planned score-admission artifact:
  derivation, trusted fixed-randomness finite difference, exact oracle, or
  `blocked_score`.
- Claude read-only review of the ledger and Phase 2 handoff.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which highdim rows can LEDH evaluate as the same observed-data filtering target, and which are blocked or scoped? |
| Baseline/comparator | Current highdim row definitions and current LEDH implementation files. |
| Primary pass criterion | Each row has a direct classification: full row, scoped component, blocked no adapter, blocked value, or blocked score. |
| Veto diagnostics | Any row marked full without adapter evidence; parameterized SIR local complete-data evidence treated as full observed-data filtering evidence; score route admitted without a row-specific total-derivative admission artifact. |
| Explanatory diagnostics | Existing prior P8o SIR value-only cell and LGSSM score validation artifacts. |
| Not concluded | No new values, no score accuracy, no runtime ranking. |
| Artifact | Row admission ledger and Phase 1 result. |

## Forbidden Claims And Actions

- Do not call a row full if LEDH computes a different likelihood target.
- Do not use finite value output as evidence of score correctness.
- Do not mark `executed_value_score` unless the ledger identifies an exact
  derivation, trusted same-target finite-difference check, or exact oracle.
- Do not write code that changes model behavior in Phase 1 except a clearly
  documented inventory helper if needed.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- all rows have an admission classification;
- required LEDH adapters are listed;
- every requested row is retained in the ledger as full, scoped, or blocked;
- score rows have a planned total-derivative admission artifact;
- blocked rows have direct reasons;
- Phase 2 runner scope is updated to match the ledger.

## Stop Conditions

- A row target cannot be identified from local code/artifacts.
- Existing LEDH code cannot support any same-target row besides LGSSM without
  new model-design decisions.
- Claude review finds unsupported same-target claims after five repair rounds.
