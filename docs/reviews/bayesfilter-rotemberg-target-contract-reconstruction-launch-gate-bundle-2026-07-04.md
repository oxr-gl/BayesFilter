# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `bayesfilter-rotemberg-target-contract-reconstruction-launch-gate`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, or approve
boundary crossings.

## Objective

Decide whether the Rotemberg target-contract reconstruction program is
consistent, feasible, and boundary-safe to launch, and whether the Phase 0 and
Phase 1 subplans contain the required controls for a gated visible execution.

## Artifacts To Inspect

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md`
- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-visible-gated-execution-runbook-2026-07-04.md`
- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase0-governance-subplan-2026-07-04.md`
- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-phase1-metadata-source-inventory-subplan-2026-07-04.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can this program launch safely with Codex as supervisor/executor, Claude as read-only reviewer, explicit repair loop, and no unsupported migration/HMC claims? |
| Baseline/comparator | User-requested gated recovery design, visible-gated execution runbook template, and the dense-IAF stop handoff that motivated this recovery program. |
| Primary criterion | The master program, runbook, Phase 0 subplan, and Phase 1 subplan all have coherent phase boundaries, required artifacts, required checks, evidence contracts, forbidden claims/actions, stop conditions, and next-phase handoff conditions. |
| Veto diagnostics | Missing required heading, hidden authority transfer, overclaim of real-artifact reuse or HMC/posterior validity, missing stop condition, inconsistent phase gating, or any clause that would let the plan continue without reviewed evidence. |
| Explanatory diagnostics | Review-round count, artifact names, and whether the launch gate is structured for visible execution. |
| Not concluded | No real-artifact reuse, no payload export, no HMC convergence, no posterior correctness, no sampler superiority, and no default-policy change. |

## Review Questions

1. Is the launch gate consistent and boundary-safe?
2. Do the Phase 0 and Phase 1 subplans contain the required phase fields and stop conditions?
3. Are there unsupported claims, hidden authority transfers, or vague boundary clauses?
4. Is the next-phase handoff structure safe enough to begin Phase 0 execution?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
