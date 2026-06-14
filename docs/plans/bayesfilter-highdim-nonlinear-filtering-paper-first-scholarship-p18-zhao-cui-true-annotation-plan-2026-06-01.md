# P18 Zhao--Cui True Annotation Plan

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao--Cui code audit and paper-code crosswalk ledgers.
- P15 fixed-branch implementation contract.
- P17 full-equation reconstruction note and ledgers.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui implementation is globally differentiable.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No claim that BayesFilter has production tensor-train filtering code.
- No claim that Zhao--Cui has been validated on BayesFilter target models.
- No default-method recommendation.

## Purpose

P17 improved the mathematical inventory but still reads too often like a
compressed reconstruction.  P18 repairs that failure mode by producing a true
annotated companion to Zhao--Cui Sections 1--3 and 5, followed only afterward by
the BayesFilter fixed-branch analytical-gradient extension.

The reader standard is:

- a fresh educated academic, including a former chemistry academic with no
  tensor-train background, can follow why each equation is introduced and how it
  follows from previous equations;
- an implementation agent can build a minimal squared-TT sequential filter from
  the note without opening the original paper;
- a skeptical numerical reviewer can identify the normalizers, mass matrices,
  conditional maps, branch choices, and diagnostics.

## Skeptical Pre-Execution Audit

Decision: `PRE_EXECUTION_AUDIT_PASS_WITH_HARDER_GATES`.

The proposed 20% equation-count rule makes sense as a necessary guardrail, but
it is not sufficient.  P17 already contains many local equations, yet the user
correctly found that some material still feels summarized rather than
annotated.  Therefore P18 uses two gates:

1. `EQUATION_COUNT_GATE`: the Zhao--Cui reconstruction part of the P18 note,
   excluding the fixed-branch and analytical-gradient extension, must contain at
   least 20% more displayed, numbered equations than the count of Zhao--Cui
   numbered equations in Sections 1--3 and 5.  The source numbered equations are
   (1)--(26) and (30)--(35), hence the baseline count is 32 and the minimum P18
   count is `ceil(1.2 * 32) = 39`.
   Counting rules:
   - one numbered display counts only if it states one distinct mathematical
     claim or derivation step;
   - cosmetic line breaks, alignment wraps, repeated source equations, and
     subcases split only for layout do not count as additional equations;
   - every P18-added numbered equation beyond the source equations must cite the
     source unit whose derivation it clarifies;
   - the equation-count ledger must separately report source-restatement
     equations, added derivation equations, and equations excluded from the
     count.
2. `TRUE_ANNOTATION_GATE`: each material source unit must be taught in source
   order.  A source unit is a paragraph, displayed formula, algorithm line,
   theorem-like statement, proof step, or figure-dependent mathematical claim
   from Zhao--Cui Sections 1--3 and 5.  Passing the equation-count gate cannot
   compensate for failing the true-annotation gate.

The true-annotation gate requires one explicit source-unit marker for every
material source unit in source order.  A source unit may refer forward or back
only after its own mathematical derivation, implementation meaning, and
reader-facing explanation are present.  Collapsing adjacent source units into a
smooth survey section is a veto failure.

The eight P18 failure modes to address are:

1. `SOURCE_ORDER`: the note must annotate the paper in paper order, not
   reorganize the paper into a survey.
2. `MISSING_DISPLAY_MATH`: every numbered equation, unnumbered displayed
   equation, and algorithm line with mathematical content from Sections 1--3 and
   5 must appear in the inventory and be taught.
3. `SYMBOLS_MEASURES`: every formula block must define symbols, dimensions,
   densities, measures, conditioning events, and normalization status before the
   formula is used.
4. `DERIVATION_GAPS`: each source formula must be derived from Bayes' rule,
   marginalization, tensor contraction, change of variables, conditioning, or
   the preceding formula; prose cannot replace the derivation.
5. `IMPLEMENTATION_OBJECTS`: each source unit must state what an implementation
   stores, evaluates, contracts, samples, differentiates, or diagnoses.
