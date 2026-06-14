# P32 Substantial Scholarly Remediation Plan

metadata_date: 2026-06-04

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-scholarly-grounding-and-engineering-exposition-remediation-plan-2026-06-04.md](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-scholarly-grounding-and-engineering-exposition-remediation-plan-2026-06-04.md)

what_is_not_concluded:
- This plan does not claim the current P32 note already resolves the four scholarly weaknesses.
- This plan does not reopen P30.
- This plan does not lower the implementation-completeness bar already achieved in the current P32 note.
- This plan does not treat more prose as equivalent to better grounding or stronger persuasion.

## Purpose

This plan is a **substantial scholarly remediation plan** for P32. It is intentionally stricter than the prior remediation pass because the prior work improved implementation explicitness but did **not** adequately fix the following four issues:

1. Section 20 remains too prose-heavy and not mathematically grounded enough.
2. The analytical gradient derivation remains too dense and insufficiently unpacked for a mixed expert panel.
3. Several sections still appear abruptly, with weak connective tissue and weak logical export/import structure.
4. The note still does not argue strongly enough why FixedSGQF was chosen and why the panel should approve it over competing algorithmic lanes.

The aim of this pass is not cosmetic improvement. It is to make the note read like a **serious, defended scholarly choice document** rather than only a technically explicit companion report.

## Target document

- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

## Governing standard for this pass

After this remediation pass:

1. **Section 20 must read like a mathematically structured selection chapter**, not a narrative taxonomy.
2. **Section 13 must become teachable**, not merely correct.
3. **Major sections must connect by logical dependency**, not merely by adjacency.
4. **The note must make a persuasive bounded approval case for FixedSGQF**, not just describe its properties.

## Report-level choice architecture

This remediation pass must make the report argue from a single repeated decision architecture rather than from isolated local claims.

The note must state clearly, early and repeatedly, that FixedSGQF is being carried because this project prioritizes the following lane-level criteria:

### Necessary conditions
1. a declared deterministic approximate scalar objective;
2. an analytical derivative of that same scalar on a fixed branch;
3. explicit approximation boundaries that can be audited.

### Strong preferences
4. reduced tensor-product explosion relative to dense Gaussian quadrature;
5. a more stable same-scalar contract than live adaptive-grid selection;
6. inspectable numerical and branch structure;
7. a complementary role relative to richer non-Gaussian density lanes.

### Tolerated weakness
8. loss of full non-Gaussian posterior geometry, provided the note remains explicit about that sacrifice and the selected lane still answers the project’s declared objective.

These criteria must appear:
- near the beginning of the note,
- in the rebuilt Section 20,
- and again in the conclusion.

If the criteria appear in only one of those three places, the persuasion problem is not solved.

## Approval standard to be defended

The note must defend a bounded approval claim, not a universal methodological claim. The target approval statement is:

> FixedSGQF is approved here not as a universal nonlinear filtering solution, but as the selected deterministic Gaussian-surrogate lane for approximate likelihood-and-gradient work under this report’s explicit contract.

All comparative and persuasive rewriting must support that exact bounded claim.

## Workstream 1 — Rebuild Section 20 as a grounded selection chapter

### Problem
The current Section 20 still functions mostly as prose comparison. It names neighboring families, but it does not ground the choice of FixedSGQF tightly enough in explicit criteria.

### Required rewrite
Section 20 must be rewritten around a formal comparison architecture.

#### 1.1 Add an explicit selection problem statement
The section must begin by stating the decision problem clearly:
- we are choosing an approximate filtering lane for nonlinear state-space models;
- the lane is intended for deterministic approximate likelihood evaluation with analytical gradient support;
- the comparison is not about global superiority, but about suitability under the report's declared objectives.

#### 1.2 Define explicit comparison axes
The section must compare neighboring methods along at least these axes:
- carried object;
- approximation target;
- source of determinism or stochasticity;
- gradient status / same-scalar status;
- what posterior information is preserved or discarded;
- dominant computational burden;
- principal veto or failure mode.

These axes must be explicit in the text, not just implied by paragraph order.

