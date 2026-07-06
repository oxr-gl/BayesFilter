# BayesFilter NeuTra Real Target HMC Smoke Phase 4 Result

Date: 2026-07-06

## Status

`BLOCKED_NO_ENTRY_HMC_SMOKE_NOT_RUN`

## Phase Objective

Do not enter HMC smoke. Phase 2 blocked the real target adapter boundary and
Phase 3 recorded that real-target mechanics did not run, so Phase 4 is a
no-entry blocker.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does Phase 4 correctly refuse HMC smoke because the real-target mechanics prerequisite is missing? |
| Baseline/comparator | Phase 2 blocker and Phase 3 no-mechanics handoff. |
| Primary criterion | Passed as no-entry blocker: no HMC was run and the missing prerequisite is preserved. |
| Veto diagnostics | No HMC/sampler launch, GPU use, retuning, training, package installation, or smoke-pass claim occurred. |
| Explanatory diagnostics | Phase 2 review accepted the target-authority blocker; Phase 3 review accepted the no-mechanics handoff. |
| Not concluded | No convergence, posterior correctness, sampler ranking, default readiness, or HMC readiness. |
| Artifact | This Phase 4 blocked/no-entry result and refreshed Phase 5 closeout subplan. |

## Decision

Phase 4 records:

```text
hmc_smoke_not_run_blocked_by_missing_real_target_mechanics
```

No HMC smoke command was planned or executed. Running HMC would be wrong
relative to the program gates because no reviewed real c603 target adapter and
no real-target mechanics pass exist.

## Local Checks

Required local checks:

```text
test -f docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md
rg -n "BLOCKER_HANDOFF_RECORDED_NO_MECHANICS_RUN" docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md
rg -n "Do not enter HMC smoke|Do not run HMC" docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase4-tiny-hmc-smoke-subplan-2026-07-06.md
git diff --check -- Phase 4/Phase 5/ledger/handoff artifacts
```

Result:

```text
PHASE4_NO_ENTRY_LOCAL_CHECKS_OK
```

## Phase 5 Handoff

Phase 5 must close the visible program. It should not add experiments or
repair work. Any continuation must be a separate reviewed repair program to
establish portable c603 real target authority before mechanics or HMC.

## Nonclaims

- no HMC smoke was run;
- no real-target mechanics was run;
- no GPU, training, package installation, live external target authority, or
  git operation was run;
- no posterior correctness, HMC readiness, production readiness, scientific
  promotion, sampler ranking, or default-policy claim is made.
