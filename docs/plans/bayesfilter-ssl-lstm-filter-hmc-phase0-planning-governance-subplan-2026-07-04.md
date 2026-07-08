# Phase 0 Subplan: Planning, Governance, And Review Launch

Date: 2026-07-04

Status: `DRAFT_UNDER_LOCAL_CHECK`

## Phase Objective

Create the master program, visible gated execution runbook, execution ledger,
Claude review ledger, stop handoff, all phase subplans, and the first bounded
Claude review bundle. Launch only the Phase 0 plan-review gate.

## Entry Conditions Inherited From Previous Phase

- No previous phase exists.
- User has approved the scientific scope: HMC over parameters plus filtering
  value/score adapters for Gaussian additive SSL-LSTM.
- User has rejected Particle Gibbs, conditional SMC, Gibbs, and
  parameter-by-parameter matching as the main target.
- Current dirty worktree changes outside this plan are treated as user work and
  must not be reverted.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-master-program-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-gated-overnight-execution-plan-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-execution-ledger-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-claude-review-ledger-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-visible-stop-handoff-2026-07-04.md`
- Phase 0 through Phase 8 subplans.
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-claude-review-bundle-2026-07-04.md`
- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-review-result-2026-07-04.md`

## Required Checks, Tests, And Reviews

- `git diff --check -- <new plan files>`
- Required-field coverage check over all phase subplans.
- Forbidden-boundary text check for detached execution, Claude executor
  authority, Particle Gibbs/conditional SMC as implementation target, automatic
  differentiation as target gradient, and unsupported scientific claims.
- Claude read-only review through
  `/home/ubuntu/python/claudecodex/scripts/claude_review_gate.sh`, if approved.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the master program, visible runbook, phase subplans, and review controls adequate to start Phase 1 without implementation or scientific overclaim? |
| Baseline/comparator | User requirements, BayesFilter AGENTS policy, and visible gated execution template. |
| Primary pass criterion | All required artifacts exist, local checks pass, and Claude returns `VERDICT: AGREE` or a recorded weaker fallback accepted by Codex as non-material. |
| Veto diagnostics | Missing subplan field, missing artifact, failed diff hygiene, review `REVISE` not repaired, or any plan text granting Claude execution authority. |
| Explanatory diagnostics | File count, grep coverage, and reviewer comments that do not affect the gate. |
| Not concluded | No implementation correctness, no HMC readiness, no filter sufficiency, no SSL-LSTM source-grounded model spec. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase0-planning-review-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not implement model code in Phase 0.
- Do not run HMC, GPU benchmarks, or scientific comparisons.
- Do not send whole repository contents to Claude.
- Do not let Claude edit files, run commands, launch workers, or approve
  boundary crossings.
- Do not claim source-faithfulness, exact posterior correctness, parameter
  recovery, method superiority, default readiness, or production readiness.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only when:

- Phase 0 result exists and says `PASSED`;
- local checks are recorded in the result;
- Claude review outcome is recorded in the Claude review ledger;
- Phase 1 subplan exists and has been reviewed for consistency and boundary
  safety;
- no unresolved human-required approval remains except future phase-specific
  approvals.

## Stop Conditions

- Claude review gate cannot be run in trusted/elevated context and the user does
  not approve the narrow wrapper.
- Claude and Codex do not converge after five rounds for the same material
  Phase 0 blocker.
- Required docs cannot be written under `docs/plans`.
- A boundary crossing is required before Phase 1.

## End-Of-Phase Protocol

1. Run the required local checks.
2. Write the Phase 0 result/close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
5. Send the bounded Phase 0 bundle to Claude as read-only reviewer and repair
   only material findings.
