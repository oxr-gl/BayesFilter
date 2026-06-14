# Plan: FixedSGQF companion note approval revision

## Date

2026-06-06

## Target document

```text
docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex
```

## Approval criterion

Revise the FixedSGQF companion note so that:

1. a mixed scholarship panel can approve it;
2. implementation engineers on the panel retain enough technical detail to audit the method;
3. first-year-PhD-level implementation workers can take the note and implement the algorithm correctly;
4. the note remains mathematically explicit and honest about approximation boundaries.

This plan addresses the previously identified issues **except scaffolding**.  We will not add a staged build-and-test training program to the main note.  Instead, we will add implementation-ready pseudocode and, if needed, place more CS-oriented execution detail in an appendix or companion supplement.

## Core decision

Use a **two-layer document architecture**:

- **Main note**: mathematically self-contained, approval-facing, implementation-ready at the algorithm level, with explicit pseudocode, contracts, notation, branch rules, worked oracle, and validation criteria.
- **CS-oriented appendix or supplement**: software-facing details that are useful for implementation engineers but would overburden the scholarship note if placed in the main flow.

### Preferred split

Preferred default:

- keep the **algorithmic mathematics and pseudocode** in the main note;
- move **software-architecture-heavy detail** to a companion supplement;
- if panel logistics require one bundled artifact, convert that supplement into an appendix.

The key constraint is that the **main note must still be implementable by a first-year-PhD-level worker**.  The appendix/supplement may clarify software structure, but it must not contain indispensable mathematical steps omitted from the main note.

## Non-goals

This revision will **not**:

- replace the note with a purely conceptual scholarship essay;
- strip out implementation contracts, branch rules, or derivative detail;
- add a long scaffolding/tutorial section organized as a training curriculum;
- weaken the same-scalar derivative contract for the sake of readability;
- add hidden numerical repair policies inconsistent with the current fixed-scalar contract.

## Diagnosis summary

The current note is strong in mathematical seriousness and implementation auditability, but it is not yet reliably implementable by junior workers from the note alone.

### Main deficiencies

1. **Audience ramp is too steep.**
   The abstract and opening sections introduce too many specialized ideas before the reader has a stable operational picture of the algorithm.

2. **Implementation order appears too late.**
   The note eventually becomes implementable, but the practical execution order is not surfaced early enough for junior workers.

3. **Pedagogical sequencing is weaker than the mathematical content.**
   Definitions, invariants, branch rules, and practical interpretation need to appear earlier and more plainly.

4. **The note mixes approval narrative and software detail inefficiently.**
   Some software-oriented precision belongs in a side document so the main note can breathe without losing rigor.

5. **Polish defects undermine confidence.**
   Visible errors in a highly exacting note create avoidable doubt.

## Revision strategy

The revision should not add more mathematics.  It should **re-sequence, clarify, compress repetition, and formalize implementation handoff structure**.

### Skeptical audit before execution

The main risk in this rewrite is not mathematical omission but editorial overcorrection.  A shorter, cleaner note could still fail the approval criterion if it hides implementation-essential branch rules, merge semantics, or derivative dependencies behind prose summaries or moves them into a supplement that junior workers would effectively need in order to implement the method.  The rewrite must therefore preserve all implementation-essential mathematics in the main note while relocating only software-architecture-heavy detail to an appendix or companion supplement.

This audit passes because the current plan explicitly preserves in the main note the fixed cloud construction, value recursion, same-scalar branch contract, analytical gradient recursion, finite-difference validity rule, and worked numerical oracle.  The remaining editorial choice is appendix versus separate supplement for CS-oriented detail; that choice affects presentation, not mathematical completeness.

The main note should read in this order:

1. what problem is being solved;
2. what exact object and approximate object are being used;
3. what the algorithm computes;
4. what the reader must implement;
5. why the approximation is coherent;
6. how the derivative is defined for the same scalar;
7. what is validated and what is not claimed.

## Planned changes

## Phase R0: Immediate technical cleanup

### R0.1 Fix visible defects

Correct at least the following:

- the broken derivation ledger display near the gradient introduction;
- the erroneous “Section 20” wording in the comparison section;
- any additional LaTeX formatting damage, line-break corruption, or malformed display math discovered during final pass;
- inconsistent section labels or stale cross-references.

