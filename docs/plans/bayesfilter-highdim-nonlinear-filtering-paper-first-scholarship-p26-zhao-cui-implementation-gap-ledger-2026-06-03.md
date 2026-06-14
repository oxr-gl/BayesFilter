# P26 Zhao--Cui Implementation Gap Ledger

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

## Initial Status

status: `EXECUTED_PENDING_CLAUDE_REVIEW`

Gaps to close:

- Boxed end-to-end fixed-branch filter and derivative algorithm.
- Explicit alternating sweep recomputation protocol.
- Multi-dimensional retained-filter storage recipe.
- Default stabilization table.
- Finite-difference numeric table.

## Controls Added

status: `ADDED_TO_P26_NOTE`

| Gap | P26 control |
|---|---|
| Need one boxed end-to-end fixed-branch filter and derivative algorithm. | Added `Boxed Algorithm: Fixed-Branch Filter And Derivative Together`, including inputs, initial retained object, target and target derivative values, square-root derivative, fixed sweeps, derivative solve, mass/normalizer derivative, retained filter derivative, scalar derivative, outputs, invariants, and failure exits. |
| Sweep environments and normal equations recomputation are scattered. | Added `Alternating-Sweep Recomputations`, including \(H,\dot H\), prefix/suffix recursions, dotted prefix/suffix recursions, recomputation of \(A_k,N_k,d_k,\dot A_k,\dot N_k,\dot d_k\), left-to-right and right-to-left update formulas, and stale-cache conditions. |
| Multi-dimensional retained filter cannot always be stored as full product-basis matrix. | Added `Retained-Filter Storage When The Product Basis Is Too Large`, including dense storage count, marginal TT evaluator option, low-rank quadratic option, compression residual checks, and evaluator/derivative evaluator contract. |
| Stabilization constants need concrete defaults. | Existing P25 default table was preserved and remains part of P26: \(\epsilon_{\rm floor}\), \(\epsilon_{\rm ridge}\), \(\delta_\tau\), \(\delta_{\rm floor}\), \(\gamma\), \(N_{\rm fit}\), \(S_{\max}\), \(\epsilon_{\rm fit}\), \(\epsilon_{\rm abs}\), \(\varepsilon_{\rm root}\), \(N_{\rm root}\), \(\chi_{\max}\), and \(\kappa_{\max}\). |
| Need a real small finite-difference table. | Added a synthetic finite-difference table with \(h,D(h),G,|D(h)-G|\), plus interpretation of decreasing error and roundoff/fitting sensitivity. |

what_is_not_concluded:
- No production implementation claim.
- No claim that the synthetic finite-difference numbers are empirical results.
- No claim that retained-filter compression is valid unless the evaluator and derivative checks pass.
