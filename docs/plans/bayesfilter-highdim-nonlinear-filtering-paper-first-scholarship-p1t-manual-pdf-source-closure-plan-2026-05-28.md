# P1T Manual PDF Source-Closure Plan

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: five user-supplied blocker PDFs in `.local_sources/highdim_nonlinear_filtering/`.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

Close the P1S source blockers for the five manually supplied PDFs by validating
local readability, inspecting technical anchors, and recording what later chapter
claims these sources can and cannot support.  This pass is source closure only:
it does not rewrite chapters, audit derivations in project notation, update the
PDF, or claim the monograph block is scholarly enough.

## Evidence Contract

Question: Do the five manually supplied PDFs close the P1S blockers for CKF,
RMHMC, high-dimensional particle-filter collapse, and the original bootstrap
particle filter?

Baseline/comparator: P1S classified these topics as source-blocked because the
technical full text had not been checked.

Pass criterion: each supplied PDF has a valid local artifact, either
machine-readable text or a documented OCR path, inspected technical anchors, and
ledger rows identifying allowed and forbidden future claims.

Veto diagnostics:

- PDF cannot be read or OCRed enough to identify technical content.
- Source identity does not match the expected title/authors/year.
- Retraction/quarantine signal is found or unresolved.
- A row attempts to use citation counts, venue rank, abstracts, or metadata as
  theorem support.
- The pass edits chapters, production code, DPF lane files, student-baseline
  files, controlled-DPF files, `docs/main.tex`, or `docs/main.pdf`.

Explanatory diagnostics:

- `pdfinfo`, `file`, `pdftotext`, `pdfimages`, `pdftoppm`, and `tesseract`
  results.
- Cached OpenAlex metadata when already present from P1S.

Artifact: P1T source, claim-support, omission-risk, and result notes under
`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*`.

## Exact Inputs

- `.local_sources/highdim_nonlinear_filtering/Cubature Kalman Filters Arasarantnam(09).pdf`
- `.local_sources/highdim_nonlinear_filtering/Riemann manifold langevin and hamiltonian monte carlo methods Girolami(11).pdf`
- `.local_sources/highdim_nonlinear_filtering/Obstacles to High-Dimensional Particle Filtering Snyder(08).pdf`
- `.local_sources/highdim_nonlinear_filtering/Curse-of-Dimensionality Revisited Collapse of the Particle Filter in Very Large Scale Systems Bengtsson(08).pdf`
- `.local_sources/highdim_nonlinear_filtering/Novel Approach to Nonlinear Non-Gaussian Bayesian State Estimation Gordon.pdf`
- P1S ledgers and result note.
- `docs/references.bib` as read-only bibliography context.
- Scholarly literature audit policy.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*`

Temporary extraction artifacts may be written under `/tmp/highdim_p1t_text`.
Do not commit or stage `.local_sources/`.

## Forbidden Writes

- Chapter files.
- `docs/main.tex` or `docs/main.pdf`.
- Production `bayesfilter/`.
- DPF implementation lane files.
- Student-baseline or controlled-DPF files.
- Downloaded PDFs or local source cache.

## Skeptical Plan Audit

Passed for this narrow pass.

- Wrong baseline risk: avoided by comparing only against P1S blocker rows.
- Proxy-metric risk: citation/venue metadata is not used as source support.
- Stop-rule risk: stop if any PDF cannot be read/OCRed or if a source identity
  mismatch appears.
- Stale-context risk: P1S artifacts and source cache are inspected before
  writing.
- Overclaim risk: result can close source blockers only; it cannot validate
  derivations, chapters, implementation, or posterior accuracy.
- PDF integration risk: out of scope and explicitly forbidden.

## Review Protocol

Claude Code is a bounded hostile reviewer only.  Codex remains final authority.

Run, if review is required:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1t-manual-pdf-source-closure-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only scholarly-literature-audit review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  If Claude rejects and Codex
agrees, patch and resubmit up to five iterations.  On iteration five, accept
only minor editorial issues; stop if any source-support, quarantine, metadata
discipline, or claim-support defect remains major.

## Validation Commands

```bash
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*
git diff --name-only -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*
git status --short .local_sources/highdim_nonlinear_filtering
rg -n "metadata_date|seed_papers|what_is_not_concluded" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*
```

## What Is Not Concluded

- The chapters are not rewritten or review-ready.
- No derivation has been audited in BayesFilter notation.
- Citation counts or venue rankings do not support technical claims.
- The supplied papers do not establish NAWM readiness, HMC convergence,
  tensor-method validation, posterior accuracy, broad GPU/XLA readiness, or
  production default readiness.
