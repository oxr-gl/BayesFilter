# P32 Scholarly Grounding And Engineering Exposition Remediation Plan

metadata_date: 2026-06-04

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

what_is_not_concluded:
- This plan does not replace the existing P32 academic-report master program; it supplements it.
- This plan does not reopen P30.
- This plan does not claim that the current P32 note already satisfies the four scholarly concerns discussed with the user.
- This plan does not lower the implementation-completeness standard in order to improve readability.

## Purpose

This plan addresses two remaining classes of weakness in the current P32 note:

1. **Engineering exposition weaknesses**
   - one more readability/clarity pass on the implementation contract and boxed algorithms;
   - cleaner presentation of branch-identity and finite-difference validity logic;
   - improved table formatting so implementation-critical details are easier to extract quickly;
   - one explicit implementation checklist that ties inputs, carried state, branch metadata, step outputs, fail conditions, and gradient reuse objects into one compact executable specification.

2. **Scholarly and persuasive weaknesses**
   - Section 20 is still too prose-heavy and not grounded tightly enough;
   - the analytical gradient derivation remains too dense and under-unpacked;
   - several sections still appear abruptly, with weak connective tissue;
   - the report still does not argue strongly enough why FixedSGQF was chosen and why the panel should approve it out of competing algorithmic lanes.

The goal is to fix both classes of problems without sacrificing the mathematical precision already achieved.

## Target document

- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

## Overarching standard

After this remediation pass, P32 should satisfy both of these claims more convincingly:

1. A former chemistry professor chair can read the note and judge it **thorough, connected, self-contained, and persuasive**.
2. An implementation engineer can extract the executable method with **less search friction and less interpretive effort** than in the current draft.

This means the rewrite must improve **argument quality, section connectivity, rhetorical force, and scanability**, not only correctness.

## Workstream A — Engineering exposition remediation

### A1. One last clarity pass on the implementation contract and boxed algorithms

#### Problem
The implementation content is now mostly present, but still harder to extract than it should be. Some algorithm steps are clear only after reading surrounding derivations.

#### Planned changes
- Rewrite the short boxed algorithm so every step reads as a compact executable summary rather than a compressed derivation fragment.
- Ensure the short boxed algorithm and long end-to-end algorithm use visibly parallel terminology for:
  - scalar increment,
  - branch acceptance,
  - carried state,
  - gradient accumulation,
  - branch failure exits.
- Tighten the prose immediately before and after the boxed algorithms so the reader knows:
  - why there are two algorithm presentations,
  - which one is the compact summary,
  - which one is authoritative for implementation ordering.

#### Done criterion
A reader should be able to understand the purpose of each boxed algorithm before reading any equations inside it.

### A2. Cleaner branch-identity and finite-difference validity presentation

#### Problem
The branch logic is now mathematically present, but it is still distributed across tuple definitions, branch-identity records, finite-difference prose, and algorithm exits.

#### Planned changes
- Consolidate the branch logic into one compact visible presentation, likely as a table or boxed checklist, covering:
  - frozen structural metadata,
  - parameter-dependent recomputed quantities,
  - accepted/failure stage-time pattern,
  - mismatch rules,
  - what invalidates an FD row.
- In the FD section, point explicitly back to that compact branch-identity presentation rather than re-describing it in prose.
- Reduce duplication by keeping one canonical definition and making later sections reference it.

#### Done criterion
A reader should be able to answer “what exactly must match for two evaluations to count as the same branch?” from one compact location.

### A3. Improve table formatting for extraction speed

#### Problem
Some implementation-critical tables are dense and visually cramped in the PDF, even though the content is correct.

#### Planned changes
- Reformat the most overloaded tables, especially:
  - implementation contract table,
  - neighboring-method comparison table,
  - final notation/formula inventory.
- Use shorter cell prose where possible without losing substance.
- Split overloaded tables into two smaller tables if that produces better scanability.
- Prefer tables with one clear organizing principle rather than mixed semantic and procedural payloads in the same rows.

#### Done criterion
Implementation-critical tables should be readable without zooming and without line-wrapped cell prose obscuring the main distinction.

### A4. Add one explicit implementation checklist subsection

#### Problem
The report now has all the pieces, but the engineer still has to synthesize them from multiple sections.

#### Planned changes
Add one compact subsection, likely near the implementation contract or inventory, containing:
- required inputs;
- carried filtering state;
- frozen branch metadata;
- per-step outputs;
- fail conditions;
- gradient reuse objects / caches.