### R0.2 Proofread for trust-damaging defects

Run a targeted pass for:

- duplicated or stale section references;
- notation introduced but never defined;
- symbols used with inconsistent meaning across sections;
- broken prose caused by aggressive editing;
- obvious typos in equations, theorem labels, or algorithm summaries.

**Success criterion:** a technically skeptical reader no longer encounters low-level defects that cast doubt on the derivations.

## Phase R1: Rebuild the front matter for junior implementers

### R1.1 Rewrite the abstract

The abstract should be shortened and simplified.

It should state only:

- the scientific problem;
- the selected approximation lane;
- the exact object computed by the note;
- the derivative claim;
- the main limitation;
- the implementation-readiness claim.

It should defer detailed positioning against TT, HMC, and neighboring methods to later sections.

### R1.2 Add a reader-orientation section immediately after the abstract

Add a short section such as:

- **Who this note is for**;
- **What background it assumes**;
- **What a reader should read first**;
- **What the note proves/derives versus what it specifies as implementation contract**.

This section should explicitly name the target implementation worker profile:
mathematically trained junior PhD-level implementer.

### R1.3 Add a front-loaded implementation summary

Before the long derivation, add a compact summary that answers:

- what inputs the algorithm receives;
- what state it carries across time;
- what cloud is fixed and when;
- what is computed at each time step;
- what causes a branch veto;
- what outputs are returned.

This is **not** the forbidden scaffolding/training program.  It is a concise execution summary so the worker sees the whole machine before entering the derivation.

**Success criterion:** a junior implementer can state the full execution order after reading the first few pages.

## Phase R2: Move key implementation structure earlier

### R2.1 Promote the object map earlier in the note

Move or duplicate the object/symbol table near the start, shortly after the early summary sections.

The table should remain concise and implementation-facing.

### R2.2 Add a compact terminology/glossary block

Define early, in one place, the load-bearing terms:

- exact filtering law;
- carried Gaussian surrogate;
- sparse-grid cloud;
- standardized coordinate;
- physical coordinate;
- fixed branch;
- same-scalar derivative;
- branch veto;
- saved branch record.

The goal is to reduce tacit dependence on prior filtering vocabulary.

### R2.3 Separate conceptual claims from implementation-policy claims

Throughout the early sections, visibly distinguish:

- exact mathematical statements;
- approximation decisions;
- implementation conventions;
- validation diagnostics;
- non-claims.

This can be done with short labeled paragraphs or remarks rather than long expository repetition.

**Success criterion:** the reader does not need to infer whether a sentence is a theorem, a design choice, or a policy rule.

## Phase R3: Replace diffuse prose with implementation-ready pseudocode

### R3.1 Add explicit pseudocode blocks in the main note

Add pseudocode for at least these routines:

1. `build_fixed_sparse_grid_cloud`
2. `fixed_sgqf_filter_value_step`
3. `fixed_sgqf_filter_gradient_step`
4. `same_scalar_fd_check`

Each pseudocode block must specify:

- inputs;
- outputs;
- internal state used;
- ordered operations;
- branch checks;
- returned failure record or veto path.

The pseudocode should be mathematical and backend-neutral, not language-specific.

### R3.2 Keep formulas, but make pseudocode authoritative for execution order

The prose should say clearly:

- equations define the mathematical objects;
- pseudocode defines the implementation order;
- the branch contract constrains both.

### R3.3 Reuse the worked example as a debugging oracle, not scaffolding

Keep the worked one-step example in the main note, but reframe it explicitly as:

- a numeric oracle for checking the value path;
- a numeric oracle for checking the derivative path;
- a concrete instance of the pseudocode.

**Success criterion:** a junior implementer can map each pseudocode line to the relevant equations and to at least one numeric checkpoint.

## Phase R4: Tighten the derivative chapter for implementability

### R4.1 Add a plain-language opening to the gradient chapter

Before the full derivative chain, add a brief explanation of:

- why the derivative is difficult;
- why the branch must be fixed first;
- which derivative objects matter for current score versus future propagation.

This can be short, but it must be operational.

### R4.2 Make the score-versus-propagation distinction more explicit

Retain the current distinction, but surface it more clearly with a small table or bullet list very early in the gradient section.

The worker should quickly understand:

