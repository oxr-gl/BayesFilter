# BayesFilter NeuTra Real Target HMC Smoke Launch Review Bundle

Date: 2026-07-06
Review name: `bayesfilter-neutra-real-target-hmc-smoke-launch`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, or approve
boundary crossings.

## Objective

Review the launch plan for the next BayesFilter NeuTra program. The question is
whether the program is scoped and bounded enough to enter Phase 1 read-only
target-authority inventory.

## Primary Exact Path

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-master-program-2026-07-06.md`

## Supporting Exact Paths If Needed

- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase0-launch-contract-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-c603-integration-visible-stop-handoff-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the new real-target NeuTra/HMC-smoke program scoped, bounded, and safe to enter Phase 1 inventory? |
| Baseline/comparator | Closed c603 import/mechanics fixture program and existing BayesFilter target-builder/fixed-transport surfaces. |
| Primary criterion | Planning artifacts preserve nonclaims, human approval boundaries, stop conditions, and Phase 1 read-only inventory before implementation. |
| Veto diagnostics | Hidden HMC/training/GPU launch, unsupported real-target authority, missing repair loop, missing stop conditions, or treating fixture mechanics as real target readiness. |
| Explanatory diagnostics | Suggestions for narrower wording or phase ordering. |
| Not concluded | No implementation correctness, mechanics pass, HMC readiness, posterior correctness, or production readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in the launch plan?
2. Does Phase 1 correctly inventory real target/value-score authority before
   implementation?
3. Are approval boundaries, nonclaims, and stop conditions explicit enough?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
