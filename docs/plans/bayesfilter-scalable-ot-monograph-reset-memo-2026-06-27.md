# Reset memo: scalable OT monograph drift and document-state diagnosis

## Date
2026-06-27

## Context
This memo is for a fresh agent resuming work on the BayesFilter OT/scalable-OT
monograph sequence after several intertwined passes:
- survey-to-monograph crosswalk audit,
- chapter restoration,
- citation restoration,
- OT-block citation expansion,
- bibliography normalization,
- and a narrative decompression pass.

The conversation drifted because the work changed character several times:
first audit, then restoration, then citation repair, then readability repair.
The user explicitly signaled that something felt wrong: the monograph still felt
incomplete and denser than the standalone scalable-OT note. That concern is
substantively valid.

## Decision / policy
Future sessions should assume the following and not re-litigate them without new
instruction:
- The OT/scalable-OT material should stay integrated into the existing monograph
  chapter sequence; do **not** create a new standalone survey chapter block by
  default.
- Citation correctness and completeness are mandatory for literature-facing
  claims.
- The current problem is no longer “missing all the material”; it is now a mix
  of:
  1. partial compression of survey-style exposition into monograph-style local
     chapters,
  2. broader document-state ambiguity from many accumulated changes,
  3. and the need for cleaner separation between technical restoration,
     bibliography normalization, and pedagogical decompression.
- Do **not** mix this document-state repair with algorithm benchmarking or
  unrelated research execution.

## What changed
### Audit and mapping artifacts added
- File: `docs/plans/bayesfilter-dpf-ledh-pfpf-ot-survey-to-monograph-crosswalk-audit-2026-06-26.md`
  - Added a retained/partial/missing crosswalk between the standalone survey and
    the current monograph sequence.
  - Identified that the survey had been redistributed rather than integrated as a
    self-contained block.

### OT/scalable-OT chapter restoration work
- File: `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
  - Added bottleneck framing, exact-online/GPU reference-lane material, and
    solver-family boundary discussion.
- File: `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
  - Added Nyström, positive-feature, low-rank, and stochastic/minibatch family
    material.
- File: `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`
  - Added taxonomy table, code-availability/reuse-risk table, research-order
    subsection, and OT synthesis.

### Broader OT-block citation repair work
- File: `docs/chapters/ch32a_soft_differentiable_resampling.tex`
  - Added differentiable-resampling citations.
- File: `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
  - Added foundational OT and ensemble-transform citations.
- File: `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
  - Added Brenier / ICNN / Monge-gap / direct-map family citations.
- File: `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
  - Added dynamic geodesic, operator-learning, and sliced/subspace family
    citations.
- File: `docs/chapters/ch19e_dpf_hmc_target_suitability.tex`
  - Added OT/EOT, soft-resampling, learned-OT, and surrogate-HMC comparison
    citations.
- File: `docs/references.bib`
  - Added a large scalable-OT bibliography slice and normalized several OT
    proceedings/preprint entries while preserving citation keys.

### Decompression / readability work
- File: `docs/chapters/ch19c_dpf_implementation_literature.tex`
  - Added a PF-PF -> OT bridge subsection.
- File: `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
  - Added an OT-block roadmap table.
- File: `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
  - Added a derivative-object comparison table.
- File: `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
  - Added a motivating retained-teacher paragraph and a comparison table.
- File: `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
  - Added roadmap/bridge prose and a direct-map comparison table.
- File: `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
  - Added a family-comparison table, taxonomy-to-audit bridge, and OT-block
    takeaway paragraph.
- File: `docs/chapters/ch19f_dpf_debugging_crosswalk.tex`
  - Added a bridge from source/implementation mapping into scalable-OT reuse and
    promotion doctrine.

## Bugs / blockers resolved
- Symptom: literature-facing scalable-OT claims in restored OT chapters lacked
  explicit citations.
- Root cause: the initial restoration pass focused on concept recovery before
  restoring the full citation apparatus.
- Resolution: added compact family-appropriate citations at first
  literature-facing claims and expanded `docs/references.bib` with the missing
  scalable-OT entries.

- Symptom: many OT/scalable-OT references cited in the restored chapters were
  undefined during intermediate builds.
- Root cause: the standalone survey carried a richer citation inventory than the
  checked-in `docs/references.bib`.
- Resolution: added the missing bibliography entries and forced BibTeX rebuilds.

- Symptom: the restored OT block still felt much denser than the previous
  standalone note.
- Root cause: the material had been redistributed into monograph chapters with
  their own local responsibilities, losing some of the survey’s framing,
  transitions, and one-glance taxonomy/conclusion devices.
- Resolution: added a limited decompression layer (roadmaps, bridges,
  comparison tables, synthesis paragraphs) without reopening the mathematical
  content.

