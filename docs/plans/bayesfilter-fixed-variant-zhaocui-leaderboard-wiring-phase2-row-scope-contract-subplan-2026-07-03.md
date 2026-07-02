# Phase 2 Subplan: Row Scope And Evidence Contract

Date: 2026-07-03

Status: `READY_EXECUTED_PHASE2_RESULT_REV1_CLAUDE_AGREE`

## Phase Objective

Define the exact leaderboard row semantics for the fixed-variant Zhao-Cui SIR
entry before runner code is edited.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has identified the fixed-variant callable(s) and classified the
  computed quantity.

## Required Artifacts

- Phase 2 result:
  `docs/plans/bayesfilter-fixed-variant-zhaocui-leaderboard-wiring-phase2-row-scope-contract-result-2026-07-03.md`
- Row contract fields:
  row id, algorithm id, route role, target scope, value/score status,
  score provenance, sidecar status, forbidden claims, and readiness summary.

## Required Checks / Tests / Reviews

- `rg` checks against current leaderboard tests and runner for the old SIR row.
- If the scope changes existing test expectations, write focused test changes
  in Phase 3 only after this result passes.
- Claude read-only review required for the Phase 2 result because it is a
  material claim-boundary decision.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Should the fixed-variant SIR evidence be a main leaderboard row, a scoped sidecar, or a blocked full-filtering row? |
| Baseline/comparator | Phase 1 inventory, current leaderboard schema, and owner directive. |
| Primary criterion | The row contract states exact target/computed quantity and avoids mismatch between full observed-data filtering and local complete-data evidence. |
| Veto diagnostics | Full filtering readiness claimed without derivative blockers closed; row id lacks theta semantics; sidecar evidence ranked as main leaderboard timing; retained-grid route admitted. |
| Explanatory diagnostics | Existing P91 statuses and row-summary implications. |
| Not concluded | No numerical regeneration, no production default change, no posterior correctness. |
| Artifact | Phase 2 result and reviewed contract table. |

## Forbidden Claims / Actions

- Do not edit runner code.
- Do not regenerate leaderboard artifacts.
- Do not use soft/evasive language to hide target mismatch.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if Phase 2 gives a direct verdict:

- `scoped_component_row_admitted`;
- `main_row_admitted_under_declared_scope`;
- `sidecar_only_not_main_row`;
- or `blocked_until_full_filtering_derivatives`.

## Stop Conditions

- The target scope requires human decision.
- Claude review finds an unpatched overclaim after five rounds.

## End-Of-Subplan Protocol

1. Run required local checks.
2. Write Phase 2 result / close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
