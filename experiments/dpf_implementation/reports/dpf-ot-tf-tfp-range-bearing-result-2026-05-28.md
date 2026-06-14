# TF/TFP OT-DPF Range-Bearing Result

## Decision

`DPF_OT_TF_TFP_RANGE_BEARING_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| primary criterion | pass | finite TF/TFP UKF/PF/OT rows, Sinkhorn residuals, reproducibility digest |
| median bootstrap state RMSE to UKF | proxy | `0.049288` |
| median OT-DPF state RMSE to UKF | proxy | `0.064598` |
| median bootstrap latent position RMSE | proxy | `0.071491` |
| median OT-DPF latent position RMSE | proxy | `0.075665` |
| median bootstrap observation proxy RMSE | proxy | `0.096541` |
| median OT-DPF observation proxy RMSE | proxy | `0.114911` |
| max OT Sinkhorn residual | veto | `4.441e-16` |

## Interpretation

The TF/TFP range-bearing smoke passed with a UKF approximate reference and a
TF bootstrap PF comparator.  UKF is not ground truth and proxy RMSE does not
establish posterior correctness.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No learned or neural OT promotion is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
- UKF is approximate and proxy RMSE is not correctness evidence.
