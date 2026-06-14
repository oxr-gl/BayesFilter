# P30 Algorithm 5(c.2) Expansion Result

metadata_date: 2026-06-03

target_document: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Rosenblatt, "Remarks on a Multivariate Transformation," Annals of Mathematical Statistics 1952.

what_is_not_concluded:
- P30 does not certify every equation in the 105-page note.
- P30 does not prove empirical accuracy, production readiness, or differentiability of the adaptive Zhao--Cui algorithm.
- MathDevMCP verified only narrow scalar cancellations, not the full block-triangular change-of-variables proof.

## Decision

P29-I001 is closed as `PATCHED_AND_PASSED_TARGETED_AUDIT`.

post_feedback_patch_status: `TT_FIRST_PRINCIPLES_WORKED_EXAMPLE_ADDED`

basis_objection_patch_status: `EXPANDED_BASIS_SELECTION_DEFENSE_ADDED`

The P30 note expands Zhao--Cui Algorithm 5(c.2)'s retained physical marginal derivation and adds two final clarifications after hostile review:

- the conditional identity is the conditional KR transport for the old-state block;
- the denominator in the final retained formula is the retained reference marginal \(\eta_A(T_A(a))\), not the full three-block reference density.

After preliminary panel feedback that Section 8, "Tensor Trains From First
Principles," was too abstract, the note was patched with a fully worked
three-variable exponential example and an explicit least-squares core-regression
trace:

- target \(h(x,y,z)=\exp\{\alpha xy+\beta yz\}\), which is coupled but has chain
  interaction structure;
- truncated Taylor edge factors \(E_{12}^{(M)}E_{23}^{(M)}\);
- explicit TT cores \(H_1,H_2,H_3\) with ranks \(R_1=R_2=M+1\);
- numerical multiplication for \(M=2\), \(\alpha=1/2\), \(\beta=-1/3\),
  \((x,y,z)=(2,1/2,-1)\);
- first-order \(M=1\) least-squares row
  \(A_{j,2}[a,\ell,b]=L_j[a]y_j^\ell R_j[b]\);
- a cross-reference from the later least-squares fitting section back to the
  worked example.

After additional panel feedback that the method seemed to depend heavily on an
unexplained basis choice, the note was patched with a long reader-facing section
`How Basis Families Are Chosen, Tuned, And Audited`:

- defines the approximation design tuple
  \((\Psi,T,\mathcal B_{1:D},p_{1:D},R_{0:D},Z_{\rm fit},W,\rho,S_{\max})\);
- states explicitly that no universal optimal basis theorem is being claimed;
- explains basis families by support, measure, and regularity: Legendre/Chebyshev,
  Hermite/polynomial chaos, Fourier, piecewise/spline/wavelet, and pilot-trained
  dictionaries;
- gives a deterministic basis-degree ladder with training and holdout residuals;
- adds evidence-stability, marginal-projection, conditioning, coefficient-stability,
  and rank-saturation diagnostics;
- explains how learned bases can be used only after being frozen for the
  fixed-branch derivative;
- adds supporting bibliography entries for approximation theory, polynomial chaos,
  wavelets, dictionary learning, and sparse/low-rank approximation.

## What Codex Inspected

- P29 unresolved item `P29-I001`.
- Zhao--Cui Section 5.4 and Algorithm 5(c.2) in the local PDF.
- P30 Algorithm 5(c.2) derivation around `eq:p30-c2-0`--`eq:p30-c2-11` and `eq:p24-p16`--`eq:p24-p17`.
- P30 source, MathDevMCP, and Claude review ledgers.

## Claude Review History

| iteration | result | Codex action |
|---|---|---|
| 1 | No blocker or major finding. One minor denominator-notation finding and one conditional-KR readability note. Claude disposition: `PATCHED_AND_PASSED`. | Codex classified both as `ACCEPT` and patched the P30 note. |
| 2 | Post-patch review confirmed both prior findings were addressed and no new blocker or major issue was introduced. | Codex independently agreed and closed the targeted review loop. |

## MathDevMCP Status

mathdevmcp_status: `NARROW_SUPPORT_ONLY`

Verified:
- `(nu/eta)*rhoA/etaA*eta = rhoA*nu/etaA`;
- `nuA/etaA*rhoA = rhoA*nuA/etaA`;
- `q/rho*eta*rho/eta = q`.

Not verified by MathDevMCP:
- the full conditional KR transport argument;
- source fidelity of every equation in the note.

## Validation

Commands run:
- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `rg -n "Citation .*undefined|Reference .*undefined|undefined citations|No file|Label\\(s\\) may have changed|Rerun|Package natbib Warning|There were undefined" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf /tmp/p30_pdf.txt`
- `rg -n "retained reference marginal|conditional KR transport|source formula in Algorithm 5\\(c\\.2\\)|perfect residual|ordinary marginalization" /tmp/p30_pdf.txt`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf /tmp/p30_pdf_after_tt_example.txt`
- `rg -n "Fully Worked Three-Variable Exponential|not separable|1105|least-squares core regression|first-order truncation|ordinary problem of choosing the middle-core" /tmp/p30_pdf_after_tt_example.txt`
- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `rg -n "Citation .*undefined|Reference .*undefined|undefined citations|undefined references|No file|Label\\(s\\) may have changed|Rerun|Package natbib Warning|There were undefined" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf /tmp/p30_basis_defense.txt`
- `rg -n "How Basis Families Are Chosen|No universal optimal basis|Basis degree is tuned|Mass, evidence, and marginal|Can the basis be learned|declared, tested, and rejectable|polynomial chaos|wavelets|pilot dictionary" /tmp/p30_basis_defense.txt`
- `git diff --check`
- `git status --short docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30* docs/chapters bayesfilter`

Validation result:
- PDF builds successfully: 112 pages after the basis-defense patch.
- No undefined citation, undefined reference, missing-file, or rerun-blocker warning was found.  The log scan matched only the `rerunfilecheck` package banner.
- `git diff --check` passed.
- Extracted PDF text contains the retained-reference and conditional-KR clarifications, plus the new three-variable exponential TT example and least-squares row trace.
- Extracted PDF text contains the new basis-selection defense, including the no-universal-optimum statement, basis-family taxonomy, degree ladder, mass/evidence/marginal checks, learned-basis discussion, and rejectability policy.
- Scoped git status shows only P30 files under `docs/plans/`; no chapter or production `bayesfilter/` file was changed in this P30 lane.

## Files Created Or Changed

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-zhao-cui-alg5c2-expanded-note-2026-06-03.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-expansion-plan-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-source-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-mathdevmcp-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-claude-review-ledger-2026-06-03.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p30-alg5c2-result-2026-06-03.md`
- `docs/references.bib`

## Remaining Gaps

- The Algorithm 5(c.2) retained marginal derivation has targeted clearance, but the whole P30 note should still be treated as a long mathematical document requiring final human proofreading before submission.
- The derivation assumes the lower-triangular conditional KR construction is valid for the bridge approximation and that the relevant densities are positive on the evaluated support.
- The result does not add empirical large-scale validation beyond the existing P27 validation section.