6. `NUMERICAL_DIAGNOSTICS`: each fragile numerical object must have a failure
   mode and diagnostic: rank growth, basis conditioning, fit residual, mass
   matrix definiteness, Cholesky failure, normalizer sign/scale, support
   mismatch, map monotonicity, root-finding residual, ESS, branch stability, and
   finite-difference parity.
7. `CHEMISTRY_READER`: dense tensor-train and transport-map blocks must be
   taught with enough intermediate mathematics and after-the-math explanation
   for a former chemistry academic to teach the step back.
8. `FIXED_BRANCH_SEPARATION`: Zhao--Cui's adaptive algorithm must be separated
   from the BayesFilter fixed-branch extension; the derivative proposition must
   differentiate exactly the scalar computed by the fixed branch, not the
   adaptive paper algorithm.

If any of these eight controls fail after the maximum Claude review loop, final
acceptance is blocked.

Scholarly-audit hardening after hostile plan review:

- P18 must create the six literature-audit ledgers required by the scholarly
  audit policy: source-support, citation/venue metadata, backward snowball,
  forward snowball, claim-support, and omitted-paper/reviewer-risk.
- The source-support ledger must record Zhao--Cui local PDF path, publication
  status, checked Sections 1--3 and 5, checked equation/algorithm/proposition
  anchors, and a retraction/withdrawal/erratum/version-conflict/quarantine
  check.  If network metadata is unavailable, record metadata blockers rather
  than inventing counts.
- Every important claim in the P18 note must map either to a checked Zhao--Cui
  source anchor, a checked Cui--Dolgov anchor where Zhao--Cui explicitly
  delegates the proof, implementation evidence from P10, or a fresh project
  derivation.  This mapping must appear in the claim-support ledger.
- Claims derived only from prior P10--P17 notes are forbidden unless the P18
  claim-support ledger maps them back to checked primary source text, checked
  code, or a fresh derivation.

## Evidence Contract

Question:

Can P18 convert P17 into a true annotated companion to Zhao--Cui Sections 1--3
and 5, with enough extra equations and source-unit teaching to satisfy a
skeptical numerical/implementation/chemistry panel?

Baselines and comparators:

- Zhao--Cui JMLR 2024 local PDF, Sections 1--3 and 5.
- P17 note and inventory, used as the negative baseline for insufficient
  annotation.
- P10 code audit/crosswalk, used only for implementation meaning.
- P15 fixed-branch note, used only for the BayesFilter derivative extension.

Primary pass criteria:

- The P18 inventory enumerates every material source unit from Sections 1--3 and
  5, not just numbered equations.
- The P18 claim-support ledger maps every important claim to inspected
  primary-source anchors, checked code anchors, or fresh project derivation.
- The P18 note follows source order and never substitutes source anchors for
  derivations.
- The Zhao--Cui reconstruction part of the P18 note passes the
  `EQUATION_COUNT_GATE`: at least 39 displayed numbered equations before the
  fixed-branch extension begins.
- Each source unit has an annotation block with:
  1. source anchor;
  2. question answered;
  3. symbols/dimensions/measures/conditioning;
  4. BayesFilter notation;
  5. derivation;
  6. after-the-math explanation;
  7. implementation object;
  8. diagnostic or failure mode.
- Every algorithmic math line has a mini implementation contract:
  inputs, outputs, persisted state, numerical operation, and dependency on prior
  objects.
- Claude execution review accepts under three personas: hostile numerical
  analyst, implementation engineer, and educated former chemistry academic.
- Codex independently audits every Claude finding and records `ACCEPT`,
  `PARTIAL`, `DISPUTE`, or `CLARIFY`.

Veto diagnostics:

- Any material source formula, algorithmic math line, or source paragraph needed
  to understand the next formula is missing from the inventory.
- Any material inventory row appears in the note only as a vague prose summary.
- The Zhao--Cui reconstruction part has fewer than 39 displayed numbered
  equations.
