# P20 Zhao--Cui Integrated Companion And Gradient Plan

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P18 true annotated Zhao--Cui companion note and ledgers.
- P19 chair-readable fixed-branch gradient note and ledgers.

what_is_not_concluded:
- No exact posterior accuracy claim.
- No global differentiability claim for adaptive TT-cross, rank selection,
  pivot selection, changing domains, changing shifts, or changing fitting
  points.
- No HMC convergence claim.
- No production BayesFilter implementation claim.
- No empirical validation on BayesFilter target models.
- No default-method recommendation.

## Purpose

P18 is the source-order annotated Zhao--Cui companion.  P19 is a separate
chair-readable fixed-branch gradient supplement.  The user correctly noticed
that a document "building on P18" should not be shorter than P18.  P20 therefore
creates one integrated note:

1. use P18 as the base annotated reconstruction of Zhao--Cui Sections 1--3 and
   5;
2. preserve P18's source-order reconstruction and implementation meaning;
3. replace the compressed P18 fixed-branch gradient tail with the accepted P19
   chair-readable fixed-branch gradient expansion;
4. keep the integrated note as a single reader-facing PDF.

P20 must not summarize P18 or replace it with P19.  It must merge them.

## Skeptical Pre-Execution Audit

Decision: `PRE_EXECUTION_AUDIT_PASS_WITH_MERGE_CONTROLS`.

The main failure risk is accidental regression into a short supplement.  The
minimum acceptable P20 output must be longer than P18 and must contain both:

- the P18 Zhao--Cui annotated companion spine through Sections 1--3 and 5;
- the P19 chair-readable fixed-branch gradient expansion with its accepted
  design-row and carried-marginal derivations.

Other risks:

- duplicate equation tags between P18 and P19;
- duplicate or contradictory fixed-branch sections;
- losing P18's source-coverage appendix;
- losing P19's fixed-branch semantic correction that structural choices are
  frozen but fitted core values are recomputed by the same fixed fitting rule;
- producing a technically compiled PDF whose narrative still reads like two
  unrelated documents pasted together.

The plan controls these risks by using P18 as the base, importing P19 with a
distinct equation-tag prefix, and requiring a hostile review to check merge
coherence, chair readability, and same-scalar correctness.

## Evidence Contract

Question:

Can P20 produce a single integrated, chair-readable Zhao--Cui TT note that
preserves P18's annotated reconstruction and incorporates P19's accepted
fixed-branch analytical-gradient expansion without shortening, summarizing, or
regressing either document?

Baselines:

- P18 true annotated companion, 37-page PDF, 3169 TeX lines.
- P19 chair-readable gradient note, 17-page PDF, 1442 TeX lines.

Primary pass criteria:

- P20 PDF builds.
- P20 TeX source is strictly longer than P18 TeX source.
- P20 PDF page count is greater than or equal to P18 PDF page count; strict
  greater-than is preferred and must be reported if achieved.
- P20 TeX source satisfies the merge-aware lower bound
  \[
  \text{P20 lines}\ge
  \text{P18 lines}+\text{P19 lines}-\text{replaced P18 tail lines}.
  \]
- P20 PDF page count is at least the merge-aware page lower bound recorded in
  the size ledger.  The bound must use the P18 PDF page count, P19 PDF page
  count, and an explicit estimate of the replaced P18 tail's page footprint;
  the default lower bound is
  \[
  \text{P20 pages}\ge
  \text{P18 pages}+\text{P19 pages}-\text{replaced P18 tail pages}.
  \]
- P20 contains the P18 Zhao--Cui source-order reconstruction before the
  BayesFilter fixed-branch boundary.
- P20 contains the P19 chair-readable gradient warmups, full derivative pass,
  two propositions, finite-difference protocol, and minimal runnable example.
- P20 avoids duplicate equation tags.
- P20 keeps fixed-branch semantics correct: structural branch choices are
  frozen; fitted core values remain parameter-dependent outputs of the fixed
  fitting rule.
- Claude execution review accepts after Codex-supervisor audit.

Veto diagnostics:

- P20 is not longer than P18 in TeX source lines.
- P20 PDF page count is below P18 PDF page count.
- P20 is shorter than the merge-aware line or page lower bounds.
- P20 omits material Zhao--Cui reconstruction from P18.
- P20 omits material accepted P19 gradient derivation.
- P20 contains duplicate equation tags that make references ambiguous.
- P20 reintroduces the wrong finite-difference rule by copying fitted cores
  rather than recomputing them through the fixed fitting rule.
- P20 differentiates adaptive branch choices.
- P20 has unresolved LaTeX build errors, missing files, undefined references,
  or serious overfull boxes.
- Claude raises a substantive veto finding that Codex accepts and does not
  patch.

Explanatory diagnostics:

- Equation count, page count, and line count are necessary guardrails but not
  sufficient evidence of self-containedness.
- MathDevMCP checks remain narrow algebra/proof diagnostics only.

## Allowed Writes

Allowed:

- New P20 files under `docs/plans/`.
- Compiled P20 PDF and same-basename `latexmk` auxiliaries.

Not allowed:

