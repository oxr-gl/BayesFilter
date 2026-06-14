# P32 Subplan E — Neighboring-Method Comparison

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-academic-report-master-program-2026-06-03.md)

what_is_not_concluded:
- This subplan does not rank the compared methods globally.
- This subplan does not justify overclaiming against richer non-Gaussian methods.
- This subplan does not convert P32 into a survey article.

## Goal

Add a comparison section that helps the review panel place FixedSGQF correctly among neighboring filtering proposals.

## P32 sections to touch

Primary target in the current note:

- `Relation To Zhao--Cui Squared TT`.

This section should be expanded or retitled so it becomes a broader positioning section rather than only a two-method contrast.

## Concrete edits to make

### 1. Reframe the comparison section around families of methods

The section should explain, in prose first, that FixedSGQF belongs most naturally to the deterministic Gaussian assumed-density family, but with a sparse-grid moment engine and a fixed-branch gradient target.

This should be stated before comparing it to TT or particle methods.

### 2. Compare against four specific neighbors

The comparison should cover:

1. **EKF / local linearization**
   - approximation enters through local Taylor linearization;
   - carries a Gaussian state;
   - cheap but can mis-handle strong curvature.
2. **Sigma-point / Gauss--Hermite / sparse-grid Gaussian filters**
   - also carry a Gaussian state;
   - approximate moments by deterministic point sets;
   - FixedSGQF should be presented as living closest to this family.
3. **Particle filtering**
   - carries weighted samples rather than one Gaussian surrogate;
   - can express non-Gaussian posterior structure better;
   - loses the same kind of deterministic scalar and fixed-rule analytical gradient story.
4. **Zhao--Cui squared-TT filtering**
   - targets a richer non-Gaussian density approximation;
   - carries more shape information than FixedSGQF;
   - pays for that richness with a more involved approximation object and different implementation burden.

### 3. Add a short comparison table

Use a compact table with rows for the four neighbors and columns such as:

- carried object;
- where approximation enters;
- ability to represent non-Gaussian posterior structure;
- deterministic/reproducible scalar story;
- gradient tractability story;
- typical failure mode;
- best intellectual use case.

The table should summarize, not replace, the prose.

### 4. Make the positioning claim explicit

The section should clearly say:

- FixedSGQF is **not** a full posterior-density approximation method;
- its closest relatives are sparse deterministic Gaussian filters;
- its distinctive contribution is to turn that lane into a fixed-scalar analytical-gradient proposal;
- this is why it belongs beside Zhao--Cui as a complementary lane rather than as a direct substitute.

### 5. Clarify what comparison claims are allowed

The prose must avoid:

- implying that FixedSGQF dominates particle filtering or TT methods;
- implying that sparse-grid moment exactness produces posterior exactness;
- implying that deterministic structure is always superior to richer non-Gaussian approximation.

Instead it should emphasize the trade-off:

- transparency, determinism, and gradient tractability versus richer posterior geometry.

## Mandatory deliverables from this subplan

The comparison rewrite is not complete unless P32 contains all of the following:

1. **A prose positioning paragraph** that identifies the method family FixedSGQF belongs to.
2. **A four-neighbor comparison** against EKF, sigma-point/Gauss--Hermite-type Gaussian filters, particle filtering, and Zhao--Cui squared TT.
3. **A compact comparison table** with at least one implementation-facing column and at least one scientific-scope column.
4. **An explicit statement** that FixedSGQF is a deterministic Gaussian-surrogate lane rather than a full non-Gaussian density lane.

The implementation-facing column requirement is important so the engineer can also understand what kind of method is being implemented.

## Questions this section must answer for the chair

After reading the comparison, the chair should be able to answer:

- what class of method FixedSGQF belongs to;
- why it is not merely “UKF with more points”;
- why it is not merely “a weaker TT method”;
- why it remains a coherent proposal in the high-dimensional filtering landscape.

## Risks to guard against

- Do not let the section turn into a literature survey.
- Do not compare methods on empirical performance that the note has not established.
- Do not blur the distinction between Gaussian carried-object methods and full-density methods.
- Do not understate the non-Gaussian expressive advantage of Zhao--Cui squared TT.

## Block review gate

After the neighboring-method comparison block is drafted, it must be reviewed by the opposite agent family before the conclusion is finalized.

The review must check:

- whether the method family positioning is scientifically accurate;
- whether the comparison avoids overclaiming against particle or TT methods;
- whether the implementation-facing comparison column is genuinely useful;
- whether the section clarifies the lane rather than turning into a survey.

Only after that review passes should the rewrite proceed to Subplan F completion.

## Done criterion

This subplan is complete only if the chair can explain why FixedSGQF is a legitimate and well-positioned lane in the broader filtering landscape, and the engineer can tell what class of algorithm they are being asked to implement.
