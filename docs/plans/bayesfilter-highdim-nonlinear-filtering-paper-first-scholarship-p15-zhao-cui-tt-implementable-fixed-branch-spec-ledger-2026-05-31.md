# P15 Implementability Ledger

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

## Skeptical Pre-Execution Audit

Decision: `PRE_EXECUTION_AUDIT_PASS_WITH_NARROW_SCOPE`

- The value path is a single declared fixed branch: affine domain, normalized Legendre basis, Halton design, uniform weights, fixed ranks, fixed ridge ALS sweeps, frozen shift, frozen defensive mass.
- The derivative target is exactly the scalar in Eq. (1.3) of the P15 note, not the adaptive Zhao-Cui code path.
- The main reader-facing note avoids governance labels in the main exposition; source/code audit material is confined to appendices and ledgers.
- The minimal example is reference-only and tests implementability plus same-scalar parity, not production readiness or posterior accuracy.

## Missing-Implementation Coverage

| Required item | P15 anchor | Status | Caveat |
|---|---|---|---|
| exact choice of domain maps / reference measure | Sections 3, Eq. affine map/change variables | `FULLY_SPECIFIED` | finite box is a branch choice |
| exact basis families and evaluation | Section 4, Legendre recurrence | `FULLY_SPECIFIED` | normalized Legendre only |
| construction of mass matrices | Section 4, Proposition 2 | `FULLY_SPECIFIED` | identity for normalized Legendre |
| fitting points | Section 6, radical inverse/Halton | `FULLY_SPECIFIED` | deterministic fixed design |
| exact core construction algorithm | Section 7, ridge ALS normal equations | `FULLY_SPECIFIED` | fixed-rank ALS, not adaptive TT-cross |
| rank protocol | Section 7 | `FULLY_SPECIFIED` | ranks fixed, no adaptation |
| tau and lambda | Section 8 | `FULLY_SPECIFIED` | uniform defensive floor |
| c_t computation/differentiation | Sections 7-8 | `FULLY_SPECIFIED` | frozen max-log shift; derivative zero |
| TT marginalization | Section 9, Proposition 4 | `FULLY_SPECIFIED` | square-core contraction representation |
| conditional/KR maps | Section 19/App A | `OPTIONAL_NOT_USED` | not needed for declared scalar |
| data structures | Section 10 | `FULLY_SPECIFIED` | exact shapes and fields listed |
| gradient recursion | Sections 12-15 | `FULLY_SPECIFIED` | through fixed ALS only |
| stabilization/failure diagnostics | Section 16 | `FULLY_SPECIFIED` | diagnostics are veto/explanatory, not validity proof |
| finite-difference protocol | Section 17 | `FULLY_SPECIFIED` | frozen branch parity |
| minimal runnable example | Section 18 and Python script | `FULLY_SPECIFIED` | reference-only toy example |

Decision: `NO_BLOCKER_ROWS_REMAIN`
