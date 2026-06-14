# P1U Rewrite Preparation Result

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T source-audit set plus P1U newly supplied local PDFs.

what_is_not_concluded: see section "What Is Not Concluded".

## Decision

`SOURCE_LOCAL_PREPARATION_COMPLETE_WITH_BLOCKERS`

P1U records a source-local preparation status for the later P2R rewrite.  It is
not a comprehensive literature-survey acceptance and it is not a broad rewrite
authorization.  Every later replacement path must cite the checked source that
actually contains the equation, theorem, algorithm, or proof sketch being used.
The rewrite must keep the following blockers explicit:

- Savostyanov maxvol/quasioptimality is not closed; the supplied file is
  misidentified and duplicates Oseledets--Tyrtyshnikov source content.
- Stroud's book is not locally inspected; the supplied file is a review only.
- Smolyak, Genz, and Knothe originals remain unavailable and cannot support
  theorem-level prose.
- Complete forward snowballing remains deferred to final chapter audit.
- Spantini et al. 2016 decomposable-transport workshop paper remains
  quarantined and cannot support claims.

## Codex Inspection

Codex inspected:

- scholarly literature audit policy and Codex skill;
- P1R/P1S/P1T plans, ledgers, omission registers, and result notes;
- `.local_sources/highdim_nonlinear_filtering/`;
- PDF metadata with `pdfinfo`;
- extracted text with `pdftotext -layout` under `/tmp/highdim_p1u_text`;
- current chapter structure in `ch33`--`ch37`;
- `docs/main.tex`, `docs/references.bib`, and `docs/source_map.yml`;
- git status to avoid unrelated DPF/student/controlled-baseline dirty files.

## Source-Support Status

Closed or scoped:

- Oseledets--Tyrtyshnikov 2010 TT-cross: `CLOSED_PRIMARY_ANCHOR_CHECKED`.
- Davis 1980 multiplicative functional transformation:
  `CLOSED_PRIMARY_ANCHOR_CHECKED`.
- Yau--Yau 2000 real-time solution without memory I:
  `CLOSED_PRIMARY_ANCHOR_CHECKED`.
- Yau--Yau 2008 real-time solution without memory II:
  `CLOSED_PRIMARY_ANCHOR_CHECKED`.
- Meng--Wang--Yau--Zhang 2025 PR-DMZ regularity/QTT:
  `CLOSED_PREPRINT_PRIMARY_ANCHOR_CHECKED_WITH_VERSION_CAVEAT`.
- Rosenblatt 1952 multivariate transformation:
  `CLOSED_PRIMARY_ANCHOR_CHECKED`.

Not closed:

- Savostyanov maxvol/quasioptimality: supplied file is misidentified.
- Stroud book: supplied file is a review only.
- Smolyak, Genz, and Knothe originals: unavailable.

## Claude Review History

Preparation execution review:

- Iteration 1: `REJECT`.  Claude found the direct source rows mostly honest but
  rejected the artifact set because the decision language was too strong, the
  alternative-source ledger did not sharply separate source-local technical
  replacement from historical/theorem replacement, and the claim-support update
  did not restate exact anchors for replacement paths.
- Codex agreed that the original language was too strong.  The first repair
  attempted a conditional rewrite-readiness label, but that label was superseded
  and must not be read as authorization.  The durable repair was to add
  replacement type semantics to the alternative-source ledger, expand
  replacement-path anchor detail in the claim-support update, and clarify that
  MCP sections are process provenance rather than claim support.
- Iteration 2: `REJECT`.  Claude accepted the improved alternative-source
  ledger but found that the result and omission-risk notes still sounded like a
  rewrite authorization, one claim-support row used a non-policy support class,
  and the MCP/tool-readiness provenance distracted from the blocker-closure
  report.
- Codex agreed and repaired the artifacts by changing the decision to
  `SOURCE_LOCAL_PREPARATION_COMPLETE_WITH_BLOCKERS`, removing MCP process
  sections from this P1U result note, using only policy support classes, and
  adding exact replacement-path anchors for the Knothe/KR substitute sources.
- Iteration 3: `ACCEPT`.  Claude found the source-support, blocker, quarantine,
  claim-support-class, and allowed-write boundaries policy-compliant after the
  superseded readiness label was neutralized.

## Files Created

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-rewrite-preparation-plan-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-source-closure-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-alternative-source-ledger-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-claim-support-update-2026-05-29.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p1u-omission-risk-update-2026-05-29.md`
- this result note.

## Commands Run

Representative commands:

```bash
git status --short
sed -n '1,260p' /home/chakwong/python/claudecodex/policies/scholarly-literature-audit-policy.md
find .local_sources/highdim_nonlinear_filtering -maxdepth 1 -type f -printf '%f\n' | sort
pdfinfo '<newly supplied PDFs>'
pdftotext -layout '<newly supplied PDFs>' /tmp/highdim_p1u_text/<name>.txt
rg -n '<technical anchor terms>' /tmp/highdim_p1u_text/*.txt
sha256sum '<TT-cross PDF>' '<Savostyanov-named PDF>'
```

## What Is Not Concluded

P1U does not conclude that the chapters are scholarly, complete, well cited, or
review-ready.  It does not validate tensor-train filtering, tensor-network
Kalman filtering, sparse-grid filtering, high-degree cubature, transport-map
filtering/smoothing, NeuTra, HMC, posterior accuracy, GPU/XLA readiness,
production readiness, or NAWM readiness.
