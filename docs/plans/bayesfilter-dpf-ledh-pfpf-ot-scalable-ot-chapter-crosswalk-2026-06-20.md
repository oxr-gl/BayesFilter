# Chapter Crosswalk: Scalable OT Survey Reintegration

**Date:** 2026-06-20
**Source survey:** `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-scalable-ot-self-contained-survey-paper-2026-06-17.tex`

## Purpose

Map the standalone scalable-OT survey into the intended BayesFilter monograph
DPF/OT chapter roles while keeping source truth, transitional chapter contents,
and provenance-only material clearly separated.

## Integration principles

1. The standalone survey is **source truth / donor material**, not a direct
   `\input` target for `docs/main.tex`.
2. The current DPF/OT block in `docs/main.tex` remains the destination topology:
   - `ch19b_dpf_literature_survey`
   - `ch19c_dpf_implementation_literature`
   - `ch32a_soft_differentiable_resampling`
   - `ch32b_deterministic_ot_equalweighting`
   - `ch32c_entropic_ot_sinkhorn`
   - `ch32d_retained_teacher_neural_ot`
   - `ch32e_icnn_brenier_monge_gap_map_learning`
   - `ch32f_dynamic_geodesic_operator_learning_target_contract`
   - `ch19e_dpf_hmc_target_suitability`
   - `ch19f_dpf_debugging_crosswalk`
3. The survey's article scaffolding---title, abstract, preamble, inline
   bibliography, appendix-style source map---must not be imported verbatim.
4. Taxonomy, validation, and code-availability material should be distributed to
   the chapters that already own implementation risk, target consequences, and
   promotion doctrine rather than becoming a new omnibus chapter.

## Foundation retained directly

### `docs/chapters/ch19b_dpf_literature_survey.tex`
Retain as the broad DPF literature and particle-flow backdrop chapter.

Owns:
- DPF family positioning,
- particle-flow context before proposal correction,
- broad literature framing before OT specialization.

Source migration policy:
- only light OT survey transplant here,
- use the standalone survey mainly to sharpen transitions into `ch19c` and the
  OT block, not to rewrite the whole chapter.

### `docs/chapters/ch32a_soft_differentiable_resampling.tex`
Retain as the non-OT differentiable resampling baseline.

Owns:
- soft/differentiable resampling as a distinct relaxation family,
- bias-versus-differentiability framing before OT.

Source migration policy:
- the scalable-OT survey does not replace this chapter,
- only add contrast language if needed so the OT block is clearly separated from
  non-OT smooth resampling.

## Target destination chapters from survey source truth

### Destination: PF-PF / LEDH-to-OT insertion point
**Target chapter file:**
- `docs/chapters/ch19c_dpf_implementation_literature.tex`

**Primary survey source sections:**
- `The LEDH-PFPF-OT Computation Problem`
- `Particle-flow context`
- `Why a scalar OT value is not enough`

**Should own:**
- the precise insertion point of OT resampling after PF-PF/LEDH weighting,
- the statement that BayesFilter needs a usable transport object rather than an
  OT scalar alone,
- the handoff from weighted post-flow clouds to equal-weight transport layers,
- the distinction between Li--Coates PF-PF source behavior and BayesFilter OT
  extensions layered on top.

**Migration class:**
- core math and bridge material.

### Destination: deterministic OT equal-weighting baseline
**Target chapter file:**
- `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`

**Primary survey source sections:**
- `Why a scalar OT value is not enough`
- the deterministic parts of `Discrete OT and Entropic Sinkhorn Basics`

**Should own:**
- weighted empirical measure versus equal-weight target measure,
- transport object language: coupling, barycentric projection, transported
  cloud,
- finite deterministic OT equal-weighting as the first explicit OT baseline,
- the distinction between deterministic OT equal-weighting and categorical
  resampling.

**Migration class:**
- core math and orientation.

### Destination: entropic OT and semantics-preserving reference lane
**Target chapter file:**
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`

**Primary survey source sections:**
- `Discrete OT and Entropic Sinkhorn Basics`
- `Exact Online and GPU Sinkhorn Methods`
- exact-semantics parts of `Accelerated Sinkhorn` discussion

**Should own:**
- entropic regularization and its exact mathematical effect,
- finite Sinkhorn as the declared numerical teacher object,
- barycentric projection from finite couplings,
- exact-online / streaming / GPU Sinkhorn as the semantics-preserving scalable
  reference lane,
- explicit statement of what counts as preserving the entropic teacher object
  versus changing it.

**Migration class:**
- core math, teacher-object discipline, and implementation-facing exact-scaling
  reference material.

### Destination: retained-teacher approximate/factored acceleration families
**Target chapter file:**
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`

**Primary survey source sections:**
- `Nystrom Kernel Sinkhorn`
- `Positive-Feature Sinkhorn`
- `Direct Low-Rank Coupling Optimal Transport`
- approximation-facing parts of `Sparse and Screened Methods`
- approximation-facing parts of `Accelerated, Greedy, and Stochastic Sinkhorn`
- `Stochastic and Minibatch Optimal Transport`

**Should own:**
- scalable families that are most naturally interpreted as teacher
  approximations, warm starts, compressed entropic solves, or retained-teacher
  accelerators,
- the distinction between predicting or compressing teacher structure versus
  redefining the final transport target,
- approximation residual and teacher-student discrepancy language,
- first implementation-bearing scalable candidates after exact online Sinkhorn.

**Migration class:**
- approximation taxonomy, retained-teacher acceleration, and implementation-risk
  framing.

