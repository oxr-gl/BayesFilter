# P24 Zhao--Cui Human-Facing Companion Result

metadata_date: 2026-06-02

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter
  Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse
  Rosenblatt Transports."
- Oseledets, "Tensor-Train Decomposition," SIAM Journal on Scientific
  Computing, 2011.
- Rosenblatt, "Remarks on a Multivariate Transformation," 1952.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross/rank-changing
  decisions.
- No production implementation claim.
- No empirical validation claim.
- No final panel endorsement claim.

## Status

decision: `LOCAL_VALIDATION_PASS_FORMAL_ACCEPTANCE_BLOCKED_BY_CLAUDE_REVIEW_TOOLING`

P24 produced a human-facing companion note and PDF.  Local Codex validation
passed after provenance-ledger patches.  Formal P24 acceptance remains blocked
because Claude execution-review prompts that read project files stalled and did
not return findings, even though a minimal Claude worker smoke test succeeded.

## Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf`
- P24 ledgers under `docs/plans/*p24-zhao-cui*2026-06-02.md`

## Build Status

- `latexmk` built the PDF successfully.
- PDF page count: 73 pages.
- P23 TeX line count: 5966.
- P24 TeX line count after final patch pass: longer than P23.
- LaTeX log has no undefined citation or undefined-reference warnings.
- Remaining log warnings: two small overfull boxes.

## Validation Commands Run

```bash
latexmk -cd -pdf -interaction=nonstopmode -halt-on-error \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex
pdftotext \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf \
  /tmp/p24_zhao_cui_text.txt
pdfinfo \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.pdf
rg -n "undefined|Undefined|Citation|Reference.*undefined|Rerun to get|No file|LaTeX Warning|Package natbib Warning|Overfull|Fatal|Emergency stop|missing|Missing" \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.log
rg -n "Codex|Claude|ledger|artifact|governance|allowed writes|execution review|review loop|source coverage summary|DPF lane|student-baseline|controlled-DPF|public API|public-API|P23|P22|P21|P20|P19|Source unit|source unit|Implementation contract|Mini implementation contract" \
  /tmp/p24_zhao_cui_text.txt
rg --files-without-match "metadata_date:" docs/plans/*p24-zhao-cui*2026-06-02.md
rg --files-without-match "seed_papers:" docs/plans/*p24-zhao-cui*2026-06-02.md
rg --files-without-match "what_is_not_concluded:" docs/plans/*p24-zhao-cui*2026-06-02.md
git diff --check -- \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-note-2026-06-02.tex \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-plan-2026-06-02.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-human-facing-companion-result-2026-06-02.md \
  docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p24-zhao-cui-claude-review-ledger-2026-06-02.md \
  docs/references.bib
```

## Claude Review History

- Plan review iteration 1: `REJECT`; Codex accepted all four findings and
  patched the plan with required scholarly-audit ledgers, source-status
  controls, snowballing/omission controls, and exact claim-anchor controls.
- Plan review iteration 2: `ACCEPT`.
- Execution-review attempt 1: stalled with no output.
- Execution-review attempt 2: stalled with no output.
- Claude worker smoke test: returned `ACCEPT / smoke test complete`.
- Execution-review attempt 3: compact file-review prompt also stalled with no
  output.

## Codex Audit Classifications

- `ACCEPT`: Source-support ledger omitted cited Oseledets and Rosenblatt
  sources; patched with source rows and allowed/forbidden claims.
- `ACCEPT`: Source/version/retraction wording was too compressed; patched to
  record local provenance and live-lookup blockers honestly.
- `ACCEPT`: Forward-snowball wording was too flat; patched into a
  scope-limited blocker table.
- `CLARIFY`: Claude execution review produced no substantive findings to
  classify because file-review prompts stalled.

## Human-Facing Readability Status

Local scan found no visible process/governance terms, no old audit equation
tags, and no visible P19--P23 labels in the PDF.  The note now contains the
chair sections on moderate TT-rank plausibility, coordinate systems, and the
narrow usefulness of the fixed-branch gradient.

Remaining gap:

- A real former-chemist chair has not reviewed the PDF.  Codex estimates the
  note is much more readable than P23, but the gradient section remains
  intrinsically demanding.

## Implementation-Math Status

The note contains the end-to-end fixed-branch squared-TT filter, deterministic
rank ladder, stabilization defaults, saved branch manifest, two-time-step
trace, derivative pass, and finite-difference protocol.

Remaining gap:

- No executable prototype was produced or tested in P24 by design.  The
  implementability claim is mathematical-specification readiness, not code
  readiness.

## Final Estimate

Conditional on a successful external review not finding new blocking issues,
Codex estimates a 0.72 probability that P24 would pass a skeptical mixed
chemistry/numerical/implementation panel as a companion note.  Because Claude
execution review did not complete, formal plan acceptance remains blocked.
