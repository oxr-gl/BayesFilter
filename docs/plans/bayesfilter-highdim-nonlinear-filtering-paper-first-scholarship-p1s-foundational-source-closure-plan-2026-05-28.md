# P1S Foundational Source-Closure Plan

Date: 2026-05-28

metadata_date: 2026-05-28

seed_papers: P1R high-dimensional nonlinear filtering paper-first seed set plus
P1R promoted blocker candidates.

what_is_not_concluded: see section "What Must Not Be Concluded".

## Purpose

P1R resolved the missing seed-PDF problem but returned
`PARTIAL_READY_WITH_BLOCKERS` because a skeptical panel would still expect
checked foundational anchors for nonlinear filtering equations, tensor-train
storage/cross approximation, sparse-grid and cubature rules, triangular
transport maps, ensemble transport baselines, HMC/RMHMC/NUTS, particle-filter
collapse, and live metadata/forward-snowball coverage.

P1S closes as many of those blockers as possible before any chapter rewrite.
It is a literature-source and metadata audit phase only.  It does not rewrite
chapters and does not validate any method.

## Evidence Contract

Question: Is the literature base ready enough for a paper-first rewrite of
Ch33--Ch37 without leaving obvious missing-foundation or metadata holes?

Comparator: P1R ledgers and omission-risk register.

Primary pass criterion: every P1R `PROMOTED_BLOCKER` is adjudicated as one of:

- `CLOSED_PRIMARY_ANCHOR_CHECKED`;
- `CLOSED_STANDARD_MONOGRAPH_ANCHOR_CHECKED`;
- `DEFER_TO_CHAPTER_REWRITE_WITH_EXPLICIT_SCOPE`;
- `REMAINS_SOURCE_BLOCKED`;
- `QUARANTINED`.

Veto diagnostics:

- a source is used as theorem/algorithm support without checked technical
  sections, equations, algorithms, proofs, appendices, or experiments;
- citation counts or venue rankings are treated as correctness evidence;
- a quarantined/retracted source is used as support;
- a key direct/foundational paper is silently omitted from the omission-risk
  adjudication table;
- network metadata lacks source, query scope, and access date;
- downloaded PDFs or HTML snapshots are staged or committed.

Explanatory diagnostics:

- citation counts and venue/ranking metadata;
- highly cited or recent citing works from OpenAlex, Crossref, Semantic
  Scholar, arXiv, journal pages, or publisher metadata pages;
- source availability and paywall blockers.

What passes do not conclude: no posterior accuracy, HMC convergence, tensor
validation, NAWM readiness, GPU/XLA readiness, production readiness, or chapter
review-readiness.

Artifact preservation:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-source-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-citation-venue-metadata-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-snowball-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-claim-support-closure-ledger-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-omission-risk-adjudication-2026-05-28.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-foundational-source-closure-result-2026-05-28.md`

## Inputs

- Scholarly audit policy:
  `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`
- P1R plan, ledgers, and result note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-*`
- Existing primary-source ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
- Bibliography and source map:
  `docs/references.bib`, `docs/source_map.yml`
- Local source cache:
  `.local_sources/highdim_nonlinear_filtering/`