- Do not overwrite P18 or P19 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane, student-baseline, controlled-DPF, public APIs, or
  unrelated dirty files.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p20-zhao-cui-integrated-companion-gradient-plan-2026-06-01.md`
- `...p20-zhao-cui-integrated-companion-gradient-note-2026-06-01.tex`
- compiled PDF beside the note
- `...p20-zhao-cui-merge-ledger-2026-06-01.md`
- `...p20-zhao-cui-equation-and-size-ledger-2026-06-01.md`
- `...p20-zhao-cui-claude-review-ledger-2026-06-01.md`
- `...p20-zhao-cui-discrepancy-report-2026-06-01.md`
- `...p20-zhao-cui-integrated-companion-gradient-result-2026-06-01.md`

Every markdown artifact must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Merge Protocol

1. Copy P18 as the base integrated note.
2. Update title, author, and abstract to P20.
3. Preserve P18 content through the source-order Zhao--Cui annotation and
   fixed-branch object/specification sections unless a conflict must be
   resolved.
4. Replace or expand only P18's compressed `Same-Scalar Analytical Derivative`,
   diagnostics, finite-difference, minimal example, and reader-facing conclusion
   material with the accepted P19 chair-readable material.  No other P18 region
   may be counted as replaced for the size-gate subtraction.
5. Prefix imported P19 equation tags with `P19-` to avoid collision with P18
   tags.
6. Add a short reader-facing bridge explaining that the next part is the
   accepted chair-readable expansion of the fixed-branch derivative.
7. Preserve P18's source-coverage summary appendix.

## Required P18 Carry-Forward Map

The P20 merge ledger must map every P18 source-order section/unit block below
to its P20 destination.  Validation fails if any listed block is omitted,
reordered before the annotation boundary, or compressed into summary prose.

- Reader contract and notation.
- What problem is being solved.
- State-space model and BayesFilter notation.
- Four marginal learning problems.
- Exact recursive bottleneck.
- Tensor trains from first principles.
- TT marginalization.
- Zhao--Cui Algorithm 1, fully annotated.
- Nonnegativity failure and square-root TT repair.
- Squared-TT density, defensive reference, and normalizer.
- Squared-TT marginalization and mass matrices.
- Conditional densities and KR maps.
- Zhao--Cui Algorithm 2, fully annotated.
- Forward conditional map and particle-filter correction.
- Backward conditional map, path estimation, and smoothing.
- Error propagation limitations.
- Preconditioning, including Algorithm 5 and P16b.1--P16b.4 bridge material.
- Source coverage summary appendix.

## Required P19 Import Checklist

The P20 merge ledger must map every accepted P19 component below to its P20
destination.  Validation fails if any component is omitted or reduced to a
vague prose summary.

- Motivation for the panel chair and same-scalar problem.
- Fixed-branch rule: structural branch choices are frozen, fitted core values
  remain parameter-dependent and are recomputed by the fixed fitting rule.
- Warmup 1: normalizing constant derivative.
- Warmup 2: squared approximation derivative.
- Warmup 3: two-coordinate rank-one TT mass derivative.
- Warmup 4: two-coordinate rank-\(R\) TT mass-matrix derivative.
- Warmup 5: fixed linear-solve derivative.
- Full fixed-branch forward object table.
- Full fixed-branch derivative object table.
- Target and square-root target derivative, including positivity-floor
  same-scalar clarification.
- Entrywise design-row derivation leading to Kronecker shorthand and
  \(\dot A\).
- Full mass-contraction bridge and derivative.
- Explicit carried-marginal contraction and derivative recipe.
- Proposition 1: normalized approximate filter.
- Proposition 2: fixed-branch derivative differentiates the same scalar.
- What this does not prove.
- Same-branch finite-difference protocol, including the rule that
  \(\beta_0\pm h\) reuse structural branch choices but recompute fitted core
  values from the same fixed fitting rule rather than copying base cores.
- Minimal runnable example.
- Closing summary.

## Size-Ledger Requirements

The size/equation ledger must record:

- P18 TeX line count and PDF page count.
- P19 TeX line count and PDF page count.
- Exact P18 replacement region by section name and line range.
- Confirmation that the replacement region is limited to the named P18
  derivative/diagnostic/minimal-example/conclusion tail in Merge Protocol step
  4.
- Replaced P18 tail line count.
- Estimated replaced P18 tail page count, with method.
- Required P20 line lower bound.
- Required P20 page lower bound.
- Actual P20 TeX line count and PDF page count.
- Equation tag count and duplicate-tag scan result.

## Claude Review Loop

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p20-zhao-cui-integrated-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p20-zhao-cui-integrated-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Maximum iterations:

- Plan review: 5.
- Execution review: 5.

Claude execution review must include:

- former chemistry academic and panel chair;
- numerical computation professor;
- implementation engineer;
- hostile mathematical reviewer.

Codex-supervisor audit protocol:

- For every Claude finding, classify as `ACCEPT`, `PARTIAL`, `DISPUTE`, or
  `CLARIFY`.
- If accepted or partially accepted, patch and record the exact control added.
- If disputed, record a rebuttal with file/section evidence and include it in
  the next Claude prompt.
- Do not treat Claude `ACCEPT` as sufficient unless Codex independently agrees.

## Validation

- Build the P20 PDF with `latexmk`.
- Run whitespace checks over P20 source and markdown artifacts.
- Scan LaTeX log for undefined references, citation warnings, rerun blockers,
  missing files, errors, and serious overfull boxes.
- Confirm P20 source and PDF satisfy the merge-aware lower bounds.
- Confirm P20 TeX source is strictly longer than P18 TeX source.
- Confirm P20 PDF page count is at least P18 PDF page count, and report whether
  it is strictly greater.
- Confirm the replacement subtraction only uses the named P18 sections from
  Merge Protocol step 4.
- Confirm no duplicate `\tag{...}` labels.
- Use `pdftotext` to confirm the PDF contains every required P18 carry-forward
  block and every required P19 import checklist item.
- Compare the P20 merge ledger against P18 block order and verify each mapped
  destination is a substantive carried section, not a summary placeholder.
- Confirm only allowed P20 files changed intentionally.
