# P15 Backward Snowball Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," FoCM 2022.
- P10-P14 BayesFilter Zhao-Cui TT artifacts.

what_is_not_concluded:
- No posterior accuracy claim.
- No global derivative claim for adaptive TT-cross or rank-changing code.
- No HMC convergence claim.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation on the target high-dimensional model.

## Status

Backward snowballing is inherited from P10-P14 source work for this execution and remains not freshly expanded. P15 does not claim literature completeness.

| Seed | Related works considered in local artifacts | Action |
|---|---|---|
| Zhao-Cui 2024 | Cui-Dolgov squared inverse Rosenblatt/functional TT substrate | included for source context |
| Zhao-Cui 2024 | particle filters, SMC, TT approximation, transport references mentioned in paper | omission-risk register rather than main P15 theorem support |
| Cui-Dolgov 2022 | transport/TT background | included only for context |

Decision: `BACKWARD_SNOWBALL_PARTIAL_NOT_COMPLETENESS_CLAIM`