## Verification already run
```bash
# Page-count comparisons
pdfinfo docs/main.pdf | grep '^Pages:'
git show HEAD~1:docs/main.pdf > /tmp/bayesfilter-main-before.pdf
pdfinfo /tmp/bayesfilter-main-before.pdf | grep '^Pages:'

# OT/scalable-OT diff summaries
git diff --stat -- docs/chapters/ch19c_dpf_implementation_literature.tex \
  docs/chapters/ch19e_dpf_hmc_target_suitability.tex \
  docs/chapters/ch19f_dpf_debugging_crosswalk.tex \
  docs/chapters/ch32a_soft_differentiable_resampling.tex \
  docs/chapters/ch32b_deterministic_ot_equalweighting.tex \
  docs/chapters/ch32c_entropic_ot_sinkhorn.tex \
  docs/chapters/ch32d_retained_teacher_neural_ot.tex \
  docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex \
  docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex \
  docs/references.bib

git diff --numstat -- docs/chapters/ch19c_dpf_implementation_literature.tex \
  docs/chapters/ch19e_dpf_hmc_target_suitability.tex \
  docs/chapters/ch19f_dpf_debugging_crosswalk.tex \
  docs/chapters/ch32a_soft_differentiable_resampling.tex \
  docs/chapters/ch32b_deterministic_ot_equalweighting.tex \
  docs/chapters/ch32c_entropic_ot_sinkhorn.tex \
  docs/chapters/ch32d_retained_teacher_neural_ot.tex \
  docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex \
  docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex \
  docs/references.bib

# Forced rebuilds with BibTeX
cd /home/chakwong/BayesFilter/docs
latexmk -pdf -g -interaction=nonstopmode -halt-on-error main.tex

# Log scans for undefined citations / errors
python ... scan build log for "undefined citation" and hard errors

# BibTeX sanity checks
cat docs/main.blg
```

Observed:
- The monograph page count moved from **333** (pre-OT restoration baseline used
  in this session) to **340** after the OT restoration/citation work, and then to
  **342** after the decompression pass.
- The OT/scalable-OT work is substantial in source terms, with the main growth in:
  - `ch32c`
  - `ch32d`
  - `ch19f`
  - `references.bib`
- Forced BibTeX rebuilds completed successfully and the generated `main.bbl`
  contains the newly added OT/scalable-OT references.
- The final rebuild succeeded and produced `docs/main.pdf` at **342 pages**.
- Remaining warnings are predominantly layout/box warnings rather than hard
  citation failures.

## Current policy
- Treat the current OT block as **substantively restored but still pedagogically
  imperfect**.
- The strongest remaining issue is not raw absence of OT families; it is that the
  monograph still does not feel as self-contained or survey-like as the standalone
  scalable-OT note.
- `ch32b` and `ch19c` now serve as the strongest front-door / bridge chapters.
- `ch32e` remains the densest chapter in the OT block and is the strongest
  candidate for any future narrowly scoped readability cleanup.
- `ch32c` remains the next-densest because it still compresses several subtle
  distinctions (teacher object, finite object, engineering route, derivative
  target) into one chapter.

## Known limitations / cautions
- The OT block is now more complete and better cited, but it is still spread over
  multiple differently-purposed monograph chapters. It should not be described as
  equivalent in readability to the original standalone survey.
- The broader working tree has many unrelated dirty changes and plan/result files.
  OT-specific document work should stay narrowly scoped to the touched chapters and
  bibliography unless the user explicitly broadens the task.
- `docs/references.bib` now contains a larger OT/scalable-OT slice, but broader
  bibliography consistency outside that slice has not been normalized.
- The sequence still carries some layout pressure (tables, underfull/overfull box
  warnings), especially in the dense doctrine chapters.
- The current page-count diagnosis is session-relative. It explains the changes
  introduced in this sequence of passes, but it does not by itself settle any
  larger historical compression that may predate the current branch state.

## Suggested next steps
1. **Do not continue broad monograph drifting work blindly.**
   First read the touched OT chapters in order and decide whether the user wants:
   - a final narrow readability cleanup of `ch32e` (and maybe `ch32c`), or
   - to stop and preserve the current state.

2. **If doing one more readability pass, keep it extremely narrow.**
   Limit it to:
   - `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
   - optionally `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
   with the explicit goal of reducing density, not adding new coverage.

3. **If the user instead wants diagnosis rather than more edits, produce a stable OT-block scorecard.**
   A clean next artifact would be a short note rating each OT chapter on:
   - completeness,
   - readability,
   - self-containedness,
   - citation sufficiency,
   so a future agent can see where the real remaining weakness is without redoing
   all the exploratory work.

4. **Avoid re-opening the bibliography globally unless asked.**
   The OT/scalable-OT slice is now functional; a broader bibliography cleanup is a
   separate task.
