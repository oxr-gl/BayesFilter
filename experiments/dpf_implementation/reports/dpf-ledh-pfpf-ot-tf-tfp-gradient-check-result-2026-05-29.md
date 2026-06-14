# TF/TFP LEDH-PF-PF-OT Gradient Check Result

## Decision

`DPF_LEDH_PFPF_OT_TF_TFP_GRADIENT_CHECK_PASSED`

## Decision Table

| Check | Status | Evidence |
| --- | --- | --- |
| scalar id | pass | `lgssm_ledh_pfpf_ot_corrected_negative_log_normalizer_proxy_tf` |
| same-scalar contract | pass | GradientTape and finite difference use fixed observations/common random numbers |
| GradientTape gradient | smoke | `1.081501` |
| finite-difference gradient | reference | `1.081501` |
| absolute error | veto | `1.484e-07` |

## Interpretation

The TF/TFP same-scalar GradientTape smoke check passed for the named corrected
LEDH-PF-PF-OT proxy scalar.  This is not posterior, HMC, or production
validation.

## Non-Implications

- No production readiness is concluded.
- No public API readiness is concluded.
- No HMC readiness is concluded.
- No posterior correctness is concluded.
- No likelihood-score validity is concluded beyond this named proxy scalar.
- No NAWM-scale readiness is concluded.
- No banking or model-risk claim is concluded.
- No monograph claim is concluded without separate review.
