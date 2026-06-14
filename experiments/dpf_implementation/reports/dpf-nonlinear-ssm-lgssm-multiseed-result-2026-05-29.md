# DPF Nonlinear-SSM LGSSM Multiseed Result

## Decision

`DPF_NONLINEAR_SSM_LGSSM_MULTISEED_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| exact-reference regression | pass | source runner `DPF_LEDH_PFPF_OT_TF_TFP_LGSSM_PASSED` |
| median LEDH RMSE to Kalman | diagnostic | `0.068304` |
| median LEDH abs loglik delta | diagnostic | `1.124797` |
| max LEDH Sinkhorn residual | veto | `5.428e-08` |

This is regression evidence only; filtered-state RMSE is diagnostic, not
parameter-estimation validation.