- `dot v_t` and `dot S_t` close the current score;
- `dot C_xz,t`, `dot K_t`, `dot m_t`, and `dot P_t` are needed to continue the recursion.

### R4.3 Keep the branch contract, but compress repeated warnings

The same-scalar branch identity is one of the note’s strongest contributions and must remain.  However, repetition can be reduced once the rule has been formalized clearly.

**Success criterion:** a junior implementer can explain why finite differences are only meaningful on the same branch without reading the same warning in multiple sections.

## Phase R5: Rebalance the note by moving CS-oriented detail out of the main flow

### R5.1 Define what stays in the main note

The main note must retain:

- all mathematical definitions required to implement the algorithm;
- cloud construction semantics;
- merge rules and branch rules;
- value and gradient recursions;
- finite-difference contract;
- worked numerical oracle;
- validation criteria and non-claims.

### R5.2 Move software-heavy detail to appendix or supplement

The appendix/supplement may hold:

- suggested software module boundaries;
- recommended data structures for cloud storage and caching;
- API-shape suggestions for value/gradient/failure records;
- serialization or saved-record conventions;
- complexity/memory accounting tables;
- implementation notes about deterministic ordering, reproducibility, and diagnostics logging;
- optional code-adjacent pseudocode closer to Python or TensorFlow style;
- engineering notes about numerical reuse and caching.

### R5.3 Decide appendix versus supplement

Use this rule:

- **Appendix** if the panel will review a single bundled PDF and wants the extra implementation detail visibly attached.
- **Supplement** if the main note should remain cleaner and the panel accepts a paired document.

Preferred recommendation at present: **supplement**, with explicit references from the main note.

**Success criterion:** the main note stays implementable, while software-heavy detail no longer interrupts the scholarly narrative.

## Phase R6: Compress and refocus the comparison material

### R6.1 Keep comparison, but shorten it

The neighboring-method comparison remains valuable, especially for panel approval, but it should be more compact and less rhetorically repetitive.

### R6.2 Add a method comparison table

Add or strengthen a table that compares:

- carried object;
- moment engine;
- deterministic scalar availability;
- same-scalar analytical derivative availability;
- growth story;
- main limitation.

This should replace some repeated prose.

### R6.3 Reduce TT/HMC positioning in the front matter

Keep the positioning, but shift most of it later.  The note should first teach the selected lane before contrasting it with others.

**Success criterion:** general panel members can understand why FixedSGQF is selected without being overloaded early by neighboring-lane rhetoric.

## Phase R7: Strengthen self-containment without adding training scaffolding

### R7.1 Add a prerequisites statement

State explicitly what the note assumes the reader already knows:

- multivariate Gaussian basics;
- covariance factorization at the level of Cholesky use;
- state-space model notation;
- basic derivative notation.

This does not weaken self-containment; it makes the boundary honest.

### R7.2 Add a “what this note does not assume” statement

State that the note will define internally:

- the sparse-grid cloud actually used;
- the fixed-scalar contract;
- the branch identity required for gradients;
- the exact per-step recursion;
- the finite-difference validity rule.

### R7.3 Make the main note implementable without hidden tacit knowledge

During revision, reject any statement that effectively says “the implementer will know what to do.”  Replace such moments with one of:

- an explicit definition;
- a pseudocode line;
- a stated convention;
- a reference to the appendix/supplement.

**Success criterion:** implementation-relevant behavior is always either defined, contracted, or referenced.

## Phase R8: Final approval pass

### R8.1 Approval-readiness checklist for the revised note

The revised note should pass the following checks:

1. A first-year-PhD-level implementation worker can name the algorithm inputs, outputs, carried state, branch checks, and debugging oracle after one read.
2. An implementation engineer can audit the value path, gradient path, and same-scalar contract without consulting undocumented assumptions.
3. A general academic panel member can understand the exact claim, approximation boundary, and reason for selecting this lane.
4. No visible formatting defect undermines credibility.
5. No implementation-essential content exists only in scattered prose.

### R8.2 Explicit non-claim preservation check

Before finalizing, verify that the revision has not accidentally weakened the note’s honesty.  The revised note must still say clearly that:

- this is not exact nonlinear filtering;
- one Gaussian cannot preserve arbitrary posterior geometry;
- sparse-grid quadrature exactness for selected moments is not exact posterior representation;
- adaptive live-grid selection is not the same scalar differentiated here.

