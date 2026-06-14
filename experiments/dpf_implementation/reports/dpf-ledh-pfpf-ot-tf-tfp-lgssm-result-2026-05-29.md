# TF/TFP LEDH-PF-PF-OT LGSSM Result

## Decision

`DPF_LEDH_PFPF_OT_TF_TFP_LGSSM_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| primary criterion | pass | finite TF/TFP LEDH-PF-PF-OT rows, Kalman comparison, corrected-weight diagnostics, Sinkhorn residuals, reproducibility digest |
| median bootstrap RMSE to Kalman | comparator | `0.078914` |
| median OT-DPF RMSE to Kalman | comparator | `0.064609` |
| median LEDH-PF-PF-OT RMSE to Kalman | smoke | `0.068304` |
| median LEDH abs loglik delta | smoke | `1.124797` |
| max LEDH Sinkhorn residual | veto | `5.428e-08` |
| min LEDH Jacobian singular value | veto | `8.049e-01` |

## Interpretation

The LGSSM smoke checks the TF/TFP LEDH-PF-PF proposal-correction path against an
exact Kalman reference and keeps bootstrap PF / bootstrap OT-DPF as comparators.
This nominates LEDH-PF-PF-OT as the default experimental DPF architecture, not
as production or posterior validation.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No NAWM-scale readiness is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
