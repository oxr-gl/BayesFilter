# P26 Zhao--Cui Panel-Readable Implementation Result

metadata_date: 2026-06-03

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P25 Zhao--Cui chair and implementation bridge note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No real panel endorsement claim.

## Status

decision: `ACCEPT_WITH_CAVEATS`

## Execution Summary

Created and built the P26 panel-readable implementation note:

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.pdf`

P26 preserves P25 and expands it: P25 has 7516 TeX lines; P26 has 8371 TeX
lines after the final patch.

## Added For The Former Chemistry Academic Chair

- Added a physical/high-dimensional rank example using local sensor/polymer or
  reaction-coordinate interactions and cross-split interaction width.
- Added `Why This Transport Is The Right Device`, deriving KR transport from
  the one-dimensional probability-integral transform through triangular
  conditional inversions.
- Added `Why Preconditioning And KR Maps Belong Together`, explaining bridge
  geometry, residual density, KR inversion, and proposal construction.
- Added `The Story Of The Fixed-Branch Derivative` before Proposition 2.
- Expanded the numerical trace with a two-step evidence table and a
  finite-difference comparison table.

## Added For Implementation Readiness

- Added a boxed fixed-branch filter-and-derivative algorithm with inputs,
  outputs, invariants, failure exits, and derivative recursions.
- Added explicit alternating-sweep recomputation equations for
  \(L,R,A,N,d\) and dotted counterparts, including stale-cache conditions.
- Added retained-filter storage for multidimensional \(z_t\), including dense,
  TT evaluator, and low-rank options.
- Added retained-filter compression diagnostics for normalization drift,
  derivative-mass drift, compression residuals, and query mismatch.
- Expanded the defaults table to explicitly include \(\lambda_t,\tau_t,c_t\),
  floor/ridge/threshold/tolerance terms, compression tolerances, and the
  finite-difference schedule.

## Claude Review

- Plan review iteration 1: `REVISE`; Codex classified all findings as
  `ACCEPT` and patched the plan controls.
- Execution review iteration 1: `REVISE`; Codex classified findings as
  `ACCEPT` or `PARTIAL` and patched the note/ledgers.
- Execution review iteration 2: `REVISE`; Codex classified all remaining
  findings as `ACCEPT` and patched human-facing wording.
- No Claude finding was disputed.

## Validation

Commands run:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p26-zhao-cui-panel-readable-implementation-note-2026-06-03.tex`
- `rg -n "undefined|Citation.*undefined|There were undefined|Label\\(s\\) may have changed|Rerun to get|No file|Missing" docs/plans/...p26...note-2026-06-03.log`
- `pdftotext docs/plans/...p26...note-2026-06-03.pdf - | rg -n "<new-section-and-forbidden-term-scan>"`
- `git diff --check -- <P26 files>`
- custom scan for labeled equations inside unnumbered `\[...\]` displays
- `wc -l` comparison between P25 and P26

Validation status:

- PDF build: `PASS`, 93 pages.
- Undefined references/citations: `PASS`, none in final log scan.
- Numbered-equation audit: `PASS`, no labeled equations inside unnumbered
  display blocks.
- Human-facing forbidden-term scan in rendered PDF: `PASS`.
- `git diff --check`: `PASS`.
- P25 preservation size gate: `PASS`, P26 is larger than P25.
- Write scope: `PASS`, intentional new/updated P26 files are under
  `docs/plans/`; unrelated dirty files were not edited.

## Remaining Caveats

- P26 is still a mathematical note, not an empirical validation or production
  implementation.
- The finite-difference table is synthetic and illustrates the required
  diagnostic format; it is not a run result.
- Moderate TT rank remains a model- and coordinate-dependent hypothesis that
  must be checked by diagnostics.
- The fixed-branch gradient differentiates the declared fixed scalar, not the
  globally adaptive Zhao--Cui algorithm.
