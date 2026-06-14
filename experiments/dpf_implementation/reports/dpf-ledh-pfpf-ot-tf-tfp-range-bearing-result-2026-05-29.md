# TF/TFP LEDH-PF-PF-OT Range-Bearing Result

## Decision

`DPF_LEDH_PFPF_OT_TF_TFP_RANGE_BEARING_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| primary criterion | pass | finite TF/TFP UKF/PF/OT/LEDH rows, corrected-weight diagnostics, Sinkhorn residuals, reproducibility digest |
| median bootstrap state RMSE to UKF | comparator | `0.078187` |
| median OT-DPF state RMSE to UKF | comparator | `0.079429` |
| median LEDH-PF-PF-OT state RMSE to UKF | proxy | `0.077422` |
| median LEDH latent position RMSE | proxy | `0.082086` |
| median LEDH observation proxy RMSE | proxy | `0.114184` |
| max LEDH Sinkhorn residual | veto | `6.661e-16` |
| min LEDH Jacobian singular value | veto | `6.431e-01` |

## Interpretation

The range-bearing smoke checks the TF/TFP LEDH-PF-PF proposal-correction path
against a UKF approximate reference and comparator filters.  UKF is not ground
truth and proxy RMSE does not establish nonlinear posterior correctness.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No NAWM-scale readiness is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
- UKF is approximate and proxy RMSE is not correctness evidence.
