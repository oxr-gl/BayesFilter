# P17 Zhao-Cui Full Equation Reconstruction Result

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.
- P11--P16 Zhao-Cui derivative, implementability, and annotated reconstruction artifacts.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui implementation is globally differentiable.
- No claim that the fixed-branch derivative proves exact posterior accuracy.
- No claim that BayesFilter has production TT filtering code.
- No claim that the method has been validated on BayesFilter target models.
- No default-method recommendation.

## Decision

`P17_EXECUTION_COMPLETE_WITH_CLAUDE_ACCEPT`

P17 produced a stricter annotated reconstruction of Zhao--Cui Sections 1--3 and
5 than P16.  The inventory explicitly found that P16 missed or compressed
material displayed formulas and mathematical algorithm lines, especially in
the notation/pushforward setup, TT summation and proportionality, KR map costs,
particle/path weights, variable-ordering cost arguments, and Section 5
preconditioning composition.

## Files Produced

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-plan-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-inventory-ledger-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.pdf`
- P17 section, source-support, MathDevMCP, Claude-review, discrepancy, and result ledgers under `docs/plans/`.

## Review Summary

Claude plan review: `REJECT`, then `ACCEPT`.

Claude execution review: `REJECT`, then `ACCEPT`.

Codex classified every Claude finding.  All findings were `ACCEPT`; all were
patched.  There are no unresolved Codex-Claude disagreements.

The chemistry persona in execution review iteration 2 stated that the
preconditioning density chain is now self-contained enough for the P17 standard
and that the method is plausible as a high-dimensional filtering method.

## MathDevMCP Summary

MathDevMCP was used only for narrow algebra/proof diagnostics.  It verified the
quotient algebra identity for the carried-filter derivative, but functional
log-normalizer, matrix-solve, TT mass-contraction, and KR Jacobian identities
remained outside useful tool scope.  The ledger records this as
`MCP_NARROW_CHECKS_ONLY`.

## Validation Summary

- The P17 PDF builds with `latexmk`.
- `git diff --check` was run on P17 files.
- The LaTeX log was scanned for undefined references, citation warnings, rerun
  blockers, and missing-file blockers.
- `pdftotext` was used to confirm Section 1, Section 2, Section 3, Section 5,
  fixed-branch derivative, and finite-difference material appear in the PDF.
- All P17 ledgers were checked for `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.

## Residual Gaps

- The note is still not a production implementation.
- The note is 30 pages, not a full 50--60 page textbook expansion.
- Section 4 theory and Section 6 numerical examples are not fully
  reconstructed.
- No empirical BayesFilter target-model validation has been run.

## Probability Estimate

Estimated probability that P17 passes a skeptical mixed numerical/chemistry
panel as a self-contained reconstruction sufficient to justify a minimal
implementation prototype: `0.78`.

Estimated probability that P17 is accepted as a complete final implementation
specification without further code and examples: `0.55`.

