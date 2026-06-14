# P32 Mathematical Expansion Pass Plan

metadata_date: 2026-06-05

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-gap-remediation-plan-2026-06-05.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-gap-remediation-plan-2026-06-05.md)

what_is_not_concluded:
- This plan does not claim the current note is already sufficient for the whole panel.
- This plan does not replace prior implementation-completeness or scholarly-remediation plans; it adds a new mathematical expansion layer.
- This plan does not justify adding decorative equations. Every new equation must carry explanatory, comparative, or inferential force.

## Purpose

This plan drives the next expansion pass on P32. The purpose is to add **substantially more mathematical exposition** so that the report no longer feels too prose-driven in its comparative and explanatory sections.

The design rule for this pass is:

> add roughly 20 to 30 more meaningful equations, distributed where they improve understanding and persuasion most.

The target audience is still the mixed panel:
- chemistry chair,
- physicist,
- macroeconomist,
- computer scientist.

The expansion must therefore improve:
1. mathematical credibility,
2. section-to-section inevitability,
3. comparative rigor in Section 20,
4. teachability of Section 13,
without damaging implementation readability.

## Target document

- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

## Expansion quota

This pass should add approximately:
- **8–12 new equations to Section 20**,
- **8–12 new equations or compact displayed derivation summaries to Section 13**,
- **4–8 bridge or reduction equations distributed across other sections**.

The point is not the number itself, but the density of mathematical support for the argument.

## What kinds of equations count as meaningful

Count only equations that do one of the following:
1. define a comparison object,
2. express an approximation family mathematically,
3. isolate a growth or complexity tradeoff,
4. decompose a dense derivation into understandable stages,
5. show how one section’s object becomes the next section’s object,
6. summarize a comparative conclusion in mathematical form.

Do **not** count equations that merely rename a concept already fully stated in prose.

## Section-by-section expansion targets

### Section 20 — Relation To Neighboring High-Dimensional Filtering Proposals

#### Goal
Turn Section 20 into a mathematically argued selection chapter rather than a mostly prose comparison.

#### Equations to add
Section 20 should gain equations in at least these categories:

1. **Exact inferential target vs surrogate target**
   - exact likelihood / posterior target,
   - FixedSGQF surrogate target.

2. **Generic deterministic Gaussian-surrogate scalar and operator**
   - one generic scalar formula,
   - one generic moment-operator formula.

3. **Deterministic point-moment family equations**
   - explicit generic point-rule formulas for \(\bar z_t^{(M)}\), \(S_t^{(M)}\), and \(C_{xz,t}^{(M)}\).

4. **Low-order vs sparse-grid comparison equations**
   - low-order deterministic rule,
   - sparse-grid deterministic rule,
   - point-count comparison,
   - moment-class difference or inclusion statement.

5. **Dense GHQF growth comparison equations**
   - tensor-product growth,
   - sparse-grid growth.

6. **Adaptive-grid target dependence equations**
   - adaptive scalar definition,
   - derivative only on locally constant index regions.

7. **Richer-object comparison equations**
   - schematic particle carried object,
   - schematic TT carried object.

8. **Mathematical selection summary**
   - a compact final equation expressing the selected lane as the conjunction of deterministic scalar, fixed-branch derivative, and sparse-grid moment engine.

#### Additional prose requirement
Every equation block in Section 20 must be followed by 2–4 sentences explaining exactly what it proves or shows in the comparison.

### Section 13 — Analytical Gradient Of The Fixed Scalar

#### Goal
Further decompress the gradient section so that a mathematically trained but non-specialist reader can follow the derivation as a staged argument.

#### Equations to add
Section 13 should gain equations in at least these categories:

1. **Local decomposition equations**
   - score split into log-determinant term and quadratic-form term,
   - propagation split into gain derivative and state derivative consequences.

2. **Dependency-chain summaries**
   - compact displayed chains for:
     - predictive stage,
     - observation stage,
     - score stage,
     - propagation stage.

3. **Intermediate reduction equations**
   - explicit “from these objects to those objects” reductions, e.g.
     - from \(\dot\chi_t^{(r)}\) to \(\dot z_t^{(r)}\),
     - from \(\dot z_t^{(r)}\) to \((\dot{\bar z}_t,\dot v_t,\dot\Delta_t^{(r)})\),
     - from \((\dot v_t,\dot S_t)\) to the score,
     - from \((\dot C_{xz,t},\dot S_t,\dot v_t)\) to \((\dot K_t,\dot m_t,\dot P_t)\).

4. **End-of-stage summary equations**
   - compact displayed summaries after major subsections stating what is now closed.

#### Additional prose requirement
Every dense subsection must explicitly answer:
- what new object is produced,
- whether it closes the current score,
- or whether it is only needed because the filter continues in time.

### Other sections to expand modestly

#### Section 5 / 6 transition
Add one or two bridge equations that make the move from exact filtering recursion to Gaussian projection more inevitable.

#### Section 10 / 11 connection
Add a small displayed map showing how the worked example instantiates the general value-path objects.

#### Section 18 / 20 connection
Add a short equation or displayed rule connecting validation evidence to later selection logic, so the comparison chapter feels earned by the prior diagnostics.

## Expansion guardrails

1. The document must **keep expanding**, not shrink by replacing equations with prose.
2. New equations must make arguments more concrete, not more opaque.
3. The implementation-facing spine must remain intact and readable.
4. Any new mathematical comparison in Section 20 must stay bounded to the actual target of the note; do not drift into universal method ranking.

## Execution order

1. Expand Section 20.
2. Expand Section 13.
3. Add smaller bridge equations in other sections.
4. Rebuild PDF.
5. Perform a chair-style reread for whether the note now feels less handwavy and more mathematically serious.

## Success criteria

This pass succeeds if:
1. Section 20 no longer feels mostly prose-driven;
2. Section 13 becomes easier to parse because the main chains are broken into more visible mathematical stages;
3. the report has noticeably more mathematical support for its major comparative and pedagogical claims;
4. the PDF grows in substance, not just length;
5. the chemistry chair and physicist would be less likely to accuse the note of handwaving.
