# OT block document regression reset memo

## Date
2026-06-22

## Scope of this memo
This memo is for a fresh agent whose only job is to repair the OT chapter / monograph document state.

Do **not** mix this task with further neural-OT algorithm benchmarking. The objective here is document integrity:
- citation scaffolding,
- chapter explanatory content,
- page-count regression,
- and clean LaTeX builds.

## Current state summary
### Confirmed current PDF state
- Current working-tree PDF:
  - `docs/main.pdf`
  - page count: **314**
- Separate clean comparison build from `origin/main`:
  - built in `/tmp/bayesfilter-main-compare/docs/main.pdf`
  - page count: **319**

This means:
- the current local tree is only about **5 pages shorter than `origin/main`**,
- but `origin/main` itself is still far shorter than the user expects (~360–370 pages),
- so there are **two different issues**:
  1. a small local regression,
  2. a larger pre-existing compression already on `origin/main`.

## OT-specific changes made in this session
### Files edited in the OT block
- `docs/chapters/ch32a_soft_differentiable_resampling.tex`
- `docs/chapters/ch32b_deterministic_ot_equalweighting.tex`
- `docs/chapters/ch32c_entropic_ot_sinkhorn.tex`
- `docs/chapters/ch32d_retained_teacher_neural_ot.tex`
- `docs/chapters/ch32e_icnn_brenier_monge_gap_map_learning.tex`
- `docs/chapters/ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
- `docs/references.bib`
- `docs/source_map.yml`

### Good changes from this pass
- foundational and family-level citations were restored into the OT chapters
- missing bib entries for the OT block were added:
  - `kolouri2019generalized`
  - `paty2019subspace`
  - `nguyen2025sliced`
- the OT block now has much stronger source visibility than before
- forced rebuild with BibTeX succeeded with no remaining missing-entry warnings from the OT restoration pass

### Suspicious / likely-regressive changes from this pass
The OT diff against `origin/main` showed more than citation insertion. It also replaced or removed explanatory subsections in some chapters.

Most important examples:
- `ch32d_retained_teacher_neural_ot.tex`
  - older explanatory subsections about approximation-family structure were replaced by a shorter recent-literature subsection and table
- `ch32e_icnn_brenier_monge_gap_map_learning.tex`
  - a conceptual “direct-map families as a different scalable-OT answer” subsection was removed and replaced by shorter recent-work framing
- `ch32f_dynamic_geodesic_operator_learning_target_contract.tex`
  - the earlier sliced/subspace/localization discussion was replaced by shorter recent-literature framing and a compact table

These replacements may have reduced page count and may also have hurt pedagogy, even though the new literature framing is useful.

## Key diagnosis
### What is *not* the main problem
- The OT block is present in the PDF and starts around page 138.
- The OT chapters themselves are not the main source of the huge missing-page gap.

### What *is* the likely local regression
- Some OT explanatory material appears to have been replaced rather than augmented.
- That likely accounts for a few pages of local shrinkage and some loss of explanatory depth.

### What is the larger document problem
The part-by-part audit of the current and comparison PDFs shows that the later parts are already very compressed on `origin/main`.

Approximate part starts in current PDF:
- High-Dimensional Nonlinear Filtering: p. 192
- HMC, Geometry, and Diagnostics: p. 260
- Industrial Applications and Case Studies: p. 271
- Appendices: p. 287

Approximate part starts in `origin/main` comparison PDF:
- High-Dimensional Nonlinear Filtering: p. 198
- HMC, Geometry, and Diagnostics: p. 266
- Industrial Applications and Case Studies: p. 277

This means the larger missing-pages issue is mainly downstream of the OT block.

## Files / parts most likely responsible for the larger missing-page gap
### Highest suspicion: HMC / Geometry / Diagnostics block
These chapters are extremely short in the current PDF and also in `origin/main`:
- `docs/chapters/ch21_hmc_for_state_space.tex`
- `docs/chapters/ch22_mass_matrices.tex`
- `docs/chapters/ch23_boundary_gradients.tex`
- `docs/chapters/ch24_xla_jit.tex`
- `docs/chapters/ch25_diagnostics.tex`
- `docs/chapters/ch26_transport_surrogates.tex`

### Next suspicion: Industrial / case-study block
These are also very compressed in both current and comparison builds:
- `docs/chapters/ch27_lgssm_validation.tex`
- `docs/chapters/ch28_nonlinear_ssm_validation.tex`
- `docs/chapters/ch29_nk_svd_case_study.tex`
- `docs/chapters/ch30_cip_afns_case_study.tex`
- `docs/chapters/ch31_nawm_design_target.tex`
- `docs/chapters/ch32_production_checklist.tex`

### Lower but nontrivial suspicion: local OT explanatory regression
For the OT block specifically, focus on whether to restore the removed explanatory subsections in:
- `ch32d`
- `ch32e`
- `ch32f`
while preserving the new citations and recent-work visibility.

## Recommended next steps for the fresh document-repair agent
1. Compare current OT chapter files against `origin/main` and restore any explanatory sections that were replaced rather than augmented.
2. Keep the citation improvements.
3. Rebuild and check whether the local OT block regains pages / depth.
4. Separately audit Part VI and Part VII on `origin/main` itself, since the main page-count gap is already present there.
5. Do **not** mix this task with neural-OT algorithm benchmarking.

## Suggested priority
### Priority 1
- repair OT chapter regressions in `ch32d/e/f`

### Priority 2
- audit Part VI (HMC / Geometry / Diagnostics)

### Priority 3
- audit Part VII (Industrial / case studies)

## Verification commands already used
- `pdfinfo docs/main.pdf`
- `pdftotext docs/main.pdf -`
- `git worktree add /tmp/bayesfilter-main-compare origin/main`
- `cd /tmp/bayesfilter-main-compare/docs && latexmk -pdf -bibtex -interaction=nonstopmode -halt-on-error -g main.tex`
- `git diff --stat origin/main -- docs/...`

## Recommended success criterion for the next agent
- restore any lost OT explanatory sections while keeping the stronger citations,
- isolate whether the remaining 40–50 page gap is in Part VI / VII,
- and produce a cleaner diagnosis of the larger document compression already present on `origin/main`.
