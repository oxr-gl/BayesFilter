# P00 Subplan: Governance And Review

Date: 2026-06-23

## Phase Objective

Verify that the `N=8192` paired-drift diagnostic lane is coherent, bounded,
artifact-complete, and safe to launch before any new GPU runs.

## Entry Conditions Inherited From Previous Phase

- Fixed-policy promotion-stress lane closed as
  `FIXED_POLICY_PROMOTION_STRESS_FAILED_OR_REPAIR_NEEDED`.
- The failure was a valid `N=8192` paired mean threshold veto, not a missing
  artifact or GPU crash.
- The owner requested the suggested next diagnostic/repair lane.

## Required Artifacts

- Master program.
- Visible runbook.
- Claude review ledger.
- Execution ledger.
- P00 result.
- P01 subplan.

## Required Checks, Tests, And Reviews

- Local path and section checks for required files.
- Local skeptical audit.
- Claude Opus max-effort read-only review of bounded paths.
- Patch fixable material issues and rerun review, stopping after five rounds
  for the same blocker.
- Write P00 result.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the diagnostic lane safe and specific enough to launch P01 replay/replication? |
| Baseline/comparator | Prior failed `N=8192` artifact is prerequisite context only. |
| Primary pass criterion | Required files exist, local consistency checks pass, Claude review returns `VERDICT: AGREE`, and P01 subplan is ready. |
| Veto diagnostics | Missing evidence contract, missing stop conditions, unsupported default/HMC/posterior claim, repair before replication, or review non-convergence. |
| Explanatory diagnostics | Review comments and prior artifact references. |
| Not concluded | No numerical result, no repair success, no default readiness. |
| Artifact | P00 result and review ledger. |

## Forbidden Claims/Actions

- Do not run benchmarks before P00 passes.
- Do not tune in P00.
- Do not claim default readiness.
- Do not let Claude edit, execute, or authorize phase crossing.

## Exact Next-Phase Handoff Conditions

Proceed to P01 only if local checks pass, Claude review returns
`VERDICT: AGREE`, and P00 result is written.

## Stop Conditions

- Material plan blocker does not converge after five review rounds.
- Continuing would require changing thresholds, changing defaults, or tuning
  before replay/replication.

## Skeptical Plan Audit

P00 checks wrong baselines, proxy metrics, missing stop conditions, unfair
comparison, hidden stochastic assumptions, stale context, GPU mismatch, and
artifact mismatch.

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.
