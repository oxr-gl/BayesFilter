# P71 Phase 0 Subplan: Governance And Current-Evidence Reset

metadata_date: 2026-06-16
status: DRAFT_PENDING_LOCAL_CHECKS_AND_CLAUDE_REVIEW
master_program: docs/plans/bayesfilter-highdim-zhao-cui-p71-sir-d18-full-validation-master-program-2026-06-16.md
phase: 0

## Phase Objective

Create the launch ledger for P71 by restating the current d18 evidence,
source anchors, blockers, and nonclaims before any validation command is run.

## Entry Conditions Inherited From Previous Phase

- User asked for a master program and phase subplans to fully test SIR d=18.
- Current repo contains P59/P60/P66/P70 source-route artifacts.
- `origin/main` has been merged into the current branch.

## Required Artifacts

- Phase 0 result note.
- Source-anchor ledger table.
- Current-evidence table separating execution-only, numeric, rank, accuracy,
  performance, gradient, and HMC ledgers.
- Commit/worktree drift reconciliation against the P70 Phase 6 blocker artifact
  recorded at git commit `5fdd0819ce0eb2994fb0509e66d9e9cce5f2d47c`.
- Refreshed Phase 1 subplan if the current blocker list changes.

## Required Checks/Tests/Reviews

- Read-level verification of cited source/local anchors using bounded
  `sed -n`/`rg -n` commands, recording whether each anchor exists and matches
  the intended source-route operation.
- `rg` check for required anchor tokens in this plan packet as a secondary
  completeness check only.
- Drift check comparing current files against the P70 blocker commit for:
  `bayesfilter/highdim/source_route.py`, `bayesfilter/highdim/fitting.py`,
  `tests/highdim/test_fixed_branch_fit.py`,
  `scripts/p70_phase6_rank_channel_normalizer_diagnostic.py`, and relevant P70
  result/subplan artifacts.
- `git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p71-*`.
- Claude read-only review if Phase 0 changes the master plan or Phase 1 gate.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the exact pre-validation state of SIR d=18? |
| Baseline/comparator | P59-9e execution-only pass, P8-B6 closure row, P70 Phase 5 unit-test pass, and P70 Phase 6 condition-number veto. |
| Primary criterion | The result identifies all current evidence, blockers, anchor-read evidence, and P70 commit/worktree drift without promoting execution-only evidence to accuracy/rank/scaling claims. |
| Veto diagnostics | Missing source anchors, stale P70 status, unreconciled material drift since the P70 blocker artifact, or any claim that d18 accuracy is already established. |
| Explanatory diagnostics | File/line anchors, status tokens, dirty-worktree note, drift table, and known test/script hooks. |
| Not concluded | No d18 accuracy, no rank convergence, no d50/d100 scaling, no HMC readiness. |
| Artifact | Phase 0 result note. |

## Forbidden Claims/Actions

- Do not run d18 validation commands.
- Do not patch implementation code.
- Do not claim the P70 condition-number blocker is resolved.
- Do not treat token presence as source-anchor verification.
- Do not use Claude as execution authority.

## Exact Next-Phase Handoff Conditions

Phase 1 may begin only if Phase 0 records:

- current source anchors;
- current blockers;
- current nonclaims;
- read-level anchor verification and P70 blocker drift reconciliation;
- exact commands/tests proposed for condition-veto capture;
- no source-governance veto.

## Stop Conditions

Stop if source anchors are missing, if the current code state or material drift
contradicts the P71 master program, or if the intended validation target is
unclear.
