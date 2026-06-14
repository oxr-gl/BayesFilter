# P14 Zhao-Cui TT Gradient Teaching Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P11/P12/P13 derivative artifacts.

what_is_not_concluded:
- No global derivative of adaptive TT-cross/rank-changing code.
- No HMC readiness.
- No numerical gradient parity test has been run.

## Proposition 2 Layers

| Layer | Mathematical object | Teaching purpose | Status |
|---|---|---|---|
| A | \(\partial_i(\log\widehat z_t-c_t)=\dot{\widehat z}_t/\widehat z_t-\dot c_t\) | Reduces score to normalizer derivative. | `DERIVED` |
| B | \(\dot{\widehat z}_t=2\int\phi_t\dot\phi_t+\dot\tau_t\) | Shows why square-root TT derivative is needed. | `DERIVED` |
| C | \(\dot\phi_t=\sum_k G_1\cdots\dot G_k\cdots G_D\) | Differentiates one TT core at a time. | `DERIVED` |
| D | \(\dot R_{t,k}\) contraction recursion | Differentiates the same mass scalar used in the forward pass. | `DERIVED` |
| E | Differentiated interpolation/LS systems | Shows core sensitivities come from the same solve path. | `DERIVED` |
| F | \(\partial_i\log\widehat p_{t-1}\) via stored numerator and normalizer | Carries filter sensitivity through time. | `DERIVED` |

## Same-Scalar Control

The P14 note explicitly distinguishes:
\[
  \widehat\ell_T(\alpha;B(\alpha))
\]
from
\[
  \widehat\ell_T(\alpha;B_0).
\]
The gradient proposition applies to the fixed branch \(B_0\), not the adaptive
branch-changing value path.

Decision:
`P14_GRADIENT_TEACHING_LAYERED`
