# SVD-Nystrom LGSSM Exact-Kalman Gate

- Status: `FAIL`
- Phase: `SVD_NYSTROM_NOHMC_PROMOTION_P02_LGSSM_REFERENCE`
- Evidence class: `trusted_gpu_exact_reference_candidate`
- Hard vetoes: `['lgssm_small_exact_ref:91001:svd_nystrom:nonfinite_route_output', 'lgssm_small_exact_ref:91001:svd_nystrom:nonfinite_nystrom_factors', 'lgssm_small_exact_ref:91001:svd_nystrom:nonfinite_nystrom_particles']`
- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p02a-lgssm-reference-small-gpu0-fp64core-2026-06-25.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Row residual | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `svd_nystrom` | `FAIL` | nan | nan | nan | nan | `['nonfinite_route_output', 'nonfinite_nystrom_factors', 'nonfinite_nystrom_particles']` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `0`
- TF32 recorded: `True`
- JIT compile: `True`

## Non-Claims

- LGSSM exact-Kalman SVD-Nystrom gate artifact only
- no model-suite promotion claim
- no statistical superiority claim
- no nonlinear posterior correctness claim
- no dense Sinkhorn equivalence claim
- no HMC readiness claim
- no package/public default readiness claim
- no code default switch
