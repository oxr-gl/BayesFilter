# P15 Source Support Ledger

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

## Source Status Table

| Source | Publication status | Local full text/status | Retraction/withdrawal/erratum/quarantine status | Status check basis | Technical anchors inspected | Allowed claims | Forbidden claims |
|---|---|---|---|---|---|---|---|
| Zhao-Cui JMLR 2024 | published JMLR article per local P10-P14 record | local PDF/source record available in `.local_sources` per prior artifacts | no local quarantine notice; no fresh network retraction query in P15 | local source ledgers and inspected PDF/code artifacts | SSM eqs (1)-(3), sequential eqs (9)-(12), Algorithm 1, Eq. (13), Lemma 1, Algorithm 2, Proposition 2, Section 4.1 | sequential joint density, squared-TT density, normalizer/marginal architecture | P15 fixed Legendre/Halton/ridge-ALS is not paper-explicit |
| Cui-Dolgov 2022 | published FoCM article per local P12-P14 record | local/source context checked via prior artifacts | no local quarantine notice; no fresh network retraction query in P15 | local source ledgers | Sections 2-3 transport substrate | squared transport/functional TT context | no claim that P15 validates KR maps |
| Zhao-Cui companion code snapshot | research code snapshot | `third_party/audit/zhao_cui_tensor_ssm_p10/source` | LGPL notice present; no quarantine notice | local code inspection | `models/full_sol.m`, `@TTSIRT/marginalise.m`, README, license | scalar-path/code-behavior evidence | no theorem support from code |

## Caveat

No fresh network retraction or metadata query was performed during P15. Therefore P15 does not claim literature completeness. Paper-backed claims are restricted to local checked technical anchors and project derivations.
