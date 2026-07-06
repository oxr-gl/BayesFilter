# BayesFilter LGSSM-First NeuTra/HMC Phase 8 Subplan

Date: 2026-07-06

## Phase Objective

Show that the same target contract can use multiple filter backends without
changing HMC/transport plumbing.

## Entry Conditions Inherited From Previous Phase

- Phase 7 simple nonlinear target adapter passed.
- At least one alternative filter backend is available or scoped.

## Required Artifacts

- Multi-filter comparison/gating result.
- Phase 8 result:
  `docs/plans/bayesfilter-lgssm-first-neutra-hmc-phase8-multifilter-result-2026-07-06.md`
- Refreshed Phase 9 subplan.

## Required Checks/Tests/Reviews

- Target signatures change when filter semantics change.
- HMC/transport adapter interface remains stable.
- Filter diagnostics stay separate from posterior claims.
- Review before DSGE/c603 stress phase.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter keep one target-adapter interface while swapping filter backends under explicit signatures? |
| Baseline/comparator | Phase 7 nonlinear target and available alternative filters. |
| Primary criterion | Multiple filter programs produce distinct target signatures and compatible adapter manifests. |
| Veto diagnostics | Filter signature collision, hidden approximation change, posterior claims from filter diagnostics, or method ranking without uncertainty. |
| Explanatory diagnostics | Value/score differences, runtime, filter metadata. |
| Not concluded | One filter is superior, production readiness, DSGE readiness. |
| Artifact | Phase 8 result and tests/logs. |

## Forbidden Claims/Actions

- Do not rank filters without statistical evidence.
- Do not claim approximation correctness from interface compatibility alone.
- Do not use DSGE/c603 yet except to prepare Phase 9 stress boundary.

## Exact Next-Phase Handoff Conditions

Phase 9 may begin only if the generic interface has passed LGSSM and simple
nonlinear non-DSGE gates.

## Stop Conditions

Stop if filter identities cannot be made stable, if swapping filters breaks
adapter semantics, or if review does not converge after five rounds.

## Phase Close Duties

At close:

1. run required local checks;
2. write Phase 8 result;
3. draft or refresh Phase 9 subplan;
4. review Phase 9 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
