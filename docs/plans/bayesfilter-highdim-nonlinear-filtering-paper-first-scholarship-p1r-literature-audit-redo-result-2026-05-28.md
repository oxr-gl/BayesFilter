# P1R Literature-Audit Redo Result

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: high-dimensional nonlinear filtering paper-first seed set.

what_is_not_concluded: see section "What Is Not Concluded".

## Decision

`PARTIAL_READY_WITH_BLOCKERS`

The source-intake blocker for the three manually supplied PDFs is resolved:
high-degree cubature Kalman filtering, sparse-grid quadrature nonlinear
filtering, and low-rank tensor UKF tractography are now locally indexed.

The literature base is not yet clean enough for an unqualified
`READY_FOR_CHAPTER_REWRITE` decision because P1R found promoted omission risks:
classical nonlinear filtering foundations, TT-SVD/TT-cross foundations,
sparse-grid/cubature foundations, transport/KR foundations, HMC foundations, and
forward snowballing metadata remain source or metadata blockers for a fully
reviewer-proof survey.

## Codex Inspection

Codex inspected:

- the shared scholarly literature audit policy;
- the Claude literature-audit review template;
- the paper-first master program and P1 source-intake plan;
- the existing P1 primary-source ledger and P1 result note;
- `.local_sources/highdim_nonlinear_filtering/`;
- `docs/references.bib`;
- current high-dimensional chapter files `ch33`--`ch37` as read-only context;
- local PDF metadata and text extracted under `/tmp/highdim_p1r_text`;
- git status to avoid DPF/student/controlled-baseline dirty files.

## ResearchAssistant MCP Use

ResearchAssistant MCP was used read-only.

- `ra_workspace_status` confirmed read-only local mode.
- Searches for tensor-train nonlinear filtering and transport-map nonlinear
  ensemble filtering returned no local curated summaries.
- NeuTra HMC returned a local draft summary with `review_status:
  needs_review`, so it was not used as theorem support.

P1R therefore relies on checked local PDFs rather than ResearchAssistant
summaries for primary-source support.

## MathDevMCP Use

MathDevMCP `doctor` was run.  It reported LaTeXML, Pandoc, Sage, SymPy, and
LeanDojo available; direct Lean version check timed out.  No derivation audit was
run because P1R is a literature/source audit phase, not a derivation rewrite.

## Claude Review History

Planning review:

- Iteration 1: `REJECT`.  Claude found schema weaknesses around exact
  venue-metric fields, forward-snowball provenance, forbidden-claim fields,
  every-seed backward snowballing, metadata-query provenance, and promotion
  rules for snowballed foundational/direct/competitor papers.
- Iteration 2: `REJECT`.  Claude required exact `venue_metric_source` and
  `venue_metric_access_date`, blocked forward-snowball fields on every row, and
  omission-risk promotion/disposition fields.
- Iteration 3: `ACCEPT`.  Residual risks: execution must keep forward
  snowballing blocked rather than overclaiming, use consistent metadata blocker
  sentinels, apply quarantine to newly found risks, and return a weaker decision
  if promoted papers remain uninspected.

Execution review: pending at time this result note was first created; final
status must be appended after Claude execution review.

Execution review update:

- Iteration 1: `REJECT`.  Claude found no substantive source-support collapse,
  but rejected the artifact set for incomplete review-loop recording, bare `N/A`
  access-date placeholders in the citation/venue ledger, and mixed support
  classes in the claim-support ledger.
- Codex agreed and repaired the artifacts by recording the execution-review
  outcome in this result note, replacing bare metadata access-date placeholders
  with the explicit `QUERY_DATE_N/A` blocked sentinel, and splitting mixed
  support-class rows into single-class claim rows.
- Iteration 2: `ACCEPT`.  Residual risks: forward snowballing remains blocked,
  many promoted omission-risk blockers remain, and the Spantini 2016 quarantine
  rests on user report rather than independent external provenance.  These
  risks are consistent with the weaker `PARTIAL_READY_WITH_BLOCKERS` decision
  and forbid any claim of comprehensive literature completeness.

## Files Created Or Updated

Created:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-literature-audit-redo-plan-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-source-support-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-citation-venue-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-snowball-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-claim-support-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-omission-risk-register-2026-05-28.md`
- this result note.

Updated:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1-source-intake-result-2026-05-28.md`

Only source-status corrections were appended to the older P1 artifacts.

## Three Newly Placed PDFs

P1R verified these with `pdfinfo` and `pdftotext`:

