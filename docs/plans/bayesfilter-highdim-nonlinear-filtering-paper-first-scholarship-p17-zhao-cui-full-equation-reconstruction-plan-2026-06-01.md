# P17 Plan: Zhao-Cui Full Annotated Equation Reconstruction

metadata_date: 2026-06-01

seed_papers:
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- Cui and Dolgov, "Deep Composition of Tensor-Trains Using Squared Inverse Rosenblatt Transports," Foundations of Computational Mathematics, 2022.
- P10 Zhao-Cui code audit and paper-code crosswalk ledgers.
- P11--P16 Zhao-Cui derivative, implementability, and annotated reconstruction artifacts.

what_is_not_concluded:
- No claim that the adaptive Zhao--Cui implementation has a globally smooth analytical gradient.
- No claim that fixed-branch differentiation proves exact posterior accuracy.
- No claim that the method is production-ready in BayesFilter.
- No claim that high-dimensional performance has been validated on BayesFilter target models.
- No default-method recommendation.

## Purpose

P16 produced a useful scaffold, but it was too permissive.  It tracked mostly
numbered equations and allowed many displayed, unnumbered, and algorithm-support
formulas in Zhao--Cui Sections 1--3 and 5 to be compressed into prose.  P17
repairs that failure mode.

The P17 output must be a reader-facing mathematical reconstruction of
Zhao--Cui Sections 1--3 and 5 in paper order.  It must not merely summarize the
paper.  It must slow the paper down so that a fresh educated academic, including
a former chemistry academic with no tensor-train background, can follow the
derivation without opening the original paper.  A coding agent should also be
able to implement a minimal squared-TT sequential filter and understand the
fixed-branch derivative variant from the document alone.

## Skeptical Pre-Execution Audit

Decision: `PRE_EXECUTION_AUDIT_PASS_AFTER_SCOPE_HARDENING`.

The plan is allowed to execute only with the following controls:

- The baseline is Zhao--Cui Sections 1--3 and 5, not P16.
- The first execution artifact is a displayed-formula and algorithm inventory.
- The inventory must include numbered equations, unnumbered displayed formulas,
  algorithm lines with mathematical content, theorem-like statements, proof
  steps needed for the reconstruction, and definitions needed before the next
  equation.
- The execution review must reject if a material displayed formula from
  Sections 1--3 or 5 is absent from the inventory or appears in the note only
  as vague prose.
- Every material displayed formula and every algorithm line with mathematical
  content in Sections 1--3 and 5 must have disposition `expanded` or
  `expanded_as_part_of_larger_derivation`.  `support_only` and
  `omitted_with_reason` are allowed only for exact duplicates, pure verbal
  scaffolding, or non-material contextual statements; each such row must point
  to the note location that reconstructs the identical mathematics or explain
  why there is no mathematics to reconstruct.
- The main note must teach in paper order before introducing the BayesFilter
  fixed-branch derivative extension.
- The main note must not contain governance/process language such as
  "exported to synthesis", "HMC label", "artifact", "ledger", or
  "review gate".
- Source anchors are allowed, but a source anchor is never a substitute for a
  derivation in the note.
- Adaptive TT-cross, pivot, rank, domain, and branch changes must not be treated
  as globally differentiable.
- The plan must stop for unresolved major source, inventory, derivation,
  same-scalar, PDF-build, or Claude-Codex disagreement blockers.

The main risks are scale and compression.  A short note can still be useful, but
it does not satisfy P17 unless it inventories and teaches the material displayed
in the source sections.

## Evidence Contract

Question:

Can P17 produce a self-contained annotated reconstruction of Zhao--Cui Sections
1--3 and 5, including displayed unnumbered formulas and algorithm-support
equations, such that a fresh mathematical reader can follow the method and a
coding agent can implement a minimal squared-TT sequential filter plus the
fixed-branch derivative extension?

Baselines and comparators:

- Zhao--Cui JMLR 2024 Sections 1--3 and 5 from the local PDF.
- P16 annotated reconstruction, used as a negative baseline for missed scope.
- P10 paper-code crosswalk, used only to confirm implementation meaning.
- P15 fixed-branch implementation contract, used for derivative branch detail.

Primary pass criteria:

- Inventory covers all material displayed formulas and mathematical algorithm
  lines from Sections 1--3 and 5.
- Every material inventory row has a concrete note mapping and is taught there,
  not merely mentioned.
- Note follows the source order for Sections 1--3 and 5.
- Every important formula has: question answered, symbols/dimensions/measures,
  BayesFilter notation, derivation, human explanation, implementation object,
  and diagnostics.
- Section 1 teaches model densities, joint density, evidence, posterior, four
  marginal learning tasks, and why sequential computation is necessary.
- Section 2 teaches posterior recursion, adjacent-state marginal recursion,
  filtering marginal, TT cores/ranks/interfaces/basis/coordinate ordering,
  marginalization by contractions, Algorithm 1, fitted object, retained object,
  and normalizer.