## Deliverables

### Deliverable D1: Revised main note

A revised `.tex` file with:

- repaired front matter;
- early reader orientation;
- early implementation summary;
- earlier object map and glossary;
- pseudocode blocks;
- compressed repetition;
- corrected defects;
- retained mathematical rigor and branch contract.

### Deliverable D2: CS-oriented appendix or supplement

A second artifact, either appended or separate, covering:

- software-facing representation choices;
- caching and data layout suggestions;
- diagnostics record layout;
- implementation-oriented reproducibility conventions;
- optional more code-adjacent pseudocode.

### Deliverable D3: Short approval memo or preface paragraph

Optional but recommended: a short approval-facing paragraph or note stating how the main note and appendix/supplement divide responsibilities.

## Suggested section-level rewrite map

### Main note structure after revision

1. Abstract
2. Reader orientation and scope
3. Problem, exact target, and selected approximation lane
4. What the algorithm computes
5. Early object map and terminology
6. FixedSGQF in one pass
7. Sparse-grid construction
8. Value-path equations and pseudocode
9. Worked value example
10. Same-scalar contract
11. Gradient equations and pseudocode
12. Finite-difference validity and diagnostics
13. Validation criteria
14. Neighboring-method comparison
15. Conclusion

### Appendix/supplement structure

1. Software representation choices
2. Cloud storage and deterministic ordering
3. Failure record and diagnostics schema
4. Suggested API surfaces
5. Complexity and memory notes
6. Optional code-adjacent pseudocode

## Section-by-section rewrite checklist

This checklist is keyed to the **current** note structure in
`docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex`.
It states what to do section by section, what to preserve, what to compress,
and what may move to an appendix or supplement.

## Front matter and global edits

### Title

Current title:

- `An Expanded Mathematical Companion To Fixed Sparse-Grid Quadrature Filtering And Its Analytical Gradient`

Checklist:

- keep the current title unless a shorter approval-facing variant is needed;
- if revised, prefer a title that still signals both **fixed sparse-grid quadrature filtering** and **analytical gradient**;
- do not make the title so broad that it sounds like exact nonlinear filtering.

### Preamble and theorem setup

Checklist:

- keep only theorem-like environments actually used after rewrite;
- consider adding an environment or formatting convention for `Implementation contract`, `Non-claim`, or `Diagnostic rule` if that improves visual separation;
- if pseudocode is added in LaTeX, decide whether to use simple boxed enumerated blocks or a dedicated pseudocode package;
- avoid adding stylistic machinery that increases maintenance burden.

### Global prose pass

Checklist:

- shorten long sentences in the abstract and first four sections;
- reduce repeated uses of “lane” where a simpler phrase such as “method” or “approximation” is clearer;
- keep scope-honesty statements, but avoid repeating the same disclaimer in nearly identical wording;
- ensure every acronym or specialized neighboring method name is introduced only when needed.

## Abstract

Current location:

- lines 38--59

Checklist:

- rewrite for one-pass comprehension by a junior implementer and general panelist;
- keep: problem, selected approximation, deterministic scalar, analytical gradient, limitation;
- remove or defer from the abstract: heavy method positioning against HMC and TT, unless kept to one short sentence;
- explicitly state that the note is intended to be **implementation-ready at the algorithm level**;
- avoid early overload from phrases like “same-scalar gradient” before the object is defined;
- if that phrase stays, add a seven-to-ten-word gloss immediately in the sentence.

Target outcome:

- after reading the abstract, a junior reader should know what is carried, what is approximated, and what is differentiated.

## New section: Reader orientation and scope

Current status:

- missing; add immediately after abstract and before table of contents or immediately after table of contents.

Checklist:

- add a short section, likely 4--8 paragraphs or a compact bullet list;
- state who the note is for:
  - implementation engineers,
  - mathematically trained first-year-PhD-level workers,
  - general scientific reviewers;
- state what background is assumed:
  - multivariate Gaussian basics,
  - state-space notation,
  - Jacobian/derivative notation,
  - Cholesky use;
- state what the note provides internally:
  - full value-path equations,
  - fixed sparse-grid cloud semantics,
  - same-scalar branch contract,
  - analytical derivative recursion,
  - worked numerical oracle;
- state clearly that the note is not a full software manual and that software-heavy conventions may appear in an appendix or supplement.

