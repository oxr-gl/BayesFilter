# P91 Phase 3 Subplan: FD Consistency

Date: 2026-06-29

Status: `PHASE2_LOCAL_PASS_FD_PRE_REFRESH_PENDING_REVIEW`

## Phase Objective

Validate engineering consistency between the Zhao-Cui analytical score and
finite differences of the same implemented scalar under fixed branch/setup.
FD is necessary for HMC-facing engineering but is not a truth oracle and does
not prove exact likelihood correctness.

## Entry Conditions Inherited From Previous Phase

- Phase 2 batched/single API reviewed pass, including setup identity exposed
  through diagnostics and branch manifests.
- Score contract and fixed branch/setup semantics are pinned.
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- This Phase 3 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- FD plan/manifest:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-manifest-2026-06-29.json`
- Phase 3 implementation artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-implementation-artifact-2026-06-29.md`
- Phase 3 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-result-2026-06-29.md`
- Refreshed Phase 4 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase4-score-identity-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Phase 3 must first write the FD implementation artifact with exact scalar,
score, FD commands, tolerances, step-size ladder, setup identity fixture,
artifact paths, and CPU/GPU choice. The implementation artifact is the reviewed
pre-runtime authority for whether and how the FD command may run. The JSON
manifest is the run-record/output schema emitted or filled by the authorized
FD command. The implementation artifact must receive Claude `VERDICT: AGREE`
before any FD runtime command. CPU-only FD must hide GPU before import. GPU FD
is not authorized in Phase 3 unless explicitly reviewed. Claude review is
required for the implementation artifact, Phase 3 result, and Phase 4 subplan.

Allowed pre-refresh check:

```bash
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does analytical score match finite differences of the same implemented scalar under fixed branch/setup? |
| Baseline/comparator | Same implemented scalar evaluated by FD step ladder using the reviewed single/batched API identity channel from Phase 2. |
| Primary criterion | Componentwise analytical-vs-FD agreement within reviewed tolerances and no branch/setup drift. |
| Veto diagnostics | FD treated as truth oracle, branch/setup identity drift, missing setup identity metadata, scalar mismatch, unstable step ladder, NaN/Inf, or discrepancy hidden by aggregate norm only. |
| Explanatory diagnostics | Step-size ladder, componentwise absolute/relative errors, batch spot checks. |
| Not concluded | No score identity pass, exact likelihood correctness, GPU/XLA readiness, HMC readiness, benchmark result, package/release/CI readiness, default-policy authorization/change, or production readiness. |
| Artifact | FD implementation artifact, FD manifest, Phase 3 result, refreshed Phase 4 subplan. |

## Forbidden Claims/Actions

- Do not claim FD proves the true likelihood gradient.
- Do not run score-identity, GPU/XLA, HMC, performance, package/release/CI, or
  default-policy commands.
- Do not change pass/fail tolerances after seeing results.
- Do not run FD before the FD implementation artifact is written and reviewed.

## Exact Next-Phase Handoff Conditions

Phase 4 may start only if:

- Phase 3 result receives Claude `VERDICT: AGREE`;
- Phase 4 subplan receives Claude `VERDICT: AGREE`;
- FD either passes under reviewed tolerances or Phase 4 is converted to a
  blocker-only result.

## Stop Conditions

- FD scalar cannot be bound to the same implemented score.
- FD setup identity cannot be preserved through diagnostics or branch
  manifests.
- Analytical-vs-FD discrepancy cannot be diagnosed in scope.
- Local checks fail and cannot be repaired.
- Claude review does not converge after five rounds.
- Continuing would require unreviewed runtime/GPU/HMC/default boundaries.

## End-Of-Phase Requirements

1. Run required local checks/tests authorized by reviewed Phase 3 refresh.
2. Write Phase 3 result / close record.
3. Draft or refresh Phase 4 subplan.
4. Review Phase 3 result and Phase 4 subplan.
