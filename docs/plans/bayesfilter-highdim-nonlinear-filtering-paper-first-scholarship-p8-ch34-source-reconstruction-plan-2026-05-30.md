# P8 Ch34 Source-Reconstruction Rewrite Plan

Date: 2026-05-30

metadata_date: 2026-05-30

seed_papers: Julier--Uhlmann 1997 unscented transform/UKF; Arasaratnam--Haykin
2009 cubature Kalman filter; Jia--Xin--Cheng 2013 high-degree CKF;
Jia--Xin--Cheng 2012 sparse-grid quadrature nonlinear filtering; Singh et al.
2018 adaptive sparse-grid Gauss--Hermite filter; P1R/P1S/P1U and P7 source
ledgers; P7 ch34 result; `ch18_svd_sigma_point.tex`; current `ch34`;
`docs/references.bib`; `.local_sources/highdim_nonlinear_filtering/`; and the
scholarly literature audit policy.

what_is_not_concluded: This plan does not conclude posterior accuracy, HMC
convergence, NAWM readiness, production readiness, default readiness, GPU/XLA
readiness, exhaustive cubature/sparse-grid literature coverage, or
machine-certified proof validity.

## Objective

Rewrite only `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex` as
a source-by-source reconstruction chapter.  The goal is not to polish the P7
survey.  The chapter must teach each method from the checked source
construction, translate it into consistent BayesFilter notation, derive the
moment formulas and the approximate likelihood-gradient contract, and explain
limitations in human language.

## Skeptical Plan Audit

The actual blocker is readability and reconstruction fidelity, not missing
tables.  A chemistry, physics, numerical-analysis, or applied-mathematics
professor should not have to decode acronyms such as UKF, CKF, high-degree CKF,
GHQF, SGQF, or ASGHF from a summary table.  Therefore P8 rejects the P7 pattern
of using broad method-family tables as the main exposition.

The likely failure modes are:

- citing a paper near a paragraph but not reproducing the paper's actual
  construction;
- using Smolyak, Stroud, Genz, Ito--Xiong, or broad Gaussian-filter history as
  hidden authority when those originals are not checked in this lane;
- presenting polynomial exactness or higher degree as posterior accuracy;
- treating adaptive sparse-grid branches as smooth HMC gradients;
- deriving the innovation score for an unnamed scalar rather than for the exact
  approximate scalar reported by the method;
- leaving "Methodological Boundary And Sources" as audit prose instead of
  readable method limitations.

The plan passes this audit only if the rewrite is source-local and derivational:
Julier--Uhlmann teaches the UT point construction; Arasaratnam--Haykin teaches
the third-degree CKF construction; Jia 2013 teaches high-degree CKF from its
Definition 3.1, Theorem 3.1, Proposition 3.1, explicit third/fifth-degree
rules, Proposition 3.2, and Remark 3.6; Jia 2012 teaches GHQ, SGQF, its
Smolyak-form construction, UKF-as-level-2 relation, and level-3 point-count
examples; Singh 2018 teaches adaptive index sets, error indicators, active/old
sets, tolerance, and adaptive branch limitations.  Unchecked originals remain
scope limits.

## Evidence Contract

Question: Can chapter 34 be made human-readable by reconstructing the checked
Gaussian/quadrature filters source by source, and can it state an analytical
approximate-likelihood gradient contract precise enough to decide HMC
admissibility?

Baseline: Current P7 `ch34`, P7 source/gradient ledgers, and the local
`ch18_svd_sigma_point.tex` gradient pattern.

Primary pass criteria:

- the chapter has exactly the requested reader-facing structure;
- each acronym is defined before it is used in tables, synthesis, or HMC labels;
- each method section follows: problem setting; original construction;
  BayesFilter notation; derivation of moment formulas; exact versus
  approximate object; running scalar example; computational cost; analytical
  gradient status; limitations/failure modes;
- citations appear at the point where checked technical results are reproduced;
- tables are compact summaries after derivations, not the main explanation;
- the "Methodological Boundary And Sources" section is removed or rewritten as
  "Limitations of These Methods" in human language;
- deterministic Gaussian quadrature gradients derive
  \(\dot\chi,\dot z,\dot{\bar z},\dot S,\dot v\), and the solve-form
  approximate innovation score;
- HMC labels are tied to a declared approximate scalar and smooth fixed branch.

Veto diagnostics:

- any method remains a short assertion paragraph;
- any table introduces unexplained terms;
- any acronym or method-specific symbol appears first in a table, synthesis row,
  or HMC label before being defined in prose or displayed math inside `ch34`;
- a source-blocked original is used as theorem support;
- source cautions are moved away from the method they affect;
- ledger-style audit prose leaks into the chapter body instead of being
  translated into reader-facing limitation sentences tied to the relevant
  method;
- adaptive sparse-grid selection is treated as a globally smooth gradient;
- posterior accuracy, HMC convergence, production readiness, NAWM readiness,
  GPU/XLA readiness, or default readiness is claimed;
