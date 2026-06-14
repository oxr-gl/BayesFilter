# P15 Claim Support Ledger

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

## Claims

| Claim | Support class | Anchor |
|---|---|---|
| Filtering step uses joint density over current state, parameter, old state | `PAPER_EXPLICIT` and `PROJECT_DERIVATION` | P15 Section 2; Zhao-Cui eqs (9)-(12) via P10 |
| Squared TT plus defensive density is nonnegative | `PROJECT_DERIVATION` | P15 Sections 5, 14 |
| Mass contraction computes square integral | `PROJECT_DERIVATION` | P15 Section 8 mass-contraction proposition |
| Marginalization by square-core contractions gives next filter numerator | `PROJECT_DERIVATION` | P15 Section 9 marginalization proposition |
| Companion code has scalar log(sirt.z)-const and z=fun_z+tau behavior | `IMPLEMENTATION_EVIDENCE` | full_sol.m, @TTSIRT/marginalise.m |
| P15 Legendre/Halton/ridge-ALS path is implementable fixed branch | `DESIGN_CHOICE_FOR_P15` | P15 Sections 3-15 and script |
| Same-scalar gradient differentiates declared fixed-branch scalar | `PROJECT_DERIVATION` | P15 Section 14 same-scalar gradient proposition and two-step parity script |
| P15 proves posterior accuracy or high-dimensional superiority | `SOURCE_GAP_BLOCKER` | explicitly not concluded |
