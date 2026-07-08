# Phase 1 Subplan: SSL-LSTM Model, Parameterization, And Estimand

Date: 2026-07-04

Status: `DRAFT_NEXT_PHASE`

## Phase Objective

Inspect the SSL-LSTM paper and current local code surfaces, then produce a
source-grounded model and estimand specification for a Gaussian additive
state-space LSTM target that HMC can sample over parameters.

## Entry Conditions Inherited From Previous Phase

- Phase 0 passed and recorded its local checks and Claude review.
- Master program and visible runbook are active.
- No implementation may begin until this phase identifies the model equations,
  parameter vector, transforms, priors, shapes, data fixtures, and invariant
  success metrics.

## Required Artifacts

- `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-result-2026-07-04.md`
- A source ledger section citing the inspected SSL-LSTM paper sections/equations.
- A local-code inventory section listing relevant existing BayesFilter modules.
- A parameterization table with constrained and unconstrained parameters.
- A model fixture specification for Gaussian additive process and observation
  noise.
- A metric specification for heldout predictive log score, decoded latent RMSE
  after alignment, trajectory alignment error, posterior predictive calibration,
  and HMC diagnostics.
- Refreshed Phase 2 subplan.

## Required Checks, Tests, And Reviews

- Verify the paper source was inspected beyond abstract/introduction.
- Verify the result separates original paper inference from this program's HMC
  estimand.
- Verify parameter matching is not used as a promotion criterion.
- Local `rg` inventory for relevant SSL, HMC, posterior adapter, SGQF, UKF,
  Zhao-Cui, and LEDH paths.
- Claude read-only review if the model/estimand spec changes the master
  program scope.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact Gaussian additive SSL-LSTM target and filter-induced posterior will later adapters evaluate? |
| Baseline/comparator | The user-supplied SSL-LSTM paper as source context plus current BayesFilter adapter contracts. |
| Primary pass criterion | A complete model/parameter/metric spec exists and is internally consistent with HMC-over-parameters. |
| Veto diagnostics | Missing paper anchors, confusion between original Particle MCMC inference and our HMC target, unbounded parameter transforms, or parameter matching as primary success. |
| Explanatory diagnostics | Local code inventory and notes on parts needing new implementation. |
| Not concluded | No code correctness, no paper reproduction, no exact likelihood claim, no estimator success. |
| Result artifact | `docs/plans/bayesfilter-ssl-lstm-filter-hmc-phase1-ssl-model-estimand-result-2026-07-04.md` |

## Forbidden Claims And Actions

- Do not implement adapters before the model spec is closed.
- Do not claim the paper used HMC for SSL-LSTM if it used Particle MCMC.
- Do not treat parameter-by-parameter recovery as primary evidence.
- Do not infer unsupported equations from memory; cite inspected source anchors.
- Do not change default backend or public API.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only when:

- the SSL-LSTM model, priors, transforms, shapes, and fixtures are specified;
- the filter-induced posterior target is declared;
- invariant metrics and non-identifiability handling are specified;
- local code surfaces for adapter integration are listed;
- Phase 2 subplan is refreshed and passes consistency review.

## Stop Conditions

- The paper source or required technical sections cannot be inspected.
- The Gaussian additive target cannot be specified without a project-direction
  decision from the user.
- A required transform or prior choice is scientifically ambiguous and no
  conservative local default exists.
- The result would need to claim paper reproduction without evidence.

## End-Of-Phase Protocol

1. Run required local source/code inventory checks.
2. Write the Phase 1 result/close record.
3. Draft or refresh the Phase 2 subplan.
4. Review Phase 2 for consistency, correctness, feasibility, artifact coverage,
   and boundary safety.
