# P57-M1 Subplan: Author Model Callback Parity

metadata_date: 2026-06-11
status: PLAN_REVIEW_CONVERGED

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do BayesFilter spatial SIR callbacks match the author spatial SIR target before paper-scale source-route implementation is judged? |
| Baseline/comparator | Author `ssmodel.m`, SIR `mainscript.m`, SIR model-specific source files, and current BayesFilter spatial SIR callbacks. |
| Primary pass criterion | A spatial SIR parity ledger records state ordering, parameters, transition density, transition sampler/push, prior, likelihood, observation indexing, covariance/noise choices, and fixed-HMC adaptations. |
| Veto diagnostics | Spatial SIR route implementation begins before callback parity is documented; state ordering differs without an approved adaptation; tests compare different targets; an `extension_or_invention` mismatch is allowed to proceed without explicit approval or blocker. |
| Not concluded | No transport correctness, no rank correctness, no HMC readiness. |

## Tasks

1. Inspect author SIR source settings and source model callbacks.
2. Inspect BayesFilter model definitions for the spatial SIR lane used by
   source-route tests.
3. Build a discrepancy table: `source_faithful`, `fixed_hmc_adaptation`, or
   `extension_or_invention`.
4. Add focused parity tests for formulas that are already implemented.
5. Treat any spatial SIR `extension_or_invention` mismatch as a blocker to
   source-faithful spatial SIR tests until resolved or explicitly approved.
6. If SV or predator-prey is inspected, label it diagnostic-only for P57. It
   cannot block or certify the P57 paper-scale spatial SIR claim unless a later
   reviewed phase explicitly re-scopes it.
7. Write result artifact with pass/block token.

## Required Checks

- `rg -n "class SpatialSIR|spatial_sir|predator|volatility|transition|likelihood" bayesfilter/highdim tests/highdim`
- source-code line references from `third_party/audit/zhao_cui_tensor_ssm_p10/source`.
- Claude review must verify that parity is not inferred from similar names.
