# Phase 2 Subplan: Derivation And Chapter Reconciliation

Date: 2026-06-29

## Status

`DRAFT_PENDING_REVIEW`

## Phase Objective

Reconcile the reset memos, derivation note, and corrected chapter statements into
one reviewed mathematical boundary artifact so later code/test phases inherit a
consistent target description.

## Entry Conditions Inherited From Previous Phase

- Phase 1 contract is frozen and reviewed.
- The 2026-06-29 derivation note and corrected chapter sections exist.
- No code/test/benchmark classification phase has started yet.

## Required Artifacts

- Single-target contract:
  `docs/plans/bayesfilter-actual-sv-single-target-contract-2026-06-29.md`
- Derivation note:
  `docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md`
- Phase 2 result:
  `docs/plans/bayesfilter-actual-sv-single-target-phase2-derivation-chapter-reconciliation-result-2026-06-29.md`
- Refreshed Phase 3 subplan:
  `docs/plans/bayesfilter-actual-sv-single-target-phase3-code-test-benchmark-boundary-audit-subplan-2026-06-29.md`

## Required Checks/Tests/Reviews

Allowed local checks:

```bash
rg -n "same-target|wrong scalar|Gaussian-closure|surrogate scalar|not a same-target approximation|Zhao--Cui" docs/chapters/ch33_highdim_nonlinear_filtering_foundations.tex docs/chapters/ch35b_highdim_fixed_cloud_filtering_and_sgqf_validation.tex docs/chapters/ch28_nonlinear_ssm_validation.tex docs/plans/bayesfilter-highdim-actual-sv-single-target-corrected-derivation-note-2026-06-29.md
git diff --check -- docs/plans/bayesfilter-actual-sv-single-target-phase2-*.md
```

Claude review is required for:

- the Phase 2 result,
- the reconciled mathematical boundary summary inside that result,
- the Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the reset memos, derivation note, and corrected chapter statements now say the same thing about the actual-SV target and the status of Gaussian closure? |
| Baseline/comparator | 2026-06-28 single-target reset memo, 2026-06-29 derivation note, and corrected `ch33`, `ch35b`, and `ch28` sections. |
| Primary criterion | Phase 2 passes if every material statement is classified as governing, compatible, historical/diagnostic, or conflicting, and no unresolved contradiction remains. |
| Veto diagnostics | unresolved contradiction; chapter language that still implies co-equal actual-SV targets; derivation note overclaim beyond chapter wording; route-status ambiguity. |
| Explanatory diagnostics | grep hits and wording tables. |
| Not concluded | No code/test/benchmark classification, no route decision, no validation result. |
| Artifact | Phase 2 result and reviewed reconciliation table. |

## Forbidden Claims/Actions

- Do not allow chapter language to outrank the contract if it conflicts.
- Do not treat historical two-lane wording as live authority.
- Do not begin code/test/benchmark rewriting before reconciliation passes.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- the Phase 2 result records no unresolved governing contradiction;
- the reconciled status of each chapter/derivation artifact is explicit;
- the Phase 3 subplan exists and is reviewed.

## Stop Conditions

- A chapter and the contract disagree materially and cannot be reconciled safely.
- The derivation note and the chapter prose imply different target classes.
- Claude review does not converge after five rounds.

## End-Of-Phase Requirements

1. Run the local wording/reconciliation checks.
2. Write the Phase 2 result with a statement-classification table.
3. Refresh the Phase 3 subplan.
4. Review the reconciliation result and next subplan.
