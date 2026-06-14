# P18 Zhao--Cui True Annotation Result

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.
- P15 fixed-branch implementation contract.
- P17 full-equation reconstruction note and ledgers.

what_is_not_concluded:
- No production BayesFilter implementation claim.
- No posterior accuracy or HMC convergence claim.
- No claim that adaptive TT-cross/rank/pivot/domain choices are globally
  differentiable.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Decision

`P18_ACCEPTED_AFTER_CLAUDE_REVIEW_LOOP`.

P18 addresses the eight main issues by replacing the summary-like P17 style
with a source-order annotated companion to Zhao--Cui Sections 1--3 and 5,
followed by a separated BayesFilter fixed-branch derivative extension.

## What Codex Inspected

- P18 plan, note, ledgers, review ledger, equation-count ledger, and PDF.
- P17 inventory/result artifacts as the negative baseline.
- P10 code audit/crosswalk context and local Zhao--Cui source availability.
- Scholarly literature audit policy and the project review requirements.

## P17 Failure Found

P18 explicitly records that P17 was still too summary-like: it tracked many
numbered equations but collapsed source units, displayed support formulas, and
Algorithm 5 details.  P18's repair was to inventory source units, teach them in
paper order, and require derivation plus implementation meaning for each major
formula.

## Equation Count

- Zhao--Cui source baseline for Sections 1--3 and 5: 32 numbered equations
  from Eqs. (1)--(26) and (30)--(35).
- Required P18 count before fixed-branch boundary: `ceil(1.2 * 32) = 39`.
- Corrected P18 counted equations from Sections 1--3 and 5 before the boundary:
  `135`.
- Decision: `EQUATION_COUNT_GATE_PASS_135_GE_39`.

Equation count is treated as a necessary guardrail, not correctness evidence.

## Claude Review History

- Plan review iteration 1: `REJECT`; Codex classified all findings `ACCEPT`
  and hardened the plan.
- Execution review iteration 1: `REJECT`; Codex classified five findings
  `ACCEPT` and one `PARTIAL`, then patched the note and ledgers.
- Execution review iteration 2: `REJECT`; Codex classified all three findings
  `ACCEPT`, split Algorithm 5 inventory rows, excluded Section 4 from the count
  gate, and added P16b.1--P16b.4.
- Execution review iteration 3: `ACCEPT`; no surviving veto findings.

## Codex Audit Classification Summary

- `ACCEPT`: all plan findings, all execution-2 findings, and all but one
  execution-1 finding.
- `PARTIAL`: one execution-1 theorem-assumption finding; Codex added local
  assumption boxes rather than attempting to reprove external Cui--Dolgov
  theorems.
- `DISPUTE`: none.
- `CLARIFY`: none.

## Files Changed

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-plan-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-inventory-ledger-2026-06-01.md`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex`
- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf`
- P18 source-support, citation/venue, backward/forward snowball, claim-support,
  omitted-risk, section source-unit, equation-count, eight-issue,
  fixed-branch-gradient, Claude-review, discrepancy, and result ledgers under
  `docs/plans/`.

No chapters, production code, DPF lane, student-baseline, controlled-DPF, or
public APIs were intentionally edited.

## PDF Build And Validation

PDF: `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf`

Validation commands run:

- `latexmk -cd -pdf -interaction=nonstopmode -halt-on-error docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex`
- `git diff --check -- docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-*.md`
- `rg -n "Warning|undefined|Citation|Reference|Rerun|Overfull|Underfull|Error|Missing" docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.log`
- `pdftotext docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotated-companion-note-2026-06-01.pdf - | rg -n "P16b\\.1|P16b\\.2|conditional pushforward|Algorithm 5\\(b\\.1\\)|Fixed-Branch|finite-difference|Equation|Preconditioning"`

Status:

- PDF builds successfully.
- `git diff --check` passes.
- LaTeX log scan found no undefined references, citation warnings, missing
  files, or real rerun blockers.
- `pdftotext` confirms the new conditional-pushforward derivation, Algorithm 5,
  fixed-branch section, finite-difference protocol, and preconditioning content
  are present.

## Remaining Self-Containedness Gaps

- External theorem proofs remain delegated to cited sources and are boxed as
  assumptions.
- Section 4 error propagation and Section 6 numerical examples are not fully
  reconstructed in P18; that is outside this plan's scope.
- Empirical validation and production implementation remain separate.

## Chemistry Persona

Claude's final chemistry persona was satisfied for veto purposes.  The persona
could teach back the Section 5.4 bridge argument after P16b.1--P16b.4 and found
Zhao--Cui plausible as a high-dimensional filtering method, while still noting
that success depends on ranks, conditioning, and model diagnostics.

## Probability Estimate

Final Codex estimate that the P18 note passes a skeptical mixed
numerical/implementation/chemistry panel as an annotated mathematical companion:
`0.78`.

The probability is below `0.9` because the note still delegates external theorem
proofs and does not include empirical validation, but it is now substantially
more self-contained and reviewable than P17.
