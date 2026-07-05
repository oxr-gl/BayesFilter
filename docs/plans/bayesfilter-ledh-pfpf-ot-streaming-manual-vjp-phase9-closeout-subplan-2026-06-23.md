# Streaming Manual VJP Phase 9 Subplan: Closeout

status: DRAFT
date: 2026-06-23
phase: S9-CLOSEOUT

## Phase Objective

Close the streaming manual VJP program with a code-doc-result audit, final
status, review trail, and stop handoff.

## Entry Conditions

- S8 completed or blocked with a reviewed result.

## Required Artifacts

- S9 closeout result.
- Updated visible stop handoff.
- Review ledger entry.

## Required Checks/Tests/Reviews

- `git diff --check` on all artifacts touched by this program.
- `rg` scan for unsupported claims and forbidden route claims.
- Focused tests only if implementation changed after S6.
- Claude one-path review of S9 result.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the program results, code, docs, limitations, and downstream handoff internally consistent? |
| Baseline/comparator | S0-S8 results, implementation diffs, tests, and review ledger. |
| Primary pass criterion | Closeout records final phase reached, artifacts, tests run, review trail, blockers, nonclaims, and next safe action. |
| Veto diagnostics | Unsupported default/HMC/posterior/production claim; missing blocker; missing review trail; artifact mismatch. |
| Explanatory only | Dirty worktree summary and warning notes. |
| Not concluded | Anything not explicitly passed by the phase gates. |

## Forbidden Claims/Actions

- Do not add new implementation in S9.
- Do not hide failed rungs.
- Do not promote proxy diagnostics.

## Exact Next-Phase Handoff Conditions

This is the final phase.  Handoff must say whether P82 may resume, remains
blocked, or requires a new remediation program.

## Stop Conditions

Stop if:

- closeout cannot reconcile artifacts and code;
- final review does not converge after five rounds.

## End-Of-Phase Protocol

1. Run required local checks.
2. Write S9 closeout.
3. Update visible stop handoff.
4. Review final closeout for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
