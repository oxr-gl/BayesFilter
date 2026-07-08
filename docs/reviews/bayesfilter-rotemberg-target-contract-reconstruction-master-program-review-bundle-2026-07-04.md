# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `bayesfilter-rotemberg-target-contract-reconstruction-master-program-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, or approve
boundary crossings.

## Objective

Decide whether the master program itself is internally consistent, boundary-safe,
and launch-safe as the top-level artifact for the Rotemberg target-contract
reconstruction program.

## Exact Artifact To Inspect

- `docs/plans/bayesfilter-rotemberg-target-contract-reconstruction-master-program-2026-07-04.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the master program launch-safe as the top-level artifact, with coherent phases, subplan requirements, evidence contracts, stop conditions, and no hidden authority transfer? |
| Baseline/comparator | The visible-gated execution runbook template and the dense-IAF stop handoff that motivated this recovery program. |
| Primary criterion | The master program contains coherent phase boundaries, required artifacts, required checks, evidence contracts, forbidden claims/actions, stop conditions, and next-phase handoff conditions. |
| Veto diagnostics | Missing required heading, hidden authority transfer, overclaim of real-artifact reuse or HMC/posterior validity, missing stop condition, inconsistent phase gating, or any clause that would let the plan continue without reviewed evidence. |
| Explanatory diagnostics | Review-round count and whether the artifact is structured for visible execution. |
| Not concluded | No real-artifact reuse, no payload export, no HMC convergence, no posterior correctness, no sampler superiority, and no default-policy change. |

## Review Questions

1. Is this master program itself consistent and boundary-safe?
2. Does it avoid unsupported claims or hidden authority transfer?
3. Are the phase boundaries, required artifacts, and stop conditions coherent enough to launch Phase 0?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