Target outcome:

- readers know what to expect and are not surprised by the mixture of derivation and implementation contract.

## New section: FixedSGQF in one pass / front-loaded implementation summary

Current status:

- partially present across the current opening sections, but not yet in operational form.

Checklist:

- add an early high-level implementation summary before the long derivation;
- answer explicitly:
  - what the inputs are,
  - what the fixed cloud is,
  - what the carried state is,
  - what happens in prediction,
  - what happens in observation,
  - when vetoes occur,
  - what outputs are returned;
- add one short ordered list of the runtime path;
- keep this section compact and operational rather than discursive;
- do not turn it into a staged training scaffold.

Target outcome:

- a junior worker can sketch the whole algorithm before entering detailed notation.

## Section: The High-Dimensional Filtering Problem And The FixedSGQF Lane

Current location:

- lines 63--113

Checklist:

- retain the scientific problem framing;
- shorten rhetorical framing aimed at general review chairs;
- reduce repeated contrast with richer non-Gaussian methods in this opening section;
- move most TT comparison later, keeping at most one sentence here;
- add one clearer sentence saying what the note contributes operationally:
  “The note defines the fixed cloud, value recursion, branch contract, and analytical derivative needed to implement the method.”
- preserve the honesty that exact filtering is not being recovered.

Target outcome:

- the section motivates the method without front-loading all comparative rhetoric.

## Section: FixedSGQF In One Page

Current location:

- lines 115--188

Checklist:

- keep this section, because its structure is strong;
- tighten it into a true executive summary;
- preserve the three approximations and the exact-vs-approximate distinction;
- add a compact box or bullet list named something like `Implementation summary` or `What must be implemented`;
- ensure the “fixed-scalar derivative contract” is described in plain language before formal use;
- remove any sentence whose main job is repeated reassurance rather than new information.

Target outcome:

- this becomes the best short section for both panelists and junior implementers.

## Section: Approximation Hierarchy And Coordinate Walk

Current location:

- lines 190--303

Checklist:

- retain the coordinate map because it is implementation-relevant;
- move the coordinate definitions only after the reader has seen the front-loaded execution summary;
- simplify prose around the exact predictive/filtering density discussion so it serves the coordinate setup rather than re-arguing the same approximation boundary;
- preserve the low-interaction explanation and physical analogy, but compress them if needed;
- consider moving the physical analogy to a remark or boxed intuition paragraph;
- ensure the relation between standardized coordinates and moving physical points is explained in one crisp operational sentence.

Target outcome:

- the reader understands why the cloud is fixed in standardized space and moved in physical space.

## Section: What This Note Computes

Current location:

- lines 304--377

Checklist:

- keep this section and move it earlier if needed, because it directly answers the implementation worker’s main question;
- preserve the scalar cell warning with the quadratic observation example;
- shorten repeated prose about what the note does not compute;
- add one sentence stating that this section is the authoritative scope statement for implementers;
- keep the distinction between carried Gaussian and discarded posterior-shape information explicit.

Target outcome:

- no reader confuses the surrogate scalar with the exact nonlinear filtering likelihood.

## Section: State-Space Model And Exact Filtering Recursion

Current location:

- lines 379--468

Checklist:

- keep the additive-noise state-space specification;
- keep the exact filtering recursion for reference;
- ensure the section explicitly marks which equations are exact target equations and which later equations are approximation equations;
- move the object map subsection earlier in the document if editorially possible;
- keep the implementation conventions subsection, but consider renaming it so junior implementers recognize it as required operational policy.

Target outcome:

- the exact problem statement and implementation conventions are both easy to locate.

## Subsection: Report-Wide Object Map And Implementation Conventions

Current location:

- lines 416--468

Checklist:

- promote this subsection much earlier, ideally right after the new reader-orientation and early implementation-summary sections;
- keep the table;
- prune the table to load-bearing objects only if visual density becomes too high;
- preserve the factor, solve, and noise conventions;
- add a short lead sentence: “This table is the object inventory an implementer should keep open while coding.”
- preserve the symmetrize-then-veto rule and its current no-hidden-repair stance.

Target outcome:

- this becomes the main navigation table for implementers.

## Section: Gaussian Projection From Moments

Current location:

- lines 469--598

Checklist:

