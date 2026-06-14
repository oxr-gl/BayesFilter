# P13 Zhao-Cui TT Human-Readable Rewrite Result

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code-audit and source ledgers.
- P11 fixed-branch derivative note.
- P12 self-contained proof expansion note.

what_is_not_concluded:
- No posterior accuracy claim.
- No HMC readiness claim.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.
- No default-method recommendation.
- No numerical validation of TT filtering on the target high-dimensional model.

## Artifacts Produced

- Human-readable LaTeX note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex`
- Compiled PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf`
- Ledgers:
  - `...p13-zhao-cui-tt-human-readable-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-reader-comprehension-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-proposition-humanization-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-source-support-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
  - `...p13-zhao-cui-tt-discrepancy-report-2026-05-31.md`

## What Codex Inspected

- P13 human-readable plan.
- P12 proof note, proof ledger, result, and source-support context.
- P11 derivative result.
- P10 filtering-scalar ledger and companion-code audit snapshot paths.
- Scholarly literature audit skill and policy.
- Claude review template.

## Claude Review History

Plan review:
- Iteration 1: `ACCEPT`.
  Codex classified all three residual risks as `ACCEPT` and added controls:
  explicit review ledger, scoped source-support statement, and honest
  MathDevMCP ledger.

Execution review:
- Iteration 1: `REJECT`.
  Six findings: ambiguous PDF cross-references, fixed-branch pseudocode too
  compressed, scalar example not closed end to end, Proposition 2 motivation
  still thin, appendix wording too audit-like, and result/review closure
  incomplete.
  Codex classified all six as `ACCEPT` and patched the note/ledgers.
- Iteration 2: `ACCEPT`.
  Residual risks were accepted as nonblocking limitations.

## MathDevMCP Status

Narrow checks verified:
- scalar-example normalization with normalized defensive density;
- log-shift score algebra;
- normalized-density derivative algebra;
- displayed direct fixed-branch score consistency.

Overall:
`NARROW_IDENTITIES_MCP_VERIFIED_FULL_TT_PROOF_HUMAN_REVIEWED`

## Readability Changes

- The main note now derives filtering from Bayes' rule before citing papers.
- A scalar nonlinear model
  \(x_t=\rho x_{t-1}+\eta_t,\ y_t=x_t^2+\epsilon_t\)
  shows the joint object \(q_t\), the squared approximation, the defensive
  density, the normalizer, and the marginal filter.
- Tensor trains are introduced after the scalar filtering object, not before.
- Zhao-Cui is explained as a filtering recursion: form \(q_t\), fit a
  square-root TT, square and stabilize, integrate, normalize, marginalize, and
  optionally build conditional transports.
- Adaptive branch changes are explained in ordinary mathematical language.
- Code/source anchors are confined to the appendix and ledgers.

## Fixed-Branch Algorithm Expansion

The fixed-branch section now specifies:
- coordinate order, domains, bases, ranks, fitting points, solver schedule,
  defensive density, defensive mass, shift rule, and factorization branches;
- target evaluation table;
- shifted square-root target construction;
- interpolation versus weighted least-squares core solves;
- mass contraction for \(R_{t,0}\);
- normalized joint and marginal filter;
- marginal numerator and saved branch objects needed by the derivative pass.

## Proposition And Gradient Summary

Proposition 1:
The fixed-branch squared-TT recursion
\[
  \widehat q_t=\phi_t^2+\tau_t\lambda_t,\qquad
  \widehat\pi_t=\widehat q_t/\widehat z_t,\qquad
  \widehat p_t=\int\widehat\pi_t\,dx_{t-1}
\]
defines normalized nonnegative approximate filters by direct normalization,
Tonelli/Fubini, and induction.

Proposition 2:
For the declared fixed-branch scalar
\[
  \widehat\ell_T^{\TT}(\alpha)
  =
  \sum_t\{\log\widehat z_t(\alpha)-c_t(\alpha)\},
\]
the direct mass-contraction score is
\[
  \partial_i\widehat\ell_T^{\TT}
  =
  \sum_t
  \left[
  \frac{\partial_iR_{t,0}+\partial_i\tau_t}{R_{t,0}+\tau_t}
  -
  \partial_i c_t
  \right].
\]
The note gives the target sensitivity, core sensitivity, mass-contraction
sensitivity, previous-filter sensitivity, and finite-difference parity test.

## Validation

Validation commands:

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.pdf - | rg -n "What Problem Are We Solving|A Scalar Example Before Tensor Trains|The Fixed-Branch Algorithm|Why We Need Two Propositions|How To Compute The Gradient|What This Construction Gives Us|What Still Must Be Tested"
rg -n "undefined|Rerun|Warning: Citation|Warning: Reference|Overfull|Underfull" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p13-zhao-cui-tt-human-readable-note-2026-05-31.log
```

Validation result:
- PDF builds.
- Required sections appear in `pdftotext`.
- No undefined citation/reference warnings after final build.
- `git diff --check` passes for P13 artifacts.
- Auxiliary files were cleaned after final build.

## Residual Gaps

- Proposition 2 remains mathematically dense for a fresh reader, though it is
  now motivated and implementable at prototype level.
- The scalar example is illustrative; it does not fit actual TT cores or
  validate performance.
- A real BayesFilter implementation still needs model-specific basis/domain,
  rank, fitting-point, conditioning, and branch-stability choices.
- The result remains a fixed-branch derivative construction, not a global
  derivative of adaptive TT-cross/rank-changing code.

Decision:
`P13_HUMAN_READABLE_REWRITE_ACCEPTED_BY_CLAUDE_AND_VALIDATED`
