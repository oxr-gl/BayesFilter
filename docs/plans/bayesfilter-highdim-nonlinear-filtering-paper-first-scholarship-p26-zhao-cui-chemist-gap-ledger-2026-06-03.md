# P26 Zhao--Cui Chemist Gap Ledger

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No real chair endorsement claim.

## Initial Status

status: `EXECUTED_PENDING_CLAUDE_REVIEW`

Gaps to close:

- KR map and preconditioning teach-back explanation.
- Vivid moderate-rank physical example.
- One-page story of the derivative before Proposition 2.
- More sequential numerical trace material.

## Controls Added

status: `ADDED_TO_P26_NOTE`

| Gap | P26 control |
|---|---|
| KR map and preconditioning remain dense. | Added `Why This Transport Is The Right Device`, with one-dimensional probability-integral transform, sequential inverse conditional CDF construction, triangular Jacobian determinant, and the TT marginal-ratio connection. Added `Why Preconditioning And KR Maps Belong Together`, with bridge ratio, oscillation reduction, two-step sampler, and combined Jacobian identity. |
| Moderate TT rank needs a vivid physical example. | Added a local sensor/polymer/reaction-coordinate example in `Why Moderate Tensor-Train Rank Is A Plausible Hypothesis`, including local energy factorization, cross-split bridge term, separated edge expansion, and a grid-width rank-pressure bound. |
| Proposition 2 needs a one-page derivative story before the formal proof. | Added `The Story Of The Fixed-Branch Derivative` immediately before Proposition 2, explaining adaptive branch jumps, fixed scalar, forward chain, dotted chain, linear-solve derivative, normalizer derivative, quotient derivative, and narrowness. |
| Numerical trace too small to make the sequential method click. | Expanded the trace with second normalizer, two-step log-evidence scalar, retained-filter role at time two, a time-step table, and a synthetic finite-difference table. |

what_is_not_concluded:
- No claim that this proves exact posterior accuracy.
- No claim that a real chemistry chair has endorsed P26.
- No claim that moderate rank will hold for arbitrary high-dimensional chemistry models without diagnostics.
