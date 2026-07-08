# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `bayesfilter-neutra-c603-integration-launch`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the launch plan for BayesFilter NeuTra c603 engineering integration.
The question is whether the master program and Phase 0/1 subplans are
internally consistent, feasible, bounded, and safe to enter Phase 1.

## Artifacts To Inspect

Primary exact path:

- `docs/plans/bayesfilter-neutra-c603-integration-master-program-2026-07-06.md`

Supporting exact paths if needed:

- `docs/plans/bayesfilter-neutra-c603-integration-phase0-launch-contract-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-c603-integration-phase1-legacy-adapter-subplan-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-c603-integration-visible-gated-execution-runbook-2026-07-06.md`

Do not inspect the whole repository.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the visible c603 integration launch plan safe and sufficient to enter Phase 1 implementation? |
| Baseline/comparator | Manual c603 import validation and existing BayesFilter dense-IAF/fixed-transport surfaces. |
| Primary criterion | Plan separates import/mechanics evidence from scientific/HMC claims, names stop conditions, and gives exact Phase 1 handoff conditions. |
| Veto diagnostics | Missing stop condition, hidden GPU/training/long-HMC launch, unsupported posterior/HMC/production claim, ambiguous review authority, or impossible artifact/check requirement. |
| Explanatory diagnostics | Suggestions for clearer wording or narrower checks that do not block safety. |
| Not concluded | No code correctness, no adapter acceptance, no mechanics success, no HMC readiness. |

## Review Questions

1. Is there a material correctness or boundary issue?
2. Is the evidence contract internally consistent?
3. Are required artifacts and checks sufficient for Phase 0 and Phase 1?
4. Are there unsupported claims or hidden authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
