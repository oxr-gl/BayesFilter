# P21 Zhao--Cui Equation-To-Specification Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No full adaptive Zhao--Cui implementation claim.

## Mapping

| Would-be block | Inputs and shapes | Outputs and shapes | Equation anchors | Type | Diagnostics |
|---|---|---|---|---|---|
| `transform_target_t1` | \(Z_{\rm fit}:(N,2)\), \(\beta\), model constants, domain map | \(\widetilde q_1:(N,)\), \(\dot{\widetilde q}_1:(N,)\) | P21-7, P21-67--P21-71 | value + derivative | \(\min_j\widetilde q_{1,j}>0\); frozen domain |
| `transform_target_t2` | \(Z_{\rm fit}:(N,2)\), carried \(P_1,\dot P_1:(p,p)\), query basis \(B^{\rm query}_{j\ell}=b_1(Z_{\rm fit}[j,2])[\ell]:(N,p)\), \(\beta\), model constants | carried values \(p,\dot p:(N,)\), \(\widetilde q_2:(N,)\), \(\dot{\widetilde q}_2:(N,)\) | P21-6, P21-57e--P21-60; P20 FB1, P19-46 | value + derivative | previous-filter derivative present; frozen \(h_{t,1}\); \(B^{\rm query}\) uses coordinate 2 |
| `sqrt_target` | \(\widetilde q_t:(N,)\), \(\dot{\widetilde q}_t:(N,)\), \(c_t\) | \(y:(N,)\), \(\dot y:(N,)\) | P21-8, P21-61; P20 C10, P19-47 | value + derivative | positive target or declared floor |
| `basis_table` | \(Z_{\rm fit}:(N,2)\), degree \(p\) | \(B_{\rm val}:(N,2,p)\), \(B_k:(p,p)\) | P21-72--P21-75 | value-only | orthonormal mass matrix or recorded quadrature error |
| `eval_tt` | \(C_1:(1,p,R)\), \(C_2:(R,p,1)\), \(B_{\rm val}\) | \(\phi:(N,)\) | P21-27--P21-29; P20 D1--D2, P19-48 | value-only | shape match and finite values |
| `fit_core_1` | \(C_2:(R,p,1)\), \(B_{\rm val}\), \(W:(N,N)\), \(y:(N,)\), \(\rho\) | \(C_1:(1,p,R)\) | P21-45--P21-47, P21-76; P19-62--P19-65 | value-only | condition number of \(N^{(1)}\) |
| `fit_core_2` | \(C_1:(1,p,R)\), \(B_{\rm val}\), \(W:(N,N)\), \(y:(N,)\), \(\rho\) | \(C_2:(R,p,1)\) | P21-48--P21-49, P21-77; P19-62--P19-65 | value-only | condition number of \(N^{(2)}\) |
| `differentiate_core_1` | \(A^{(1)},\dot A^{(1)},W,y,\dot y,C_1,\rho\) | \(\dot C_1:(1,p,R)\) | P21-40--P21-44, P21-78 | derivative-producing | same \(N^{(1)}\) as value solve |
| `differentiate_core_2` | \(A^{(2)},\dot A^{(2)},W,y,\dot y,C_2,\rho\) | \(\dot C_2:(R,p,1)\) | P21-40--P21-44, P21-78 | derivative-producing | same \(N^{(2)}\) as value solve |
| `mass_contraction` | \(C_1,C_2,B_1,B_2\) | \(R_\phi\), \(S_2:(R,R)\) | P21-35--P21-37; P19-66--P19-72 | value-only | \(R_\phi\ge0\) |
| `differentiate_mass` | \(C_1,C_2,\dot C_1,\dot C_2,B_1,B_2\) | \(\dot R_\phi\), \(\dot S_2:(R,R)\) | P21-38--P21-39; P19-67--P19-72 | derivative-producing | product-rule terms all present |
| `normalizer` | \(R_\phi,\dot R_\phi,c_t,\tau_t\) | \(\widehat Z_t,\dot{\widehat Z}_t\) | P21-10, P21-17--P21-21; P19-71--P19-72 | value + derivative | \(\widehat Z_t>0\) |
| `carried_numerator` | \(C_1:(1,p,R)\), \(S_2:(R,R)\), \(c_t,\tau_t\), Legendre constant \(b_1[0]=1/\sqrt2\) | \(Q_t:(p,p)\), evaluator \(a_t(z)=b_1(z)^\top Q_t b_1(z)\) | P21-53--P21-57c; P19-73--P19-74d | value-only | nonnegative marginal; defensive term stored as \(Q_t[0,0]\gets Q_t[0,0]+\tau_t\) |
| `differentiate_carried_numerator` | \(C_1,\dot C_1:(1,p,R)\), \(S_2,\dot S_2:(R,R)\), \(c_t\) | \(\dot Q_t:(p,p)\), evaluator \(\dot a_t(z)=b_1(z)^\top\dot Q_t b_1(z)\) | P21-56--P21-57d; P19-74d | derivative-producing | three product-rule groups present; no derivative of frozen \(\tau_t\) |
| `carried_filter` | \(Q_t,\dot Q_t:(p,p)\), \(\widehat Z_t,\dot{\widehat Z}_t\), query basis \(B^{\rm query}:(M,p)\) | \(P_t,\dot P_t:(p,p)\), \(\widehat p_t^{\rm ref},\dot{\widehat p}_t^{\rm ref}:(M,)\) | P21-51--P21-57i; P19-75--P19-76 | value + derivative | normalization and quotient-rule check; query coordinate declared |
| `log_evidence` | \(\widehat Z_1,\widehat Z_2,\dot{\widehat Z}_1,\dot{\widehat Z}_2\) | \(\widehat\ell_2,\partial_\beta\widehat\ell_2\) | P21-20--P21-21; P19-85 | value + derivative | positive normalizers |
| `finite_difference_protocol` | \(\mathcal M_0,\beta_0,h_i\in\{10^{-2},10^{-3},10^{-4},10^{-5}\}\) | report \(\mathcal R_{\rm FD}=\{\widehat\ell_2(\beta_0),G,(h_i,D(h_i),e(h_i),e_{\rm rel}(h_i)),I_\pm,K_\pm,W_i,\text{status}\}\) | P21-82--P21-87; P19-94--P19-101 | protocol | identical manifest, recomputed cores, explicit pass/fail status |

## Review Note

This ledger intentionally names would-be functions, not implemented functions.
It is a bridge from derivation to a later coding phase.
