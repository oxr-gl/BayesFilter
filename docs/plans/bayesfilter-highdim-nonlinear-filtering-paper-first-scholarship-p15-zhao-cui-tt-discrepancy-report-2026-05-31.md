# P15 Discrepancy Report

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

No unresolved Codex-Claude discrepancies remain.

Claude execution review iteration 1 rejected with five findings; Codex classified all as `ACCEPT` and patched them. Claude execution review iteration 2 accepted. The only residual note was a non-blocking result-ledger status phrase, which Codex patched.
