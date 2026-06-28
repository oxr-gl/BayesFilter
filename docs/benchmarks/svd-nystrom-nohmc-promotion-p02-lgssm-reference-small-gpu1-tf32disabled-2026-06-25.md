# SVD-Nystrom LGSSM Exact-Kalman Gate

- Status: `PASS`
- Phase: `SVD_NYSTROM_NOHMC_PROMOTION_P02_LGSSM_REFERENCE`
- Evidence class: `trusted_gpu_exact_reference_candidate`
- Hard vetoes: `[]`
- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-lgssm-reference-small-gpu1-tf32disabled-2026-06-25.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Row residual | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `svd_nystrom` | `PASS` | 0.12203076773031596 | 0.24273017634681113 | 1.7836990356445312 | 0.0035163164138793945 | `[]` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 recorded: `False`
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
