# P2R Chapter Rewrite Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U accepted source-local literature base.

what_is_not_concluded: see section "What Must Not Be Concluded".

## Purpose

P2R rewrites Chapters 33--37 as a paper-first scholarly monograph block.  The
main text should explain the mathematical and algorithmic content of the
literature, not read like an internal compliance memo.  BayesFilter evidence
belongs in compact implementation-boundary notes at the end of chapters.

## Skeptical Execution Audit

The rewrite is allowed only because P1U conditionally permits a source-local
rewrite.  It must not convert unavailable originals into hidden authority.

Risks checked before execution:

- Wrong baseline: compare methods to their declared filtering/sampling problem,
  not to weak strawmen.
- Proxy metric risk: citation counts, venue rank, smoke tests, and runtime are
  not correctness evidence.
- Source risk: Savostyanov maxvol, Stroud book, Smolyak, Genz, Knothe, and
  original DMZ priority sources remain blockers unless source-local checked
  alternatives are cited precisely.
- Derivation risk: equations written in project notation need assumptions and
  proof sketches; MathDevMCP attempts are evidence of audit effort, not proof
  unless the tool certifies a scoped obligation.
- PDF risk: chapters must build in `docs/main.pdf`; undefined citations or
  unreadable tables veto acceptance.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
- `docs/chapters/ch34_highdim_gaussian_and_sparse_quadrature.tex`
- `docs/chapters/ch35_highdim_particle_transport_tensor_filters.tex`
- `docs/chapters/ch36_nonlinear_ssm_hmc_research_program.tex`
- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`
- `docs/main.tex`
- `docs/main.pdf`
- `docs/references.bib`
- `docs/source_map.yml`

## Chapter Structures

### Chapter 33: Foundations

- nonlinear discrete-time and continuous-time SSM contracts;
- filtering recursion and likelihood factorization;
- continuous-time Kushner--Stratonovich/Zakai/DMZ equations from checked
  standard sources;
- Davis multiplicative/pathwise transformation;
- Yau--Yau robust DMZ and memoryless/offline-online Kolmogorov algorithm;
- particle-collapse and exact/approximate posterior boundaries;
- compact implementation-boundary note.

### Chapter 34: Gaussian, Cubature, and Sparse-Grid Competitors

- Gaussian moment projection theorem;
- EKF/second-order EKF derivations;
- UKF/CKF/cubature rule hierarchy;
- Jia 2012 sparse-grid quadrature filtering source-local formulation;
- Jia 2013 high-degree CKF source-local formulation;
- adaptive sparse-grid Gauss--Hermite competitor;
- complexity, point-count, and failure diagnostics table;
- source blockers for Stroud/Genz/Smolyak beyond checked filtering sources.

### Chapter 35: Particle, Transport, TT, and Tensor-Network Filters

- SIR/bootstrap PF baseline and collapse propositions;
- guided/corrected proposals;
- Rosenblatt/KR/triangular transport and transport-map filtering;
- direct TT/functional TT/PR-DMZ/QTT nonlinear filtering papers;
- Zhao--Cui TT sequential learning and conditional KR bridge;
- tensor-network Kalman and tensor-network square-root Kalman distinction;
- TT rank/positivity/normalization/factor-validity diagnostics;
- compact implementation-boundary note.

### Chapter 36: HMC, Transport Acceleration, and TT/KR Bridge

- HMC potential and same-scalar value/gradient contract;
- Neal/Hoffman--Gelman/Betancourt mechanics and diagnostics;
- RMHMC from Girolami--Calderhead as geometry-aware but expensive competitor;
- Parno--Marzouk transport-map accelerated MCMC;
- NeuTra as learned transport preconditioning;
- deep inverse Rosenblatt TT and Zhao--Cui conditional KR as bridge concepts;
- algorithmic promotion ladder and no-convergence boundary.

### Chapter 37: Synthesis

- long synthesis architecture with propositions/proof sketches:
  block-local Gaussian scaffold;
  sparse-grid/high-degree cubature as local diagnostic;
  TT/TN compression for density/operator/covariance structure;
  decomposable/triangular transport for filtering/smoothing;
  transport-preconditioned HMC/NeuTra as posterior inference substrate;
  explicit approximation-composition diagnostics;
- industrial-scale failure modes and evidence needed before promotion.

## Rewrite Acceptance Gates

For each chapter:

- primary-source fidelity: every method claim maps to inspected source-local
  anchors or a blocker;
- derivation substance: major equations have assumptions and proof sketches;
- algorithm clarity: implementable method families include pseudocode;
- scaling: dimensional and memory scaling plus degeneracy diagnostics;
- industrial relevance: what breaks at NAWM-like scale, what structure could
  rescue it, and what evidence is needed;
- no internal-audit clutter: implementation evidence is compact and secondary;
- no overclaim: no NAWM readiness, HMC convergence, tensor validation,
  posterior accuracy, GPU/XLA readiness, or production default readiness.

## MathDevMCP Plan

Attempt scoped checks for:

- likelihood factorization and score identity;
- Gaussian moment projection update;
- transport change-of-variables correction;
- HMC coordinate-transform potential/gradient relation.

If a check is unsupported by the symbolic backend or too semantic for tooling,
record the limitation in the P2R result note.  Do not claim formal
certification unless the tool returns a certified success for the exact scoped
obligation.

## Claude Review Loop

After each chapter rewrite, launch Claude read-only hostile academic review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-paperfirst-ch<NN>-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded hostile academic review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude's findings.
If Claude rejects and Codex agrees, Codex rewrites and resubmits.  Maximum five
iterations per chapter.  On iteration five, accept only minor editorial issues;
stop if any major scholarly defect remains.

## PDF Integration And Final Review

- Confirm `docs/main.tex` includes ch33--ch37.
- Build `docs/main.pdf` with `latexmk`.
- Verify no undefined citations/references for the rewritten block.
- Use `pdftotext docs/main.pdf -` to confirm the chapter titles are present.
- Launch Claude final hostile review of the rewritten chapters and PDF text.
- Maximum five final iterations.

## Validation Commands

```bash
git diff --check
latexmk -pdf -interaction=nonstopmode -halt-on-error docs/main.tex
pdftotext docs/main.pdf - | rg "High-Dimensional Nonlinear Filtering Foundations|Gaussian Projection and High-Order Quadrature Filters|Particle, Transport, Tensor-Train, and Tensor-Network Filters|HMC as a Research Program|Candidate Synthesis"
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined" docs/main.log
git status --short
```

## What Must Not Be Concluded

P2R must not conclude NAWM readiness, HMC convergence, tensor-method
validation, posterior accuracy, broad GPU/XLA readiness, production default
readiness, exhaustive literature coverage, or formal theorem certification
unless directly supported by the checked source/audit artifact.
