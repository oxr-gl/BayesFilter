# Low-Rank Residual Posterior-Gradient Calibration P01

- Status: `PASS`
- Phase: `LOW_RANK_RESIDUAL_POSTERIOR_GRADIENT_CALIBRATION_P01`
- Evidence class: `cpu_hidden_command_shape_debug_only`
- Hard vetoes: `[]`
- JSON artifact: `docs/benchmarks/low-rank-residual-posterior-gradient-calibration-p01-smoke-2026-06-24.json`

## Rows

| Case | Seed | Route | Status | Peak Match | Max Value Error | Max Grad Rel Error | Min Grad Cos | Vetoes |
| --- | ---: | --- | --- | --- | ---: | ---: | ---: | --- |
| lgssm_small_exact_ref | 91001 | `low_rank` | `PASS` | `False` | 0.576040506362915 | 6.747677223332192 | 0.256657694114053 | `[]` |

## Run Manifest

- Git commit: `01213338c7037c468f38b01d013e4ce13526c9e4`
- Device scope: `cpu`
- CUDA_VISIBLE_DEVICES: `-1`
- TF32 recorded: `False`
- JIT compile: `True`

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
