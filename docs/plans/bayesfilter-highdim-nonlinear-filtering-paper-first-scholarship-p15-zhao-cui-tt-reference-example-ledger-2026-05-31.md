# P15 Reference Example Ledger

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

Decision: `TWO_STEP_REFERENCE_EXAMPLE_PASS`

Command:

```text
python docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p15-zhao-cui-tt-fixed-branch-minimal-example-2026-05-31.py
```

Output summary:

```text
P15_FIXED_BRANCH_REFERENCE_ONLY
alpha0=0.72
c1_shift=-0.44546019351
c2_shift=-1.49696143428
ell=-0.569442222488
grad=-1.00473154806
step1_fit_residual=3.905823e-01
step2_fit_residual=3.544318e-01
step1_max_normal_eq_cond=2.977710e+00
step2_max_normal_eq_cond=2.914195e+00
min_parity_relerr=7.604872e-12
P15_REFERENCE_EXAMPLE_PASS
```

## Interpretation

The example confirms that the fixed-branch analytical derivative differentiates the same scalar computed by the forward pass on a two-step scalar model. Unlike the first draft, it carries the saved step-1 numerator and derivative object into step 2 through the previous-filter term.

## Explicit Non-Claims

The script is reference/prototype material only. It is not a BayesFilter production implementation, not a TensorFlow/TFP path, and not high-dimensional validation.
