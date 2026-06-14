# P19 Zhao--Cui Chair-Readable Gradient Result

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui filtering-scalar and gradient-feasibility ledgers.
- P15 implementable fixed-branch squared-TT specification.
- P18 true annotated Zhao--Cui companion and review ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, or changing fitting
  points.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Decision

Decision: `P19_ACCEPTED_AFTER_REVIEW_LOOP`.

P19 produced a chair-readable fixed-branch squared tensor-train gradient note
and compiled PDF.  Claude execution review iteration 1 rejected the note on two
substantive teach-back gaps.  Codex accepted the findings, patched the note, and
Claude execution review iteration 2 accepted the patched result with no
remaining findings.

## What Codex Inspected

- P19 plan and review ledger.
- P19 note source and compiled PDF.
- P19 teaching, equation, fixed-branch scalar, finite-difference, MathDevMCP,
  Claude-review, discrepancy, and result ledgers.
- Prior P10/P15/P18 artifacts as context for the declared scalar and fixed
  branch semantics.
- LaTeX log, extracted PDF text, and banned-term scans.

## Main Output

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.pdf`

The final note is 17 pages and contains 124 numbered or locally tagged
displayed equations.

## Substantive Improvements

- Clarified the fixed-branch contract: structural choices are frozen, while
  fitted core values \(C_{t,k}(\beta)\) remain parameter-dependent outputs of
  the fixed fitting equations.
- Expanded the derivation from normalizer derivative to squared approximation,
  rank-one TT, rank-\(R\) mass matrices, fixed linear solve, full design rows,
  full mass contractions, carried filter, propositions, finite differences, and
  a minimal runnable example.
- Added an entrywise derivation of the TT design row before using Kronecker
  shorthand.
- Added an explicit carried-marginal contraction and derivative recipe.
- Added a same-scalar warning for positivity floors.
- Added a finite-difference protocol that freezes structural branch choices but
  recomputes fitted core values by the same fixed fitting rule.

## Claude Review History

| Stage | Iteration | Status | Codex audit |
|---|---:|---|---|
| Plan review | 1 | `REJECT` | Accepted all four findings and patched the plan. |
| Plan review | 2 | `ACCEPT` | Agreed; no material plan blocker remained. |
| Execution review | 1 | `REJECT` | Accepted all five findings; patched the note and ledgers. |
| Execution review | 2 | `ACCEPT` | Agreed; no remaining findings. |

Codex classifications summary:

- `ACCEPT`: 9 findings.
- `PARTIAL`: 0 findings.
- `DISPUTE`: 0 findings.
- `CLARIFY`: 0 findings.

## MathDevMCP Status

Decision: `MIXED_MCP_VERIFIED_AND_TOOL_LIMIT_NO_BROAD_CERTIFICATION`.

MathDevMCP verified narrow algebraic identities for the quotient derivative,
scalar linear-solve rearrangement, and product-rule skeletons.  It did not
certify broad functional calculus obligations involving `diff(log(Z(beta)),
beta)` due to parser/tool limitations.  Those steps remain human-reviewed
derivations in the note.

## Validation Summary

Validation status: `PASS_WITH_MINOR_LAYOUT_WARNINGS`.

Commands run:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.tex`
- `git diff --check -- <exact P19 source and ledger files>`
- `rg -n "[ \t]+$" <exact P19 source and ledger files>`
- `rg -n "undefined|Undefined|Citation|Rerun|missing|Missing|Error|Overfull|Underfull" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p19-zhao-cui-chair-readable-gradient-note-2026-06-01.pdf - | rg <required section patterns>`
- banned-term scans on main note source and extracted PDF text.
- metadata-field scan over all P19 markdown files.

Results:

- PDF built successfully and is up to date.
- No trailing whitespace was found in P19 markdown or note source files.
- No banned process/governance terms were found in the main note source or PDF
  text.
- Extracted PDF text contains the required warmups, forward pass, derivative
  pass, propositions, finite-difference protocol, and minimal runnable example.
- All P19 markdown files contain `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.
- LaTeX log contains underfull table-line warnings only; no fatal errors,
  undefined references, citation warnings, rerun blockers, missing files, or
  overfull boxes were found.

## Remaining Chair-Readable Gaps

No remaining gaps were identified by Claude execution review iteration 2.
Codex residual risk: the real chair may still prefer additional numerical
figures or a worked table of actual scalar values, but that is outside P19's
derivation scope.

## Panel Probability Estimate

Estimated probability that P19 passes a skeptical mixed numerical/chemistry
panel as a derivation note: `0.83`.

Rationale: the biggest prior failure modes, design-row opacity and carried
marginal opacity, were explicitly patched and accepted by the hostile review.
The remaining weakness is that no finite-difference implementation run is
included in P19.
