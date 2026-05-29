# P2R Chapter Rewrite Result

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U source-local literature base and rewritten
high-dimensional nonlinear filtering chapters.

what_is_not_concluded: see section "What Is Not Concluded".

## Decision

`ACADEMIC_REVIEW_PASS_WITH_RESIDUAL_SOURCE_AND_FORMALIZATION_LIMITS`

The rewritten high-dimensional nonlinear filtering block is now a
paper-first, source-local monograph artifact suitable for skeptical academic
review.  It is not a validation claim for BayesFilter, NAWM-scale filtering,
HMC convergence, tensor methods, GPU/XLA execution, posterior accuracy, or
production default readiness.

## Codex Inspection

Codex inspected:

- the scholarly literature audit skill and shared policy;
- P1R/P1S/P1T/P1U source ledgers, omission-risk updates, and preparation result;
- `.local_sources/highdim_nonlinear_filtering/` source-cache status without
  committing local PDFs or HTML snapshots;
- `docs/main.tex`, `docs/main.pdf`, `docs/main.log`, and `docs/references.bib`;
- the rewritten chapter files `ch33`--`ch37`;
- the dirty worktree to avoid unrelated DPF, student-baseline, and
  controlled-DPF files.

## Preparation Result

P1U ended as `SOURCE_LOCAL_PREPARATION_COMPLETE_WITH_BLOCKERS`.  The rewrite
was allowed only with explicit alternative-source discipline:

- Oseledets--Tyrtyshnikov TT-cross, Davis transformation, Yau--Yau robust DMZ,
  Meng PR-DMZ sparse approximation, and Rosenblatt transformation were locally
  inspected and used only within checked anchor scope.
- Savostyanov maxvol/quasioptimality, Stroud's book, Smolyak, Genz, and Knothe
  originals remain source blockers or replacement-path items.
- Spantini et al. 2016 decomposable-transport workshop paper remains
  quarantined and cannot support claims.
- Citation counts, venue rank, abstracts, metadata, introductions, and
  conclusions were not used as theorem-level support.

## Chapter Rewrite Summary

- Chapter 33 rewrites the nonlinear SSM foundations, exact filtering recursion,
  predictive likelihood/score identity, Zakai/DMZ/pathwise robust DMZ
  formulations, approximate posterior target boundary, and failure modes.
- Chapter 34 rewrites Gaussian projection, derivative filters, UKF/CKF,
  high-degree cubature, sparse-grid quadrature, adaptive Gauss--Hermite
  competitors, complexity, and source blockers.
- Chapter 35 rewrites SIR particle filters, transport-corrected proposals,
  triangular/ensemble transports, direct TT/functional TT/PR-DMZ filters,
  Zhao--Cui TT/KR sequential learning, TN Kalman, and square-root covariance
  caution.
- Chapter 36 rewrites the HMC target contract, fixed HMC/NUTS diagnostics,
  RMHMC burden, transport-map accelerated MCMC, NeuTra, and TT/KR transport
  bridge as a research program.
- Chapter 37 rewrites the synthesis architecture with propositions and proof
  sketches for Gaussian scaffolding, high-order diagnostics, transport/tensor
  layers, transport-preconditioned HMC, and industrial-scale failure questions.

BayesFilter evidence is kept in compact implementation-boundary or non-claim
sections rather than in repeated main-flow evidence boxes.

## MathDevMCP Derivation Audit Status

MathDevMCP was used for diagnostic label audits on:

- `prop:bf-hd-score`;
- `prop:bf-hd-affine-projection`;
- `prop:bf-hd-transport-correction`;
- `prop:bf-hd-jacobian-target`.

All four labels were found and parsed with line provenance, but the audits
returned `unverified` or `inconclusive` diagnostic status.  The tool requested
manual formalization, additional assumptions, or backend support for these
measure/probability/linear-algebra obligations.  Therefore the chapter proof
sketches are human-readable scholarly derivations, not machine-certified
theorems.

## Claude Review History

Preparation result review:

- Iteration 1: `REJECT`; decision language and alternative-source semantics were
  too strong.
