# BayesFilter NeuTra Real Target HMC Smoke Phase 1 Subplan

Date: 2026-07-06

## Phase Objective

Inventory whether BayesFilter has enough real c603 target/value-score authority
to replace the synthetic quadratic base adapter used by the c603 mechanics
fixture.

## Entry Conditions Inherited From Previous Phase

- Phase 0 launch gate passed or passed with explicitly weaker bounded fallback
  review.
- No code implementation authority has been inferred from c603 fixture
  mechanics.

## Required Artifacts

- Inventory result:
  `docs/plans/bayesfilter-neutra-real-target-hmc-smoke-phase1-target-authority-inventory-result-2026-07-06.md`.
- Optional structured inventory JSON if useful.
- Refreshed Phase 2 subplan.

## Required Checks/Tests/Reviews

- Read-only inspection of relevant BayesFilter files and c603 result notes.
- Local checks only: `test -f` / `rg` / optional JSON validation.
- Bounded Claude review of the Phase 1 result or refreshed Phase 2 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is there a reviewed real c603 target/value-score authority in BayesFilter that can support Phase 2 adapter work? |
| Baseline/comparator | Existing `GenericSSMPosteriorAdapter`, Rotemberg reconstruction results, c603 import/mechanics fixture results, and local code inventory. |
| Primary criterion | Classify the next boundary as `bridgeable_real_target_adapter`, `design_only`, or `blocked_missing_real_target_authority` with exact source paths. |
| Veto diagnostics | Treating historical dsge_hmc code as live BayesFilter authority, inventing prior/filter/data fields, or promoting synthetic fixture mechanics. |
| Explanatory diagnostics | Candidate files, missing methods, existing contract signatures, target-builder APIs. |
| Not concluded | No adapter correctness, no HMC readiness, no posterior correctness. |
| Artifact | Phase 1 inventory result. |

## Forbidden Claims/Actions

- Do not import or execute live `dsge_hmc` modules.
- Do not write adapter code before the inventory classifies the authority.
- Do not run HMC, GPU, or training.

## Exact Next-Phase Handoff Conditions

Phase 2 may begin only if Phase 1 names a bridgeable implementation path or a
design-only path with exact missing real-target authority. If blocked, Phase 2
must be a blocker/closeout phase rather than implementation.

## Stop Conditions

Stop if no real target/value-score authority exists, if target fields would
need to be invented, or if review does not converge after five rounds for the
same material blocker.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 1 result;
3. draft or refresh Phase 2 subplan;
4. review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
