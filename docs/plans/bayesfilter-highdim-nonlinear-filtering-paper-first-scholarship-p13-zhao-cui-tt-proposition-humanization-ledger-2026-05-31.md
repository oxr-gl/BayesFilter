# P13 Zhao-Cui TT Proposition-Humanization Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P12 proposition-proof ledger.

what_is_not_concluded:
- No proof of posterior accuracy.
- No global derivative of adaptive TT-cross/rank-changing code.
- No HMC readiness.

## Proposition 1 Preservation

P12 substance:
The fixed-branch squared-TT recursion defines
\[
  \widehat q_t=\phi_t^2+\tau_t\lambda_t,\qquad
  \widehat\pi_t=\widehat q_t/\widehat z_t,\qquad
  \widehat p_t=\int\widehat\pi_t\,dx_{t-1}.
\]
Under nonnegativity, measurability, normalized defensive density, and positive
finite normalizer assumptions, the output is a nonnegative normalized
approximate filter by Tonelli/Fubini and induction.

P13 humanization:
- Added a plain-language claim before the formal statement.
- Added an "objects being approximated" paragraph.
- Kept the same assumptions and proof logic.
- Added "what this gives us" and "what this does not give us" paragraphs.

Status:
`PRESERVED_AND_HUMANIZED`

## Proposition 2 Preservation

P12 substance:
The fixed-branch scalar
\[
  \widehat\ell_T^{\TT}(\alpha)=
  \sum_t\{\log\widehat z_t(\alpha)-c_t(\alpha)\}
\]
has derivative
\[
  \partial_i\widehat\ell_T^{\TT}
  =
  \sum_t
  \left[
  \frac{\partial_iR_{t,0}+\partial_i\tau_t}
       {R_{t,0}+\tau_t}
  -
  \partial_i c_t
  \right]
\]
for the direct fixed mass-contraction path, with previous-filter sensitivity
propagated recursively.

P13 humanization:
- Added a plain-language claim and implementation-path paragraph.
- Kept the same scalar and score.
- Re-derived \(\partial_i\widehat z_t\), TT product rule, mass-contraction
  derivative, interpolation sensitivity, least-squares sensitivity, and
  previous-filter sensitivity.
- Added a separate implementation recipe and parity test.

Status:
`PRESERVED_AND_MADE_MORE_IMPLEMENTABLE`

Decision:
`P12_PROPOSITION_SUBSTANCE_RETAINED_IN_P13`
