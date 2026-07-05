# P85 Phase 3 Subplan: Implementation And Test Matrix Review

Date: 2026-06-23

Status: `DRAFT_BLOCKED_PENDING_PHASE2`

## Phase Objective

Freeze the exact implementation surface, file list, tests, and command contract
before changing BayesFilter code.

## Entry Conditions Inherited From Previous Phase

- Phase 2 has produced a reviewed setup API and XLA/static contract.
- No implementation has yet been performed.
- P84 Phase 2 fitting remains blocked.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p85-phase3-implementation-test-matrix-result-2026-06-23.md`
- Exact list of code files allowed for Phase 4.
- Exact list of tests to add or modify.
- Exact CPU-hidden test commands for Phase 4.
- Refreshed Phase 4 subplan.

## Required Checks / Tests / Reviews

- Inspect current dirty worktree paths touching planned files before editing.
- Scan existing tests for local patterns:

```bash
rg -n "LegendreBasis1D|ProductBasis|basis_dim_tuple|manifest\\[|nonclaims|CUDA_VISIBLE_DEVICES" tests/highdim bayesfilter/highdim -S
```

- Run P85 documentation hygiene checks.
- Claude read-only review of the Phase 3 result before Phase 4 implementation.

## Evidence Contract

| Field | Contract |
|---|---|
| Question | Are the planned code edits and tests narrow enough to implement the Phase 2 design without touching unrelated work? |
| Baseline/comparator | Phase 2 design and current local basis/source-route tests. |
| Primary criterion | Phase 3 freezes exact files, expected behaviors, tests, and CPU-hidden commands for Phase 4. |
| Veto diagnostics | Unbounded file list; missing regression tests; hidden default-policy change; no dirty-worktree assessment; no exact commands. |
| Explanatory diagnostics | Diff-risk assessment, API export list, expected manifest payload examples. |
| Not concluded | No implementation correctness, no source repair, no fit quality. |
| Artifact | Phase 3 result and refreshed Phase 4 subplan. |

## Forbidden Claims / Actions

- Do not edit code in Phase 3.
- Do not approve Phase 4 without exact command and artifact paths.
- Do not run TensorFlow, fitting, GPU, HMC, LEDH, d=50/d=100, or long commands.
- Do not classify `extension_or_invention` as source-faithful.

## Exact Next-Phase Handoff Conditions

Phase 4 may begin only if:

- Phase 3 is reviewed and local checks pass;
- exact files/tests are frozen;
- dirty-worktree interactions are recorded;
- CPU-hidden commands are specified;
- no human approval boundary remains unresolved for the code edits/tests.

## Stop Conditions

Stop if:

- planned implementation would require touching unrelated dirty files;
- exact tests cannot be stated;
- Claude review does not converge after five rounds;
- human approval is required and absent.

## End-Of-Phase Protocol

At the end of this subplan:

1. run the required local checks;
2. write the Phase 3 result / close record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
