# P15 Gradient Derivation Ledger

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

## Gradient Target

Declared scalar:

```tex
\widehat\ell_T^{TT}(\alpha;B)=\sum_t [\log(R_{t,0}(\alpha;B_t)+\tau_t)-c_t].
```

Primary branch has fixed `tau_t` and `c_t`, so their derivatives are zero.

## Obligations

| Obligation | Note anchor | Status |
|---|---|---|
| target value derivative ydot | Section 12 | `DERIVED_IN_NOTE` |
| previous-filter log derivative | Section 12 | `DERIVED_IN_NOTE` |
| ALS solve derivative | Section 13 fixed-rank ridge ALS solve derivative proposition | `DERIVED_IN_NOTE` |
| design-row derivative | Section 13 | `DERIVED_IN_NOTE` |
| mass-contraction derivative | Section 14 | `DERIVED_IN_NOTE` |
| square-core derivative | Section 14 | `DERIVED_IN_NOTE` |
| final score | Section 14 same-scalar fixed-branch gradient proposition | `DERIVED_IN_NOTE` |
| parity check | Section 17 and script | `REFERENCE_EXAMPLE_PASS` |

## Reference Example Result

The Python script passed finite-difference parity with minimum relative error `7.604872e-12` for the tested one-parameter scalar model.
