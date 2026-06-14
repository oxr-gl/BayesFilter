# P32 Academic-Report Master Program

metadata_date: 2026-06-03

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-standard-upgrade-plan-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-panel-standard-upgrade-plan-2026-06-03.md)

what_is_not_concluded:
- This master program does not itself revise the P32 note.
- This master program does not authorize changes to P30.
- This master program does not claim that every subplan will survive unchanged after drafting.
- This master program does not treat stylistic completeness as evidence of scientific correctness.

## Program purpose

This master program organizes the rewrite of P32 as a **self-contained academic report** that must satisfy two review-panel criteria simultaneously:

1. **Chair criterion**: a former chemistry professor serving as chair can understand the document, find it thorough and self-contained, and judge the proposal persuasive enough to approve the work.
2. **Engineer criterion**: an implementation engineer on the panel can implement the full method, with Claude Code, directly from the report and without consulting additional sources.

The purpose of the master program is to turn those two broad goals into a concrete orchestration and acceptance contract for the rewrite.

## Target document

- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

## Governing report standard

The revised report must be all of the following at once:

- mathematically explicit;
- self-contained in notation and derivation;
- readable by a strong scientist outside the exact subfield;
- detailed enough for direct implementation;
- honest about approximation scope and limits;
- persuasive as a serious high-dimensional filtering proposal.

## Non-negotiable report artifacts

The final P32 report must contain all of the following inside the report itself, not only in external notes:

1. **A scientific opening** that states the problem, the proposal, the narrowing of the approximation target, and the relation to neighboring methods.
2. **A notation and object map** that defines the major carried objects, coordinates, moments, covariances, and scalar target before dense derivations rely on them.
3. **A complete value-path derivation** with explicit formulas for prediction, observation moments, update quantities, likelihood increment, and carried-state recursion.
4. **A complete gradient-path derivation** with explicit frozen-branch semantics, factor derivative path, moment sensitivities, innovation-score derivative, and propagated sensitivities.
5. **At least one implementation-order algorithm block** for the value path and one for the gradient path.
6. **At least one compact worked example** with concrete nodes, weights, moments, update quantities, and one same-branch derivative.
7. **A neighboring-method positioning section** that places FixedSGQF among Gaussian assumed-density filters, particle methods, and Zhao--Cui squared-TT filtering.
8. **A scholarly conclusion** that states what the report has established, what remains narrow, and why approval is justified.

If any of these eight artifacts is absent, the report is not yet panel-ready.

## Implementation-readiness contract

To count as implementable from the report alone, P32 must explicitly specify all of the following.

### A. Mathematical object contract

The report must define, before first heavy use:

- state, observation, and parameter dimensions;
- time indexing conventions;
- quadrature-node indexing conventions;
- all carried means, covariances, and factors;
- all node families in standard, physical, transition, and observation coordinates;
- the exact scalar objective being accumulated and differentiated.

### B. Formula completeness contract

The report must include explicit formulas for:

- predictive mean and predictive covariance;
- observation mean, innovation covariance, and state-observation cross-covariance;
- Kalman-style gain, posterior mean, and posterior covariance;
- per-step approximate log-likelihood increment;
- full accumulated scalar objective;
- factor derivative path on a fixed branch;
- moment sensitivities;
- innovation-score derivative;
- posterior sensitivity recursion.

### C. Algorithm contract

The report must contain implementation-order algorithm blocks that state:

- one-time sparse-grid construction and duplicate merging;
- per-time-step value recursion;
- per-time-step gradient recursion;
- branch-validity checks;
- what is carried forward to the next time step;
- what cached objects are reused by the gradient path.

### D. Numerical linear algebra contract

The report must specify the conventions used for:

- covariance factorization choice;
- matrix solve versus explicit inverse usage;
- symmetry restoration if assumed;
- positive-definiteness requirements;
- branch failure or veto behavior;
- duplicate-node equality or merge semantics if tolerance-sensitive.

### E. Same-branch finite-difference contract

The report must specify:

- what exactly is frozen on the branch;
- what is recomputed under perturbed parameters;
- what constitutes branch mismatch;
- why mismatch invalidates the finite-difference comparison.