### Destination: direct-map / learned-map boundary families
**Target chapter file:**
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`

**Primary survey source sections:**
- map-learning-relevant synthesis from `Method Taxonomy`
- any survey language distinguishing direct learned maps from retained entropic
  teachers

**Should own:**
- the transition from retained-teacher acceleration to direct learned transport
  maps,
- the warning that map-learning families answer a different target question than
  exact or approximate entropic OT,
- summary comparisons that position ICNN/Brenier/Monge-gap methods relative to
  the scalable entropic family.

**Migration class:**
- orientation and target-boundary synthesis, not the whole scalable survey.

### Destination: dynamic path / operator learners and replacement semantics
**Target chapter file:**
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`

**Primary survey source sections:**
- `Sliced and Subspace OT`
- `Localization and Particle-Filter Structure`
- replacement-facing parts of `Sparse and Screened Methods`
- broader target-contract synthesis from `Method Taxonomy`

**Should own:**
- families that are better interpreted as explicit new transport or resampling
  methods rather than compressed versions of the same entropic teacher,
- localization, block structure, sliced/subspace OT, and operator-style methods
  as target-changing or structure-changing candidates,
- the stronger target-contract burden attached to dynamic, operator, and
  replacement transport objects.

**Migration class:**
- target-contract and semantic-replacement doctrine.

### Destination: HMC target-status consequences
**Target chapter file:**
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`

**Primary survey source sections:**
- HMC-relevant pieces of `Method Taxonomy`
- HMC-relevant pieces of `Validation Ladder Before Any Default Change`
- HMC-relevant non-claims from `Conclusions`

**Should own:**
- which scalable OT families can still be treated as coherent relaxed targets if
  value-gradient parity holds,
- which families are only learned/replacement targets unless separately
  corrected,
- explicit warnings that exact online Sinkhorn, approximate entropic families,
  and replacement/localized/sliced families occupy different target-status
  classes.

**Migration class:**
- target taxonomy and HMC consequence boundaries.

### Destination: debugging, code availability, validation, and promotion doctrine
**Target chapter file:**
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`

**Primary survey source sections:**
- `Code Availability and Reuse Risk`
- `Recommended Research Program`
- `Validation Ladder Before Any Default Change`
- implementation-facing parts of `Conclusions`

**Should own:**
- code-availability and reuse-risk summaries,
- research sequencing for exact-online, retained-teacher approximate, and
  replacement-family lanes,
- validation ladder and promotion doctrine,
- explicit non-claims for default-readiness, HMC-readiness, and posterior
  fidelity from literature-only evidence.

**Migration class:**
- implementation-risk note, validation doctrine, and promotion logic.

## Distributed summary material

### `Method Taxonomy`
Do **not** make this a standalone monograph chapter.

Distribute as summary tables or chapter-end comparison blocks across:
- `ch32c` for exact/teacher-preserving scalable routes,
- `ch32d` for retained-teacher approximate families,
- `ch32f` for target-changing/replacement families,
- `ch19e` / `ch19f` for target-status and promotion consequences.

### `Conclusions`
Do not import as a standalone conclusion chapter.

Distribute:
- technical conclusions to `ch32c`--`ch32f`,
- target-status non-claims to `ch19e`,
- implementation/program conclusions to `ch19f`.

## Provenance-only or exclude-from-body material

### Article-class front matter
- title
- author
- abstract
- article-specific evidence-contract table presentation

Use only as drafting guidance.  Do not import verbatim into reader-facing chapter
prose.

### Inline `thebibliography`
Migrate citations into `docs/references.bib` after key-conflict and
claim-support audit.  Do not keep chapter-local bibliography blocks.

### `Local Source Map` and incomplete-download note
Treat as provenance only.

Destination:
- `docs/source_map.yml`
- monograph appendix source-map machinery via `appendices/app_f_source_map`

Do not keep this material as chapter-body exposition.

## Salvage-only chapter set

### Current DPF/OT block contents (salvage only where overwritten)
- `docs/chapters/ch19c_dpf_implementation_literature.tex`
- `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
- `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`
- `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`

Use current contents only for:
- notation harmonization,
- cross-reference scaffolding,
- already repaired claim-discipline text,
- reusable tables/equations that remain consistent with the survey source truth.

Do not assume transitional current wording is the final source truth where the
standalone survey is intended to deepen or replace it.

## Staging principle

Canonical `docs/main.tex` may switch only after:
1. a DPF/OT staging driver exists,
2. the survey-to-chapter migration is complete on that staging surface,
3. bibliography and source-map integration are finished,
4. the whole DPF/OT block passes compile and narrative audit,
5. target-status and validation-language audits pass.

## Verification gates for this crosswalk

1. **Crosswalk completeness**
   - every survey section/subsection has a destination or exclusion decision.

2. **Staging compile gate**
   - no undefined citations,
   - no undefined references,
   - no duplicate labels,
   - no article-only scaffolding remaining in staged chapter files.

3. **Bibliography gate**
   - source-audited keys merged into `docs/references.bib`,
   - no duplicate/conflicting citation keys,
   - no chapter-local `thebibliography` left behind.

4. **Source-map gate**
   - `docs/source_map.yml` records the standalone survey as donor provenance,
   - lineage into final revised DPF/OT chapters is explicit.

5. **Narrative gate**
   - the resulting staged block reads as one monograph treatment,
   - OT preliminaries are not duplicated across `ch32b` and `ch32c` unless
     deliberately tiered,
   - taxonomy tables support the chapter roles rather than repeating the survey.

6. **Claim-discipline gate**
   - exact-online entropic routes remain clearly separated from approximate
     retained-teacher routes,
   - retained-teacher routes remain clearly separated from replacement /
     target-changing families,
   - no unsupported claims of exactness, convergence, unbiasedness,
     posterior-validity, or HMC-default readiness.
