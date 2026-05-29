# P1U Alternative-Source Ledger

Date: 2026-05-29

metadata_date: 2026-05-29

seed_papers: P1R/P1S/P1T checked sources plus P1U newly supplied PDFs.

what_is_not_concluded: see section "What Is Not Concluded".

## Purpose

This ledger states how the rewrite may proceed when a requested original source
is unavailable, duplicated, or only present as a review.  Alternative sources
are allowed only for the technical claims actually checked in those sources.

## Alternative-Source Rows

The column `replacement_type` is part of the evidence contract:

- `TECHNICAL_SOURCE_LOCAL`: the alternative source can support only the
  equations, algorithms, or propositions inspected in that source.
- `HISTORICAL_CONTEXT_ONLY`: the alternative source can explain why a missing
  source matters, but cannot support the missing source's theorem.
- `BLOCKER_ONLY`: the missing source remains a blocker and no replacement claim
  is authorized.

| missing_or_problem_source | status | replacement_type | permitted alternative | permitted scope | forbidden scope | rewrite instruction |
| --- | --- | --- | --- | --- | --- | --- |
| Savostyanov 2014 maxvol/quasioptimality | Supplied local PDF is misidentified; it is another Oseledets--Tyrtyshnikov TT-cross paper. | `BLOCKER_ONLY` for Savostyanov; `TECHNICAL_SOURCE_LOCAL` for Oseledets--Tyrtyshnikov | Oseledets--Tyrtyshnikov 2010 for TT-cross and its internal maxvol-based construction; Oseledets 2011 for TT-SVD/rounding. | TT-cross source-local interpolation formula, low-rank unfolding assumptions, algorithmic maxvol selection as described in the TT-cross paper. | Do not state Savostyanov-specific quasioptimality theorem, do not cite the misidentified file as Savostyanov support, and do not treat the duplicate as independent corroboration. | Ch35 may discuss TT-cross as Oseledets--Tyrtyshnikov; any stronger maxvol theorem is a source blocker. |
| Stroud book `Approximate Calculation of Multiple Integrals` | Local file is a five-page review, not the book. | `HISTORICAL_CONTEXT_ONLY` for Stroud; `TECHNICAL_SOURCE_LOCAL` for checked filtering papers | Arasaratnam--Haykin 2009 CKF; Jia 2012 SGQF; Jia 2013 high-degree CKF; the Stroud review only as historical context. | Filtering-specific cubature/sparse-grid formulas and exactness claims contained in Jia/Arasaratnam; contextual mention that Stroud's book is a major catalogue. | Do not derive Stroud formulas, quote book theorems, or claim inspected Stroud degree proofs. | Ch34 must be source-local to CKF, SGQF, and high-degree CKF. |
| Smolyak original | Not locally available. | `TECHNICAL_SOURCE_LOCAL` for filtering papers; `BLOCKER_ONLY` for original Smolyak theorem/history | Jia 2012 sparse-grid quadrature nonlinear filtering, equations (26)--(29), Theorem 3.1, Algorithm 1; adaptive sparse-grid Gauss-Hermite filtering source. | Sparse-grid construction as used in the checked filtering papers. | Do not claim independent Smolyak theorem/history support. | Ch34 may say "Smolyak-type sparse-grid rules as formulated in Jia 2012" and retain historical-source blocker. |
| Genz cubature foundations | Not locally available. | `TECHNICAL_SOURCE_LOCAL` for checked cubature-filter papers; `BLOCKER_ONLY` for Genz-specific formulas | Arasaratnam--Haykin CKF; Jia 2013 high-degree cubature Kalman filter; Stroud review as context only. | Gaussian cubature filtering formulas, point counts, and exactness statements from checked filtering papers. | Do not make independent Genz formula claims. | Ch34 should focus on cubature filters, not a full cubature-history chapter. |
| Knothe rearrangement original | Not locally available. | `TECHNICAL_SOURCE_LOCAL` for modern KR/triangular algorithms; `HISTORICAL_CONTEXT_ONLY` for Rosenblatt; `BLOCKER_ONLY` for Knothe priority/proof | Rosenblatt 1952; Spantini--Baptista--Marzouk transport filtering; Zhao--Cui TT sequential learning; deep inverse Rosenblatt TT paper. | Rosenblatt conditional-CDF transformation; triangular/Rosenblatt/KR map definitions and algorithms as stated in checked modern sources. | Do not claim original Knothe proof, priority, or theorem support. | Ch35/Ch36 may use "Rosenblatt/KR triangular transport" with source-specific wording and a Knothe-source blocker. |
| Original Duncan/Mortensen/Zakai papers | Not all originals locally inspected. | `TECHNICAL_SOURCE_LOCAL` for standard equations/PR-DMZ; `BLOCKER_ONLY` for historical priority | van Handel notes for standard Zakai/KS equations; Davis 1980; Yau--Yau 2000/2008; Meng 2025 for PR-DMZ/QTT regularity. | Derivation/exposition of normalized/unnormalized filtering equations and PR-DMZ source-local transformations under stated assumptions. | Do not claim historical priority proof beyond checked sources. | Ch33 should cite van Handel as standard derivation anchor and use Davis/Yau/Meng for pathwise robust DMZ. |
| Complete forward snowballing | Incomplete across all seed papers. | `BLOCKER_ONLY` for comprehensive-survey claims | P1R/P1S/P1T/P1U ledgers and chapter-specific omission registers. | Scoped chapter rewrite that does not claim comprehensive survey completeness. | Do not claim exhaustive literature coverage. | Each chapter must include a compact omitted-source register. |

## What Is Not Concluded

This ledger does not say alternative sources are equivalent to the missing
classics.  It only authorizes narrower, source-local claims where the checked
successor or standard source contains the needed equations, algorithms, or
proof sketches.
