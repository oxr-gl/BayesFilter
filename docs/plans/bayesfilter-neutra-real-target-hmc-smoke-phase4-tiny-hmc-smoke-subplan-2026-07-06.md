# BayesFilter NeuTra Real Target HMC Smoke Phase 4 Subplan

Date: 2026-07-06

## Phase Objective

Do not enter HMC smoke. Phase 2 blocked the real target adapter boundary and
Phase 3 recorded that real-target mechanics did not run, so Phase 4 is
refreshed into a no-entry blocker record.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result exists with status
  `BLOCKER_HANDOFF_RECORDED_NO_MECHANICS_RUN`.
- Phase 2 remains blocked by missing portable real-target authority.
- No real-target mechanics pass exists.

## Required Artifacts

- Phase 4 blocked/no-entry result:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-result-2026-07-06.md`.
- Refreshed Phase 5 closeout subplan.

## Required Checks/Tests/Reviews

- Local text checks that Phase 4 did not run HMC and that Phase 5 closeout
  records the Phase 2 blocker.
- Review of Phase 5 closeout subplan before final close.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does Phase 4 correctly refuse HMC smoke because the real-target mechanics prerequisite is missing? |
| Baseline/comparator | Phase 2 blocker and Phase 3 no-mechanics handoff. |
| Primary criterion | Phase 4 result records no HMC run and preserves the exact blocking prerequisite. |
| Veto diagnostics | Any HMC/sampler launch, GPU use, retuning, training, or claim that the smoke passed. |
| Explanatory diagnostics | Phase 2/3 artifact paths and review status. |
| Not concluded | No convergence, no posterior correctness, no sampler ranking, no default readiness. |
| Artifact | Phase 4 blocked/no-entry result and refreshed Phase 5 closeout subplan. |

## Forbidden Claims/Actions

- Do not run HMC.
- Do not run long HMC or training.
- Do not claim HMC readiness from this smoke.
- Do not use GPU.
- Do not treat Phase 4 as passed smoke evidence.

## Exact Next-Phase Handoff Conditions

Phase 5 may begin after the no-entry Phase 4 result is recorded and the Phase 5
closeout subplan is refreshed.

## Stop Conditions

Stop immediately if any action would run HMC, GPU/CUDA, training, package
installation, live `dsge_hmc` runtime target authority, or unsupported
scientific/product claims.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 4 result;
3. draft or refresh Phase 5 subplan;
4. review Phase 5 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
