# P11 Zhao-Cui TT Analytical Derivative Result

metadata_date: 2026-05-30

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports."
- Zhao-Cui companion code audit snapshot at `third_party/audit/zhao_cui_tensor_ssm_p10/source`.

what_is_not_concluded:
- No complete analytical derivative for the adaptive stochastic companion code.
- No HMC readiness.
- No production BayesFilter implementation.
- No posterior accuracy or paper-figure replication.
- No default-method recommendation.
- No permission to copy third-party code into production modules.

## Artifacts Produced

- Plan:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-plan-2026-05-30.md`
- LaTeX note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex`
- Compiled PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.pdf`
- Derivation ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-derivation-ledger-2026-05-30.md`
- MathDevMCP ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-mathdevmcp-ledger-2026-05-30.md`
- Claude review ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-claude-review-ledger-2026-05-30.md`

## Plan And Review

Claude plan review:
`ACCEPT`

Claude execution review:
`ACCEPT`

Claude's minor execution risks were:
- the local TT update sensitivity is still abstract until a concrete frozen
  BayesFilter core-construction branch is selected;
- a future implementation must choose the direct mass-contraction scalar or
  the QR-contraction companion-code scalar and differentiate that same value
  path;
- regularity assumptions needed explicit statement.

Codex patched the note to add explicit regularity assumptions.

## MathDevMCP Status

MathDevMCP verified:
- algebraic score form \(\partial_i(\log Z-c)=\dot Z/Z-\dot c\);
- scalar product-rule form;
- normalized-density derivative \(\dot(q/Z)=(\dot q Z-q\dot Z)/Z^2\).

MathDevMCP was inconclusive for the function-valued squared-density
normalizer derivative because the SymPy backend could not encode the callable
integral obligation.

Overall status:
`HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

## Main Derivation Result

For a fixed branch of the Zhao-Cui squared-TT/SIRT sequential filter, the
declared scalar is
\[
  \widehat\ell_T^{\rm TT}(\alpha)
  =
  \sum_{t=1}^T\{\log\widehat z_t(\alpha)-c_t(\alpha)\}.
\]

If the square-root TT is
\[
  \phi_t(r)=G_{t,1}(r_1)\cdots G_{t,D}(r_D),
\]
and \(R_{t,0}\) is the direct mass-matrix contraction of \(\phi_t^2\), then
\[
  \partial_i\widehat\ell_T^{\rm TT}
  =
  \sum_{t=1}^T
  \left[
  \frac{\partial_i R_{t,0}+\partial_i\tau_t}{R_{t,0}+\tau_t}
  -
  \partial_i c_t
  \right].
\]

The derivative of \(R_{t,0}\) is computed by differentiating the TT cores and
propagating those sensitivities through the same mass-matrix contractions used
for the normalizer.

## Same-Scalar Boundary

The note keeps the companion-code scalar `log(sirt.z)-const`.  If a future
implementation fixes the numerical value of `const`, differentiates the direct
mass contraction instead of the QR contraction, or changes the defensive term,
it must rename the scalar and run value-gradient parity checks against that
new scalar.

## Adaptive-Code Boundary

The result does not differentiate:
- changing TT-cross interpolation sets;
- rank adaptation;
- SVD/QR branch changes;
- random enrichment or debug samples;
- ESS-triggered reapproximation;
- nonunique minimizers for `const`;
- full companion code as an HMC-ready backend.

## Validation Commands

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.tex
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-analytical-derivative-note-2026-05-30.pdf - | rg -n "Fixed-Branch Analytical Derivative|log|sirt|Final Score|What Is Not Derived|same-scalar|adaptive"
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p11-zhao-cui-tt-* third_party/audit/zhao_cui_tensor_ssm_p10
```

Validation result:
- PDF compiled successfully.
- `pdftotext` confirmed the scalar, final score, and non-derived adaptive
  boundary are present.
- `git diff --check` reported no whitespace errors.
- Root-level accidental LaTeX byproducts from the first compile were removed.

Layout warnings:
- The standalone note has minor overfull/underfull box warnings caused by long
  monospaced paths and code symbols.  These are layout warnings, not derivative
  blockers.

Decision:
`FIXED_BRANCH_ZHAO_CUI_TT_ANALYTICAL_DERIVATIVE_DERIVED_AND_REVIEWED`