- a reproduced construction lacks a nearby citation anchor to the checked
  source or a `PROJECT_DERIVATION` label;
- Claude rejects for a major readability, source-support, unsupported-claim,
  gradient, or PDF blocker after five iterations;
- `latexmk` fails or new undefined citation/reference blockers remain.

Explanatory diagnostics:

- MathDevMCP checks of narrow algebraic identities;
- layout warnings;
- Claude minor wording or table-density notes.

## Allowed Writes

- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/main.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-*`

Only if unavoidable for a broken reference may another chapter be touched; any
such change must be recorded as an exception.  Any exception is limited to
cross-reference or build repair and must not introduce substantive scholarly
claims outside `ch34`.  No such exception is planned.

Forbidden writes:

- DPF lane files;
- student-baseline or controlled-DPF files;
- production `bayesfilter/` code;
- public APIs;
- `.local_sources/`;
- unrelated dirty files.

## Source Reconstruction Scope

Every source used below must have a P8 ledger row with:

- title, authors, year, DOI/arXiv/URL when known;
- local artifact path;
- publication status;
- full-text status;
- retraction/quarantine/erratum/version-conflict status;
- inspected technical sections/equations/theorems/algorithms;
- allowed claims;
- forbidden claims;
- support class.

Allowed support classes are `PRIMARY_TECHNICAL_SUPPORT`,
`PROJECT_DERIVATION`, `SURVEY_CONTEXT_ONLY`, `SOURCE_GAP_BLOCKER`, and
`RETRACTED_OR_QUARANTINED`.  Quarantined or source-blocked papers cannot
support theorem-level or method-construction claims.

### Julier--Uhlmann UT/UKF

Use the checked 1997 source around Eq. 12--14 and the UKF prediction/update
boxes.  Reconstruct:

- sigma points \(x_0=m\), \(x_i=m+\sqrt{n+\kappa}\,C e_i\),
  \(x_{i+n}=m-\sqrt{n+\kappa}\,C e_i\);
- weights \(w_0=\kappa/(n+\kappa)\), \(w_i=1/[2(n+\kappa)]\);
- transformed mean/covariance formulas;
- the human limitation that negative \(w_0\) can damage covariance semantics.

Do not use the source to claim global nonlinear accuracy.

### Arasaratnam--Haykin CKF

Use the checked 2009 source for the third-degree spherical--radial rule and CKF
update.  Reconstruct:

- the standard Gaussian integral target;
- the CKF point set \(\pm\sqrt n e_j\) with equal weights \(1/(2n)\);
- transformation through a covariance factor;
- observation moment, innovation covariance, cross covariance, gain, and update;
- derivative-free function-evaluation cost \(2n\) plus dense linear algebra.

Do not claim CKF solves high dimensionality; the source itself separates
function-evaluation scaling from cubic dense algebra.

### Jia--Xin--Cheng High-Degree CKF

Use the checked 2013 source for:

- Definition 3.1 of a degree-\(d\) rule;
- spherical--radial decomposition;
- Proposition 3.1, combining degree-\(d\) radial and spherical rules;
- the explicit third-degree rule as CKF;
- the explicit fifth-degree rule with \(2n^2+1\) points;
- Proposition 3.2 polynomial point-count growth for fixed degree;
- Remark 3.6 negative-weight stability caveat.

Limit claims to source-local high-degree CKF.  Do not independently derive
Genz/Stroud/Cools foundations from blocked originals.

### Tensor-Product Gauss--Hermite Filtering

Use Jia 2012 Section 2.2.1 as a checked source for the GHQ construction:

- one-dimensional nodes/weights from Gaussian quadrature;
- tensor-product multi-index nodes and product weights;
- exactness up to one-dimensional polynomial degree \(2m_q-1\);
- exponential point count \(m_q^n\).

If the text gives a standard derivation, label it as a project numerical
analysis derivation or Jia-source-local reconstruction.  Do not cite blocked
Ito--Xiong as theorem support.

### Jia--Xin--Cheng SGQF

Use Jia 2012 Sections 2--3, equations (13)--(14), (26)--(30), Theorem 3.1,
Algorithm 1, propositions, appendix examples, and the paper's UKF-as-level-2
relation.  Reconstruct:

- the Gaussian approximation filter integral;
- univariate level rules and accuracy levels;
- Smolyak/source-local sparse-grid combination;
- repeated point merging and weight aggregation;
- level-3 point-count examples;
- fixed-level polynomial point growth and omitted-interaction limitations.

The broad Smolyak original remains uninspected and cannot support independent
historical or theorem claims.

### Singh et al. Adaptive SGHF

Use Singh et al. 2018 Sections 2--3:

- SGHF difference formula \(\Delta_l=I_l-I_{l-1}\);
- index set, forward/backward indices, admissibility;
- local error indicator \(g_\lambda\);
- active and old sets;
- tolerance and error-weighting parameters;
- adaptive index construction.

State that adaptive selection is computationally useful but not a globally
smooth HMC scalar unless the branch is frozen or smoothed.

## Required Chapter Structure

1. What This Chapter Computes
2. Gaussian Moment Projection
3. EKF and Second-Order Taylor Filters
4. Julier-Uhlmann Unscented Transform / UKF
5. Arasaratnam-Haykin Cubature Kalman Filter
6. Jia-Xin-Cheng High-Degree CKF
7. Tensor-Product Gauss-Hermite Filtering
8. Jia-Xin-Cheng Sparse-Grid Quadrature Filter
9. Adaptive Sparse-Grid Gauss-Hermite Filter
10. Approximate Likelihood and Analytical Gradient
11. Limitations of These Methods

## MathDevMCP Protocol

Use MathDevMCP only for narrow checks:

- derivative of \(\log\det S\);
- derivative of \(v^\top S^{-1}v\);
- scalar Gaussian innovation score specialization;
- fixed quadrature moment derivative algebra when expressible;
- simple equalities in the running scalar cell.

Record each attempt as `MCP_VERIFIED`, `MCP_UNVERIFIED`, `MCP_INCONCLUSIVE`,
`MCP_TOOL_LIMIT`, or `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`.  Do not claim
broad chapter certification.

## Claude Review Loop

Run a read-only hostile plan review before rewriting.  Claude must output
`ACCEPT` or `REJECT` first.  If Claude rejects and Codex agrees, patch and
resubmit, up to five iterations.

After the rewrite and P8 ledgers, run a read-only hostile execution review.
Review criteria:

- Can a mixed numerical professor understand the chapter linearly?
- Are the original checked source constructions reconstructed in BayesFilter
  notation?
- Are all terms defined before use?
- Are citations placed exactly where checked results are used?
- Are tables summaries only?
- Are limitations expressed in human language?
- Is the approximate likelihood-gradient derivation correct under stated
  assumptions?
- Are HMC admissibility labels honest?
- Are source blockers and quarantines respected?
- Are overclaims absent?

Loop to convergence or max five.  Accept iteration five only if remaining
issues are minor editorial/layout concerns.

## Required P8 Artifacts

Create:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-source-reconstruction-ledger-2026-05-30.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-gradient-obligation-ledger-2026-05-30.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-source-anchor-ledger-2026-05-30.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-mathdevmcp-ledger-2026-05-30.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-claude-review-ledger-2026-05-30.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p8-ch34-source-reconstruction-result-2026-05-30.md`

