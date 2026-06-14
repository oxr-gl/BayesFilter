# P25 Zhao--Cui Chair And Implementation Bridge Result

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.
- P24 Zhao--Cui human-facing companion note.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No adaptive global differentiability claim.
- No production implementation claim.
- No empirical validation claim.
- No final panel endorsement claim.

## Status

decision: `LOCAL_VALIDATION_PASS_BOUNDED_CLAUDE_REVIEW_ACCEPTED_PATCHED`

P25 produced an expanded chair-facing and implementation-facing companion note
and PDF.  Local validation passed.  Two file-inspection Claude execution-review
attempts stalled, but a bounded excerpt review completed with
`ACCEPT_WITH_MINOR_RESIDUALS`; Codex accepted and patched all minor residuals.

## Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf`
- P25 ledgers under `docs/plans/*p25-zhao-cui*2026-06-02.md`

## Build And Size Status

- P24: 6518 TeX lines and 73 PDF pages.
- P25 before bounded-review patches: 7422 TeX lines and 83 PDF pages.
- `latexmk` built the P25 PDF successfully.
- LaTeX log scan found no undefined references, undefined citations, rerun
  blockers, missing files, or fatal errors.
- Remaining layout issues are small overfull/underfull boxes.

## Five Gap Closure

| Gap | P25 section |
|---|---|
| Chair Bayesian-to-TT plausibility bridge | `From Bayesian Filtering To A Tensor-Train Approximation Family` |
| One observation-step coordinate walkthrough | `One Observation Step Through All Coordinate Systems` |
| Gradient teaching layer | `Gradient Teaching Layer: What Is Differentiated` |
| Less-toy numerical trace | `A Less-Toy Two-Point Basis Trace` |
| Consolidated implementation protocol | `Consolidated Fixed Least-Squares Lane` |

## Validation Commands Run

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex
pdftotext \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf \
  /tmp/p25_zhao_cui_text.txt
pdfinfo \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.pdf
wc -l \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex
rg -n "undefined|Undefined|Citation.*undefined|Reference.*undefined|Rerun to get|No file|LaTeX Warning|Package natbib Warning|Fatal|Emergency stop|missing|Missing" \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.log
rg -n "Codex|Claude|ledger|artifact|governance|allowed writes|execution review|review loop|source coverage summary|DPF lane|student-baseline|controlled-DPF|public API|public-API|P24|P23|P22|P21|P20|P19|Source unit|source unit|Implementation contract|Mini implementation contract" \
  /tmp/p25_zhao_cui_text.txt
rg -n "From Bayesian Filtering To A Tensor-Train Approximation Family|One Observation Step Through All Coordinate Systems|Gradient Teaching Layer|A Less-Toy Two-Point Basis Trace|Consolidated Fixed Least-Squares Lane" \
  /tmp/p25_zhao_cui_text.txt
rg --files-without-match "metadata_date:" docs/plans/*p25-zhao-cui*2026-06-02.md
rg --files-without-match "seed_papers:" docs/plans/*p25-zhao-cui*2026-06-02.md
rg --files-without-match "what_is_not_concluded:" docs/plans/*p25-zhao-cui*2026-06-02.md
git diff --check -- docs/plans/*p25-zhao-cui*2026-06-02.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p25-zhao-cui-chair-implementation-bridge-note-2026-06-02.tex
```

## Claude Review History

- Plan review iteration 1: `ACCEPT`.
- Execution review iteration 1: stalled with no output and was stopped.
- Execution review iteration 2: narrower file-inspection review stalled with
  no output and was stopped.
- Claude health check: `CLAUDE_HEALTHCHECK_OK`.
- Execution review iteration 3: bounded excerpt review completed with
  `ACCEPT_WITH_MINOR_RESIDUALS`.

## Codex Audit Classifications

- `ACCEPT`: Claude plan residual risks were materially correct but not
  plan-blocking; controls are recorded in the plan and five-gap ledger.
- `CLARIFY`: Claude execution review produced no substantive findings to
  classify for iterations 1--2 because file review stalled.
- `ACCEPT`: Claude bounded-review minor residuals were materially correct and
  patched:
  - anti-overclaim language for TT-rank plausibility;
  - reference/physical measure-bookkeeping equation;
  - shape/flattening/mass-contraction ledger for the fixed least-squares lane;
  - numeric trace verification equations.

## Remaining Gaps

- A real former-chemist chair has not reviewed P25.
- A real implementation engineer has not attempted an implementation from P25.
- No executable prototype or empirical validation was produced by design.
- Claude completed only bounded excerpt review, not full-document machine
  certification.

## Final Estimate

Conditional on later external review not finding new blockers, Codex estimates
a 0.83 probability that P25 passes a skeptical mixed chemistry/numerical/
implementation panel as a companion note.
