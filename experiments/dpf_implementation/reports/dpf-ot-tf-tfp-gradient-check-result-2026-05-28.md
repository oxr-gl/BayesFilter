# TF/TFP OT-DPF Gradient Check Result

## Decision

`DPF_OT_TF_TFP_GRADIENT_CHECK_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| scalar id | pass | `lgssm_relaxed_ot_negative_log_normalizer_proxy_tf` |
| same-scalar contract | pass | GradientTape and finite difference use fixed observations/common random numbers |
| GradientTape gradient | smoke | `0.359155` |
| finite-difference gradient | reference | `0.359153` |
| absolute error | veto | `2.118e-06` |

## Interpretation

The TF/TFP same-scalar GradientTape smoke check passed for the named relaxed
OT-DPF proxy scalar.  This is not posterior, HMC, or production validation.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No likelihood-score validity is concluded beyond this named proxy scalar.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
