# Low-Rank LEDH LGSSM Exact-Kalman Gate Aggregate

- Status: `FAIL`
- Decision: `STOP_P01_HARD_ROUTE_DIAGNOSTIC_VETO`
- Hard vetoes: `['lgssm_small_exact_ref:91003:low_rank:factor_marginal_residual_threshold']`
- Stop reason: low-rank route exceeded the predeclared factor marginal residual threshold on `lgssm_small_exact_ref`, seed `91003`.
- JSON artifact: `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik Delta | Factor Residual | Iterations | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `streaming` | `PASS` | 0.118716 | 0.243295 | 1.68497 | 0 | 0 | `[]` |
| lgssm_small_exact_ref | 91001 | `low_rank` | `PASS` | 0.12217 | 0.243102 | 1.78362 | 1.49012e-08 | 23 | `[]` |
| lgssm_small_exact_ref | 91002 | `streaming` | `PASS` | 0.076188 | 0.242964 | 0.785164 | 0 | 0 | `[]` |
| lgssm_small_exact_ref | 91002 | `low_rank` | `PASS` | 0.0756881 | 0.242257 | 0.791777 | 1.49012e-08 | 19 | `[]` |
| lgssm_small_exact_ref | 91003 | `streaming` | `PASS` | 0.0662255 | 0.242857 | 0.868298 | 0 | 0 | `[]` |
| lgssm_small_exact_ref | 91003 | `low_rank` | `FAIL` | 0.0663892 | 0.242455 | 0.864454 | 0.00665334 | 120 | `['factor_marginal_residual_threshold']` |

## Not Run

- `lgssm_medium_exact_ref` seeds `[91011, 91012, 91013]` routes `['streaming', 'low_rank']`: P01 stopped after earlier hard route diagnostic veto.
- `lgssm_informative_obs_stress` seeds `[91021, 91022, 91023]` routes `['streaming', 'low_rank']`: P01 stopped after earlier hard route diagnostic veto.

## Non-Claims

- LGSSM exact-Kalman gate artifact only
- no model-suite promotion claim
- no statistical superiority claim
- no nonlinear posterior correctness claim
- no dense Sinkhorn equivalence claim
- no HMC readiness claim
- no package/public default readiness claim