- Section 3 teaches squared-TT nonnegativity, defensive density, normalizer,
  Hellinger/L2 support at the level needed here, mass matrices, conditional
  densities, lower and upper KR maps, inverse sampling, particle correction,
  smoothing/path estimation, weights, and computational-cost reasons for the
  variable ordering.
- Section 5 teaches preconditioning: bridge density, KR coordinate map,
  pushforward density, residual ratio, squared-TT residual, composite map,
  pullback/pushforward identities, normalizer invariance, Gaussian bridge,
  tempering bridge, Algorithm 5, and conditional-map consequences.
- Fixed-branch extension states and proves normalized approximate filtering
  for the declared scalar and proves the derivative differentiates that same
  scalar.
- Claude plan review and execution review accept, or any remaining issues are
  minor editorial/layout issues after the allowed loop.

Veto diagnostics:

- Missing material displayed formula from Sections 1--3 or 5.
- Formula appears only as a prose summary where a derivation is needed.
- Any material displayed formula or mathematical algorithm line classified as
  `support_only` or `omitted_with_reason` without exact duplicate mapping or a
  non-mathematical reason.
- Any inventory row lacking a concrete source-to-note reconciliation.
- Any conditional/KR map appears before the marginal/conditional density ratios
  that define it.
- Any normalizer or evidence formula is not tied to a computable contraction.
- Any gradient formula differentiates a different scalar from the forward pass.
- Adaptive branch changes are treated as globally smooth.
- Any accepted or partially accepted Claude finding is not patched.
- Unresolved Codex-Claude disagreement after the maximum loop without human
  override.
- LaTeX build failure, undefined-reference/citation blockers, or missing PDF.

Explanatory diagnostics:

- Code anchors, fitting residuals, TT ranks, mass ratios, condition numbers,
  effective sample size, and finite-difference parity errors explain risk.
  They do not prove posterior accuracy, HMC convergence, or production
  readiness.

## Allowed Writes

Allowed:

- New P17 files under `docs/plans/`.
- Compiled P17 PDF and auxiliary LaTeX files beside the P17 note.

Not allowed:

- Do not overwrite P10--P16 artifacts.
- Do not edit `docs/chapters/`.
- Do not edit production `bayesfilter/`.
- Do not edit DPF lane files, student-baseline files, controlled-DPF files, or
  public APIs.
- Do not commit.

## Required Outputs

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p17-zhao-cui-full-equation-reconstruction-plan-2026-06-01.md`
- `...p17-zhao-cui-full-equation-inventory-ledger-2026-06-01.md`
- `...p17-zhao-cui-full-annotated-reconstruction-note-2026-06-01.tex`
- compiled PDF beside the note
- `...p17-zhao-cui-section1-ledger-2026-06-01.md`
- `...p17-zhao-cui-section2-ledger-2026-06-01.md`
- `...p17-zhao-cui-section3-ledger-2026-06-01.md`
- `...p17-zhao-cui-section5-ledger-2026-06-01.md`
- `...p17-zhao-cui-fixed-branch-derivative-ledger-2026-06-01.md`
- `...p17-zhao-cui-source-support-ledger-2026-06-01.md`
- `...p17-zhao-cui-mathdevmcp-ledger-2026-06-01.md`
- `...p17-zhao-cui-claude-review-ledger-2026-06-01.md`
- `...p17-zhao-cui-discrepancy-report-2026-06-01.md`
- `...p17-zhao-cui-full-equation-reconstruction-result-2026-06-01.md`

Every ledger must contain `metadata_date`, `seed_papers`, and
`what_is_not_concluded`.

## Inventory Protocol

Before drafting the note, build an inventory of:

- every numbered equation;
- every unnumbered displayed equation;
- every algorithm line with mathematical content;
- every lemma/proposition/theorem/corollary statement;
- every proof step needed for Sections 1--3 and 5;
- every definition needed to understand the next equation.

For each inventory item, record:

- source section/page/equation or local text anchor;
- source role;
- P17 disposition: `expanded`, `expanded_as_part_of_larger_derivation`,
  `support_only`, or `omitted_with_reason`;
- exact P17 note location where it is taught;
- whether the note gives derivation, implementation meaning, or both;
- whether P16 missed, compressed, or already adequately covered it.

Hard disposition rule:

- A material displayed formula or mathematical algorithm line must be
  `expanded` or `expanded_as_part_of_larger_derivation`.
- `support_only` is allowed only when the row is an exact duplicate of
  mathematics reconstructed elsewhere in P17 or is a theorem statement whose
  proof is external and whose local role is explicitly limited.
- `omitted_with_reason` is allowed only for pure prose scaffolding, figure-only
  explanatory matter, or formulas outside Sections 1--3 and 5.
- Each `support_only` or `omitted_with_reason` row must include an explicit
  duplicate pointer or non-mathematical reason.  Otherwise validation fails.

## Reader-Facing Reconstruction Protocol

For every important formula, the note must use this order:

1. State the question the formula answers.
2. Define every symbol, dimension, density, measure, and conditioning event.
3. Translate the Zhao--Cui object into BayesFilter notation.
4. Derive the formula step by step.
5. Explain the filtering or transport meaning in human language.
6. State what an implementation stores.
7. State numerical failure modes and diagnostics.

The prose comes after the math.  The note may be long.  Do not compress to fit
an artificial page target.

## Main Note Structure

1. Reader contract and notation.
2. Section 1 reconstruction: state-space model, joint density, evidence,
   posterior, filtering, parameter learning, path learning, smoothing, and
   sequential necessity.
3. Section 2 reconstruction: posterior recursion, adjacent-state marginal,
   filtering marginal, TT decomposition, interfaces, basis, ranks, core
   contractions, Algorithm 1, retained objects, and normalizer.
4. Section 3 reconstruction: squared-TT construction, defensive density,
   Lemma 1 meaning, mass matrices, marginal density proposition, conditional
   densities, lower/upper KR maps, particle filter, smoothing, path weights,
   and variable ordering.
5. Section 5 reconstruction: preconditioning bridge, KR map, pushforward
   residual, squared-TT residual, composite map, pullback density, normalizer
   invariance, Gaussian/linear bridge, tempering/nonlinear bridge, Algorithm 5,
   and conditional-map consequences.
6. BayesFilter fixed-branch extension: fixed branch, normalized approximate
   filtering proposition, same-scalar derivative proposition, finite-difference
   test protocol.
7. Reader-facing conclusion.

## Claude Review Protocol

Plan review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p17-zhao-cui-full-equation-plan-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile plan review prompt>"
```

