# P1S Foundational Source-Closure Result

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: P1R seed set plus P1S promoted blocker candidates.

what_is_not_concluded: see section "What Is Not Concluded".

## Decision

`PARTIAL_READY_WITH_BLOCKERS`

P1S closed several important P1R blockers and improved metadata/forward
snowball coverage, but it is not rewrite-ready and it is not enough for
`READY_FOR_CHAPTER_REWRITE`.  The next step may draft only scoped,
source-local material whose anchors are explicitly closed in the P1S ledgers.
It must not claim comprehensive survey coverage, rewrite-readiness,
robust-DMZ closure, TT-cross closure, CKF-primary closure,
high-dimensional particle-collapse closure, or RMHMC closure unless additional
sources are supplied, checked, and reviewed.

Surviving scholarly blockers after P1S:

- TT-cross/maxvol primary foundations;
- robust/pathwise DMZ transformations;
- Arasaratnam--Haykin CKF primary paper;
- high-dimensional particle-filter collapse papers, especially Snyder et al.
  and Bengtsson--Bickel--Li technical text;
- Girolami--Calderhead RMHMC primary paper;
- broad Smolyak/Stroud/Genz cubature foundations if Ch34 goes beyond
  Jia-source-local derivations;
- complete forward-snowball coverage for all seed papers and promoted blockers.

These are unresolved scholarly blockers, not merely editorial rewrite tasks.

## Codex Inspection

Codex inspected:

- scholarly literature audit policy and Codex skill;
- Claude literature audit review and execution prompt templates;
- P1R result, source-support, citation/venue, snowball, claim-support, and
  omission-risk ledgers;
- existing paper-first master/subplans and primary-source ledger;
- `.local_sources/highdim_nonlinear_filtering/`;
- `docs/references.bib` and `docs/source_map.yml` as read-only context;
- current Ch33--Ch37 as read-only context;
- local PDF metadata and extracted text under `/tmp/highdim_p1s_text`;
- OpenAlex metadata and forward-snowball JSON snapshots cached under
  `.local_sources/highdim_nonlinear_filtering/`.

## ResearchAssistant MCP Use

ResearchAssistant MCP was used read-only.

- `ra_workspace_status` confirmed local read-only mode.
- Searches for HMC foundations, tensor-train foundations, and nonlinear
  filtering foundations returned no usable curated local summaries.

P1S therefore relied on checked local PDFs and public metadata rather than
ResearchAssistant claim support.

## MathDevMCP Use

MathDevMCP was not used for derivation audits in P1S because this phase is a
literature-source and metadata closure pass, not a chapter derivation phase.
The later rewrite should use MathDevMCP when equations are written in project
notation.

## Claude Review History

Plan review:

- Iteration 1: `REJECT`.  Claude required explicit forward-snowball fields,
  retraction/version check fields, stronger omission-risk closure schema,
  cache non-authority language, and local-vs-live metadata separation.
- Iteration 2: `REJECT`.  Claude found metadata-blocked status could still be
  mistaken for blocker closure, `CLOSED` rows did not require concrete anchors,
  per-seed forward rows were not mandatory, and non-clean retraction/version
  dispositions needed stricter rules.
- Iteration 3: `ACCEPT`.  Residual risks moved to execution quality rather than
  plan sufficiency.

Execution review:

- Iteration 1: `REJECT`.  Claude found that this result note still said
  execution review was pending, forward-snowball coverage was incomplete
  relative to the plan's per-seed requirement, surviving blockers were not
  prominent enough in the Decision section, metadata-count language needed a
  sharper non-closure caveat, and the final comprehensive-survey blocker needed
  stronger wording.
- Codex agreed and repaired the artifacts by appending explicit per-seed
  forward-snowball status rows, listing surviving blockers in the Decision
  section, clarifying that metadata captures never close blockers by
  themselves, and marking incomplete forward coverage as an active
  reviewer-risk blocker.
- Iteration 2: `REJECT`.  Claude found no remaining substantive source-anchor,
  metadata-discipline, quarantine, or per-seed forward-row defect, but rejected
  because this result note still said iteration 2 was pending and because the
  Decision section said the rewrite "may proceed" too loosely despite
  incomplete forward-snowball coverage.
- Codex agreed and repaired the Decision section to state that P1S is not
  rewrite-ready; only scoped, source-local drafting is allowed until the
  forward-snowball blocker is cleared or formally deferred at a later gate.
- Iteration 3: `REJECT`.  Claude found only an internal review-status defect:
  this note still contained a stale "Iteration 3 pending" marker.