- Iteration 2: `REJECT`; residual rewrite-authorization language and support
  classes needed tightening.
- Iteration 3/latest confirmation: `ACCEPT`; source blockers, quarantine, and
  claim-support boundaries were policy-compliant.

Chapter rewrite review:

- Iteration 1: `REJECT` overall.  Claude accepted `ch33`, `ch34`, `ch35`, and
  `ch36`, but rejected `ch37` because the Reich citation was too broad and the
  tensor-source bundle was too compressed.
- Codex agreed, narrowed Reich to deterministic ensemble-transform analysis
  updates, and split tensor-source roles across Li--Wang--Yau--Zhang,
  Fox--Dolgov--Morrison--Molteno, Zhao--Cui, Meng preprints, and TN Kalman
  square-root caution.
- `ch37` iteration 2: `ACCEPT`.

Final PDF/source review:

- Iteration 1: `REJECT`; PDF/source mismatch because `docs/main.pdf` had not
  yet been rebuilt from the current source.
- Codex rebuilt `docs/main.pdf` from `docs/main.tex`.
- Iteration 2: `ACCEPT`; the rebuilt PDF includes the rewritten block, has no
  undefined citation/reference warnings for the block, and reads as a serious
  academic monograph artifact under the stated boundaries.

## PDF Build Status

`docs/main.tex` includes the rewritten high-dimensional block.  In the current
book numbering, the source files named `ch33`--`ch37` render as Chapters
28--32 because other nonlinear chapters precede them.  This is a numbering
artifact, not a missing-PDF issue.

`docs/main.pdf` was rebuilt successfully from `docs/main.tex` with
`latexmk`.  `pdfinfo` reported 246 pages and modification time
2026-05-29 01:06:14 HKT.  `pdftotext` confirmed the rendered PDF contains the
new block titles/content, including:

- High-Dimensional Filtering Foundations;
- Gaussian Projection and High-Order Quadrature Filters;
- Particle, Transport, Tensor-Train, and Tensor-Network Filters;
- HMC as a Research Program for Nonlinear State-Space Models;
- Candidate Synthesis for Industrial-Scale Nonlinear Filtering.

The LaTeX log still contains ordinary overfull/underfull box warnings,
including table-related warnings in the broader monograph and the high-dimensional
block.  No undefined citation/reference warning was found for the rebuilt block.

## Validation Commands

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext docs/main.pdf - | rg -n "High-Dimensional|Gaussian|Particle, Transport|Tensor|HMC as|Candidate Synthesis|Industrial-Scale Nonlinear Filtering"
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references" docs/main.log
git diff --check
git diff --check -- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/main.pdf docs/references.bib docs/source_map.yml docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*
git status --short -- docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/main.tex docs/main.pdf docs/references.bib docs/source_map.yml docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-* .local_sources
```

## Files Changed In This Lane

- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.pdf`
- `docs/references.bib`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-*`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p2r-chapter-rewrite-plan-2026-05-29.md`
- this result note.

No commit was made.  The repository contains unrelated dirty DPF/student/
controlled-DPF files that were not part of this lane and must not be staged for
this task.

## Residual Gaps

- Formal proof certification remains open; MathDevMCP audits were diagnostic,
  not verified.
- Savostyanov maxvol, Stroud, Smolyak, Genz, and Knothe originals remain
  unavailable or replacement-scoped and must not be cited as checked theorem
  support.
- Recent arXiv sources are treated provisionally.
- Forward snowballing and citation/venue metadata are coverage signals, not
  truth evidence, and are not exhaustive.
- The PDF still has layout warnings, mostly ordinary overfull/underfull boxes.
- No empirical validation, BayesFilter backend promotion, NAWM readiness,
  HMC convergence, tensor validation, posterior accuracy, or production default
  readiness is concluded.

## What Is Not Concluded

This result does not conclude that any high-dimensional nonlinear filtering
method is correct for BayesFilter, NAWM-ready, production-ready, GPU/XLA-ready,
posterior-accurate, tensor-validated, or HMC-convergent.  It concludes only that
the rewritten source-local monograph block passed hostile scholarly review as a
serious academic artifact with explicit residual limits.