Execution review:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh \
  --cwd /home/chakwong/BayesFilter \
  --name highdim-p17-zhao-cui-full-equation-exec-review-iter<N> \
  --model sonnet --effort high \
  "<bounded hostile execution review prompt>"
```

Plan review max: 5 iterations.

Execution review max: 10 iterations.

Execution review must include three personas:

1. hostile numerical analyst;
2. implementation engineer;
3. educated former chemistry academic.

The chemistry persona must explicitly answer:

- What is still not self-contained?
- Which equation or concept could not be taught back?
- What exact additional derivation would satisfy him?
- Would he be convinced this is a plausible high-dimensional filtering method?

## Codex-Supervisor Audit Protocol

After each Claude review round, Codex independently audits every Claude finding
before patching or accepting.  For every finding, classify:

- `ACCEPT`: materially correct; patch required.
- `PARTIAL`: directionally correct but needs a different or narrower patch.
- `DISPUTE`: incorrect, over-scoped, inconsistent with policy, or would weaken
  the document.
- `CLARIFY`: cannot evaluate without more evidence or human direction.

Record the classification in the Claude review ledger.

If Codex accepts or partially accepts a finding, patch the relevant file and
record the exact section/equation/control added.

If Codex disputes a finding, write a concise rebuttal with file/section
evidence and include it in the next Claude prompt, asking Claude to withdraw,
revise, or explain why the rebuttal is wrong.

Do not silently ignore disputed findings.  Do not treat Claude `ACCEPT` as
sufficient unless Codex independently agrees.

## MathDevMCP Protocol

Use MathDevMCP only for narrow checks:

- Bayes-rule posterior/evidence algebra;
- marginalization identities;
- normalization identities;
- triangular KR Jacobian identity;
- derivative of log normalizer;
- fixed-matrix linear solve derivative;
- quotient derivative for carried filter.

Record statuses:

- `MCP_VERIFIED`
- `MCP_UNVERIFIED`
- `MCP_INCONCLUSIVE`
- `MCP_TOOL_LIMIT`
- `HUMAN_REVIEWED_NOT_MACHINE_CERTIFIED`

Do not claim broad machine certification.

## Validation

- Build the P17 PDF with `latexmk`.
- Run `git diff --check` on P17 files.
- Scan the LaTeX log for undefined references, citation warnings, rerun
  blockers, or missing files.
- Use `pdftotext` to confirm the PDF contains expanded material for Sections
  1, 2, 3, 5, fixed branch, derivative, and finite-difference protocol.
- Run a final source-to-note completeness audit: every inventory row must
  record source anchor, disposition, exact note location, and whether the row is
  fully reconstructed at that location.  The run fails if any material row lacks
  a concrete note mapping or if any non-duplicate displayed formula from
  Sections 1--3 or 5 is not reconstructed in the note.
- Confirm all ledgers contain required metadata fields.
- Confirm only allowed files changed.

## Stop Conditions

Stop and report rather than claim success if:

- the inventory cannot be built from the local PDF;
- a material source formula cannot be reconstructed without copying prose or
  inventing unsupported theory;
- Claude finds a major unresolved inventory, derivation, source, same-scalar,
  or self-containedness blocker after the maximum loop;
- MathDevMCP results are overstated beyond narrow checks;
- the P17 PDF fails to build;
- validation finds forbidden file edits.
