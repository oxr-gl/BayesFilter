# P57-M6 Subplan: Full Sequential Fixed-HMC Source Loop

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can BayesFilter run the author sequential retained-object route with fixed-HMC replayability? |
| Baseline/comparator | Author `full_sol.solve`, paper equations (9)--(11), Algorithm 2, P56 D01/D02/D07. |
| Primary pass criterion | A loop over `t=1..T` carries retained transport objects, previous marginal density, frozen draws, fixed ranks/bases/schedules, fixed ESS stop conditions, fixed resampling, normalizer increments, and proposal corrections, with a branch-by-branch source-faithful versus fixed-HMC-adaptation ledger. |
| Veto diagnostics | One-step-only route promoted as sequential filtering; previous retained marginal omitted; stochastic branch changes inside likelihood; rank/basis/sample schedule mutates during HMC. |
| Not concluded | No preconditioned Algorithm 5 route or paper-scale SIR until M8-M9 pass. |

## Tasks

1. Translate `full_sol.solve` into fixed-HMC pseudocode with source anchors.
2. Implement or plan retained-object state carrying from M2-M5.
3. Freeze all random/reference draws and branch schedules before likelihood.
4. For each branch in initialize, push, augment, ESS enhancement, recenter,
   fit, inverse-map sampling, retained marginalization, resampling, and proposal
   correction, record whether it is `source_faithful`,
   `fixed_hmc_adaptation`, or `extension_or_invention`. Any
   `extension_or_invention` branch blocks source-faithful pass unless approved.
5. Add deterministic replay tests and scalar/two-step reference tests.
6. Write result artifact.

## Required Checks

- `rg -n "one_step|previous retained|retained_object|normalizer|ESS|resample|sequential" bayesfilter/highdim tests/highdim`
- Claude review must reject a pass without previous retained-object
  marginalization.
