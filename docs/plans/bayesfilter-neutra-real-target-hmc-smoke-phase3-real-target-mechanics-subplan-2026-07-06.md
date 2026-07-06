# BayesFilter NeuTra Real Target HMC Smoke Phase 3 Subplan

Date: 2026-07-06

## Phase Objective

Close the Phase 2 blocker without running mechanics. Phase 2 did not establish
a reviewed BayesFilter-owned real c603 target adapter, so Phase 3 is refreshed
from a mechanics phase into blocker-handoff handling.

## Entry Conditions Inherited From Previous Phase

- Phase 2 result exists with status
  `BLOCKED_MISSING_PORTABLE_REAL_TARGET_AUTHORITY`.
- The c603 frozen transport import remains valid as transport evidence only.
- No real-target mechanics, HMC, GPU, training, package installation, or git
  commit/push has been run.

## Required Artifacts

- Phase 3 blocker-handoff result:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase3-real-target-mechanics-result-2026-07-06.md`.
- Refreshed Phase 4 subplan that preserves the stop condition, or a terminal
  closeout handoff if the program stops here.
- Updated visible stop handoff.

## Required Checks/Tests/Reviews

- Local text checks that Phase 2 blocker status and Phase 3 non-execution
  status are recorded.
- Review of blocker handoff for consistency, correctness, feasibility,
  artifact coverage, and boundary safety.
- No mechanics pytest is required because mechanics is forbidden unless Phase 2
  real-target adapter authority passes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the program preserve the Phase 2 real-target authority blocker without accidentally running or claiming mechanics? |
| Baseline/comparator | Phase 2 blocker result and the original Phase 3 mechanics plan. |
| Primary criterion | A blocker-handoff result records that mechanics did not run, names the next valid repair boundary, and preserves all nonclaims. |
| Veto diagnostics | Any mechanics/HMC/GPU/training launch, synthetic target promotion, live `dsge_hmc` runtime promotion, or unsupported HMC/posterior/product claim. |
| Explanatory diagnostics | Artifact paths, local text-check status, review status. |
| Not concluded | Real target adapter correctness, mechanics validity, HMC readiness, posterior correctness, production readiness. |
| Artifact | Phase 3 blocker-handoff result and updated visible stop handoff. |

## Forbidden Claims/Actions

- Do not run mechanics.
- Do not run HMC sampling.
- Do not call synthetic mechanics real c603 target evidence.
- Do not import live `dsge_hmc` modules as BayesFilter authority.
- Do not use GPU, training, package installation, or git commit/push.

## Exact Next-Phase Handoff Conditions

Phase 4 tiny HMC smoke must remain blocked unless a separate reviewed repair
program first establishes a BayesFilter-owned real c603 target adapter and then
passes real-target mechanics. If Phase 3 closes the blocker handoff, Phase 5
closeout may summarize the stopped program.

## Stop Conditions

Stop if any action would run mechanics, HMC, GPU, training, package
installation, or live external runtime authority before the real target adapter
boundary is repaired and reviewed. Stop if review does not converge after five
rounds for the same material blocker.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 3 result;
3. refresh Phase 4 or Phase 5 handoff as stopped/blocked;
4. review the handoff for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
