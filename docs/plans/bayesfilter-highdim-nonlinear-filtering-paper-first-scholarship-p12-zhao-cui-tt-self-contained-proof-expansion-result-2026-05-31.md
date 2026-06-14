# P12 Zhao-Cui TT Self-Contained Proof Expansion Result

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

what_is_not_concluded:
- No exact posterior accuracy.
- No global analytical gradient for the adaptive Zhao-Cui companion code.
- No HMC readiness.
- No production BayesFilter implementation.
- No NAWM readiness, GPU/XLA readiness, or default-method recommendation.
- No permission to copy third-party code into production BayesFilter modules.

## Artifacts Produced

- Plan:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-plan-2026-05-31.md`
- LaTeX proof note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex`
- PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf`
- Ledgers:
  - `...p12-zhao-cui-tt-self-contained-proof-expansion-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-proposition-proof-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-source-anchor-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-source-support-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-claim-support-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-coverage-and-omission-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
  - `...p12-zhao-cui-tt-claude-review-ledger-2026-05-31.md`

## What Codex Inspected

- P12 plan.
- P10 Zhao-Cui paper-code crosswalk, filtering-scalar, gradient-feasibility,
  and reproducibility/code-audit context.
- P11 fixed-branch derivative note and ledgers.
- Local Zhao-Cui JMLR PDF.
- Local Cui-Dolgov arXiv PDF.
- Zhao-Cui audit snapshot code paths:
  `models/full_sol.m`, `SIRT.m`, `@TTSIRT/TTSIRT.m`,
  `@TTSIRT/marginalise.m`.
- Scholarly literature audit policy and Claude review template.

## Claude Review History

Plan review:
- Iteration 1: `REJECT`.
  Claude found missing scoped source-support, claim-support,
  coverage/omission, and quarantine/version ledgers.  Codex agreed and patched
  the plan.
- Iteration 2: `ACCEPT`.

Execution review:
- Iteration 1: `REJECT`.
  Claude found the PDF missing at review time, Proposition 2 too sketchy on the
  previous-filter numerator derivative, coarse source anchors in the note, and
  pending/in-progress ledger status.  Codex agreed and patched.
- Iteration 2: `ACCEPT`.

## MathDevMCP Status

Verified:
- algebraic score identity for \(\partial(\log Z-c)\);
- normalized-density derivative algebra;
- scalar product-rule analogue;
- fixed scalar interpolation sensitivity;
- scalar weighted least-squares normal-equation sensitivity form.

Tool-limited or human-reviewed:
- function-valued identity \(\partial\int\phi^2=2\int\phi\,\partial\phi\);
- full TT mass-contraction derivative.

Overall:
`NARROW_IDENTITIES_VERIFIED_BROAD_PROOF_HUMAN_REVIEWED`

## Proof Summary

Proposition 1:
The fixed-branch squared-TT recursion defines
\[
  \widehat q_t=\phi_t^2+\tau_t\lambda_t,
  \qquad
  \widehat\pi_t=\widehat q_t/\widehat z_t,
  \qquad
  \widehat p_t=\int\widehat\pi_t\,dx_{t-1}.
\]
The proof shows nonnegativity, positive finite normalization, marginal
normalization by Tonelli/Fubini, and induction over time.  Exact filtering is
recovered only if \(\widehat q_t=q_t\) at every step.

Proposition 2:
The fixed-branch scalar is
\[
  \widehat\ell_T^{TT}(\alpha)
  =
  \sum_t\{\log\widehat z_t(\alpha)-c_t(\alpha)\}.
\]
The proof derives
\[
  \partial_i\widehat\ell_T^{TT}
  =
  \sum_t
  \left[
  \frac{\partial_iR_{t,0}+\partial_i\tau_t}
       {R_{t,0}+\tau_t}
  -
  \partial_i c_t
  \right]
\]
for the direct mass-contraction branch, with TT product-rule derivatives,
mass-contraction derivatives, fixed interpolation sensitivities, fixed
least-squares sensitivities, and explicit previous-filter marginal derivative.

## Source Support Status

- Zhao-Cui JMLR source anchors are recorded by equations, algorithms,
  propositions, and section.
- Cui-Dolgov is used only for the squared inverse Rosenblatt transport
  substrate.
- Code anchors are implementation evidence only.
- The source-support ledger records public status checks and the local arXiv
  versus publisher-version caveat for Cui-Dolgov.

## Validation Commands

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.pdf - | rg -n "State-Space Filtering From First Principles|Zhao.*Cui Sequential Squared-TT Algorithm|Fixed-Branch TT Filtering Variant|Proposition 1|Proposition 2|same-scalar|What Is Not Proved|Analytical gradient differentiates"
rg -n "undefined|Rerun|Warning: Citation|Warning: Reference" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.log
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-*
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p12-zhao-cui-tt-self-contained-proof-expansion-note-2026-05-31.tex
```

Validation result:
- PDF built successfully.
- No undefined citation/reference warnings remain.
- `pdftotext` found the required sections.
- `git diff --check` passed for P12 files.
- Only a minor overfull hbox warning remains.

## Residual Gaps

- The proof is for fixed normalized \(\lambda_t\) in the final boxed score; a
  parameter-dependent defensive density requires the extra term discussed in
  Proposition 2.
- The least-squares and TT-contraction derivative are human-reviewed at the
  mathematical level, not fully machine-certified.
- The note is rigorous but dense; a future chapter-facing version should add a
  small scalar worked example before the propositions.
- HMC use still requires implementation and same-scalar finite-difference
  parity tests under branch stability.

Decision:
`P12_SELF_CONTAINED_PROOF_EXPANSION_ACCEPTED_BY_CLAUDE_AND_VALIDATED`
