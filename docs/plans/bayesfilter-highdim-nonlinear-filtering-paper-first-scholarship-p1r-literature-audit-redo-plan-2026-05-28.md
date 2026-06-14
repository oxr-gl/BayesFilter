# P1R Literature-Audit Redo Plan

Date: 2026-05-28

Lane: high-dimensional nonlinear filtering paper-first scholarship.

## Purpose

Redo the literature survey/source audit under the shared scholarly literature
audit policy before any chapter rewrite.  The prior P1 source-intake pass
established local full-text availability and technical anchors, but it did not
yet provide reviewer-facing citation/venue metadata provenance, backward and
forward snowballing, retraction/quarantine handling, claim-support mapping, or
omitted-paper risk analysis.

This phase does not rewrite chapters and does not validate any method.  It
decides whether the literature base is ready for paper-first scholarly rewrite
or whether the rewrite remains blocked by source-support, metadata, snowballing,
or omission-risk gaps.

## Evidence Contract

- **Question.** Is the high-dimensional nonlinear filtering paper-first lane
  ready to support chapter rewrites with checked primary sources, explicit
  citation/venue metadata provenance or blockers, snowballing coverage, claim
  support, and omission-risk registers?
- **Comparator.** The existing P1 primary-source ledger and P1 result note.
- **Primary pass criterion.** Every seed paper has a source-support row with
  local artifact status, publication/quarantine status, inspected technical
  anchors, allowed claims, forbidden claims, and support limits.
- **Veto diagnostics.**
  - Any retracted or quarantined paper used as support.
  - Any theorem-level or algorithm-level claim supported only by an abstract,
    introduction, conclusion, citation count, venue rank, or metadata.
  - Any newly placed PDF not indexed or recorded as invalid/source-blocked.
  - Missing separate ledgers for source support, citation/venue metadata,
    backward/forward snowballing, claim support, and omitted-paper risk.
  - No explicit metadata blocker when live citation/ranking metadata is not
    locally or approvingly available.
- **Explanatory diagnostics.**
  - Citation counts, venue rankings, journal/conference prestige, and local
    ResearchAssistant availability.  These are coverage signals only.
  - Number of snowballed references classified per seed paper.
- **Artifact.** The six P1R outputs listed below.
- **What will not be concluded.** P1R will not conclude that the chapters are
  scholarly, that any method is correct, that tensor methods scale, that HMC
  converges, that sparse-grid/cubature methods are promoted, or that any
  BayesFilter implementation is production-ready or NAWM-ready.

## Inputs

- Shared policy:
  `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`
- Claude templates:
  `/home/chakwong/python/claudecodex/claude/prompts/scholarly_literature_audit_review.md`
  and
  `/home/chakwong/python/claudecodex/claude/prompts/scholarly_literature_audit_execution.md`
- Paper-first master/subplans:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- Existing P1 source ledger:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
- Existing P1 result note:
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1-source-intake-result-2026-05-28.md`
- Local source cache:
  `.local_sources/highdim_nonlinear_filtering/`
- Bibliography:
  `docs/references.bib`
- Active chapter files, read-only for context:
  `docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex`
  through
  `docs/chapters/ch37_highdim_filtering_candidate_synthesis.tex`

## Seed Papers

P1R treats the required literature pillars from the paper-first master program
as seed papers, including:

- direct tensor-train nonlinear filtering papers by Li--Wang--Yau--Zhang,
  Zhao--Cui, the functional TT grid filtering paper, and
  Meng--Yau--Zhang;
- tensor-network Kalman papers by Batselier--Chen--Wong, the tensor-network
  square-root Kalman filter paper, and the low-rank tensor UKF tractography
  paper;
- transport-map filtering/smoothing papers by
  Spantini--Baptista--Marzouk and ensemble transport smoothing;
- sparse-grid and high-degree cubature competitors by Jia et al. and adaptive
  sparse-grid Gauss--Hermite filtering;
- transport-preconditioned MCMC/HMC substrate papers including
  transport-map accelerated MCMC, NeuTra HMC, and deep inverse Rosenblatt
  transports using tensor trains;
- numerical tensor substrate papers on TT sampling, TT rank bounds for Gaussian
  densities, Fokker--Planck by TT cross approximation, and high-dimensional
  tensor-network integration.

Spantini et al. 2016, "Decomposable Transport Maps for Bayesian Filtering and
Smoothing", is user-reported retracted and must be recorded as
`RETRACTED_OR_QUARANTINED`, not used as support.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-*`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-primary-source-ledger-2026-05-28.md`
  only to update source status from newly placed PDFs or quarantine
  corrections.
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1-source-intake-result-2026-05-28.md`
  only to append source-status corrections.

