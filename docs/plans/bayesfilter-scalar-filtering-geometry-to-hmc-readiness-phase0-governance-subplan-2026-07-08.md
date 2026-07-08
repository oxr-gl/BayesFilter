# Phase 0 Subplan: Scalar Filtering Geometry To HMC Readiness Governance

Date: 2026-07-08
Status: `DRAFT_READY_FOR_REVIEW`
Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`

## Phase Objective

Create and review the master program, visible runbook, execution ledger, stop handoff, and compact Claude review bundle before any implementation, benchmark, or HMC action begins.

## Entry Conditions

- User requested execution of the gated runbook prompt.
- Current repository is `/home/ubuntu/python/BayesFilter`.
- Prior complete-data oracle geometry result exists and passed only within its declared scope.
- Existing dirty worktree and untracked artifacts must be preserved.
- This program is not a Zhao-Cui source-faithfulness program and must not claim to close that gate.

## Required Artifacts

- Master program: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-master-program-2026-07-08.md`
- Visible runbook: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-gated-execution-runbook-2026-07-08.md`
- Execution ledger: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-execution-ledger-2026-07-08.md`
- Stop handoff: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-visible-stop-handoff-2026-07-08.md`
- Phase 0 subplan: this file
- Review bundle: `docs/reviews/scalar-filtering-geometry-hmc-phase0-review-bundle-2026-07-08.md`
- Phase 0 result: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase0-governance-result-2026-07-08.md`
- Phase 1 subplan draft at phase close: `docs/plans/bayesfilter-scalar-filtering-geometry-to-hmc-readiness-phase1-filtering-geometry-subplan-2026-07-08.md`

## Required Checks, Tests, Reviews

- `git diff --check` after creating planning artifacts.
- Claude read-only review gate for the compact Phase 0 bundle if available.
- If Claude is unavailable, use the review gate probe/fallback status and write a Codex substitute review.
- If Claude review is policy-blocked because the bundle would transfer private repository context externally, do not work around the block; record `CLAUDE_REVIEW_POLICY_BLOCKED` and write a Codex substitute review labeled weaker than Claude review.
- No code tests or benchmarks are required in Phase 0.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the runbook internally consistent, bounded, and aligned with BayesFilter scientific-evidence policy before code or experiment execution? |
| Baseline/comparator | Passed complete-data oracle geometry result plus existing filtering-score helper paths. |
| Primary criterion | Plan artifacts exist, include research intent/evidence contract/skeptical audit/forbidden claims, and review finds no unresolved material blocker. |
| Veto diagnostics | Missing stop conditions, hidden default/scientific claims, hidden source-faithfulness claim, coordinate ambiguity, unresolved `REVISE`, failed `git diff --check`, or destructive action. |
| Explanatory only | Review transport status, minor style findings, exact wording repairs. |
| Not concluded | No implementation correctness, no filtering-likelihood validity, no HMC readiness, no HMC convergence, no posterior correctness. |
| Preserving artifact | Phase 0 result note and review status/log references. |

## Forbidden Claims And Actions

- Do not edit implementation code in Phase 0.
- Do not launch benchmarks, HMC, or long diagnostics in Phase 0.
- Do not claim Claude approval authorizes scientific/runtime/default-policy boundaries.
- Do not claim this program is source-faithful Zhao-Cui work.
- Do not revert unrelated dirty worktree files.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Required Phase 0 artifacts are written.
- `git diff --check` passes.
- Claude review gate returns `AGREE` or bounded fallback `AGREE`, or a documented Codex substitute review records that Claude was unavailable or policy-blocked, inspects the same required Phase 0 governance artifacts including the ledger and stop handoff, and finds no material blockers.
- Phase 0 result records review status, checks, non-claims, and next action.
- Phase 1 subplan is drafted or refreshed before any Phase 1 command runs.

## Stop Conditions

- Claude/Codex review finds a material issue that cannot be patched locally.
- Proceeding would require package install, network fetch, credentials, destructive git/filesystem action, default-policy change, model-file edit, or unsupported scientific/runtime claim.
- `git diff --check` fails and cannot be repaired locally.

## Skeptical Audit

- Wrong baseline: Phase 0 uses the passed oracle geometry only as an anchor, not as proof that filtering geometry works.
- Proxy metric risk: no residual, acceptance, or trajectory metric is a Phase 0 pass criterion.
- Missing stop conditions: stop conditions are explicit above and in the runbook.
- Unfair comparison: no ranking or sampler comparison occurs in Phase 0.
- Hidden assumptions: scalar/four-parameter scope and CPU-hidden debug exceptions are labeled.
- Stale context: the plan cites the 2026-07-08 oracle result and previous tuning issues.
- Environment mismatch: no GPU or CPU benchmark is launched in this phase.
- Artifact adequacy: the artifacts answer planning consistency only.

Audit result: `PASS_WITH_BOUNDARIES`. Phase 0 can proceed to local document check and review.
