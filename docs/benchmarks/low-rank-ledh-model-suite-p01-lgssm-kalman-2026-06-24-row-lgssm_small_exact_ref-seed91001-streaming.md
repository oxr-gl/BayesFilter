# Low-Rank LEDH LGSSM Exact-Kalman Gate

- Status: `PASS`
- Phase: `LOW_RANK_LEDH_MODEL_SUITE_P01_LGSSM_KALMAN`
- Evidence class: `trusted_gpu_candidate_only_if_launcher_records_trusted_context`
- Hard vetoes: `[]`
- JSON artifact: `docs/benchmarks/low-rank-ledh-model-suite-p01-lgssm-kalman-2026-06-24-row-lgssm_small_exact_ref-seed91001-streaming.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Invocations | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `streaming` | `PASS` | 0.11871645985323664 | 0.24329509510026948 | 1.6849708557128906 | 12 | `[]` |

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
