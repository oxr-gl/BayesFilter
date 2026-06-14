# DPF Nonlinear-SSM Structural AR(1) Gradient/MLE Result

## Decision

`DPF_NONLINEAR_SSM_STRUCTURAL_AR1_EXECUTED_WITH_ESTIMATION_CALIBRATION_WARNING`

| Check | Status | Evidence |
| --- | --- | --- |
| same scalar | pass | `structural_ar1_negative_log_normalizer_b_parameter_tf` |
| CUT4 gradient at true b | diagnostic | `-0.758732` |
| DPF gradient at true b | diagnostic | `3.892786` |
| CUT4 grid MLE b | diagnostic | `0.650000` |
| DPF median grid MLE b | diagnostic | `0.350000` |
| z distance | calibration | `1.196400` |
| max deterministic residual | veto | `0.000e+00` |

CUT4 is a differentiable comparator, not ground truth.  The structural model is
a toy non-DSGE endogenous/exogenous split fixture.  The z-distance is a
calibration statistic, not a final universal threshold.