- The equation-count ledger counts cosmetic line breaks, duplicate equations, or
  layout-only subcases as added derivation equations.
- A formula uses an undefined measure, density, dimension, conditioning event,
  rank, basis, mass matrix, map, or normalization constant.
- A conditional/KR map appears before its conditional-density ratio is derived.
- A normalizer/evidence increment is not tied to a computable contraction or
  integral.
- A same-scalar gradient claim is made for an adaptive branch.
- Any important claim lacks a source-support or project-derivation row.
- The chemistry persona cannot teach back the TT marginalization, squared-TT
  nonnegativity, KR conditional maps, particle correction weights,
  preconditioning density chain, or fixed-branch derivative.
- Any accepted or partially accepted Claude finding is not patched.
- Codex and Claude still disagree after the maximum loop and the human has not
  explicitly overridden the disagreement.
- LaTeX build fails, the PDF is missing, or validation shows forbidden file
  edits.

Explanatory diagnostics:

- Raw equation count, note page count, and Claude `ACCEPT` are explanatory
  unless the eight controls above also pass.
- Code anchors and source-code variable names can clarify implementation
  meaning, but they cannot replace a self-contained mathematical derivation.

What will not be concluded:

- No posterior accuracy guarantee for BayesFilter targets.
- No HMC convergence or NAWM readiness.
- No production-readiness claim.
- No GPU/XLA readiness.
- No default-method decision between SGQF and Zhao--Cui.

## Allowed Writes

Allowed:

- New P18 files under `docs/plans/`.
- P18 compiled PDF and LaTeX auxiliary files beside the note.

Not allowed:

