# P0 Failure Diagnosis And Acceptance Criteria Reset Plan

## Objective

Record why the prior high-dimensional nonlinear filtering block failed the
academic-artifact standard and reset acceptance criteria before any rewrite.

## Inputs

- Current chapters `ch33`--`ch37`.
- Prior scholarly-refinement execution result note.
- Current `docs/main.pdf` and LaTeX log.
- User diagnosis that BayesFilter evidence boxes and source-gap language are
  excessive for the main exposition.

## Work

1. Identify internal-audit content that should be moved to an implementation
   boundary note or appendix.
2. Identify method families currently treated too thinly.
3. Define the new paper-first gate: primary-source exposition, derivation,
   proposition/proof structure, algorithm, complexity, failure modes, synthesis.
4. Record that no subsequent phase may treat source-gap labels as final
   scholarship.

## Outputs

- P0 result note under the paper-first scholarship prefix.
- A concise rewrite target inventory by chapter and method family.
- A durable reset statement that chapter execution is blocked until P1 marks
  every phase-required source as `LOCAL_FULL_TEXT_CHECKED`; `LOCAL_SUMMARY_ONLY`,
  `METADATA_ONLY`, and abstract-level knowledge cannot support chapter
  mathematics or paper-specific derivations.

## Stop Conditions

- Stop if the user asks to preserve the existing compliance-first structure.
- Stop if the allowed write set would need production code or DPF lane changes.

## Verification

- `rg -n "BayesFilter Evidence|source-gap|blocker|What Is Not Concluded" docs/chapters/ch3*_highdim*.tex`
- `git diff --check`

## Allowed Writes

- `docs/plans/bayesfilter-highdim-nonlinear-filtering-paper-first-scholarship-*`

No chapter, bibliography, PDF, source-map, production, DPF, student-baseline, or
controlled-DPF edits are authorized by P0.

## What Must Not Be Concluded

P0 does not validate any paper or method.  It resets the standard only.