- retain the Gaussian projection derivation and affine projection proposition;
- keep the proposition because it clarifies why the update has Kalman form;
- shorten explanatory repetition around “two layers of approximation” if that point has already been made clearly earlier;
- strengthen the source-bridge subsection so that a junior implementer can see exactly what is inherited from Jia--Xin--Cheng and what is newly fixed by this note;
- consider ending the section with a short implementation takeaway bullet list.

Target outcome:

- the implementer understands that sparse-grid machinery feeds Gaussian projection moments, not an entirely different update algebra.

## Section: One-Dimensional Gaussian Quadrature And Tensor Products

Current location:

- lines 599--637

Checklist:

- keep this section, but trim it to what is actually needed later;
- make its purpose explicit: it prepares the sparse-grid cloud construction;
- avoid overexplaining tensor products beyond what the later sparse-grid section uses;
- ensure notation aligns exactly with the cloud-construction section.

Target outcome:

- this becomes a short bridge rather than a detour.

## Section: Sparse-Grid Rule Reconstructed In Source Order

Current location:

- lines 638--926

Checklist:

- keep this as a central technical section;
- preserve the source-order reconstruction because that supports mathematical honesty;
- preserve the Smolyak coefficient derivation and duplicate-merge semantics;
- add explicit pseudocode block `build_fixed_sparse_grid_cloud` near or at the end of this section;
- in that pseudocode, include:
  - inputs: dimension, level, univariate rules, merge tolerance, zero threshold;
  - outputs: stored merged cloud;
  - lexicographic enumeration rule;
  - duplicate merge behavior;
  - near-zero pruning;
  - final sorting;
  - cloud invariants such as weight-total check;
- keep exactness and UKF relation discussion, but compress prose where possible;
- keep the deterministic level-ladder subsection, but clearly mark it as a diagnostic selection policy rather than a theorem.

Target outcome:

- a junior worker can implement cloud construction directly from this section.

## Section: A Toy Fixed Grid With Duplicate Merging

Current location:

- lines 927--989

Checklist:

- keep this section in the main note;
- explicitly label it as a `worked cloud-construction oracle`;
- preserve all numeric values and merged weights;
- add a sentence saying that any implementation should reproduce this cloud exactly up to declared tolerance;
- optionally add a short table of expected sorted node order if ordering is part of the fixed contract.

Target outcome:

- implementers have a minimal deterministic cloud test case.

## Section: FixedSGQF Filtering Value Path

Current location:

- lines 991--1082

Checklist:

- keep the equations;
- add explicit pseudocode block `fixed_sgqf_filter_value_step` immediately after or within this section;
- pseudocode must specify:
  - inputs: previous mean/covariance, observation, model objects, process/observation noise, fixed cloud, branch thresholds;
  - ordered operations: factor, place points, transition map, predictive moments, branch check, observation points, observation moments, innovation covariance check, likelihood contribution, update;
  - outputs: one-step increment, updated mean/covariance, diagnostics or failure record;
- add brief labels in prose for `prediction stage` and `observation stage` so the equations read as code blocks;
- explicitly note which quantities should be cached for later gradient reuse.

Target outcome:

- this section becomes directly translatable into a value routine.

## Section: A Worked One-Step Example With A Numeric Oracle

Current location:

- lines 1084--1353

Checklist:

- keep this section in the main note;
- rename or subtitle it to emphasize `numeric oracle`;
- preserve all numerical values;
- add a short checklist of what this example should verify in an implementation:
  - predictive mean and covariance,
  - observation moments,
  - innovation score,
  - updated mean and covariance,
  - derivative quantities;
- keep the derivative half of the example because it is a major approval asset;
- ensure line breaks and explanatory sentences are readable for junior workers.

Target outcome:

- this becomes the primary end-to-end hand-calculation reference.

## Section: The Saved Scalar And Same-Scalar Contract

Current location:

- lines 1354--1447

Checklist:

- keep this section and keep it mathematically explicit;
- this is one of the note’s strongest distinctive contributions and should remain in the main note;
- add a plain-language introductory paragraph before the formal branch tuple;
- add a small bullet list stating operationally what must not change between value, gradient, and finite differences;
- reduce duplication across later sections once this section is strengthened;
- keep the branch-identity record and the accepted/failure stage-time pattern, because implementation engineers will care about them.

