# P15 Omitted Paper And Reviewer Risk Ledger

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

## Omission Risks

| Risk | Why a reviewer may ask | Current action |
|---|---|---|
| TT-cross and TT approximation foundations beyond Zhao-Cui/Cui-Dolgov | P15 uses TT ideas but fixes ridge ALS | record as background omission; P15 is design spec not survey |
| SMC/particle filter competitors | high-dimensional filtering baseline concern | compare later in chapter synthesis; not theorem support here |
| Sparse-grid Gaussian projection from ch34 | direct competing candidate | named as comparator; not repeated in P15 note |
| Transport map foundations | KR maps mentioned but not used | optional only; no gradient claim depends on KR maps |

Decision: `OMISSION_RISKS_RECORDED_NO_COMPLETENESS_CLAIM`
