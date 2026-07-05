# P90 Phase 3 Subplan: Value Bridge Execution And Correctness Candidate

Date: 2026-06-28

Status: `PENDING_PHASE2_REVIEW_READY_FOR_PHASE3_REVIEW`

## Phase Objective

Execute the reviewed value bridge on deterministic same-scalar cases and decide
whether `D18_CORRECTNESS_CANDIDATE` may be nominated without overclaiming
production readiness.

## Entry Conditions Inherited From Previous Phase

- Phase 2 implementation artifact reviewed pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-implementation-review-artifact-2026-06-28.md`
- Phase 2 result reviewed pass:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase2-value-bridge-implementation-result-2026-06-28.md`
- Bridge contract, implementation, deterministic cases, tolerances, and
  fail-closed tests are frozen.
- Phase 3 subplan has Claude `VERDICT: AGREE`.

## Required Artifacts

- Bridge execution output manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json`
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-result-2026-06-28.md`
- Refreshed Phase 4 derivative-carry design subplan.
  `docs/plans/bayesfilter-highdim-zhao-cui-p90-phase4-derivative-carry-design-subplan-2026-06-28.md`

## Required Checks/Tests/Reviews

Allowed runtime command after the Phase 2 implementation artifact, Phase 2
result, and this Phase 3 subplan receive Claude `VERDICT: AGREE`:

```bash
env CUDA_VISIBLE_DEVICES=-1 pytest tests/highdim/test_p90_value_bridge_execution.py::test_p90_phase3_source_scalar_matches_author_formula_replay --maxfail=1
```

Allowed document hygiene command:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p90*.md
```

The runtime command is deliberately CPU-only with GPU devices hidden before
TensorFlow import. The named test node must write the bridge execution output
manifest at:

```text
docs/plans/bayesfilter-highdim-zhao-cui-p90-phase3-value-bridge-execution-2026-06-28.json
```

GPU/CUDA is forbidden unless this subplan is amended.

Claude review is required for the Phase 3 result and Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the local Zhao-Cui SIR d18 value match the source-backed bridge for the exact same scalar and branch within pinned tolerances? |
| Baseline/comparator | Reviewed same-target author-formula replay bridge reference. |
| Primary criterion | All predeclared deterministic cases match within pinned tolerances and no branch/retained/setup veto fires. |
| Veto diagnostics | Wrong scalar, branch mismatch, retained-object mismatch, tolerance changed after result, nonfinite value, missing source reference, or proxy comparator. |
| Explanatory diagnostics | Per-case residuals, component decomposition, branch hashes. |
| Not concluded | No analytical-gradient correctness, FD validation, HMC readiness, GPU/XLA readiness, production readiness, or default-policy change. |
| Artifact | Bridge execution manifest and Phase 3 result. |

## Forbidden Claims/Actions

- Do not claim production readiness.
- Do not claim gradient correctness or FD validation.
- Do not run HMC, GPU/CUDA, packaging, CI, release, or default-policy commands.
- Do not change tolerances after seeing results.
- Do not use proxy bridges as correctness evidence.
- Do not run the full Phase 2 test file as Phase 3 evidence unless this
  subplan is reviewed again with exact nodeids. Phase 3 evidence must come
  from the named source-scalar-vs-replay comparison node.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- Phase 3 result receives Claude `VERDICT: AGREE`;
- value bridge passes or Phase 3 explicitly writes a value blocker;
- if passed, Phase 4 may design derivative carry for exactly the same scalar
  and branch.

## Stop Conditions

- Value bridge fails or produces ambiguous evidence.
- Runtime command cannot be run in trusted/reviewed context.
- Branch/setup/tolerance mismatch occurs.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed runtime/GPU/HMC/package/default-policy or
  unrelated dirty-worktree changes.

## End-Of-Phase Requirements

1. Run required local checks.
2. Write Phase 3 result / close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 4 subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
