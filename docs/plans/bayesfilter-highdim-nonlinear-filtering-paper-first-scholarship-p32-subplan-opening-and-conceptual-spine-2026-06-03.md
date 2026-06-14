# P32 Subplan A — Opening Motivation And Conceptual Spine

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not complete the whole report rewrite.
- This subplan does not finalize the value-path or gradient-path derivations.
- This subplan does not weaken mathematical depth for the sake of simplification.

## Goal

Rewrite the opening of P32 so that the chair understands the scientific problem, the intellectual niche of FixedSGQF, and the conceptual sequence of approximations before the heavy technical machinery begins.

## P32 sections to touch

Primary targets in the current note:

- abstract;
- material immediately after `\tableofcontents`;
- `\section{Approximation Hierarchy And Coordinate Walk}`;
- `\section{What This Note Computes}`.

These sections already contain the right raw material. The task is to reorder and sharpen them so the report begins with a scientific argument rather than with machinery.

## Expansion guardrail

The opening rewrite must expand the existing LaTeX report rather than compress it into a shorter executive summary. New framing should be added by insertion and restructuring, while preserving and extending the mathematical substance already present.

## Concrete edits to make

### 1. Strengthen the abstract

Revise the abstract so it does four jobs in order:

1. state the scientific problem: high-dimensional nonlinear filtering with a desire for deterministic value-and-gradient evaluation;
2. state the proposal: FixedSGQF as a Gaussian-projection plus sparse-grid moment method with a fixed-branch analytical gradient;
3. state the key narrowing: the note does not represent the full nonlinear posterior;
4. state the neighboring-method position: this is the transparent Gaussian-surrogate lane, not the richer non-Gaussian density lane of Zhao--Cui squared TT.

The abstract should sound like the opening of a report to experts, not only like an extended companion note.

### 2. Insert a new opening section before the current approximation hierarchy

Insert a new section after the table of contents, tentatively titled:

- `The High-Dimensional Filtering Problem And The FixedSGQF Lane`

This section should contain five short subsections or paragraphs:

1. **The scientific problem**
   - exact filtering becomes function-valued and intractable in nonlinear high-dimensional settings;
   - the panel is not being asked to approve exactness, but a principled approximation lane.
2. **Why deterministic surrogates are attractive**
   - reproducibility;
   - absence of Monte Carlo noise in the target scalar;
   - compatibility with analytical gradient construction.
3. **What FixedSGQF chooses to approximate**
   - not the full posterior density;
   - rather a Gaussian carried object and a deterministic approximate innovation likelihood.
4. **What is gained by this choice**
   - transparency;
   - moderate computational structure;
   - a stable same-scalar derivative target on a fixed branch.
5. **What is sacrificed**
   - non-Gaussian posterior geometry;
   - global multimodal fidelity;
   - adaptivity differentiation.

This should be prose-led, not equation-led.

### 3. Insert a one-page conceptual summary section

After the scientific-problem section and before the current approximation hierarchy, insert a section tentatively titled:

- `FixedSGQF In One Page`

It should present the method as three deliberate approximations:

1. **Gaussian carried state**
   - replace the carried filtering law by `(m_t, P_t)`.
2. **Sparse-grid moment estimation**
   - approximate the nonlinear moments required by Gaussian projection using a deterministic sparse-grid cloud.
3. **Fixed-branch differentiation**
   - freeze the cloud, merge structure, factor branch, and branch-validity rules so the derivative is of the same scalar the value path computes.

This section should explicitly state the exact object, the approximate object, and the accumulated scalar.

### 4. Rework the opening of the current approximation-hierarchy section

Do not delete the current `Approximation Hierarchy And Coordinate Walk` section. Instead:

- shorten its first paragraph slightly;
- remove any burden of first contact from it;
- make it serve as the formal expansion of the conceptual summary rather than the very first explanation.

The beginning of the section should explicitly refer back to the three deliberate approximations already introduced in prose.

### 5. Strengthen `What This Note Computes`

This section should become the first sharp statement of scientific scope inside the body.

Make it answer three exact questions:

1. What object does the algorithm carry from one time step to the next?
2. What scalar does it accumulate?
3. What full-posterior information is intentionally not preserved?

The scalar quadratic example should be retained, but it should be framed as the canonical warning that moment accuracy does not imply posterior-shape fidelity.

### 6. Add one compact opening-side approximation ladder

Add a short boxed or enumerated approximation ladder near the end of the opening material. It should list, in one place:

1. exact nonlinear filtering target;
2. Gaussian carried-state surrogate;
3. sparse-grid moment approximation;
4. fixed-branch derivative restriction.

This ladder is required because the chair criterion depends on being able to remember where each narrowing enters.

## Mandatory deliverables from this subplan

The opening rewrite is not complete unless P32 contains all of the following:

- a problem-first opening section;
- a one-page conceptual summary of the method;
- one compact approximation ladder;
- an explicit statement of the exact object, approximate object, and accumulated scalar;
- one short chair-facing explanation of why this is a legitimate but narrower lane than full non-Gaussian density approximation.

## Suggested section order after revision

The preferred opening order is:

1. abstract;
2. table of contents;
3. `The High-Dimensional Filtering Problem And The FixedSGQF Lane`;
4. `FixedSGQF In One Page`;
5. `Approximation Hierarchy And Coordinate Walk`;
6. `What This Note Computes`;
7. `State-Space Model And Exact Filtering Recursion`.

## Required prose outcomes

After these edits, the opening pages should let the chair answer:

- what intellectual problem the report is solving;
- why a deterministic approximate likelihood with an analytical gradient is interesting;
- why the report chooses a Gaussian carried object;
- why this is a valid but narrower lane than full non-Gaussian density approximation.

## Risks to guard against

- Do not turn the opening into a slogan-heavy executive summary.
- Do not remove equations entirely; the opening still needs mathematical seriousness.
- Do not apologize for approximation. The tone should be intellectually deliberate, not defensive.
- Do not present FixedSGQF as a weaker Zhao--Cui. Present it as a different lane with different commitments.

## Block review gate

After the opening block is drafted, it must be reviewed by the opposite agent family before any value-path drafting begins.

The review must check:

- whether the opening really makes the scientific problem legible to the chair;
- whether the exact-vs-approximate object distinction is explicit;
- whether the approximation ladder is memorable rather than diffuse;
- whether the new framing expanded the LaTeX substance rather than summarizing away detail.

Only after that review passes should the rewrite proceed to Subplan B.

## Done criterion

This subplan is complete only if a strong scientist outside the exact subfield can read the first few pages and accurately explain what kind of proposal FixedSGQF is, why it exists, where its approximation enters, and why the lane is scientifically coherent.
