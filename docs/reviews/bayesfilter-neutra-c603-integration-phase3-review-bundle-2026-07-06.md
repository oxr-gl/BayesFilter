# Claude Read-Only Review Bundle

Date: 2026-07-06
Review name: `bayesfilter-neutra-c603-integration-phase3`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the refreshed Phase 3 fixed-transport mechanics subplan. The question is
whether the subplan is internally consistent, feasible, artifact-complete, and
boundary-safe before Codex implements the c603 mechanics-only fixture test.

## Artifacts To Inspect

Primary exact path:

- `docs/plans/bayesfilter-neutra-c603-integration-phase3-fixed-transport-mechanics-subplan-2026-07-06.md`

Supporting exact paths if needed:

- `docs/plans/bayesfilter-neutra-c603-integration-phase2-c603-fixture-tests-result-2026-07-06.md`
- `docs/plans/bayesfilter-neutra-c603-integration-phase4-generic-interface-subplan-2026-07-06.md`
- `tests/test_fixed_transport_hmc_binding.py`

Do not inspect the whole repository.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the refreshed Phase 3 mechanics-only subplan safe and sufficient to enter implementation? |
| Baseline/comparator | Existing toy fixed-transport mechanics tests and the completed Phase 2 c603 local-fixture result. |
| Primary criterion | The subplan preserves mechanics-only scope, exact CPU-only checks, clear c603 local-artifact provenance, explicit fixture-base-adapter boundaries, and a clean Phase 4 handoff. |
| Veto diagnostics | Hidden HMC sampling, hidden GPU dependency, silent promotion of fixture authority into Rotemberg/HMC readiness, missing artifact provenance, or missing stop conditions. |
| Explanatory diagnostics | Suggestions for narrower fixture wording or cleaner handoff phrasing that do not block safety. |
| Not concluded | No mechanics correctness yet, no Rotemberg target-adapter correctness, no HMC readiness, no production readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in the refreshed Phase 3 subplan?
2. Does it clearly preserve the mechanics-only boundary and forbid silent drift into real HMC or real Rotemberg target authority?
3. Are the required checks exact and sufficient for the phase question?
4. Are there unsupported claims or missing stop conditions?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
