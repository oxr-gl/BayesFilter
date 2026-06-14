# P32 Chair-Perspective Punch List

metadata_date: 2026-06-05

seed_papers:
- Jia, Xin, and Cheng, "Sparse-Grid Quadrature Nonlinear Filtering," Automatica 2012.
- Singh, Radhakrishnan, Bhaumik, and Date, "Adaptive Sparse-grid Gauss-Hermite Filter," arXiv 2018.
- Zhao and Cui, "Tensor-Train Methods for Sequential State and Parameter Learning in State-Space Models," JMLR 2024.
- [docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex](docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-p32-fixed-sgqf-expanded-companion-note-2026-06-03.tex)

what_is_not_concluded:
- This punch list does not replace the larger scholarly remediation plan.
- This punch list does not lower the implementation standard.
- This punch list does not claim the current note is unacceptable; it identifies what likely prevents strong approval by a scientifically serious chair.

## Perspective

This punch list is written from the perspective of a former academic chemist serving as review chair.

The current note reads as serious, mathematically literate, and much improved. It is no longer naive. But it still feels more like a technically competent companion report than a fully convincing selection argument. The likely chair reaction is:

> close, credible, but not yet fully compelling.

The goal of this punch list is to move the note from **close** to **approve**.

## Chair-level diagnosis

The remaining problem is not basic mathematical correctness. It is that the note still does not fully feel like an unavoidable argument. The chair can now understand what FixedSGQF is, but still may not feel that the report has fully earned the choice of this lane over the nearest alternatives.

The main residual weaknesses are:
1. Section 20 still feels somewhat self-justifying.
2. Section 13 is still too cognitively compressed.
3. The middle of the report still weakens the “why this lane?” thread.
4. The note still feels somewhat modular rather than inevitable.

## Punch list

### 1. Make Section 20 less self-justifying and more externally convincing

#### Problem
Section 20 now selects a lane, but it can still feel like the note defines criteria that happen to favor the method it already wanted.

#### Needed fix
Strengthen the comparison against the **nearest deterministic Gaussian competitors** with sharper mathematical reasoning, especially:
- UKF / CKF,
- standard GHQF,
- tensor-product GHQF,
- live adaptive sparse-grid selection.

#### Concrete chair-facing revision goal
A reader should come away feeling:
- “Given the target object and gradient requirements, I see why these alternatives fail or become less suitable,”
not merely
- “I see why the author prefers this method.”

#### What to add
- For each nearest alternative, one short mathematically grounded paragraph that states:
  1. what surrogate object it builds,
  2. what it gains,
  3. what specific property makes it lose for this note’s target.
- Make especially sure the UKF/CKF comparison does not rest only on “contract clarity.” It needs a stronger argument about what sparse-grid structure buys mathematically.

### 2. Slow down the analytical gradient section even more

#### Problem
Section 13 is better than before, but the chair still has to work too hard to keep the derivative chain in working memory.

#### Needed fix
Insert more “pause points” where the section explicitly says:
- what has just been derived,
- what role it serves,
- and why the next object is needed.

#### Concrete chair-facing revision goal
A chair should be able to read Section 13 as a guided derivation, not as a symbolic climb.

#### What to add
- One short recap after each major derivative stage:
  - factor derivative,
  - predictive sensitivities,
  - observation sensitivities,
  - innovation score,
  - posterior propagation.
- One or two additional plain-language sentences before the densest equations explaining what the reader should be watching for.

### 3. Carry the “why this lane?” argument through the middle of the note

#### Problem
The opening and conclusion are stronger than the middle. The document still becomes dry in the technical center, where the approval case should be reinforced.

#### Needed fix
At key points in the body, remind the reader why the current technical construction matters for the lane choice.

#### Concrete chair-facing revision goal
The chair should not have to wait until Section 20 or the conclusion to remember why this lane is under consideration.

#### Where to reinforce
- after the Gaussian projection section;
- after the sparse-grid construction section;
- after the same-scalar contract section;
- after the worked example;
- after the innovation-score and propagation subsections.

#### What to say
Short reminders such as:
- why this construction helps define a deterministic scalar,
- why this matters for branch-conditioned differentiation,
- why this still differs from richer non-Gaussian lanes.

### 4. Make the report feel more like one lecture than several modules

#### Problem
The document still reads in places like a sequence of strong components rather than one unfolding argument.

#### Needed fix
Add stronger import/export transitions at major pivots.

#### Concrete chair-facing revision goal
The chair should feel that every section is a necessary next answer to the previous section’s unresolved question.

#### Priority transitions to strengthen
- Section 4 -> Section 5
- Section 6 -> Section 8
- Section 10 -> Section 11
- Section 13 -> Sections 14–16
- Section 18 -> Section 19 -> Section 20

#### What each bridge should do
Each bridge should say:
1. what was just established,
2. what remains unresolved,
3. why the next section is needed now.

### 5. Improve the approval tone without losing honesty

#### Problem
The note is now honest, but still occasionally so cautious that the positive case loses force.

#### Needed fix
Keep the non-claims, but phrase the positive scientific contribution more assertively where justified.

#### Concrete chair-facing revision goal
The chair should feel:
- “this report knows its limits,”
- but also
- “this is a serious and worthwhile lane, not merely a defensible compromise.”

#### Best places to tighten tone
- the end of Section 20,
- the opening paragraph of the conclusion,
- the strongest-suitability paragraph in the conclusion.

### 6. Preserve the worked example as the chair’s anchor

#### Problem
The worked example is one of the most helpful parts for the chair. It should become the recurring anchor for later dense sections.

#### Needed fix
Cross-reference the example more often in the gradient and comparison discussions.

#### Concrete chair-facing revision goal
The chair should be able to fall back on the worked example whenever the general derivation becomes abstract.

#### Where to cross-reference it
- factor derivative subsection,
- innovation score subsection,
- posterior sensitivity propagation subsection,
- Section 20 when discussing deterministic Gaussian-surrogate lanes.

## Approval threshold

The note will likely move from “close” to “approve” for a scientifically strong chair if these changes succeed in producing the following reaction:

> I understand the mathematical object being chosen, I understand why the nearby alternatives lose for this objective, I can follow the gradient argument without reconstructing it from scratch, and I believe this lane is worth approving as one serious method in the program.

## Summary

If only a few changes are made, the highest-priority chair-facing interventions are:

1. strengthen the mathematical comparison against the nearest deterministic Gaussian alternatives in Section 20;
2. add more pause-and-recap structure inside Section 13;
3. reinforce the “why this lane?” thread through the middle of the document;
4. improve transitions so the report reads like one argument rather than a sequence of modules.
