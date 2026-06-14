# DPF Nonlinear-SSM Range-Bearing Stress Result

## Decision

`DPF_NONLINEAR_SSM_RANGE_BEARING_STRESS_PASSED`

| Check | Status | Evidence |
| --- | --- | --- |
| source nonlinear runner | pass | `DPF_LEDH_PFPF_OT_TF_TFP_RANGE_BEARING_PASSED` |
| median LEDH state RMSE to UKF | proxy | `0.077422` |
| max LEDH Sinkhorn residual | veto | `6.661e-16` |
| min LEDH Jacobian singular value | veto | `6.431e-01` |

UKF is approximate, not ground truth; proxy RMSE is diagnostic only.
