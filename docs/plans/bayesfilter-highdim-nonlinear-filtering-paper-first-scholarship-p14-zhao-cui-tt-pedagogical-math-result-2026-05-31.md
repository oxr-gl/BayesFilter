# P14 Zhao-Cui TT Pedagogical Mathematical Rewrite Result

metadata_date: 2026-05-31

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10/P11/P12/P13 BayesFilter Zhao-Cui artifacts.

what_is_not_concluded:
- No posterior accuracy.
- No HMC readiness.
- No global derivative of adaptive TT-cross/rank-changing code.
- No production BayesFilter implementation.
- No numerical validation on the target high-dimensional model.

## Artifacts Produced

- Plan:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-plan-2026-05-31.md`
- Pedagogical mathematical note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex`
- Compiled PDF:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf`
- Ledgers:
  - `...p14-zhao-cui-tt-pedagogical-math-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-reader-panel-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-gradient-teaching-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-source-support-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-mathdevmcp-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-claude-review-ledger-2026-05-31.md`
  - `...p14-zhao-cui-tt-discrepancy-report-2026-05-31.md`

## What Codex Inspected

- P13 note/result/ledgers.
- P12 proof and source-support context.
- P11 derivative result.
- P10 filtering-scalar context.
- Scholarly literature audit skill and policy.
- Claude review template.

## Claude Review History

Plan review:
- Iteration 1: `REJECT`.
  Seven findings on source discipline, audience criteria, math-without-teaching
  veto, MCP boundary, review closure, validation, and skeptical audit.  Codex
  classified all seven as `ACCEPT` and patched the plan.
- Iteration 2: `ACCEPT`.

Execution review:
- Iteration 1: `REJECT`.
  Claude found equation labels resolving to section numbers, breaking
  mathematical navigation.  Codex classified all findings as `ACCEPT` and
  patched the note so displayed formulas are numbered.
- Iteration 2: `ACCEPT`.

## MathDevMCP Status

Verified:
- log-shift score identity;
- normalized-density derivative algebra;
- normalized defensive-density scalar \(A+\tau\cdot1=A+\tau\).

Unverified by tool but human-derived:
- generic fixed interpolation derivative submitted to MCP.

Overall:
`P14_NARROW_SCALAR_IDENTITIES_VERIFIED_TT_AND_SOLVE_DERIVATIONS_HUMAN_REVIEWED`

## Main Pedagogical Changes

- Section 3 now teaches TT as low-rank coupling:
  \(F_{ab}\approx\sum_\ell U_{a\ell}V_{\ell b}\), then the three-coordinate
  chain, then functional TT notation.
- Sections 4--11 follow math-first structure: displayed object, worked step,
  prose explanation, and mathematical failure mode.
- Proposition 2 is decomposed into Layers A--F before the formal proposition:
  scalar derivative, normalizer derivative, TT product derivative, mass
  contraction derivative, core-solve derivative, and previous-filter
  sensitivity.
- The algorithmic gradient recipe references distinct numbered equations after
  the numbering fix.
- Source claims are labeled as `PAPER_EXPLICIT`, `DERIVED_IN_NOTE`, or
  `IMPLEMENTATION_INTERPRETATION`.

## Validation Commands

```text
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex
latexmk -cd -c docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.tex
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-*
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf - | rg -n "Tensor Trains As Low-Rank Coupling|Proposition 2 In Layers|Algorithmic Gradient Recipe|What The Construction Gives"
pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.pdf - | rg -n "Layer A|Layer B|Layer C|Layer D|Layer E|Layer F|Why this matters|Failure mode"
rg -n "undefined|Rerun|Warning: Citation|Warning: Reference|Overfull|Underfull" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p14-zhao-cui-tt-pedagogical-math-note-2026-05-31.log
```

Validation result:
- PDF builds.
- Required headings and Layers A--F appear in `pdftotext`.
- Cross-reference blocker repaired; equation labels now resolve to unique
  equation numbers.
- `git diff --check` passed for P14 artifacts.
- Auxiliary files cleaned after final build.

## Residual Gaps

- Audience-fit is still proxy-validated rather than tested with an actual
  chemistry/physics reader.
- Proposition 2 remains mathematically substantial, although it is now layered
  and navigable.
- The note teaches and proves the fixed-branch construction; it does not
  implement or numerically validate the method.
- The result does not differentiate adaptive TT-cross/rank-changing code.

Decision:
`P14_PEDAGOGICAL_MATH_REWRITE_ACCEPTED_BY_CLAUDE_AND_VALIDATED`