Target outcome:

- a junior implementer understands both the formal branch tuple and the practical rule: same structure, recomputed numbers.

## Section: Analytical Gradient Of The Fixed Scalar

Current location:

- lines 1448--1844

Checklist:

- keep this as the core derivative section;
- immediately fix the broken derivation-ledger display;
- add a short plain-language preface before the full chain;
- preserve the six-stage dependency chain;
- keep the score-role vs propagation-role distinction and surface it earlier;
- keep the Cholesky derivative subsection, but consider adding one short sentence explaining why this derivative matters operationally for point placement;
- ensure every derivative quantity is defined before first use;
- remove repeated warnings that do not add new operational information;
- if needed, break the section visually into numbered subsections or mini-algorithm steps for readability.

Target outcome:

- a junior implementer can follow the derivative as a recursion rather than a wall of formulas.

## Section: One Boxed Mathematical Algorithm

Current location:

- lines 1845--1917

Checklist:

- keep this section;
- rewrite it so it is unmistakably pseudocode-like and not just dense prose in a box;
- consider renaming it `One-Component Gradient Pseudocode` or similar;
- make sure each step begins with a verb and names the produced objects;
- align it explicitly with the earlier value-step pseudocode and the later end-to-end algorithm.

Target outcome:

- this becomes a compact worker-facing summary for one parameter component.

## Section: Implementation Contract

Current location:

- lines 1918--2062

Checklist:

- keep this section in the main note, but make it cleaner;
- preserve the input/output/invariant/failure contract;
- add a short opening sentence explaining that this section is the formal API-level mathematical contract;
- decide which software-facing details belong here and which move to appendix/supplement;
- keep the invariant list and failure criteria in the main note;
- move API-shape suggestions, serialization ideas, and engineering metadata layout to supplement if they become too software-heavy.

Target outcome:

- the main note retains the formal contract without becoming a software design memo.

## Section: End-To-End Mathematical Algorithm

Current location:

- lines 2063--2128

Checklist:

- keep this section;
- rewrite it into more explicit pseudocode style if the boxed algorithm remains more conceptual;
- if two algorithms remain, distinguish them clearly:
  - one-step / one-component summary algorithm,
  - full end-to-end multi-parameter algorithm;
- ensure all branch exits are explicitly labeled and consistent with the failure contract section;
- state clearly whether this section is the authoritative execution order.

Target outcome:

- readers can identify one section as the full execution-order reference.

## Section: Formula Inventory For The Value Path

Current location:

- lines 2130--2154

Checklist:

- keep in some form because it helps navigation;
- shorten if the note becomes too long;
- optionally merge with a broader `How to navigate this note` inventory near the end;
- ensure references remain correct after restructuring.

Target outcome:

- implementers can locate formulas quickly without excessive paging.

## Section: Finite-Difference Same-Scalar Check

Current location:

- lines 2156--2310

Checklist:

- keep in the main note;
- add explicit pseudocode block `same_scalar_fd_check`;
- pseudocode should specify:
  - input parameter component and step ladder,
  - recomputation under same structural branch,
  - branch-valid versus branch-invalid rows,
  - error metric and pass criterion;
- keep both scalar numerical traces;
- add a short plain-language explanation that the finite-difference routine checks the implemented derivative contract, not just algebra;
- reduce duplicated wording about branch mismatch once the rule has been stated clearly.

Target outcome:

- a junior worker can implement the FD diagnostic without guessing what “same branch” means.

## Section: Diagnostics, Accuracy, Memory, And Performance Tests

Current location:

- lines 2312--2486

Checklist:

- keep the validation suite;
- rename or refocus it so the distinction between mathematical validation and engineering benchmarking is visible;
- preserve the test-model inventory;
- keep memory/runtime reporting, but move highly software-specific benchmarking methodology to supplement if needed;
- maintain the distinction between passing the declared scalar contract and proving posterior accuracy;
- add one lead sentence explaining that this section states what evidence supports correctness of the implementation and what evidence supports only approximate usefulness.

Target outcome:

- the validation section supports both scientific and implementation approval.

## Section: Adaptive Sparse Grids As Grid Design

Current location:

- lines 2488--2510

Checklist:

- keep this section short;
- preserve the main point that adaptation may choose the cloud upstream but cannot define the live differentiated scalar here;
- reduce prose if earlier sections have already established the fixed-branch rule;
- ensure the section reads as a boundary clarification rather than a new detour.

