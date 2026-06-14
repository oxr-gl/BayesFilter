# P2 Result: Range-Bearing Stress

Date: 2026-05-29

## Decision

`DPF_NONLINEAR_SSM_RANGE_BEARING_STRESS_PASSED`

## Evidence Contract Result

The bounded range-bearing stress run reused the TF/TFP UKF approximate
reference, bootstrap PF, bootstrap OT-DPF, and LEDH-PF-PF-OT comparator ladder.
The UKF is approximate, not ground truth.

## Metrics

| Diagnostic | Value | Role |
| --- | ---: | --- |
| median LEDH state RMSE to UKF | 0.07742171157461389 | proxy |
| median LEDH latent position RMSE | 0.08208559692155928 | proxy |
| median LEDH observation proxy RMSE | 0.1141841886622492 | proxy |
| max LEDH Sinkhorn residual | 6.661338147750939e-16 | veto |
| min LEDH Jacobian singular value | 0.643116090267122 | veto |

## Verification

- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_stress_ledh_pfpf_ot_tf`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_stress_ledh_pfpf_ot_tf --validate-only`: passed.
- `MPLCONFIGDIR=/tmp CUDA_VISIBLE_DEVICES=-1 python -m experiments.dpf_implementation.tf_tfp.runners.run_range_bearing_stress_ledh_pfpf_ot_tf --check-reproducibility`: passed.

JSON: `experiments/dpf_implementation/reports/outputs/dpf_nonlinear_ssm_range_bearing_stress_2026-05-29.json`.

## Caveats

UKF is approximate and proxy RMSE is diagnostic.  No posterior correctness, HMC
readiness, production readiness, DSGE/NAWM validation, or monograph claim is
concluded.
