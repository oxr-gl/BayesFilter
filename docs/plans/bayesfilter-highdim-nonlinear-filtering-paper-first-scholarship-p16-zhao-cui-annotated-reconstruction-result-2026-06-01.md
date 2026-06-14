# P16 Zhao-Cui Annotated Reconstruction Result

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit, paper-code crosswalk, filtering-scalar, reproducibility, and gradient-feasibility ledgers.
- P15 fixed-branch implementability specification and two-step reference example.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui implementation has a globally smooth analytical gradient.
- No claim that the fixed-branch derivative proves exact posterior accuracy.
- No claim that the method is production-ready in BayesFilter.
- No claim that high-dimensional performance has been validated on the target BayesFilter model.
- No default-method recommendation.

## Decision

`P16_EXECUTION_COMPLETE_WITH_CLAUDE_ACCEPT`

The P16 workflow produced a standalone reader-facing annotated reconstruction
of Zhao--Cui tensor-train sequential filtering, plus a fixed-branch approximate
filter and same-scalar derivative derivation.

## Artifacts Produced

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p16-zhao-cui-annotated-reconstruction-note-2026-06-01.pdf`
- P16 source-support, equation-by-equation, BayesFilter translation, code-crosswalk, fixed-branch, gradient-derivation, literature-audit, MathDevMCP, Claude-review, discrepancy, and result files under `docs/plans/`.

## Content Summary

The note follows Zhao--Cui Sections 1--3 and 5 in order, with selected support
from Section 4, Section 6, Appendix A, and checked companion-code paths.  It
reconstructs the state-space learning tasks, exact recursive bottleneck, tensor
train representation, squared-TT nonnegativity mechanism, defensive reference
term, mass-matrix marginalization, conditional density ratios, KR maps,
forward correction, backward smoothing, preconditioning, and implementable
branch objects.

The fixed-branch part declares the shifted convention
\[
    \phi_t(z;\beta)\approx e^{c_t/2}\sqrt{\widetilde q_t(z;\beta)},\qquad
    \widehat q_t(z;\beta)=e^{-c_t}\phi_t(z;\beta)^2+\tau_t\lambda_t(z),
\]
and the approximate evidence increment
\[
    \widehat Z_t(\beta)=e^{-c_t}\int\phi_t(z;\beta)^2\,dz+\tau_t .
\]
The final patch made the two-step executable value path use the same convention
for both steps, removing the last same-scalar ambiguity found by Claude.

## Review Summary

Claude plan review: `REJECT`, then `ACCEPT`.

Claude execution review: `REJECT`, `REJECT`, `REJECT`, then `ACCEPT`.

Codex independently audited every Claude finding.  Accepted or partially
accepted findings were patched.  There are no unresolved Codex-Claude
disagreements.

## MathDevMCP Summary

MathDevMCP was used only for narrow algebraic diagnostics.  Functional
TT/filtering identities exceeded the tool's useful symbolic scope, so the
ledger records `MCP_INCONCLUSIVE`, `MCP_UNVERIFIED`, and
`HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED` rather than broad certification.

## Validation Summary

- Standalone PDF build succeeded with `latexmk`.
- No undefined-reference, citation-warning, label-change, or rerun-blocker hits were found in the P16 LaTeX log.
- `pdftotext` confirmed the PDF contains the shifted-convention and two-step value-path material.
- `git diff --check` was run on P16 files after the final patch.

## Residual Gaps

- The note is substantially more self-contained than P13--P15, but it is still 24 pages rather than a 50--60 page annotated textbook treatment.
- It does not include a production implementation.
- It does not empirically validate Zhao--Cui TT filtering on the target BayesFilter model.
- It proves normalized approximate filtering and same-scalar fixed-branch differentiation for the declared branch, not exact posterior correctness.

## Probability Estimate

Estimated probability that the P16 note, as a standalone planning artifact,
passes a skeptical mixed numerical/chemistry panel for "clear enough to justify
a next implementation prototype": `0.70`.

Estimated probability that the same panel accepts it as a complete final
implementation specification without further code and examples: `0.45`.

