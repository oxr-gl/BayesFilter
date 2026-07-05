# P90 Phase 2 Subplan: Value Bridge Implementation

Date: 2026-06-28

Status: `REVIEWED_READY_FOR_PHASE2_VALUE_BRIDGE_IMPLEMENTATION`

## Phase Objective

Implement the reviewed same-target value bridge contract and fail-closed tests
without executing production-scale validation.

## Entry Conditions Inherited From Previous Phase

- Phase 1 bridge contract is reviewed pass.
- Phase 1 result and Phase 2 subplan have Claude `VERDICT: AGREE`.
- Exact target, branch, retained-object, setup-static, parameterization, and
  tolerance bindings are frozen in the bridge contract.

## Required Artifacts

- Code changes implementing the bridge helper or test-only reference path
  required by:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-value-bridge-contract-2026-06-28.md`
- Focused tests for same target, branch identity, retained-object identity,
  setup-static fields, parameterization, tolerance version, and negative
  controls named by the Phase 1 contract.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-result-2026-06-28.md`
- Refreshed Phase 3 execution subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed implementation/check commands after Phase 1 review:

```bash
pytest tests/highdim/test_p90_value_bridge_contract.py --maxfail=1
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

If implementation uses a different test filename, Phase 2 must replace the
pytest command with exact focused test path(s) or nodeid(s) before execution
and record the replacement in the result. Broad selectors such as
`-k source_route` are forbidden because they may match unrelated tests.
TensorFlow/Python runtime remains CPU/GPU-neutral unless the implementation
test explicitly initializes GPU, in which case it requires escalated/trusted
execution under AGENTS.md.

Claude read-only review is required for implementation summary/diff artifact,
Phase 2 result, and Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the implementation faithfully instantiate the reviewed same-target value bridge contract? |
| Baseline/comparator | Reviewed Phase 1 bridge contract. |
| Primary criterion | Implementation provides the exact bridge surfaces and fail-closed tests required by the contract, with no uncontrolled target/branch/setup drift. |
| Veto diagnostics | Missing binding, wrong scalar, missing fail-closed tests, proxy comparator, unreviewed runtime, or source-anchor mismatch. |
| Explanatory diagnostics | Focused unit tests and code review. |
| Not concluded | No value correctness until Phase 3 execution passes. |
| Artifact | Phase 2 result and implementation review artifact. |

## Forbidden Claims/Actions

- Do not run Phase 3 bridge execution unless Phase 2 passes.
- Do not claim value correctness.
- Do not run FD, HMC, GPU/CUDA, production benchmark, packaging, CI, release,
  or default-policy commands.
- Do not alter the target manifest unless a reviewed manifest amendment exists.
- Do not revive ALS training.
- Do not use NumPy in differentiable or production algorithmic bridge paths.
- Do not claim runtime, performance, memory, cost, production, or efficiency
  conclusions from Phase 2. Any runtime observations from focused tests are
  explanatory only and cannot promote the bridge.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- implementation checks pass;
- Phase 2 result receives Claude `VERDICT: AGREE`;
- Phase 3 execution subplan receives Claude `VERDICT: AGREE`;
- all bridge contract fields remain bound and unchanged.

## Stop Conditions

- Implementation cannot match the reviewed bridge contract.
- Required tests cannot be written or fail.
- Local checks fail and cannot be repaired within scope.
- Claude review does not converge after five rounds.
- Runtime/GPU/HMC/package/default-policy/destructive/unrelated-dirty-work
  boundary would be crossed without exact reviewed authorization.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 2 result / close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 3 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
