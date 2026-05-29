# P3 Industrial Defect Calculus And Synthesis Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T/P1U/P2R source-local literature base, rewritten
chapters `ch33`--`ch37`, and `docs/main.pdf`.

what_is_not_concluded: see section "What Must Not Be Concluded".

## Purpose

P3 strengthens the high-dimensional nonlinear filtering monograph block for an
industrial panel of global-bank and central-bank model users.  The goal is not
IT governance and not academic novelty.  The goal is a defect-first
mathematical synthesis: what fails, why it fails, how it can be mitigated, when
method combinations are useful even if not novel, what numerical and
performance problems remain, and which literature supports those claims.

## Skeptical Plan Audit

This plan passes only if it avoids the previous failure modes:

- no vague industrial-relevance prose without equations, counterexamples, or
  source-local anchors;
- no production, NAWM, posterior-accuracy, HMC-convergence, GPU/XLA, or tensor
  validation claims;
- no use of citation counts, venue rank, abstracts, introductions, or metadata
  as theorem-level support;
- no hidden use of source-blocked or quarantined papers;
- no drift into DPF implementation, student-baseline, controlled-DPF, or
  production `bayesfilter/` code;
- no global "complete literature" claim while forward snowballing and some
  numerical-analysis sources remain incomplete.

## Eight Required Blocks

Each block must be represented in the rewritten synthesis chapter or in an
explicit P3 ledger/result note.

1. Full derivation gap: expand or register where current derivations remain
   proof sketches rather than full paper-level derivations.
2. MathDevMCP certification gap: record that prior MCP audits were diagnostic,
   not certified, and split new obligations where feasible.
3. Exposition depth gap: replace compact synthesis with fuller worked
   counterexamples, assumptions, derivations, and mitigation logic.
4. PDF/layout polish gap: validate PDF after rewrite and record remaining
   layout warnings separately from citation/reference blockers.
5. Industrial synthesis propositions: include propositions such as tensor
   viability only under stable ranks, transport usefulness only under target
   auditability, HMC downstream of same-scalar likelihood, and sparse-grid
   cubature as local diagnostics before global defaults.
6. Defect derivation gap: derive likely defects mathematically or through
   explicit worked examples.
7. Mitigation derivation gap: derive how the defects can be mitigated and under
   what assumptions.
8. Performance model gap: give cost and memory equations with the scaling
   variable that can kill the method.

## Source-Local Literature Map

Use source-local checked anchors where available:

- particle collapse and particle-filter baselines:
  \citet{gordon1993novel,arulampalam2002tutorial,bengtsson2008curse,snyder2008obstacles};
- pseudo-marginal and particle MCMC target distinction:
  \citet{andrieu2009pseudo,andrieu2010particle};
- Gaussian/cubature/sparse-grid competitors:
  \citet{julier1997new,arasaratnam2009cubature,jia2012sparsegrid,jia2013highdegree,singh2018adaptive};
- TT/TN rank and factor caution:
  \citet{oseledets2011tt,oseledets2010ttcross,zhao2024ttsequential,batselier2016tnkf,menzen2024tnsrkf};
- TT/PDE filtering routes:
  \citet{davis1980multiplicative,yau2000realtime,yau2008realtime,li2019ttfiltering,fox2021grid,meng2025regularity,meng2026correlated};
- triangular and ensemble transports:
  \citet{rosenblatt1952remarks,reich2013nonparametric,spantini2022coupling,ramgraber2023ensemble};
- HMC and transport-preconditioned inference:
  \citet{neal2011mcmc,hoffman2014nuts,betancourt2017conceptual,girolami2011riemann,parno2018transport,hoffman2019neutra,cui2021deep};
- DSGE/nonlinear macro context:
  \citet{herbst2015bayesian,andreasen2018pruned}.

If a desired numerical-analysis or local-particle-filter source is not
source-local checked, record it as a P3 source-risk item rather than citing it
as theorem support.

## Execution Scope

Primary rewrite target:

- `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

Supporting artifacts:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-industrial-defect-synthesis-result-2026-05-29.md`

Build/update:

- `docs/main.pdf`
- `docs/references.bib` only if citations require it.

No edit is planned for `docs/main.tex` unless the build proves the chapter is
not included.

## Chapter Rewrite Requirements

Rewrite `ch37` around these elements:

- defect calculus introduction;
- particle collapse derivation using log-weight variance and ESS behavior;
- Gaussian/cubature and sparse-grid defect examples;
- tensor-rank, positivity, normalization, and covariance-factor propositions;
- transport support/Jacobian/auditability propositions;
- HMC same-scalar and approximate-target propositions;
- numerical failure table with mitigation equations;
- performance table with cost and memory equations;
- synthesis propositions that combine methods without claiming academic
  novelty;
- literature map and remaining source-risk note;
- compact non-claims section.

The chapter must continue to read as monograph prose, not as an internal audit
memo.  Process details such as Claude iterations and validation commands belong
in the result note, not in the main mathematical flow.

## MathDevMCP Plan

Attempt diagnostic audits after the rewrite for new labels that encode:

- particle ESS/log-weight defect;
- tensor rank/factor gate;
- transport support/auditability;
- approximate-likelihood posterior perturbation;
- performance/sparse-grid local-dimension gate if extractable.

If MathDevMCP cannot certify the obligations, record the result as diagnostic
only.  Do not call the propositions machine-certified unless verified.

## Claude Review Loop

Run a read-only hostile Claude review for the plan and then for each execution
block:

1. Block A: derivation depth and MCP/formalization honesty.
2. Block B: likely defects and mathematical counterexamples.
3. Block C: mitigation derivations.
4. Block D: synthesis propositions.
5. Block E: numerical problems and mitigation equations.
6. Block F: performance model equations.
7. Block G: literature coverage/source-risk honesty.
8. Block H: PDF/layout/integration.

Each block review loops until convergence or five iterations.  On the fifth
iteration, accept only if remaining issues are minor editorial or layout issues.
Stop with a structured blocker if any major source-support, mathematical
derivation, unsupported-claim, numerical-validity, or PDF-integration defect
remains.

Claude must output `ACCEPT` or `REJECT` first.  Codex is supervisor and final
authority.

## Validation Commands

```bash
git diff --check
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
pdftotext docs/main.pdf - | rg -n "Industrial Defect Calculus|Particle collapse|Tensor rank|Transport auditability|Performance model|What Is Not Concluded"
rg -n "undefined|Citation .* undefined|Reference .* undefined|There were undefined|Rerun to get cross-references" docs/main.log
git status --short -- docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex docs/main.pdf docs/references.bib docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p3-*
```

## What Must Not Be Concluded

P3 must not conclude production readiness, NAWM readiness, tensor-method
validation, transport-method validation, posterior accuracy, HMC convergence,
GPU/XLA readiness, broad literature completeness, or machine-certified proof
validity.  It may conclude that the monograph now contains a stronger
source-local industrial defect calculus if the review and validation pass.