No chapter, PDF, `docs/main.tex`, production code, DPF implementation lane,
student-baseline, controlled-DPF, or test edits are authorized.

## Required Outputs

1. Source-support ledger:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-source-support-ledger-2026-05-28.md`
2. Citation/venue metadata ledger:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-citation-venue-ledger-2026-05-28.md`
3. Backward/forward snowball ledger:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-snowball-ledger-2026-05-28.md`
4. Claim-support ledger:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-claim-support-ledger-2026-05-28.md`
5. Omitted-paper/reviewer-risk register:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-omission-risk-register-2026-05-28.md`
6. Result note:
   `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-literature-audit-redo-result-2026-05-28.md`

## Ledger Schemas

### Source-Support Ledger

Each seed row must include:

- `metadata_date`
- `seed_papers`
- paper identity: title, authors, year, DOI/arXiv/URL when locally available;
- method family and classification:
  `FOUNDATIONAL`, `DIRECT_METHOD`, `COMPETITOR`, `SURVEY_OR_TUTORIAL`,
  `IMPLEMENTATION_OR_SOFTWARE`, `EMPIRICAL_EXAMPLE`, `BACKGROUND`,
  `PERIPHERAL`, `SUPERSEDED`, `SOURCE_BLOCKED`, or
  `RETRACTED_OR_QUARANTINED`;
- local artifact path and validity check;
- publication/retraction/quarantine status;
- inspected technical sections, equations, algorithms, theorems, propositions,
  appendices, tables, or experiments;
- problem class, assumptions, main technical objects;
- direct relevance to high-dimensional nonlinear SSMs and BayesFilter/NAWM-like
  DSGE limits;
- `allowed_claims`: claims the source can support, each tied to inspected
  technical anchors or to explicit source scope;
- `forbidden_claims`: claims the source cannot support, each tied to the
  inspected-scope limit, source-gap reason, or quarantine reason;
- `support_class_limits`: what the source-support class permits and forbids for
  chapter rewrite use;
- `what_is_not_concluded`.

### Citation/Venue Metadata Ledger

Each row must include:

- `metadata_date`;
- paper identity and seed flag;
- `citation_count`, `citation_metadata_source`, `citation_metadata_access_date`,
  and citation caveats, or explicit `METADATA_BLOCKED` values;
- `venue`, `venue_metric`, `venue_metric_source`,
  `venue_metric_access_date`, and venue caveats, or explicit
  `VENUE_RANK_BLOCKED` values;
- statement that citation/venue metadata is only a coverage and prioritization
  signal, never claim support;
- action: inspect, cite for context, cite for primary support only after source
  anchors are checked, omit with reason, or quarantine;
- `what_is_not_concluded`.

### Backward/Forward Snowball Ledger

Each seed paper must include:

- `metadata_date`;
- `seed_papers`;
- inspected related-work, literature-survey, introduction, comparison, or
  reference-list sections;
- relevant backward references extracted and classified;
- action for each candidate: cite, inspect next, omit with reason, source
  blocked, or quarantine;
- every seed row must include `forward_snowball_query_status`,
  `query_source`, `query_scope`, and `query_date`.  If no approved metadata
  source is available, use explicit blocked values such as
  `FORWARD_SNOWBALL_BLOCKED_NO_APPROVED_METADATA_QUERY`,
  `QUERY_SOURCE_BLOCKED`, `QUERY_SCOPE_BLOCKED`, and `QUERY_DATE_N/A`;
- when a forward-snowball query is approved and executed: `query_source`,
  `query_scope`, `query_date`, `highly_cited_citing_works`,
  `recent_citing_works`, `followups_or_corrections`, and `forward_action`;
- `what_is_not_concluded`.

### Claim-Support Ledger

Each claim row must include:

- `metadata_date`;
- claim text;
- intended chapter consumer;
- support class:
  `PRIMARY_TECHNICAL_SUPPORT`, `PROJECT_DERIVATION`,
  `IMPLEMENTATION_EVIDENCE`, `SURVEY_CONTEXT_ONLY`,
  `SOURCE_GAP_BLOCKER`, or `QUARANTINED`;
- supporting checked source anchors or project derivation location;
- explicit limits and non-implications;
- reviewer risk if the support is incomplete;
- `what_is_not_concluded`.

### Omitted-Paper/Reviewer-Risk Register

Each candidate row must include:

- `metadata_date`;
- candidate paper or topic;
- reason it arose: seed related work, repeated across seeds, foundational
  expectation, recent/direct competitor, or user concern;
- classification;
- source status;
- expected hostile-review question;
- omission reason or next action;
- severity: high, medium, or low;
- `promotion_rule_status`: `PROMOTED_MANDATORY_INSPECT`,
  `PROMOTED_BLOCKER`, `NOT_PROMOTED`, or `QUARANTINED`;
- `blocking_disposition`: `INSPECTED_CANDIDATE`, `EXPLICIT_BLOCKER`,
  `ACCEPTABLE_OMISSION`, `QUARANTINED`, or `PARTIAL_READY_BLOCKER`;
- `what_is_not_concluded`.

## Retraction And Quarantine Protocol

- Treat user-reported retraction/withdrawal notices as sufficient to quarantine
  until cleared by a human-reviewed source.
- Quarantined papers may be mentioned only to explain exclusion.
- Quarantined papers cannot support claims, derivations, algorithms,
  literature-priority decisions, or synthesis propositions.
- The decomposable-transport workshop paper is quarantined in P1R.  Any
  decomposable/triangular transport exposition must rely on checked,
  non-quarantined transport-map filtering/smoothing sources.

## Metadata Access Protocol

- Do not perform live network/API metadata lookup unless an exact metadata
  source and query scope is approved.
- If an approved metadata query is executed, record the exact source, query
  scope, access date, affected papers, and command or UI procedure in the
  citation/venue ledger and forward-snowball ledger.
- Use local PDFs, local bibliography records, local HTML snapshots, and local
  ResearchAssistant records where available.
- If citation counts or venue rankings are not locally available, record
  `METADATA_BLOCKED_NO_APPROVED_QUERY` or `VENUE_RANK_BLOCKED_NO_APPROVED_QUERY`.
- Do not treat citation count, venue ranking, publication venue, or metadata as
  truth evidence.

## Execution Steps

1. Re-index all locally available seed PDFs into `/tmp/highdim_p1r_text`.
2. Confirm the three user-placed PDFs are valid and indexable:
   - high-degree cubature Kalman filter;
   - sparse-grid quadrature nonlinear filtering;
   - low-rank tensor UKF tractography.
3. For every seed paper, inspect technical sections and the
   related-work/literature-survey/introduction/comparison sections, then extract
   and classify all relevant backward references in the snowball ledger.
4. Create the six P1R output files.
5. If needed, update the older P1 source ledger and P1 result note only for the
   three newly placed PDFs and quarantine correction.
6. Run Claude read-only hostile execution review.
7. Repair ledgers/result notes only if Codex agrees with reviewer findings.

## Snowball Promotion Rule

Any snowballed paper classified as `FOUNDATIONAL`, `DIRECT_METHOD`, or
high-severity `COMPETITOR` becomes one of:

- a mandatory inspected candidate with local source-support status and claim
  limits before declaring `READY_FOR_CHAPTER_REWRITE`; or
- an explicit blocker in the omission-risk register with source status,
  reviewer-risk severity, and next action.

Such papers may be listed in the omission-risk register without blocking only
when the result decision is weaker than `READY_FOR_CHAPTER_REWRITE`, for
example `PARTIAL_READY_WITH_BLOCKERS`.

## Claude Review Loop

Planning review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1r-lit-audit-plan-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only review prompt using scholarly_literature_audit_review.md>"
```