- Codex agreed and removed the stale pending marker.  No source-support,
  metadata-discipline, quarantine, forward-row, or overclaim defect was newly
  identified in iteration 3.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-foundational-source-closure-plan-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-source-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-citation-venue-metadata-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-snowball-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-claim-support-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-omission-risk-adjudication-2026-05-28.md`
- this result note.

No chapter, production, DPF, student-baseline, controlled-DPF, `docs/main.tex`,
or `docs/main.pdf` file was intentionally edited by P1S.

## Newly Closed Sources

Closed with checked technical anchors:

- Oseledets 2011 TT decomposition and TT-SVD:
  `.local_sources/highdim_nonlinear_filtering/oseledets_tt_decomposition_2011.pdf`.
- van Handel stochastic filtering lecture notes for standard Zakai,
  Kushner--Stratonovich, innovations, and Zakai PDE anchors:
  `.local_sources/highdim_nonlinear_filtering/van_handel_stochastic_calculus_filtering_control_acm217.pdf`.
- Julier--Uhlmann 1997 UKF/UT:
  `.local_sources/highdim_nonlinear_filtering/julier_uhlmann_new_extension_1997.pdf`.
- Reich 2013 ensemble transform:
  `.local_sources/highdim_nonlinear_filtering/reich_nonparametric_ensemble_transform_2013.pdf`.
- Neal 2011 HMC:
  `.local_sources/highdim_nonlinear_filtering/neal_hmc_2011.pdf`.
- Hoffman--Gelman 2014 NUTS:
  `.local_sources/highdim_nonlinear_filtering/hoffman_gelman_nuts_2014.pdf`.
- Betancourt 2017 HMC conceptual/diagnostic source:
  `.local_sources/highdim_nonlinear_filtering/betancourt_conceptual_hmc_1701.02434.pdf`.
- Arulampalam et al. 2002 particle-filter tutorial:
  `.local_sources/highdim_nonlinear_filtering/arulampalam_particle_filter_tutorial_2002.pdf`.

## Source Attempts That Remain Blocked

- TT-cross/maxvol primary source: one public URL attempt returned 404.
- Arasaratnam--Haykin CKF: CiteseerX public attempt failed SSL certificate
  verification; no local full text was accepted.
- Girolami--Calderhead RMHMC: arXiv/DOI-style public attempt returned 404.
- Gordon--Salmond--Smith bootstrap particle filter: public URL attempt returned
  404.
- Snyder et al. high-dimensional PF obstacles: publisher PDF endpoint attempt
  returned 405; exact OpenAlex metadata found but no local technical text.
- Bain--Crisan Springer PDF attempt saved an HTML page, not a PDF; it was not
  used as technical support.
- Peyre--Cuturi download saved an HTML landing page, not the full technical
  book; it was not used as theorem support.

## Metadata/Citation/Venue Coverage

OpenAlex exact DOI/title records were captured for:

- Oseledets TT decomposition: 2617 citations.
- Jia 2012 SGQF: 259 citations.
- Jia 2013 high-degree CKF: 460 citations.
- Spantini--Baptista--Marzouk transport filtering: 64 citations.
- Parno--Marzouk transport-map MCMC: 81 citations.
- Reich ensemble transform: 184 citations.
- Hoffman--Gelman NUTS: 169 citations.
- Arulampalam PF tutorial: exact search top result, 11461 citations.
- Snyder et al. obstacles to high-dimensional PF: exact search top result, 700
  citations, but source text blocked.

Venue rankings were not queried.  Citation counts and venue names are coverage
signals only.

None of these metadata captures changed a blocker adjudication unless paired
with checked technical anchors in the source-closure and omission-risk ledgers.
Counts for source-blocked items such as Snyder et al. raise reviewer-risk
priority; they do not support collapse claims or close the source blocker.

## Forward-Snowball Coverage

OpenAlex forward-snowball queries were completed for exact OpenAlex work ids
where available:

- Oseledets TT;
- Jia SGQF;
- Jia high-degree CKF;
- Spantini transport filtering;
- Parno transport-map MCMC;
- Reich ensemble transform.

Important candidates surfaced for later inspection:

- tensor-decomposition and model-reduction surveys citing Oseledets;
- Gaussian-filter/nonlinear Bayesian estimation reviews citing Jia;
- monotone triangular transport-map work and ensemble score filter citing
  Spantini;
- high-dimensional geoscience particle-filter review citing Reich.

These candidates are metadata-only until their technical text is inspected.

Forward-snowball coverage is still incomplete for many seed papers and promoted
blockers.  The snowball ledger now records explicit per-seed
`FORWARD_QUERY_BLOCKED_P1S_INCOMPLETE`, `FORWARD_QUERY_FAILED_RECORDED`, or
search-only rows rather than silently treating them as closed.  This remains an
active reviewer-risk blocker for any later comprehensive-survey or
rewrite-readiness claim.

## Quarantined Papers

- Spantini et al. 2016, "Decomposable Transport Maps for Bayesian Filtering and
  Smoothing": remains `RETRACTED_OR_QUARANTINED` due to user report on
  2026-05-28.  It cannot support claims.

## Commands Run

Representative commands:

- `sed -n ...` on policy, skill, Claude templates, P1R ledgers, plans,
  bibliography, and source ledgers.
- `find .local_sources/highdim_nonlinear_filtering ...`, `rg ...`,
  `git status --short`.
- ResearchAssistant MCP: `ra_workspace_status`, `ra_find_paper`.
- Claude plan review via
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh ...`.
- `curl -L --fail --retry 2 ...` for public PDFs and OpenAlex metadata.
- `pdfinfo ...`, `file ...`, `wc -c ...`.
- `pdftotext -layout ... /tmp/highdim_p1s_text/*.txt`.
- Python JSON parsing for OpenAlex snapshots.

Validation and execution-review commands are recorded after final review.

## What Is Not Concluded

P1S does not conclude that the chapters are scholarly, complete, well cited, or
ready for a skeptical panel.  It does not validate TT filtering, TT-cross,
tensor-network Kalman filtering, sparse-grid/cubature filtering, transport
filtering, HMC, NeuTra, RMHMC, BayesFilter posterior accuracy, NAWM readiness,
GPU/XLA readiness, or production defaults.
