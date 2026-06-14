# P15 Algorithm Choices Ledger

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

## Declared Primary Path

| Choice | P15 value | Reason | Source class |
|---|---|---|---|
| domain | finite hyperrectangle mapped to [-1,1]^D | explicit integrals and finite basis | `DESIGN_CHOICE_FOR_P15` |
| basis | normalized Legendre | identity mass matrix | `DESIGN_CHOICE_FOR_P15` |
| fitting design | deterministic Halton, first D primes | reproducible fixed points | `DESIGN_CHOICE_FOR_P15` |
| weights | W = I/N_fit | single fixed least-squares objective | `DESIGN_CHOICE_FOR_P15` |
| core construction | fixed-rank ridge ALS | differentiable stored linear solves | `DESIGN_CHOICE_FOR_P15` |
| ranks | fixed declared ranks | avoids branch changes | `DESIGN_CHOICE_FOR_P15` |
| defensive density | uniform 2^{-D} | normalized positive floor | `PROJECT_DERIVATION` |
| tau | epsilon_tau 2^D | uniform floor epsilon_tau | `DESIGN_CHOICE_FOR_P15` |
| shift | c=-max_j log q at alpha0 | frozen stabilizing shift | `DESIGN_CHOICE_FOR_P15` |
| KR maps | not used | not needed for likelihood/gradient | `DESIGN_CHOICE_FOR_P15` |

## Deliberate Narrowing

The path is narrower than Zhao-Cui adaptive research code. This is intentional: a same-scalar analytical gradient requires fixed branch objects.