Execution review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1r-lit-audit-exec-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only review prompt using scholarly_literature_audit_review.md>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude's review;
Claude is not final authority.  Loop up to five iterations.  On iteration 5,
accept only minor editorial issues; stop if any major source-support,
snowballing, quarantine, omission-risk, metadata-provenance, or claim-support
defect remains.

## Stop Conditions

- A seed source is unreadable and its method is required for a chapter claim.
- Any quarantined paper is needed to support a claim.
- The three user-placed PDFs cannot be indexed or verified.
- Metadata fields are fabricated or treated as proof.
- Backward snowballing is not recorded for seed papers.
- The final hostile review finds a major scholarly-policy blocker.

## Validation Commands

- `git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`
- Verify only allowed planning/result files changed.
- Verify `.local_sources/` remains untracked and unstaged.
- Verify the decomposable-transport workshop paper is quarantined.
- Verify the three newly placed PDFs are indexed or recorded as invalid/blocker.
- Verify each P1R ledger has `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.
- Verify Claude `ACCEPT` or structured blocker is recorded in the result note.

## What Must Not Be Concluded

P1R does not conclude that the current chapters are scholarly, complete, or
review-ready.  It does not validate tensor-train filtering, tensor-network
Kalman filtering, sparse-grid filtering, cubature filtering, transport-map
filtering/smoothing, NeuTra, HMC, GPU/XLA acceleration, posterior accuracy,
BayesFilter production readiness, or NAWM readiness.
