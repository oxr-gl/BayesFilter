# SVD-Nystrom LGSSM Exact-Kalman Gate

- Status: `PASS`
- Phase: `SVD_NYSTROM_NOHMC_PROMOTION_P02_LGSSM_REFERENCE`
- Evidence class: `cpu_hidden_command_shape_debug_only`
- Hard vetoes: `[]`
- JSON artifact: `docs/benchmarks/svd-nystrom-nohmc-promotion-p02-cpu-shape-lgssm-small-2026-06-25.json`

## Rows

| Case | Seed | Route | Status | Mean RMSE | Var RMSE | Loglik delta | Row residual | Vetoes |
| --- | ---: | --- | --- | ---: | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `svd_nystrom` | `PASS` | 0.15599040895361252 | 0.1551334773980879 | 0.587857723236084 | 1.681442154222168e-05 | `[]` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
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
