# P1T Manual PDF Source-Closure Result

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: Arasaratnam--Haykin CKF; Girolami--Calderhead RMHMC; Snyder et al. high-dimensional PF obstacles; Bengtsson--Bickel--Li PF collapse; Gordon--Salmond--Smith bootstrap particle filter.

what_is_not_concluded: see section "What Is Not Concluded".

## Decision

`PARTIAL_READY_WITH_REDUCED_BLOCKERS`

The five manually supplied PDFs are visible, valid enough for local inspection,
and now close the P1S source blockers for:

- Arasaratnam--Haykin CKF;
- Girolami--Calderhead RMHMC;
- Snyder et al. high-dimensional PF obstacles;
- Bengtsson--Bickel--Li high-dimensional PF collapse;
- Gordon--Salmond--Smith original bootstrap particle filter, with an OCR caveat.

This is not yet `READY_FOR_CHAPTER_REWRITE` because other P1S risks remain:
TT-cross/maxvol, robust/pathwise DMZ, broad Smolyak/Stroud/Genz foundations,
Rosenblatt/Knothe historical foundations, incomplete forward snowballing, and
MathDevMCP derivation audits.

## Codex Inspection

Codex inspected:

- scholarly literature audit policy and Codex skill;
- P1S source, claim-support, citation/venue, omission-risk, and result files;
- `docs/references.bib` entries for the supplied papers;
- `.local_sources/highdim_nonlinear_filtering/`;
- local PDF metadata using `pdfinfo`;
- text extraction using `pdftotext -layout`;
- OCR feasibility for Gordon--Salmond--Smith using `pdfimages`, `pdftoppm`, and
  `tesseract`;
- selected technical sections/equations/algorithms/propositions in the five
  papers.

## Skeptical Execution Audit

Passed with constraints.

- The pass compares only against P1S blocker rows.
- Source closure is not treated as derivation validation.
- Cached metadata is not used as theorem support.
- The Gordon source is OCR-based and therefore requires visual checking before
  exact formula quotation.
- No chapter, production, DPF, student-baseline, controlled-DPF, `docs/main.tex`,
  or `docs/main.pdf` edits are part of this pass.

## Source-Support Status

Closed:

- `Cubature Kalman Filters Arasarantnam(09).pdf`: valid 16-page PDF; text
  extracted; CKF equations, spherical-radial cubature derivation, CKF algorithm,
  and SCKF algorithm anchors checked.
- `Riemann manifold langevin and hamiltonian monte carlo methods Girolami(11).pdf`:
  valid 92-page PDF; text extracted; MMALA/RMHMC Hamiltonian, metric, and
  generalized-leapfrog anchors checked.
- `Obstacles to High-Dimensional Particle Filtering Snyder(08).pdf`: valid
  12-page PDF; text extracted; PF update, log-likelihood variance `tau^2`,
  maximum-weight collapse heuristic, and conclusion caveats checked.
- `Curse-of-Dimensionality Revisited Collapse of the Particle Filter in Very Large Scale Systems Bengtsson(08).pdf`:
  valid 19-page PDF; text extracted; importance weights, Lemma 3.1,
  Propositions 3.2--3.4, Proposition 4.1, and discussion checked.
- `Novel Approach to Nonlinear Non-Gaussian Bayesian State Estimation Gordon.pdf`:
  valid 7-page scan-only PDF; OCR performed; recursive Bayesian equations,
  bootstrap prediction/update/resampling, weighted-bootstrap justification, and
  sample-impoverishment caveats checked with OCR caveat.

## Metadata/Citation/Venue Coverage

No live metadata refresh was run in P1T.  Existing P1S cached OpenAlex metadata
remains usable only as dated coverage context, not technical support.

- Snyder exact cached OpenAlex row records 700 citations and `is_retracted=false`
  as of the P1S metadata date, but the P1T source closure relies on the local
  PDF, not the count.
- Arasaratnam and Girolami cached OpenAlex searches were noisy in P1S; P1T
  closes source support from local PDFs, not from metadata counts.
- Gordon and Bengtsson live citation metadata was not refreshed in P1T.
- Venue ranking was not queried.

Per-paper metadata status is recorded in:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-citation-venue-metadata-ledger-2026-05-28.md`

## Quarantined Papers

Unchanged:

- Spantini et al. 2016, "Decomposable Transport Maps for Bayesian Filtering and
  Smoothing": remains `RETRACTED_OR_QUARANTINED` from the prior user report and
  cannot support claims.

## MathDevMCP Use

MathDevMCP was not used in P1T.  This pass checked primary-source anchors only.
The later chapter rewrite must write the derivations in BayesFilter notation and
then use MathDevMCP where feasible for equation/proof-obligation audits.

## Claude Review History

- Iteration 1: `REJECT`. Claude found five substantive issues: abstract text
  was listed as a Snyder support anchor; two non-policy support-class variants
  were used; per-paper metadata fields were under-specified; integrity checks
  did not separately record retraction/erratum/version/publisher-local scope;
  and one synthesis recommendation was overstated as primary support.
- Codex agreed and repaired the artifacts by removing abstract support,
  normalizing support classes, adding a P1T citation/venue metadata ledger,
  adding per-paper integrity-check subfields, and downgrading the synthesis row
  to `SURVEY_CONTEXT_ONLY`.
- Iteration 2: `ACCEPT`. Claude found the repaired artifacts acceptable for
  this narrow local-PDF source-closure pass, with residual risks limited to
  later live metadata refresh, formula visual checks for the Gordon OCR source,
  complete forward snowballing, remaining source blockers, and future
  MathDevMCP derivation audit.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-manual-pdf-source-closure-plan-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-source-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-citation-venue-metadata-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-claim-support-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-omission-risk-update-2026-05-28.md`
- this result note.

## Commands Run

Representative commands:

```bash
find .local_sources/highdim_nonlinear_filtering -maxdepth 1 -type f -printf '%f\n' | sort
pdfinfo '<each supplied PDF>'
pdftotext -layout '<each supplied PDF>' /tmp/highdim_p1t_text/<name>.txt
pdfimages -list '.local_sources/highdim_nonlinear_filtering/Novel Approach to Nonlinear Non-Gaussian Bayesian State Estimation Gordon.pdf'
pdftoppm -r 300 -png '.local_sources/highdim_nonlinear_filtering/Novel Approach to Nonlinear Non-Gaussian Bayesian State Estimation Gordon.pdf' /tmp/highdim_p1t_text/gordon_page
tesseract /tmp/highdim_p1t_text/gordon_page-1.png /tmp/highdim_p1t_text/gordon_page-1 --psm 6
rg -n '<technical anchor terms>' /tmp/highdim_p1t_text/*.txt
sed -n '<technical line ranges>' /tmp/highdim_p1t_text/*.txt
```

Validation commands are recorded after hostile review.

## What Is Not Concluded

- The chapters are not rewritten or review-ready.
- The literature survey is not yet comprehensive.
- No derivation has been audited with MathDevMCP.
- OCR text from Gordon is not safe for exact quotation without visual checking.
- Citation counts and venue status are not correctness evidence.
- No BayesFilter implementation, benchmark, posterior-accuracy, HMC
  convergence, tensor-method validation, NAWM-readiness, GPU/XLA-readiness, or
  production-readiness claim is supported by P1T.
