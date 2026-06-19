# P8h Phase 10 Subplan: Repo Hygiene And Commit-Boundary Review

Date: 2026-06-16

Status: `READY_FOR_REVIEW_AFTER_PHASE9`

## Phase Objective

Identify the exact P8h file set needed to preserve the completed P8h behavior,
evidence, provenance, and claim boundaries for later review or
machine-to-machine reconstruction, separate it from unrelated Zhao-Cui,
monograph, and user worktree changes, and write a commit-boundary result.
Commit or push only if the user explicitly requests it after reviewing the
boundary.

## Entry Conditions

- Phase 9 closeout and artifact refresh completed with a reviewed result or
  blocker.
- The Phase 9 final handoff artifact was written and reviewed.

## Required Artifacts

- P8h commit-boundary manifest listing intended P8h files and excluded
  unrelated dirty files.
- Consume the Phase 9 artifact index:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-artifact-index-2026-06-16.json`.
- Manifest coverage for P8h code/test files, phase subplans/results, generated
  diagnostic artifacts selected for preservation, Claude review ledger,
  execution ledger, stop/final handoff, refreshed matrices/results, and any
  environment/run-manifest artifacts needed to reconstruct the completed gate
  evidence on another machine.
- Phase 10 result:
  `docs/plans/bayesfilter-filtering-value-gradient-benchmark-p8h-phase10-repo-hygiene-result-2026-06-16.md`.

## Required Checks, Tests, Reviews

- `git status --short`.
- `git diff --check` over intended P8h files.
- Focused tests/checks required by the latest passing P8h result if code was
  modified after that result.
- Claude read-only review only if the boundary is ambiguous or includes
  material code/test artifacts.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Can the P8h artifact/code/test/provenance set be isolated for review and a possible later commit without pulling in unrelated lanes? |
| Baseline/comparator | Phase 9 result, reviewed Phase 9 final handoff, current git status, and the P8h master/runbook/result/ledger artifacts. |
| Primary criterion | Write a manifest that separates intended P8h files from unrelated dirty work, covers the P8h code/test/result/ledger/handoff/environment evidence set, and records required checks before any commit/push. |
| Veto diagnostics | Unrelated Zhao-Cui/monograph/user work included without explicit approval; generated cache/local state included; missing P8h code/test/result/ledger/handoff/environment artifacts needed for gate provenance; commit or push attempted without a fresh user request. |
| Explanatory diagnostics | Git status grouping, untracked file list, focused diff summaries, check output. |
| Not concluded | Remote synchronization, merge safety, bit-for-bit machine reproducibility, or final publish status unless a later explicit git operation or reproduction check is requested and succeeds. |

## Forbidden Claims And Actions

- Do not commit or push unless the user explicitly requests that action after
  seeing the Phase 10 boundary.
- Do not stage unrelated Zhao-Cui, monograph, cache, local environment, or user
  files as part of the P8h boundary.
- Do not hide negative or blocked P8h results from the boundary.

## Exact Next-Phase Handoff Conditions

The P8h gated program closes after the Phase 10 result records the boundary,
remaining exclusions, final check status, and any recommended explicit git
operation.

## Stop Conditions

- The P8h file set cannot be separated from unrelated dirty changes.
- Required final checks fail and need code or artifact repair.
- The user asks to commit/push but the worktree would include unrelated files
  without a separable boundary.
