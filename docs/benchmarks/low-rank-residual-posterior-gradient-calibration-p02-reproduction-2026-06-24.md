# Low-Rank Residual Posterior-Gradient Calibration P01

- Status: `FAIL`
- Phase: `LOW_RANK_RESIDUAL_POSTERIOR_GRADIENT_CALIBRATION_P01`
- Evidence class: `owner_designated_managed_session_visible_gpu_trusted`
- Hard vetoes: `['lgssm_small_exact_ref:91002:low_rank:qr_plus:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:center:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:q_plus:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:q_minus:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:r_plus:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:r_minus:route_value_gradient_nonfinite', 'lgssm_small_exact_ref:91003:low_rank:qr_plus:route_value_gradient_nonfinite']`
- JSON artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p02-reproduction-2026-06-24.json`

## Rows

| Case | Seed | Route | Status | Peak Match | Max Value Error | Max Grad Rel Error | Min Grad Cos | Vetoes |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `streaming` | `PASS` | `False` | 1.8691673278808594 | 95.39123646636848 | 0.5425920843771693 | `[]` |
| lgssm_small_exact_ref | 91001 | `low_rank` | `PASS` | `False` | 1.9766120910644531 | 1.3879955018116232 | 0.7790965268517905 | `[]` |
| lgssm_small_exact_ref | 91002 | `streaming` | `PASS` | `True` | 0.84759521484375 | 0.46733367846566354 | 0.9336252867698753 | `[]` |
| lgssm_small_exact_ref | 91002 | `low_rank` | `FAIL` | `True` | 0.8533077239990234 | 0.27357667743077113 | 0.9620311935393715 | `['qr_plus:route_value_gradient_nonfinite']` |
| lgssm_small_exact_ref | 91003 | `streaming` | `PASS` | `True` | 0.9239311218261719 | 71.04166096343143 | -0.22177463496854144 | `[]` |
| lgssm_small_exact_ref | 91003 | `low_rank` | `FAIL` | `True` | 0.9209480285644531 | nan | nan | `['center:route_value_gradient_nonfinite', 'q_plus:route_value_gradient_nonfinite', 'q_minus:route_value_gradient_nonfinite', 'r_plus:route_value_gradient_nonfinite', 'r_minus:route_value_gradient_nonfinite', 'qr_plus:route_value_gradient_nonfinite']` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `visible`
- CUDA_VISIBLE_DEVICES: `1`
- TF32 recorded: `True`
- JIT compile: `True`
- GPU trust basis: `owner_designated_managed_session_visible_gpu_trusted`

## Non-Claims

- P01 instrumentation and command-shape artifact only
- residual remains a proxy until calibrated against value/gradient/peak diagnostics
- fixed probe-neighborhood peak is not a global MAP claim
- no calibrated threshold claim
- no posterior correctness claim
- no HMC readiness claim
- no package/public default readiness claim
- no statistical superiority claim
- no scientific validity claim
