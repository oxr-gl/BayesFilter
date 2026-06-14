# P4 Industrial Worked Example Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U source-local literature base, P2R/P3 chapter
rewrites, and P4 edited `ch37`.

what_is_not_concluded: The worked example is not NAWM validation, not client
model validation, not posterior accuracy evidence, not production readiness,
not a validated method selection, and not an empirical benchmark.

## Location

`docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`,
Section `Controlled Industrial-Style Worked Example`
(`sec:bf-hd-industrial-worked-example`).

## Example Scope

The example introduces a stylized macro-finance state
\[
  x_t=(m_t,f_t,v_t,u_t)
\]
with macro factors, financial-stress factors, latent volatility, and
measurement/survey wedges.  The nonlinear stress-cell observation is
\[
  h(x_t)=\beta^\top m_t+f_t^\top A f_t+\exp(v_t/2)u_{t,1}.
\]

This cell was chosen because it activates the exact defects discussed in the
chapters:

- Gaussian projection and innovation/factor diagnostics;
- particle log-weight variance;
- local sparse-grid active dimension;
- TT rank/mass/positivity gates;
- transport support/Jacobian gates;
- HMC same-scalar target gates.

## Claim-Support And Decision Gates

| example_component | support_class | derivation_or_source_anchor | gate | forbidden_interpretation |
|---|---|---|---|---|
| block Gaussian scaffold | `PROJECT_DERIVATION` plus Gaussian projection chapter | compute `bar y`, `S`, `C`; veto failed factorization, ill-conditioned `S`, PSD loss | numerical coherence only | not posterior accuracy |
| particle collapse diagnostic | `PROJECT_DERIVATION` plus Bengtsson/Snyder source-local warning | `Var(L) approx d_eff/(2R^2)` and lognormal factor `exp(d_eff/(2R^2))` | reject heroic unstructured particle count if factor is large | not a theorem for all particle methods |
| sparse-grid diagnostic | `PROJECT_DERIVATION` plus Jia/Singh source-local rules | active block `z_t=(f_t,v_t,u_{t,1})`, dimension `b=b_f+2` | require smooth block map and point budget `N_sg(b,l) C_h` | not global sparse-grid filter |
| TT local density gate | `PROJECT_DERIVATION` plus TT/TN source-local warnings | rank cap, mass error, positivity tolerance, likelihood/moment agreement | reject rank spike or negative density | not tensor-method validation |
| transport/HMC gate | `PROJECT_DERIVATION` plus change-of-variables/HMC sources | support, monotonicity, Jacobian, same scalar `U_z` | compare samplers only after gates pass | not HMC convergence or production evidence |

## Reviewer-Risk Controls

- The example is explicitly stylized.
- It does not name a client model.
- It does not claim NAWM readiness.
- It does not use local smoke tests as scientific validation.
- It does not use citation counts, venue rank, metadata, abstracts, or
  quarantined sources as support.
- It turns method selection into defect scoping: stop, localize, correct, or
  fall back before comparing speed.

## Residual Limitations

The example is analytically useful but not calibrated.  It has no data, no
posterior reference, no benchmark ladder, no production implementation, and no
institution-specific model evidence.  A future empirical program would need a
separate evidence contract, controlled references, and validation artifacts.