This checklist should be intentionally redundant with the longer derivation, but far more executable as a build checklist.

#### Done criterion
An engineer should be able to use this subsection as a top-level implementation checklist before diving into equations.

## Workstream B — Scholarly grounding and persuasion remediation

### B1. Ground Section 20 more tightly

#### Problem
Section 20 is still mostly prose comparison and can feel handwavy.

#### Planned changes
- Recast Section 20 so that each comparison is anchored to a sharper axis, such as:
  - carried object,
  - approximation target,
  - source of determinism or stochasticity,
  - gradient status,
  - what posterior information is preserved or discarded.
- Reduce vague family language and replace it with more explicit “because X, therefore Y” structure.
- Make the final comparison claim less descriptive and more argumentative: why this lane exists in this project, not just where it sits abstractly.

#### Done criterion
Section 20 should read less like method taxonomy and more like a justified positioning argument.

### B2. Unpack the analytical gradient derivation

#### Problem
The gradient section is mathematically explicit but still too dense for the intended panel.

#### Planned changes
- Insert more short explanatory paragraphs between subsections 13.2–13.6 clarifying:
  - why each derivative object is needed,
  - what role it plays in score versus propagation,
  - what would break if it were omitted.
- Add micro-bridges before equations that currently appear with too little context.
- Make the transition from square-root derivative to point sensitivities, and from point sensitivities to score/update objects, more verbally explicit.
- Use the worked example to cross-reference the general derivation more often.

#### Done criterion
A strong reader should be able to follow the derivative section without repeatedly reconstructing the dependency chain from symbols alone.

### B3. Add connective tissue between major sections

#### Problem
Several sections still appear abruptly, even though their content is individually strong.

#### Planned changes
Add short bridge paragraphs at the starts or ends of sections such as:
- Section 5: why the formal state-space model is the next step after “What This Note Computes”;
- Section 6: why Gaussian projection formulas must be stated before sparse-grid mechanics;
- Section 10 to Section 11: why the worked example now appears and what it is meant to teach;
- Section 18 onward: why validation, adaptive-grid interpretation, and comparison appear after the method and derivative sections.

These bridges should explain not just what comes next, but why the reader needs it next.

#### Done criterion
The report should feel sequentially argued rather than serially assembled.

### B4. Strengthen the case for why FixedSGQF was chosen

#### Problem
The note explains what FixedSGQF is, but still not strongly enough why the panel should care about this lane out of all possible methods.

#### Planned changes
- Strengthen the opening and/or conclusion with a more explicit project-level rationale:
  - deterministic surrogate likelihood;
  - explicit approximation boundary;
  - inspectable branch-conditioned gradient;
  - complementary role relative to richer non-Gaussian lanes.
- Reinforce that the choice is not arbitrary or merely convenient, but scientifically motivated by a distinct tradeoff the project wants to preserve.
- Make the approval case more active: not just “this is coherent,” but “this is worth carrying as one of the serious candidate lanes.”

#### Done criterion
A skeptical panel member should understand not only what FixedSGQF is, but why the project rationally chose to develop it.

## Execution order

1. Engineering exposition fixes A1–A4.
2. Scholarly/persuasive fixes B1–B4.
3. Run Codex review focused on engineering readability and extraction.
4. Run Codex review focused on scholarly grounding, section transitions, and persuasion.
5. Rebuild PDF and perform a final read against the two goals.

## Codex review protocol for this remediation plan

After drafting this remediation pass:

1. Ask Codex to review whether the engineering exposition now supports fast extraction of:
   - implementation contract,
   - branch logic,
   - algorithm order,
   - worked-example checkpoints.
2. Ask Codex to review whether the non-engineering critiques are now resolved:
   - Section 20 still handwavy or now grounded,
   - gradient derivation still too dense or now unpacked,
   - sections still abrupt or now connected,
   - report still dry or now persuasive.
3. Patch any accepted findings before final PDF rebuild.

## Success criteria

This remediation plan succeeds if, after execution:

1. the implementation engineer can find the executable specification faster and with less interpretation burden than in the current draft;
2. Section 20 reads as a grounded positioning argument rather than loose method prose;
3. Section 13 feels meaningfully more guided and less compressed;
4. the report’s large sections connect into an intentional narrative;
5. the note makes a stronger case for why FixedSGQF should be considered and approved as one of the serious algorithmic lanes.