- Chapter files as read-only context:
  `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  through
  `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-*`
- Existing P1R ledgers/result notes only if appending a clearly labeled
  correction.
- `.local_sources/highdim_nonlinear_filtering/` for uncommitted source cache
  PDFs, HTML snapshots, and metadata snapshots.

`.local_sources` artifacts are cache/provenance artifacts only.  They may
support a statement that a query or source-intake attempt occurred, but they do
not by themselves support technical claims and cannot substitute for checked
primary technical text or a project derivation.

## Forbidden Writes

- No chapter edits.
- No `docs/main.tex` or `docs/main.pdf` edits.
- No production `bayesfilter/` edits.
- No DPF implementation-lane, student-baseline, or controlled-DPF edits.
- No public API changes.
- No commits.
- No staged downloaded PDFs, HTML snapshots, or `.local_sources/` files.

## Source-Closure Targets

### Nonlinear Filtering Foundations

Close or explicitly block primary/standard anchors for:

- Zakai equation and unnormalized conditional density;
- Duncan--Mortensen--Zakai lineage;
- Kushner--Stratonovich normalized filtering equation;
- robust/pathwise DMZ transformations used by TT/DMZ sources;
- nonlinear filtering stability sources only if the rewrite will make stability
  claims.

### Tensor Foundations

Close or explicitly block:

- Oseledets TT decomposition and TT-SVD;
- TT-rounding storage and rank notation;
- TT-cross and maxvol/cross approximation foundations;
- low-rank tensor surveys for orientation only, not theorem support;
- TT rank/pathology references needed to prevent overclaiming.

### Sparse-Grid And Cubature Foundations

Close or explicitly block:

- Smolyak sparse-grid construction;
- Stroud/Genz/Mysovskikh/Cools cubature rules where needed for exactness;
- Julier--Uhlmann unscented transform and van der Merwe sigma-point thesis;
- Arasaratnam--Haykin CKF and continuous-discrete CKF;
- Ito--Xiong or standard Gaussian approximation filtering references if
  Ch34 derives Gaussian-filter forms.

### Transport Filtering Foundations

Close or explicitly block:

- Rosenblatt and Knothe rearrangements or a checked standard transport-map
  source for triangular/KR definitions;
- Villani and Peyre--Cuturi as optimal-transport context sources;
- Reich ensemble transform particle filter;
- EnKF/LETKF/localization foundations if localization is discussed;
- feedback particle filter or multivariate-rank-histogram competitors only if
  retained in chapter scope.

### HMC And Transport-Acceleration Foundations

Close or explicitly block:

- Neal HMC;
- Hoffman--Gelman NUTS;
- Betancourt HMC diagnostics;
- Girolami--Calderhead RMHMC;
- Parno--Marzouk transport-map MCMC and NeuTra remain checked seed supports,
  but P1S must ensure their HMC comparison claims are anchored in checked HMC
  foundations.

### Particle-Filter Baselines And Collapse

Close or explicitly block:

- Gordon--Salmond--Smith bootstrap particle filter;
- Doucet/de Freitas/Gordon and Chopin--Papaspiliopoulos SMC monographs as
  standard references;
- Arulampalam tutorial for tracking-oriented exposition only;
- Bengtsson--Bickel--Li and Snyder et al. high-dimensional collapse warnings.

## Metadata And Forward-Snowball Protocol

Approved public metadata/query sources for P1S:

- OpenAlex;
- Crossref;
- Semantic Scholar;
- arXiv;
- journal/publisher metadata pages;
- local PDFs and `docs/references.bib`.

Each metadata row must record:

- `local_bibliographic_fact_source`;
- `live_metadata_source_status`;
- `citation_count`;
- `citation_metadata_source`;
- `citation_metadata_query`;
- `citation_metadata_access_date`;
- `venue`;
- `venue_metric`;
- `venue_metric_source`;
- `venue_metric_query`;
- `venue_metric_access_date`;
- `metadata_caveat`.

If unavailable, use explicit blocked sentinels such as:

- `METADATA_UNAVAILABLE_FROM_APPROVED_PUBLIC_SOURCE`;
- `VENUE_METRIC_UNAVAILABLE_FROM_APPROVED_PUBLIC_SOURCE`;
- `PAYWALL_OR_ACCESS_BLOCKED`;
- `QUERY_FAILED_RECORDED`.

Citation counts and venue ranks are only coverage signals.  They cannot support
technical claims.

Forward-snowball rows must record:

- seed paper;
- query source;
- query string or DOI/arXiv identifier;
- query date;
- highly cited citing works when available;
- recent citing works when available;
- followups/corrections/negative results when found;
- action: `INSPECT_NEXT`, `CITE_FOR_CONTEXT`, `DEFER`, `OMIT_WITH_REASON`,
  `SOURCE_BLOCKED`, or `QUARANTINE`.

Every non-quarantined seed paper and every promoted blocker requiring live
coverage must have at least one forward-snowball row.  If the query fails,
returns no usable citing works, or is unavailable, the row must still record
the source, query identifier/string, access date, and explicit failure/blocker
sentinel.  Silence is not an allowed forward-snowball status.

## Retraction And Quarantine Protocol

Before a source closes a blocker, check available public/local status for:

- retraction or withdrawal;
- expression of concern;
- major erratum/corrigendum;
- arXiv version mismatch;
- publisher/local PDF identity mismatch;
- user or reviewer quarantine notice.

Spantini et al. 2016 "Decomposable Transport Maps for Bayesian Filtering and
Smoothing" remains `RETRACTED_OR_QUARANTINED` unless a later explicit human
decision clears it.  It cannot support claims.

Any non-clean retraction, withdrawal, erratum, version, publisher-identity, or
user/reviewer quarantine check must include a disposition note naming the
clearing source and rationale.  If no clearing source is available, the row
must remain `QUARANTINED`, `REMAINS_SOURCE_BLOCKED`, or otherwise blocked; it
cannot be treated as closed.

## Ledger Schemas

### Source-Closure Ledger

Columns:

`blocker_topic`, `source`, `classification`, `local_artifact_or_url`,
`source_status`, `publication_status`, `retraction_quarantine_status`,
`retraction_check_source`, `retraction_check_date`, `version_identity_check`,
`erratum_check_result`, `quarantine_basis`, `technical_anchors_checked`,
`allowed_claims`, `forbidden_claims`, `closure_decision`, `remaining_action`.

### Citation/Venue Metadata Ledger

Columns:

`paper_or_topic`, `seed_or_blocker`, `local_bibliographic_fact_source`,
`live_metadata_source_status`, `citation_count`, `citation_metadata_source`,
`citation_metadata_query`, `citation_metadata_access_date`, `venue`,
`venue_metric`, `venue_metric_source`, `venue_metric_query`,
`venue_metric_access_date`, `metadata_caveat`, `coverage_action`.

### Snowball Closure Ledger

Columns:

`seed_or_blocker`, `backward_or_forward`, `inspected_section_or_query`,
`query_source`, `query_identifier_or_string`, `query_access_date`,
`forward_query_status`, `candidate_work`, `classification`, `source_status`,
`citation_signal`, `recency_signal`, `highly_cited_citing_works`,
`recent_citing_works`, `followups_corrections_negative_results`, `action`,
`omission_risk`.

Blocked forward-snowball fields must use explicit sentinels, not blank cells:
`FORWARD_QUERY_BLOCKED`, `FORWARD_QUERY_FAILED_RECORDED`,
`NO_CITING_WORKS_RETURNED_BY_APPROVED_SOURCE`, or
`NOT_APPLICABLE_BACKWARD_ROW`.

### Claim-Support Closure Ledger

Columns:

`future_claim`, `intended_chapter`, `support_class`,
`checked_anchor_or_blocker`, `allowed_scope`, `forbidden_scope`,
`rewrite_instruction`.

### Omission-Risk Adjudication

Columns:

`p1r_source_row_or_topic`, `p1r_risk`, `severity`, `p1s_evidence`,
`closure_basis`, `technical_anchor_reference`, `adjudication`,
`reviewer_answer`, `next_action`.

Any row marked `CLOSED` with `closure_basis` equal to `PRIMARY_ANCHOR` or
`STANDARD_MONOGRAPH_ANCHOR` must cite concrete checked anchors in
`technical_anchor_reference`: section, equation, theorem, proposition,
algorithm, appendix, table, or equivalent stable locator.  Generic phrases
such as "checked standard source" or blank anchors are invalid and must be
treated as a failed closure.

Allowed closure bases:

- `PRIMARY_ANCHOR`;
- `STANDARD_MONOGRAPH_ANCHOR`;
- `EXPLICIT_SCOPE_DEFERRAL`;
- `SOURCE_BLOCKED`;
- `QUARANTINED`;
- `NOT_IN_REWRITE_SCOPE`.

Allowed adjudications:

- `CLOSED`;
- `DEFER_TO_CHAPTER_REWRITE`;
- `REMAINS_SOURCE_BLOCKED`;
- `QUARANTINED`.

Metadata status is ancillary provenance only.  A metadata blocker cannot close
or resolve a P1R scholarly blocker by itself.  If live metadata is unavailable,
the scientific blocker must still be adjudicated by primary/standard source
anchors, explicit scope deferral, source block, quarantine, or not-in-scope
status.

## Skeptical Plan Audit

Pre-execution audit result:

- Wrong baselines: avoided by using P1R risks as comparator, not method
  performance rankings.
- Proxy metrics: citation and venue metadata are explicitly explanatory
  coverage signals only.
- Stop rules: veto diagnostics require stopping or preserving blockers if
  sources remain unchecked, quarantined, paywalled, or metadata is unavailable.
- Unfair comparisons: no method ranking is produced in P1S.
- Stale context: P1S re-inspects P1R ledgers, local source cache, bibliography,
  and approved public metadata.
- Unsupported claims: P1S forbids chapter-readiness, method validation,
  tensor-readiness, HMC convergence, NAWM readiness, GPU/XLA readiness, and
  production claims.

The plan passes the skeptical audit for a source-closure phase.  It would fail
as a chapter-rewrite plan, so chapter rewriting remains out of scope.

## Claude Review Loop

Claude Code is read-only for plan and execution review.

Plan review command pattern:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1s-source-closure-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only review prompt>"
```

