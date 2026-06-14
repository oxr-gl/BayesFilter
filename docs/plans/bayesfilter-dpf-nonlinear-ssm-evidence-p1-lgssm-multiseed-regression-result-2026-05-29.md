# P1 Result: LGSSM Multiseed Regression

Date: 2026-05-29

## Decision

`DPF_NONLINEAR_SSM_LGSSM_MULTISEED_PASSED`

## Evidence Contract Result

The bounded LGSSM regression reused the exact Kalman reference and the existing
TF/TFP LEDH-PF-PF-OT runner.  It exercised bootstrap PF, bootstrap OT-DPF, and
LEDH-PF-PF-OT rows over seeds `[111, 222, 333]` with 64 particles.

## Metrics

| Diagnostic | Value | Role |
| --- | ---: | --- |
| median LEDH filtered mean RMSE to Kalman | 0.06830431164955209 | diagnostic |
| median LEDH absolute log-likelihood delta to Kalman | 1.1247968987647852 | diagnostic |
| max LEDH Sinkhorn residual | 5.427581322575703e-08 | veto |
| min LEDH Jacobian singular value | 0.8048770788598271 | veto |

## Verification

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_multiseed_ledh_pfpf_ot_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_multiseed_ledh_pfpf_ot_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_lgssm_multiseed_ledh_pfpf_ot_tf --check-reproducibility`: passed.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_lgssm_multiseed_2026-05-29.json`.

## Caveats

This is regression and numerical-smoke evidence.  Filtered-state RMSE does not
validate nonlinear parameter estimation, posterior correctness, HMC readiness,
production readiness, DSGE/NAWM behavior, or monograph claims.
