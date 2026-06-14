# P32 Panel-Gap Remediation Plan

metadata_date: 2026-06-05

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

what_is_not_concluded:
- This plan does not claim the current note fails for all readers equally.
- This plan does not replace the existing implementation-completeness or scholarly-remediation plans; it focuses specifically on the remaining gaps as seen by the current review panel composition.
- This plan does not lower the mathematical rigor standard in order to make the note easier to read.

## Purpose

This plan addresses the remaining gaps in the current P32 note as perceived by the review panel:
- a chemistry-chair reader,
- a physicist,
- a macroeconomist,
- and a computer scientist.

The note is now much stronger than before, but the panel-level gap is still this:

> readers can increasingly see what FixedSGQF is, but they are not all equally convinced why it is the selected lane, and not all of them can follow the gradient section without excessive reconstruction.

So this plan focuses on **panel-specific weakness reduction**, not on basic completeness.

## Panel-level diagnosis

### Shared gaps across the panel

All four readers still face some version of these problems:

1. the **selection case** is weaker than the **construction case**;
2. the **gradient section** is still too cognitively dense;
3. the document still feels somewhat **modular rather than inevitable**;
4. the note is stronger on **bounded caution** than on **positive approval-level advocacy**.

### Reader-specific gaps

#### Chemist chair
- understands the broad story, but may still not feel the choice of lane is fully earned;
- can follow the beginning and end of the argument better than the derivative-heavy middle;
- still experiences the note as a technically strong companion rather than a fully persuasive review report.

#### Physicist
- understands the mathematical structure, but may still find Section 20 too soft in comparative force;
- is likely to want a more mathematically grounded case against nearby deterministic Gaussian alternatives;
- may judge Section 13 as correct but still not well taught.

#### Macroeconomist
- understands the approximate-likelihood goal, but may still not see clearly enough what this lane means for inference quality;
- may want stronger argument for why this lane matters for likelihood-based work rather than simpler Gaussian approximations;
- may want clearer statements of what one should and should not trust inferentially.

#### Computer scientist
- can probably implement the method, but may still find extraction more effortful than necessary;
- may still judge the implementation story stronger than the method-selection story;
- may still feel the note mixes too many genres without one clean executable spine.

## Remediation objective

After this pass, the note should satisfy the following stronger panel-facing condition:

> each panel member can not only understand what FixedSGQF is, but also see why it is being carried as a serious lane for this project, what exact mathematical tradeoff it makes, and how the derivative and implementation contracts support that choice.

## Workstream 1 — strengthen the selection case so it persuades all four readers

### Problem
The current note explains FixedSGQF well, but the comparative and approval logic still does not fully convince all readers, especially the physicist and macroeconomist.

### Required changes

#### 1.1 Add a short “why this lane for this project?” synthesis subsection
Insert a compact subsection in the middle-to-late part of the note, after the method and before or inside Section 20, that explicitly gathers the positive reasons for carrying FixedSGQF:
- deterministic scalar;
- same-scalar analytical gradient;
- explicit approximation boundary;
- auditable branch logic;
- reduced dense-growth burden versus tensor-product GHQF;
- complementary role relative to richer non-Gaussian lanes.

This subsection should not be vague. It should read like a compact synthesis of what the technical sections have already established.

#### 1.2 Strengthen the nearest-neighbor comparative case
In Section 20, make the strongest nearby comparisons more explicit:
- EKF / local linearization;
- UKF / CKF / low-order deterministic Gaussian rules;
- standard or tensor-product GHQF;
- live adaptive sparse-grid filtering.

For each, the note should answer:
1. what object it carries;
2. what scalar it naturally defines;
3. what its main mathematical advantage is;
4. what project-level criterion makes it lose or remain unselected here.

#### 1.3 Add an inference-facing interpretation paragraph
Add a paragraph, likely near the end of Section 20 or near the conclusion, answering the macroeconomist’s question:
- what does it mean to use this lane for approximate likelihood-based inference?
- what is being approximated in the likelihood?
- what success of the gradient contract does and does not imply for inference quality?

