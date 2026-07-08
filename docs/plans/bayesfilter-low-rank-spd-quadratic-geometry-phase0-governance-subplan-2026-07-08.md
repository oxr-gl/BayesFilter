# Phase 0 Subplan: Low-Rank SPD Quadratic Geometry Governance

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`

## Phase Objective

Create the master program, visible runbook, initial subplans, and compact review bundle for the low-rank SPD quadratic geometry utility before implementation begins.

## Entry Conditions

- User requested execution of the reviewed prompt.
- Current repository is `/home/ubuntu/python/BayesFilter`.
- Existing dirty worktree must be preserved.
- This work is classified as `extension_or_invention`, not Zhao-Cui source-faithful implementation.

## Required Artifacts

- Master program: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-master-program-2026-07-08.md`
- Visible runbook: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-gated-execution-runbook-2026-07-08.md`
- Execution ledger: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-visible-execution-ledger-2026-07-08.md`
- Phase 0 subplan: this file
- Phase 1 subplan: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase1-utility-subplan-2026-07-08.md`
- Review bundle: `docs/reviews/bayesfilter-low-rank-spd-quadratic-geometry-phase0-review-bundle-2026-07-08.md`
- Phase 0 result: `docs/plans/bayesfilter-low-rank-spd-quadratic-geometry-phase0-governance-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- Review the plan bundle through Claude read-only review gate if available.
- If Claude is blocked or unavailable, write a Codex substitute review.
- No code tests are required in Phase 0 because Phase 0 creates planning artifacts only.
- Run `git diff --check` after writing planning artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the execution plan internally consistent, bounded, and aligned with BayesFilter evidence policy before code edits? |
| Baseline/comparator | Existing Phase 5 minimal SSL-LSTM geometry path and 2026-07-07 geometry/tau-gate result. |
| Primary criterion | Plan artifacts exist, include research intent/evidence contract/skeptical audit/forbidden claims, and review does not find unresolved material blockers. |
| Veto diagnostics | Missing stop conditions, unsupported default/promotion claims, hidden Zhao-Cui faithfulness claim, hidden default-policy change, review `REVISE` unresolved, dirty-worktree destructive action. |
| Explanatory only | Review availability, review transport status, minor style findings. |
| Not concluded | No implementation correctness, no HMC readiness, no posterior correctness, no sampler convergence. |
| Preserving artifact | Phase 0 result note and review status/log references. |

## Forbidden Claims And Actions

- Do not edit implementation code in Phase 0.
- Do not launch long diagnostics in Phase 0.
- Do not claim Claude approval authorizes scientific/runtime/default-policy boundaries.
- Do not claim this work is Zhao-Cui source-faithful.
- Do not revert unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Plan/runbook/ledger/review bundle/Phase 1 subplan are written.
- Review gate returns `AGREE`, bounded fallback `AGREE`, or a documented Codex substitute review with no material blockers.
- `git diff --check` passes.
- Phase 0 result records review status and nonclaims.

## Stop Conditions

- Claude/Codex review finds a material plan issue that cannot be patched locally.
- Proceeding would require package install, network fetch, destructive git operation, default-policy change, or a scientific claim boundary.
- `git diff --check` fails and cannot be repaired locally.

## Skeptical Audit

Phase 0 passes the skeptical audit if the master program keeps the research question separate from implementation tasks, treats residuals and short diagnostics as non-promoting, has explicit stop conditions, and does not ask artifacts to prove HMC convergence. This subplan satisfies those constraints.
