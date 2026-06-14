# P29 Notation Shape Contract Ledger

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p27-zhao-cui-large-scale-validation-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific Computing 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.
- Cui and Dolgov, squared inverse Rosenblatt transport / squared TT background used by Zhao and Cui.

audit_scope:
- Compact notation-shape contract for the risky subsystems identified by P28/P29.

what_is_not_concluded:
- This is a contract ledger, not executable code.
- This does not prove numerical stability.

## Contract

| object | shape/domain | measure / density convention | implementation note | status |
|---|---|---|---|---|
| physical block `r=(x_t,theta,x_{t-1})` | dimension `D=2m+d` | Lebesgue in physical coordinates unless stated | block order matters for lower/upper maps | PASS_TARGETED_AUDIT |
| reference block `u=T(r)` | dimension `D` | product reference `eta(u) du` | store map, inverse, log-Jacobian or density ratio | PASS_TARGETED_AUDIT |
| lower KR map `F(r)` | `[0,1]^D`; component k depends on `r_{<=k}` | diagonal derivative is conditional density | determinant is product of conditionals | PASS_TARGETED_AUDIT |
| TT core `H_k(r_k)` | `R_{k-1} x R_k` | basis-expanded matrix-valued function | endpoint ranks `R_0=R_D=1` | PASS_TARGETED_AUDIT |
| right mass `M_{>k}` | `R_k x R_k` | integral over coordinates `>k` | PSD Gram matrix; Cholesky may need jitter | PASS_TARGETED_AUDIT |
| fixed LS row `A_{j,k}` | row length `R_{k-1} p_k R_k` | evaluated at fixed fitting point | vectorization order must be fixed in branch | PASS_WITH_LIMITATION |
| normal matrix `N_k` | square length `R_{k-1}p_kR_k` | weighted LS plus ridge | nonsingular assumption required | PASS_TARGETED_AUDIT |
| carried numerator `a_t(z_t)` | retained-coordinate evaluator | unnormalized marginal | denominator is `Zhat_t` | PASS_TARGETED_AUDIT |
| carried filter `phat_t=a_t/Zhat_t` | retained density | normalized if `Zhat_t>0` | quotient derivative required | PASS_TARGETED_AUDIT |
| fixed branch `B` | collection of domains, ranks, points, weights, sweeps, shifts, floors | not a density | must be held fixed under derivative and finite difference | PASS_TARGETED_AUDIT |

## Verdict

notation_shape_contract_verdict: `PASS_TARGETED_AUDIT_WITH_IMPLEMENTATION_CAVEAT`

The shape contract is coherent. A coder still needs an explicit vectorization convention test for `vec(C_k)` and `A_{j,k}`.

