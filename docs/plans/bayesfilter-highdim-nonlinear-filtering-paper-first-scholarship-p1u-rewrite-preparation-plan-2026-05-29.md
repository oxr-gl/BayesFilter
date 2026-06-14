# P1U Rewrite Preparation Plan

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T source audit set plus the newly supplied TT-cross,
robust/pathwise DMZ, cubature-review, and Rosenblatt PDFs.

what_is_not_concluded: see section "What Must Not Be Concluded".

## Purpose

P1U is a narrow preparation gate before rewriting Chapters 33--37.  It closes
source blockers that can be closed from newly supplied local PDFs and records
honest alternatives for unavailable or misidentified classical sources.  P1U is
not a chapter rewrite and does not validate any BayesFilter implementation.

## Evidence Contract

- Question: are the remaining source blockers sufficiently closed, scoped, or
  quarantined to permit a paper-first scholarly rewrite?
- Comparator: P1R, P1S, and P1T blocker rows.
- Pass criterion: each newly supplied PDF is validated and either mapped to
  checked technical anchors or explicitly rejected as the wrong/insufficient
  source; unavailable originals are replaced only by checked successor sources
  with scoped claims.
- Veto diagnostics: duplicate/misidentified PDF, scan/OCR uncertainty for exact
  formulas, source used beyond inspected technical anchors, quarantined source
  used as support, or metadata/abstract promoted to theorem support.
- Explanatory diagnostics: citation counts, venue metadata, local file names,
  and chapter rewrite usefulness.
- Artifact: the P1U ledgers and result note under `docs/plans/`.

## Exact Inputs

- P1R ledgers and result notes under
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1r-*`.
- P1S ledgers and result notes under
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1s-*`.
- P1T ledgers and result notes under
  `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1t-*`.
- Local cache `.local_sources/highdim_nonlinear_filtering/`.
- Current chapter files `docs/chapters/ch33_*.tex` through `ch37_*.tex`.
- `docs/references.bib` and `docs/source_map.yml`.
- Scholarly literature audit policy
  `/home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md`.

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-*`.

No chapter, bibliography, source-map, production, DPF, student-baseline, or
controlled-DPF file is edited during P1U.

## Source-Closure Tasks

Validate and inspect:

- Oseledets--Tyrtyshnikov, TT-cross approximation.
- Savostyanov-named maxvol/cross PDF.
- Davis, multiplicative functional transformation in nonlinear filtering.
- Yau--Yau, real-time solution without memory I.
- Yau--Yau, real-time solution without memory II.
- Meng--Wang--Yau--Zhang, regularity and sparse approximation of pathwise
  robust DMZ.
- Stroud-named multiple-integrals PDF.
- Rosenblatt, multivariate transformation.

For each source, record local path, PDF status, publication identity,
technical anchors, allowed claims, forbidden claims, and closure decision.

## Alternative-Source Protocol

Unavailable or misidentified sources must be handled as follows:

- Smolyak: use Jia 2012 only for the sparse-grid quadrature filtering rule
  actually inspected there; do not derive historical Smolyak theory unless a
  checked source is later supplied.
- Genz/Stroud: use Jia 2013 and Arasaratnam--Haykin for filtering-specific
  cubature formulas; use the Stroud review only as context that the book exists
  and is a standard catalogue, not as theorem support.
- Knothe: use Rosenblatt 1952 plus checked modern triangular/KR transport-map
  sources; do not claim historical Knothe proof support.
- Savostyanov maxvol: if the supplied PDF is not the Savostyanov paper, keep
  Savostyanov as blocked and use Oseledets--Tyrtyshnikov's internal maxvol
  discussion only within that paper's TT-cross scope.

## Stop Conditions

Stop before rewrite if any of the following remain unresolved:

- robust/pathwise DMZ cannot be supported beyond source-local statements;
- TT-cross cannot be supported as at least Oseledets--Tyrtyshnikov source-local;
- Rosenblatt/KR definitions cannot be supported by Rosenblatt or modern checked
  transport papers;
- the ledgers would allow claims from a quarantined/retracted source;
- the ledgers hide a wrong or duplicate PDF identity.

## Claude Review Loop

After producing P1U ledgers and result note, launch Claude read-only hostile
review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p1u-rewrite-prep-review-iter<N> \
  --model sonnet \
  --effort high \
  "<bounded read-only scholarly literature audit review prompt>"
```

Claude must output `ACCEPT` or `REJECT` first.  Codex audits Claude's findings.
If Claude rejects and Codex agrees, Codex repairs the ledgers/result note and
resubmits.  Maximum: five iterations.  On iteration five, accept only minor
editorial issues; stop on major source-support, omission-risk, quarantine, or
alternative-source honesty defects.

## Validation Commands

```bash
git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-*
git status --short -- .local_sources docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-*
rg -n "metadata_date|seed_papers|what_is_not_concluded|SOURCE_BLOCKED|QUARANTINED|DUPLICATE_OR_MISIDENTIFIED" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-*.md
```

## What Must Not Be Concluded

P1U must not conclude that the chapters are scholarly, complete, or
review-ready.  It must not validate tensor filtering, TT-cross in BayesFilter,
QTT/DMZ convergence for DSGE, sparse-grid filtering, cubature filters,
transport filtering, HMC, posterior accuracy, NAWM readiness, GPU/XLA readiness,
or production defaults.
