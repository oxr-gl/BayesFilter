# P91 Phase 2 Subplan: Batched Value/Score API

Date: 2026-06-29

Status: `PHASE1_REVIEW_PENDING_BATCHED_API_READY`

## Phase Objective

Implement or harden single and batched Zhao-Cui value/score APIs and test that
batched outputs match looped single-dataset outputs with stable shapes, dtypes,
branch identity, setup-identity metadata, and finite values/scores.

## Entry Conditions Inherited From Previous Phase

- Phase 1 score contract reviewed pass.
- Score contract:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-score-contract-2026-06-29.md`
- Single and batched API semantics are pinned, including the requirement to
  expose setup identity through manifest, diagnostics payload, or return
  metadata.
- This Phase 2 subplan receives Claude `VERDICT: AGREE`.

## Required Artifacts

- Phase 2 implementation review artifact:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-implementation-artifact-2026-06-29.md`
- Phase 2 result:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase2-batched-api-result-2026-06-29.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-highdim-zhao-cui-p91-phase3-fd-consistency-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Initial allowed checks are document/source inventory only:

```bash
rg -n "batched|batch|score|gradient|SourceRoute|value" bayesfilter/highdim tests/highdim
git diff --check -- docs/plans/bayesfilter-highdim-zhao-cui-p91*.md
```

Before any Phase 2 code edit or pytest command, write the Phase 2
implementation artifact as a design/test manifest and obtain Claude
`VERDICT: AGREE` on that artifact. CPU-only TensorFlow tests must set
`CUDA_VISIBLE_DEVICES=-1` before framework import. Claude review is required
for the implementation artifact, Phase 2 result, and Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do single and batched Zhao-Cui value/score APIs exist and agree on deterministic SIR d18 fixtures? |
| Baseline/comparator | Looped single-dataset API under reviewed Phase 1 score contract. |
| Primary criterion | Batched value/score equals looped single value/score within pinned tolerance, with stable shape/dtype, branch identity, and setup-identity metadata. |
| Veto diagnostics | Batch/single mismatch, branch/setup identity drift, missing identity metadata, ambiguous or mixed batched identity without per-item metadata and fail-closed behavior, NaN/Inf, dtype drift, hidden retracing as correctness claim, or performance proxy treated as validity. |
| Explanatory diagnostics | Shape/dtype reports, batch-size smoke, local parity tests. |
| Not concluded | No FD pass, score identity pass, GPU/XLA readiness, HMC readiness, benchmark result, or production readiness. |
| Artifact | Implementation artifact, tests/manifests, Phase 2 result, refreshed Phase 3 subplan. |

## Forbidden Claims/Actions

- Do not claim batched speed proves scientific validity.
- Do not run GPU/XLA/HMC/performance benchmarks.
- Do not change defaults or package/release/CI settings.
- Do not revive ALS.
- Do not hide setup/basis/rank/sample/seed identity in local variables only.
- Do not allow mixed batched setup identity unless per-item metadata is
  returned and ambiguous metadata fails closed.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- Phase 2 result receives Claude `VERDICT: AGREE`;
- Phase 3 subplan receives Claude `VERDICT: AGREE`;
- deterministic single/batched parity evidence is recorded, or Phase 2 closes
  with an explicit API blocker.
- setup identity is recorded in manifest, diagnostics payload, or return
  metadata.

## Stop Conditions

- Batched and single semantics cannot be reconciled.
- Score API cannot be exposed without changing the Phase 1 contract.
- Local tests/checks fail and cannot be repaired in Phase 2 scope.
- Claude review does not converge after five rounds.
- Continuing would require GPU/HMC/package/default actions.

## End-Of-Phase Requirements

1. Run required local checks/tests authorized by reviewed Phase 2 artifacts.
2. Write Phase 2 result / close record.
3. Draft or refresh Phase 3 subplan.
4. Review Phase 2 result and Phase 3 subplan.
