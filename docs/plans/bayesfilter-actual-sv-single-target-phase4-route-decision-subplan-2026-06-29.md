# Phase 4 Subplan: Corrected Lane-B Route Decision

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Make one reviewed route decision for augmented-noise actual-SV inference under
the single-target rule:

1. a reviewed future artifact proves that a same-target augmented route exists
   and it survives as a distinct route,
2. any same-target augmented route collapses into an implementation variant of
   Lane A, or
3. augmented-lane inference is retired and only Lane A + Zhao--Cui remain
   inference-facing.

This phase must not presume at entry that a corrected same-target Lane B already
exists.

## Entry Conditions Inherited From Previous Phase

- Phase 3 route classification has passed.
- The single-target contract and route-inventory manifest are active authority.
- No same-target validation phase has started.

## Required Artifacts

- Phase 3 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-result-2026-06-29.md`
- Phase 4 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase4-route-decision-result-2026-06-29.md`
- Refreshed Phase 5 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase5-same-target-value-validation-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "same-target|wrong scalar|surrogate scalar|not exact transformed same-target admission|not direct actual-SV likelihood quadrature" bayesfilter/highdim/sv_mixture_cut4.py docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-phase4-*.md
```

Claude review is required for:

- the Phase 4 route decision result,
- the route-decision table,
- the Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Under the one-target contract, what is the reviewed status of augmented-noise actual-SV inference: same-target route proven and retained, implementation variant of Lane A, or retired inference lane? |
| Baseline/comparator | single-target contract, derivation note, reconciled chapters, and Phase 3 route manifest. |
| Primary criterion | Phase 4 passes only if one of the three route outcomes is chosen explicitly and justified from the scalar contract rather than from wrapper inertia. |
| Veto diagnostics | preserving an augmented inference lane merely because wrappers/tests already exist; same-target admission without reviewed derivation; route ambiguity after review. |
| Explanatory diagnostics | implementation complexity, code reuse, benchmark relevance, and surrogate utility. |
| Not concluded | No value pass, no gradient pass, and no same-target augmented implementation is presumed merely because this phase exists. |
| Artifact | Phase 4 route-decision result. |

## Forbidden Claims/Actions

- Do not assume or imply that a corrected same-target Lane B already exists.
- Do not use benchmark/test convenience as a reason to preserve an inference lane.
- Do not start validation work until the route decision is explicit.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- the route decision result is reviewed and explicit;
- the surviving same-target comparator set is named exactly;
- the Phase 5 subplan exists and is reviewed.

## Stop Conditions

- No reviewed route decision can be justified from the current derivation/contract.
- A new scalar contradiction is discovered that requires a reset memo.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run the local route-decision wording checks.
2. Write the Phase 4 route-decision result.
3. Refresh the Phase 5 subplan.
4. Review the route decision and next subplan.
