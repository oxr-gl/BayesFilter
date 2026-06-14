# P3 Industrial Defect Synthesis Result

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R source-local literature base, rewritten
chapters `ch33`--`ch37`, `docs/references.bib`, and `docs/main.pdf`.

what_is_not_concluded: This result does not conclude NAWM readiness,
production readiness, posterior accuracy, HMC convergence, tensor-method
validation, transport-method validation, GPU/XLA readiness, default readiness,
machine-certified proof validity, or exhaustive literature completeness.

## Codex Inspection

Codex inspected:

- the P3 plan and ledger;
- the P2R rewrite result and prior high-dimensional literature ledgers;
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`;
- `docs/references.bib`;
- `docs/preamble.tex` for algorithm support;
- `docs/main.log`, `docs/main.pdf`, and `pdftotext` output;
- the dirty worktree status to preserve unrelated DPF, student-baseline,
  controlled-DPF, production-code, and local-source changes.

## Skeptical Execution Audit

The execution scope remained in the high-dimensional nonlinear filtering
paper-first lane.  The plan avoided DPF implementation changes, production code
edits, public API changes, GPU/CUDA work, source-blocked theorem support,
abstract-only claims, citation-count truth claims, and production-readiness
claims.  The primary risk was mistaking industrial synthesis prose for
mathematical evidence, so the chapter was organized around explicit defects,
diagnostic variables, counterexamples, propositions, proof sketches, and
performance killing variables.

## Files Changed

- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-plan-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-claude-block-review-prompt-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-result-2026-05-29.md`

No chapter files outside the high-dimensional lane were intentionally edited in
this P3 pass.  No `.local_sources/` files were staged or committed.

## Chapter Strengthening

The synthesis chapter now frames industrial use as a defect calculus rather than
as academic novelty.  It includes:

- particle collapse derivation through ESS and log-weight variance;
- a Gaussian observation worked example where log-weight variance scales with
  dimension;
- Gaussian projection and cubature limitations through a quadrature-remainder
  identity and bimodal-mixture counterexample;
- TT/TN rank, mass, positivity, likelihood, and PSD failure diagnostics;
- a covariance-rounding counterexample showing how a tiny perturbation leaves
  the PSD cone;
- transport support, Jacobian, correction, and auditability requirements;
- HMC same-scalar likelihood and value-gradient parity diagnostics;
- numerical defect and mitigation tables;
- performance models with killing variables;
- propositions for block-local Gaussian scaffolds, tensor viability,
  transport auditability, HMC downstream use, local sparse-grid diagnostics,
  and useful non-novel composition;
- a defect-first synthesis algorithm.

## Source And Claim Support

The chapter uses checked source families from the P1R/P1S/P1T/P1U/P2R ledgers:
particle-filter collapse, Gaussian/cubature/sparse-grid competitors, TT/TN
filtering routes, transport-map filtering and smoothing, transport-accelerated
MCMC, NeuTra, HMC/NUTS/RMHMC, pseudo-marginal particle MCMC, and DSGE/nonlinear
macro context.

The Spantini et al. 2016 decomposable-transport workshop paper remains
quarantined and is not used as support.  Smolyak, Stroud, Genz, Knothe,
Savostyanov-specific maxvol quasioptimality, local-particle-filter literature,
and broader finite-precision numerical-analysis sources remain scoped source
risks and are not used as hidden theorem authority.

## MathDevMCP Status

MathDevMCP was used for diagnostic audits of:

- `prop:bf-hd-particle-collapse-calculus`;
- `prop:bf-hd-tensor-viability`;
- `prop:bf-hd-transport-auditability`;
- `prop:bf-hd-hmc-downstream`.

All proposition-label audits returned `unverified` or `inconclusive`
diagnostic status.  Main reasons were manual formalization requirements,
backend-unavailable obligations, missing shape/domain assumptions for
Jacobian/log-determinant constructs, and ambiguous derivation rows that would
need splitting into narrower proof obligations.

Two bounded algebraic checks were certified by SymPy:

- `exp(2*mu + 2*v) / (exp(mu + v/2)**2) = exp(v)`;
- `1 - (1 + eps)**2 = -eps*(2 + eps)`.

These checks support local algebraic identities only.  They do not certify the
industrial propositions or the chapter derivations as formal proofs.

## Claude Review History

- Plan review `highdim-p3-industrial-defect-plan-review-iter1`: `ACCEPT`.
- Execution review iteration 1: `REJECT`.  Findings: algorithm package
  integration needed confirmation; sparse-grid scaling wording was too broad;
  the P3 ledger needed an explicit snowball and omission-risk register.
- Codex repairs after iteration 1: confirmed `algorithm` and `algpseudocode`
  are loaded in `docs/preamble.tex`; narrowed sparse-grid scaling to the
  source-local SGQF scope; added the P3 snowball and omission-risk register.
- Execution review iteration 2: `REJECT` only for Block H pending rendered
  PDF/log evidence.  Blocks A--G were accepted.
- Block H review iteration 3
  `highdim-p3-industrial-defect-blockH-review-iter3`: `ACCEPT`.  Claude
  accepted PDF/layout/integration readiness with residual layout polish risks
  only.

The review loop converged before the five-iteration cap.  No fifth-iteration
override was used.

## PDF Build Status

Command run from `docs/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Result: success.  `docs/main.pdf` exists, has 251 pages, and was rebuilt on
2026-05-29 at 02:28:25 HKT.  `pdftotext docs/main.pdf -` finds:

- `Industrial Defect Calculus`;
- `Particle Collapse`;
- `Tensor viability`;
- `Transport usefulness`;
- `same-scalar`;
- `Algorithm 9 Defect-first high-dimensional filtering synthesis`;
- `Formal And Editorial Boundaries`;
- `What Is Not Concluded`.

Log scan found no final undefined citation/reference/rerun blockers:

```bash
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
```

Remaining LaTeX warnings are layout polish issues, mainly underfull table cells
and a small overfull section heading in `ch37`, plus pre-existing warnings
elsewhere in the monograph.  They are not citation, reference, or build
blockers.

## Validation Commands

```bash
git status --short
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdfinfo docs/main.pdf
pdftotext docs/main.pdf - | rg -n "Industrial Defect Calculus|Particle Collapse|Tensor viability|Transport usefulness|same-scalar|Defect-first high-dimensional filtering synthesis|Formal And Editorial Boundaries|What Is Not Concluded"
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references|Rerun to get outlines" docs/main.log
```

Final path-scoped validation is recorded after this result note.

## Decision

`READY_FOR_USER_REVIEW_WITH_RESIDUAL_LIMITS`.

The P3 pass materially improves the industrial suitability of the synthesis
chapter: defects are named mathematically, mitigations are attached to
diagnostic contracts, performance limits are visible, and the method synthesis
is explicitly useful rather than novelty-driven.

Residual limits remain:

- the derivations are still monograph proof sketches, not full paper-length
  proofs;
- MathDevMCP did not certify the proposition obligations;
- the chapter is still compact relative to a full professor-proof treatment;
- layout warnings remain;
- source risks remain for several classical or numerical-analysis originals;
- no production, NAWM, posterior-accuracy, HMC-convergence, tensor-validation,
  transport-validation, GPU/XLA-readiness, or default-readiness conclusion is
  justified.