#### 1.3 Add a formal criterion statement
The section must contain at least one formal criterion or proposition of the form:
- a method is acceptable for this lane only if it defines a declared scalar objective and a derivative of that same scalar on a fixed smooth branch; or
- moment exactness, by itself, does not justify posterior-shape fidelity or HMC suitability.

This is needed to move the section out of pure prose and into explicit mathematical judgment.

#### 1.4 Add a true decision matrix with criterion-to-verdict mapping
The section must include one compact selection matrix with rows for at least:
- EKF;
- sigma-point / CKF / Gauss--Hermite / sparse-grid Gaussian filters;
- tensor-product GHQF;
- fixed SGQF;
- adaptive sparse-grid / frozen adaptive sparse-grid lane;
- particle filtering;
- Zhao--Cui squared TT.

The matrix must classify each competitor as one of:
- **not suitable for this lane**,
- **viable but not selected**,
- **selected lane**,
- **complementary richer lane**.

For each row, the verdict must be tied explicitly to the declared project criteria. A labeled matrix without criterion-to-verdict justification is not sufficient.

#### 1.5 Add dedicated nearest-neighbor elimination arguments
This is mandatory. The section must not only explain why FixedSGQF differs from particle or TT methods; it must explicitly justify why it is chosen over its closest substitutes:
- EKF;
- UKF / CKF;
- standard GHQF;
- tensor-product GHQF;
- live adaptive sparse-grid filtering.

Each of these comparisons must answer:
- what the alternative offers;
- what project criterion it fails, partially satisfies, or satisfies less well than FixedSGQF;
- why that is enough to make it unselected or complementary for this lane.

#### 1.6 Require evidence discipline for all major verdicts
Every major Section 20 verdict must be backed by one of:
- a direct consequence of the report’s approximation contract;
- a claim grounded in cited literature;
- a methodological property established earlier in the note.

A verdict without one of these support types is not acceptable.

#### 1.7 End Section 20 with a choice claim, not just a tradeoff summary
The section must conclude with a bounded but affirmative statement answering:
- why FixedSGQF is being carried as a serious lane in this project now;
- what it buys relative to the alternatives;
- why that benefit justifies approval despite its narrower posterior representation.

### Done criterion
Section 20 should read less like “here are some neighboring methods” and more like “here are the explicit criteria under which FixedSGQF is the selected deterministic Gaussian-surrogate lane.”

## Workstream 2 — Rebuild Section 13 as a staged teaching scaffold

### Problem
The analytical gradient section is mathematically explicit but still cognitively dense. A strong reader can follow it, but the report does not guide them through the dependency structure well enough.

### Required rewrite
Section 13 must be reorganized as a staged derivation rather than a long unbroken technical descent.

#### 2.1 Add a derivation roadmap at the start of Section 13
Before the first dense derivative subsection, add a short roadmap stating the derivation stages explicitly:
1. factor derivative;
2. point sensitivities;
3. predictive moment sensitivities;
4. observation moment sensitivities;
5. innovation score;
6. posterior sensitivity propagation.

This roadmap must say what each stage contributes to the final derivative and whether it serves score evaluation, future-step propagation, or both.

#### 2.2 Insert explanatory bridge paragraphs between 13.2–13.6
Each subsection must begin with one short paragraph answering:
- what object is being differentiated here;
- why it is needed next;
- what breaks if this derivative is omitted or inconsistent.

#### 2.3 Add visible stage conclusions
At the end of each major derivative stage, add one short recap sentence stating:
- what has now been derived;
- whether it is sufficient for current-period score computation;
- or whether it is needed only for propagation into the next step.

This is mandatory because Section 13 currently forces the reader to infer local closure by themselves.

#### 2.4 Add a compact dependency/role table near the beginning
The section must contain a compact table or boxed list mapping each main derivative object to its role:
- current-score only,
- next-step propagation only,
- both.

#### 2.5 Cross-reference the worked example from the derivation
Section 13 must point explicitly to the worked example at the points where readers benefit most:
- factor derivative,
- score decomposition,
- propagation update.

