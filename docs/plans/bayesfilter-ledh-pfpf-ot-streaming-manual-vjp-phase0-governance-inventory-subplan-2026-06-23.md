# Streaming Manual VJP Phase 0 Subplan: Governance And Inventory

status: DRAFT
date: 2026-06-23
phase: S0-GOVERNANCE-INVENTORY

## Phase Objective

Lock the program boundary, inventory current dense/manual and streaming/replay
routes, and confirm that execution can start without repeating the P82
`N=10000` OOM route or making unsupported claims.

## Entry Conditions

- P82 closeout exists and records `P82_STOPPED_AT_P7_N10000_GPU_OOM_P8_NOT_RUN`.
- Current repo may be dirty; unrelated changes must be preserved.
- This program has a master program and visible runbook.

## Required Artifacts

- This subplan.
- `docs/plans/bayesfilter-ledh-pfpf-ot-streaming-manual-vjp-phase0-governance-inventory-result-2026-06-23.md`
- Refreshed S1 subplan, if S0 changes boundaries.
- Execution ledger entry.
- Claude review ledger entry for material plan review.

## Required Checks/Tests/Reviews

- `test -f` for the master program, runbook, and S0/S1 subplans.
- `rg` route-boundary scan for `GradientTape`, dense manual VJP, streaming
  replay, P82 OOM, and forbidden full-AD routes.
- `git diff --check` on new plan artifacts.
- Claude one-path read-only review of the master/runbook gate.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Is the streaming manual VJP program ready to start from verified current artifacts and route boundaries? |
| Baseline/comparator | P82 closeout, prior manual-adjoint M6/M8 results, current code anchors, and `memory.md` review rule. |
| Primary pass criterion | Inventory identifies the dense hand-coded VJP, the current streaming `GradientTape` replay route, the P82 OOM blocker, and the forbidden routes; local checks and Claude review pass. |
| Veto diagnostics | Missing P82 closeout; route inventory cannot find current backward replay; plan authorizes GPU or implementation before S1; Claude review not bounded to one exact path. |
| Explanatory only | Dirty worktree summary, route names, and exact line anchors. |
| Not concluded | No implementation correctness, no large-N memory success, no FD agreement, no default-policy change. |

## Forbidden Claims/Actions

- Do not edit implementation code in S0.
- Do not run GPU jobs.
- Do not run FD validation.
- Do not claim that the streaming VJP exists yet.
- Do not send code chunks or artifact packets to Claude.

## Exact Next-Phase Handoff Conditions

Advance to S1 only if:

- S0 result records the route inventory and skeptical audit;
- forbidden route scan finds no active command to run `transport_ad_mode=full`
  for governed `N=10000`;
- Claude review of the program/runbook gate returns `VERDICT: AGREE`;
- S1 subplan exists and still requires derivation before implementation.

## Stop Conditions

Stop and write a blocker if:

- current code no longer matches the known route split;
- P82 closeout or prior manual-adjoint artifacts are missing;
- Claude review does not converge after five rounds;
- implementation or GPU work is required to answer S0.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write the S0 result or blocker.
3. Draft or refresh S1.
4. Review S1 for consistency, correctness, feasibility, artifact coverage, and
   boundary safety.
