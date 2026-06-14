# P24 Zhao--Cui Claim-Support Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.

what_is_not_concluded:
- No claim that adaptive branches are globally differentiable.
- No claim of exact posterior accuracy.
- No production implementation claim.

## Claim Mapping

| P24 claim | Support class | Anchor |
|---|---|---|
| State-space model has Markov transition and conditionally independent observation density. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (1)--(2); P24 BF-1--BF-2. |
| Joint density factors as prior, initial density, transition factors, and likelihood factors. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eq. (3); P24 BF-3/BF-3a. |
| Filtering, parameter learning, path estimation, and smoothing are marginalization problems. | `PRIMARY_TECHNICAL_SUPPORT` | Zhao--Cui Eqs. (5)--(8); P24 BF-5--BF-8. |
| Sequential update reduces to three-block adjacent-state density and marginalization over old state. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (9)--(11); P24 BF-9--BF-11. |
| Functional TT represents a multivariate function by rank-linked univariate matrix cores. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Section 2.2; P24 TT-1--TT-3a. |
| TT marginalization can be done by integrated core contractions. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Section 2.2; P24 TT-4--TT-5. |
| Algorithm 1 fits a nonseparable target, reapproximates it by TT, and retains the old-state marginal. | `PRIMARY_TECHNICAL_SUPPORT` | Zhao--Cui Algorithm 1/Eq. (12); P24 A1-1--A1-7. |
| Squared TT gives a nonnegative density with defensive reference mass. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eq. (13); P24 S1--S3. |
| Square-root fit error controls Hellinger error at the level stated by Zhao--Cui. | `PRIMARY_TECHNICAL_SUPPORT` delegated | Zhao--Cui Lemma 1 citing Cui--Dolgov; P24 S4--S6. |
| Squared-TT marginalization uses mass matrices and Cholesky/square-root factors. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Proposition 2/Eq. (14); P24 M1--M9. |
| KR conditional maps are built from marginal ratios and triangular CDFs. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (17)--(20), Proposition 4, Remark 3; P24 K1--K8. |
| Particle correction weights divide exact recursive target by TT proposal. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (21)--(23), Algorithm 3; P24 F1--F7. |
| Backward smoothing/path weights use lower conditional maps and path proposal ratio. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (24)--(26), Algorithm 4; P24 B1--B9. |
| Preconditioning fits a residual density in transformed coordinates and pulls it back. | `PRIMARY_TECHNICAL_SUPPORT` + `PROJECT_DERIVATION` | Zhao--Cui Eqs. (30)--(33); P24 P1--P5. |
| Gaussian and tempered bridges are Zhao--Cui preconditioning choices. | `PRIMARY_TECHNICAL_SUPPORT` | Zhao--Cui Sections 5.2--5.3, Eqs. (34)--(35); P24 P6a--P7. |
| Fixed-branch derivative differentiates the declared scalar only when branch objects are fixed. | `PROJECT_DERIVATION` + `IMPLEMENTATION_EVIDENCE` | P24 FB/G propositions; P10/P15 fixed-branch evidence. |

Decision: `CLAIM_SUPPORT_PASS_FOR_P24_DRAFT`.
