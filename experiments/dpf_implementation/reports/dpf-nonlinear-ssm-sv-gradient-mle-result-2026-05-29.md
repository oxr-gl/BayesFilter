# DPF Nonlinear-SSM SV Gradient/MLE Result

## Decision

`DPF_NONLINEAR_SSM_SV_GRADIENT_MLE_PASSED_SMOKE`

| Check | Status | Evidence |
| --- | --- | --- |
| same scalar | pass | `sv_negative_log_normalizer_mu_parameter_tf` |
| CUT4 gradient at true mu | diagnostic | `1.777923` |
| DPF gradient at true mu | diagnostic | `2.953948` |
| CUT4 grid MLE mu | diagnostic | `-1.000000` |
| DPF median grid MLE mu | diagnostic | `-1.000000` |
| z distance | calibration | `0.000000` |

CUT4 is a differentiable comparator, not ground truth.  The z-distance is a
calibration statistic, not a final universal threshold.
