# P20 Zhao--Cui Integrated Companion And Gradient Result

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank/pivot/domain
  choices.
- No HMC convergence claim.
- No production implementation readiness claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Decision

Decision: `P20_ACCEPTED_AS_INTEGRATED_P18_P19_NOTE`.

P20 was built as a true merge: P18 supplies the annotated Zhao--Cui companion
spine, and P19 supplies the chair-readable fixed-branch gradient expansion.
P20 is not a shorter supplement.

## Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.pdf`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-plan-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-merge-ledger-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-equation-and-size-ledger-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-claude-review-ledger-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-discrepancy-report-2026-06-01.md`

## Size And Merge Gates

| Quantity | Value |
|---|---:|
| P18 TeX lines | 3169 |
| P19 TeX lines | 1442 |
| P20 TeX lines | 4295 |
| P18 PDF pages | 37 |
| P19 PDF pages | 17 |
| P20 PDF pages | 50 |
| Required merge-aware line lower bound | 4249 |
| Required merge-aware page lower bound | 49 |
| Equation tags | 288 |
| Duplicate equation tags | 0 |

The line and page gates pass:
\[
4295 \ge 3169+1442-362 = 4249,
\qquad
50 \ge 37+17-5 = 49.
\]

## Claude Review History

- Plan review iteration 1: `REJECT`; Codex accepted and patched merge controls.
- Plan review iteration 2: `REJECT`; Codex accepted and patched direct P20 > P18 hard gates.
- Plan review iteration 3: `ACCEPT`.
- Execution review iteration 1: `REJECT`; Codex accepted the missing page-bound ledger finding and partially accepted the chair-readability differentiability suggestion.
- Execution review iteration 2: `ACCEPT`.

## Codex Audit Summary

Codex classified all material Claude findings as `ACCEPT` or `PARTIAL`; there
were no unresolved `DISPUTE` or `CLARIFY` items.  Accepted controls were
patched into the plan, ledgers, and note.

## Validation Summary

Validation status: `PASS`.

Commands run:
- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex`
- `git diff --check -- <P20 files>`
- direct trailing-whitespace scan over P20 markdown and TeX files
- LaTeX log scan for errors, undefined references, citation warnings, rerun blockers, missing files, and serious overfull boxes
- duplicate equation-tag scan
- PDF text anchor scan
- metadata-field scan for P20 markdown artifacts

The PDF build succeeded.  The log contains underfull hbox warnings only; no
fatal build error, undefined reference, citation warning, missing file, rerun
blocker, or overfull hbox was found in the final scan.

## Panel Probability Estimate

Estimated probability that P20 passes a skeptical mixed numerical/chemistry
panel as an integrated explanatory note: `0.78`.

The main remaining risk is not a merge defect; it is that the fixed-branch
gradient is intrinsically dense.  P20 now gives the chair a warmer path through
that density by preserving P18's annotated algorithm story and inserting P19's
stepwise derivative warmups plus the fixed ridge-sweep differentiability lemma.
