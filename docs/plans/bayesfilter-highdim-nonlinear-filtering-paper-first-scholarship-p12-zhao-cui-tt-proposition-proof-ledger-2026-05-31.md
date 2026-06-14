# P12 Zhao-Cui TT Proposition-Proof Ledger

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, JMLR 2024.
- Cui and Dolgov, Foundations of Computational Mathematics 2022.
- P11 fixed-branch derivative note.

what_is_not_concluded:
- No exact-filter claim except under zero approximation error.
- No adaptive-code global derivative.
- No HMC readiness.

## Proposition 1

Title:
`Fixed-branch squared-TT recursion defines a normalized approximate filter`

Assumptions:
- dominated densities;
- previous approximate filter is nonnegative and normalized;
- transition and observation densities are nonnegative and measurable;
- fixed branch produces measurable \(\phi_t\);
- \(\lambda_t\ge0\), \(\int\lambda_t=1\);
- \(\tau_t\ge0\);
- \(0<\widehat z_t<\infty\).

Proof obligations:
- \(\widehat q_t=\phi_t^2+\tau_t\lambda_t\ge0\): proved.
- \(\widehat\pi_t=\widehat q_t/\widehat z_t\) is well-defined: proved from positive finite \(\widehat z_t\).
- \(\int\widehat\pi_t=1\): proved by direct division by the normalizer.
- marginal \(\widehat p_t\) is nonnegative and integrates to one: proved by Tonelli/Fubini.
- induction over time: proved.
- exact-filter recovery only when \(\widehat q_t=q_t\): proved in corollary.

Status:
`PROJECT_DERIVATION_HUMAN_REVIEWED`

## Proposition 2

Title:
`Analytical gradient differentiates the declared fixed-branch approximate likelihood`

Assumptions:
- Proposition 1 assumptions;
- all branch choices fixed;
- model densities, previous filter, coordinate maps, basis maps, core coefficients, \(\tau_t\), and \(c_t\) differentiable;
- differentiation passes through finite contractions and displayed integrals;
- fixed interpolation/least-squares systems nonsingular or declared differentiable pseudoinverse branch;
- positive normalizers.

Proof obligations:
- \(\partial_i(\log\widehat z_t-c_t)=\partial_i\widehat z_t/\widehat z_t-\partial_i c_t\): proved and MathDevMCP checked.
- \(\partial_i\widehat z_t=2\int\phi_t\partial_i\phi_t+\partial_i\tau_t\): proved under dominated/fixed-branch differentiation; human reviewed.
- TT product rule: proved by finite product rule and MathDevMCP scalar analogue checked.
- mass contraction derivative: proved by product rule through TT contractions; human reviewed.
- fixed interpolation core sensitivity: derived by differentiating \(Ag=b\); MathDevMCP scalar/matrix analogue checked.
- fixed least-squares core sensitivity: derived from normal equations; human reviewed and partially MathDevMCP checked.
- previous-filter derivative enters \(q_t\): proved through \(\partial_i\log q_t\) and \(\partial_i\log(a/\widehat z)\).
- final score formula: proved by combining the above.

Status:
`PROJECT_DERIVATION_HUMAN_REVIEWED_NOT_BROADLY_MACHINE_CERTIFIED`

Decision:
`PROPOSITIONS_STATED_AND_PROVED_IN_P12_NOTE`