If these details are not explicit, the engineer criterion is not met.

## Report-wide implementation convention lock

Before rewriting P32, the drafting pass must commit the report to one consistent implementation convention set and keep it fixed throughout the document.

At minimum, the rewritten report must make one unambiguous choice for each of the following and then use that choice everywhere:

1. **Covariance factor convention**
   - e.g. lower-triangular Cholesky factor, symmetric square root, or another named branch.
2. **Factor-derivative convention**
   - the governing equation for the chosen factor derivative and the uniqueness constraint that closes it.
3. **Solve convention**
   - whether update formulas are written in inverse notation for mathematics but implemented/recommended as linear solves.
4. **Symmetry and PSD convention**
   - whether covariance symmetrization is applied after floating-point accumulation and what positive-definiteness check is required before proceeding.
5. **Branch-failure convention**
   - whether an invalid branch yields veto, explicit invalid status, NaN objective, or another fixed report-wide outcome.
6. **Duplicate-merge convention**
   - whether node identity is exact or tolerance-based, how merged ordering is fixed, and how weight accumulation is defined.

These are not optional editorial choices. If the report leaves any of them ambiguous, direct implementation from the report alone is not yet supported.

## Notation and formula inventory requirement

The final report must include, either in the main body or a dedicated appendix, an inventory that lets a reader audit completeness without searching the whole document.

The inventory must map each of the following to a report location:

- principal symbols and their dimensions;
- carried state objects;
- per-step value-path equations;
- per-step gradient-path equations;
- branch-definition and branch-validity rules;
- algorithm blocks for value and gradient paths;
- worked-example inputs and outputs.

The inventory may be presented as a compact table, a formula map, or a notation appendix, but it must exist explicitly.

## Chair-readability contract

To count as acceptable for the chair, P32 must let a mathematically serious reader outside the exact subfield answer all of the following from the report alone:

1. What scientific problem is being solved?
2. Why is exact nonlinear filtering impractical here?
3. What object is being approximated, and by what narrower surrogate?
4. Why might sparse-grid Gaussian moment approximation still be plausible in some high-dimensional regimes?
5. Where exactly does the approximation enter?
6. What is gained by determinism and fixed-branch differentiation?
7. What is lost relative to richer non-Gaussian density methods?
8. Why is this a legitimate lane rather than an incoherent hybrid?

If the report does not let the chair answer all eight questions confidently, the chair criterion is not met.

## Cross-agent review protocol

The rewrite must be review-gated after each major block, using the opposite agent family as reviewer.

Rule:

- if **Codex** performs the drafting or patching of a block, then **Claude Code** must review that block before the next block begins;
- if **Claude Code** performs the drafting or patching of a block, then **Codex** must review that block before the next block begins.

A “block” means one completed subplan insertion or revision unit, for example:

- Subplan A opening rewrite;
- Subplan B value-path expansion;
- Subplan C gradient-path expansion;
- Subplan D worked-example insertion;
- Subplan E neighboring-method comparison rewrite;
- Subplan F conclusion rewrite.

Each block review must answer three questions:

1. Does this block satisfy its own subplan deliverables?
2. Does this block preserve consistency with the master-program contracts?
3. Did the block accidentally compress, blur, or contradict earlier mathematical content?

If the reviewer finds a material issue, patch the block and rerun the opposite-agent review before moving on.

## Block-level review ledger requirement

For each block A-F, maintain a short execution note or ledger entry recording:

- drafting agent (`Codex` or `Claude Code`);
- reviewing agent (the opposite family);
- files/sections touched;
- accepted findings;
- disputed findings;
- whether the block passed its review gate.

Do not treat a block as complete until this review gate passes.

## Program structure

The rewrite is divided into six subplans.

### Subplan A — Opening motivation and conceptual spine
Goal:
- make the chair understand the scientific problem, the intellectual niche of FixedSGQF, and the deliberate sequence of approximations before heavy notation begins.

Deliverable:
- a stronger opening of P32 that explains why this proposal exists and what kind of method it is.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-opening-and-conceptual-spine-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-opening-and-conceptual-spine-2026-06-03.md)

### Subplan B — Value-path implementation completeness
Goal:
- make the full filtering value path self-contained enough for implementation from P32 alone.

