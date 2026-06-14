# P1U Omission-Risk Update

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T plus P1U newly supplied local PDFs.

what_is_not_concluded: see section "What Is Not Concluded".

## Omission-Risk Rows

| risk | prior_status | p1u_evidence | p1u_adjudication | reviewer-facing answer | next action |
| --- | --- | --- | --- | --- | --- |
| TT-cross/maxvol foundations | P1S blocker | Oseledets--Tyrtyshnikov 2010 local PDF checked; Savostyanov-named file misidentified. | `PARTIALLY_CLOSED` | TT-cross source-local exposition is closed; Savostyanov-specific maxvol/quasioptimality remains blocked. | Ch35 may use Oseledets--Tyrtyshnikov; retain Savostyanov blocker if mentioned. |
| Robust/pathwise DMZ transformations | P1S blocker | Davis 1980, Yau--Yau 2000, Yau--Yau 2008, and Meng 2025 checked. | `CLOSED_FOR_SOURCE_LOCAL_REWRITE` | The rewrite can present PR-DMZ and memoryless algorithms under checked assumptions. | Ch33/Ch35 must include assumptions and no BayesFilter validation claim. |
| Broad cubature foundations: Stroud/Genz | P1S scoped/blocker | Stroud file is a book review only; Jia/Arasaratnam sources are checked. | `DEFER_WITH_ALTERNATIVE_SUPPORT` | Ch34 can derive filtering-specific cubature from CKF/SGQF/HdCKF papers, not from Stroud/Genz originals. | Keep Stroud/Genz as omitted-source risk if making history claims. |
| Smolyak original | P1S scoped/blocker | No original supplied; Jia 2012 provides SGQF formulation. | `DEFER_WITH_ALTERNATIVE_SUPPORT` | Sparse-grid filtering is source-local to Jia/adaptive SGQH; no historical Smolyak proof claim. | Avoid broad Smolyak theorem language. |
| Rosenblatt/Knothe | P1S scoped/blocker | Rosenblatt 1952 checked; Knothe original unavailable. | `PARTIALLY_CLOSED` | Rosenblatt transform is closed; Knothe priority/proof remains blocked. Modern checked transport papers support KR-style algorithms in their own scope. | Use "Rosenblatt/KR" carefully with source-specific citations. |
| Forward snowballing | P1S blocker | No complete forward-snowball refresh in P1U. | `DEFER_TO_FINAL_CHAPTER_AUDIT` | Chapters may not claim exhaustive coverage; they must include omitted-source registers. | Final academic review must check famous/direct/recent omissions. |
| Spantini et al. 2016 decomposable transport workshop | Quarantined | No clearing evidence. | `QUARANTINED` | It remains excluded and cannot support claims. | Use non-quarantined Spantini 2022 and Ramgraber 2023 sources. |

## Decision

`SOURCE_LOCAL_PREPARATION_COMPLETE_WITH_BLOCKERS`

P1U records a source-local preparation status, not a comprehensive rewrite
gate.  Every later rewrite claim must cite the checked source that actually
contains the equation, theorem, algorithm, or proof sketch being used.  This
status does not close the unavailable originals as historical or theorem
sources.  It records which scoped chapter prose can be attempted while keeping
blockers explicit, avoiding comprehensive-survey language, and never using the
misidentified Savostyanov file or Stroud review as theorem support.

## What Is Not Concluded

This update does not close complete forward snowballing, Savostyanov
quasioptimality, Stroud/Genz/Smolyak originals, or Knothe original proof
support.  It does not validate the chapters.
