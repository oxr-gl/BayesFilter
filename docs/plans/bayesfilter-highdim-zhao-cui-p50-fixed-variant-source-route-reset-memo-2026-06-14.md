# BayesFilter Zhao-Cui P50 Fixed Variant Source-Route Reset Memo

Date: 2026-06-14

## Scope

Documented the HMC-facing fixed variant of the Zhao-Cui source route in
`docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`.
The target section is `Source-Route Fixed Variant For HMC-Facing Use`.

## Main Change

The fixed branch is now written as a proposition/proof-style adaptation of the
author route.  It defines a branch tuple \(B_t\), the source-scale density
\[
q_{t,\mathrm{src}}^B=\phi_t^2+\tau_t\lambda_t,
\qquad
\zeta_t^B=\int q_{t,\mathrm{src}}^B,
\]
and the unshifted evidence-scale density
\[
\overline q_t^B=e^{-c_t}q_{t,\mathrm{src}}^B,
\qquad
\overline Z_t^B=e^{-c_t}\zeta_t^B.
\]
The per-step log evidence is therefore
\[
\log \overline Z_t^B = \log \zeta_t^B - c_t.
\]

The defensive mass convention is explicit: \(\tau_t\) is source-scale.  The
unshifted defensive mass is \(e^{-c_t}\tau_t\).  If a variant instead wants to
hold an unshifted mass \(\overline\tau_t\) fixed, it must pass
\(e^{c_t}\overline\tau_t\) into the SIRT route.

## Source Anchors

Author code anchors cited in the document:

- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:21--68`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/full_sol.m:84--124`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/models/computeL.m:24--47`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/marginalise.m:81--85`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/AbstractIRT.m:352--354`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/Options/TTOption.m:40--92`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/deep-tensor.dev/src/@TTSIRT/TTSIRT.m:238--247`
- `third_party/audit/zhao_cui_tensor_ssm_p10/source/eg3_sir/mainscript.m:14--55`

Paper anchors cited in the document: Zhao and Cui Eq. (13),
Proposition 2/Eq. (14), Algorithm 2, and Section 3.2.

## Author Versus Fixed Variant

The document now separates:

- `source_faithful`: pushed target route, affine recentering/determinant
  convention, shifted square-root target, squared-plus-defensive density, and
  `log(sirt.z)-const` normalizer accounting.
- `fixed_hmc_adaptation`: deterministic or seeded fit samples, frozen frame,
  recorded shift, fixed ranks, fixed initialization, fixed sweep order, fixed
  ridge, and saved branch fields.

The document explicitly says this is not adaptive MATLAB parity.  The author
uses adaptive sampling, ESS guards, recentering, rank caps, enrichment, and
multiple ALS iterations because the posterior support and low-rank structure are
not known in advance; those mechanisms are practical numerical safeguards for
constructing an adequate approximation.  The fixed variant freezes the realized
choice mechanism so repeated HMC-facing evaluations refer to one scalar.

## Audits Run

Claude Opus max-effort final acceptance check:

- Result: `ACCEPT`.
- Scope: target file only; checked shared \(e^{-c_t}\) placement for fitted and
  defensive terms, and absence of source-scale \(\tau_t/\widehat Z_t\) or
  \(\tau_t/\overline Z_t\) fixed-branch normalizer mistakes.

Local scans:

- No fixed-branch source-scale `tau_t / widehat Z` or `tau_t / overline Z`
  matches in the target file.
- The broad mixed-scale scan only found bracketed corrected forms:
  `\widehat Z_t=e^{-c_t}(R_t+\tau_t)` and
  `\overline q_t=e^{-c_t}(\phi_t^2+\tau_t\lambda_t)`.

MathDevMCP:

- Label lookup found the target labels in the intended file.
- `audit_derivation_v2_label` for the new propositions returned
  `unverified`, with no concrete mismatch.  The remaining status is manual
  formalization/backend limitation, including conservative log-determinant
  domain diagnostics.  The proposition now explicitly assumes \(L_t\) is a
  square nonsingular Cholesky-style frame with finite \(\log|\det L_t|\).

LaTeX:

- Command:
  `latexmk -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.tex`
- Exit status: 0.
- Output: `bayesfilter-highdim-zhao-cui-p50-chapter-discipline-rewrite-2026-06-12.pdf`.
- Caveat: BibTeX was vetoed because `../references.bib` is not found from the
  repo-root invocation; citations remain unresolved.  There are also existing
  overfull/underfull box warnings, especially around wide tables.

## Nonclaims

This artifact does not claim:

- adaptive MATLAB parity;
- rank adequacy or convergence of a fixed rank ladder;
- HMC readiness;
- complete formal proof certification;
- source-faithfulness for any new code not separately checked against paper and
  author-source anchors.

## Next Step

If moving from document to implementation, implement only the documented
`fixed_hmc_adaptation` route and preserve the source-scale/evidence-scale
normalizer split in code tests before using any fixed branch in sampler-facing
experiments.