Execution review command pattern:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1s-source-closure-exec-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude's findings
and remains final authority.  Loop up to 5 iterations.  Iteration count never
overrides policy-critical defects.  "Minor editorial issues" excludes any issue
affecting source-support specificity, omission-risk closure logic,
forward-snowball completeness, metadata provenance, or quarantine enforcement.
On iteration 5, stop if any such defect remains.

## Execution Steps

1. Extract source identities from P1R promoted blockers and `docs/references.bib`.
2. Locate local full text first; use public URLs only when local text is absent.
3. Download or snapshot public full text/metadata only into
   `.local_sources/highdim_nonlinear_filtering/`.
4. Convert PDFs to text where possible for anchor inspection.
5. Inspect technical sections/equations/algorithms/proofs for each closure
   target; do not rely on abstracts.
6. Query approved metadata/forward-snowball sources where possible.
7. Populate the P1S ledgers and result note.
8. Run Claude execution review and repair agreed defects.
9. Validate changed paths and unstaged `.local_sources/`.

## Validation Commands

```bash
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*
git diff --name-only -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*
git status --short -- .local_sources docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*
rg -n "metadata_date|seed_papers|what_is_not_concluded" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-*.md
rg -n "RETRACTED_OR_QUARANTINED|QUARANTINED" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-*.md
```

## Stop Conditions

Stop and record `BLOCKED` if:

- the plan fails Claude review by iteration 5 with a major scholarly-policy
  defect;
- downloaded/source artifacts become too large for normal local cache handling;
- a required source is paywalled and no local copy exists;
- a retraction or quarantine notice affects a source needed for a central
  claim;
- metadata/forward-snowball queries are unavailable and the remaining omission
  risk would make chapter rewrite unsafe;
- validation detects disallowed path changes.

## What Must Not Be Concluded

P1S does not conclude that the chapters are scholarly, complete, well cited, or
ready for a skeptical panel.  It does not validate TT filtering, tensor-network
Kalman filtering, sparse-grid/cubature filtering, transport filtering, HMC,
NeuTra, BayesFilter posterior accuracy, NAWM readiness, GPU/XLA readiness, or
production defaults.
