# P00 Subplan: Governance, Local Audit, And Claude Review

Date: 2026-06-23

## Phase Objective

Verify that the fixed-policy promotion-stress program is coherent, bounded,
artifact-complete, and safe to launch before any new GPU or HMC runs.

## Entry Conditions Inherited From Previous Phase

- The fixed-policy validation lane is closed as passed for the serious
  `N=1024,T=20` row.
- The fixed-policy stress lane is closed as passed but explicitly not
  default-ready.
- The less-intrusive balanced-scaling repair lane is closed as failed or
  restricted-policy evidence.
- The owner requested continuation with the suggested next step.

## Required Artifacts

- Master program:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-master-program-2026-06-23.md`
- Visible runbook:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-gated-execution-runbook-2026-06-23.md`
- Claude review ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-claude-review-ledger-2026-06-23.md`
- Execution ledger:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-visible-execution-ledger-2026-06-23.md`
- P00 result:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p00-governance-result-2026-06-23.md`
- Refreshed P01 subplan:
  `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-actual-sir-nystrom-fixed-policy-promotion-stress-p01-replicated-high-n-subplan-2026-06-23.md`

## Required Checks, Tests, And Reviews

- Local path check for required program, runbook, ledger, and phase subplan
  files.
- Local consistency check that the runbook contains the required role contract,
  evidence contract, skeptical audit, phase index, stop conditions, and
  no-detached-execution rule.
- Claude Opus max-effort read-only review of bounded excerpts and path list.
- If Claude finds a fixable material issue, patch the same plan artifacts and
  rerun focused checks/review, stopping after five rounds for the same blocker.
- Write P00 result.
- Refresh/review P01 subplan for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the promotion-stress lane sufficiently bounded and artifact-complete to launch P01? |
| Baseline/comparator | Prior closed fixed-policy validation/stress artifacts are prerequisites; no numerical comparison is performed in P00. |
| Primary pass criterion | Required files exist; local consistency checks pass; Claude read-only review returns `VERDICT: AGREE` or all material issues are repaired and then agreed; P00 result and P01 subplan exist. |
| Veto diagnostics | Missing required artifact, missing evidence contract, missing stop conditions, missing no-detached rule, unsupported default/HMC/posterior claim, Claude non-response after small probe confirms prompt issue and redesigned prompt still fails, or Claude/Codex non-convergence after five rounds. |
| Explanatory diagnostics | Dirty worktree size, prior lane artifact index, review comments. |
| Not concluded | No algorithm validity, no default readiness, no HMC readiness, no numerical pass/fail evidence. |
| Artifact | P00 result and Claude review ledger. |

## Forbidden Claims/Actions

- Do not run benchmark rows before P00 converges.
- Do not claim default readiness.
- Do not let Claude execute, edit, or authorize phase crossing.
- Do not send whole large files to Claude if bounded excerpts suffice.
- Do not launch detached supervisors.

## Exact Next-Phase Handoff Conditions

Proceed to P01 only if:

- P00 local checks pass;
- Claude read-only review converges with `VERDICT: AGREE`;
- P00 result exists and records the review trail;
- P01 subplan exists and is internally reviewed;
- no human-required stop condition fired.

## Stop Conditions

- Required files are missing and cannot be repaired without crossing
  boundaries.
- Claude review finds a material issue that does not converge after five
  rounds.
- Continuing would require a default-policy decision, tuning change, package
  installation, network fetch beyond Claude review, destructive action, or
  unrelated worktree modification.

## Skeptical Plan Audit

P00 specifically checks for wrong baselines, proxy metrics being used as
promotion criteria, missing stop conditions, unfair comparison from changing
fixed policy, hidden assumptions about full-history behavior, stale context,
GPU environment mismatch, and artifact mismatch.

Audit status: `READY_FOR_LOCAL_AND_CLAUDE_REVIEW`.