| Paper | Local path | P1R status | Key anchors |
| --- | --- | --- | --- |
| High-degree cubature Kalman filter | `.local_sources/highdim_nonlinear_filtering/High-degree cubature Kalman filter Jia(13).pdf` | `LOCAL_FULL_TEXT_INDEXED` | Automatica 49 (2013) 510--518, DOI `10.1016/j.automatica.2012.11.014`; equations (1)--(46), Definition 3.1, Theorem 3.1, Propositions 3.1--3.2, Tables 1--3. |
| Sparse-grid quadrature nonlinear filtering | `.local_sources/highdim_nonlinear_filtering/Sparse-grid quadrature nonlinear filtering Jia(11).pdf` | `LOCAL_FULL_TEXT_INDEXED` | Automatica 48 (2012) 327--341, DOI `10.1016/j.automatica.2011.08.057`; equations (1)--(29), Theorems 3.1--3.2, Algorithm 1, Propositions 3.1--3.2, Appendix formulas (47)--(52). |
| Spatially regularized low-rank tensor approximation for accurate and fast tractography | `.local_sources/highdim_nonlinear_filtering/Spatially regularized low-rank tensor approximation for accurate and fast tractography Gruen(23).pdf` | `LOCAL_FULL_TEXT_INDEXED` | NeuroImage 271 (2023) 120004, DOI `10.1016/j.neuroimage.2023.120004`; equations (1)--(20), low-rank tensor approximation, spatial weights, low-rank UKF, experiments, Table 1. |

## Quarantined Papers

- Spantini et al. 2016, "Decomposable Transport Maps for Bayesian Filtering
  and Smoothing": `RETRACTED_OR_QUARANTINED` due to user report on
  2026-05-28.  It cannot support claims, derivations, algorithms, synthesis, or
  literature-priority judgments.

## Citation/Venue Metadata Status

Citation counts and venue rankings were not queried.  Every live metadata field
uses blocked sentinels such as:

- `METADATA_BLOCKED_NO_APPROVED_QUERY`
- `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY`
- `QUERY_SOURCE_BLOCKED`
- `QUERY_SCOPE_BLOCKED`
- `QUERY_DATE_N/A`

Local venue/DOI facts were recorded only from local PDF metadata, article
headers, or existing bibliography entries.

## Top Omitted-Paper / Reviewer Risks

High-severity promoted blockers:

- Oseledets TT decomposition and TT-SVD.
- TT-cross/maxvol foundations.
- Zakai/Duncan/Mortensen/Kushner--Stratonovich nonlinear filtering foundations.
- Robust/pathwise DMZ references used by the TT/DMZ papers.
- Smolyak sparse-grid construction.
- Arasaratnam--Haykin CKF and Julier--Uhlmann UKF/UT foundations.
- Reich ensemble transform, Rosenblatt/Knothe transport foundations, and
  EnKF/localization references.
- Neal/Hoffman--Gelman/Betancourt HMC foundations and Girolami--Calderhead
  RMHMC.
- Forward snowballing for recent/highly cited citing works.

These are not all missing from the repository bibliography, but their relevant
technical sections were not checked in P1R.

## Commands Run

- `sed -n ...` on the skill, policy, Claude review template, plans, ledgers,
  result notes, chapters, and extracted text.
- `rg --files`, `rg -n ...`, `find ...`, `git status --short`.
- ResearchAssistant MCP: `ra_workspace_status`, `ra_find_paper`.
- MathDevMCP: `doctor`.
- Claude plan reviews via
  `bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh ...`.
- `mkdir -p /tmp/highdim_p1r_text`.
- `pdftotext -layout` for all local seed PDFs into `/tmp/highdim_p1r_text`.
- `pdfinfo` for local seed PDFs, especially the three user-placed PDFs.

Validation commands and execution-review commands are recorded after execution
review below.

## Execution Review Repair

After Claude execution review iteration 1, Codex made the following repairs:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-citation-venue-ledger-2026-05-28.md`:
  replaced bare `N/A` access-date placeholders with `QUERY_DATE_N/A` and
  recorded the sentinel convention.
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-claim-support-ledger-2026-05-28.md`:
  split mixed support-class rows into separate `PRIMARY_TECHNICAL_SUPPORT`,
  `SOURCE_GAP_BLOCKER`, and `PROJECT_DERIVATION` rows.
- This result note: recorded the execution-review iteration 1 rejection and
  repairs so the review loop is auditable.

Claude execution review iteration 2 returned `ACCEPT`; final validation follows.

## Final Validation

Validation commands:

- `git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `git diff --name-only -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `git status --short -- .local_sources docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- `rg -n "metadata_date|seed_papers|what_is_not_concluded|RETRACTED_OR_QUARANTINED|QUERY_DATE_N/A|FORWARD_SNOWBALL_BLOCKED" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-*.md`

Validation result must be checked in the final Codex response.  No commit is
authorized by this P1R task.

## What Is Not Concluded

P1R does not conclude that the chapters are scholarly, complete, well cited, or
review-ready.  It does not validate tensor-train filtering, tensor-network
Kalman filtering, sparse-grid filtering, high-degree cubature, transport-map
filtering/smoothing, NeuTra, HMC, posterior accuracy, GPU/XLA readiness,
production readiness, or NAWM readiness.
