# Phase 0 Subplan: Launch Boundary Freeze

Date: 2026-07-03

Status: `DRAFT_PENDING_CLAUDE_REVIEW`

## Phase Objective

Freeze the comparison boundary before implementation: current baseline artifact,
row set, algorithm set, LEDH nonclaims, permissions, and review protocol.

## Entry Conditions Inherited From Previous Phase

- Human request asks for a LEDH-inclusive highdim leaderboard across the same
  model rows as `docs/benchmarks/benchmark_two_lane_highdim_leaderboard.py`.
- Current July 3 highdim leaderboard exists and excludes LEDH.
- No phase has permission to reinterpret the July 3 artifact as a LEDH run.

## Required Artifacts

- This subplan.
- Master program:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-master-program-2026-07-03.md`.
- Visible runbook:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-gated-execution-runbook-2026-07-03.md`.
- Execution ledger:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-visible-execution-ledger-2026-07-03.md`.
- Claude review ledger:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-claude-review-ledger-2026-07-03.md`.
- Phase result:
  `docs/plans/bayesfilter-ledh-inclusive-highdim-leaderboard-phase0-launch-boundary-freeze-result-2026-07-03.md`.

## Required Checks, Tests, Reviews

- Local static check that all phase plan paths exist.
- Local grep check that the July 3 leaderboard records LEDH exclusion.
- Bounded Claude read-only review of master program, runbook, and Phase 0/1
  subplans by exact path.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the target rows, algorithms, baseline, and nonclaims frozen before implementation? |
| Baseline/comparator | July 3 highdim leaderboard JSON and current highdim runner. |
| Primary pass criterion | Phase 0 result states the frozen row set, algorithm set, baseline artifact, LEDH exclusion status, and next phase handoff. |
| Veto diagnostics | Missing baseline artifact; plan claims LEDH already exists in July 3 full leaderboard; no stop conditions; no Claude read-only role boundary. |
| Explanatory diagnostics | Dirty worktree summary and prior LEDH value-only artifacts. |
| Not concluded | No LEDH value correctness, score correctness, or all-model readiness. |
| Artifact | Phase 0 result plus Claude review ledger entry. |

## Forbidden Claims And Actions

- Do not claim LEDH has already run in the current full leaderboard.
- Do not edit algorithm code in Phase 0.
- Do not run GPU benchmarks in Phase 0 except a later trusted device probe if
  Phase 1 requires it.
- Do not launch detached background execution.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- baseline and row inventory are frozen;
- Claude review returns `VERDICT: AGREE` or a reviewed fix is applied;
- Phase 1 subplan exists and names row-admission evidence needed for every row.

## Stop Conditions

- Claude health probe fails twice in trusted context.
- Baseline artifact cannot be found.
- Current runner row set cannot be identified.
- Review finds a material plan flaw that is not fixed after five rounds.