Deliverable:
- complete derivation and exposition of the carried Gaussian, sparse-grid construction, prediction/update moments, likelihood increment, and posterior recursion.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-value-path-implementation-completeness-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-value-path-implementation-completeness-2026-06-03.md)

### Subplan C — Gradient-path implementation completeness
Goal:
- make the fixed-branch analytical gradient path fully implementable from P32 alone.

Deliverable:
- explicit treatment of branch freezing, factor sensitivities, moment sensitivities, innovation-score derivative, posterior sensitivities, and derivative recursion.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-gradient-path-implementation-completeness-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-gradient-path-implementation-completeness-2026-06-03.md)

### Subplan D — Worked example as teaching bridge
Goal:
- build one compact example that simultaneously teaches the chair and anchors the engineer.

Deliverable:
- one end-to-end one-step example covering value path and one parameter derivative on the same branch.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-worked-example-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-worked-example-2026-06-03.md)

### Subplan E — Neighboring-method comparison and positioning
Goal:
- help the panel place FixedSGQF correctly within the larger filtering landscape.

Deliverable:
- a comparison section that clarifies the relationship to EKF/sigma-point/Gauss--Hermite Gaussian filters, particle methods, and Zhao--Cui squared-TT filtering.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-neighboring-method-comparison-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-neighboring-method-comparison-2026-06-03.md)

### Subplan F — Conclusion and panel positioning
Goal:
- make the final judgment of the report sound balanced, scholarly, and persuasive.

Deliverable:
- a conclusion that tells the panel what the report has established, what remains narrow, and why the proposal still merits approval as one lane of high-dimensional filtering work.

Subplan file:
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-conclusion-and-panel-positioning-2026-06-03.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-subplan-conclusion-and-panel-positioning-2026-06-03.md)

## Cross-subplan constraints

Every subplan must preserve the following global constraints:

1. P32 must remain a **human-readable academic report**, not a governance or software-process artifact.
2. P32 must remain **mathematically explicit** enough that an implementation engineer can code from it directly.
3. P32 must remain **self-contained** and should not rely on the reader having Jia--Xin--Cheng open beside it.
4. P32 must state clearly where the approximation enters and must not blur the distinction between exact filtering and the FixedSGQF surrogate.
5. P32 must not oversell itself against richer non-Gaussian methods such as Zhao--Cui squared TT.
6. P32 must not be revised at the cost of introducing vagueness for the sake of elegance.
7. P32 must be revised by **expanding the LaTeX report itself**: add missing exposition, derivations, examples, comparison material, and implementation detail inside the note rather than replacing existing content with shorter summary prose.

## Execution order

The recommended order is:

1. Subplan A — Opening motivation and conceptual spine
2. Subplan B — Value-path implementation completeness
3. Subplan C — Gradient-path implementation completeness
4. Subplan D — Worked example
5. Subplan E — Neighboring-method comparison and positioning
6. Subplan F — Conclusion and panel positioning

This order is intentional. The report first needs its scientific argument, then its implementation completeness, then its pedagogical bridge, then its comparative positioning, and finally its closing judgment.

## Program-level acceptance test

The master program succeeds only if the completed P32 passes **both** of the following tests.

### Chair test

A former chemistry professor who is mathematically serious but not inside this exact subfield can read the report and truthfully say:

- I understand the scientific problem.
- I understand what is being approximated and what is not.
- I understand where the approximation enters and why it may be reasonable.
- I understand why the method is scientifically narrower than a full non-Gaussian density method.
- I find the report thorough, self-contained, and persuasive enough to approve this lane of work.

### Engineer test

An implementation engineer can read the report and truthfully say:

- I know the exact scalar objective being computed.
- I know the complete value recursion.
- I know the complete fixed-branch gradient recursion.
- I know what branch data are frozen and how branch validity is tested.
- I know enough notation, shapes, formulas, and numerical conventions to implement the method with Claude Code without reopening external sources.

If either test fails, the program is not complete.

## Current orchestration state

The master program and all six subplans now exist. The next step is to refine any remaining ambiguity at the convention level and then execute the rewrite against P32 itself.