Each ledger must include `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

The P8 artifacts must cover the scholarly-audit ledgers required by policy:

- **source-support coverage** in the source-reconstruction ledger, one row per
  paper with full-text, quarantine, inspected-anchor, allowed-claim, and
  forbidden-claim fields;
- **claim-support coverage** in the source-anchor ledger, mapping each major
  `ch34` claim or derivation to `PRIMARY_TECHNICAL_SUPPORT`,
  `PROJECT_DERIVATION`, `SOURCE_GAP_BLOCKER`, or `RETRACTED_OR_QUARANTINED`;
- **omission-risk coverage** in the source-anchor ledger or result, especially
  Smolyak, Stroud, Genz/Cools, Ito--Xiong, van der Merwe scaled UKF, and
  Arasaratnam--Haykin--Elliott GHQ;
- **backward-snowball coverage** from each seed paper's related-work,
  introduction, and comparison sections, recorded as classified candidates or
  as inherited from P1R/P1S/P1U with P8 scope notes;
- **forward-snowball coverage** from existing OpenAlex/local metadata where
  available, or an explicit `FORWARD_SNOWBALL_BLOCKED_NO_NEW_NETWORK` note;
- **quarantine coverage**, explicitly recording that quarantined/retracted
  sources cannot support `ch34` claims.

The gradient-obligation ledger must label each analytical step
`\dot\chi,\dot z,\dot{\bar z},\dot S,\dot v`, the score formula, and
branch-smoothness condition as `PROJECT_DERIVATION`,
`PRIMARY_TECHNICAL_SUPPORT`, or `SOURCE_GAP_BLOCKER`.

## PDF And Validation Requirements

Build:

```sh
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
```

Validate:

- `git diff --check`;
- no undefined citation/reference/rerun blockers in `docs/main.log`;
- `pdftotext docs/main.pdf -` contains the new chapter sections;
- `.local_sources/` remains untracked and unstaged;
- only allowed paths are changed intentionally.

## Stop Conditions And Decision

Return `BLOCKED` if the chapter cannot be made source-local without uninspected
foundations, if the gradient derivation cannot be made honest, if Claude finds a
major unresolved blocker after five iterations, or if PDF build/citation
blockers remain.

Return `PARTIAL_READY_WITH_BLOCKERS` if source reconstruction is materially
improved but some section remains not self-contained or diagnostic-only due to
honest source/gradient limits.

Return `READY_FOR_CH34_PANEL_REVIEW_WITH_LIMITS` only if the chapter reads as a
source-reconstruction monograph chapter, the ledgers record source and gradient
support, Claude accepts or records only minor residuals, and PDF validation
passes.
