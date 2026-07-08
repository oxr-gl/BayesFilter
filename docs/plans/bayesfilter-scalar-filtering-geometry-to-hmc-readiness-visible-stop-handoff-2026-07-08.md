# Scalar Filtering Geometry To HMC Readiness Visible Stop Handoff

Date: 2026-07-08
Status: `NOT_STOPPED`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
Runbook: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-gated-execution-runbook-2026-07-08.md`

## Current State

The visible runbook has started Phase 0 governance. No implementation, benchmark, HMC, or long diagnostic command has been launched by this program yet.

## Resume Instructions If Interrupted

1. Read the master program, visible runbook, ledger, and current phase subplan.
2. Confirm the dirty worktree is preserved and unrelated files are not reverted.
3. Continue from the latest ledger entry.
4. Before any nontrivial experiment, restate the evidence contract and skeptical audit.
5. For material review, use the compact bundle and `claude_review_gate.sh`; if Claude is unavailable or external review is policy-blocked for private-context transfer risk, record the gate status and write a Codex substitute review labeled weaker than Claude review.

## Stop Conditions To Preserve

Stop rather than continue if the next action would require package installation, network fetch, credentials, destructive git/filesystem actions, default-policy changes, model-file edits, or unsupported scientific/runtime claims.
