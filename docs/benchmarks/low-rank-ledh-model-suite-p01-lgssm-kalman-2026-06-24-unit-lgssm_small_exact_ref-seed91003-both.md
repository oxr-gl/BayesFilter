# Low-Rank LEDH LGSSM Exact-Kalman Gate

- Status: `FAIL`
- Phase: `LOW_RANK_LEDH_MODEL_SUITE_P01_LGSSM_KALMAN`
- Evidence class: `trusted_gpu_candidate_only_if_launcher_records_trusted_context`
- Hard vetoes: `['lgssm_small_exact_ref:91003:low_rank:factor_marginal_residual_threshold']`
- JSON artifact: `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-unit-lgssm_small_exact_ref-seed91003-both.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Invocations | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91003 | `streaming` | `PASS` | 0.06622548366293084 | 0.24285652711380687 | 0.8682975769042969 | 12 | `[]` |
| lgssm_small_exact_ref | 91003 | `low_rank` | `FAIL` | 0.06638920035056725 | 0.24245469677909753 | 0.8644542694091797 | 12 | `['factor_marginal_residual_threshold']` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 recorded: `True`
- JIT compile: `True`

## Non-Claims

- LGSSM exact-Kalman gate artifact only
- no model-suite promotion claim
- no statistical superiority claim
- no nonlinear posterior correctness claim
- no dense Sinkhorn equivalence claim
- no HMC readiness claim
- no package/public default readiness claim
