# Phase 5 Subplan: Merge And Cross-Algorithm Comparison

Date: 2026-07-03

Status: `DRAFT_PENDING_PHASE4`

## Phase Objective

Merge LEDH row evidence into a new highdim leaderboard artifact and compare
LEDH to existing algorithms without changing the meaning of baseline rows.

## Entry Conditions Inherited From Previous Phase

- Phase 4 raw LEDH artifacts exist for all admitted rows.
- Blocked and scoped rows are explicitly recorded.
- Existing non-LEDH baseline artifact remains frozen.

## Required Artifacts

- Merged JSON:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.json`.
- Merged Markdown:
  `docs/plans/bayesfilter-two-lane-highdim-ledh-inclusive-leaderboard-results-2026-07-03.md`.
- Phase 5 result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase5-merge-comparison-result-2026-07-03.md`.
- Updated Phase 6 subplan.

## Required Checks, Tests, Reviews

- JSON schema/content check.
- Row count check: every model row has all intended algorithms or a direct
  blocked status.
- Compare row statuses, values, MCSE, score status, runtime, and device status.
- Claude review of merged artifact claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the merged leaderboard compare LEDH with the other algorithms on every row while preserving target and score status? |
| Baseline/comparator | July 3 non-LEDH highdim leaderboard plus Phase 4 LEDH artifacts. |
| Primary pass criterion | Merged artifact exists and has no hidden missing LEDH rows, no unsupported score rows, and no baseline mutation. |
| Veto diagnostics | Missing row; hidden blocked row; value-only row ranked as score-ready; scoped row ranked as full row; baseline row changed without recorded reason. |
| Explanatory diagnostics | Runtime and MCSE comparisons. |
| Not concluded | No posterior correctness, no HMC readiness, no broad superiority claim. |
| Artifact | Merged JSON/MD and Phase 5 result. |

## Forbidden Claims And Actions

- Do not overwrite the July 3 non-LEDH artifact.
- Do not rank rows whose targets differ.
- Do not call MCSE-stable value evidence score evidence.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- merged artifact passes content checks;
- Claude review agrees or material issues are patched;
- all nonclaims are direct and plain.

## Stop Conditions

- Merged artifact cannot preserve row target distinctions.
- LEDH artifacts and baseline row IDs cannot be reconciled.
- Claude review finds a material unsupported claim after five repair rounds.