#### 2.6 Require local pedagogical decoding, not only global structure
At the hardest symbolic transitions, the rewrite must add sentence-level unpacking, not only section-level signposting. In particular:
- why factor differentiation must appear before point sensitivities;
- why `\dot v_t` and `\dot S_t` are sufficient for the current score;
- why `\dot C_{xz,t}` matters only because the filter must propagate to the next step;
- what exact quantity the reader should retain before moving onward.

#### 2.7 Add derivation triage
The rewrite must explicitly identify:
- what derivation material is essential to the main line and must remain visible;
- what can be compressed into summary prose without loss of understanding;
- what should be cross-referenced to the worked example rather than re-explained abstractly.

This is needed so Section 13 becomes clearer, not merely longer.

#### 2.8 Prevent clarity-loss through overgrowth
If extra unpacking makes the section much longer, duplicated low-value prose or repeated formula commentary elsewhere must be trimmed. The goal is not maximal length; it is maximal guided readability.

### Done criterion
A technically strong reader should be able to follow the gradient section without having to reconstruct the dependency chain entirely from symbols and memory.

## Workstream 3 — Add connective tissue as logical dependency, not decoration

### Problem
Several sections still arrive as strong local units without clearly explaining why they are the necessary next move in the report-wide argument.

### Required rewrite
The report must add bridge paragraphs that do real dependency work.

#### 3.1 Add explicit import/export logic at major section boundaries
At the starts or ends of major sections, add short bridge paragraphs that answer:
- what the previous section established;
- what it did not yet settle;
- why the next section is the right next object;
- what exact later claim the next section will enable.

Priority boundaries:
- Section 4 -> Section 5;
- Section 6 -> Section 8;
- Section 10 -> Section 11;
- Section 13 -> Section 14/15/16;
- Section 18 -> Section 19 -> Section 20.

#### 3.2 Test whether abruptness is architectural, not only local
Before inserting bridges, explicitly judge whether some abruptness comes from section placement/order rather than missing prose. If so, section order or local placement may need adjustment, not just transitional text.

#### 3.3 Permit structural reordering if needed
If the abruptness diagnosis shows that some transitions fail because the chapter order itself is suboptimal, the rewrite may:
- move subsections,
- split or merge local subsections,
- relocate some material earlier or later,
provided the mathematical dependence remains sound.

#### 3.4 Make later sections cash prior commitments
For example:
- validation should read as the consequence of the declared approximation contract;
- adaptive-grid interpretation should read as the consequence of the same-scalar derivative contract;
- comparison should read as the culmination of the method specification, not as a late appendix.

#### 3.5 Use recurring decision criteria across the note
The report-level choice criteria from the opening must recur later, especially:
- before or inside Section 20;
- and in the conclusion.

This repetition is not redundancy. It is what turns local exposition into a continuous argument.

### Done criterion
The report should feel like one continuous argument in which each major section solves a problem left open by the previous one.

## Workstream 4 — Build a stronger persuasive case for choosing FixedSGQF

### Problem
The note explains what FixedSGQF is, but the approval case is still too weak in the middle of the report. The panel needs to understand why this lane was chosen among serious alternatives.

### Required rewrite
The report must make a more active, comparative case for FixedSGQF.

#### 4.1 State the positive case, not only the negative limits of others
The report must say clearly why FixedSGQF is worth carrying:
- deterministic surrogate likelihood;
- explicit approximation boundary;
- inspectable branch-conditioned analytical gradient;
- reduced cloud complexity relative to tensor-product GHQF;
- a clearer same-scalar contract than live adaptive-grid selection;
- a complementary role relative to richer non-Gaussian lanes.

#### 4.2 Tie the approval case to explicit project criteria
The case for FixedSGQF should be framed not as “best overall,” but as “selected for this lane because the project values these criteria.”

That means the note should argue that FixedSGQF is a serious candidate because it preserves a combination of:
- deterministic reproducibility,
- inspectable approximation structure,
- same-scalar differentiability,
- and moderate high-dimensional plausibility.

