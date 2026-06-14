# P21 Zhao--Cui Finite-Difference Protocol Ledger

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- P20 integrated Zhao--Cui companion and fixed-branch gradient note.

what_is_not_concluded:
- No executable prototype claim.
- No finite-difference numerical pass claim.
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive branch choices.
- No HMC convergence claim.

## Protocol

Base parameter:
\[
\beta_0\quad\text{declared by the later implementation.}
\]

Step sizes:
\[
h\in\{10^{-2},10^{-3},10^{-4},10^{-5}\}.
\]

Branch manifest:
\[
\mathcal M_0
=
\{T,D,N,p,R,\text{domains},\text{basis},Z_{\rm fit},\rho,c_t,\tau_t,
\lambda_t,\text{sweeps},\text{seed}\}.
\]

Required identity check:
\[
\mathcal M(\beta_0-h)=\mathcal M(\beta_0)=\mathcal M(\beta_0+h)=\mathcal M_0.
\]

Recompute-core rule:
\[
C_k(\beta_0\pm h;\mathcal M_0)
=
\text{fixed fitting rule evaluated at }\beta_0\pm h.
\]
The cores must not be copied from \(\beta_0\).

Centered difference:
\[
D(h)
=
\frac{\widehat\ell_2(\beta_0+h;\mathcal M_0)
-\widehat\ell_2(\beta_0-h;\mathcal M_0)}{2h}.
\]

Errors:
\[
e(h)=|D(h)-G|,
\qquad
e_{\rm rel}(h)=\frac{|D(h)-G|}{1+|G|},
\qquad
G=\partial_\beta\widehat\ell_2(\beta_0;\mathcal M_0).
\]

Required report object:
\[
\begin{aligned}
\mathcal R_{\rm FD}
=
\{&
\widehat\ell_2(\beta_0;\mathcal M_0),
G,
(h_i,D(h_i),e(h_i),e_{\rm rel}(h_i))_{i=1}^{4},\\
&I_-(h_i),I_+(h_i),K_-(h_i),K_+(h_i),W_i,
\text{status}\}.
\end{aligned}
\]

Manifest-equality flags:
\[
I_\pm(h_i)
=
{\bf 1}\{\mathcal M(\beta_0\pm h_i)=\mathcal M_0\}.
\]

Recomputed-core flags:
\[
K_\pm(h_i)
=
{\bf 1}\{C_k(\beta_0\pm h_i;\mathcal M_0)
\text{ was recomputed by the fixed fitting rule, not copied}\}.
\]

Decreasing-window flags:
\[
W_i={\bf 1}\{e(h_i)>e(h_{i+1})>e(h_{i+2})\},
\qquad i=1,2.
\]

Pass/fail status:
\[
\text{status}
=
\begin{cases}
\texttt{FAIL\_BRANCH},&
    \min_{i,\pm}I_\pm(h_i)=0,\\
\texttt{FAIL\_COPIED\_CORES},&
    \min_{i,\pm}K_\pm(h_i)=0,\\
\texttt{PASS},&
    \max(W_1,W_2)=1,\\
\texttt{INCONCLUSIVE\_NO\_DECREASING\_WINDOW},&
    \text{otherwise}.
\end{cases}
\]

Expected pattern:

- At least one decreasing window across adjacent step sizes before roundoff.
- Failure to decrease is a diagnostic blocker for a later coding phase, not a
  scientific conclusion about Zhao--Cui.

Failure triage:

1. branch manifest mismatch;
2. copied cores instead of recomputed cores;
3. missing carried-filter derivative;
4. missing product-rule term in mass derivative;
5. wrong reference-coordinate Jacobian factor;
6. ill-conditioned ridge solve;
7. target floor or positivity convention mismatch.

## Status

Decision: `PROTOCOL_SPECIFIED_NOT_EXECUTED`.