### Done criterion
A skeptical reader should be able to say not only “I know what FixedSGQF is,” but “I see why this project is carrying this lane rather than a nearby deterministic Gaussian competitor.”

## Workstream 2 — make the gradient section more teachable for mixed readers

### Problem
Section 13 is now more explicit than before, but it is still one of the hardest parts of the note for the chemist chair and the macroeconomist, and still not elegant enough for the physicist.

### Required changes

#### 2.1 Add more recap moments inside Section 13
After each major derivative stage, add one short recap sentence of the form:
- what was just derived;
- whether it closes the current score;
- or whether it exists only for propagation.

#### 2.2 Add one “what to retain from this subsection” sentence at the end of the hardest subsections
Priority subsections:
- Square-Root Branch,
- Observation Sensitivities,
- Innovation Score,
- Posterior Sensitivity Propagation.

These sentences should prevent a mixed reader from losing the main thread.

#### 2.3 Tie the worked example back into the derivative section more aggressively
Where the derivation becomes most abstract, refer back to the numeric oracle so that the reader can map symbols to a concrete one-step instance.

#### 2.4 Add one short summary paragraph before the section ends
Before moving from Section 13 into the algorithm/contract sections, summarize in prose:
- the derivative of the current score is now closed;
- the propagated differentiated state is now closed;
- the next sections convert those results into executable algorithm form.

### Done criterion
A scientifically strong but non-specialist reader should be able to follow Section 13 with less backtracking and less need to mentally reconstruct the entire dependency chain.

## Workstream 3 — make the report feel more inevitable and less assembled

### Problem
The report still has good local sections but can feel like a sequence of modules rather than one inevitable argument.

### Required changes

#### 3.1 Add stronger export/import transitions at critical boundaries
Priority boundaries:
- Section 4 -> 5,
- Section 6 -> 8,
- Section 10 -> 11,
- Section 13 -> 14/15/16,
- Section 18 -> 19 -> 20.

Each transition should answer:
1. what was established,
2. what remains unresolved,
3. why the next section must now appear.

#### 3.2 Add one mid-report orientation sentence before the comparison phase
Before the note enters the adaptive-grid/comparison/conclusion phase, add a sentence making clear that the report has now finished constructing the lane technically and is turning to judging and locating it among alternatives.

### Done criterion
The report should feel more like one extended lecture or defended chapter, and less like a stack of individually strong technical notes.

## Workstream 4 — make the approval tone more active without losing honesty

### Problem
The current note is careful and bounded, but that care sometimes weakens the positive force of the approval case.

### Required changes

#### 4.1 Strengthen the “why approval is rational” language
In the conclusion and possibly once earlier in the note, make the positive case more explicit:
- not merely that the lane is coherent,
- but that it is worth approving as one serious project lane because it preserves a specific and valuable combination of properties.

#### 4.2 Preserve the bounded nature of the claim
Do not let stronger advocacy become overclaiming. The note should still say that this is a selected lane for a specific objective, not the universally best nonlinear filtering method.

### Done criterion
The note should feel more willing to defend the lane, while still remaining scientifically disciplined.

## Workstream 5 — retain implementation usability while reducing friction

### Problem
The computer scientist can likely implement the method, but extraction still takes more work than ideal.

### Required changes

#### 5.1 Tighten the implementation checklist and inventory language
Make sure the compact implementation aids remain easy to extract even after the rhetorical strengthening.

#### 5.2 Keep tables readable after any added comparison or explanatory material
If new arguments make tables denser, split or reformat them rather than letting scanability degrade.

### Done criterion
The implementation spine should remain intact and easy to find even after scholarly strengthening.

## Success criteria

This panel-gap remediation succeeds if, after revision:

1. the chemistry-chair reader can understand the broad lane and feel the note is genuinely persuasive rather than merely careful;
2. the physicist can see a mathematically grounded reason for choosing FixedSGQF over the nearest deterministic Gaussian alternatives;
3. the macroeconomist can see what this lane means for approximate likelihood-based inference and why it is being chosen;
4. the computer scientist can still extract the method quickly;
5. the report feels more like a defended scientific chapter than a technically competent bundle of sections.