#### 4.3 Make the case explicitly comparative against the nearest alternatives
The approval case must not only be affirmative in isolation. It must explicitly state why FixedSGQF is selected **despite** and **relative to** nearby deterministic Gaussian alternatives, not only relative to particle or TT methods.

#### 4.4 Keep the claim bounded
The report must preserve honesty about what FixedSGQF does not solve. Persuasiveness here comes from a disciplined bounded claim, not from aggressive superiority language.

#### 4.5 Recur to the bounded approval standard explicitly
The report must defend the approval standard defined above, not drift into a generic “interesting method” conclusion.

### Done criterion
A skeptical panel member should be able to say: “I understand why this lane is not universal, but I also understand why this project rationally chose to develop and approve it.”

## Workstream 5 — Engineering exposition polish without diluting substance

### Problem
The engineering material is now mostly present, but extraction still requires too much scanning effort.

### Required rewrite
This workstream is narrower than the prior engineering remediation pass, and it must not dominate the scholarly work. It should include:
- one last readability pass on the implementation contract and boxed algorithms;
- improved formatting of dense extraction tables;
- one explicit implementation checklist subsection tying together:
  - inputs,
  - carried state,
  - branch metadata,
  - step outputs,
  - fail conditions,
  - gradient reuse objects.

### Done criterion
An implementation reader should be able to locate the executable specification quickly without the note feeling like an engineering memo.

## Execution order

This remediation pass must proceed in **rhetoric-first** order, not engineering-first order.

1. Rebuild the report-level choice architecture and seed it in the opening and conclusion.
2. Rebuild Section 20 as a true selection chapter.
3. Rebuild Section 13 as a staged teaching scaffold.
4. Add connective tissue across the note.
5. Apply the narrower engineering exposition polish.
6. Run hostile Codex review focused on the four scholarly weaknesses.
7. Rebuild PDF and perform a final read against the two goals.

## Intermediate hostile-review gates

Do not wait until the end of the rewrite to test whether the key weaknesses remain. Run hostile review after:
1. rebuilt Section 20;
2. rebuilt Section 13;
3. inserted cross-section bridges.

If any of those targeted reviews still says the note compares rather than selects, remains pedagogically hostile, or still feels abruptly assembled, revise before continuing.

## Anti-failure guardrails

The rewrite must explicitly guard against the following failure modes:

1. **More text without more grounding.**
   New prose must tie claims to explicit criteria, equations, or support tables.
2. **Longer gradient section without more clarity.**
   Unpacking must add dependency guidance, not only more notation.
3. **Decorative transitions.**
   Bridges must state logical dependency, not generic signposting.
4. **Argument by criticism of rivals only.**
   The note must give a positive, project-specific case for FixedSGQF.
5. **Overclaiming.**
   The case must remain bounded to the declared surrogate lane.
6. **Engineering overgrowth.**
   Extraction aids must not turn the report into a software manual.
7. **Another patch-oriented pass.**
   This remediation must re-thread the report-level argument, not merely improve isolated sections.

## Codex hostile-review protocol

After drafting this pass, run a deliberately hostile Codex review focused only on whether the four weaknesses are still present.

Codex should be asked to judge:
1. whether Section 20 still compares rather than selects;
2. whether the revised note explains why FixedSGQF beats its nearest deterministic Gaussian substitutes for this lane;
3. whether Section 13 is still mathematically correct but pedagogically hostile;
4. whether large sections still arrive abruptly;
5. whether the note still fails to justify choosing FixedSGQF over serious alternatives.

This review should not default back to generic implementation praise. The point is to force judgment on the unresolved scholarly weaknesses.

## Success standard

This remediation succeeds only if:

1. Section 20 reads like a selection chapter with explicit criteria rather than a prose overview.
2. Section 13 becomes notably easier to follow for a mixed expert panel.
3. Major sections feel connected by logical necessity rather than just topic adjacency.
4. The report makes a stronger, bounded, and persuasive case for why FixedSGQF should be approved as one serious algorithmic lane.
5. The implementation engineer can still extract the method quickly after the rhetorical rewrite.