- Do not overwrite P10--P17 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane files, student-baseline files, controlled-DPF files, or
  public APIs.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p18-zhao-cui-true-annotation-plan-2026-06-01.md`
- `...p18-zhao-cui-true-annotation-inventory-ledger-2026-06-01.md`
- `...p18-zhao-cui-true-annotated-companion-note-2026-06-01.tex`
- compiled PDF beside the note
- `...p18-zhao-cui-source-support-ledger-2026-06-01.md`
- `...p18-zhao-cui-citation-venue-metadata-ledger-2026-06-01.md`
- `...p18-zhao-cui-backward-snowball-ledger-2026-06-01.md`
- `...p18-zhao-cui-forward-snowball-ledger-2026-06-01.md`
- `...p18-zhao-cui-claim-support-ledger-2026-06-01.md`
- `...p18-zhao-cui-omitted-paper-risk-ledger-2026-06-01.md`
- `...p18-zhao-cui-section1-source-unit-ledger-2026-06-01.md`
- `...p18-zhao-cui-section2-source-unit-ledger-2026-06-01.md`
- `...p18-zhao-cui-section3-source-unit-ledger-2026-06-01.md`
- `...p18-zhao-cui-section5-source-unit-ledger-2026-06-01.md`
- `...p18-zhao-cui-equation-count-ledger-2026-06-01.md`
- `...p18-zhao-cui-eight-issue-control-ledger-2026-06-01.md`
- `...p18-zhao-cui-fixed-branch-gradient-ledger-2026-06-01.md`
- `...p18-zhao-cui-claude-review-ledger-2026-06-01.md`
- `...p18-zhao-cui-discrepancy-report-2026-06-01.md`
- `...p18-zhao-cui-true-annotation-result-2026-06-01.md`

Every ledger must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Source-Unit Annotation Protocol

Before drafting, build a source-unit inventory from the local PDF text for
Sections 1--3 and 5.  For each row record:

- source section and local text anchor;
- source unit type: `paragraph`, `numbered_equation`, `unnumbered_display`,
  `algorithm_math_line`, `theorem_like_statement`, `proof_step`,
  `figure_math_claim`, or `definition`;
- source role;
- required annotation controls from the eight-issue list;
- note destination;
- disposition: `expanded`, `expanded_as_part_of_larger_derivation`,
  `duplicate_expanded_elsewhere`, or `omitted_nonmathematical`;
- reason for any non-expanded disposition.
- exact P18 source-unit marker and note equation identifiers.

Hard disposition rule:

- Material displayed formulas and algorithmic math lines must be `expanded` or
  `expanded_as_part_of_larger_derivation`.
- A material source unit must receive its own explicit marker in the note before
  it can be cross-referenced as part of a larger derivation.
- `duplicate_expanded_elsewhere` is allowed only when the row points to the
  exact P18 equation/block that teaches the same mathematics.
- `omitted_nonmathematical` is allowed only for pure prose or bibliographic
  context that contains no mathematical dependence needed by the next source
  formula.

## Reader-Facing Note Protocol

The main note must not use governance/process language such as "artifact",
"ledger", "review gate", "exported to synthesis", or "HMC label".

For each material source unit, write a block in this order:

0. **Source unit marker.** State the source section and anchor, for example
   `Source unit S3.2-A2(b)`.
1. **What question is answered?** A short mathematical motivation.
2. **Objects and measures.** Define symbols, dimensions, measures, ranks,
   densities, conditioning events, and normalization status.
3. **Paper-to-BayesFilter translation.** Translate Zhao--Cui notation into the
   note's notation.
4. **Derivation.** Show the intermediate equalities.
5. **Meaning.** Explain after the math, not instead of the math.
6. **Implementation.** State the stored evaluator, core, mass matrix,
   contraction, branch choice, map, sampler, weight, or diagnostic.
7. **Failure check.** State at least one numerical or conceptual failure mode.

For each algorithmic math line, add a mini implementation contract:

- inputs;
- outputs;
- persisted state;
- numerical operation;
- dependency on earlier stored objects;
- diagnostic that would fail the step.

Chemistry-reader binary rubric:

- every symbol is defined before use in the local block or in a nearby notation
  table;
- every tensor-train operation is paired with a low-dimensional matrix/vector
  analogy after the formal equations;
- every KR step is tied to the one-dimensional conditional-CDF identity before
  the multivariate triangular map is used;
- every bridge/preconditioning step explains which density is exact, which is
  approximate, and which coordinate system it lives in;
- every failed teach-back item from Claude must be patched before acceptance.

Structural separation rule:

- The note must contain a hard section boundary titled exactly
  `End of Zhao--Cui Annotation and Start of BayesFilter Fixed-Branch Extension`.
- The equation-count ledger freezes the Zhao--Cui equation count at that
  boundary.
- No adaptive-branch differentiability claim is allowed before that boundary.
- The fixed-branch section may refer back to Zhao--Cui objects, but it must
  identify which branch choices are frozen and which paper operations remain
  adaptive in the original algorithm.

## Mandatory Content

Section 1 annotation must cover:

- transition density, observation density, initial density, parameter prior;
- stochastic-volatility example at a conceptual level;
- full joint density derivation;
- evidence and posterior;
- filtering, parameter learning, path estimation, smoothing;
- why all four tasks are marginalization problems;
- why sequential computation is necessary.

Section 2 annotation must cover:

- recursive posterior update and conditional evidence;
- adjacent-state marginal recursion;
- current filter marginal;
- TT decomposition from first principles;
- cores, ranks, interfaces, basis functions, coordinate ordering;
- endpoint and middle marginalization costs;
- Algorithm 1 line-by-line, including fitted target, retained filter, and
  normalizer.

Section 3 annotation must cover:

- why ordinary TT can become negative;
- square-root target and squared-TT density;
- defensive/reference density and support condition;
- normalizer and Hellinger/L2 role;
- mass matrices, Cholesky factors, and marginalization proof;
- conditional densities and CDFs;
- lower and upper KR maps;
- inverse conditional sampling;
- particle proposal and correction weights;
- backward path estimation and smoothing;
- variable-ordering cost argument.

Section 5 annotation must cover:

- why preconditioning is needed;
- general KR preconditioning framework;
- pushforward and pullback density identities;
- residual target and normalizer invariance;
- Gaussian bridge and linear preconditioning;
- tempering bridge and nonlinear preconditioning;
- bridge approximation;
- Algorithm 5 line-by-line;
- how preconditioning changes stored implementation objects.

Fixed-branch extension must cover:

- why adaptive TT-cross/rank/pivot/domain changes are not globally
  differentiable;
- fixed-branch definition;
- normalized approximate filtering proposition;
- same-scalar derivative proposition;
- derivative recursion through target evaluations, fitted coefficients, mass
  contractions, normalizers, carried filters, next-step targets, and
  finite-difference tests.

## Claude Review Loop

Plan review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p18-zhao-cui-true-annotation-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review command:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p18-zhao-cui-true-annotation-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Plan review maximum: 5 iterations.

Execution review maximum: 10 iterations.

Claude execution review has veto power for:

- failure of any of the eight P18 controls;
- failure of the equation-count gate;
- any source unit from Sections 1--3 or 5 reduced to vague prose;
- any finding accepted by Codex but not patched.

If Claude flags failure of any veto item, final acceptance is automatically
blocked until the specific item is patched and Claude no longer flags it, unless
the human explicitly overrides the block.  Codex may dispute the diagnosis or
scope of the patch, but Codex may not waive the block silently.

Claude execution review must include three personas:

1. hostile numerical analyst;
2. implementation engineer;
3. educated former chemistry academic.

The chemistry persona must explicitly answer:

- What is still not self-contained?
- Which equation or concept could not be taught back?
- What exact additional derivation would satisfy the persona?
- Would the persona be convinced that Zhao--Cui is a plausible
  high-dimensional filtering method?

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex independently audits every Claude
finding before patching or accepting.

Classification options:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a narrower or different patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

For every accepted or partially accepted finding, Codex must patch the relevant
file and record the exact section, equation, or control added.

For every disputed finding, Codex must write a concise rebuttal with
file/section evidence and include that rebuttal in the next Claude prompt,
asking Claude to withdraw, revise, or explain why the rebuttal is wrong.

Codex must not silently ignore disputed findings and must not treat Claude
`ACCEPT` as sufficient unless Codex independently agrees.

If Codex and Claude still disagree after the maximum loop, record the
disagreement in the discrepancy report and block final acceptance unless the
human explicitly decides.

## Validation

- Build the P18 PDF with `latexmk`.
- Run `git diff --check` on the P18 files.
- Scan the LaTeX log for undefined references, citation warnings, rerun
  blockers, missing files, and serious overfull boxes.
- Count the displayed numbered equations in the Zhao--Cui reconstruction part
  before the fixed-branch extension; require at least 39.
- Run the equation-count ledger rules: exclude cosmetic splits, repeated
  source equations, and layout-only subcases from the added-equation count.
- Run ledger-level reconciliation: every inventory row maps to exact P18
  source-unit marker and note equation identifiers.
- Run a hostile spot-audit: sample at least three source units from each of
  Sections 1, 2, 3, and 5, and verify manually that the note contains the
  question, definitions, derivation, meaning, implementation object, and
  failure check.
- Use `pdftotext` to confirm the PDF contains expanded source-order annotation
  for Sections 1, 2, 3, 5, fixed branch, same-scalar derivative, and
  finite-difference protocol.
- Confirm every ledger contains `metadata_date`, `seed_papers`, and
  `what_is_not_concluded`.
- Confirm only allowed P18 files changed.

## Final Result Requirements

The result note must include:

- what Codex inspected;
- whether P18 found that P17 was still summary-like;
- the source numbered-equation baseline and P18 equation count;
- Claude plan review history;
- Claude execution review history;
- Codex audit classifications summary;
- files changed;
- PDF build status;
- validation commands run;
- remaining self-containedness gaps;
- whether the chemistry persona was satisfied;
- final probability estimate that the P18 note passes a skeptical mixed
  numerical/implementation/chemistry panel.