Target outcome:

- the reader understands why adaptation is auxiliary rather than the selected derivative target.

## Section: Relation To Neighboring High-Dimensional Filtering Proposals

Current location:

- lines 2512--2754

Checklist:

- keep this section, but shorten it;
- fix the “Section 20” bug immediately;
- add or strengthen a summary comparison table;
- preserve the mathematical criterion for lane selection;
- reduce repeated prose about local choice architecture once the table and conditions are in place;
- keep EKF, UKF/CKF, dense GHQF, adaptive sparse grids, particle methods, and TT comparison, but present them more compactly;
- make sure this section no longer carries explanatory load that should belong earlier.

Target outcome:

- the section justifies the method choice without exhausting the reader.

## Section: Where Each Construction Comes From

Current location:

- lines 2756--2776

Checklist:

- keep this section;
- it is helpful for approval because it separates source-derived components from BayesFilter-derived components;
- verify all source claims are accurately scoped;
- update references if section numbers or theorem labels change.

Target outcome:

- reviewers can see provenance clearly.

## Section: Notation And Formula Inventory

Current location:

- lines 2778--2809

Checklist:

- keep some final inventory, but consider whether it overlaps too much with earlier navigation aids;
- if the object map is moved earlier, this ending inventory can be shortened;
- ensure references remain accurate after restructuring;
- keep only if it materially helps implementation navigation.

Target outcome:

- the note ends with a useful map rather than redundant bookkeeping.

## Section: Conclusion

Current location:

- lines 2811--2874

Checklist:

- keep the conclusion, but shorten repeated material;
- preserve the bounded approval claim;
- make the final paragraph more directly aligned with the actual approval criterion:
  - coherent,
  - mathematically explicit,
  - implementation-ready for junior workers,
  - honest about limits;
- avoid rearguing every comparator in full.

Target outcome:

- the conclusion reads as a disciplined approval summary, not a restatement of the whole note.

## Appendix or supplement rewrite checklist

Use this only for details that are helpful but not mathematically indispensable in the main note.

### Appendix/supplement section A: Software representation choices

Checklist:

- define suggested record layouts for cloud objects, step diagnostics, and failure records;
- describe recommended immutable saved-branch metadata structure;
- explain how to separate value-path caches from gradient-path caches.

### Appendix/supplement section B: Deterministic ordering and storage

Checklist:

- specify practical storage choices for lexicographic node ordering;
- discuss hash/dictionary versus sorted-array cloud storage;
- record reproducibility implications of ordering and tolerance handling.

### Appendix/supplement section C: Suggested API surfaces

Checklist:

- give software-facing signatures for value, gradient, and FD-check routines;
- include result-object suggestions for success and failure returns;
- keep these suggestions consistent with the main note’s mathematical contract.

### Appendix/supplement section D: Complexity and memory notes

Checklist:

- place software-oriented cost accounting here if it distracts from the main note;
- include point-count, memory, and cached-array considerations;
- keep claims qualitative unless measured evidence is available.

### Appendix/supplement section E: Optional code-adjacent pseudocode

Checklist:

- if desired, include more CS-oriented pseudocode closer to implementation conventions;
- do not let this supplement become required reading for the mathematical algorithm itself.

## Execution order for the rewrite

Recommended editorial order:

1. fix global defects;
2. rewrite abstract;
3. add reader orientation and early implementation summary;
4. move/promote object map and terminology;
5. insert pseudocode into cloud, value, gradient, and FD sections;
6. compress repetition across same-scalar and comparison sections;
7. decide appendix versus supplement split;
8. run final consistency pass on notation, references, and non-claims.

## Main uncertainty

The principal unresolved choice is not mathematical.  It is editorial: whether the panel will prefer one integrated document with appendix, or a cleaner main note plus separate supplement.  The mathematical revision is robust either way.

## Recommendation

Proceed with a revision that:

- keeps all implementation-essential mathematics in the main note;
- adds pseudocode to make the execution order explicit;
- improves the early pedagogical ramp for junior implementers;
- moves software-heavy detail to a supplement unless the panel strongly prefers a single bundled artifact.

This is the shortest path to satisfying all current concerns without diluting the note’s technical integrity.
